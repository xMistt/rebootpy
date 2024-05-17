 # rebootpy

[![Supported py versions](https://img.shields.io/pypi/pyversions/fortnitepy.svg)](https://pypi.org/project/rebootpy/)
[![Current pypi version](https://img.shields.io/pypi/v/fortnitepy.svg)](https://pypi.org/project/rebootpy/)
[![Donate link](https://img.shields.io/badge/paypal-donate-blue.svg)](https://www.paypal.me/terbau)

Asynchronous library for interacting with Fortnite and EpicGames' API and XMPP services.
This library is a fork of [Terbau](https://github.com/Terbau/)'s [fortnitepy](https://github.com/Terbau/fortnitepy) which was abandoned.

**Note:** This library is still under developement so breaking changes might happen at any time.

**Some key features:**
- Full support for Friends.
- Support for XMPP events including friend and party messages + many more.
- Support for Parties.
- Support for Battle Royale stats.

# Documentation
https://fortnitepy.readthedocs.io/en/latest/

# Installing
```
# windows
py -3 -m pip install -U rebootpy

# linux
python3 -m pip install -U rebootpy
```

# Basic usage
```py
import rebootpy
import json
import os

from rebootpy.ext import commands

bot = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AuthorizationCodeAuth()
)

@bot.event
async def event_ready():
    print(f'Bot ready as {bot.user.display_name} ({bot.user.id})')

@bot.event
async def event_friend_request(request):
    await request.accept()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run()
```

# Authorization
How to get a one time authorization code:
1. Log into the epic games account of your choice [here](https://www.epicgames.com/id/logout?redirectUrl=https%3A//www.epicgames.com/id/login%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3446cd72694c4a4485d81b77adbb2141%2526responseType%253Dcode).
2. Copy the hex part from the url that shows up as showcased by the image below:

![Authorization Code](https://raw.githubusercontent.com/Terbau/fortnitepy/dev/docs/resources/images/authorization_code.png)

# Credit
Thanks to [Kysune](https://github.com/SzymonLisowiec), [iXyles](https://github.com/iXyles), [Vrekt](https://github.com/Vrekt) and [amrsatrio](https://github.com/Amrsatrio) for ideas and/or work that this library is built upon.

Also thanks to [discord.py](https://github.com/Rapptz/discord.py) for much inspiration code-wise.

# Need help?
If you need more help feel free to join this [discord server](https://discord.gg/rnk869s).
