from rich.live import Live
from rich.text import Text

try:
    from .models import *
    from .server import *
    from .tables import *
    from .managers.token_manager import *
    from .managers.storage_manager import *
    from .helpers.click_callbacks import *
    from .helpers.utils import *
except ImportError:
    from models import *
    from server import *
    from tables import *
    from managers.token_manager import *
    from managers.storage_manager import *
    from helpers.click_callbacks import *
    from helpers.utils import *


@retry(message='Error: The operation failed for an unknown reason.')
def get_prices(show_only: List[str] = None):
    """
    Retrieves prices for currencies, coins, and golds, optionally filtered by a list of codes.

    :param show_only: Optional list of codes to filter the results.
    :return: Tuple of lists containing currencies, coins, and golds.
    """
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
    """
    Main CLI group function to handle the base command and options.

    :param ctx: Click context.
    :param show_only: Filter for showing only specified currencies, coins, or golds.
    """
    if ctx.invoked_subcommand is None:
        currencies_list, coins_list, golds_list = get_prices(show_only)
        currencies_list, coins_list, golds_list = filter_valids(currencies_list, coins_list, golds_list)

        currency_table = get_currencies_table(currencies_list, columns=2)
        coin_table = get_coins_table(coins_list)
        gold_table = get_gold_table(golds_list)

        print_tables(currency_table, coin_table, gold_table)


@cli.command()
@click.argument('currency', type=click.Choice(Currency.VALUES.keys(), case_sensitive=False))
@click.option(
    '--start-date',
    type=click.DateTime(formats=["%Y    /%m/%d", '%Y-%m-%d']),
    prompt=False,
    help='Start Date for the range. If not specified, it will default to a 30-day period from the end date.'
)
@click.option(
    '--end-date',
    type=click.DateTime(formats=["%Y/%m/%d", '%Y-%m-%d']),
    prompt=False,
    help='End Date for the range. If not specified, it will default to today.'
)
def graph(currency, start_date, end_date):
    """
    CLI command to display graph data for a specified currency over a date range.

    :param currency: The currency code.
    :param start_date: The start date for the range.
    :param end_date: The end date for the range.
    """
    end_date = end_date or datetime.today()
    start_date = start_date or end_date - timedelta(days=30)

    if end_date <= start_date:
        raise click.BadOptionUsage('', 'End date can\'t be the same or before the start date.')

    result = get_graph_data(currency.lower(), start_date, end_date)
    for date, rate in result.items():
        click.echo(f'{date.date()}: {rate}')
    pass


@cli.group(invoke_without_command=True)
@click.pass_context
def live(ctx):
    """
    CLI group command to handle live data commands.

    :param ctx: Click context.
    """
    if ctx.invoked_subcommand is None:
        print('Show full table with live prices / up and down arrows')
    pass


@live.command('simple')
@click.option('-i', '--interval', type=click.IntRange(min=1), default=30, help='Interval in seconds')
@click.option(
    '--show-only',
    help='Show only specified currencies, coins, or golds (separated by comma)',
    callback=parse_show_only,
)
def live_simple(interval, show_only):
    """
    CLI command to display live simple text data for currencies, coins, or golds.

    :param interval: The refresh interval in seconds.
    :param show_only: Filter for showing only specified currencies, coins, or golds.
    """
    old_collections = (None, None, None)
    with Live(auto_refresh=False) as live:
        while True:
            collections = get_prices(show_only)

            prices_text = Text()
            prices_text.append(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n', style='bold')

            for collection_index, collection in enumerate(collections):
                for index, model in enumerate(collection):
                    old_collection = old_collections[collection_index]
                    if old_collection is not None \
                            and len(old_collection) > index \
                            and old_collection[index].code == model.code:
                        old_model = old_collection[index]
                    else:
                        old_model = None

                    prices_text.append(model.assemble_simple_text(old_model))

            prices_text.rstrip()
            live.update(prices_text, refresh=True)
            old_collections = collections
            time.sleep(interval)


@live.command('currency')
@click.option('-i', '--interval', type=click.IntRange(min=1), default=30, help='Interval in seconds')
@click.argument(
    'currency', nargs=1,
    type=click.Choice(
        list(Currency.VALUES.keys()) + list(Gold.VALUES.keys()) + list(Coin.VALUES.keys()), case_sensitive=False
    )
)
def live_currency(interval, currency):
    """
    CLI command to display live data for a specific currency, coin, or gold.

    :param interval: The refresh interval in seconds.
    :param currency: The currency, coin, or gold code.
    """
    table = Table()
    first_time = True
    old_model = None
    with Live(table, auto_refresh=False) as live:
        while True:
            # request to get all the currencies
            collections = get_prices([currency])

            # flatten the list of currencies and get the first element
            items = (item for collection in collections for item in collection)
            item = next(items)

            # if it's the first time, add the header
            if first_time:
                table.add_column("Date", no_wrap=True)
                table.add_column("Name", no_wrap=True)
                if type(item) is Currency or type(item) is Coin:
                    table.add_column("Sell", no_wrap=True)
                    table.add_column("Buy", no_wrap=True)
                else:
                    table.add_column("Price", no_wrap=True)

                first_time = False

            # add a row with the new information
            if type(item) is Currency or type(item) is Coin:
                sell_symbol = f' {get_change_char(item.sell, old_model.sell)}' if old_model is not None else ''
                sell_str = (item.formatted_sell if item.sell is not None else '-') + sell_symbol
                sell_color = get_color(item.sell, None if old_model is None else old_model.sell)

                buy_symbol = f' {get_change_char(item.buy, old_model.buy)}' if old_model is not None else ''
                buy_str = (item.formatted_buy if item.buy is not None else '-') + buy_symbol
                buy_color = get_color(item.buy, None if old_model is None else old_model.buy)

                price = (
                    Text(sell_str, style=sell_color),
                    Text(buy_str, style=buy_color),
                )
            else:
                price_char = f' {get_change_char(item.price, old_model.price)}' if old_model is not None else ''
                price_str = (item.formatted_price if item.price is not None else '-') + price_char
                price_color = get_color(item.price, None if old_model is None else old_model.price)

                price = (
                    Text(price_str, style=price_color),
                )

            table.add_row(
                Text(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style=DEFAULT_TEXT_COLOR),
                Text(item.name, style=DEFAULT_TEXT_COLOR),
                *price,
            )

            live.update(table, refresh=True)
            old_model = item
            time.sleep(interval)


@cli.command()
@click.option('-s', '--source', type=click.Choice(Currency.VALUES, case_sensitive=False))
@click.option('-d', '--destination', type=click.Choice(Currency.VALUES, case_sensitive=False))
@click.argument('amount', type=click.FLOAT)
@click.option('--only-buy', is_flag=True, default=False, help='Only show buy price')
@click.option('--only-sell', is_flag=True, default=False, help='Only show sell price')
@click.pass_context
def convert(ctx, source, destination, amount, only_buy, only_sell):
    """
    CLI command to convert an amount from one currency to another.

    :param ctx: Click context.
    :param source: Source currency code.
    :param destination: Destination currency code.
    :param amount: Amount to convert.
    :param only_buy: Flag to show only buy price.
    :param only_sell: Flag to show only sell price.
    """
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
@click.option('--json', 'is_json', is_flag=True, default=False, help='Output in JSON format')
@click.option('--pretty', is_flag=True, default=False, help='Pretty print the output')
@click.option('--expanded', is_flag=True, default=False, help='Tries to expand the JSON')
def history(date, is_json, pretty, expanded):
    """
    CLI command to display historical prices for a specific date.

    :param date: The date for which to retrieve prices.
    :param is_json: Flag to output in JSON format.
    :param pretty: Flag for pretty printing the output.
    :param expanded: Flag to expand all fields in the output.
    """
    currencies_list, coins_list = get_history(date)
    currencies_list, coins_list = filter_valids(currencies_list, coins_list)

    if not is_json:
        currency_table = get_currencies_table(currencies_list, columns=2)
        coin_table = get_coins_table(coins_list)
        print_tables(currency_table, coin_table)
    else:
        print_json(currencies_list, coins_list, pretty=pretty, expanded=expanded)


@cli.command()
@click.option('--pretty', is_flag=True, default=False, help='Pretty print the output')
@click.option('--expanded', is_flag=True, default=False, help='Tries to expand the JSON')
@click.option(
    '--show-only',
    help='Show only specified currencies, coins, or golds (separated by comma)',
    callback=parse_show_only,
)
def export(pretty, expanded, show_only):
    """
    CLI command to export current prices to JSON format.

    :param pretty: Flag for pretty printing the output.
    :param expanded: Flag to expand all fields in the output.
    :param show_only: Filter for showing only specified currencies, coins, or golds.
    """
    currencies_list, coins_list, golds_list = get_prices(show_only)
    print_json(currencies_list, coins_list, golds_list, pretty=pretty, expanded=expanded)


if __name__ == '__main__':
    cli()
