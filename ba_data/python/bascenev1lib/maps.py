# Released under the MIT License. See LICENSE for details.
#
"""Standard maps."""
# pylint: disable=too-many-lines

from __future__ import annotations

from typing import TYPE_CHECKING, override

import bascenev1 as bs
import random

from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any


def register_all_maps() -> None:
    """Registering all maps."""
    for maptype in [
        Rudebuster,
        MewersLive,
        CardCastle,
    ]:
        bs.register_map(maptype)

class Rudebuster(bs.Map):
    """rude."""

    from delta.mapdata import rudebuster_mapdefs as defs

    name = 'Rude Buster'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'hockey', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rampagePreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh': bs.getmesh('rudebuster_stage'),
            'collision_mesh': bs.getcollisionmesh('rudebuster_stage'),
            'tex': bs.gettexture('deltafield'),
            'bgtex': bs.gettexture('rudebuster'),
            'bgmesh': bs.getmesh('rudebuster_bg'),
            'railing_collision_mesh': bs.getcollisionmesh('rudebuster_railing'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': self.preloaddata['collision_mesh'],
                'mesh': self.preloaddata['mesh'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['bgmesh'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )

        self.railing = bs.newnode(
            'terrain',
            attrs={
                'collision_mesh': self.preloaddata['railing_collision_mesh'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
    
    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        
        
        return random.choice([
            bs.MusicType.RUDE_BUSTER,
            bs.MusicType.RUDER_BUSTER,
            bs.MusicType.CH4_BUSTER,
            bs.MusicType.RAKUICHI_BUSTER
        ])

class MewersLive(bs.Map):
    """the nonexistent stage from
    pink's fight but i made it better"""

    from delta.mapdata import mewerslive_mapdefs as defs

    name = 'Mewers Live'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'mewersLivePreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh': bs.getmesh('mewers_live'),
            'collision_mesh': bs.getcollisionmesh('mewers_live'),
            'tex': bs.gettexture('mewers_live'), # everything is stored into a single nice texture... who's good at optimizing now huh >:3
            # i dont care lol
            'bgmesh': bs.getmesh('mewers_liveBG'),
            'kill_cmesh': bs.getcollisionmesh('mewers_live_death'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': self.preloaddata['collision_mesh'],
                'mesh': self.preloaddata['mesh'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['bgmesh'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['tex'],
            },
        )
        # kill_mat = []
        kill_mat = [shared.death_material]
        self.kill_node = bs.newnode(
            'terrain',
            attrs={
                'collision_mesh': self.preloaddata['kill_cmesh'],
                'materials': kill_mat,
            },
        )
        # oh yeah fun fact press ctrl shift k to uncomment
        # (and ctrl k to comment)
        
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.2, 1.2)
        gnode.ambient_color = (1.1, 1.2, 1.1)
        gnode.vignette_outer = (0.8, 0.8, 0.8)
        gnode.vignette_inner = (0.8, 0.8, 0.8)

    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        
        return bs.MusicType.MEW_MEW_KISSY

class CardCastle(bs.Map):
    """card caslte"""

    from delta.mapdata import cardcastle_mapdefs as defs

    name = 'Card Castle'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'cardcastlePreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        return {}

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        # yeah man im NOT using on_preload 
        # its just soo many assets + its only loadded once so. .,

        # not used or just collision
        bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': bs.getcollisionmesh('cardcastleDonut'),
                'mesh': bs.getmesh('cardcastleDonut'),
                'color_texture': bs.gettexture('cardCaslteDonut'),
                'materials': [shared.footing_material],
            },
        )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleDoor1BackCollide'),
                    'materials': [shared.footing_material],
                },
            )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleDoor2BackCollide'),
                    'materials': [shared.footing_material],
                },
            )
        

        self.nodes1= []
        self.nodes1.append(
            bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleDoor1'),
                    'mesh': bs.getmesh('cardcastleDoor1'),
                    'color_texture': bs.gettexture('cardcastleDoor1'),
                    'materials': [shared.footing_material],
                },
            )
        )
        
        self.nodes1.append(
            bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'mesh': bs.getmesh('cardcastleDoor1Hider'),
                    'color_texture': bs.gettexture('black'),
                    'materials': [shared.footing_material],
                },
            )
        )

        self.nodes2= []
        self.nodes2.append(
            bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleDoor2'),
                    'mesh': bs.getmesh('cardcastleDoor2'),
                    'color_texture': bs.gettexture('cardcastleDoor2'),
                    'materials': [shared.footing_material],
                },
            )
        )
        self.nodes2.append(
            bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'mesh': bs.getmesh('cardcastleDoor2Hider'),
                    'color_texture': bs.gettexture('black'),
                    'materials': [shared.footing_material],
                },
            )
        )

        # uh rooms
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleFloor'),
                    'mesh': bs.getmesh('cardcastleFloor'),
                    'color_texture': bs.gettexture('cardcastleFloor'),
                    'materials': [shared.footing_material],
                },
        )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleMainWall'),
                    'mesh': bs.getmesh('cardcastleMainWall'),
                    'color_texture': bs.gettexture('cardcastleWall'),
                    'materials': [shared.footing_material],
                },
        )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardCastleRoom1Wall'),
                    'mesh': bs.getmesh('cardCastleRoom1Wall'),
                    'color_texture': bs.gettexture('cardCastleRoom1'),
                    'materials': [shared.footing_material],
                },
        )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardCastleRoom2Wall'),
                    'mesh': bs.getmesh('cardCastleRoom2Wall'),
                    'color_texture': bs.gettexture('cardCastleRoom2'),
                    'materials': [shared.footing_material],
                },
        )
        bs.newnode(
                'terrain',
                delegate=self,
                attrs={
                    'collision_mesh': bs.getcollisionmesh('cardcastleWalls'),

                    'materials': [shared.footing_material],
                },
        )



        self.background = bs.newnode(
            'terrain',
            attrs={
                
                'mesh': bs.getmesh('thePadBG'),
                'lighting': False,
                'background': True,
                'color_texture': bs.gettexture('black'),
            },
        )
        
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.2, 1.2)
        gnode.ambient_color = (1.1, 1.2, 1.1)
        gnode.vignette_outer = (0.8, 0.8, 0.8)
        gnode.vignette_inner = (0.8, 0.8, 0.8)
        # mat
        self.door1_occupants = 0    
        self.door2_occupants = 0
        door_detection_mat1 = bs.Material()
        door_detection_mat2 = bs.Material()
        from bascenev1lib.actor.flag import FlagFactory
        door_detection_mat1.add_actions(
            conditions=(    
                ('they_have_material', shared.player_material),
                'or',
                ('they_have_material', FlagFactory.get().flagmaterial)

            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', bs.Call(self._handle_door_change, 1, True)),
                ('call', 'at_disconnect', bs.Call(self._handle_door_change, 1, False))
            ),
        )
        door_detection_mat2.add_actions(
            conditions=(    
                ('they_have_material', shared.player_material),
                'or',
                ('they_have_material', FlagFactory.get().flagmaterial)
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', bs.Call(self._handle_door_change, 2, True)),
                ('call', 'at_disconnect', bs.Call(self._handle_door_change, 2, False))
            ),
        )

        # Ok hitboxes
        hitbox_size = (8, 20, 5)
        position1=(-12.8, 0, -8.94)
        position2=(12.8, 0, -8.94)
       
        bs.newnode('region',delegate=self,
                    attrs={'scale': hitbox_size,
                           'position': position1,
                           'type': 'box',
                           'materials': [door_detection_mat1]})
        bs.newnode('region',delegate=self,
                    attrs={'scale': hitbox_size,
                           'position': position2,
                           'type': 'box',
                           'materials': [door_detection_mat2]})
    
    def _handle_door_change(self, door_id: int, entering: bool):
        print('hi')
        if door_id == 1:
            self.door1_occupants += 1 if entering else -1
            count = self.door1_occupants
            nodes = self.nodes1
        else:
            self.door2_occupants += 1 if entering else -1
            count = self.door2_occupants
            nodes = self.nodes2

        # only animate if the first to enter, or leave
        if (entering and count == 1) or (not entering and count == 0):
            target_opacity = 0.1 if entering else 1.0
            for node in nodes:
           
                bs.animate(node, 'opacity', {0: node.opacity, 0.25: target_opacity})


  
    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        
        return bs.MusicType.KING_BOSS