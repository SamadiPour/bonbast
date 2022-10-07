# Bonbast

[bonbast.com](https://bonbast.com) offers accurate and reliable gold prices and IRR exchange rates for businesses.
Bonbast is the most accurate and reputable foreign exchange trading data collector of the Iranian market.

I don't alter any of the data in this tool; it all comes from bonbast. The sole purpose of this tool is to offer a
different method of obtaining bonbast prices.

## Installation

To install this program, you can to use pip:

```shell
$ pip install bonbast
# Or
$ python -m pip install bonbast
```

Then you can use it:

```shell
$ bonbast
# Or
$ python -m bonbast
```


# Development

## Setup

1. Clone the repo
2. Install the dependencies
3. Run it with python

```shell
git clone https://github.com/SamadiPour/bonbast.git
cd bonbast
pip install .
python -m src.bonbast.main
```

## Building the package

1. Install build dependencies
2. Build the package
3. install it locally if you want (or you can use `local_install` script)

```shell
python -m pip install ".[build]"
python -m build
python -m pip install dist/*.whl
```
