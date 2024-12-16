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


class FortniteSeason:
    def __init__(self,
                 start_timestamp: int,
                 end_timestamp: int,
                 battlepass_level: str = None,
                 ranked_tracks: tuple = None
                 ) -> None:
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.battlepass_level = battlepass_level
        self.ranked_tracks = ranked_tracks


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


class Season(Enum):
    C1S1 = FortniteSeason(start_timestamp=1508889601, end_timestamp=1513123200)
    C1S2 = FortniteSeason(start_timestamp=1513209601, end_timestamp=1519171200)
    C1S3 = FortniteSeason(start_timestamp=1519257601, end_timestamp=1525046400)
    C1S4 = FortniteSeason(start_timestamp=1525132801, end_timestamp=1531353600)
    C1S5 = FortniteSeason(start_timestamp=1531353601, end_timestamp=1538006400)
    C1S6 = FortniteSeason(start_timestamp=1538006401, end_timestamp=1544054400)
    C1S7 = FortniteSeason(start_timestamp=1544054401, end_timestamp=1551312000)
    C1S8 = FortniteSeason(start_timestamp=1551312001, end_timestamp=1557360000)
    C1S9 = FortniteSeason(start_timestamp=1557360001, end_timestamp=1564617600)
    C1SX = FortniteSeason(start_timestamp=1564617601, end_timestamp=1570924800)
    C2S1 = FortniteSeason(
        start_timestamp=1571097601,
        end_timestamp=1582156800,
        battlepass_level='s11_social_bp_level'
    )
    C2S2 = FortniteSeason(
        start_timestamp=1582156801,
        end_timestamp=1592352000,
        battlepass_level='s11_social_bp_level'
    )
    C2S3 = FortniteSeason(
        start_timestamp=1592352001,
        end_timestamp=1598486400,
        battlepass_level=('s13_social_bp_level', 's11_social_bp_level')
    )
    C2S4 = FortniteSeason(
        start_timestamp=1598486401,
        end_timestamp=1606867200,
        battlepass_level='s14_social_bp_level'
    )
    C2S5 = FortniteSeason(
        start_timestamp=1606867201,
        end_timestamp=1615852800,
        battlepass_level='s15_social_bp_level'
    )
    C2S6 = FortniteSeason(
        start_timestamp=1615852801,
        end_timestamp=1623110400,
        battlepass_level='s16_social_bp_level'
    )
    C2S7 = FortniteSeason(
        start_timestamp=1623110401,
        end_timestamp=1631491200,
        battlepass_level='s17_social_bp_level'
    )
    C2S8 = FortniteSeason(
        start_timestamp=1631491201,
        end_timestamp=1638651540,
        battlepass_level='s18_social_bp_level'
    )
    C3S1 = FortniteSeason(
        start_timestamp=1638716400,
        end_timestamp=1647759540,
        battlepass_level='s19_social_bp_level'
    )
    C3S2 = FortniteSeason(
        start_timestamp=1647763140,
        end_timestamp=1654372800,
        battlepass_level='s20_social_bp_level'
    )
    C3S3 = FortniteSeason(
        start_timestamp=1654430400,
        end_timestamp=1663479000,
        battlepass_level='s21_social_bp_level'
    )
    C3S4 = FortniteSeason(
        start_timestamp=1663503780,
        end_timestamp=1670140800,
        battlepass_level='s22_social_bp_level'
    )
    C4S1 = FortniteSeason(
        start_timestamp=1670157000,
        end_timestamp=1678429800,
        battlepass_level='s23_social_bp_level'
    )
    C4S2 = FortniteSeason(
        start_timestamp=1678453200,
        end_timestamp=1686288600,
        battlepass_level='s24_social_bp_level',
        ranked_tracks=('2776dc', '9d7ebd')
    )
    C4S3 = FortniteSeason(
        start_timestamp=1686313800,
        end_timestamp=1692945000,
        battlepass_level='s25_social_bp_level',
        ranked_tracks=('ggOwuK', 'AjRdrb')
    )
    C4S4 = FortniteSeason(
        start_timestamp=1692966600,
        end_timestamp=1698994800,
        battlepass_level='s26_social_bp_level',
        ranked_tracks=('gXffl', 'yHNFu')
    )
    C4SOG = FortniteSeason(
        start_timestamp=1699016400,
        end_timestamp=1701576000,
        battlepass_level='s27_social_bp_level',
        ranked_tracks=('OiK9k9', 'hEKWqj')
    )
    C5S1 = FortniteSeason(
        start_timestamp=1701577740,
        end_timestamp=1709794800,
        battlepass_level='s28_social_bp_level',
        ranked_tracks=('EYpme7', 'd0zEcd', 'dmd372')
    )
    C5S2 = FortniteSeason(
        start_timestamp=1709951400,
        end_timestamp=1716533100,
        battlepass_level='s29_social_bp_level',
        ranked_tracks=('ch3353', 'a1m0n3', 'rrwpwg')
    )
    C5S3 = FortniteSeason(
        start_timestamp=1716508800,
        end_timestamp=1723777200,
        battlepass_level='s30_social_bp_level',
        ranked_tracks=('N4PK1N', 'L1GHT5', 'rrzuel')
    )
    C5S4 = FortniteSeason(
        start_timestamp=1723802400,
        end_timestamp=1730505599,
        battlepass_level='s31_social_bp_level',
        ranked_tracks=('S4LT3D', 'P0T4T0', 'rr9qlw', 'M4rC4S', 'L4nC3r')
    )
    C5SOG = FortniteSeason(
        start_timestamp=1730505600,
        end_timestamp=1733021940,
        battlepass_level='s32_social_bp_level',
        ranked_tracks=('P3PP3R', 'D13tDw', 'rr9qlw', 'W4FFL3', 'Fr3SkA')
    )
    C6S1 = FortniteSeason(
        start_timestamp=1733022000,
        end_timestamp=1740131940,
        battlepass_level='s33_social_bp_level',
        ranked_tracks=('rrhr6d', 'P3PP3R', 'SP1D3R', 'Gl4ss1', 'W4FFL3',
                       'G4RL1C', 'DR3AM5', 'M3M0RY')
    )

    def __new__(cls, value: FortniteSeason) -> 'Season':
        obj = object.__new__(cls)
        obj._value_ = value
        obj.start_timestamp = value.start_timestamp
        obj.end_timestamp = value.end_timestamp
        obj.battlepass_level = value.battlepass_level
        obj.ranked_tracks = value.ranked_tracks
        return obj


class RankingType(Enum):
    BATTLE_ROYALE   = 'ranked-br'
    ZERO_BUILD      = 'ranked-zb'
    ROCKET_RACING   = 'delmar-competitive'
    RELOAD          = 'ranked_blastberry_build'
    RELOAD_ZB       = 'ranked_blastberry_nobuild'
    BALLISTIC       = 'ranked-feral'
    OG              = 'ranked-figment-build'
    OG_ZERO_BUILD   = 'ranked-figment-nobuild'


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
    FISH      = 'collection_fish'
    CHARACTER = 'collection_character'
