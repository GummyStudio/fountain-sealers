"""Factory for particles and etc."""
import bascenev1 as bs
import random
from dataclasses import dataclass

@dataclass
class SnowgraveTouchedMessage:
    """A message informing a snowgrave
    that a node has touched its region."""
    state: bool

class ParticalFactory:
    """A collection of media and other resources used by particals.

    Also, just general assets used by the modpack

    A single instance of this is shared between all powerups
    and can be retrieved via Partical.get_factory().
    """
    _STORENAME = 'particalfact'

  
    def __init__(self) -> None:
        """Instantiate a ParticalFactory

        You shouldn't need to do this; call ParticalFactory.get()
        to get a shared instance.
        """
        self.snowflake_mesh = bs.getmesh('snowflake')
        self.snowflake_tex = bs.gettexture('snowflake')
        self.rudebuster_mesh = bs.getmesh('box')
        self.rudebuster_tex = bs.gettexture('white')

        self.snowgrave_sfx = bs.getsound('snd_snowgrave')
        self.snowgrave_crystal_spawn_sfx = bs.getsound('snowgraveCreate')
        self.snowgrave_crystal_break_sfx = bs.getsound('snowgraveBreak')
        self.snowgrave_tex = bs.gettexture('white')
        self.snowgrave_mesh = bs.getmesh('box')
       
        self.ominous_sound = bs.getsound('ominous')

        self.pink_bomb_explode_sfx = bs.getsound('pinkBoom')
        self.pink_short_laugh_sfx = bs.getsound('snd_pink_laugh_short')
        self.pink_throw1_sfx = bs.getsound('snd_pink_throw')
        self.pink_throw2_sfx = bs.getsound('snd_pink_throw2')

        self._tough_glove_weak_sfx = bs.getsound('tough_glove_weak')
        self._tough_glove_strong_sfx = bs.getsound('tough_glove_strong')
        self._snowgrave_mat: bs.Material | None = None
    
    # NOTE TO GUMMY: put fucking materials in fucking factory
    # before i kill you because fun fact actually too many materials
    # will eventually cause players to get kicked so kys

    # ok :((
    @property
    def snowgrave_mat(self) -> bs.Material:
        """A material that gives a SnowgraveTouchedMessage
        upon being touched."""
        from bascenev1lib.gameutils import SharedObjects
        if not self._snowgrave_mat:
            mat = self._snowgrave_mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', SharedObjects.get().object_material),
                actions=(
                    ('modify_part_collision', 'collide', True),
                    ('modify_part_collision', 'physical', False),
                    ('message', 'our_node', 'at_connect', SnowgraveTouchedMessage(True)),
                    ('message', 'our_node', 'at_disconnect', SnowgraveTouchedMessage(False)),
                ),
            )
        return self._snowgrave_mat


    @classmethod
    def get(cls):
        """Return a shared bs.PowerupBoxFactory object, creating if needed."""
        activity = bs.getactivity()
        if activity is None:
            raise bs.ContextError('No current activity.')
        factory = activity.customdata.get(cls._STORENAME)
        if factory is None:
            factory = activity.customdata[cls._STORENAME] = ParticalFactory()
        assert isinstance(factory, ParticalFactory)
        return factory


class Partical(bs.Actor):
    def __init__(self,
                position: tuple[float, float, float], 
                texture: bs.Texture, 
                mesh: bs.Mesh,
                
                mesh_scale: int,
                velocity: tuple[float, float, float] = (0, 0, 0), 
                random_vel: bool = False,
                random_range: float = 1.5,
                body: str = 'landMine',
                body_scale: int = 1.0,
                alive_for: float = 3.0,
                gravity_scale: int = 1.0,
                collide_with: str = "floor"# or nothing
        ):
        super().__init__()
        from bascenev1lib.gameutils import SharedObjects

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': ((
                    random.uniform(-random_range, random_range),
                    random.uniform(-random_range, random_range)*1.2,
                    random.uniform(-random_range, random_range),
                ) if random_vel else velocity),
                'color_texture': texture,
                'mesh': mesh,
                'mesh_scale': mesh_scale,
                'body': body,
                'body_scale': body_scale,
                'shadow_size': 0.44,
                'gravity_scale': gravity_scale,
                'materials': [SharedObjects.get().only_collide_with_floor_mat] if
                    collide_with == 'floor' else [SharedObjects.get().no_collide_mat]
            }
        )
        bs.timer(alive_for, bs.Call(self.handlemessage, bs.DieMessage()))
    def exists(self):
        return bool(self.node)
    
    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if not self.exists():
                return
            if msg.immediate:
                self.node.delete()
            else:
                bs.animate(
                    self.node,
                    'mesh_scale',
                    {
                        0: self.node.mesh_scale,
                        0.35: 0,
                    }
                )
                bs.timer(0.35, self.node.delete)
        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage(True))

            
        return super().handlemessage(msg)