Getting started
===============

Installation
------------

**rebootpy requires Python 3.7 or higher**

**Windows**

.. code:: sh

    py -3 -m pip install rebootpy

**Linux**

.. code:: sh

    python3 -m pip install rebootpy

Authentication
--------------

To get a bot running, you must use one of several :ref:`authentication methods <authentication>`. If you do not know which one to use, you should stick with :class:`AdvancedAuth` which is used in most examples. :class:`AdvancedAuth` requires you to enter an authorization code upon the bots initial launch. When the bot has successfully authenticated, it will automatically generate credentials which can be used at a later point. That means you can launch your bot without any extra stuff needed after its first launch.

**How to get an authorization code:**

#. Log into an Epic Games account of your choice `here <https://www.epicgames.com/id/logout?redirectUrl=https%3A//www.epicgames.com/id/login%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3f69e56c7649492c8cc29f1af08a8a12%2526responseType%253Dcode>`_.
#. Copy the value of the `authorizationCode` field from the response as shown in the image below:

.. image:: https://raw.githubusercontent.com/xMistt/rebootpy/main/docs/resources/images/authorization_code.png

**Note:** An authorization code expires after 5 minutes.

Basic example
-------------

.. code-block:: python3

    import rebootpy
    import json
    import os

    filename = 'device_auths.json'


    class MyClient(rebootpy.Client):
        def __init__(self):
            device_auth_details = self.get_device_auth_details()
            super().__init__(
                auth=rebootpy.AdvancedAuth(
                    prompt_device_code=True,
                    **device_auth_details
                )
            )

        def get_device_auth_details(self):
            if os.path.isfile(filename):
                with open(filename, 'r') as fp:
                    return json.load(fp)
            return {}

        def store_device_auth_details(self, details):
            with open(filename, 'w') as fp:
                json.dump(details, fp)

        async def event_device_auth_generate(self, details):
            self.store_device_auth_details(details)

        async def event_ready(self):
            print(f'Client ready as {self.user.display_name}')

        async def event_friend_request(self, request):
            await request.accept()

        async def event_friend_message(self, message):
            print(f'{message.author.display_name}: {message.content}')
            await message.reply('Thanks for your message!')


    bot = MyClient()
    bot.run()
