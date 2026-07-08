# Released under the MIT License. See LICENSE for details.
#
"""Appearance functionality for spazzes."""
from __future__ import annotations

import bascenev1 as bs


def get_appearances(include_locked: bool = False) -> list[str]:
    """Get the list of available spaz appearances."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    plus = bs.app.plus
    assert plus is not None

    assert bs.app.classic is not None
    get_purchased = plus.get_v1_account_product_purchased
    disallowed = []
    if not include_locked:
        # Hmm yeah this'll be tough to hack...
        pass

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
        self.color_texture = ''
        self.color_mask_texture = ''
        self.icon_texture = ''
        self.icon_mask_texture = ''
        self.head_mesh = ''
        self.torso_mesh = ''
        self.pelvis_mesh = ''
        self.upper_arm_mesh = ''
        self.forearm_mesh = ''
        self.hand_mesh = ''
        self.upper_leg_mesh = ''
        self.lower_leg_mesh = ''
        self.toes_mesh = ''
        self.jump_sounds: list[str] = []
        self.attack_sounds: list[str] = []
        self.impact_sounds: list[str] = []
        self.death_sounds: list[str] = []
        self.pickup_sounds: list[str] = []
        self.fall_sounds: list[str] = []
        self.style = 'spaz'
        self.default_color: tuple[float, float, float] | None = None
        self.default_highlight: tuple[float, float, float] | None = None


def register_appearances() -> None:
    """Register our builtin spaz appearances."""

    # This is quite ugly but will be going away so not worth cleaning up.
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    # Spaz #######################################
    t = Appearance('Spaz')
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
    
    # The Knight #####################################
    t = Appearance('Kris')
    t.color_texture = 'krisColor'
    t.color_mask_texture = 'krisColorMask'
    t.icon_texture = 'krisIcon'
    t.earthportrait = 'earthbound/krisbound'
    t.EBwin = 'earthbound/krisbound'
    t.EBlose = 'earthbound/krisbound_lose'
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
    t.victory_sounds = ['voicelines/kris/win']
    t.gloat_sounds = ['voicelines/kris/gloat']
    t.style = 'agent'
    t.default_color = (0.4588235294117647, 0.984313725490196, 0.9294117647058824)
    t.default_highlight = (0.9215686274509803, 0.0, 0.5843137254901961)
    
    # The Monster #####################################
    t = Appearance('Susie')
    t.color_texture = 'susieColor'
    t.color_mask_texture = 'susieColorMask'
    t.icon_texture = 'susieIcon'
    t.earthportrait = 'earthbound/susiebound'
    t.EBwin = 'earthbound/susiebound_win'
    t.EBlose = 'earthbound/susiebound_lose'
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
    t.attack_sounds = ['voicelines/susie/attack' + str(i + 1) + '' for i in range(4)]
    t.victory_sounds = ['voicelines/susie/win']
    t.gloat_sounds = ['voicelines/susie/gloat']
    t.impact_sounds = ['voicelines/susie/hurt' + str(i + 1) + '' for i in range(2)]
    t.death_sounds = ['voicelines/susie/death']
    t.pickup_sounds = ['voicelines/susie/attack' + str(i + 1) + '' for i in range(4)]
    t.fall_sounds = ['voicelines/susie/fall']
    t.style = 'agent'
    t.default_color = (0.9725490196078431, 0.5137254901960784, 0.8431372549019608)
    t.default_highlight = (0.5333333333333333, 0.09019607843137255, 0.41568627450980394)
