#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title bonbast
# @raycast.mode inline
# @raycast.refreshTime 3h

# Optional parameters:
# @raycast.icon 💰
# @raycast.packageName Bonbast

# Documentation:
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

function thousands {
    awk '{ printf("%'"'"'d\n",$1); }'
}

DATA="$(/opt/homebrew/bin/python3 -m bonbast export | jq -r .)"
USD="$(echo "$DATA" | jq '.USD.buy' | thousands)"
EUR="$(echo "$DATA" | jq '.EUR.buy' | thousands)"
GBP="$(echo "$DATA" | jq '.GBP.buy' | thousands)"

echo "🇺🇸 USD: ${USD}  |  🇪🇺 EUR: ${EUR}  |  🇬🇧 GBP: ${GBP}"
