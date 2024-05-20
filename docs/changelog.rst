.. currentmodule:: rebootpy

Changelog
=========

Detailed version changes.


v1.0.0
------

Changes
~~~~~~~

- (**Breaking**) Removed :class:`EmailAndPasswordAuth`.
- (**Breaking**) :class:`AdvancedAuth` no longer accepts `email` & `password` and instead by default uses device code if there are no device auths.
- (**Breaking**) As featured & daily items are no longer different in the store, `featured_items` & `daily_items` have been combined to :attr:`Store.items` which uses the :class:`StoreItem` type.
- Added `prompt_device_code` & `open_link_in_browser` parameters to  :class:`AdvancedAuth`.


Added
~~~~~

- Added functionality for new `cosmeticStats` values in party member meta.

  - Added :meth:`ClientPartyMember.equip_crown()`.
  - Added :meth:`ClientPartyMember.set_victory_crowns()`.  
  - Added :meth:`ClientPartyMember.set_rank()`.  
  - Added :attr:`PartyMember.has_crown`.
  - Added :attr:`PartyMember.victory_crowns`.
  - Added :attr:`PartyMember.rank`.

- Added :class:`DeviceCodeAuth`.


Removed
~~~~~~~

- Removed `Client.fetch_user_by_email()` as it had been deprecated by epic.


Bug Fixes
~~~~~~~~~

- Updated party & party member meta to reflect changes from C4 & C5 which completely broke them.
- Fixed broken events which either never dispatched or returned None.
- Fixed :meth:`Client.fetch_item_shop()`.