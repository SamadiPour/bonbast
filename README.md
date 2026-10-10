# Bonbast

[bonbast.com](https://bonbast.com) publishes accurate and reliable gold prices and Iranian Rial (IRR) exchange rates.
Bonbast is the most accurate and reputable collector of foreign exchange data for the Iranian market.

This tool doesn't alter any of the data; it all comes from bonbast. Its only purpose is to give you a different way to
get bonbast prices: in your terminal, as JSON for other programs, or from Python.

All prices are in **Toman** (1 Toman = 10 Rials), except Gold Ounce and Bitcoin, which are in US Dollars.

## Contents

1. [Installation](#installation)
2. [Usage](#usage)
   * [Current prices](#current-prices)
   * [Live](#live)
   * [History](#history)
   * [Graph](#graph)
   * [Convert](#convert)
   * [JSON output](#json-output)
   * [Supported codes](#supported-codes)
3. [Usage in other programs](#usage-in-other-programs)
   * [Python](#python)
   * [Mac Shortcuts](#mac-shortcuts)
   * [Raycast](#raycast)
4. [Development](#development)

## Installation

Bonbast needs Python 3.10 or newer.

### uv / pipx

```shell
uv tool install bonbast
# or
pipx install bonbast
```

### pip

```shell
python -m pip install bonbast
```

To update, run `uv tool upgrade bonbast`, `pipx upgrade bonbast` or `python -m pip install -U bonbast`.

### Homebrew

```shell
brew install samadipour/bonbast/bonbast
```

### Arch Linux (AUR)

Use any AUR helper, such as [yay](https://github.com/Jguer/yay) or [paru](https://github.com/Morganamilo/paru):

```shell
yay -S python-bonbast
```

or build the [package](https://aur.archlinux.org/packages/python-bonbast/) manually:

```shell
git clone https://aur.archlinux.org/python-bonbast.git
cd python-bonbast
makepkg -si
```

---

## Usage

Run `bonbast --help`, or `bonbast <command> --help`, to see every option. `python -m bonbast` works too.

### Current prices

Running `bonbast` without a command shows the current prices of currencies, coins and gold in separate tables.

```shell
bonbast
bonbast --show-only usd,eur,emami1,mithqal
```

![bonbast](https://user-images.githubusercontent.com/24422125/194708514-e7b76a69-0671-4a6c-a025-51f29558f087.png)

### Live

Live mode keeps the prices on screen and refreshes them periodically. Prices that went up turn green with a `↑`,
prices that went down turn red with a `↓`. Press `Ctrl+C` to stop.

bonbast.com updates its prices every 30 seconds, which is also the default interval. Change it with `-i` / `--interval`.

```shell
# The full tables
bonbast live --show-only usd,eur,gbp,azadi1 -i 60
```

#### Simple

Shows the prices as lines of text.

```shell
bonbast live simple --show-only usd,eur,gbp,cad -i 300
```

![bonbast_live_simple](https://user-images.githubusercontent.com/24422125/194708537-09f98a47-a6b2-4489-a106-9bf22db6d527.png)

#### Currency

Tracks a single currency, coin or gold price and adds a row on every refresh.

```shell
bonbast live currency usd -i 300
```

![bonbast_live_currency](https://user-images.githubusercontent.com/24422125/194708542-241d2e11-35ec-4868-91ec-30ff7ca5e6e0.png)

### History

Shows the currency and coin prices of a past day. Pass a Gregorian date as `YYYY-MM-DD` or `YYYY/MM/DD` with `-d` /
`--date`. bonbast has data from 2012-10-09 up to yesterday.

```shell
bonbast history --date 2020/10/10
bonbast history --date 2020-10-10 --show-only usd,eur
bonbast history --date 2020-10-10 --json
```

![bonbast_history](https://user-images.githubusercontent.com/24422125/194708555-fb5ada09-8e74-497d-8b61-74f27dea9220.png)

### Graph

Shows the daily sell price of a currency over a date range, with a bar for each day and a summary (low, high, average
and change). Both ends of the range are included.

Without `--end-date`, the range ends today. Without `--start-date`, it starts 30 days before the end date.

```shell
bonbast graph eur
bonbast graph eur --start-date 2023-01-02
bonbast graph eur --start-date 2023-02-12 --end-date 2023-05-09
bonbast graph eur --json   # {"2023-02-12": 590000, ...}
```

![bonbast_graph](https://github.com/user-attachments/assets/a4d48a1a-3b2a-4db9-8ef6-9aae49dfd4fe)

### Convert

Converts an amount of a currency to Toman with `-s` / `--source`:

```shell
bonbast convert -s eur 12.5
```

or an amount of Toman to a currency with `-d` / `--destination`:

```shell
bonbast convert -d usd 1837850
```

The output is `buy / sell`. Use `--only-buy` or `--only-sell` to print only one of them.

```shell
bonbast convert -d usd 1837850 --only-buy
```

![bonbast_convert](https://user-images.githubusercontent.com/24422125/194708562-38f9f08c-9bc7-41d0-9889-04f38007b7f3.png)

### JSON output

`export` prints the current prices as JSON, to use in other programs or to pipe into tools like `jq`. Add `--pretty`
for indented, highlighted output.

```shell
bonbast export
bonbast export --pretty --show-only usd,emami1,mithqal
bonbast export | jq .USD.sell
```

```json
{
  "USD": {"name": "US Dollar", "sell": 269300, "buy": 269200},
  "emami1": {"name": "Emami", "sell": 271000000, "buy": 267000000},
  "mithqal": {"name": "Gold Mithqal", "price": 114370000}
}
```

`history --json` prints the same format.

### Supported codes

Use these codes with `--show-only` (comma separated), `live currency`, `graph`, `convert` and as keys in the JSON
output. Codes are case-insensitive.

<details>
<summary>Currencies</summary>

| Flag | Currency          | Code |
|:----:|-------------------|:----:|
|  🇺🇸  | US Dollar         | USD  |
|  🇪🇺  | Euro              | EUR  |
|  🇬🇧  | British Pound     | GBP  |
|  🇨🇭  | Swiss Franc       | CHF  |
|  🇨🇦  | Canadian Dollar   | CAD  |
|  🇦🇺  | Australian Dollar | AUD  |
|  🇸🇪  | Swedish Krona     | SEK  |
|  🇳🇴  | Norwegian Krone   | NOK  |
|  🇷🇺  | Russian Ruble     | RUB  |
|  🇹🇭  | Thai Baht         | THB  |
|  🇸🇬  | Singapore Dollar  | SGD  |
|  🇭🇰  | Hong Kong Dollar  | HKD  |
|  🇦🇿  | Azerbaijani Manat | AZN  |
|  🇦🇲  | 10 Armenian Dram  | AMD  |
|  🇩🇰  | Danish Krone      | DKK  |
|  🇦🇪  | UAE Dirham        | AED  |
|  🇯🇵  | 10 Japanese Yen   | JPY  |
|  🇹🇷  | Turkish Lira      | TRY  |
|  🇨🇳  | Chinese Yuan      | CNY  |
|  🇸🇦  | Saudi Riyal       | SAR  |
|  🇮🇳  | Indian Rupee      | INR  |
|  🇲🇾  | Malaysian Ringgit | MYR  |
|  🇦🇫  | Afghan Afghani    | AFN  |
|  🇰🇼  | Kuwaiti Dinar     | KWD  |
|  🇮🇶  | 100 Iraqi Dinar   | IQD  |
|  🇧🇭  | Bahraini Dinar    | BHD  |
|  🇴🇲  | Omani Rial        | OMR  |
|  🇶🇦  | Qatari Riyal      | QAR  |

bonbast quotes AMD and JPY per 10 units and IQD per 100 units. `convert` takes that into account.

</details>

<details>
<summary>Coins</summary>

| Coin    | Code     |
|---------|----------|
| Emami   | emami1   |
| Gerami  | azadi1g  |
| Azadi   | azadi1   |
| ½ Azadi | azadi1_2 |
| ¼ Azadi | azadi1_4 |

</details>

<details>
<summary>Gold</summary>

| Name         | Code    | Unit  |
|--------------|---------|-------|
| Gold Mithqal | mithqal | Toman |
| Gold Gram    | gol18   | Toman |
| Gold Ounce   | ounce   | USD   |
| Bitcoin      | bitcoin | USD   |

</details>

---

## Usage in other programs

The JSON output is the easiest way to use the prices in another program.

### Python

bonbast can also be used as a library:

```python
from datetime import date

from bonbast import BonbastClient

with BonbastClient() as client:
    prices = client.prices()
    usd = prices.get("usd")
    print(usd.sell, usd.buy)

    for coin in prices.coins:
        print(coin.name, coin.sell)

    old = client.history(date(2020, 10, 10))
    chart = client.graph("eur", date(2023, 1, 1), date(2023, 1, 31))  # {date: sell price}
```

Errors are raised as `bonbast.BonbastError` subclasses: `NetworkError`, `ParseError` and `InvalidDateError`.

### Mac Shortcuts

Use the JSON output or the `convert` command in a shortcut, for example to show the price of a currency as a
notification.

### [Raycast](https://www.raycast.com/)

Raycast is a launcher for macOS that can run script commands. The [raycast_script](./raycast_script) folder contains
a script command that shows prices inline in Raycast, using the JSON output.

![bonbast_raycast](https://user-images.githubusercontent.com/24422125/194708612-a5f5557c-aab3-4ded-b500-9e08b594949c.png)

#### Setup for Raycast

Use the [setup-raycast.sh](./raycast_script/setup-raycast.sh) script to set up the script command, then follow the
instructions in the image below or the Raycast docs.

```shell
chmod +x setup-raycast.sh

./setup-raycast.sh standalone
# or
./setup-raycast.sh python
```

Or set it up manually:

1. Enable script commands in Raycast.
2. Copy [bonbast.sh](./raycast_script/bonbast.sh) into the Raycast `script-commands` folder.
3. Follow the instructions below or read the Raycast docs.

![raycast-setup](https://github.com/SamadiPour/bonbast/blob/master/.github/setup-raycast.png?raw=true)

---

## Development

The project uses [uv](https://docs.astral.sh/uv/).

```shell
git clone https://github.com/SamadiPour/bonbast.git
cd bonbast
uv sync                 # create .venv with the package and dev dependencies
uv run bonbast          # run the CLI from source
uv run pytest           # run the tests
```

The tests run offline against pages recorded from bonbast.com in `tests/fixtures`. To also check that the real website
still works with the parsers, run `BONBAST_LIVE_TESTS=1 uv run pytest`.

### Layout

| Module                   | Purpose                                                     |
|--------------------------|-------------------------------------------------------------|
| `bonbast/cli.py`         | The `bonbast` command (click)                               |
| `bonbast/client.py`      | `BonbastClient`: talks to bonbast.com                       |
| `bonbast/parsers.py`     | Turns bonbast.com responses into models                     |
| `bonbast/models.py`      | `Currency`, `Coin`, `Gold` and `Prices` dataclasses         |
| `bonbast/catalog.py`     | Every currency, coin and gold bonbast.com publishes         |
| `bonbast/render.py`      | Tables and text for the terminal (rich)                     |
| `bonbast/token_cache.py` | Caches the bonbast.com access token between runs            |

### Releasing

```shell
uv version --bump patch   # or minor / major
git commit -am "bump version $(uv version --short)" && git tag "$(uv version --short)"
git push --follow-tags    # the publish workflow tests, builds and uploads to PyPI
```

To build or install locally, use `uv build` or [scripts/local_install.sh](./scripts/local_install.sh).
