import bascenev1 as bs
from delta.actor.particals import ParticalFactory
from bascenev1lib.actor.popuptext import PopupText
import random
from delta.actor.rudebuster import RudeBusterHitMessage

class PacifySpell(bs.Actor):

    def __init__(self,
                position: tuple[float, float, float], 
                velocity: float,
                source_player = None

        ):
        super().__init__()
        from bascenev1lib.gameutils import SharedObjects
        self.source_player = source_player
        ParticalFactory.get().pacify_sound.play()
        self.loc = bs.Node(None)
       
        velocity = list(velocity)
        if velocity[0] == 0 and velocity[2]==0:
            velocity[0] = 1
        speed = 0.06
        self.velocity = (
                    max(-1, min(velocity[0]*999, 1))*speed, 
                    0, 
                    max(-1, min(velocity[2]*999, 1))*speed
                )
        self.hitbox_size = (1,1.5,1)
        self.node = bs.newnode('region',delegate=self,
                    attrs={'scale': self.hitbox_size,
                           'position': position,
                           'type': 'box',
                           'materials': [SharedObjects.get().rude_buster_material]})
        debug = False
        if debug:
            self.loc=bs.newnode('locator',
                        attrs={'shape': 'box',
                               'color': (1,0,0),
                               'opacity': 0.02,
                               'draw_beauty': True,
                               'size': self.hitbox_size,
                               'additive': False})
            self.node.connectattr('position', self.loc, 'position')
            
                           
        
        # Automatically die after,, i dunno 5 seconds
        self.tick_timer = bs.Timer(0.01, self.tick, repeat=True)
        self.z_timer = bs.Timer(0.15, self.create_z, repeat=True)
        bs.timer(5, bs.Call(self.handlemessage, bs.DieMessage(True)))
    def create_z(self):
        for _ in range(random.randint(3, 5)):
            rand_x = random.uniform(-0.5, 0.5)
            rand_y = random.uniform(-0.5, 0.5)
            rand_z = random.uniform(-0.5, 0.5)
            pos = (
                    (self.node.position[0] + (self.hitbox_size[0] * rand_x))+(self.velocity[0]*2.5),
                    (self.node.position[1] + (self.hitbox_size[1] * rand_y)-0.5)+(self.velocity[1]*2.5),
                    (self.node.position[2] + (self.hitbox_size[2] * rand_z))+(self.velocity[2]*2.5),
                )
            text = bs.newnode(
                'text',
                attrs={
                    'text': 'Z',
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'h_align': 'center',
                    'position': pos,
                    'scale':  0.011
                },
            )
            bs.animate(text, 'opacity', {
                0: 1,
                0.35: 0
            })
            bs.timer(1.5, text.delete)
                
    def tick(self):
        if not self.exists():
            return
        
      
            
        self.node.position = (
            self.node.position[0]+self.velocity[0],
            self.node.position[1]+self.velocity[1],
            self.node.position[2]+self.velocity[2],
        )

    def exists(self):
        return bool(self.node)
    
    def handlemessage(self, msg):
        if isinstance(msg, RudeBusterHitMessage):
            if not self.node:
                return None
            
            node = bs.getcollision().opposingnode

            if not node:
                return
            # goooo to sleep
            node.handlemessage("knockout", 500)
            # damage
            node.handlemessage(
                bs.HitMessage(
                    flat_damage=25,
                    source_player=self.source_player,
                    hit_type=bs.DeathType.SPARED
                ),
            )
            self.handlemessage(bs.DieMessage())
          

        elif isinstance(msg, bs.DieMessage):
            self.tick_timer = None
            self.z_timer = None
            self.node.delete()
            self.loc.delete()

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage(True))
            
        return super().handlemessage(msg)