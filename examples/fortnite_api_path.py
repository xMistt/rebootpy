"""This example showcases how to use rebootpy integrating with an api
in order to correctly get the path for cosmetics other than outfits.

NOTE: This example uses AdvancedAuth and stores the details in a file.
It is important that this file is moved whenever the script itself is moved
because it relies on the stored details. However, if the file is nowhere to
be found, it will simply use device code to generate a new file.
"""

import rebootpy
import json
import os
import aiohttp

from rebootpy.ext import commands

filename = 'device_auths.json'


def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}


def store_device_auth_details(details):
    with open(filename, 'w') as fp:
        json.dump(details, fp)


device_auth_details = get_device_auth_details()
bot = commands.Bot(
    command_prefix='!',
    auth=rebootpy.AdvancedAuth(
        prompt_device_code=True,
        open_link_in_browser=True,
        **device_auth_details
    )
)


@bot.event
async def event_device_auth_generate(details):
    store_device_auth_details(details)


@bot.event
async def event_ready():
    print(f'Bot ready as {bot.user.display_name} ({bot.user.id}).')


@bot.event
async def event_friend_request(request):
    await request.accept()


@bot.event
async def event_party_invite(invite):
    await invite.accept()


@bot.command()
async def emote(ctx, *, search: str):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method="GET",
            url="https://fortnite-api.com/v2/cosmetics/br/search?name=" \
            f"{search}&matchMethod=contains&backendType=AthenaDance"
        ) as request:
            if request.status == 404:
                return await ctx.send('Dance not found!')

            data = await request.json()

    if "brcosmetics" in data['data']['path'].lower():
        await bot.party.me.set_emote(asset=data['data']['id'])
    else:
        path = f"/Game/Athena/Items/Cosmetics/Dances/{data['data']['id']}.{data['data']['id']}"
        await bot.party.me.set_emote(asset=path)


bot.run()
