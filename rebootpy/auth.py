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

import datetime
import asyncio
import logging
import uuid
import time
import webbrowser
import json

from random import randint
from aioconsole import ainput
from typing import TYPE_CHECKING, Optional, Any, List

from .errors import AuthException, HTTPException
from .typedefs import StrOrMaybeCoro
from .utils import from_iso, to_iso

if TYPE_CHECKING:
    from .client import BasicClient

log = logging.getLogger(__name__)
_prompt_lock = asyncio.Lock()


class Auth:
    def __init__(self, **kwargs: Any) -> None:
        self.ios_token = kwargs.get('ios_token', 'M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=')  # noqa
        self.fortnite_token = kwargs.get('fortnite_token', 'ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=')  # noqa
        self.device_id = getattr(self, 'device_id', None) or uuid.uuid4().hex

    def initialize(self, client: 'BasicClient') -> None:
        self.client = client
        self._refresh_event = asyncio.Event()
        self._refresh_lock = asyncio.Lock()
        self.refresh_i = 0

    @property
    def ios_authorization(self) -> str:
        return 'bearer {0}'.format(self.ios_access_token)

    @property
    def chat_authorization(self) -> str:
        return 'bearer {0}'.format(self.chat_access_token)

    @property
    def authorization(self) -> str:
        return 'bearer {0}'.format(self.access_token)

    @property
    def identifier(self) -> str:
        raise NotImplementedError

    def eula_check_needed(self) -> bool:
        return True

    async def authenticate(self, **kwargs) -> dict:
        raise NotImplementedError

    async def _authenticate(self, priority: int = 0) -> None:
        max_attempts = 3
        for i in range(max_attempts):
            try:
                log.info('Running authentication.')
                return await self.authenticate(priority=priority)
            except HTTPException as exc:
                codes = (
                    ('errors.com.epicgames.account.oauth.'
                     'exchange_code_not_found'),
                    ('errors.com.epicgames.account.oauth.'
                     'expired_exchange_code_session'),
                )
                if exc.message_code in codes:
                    if i != max_attempts-1:
                        continue

                raise
            except asyncio.CancelledError:
                return False

    async def reauthenticate(self, priority: int = 0) -> dict:
        raise NotImplementedError

    async def get_eula_version(self, **kwargs: Any) -> int:
        data = await self.client.http.eulatracking_get_data(**kwargs)
        return data['version'] if isinstance(data, dict) else 0

    async def accept_eula(self, **kwargs: Any) -> None:
        version = await self.get_eula_version(**kwargs)
        if version != 0:
            await self.client.http.eulatracking_accept(
                version,
                **kwargs
            )

            try:
                await self.client.http.fortnite_grant_access(**kwargs)
            except HTTPException as e:
                if e.message_code != 'errors.com.epicgames.bad_request':
                    raise

    def _update_ios_data(self, data: dict) -> None:
        self.ios_access_token = data['access_token']
        self.ios_expires_in = data['expires_in']
        self.ios_expires_at = from_iso(data["expires_at"])
        self.ios_token_type = data['token_type']
        self.ios_refresh_token = data['refresh_token']
        self.ios_refresh_expires = data['refresh_expires']
        self.ios_refresh_expires_at = data['refresh_expires_at']
        self.ios_account_id = data['account_id']
        self.ios_client_id = data['client_id']
        self.ios_internal_client = data['internal_client']
        self.ios_client_service = data['client_service']
        self.ios_app = data['app']
        self.ios_in_app_id = data['in_app_id']

    def _update_chat_data(self, data: dict) -> None:
        self.chat_access_token = data['access_token']
        self.chat_expires_in = data['expires_in']
        self.chat_expires_at = from_iso(data["expires_at"])
        self.chat_token_type = data['token_type']
        self.chat_refresh_token = data['refresh_token']
        self.chat_client_id = data['client_id']
        self.chat_application_id = data['application_id']
        self.chat_scope = data['scope']

    def _update_data(self, data: dict) -> None:
        self.access_token = data['access_token']
        self.expires_in = data['expires_in']
        self.expires_at = from_iso(data["expires_at"])
        self.token_type = data['token_type']
        self.refresh_token = data['refresh_token']
        self.refresh_expires = data.get('refresh_expires', 28800)
        self.refresh_expires_at = data.get(
            'refresh_expires_at',
            datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        )
        self.account_id = data['account_id']
        self.client_id = data['client_id']
        self.internal_client = data['internal_client']
        self.client_service = data['client_service']
        self.app = data['app']
        self.in_app_id = data['in_app_id']

    async def grant_refresh_token(self, refresh_token: str, auth_token: str, *,
                                  priority: int = 0) -> dict:
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        return await self.client.http.account_oauth_grant(
            auth='basic {0}'.format(auth_token),
            data=payload,
            priority=priority
        )

    async def grant_chat_refresh_token(self,
                                       refresh_token: str,
                                       priority: int = 0) -> dict:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "deployment_id": self.client.deployment_id
        }

        return await self.client.http.account_chat_oauth_grant(
            auth='basic {0}'.format(self.fortnite_token),
            data=payload,
            priority=priority
        )

    async def get_exchange_code(self, *,
                                auth='IOS_ACCESS_TOKEN',
                                priority: int = 0) -> str:
        data = await self.client.http.account_get_exchange_data(
            auth=auth,
            priority=priority
        )
        return data['code']

    async def exchange_code_for_session(self, token: str, code: str, *,
                                        priority: int = 0) -> dict:
        payload = {
            'grant_type': 'exchange_code',
            'exchange_code': code,
            'token_type': 'eg1',
        }

        return await self.client.http.account_oauth_grant(
            auth='basic {0}'.format(token),
            data=payload,
            priority=priority
        )

    async def get_ios_client_credentials(self):
        payload = {
            'grant_type': 'client_credentials'
        }

        return await self.client.http.account_oauth_grant(
            auth='IOS_BASIC_TOKEN',
            data=payload
        )

    async def kill_token(self, token: str) -> None:
        await self.client.http.account_sessions_kill_token(
            token,
            auth='bearer {0}'.format(token)
        )

    async def kill_other_sessions(self, auth: str = 'IOS_ACCESS_TOKEN', *,
                                  priority: int = 0) -> None:
        await self.client.http.account_sessions_kill(
            'OTHERS_ACCOUNT_CLIENT_SERVICE',
            auth=auth,
            priority=priority
        )
        log.debug('Killing other sessions')

    def refresh_loop_running(self):
        try:
            task = self.client._refresh_task
        except AttributeError:
            return False

        return task is not None and not task.cancelled()

    async def schedule_token_refresh(self) -> None:
        min_expires_at = min([self.ios_expires_at, self.expires_at])
        subtracted = min_expires_at - datetime.datetime.utcnow()
        self.token_timeout = (subtracted).total_seconds() - 300
        await asyncio.sleep(self.token_timeout)

    async def run_refresh_loop(self) -> None:
        loop = self.client.loop

        while True:
            self._refresh_event.clear()
            _, p = await asyncio.wait((
                loop.create_task(self._refresh_event.wait()),
                loop.create_task(self.schedule_token_refresh())
            ), return_when=asyncio.FIRST_COMPLETED)

            for pending in p:
                if not pending.cancelled():
                    pending.cancel()

            await self.do_refresh()

    async def do_refresh(self) -> None:
        reauth_lock = self.client._reauth_lock
        reauth_lock.priority += 1
        forced = reauth_lock.locked()

        try:
            if not forced:
                await self._refresh_lock.acquire()

            log.debug('Refreshing session')
            self.client._refresh_times.append(time.time())

            try:
                data = await self.grant_refresh_token(
                    self.ios_refresh_token,
                    self.ios_token,
                    priority=reauth_lock.priority
                )
                self._update_ios_data(data)

                data = await self.grant_refresh_token(
                    self.refresh_token,
                    self.fortnite_token,
                    priority=reauth_lock.priority
                )
                self._update_data(data)

                data = await self.grant_chat_refresh_token(
                    self.chat_refresh_token,
                    priority=reauth_lock.priority
                )
                self._update_chat_data(data)
            except (HTTPException, AttributeError) as exc:
                m = 'errors.com.epicgames.account.auth_token.' \
                    'invalid_refresh_token'
                if isinstance(exc, HTTPException) and exc.message_code != m:
                    raise

                log.debug(
                    'Invalid refresh token was supplied. Attempting to '
                    'reconnect if possible.'
                )
                try:
                    await self.reauthenticate(
                        priority=reauth_lock.priority
                    )
                except NotImplementedError:
                    raise exc

                log.debug('Successfully reauthenticated.')

            await self.client.dispatch_and_wait_event('internal_auth_refresh')

            self.refresh_i += 1
            log.debug('Sessions was successfully refreshed.')
            self.client.dispatch_event('auth_refresh')

        finally:
            if not forced:
                self._refresh_lock.release()

    async def run_refresh(self) -> None:
        self._refresh_event.set()
        await self.client.wait_for('auth_refresh')

    def refreshing(self) -> bool:
        return self._refresh_lock.locked()

    async def fetch_device_auths(self) -> List[dict]:
        # Return payload:
        # [
        #     {
        #         "deviceId": "01fbc14162634294a1db59ddced3c10c",
        #         "accountId": "4a6313cbbe7d432b8132b5ee67ad53fa",
        #         "userAgent": "EpicGamesLauncher/++Fortnite+Release-12.00-CL-11586896 Windows/10.0.17134.1.768.64bit",  # noqa
        #         "created": {
        #             "location": "Oslo, Norway",
        #             "ipAddress": "",  # ipv4 address
        #             "dateTime": "2020-04-25T20:38:57.570Z"
        #         },
        #         "lastAccess": {
        #             "location": "Oslo, Norway",
        #             "ipAddress": "",  # ipv4 address
        #             "dateTime": "2020-05-13T16:33:43.075Z"
        #         }
        #     }
        # ]
        return await self.client.http.account_get_device_auths(
            self.ios_account_id
        )

    async def generate_device_auth(self) -> dict:
        # Return payload:
        # {
        #     "deviceId": "e2ba6aa72411468ba4fee016086809d7",
        #     "accountId": "4a6313cbbe7d432b8132b5ee67ad53fa",
        #     "secret": "",  # 32 char (not hex)
        #     "userAgent": "EpicGamesLauncher/++Fortnite+Release-12.00-CL-11586896 Windows/10.0.17134.1.768.64bit",  # noqa
        #     "created": {
        #         "location": "Oslo, Norway",
        #         "ipAddress": "",  # ipv4
        #         "dateTime": "2020-05-13T18:32:07.601Z"
        #     }
        # }
        return await self.client.http.account_generate_device_auth(
            self.ios_account_id
        )

    async def delete_device_auth(self, device_id: str) -> None:
        await self.client.http.account_delete_device_auth(
            self.ios_account_id,
            device_id
        )

class ExchangeCodeAuth(Auth):
    """Authenticates by an exchange code.

    .. note::

        The method to get an exchange code has been significantly harder
        since epic patched the old method of copying the code from one of
        their own endpoints that could be requested easily in a browser.
        To obtain an exchange code it is recommended to provide a custom
        solution like running a selenium process where you log in on
        https://epicgames.com and then redirect to /id/api/exchange/generate.
        You can then return the exchange code. You can put this solution
        in a function and then pass this to ``exchange_code``.

    .. note::

        An exchange code only works for a single login within a short
        timeframe (300 seconds). Therefore you need to get a new code for each
        login. You can get a new code by refreshing the site.

    Parameters
    ----------
    code: Union[:class:`str`, Callable, Awaitable]
        The exchange code or a function/coroutine that when called returns
        the exchange code.
    device_id: Optional[:class:`str`]
        A 32 char hex string representing your device.
    ios_token: Optional[:class:`str`]
        The ios token to use with authentication. You should generally
        not need to set this manually.
    fortnite_token: Optional[:class:`str`]
        The fortnite token to use with authentication. You should generally
        not need to set this manually.
    """
    def __init__(self, code: StrOrMaybeCoro,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.code = code
        self.resolved_code = None

    async def resolve(self, code: StrOrMaybeCoro) -> str:
        if isinstance(code, str):
            return code

        elif asyncio.iscoroutinefunction(code):
            res = await code()
        else:
            res = code()

        if not isinstance(res, str):
            raise TypeError('Return type of callable func/coro must be str')

        return res

    @property
    def identifier(self) -> str:
        return self.resolved_code

    async def ios_authenticate(self) -> dict:
        log.info('Exchanging code.')
        self.resolved_code = await self.resolve(self.code)

        try:
            data = await self.exchange_code_for_session(
                self.ios_token,
                self.resolved_code
            )
        except HTTPException as e:
            m = 'errors.com.epicgames.account.oauth.exchange_code_not_found'
            if e.message_code == m:
                raise AuthException(
                    'Invalid exchange code supplied',
                    e
                ) from e

            raise

        return data

    async def authenticate(self, **kwargs) -> None:
        data = await self.ios_authenticate()
        self._update_ios_data(data)

        if self.client.kill_other_sessions:
            await self.kill_other_sessions()

        code = await self.get_exchange_code()
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
        )
        self._update_chat_data(data)


class AuthorizationCodeAuth(ExchangeCodeAuth):
    """Authenticates by exchange code.

    You can get the code from `here
    <https://www.epicgames.com/id/api/redirect?
    clientId=3f69e56c7649492c8cc29f1af08a8a12&responseType=code>`_ by logging
    in and copying the code from the redirectUrl's query parameters. If you
    are already logged in and want to change accounts, simply log out at
    https://www.epicgames.com, log in to the new account and then enter the
    link above again to generate an authorization code.

    **How to get an authorization code:**

    .. image:: https://raw.githubusercontent.com/xMistt/rebootpy/main/docs/resources/images/authorization_code.png

    .. note::

        An authorization code only works for a single login within a short
        timeframe (300 seconds). Therefore you need to get a new code for each
        login. You can get a new code by refreshing the site.

    Parameters
    ----------
    code: Union[:class:`str`, Callable, Awaitable]
        The authorization code or a function/coroutine that when called returns
        the authorization code.
    device_id: Optional[:class:`str`]
        A 32 char hex string representing your device.
    ios_token: Optional[:class:`str`]
        The ios token to use with authentication. You should generally
        not need to set this manually.
    fortnite_token: Optional[:class:`str`]
        The fortnite token to use with authentication. You should generally
        not need to set this manually.
    """
    def __init__(self, code: StrOrMaybeCoro,
                 **kwargs: Any) -> None:
        super().__init__(code, **kwargs)

    async def ios_authenticate(self) -> dict:
        self.resolved_code = await self.resolve(self.code)

        payload = {
            'grant_type': 'authorization_code',
            'code': self.resolved_code,
        }

        try:
            data = await self.client.http.account_oauth_grant(
                auth='basic {0}'.format(self.ios_token),
                data=payload
            )
        except HTTPException as e:
            m = 'errors.com.epicgames.account.oauth.authorization_code_not_found'  # noqa
            if e.message_code == m:
                raise AuthException(
                    'Invalid authorization code supplied',
                    e
                ) from e

            raise

        return data


class DeviceAuth(Auth):
    """Authenticate with device auth details.

    .. note::

        When an account's password is reset, all device authentications
        associated with the account are removed. If your device ID and secret 
        are compromised, resetting your password will invalidate all
        authentication data,  making it useless to anyone who may have
        accessed the leaked data.

    Parameters
    ----------
    device_id: :class:`str`
        The device id.
    account_id: :class:`str`
        The account's id.
    secret: :class:`str`
        The secret.
    ios_token: Optional[:class:`str`]
        The ios token to use with authentication. You should generally
        not need to set this manually.
    fortnite_token: Optional[:class:`str`]
        The fortnite token to use with authentication. You should generally
        not need to set this manually.
    """
    def __init__(self, device_id: str,
                 account_id: str,
                 secret: str,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret

    @property
    def identifier(self) -> str:
        return self.account_id

    def eula_check_needed(self) -> bool:
        return False

    async def ios_authenticate(self, priority: int = 0) -> dict:
        payload = {
            'grant_type': 'device_auth',
            'device_id': self.device_id,
            'account_id': self.account_id,
            'secret': self.secret,
            'token_type': 'eg1'
        }

        try:
            data = await self.client.http.account_oauth_grant(
                auth='basic {0}'.format(self.ios_token),
                data=payload,
                priority=priority
            )
        except HTTPException as exc:
            m = 'errors.com.epicgames.account.invalid_account_credentials'
            if exc.message_code == m:
                raise AuthException(
                    'Invalid device auth details passed.',
                    exc
                ) from exc

            if exc.message_code == 'errors.com.epicgames.oauth.corrective_action_required':
                action = exc.raw.get('correctiveAction')
                log.debug("Corrective action is required: " + action)
                if action == 'DATE_OF_BIRTH':
                    client_credentials = await self.get_ios_client_credentials()
                    client_access_token = client_credentials.get('access_token')

                    random_date = "{:04d}-{:02d}-{:02d}".format(randint(1990, 2002), randint(1, 12), randint(1, 28))

                    await self.client.http.account_put_date_of_birth_correction(
                        continuation=exc.raw.get('continuation'),
                        date_of_birth=random_date,
                        auth='bearer {0}'.format(client_access_token)
                    )
                    return await self.ios_authenticate(priority)
                raise AuthException(
                    'Required corrective action {} is not supported'.format(action),
                    exc
                ) from exc

            raise

        return data

    async def authenticate(self, priority: int = 0) -> None:
        data = await self.ios_authenticate(priority=priority)
        self._update_ios_data(data)
        
        if self.client.kill_other_sessions:
            await self.kill_other_sessions(priority=priority)

        code = await self.get_exchange_code(priority=priority)
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code,
            priority=priority
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
            priority=priority
        )
        self._update_chat_data(data)

    async def reauthenticate(self, priority: int = 0) -> None:
        """Used for reauthenticating if refreshing fails."""
        log.debug('Starting reauthentication.')

        ret = await self.authenticate(priority=priority)
        log.debug('Successfully reauthenicated.')
        return ret


class RefreshTokenAuth(Auth):
    """Authenticates by the passed launcher refresh token.

    Parameters
    ----------
    refresh_token: :class:`str`
        A valid launcher refresh token.
    """
    def __init__(self, refresh_token: str,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._refresh_token = refresh_token

    @property
    def identifier(self) -> str:
        return self._refresh_token

    def eula_check_needed(self) -> bool:
        return False

    async def ios_authenticate(self, priority: int = 0) -> dict:
        data = await self.grant_refresh_token(
            self._refresh_token,
            self.ios_token,
            priority=priority
        )
        return data

    async def authenticate(self, priority: int = 0) -> None:
        data = await self.ios_authenticate(priority=priority)
        self._update_ios_data(data)

        code = await self.get_exchange_code(priority=priority)
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code,
            priority=priority
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
            priority=priority
        )
        self._update_chat_data(data)


class AdvancedAuth(Auth):
    """Authenticates by the available data in the following order:

    1. By :class:`DeviceAuth` if ``device_id``, ``account_id`` and ``secret``
    are present.

    2. :class:`DeviceCodeAuth` is tried if ``prompt_device_code``
    is ``True``.

    3. :class:`ExchangeCodeAuth` is tried if ``exchange_code`` is present
    or if ``prompt_exchange_code`` is ``True``.

    4. :class:`AuthorizationCodeAuth` is tried if ``authorization_code`` is
    present or if ``prompt_authorization_code`` is ``True``.

    If the authentication was not done by step 1, a device auth is
    automatically generated and the details will be dispatched to
    :func:`event_device_auth_generate`. It is important to store
    these values somewhere since they can be used for easier logins.

    If you'd like to deal with the device code link yourself instead of it being printed to console, you can use :func:`event_device_code_generated()`.

    Parameters
    ----------


    exchange_code: Optional[Union[:class:`str`, Callable, Awaitable]]
        The exchange code or a function/coroutine that when called returns
        the exchange code.
    authorization_code: Optional[Union[:class:`str`, Callable, Awaitable]]
        The authorization code or a function/coroutine that when called returns
        the authorization code.
    device_id: Optional[:class:`str`]
        The device id to use for the login.
    account_id: Optional[:class:`str`]
        The account id to use for the login.
    secret: Optional[:class:`str`]
        The secret to use for the login.
    prompt_device_code: :class:`bool`
        If this is set to ``True`` and no exchange code is passed,
        you will be prompted to enter the exchange code in the console
        if needed.

        .. note::

            Both ``prompt_exchange_code`` and ``prompt_authorization_code``
            cannot be True at the same time.
    prompt_exchange_code: :class:`bool`
        If this is set to ``True`` and no exchange code is passed,
        you will be prompted to enter the exchange code in the console
        if needed.

        .. note::

            Both ``prompt_exchange_code`` and ``prompt_authorization_code``
            cannot be True at the same time.
    prompt_authorization_code: :class:`bool`
        If this is set to ``True`` and no authorization code is passed,
        you will be prompted to enter the authorization code in the console
        if needed.

        .. note::

            Both ``prompt_exchange_code`` and ``prompt_authorization_code``
            cannot be True at the same time.
    prompt_code_if_invalid: :class:`bool`
        Whether or not to prompt a code if the device auth details
        was invalid. If this is False then the regular :exc:`AuthException` is
        raised instead.

        .. note::

            This only works if ``prompt_exchange_code`` or
            ``prompt_authorization_code`` is ``True``.
    prompt_code_if_throttled: :class:`bool`
        If this is set to ``True`` and you receive a throttling response,
        you will be prompted to enter a code in the console.

        .. note::

            This only works if ``prompt_exchange_code`` or
            ``prompt_authorization_code`` is ``True``.
    delete_existing_device_auths: :class:`bool`
        Whether or not to delete all existing device auths when a new
        is created.
    ios_token: Optional[:class:`str`]
        The ios token to use with authentication. You should generally
        not need to set this manually.
    fortnite_token: Optional[:class:`str`]
        The fortnite token to use with authentication. You should generally
        not need to set this manually.
    """
    def __init__(self,
                 exchange_code: Optional[StrOrMaybeCoro] = None,
                 authorization_code: Optional[StrOrMaybeCoro] = None,
                 device_id: Optional[str] = None,
                 account_id: Optional[str] = None,
                 secret: Optional[str] = None,
                 prompt_exchange_code: bool = False,
                 prompt_authorization_code: bool = False,
                 prompt_device_code: bool = True,
                 open_link_in_browser: bool = True,
                 prompt_code_if_invalid: bool = False,
                 prompt_code_if_throttled: bool = False,
                 delete_existing_device_auths: bool = False,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.exchange_code = exchange_code
        self.authorization_code = authorization_code
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret

        self.delete_existing_device_auths = delete_existing_device_auths
        self.prompt_exchange_code = prompt_exchange_code
        self.prompt_authorization_code = prompt_authorization_code
        self.prompt_device_code = prompt_device_code
        self.open_link_in_browser = open_link_in_browser

        if self.prompt_exchange_code and self.prompt_authorization_code:
            raise ValueError('Both prompt_exchange_code and '
                             'prompt_authorization_code cannot be True at '
                             'the same time.')

        self.prompt_code_if_invalid = prompt_code_if_invalid
        self.prompt_code_if_throttled = prompt_code_if_throttled
        self.kwargs = kwargs

        self._used_auth = None

    @property
    def identifier(self) -> str:
        return self.account_id or self.authorization_code or self.exchange_code

    def eula_check_needed(self) -> bool:
        return self._used_auth.eula_check_needed()

    def exchange_code_ready(self) -> bool:
        return self.exchange_code is not None

    def authorization_code_ready(self) -> bool:
        return self.authorization_code is not None

    def code_ready(self) -> bool:
        return self.exchange_code_ready() or self.authorization_code_ready()

    def device_auth_ready(self) -> bool:
        return self.device_id and self.account_id and self.secret

    def prompt_enabled(self) -> bool:
        return True in (self.prompt_exchange_code, self.prompt_authorization_code)  # noqa

    def get_prompt_type_name(self) -> str:
        if self.prompt_exchange_code:
            return 'exchange'
        elif self.prompt_authorization_code:
            return 'authorization'

    async def run_exchange_code_authenticate(self) -> dict:
        auth = ExchangeCodeAuth(
            code=self.exchange_code,
            **self.kwargs
        )
        auth.initialize(self.client)
        self._used_auth = auth

        return await auth.ios_authenticate()

    async def run_authorization_code_authenticate(self) -> dict:
        auth = AuthorizationCodeAuth(
            code=self.authorization_code,
            **self.kwargs
        )
        auth.initialize(self.client)
        self._used_auth = auth

        return await auth.ios_authenticate()

    async def run_device_code_authenticate(self) -> dict:
        auth = DeviceCodeAuth(
            open_link_in_browser=self.open_link_in_browser
        )
        auth.initialize(self.client)
        self._used_auth = auth

        return await auth.ios_authenticate()

    async def run_device_authenticate(self, device_id: Optional[str] = None,
                                      account_id: Optional[str] = None,
                                      secret: Optional[str] = None,
                                      *, priority: int = 0
                                      ) -> dict:
        auth = DeviceAuth(
            device_id=device_id or self.device_id,
            account_id=account_id or self.account_id,
            secret=secret or self.secret,
            **self.kwargs
        )
        auth.initialize(self.client)
        self._used_auth = auth

        data = await auth.ios_authenticate(priority=priority)
        self._update_ios_data(data)

        code = await auth.get_exchange_code(priority=priority)
        return await auth.exchange_code_for_session(
            auth.fortnite_token,
            code,
            priority=priority
        )

    async def ios_authenticate(self) -> dict:
        data = None
        prompt_message = ''

        if self.device_auth_ready():
            try:
                return await self.run_device_authenticate()
            except AuthException as exc:
                original = exc.original
                if not self.prompt_enabled() or not self.prompt_code_if_invalid:  # noqa
                    raise

                if isinstance(original, HTTPException):
                    m = 'errors.com.epicgames.account.invalid_account_credentials'  # noqa
                    if original.message_code != m:
                        raise

                prompt_message = 'Invalid device auth details passed. '

        if self.prompt_device_code:
            try:
                data = await self.run_device_code_authenticate()
            except AuthException as exc:
                original = exc.original
                if not self.prompt_enabled() or not self.prompt_code_if_invalid:  # noqa
                    raise

        if data is None:
            prompted = False
            code = None
            if not self.code_ready() and self.prompt_enabled():
                prompted = True
                code_type = self.get_prompt_type_name()
                text = '{0}Please enter a valid {1} code.\n'.format(
                    prompt_message,
                    code_type
                )

                async with _prompt_lock:
                    code = await ainput(
                        text,
                    )

            if (prompted and self.prompt_exchange_code) or self.exchange_code_ready():  # noqa
                self.exchange_code = code or self.exchange_code
                data = await self.run_exchange_code_authenticate()
            else:
                self.authorization_code = code or self.authorization_code
                data = await self.run_authorization_code_authenticate()

        self._update_ios_data(data)

        if self.delete_existing_device_auths:
            tasks = []
            auths = await self.fetch_device_auths()
            for auth in auths:
                tasks.append(self.client.loop.create_task(
                    self.delete_device_auth(
                        auth['deviceId']
                    )
                ))

            if tasks:
                await asyncio.gather(*tasks)

        data = await self.generate_device_auth()
        details = {
            'device_id': data['deviceId'],
            'account_id': data['accountId'],
            'secret': data['secret'],
        }
        self.__dict__.update(details)

        self.client.dispatch_event(
            'device_auth_generate',
            details
        )

        return data

    async def authenticate(self, **kwargs) -> None:
        await self.ios_authenticate()

        if self.client.kill_other_sessions:
            await self.kill_other_sessions()

        code = await self.get_exchange_code()
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
        )
        self._update_chat_data(data)

    async def reauthenticate(self, priority: int = 0) -> None:
        log.debug('Starting reauthentication.')

        await self.run_device_authenticate(
            device_id=self.device_id,
            account_id=self.account_id,
            secret=self.secret,
            priority=priority,
        )

        if self.client.kill_other_sessions:
            await self.kill_other_sessions(priority=priority)

        code = await self.get_exchange_code(priority=priority)
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code,
            priority=priority
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
            priority=priority
        )
        self._update_chat_data(data)
        log.debug('Successfully reauthenticated.')


class DeviceCodeAuth(Auth):
    """Authenticate with device code.

    If you'd like to deal with the device code link yourself instead of it being printed to console, you can use :func:`event_device_code_generated()`.

    Parameters
    ----------
    open_link_in_browser: :class:`bool`
        Whether or not to automatically open the Epic Games login in the default browser.
    ios_token: Optional[:class:`str`]
        The ios token to use with authentication. You should generally
        not need to set this manually.
    switch_token: Optional[:class:`str`]
        The switch token to use with authentication. You should generally
        not need to set this manually.
    fortnite_token: Optional[:class:`str`]
        The fortnite token to use with authentication. You should generally
        not need to set this manually.
    """
    def __init__(self, open_link_in_browser: bool = True,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.switch_token = kwargs.get('switch_token', 'OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3') #noqa
        self.open_link_in_browser = open_link_in_browser

    @property
    def identifier(self) -> str:
        return self.account_id

    def eula_check_needed(self) -> bool:
        return False

    async def ios_authenticate(self, priority: int = 0) -> dict:
        switch_token = await self.client.http.account_oauth_grant(
            auth=f'basic {self.switch_token}',
            data={
                'grant_type': 'client_credentials'
            },
            priority=priority
        )

        device_code = await self.client.http.account_create_device_code(
            auth=f'bearer {switch_token["access_token"]}',
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            priority=priority
        )

        if self.open_link_in_browser:
            webbrowser.open(device_code['verification_uri_complete'], new=1)

        if self.client._event_has_destination('device_code_generated'):
            self.client.dispatch_event(
                'device_code_generated',
                device_code['verification_uri_complete']
            )
        else:
            print(
                f"Please login via {device_code['verification_uri_complete']}"
            )

        while True:
            try:
                exchange_access_token = await self.client.http.account_oauth_grant(
                    auth=f'basic {self.switch_token}',
                    data={
                        "grant_type": "device_code",
                        "device_code": device_code['device_code'],
                        'token_type': 'eg1'
                    },
                    headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                    },
                    priority=priority
                )

                if 'access_token' in exchange_access_token:
                    break
            except HTTPException as exc:
                if exc.message_code == 'errors.com.epicgames.account.oauth.authorization_pending':
                    pass
                elif exc.message_code == 'errors.com.epicgames.not_found':
                    pass
                elif exc.message_code == 'errors.com.epicgames.oauth.corrective_action_required':
                    action = exc.raw.get('correctiveAction')
                    log.debug("Corrective action is required: " + action)
                    if action == 'DATE_OF_BIRTH':
                        client_credentials = await self.get_ios_client_credentials()
                        client_access_token = client_credentials.get('access_token')

                        random_date = "{:04d}-{:02d}-{:02d}".format(randint(1990, 2002), randint(1, 12), randint(1, 28))

                        await self.client.http.account_put_date_of_birth_correction(
                            continuation=exc.raw.get('continuation'),
                            date_of_birth=random_date,
                            auth='bearer {0}'.format(client_access_token)
                        )
                        return await self.ios_authenticate(priority)
                    raise AuthException(
                        'Required corrective action {} is not supported'.format(action),
                        exc
                    ) from exc
                else:
                    raise AuthException(f'Unknown error when checking device code - {exc.message_code}', exc)
                    
            await asyncio.sleep(10)

        exchange_code = await self.client.http.account_get_exchange_data(
            auth=f"bearer {exchange_access_token['access_token']}",
            priority=priority
        )

        data = await self.client.http.account_oauth_grant(
            auth=f'basic {self.ios_token}',
            data={
                "grant_type": "exchange_code",
                "exchange_code": exchange_code['code'],
                'token_type': 'eg1'
            },
            priority=priority
        )

        return data

    async def authenticate(self, priority: int = 0) -> None:
        data = await self.ios_authenticate(priority=priority)
        self._update_ios_data(data)

        if self.client.kill_other_sessions:
            await self.kill_other_sessions(priority=priority)

        code = await self.get_exchange_code(priority=priority)
        data = await self.exchange_code_for_session(
            self.fortnite_token,
            code,
            priority=priority
        )
        self._update_data(data)

        data = await self.grant_chat_refresh_token(
            self.refresh_token,
            priority=priority
        )
        self._update_chat_data(data)

    async def reauthenticate(self, priority: int = 0) -> None:
        """Used for reauthenticating if refreshing fails."""
        log.debug('Starting reauthentication.')

        ret = await self.authenticate(priority=priority)
        log.debug('Successfully reauthenicated.')
        return ret
