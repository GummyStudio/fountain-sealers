
import bascenev1 as bs, random
from delta.actor.particals import Partical, ParticalFactory
from delta.actor.damagetext import DamageText
from bascenev1lib.gameutils import SharedObjects



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
    def __init__(self, position, source_player):
        
        self.position = position
        self.source_player = source_player
        self.active = True
        self.snowgrave_mat = bs.Material()
        self.snowgrave_mat.add_actions(
            conditions=
                ('they_have_material', SharedObjects.get().object_material)
            ,
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                (
                    'call',
                    'at_connect',
                    lambda: self.handle_touched_snowgrave(True)
                ),
                (
                    'call',
                    'at_disconnect',
                    lambda: self.handle_touched_snowgrave(False)
                ),
            ),
        )
        ParticalFactory.get().snowgrave_sfx.play(2.5)
        self.light = bs.newnode('light', attrs={
            'position': position,
            'color': (0.2, 0.5, 1.0),
            'radius': 0.2,
        })
        self.nodes: list[bs.Node] = []
        self.spaz_specific_hits = {}
        self.spaz_touch_cooldown = bs.time()
        bs.timer(1, self.make)
        self.tick_timer = bs.timer(0.1, self.handle_nodes_inside, repeat=True)

    def handle_nodes_inside(self):
        if not self.active:
            return
        from bascenev1lib.actor.spaz import Spaz
        for node in self.nodes:
            if node.getdelegate(Spaz):
                # cooldown
                if not (self.spaz_touch_cooldown - bs.time() < 0):
                    return
                self.spaz_touch_cooldown = bs.time() + 0.1

                actor = node.getdelegate(Spaz)
                assert isinstance(actor, Spaz)
                actor_id = id(actor)

                actor.handlemessage(bs.HitMessage(
                    flat_damage=20,
                    source_player=self.source_player
                ))
                actor.impulse(y=15)
                if actor_id not in self.spaz_specific_hits:
                    self.spaz_specific_hits[actor_id] = 0

                self.spaz_specific_hits[actor_id] += 1
                print(self.spaz_specific_hits[actor_id])

                if self.spaz_specific_hits[actor_id] > 15 and not actor.snowgraved:
                    actor.snowgraved = True
                   

            else:
                if node.getdelegate(bs.Actor):
                    actor = node.getdelegate(bs.Actor)
                    assert isinstance(actor, bs.Actor)
                    actor.impulse(y=40)

                    



    def handle_touched_snowgrave(self, entered):

        

        collision = bs.getcollision()
        node = collision.opposingnode

        if not node:
            return
        if entered:
            self.nodes.append(node)
        else:
            self.nodes.remove(node)

        
        
    
    def make(self):

        hitbox_size = (2, 10, 2)
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
                           'position': self.position,
                           'type': 'box',
                           'materials': [self.snowgrave_mat,SharedObjects.get().attack_material]})
        timer=0.1
        for _ in range(30):
            bs.timer(timer, self.emit)
            timer += 0.1

        bs.timer(timer, self.end)
    
    def end(self):
        self.active = False
        self.light.delete()
        self.hitbox.delete()
        self.loc.delete()
        self.tick_timer = None
        self.spaz_specific_hits = {}
        self.nodes.clear()
        

        
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
                    random.uniform(-0.6, 0.6),
                    random.uniform(1.0, 2.0),
                    random.uniform(-0.6, 0.6)
                ),
                gravity_scale=1.2,
                alive_for=8,
                collide_with=None
            ).autoretain()
            try: # just incase it hits the void or something
                bs.timer(
                    0.35,
                    lambda: (
                        setattr(p.node, 'gravity_scale', -1.3),
                        p.impulse(random.uniform(-1.5, 1.5), 0)
                    )
                )
            except: pass
            
        bs.animate(self.light, 'radius', {
            0: 0.2,
            0.1: 0.65,
            0.2: 0.2
        })
        
