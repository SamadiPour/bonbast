# Bonbast

[bonbast.com](https://bonbast.com) offers accurate and reliable gold prices and IRR exchange rates for businesses.
Bonbast is the most accurate and reputable foreign exchange trading data collector of the Iranian market.

I don't alter any of the data in this tool; it all comes from bonbast. The sole purpose of this tool is to offer a
different method of obtaining bonbast prices.

## Contents
1. [Installation](#installation)
   * [Brew](#brew)
   * [Python](#python)
   * [Raycast](#setup-for-raycast)
2. [Usage](#usage)
   1. [Command Line](#command-line)
      * [Main mode](#main-mode)
      * [Live](#live)
      * [Simple](#simple)
      * [Currency](#currency)
      * [History](#history)
      * [Convert](#convert)
      * [Json Output](#json-output)
      * [Pretty Print Json](#pretty-print-json)
      * [List of supported currencies](#list-of-supported-currencies)
   2. [Usage in other programs](#usage-in-other-programs)
   3. [Mac Shortcuts](#mac-shortcuts)
   4. [Raycast](#raycast)
3. [Development](#development)

## Installation

### Brew

```
brew install samadipour/bonbast/bonbast
```

or

```
brew tap samadipour/bonbast
brew update
brew install bonbast
```

### Python

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

## Usage

I tried my best to display the price data in a variety of ways that would be useful in a variety of circumstances.

### Command Line

#### Main mode

This will be the default mode if you run the program without any arguments. It will show the current prices for gold,
coins, and the IRR exchange rate in separate tables.

![bonbast](https://user-images.githubusercontent.com/24422125/194708514-e7b76a69-0671-4a6c-a025-51f29558f087.png)

#### Live

In live mode, the program tries to update the prices in a specified interval. This is useful if you want to keep an eye
on the prices.

The website updates the prices every 30 seconds and the default value is 30 seconds as well. You can change this value
by using the `-i` or `--interval` argument.

```shell
$ bonbast -i 60
# Or
$ python -m bonbast -i 60
```

#### Simple

In this mode, the program will show the prices as text in the terminal.

```shell
$ bonbast live simple --show-only usd,eur,gbp,cad -i 300
# Or
$ python -m bonbast live simple --show-only usd,eur,gbp,cad -i 300
```

![bonbast_live_simple](https://user-images.githubusercontent.com/24422125/194708537-09f98a47-a6b2-4489-a106-9bf22db6d527.png)

#### Currency

In this mode, the program will show the prices in a table. It can only show one currency at a time.

```shell
$ bonbast live currency --show-only usd,eur,gbp,cad -i 300
# Or
$ python -m bonbast live currency --show-only usd,eur,gbp,cad -i 300
```

![bonbast_live_currency](https://user-images.githubusercontent.com/24422125/194708542-241d2e11-35ec-4868-91ec-30ff7ca5e6e0.png)

#### History

This is useful if you want to see the prices for a specific date. You can use the `-d` or `--date` argument to specify
the date. The date must be in the format `YYYY-MM-DD` or `YYYY/MM/DD`. Also, the date needs to be Gregorian.

The date is valid from 2012-10-09 to one day before the current date.

```shell
$ bonbast history --date 2020/10/10
# Or
$ python -m bonbast history --date 2020/10/10
```

![bonbast_history](https://user-images.githubusercontent.com/24422125/194708555-fb5ada09-8e74-497d-8b61-74f27dea9220.png)

#### Convert

This is useful if you want to convert a value from one currency to Rial or from Rial to another currency.
If you want to convert from a currency to Rial, you need to use `-s` or `--source` argument to specify the currency you
want to convert from.

```shell
$ bonbast convert -s EUR 12.5
# Or
$ python -m bonbast convert -s EUR 12.5
```

If you want to convert from Rial to another currency, you need to use the `-d` or `--destination` argument to specify
the currency you want to convert to.

```shell
$ bonbast convert -d USD 1837850
# Or
$ python -m bonbast convert -d USD 1837850
```

You can also use `--only-buy` or `--only-sell` to specify which price you want to use.

```shell
$ bonbast convert -d USD 1837850 --only-buy
$ bonbast convert -d USD 1837850 --only-sell
# Or
$ python -m bonbast convert -d USD 1837850 --only-buy
$ python -m bonbast convert -d USD 1837850 --only-sell
```

![bonbast_convert](https://user-images.githubusercontent.com/24422125/194708562-38f9f08c-9bc7-41d0-9889-04f38007b7f3.png)

#### Json Output

It can be useful if you want to use the result of the program in another program. You can also pipe the output in
terminal to another program like `JQ`.

```shell
$ bonbast export
# Or
$ python -m bonbast export
```

![bonbast_export](https://user-images.githubusercontent.com/24422125/194708575-58fc19a5-9aa9-4e6d-b020-a40835d9d55d.png)

#### Pretty Print Json

There is also a way to pretty print the json output. You can use the `--pretty` argument to do that. It helps to see the
output in a more readable way.

```shell
$ bonbast export --pretty
# Or
$ python -m bonbast export --pretty
```
![bonbast_export_pretty](https://user-images.githubusercontent.com/24422125/194708592-471a189b-e3f4-4a29-b36c-ad536d93822e.png)

#### List of supported currencies

| Flag | Currency          | Code |
|:----:|-------------------|:----:|
| 🇺🇸 | US Dollar         | USD  |
| 🇪🇺 | Euro              | EUR  |
| 🇬🇧 | British Pound     | GBP  |
| 🇨🇭 | Swiss Franc       | CHF  |
| 🇨🇦 | Canadian Dollar   | CAD  |
| 🇦🇺 | Australian Dollar | AUD  |
| 🇸🇪 | Swedish Krona     | SEK  |
| 🇳🇴 | Norwegian Krone   | NOK  |
| 🇷🇺 | Russian Ruble     | RUB  |
| 🇹🇭 | Thai Baht         | THB  |
| 🇸🇬 | Singapore Dollar  | SGD  |
| 🇭🇰 | Hong Kong Dollar  | HKD  |
| 🇦🇿 | Azerbaijani Manat | AZN  |
| 🇦🇲 | 10 Armenian Dram  | AMD  |
| 🇩🇰 | Danish Krone      | DKK  |
| 🇦🇪 | UAE Dirham        | AED  |
| 🇯🇵 | 10 Japanese Yen   | JPY  |
| 🇹🇷 | Turkish Lira      | TRY  |
| 🇨🇳 | Chinese Yuan      | CNY  |
| 🇸🇦 | Saudi Riyal       | SAR  |
| 🇮🇳 | Indian Rupee      | INR  |
| 🇲🇾 | Malaysian Ringgit | MYR  |
| 🇦🇫 | Afghan Afghani    | AFN  |
| 🇰🇼 | Kuwaiti Dinar     | KWD  |
| 🇮🇶 | 100 Iraqi Dinar   | IQD  |
| 🇧🇭 | Bahraini Dinar    | BHD  |
| 🇴🇲 | Omani Rial        | OMR  |
| 🇶🇦 | Qatari Rial       | QAR  |

---

### Usage in other programs

There are few ways to use the program in other programs. The best way is to use the json output.

### Mac Shortcuts

You can use the json output or the convert function to create a shortcut in Mac. You can use the shortcut to show the
currency price as a notification.

### [Raycast](https://www.raycast.com/)

Raycast is a tool for searching your Mac, launching applications, and controlling your computer, and it is far superior
to Spotlight. You can use the json output to create a script command in Raycast. In this way, you can easily access the
prices in Raycast.

I included an example script command in the `raycast` folder. You can use it to create your own script.

![bonbast_raycast](https://user-images.githubusercontent.com/24422125/194708612-a5f5557c-aab3-4ded-b500-9e08b594949c.png)

#### Setup for Raycast

You can use this [setup-raycast.sh](./raycast_script/setup-raycast.sh) script to setup the script command in Raycast. Then Follow the instructions in below image or read Raycast docs.

```shell
$ chmod +x setup-raycast.sh

$ ./setup-raycast.sh standalone
or
$ ./setup-raycast.sh python
```

or manually:

1. Enable the script command in Raycast.
2. Copy [bonbast.sh](./raycast_script/bonbast.sh) file to the Raycast `script-commands` folder.
3. Follow the instructions below or read Raycast docs.

![raycast-setup](https://github.com/SamadiPour/bonbast/blob/master/.github/setup-raycast.png?raw=true)

---

## Development

### Setup

1. Clone the repo
2. Install the dependencies
3. Run it with python

```shell
git clone https://github.com/SamadiPour/bonbast.git
cd bonbast
pip install .
python -m src.bonbast.main
```

### Building the package

1. Install build dependencies
2. Build the package
3. install it locally if you want (or you can use `local_install` script)

```shell
python -m pip install ".[build]"
python -m build
python -m pip install dist/*.whl
```
