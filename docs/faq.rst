.. currentmodule:: rebootpy

Frequently Asked Questions (FAQ)
================================

Authentication
--------------

Why are there so many different authentication methods?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the introduction of captcha on email and password authentication, there was
a need of different ways to authenticate. Therefore, rebootpy tries to offer
as many different authentication methods as possible. You can read more about the
different possibilities over `here <https://github.com/MixV2/EpicResearch/tree/master/docs/auth/grant_types>`_.


Which authentication method should I use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer to this question depends completely on what information you already
have, but it usually comes down to :class:`AdvancedAuth` no matter what. It's
simply the best right now as it combines other authentication methods and handles
all of the annoying stuff like creating device auths etc. If you are unsure how to
use :class:`AdvancedAuth`, you can take a look at the `examples folder <https://github.com/xMistt/rebootpy/tree/main/examples>`_
where it's used in all of the examples.


Whats the best way of storing the device auth details of an account?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This depends on the complexity of the bot with multiple accounts in mind. For
a program running a single bot, the easiest method of storage would be using
a json file. A method for this is showcased in all `examples <https://github.com/xMistt/rebootpy/tree/main/examples>`_.

For bots with multiple accounts I suggest using a database for the single reason
that file io is blocking and sometimes the operating system might spit out
errors because too many files are opened at the same time. 

**Note:** If you're going to use a database for anything in the same program as
the fortnite bot, please use an asynchronous database library. I can personally
recommend using a postgresql database and `asyncpg <https://github.com/MagicStack/asyncpg>`_
as the library.


General
-------

What is async/await and how do I use it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Asynchronous programming lets the program sort of perform multiple actions at
once. For newcomers to python/programming in general, the `discord.py faq <https://discordpy.readthedocs.io/en/latest/faq.html#coroutines>`_
has a great simplified explanation of its basic concepts. For people with existing
knowledge of asynchronous programming that want to know even more about it, I can
suggest `this article <https://realpython.com/async-io-python/>`_ on it. As well as
breakign down pretty much all you need to know about asynchronous programming, it
also explains the differences between multiprocessing, threading and asyncio in python
in an understandable way.


Where can I find usage examples?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find example code in the `examples folder <https://github.com/xMistt/rebootpy/tree/main/examples>`_
in the github repository.


How can I access the clients current party object?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The clients current party object can be accessed through :attr:`Client.party`.


How can I access the clients current party member object?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The clients current party member object can be accessed through :attr:`ClientParty.me`.
Example usage: ``await client.party.me.set_emote('EID_Floss')``


How can I send a DM?
~~~~~~~~~~~~~~~~~~~~

To send a DM you first need the :class:`Friend` object of the friend you
want to send the dm to and then use :meth:`Friend.send()`. Example: ::

    friend = client.get_friend('7e9f8dd37a924496bc5083733887b44c')
    await friend.send('Hello friend!')

If you want to respond to a friend message in :func:`event_friend_message()`, you
can do this by using :meth:`FriendMessage.reply()`. Example: ::

    @client.event
    async def event_friend_message(message):
        await message.reply('Thanks for the message!')

        # Not as clean but would still work:
        await message.author.send('Thanks for the message!')


How can I set a status?
~~~~~~~~~~~~~~~~~~~~~~~
You can pass a status message for the client to use when creating 
client. 

.. code-block:: python3

    client = rebootpy.Client(
        auth=rebootpy.Auth, // Here goes an authentication method like rebootpy.AdvancedAuth or rebootpy.DeviceAuth
        status="This is my status"
    )

.. warning::

    This will override all status messages in the future. The standard
    status message (``Battle Royale Lobby {party size} / {party max size}``)
    will also be overridden. If you just want to send a status message once
    and not override all upcoming status messages, :meth:`Client.send_presence`
    is the function you are looking for.

Alternatively you can change the presence with :meth:`Client.set_presence`.


How can I get the CID of a skin?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is no good easy way to obtain these yourself. However, some great minds
have created tools to make this easier for others. Here are some of them: 
- `FunGames' API <https://benbot.stoplight.io/docs/benbot-docs>`_.
- `NotOfficer's API <https://fortnite-api.com/>`_.


How can I use Two Factor Authentication when logging into the client?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the user the client attempts to log in as requires two factor authentication, the code will
be prompted in console on startup. Then just type it into console and if accepted, 
the login process will continue.

Alternatively, you might pass the code when intitializing :class:`Client` with the keyword ``two_factor_code``.


How can I get a users K/D or Win Percentage?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the stats request does not return a K/D or win percentage, you must
calculate them yourself. Just to make it easy :class:`StatsV2` includes 
functions that calculates these values for you.

Take a closer look at :meth:`StatsV2.get_kd` and 
:meth:`StatsV2.get_winpercentage`.


Why are some cosmetics invisible/dances not playing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since ~C4S3, cosmetics have been stored in 2 paths, some in the old folder but the majority in a new folder
called BRCosmetics. Since the path in rebootpy is hard-coded, theres no good way of getting the correct path
since it would require installing the entire game to wherever your instance of rebootpy is running. However,
the best way I have found is to use a third party API such as Fortnite-API to get the path.

Outfits do not have this issue anymore as they no longer require a path at all, so you can just pass the ID
of any outfit to `set_outfit()` and regardless of its location, it will show correctly (as long as the ID
 is valid).
**Guide to find path using Fortnite-API:** 

1. Head over to the `Fortnite-API docs <https://dash.fortnite-api.com/endpoints/cosmetics>`_.
2. Choose an endpoint that you want to use to lookup cosmetics, either via ID or name.
3. The response will have a key called `path` in `data`, if it contains BRCosmetic, just pass
the plain ID to the `set_` function as this is the path that the library is already using.
4. If the cosmetic is in the original path, use `FortniteGame/Content/Athena/Items/<CosmeticPath>/`
as the path, example usage for a dance would be: `await bot.party.me.set_emote('/Game/Athena/Items/Cosmetics/Dances/EID_Coronet.EID_Coronet')`

**Here is an example of using Fortnite-API to get the correct path for a dance:**

.. code-block::

    @bot.command()
    async def emote(ctx, *, search: str):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="GET",
                url="https://fortnite-api.com/v2/cosmetics/br/search/all?name=" \
                f"{search}t&matchMethod=contains&backendType=AthenaDance"
            ) as request:
                if request.status == 404:
                    await ctx.send('Skin not found!')

                data = await request.json()

        if "brcosmetics" in data['data']['path']:
            await bot.party.me.set_outfit(asset=data['data']['id'])
        else:
            path = f"/Game/Athena/Items/Cosmetics/Dances/{cosmetic.id}.{cosmetic.id}'"
            await bot.party.me.set_outfit(asset=path)

A full example can be found `here <https://github.com/xMistt/rebootpy/blob/main/examples/fortnite_api_path.py>`_.



