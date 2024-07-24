.. currentmodule:: rebootpy

Changelog
=========

Detailed version changes.
You can also view the changelog of the original library, fortnitepy, `here <https://fortnitepy.readthedocs.io/en/latest/changelog.html>`_.

v0.0.6
------

Bug Fixes
~~~~~

- Fixed some clients not receiving the same websocket responses as others,
causing the websocket connection to be lost.


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
- Added ``prompt_device_code`` & ``open_link_in_browser`` parameters to  :class:`AdvancedAuth`.


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
