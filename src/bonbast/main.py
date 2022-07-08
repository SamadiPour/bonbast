import json

from rich.console import Console
from rich.pretty import pprint

try:
    from .utils import *
    from .models import *
    from .server import *
    from .tables import *
    from .managers.token_manager import *
    from .managers.storage_manager import *
    from .click_helper.callbacks import *
except ImportError:
    from utils import *
    from models import *
    from server import *
    from tables import *
    from managers.token_manager import *
    from managers.storage_manager import *
    from click_helper.callbacks import *


@retry(message='Error: token is expired. Try again later.')
def get_prices(show_only: List[str] = None):
    token = token_manager.generate()
    try:
        response = get_prices_from_api(token.value)
        if show_only is not None and len(show_only) > 0:
            response = list(response)
            for index, item in enumerate(response):
                response[index] = [item for item in item if item.code.lower() in show_only]
            response = tuple(response)

        return response
    except ResetAPIError as e:
        token_manager.invalidate_token()
        raise e


@click.group(invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option(
    '--show-only',
    help='Show only specified currencies, coins, or golds (separated by comma)',
    callback=parse_show_only
)
@click.pass_context
def cli(ctx, show_only):
    if ctx.invoked_subcommand is None:
        currencies_list, coins_list, golds_list = get_prices(show_only)
        console = Console()

        if currencies_list is not None and len(currencies_list) > 0:
            console.print(get_currencies_table(currencies_list, columns=2))

        if coins_list is not None and len(coins_list) > 0:
            console.print(get_coins_table(coins_list))

        if golds_list is not None and len(golds_list) > 0:
            console.print(get_gold_table(golds_list))


# @cli.command()
# def graph():
#     click_helper.echo('Graph is not implemented yet')


@cli.group(invoke_without_command=True)
@click.pass_context
def live(ctx):
    if ctx.invoked_subcommand is None:
        print('Show full table with live prices / up and down arrows')
    pass


@live.command('graph')
def live_graph():
    print('show graph updating live every x seconds')
    pass


@live.command('simple')
def live_table():
    print('show each currency in separate line with live prices')
    pass


@live.command('currency')
def live_currency():
    print('show one currency in table with date / live prices')
    pass


@cli.command()
@click.option('-s', '--source', type=click.Choice(Currency.VALUES, case_sensitive=False))
@click.option('-d', '--destination', type=click.Choice(Currency.VALUES, case_sensitive=False))
@click.argument('amount', type=click.FLOAT)
@click.option('--only-buy', is_flag=True, default=False, help='Only show buy price')
@click.option('--only-sell', is_flag=True, default=False, help='Only show sell price')
@click.pass_context
def convert(ctx, source, destination, amount, only_buy, only_sell):
    if source is None and destination is None:
        raise click.BadOptionUsage('', 'Please specify source or destination currency')

    if source is not None and destination is not None:
        raise click.BadOptionUsage('', 'Don\'t use --source and --destination together')

    if only_buy and only_sell:
        raise click.BadOptionUsage('', 'Don\'t use --only-buy and --only-sell together')

    currencies_list, _, __ = get_prices()
    if source is not None:
        currency = next(currency for currency in currencies_list if currency.code.lower() == source.lower())
        buy = format_toman(int(amount * currency.buy))
        sell = format_toman(int(amount * currency.sell))
    else:
        currency = next(currency for currency in currencies_list if currency.code.lower() == destination.lower())
        buy = format_price(amount / currency.sell)
        sell = format_price(amount / currency.buy)

    if only_buy:
        click.echo(buy)
    elif only_sell:
        click.echo(sell)
    else:
        click.echo(f'{buy} / {sell}')


@cli.command()
@click.option(
    '--date',
    type=click.DateTime(formats=["%Y/%m/%d", '%Y-%m-%d']),
    prompt=True,
    help='Date to get prices for'
)
def history(date):
    currencies = get_history(date)
    console = Console()
    console.print(get_currencies_table(currencies, 2))


@cli.command()
@click.option('--pretty', is_flag=True, default=False, help='Pretty print the output')
@click.option('--expanded', is_flag=True, default=False, help='Tries to expand the JSON')
@click.option(
    '--show-only',
    help='Show only specified currencies, coins, or golds (separated by comma)',
    callback=parse_show_only,
)
def export(pretty, expanded, show_only):
    items = get_prices(show_only)
    prices = {}
    for item in items:
        for model in item:
            prices.update(model.to_json())

    if pretty:
        pprint(prices, expand_all=expanded)
    else:
        click.echo(json.dumps(prices, ensure_ascii=False))


if __name__ == '__main__':
    cli()
