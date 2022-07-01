import click
from rich.console import Console

try:
    from .__init__ import *
    from .server import *
    from .storage_manager import *
    from .tables import *
except:
    from __init__ import *
    from server import *
    from storage_manager import *
    from tables import *


def get_prices():
    # get token from storage
    # check if token's time and make sure it's not expired
    token, token_date = StorageManager().get_token()
    if token is not None:
        # token will expire in 10 minutes
        # if expired, delete it and get a new one
        if datetime.now() - token_date > timedelta(minutes=9, seconds=45):
            StorageManager().delete_token()
            return get_prices()
    else:
        # if we don't have a token, we will get it from the main page
        token = get_token_from_main_page()
        StorageManager().save_token(token, datetime.now())

    # get prices from the api with the token acquired from main page
    response = get_prices_from_api(token)
    if 'reset' in response:
        # if we got a reset response, delete the token and get a new one
        StorageManager().delete_token()
        return get_prices()
    else:
        return response


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    else:
        click.echo(bonbast_version)
        ctx.exit()


@click.group(invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        currencies_list, coins_list, golds_list = get_prices()

        currencies_table = get_currencies_table(currencies_list, 2)
        coins_table = get_coins_table(coins_list)
        gold_table = get_gold_table(golds_list)

        console = Console()
        console.print(currencies_table, coins_table, gold_table)


# @cli.command()
# def graph():
#     click.echo('Graph is not implemented yet')


# @cli.command()
# def live():
#     click.echo('Live is not implemented yet')


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


# @cli.command()
# def history():
#     click.echo('History is not implemented yet')


# @cli.command()
# def export():
#     click.echo('Export is not implemented yet')


if __name__ == '__main__':
    cli()
