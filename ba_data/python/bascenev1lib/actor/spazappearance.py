# Released under the MIT License. See LICENSE for details.
#
"""Appearance functionality for spazzes."""
from __future__ import annotations

import bascenev1 as bs
from enum import Enum
class CharacterTag(Enum):
    """ 
        basically, the thing from bser idek
        i just like orginization
    """

    # Series
    UNDERTALE = 'Undertale'
    DELTARUNE = 'Deltarune'

    # Species
    HUMAN = 'Human'
    MONSTER = 'Monster'

    # Role
    LIGHTER = 'Lighter'
    DARKNER = 'Darkner'
    HERO = 'Hero'
    BYSTANDER = 'Neutral'
    ENEMY = 'Enemy'

    # Gender 
    FEMALE = 'Female'
    MALE = 'Male'
    NONBINARY = 'Non Binary'
    UNKNOWN_GENDER = 'Gender Unknown'

    # Misc
    MEME = 'Meme'
    

def get_appearances(include_locked: bool = False) -> list[str]:
    """Get the list of available spaz appearances."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    plus = bs.app.plus
    assert plus is not None

    assert bs.app.classic is not None
    startup = bs.app.classic.startup
    disallowed = []

    if not include_locked:
        # Automatec process, yay!!
        # Check the store if we unlocked it, otherwise just say no to it
        for item in startup.store:
            if not startup.gameconfig[startup.store[item]['config']]:
                disallowed.append(item)



    return [
        s
        for s in list(bs.app.classic.spaz_appearances.keys())
        if s not in disallowed
    ]


class Appearance:
    """Create and fill out one of these suckers to define a spaz appearance."""

    def __init__(self, name: str):
        assert bs.app.classic is not None
        self.name = name
        if self.name in bs.app.classic.spaz_appearances:
            raise RuntimeError(
                f'spaz appearance name "{self.name}" already exists.'
            )
        bs.app.classic.spaz_appearances[self.name] = self
        self.color_texture = 'null'
        self.color_mask_texture = 'null'
        self.icon_texture = 'null'
        self.icon_mask_texture = 'null'
        self.head_mesh = 'none'
        self.torso_mesh = 'none'
        self.pelvis_mesh = 'none'
        self.upper_arm_mesh = 'none'
        self.forearm_mesh = 'none'
        self.hand_mesh = 'none'
        self.upper_leg_mesh = 'none'
        self.lower_leg_mesh = 'none'
        self.toes_mesh = 'none'
        self.jump_sounds: list[str] = []
        self.attack_sounds: list[str] = []
        self.impact_sounds: list[str] = []
        self.death_sounds: list[str] = []
        self.pickup_sounds: list[str] = []
        self.fall_sounds: list[str] = []
        self.style = 'spaz'
        self.tags: list[CharacterTag] = []
        self.default_color: tuple[float, float, float] | None = None
        self.default_highlight: tuple[float, float, float] | None = None


def register_appearances() -> None:
    """Register our builtin spaz appearances."""

    # This is quite ugly but will be going away so not worth cleaning up.
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    # Spaz #######################################
    t = Appearance('Vessel')
    t.color_texture = 'neoSpazColor'
    t.color_mask_texture = 'neoSpazColorMask'
    t.icon_texture = 'neoSpazIcon'
    t.icon_mask_texture = 'neoSpazIconColorMask'
    t.head_mesh = 'neoSpazHead'
    t.torso_mesh = 'neoSpazTorso'
    t.pelvis_mesh = 'neoSpazPelvis'
    t.upper_arm_mesh = 'neoSpazUpperArm'
    t.forearm_mesh = 'neoSpazForeArm'
    t.hand_mesh = 'neoSpazHand'
    t.upper_leg_mesh = 'neoSpazUpperLeg'
    t.lower_leg_mesh = 'neoSpazLowerLeg'
    t.toes_mesh = 'neoSpazToes'
    t.jump_sounds = ['spazJump01', 'spazJump02', 'spazJump03', 'spazJump04']
    t.attack_sounds = [
        'spazAttack01',
        'spazAttack02',
        'spazAttack03',
        'spazAttack04',
    ]
    t.impact_sounds = [
        'spazImpact01',
        'spazImpact02',
        'spazImpact03',
        'spazImpact04',
    ]
    t.death_sounds = ['spazDeath01']
    t.pickup_sounds = ['spazPickup01']
    t.fall_sounds = ['spazFall01']
    t.style = 'spaz'
    t.tags = [
        CharacterTag.DELTARUNE,
        CharacterTag.HUMAN,
        CharacterTag.BYSTANDER,
        CharacterTag.NONBINARY,
    ]
    

    # Prince of the Dark ###################################
    t = Appearance('Ralsei')
    t.color_texture = 'ralseiColor'
    t.color_mask_texture = 'ralseiColorMask'
    t.icon_texture = 'ralsIcon'
    t.icon_mask_texture = 'ralsIconCM'
    t.head_mesh = 'ralseiHead'
    t.torso_mesh = 'ralseiTorso'
    t.pelvis_mesh = 'ralseiPelvis'
    t.upper_arm_mesh = 'ralseiUpperArm'
    t.forearm_mesh = 'ralseiForeArm'
    t.hand_mesh = 'ralseiHand'
    t.upper_leg_mesh = 'ralseiUpperLeg'
    t.lower_leg_mesh = 'ralseiLowerLeg'
    t.toes_mesh = 'none'
    ralsei_sounds = ['voicelines/ralsei/sound' + str(i + 1) + '' for i in range(4)]
    ralsei_hit_sounds = ['voicelines/ralsei/hit']
    t.jump_sounds = ralsei_sounds
    t.attack_sounds = ralsei_sounds
    t.impact_sounds = ralsei_hit_sounds
    t.death_sounds = ['voicelines/ralsei/death']
    t.pickup_sounds = ralsei_sounds
    t.fall_sounds = ['voicelines/ralsei/fall']
    t.style = 'bones'
    t.default_color = (0.0, 0.7699999999999998, 0.11999999999999998)
    t.default_highlight = (1, 0.08, 0.5)
    t.tags = [
        CharacterTag.DARKNER,
        CharacterTag.DELTARUNE,
        CharacterTag.MONSTER,
        CharacterTag.HERO,
        CharacterTag.MALE,
    ]

    # Prince of the Light ###################################
    t = Appearance('NoHatRalsei')
    t.color_texture = 'noHatseiColor'
    t.color_mask_texture = 'noHatseiColorMask'
    t.icon_texture = 'noHatseiIcon'
    t.icon_mask_texture = 'noHatseiIconCM'
    t.head_mesh = 'noHatseiHead'
    t.torso_mesh = 'noHatseiTorso'
    t.pelvis_mesh = 'none'
    t.upper_arm_mesh = 'noHatseiUpperArm'
    t.forearm_mesh = 'noHatseiForeArm'
    t.hand_mesh = 'noHatseiHand'
    t.upper_leg_mesh = 'noHatseiUpperLeg'
    t.lower_leg_mesh = 'noHatseiLowerLeg'
    t.toes_mesh = 'none'
    ralsei_sounds = ['voicelines/ralsei/sound' + str(i + 1) + '' for i in range(4)]
    ralsei_hit_sounds = ['voicelines/ralsei/hit']
    t.jump_sounds = ralsei_sounds
    t.attack_sounds = ralsei_sounds
    t.impact_sounds = ralsei_hit_sounds
    t.death_sounds = ['voicelines/ralsei/death']
    t.pickup_sounds = ralsei_sounds
    t.fall_sounds = ['voicelines/ralsei/fall']
    t.style = 'bones'
    t.default_color = (0.0, 0.7699999999999998, 0.11999999999999998)
    t.default_highlight = (1, 0.08, 0.5)
    t.tags = [
        CharacterTag.DARKNER,
        CharacterTag.DELTARUNE,
        CharacterTag.MONSTER,
        CharacterTag.HERO,
        CharacterTag.MALE,
    ]
    
    # The Human #####################################
    t = Appearance('Kris')
    t.color_texture = 'krisColor'
    t.color_mask_texture = 'krisColorMask'
    t.icon_texture = 'krisIcon'
    t.icon_mask_texture = 'krisIconCM'
    t.head_mesh = 'krisHead'
    t.torso_mesh = 'krisTorso'
    t.pelvis_mesh = 'krisPelvis'
    t.upper_arm_mesh = 'krisUpperArm'
    t.forearm_mesh = 'krisForeArm'
    t.hand_mesh = 'krisHand'
    t.upper_leg_mesh = 'krisUpperLeg'
    t.lower_leg_mesh = 'krisLowerLeg'
    t.toes_mesh = 'krisToes'
    t.jump_sounds = ['voicelines/kris/jump']
    t.attack_sounds = ['voicelines/kris/attack' + str(i + 1) + '' for i in range(4)]
    t.impact_sounds = ['voicelines/kris/hurt' + str(i + 1) + '' for i in range(4)]
    t.death_sounds = ['voicelines/kris/death']
    t.pickup_sounds = ['voicelines/kris/pickup']
    t.fall_sounds = ['voicelines/kris/fall']
    t.style = 'agent'
    t.default_color = (0.4588235294117647, 0.984313725490196, 0.9294117647058824)
    t.default_highlight = (0.9215686274509803, 0.0, 0.5843137254901961)
    t.tags = [
        CharacterTag.LIGHTER,
        CharacterTag.DELTARUNE,
        CharacterTag.HUMAN,
        CharacterTag.HERO,
        CharacterTag.NONBINARY,
    ]
    
    # The Monster #####################################
    t = Appearance('Susie')
    t.color_texture = 'susieColor'
    t.color_mask_texture = 'susieColorMask'
    t.icon_texture = 'susieIcon'
    t.icon_mask_texture = 'susieIconCM'
    t.head_mesh = 'susieHead'
    t.torso_mesh = 'susieTorso'
    t.pelvis_mesh = 'susiePelvis'
    t.upper_arm_mesh = 'susieUpperArm'
    t.forearm_mesh = 'susieForeArm'
    t.hand_mesh = 'susieHand'
    t.upper_leg_mesh = 'susieUpperLeg'
    t.lower_leg_mesh = 'susieLowerLeg'
    t.toes_mesh = 'susieToes'
    t.jump_sounds = ['voicelines/susie/jump' + str(i + 1) + '' for i in range(4)]
    t.attack_sounds = ['voicelines/susie/jump' + str(i + 1) + '' for i in range(4)]
    t.impact_sounds = ['voicelines/susie/hurt' + str(i + 1) + '' for i in range(2)]
    t.death_sounds = ['voicelines/susie/death']
    t.pickup_sounds = ['voicelines/susie/attack' + str(i + 1) + '' for i in range(4)]
    t.fall_sounds = ['voicelines/susie/fall']
    t.style = 'agent'
    t.default_color = (0.9725490196078431, 0.5137254901960784, 0.8431372549019608)
    t.default_highlight = (0.5333333333333333, 0.09019607843137255, 0.41568627450980394)
    t.tags = [
        CharacterTag.LIGHTER,
        CharacterTag.DELTARUNE,
        CharacterTag.MONSTER,
        CharacterTag.HERO,
        CharacterTag.FEMALE,
    ]
    
    # The Knight of Darkness #####################################
    t = Appearance('Roaring Knight')
    t.color_texture = 'knightColor'
    t.color_mask_texture = 'knightColorMask'
    t.icon_texture = 'knightIcon'
    t.icon_mask_texture = 'knightIconCM'
    t.head_mesh = 'knightHead'
    t.torso_mesh = 'knightTorso'
    t.pelvis_mesh = 'none'
    t.upper_arm_mesh = 'knightUpperArm'
    t.forearm_mesh = 'knightForeArm'
    t.hand_mesh = 'knightHand'
    t.upper_leg_mesh = 'knightUpperLeg'
    t.lower_leg_mesh = 'knightLowerLeg'
    t.toes_mesh = 'knightToes'
    knightsounds = ['voicelines/knight/sound' + str(i + 1) + '' for i in range(4)]
    t.jump_sounds = knightsounds
    t.attack_sounds = knightsounds
    t.impact_sounds = ['voicelines/knight/hurt' + str(i + 1) + '' for i in range(2)]
    t.death_sounds = ['voicelines/knight/death']
    t.pickup_sounds = knightsounds
    t.fall_sounds = ['voicelines/knight/fall']
    t.style = 'agent'
    t.default_color = (0.0, 0.0, 0.0)
    t.default_highlight = (1, 1, 1)
    t.tags = [
        CharacterTag.LIGHTER,
        CharacterTag.DELTARUNE,
        CharacterTag.MONSTER,
        CharacterTag.ENEMY,
        CharacterTag.UNKNOWN_GENDER,
    ]


    # Temmie Chan #####################################
    t = Appearance('Temmie')
    t.color_texture = 'temmieColor'
    t.color_mask_texture = 'temmieColorMask'
    t.icon_texture = 'temmieIconColor'
    t.icon_mask_texture = 'temmieIconColorMask'
    t.head_mesh = 'temmieHead'
    t.torso_mesh = 'temmieTorso'
    t.upper_arm_mesh = 'temmieUpperArm'
    t.forearm_mesh = 'temmieForeArm'
    t.hand_mesh = 'temmieHand'
    t.upper_leg_mesh = 'temmieUpperLeg'
    t.lower_leg_mesh = 'temmieLowerLeg'
    temmiesounds = []
    t.jump_sounds = temmiesounds
    t.attack_sounds = temmiesounds
    t.impact_sounds = []
    t.death_sounds = []
    t.pickup_sounds = temmiesounds
    t.fall_sounds = []
    t.style = 'agent'
    t.default_color = (0.0, 0.0, 0.0)
    t.default_highlight = (1, 1, 1)
    t.tags = [
        CharacterTag.LIGHTER,
        CharacterTag.DELTARUNE,
        CharacterTag.UNDERTALE,
        CharacterTag.MONSTER,
        CharacterTag.BYSTANDER,
        CharacterTag.FEMALE,
    ]

    # togore BEFORE asriel #####################################
    t = Appearance('Togore')
    t.color_texture = 'togoreColor'
    t.color_mask_texture = 'togoreColorMask'
    t.icon_texture = 'togoreIconColor'
    t.icon_mask_texture = 'togoreIconColorMask'
    t.head_mesh = 'togoreHead'
    t.torso_mesh = 'togoreTorso'
    t.forearm_mesh = 'togoreHand'
    t.lower_leg_mesh = 'togoreFoot'
    togoresounds = []
    t.jump_sounds = togoresounds
    t.attack_sounds = togoresounds
    t.impact_sounds = []
    t.death_sounds = []
    t.pickup_sounds = togoresounds
    t.fall_sounds = []
    t.style = 'agent'
    t.default_color = (0.0, 0.0, 0.0)
    t.default_highlight = (1, 1, 1)
    t.tags = [
        CharacterTag.UNDERTALE,
        CharacterTag.MONSTER,
        CharacterTag.BYSTANDER,
        CharacterTag.MALE,
        CharacterTag.MEME,
    ]



