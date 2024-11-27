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

import re
import datetime
import json

from typing import TYPE_CHECKING, Optional, List

from .utils import from_iso

if TYPE_CHECKING:
    from .client import Client


class CreativeIslandRating:
    """Creative island rating."""
    def __init__(self, board: str, data: dict) -> None:
        self._board = board
        self._descriptors = data['descriptors']
        self._rating_overridden = data['rating_overridden']
        self._rating = data['rating']
        self._initial_rating = data['initial_rating']
        self._interactive_elements = data['interactive_elements']

        self._raw = data

    def __str__(self) -> str:
        return self._rating

    def __repr__(self) -> str:
        return f'<CreativeIslandRating board={self.board!r} ' \
               f'rating={self.rating!r}>'

    @property
    def board(self) -> str:
        """:class:`str`: The name of the board of which the rating is from."""
        return self._board

    @property
    def descriptors(self) -> str:
        """:class:`str`: Rating descriptors of the island."""
        return self._descriptors

    @property
    def rating(self) -> str:
        """:class:`str`: The rating of the island."""
        return self._rating

    @property
    def initial_rating(self) -> str:
        """:class:`str`: The initial rating of the island."""
        return self._initial_rating

    @property
    def interactive_elements(self) -> str:
        """:class:`str`: Interactive elements of the island."""
        return self._interactive_elements


class CreativeIsland:
    """Creative island."""
    def __init__(self, client: 'Client', data: dict) -> None:
        self.client = client

        self._creator_name = data['creatorName']
        self._creator_account_id = data['accountId']
        self._mnemonic = data['mnemonic']
        self._name = data['metadata']['title']
        self._image_url = data['metadata']['image_url']
        self._version = data['version']
        self._active = data['active']
        self._created = from_iso(data['created'])
        self._published = from_iso(data['published'])
        self._description_tags = data['descriptionTags']
        self._type = data['linkType']
        self._lobby_background_image = data['metadata'].get(
            'lobby_background_image_urls', {'url': None}
        )['url']
        self._creator_sac_slug = data['metadata'].get('support_code')
        self._tagline = data['metadata'].get('tagline')
        self._ratings = data['metadata'].get('ratings', {"boards": {}})

        self._raw = data

    def __str__(self) -> str:
        return self._title

    def __repr__(self) -> str:
        return f'<CreativeIsland name={self.name!r} mnemonic={self.mnemonic!r}>'

    @property
    def creator_name(self) -> str:
        """:class:`str`: The name of the island creator."""
        return self._creator_name

    @property
    def creator_account_id(self) -> str:
        """:class:`str`: The account id of the island creator."""
        return self._creator_account_id

    @property
    def mnemonic(self) -> str:
        """:class:`str`: The mnemonic of the island, either being island code or playlist id."""
        return self._mnemonic

    @property
    def name(self) -> str:
        """:class:`str`: The name of the island."""
        return self._name

    @property
    def image_url(self) -> str:
        """:class:`str`: The image URL of the island."""
        return self._image_url

    @property
    def version(self) -> int:
        """:class:`int`: The current iteration of the island."""
        return self._version

    @property
    def active(self) -> bool:
        """:class:`bool`: Whether or not the island is active."""
        return self._active

    @property
    def created(self) -> datetime.datetime:
        """:class:`datetime.datetime`: The UTC time the island was created."""
        return self._created

    @property
    def published(self) -> datetime.datetime:
        """:class:`datetime.datetime`: The UTC time the island was published."""
        return self._published

    @property
    def description_tags(self) -> list:
        """:class:`list`: List of description tags."""
        return self._description_tags

    @property
    def lobby_background_image(self) -> str:
        """:class:`str`: The image URL of the lobby background, if none Fortnite will use the default."""
        return self._lobby_background_image

    @property
    def creator_sac_slug(self) -> str:
        """:class:`str`: The Support-a-Creator slug of the island creator."""
        return self._creator_sac_slug

    @property
    def tagline(self) -> str:
        """:class:`str`: The tagline of the island."""
        return self._tagline

    @property
    def ratings(self) -> List[CreativeIslandRating]:
        """List[:class:`CreativeIslandRating`]: A list containing data about
        all age ratings for the island.
        """
        return [CreativeIslandRating(board=board, data=data) for board, data in self._ratings['boards'].items()]

    @property
    def is_creative_island(self) -> bool:
        """:class:`bool`: Returns ``True`` if the island is a creative map,
        ``False`` if it is a playlist."""
        return self._type in ('valkyrie:application', 'Creative:Island')
