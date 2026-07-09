"""Class for a snowgrave actor."""
from typing import override, Any
import bascenev1 as bs
import babase as ba
import random
from delta.actor.particals import Partical, ParticalFactory, SnowgraveTouchedMessage
from delta.actor.damagetext import DamageText
from bascenev1lib.gameutils import SharedObjects

class SnowgraveProp(bs.Actor):
    def __init__(self, position, meshes):
        super().__init__()

class Snowgrave(bs.Actor):
    """Cast a snowgrave in this position. 

    This creates an area that makes bomb icey
    Slowly damages Spaz's and freezes them and eventually snowgraves them
    (see class above)
    """
    def __init__(self, position: tuple, source_player: bs.Player):
        super().__init__()
        self.position = position
        self.source_player = source_player
        self.active = True
        self.loc = None
        self.snowgrave_mat = ParticalFactory.get().snowgrave_mat
        ParticalFactory.get().snowgrave_sfx.play(2.5)
        self.light = bs.newnode('light', delegate=self, attrs={
            'position': position,
            'color': (0.2, 0.5, 1.0),
            'radius': 0.2,
        })
        # animate it in nicely
        bs.animate(
            self.light,
            'radius',
            {
                0: 0,
                0.2: 0.2,
            }
        )
        self.nodes: list[bs.Node] = []
        self.spaz_specific_hits = {}
        self.spaz_touch_cooldown = bs.time()
        bs.timer(1, self.make)
        self.tick_timer = bs.Timer(0.1, self.handle_nodes_inside, repeat=True)

    def handle_nodes_inside(self):
        if not self.active:
            return
        from bascenev1lib.actor.spaz import Spaz
        # wanna clone here cuz we're iterating it somewhat
        for node in self.nodes[:]:
            # node doesn't exist, die
            if not node:
                self.nodes.remove(node)
                return
            delegate = node.getdelegate(bs.Actor)
            if isinstance(delegate, Spaz):
                # cooldown
                if not (self.spaz_touch_cooldown - bs.time() < 0):
                    return
                self.spaz_touch_cooldown = bs.time() + 0.1
                
                actor_id = id(delegate)

                # keep hitting it
                delegate.handlemessage(bs.HitMessage(
                    flat_damage=20,
                    source_player=self.source_player
                ))
                delegate.impulse(y=15)
                if actor_id not in self.spaz_specific_hits:
                    self.spaz_specific_hits[actor_id] = 0

                self.spaz_specific_hits[actor_id] += 1

                # if this spaz got hit 15 times, freeze it
                if self.spaz_specific_hits[actor_id] > 15 and not delegate.snowgraved:
                    delegate.snowgraved = True
                    delegate.handlemessage(bs.FreezeMessage())

            elif isinstance(delegate, bs.Actor):
                # any other actor gets swept away... hopefully
                delegate.impulse(y=40)


    def handle_touched_snowgrave(self, entered):
        collision = bs.getcollision()
        # try getting the node, but if it
        # doesnt exist then just nullify it
        try:
            node = collision.opposingnode
        except ba._error.NodeNotFoundError:
            node = None

        if not node:
            return
        if entered:
            self.nodes.append(node)
        else:
            self.nodes.remove(node)

    
    def make(self):
        hitbox_size = (2, 10, 2)
        # i'm assuming this is debug;
        # if not, just keep it true
        debug = False
        if debug:
            self.loc=bs.newnode('locator',
                        attrs={'shape': 'box',
                               'position': self.position,
                               'color': (1,1,1),
                               'opacity': 1.0,
                               'draw_beauty': True,
                               'size': hitbox_size,
                               'additive': False})
                           
        
        self.hitbox=bs.newnode('region',delegate=self,
                    attrs={'scale': hitbox_size,
                           'position': self.position,
                           'type': 'box',
                           'materials': [self.snowgrave_mat, SharedObjects.get().attack_material]})
        timer=0.1
        for _ in range(30):
            bs.timer(timer, self.emit)
            timer += 0.1

        bs.timer(timer, self.end)
    
    def end(self):
        self.active = False
        # delete nodes if they exist
        if self.light:
            self.light.delete()
        if self.hitbox:
            self.hitbox.delete()
        if self.loc:
            self.loc.delete()
        if self.tick_timer:
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
            scale=1.3,
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
            scale=1.2,
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
    
    @override
    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            self.end()
        elif isinstance(msg, SnowgraveTouchedMessage):
            # just fallback to our function
            self.handle_touched_snowgrave(msg.state)
        else:
            return super().handlemessage(msg)
        return None
    
    @override
    def exists(self) -> bool:
        # should use something else 
        # than the light maybe??
        # REMINDER: this gets used for autoretain
        return bool(self.light)
