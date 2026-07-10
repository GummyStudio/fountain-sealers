"""Class for a snowgrave actor."""
from typing import override, Any
import bascenev1 as bs
import babase as ba
import random
from delta.actor.particals import Partical, ParticalFactory, SnowgraveTouchedMessage
from delta.actor.damagetext import DamageText
from bascenev1lib.gameutils import SharedObjects

class SnowgraveCrystal:
    """
    basically a snowgrave thingy like what friend chicken was in 

    also it'll break eventually and reveal the frozen spaz
    
    also DONT make this an actor all the classes already have a diemessage and obb messge
    """
    def __init__(self, position, character, color, highlight, name):
        # Ok spawn a partical and when it dies we do cool thing

        lifespan = 10
        # i got lazy ok
        self.spazdata = {
            'pos': position,
            'char': character,
            'clr': color,
            'high': highlight,
            'name': name
        }
        velocity = (
                    random.uniform(-1.8, 1.8),
                    5,
                    random.uniform(-1.8, 1.8)
            )

        ParticalFactory.get().snowgrave_crystal_spawn_sfx.play()
        self.partical=Partical(
            position=(
                position[0],
                position[1] + 1, # brodie spawned IN THE FLOOOR
                position[2]
            ),
            texture=ParticalFactory.get().snowgrave_tex,
            mesh=ParticalFactory.get().snowgrave_mesh,
            mesh_scale=1.0,
            body='puck',
            velocity=velocity,
            gravity_scale=0.0,
            alive_for=lifespan+1.0,
            collide_with='floor'
        ).autoretain()
        

        t_peak = lifespan * 0.1
        t_start_descend = lifespan * 0.18
        t_stop = lifespan*0.2219921929138

        bs.animate_array(self.partical.node, 'velocity', 3, {
            0: velocity,               
            t_peak: (velocity[0]*0.5, 0.2, velocity[2]*0.5),               
            t_start_descend: (velocity[0]*0.2, -1.4, velocity[2]*0.2),     
            t_stop: (0, -0.2, 0)                
        })

        



        
        bs.timer(lifespan, self._break)


    def _break(self):
        from bascenev1lib.actor.spaz import Spaz
        # uhh the partical fell out of bounds lol
        if not self.partical.exists():
            return
        self.spazdata['pos'] = self.partical.node.position
        self.partical.handlemessage(bs.DieMessage(True))
        # Spawn in an identical lookin' spaz freeze and break immedieatley eykr
        ParticalFactory.get().snowgrave_crystal_break_sfx.play()
        spaz=Spaz(
            color=self.spazdata['clr'],
            highlight=self.spazdata['high'],
            character=self.spazdata['char'],
            can_accept_powerups=False,
        ).autoretain()
        
        # tp
        spaz.handlemessage(bs.StandMessage(self.spazdata['pos']))
        # rip out his vocal cords (only ones we'll reasonably hear)
        spaz.impact_sounds=[]
        spaz.death_sounds=[]
        spaz.fall_sounds=[]
        # kill him
        spaz.handlemessage(bs.DieMessage())
        # freeze, and add attributes so the original snowgrave thing doesnt kill this guy again lol
        spaz.frozen = True
        spaz.snowgraved = True
        spaz.node.frozen = True

        # throw him
        spaz.impulse(y=185, x=25)

        # anddd shatter!
        spaz.node.shattered = 1

        # Finally get some more particals and were done
        bs.emitfx(
            position=self.spazdata['pos'],
            count=9,
            spread=0.23,
            velocity=(
                0, 
                5, 
                0
            ),
            chunk_type='ice',
            scale=3.2,
        )




        


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
        self.tick_timer = bs.Timer(0.01, self.handle_nodes_inside, repeat=True)

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
                    # Ice em
                    delegate.handlemessage(bs.FreezeMessage())
                    if delegate.frozen and delegate.is_alive():
                        # Okay, you're gonna die
                        delegate.snowgraved = True
                        DamageText(
                            position=self.position,
                            text=str(random.randint(988, 1199)),
                            color=(1,1,1)
                        ).autoretain()
                        ParticalFactory.get().ominous_sound.play()
                        # Delete their node but save their data
                        SnowgraveCrystal(
                            delegate.last_saved_position,
                            delegate.character,
                            delegate.color,
                            delegate.highlight,
                            delegate.name,
                        )
                        # soo what ever activity knows they died,
                        #  and we were the last to hit em
                        delegate.handlemessage(bs.HitMessage(
                            flat_damage=1,
                            source_player=self.source_player
                        ))
                        # we need regular for some reason
                        delegate.handlemessage(bs.DieMessage())
                        delegate.node.delete()
                        
                   

            elif isinstance(delegate, bs.Actor):
                # any other actor gets swept away... hopefully
                delegate.impulse(y=6)


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
