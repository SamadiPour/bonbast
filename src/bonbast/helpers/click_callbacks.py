import click

try:
    from ..__init__ import *
except ImportError:
    from src.bonbast.__init__ import *


def print_version(ctx, param, value):
    """
    Prints the version of the bonbast package.

    :param ctx: Click context.
    :param param: The command line parameter.
    :param value: The value of the parameter.
    """
    if not value or ctx.resilient_parsing:
        return
    else:
        click.echo(bonbast_version)
        ctx.exit()


def parse_show_only(ctx, param, value):
    """
    Parses the --show-only option from the command line.

    :param ctx: Click context.
    :param param: The command line parameter.
    :param value: The value of the parameter.
    :return: A list of items to show only.
    """
    if value is not None and value != '':
        if value[0] == '\'' and value[-1] == '\'':
            value = value[1:-1]
        value = value.split(',')
        return [item.lower().strip() for item in value]
