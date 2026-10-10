"""The ``bonbast`` command."""

from __future__ import annotations

import json
import time
from collections import deque
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

import click
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.text import Text

from . import render
from .catalog import ALL_CODES, COINS, CURRENCIES, GOLDS
from .client import BonbastClient, tehran_today
from .errors import BonbastError
from .models import Asset, Currency, Prices

console = Console()

CURRENCY = click.Choice([code.lower() for code in CURRENCIES], case_sensitive=False)
ANY_CODE = click.Choice([*(code.lower() for code in CURRENCIES), *COINS, *GOLDS], case_sensitive=False)
DATE = click.DateTime(formats=["%Y-%m-%d", "%Y/%m/%d"])


def _parse_codes(ctx: click.Context, param: click.Parameter, value: str | None) -> frozenset[str] | None:
    if not value:
        return None
    codes = {code.strip().strip("'\"").lower() for code in value.split(",")} - {""}
    unknown = sorted(codes - ALL_CODES)
    if unknown:
        raise click.BadParameter(f"unknown code(s) {', '.join(unknown)}. Valid codes: {', '.join(sorted(ALL_CODES))}")
    return frozenset(codes) or None


show_only_option = click.option(
    "--show-only",
    metavar="CODES",
    callback=_parse_codes,
    help="Only show these comma-separated codes, e.g. usd,eur,emami1,mithqal.",
)
interval_option = click.option(
    "-i",
    "--interval",
    type=click.IntRange(min=1),
    default=30,
    show_default=True,
    help="Seconds between refreshes. bonbast.com updates every 30 seconds.",
)
pretty_option = click.option("--pretty", is_flag=True, help="Indent and highlight the JSON.")
# Kept so existing scripts don't break; --pretty output is always fully expanded now.
expanded_option = click.option("--expanded", is_flag=True, hidden=True)

pass_client = click.make_pass_decorator(BonbastClient)


class _Group(click.Group):
    """Shows bonbast errors as a one-line message instead of a traceback."""

    def invoke(self, ctx: click.Context) -> Any:
        try:
            return super().invoke(ctx)
        except BonbastError as error:
            raise click.ClickException(str(error)) from error


@click.group(cls=_Group, invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(None, "-v", "--version", package_name="bonbast", message="%(version)s")
@show_only_option
@click.pass_context
def cli(ctx: click.Context, show_only: frozenset[str] | None) -> None:
    """Gold prices and Iranian Rial exchange rates from bonbast.com.

    Run without a command to show the current prices.
    """
    if not isinstance(ctx.obj, BonbastClient):
        ctx.obj = ctx.with_resource(BonbastClient())
    if ctx.invoked_subcommand is None:
        console.print(render.prices_view(_fetch(ctx.obj, show_only).valid()))


@cli.command()
@pretty_option
@expanded_option
@show_only_option
@pass_client
def export(client: BonbastClient, pretty: bool, expanded: bool, show_only: frozenset[str] | None) -> None:
    """Print the current prices as JSON."""
    _print_json(_fetch(client, show_only).to_dict(), pretty)


@cli.command()
@click.option("-d", "--date", "day", type=DATE, prompt=True, help="Gregorian date, as YYYY-MM-DD or YYYY/MM/DD.")
@click.option("--json", "as_json", is_flag=True, help="Print JSON instead of tables.")
@pretty_option
@expanded_option
@show_only_option
@pass_client
def history(
    client: BonbastClient,
    day: datetime,
    as_json: bool,
    pretty: bool,
    expanded: bool,
    show_only: frozenset[str] | None,
) -> None:
    """Show the prices of a past day, from 2012-10-09 to yesterday."""
    prices = client.history(day.date()).valid()
    if show_only:
        prices = prices.only(show_only)
    if as_json or pretty:
        _print_json(prices.to_dict(), pretty)
    else:
        console.print(render.prices_view(prices, title=f"Prices on {day:%Y-%m-%d}"))


@cli.command()
@click.argument("currency", type=CURRENCY, metavar="CURRENCY")
@click.option("--start-date", type=DATE, help="First day of the range. Defaults to 30 days before the end date.")
@click.option("--end-date", type=DATE, help="Last day of the range. Defaults to today.")
@click.option("--json", "as_json", is_flag=True, help='Print JSON, e.g. {"2024-01-31": 580000, ...}.')
@pass_client
def graph(
    client: BonbastClient,
    currency: str,
    start_date: datetime | None,
    end_date: datetime | None,
    as_json: bool,
) -> None:
    """Show the daily sell price of CURRENCY over a date range."""
    end = end_date.date() if end_date else tehran_today()
    start = start_date.date() if start_date else end - timedelta(days=30)
    points = client.graph(currency, start, end)
    if as_json:
        click.echo(json.dumps({day.isoformat(): price for day, price in points.items()}))
    else:
        console.print(render.graph_view(currency, points))


@cli.command()
@click.argument("amount", type=click.FloatRange(min=0))
@click.option("-s", "--source", type=CURRENCY, metavar="CURRENCY", help="Convert AMOUNT of this currency to Toman.")
@click.option("-d", "--destination", type=CURRENCY, metavar="CURRENCY", help="Convert AMOUNT Toman to this currency.")
@click.option("--only-buy", is_flag=True, help="Only print the result at the buy price.")
@click.option("--only-sell", is_flag=True, help="Only print the result at the sell price.")
@pass_client
def convert(
    client: BonbastClient,
    amount: float,
    source: str | None,
    destination: str | None,
    only_buy: bool,
    only_sell: bool,
) -> None:
    """Convert AMOUNT between Toman and a currency. Prints "buy / sell".

    \b
    Examples:
      bonbast convert -s eur 12.5      # 12.5 Euro in Toman
      bonbast convert -d usd 1837850   # 1,837,850 Toman in US Dollar
    """
    code = source or destination
    if code is None or (source and destination):
        raise click.UsageError("Use exactly one of --source and --destination.")
    if only_buy and only_sell:
        raise click.UsageError("--only-buy and --only-sell can't be used together.")

    currency = client.prices().get(code)
    if not isinstance(currency, Currency) or currency.buy is None or currency.sell is None:
        raise click.ClickException(f"bonbast.com has no price for {code.upper()} right now.")

    if source:
        units = amount / currency.quantity
        buy, sell = f"{round(units * currency.buy):,}", f"{round(units * currency.sell):,}"
    else:
        buy = render.format_amount(amount / currency.sell * currency.quantity)
        sell = render.format_amount(amount / currency.buy * currency.quantity)

    click.echo(buy if only_buy else sell if only_sell else f"{buy} / {sell}")


@cli.group(invoke_without_command=True)
@interval_option
@show_only_option
@click.pass_context
def live(ctx: click.Context, interval: int, show_only: frozenset[str] | None) -> None:
    """Keep prices on screen, refreshing them periodically.

    Without a subcommand, shows the full price tables. Prices that went up
    turn green and prices that went down turn red. Press Ctrl+C to stop.
    """
    if ctx.invoked_subcommand is not None:
        return
    client: BonbastClient = ctx.obj
    trends = render.TrendTracker()

    def update() -> RenderableType:
        prices = _fetch(client, show_only).valid()
        trends.update(prices)
        return Group(Text(f"{datetime.now():%Y-%m-%d %H:%M:%S}", style="bold"), render.prices_view(prices, trends))

    _live_loop(interval, update)


@live.command("simple")
@interval_option
@show_only_option
@pass_client
def live_simple(client: BonbastClient, interval: int, show_only: frozenset[str] | None) -> None:
    """Show prices as plain lines of text."""
    trends = render.TrendTracker()

    def update() -> RenderableType:
        prices = _fetch(client, show_only).valid()
        trends.update(prices)
        return render.simple_text(prices, trends, timestamp=datetime.now())

    _live_loop(interval, update)


@live.command("currency")
@click.argument("code", type=ANY_CODE, metavar="CODE")
@interval_option
@pass_client
def live_currency(client: BonbastClient, code: str, interval: int) -> None:
    """Track the price of one CODE, adding a row per refresh."""
    rows: deque[tuple[datetime, Asset, Asset | None]] = deque(maxlen=max(5, console.height - 6))
    previous: Asset | None = None

    def update() -> RenderableType:
        nonlocal previous
        asset = client.prices().get(code)
        if asset is None:
            raise BonbastError(f"bonbast.com did not return a price for {code}")
        rows.append((datetime.now(), asset, previous))
        previous = asset
        return render.ticker_table(rows)

    _live_loop(interval, update)


def _fetch(client: BonbastClient, show_only: frozenset[str] | None) -> Prices:
    prices = client.prices()
    return prices.only(show_only) if show_only else prices


def _print_json(data: dict[str, Any], pretty: bool) -> None:
    if pretty:
        console.print_json(data=data)
    else:
        click.echo(json.dumps(data, ensure_ascii=False))


def _live_loop(interval: int, update: Callable[[], RenderableType]) -> None:
    """Redraw ``update()`` every ``interval`` seconds until Ctrl+C, riding out failed refreshes."""
    view: RenderableType = Text("Loading…", style="dim")
    try:
        with Live(view, console=console, auto_refresh=False) as screen:
            while True:
                try:
                    view = update()
                    screen.update(view, refresh=True)
                except BonbastError as error:
                    message = Text(f"Refresh failed: {error}. Retrying in {interval}s.", style="red")
                    screen.update(Group(view, message), refresh=True)
                time.sleep(interval)
    except KeyboardInterrupt:
        pass
