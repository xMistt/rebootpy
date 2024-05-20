"""This example showcases how to use rebootpy with the asynchronous
web framework sanic.
"""

import rebootpy
import json
import os
import sanic

from rebootpy.ext import commands


filename = 'device_auths.json'
description = 'My awesome fortnite bot / sanic app!'


def get_device_auth_details():
    with open(filename, 'r') as fp:
        return json.load(fp)


device_auths = get_device_auth_details()
bot = commands.Bot(
    command_prefix='!',
    auth=rebootpy.DeviceAuth(
        **device_auth
    )
)

sanic_app = sanic.Sanic(__name__)
server = None


@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@sanic_app.route('/friends', methods=['GET'])
async def get_friends_handler(request):
    friends = [friend.id for friend in bot.friends]
    return sanic.response.json(friends)


@bot.event
async def event_ready():
    global server

    print('----------------')
    print('Bot ready as')
    print(bot.user.display_name)
    print(bot.user.id)
    print('----------------')

    coro = sanic_app.create_server(
        host='0.0.0.0',
        port=8000,
        return_asyncio_server=True,
    )
    server = await coro


@bot.event
async def event_before_close():
    global server

    if server is not None:
        await server.close()


@bot.event
async def event_friend_request(request):
    await request.accept()


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


bot.run()
