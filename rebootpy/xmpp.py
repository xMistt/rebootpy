# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019-2021 Terbau

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
import json
import logging
import datetime
import uuid
import itertools
import unicodedata
import aiohttp
import base64

from xml.etree import ElementTree
from collections import defaultdict
from typing import TYPE_CHECKING, Optional, Union, Awaitable, Any, Tuple
from .errors import HTTPException
from .party import (Party, PartyJoinRequest, ReceivedPartyInvitation,
                    PartyJoinConfirmation)
from .presence import Presence
from .enums import AwayStatus
from .utils import to_iso, from_iso

if TYPE_CHECKING:
    from .client import Client

log = logging.getLogger(__name__)

_party_meta_attrs = {'playlist_info': 'playlist', 'squad_fill': None,
                     'privacy': None}

_member_meta_attrs = ('ready', 'input', 'outfit',
                      'backpack', 'pet', 'pickaxe', 'contrail', 'emote',
                      'emoji', 'banner', 'battlepass_info', 'in_match',
                      'match_players_left', 'enlightenments', 'corruption',
                      'outfit_variants', 'backpack_variants',
                      'pickaxe_variants', 'contrail_variants',
                      'lobby_map_marker_is_visible',
                      'lobby_map_marker_coordinates', 'playlist_selection',)


def is_RandALCat(c: str) -> bool:
    return unicodedata.bidirectional(c) in ('R', 'AL')


class EventContext:

    __slots__ = ('client', 'body', 'party', 'created_at')

    def __init__(self, client: 'Client', body: dict) -> None:
        self.client = client
        self.body = body

        self.party = self.client.party
        self.created_at = datetime.datetime.utcnow()


class EventDispatcher:
    listeners = defaultdict(list)
    presence_listeners = []
    interactions_enabled = False

    @classmethod
    def process_presence(cls, client, *args) -> None:
        for coro in cls.presence_listeners:
            if __name__ == coro.__module__:
                asyncio.ensure_future(coro(client.xmpp, *args))
            else:
                asyncio.ensure_future(coro(*args))

    @classmethod
    def presence(cls) -> Awaitable:
        def decorator(coro: Awaitable) -> Awaitable:
            cls.add_presence_handler(coro)
            return coro
        return decorator

    @classmethod
    def add_presence_handler(cls, coro: Awaitable) -> None:
        if coro not in cls.presence_listeners:
            cls.presence_listeners.append(coro)

    @classmethod
    def remove_presence_handler(cls, coro: Awaitable) -> None:
        cls.presence_listeners = [
            c for c in cls.presence_listeners if c is not coro
        ]

    @classmethod
    def process_event(cls, client: 'Client', raw_body: dict) -> None:
        body = json.loads(raw_body)

        type_ = body.get('type')
        if type_ is None:
            if cls.interactions_enabled:
                for interaction in body['interactions']:
                    cls.process_event(client, interaction)
            return

        log.debug('Received event `{}` with body `{}`'.format(type_, body))

        coros = cls.listeners.get(type_, [])
        for coro in coros:
            ctx = EventContext(client, body)

            if __name__ == coro.__module__:
                asyncio.ensure_future(coro(client.xmpp, ctx))
            else:
                asyncio.ensure_future(coro(ctx))

    @classmethod
    def event(cls, event: str) -> Awaitable:
        def decorator(coro: Awaitable) -> Awaitable:
            cls.add_event_handler(event, coro)
            return coro
        return decorator

    @classmethod
    def add_event_handler(cls, event: str, coro: Awaitable) -> None:
        cls.listeners[event].append(coro)
        log.debug('Added handler for {0} to {1}'.format(event, coro))

    @classmethod
    def remove_event_handler(cls, event: str, coro: Awaitable) -> None:
        handlers = [c for c in cls.listeners[event] if c is not coro]
        log.debug('Removed {0} handler(s) for {1}'.format(
            len(cls.listeners[event]) - len(handlers),
            event
        ))
        cls.listeners[event] = handlers


# Not really used anymore, but it won't get removed as people might rely on it.
dispatcher = EventDispatcher()


class XMLProcessor:
    def _process_presence(self, raw: str) -> Optional[Union[tuple, bool]]:
        tree = ElementTree.fromstring(raw)

        type_ = tree.get('type')

        # Only intercept presences with either no type attribute
        # (which means available) or unavailable type.
        if type_ is not None and type_ not in ('available', 'unavailable'):
            return False

        from_ = tree.get('from')

        # If from is a party, let aioxmpp handle it.
        if from_ is not None and '-' in from_:
            return False

        status = None
        show = None
        for elem in tree:
            if 'status' in elem.tag:
                status = elem.text
            if 'show' in elem.tag:
                show = elem.text

        # We have no use for the presence if status is None and
        # therefore it's better to just let aioxmpp handle it.
        if status is None:
            return False

        split = from_.split('@')
        user_id = split[0]
        platform = split[1].split(':')[2]

        return 'presence', (user_id, platform, type_, status, show)

    def _process_message(self, raw: str) -> Optional[Union[tuple, bool]]:
        tree = ElementTree.fromstring(raw)

        # Only intercept messages sent by epic
        if tree.get('from', '') != 'xmpp-admin@prod.ol.epicgames.com':
            return False

        type_ = tree.get('type')

        # Only intercept messages with either no type attribute
        # (which means normal) or  type.
        if type_ is not None and type_ != 'normal':
            return False

        # Let aioxmpp handle it if no body tag is found. Also, technically
        # a message can include multiple body tags for different languages
        # but afaik only one body tag is sent from epics servers.
        body = None
        for elem in tree:
            if 'body' in elem.tag:
                body = elem.text
                break
        else:
            return False

        return 'message', (body,)

    def process(self, raw: str) -> Optional[Union[tuple, bool]]:
        # Yes, this is a hacky solution but it's better than
        # using the quite unnecessary slow aioxmpp one.
        if '<presence' in raw:
            return self._process_presence(raw)
        elif '<message' in raw:
            return self._process_message(raw)

        return False


class XMPPClient:
    def __init__(self, client: 'Client', ws_connector=None) -> None:
        self.client = client
        # self.ws_connector = ws_connector
        #
        # self.xmpp_client = None
        # self.stream = None

        self._ping_task = None
        self._presence_task = None
        self._watchdog_task = None
        self._is_suspended = False
        self._reconnect_recover_task = None
        self._last_disconnected_at = None
        self._last_known_party_id = None
        self._xmpp_task = None

        self.send_presence_on_add = True

        # new attributes
        self.http_session = None
        self.websocket = None

        self._authed = False
        self._bound = False
        self._ready = False
        self._connected = False
        self._restarting = False
        self._last_pong = None

        self.resource_hex = uuid.uuid4().hex.upper()

        self.xml_processor = XMLProcessor()

        self.stanza = "<presence/>"

    @property
    def resource(self) -> str:
        return f"V2:Fortnite:{self.client.platform.value}::{self.resource_hex}"

    @property
    def local_jid(self) -> str:
        return f"{self.client.user.id}@prod.ol.epicgames.com/{self.resource}"

    def _jid(self, user_id: str) -> str:
        return f"{user_id}@{self.client.service_host}"

    def _create_invite(self, from_id: str, data: dict) -> dict:
        sent_at = from_iso(data['sent'])
        expires_at = sent_at + datetime.timedelta(hours=4)

        member = None
        for m in data['members']:
            if m['account_id'] == from_id:
                member = m
                break

        if member is None:
            # This should theoretically never happen.
            raise RuntimeError('Inviter is missing from payload.')

        party_m = data['meta']
        member_m = member['meta']

        meta = {
            'urn:epic:conn:type_s': 'game',
            'urn:epic:cfg:build-id_s': party_m['urn:epic:cfg:build-id_s'],
            'urn:epic:invite:platformdata_s': '',
        }

        if 'Platform_j' in member_m:
            meta['Platform_j'] = json.loads(
                member_m['Platform_j']
            )['Platform']['platformStr']

        if 'urn:epic:member:dn_s' in member['meta']:
            meta['urn:epic:member:dn_s'] = member_m['urn:epic:member:dn_s']

        inv = {
            'party_id': data['id'],
            'sent_by': from_id,
            'sent_to': self.client.user.id,
            'sent_at': to_iso(sent_at),
            'updated_at': to_iso(sent_at),
            'expires_at': to_iso(expires_at),
            'status': 'SENT',
            'meta': meta
        }
        return inv

    @EventDispatcher.event('com.epicgames.friends.core.apiobjects.Friend')
    async def friend_event(self, ctx: EventContext) -> None:
        body = ctx.body

        await self.client.wait_until_ready()
        _payload = body['payload']
        _status = _payload['status']
        _id = _payload['accountId']

        if _status == 'ACCEPTED':

            data = self.client.get_user(_id)
            if data is None:
                if self.client.fetch_user_data_in_events:
                    data = await self.client.fetch_user(_id, raw=True)
            else:
                data = data.get_raw()

            try:
                timestamp = body['timestamp']
            except (TypeError, KeyError):
                timestamp = datetime.datetime.utcnow()

            f = self.client.store_friend({
                **(data or {}),
                'id': _payload['accountId'],
                'favorite': _payload['favorite'],
                'direction': _payload['direction'],
                'status': _status,
                'created': timestamp,
            })

            try:
                del self.client._pending_friends[f.id]
            except KeyError:
                pass

            # Send presence to the newly added friend as that is now
            # required to do by the server (or at least thats what
            # i suspect)
            if self.send_presence_on_add:
                self.client.loop.create_task(self.send_presence(
                    to=f.jid,
                    status=self.client.party.last_raw_status,
                    show=self.client.away.value
                ))

            self.client.dispatch_event('friend_add', f)

        elif _status == 'PENDING':
            data = self.client.get_user(_id)
            if data is None:
                if self.client.fetch_user_data_in_events:
                    data = await self.client.fetch_user(_id, raw=True)
            else:
                data = data.get_raw()

            data = {
                **(data or {}),
                'id': _payload['accountId'],
                'direction': _payload['direction'],
                'status': _status,
                'created': body['timestamp']
            }
            if _payload['direction'] == 'INBOUND':
                pf = self.client.store_incoming_pending_friend(data)
            else:
                pf = self.client.store_outgoing_pending_friend(data)

            self.client.dispatch_event('friend_request', pf)

    @EventDispatcher.event('FRIENDSHIP_REMOVE')
    async def friend_remove_event(self, ctx: EventContext) -> None:
        body = ctx.body

        if body['from'] == self.client.user.id:
            _id = body['to']
        else:
            _id = body['from']

        if body['reason'] == 'ABORTED':
            pf = self.client.get_pending_friend(_id)
            if pf is not None:
                self.client.store_user(pf.get_raw())

                try:
                    del self.client._pending_friends[pf.id]
                except KeyError:
                    pass

                self.client.dispatch_event('friend_request_abort', pf)
        elif body['reason'] == 'REJECTED':
            pf = self.client.get_pending_friend(_id)
            if pf is not None:
                self.client.store_user(pf.get_raw())

                try:
                    del self.client._pending_friends[pf.id]
                except KeyError:
                    pass

                self.client.dispatch_event('friend_request_decline', pf)
        else:
            f = self.client.get_friend(_id)
            if f is not None:
                self.client.store_user(f.get_raw())

                try:
                    del self.client._friends[f.id]
                except KeyError:
                    pass

                self.client.dispatch_event('friend_remove', f)

        try:
            del self.client._presences[_id]
        except KeyError:
            pass

    @EventDispatcher.event('com.epicgames.friends.core.apiobjects.BlockListEntryAdded')  # noqa
    async def event_blocklist_added(self, ctx: EventContext) -> None:
        body = ctx.body

        account_id = body['payload']['accountId']
        data = self.client.get_user(account_id)
        if data is None:
            if self.client.fetch_user_data_in_events:
                data = await self.client.fetch_user(account_id, raw=True)
        else:
            data = data.get_raw()

        blocked_user = self.client.store_blocked_user({
            **(data or {}),
            'id': account_id
        })
        self.client.dispatch_event('user_block', blocked_user)

    @EventDispatcher.event('com.epicgames.friends.core.apiobjects.BlockListEntryRemoved')  # noqa
    async def event_blocklist_remove(self, ctx: EventContext) -> None:
        body = ctx.body

        account_id = body['payload']['accountId']
        data = self.client.get_blocked_user(account_id)
        if data is None:
            if self.client.fetch_user_data_in_events:
                data = await self.client.fetch_user(account_id, raw=True)
        else:
            data = data.get_raw()

        user = self.client.store_user({
            **(data or {}),
            'id': account_id,
        })

        try:
            del self.client._blocked_users[user.id]
        except KeyError:
            pass

        self.client.dispatch_event('user_unblock', user)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.PING')
    async def event_ping_received(self, ctx: EventContext) -> None:
        body = ctx.body
        pinger = body['pinger_id']
        try:
            data = (await self.client.http.party_lookup_ping(pinger))[0]
        except (IndexError, HTTPException) as exc:
            if isinstance(exc, HTTPException):
                m = 'errors.com.epicgames.social.party.ping_not_found'
                if exc.message_code != m:
                    raise

            self.client.dispatch_event(
                'invalid_party_invite',
                self.client.get_friend(pinger)
            )
            return

        for inv in data['invites']:
            if inv['sent_by'] == pinger and inv['status'] == 'SENT':
                invite = inv
                break
        else:
            invite = self._create_invite(pinger, {**body, **data})

        if 'urn:epic:cfg:build-id_s' not in invite['meta']:
            pres = self.client.get_presence(pinger)
            if (pres is not None and pres.party is not None
                    and not pres.party.private):
                net_cl = pres.party.net_cl
            else:
                net_cl = self.client.net_cl
        else:
            s = invite['meta']['urn:epic:cfg:build-id_s']
            net_cl = s[4:] if s.startswith('1:') else s

        if net_cl != self.client.net_cl and self.client.net_cl != '':
            log.debug(
                'Could not match the currently set net_cl ({0!r}) to the '
                'received value ({1!r})'.format(self.client.net_cl, net_cl)
            )

        new_party = Party(self.client, data)
        await new_party._update_members(
            members=data['members'],
            fetch_user_data=self.client.fetch_user_data_in_events,
        )

        invitation = ReceivedPartyInvitation(
            self.client,
            new_party,
            net_cl,
            invite
        )
        self.client.dispatch_event('party_invite', invitation)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_JOINED')  # noqa
    async def event_party_member_joined(self,
                                        ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client.wait_until_party_ready()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        if user_id == self.client.user.id:
            await self.client._internal_join_party_lock.wait()

        member = party.get_member(user_id)
        if member is None:
            member = (await party._update_members(
                (body,),
                remove_missing=False,
                fetch_user_data=self.client.fetch_user_data_in_events,
            ))[0]

        member.meta.has_been_updated = False

        fut = None
        if party.me is not None:
            party.me.do_on_member_join_patch()

            yielding = party.me._default_config.yield_leadership
            if party.me.leader and not yielding:
                fut = asyncio.ensure_future(party.refresh_squad_assignments())

        if fut is not None:
            await fut

        self.client.dispatch_event('internal_party_member_join', member)

        if self.client.wait_for_member_meta_in_events:
            if not member.meta.has_been_updated:
                try:
                    await self.client.wait_for(
                        'internal_initial_party_member_meta',
                        check=lambda m: m.id == member.id,
                        timeout=2
                    )
                except asyncio.TimeoutError:
                    pass

        self.client.dispatch_event('party_member_join', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_LEFT')  # noqa
    async def event_party_member_left(self, ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        party._remove_member(member.id)

        if party.me and party.me.leader and member.id != party.me.id:
            await party.refresh_squad_assignments()

        self.client.dispatch_event('party_member_leave', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_KICKED')  # noqa
    async def event_party_member_kicked(self, ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        party._remove_member(member.id)

        if party.me and party.me.leader and member.id != party.me.id:
            await party.refresh_squad_assignments()

        if member.id == self.client.user.id:
            p = await self.client._create_party()

            self.client.party = p

        self.client.dispatch_event('party_member_kick', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_DISCONNECTED')  # noqa
    async def event_party_member_disconnected(self, ctx: EventContext) -> None:
        body = ctx.body
        user_id = body.get('account_id')

        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        # Dont continue processing for old connections
        data = await self.client.http.party_lookup(party.id)
        for member_data in data['members']:
            if member_data['account_id'] == user_id:
                connections = member_data['connections']
                if len(connections) == 1:
                    break

                for connection in connections:
                    if 'disconnected_at' not in connection:
                        return

        member._update_connection(body.get('connection'))
        self.client.dispatch_event('party_member_zombie', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_EXPIRED')  # noqa
    async def event_party_member_expired(self, ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        party._remove_member(member.id)

        if party.me and party.me.leader and member.id != party.me.id:
            await party.refresh_squad_assignments()

        if member.id == self.client.user.id:
            p = await self.client._create_party()
            self.client.party = p

        self.client.dispatch_event('party_member_expire', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_CONNECTED')  # noqa
    async def event_party_member_connected(self, ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        member._update_connection(body.get('connection'))
        if member.id == self.client.user.id:
            party.update_presence()

        self.client.dispatch_event('party_member_reconnect', member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_NEW_CAPTAIN')  # noqa
    async def event_party_new_captain(self, ctx: EventContext) -> None:
        body = ctx.body
        party = ctx.party

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            return

        old_leader = party.leader
        party._update_roles(member)

        party.update_presence()
        self.client.dispatch_event('party_member_promote', old_leader, member)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.PARTY_UPDATED')  # noqa
    async def event_party_updated(self, ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        def _getattr(member, key):
            value = getattr(member, key)
            if callable(value):
                value = value()
            return value

        pre_values = {k: _getattr(party, k) for k in _party_meta_attrs}

        party._update(body)
        self.client.dispatch_event('party_update', party)

        for key, pre_value in pre_values.items():
            value = _getattr(party, key)
            if pre_value != value:
                self.client.dispatch_event(
                    'party_{0}_change'.format(_party_meta_attrs[key] or key),
                    party,
                    pre_value,
                    value
                )

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_STATE_UPDATED')  # noqa
    async def event_party_member_state_updated(self,
                                               ctx: EventContext) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        member = party.get_member(user_id)
        if member is None:
            def check(m):
                return m.id == user_id

            try:
                member = await self.client.wait_for(
                    'internal_party_member_join',
                    check=check,
                    timeout=1
                )
            except asyncio.TimeoutError:
                party_data = await self.client.http.party_lookup(party.id)
                for m_data in party_data['members']:
                    if user_id == m_data['account_id']:
                        member = (await party._update_members(
                            (m_data,),
                            remove_missing=False,
                            fetch_user_data=self.client.fetch_user_data_in_events,  # noqa
                        ))[0]
                        break
                else:
                    if user_id == self.client.user.id:
                        await party._leave()
                        p = await self.client._create_party()
                        self.client.party = p
                    return

                yielding = party.me._default_config.yield_leadership
                if party.me and party.me.leader and not yielding:
                    await party.refresh_squad_assignments()

        def _getattr(member, key):
            value = getattr(member, key)
            if callable(value):
                value = value()
            return value

        should_dispatch_extra_events = member.meta.has_been_updated
        if should_dispatch_extra_events:
            pre_values = {k: _getattr(member, k) for k in _member_meta_attrs}

        member.update(body)
        if len(body['member_state_updated']) > 5 and not member.meta.has_been_updated:  # noqa
            member.meta.has_been_updated = True
            self.client.dispatch_event(
                'internal_initial_party_member_meta',
                member
            )

        if party._default_config.team_change_allowed or not party.me.leader:
            req_j = body['member_state_updated'].get(
                'Default:MemberSquadAssignmentRequest_j'
            )
            if req_j is not None:
                req = json.loads(req_j)['MemberSquadAssignmentRequest']
                version = req.get('version')

                if member.id == self.client.user.id:
                    assignment_version = party.me._assignment_version
                else:
                    assignment_version = member._assignment_version

                if version is not None and version != assignment_version:
                    new_positions = {
                        member.id: req['targetAbsoluteIdx'],
                    }

                    member._assignment_version = version
                    if member.id == self.client.user.id:
                        party.me._assignment_version = version

                    swap_member_id = req['swapTargetMemberId']
                    if swap_member_id != 'INVALID':
                        new_positions[swap_member_id] = req['startingAbsoluteIdx']  # noqa

                    if party.me.leader:
                        await party.refresh_squad_assignments(
                            new_positions=new_positions
                        )

                    try:
                        self.client.dispatch_event(
                            'party_member_team_swap',
                            *[party._members.get(k) for k in (member.id, swap_member_id)]  # noqa
                        )
                    except KeyError:
                        pass

        self.client.dispatch_event('party_member_update', member)

        # Only dispatch the events below if the update is not the initial
        # party join one.
        if not should_dispatch_extra_events:
            return

        def _dispatch(key, member, pre_value, value):
            self.client.dispatch_event(
                'party_member_{0}_change'.format(key),
                member,
                pre_value,
                value
            )

        def compare(a, b):
            def construct_set(v):
                return set(itertools.chain(
                    *[list(x.values()) if isinstance(x, dict) else (x,)
                      for x in v]
                ))

            if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
                return construct_set(a) == construct_set(b)
            return a == b

        for key, pre_value in pre_values.items():
            value = _getattr(member, key)
            if not compare(pre_value, value):
                _dispatch(key, member, pre_value, value)

                if key == 'playlist_selection':
                    self.client.dispatch_event(
                        'party_playlist_change',
                        self.client.party,
                        (pre_value, ''),
                        (value, '')
                    )

                    if self.client.auto_update_status:
                        self.client.loop.create_task(
                            self.client.auto_update_status_text()
                        )

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.MEMBER_REQUIRE_CONFIRMATION')  # noqa
    async def event_party_member_require_confirmation(self,
                                                      ctx: EventContext
                                                      ) -> None:
        body = ctx.body

        user_id = body.get('account_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        data = self.client.get_user(user_id)
        if data is None:
            if self.client.fetch_user_data_in_events:
                data = await self.client.fetch_user(user_id, raw=True)
        else:
            data = data.get_raw()

        user = self.client.store_user({
            **(data or {}),
            'id': user_id,
        })
        confirmation = PartyJoinConfirmation(self.client, party, user, body)

        # Automatically confirm if event is received but no handler is found.
        if not self.client._event_has_destination('party_member_confirm'):
            return await confirmation.confirm()

        self.client.dispatch_event('party_member_confirm', confirmation)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.INITIAL_INTENTION')  # noqa
    async def event_party_join_request_received(self, ctx: EventContext) -> None:  # noqa
        body = ctx.body

        user_id = body.get('requester_id')
        if user_id != self.client.user.id:
            await self.client._join_party_lock.wait()

        party = self.client.party

        if party is None:
            return

        if party.id != body.get('party_id'):
            return

        friend = self.client.get_friend(user_id)
        if friend is None:
            return

        request = PartyJoinRequest(
            self.client,
            party,
            friend,
            body
        )
        self.client.dispatch_event('party_join_request', request)

    @EventDispatcher.event('com.epicgames.social.party.notification.v0.INVITE_DECLINED')  # noqa
    async def event_party_invite_declined(self, ctx: EventContext) -> None:
        body = ctx.body

        friend = self.client.get_friend(body['invitee_id'])
        if friend is not None:
            self.client.dispatch_event('party_invite_decline', friend)

    @EventDispatcher.presence()
    async def process_presence(self, user_id: str,
                               platform: str,
                               type_: str,
                               status: str,
                               show: str) -> None:
        try:
            data = json.loads(status)

            ch = data.get('Status', '') != ''

            is_dict = isinstance(data.get('Properties', {}), dict)
            if (not ch or 'bIsPlaying' not in data or not is_dict):
                return
        except ValueError:
            return

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

        is_available = type_ is None or type_ == 'available'

        try:
            away = AwayStatus(show)
        except ValueError:
            away = AwayStatus.ONLINE

        _pres = Presence(
            self.client,
            user_id,
            platform,
            is_available,
            away,
            data
        )

        if _pres.party is not None:
            try:
                display_name = _pres.party.raw['sourceDisplayName']
                if display_name != _pres.friend.display_name:
                    _pres.friend._update_display_name(display_name)
            except (KeyError, AttributeError):
                pass

        before_pres = friend.last_presence

        if not is_available and friend.is_online():
            friend._update_last_logout(datetime.datetime.utcnow())

            try:
                del self.client._presences[user_id]
            except KeyError:
                pass

        else:
            self.client._presences[user_id] = _pres

        self.client.dispatch_event('friend_presence', before_pres, _pres)

    # def on_stream_established(self) -> None:
    #     self.client.dispatch_event('xmpp_session_establish')
    #
    #     async def on_establish():
    #         # Just incase the recover task hangs we don't want it
    #         # running forever in the background until a new close is
    #         # dispatched potentially fucking shit up big time.
    #         task = self._reconnect_recover_task
    #         if task is not None and not task.done():
    #             try:
    #                 await asyncio.wait_for(task, timeout=20)
    #             except asyncio.TimeoutError:
    #                 pass
    #
    #     async def run_reconnect():
    #         now = datetime.datetime.utcnow()
    #         secs = (now - self._last_disconnected_at).total_seconds()
    #         if secs >= self.client.default_party_member_config.offline_ttl:
    #             return await self.client._create_party()
    #
    #         await self.client._reconnect_to_party()
    #
    #     if self._is_suspended:
    #         self.client.dispatch_event('xmpp_session_reconnect')
    #         self.client.loop.create_task(run_reconnect())
    #
    #     self._is_suspended = False
    #     self.client.loop.create_task(on_establish())
    #
    # def on_stream_suspended(self, reason: Optional[Exception]) -> None:
    #     jid = self.xmpp_client.local_jid
    #     resource = jid.resource[:-32] + (uuid.uuid4().hex).upper()
    #     self.xmpp_client._local_jid = jid.replace(resource=resource)
    #
    #     def on_events_recovered(*args):
    #         self._reconnect_recover_task = None
    #
    #     self._reconnect_recover_task = task = self.client.loop.create_task(
    #         self.client.recover_events(
    #             refresh_caches=True,
    #             wait_for_close=False
    #         )
    #     )
    #     task.add_done_callback(on_events_recovered)
    #
    #     if self.client.party is not None:
    #         self._last_known_party_id = self.client.party.id
    #
    #     self._is_suspended = True
    #     self.client.dispatch_event('xmpp_session_lost')
    #
    # def on_stream_destroyed(self, reason: Optional[Exception] = None) -> None:
    #     if not self._is_suspended:
    #         task = self._reconnect_recover_task
    #         if task is not None and not task.cancelled():
    #             task.cancel()
    #
    #     self._last_disconnected_at = datetime.datetime.utcnow()
    #     self.client.dispatch_event('xmpp_session_close')
    #
    # def setup_callbacks(self) -> None:
    #     client = self.xmpp_client
    #
    #     client.on_stream_established.connect(self.on_stream_established)
    #     client.on_stream_suspended.connect(self.on_stream_suspended)
    #     client.on_stream_destroyed.connect(self.on_stream_destroyed)

    async def ping_watchdog(self) -> None:
        while self._connected:
            log.debug(f'last pong: {self._last_pong}')
            if (
                self._last_pong is not None and
                datetime.datetime.now() - self._last_pong
                > datetime.timedelta(seconds=20)
            ):
                log.debug(
                    'No ping response in 20 second, '
                    'assuming dead connection and restarting.'
                )
                await self.restart()

            await asyncio.sleep(5)

    async def xmpp_send(self, data: str) -> None:
        if self.websocket.closed:
            raise ConnectionError("Attempted to write to closed websocket.")

        try:
            await asyncio.wait_for(
                self.websocket.send_str(data),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            log.debug('XMPP send timed out, restarting now...')
            await self.restart()
        except aiohttp.client_exceptions.ClientConnectionResetError:
            log.debug('Disconnected from websocket, restarting now...')
            await self.restart()
        except Exception as e:
            log.debug(f'Unknown XMPP send error: {e}')
            raise

    async def loop_ping(self) -> None:
        while self._connected:
            log.debug('Sending XMPP ping')
            await self.xmpp_send(
                "<iq type='get' id='ping'><ping xmlns='urn:xmpp:ping'/></iq>"
            )
            log.debug('Sent XMPP ping')
            await asyncio.sleep(10)

    async def parse_message(self, raw: str) -> None:
        if '<presence' not in raw:
            log.debug(f'Received websocket message - {raw}')

        if "<stream:features" in raw and not self._authed:
            sasl_msg = base64.b64encode(
                f"\x00{self.client.user.id}\x00{self.client.auth.access_token}".encode()
            ).decode()

            await self.xmpp_send(
                f"<auth xmlns='urn:ietf:params:xml:ns:xmpp-sasl' mechanism='PLAIN'>{sasl_msg}</auth>"
            )

        elif "<success" in raw:
            self._authed = True
            self.client.dispatch_event('xmpp_session_establish')

            await self.xmpp_send(
                "<open xmlns='urn:ietf:params:xml:ns:xmpp-framing' to='prod.ol.epicgames.com' version='1.0' />"
            )

        elif raw.startswith("<stream:features") and "xmpp-bind" in raw:
            self._bound = True
            await self.xmpp_send(
                f"<iq type='set' id='bind_1'>"
                f"<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'>"
                f"<resource>{self.resource}</resource>"
                f"</bind></iq>"
            )
        elif 'type="result"' in raw and 'id="bind_1"' in raw:
            await self.xmpp_send(
                "<iq type='set' id='sess_1'><session xmlns='urn:ietf:params:xml:ns:xmpp-session'/></iq>"
            )
            self._ping_task = self.client.loop.create_task(self.loop_ping())
            self._watchdog_task = self.client.loop.create_task(
                self.ping_watchdog()
            )
            self._presence_task = self.client.loop.create_task(
                self.presence_manager()
            )

            self._ready = True
        elif 'type="result"' in raw and 'id="ping"' in raw:
            self._last_pong = datetime.datetime.now()
            self.client.dispatch_event('internal_xmpp_session_pong')
            log.debug(f'Received XMPP pong')
        else:
            ret = self.xml_processor.process(raw)

            if ret is None:
                return
            elif ret is False:
                # aioxmpp used self.stream.data_received(msg.data)
                # now nothing to feed here, so just ignore gracefully
                return
            else:
                type_ = ret[0]
                if type_ == "presence":
                    EventDispatcher.process_presence(self.client, *ret[1])
                elif type_ == "message":
                    EventDispatcher.process_event(self.client, *ret[1])
                else:
                    log(f"Unhandled XML type: {type_}")

    async def presence_manager(self) -> None:
        stanza = ""
        while self._connected:
            if self.stanza != stanza:
                await self.xmpp_send(self.stanza)
                stanza = self.stanza
            await asyncio.sleep(1)

    async def connect_to_xmpp(self) -> None:
        log.debug('Attempting to connect to XMPP...')
        while True:
            try:
                async with self.http_session.ws_connect(
                    "wss://xmpp-service-prod.ol.epicgames.com",
                    headers={
                        "Authorization": f"Bearer {self.client.auth.access_token}",
                        "Sec-WebSocket-Protocol": "xmpp"
                    },
                ) as websocket:
                    self.websocket = websocket
                    self._connected = True

                    await self.xmpp_send(
                        "<open xmlns='urn:ietf:params:xml:ns:xmpp-framing' to='prod.ol.epicgames.com' version='1.0' />"
                    )

                    async for msg in websocket:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            await self.parse_message(msg.data)
            except aiohttp.client_exceptions.ClientConnectorDNSError:
                log.debug(
                    'DNS error when attempting to connect to XMPP, '
                    'retrying in 5 seconds..'
                )
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                log.debug("XMPP connect task cancelled")
                return
            finally:
                await self._close(close_http=False)

    async def run(self) -> None:
        if self._xmpp_task and not self._xmpp_task.done():
            return

        self.http_session = aiohttp.ClientSession()
        self._xmpp_task = self.client.loop.create_task(self.connect_to_xmpp())

        # need to replace with asyncio event
        while not self._ready:
            await asyncio.sleep(1)

    async def restart(self) -> None:
        if self._restarting:
            return

        self._restarting = True

        log.debug('Reconnecting to XMPP...')

        await self._close()

        if self._xmpp_task:
            self._xmpp_task.cancel()
            try:
                await self._xmpp_task
            except asyncio.CancelledError:
                pass
            self._xmpp_task = None

        await self.run()

        await asyncio.sleep(2)
        await self.client._reconnect_to_party()

        self._restarting = False

    async def _close(self, close_http: bool = True) -> None:
        log.debug('Attempting to close xmpp client')

        self._ready = False
        self._connected = False
        self._authed = False

        tasks = [
            self._presence_task,
            self._ping_task,
            self._watchdog_task
        ]
        for task in tasks:
            if task:
                task.cancel()

        self._presence_task = None
        self._ping_task = None
        self._watchdog_task = None

        if self.websocket is not None and not self.websocket.closed:
            try:
                await asyncio.wait_for(self.websocket.close(), timeout=1.0)
            except Exception:
                pass

        self.websocket = None

        if self.http_session and close_http:
            await self.http_session.close()

            self.http_session = None

        # # let loop run one iteration for events to be dispatched
        # await asyncio.sleep(0)

        self.client.dispatch_event('xmpp_session_close')
        log.debug('Successfully closed xmpp client')


    def set_presence(self, *,
                     status: Optional[Union[str, dict]] = None,
                     show: Optional[str]) -> None:
        if status is None:
            self.stanza = "<presence/>"
        else:
            if isinstance(status, dict):
                _status = status
            elif self.client.party:
                _status = self.client.party.construct_presence(text=status)
            else:
                _status = {
                    "Status": status,
                    "ProductName": "Fortnite"
                }

            self.stanza = (
                f"<presence from='{self.local_jid}'>"
                f"<status>{json.dumps(_status)}</status>"
                f"<show>{show}</show>"
                f"</presence>"
            )

    async def send_presence(
        self,
        to: Optional[str] = None,
        status: Optional[Union[str, dict]] = None,
        show: Optional[str] = None,
    ) -> None:
        if status is None:
            status_json = None
        elif isinstance(status, str):
            if self.client.party:
                status_json = json.dumps(
                    self.client.party.construct_presence(text=status)
                )
            else:
                status_json = json.dumps({"Status": status})
        elif isinstance(status, dict):
            status_json = json.dumps(status)
        else:
            raise TypeError("status must be None, str or dict")

        to_attr = f" to='{to}'" if to else ""
        show_tag = f"<show>{show}</show>" if show else ""
        status_tag = f"<status>{status_json}</status>" if status_json else ""

        presence = f"<presence{to_attr}>{show_tag}{status_tag}</presence>"

        await self.xmpp_send(presence)

    async def get_presence(self, jid: str):
        await self.send_presence_probe(jid)

        # Wait for incoming friend presence event
        _, after = await self.client.wait_for(
            'friend_presence',
            check=lambda b, a: a.friend.id == jid.split("@")[0]
        )
        return after

    async def send_presence_probe(self, to: str) -> None:
        await self.xmpp_send(f"<presence to='{to}' type='probe'/>")

