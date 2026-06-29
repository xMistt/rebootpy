# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2024 Oli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import aiohttp
import json
import functools
import logging
import base64
import datetime

from .message import FriendMessage, PartyMessage
from .presence import Presence

from aiohttp import hdrs, helpers, client_reqrep, connector
from aiohttp.http import StreamWriter, HttpVersion10, HttpVersion11

log = logging.getLogger(__name__)


def decode_message_body(body: str) -> str:
    try:
        decoded = base64.b64decode(body).decode('utf-8')
        decoded = decoded.rstrip('\x00')
        parsed = json.loads(decoded)
        return parsed.get('msg', body)
    except (ValueError, KeyError, json.JSONDecodeError, Exception):
        return body


class WebsocketClient:
    def __init__(self, client) -> None:
        self.client = client

        self.wss_session = None
        self.websocket = None
        self.ws_task = None

        self.heartbeat_started = False

        self.connection_id = None

    async def set_session(self) -> None:
        self.wss_session = aiohttp.ClientSession()

    async def send_presence(self, connection_id: str) -> None:
        await self.client.http.chat_send_presence(
            connection_id=connection_id,
            auth="EAS_ACCESS_TOKEN"
        )

    async def send_heartbeat(self, delay: int) -> None:
        while not self.websocket.closed:
            await self.websocket.send_str("\n")
            await asyncio.sleep(delay)

    async def parse_message(self, raw: str) -> None:
        raw_headers, raw_json = raw.split('\n\n', 1)
        header_lines = raw_headers.splitlines()
        message_type = header_lines[0]

        headers = {}
        for line in header_lines[1:]:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

        data = json.loads(raw_json[:-1]) if len(raw_json) >= 3 else {}

        log.debug(
            f'{datetime.datetime.now(datetime.timezone.utc)} - Received websocket message with type'
            f' {message_type} with the headers {headers} and body \n{data}.')

        if message_type == 'CONNECTED' and not self.heartbeat_started:
            self.heartbeat_started = True

            delay = int(headers['heart-beat'].split(',')[1]) // 1000
            self.client.loop.create_task(self.send_heartbeat(delay))

            await self.websocket.send_str(f"SUBSCRIBE\nid:0\n"
                                          f"destination:launcher\n\n\x00")
        elif (message_type == 'MESSAGE' and 'type' in data
              and data['type'] == 'core.connect.v1.connected'):
            self.connection_id = data['connectionId']
            await self.send_presence(
                connection_id=self.connection_id
            )
        elif (
            message_type == 'MESSAGE' and
            data.get('type') == 'social.chat.v1.NEW_MESSAGE' and
            data.get('payload').get('conversation').get('type') == 'dm'
        ):
            author = self.client.get_friend(
                data['payload']['message']['senderId']
            )
            if author is None:
                try:
                    author = await self.client.wait_for(
                        'friend_add',
                        check=lambda f: f.id == data['payload']['message']
                        ['senderId'],
                        timeout=2
                    )
                except asyncio.TimeoutError:
                    return

            try:
                decoded_content = decode_message_body(
                    data['payload']['message']['body']
                )
                m = FriendMessage(
                    client=self.client,
                    author=author,
                    content=decoded_content
                )
                self.client.dispatch_event('friend_message', m)
            except ValueError:
                pass
        elif (
            message_type == 'MESSAGE' and
            data.get('type') == 'social.chat.v1.NEW_MESSAGE' and
            data.get('payload').get('conversation').get('type') == 'party'
        ):
            user_id = data['payload']['message']['senderId']
            party = self.client.party

            if (user_id == self.client.user.id
                    or user_id not in party._members):
                return

            decoded_content = decode_message_body(
                data['payload']['message']['body']
            )
            self.client.dispatch_event('party_message', PartyMessage(
                client=self.client,
                party=party,
                author=party._members[data['payload']['message']['senderId']],
                content=decoded_content
            ))
        elif (
            message_type == 'MESSAGE' and
            data.get('type') == 'presence.v1.UPDATE'
        ):
            user_id = data['payload']['accountId']
            friend = self.client.get_friend(user_id)
            if friend is None:
                try:
                    friend = await self.client.wait_for(
                        'friend_add',
                        check=lambda f: f.id == user_id,
                        timeout=1
                    )
                except asyncio.TimeoutError:
                    return

            _pres = Presence(
                self.client,
                data['payload']
            )

            if _pres.party is not None:
                try:
                    display_name = _pres.party.raw['sDN']
                    if display_name != _pres.friend.display_name:
                        _pres.friend._update_display_name(display_name)
                except (KeyError, AttributeError):
                    pass

            before_pres = friend.last_presence

            # Check how real client handles this.
            # if not is_available and friend.is_online():
            #     friend._update_last_logout(datetime.datetime.utcnow())
            #
            #     try:
            #         del self.client._presences[user_id]
            #     except KeyError:
            #         pass
            #
            # else:
            self.client._presences[user_id] = _pres

            self.client.dispatch_event('friend_presence', before_pres, _pres)
        elif (
            message_type == 'ERROR' and
            data.get('statusCode') == 4019
        ):
            log.debug('STOMP authentication token is now invalid')
            await self.restart()

    async def connect_to_websocket(self) -> None:
        print('connecting to ws')
        headers = {
            'Authorization': f'Bearer {self.client.auth.eas_access_token}',
            'Epic-Connect-Protocol': 'stomp',
            "Sec-WebSocket-Protocol": "v10.stomp,v11.stomp,v12.stomp",
            'Epic-Connect-Device-Id': " ",
        }
        async with self.wss_session.ws_connect(
            "wss://connect.epicgames.dev/",
            protocols=['stomp'],
            headers=headers
        ) as websocket:
            self.websocket = websocket
            connect_frame = f"CONNECT\nheart-beat:30000,0\n" \
                            f"accept-version:1.0,1.1,1.2\n\n\x00"
            await websocket.send_str(connect_frame)

            async for msg in websocket:
                await self.parse_message(msg.data.decode())

    async def run(self) -> None:
        log.debug('Starting STOMP websocket client')
        await self.set_session()
        self.ws_task = self.client.loop.create_task(
            self.connect_to_websocket()
        )

    async def close(self) -> None:
        log.debug('Closing STOMP websocket client')
        await self.websocket.close()
        await self.wss_session.close()

        self.heartbeat_started = False

    async def restart(self) -> None:
        log.debug('Restarting STOMP websocket client')
        await self.close()

        if self.ws_task:
            self.ws_task.cancel()
            try:
                await self.ws_task
            except asyncio.CancelledError:
                pass
            self.ws_task = None

        await self.run()
