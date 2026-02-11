.. currentmodule:: rebootpy


API Reference
=============

.. _authentication:

Authentication
--------------

The preferred method to login is :class:`DeviceAuth`. To set up and handle this type
of auth, you should use :class:`AdvancedAuth`. `This example <https://github.com/xMistt/rebootpy/blob/main/examples/basic_bot.py>`_ demonstrates
how you can set up this auth with file storage for the preferred login which is :class:`DeviceAuth`.

.. autoclass:: AdvancedAuth

.. autoclass:: DeviceCodeAuth

.. autoclass:: DeviceAuth

.. autoclass:: AuthorizationCodeAuth

.. autoclass:: ExchangeCodeAuth

.. autoclass:: RefreshTokenAuth


Clients
-------

BasicClient
~~~~~~~~~~~

.. attributetable:: BasicClient

.. autoclass:: BasicClient()
    :members:

Client
~~~~~~

.. attributetable:: Client

.. autoclass:: Client()
    :members:
    :inherited-members:


Utility Functions
-----------------

Utility functions provided by the package.

.. autofunction:: run_multiple

.. autofunction:: start_multiple
    
.. autofunction:: close_multiple


Enumerations
------------

.. class:: PartyPrivacy

    Specifies the privacy used in parties created by the client.

    .. attribute:: PUBLIC

        Sets privacy to completely public. This means everyone can join the party, even friends of friends.
    .. attribute:: FRIENDS_ALLOW_FRIENDS_OF_FRIENDS

        Sets privacy to only allow friends but friends of friends are able to join.
    .. attribute:: FRIENDS

        Sets privacy to friends only.
    .. attribute:: PRIVATE_ALLOW_FRIENDS_OF_FRIENDS

        Sets privacy to private but allows friends of friends.
    .. attribute:: PRIVATE

        Sets privacy to private without the possibility of friends of friends joining.

.. class:: V2Input

    An enumeration for valid input types used for stats.

    .. attribute:: KEYBOARDANDMOUSE

        Input type used for all users of keyboard and mouse. This is not only used
        for pc players but also other platforms where it's possible to use keyboard
        and mouse.
    .. attribute:: GAMEPAD

        Input type used for all players using a gamepad/controller. This is not only
        used for console players but also other platforms where it's possible to use
        a gamepad/controller.
    .. attribute:: TOUCH

        Input type used for all players using a touch display as controls. This is not
        only used for mobile players but also other platforms where it's possible to
        use a touch display as controls.

.. class:: Region

    An enumeration for all currently available Fortnite regions.

    .. attribute:: NAEAST

        The North America East region.
    .. attribute:: NAWEST

        The North America West region.
    .. attribute:: NACENTRAL

        The North America Central region.
    .. attribute:: EUROPE

        The Europe region.
    .. attribute:: BRAZIL

        The Brazil region.
    .. attribute:: OCEANIA

        The Oceania region.
    .. attribute:: ASIA

        The Asia region.
    .. attribute:: MIDDLEEAST

        The Middle East region.

.. class:: Platform

    An enumeration for all currently available platforms.

    .. attribute:: WINDOWS
    .. attribute:: MAC
    .. attribute:: PLAYSTATION_4

        Also accessible under ``PLAYSTATION`` for legacy reasons.
    .. attribute:: PLAYSTATION_5
    .. attribute:: XBOX_ONE

        Also accessible under ``XBOX`` for legacy reasons.
    .. attribute:: XBOX_X
    .. attribute:: SWITCH
    .. attribute:: IOS
    .. attribute:: ANDROID
    .. attribute:: SWITCH_2
    .. attribute:: UNKNOWN

        Used when an un-official client (e.g. one using a library similar to
        this) passes an invalid client to their presence such as ``EPIC``,
        if you get this and it's coming from a legitimate Fortnite client,
        please make an issue.

.. class:: ReadyState

    An enumeration for the available ready states.

    .. attribute:: READY
    .. attribute:: NOT_READY
    .. attribute:: SITTING_OUT
    .. attribute:: SLEEPING

.. class:: UserSearchPlatform

    .. attribute:: EPIC_GAMES

        This represents all platforms that use epic games as account service like PC and Mobile.

    .. attribute:: PLAYSTATION
    .. attribute:: XBOX
    .. attribute:: STEAM

.. class:: ProfileSearchMatchType

    .. attribute:: EXACT

        The prefix matched the display name perfectly.

    .. attribute:: PREFIX

        The prefix matched the start of the display name perfectly.

.. class:: AwayStatus

    .. attribute:: ONLINE

        User is currently active.

    .. attribute:: AWAY

        User has set his status to away in-game

    .. attribute:: EXTENDED_AWAY

        User is AFK. This can only be applied by the game and it is set after a specific time of no activity.

.. class:: StatsCollectionType

    An enumeration for stats collection types.

    .. attribute:: FISH

.. class:: Season

    An enumeration for a Fortnite season.

    Attributes
    ----------

    These attributes are shared across all seasons:

    - **start_timestamp** (:class:`int`): The start timestamp of the season in seconds since the epoch.
    - **end_timestamp** (:class:`int`): The end timestamp of the season in seconds since the epoch.
    - **battlepass_level** (:class:`str` or :class:`tuple`): The StatsV2 value for this season's battle pass level. ``None`` for seasons before Chapter 2.
    - **ranked_tracks** (:class:`tuple`): The ranked tracks for this season. ``None`` for seasons before Chapter 4, Season 2.

    You don't need to use ``.value`` to access these; you can access them directly, e.g. ``Season.C5SOG.start_timestamp``.

    Enums
    ----------

    .. attribute:: C1S1
    .. attribute:: C1S2
    .. attribute:: C1S3
    .. attribute:: C1S4
    .. attribute:: C1S5
    .. attribute:: C1S6
    .. attribute:: C1S7
    .. attribute:: C1S8
    .. attribute:: C1S9
    .. attribute:: C1SX
    .. attribute:: C2S1
    .. attribute:: C2S2
    .. attribute:: C2S3
    .. attribute:: C2S4
    .. attribute:: C2S5
    .. attribute:: C2S6
    .. attribute:: C2S7
    .. attribute:: C2S8
    .. attribute:: C3S1
    .. attribute:: C3S2
    .. attribute:: C3S3
    .. attribute:: C3S4
    .. attribute:: C4S1
    .. attribute:: C4S2
    .. attribute:: C4S3
    .. attribute:: C4S4
    .. attribute:: C4SOG
    .. attribute:: C5S1
    .. attribute:: C5S2
    .. attribute:: C5S3
    .. attribute:: C5S4
    .. attribute:: C5SOG
    .. attribute:: C6S1

.. class:: RankingType

    An enumeration for the available ranking types.

    .. attribute:: BATTLE_ROYALE
    .. attribute:: ZERO_BUILD
    .. attribute:: ROCKET_RACING
    .. attribute:: RELOAD
    .. attribute:: RELOAD_ZB
    .. attribute:: BALLISTIC
    .. attribute:: OG
    .. attribute:: OG_ZERO_BUILD

.. class:: Rank

    An enumeration for the available ranks.

    .. attribute:: UNRANKED
    .. attribute:: BRONZE_1
    .. attribute:: BRONZE_2
    .. attribute:: BRONZE_3
    .. attribute:: SILVER_1
    .. attribute:: SILVER_2
    .. attribute:: SILVER_3
    .. attribute:: GOLD_1
    .. attribute:: GOLD_2
    .. attribute:: GOLD_3
    .. attribute:: PLATINUM_1
    .. attribute:: PLATINUM_2
    .. attribute:: PLATINUM_3
    .. attribute:: DIAMOND_1
    .. attribute:: DIAMOND_2
    .. attribute:: DIAMOND_3
    .. attribute:: ELITE
    .. attribute:: CHAMPION
    .. attribute:: UNREAL

.. class:: Country

    An enumeration for the available selectable flags.

    .. attribute:: ARGENTINA
    .. attribute:: AUSTRALIA
    .. attribute:: BELARUS
    .. attribute:: BELGIUM
    .. attribute:: BRAZIL
    .. attribute:: CANADA
    .. attribute:: COLOMBIA
    .. attribute:: CZECHREPUBLIC
    .. attribute:: DENMARK
    .. attribute:: EGYPT
    .. attribute:: ENGLAND
    .. attribute:: FRANCE
    .. attribute:: GERMANY
    .. attribute:: GLOBAL
    .. attribute:: ICELAND
    .. attribute:: IRELAND
    .. attribute:: ITALY
    .. attribute:: JAPAN
    .. attribute:: LATVIA
    .. attribute:: MEXICO
    .. attribute:: NETHERLANDS
    .. attribute:: NEWZEALAND
    .. attribute:: NIGERIA
    .. attribute:: NORWAY
    .. attribute:: POLAND
    .. attribute:: PORTUGAL
    .. attribute:: RUSSIA
    .. attribute:: SAUDIARABIA
    .. attribute:: SCOTLAND
    .. attribute:: SOUTHKOREA
    .. attribute:: SPAIN
    .. attribute:: SWEDEN
    .. attribute:: SWITZERLAND
    .. attribute:: TURKEY
    .. attribute:: UKRAINE
    .. attribute:: UNITEDKINGDOM
    .. attribute:: UNITEDSTATES
    .. attribute:: URUGUAY
    .. attribute:: WALES

.. _rebootpy-api-events:

Event Reference
---------------

Events can be registered by the ``@client.event`` decorator. You do not need 
this decorator if you are in a subclass of :class:`Client`.

.. warning::

    All events must be registered as coroutines!

.. function:: event_ready()

    This event is called when the client .has been successfully established and connected to all services.
    
    .. note::
    
        This event is not called when the client starts in :class:`Client.close()`.

.. function:: event_before_start()

    This event is called and waited for before the client starts.

    .. warning::
    
        This event is not called when the client starts in :class:`Client.restart()`.

    .. note::

        This event behaves differently from the other events. The client will wait until the event handlers for this event is finished processing before actually closing. This makes it so you are able to do heavy and/or time consuming operations before the client fully logs out. This unfortunately also means that this event is not compatible with :meth:`Client.wait_for()`.

.. function:: event_before_close()

    This event is called when the client is beginning to log out. This event also exists under the name ``event_close()`` for legacy reasons.

    .. warning::
        
        This event is not called when the client logs out in :class:`Client.restart()`.

    .. note::

        This event behaves differently from the other events. The client will wait until the event handlers for this event is finished processing before actually closing. This makes it so you are able to do heavy and/or time consuming operations before the client fully logs out. This unfortunately also means that this event is not compatible with :meth:`Client.wait_for()`.

.. function:: event_restart()

    This event is called when the client has successfully restarted.

.. function:: event_xmpp_session_establish()

    Called whenever a xmpp session has been established. This can be called multiple times.

.. function:: event_xmpp_session_lost()

    Called whenever the xmpp connection is lost. This can happen when the internet connection is lost or if epics services goes down.

.. function:: event_xmpp_session_close()

    Called whenever the xmpp connection is closed. This means that it is called both when it's lost or closed gracefully.
    
.. function:: event_device_auth_generate(details)

    This event is called whenever new device authentication details are generated.

    :param details: A dictionary containing the keys ``device_id``, ``account_id`` and ``secret``.
    :type details: :class:`dict`

.. function:: event_device_code_generated(link)

    This event is called whenever a device code link is generated during :class:`DeviceCodeAuth` or :class:`AdvancedAuth`.

    .. warning::

        If this event isn't referenced, the device code link will be printed to the console.

    :param link: The link to complete the device code login.
    :type link: :class:`str`

.. function:: event_auth_refresh()

    This event is called when the clients authentication has been refreshed.

.. function:: event_friend_message(message)

    This event is called when :class:`ClientUser` receives a private message.
    
    :param message: Message object.
    :type message: :class:`FriendMessage`

.. function:: event_party_message(message)
    
    This event is called when :class:`ClientUser`'s party receives a message.
    
    :param message: Message object.
    :type message: :class:`PartyMessage`

.. function:: event_friend_add(friend)

    This event is called when a friend has been added.
    
    .. note::
        
        This event is called regardless of the direction. That means it will get called even if the client were to be the one to accept the user.
    
    :param friend: Friend that has been added.
    :type friend: :class:`Friend`

.. function:: event_friend_remove(friend)

    This event is called when a friend has been removed from the friendlist.
    
    .. note::
        
        This event is called regardless of the direction. That means it will get called even if the client were to be the one to remove the friend.
    
    :param friend: Friend that was removed.
    :type friend: :class:`Friend`

.. function:: event_friend_request(request)

    This event is called when the client receives a friend request.
    
    :param request: Request object.
    :type request: Union[:class:`IncomingPendingFriend`, :class:`OutgoingPendingFriend`]

.. function:: event_friend_request_decline(friend)

    This event is called when a friend request is declined.

    :param request: Request object.
    :type request: Union[:class:`IncomingPendingFriend`, :class:`OutgoingPendingFriend`]

.. function:: event_friend_request_abort(friend)

    This event is called when a friend request is aborted. Aborted means that the friend request was deleted before the receiving user managed to accept it.

    :param request: Request object.
    :type request: Union[:class:`IncomingPendingFriend`, :class:`OutgoingPendingFriend`]

.. function:: event_friend_presence(before, after)

    This event is called when the client receives a presence from a friend.
    Presence is received when a user logs into fortnite, closes fortnite or
    when an user does an action when logged in e.g. joins into a game or joins
    a party.

    :param before: The previously received presence object. Can be ``None`` usually because the friend was previously offline or because the client just started and therefore no presence had been already stored in the presence cache.
    :type before: Optional[:class:`Presence`]
    :param after: The new presence object.
    :type after: :class:`Presence`

.. function:: event_party_invite(invitation)

    This event is called when a party invitation is received.
    
    :param invitation: Invitation object.
    :type invitation: :class:`ReceivedPartyInvitation`

.. function:: event_invalid_party_invite(friend)

    This event is called whenever you received an invite that was invalid. Usually this is because the invite was from a private party you have been kicked from.

    :param friend: The friend that invited you.
    :type friend: :class:`Friend`
    
.. function:: event_party_member_promote(old_leader, new_leader)

    This event is called when a new partyleader has been promoted.
    
    :param old_leader: Member that was previously leader.
    :type old_leader: :class:`PartyMember`
    :param new_leader: Member that was promoted.
    :type new_leader: :class:`PartyMember`
    
.. function:: event_party_member_kick(member)

    This event is called when a member has been kicked from the party.
    
    :param member: The member that was kicked.
    :type member: :class:`PartyMember`

.. function:: event_party_member_zombie(member)

    This event is called when a members connection was lost and therefore entered a zombie state waiting for their offline time to live expires. If the connection is restored before timing out, :func:`event_party_member_reconnect()` is called. If not then :func:`event_party_member_expire()` is called when their time to live runs out.

    :param member: The member that lost its connection.
    :type member: :class:`PartyMember`

.. function:: event_party_member_reconnect(member)

    This event is called when a member reconnects after losing their connection.

    :param member: The member that reconnected.
    :type member: :class:`PartyMember`

.. function:: event_party_member_expire(member)

    This event is called when a member expires after being in their zombie state for 30 seconds.
    
    :param member: The member that expired.
    :type member: :class:`PartyMember`

.. function:: event_party_update(party)

    This event is called when :class:`ClientUser`'s partymeta is updated. An example of when this is called is when a new custom key has been set.

    :param party: The party that was updated.
    :type party: :class:`Party`

.. function:: event_party_member_update(member)

    This event is called when the meta of a member of :class:`ClientUser`'s party is updated. An example of when this might get called is when a member changes outfit.

    :param member: The member whos meta was updated.
    :type member: :class:`PartyMember`

.. function:: event_party_member_join(member)

    This event is called when a new member has joined :class:`ClientUser`'s party.

    :param member: The member who joined.
    :type member: :class:`PartyMember`

.. function:: event_party_member_leave(member)

    This event is called when a member leaves the party.
    
    :param member: The member who left the party.
    :type member: :class:`PartyMember`

.. function:: event_party_member_confirm(confirmation)

    This event is called when a member asks to join the party.

    .. warning::

        This event is automatically handled by the client which automatically always accepts the user. If you have this event referenced in your code the client won't automatically handle it anymore and you must handle it yourself.

    .. note::

        This event differs from :func:`event_party_join_request` by the fact that this event is fired whenever someone is in the middle of joining the party, while :func:`event_party_join_request` is called when someone explicitly requests to join your private party.
    
    :param confirmation: Confirmation object with accessible confirmation methods.
    :type confirmation: :class:`PartyJoinConfirmation`

.. function:: event_party_join_request(request)

    This event is called when a friend requests to join your private party.

    .. note::

        This event differs from :func:`event_party_member_confirm` by the fact that this event is called when someone explicitly requests to join the bots party, while :func:`event_party_member_confirm` is an event that is fired whenever someone is in the middle of joining the party.

    :param request: Request object.
    :type request: :class:`PartyJoinRequest`

.. function:: event_party_invite_decline(friend)

    This event is called when an invite has been declined.

    :param friend: The friend who declined the invite.
    :type party: :class:`Friend`

.. function:: event_party_playlist_change(party, before, after)

    This event is called when the playlist data has been changed.

    :param party: The party that changed.
    :type party: :class:`ClientParty`
    :param before: The previous playlist data. Same structure as `ClientParty.playlist_info`.
    :type before: :class:`tuple`
    :param after: The current playlist data. Same structure as `ClientParty.playlist_info`.
    :type after: :class:`tuple`

.. function:: event_party_squad_fill_change(party, before, after)

    This event is called when squad fill has been changed.

    :param party: The party that changed.
    :type party: :class:`ClientParty`
    :param before: The previous squad fill value.
    :type before: :class:`bool`
    :param after: The current squad fill value.
    :type after: :class:`bool`

.. function:: event_party_privacy_change(party, before, after)

    This event is called when the party privacy has been changed.

    :param party: The party that changed.
    :type party: :class:`ClientParty`
    :param before: The previous party privacy.
    :type before: :class:`Privacy`
    :param after: The current party privacy.
    :type after: :class:`Privacy`

.. function:: event_party_member_team_swap(member, other)

    .. note::

        Because of how party teams work, you can swap team with another member without their permission. If you don't want this to be possible, you can set ``team_change_allowed`` to ``False`` in :class:`DefaultPartyConfig`.

    This event is called whenever a party member swaps their position. If the member switches to a position that was taken my another member, the two members will swap positions. You can get their new positions from :attr:`PartyMember.position`.

    :param member: The member that instigated the team swap.
    :type member: :class:`PartyMember`
    :param other: The member that was swapped teams with. If no member was previously holding the position, this will be ``None``.
    :type other: Optional[:class:`PartyMember`]

.. function:: event_party_member_ready_change(member, before, after)

    This event is called when a members ready state has changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous ready state.
    :type before: :class:`ReadyState`
    :param after: The current ready status.
    :type after: :class:`ReadyState`

.. function:: event_party_member_input_change(member, before, after)

    This event is called when a members input has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous input.
    :type before: :class:`str`
    :param after: The current input.
    :type after: :class:`str`

.. function:: event_party_member_outfit_change(member, before, after)

    This event is called when a members outfit has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous outfit cid.
    :type before: :class:`str`
    :param after: The current outfit cid.
    :type after: :class:`str`

.. function:: event_party_member_backpack_change(member, before, after)

    This event is called when a members backpack has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous backpack bid.
    :type before: :class:`str`
    :param after: The current backpack bid.
    :type after: :class:`str`

.. function:: event_party_member_pet_change(member, before, after)

    This event is called when a members pet has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous pet id.
    :type before: :class:`str`
    :param after: The current pet id.
    :type after: :class:`str`

.. function:: event_party_member_pickaxe_change(member, before, after)

    This event is called when a members pickaxe has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous pickaxe pid.
    :type before: :class:`str`
    :param after: The current pickaxe pid.
    :type after: :class:`str`

.. function:: event_party_member_contrail_change(member, before, after)

    This event is called when a members contrail has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous contrail id.
    :type before: :class:`str`
    :param after: The current contrail id.
    :type after: :class:`str`

.. function:: event_party_member_emote_change(member, before, after)

    This event is called when a members emote has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous emote eid. ``None`` if no emote was currently playing.
    :type before: :class:`str`
    :param after: The current emote eid. ``None`` if the emote was stopped.
    :type after: :class:`str`

.. function:: event_party_member_emoji_change(member, before, after)

    This event is called when a members emoji has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous emoji id. ``None`` if no emoji was currently playing.
    :type before: :class:`str`
    :param after: The current emoji id. ``None`` if the emoji was stopped.
    :type after: :class:`str`

.. function:: event_party_member_banner_change(member, before, after)

    This event is called when a members banner has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous banner data. Same structure as :attr:`PartyMember.banner`.
    :type before: :class:`tuple`
    :param after: The current banner data. Same structure as :attr:`PartyMember.banner`.
    :type after: :class:`tuple`

.. function:: event_party_member_battlepass_info_change(member, before, after)

    This event is called when a members battlepass info has been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous battlepass data. Same structure as :attr:`PartyMember.battlepass_info`.
    :type before: :class:`tuple`
    :param after: The current battlepass data. Same structure as :attr:`PartyMember.battlepass_info`.
    :type after: :class:`tuple`

.. function:: event_party_member_enlightenments_change(member, before, after)

    This event is called when a members enlightenments values are changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous enlightenment values.
    :type before: :class:`list`
    :param after: The current enlightenment values.
    :type after: :class:`list`

.. function:: event_party_member_corruption_change(member, before, after)

    This event is called when a members corruption value is changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous corruption value. Could be ``None`` if not set.
    :type before: Optional[:class:`list`]
    :param after: The current corruption value. Could be ``None`` if not set.
    :type after: Optional[:class:`list`]

.. function:: event_party_member_outfit_variants_change(member, before, after)

    This event is called when a members outfit variants been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous outfit variants. Same structure as :attr:`PartyMember.outfit_variants`.
    :type before: :class:`list`
    :param after: The current outfit variants. Same structure as :attr:`PartyMember.outfit_variants`.
    :type after: :class:`list`

.. function:: event_party_member_backpack_variants_change(member, before, after)

    This event is called when a members backpack variants been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous backpack variants. Same structure as :attr:`PartyMember.backpack_variants`.
    :type before: :class:`list`
    :param after: The current backpack variants. Same structure as :attr:`PartyMember.backpack_variants`.
    :type after: :class:`list`

.. function:: event_party_member_pickaxe_variants_change(member, before, after)

    This event is called when a members pickaxe variants been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous pickaxe variants. Same structure as :attr:`PartyMember.pickaxe_variants`.
    :type before: :class:`list`
    :param after: The current pickaxe variants. Same structure as :attr:`PartyMember.pickaxe_variants`.
    :type after: :class:`list`

.. function:: event_party_member_contrail_variants_change(member, before, after)

    This event is called when a members contrail variants been changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous contrail variants. Same structure as :attr:`PartyMember.contrail_variants`.
    :type before: :class:`list`
    :param after: The current contrail variants. Same structure as :attr:`PartyMember.contrail_variants`.
    :type after: :class:`list`

.. function:: event_party_member_in_match_change(member, before, after)

    This event is called when a member join or leaves a match.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous match state.
    :type before: :class:`bool`
    :param after: The new and current match state.
    :type after: :class:`bool`

.. function:: event_party_member_match_players_left_change(member, before, after)

    This event is called when the servercount changes in the match the member is currently in.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous servercount.
    :type before: :class:`int`
    :param after: The new and current servercount.
    :type after: :class:`int`

.. function:: event_party_member_lobby_map_marker_is_visible_change(member, before, after)

    This event is called when the visibility of a members lobby map marker is toggled.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: Whether or not the marker used to be visible.
    :type before: :class:`bool`
    :param after: Whether or not the marker is now currently visible.
    :type after: :class:`bool`

.. function:: event_party_member_lobby_map_marker_coordinates_change(member, before, after)

    This event is called when the coordinates of a members lobby map marker is changed.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous coordinates.
    :type before: Tuple[:class:`float`, class:`float`]
    :param after: The new coordinates.
    :type after: Tuple[:class:`float`, class:`float`]


.. function:: event_party_member_playlist_selection_change(member, before, after)

    This event is called when a party member selects a different playlist.

    :param member: The member that changed.
    :type member: :class:`PartyMember`
    :param before: The previous playlist id/island code.
    :type before: :class:`str`
    :param after: The new playlist id/island code.
    :type after: :class:`str`


Stats Reference
---------------

Gamemode names
~~~~~~~~~~~~~~

Since stats received from Fortnite's services changes all the time by adding 
new gamemodes and such, none of the gamemode names have been changed from the 
original response gotten from the request. Therefore, if you want to access a 
users solo stats, you must use the internal name for the solo gamemode:
``defaultsolo``.

There is no good, easy way of retrieving all these internal names. So for now
the best way you can do this is by fetching stats from someone that has played
a lot of different gamemode e.g. the user ``Dark`` (more known as Dakotaz) and
just write the gamemode names down.

Stats
~~~~~~~~~~~~~~~

**Default Solos Gamemode (defaultsolo)**

.. code-block:: python3

    {
      'wins': int,
      'placetop10': int,
      'placetop25': int,
      'kills': int,
      'score': int,
      'playersoutlives': int,
      'minutesplayed': int,
      'matchesplayed': int,
      'lastmodified': datetime.datetime,
    }


**Default Duos Gamemode (defaultduo)**

.. code-block:: python3

    {
      'wins': int,
      'placetop5': int,
      'placetop12': int,
      'kills': int,
      'score': int,
      'playersoutlives': int,
      'minutesplayed': int,
      'matchesplayed': int,
      'lastmodified': datetime.datetime,
    }

**Default Trios Gamemode (trios)**

.. code-block:: python3

    {
      'wins': int,
      'kills': int,
      'score': int,
      'playersoutlives': int,
      'minutesplayed': int,
      'matchesplayed': int,
      'lastmodified': datetime.datetime,
    }

**Default Squads Gamemode (defaultsquad)**

.. code-block:: python3

    {
      'wins': int,
      'placetop3': int,
      'placetop6': int,
      'kills': int,
      'score': int,
      'playersoutlives': int,
      'minutesplayed': int,
      'matchesplayed': int,
      'lastmodified': datetime.datetime,
    }


Fortnite Models
---------------

.. danger::

    The classes below should never be created by users. These are classed representing data received from fortnite's services.

ClientUser
~~~~~~~~~~

.. attributetable:: ClientUser

.. autoclass:: ClientUser()
    :members:
    :inherited-members:

ExternalAuth
~~~~~~~~~~~~

.. attributetable:: ExternalAuth

.. autoclass:: ExternalAuth()
    :members:

User
~~~~

.. attributetable:: User

.. autoclass:: User()
    :members:
    :inherited-members:

BlockedUser
~~~~~~~~~~~

.. attributetable:: BlockedUser

.. autoclass:: BlockedUser()
    :members:
    :inherited-members:

UserSearchEntry
~~~~~~~~~~~~~~~

.. attributetable:: UserSearchEntry

.. autoclass:: UserSearchEntry()
    :members:
    :inherited-members:

SacSearchEntryUser
~~~~~~~~~~~~~~~~~~

.. attributetable:: SacSearchEntryUser

.. autoclass:: SacSearchEntryUser()
    :members:
    :inherited-members:

Friend
~~~~~~

.. attributetable:: Friend

.. autoclass:: Friend()
    :members:
    :inherited-members:

IncomingPendingFriend
~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: IncomingPendingFriend

.. autoclass:: IncomingPendingFriend()
    :members:
    :inherited-members:

OutgoingPendingFriend
~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: OutgoingPendingFriend

.. autoclass:: OutgoingPendingFriend()
    :members:
    :inherited-members:

FriendMessage
~~~~~~~~~~~~~

.. attributetable:: FriendMessage

.. autoclass:: FriendMessage()
    :members:
    :inherited-members:

PartyMessage
~~~~~~~~~~~~

.. attributetable:: PartyMessage

.. autoclass:: PartyMessage()
    :members:
    :inherited-members:

PartyMember
~~~~~~~~~~~

.. attributetable:: PartyMember

.. autoclass:: PartyMember()
    :members:
    :inherited-members:

ClientPartyMember
~~~~~~~~~~~~~~~~~

.. attributetable:: ClientPartyMember

.. autoclass:: ClientPartyMember()
    :members:
    :inherited-members:

Party
~~~~~

.. attributetable:: Party

.. autoclass:: Party()
    :members:
    :inherited-members:

ClientParty
~~~~~~~~~~~

.. attributetable:: ClientParty

.. autoclass:: ClientParty()
    :members:
    :inherited-members:

ReceivedPartyInvitation
~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: ReceivedPartyInvitation

.. autoclass:: ReceivedPartyInvitation()
    :members:

SentPartyInvitation
~~~~~~~~~~~~~~~~~~~

.. attributetable:: SentPartyInvitation

.. autoclass:: SentPartyInvitation()
    :members:

PartyJoinConfirmation
~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: PartyJoinConfirmation

.. autoclass:: PartyJoinConfirmation()
    :members:

PartyJoinRequest
~~~~~~~~~~~~~~~~

.. attributetable:: PartyJoinRequest

.. autoclass:: PartyJoinRequest
    :members:

Presence
~~~~~~~~

.. attributetable:: Presence

.. autoclass:: Presence()
    :members:

PresenceParty
~~~~~~~~~~~~~

.. attributetable:: PresenceParty

.. autoclass:: PresenceParty()
    :members:

PresenceGameplayStats
~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: PresenceGameplayStats

.. autoclass:: PresenceGameplayStats()
    :members:

StatsV2
~~~~~~~

.. attributetable:: StatsV2

.. autoclass:: StatsV2()
    :members:

StatsCollection
~~~~~~~~~~~~~~~

.. attributetable:: StatsCollection

.. autoclass:: StatsCollection()
    :members:

BattleRoyaleNewsPost
~~~~~~~~~~~~~~~~~~~~

.. attributetable:: BattleRoyaleNewsPost

.. autoclass:: BattleRoyaleNewsPost()
    :members:

Store
~~~~~

.. attributetable:: Store

.. autoclass:: Store()
    :members:

StoreItem
~~~~~~~~~~~~~~~~~

.. attributetable:: StoreItem

.. autoclass:: StoreItem()
    :members:
    :inherited-members:

Playlist
~~~~~~~~

.. attributetable:: Playlist

.. autoclass:: Playlist()
    :members:

CreativeIsland
~~~~~

.. attributetable:: CreativeIsland

.. autoclass:: CreativeIsland()
    :members:

CreativeIslandRating
~~~~~~~~~~~~~~~~~

.. attributetable:: CreativeIslandRating

.. autoclass:: CreativeIslandRating()
    :members:
    :inherited-members:

CompetitiveRank
~~~~~~~~~~~~~~~~~

.. attributetable:: CompetitiveRank

.. autoclass:: CompetitiveRank()
    :members:
    :inherited-members:

Data Classes
------------

Data classes used as data containers in the library.

DefaultPartyConfig
~~~~~~~~~~~~~~~~~~

.. attributetable:: DefaultPartyConfig

.. autoclass:: DefaultPartyConfig()
    :members:

DefaultPartyMemberConfig
~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: DefaultPartyMemberConfig

.. autoclass:: DefaultPartyMemberConfig()
    :members:

HTTPRetryConfig
~~~~~~~~~~~~~~~

.. autoclass:: HTTPRetryConfig()
    :members:

Route
~~~~~

.. attributetable:: Route

.. autoclass:: Route()
    :members:

Avatar
~~~~~~

.. attributetable:: Avatar

.. autoclass:: Avatar()
    :members:

SquadAssignment
~~~~~~~~~~~~~~~

.. attributetable:: SquadAssignment

.. autoclass:: SquadAssignment()
    :members:


Exceptions
----------

.. autoexception:: FortniteException

.. autoexception:: AuthException

.. autoexception:: HTTPException

.. autoexception:: ValidationFailure

.. autoexception:: EventError

.. autoexception:: XMPPError

.. autoexception:: PartyError

.. autoexception:: PartyIsFull

.. autoexception:: Forbidden

.. autoexception:: NotFound

.. autoexception:: DuplicateFriendship

.. autoexception:: FriendshipRequestAlreadySent

.. autoexception:: MaxFriendshipsExceeded

.. autoexception:: InviteeMaxFriendshipsExceeded

.. autoexception:: InviteeMaxFriendshipRequestsExceeded

.. autoexception:: FriendOffline

.. autoexception:: InvalidOffer

.. autoexception:: ChatError