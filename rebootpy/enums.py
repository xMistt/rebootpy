# -*- coding: utf-8 -*-
# flake8: noqa

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

import random
import types

from typing import Optional, Any
from enum import Enum as OriginalEnum


class Enum(OriginalEnum):
    @classmethod
    def get_random_member(cls) -> Optional[Any]:
        try:
            return cls[random.choice(cls._member_names_)]
        except IndexError:
            pass

    @classmethod
    def get_random_name(cls) -> Optional[Any]:
        member = cls.get_random_member()
        if member is not None:
            return member.name

    @classmethod
    def get_random_value(cls) -> Optional[Any]:
        member = cls.get_random_member()
        if member is not None:
            return member.value


class PartyPrivacy(Enum):
    PUBLIC = {
        'partyType': 'Public',
        'inviteRestriction': 'AnyMember',
        'onlyLeaderFriendsCanJoin': False,
        'presencePermission': 'Anyone',
        'invitePermission': 'Anyone',
        'acceptingMembers': True,
    }
    FRIENDS_ALLOW_FRIENDS_OF_FRIENDS = {
        'partyType': 'FriendsOnly',
        'inviteRestriction': 'AnyMember',
        'onlyLeaderFriendsCanJoin': False,
        'presencePermission': 'Anyone',
        'invitePermission': 'AnyMember',
        'acceptingMembers': True,
    }
    FRIENDS = {
        'partyType': 'FriendsOnly',
        'inviteRestriction': 'LeaderOnly',
        'onlyLeaderFriendsCanJoin': True,
        'presencePermission': 'Leader',
        'invitePermission': 'Leader',
        'acceptingMembers': False,
    }
    PRIVATE_ALLOW_FRIENDS_OF_FRIENDS = {
        'partyType': 'Private',
        'inviteRestriction': 'AnyMember',
        'onlyLeaderFriendsCanJoin': False,
        'presencePermission': 'Noone',
        'invitePermission': 'AnyMember',
        'acceptingMembers': False,
    }
    PRIVATE = {
        'partyType': 'Private',
        'inviteRestriction': 'LeaderOnly',
        'onlyLeaderFriendsCanJoin': True,
        'presencePermission': 'Noone',
        'invitePermission': 'Leader',
        'acceptingMembers': False,
    }


class PartyDiscoverability(Enum):
    ALL          = 'ALL'
    INVITED_ONLY = 'INVITED_ONLY'


class PartyJoinability(Enum):
    OPEN              = 'OPEN'
    INVITE_ONLY       = 'INVITE_ONLY'
    INVITE_AND_FORMER = 'INVITE_AND_FORMER' 


class DefaultCharactersChapter1(Enum):
    CID_001_Athena_Commando_F_Default = 1
    CID_002_Athena_Commando_F_Default = 2
    CID_003_Athena_Commando_F_Default = 3
    CID_004_Athena_Commando_F_Default = 4
    CID_005_Athena_Commando_M_Default = 5
    CID_006_Athena_Commando_M_Default = 6
    CID_007_Athena_Commando_M_Default = 7
    CID_008_Athena_Commando_M_Default = 8


class DefaultCharactersChapter2(Enum):
    CID_556_Athena_Commando_F_RebirthDefaultA = 1
    CID_557_Athena_Commando_F_RebirthDefaultB = 2
    CID_558_Athena_Commando_F_RebirthDefaultC = 3
    CID_559_Athena_Commando_F_RebirthDefaultD = 4
    CID_560_Athena_Commando_M_RebirthDefaultA = 5
    CID_561_Athena_Commando_M_RebirthDefaultB = 6
    CID_562_Athena_Commando_M_RebirthDefaultC = 7
    CID_563_Athena_Commando_M_RebirthDefaultD = 8


class DefaultCharactersChapter3(Enum):
    CID_A_272_Athena_Commando_F_Prime = 1
    CID_A_273_Athena_Commando_F_Prime_B = 2
    CID_A_274_Athena_Commando_F_Prime_C = 3
    CID_A_275_Athena_Commando_F_Prime_D = 4
    CID_A_276_Athena_Commando_F_Prime_E = 5
    CID_A_277_Athena_Commando_F_Prime_F = 6
    CID_A_278_Athena_Commando_F_Prime_G = 7
    CID_A_279_Athena_Commando_M_Prime = 8
    CID_A_280_Athena_Commando_M_Prime_B = 9
    CID_A_281_Athena_Commando_M_Prime_C = 10
    CID_A_282_Athena_Commando_M_Prime_D = 11
    CID_A_283_Athena_Commando_M_Prime_E = 12
    CID_A_284_Athena_Commando_M_Prime_F = 13
    CID_A_285_Athena_Commando_M_Prime_G = 14


class V2Input(Enum):
    KEYBOARDANDMOUSE = 'keyboardmouse'
    GAMEPAD          = 'gamepad'
    TOUCH            = 'touch'


class Region(Enum):
    NAEAST     = 'NAE'
    NAWEST     = 'NAW'
    NACENTRAL  = 'NAC'
    EUROPE     = 'EU'
    BRAZIL     = 'BR'
    OCEANIA    = 'OCE'
    ASIA       = 'ASIA'
    MIDDLEEAST = 'ME'


class Platform(Enum):
    WINDOWS       = 'WIN'
    MAC           = 'MAC'
    PLAYSTATION   = 'PSN'
    PLAYSTATION_4 = 'PSN'
    PLAYSTATION_5 = 'PS5'
    XBOX          = 'XBL'
    XBOX_ONE      = 'XBL'
    XBOX_X        = 'XSX'
    SWITCH        = 'SWT'
    IOS           = 'IOS'
    ANDROID       = 'AND'


class UserSearchPlatform(Enum):
    EPIC_GAMES  = 'epic'
    PLAYSTATION = 'psn'
    XBOX        = 'xbl'
    STEAM       = 'steam'


class UserSearchMatchType(Enum):
    EXACT = 'exact'
    PREFIX = 'prefix'


class ReadyState(Enum):
    READY       = 'Ready'
    NOT_READY   = 'NotReady'
    SITTING_OUT = 'SittingOut'
    SLEEPING    = 'Away'


class AwayStatus(Enum):
    ONLINE        = None
    AWAY          = 'away'
    EXTENDED_AWAY = 'xa'


class SeasonStartTimestamp(Enum):
    SEASON_1  = 1508889601
    SEASON_2  = 1513209601
    SEASON_3  = 1519257601
    SEASON_4  = 1525132801
    SEASON_5  = 1531353601
    SEASON_6  = 1538006401
    SEASON_7  = 1544054401
    SEASON_8  = 1551312001
    SEASON_9  = 1557360001
    SEASON_10 = 1564617601
    SEASON_11 = 1571097601
    SEASON_12 = 1582156801
    SEASON_13 = 1592352001
    SEASON_14 = 1598486401
    SEASON_15 = 1606867201
    SEASON_16 = 1615852801
    SEASON_17 = 1623110401
    SEASON_18 = 1631491201
    SEASON_19 = 1638716400
    SEASON_20 = 1647763140
    SEASON_21 = 1654430400
    SEASON_22 = 1663503780
    SEASON_23 = 1670157000
    SEASON_24 = 1678453200
    SEASON_25 = 1686313800
    SEASON_26 = 1692966600
    SEASON_27 = 1699016400
    SEASON_28 = 1701577740
    SEASON_29 = 1709951400
    SEASON_30 = 1716508800


class SeasonEndTimestamp(Enum):
    SEASON_1  = 1513123200
    SEASON_2  = 1519171200
    SEASON_3  = 1525046400
    SEASON_4  = 1531353600
    SEASON_5  = 1538006400
    SEASON_6  = 1544054400
    SEASON_7  = 1551312000
    SEASON_8  = 1557360000
    SEASON_9  = 1564617600
    SEASON_10 = 1570924800
    SEASON_11 = 1582156800
    SEASON_12 = 1592352000
    SEASON_13 = 1598486400
    SEASON_14 = 1606867200
    SEASON_15 = 1615852800
    SEASON_16 = 1623110400
    SEASON_17 = 1631491200
    SEASON_18 = 1638651540
    SEASON_19 = 1647759540
    SEASON_20 = 1654372800
    SEASON_21 = 1663479000
    SEASON_22 = 1670140800
    SEASON_23 = 1678429800
    SEASON_24 = 1686288600
    SEASON_25 = 1692945000
    SEASON_26 = 1698994800
    SEASON_27 = 1701576000
    SEASON_28 = 1709794800
    SEASON_29 = 1716533100


class BattlePassStat(Enum):
    SEASON_11 = ('s11_social_bp_level', SeasonEndTimestamp.SEASON_11.value)
    SEASON_12 = ('s11_social_bp_level', SeasonEndTimestamp.SEASON_12.value)
    SEASON_13 = (('s13_social_bp_level', 's11_social_bp_level'), SeasonEndTimestamp.SEASON_13.value)
    SEASON_14 = ('s14_social_bp_level', SeasonEndTimestamp.SEASON_14.value)
    SEASON_15 = ('s15_social_bp_level', SeasonEndTimestamp.SEASON_15.value)
    SEASON_16 = ('s16_social_bp_level', SeasonEndTimestamp.SEASON_16.value)
    SEASON_17 = ('s17_social_bp_level', SeasonEndTimestamp.SEASON_17.value)
    SEASON_18 = ('s18_social_bp_level', SeasonEndTimestamp.SEASON_18.value)
    SEASON_19 = ('s19_social_bp_level', SeasonEndTimestamp.SEASON_19.value)
    SEASON_20 = ('s20_social_bp_level', SeasonEndTimestamp.SEASON_20.value)
    SEASON_21 = ('s21_social_bp_level', SeasonEndTimestamp.SEASON_21.value)
    SEASON_22 = ('s22_social_bp_level', SeasonEndTimestamp.SEASON_22.value)
    SEASON_23 = ('s23_social_bp_level', SeasonEndTimestamp.SEASON_23.value)
    SEASON_24 = ('s24_social_bp_level', SeasonEndTimestamp.SEASON_24.value)
    SEASON_25 = ('s25_social_bp_level', SeasonEndTimestamp.SEASON_25.value)
    SEASON_26 = ('s26_social_bp_level', SeasonEndTimestamp.SEASON_26.value)
    SEASON_27 = ('s27_social_bp_level', SeasonEndTimestamp.SEASON_27.value)
    SEASON_28 = ('s28_social_bp_level', SeasonEndTimestamp.SEASON_28.value)
    SEASON_29 = ('s29_social_bp_level', SeasonEndTimestamp.SEASON_29.value)


class Seasons(Enum):
    C4S2 = ('2776dc', '9d7ebd')
    C4S3 = ('ggOwuK', 'AjRdrb')
    C4S4 = ('gXffl', 'yHNFu')
    C4SOG = ('OiK9k9', 'hEKWqj')
    C5S1 = ('EYpme7', 'd0zEcd', 'dmd372')
    C5S2 = ('ch3353', 'a1m0n3', 'rrwpwg')
    C5S3 = ('N4PK1N', 'L1GHT5', 'rrzuel')
    C5S4 = ('S4LT3D', 'P0T4T0', 'rr9qlw', 'M4rC4S', 'L4nC3r')


class RankingType(Enum):
    BATTLE_ROYALE = 'ranked-br'
    ZERO_BUILD = 'ranked-zb'
    ROCKET_RACING = 'delmar-competitive'
    RELOAD = 'ranked_blastberry_build'
    RELOAD_ZB = 'ranked_blastberry_nobuild'


class Rank(Enum):
    UNRANKED = None
    BRONZE_1 = 0
    BRONZE_2 = 1
    BRONZE_3 = 2
    SILVER_1 = 3
    SILVER_2 = 4
    SILVER_3 = 5
    GOLD_1 = 6
    GOLD_2 = 7
    GOLD_3 = 8
    PLATINUM_1 = 9
    PLATINUM_2 = 10
    PLATINUM_3 = 11
    DIAMOND_1 = 12
    DIAMOND_2 = 13
    DIAMOND_3 = 14
    ELITE = 15
    CHAMPION = 16
    UNREAL = 17


class StatsCollectionType(Enum):
    FISH = 'collection_fish'
