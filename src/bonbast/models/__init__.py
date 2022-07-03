try:
    from .coin import Coin
    from .gold import Gold
    from .graph import Graph
    from .currency import Currency
except:  # noqa
    from coin import Coin
    from gold import Gold
    from graph import Graph
    from currency import Currency
