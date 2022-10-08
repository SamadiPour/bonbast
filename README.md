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

Also, to update the program, you can use pip:

```shell
pip install -U bonbast
#or
python -m pip install -U bonbast
```

---

# Usage

I tried my best to display the price data in a variety of ways that would be useful in a variety of circumstances.

## Main mode

This will be the default mode if you run the program without any arguments. It will show the current prices for gold,
coins, and the IRR exchange rate in separate tables.

## Live

In live mode, the program tries to update the prices in a specified interval. This is useful if you want to keep an eye
on the prices.

The website updates the prices every 30 seconds and the default value is 30 seconds as well. You can change this value
by using the `-i` or `--interval` argument.

### Simple

In this mode, the program will show the prices as text in the terminal.

### Currency

In this mode, the program will show the prices in a table. It can only show one currency at a time.

## History

This is useful if you want to see the prices for a specific date. You can use the `-d` or `--date` argument to specify
the date. The date must be in the format `YYYY-MM-DD` or `YYYY/MM/DD`. Also, the date needs to be Gregorian.

## Convert

This is useful if you want to convert a value from one currency to Rial or from Rial to another currency.

If you want to convert from Rial to another currency, you need to use the `-d` or `--destination` argument to specify
the currency you want to convert to.

If you want to convert from a currency to Rial, you need to use `-s` or `--source` argument to specify the currency you
want to convert from.

## Json Output

It can be useful if you want to use the result of the program in another program. You can also pipe the output in
terminal to another program like `JQ`.

## List of supported currencies

| Flag |     Currency      | Code |
|:----:|:-----------------:|:----:|
| 🇺🇸 |     US Dollar     | USD  |
| 🇪🇺 |       Euro        | EUR  |
| 🇬🇧 |   British Pound   | GBP  |
| 🇨🇭 |    Swiss Franc    | CHF  |
| 🇨🇦 |  Canadian Dollar  | CAD  |
| 🇦🇺 | Australian Dollar | AUD  |
| 🇸🇪 |   Swedish Krona   | SEK  |
| 🇳🇴 |  Norwegian Krone  | NOK  |
| 🇷🇺 |   Russian Ruble   | RUB  |
| 🇹🇭 |     Thai Baht     | THB  |
| 🇸🇬 | Singapore Dollar  | SGD  |
| 🇭🇰 | Hong Kong Dollar  | HKD  |
| 🇦🇿 | Azerbaijani Manat | AZN  |
| 🇦🇲 | 10 Armenian Dram  | AMD  |
| 🇩🇰 |   Danish Krone    | DKK  |
| 🇦🇪 |    UAE Dirham     | AED  |
| 🇯🇵 |  10 Japanese Yen  | JPY  |
| 🇹🇷 |   Turkish Lira    | TRY  |
| 🇨🇳 |   Chinese Yuan    | CNY  |
| 🇸🇦 |    Saudi Riyal    | SAR  |
| 🇮🇳 |   Indian Rupee    | INR  |
| 🇲🇾 | Malaysian Ringgit | MYR  |
| 🇦🇫 |  Afghan Afghani   | AFN  |
| 🇰🇼 |   Kuwaiti Dinar   | KWD  |
| 🇮🇶 |  100 Iraqi Dinar  | IQD  |
| 🇧🇭 |  Bahraini Dinar   | BHD  |
| 🇴🇲 |    Omani Rial     | OMR  |
| 🇶🇦 |    Qatari Rial    | QAR  |

---

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
