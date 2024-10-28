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
    UNKNOWN       = 'UNKNOWN'

    @classmethod
    def _missing_(cls, value) -> 'Platform':
        return cls.UNKNOWN


class UserSearchPlatform(Enum):
    EPIC_GAMES  = 'epic'
    PLAYSTATION = 'psn'
    XBOX        = 'xbl'
    STEAM       = 'steam'


class UserSearchMatchType(Enum):
    EXACT  = 'exact'
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
    C1S1   = 1508889601
    C1S2   = 1513209601
    C1S3   = 1519257601
    C1S4   = 1525132801
    C1S5   = 1531353601
    C1S6   = 1538006401
    C1S7   = 1544054401
    C1S8   = 1551312001
    C1S9   = 1557360001
    C1SX   = 1564617601
    C2S1   = 1571097601
    C2S2   = 1582156801
    C2S3   = 1592352001
    C2S4   = 1598486401
    C2S5   = 1606867201
    C2S6   = 1615852801
    C2S7   = 1623110401
    C2S8   = 1631491201
    C3S1   = 1638716400
    C3S2   = 1647763140
    C3S3   = 1654430400
    C3S4   = 1663503780
    C4S1   = 1670157000
    C4S2   = 1678453200
    C4S3   = 1686313800
    C4S4   = 1692966600
    C4SOG  = 1699016400
    C5S1   = 1701577740
    C5S2   = 1709951400
    C5S3   = 1716508800
    C5S4   = 1723802400


class SeasonEndTimestamp(Enum):
    C1S1  = 1513123200
    C1S2  = 1519171200
    C1S3  = 1525046400
    C1S4  = 1531353600
    C1S5  = 1538006400
    C1S6  = 1544054400
    C1S7  = 1551312000
    C1S8  = 1557360000
    C1S9  = 1564617600
    C1SX  = 1570924800
    C2S1  = 1582156800
    C2S2  = 1592352000
    C2S3  = 1598486400
    C2S4  = 1606867200
    C2S5  = 1615852800
    C2S6  = 1623110400
    C2S7  = 1631491200
    C2S8  = 1638651540
    C3S1  = 1647759540
    C3S2  = 1654372800
    C3S3  = 1663479000
    C3S4  = 1670140800
    C4S1  = 1678429800
    C4S2  = 1686288600
    C4S3  = 1692945000
    C4S4  = 1698994800
    C4SOG = 1701576000
    C5S1  = 1709794800
    C5S2  = 1716533100
    C5S3  = 1723777200


class BattlePassStat(Enum):
    C2S1  = ('s11_social_bp_level', SeasonEndTimestamp.C2S1.value)
    C2S2  = ('s11_social_bp_level', SeasonEndTimestamp.C2S2.value)
    C2S3  = (('s13_social_bp_level', 's11_social_bp_level'), SeasonEndTimestamp.C2S3.value)
    C2S4  = ('s14_social_bp_level', SeasonEndTimestamp.C2S4.value)
    C2S5  = ('s15_social_bp_level', SeasonEndTimestamp.C2S5.value)
    C2S6  = ('s16_social_bp_level', SeasonEndTimestamp.C2S6.value)
    C2S7  = ('s17_social_bp_level', SeasonEndTimestamp.C2S7.value)
    C2S8  = ('s18_social_bp_level', SeasonEndTimestamp.C2S8.value)
    C3S1  = ('s19_social_bp_level', SeasonEndTimestamp.C3S1.value)
    C3S2  = ('s20_social_bp_level', SeasonEndTimestamp.C3S2.value)
    C3S3  = ('s21_social_bp_level', SeasonEndTimestamp.C3S3.value)
    C3S4  = ('s22_social_bp_level', SeasonEndTimestamp.C3S4.value)
    C4S1  = ('s23_social_bp_level', SeasonEndTimestamp.C4S1.value)
    C4S2  = ('s24_social_bp_level', SeasonEndTimestamp.C4S2.value)
    C4S3  = ('s25_social_bp_level', SeasonEndTimestamp.C4S3.value)
    C4S4  = ('s26_social_bp_level', SeasonEndTimestamp.C4S4.value)
    C4SOG = ('s27_social_bp_level', SeasonEndTimestamp.C4SOG.value)
    C5S1  = ('s28_social_bp_level', SeasonEndTimestamp.C5S1.value)
    C5S2  = ('s29_social_bp_level', SeasonEndTimestamp.C5S2.value)


class Seasons(Enum):
    C4S2  = ('2776dc', '9d7ebd')
    C4S3  = ('ggOwuK', 'AjRdrb')
    C4S4  = ('gXffl', 'yHNFu')
    C4SOG = ('OiK9k9', 'hEKWqj')
    C5S1  = ('EYpme7', 'd0zEcd', 'dmd372')
    C5S2  = ('ch3353', 'a1m0n3', 'rrwpwg')
    C5S3  = ('N4PK1N', 'L1GHT5', 'rrzuel')
    C5S4  = ('S4LT3D', 'P0T4T0', 'rr9qlw', 'M4rC4S', 'L4nC3r')


class RankingType(Enum):
    BATTLE_ROYALE   = 'ranked-br'
    ZERO_BUILD      = 'ranked-zb'
    ROCKET_RACING   = 'delmar-competitive'
    RELOAD          = 'ranked_blastberry_build'
    RELOAD_ZB       = 'ranked_blastberry_nobuild'


class Rank(Enum):
    UNRANKED    = None
    BRONZE_1    = 0
    BRONZE_2    = 1
    BRONZE_3    = 2
    SILVER_1    = 3
    SILVER_2    = 4
    SILVER_3    = 5
    GOLD_1      = 6
    GOLD_2      = 7
    GOLD_3      = 8
    PLATINUM_1  = 9
    PLATINUM_2  = 10
    PLATINUM_3  = 11
    DIAMOND_1   = 12
    DIAMOND_2   = 13
    DIAMOND_3   = 14
    ELITE       = 15
    CHAMPION    = 16
    UNREAL      = 17


class StatsCollectionType(Enum):
    FISH = 'collection_fish'
