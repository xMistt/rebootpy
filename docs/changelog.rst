.. currentmodule:: rebootpy

Changelog
=========

Detailed version changes.


v1.0.0
------

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

Bug Fixes
~~~~~~~~~

- Updated party & party member meta to reflect changes from C4 & C5 which completely broke them.
