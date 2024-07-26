 # rebootpy

[![Supported py versions](https://img.shields.io/pypi/pyversions/rebootpy.svg)](https://pypi.org/project/rebootpy/)
[![Current pypi version](https://img.shields.io/pypi/v/rebootpy.svg)](https://pypi.org/project/rebootpy/)
[![Donate link](https://img.shields.io/badge/paypal-donate-blue.svg)](https://www.paypal.me/terbau)

Asynchronous library for interacting with Fortnite and EpicGames' API and XMPP services.

This library is a fork of [Terbau](https://github.com/Terbau/)'s [fortnitepy](https://github.com/Terbau/fortnitepy) which was abandoned.<br>
If you want to check out the original commit history, you can view it [here](https://github.com/Terbau/fortnitepy/commits/master/).

**Note:** This library is still under developement so breaking changes might happen at any time.

**Some key features:**
- Full support for Friends.
- Support for XMPP events.
- Support for Parties.
- Support for Battle Royale stats.
- Support for friend & party messages.

# Documentation
https://rebootpy.readthedocs.io/en/latest/

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

from rebootpy.ext import commands

bot = commands.Bot(
    command_prefix='!',
    auth=rebootpy.AuthorizationCodeAuth()
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
1. Log into the epic games account of your choice [here](https://www.epicgames.com/id/login?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Fapi%2Fredirect%3FclientId%3D3446cd72694c4a4485d81b77adbb2141%26responseType%3Dcode).
2. Copy the hex part from the url that shows up as showcased by the image below:

![Authorization Code](https://raw.githubusercontent.com/xMistt/rebootpy/main/docs/resources/images/authorization_code.png)

Keep in mind that authorization code isn't the only method of authentication, you can view all of them [here](https://rebootpy.readthedocs.io/en/latest/api.html#authentication), DeviceAuth is recommended once you've generated device auths.

# Credit
Thanks to [Kysune](https://github.com/SzymonLisowiec), [iXyles](https://github.com/iXyles), [Vrekt](https://github.com/Vrekt), [amrsatrio](https://github.com/Amrsatrio) for ideas and/or work that this library is built upon.

# Need help?
If you need more help feel free to join this [discord server](https://discord.gg/rnk869s).
