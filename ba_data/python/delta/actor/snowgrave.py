
import bascenev1 as bs, random
from delta.actor.particals import Partical, ParticalFactory


class SnowgraveProp(bs.Actor):
    def __init__(self, position, meshes):
        super().__init__()

class Snowgrave:
    """
        Cast a snowgrave in this position. 

        This creates an area that makes bomb icey
        Slowly damages Spaz's and freezes them and eventually snowgraves them
        (see class above)

    """
    def __init__(self, position):
        self.position = position
        ParticalFactory.get().snowgrave_sfx.play(2.5)
        self.light = bs.newnode('light', attrs={
            'position': position,
            'color': (0.2, 0.5, 1.0),
            'radius': 0.2,
        })
        bs.timer(1, self.make)
    
    def make(self):
        hitbox_size = (20, 99)
        self.loc=bs.newnode('locator',
                    attrs={'shape': 'box',
                           'position': self.position,
                           'color': (1,1,1),
                           'opacity': 1.0,
                           'draw_beauty': True,
                           'size': hitbox_size,
                           'additive': False})
                           
        
        self.hitbox=bs.newnode('region',
                    attrs={'scale': hitbox_size,
                           'type': 'box',
                           'materials': []})
        timer=0.1
        for _ in range(30):
            bs.timer(timer, self.emit)
            timer += 0.1

        bs.timer(timer, self.end)
    
    def end(self):
        self.light.delete()
        self.hitbox.delete()
        self.loc.delete()

        
    def emit(self):
        bs.emitfx(
            position=self.position,
            count=10,
            spread=0.025,
            velocity=(
                0, 
                20, 
                0
            ),
            chunk_type='ice',
        )
        bs.emitfx(
            position=self.position,
            count=4,
            spread=0.09,
            velocity=(
                random.uniform(-0.2, 0.2), 
                10, 
                random.uniform(-0.2, 0.2)
            ),
            chunk_type='ice',
        )
        if random.randint(0, 1) == 0:
            p=Partical(
                position=self.position,
                texture=ParticalFactory.get().snowflake_tex, 
                mesh=ParticalFactory.get().snowflake_mesh,
                mesh_scale=0.2,
                body='puck',
                velocity=(
                    random.uniform(-1.5, 1.5),
                    random.uniform(1.0, 8.0),
                    random.uniform(-1.5, 1.5)
                ),
                gravity_scale=0.0,
                alive_for=8,
                collide_with=None
            ).autoretain()
            
        bs.animate(self.light, 'radius', {
            0: 0.2,
            0.1: 0.65,
            0.2: 0.2
        })
        
