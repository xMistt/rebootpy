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


# Epic for some reason will deny the websocket request if the request line
# doesn't have the absolute url so we need to monekypatch the aiohttp
# function ourselves. This is taken from ClientRequestBase in client_reqrep.py
# and will continously need to be updated if aiohttp makes breaking changes.
class WebsocketRequest(aiohttp.client_reqrep.ClientRequest):
    async def send(self, conn: "Connection") -> "ClientResponse":
        # Specify request target:
        # - CONNECT request must send authority form URI
        # - not CONNECT proxy must send absolute form URI
        # - most common is origin form URI
        if self.method == hdrs.METH_CONNECT:
            connect_host = self.url.host_subcomponent
            assert connect_host is not None
            path = f"{connect_host}:{self.url.port}"
        elif self.proxy and not self.is_ssl():
            path = str(self.url)
        else:
            path = self.url.raw_path_qs

        protocol = conn.protocol
        assert protocol is not None
        writer = StreamWriter(
            protocol,
            self.loop,
            on_chunk_sent=(
                functools.partial(self._on_chunk_request_sent, self.method, self.url)
                if self._traces
                else None
            ),
            on_headers_sent=(
                functools.partial(self._on_headers_request_sent, self.method, self.url)
                if self._traces
                else None
            ),
        )

        if self.compress:
            writer.enable_compression(self.compress)  # type: ignore[arg-type]

        if self.chunked is not None:
            writer.enable_chunking()

        # set default content-type
        if (
                self.method in self.POST_METHODS
                and (
                self._skip_auto_headers is None
                or hdrs.CONTENT_TYPE not in self._skip_auto_headers
        )
                and hdrs.CONTENT_TYPE not in self.headers
        ):
            self.headers[hdrs.CONTENT_TYPE] = "application/octet-stream"

        v = self.version
        if hdrs.CONNECTION not in self.headers:
            if conn._connector.force_close:
                if v == HttpVersion11:
                    self.headers[hdrs.CONNECTION] = "close"
            elif v == HttpVersion10:
                self.headers[hdrs.CONNECTION] = "keep-alive"

        # status + headers
        status_line = (
            f"{self.method} https://connect.epicgames.dev/ HTTP/{v.major}.{v.minor}"
            if "/stomp" in path
            else f"{self.method} {path} HTTP/{v.major}.{v.minor}"
        )
        # original line:
        # status_line = f"{self.method} {path} HTTP/{v.major}.{v.minor}"

        # Buffer headers for potential coalescing with body
        await writer.write_headers(status_line, self.headers)

        task: asyncio.Task[None] | None
        if self._body or self._continue is not None or protocol.writing_paused:
            coro = self.write_bytes(writer, conn, self._get_content_length())
            if sys.version_info >= (3, 12):
                # Optimization for Python 3.12, try to write
                # bytes immediately to avoid having to schedule
                # the task on the event loop.
                task = asyncio.Task(coro, loop=self.loop, eager_start=True)
            else:
                task = self.loop.create_task(coro)
            if task.done():
                task = None
            else:
                self._writer = task
        else:
            # We have nothing to write because
            # - there is no body
            # - the protocol does not have writing paused
            # - we are not waiting for a 100-continue response
            protocol.start_timeout()
            writer.set_eof()
            task = None
        response_class = self.response_class
        assert response_class is not None
        self.response = response_class(
            self.method,
            self.original_url,
            writer=task,
            continue100=self._continue,
            timer=self._timer,
            request_info=self.request_info,
            traces=self._traces,
            loop=self.loop,
            session=self._session,
            stream_writer=writer,
        )
        return self.response


class WebsocketClient:
    def __init__(self, client) -> None:
        self.client = client

        self.wss_session = None
        self.websocket = None
        self.ws_task = None

        self.heartbeat_started = False

        self.connection_id = None

    async def set_session(self) -> None:
        self.wss_session = aiohttp.ClientSession(
            skip_auto_headers=["Accept", "Accept-Encoding", "User-Agent"],
            request_class=WebsocketRequest
        )

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
            "wss://connect.epicgames.dev/stomp",
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
