# Released under the MIT License. See LICENSE for details.
#
"""Standard maps."""
# pylint: disable=too-many-lines

from __future__ import annotations

from typing import TYPE_CHECKING, override

import bascenev1 as bs
import random
from babase._logging import deltalog

from bascenev1lib.gameutils import SharedObjects
from delta.actor.particals import Partical, ParticalFactory


if TYPE_CHECKING:
    from typing import Any


def register_all_maps() -> None:
    """Registering all maps."""
    for maptype in [
        Rudebuster,
        MewersLive,
        CardCastle,
        JevilStage,
        MettatonStage,
        FlowerMan,
        TitanStage,
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
        return ['melee', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rudebusterPreview'

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
            bs.MusicType.RAKUICHI_BUSTER,
            bs.MusicType.MIX_SOUL_BUSTER
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
        
        return random.choice([
            bs.MusicType.MEW_MEW_KISSY,
            bs.MusicType.MIX_MEW_MEW_KISSY_JACKPOT,
            bs.MusicType.MIX_MEW_MEW_KISSY_ROCK
        ])


class JevilStage(bs.Map):
    """Jevil's battle stage 
    in bombsquad fountain sealers"""

    from delta.mapdata import jevilstage_mapdefs as defs

    name = 'Chaotic Carousel'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'jevilStagePreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        # we can assume if we're mell's stages,
        # we use the same name for cmesh and mesh
        name = 'jevil_stage'
        data: dict[str, Any] = {
            'mesh': bs.getmesh(name),
            'collision_mesh': bs.getcollisionmesh(name),
            'tex': bs.gettexture(name), # everything is still stored in a single tex because im awesome
            'bgmesh': bs.getmesh(f'{name}BG'),
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
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.2, 1.2)
        gnode.ambient_color = (1.1, 1.2, 1.1)
        gnode.vignette_outer = (0.8, 0.8, 0.8)
        gnode.vignette_inner = (0.8, 0.8, 0.8)

    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        return bs.MusicType.JEVIL_BOSS

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
        deltalog.debug('player went through door')
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
        
        return random.choice([
            bs.MusicType.KING_BOSS,
            bs.MusicType.MIX_CHAOS_KING,
        ])
    

class MettatonStage(bs.Map):
    """oooohhhh yeahhh"""

    from delta.mapdata import mettaton_mapdefs as defs

    name = 'Mettaton\'s Stage'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'mettatonStagePreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        # we can assume if we're mell's stages,
        # we use the same name for cmesh and mesh
        name = 'mettatonStage'
        data: dict[str, Any] = {
            'mesh': bs.getmesh(name),
            'collision_mesh': bs.getcollisionmesh(name),
            'tex': bs.gettexture(name+'Color'), 
            'bgmesh': bs.getmesh('thePadBG'),
            'black': bs.gettexture('black'),
            'meshbottom': bs.getmesh(name+"Bottom"),
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
                'color_texture': self.preloaddata['black'], # mb gang bs.gettexture('blac'),
            },
        )
        self.bottom = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['meshbottom'],
                'color_texture': self.preloaddata['tex'],
            },
        )
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.0, 1.0, 1.0)
        gnode.ambient_color = (1.1, 1.2, 1.1)
        gnode.vignette_outer = (0.8, 0.8, 0.8)
        gnode.vignette_inner = (0.8, 0.8, 0.8)

    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        return bs.MusicType.DEATH_BY_GLAMOUR
    
class FlowerMan(bs.Map):
    """HE SOLOS BRO"""

    class PetalPlatform:

        def __init__(self, preloaddata, position, lifespan: int | None = None, cfg=None):

            self.lifespan = lifespan
            self.cfg = cfg

            self.assets = {
                'anim1': preloaddata['platform1'],
                'anim2': preloaddata['platform2'],
                'anim3': preloaddata['platform3'],

            }

            self.alive = True
            self.anim_index = 1
            self.partical = Partical(
                mesh=self.assets['anim1'],
                texture=random.choice(preloaddata['platform_texs']),
                position=position, 
                body='landMine',
                gravity_scale=0.0,
                velocity=(0,0,0),  
                alive_for=lifespan+2.5 if lifespan else None, 
                collide_with=None,
                animate_in={
                    0: 0.0,
                    0.65: 1.0
                }
            ).autoretain()




            self.position=position

            self.visual_position=(
                position[0]+0.08,
                position[1],
                position[2],
            )
            self.hitbox = bs.Node(None)

            if lifespan is not None:

                bs.timer(lifespan, self.die)


            bs.timer(random.uniform(0.81, 0.9), self.next_anim)

            
           

            bs.timer(0.2, self.spawn)

        def spawn(self):
            hitbox_size = (1.5, 1, 1.5)
            self.hitbox=bs.newnode('region',
                attrs={'scale': hitbox_size,
                'position':self.visual_position,
                'type': 'box',
                'materials': [SharedObjects.get().collision, SharedObjects.get().footing_material]})

        def is_alive(self):
            return bool(
                self.alive and self.partical.exists()
            )


        def die(self):

            def cleanup():
                self.alive = False
                # Delete the hitbox
                self.hitbox.delete()
                # kILL OURSEFLS
                if self.cfg in bs.getactivity().map.occupied_cells:
                    del bs.getactivity().map.occupied_cells[self.cfg]

            bs.timer(1.0, bs.Call(setattr, self.partical.node, 'flashing', True))
            bs.timer(2.6, cleanup)

        def next_anim(self):
            if self.is_alive():
                self.partical.node.position = self.position
                self.partical.node.mesh = self.assets['anim'+str(self.anim_index)]
                if self.anim_index == 3:
                    self.anim_index = 1
                else:
                    self.anim_index += 1
                bs.timer(0.6, self.next_anim)

    from delta.mapdata import flowerman_mapdefs as defs


    name = 'Flower Man'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'team_flag', 'keep_away','king_of_the_hill']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'flowermanPreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        # we can assume if we're mell's stages,
        # we use the same name for cmesh and mesh
        data: dict[str, Any] = {
     
            'bgmesh': bs.getmesh('thePadBG'),
            'bgtex': bs.gettexture('alwaysLandBGColor'),
            # petal animation
            'platform1': bs.getmesh('flowerPlatform1'),
            'platform2': bs.getmesh('flowerPlatform2'),
            'platform3': bs.getmesh('flowerPlatform3'),
            'platform_texs': [
                bs.gettexture('flowerPlatformColor'),
                bs.gettexture('flowerPlatformColor1'),
                bs.gettexture('flowerPlatformColor2'),
                bs.gettexture('flowerPlatformColor3'),
                bs.gettexture('flowerPlatformColor4'),
                bs.gettexture('flowerPlatformColor5'),
                bs.gettexture('flowerPlatformColor6'),
                bs.gettexture('flowerPlatformColor7'),
                bs.gettexture('flowerPlatformColor8'),
                bs.gettexture('flowerPlatformColor9'),
            ],
      
            'big_vine': bs.getmesh('floweryBigVine'),
            'big_vine_tex':bs.gettexture('bigVineColor'),

        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.big_vine_pos = (0, -4, -15)
        self.big_vine=Partical(
            mesh=self.preloaddata['big_vine'],
            texture=self.preloaddata['big_vine_tex'],
            mesh_scale=1.5,
            position=self.big_vine_pos,
            body='puck',
            gravity_scale=0.0,
            velocity=(0,0,0),
            alive_for=None,
            collide_with=None
        ).autoretain()
       
        
        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['bgmesh'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )

        
        
        gnode = bs.getactivity().globalsnode
        gnode.tint = (0.8, 0.8, 0.8)
        gnode.ambient_color = (1.1, 1.2, 1.1)
        gnode.vignette_outer = (0.8, 0.8, 0.8)
        gnode.vignette_inner = (0.8, 0.8, 0.8)
        # This map is SUPER unique, uses PETAL PLATFORMS that come in and out for play.
        self.do_rotate()

        # petal platforms
        self.all_platforms = []
        self.platform_y = 0.2
       
      
      
       
    
        self.grid_size = 1.2
        self.grid_offs = [0.15, -0.3]
        self.occupied_cells = {} # { (grid_x, grid_y): platform_obj }
        
        for pos in [
            self.defs.points['flag_default'],
            self.defs.points['flag1'],
            self.defs.points['flag2'],
            self.defs.points['powerup_spawn1'],
            self.defs.points['powerup_spawn2'],
            self.defs.points['powerup_spawn3'],
            self.defs.points['powerup_spawn4'],
            self.defs.points['powerup_spawn5'],
            self.defs.points['powerup_spawn6'],
            self.defs.points['powerup_spawn7'],
            self.defs.points['powerup_spawn8'],
        ]:
            self.try_spawn_grid_platform(pos[0], pos[2], None)
               
        for box in [
            self.defs.points['ffa_spawn1'],
            self.defs.points['ffa_spawn2'],
            self.defs.points['ffa_spawn3'],
            self.defs.points['ffa_spawn4'],
            self.defs.points['spawn1'],
            self.defs.points['spawn2'],
        ]:
           
            center_x, center_z = box[0], box[2]
            width, depth = box[3], box[5]
            
            start_x = center_x - (width / 2.0)
            start_z = center_z - (depth / 2.0)
            
            for i in range(int(max(1, width+2))):
                for j in range(int(max(1, depth+2))):
                    target_x = (int((start_x + i) / self.grid_size) * self.grid_size)
                    target_z = (int((start_z + j) / self.grid_size) * self.grid_size)
                    
                    self.try_spawn_grid_platform(target_x, target_z)
                        

        for _ in range(5):
            self.try_spawn_grid_platform(random.randint(-5,5), random.randint(-5,5), random.uniform(20, 70))
        bs.timer(0.1, self.attempt_platform)
        bs.timer(0.1, self.clean, repeat=True)

    def clean(self):
        self.all_platforms = [p for p in self.all_platforms if p.is_alive()]
    
   
    def get_random_free_space(self):
        candidates = []
        for x in range(-4, 5):
            for z in range(-4, 5):
                world_x = x * self.grid_size
                world_z = z * self.grid_size
                
                if (x**2 + z**2)**0.5 >= 1:
                    grid_key = self.get_grid_pos(world_x, world_z)
                    
                    if grid_key not in self.occupied_cells:
                        candidates.append((world_x, world_z))
        
        if candidates:
            return random.choice(candidates)
        return None # map ful
      
    def attempt_platform(self):   
        pos = self.get_random_free_space()   

        
     
            
        if not len(self.all_platforms) > 45 and pos:
            self.try_spawn_grid_platform(
                pos[0], pos[1],
                random.uniform(10, 30)
            )
            
            
           
        bs.timer(random.uniform(0.2, 0.8), self.attempt_platform)
        
        
    def get_grid_pos(self, x, z):
        return (round(x / self.grid_size)+self.grid_offs[0], round(z / self.grid_size)+self.grid_offs[1])

    def try_spawn_grid_platform(self, x, z, lifespan=None):
        grid_x, grid_y = self.get_grid_pos(x, z)
        
        if (grid_x, grid_y) not in self.occupied_cells:
            pos = (grid_x*self.grid_size, self.platform_y, grid_y*self.grid_size)
            plat = self.PetalPlatform(self.preloaddata, pos, lifespan=lifespan, cfg=(grid_x, grid_y))
            
            self.occupied_cells[(grid_x, grid_y)] = plat
            self.all_platforms.append(plat)
            return plat
        return None

    def fix_the_fucking_vine_oml(self):
       
        dir_x = 0.2
        dir_z = 0
        pos = self.big_vine.node.position
        force = -0.2
        self.big_vine.node.handlemessage(
            'impulse',
            pos[0],
            pos[1],
            pos[2]+0.2,
            0, 0, 0,
            force,
            force,
            0,
            0,
            dir_x,
            0,
            dir_z,
        )
        bs.timer(0.5, bs.Call(self.do_rotate))
    
    def do_rotate(self):
        if not self.big_vine.exists():
            return
        self.big_vine.node.velocity = (0, 0, 0) 
        self.big_vine.node.position = self.big_vine_pos
        bs.timer(0.1, bs.Call(self.fix_the_fucking_vine_oml))
        
  
        
   
    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        return bs.MusicType.FLOWER_MAN

class TitanStage(bs.Map):
    """we need to lock in"""

    from delta.mapdata import titanstage_mapdefs as defs

    name = 'Titan'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee','team_flag', 'king_of_the_hill', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'titanPreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh': bs.getmesh('titanStageLevel'),
            'collision_mesh': bs.getcollisionmesh('titanStageLevel'),
            
            'tex': bs.gettexture('sancuary'),
            'black': bs.gettexture('black'),
            'bgmesh': bs.getmesh('titanStageBG'),

            'collision': bs.getcollisionmesh('titanStageBGCollision'),

            'titan': bs.getmesh('titan'),
            'titan_textures': [
                bs.gettexture('titan/titan0'),
                bs.gettexture('titan/titan1'),
                bs.gettexture('titan/titan2'),
                bs.gettexture('titan/titan4'),
                bs.gettexture('titan/titan5'),
                bs.gettexture('titan/titan6'),
                bs.gettexture('titan/titan7'),
            ],

            

            'foreground': bs.getmesh('titanForeground'),
            'foreground_smoke': bs.getmesh('titanForegroundSmoke'),
            'background_smoke': bs.getmesh('titanStageSmoke'),
            'smoke_tex': bs.gettexture('titanSmoke'),

            'glass': bs.gettexture('glass'),
            
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
                'color_texture': self.preloaddata['black'],
            },
        )

        
        bs.newnode(
            'terrain',
            attrs={
                'collision_mesh': self.preloaddata['collision'],
            },
        )

         
        bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['foreground'],
                'color_texture': self.preloaddata['black'],
            },
        )
        bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['foreground_smoke'],
                'color_texture': self.preloaddata['smoke_tex'],
            },
        )
        bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['background_smoke'],
                'color_texture': self.preloaddata['smoke_tex'],
            },
        )

        self.titan =  bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['titan'],
                'color_texture': self.preloaddata['titan_textures'][0],
            },
        )
        self.anim_index = 0

        self.plat1_occupants = 0    
        self.plat2_occupants = 0
        plat_detection_mat1 = bs.Material()
        plat_detection_mat2 = bs.Material()
        from bascenev1lib.actor.spazfactory import SpazFactory
        from bascenev1lib.actor.flag import FlagFactory
        # only flags and spazes can walk on these
        plat_detection_mat1.add_actions(('modify_part_collision', 'collide', False))
        plat_detection_mat2.add_actions(('modify_part_collision', 'collide', False))
        plat_detection_mat1.add_actions(
            conditions=(    
                ('they_have_material', SpazFactory.get().roller_material),
                'or',
                ('they_have_material', FlagFactory.get().flagmaterial),
                'or',
                ('they_have_material', SpazFactory.get().spaz_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('message', 'their_node', 'at_connect', 'footing', 1),
                ('message', 'their_node', 'at_disconnect', 'footing', -1),
                ('call', 'at_connect', bs.Call(self._handle_touch_plat, 1, True)),
                ('call', 'at_disconnect', bs.Call(self._handle_touch_plat, 1, False))
            ),
        )
        plat_detection_mat2.add_actions(
            conditions=(    
                ('they_have_material', SpazFactory.get().roller_material),
                'or',
                ('they_have_material', FlagFactory.get().flagmaterial),
                'or',
                ('they_have_material', SpazFactory.get().spaz_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('message', 'their_node', 'at_connect', 'footing', 1),
                ('message', 'their_node', 'at_disconnect', 'footing', -1),
                ('call', 'at_connect', bs.Call(self._handle_touch_plat, 2, True)),
                ('call', 'at_disconnect', bs.Call(self._handle_touch_plat, 2, False))
            ),
        )
        self.glass1 = bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': bs.getcollisionmesh('titanStageGlass1'),
                'mesh': bs.getmesh('titanStageGlass1'),
                'color_texture': self.preloaddata['glass'],
                'materials': [plat_detection_mat1],
                'opacity': 0.0
            },
        )

        self.glass2 = bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': bs.getcollisionmesh('titanStageGlass2'),
                'mesh': bs.getmesh('titanStageGlass2'),
                'color_texture': self.preloaddata['glass'],
                'materials': [ plat_detection_mat2],
                'opacity': 0.0
            },
        )



        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        bs.timer(0.175, self.animate_titan, repeat=True)
    
    def animate_titan(self):
        if not self.titan:
            return
        self.titan.color_texture = self.preloaddata['titan_textures'][self.anim_index]
        self.anim_index += 1
        if self.anim_index == 6:
            self.anim_index = 0
    
    def _handle_touch_plat(self, id: int, entering: bool):
        if id == 1:
            self.plat1_occupants += 1 if entering else -1
            count = self.plat1_occupants
            node = self.glass1
        else:
            self.plat2_occupants += 1 if entering else -1
            count = self.plat2_occupants
            node = self.glass2

        # only animate if the first to enter, or leave
        if (entering and count == 1) or (not entering and count == 0):
            target_opacity = 1.0 if entering else 0.0
            bs.animate(node, 'opacity', {0: node.opacity, 0.1: target_opacity})


    
    @override
    @classmethod
    def get_music_type(cls) -> bs.MusicType:
        
        
        return random.choice([
            bs.MusicType.TITAN,
            bs.MusicType.MIX_SPADE,
            bs.MusicType.MIX_JAGGED_BLADE
        ])
