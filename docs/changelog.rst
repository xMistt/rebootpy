.. currentmodule:: rebootpy

Changelog
=========

Detailed version changes.
You can also view the changelog of the original library, fortnitepy, `here <https://fortnitepy.readthedocs.io/en/latest/changelog.html>`_.

v0.9.6 (pre-release)
------

Bug Fixes
~~~~~

- Fixed :meth:`ClientPartyMember.set_emote()` not playing emotes & ``PartyMember.emote`` always being ``None`` no matter what.
- Fixed :meth:`ClientPartyMember.set_ready()`.
- Fixed :meth:`ClientParty.set_playlist()`.

v0.9.5
------

Added
~~~~~

- Added ``RankingType.BALLISTIC``
- Added ``RankingType.OG`` & ``RankingType.OG_ZERO_BUILD``
- Added :meth:`ClientPartyMember.set_jam_emote()`
- Added :meth:`ClientPartyMember.set_instruments()`

Bug Fixes
~~~~~

- Fixed an issue where ``Client.user`` couldn't be created.
- Fixed :meth:`Client.fetch_user_by_display_name()` not fetching ``external_auths``.

v0.9.4
------

Changes
~~~~~~~

- :meth:`Client.fetch_ranked_stats()` / :meth:`User.fetch_ranked_stats()` now accepts passing no season which will then automatically fetch the current seasons tracks.
- (**Breaking**) Removed ``SeasonStartTimestamp``, ``SeasonEndTimestamp``, ``BattlePassStat`` and ``Seasons`` to merge them into a new universal enum :class:`Season`. Affected functions (please re-read the documentation if you use these as they have been updated):
    - :meth:`Client.fetch_battlepass_level()`
    - :meth:`Client.fetch_multiple_br_stats`
    - :meth:`Client.fetch_multiple_br_stats_collections`
    - :meth:`Client.fetch_multiple_battlepass_levels`
    - :meth:`Client.fetch_battlepass_level`
    - :meth:`Client.fetch_ranked_stats`
    - :meth:`User.fetch_br_stats`
    - :meth:`User.fetch_br_stats_collection`
    - :meth:`User.fetch_battlepass_level`
    - :meth:`User.fetch_ranked_stats`

    If you were using the old enums, here is how you can replace them:

    - ``SeasonStartTimestamp.C5SOG.value`` -> ``Season.C5SOG.start_timestamp``
    - ``SeasonEndTimestamp.C5SOG.value`` -> ``Season.C5SOG.end_timestamp``
    - ``BattlePassStat.C5SOG.value[0]`` -> ``Season.C5SOG.battlepass_level``
    - ``Seasons.C5SOG`` -> ``Season.C5SOG.ranked_tracks``
- :meth:`Client.set_platform()` won't restart the client anymore and will stay in the same party.

Added
~~~~~

- Added :meth:`Client.fetch_gold_bars()` & :meth:`User.fetch_gold_bars()`
- Added ``StatsCollectionType.CHARACTER``
- [:ref:`Ext Commands <rebootpy_ext_commands>`] Added :attr:`ext.commands.Context.member` & :attr:`ext.commands.Context.friend`
- Added :meth:`ClientPartyMember.set_kicks()`, :meth:`ClientPartyMember.clear_kicks()` & :attr:`PartyMember.kicks`
- Added :func:`event_party_playlist_request()` and :class:`PlaylistRequest` which is used whenever a party member attempts to change the current playlist.
- Added ``Season.C6S1``
.. note::

    The C5SOG reload ranked season has extended into C6S1 resetting in C6S2. This means C5SOG & C6S1 ranked stats will be identical.

Bug Fixes
~~~~~

- Fixed an issue parsing squad assignments if the client wasn't leader.
- Fixed :meth:`Client.fetch_multiple_br_stats_collections` and :meth:`User.fetch_br_stats_collection` incorrectly saying the user was private.
- Fixed an issue where :meth:`Client.restart` would be stuck forever.
- Updated member meta to reflect new season changes.

Removed
~~~~~~~

- Removed all muc (xmpp party chat) related things so if you were relying on any internal events e.g. ``muc_enter``, they have now been removed. This includes ``PartyMember.chatban()`` which has been broken since the party chat changes anyway.

v0.9.3
------

Changes
~~~~~~~

- (**Breaking**) The :class:`SeasonStartTimestamp`, :class:`SeasonEndTimestamp` & :class:`BattlePassStat` enums have had their values renamed from the ``SEASON_?`` format to ``C?S?`` as it got confusing after Chapter 2. (e.g. ``SEASON_29`` is now ``C5S2``)
- (**Breaking**) :meth:`Client.fetch_battlepass_level()` & :meth:`Client.fetch_multiple_battlepass_levels()` now take :class:`BattlePassStat` in their ``season`` parameter instead of :class:`int`.

Added
~~~~~

- Added :meth:`Client.fetch_ranked_stats()` & :meth:`User.fetch_ranked_stats()` (all classes that inherit from :class:`User` like :class:`Friend`, :class:`PartyMember`, etc will all have this method - search ``fetch_ranked_stats`` to see all).
- Added new enum values for the new season:

    - ``SeasonStartTimestamp.C5SOG``

      .. note::

         This timestamp includes the last 6 hours of C5S4 in order to include all stats from the first day of the season. It's the same timestamp that both `FortniteTracker <https://fortnitetracker.com/>`_ and `fortnite.gg <https://fortnite.gg/>`_ use for this season.

    - ``SeasonEndTimestamp.C5S4``
    - ``SeasonEndTimestamp.C5SOG``
    - ``BattlePassStat.C5SOG``

- Added ``kill_other_sessions`` parameter to :class:`BasicClient` & :class:`Client`, if you were manually setting the value of the attribute yourself, this'll still work.

Bug Fixes
~~~~~

- Fixed an issue preventing the use of newer aiohttp versions.
- Fixed an issue with certain headless accounts with missing properties.
- Invalid platforms (thanks to messed up non-official clients) won't raise errors and will instead return ``Platform.UNKNOWN``.
- Updated party meta to reflect the new season changes.

v0.9.2
------

Changes
~~~~~~~

- (**Breaking**) Switched to the Android client as old iOS client is now buggy (i.e. authorisation code no longer works), meaning all previous device auths will now be invalid.
- Updated default status formatting to reflect new changes.
- Reverted help command changes.
- Increased message character limit from 256 to 2048.

Added
~~~~~

- Added :func:`event_device_code_generated()`
- Added :exc:`ChatError`
- Added ``SLEEPING`` to :class:`ReadyState`

Bug Fixes
~~~~~

- Fixed an exception being thrown if a party member had an invalid outfit ID.
- Fixed presences sometimes not being able to be parsed if a specific key was missing.

v0.9.1
------

Bug Fixes
~~~~~

- Fixed refresh failing due to response missing certain keys.
- Fixed caches not being refreshed while recovering events.


v0.9.0
------

Major version shift as the library comes closer to the 1.0 release.

Added
~~~~~

- Added websocket logger.

Bug Fixes
~~~~~

- Fixed some clients not receiving messages.
- Removed the controller icon next to the bots banner, hiding level.
- Websocket connection is now closed gracefully on exit.

Removed
~~~~~~~

- Removed :meth:`ClientPartyMember.set_rank()` as it no longer changes visual rank in the lobby.


v0.0.6
------

Bug Fixes
~~~~~

- Fixed some clients not receiving the same websocket responses as others, causing the websocket connection to be lost.


v0.0.5
------

Bug Fixes
~~~~~

- Fixed :meth:`Friend.send()`.
- Fixed :meth:`ClientParty.send()`.
- Fixed :meth:`FriendMessage.reply()`.
- Fixed :meth:`PartyMessage.reply()`.
- Fixed :func:`event_party_message()`.
- Fixed :func:`event_friend_message()`.


v0.0.4
------

Added
~~~~~

- Added :meth:`Client.fetch_creative_island()`.
- Added ``{current_playlist}`` variable to clients status.


v0.0.3
------

Bug Fixes
~~~~~~~~~

- Fixed :meth:`rebootpy.run_multiple()` throwing an excepton if :class:`AdvancedAuth` is used.
- Fixed ``multiple_clients.py`` example.


v0.0.2
------

Bug Fixes
~~~~~~~~~

- Fixed ``KeyError: 'party.joininfodata.286331153_j'``.


Added
~~~~~

- ``SEASON_30`` added to :class:`SeasonStartTimestamp` & ``SEASON_29`` added to :class:`SeasonEndTimestamp`.


v0.0.1
------

Changes
~~~~~~~

- (**Breaking**) Removed :class:`EmailAndPasswordAuth`.
- (**Breaking**) :class:`AdvancedAuth` no longer accepts `email` & `password` and instead by default uses device code if there are no device auths.
- (**Breaking**) As featured & daily items are no longer different in the store, ``featured_items`` & ``daily_items`` have been combined to :attr:`Store.items` which uses the :class:`StoreItem` type.
- Added ``prompt_device_code`` & ``open_link_in_browser`` parameters to :class:`AdvancedAuth`.


Added
~~~~~

- Added functionality for new ``cosmeticStats`` values in party member meta.

  - Added :meth:`ClientPartyMember.equip_crown()`.
  - Added :meth:`ClientPartyMember.set_victory_crowns()`.  
  - Added :meth:`ClientPartyMember.set_rank()`.  
  - Added :attr:`PartyMember.has_crown`.
  - Added :attr:`PartyMember.victory_crowns`.
  - Added :attr:`PartyMember.rank`.

- Added :class:`DeviceCodeAuth`.


Removed
~~~~~~~

- Removed ``Client.fetch_user_by_email()`` as it had been deprecated by epic.


Bug Fixes
~~~~~~~~~

- Updated party & party member meta to reflect changes from C4 & C5 which completely broke them.
- Fixed broken events which either never dispatched or returned None.
- Fixed :meth:`Client.fetch_item_shop()`.
