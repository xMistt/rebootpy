"""This example makes use of multiple accounts.

NOTE: This example uses AdvancedAuth and stores the details in a file.
It is important that this file is moved whenever the script itself is moved
because it relies on the stored details. However, if the file is nowhere to
be found, it will simply use device code to generate a new file.
"""

import rebootpy
import asyncio
import functools
import os
import json

instances = {}
filename = 'device_auths.json'

def get_device_auth_details():
    with open(filename, 'r') as fp:
        return json.load(fp)

async def event_sub_ready(client):
    instances[client.user.id] = client
    print('{0.user.display_name} ready.'.format(client))

async def event_sub_friend_request(request):
    print('{0.client.user.display_name} received a friend request.'.format(request))
    await request.accept()

async def event_sub_party_member_join(member):
    print("{0.display_name} joined {0.client.user.display_name}'s party.".format(member))            


clients = []
device_auths = get_device_auth_details()
for device_auth in credentials.items():
    authentication = rebootpy.DeviceAuth(
        **device_auth
    )

    client = rebootpy.Client(
        auth=authentication,
        default_party_member_config=rebootpy.DefaultPartyMemberConfig(
            meta=(
                functools.partial(rebootpy.ClientPartyMember.set_outfit, 'CID_175_Athena_Commando_M_Celestial'), # galaxy skin
            )
        )
    )

    # register events here
    client.add_event_handler('device_auth_generate', event_sub_device_auth_generate)
    client.add_event_handler('friend_request', event_sub_friend_request)
    client.add_event_handler('party_member_join', event_sub_party_member_join)

    clients.append(client)

rebootpy.run_multiple(
    clients,
    ready_callback=event_sub_ready,
    all_ready_callback=lambda: print('All clients ready')
)
