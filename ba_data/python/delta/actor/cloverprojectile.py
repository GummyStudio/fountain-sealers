import bascenev1 as bs
from delta.actor.particals import Partical, ParticalFactory
import random
from delta.actor.rudebuster import RudeBusterHitMessage
""" I JUST REALIED ITS SPADES NOT CLOVER MY LAZY ASSS """

class clover(bs.Actor):
    """i got lazy ok"""

    def __init__(self,
                position: tuple[float, float, float], 
                velocity: float,
                source_player = None

        ):
        super().__init__()
        from bascenev1lib.gameutils import SharedObjects
        self.source_player = source_player
       
        velocity = tuple(velocity)
        speed = 10
        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': (
                    max(-1, min(velocity[0]*999, 1))*speed, 
                    0, 
                    max(-1, min(velocity[2]*999, 1))*speed
                ),
                'gravity_scale': 0.0,
                'color_texture': bs.gettexture('white'),
                'mesh': bs.getmesh('box'),
                'mesh_scale': 0.8,
                'body': 'landMine',
                'body_scale': 1.2,
                'shadow_size': 0.44,
                'materials': [SharedObjects.get().rude_buster_material]
            }
        )

        # Automatically die after,, i dunno 10 seconds
        bs.timer(10, bs.Call(self.handlemessage, bs.DieMessage(True)))

    def exists(self):
        return bool(self.node)
    
    def handlemessage(self, msg):
        if isinstance(msg, RudeBusterHitMessage):
            if not self.node:
                return None
            
            node = bs.getcollision().opposingnode

            if not node:
                return

            punch_momentum_angular = (
                1.0
            )
            punch_power = 0.35
            ppos = self.node.position
            punchdir = self.node.velocity
            vel = self.node.velocity
            # knockback
            node.handlemessage(
                bs.HitMessage(
                    pos=ppos,
                    velocity=vel,
                    magnitude=punch_power * punch_momentum_angular * 110.0,
                    velocity_magnitude=punch_power * 40,
                    radius=0,
                    srcnode=self.node,
                    source_player=self.source_player,
                    force_direction=punchdir,
                    hit_type=bs.DeathType.SPADES
                ),
            )
            # damage
            node.handlemessage(
                bs.HitMessage(
                    flat_damage=250,
                    source_player=self.source_player,
                    hit_type=bs.DeathType.SPADES
                ),
            )
            self.handlemessage(bs.DieMessage())
          

        elif isinstance(msg, bs.DieMessage):
            if not self.exists():
                return
            if msg.immediate:
                self.node.delete()
            else:
                self.node.velocity = (0, 0, 0)
                
                bs.animate(
                    self.node,
                    'mesh_scale',
                    {
                        0.0: self.node.mesh_scale,
                        0.1: self.node.mesh_scale*1.2,
                        0.11: self.node.mesh_scale*0.25,
                        0.12: 0
                    }
                )
                bs.timer(0.12, self.node.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage(True))
            
        return super().handlemessage(msg)