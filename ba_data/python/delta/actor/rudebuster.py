import bascenev1 as bs
from delta.actor.particals import Partical, ParticalFactory
import random

class RudeBusterHitMessage:
    """ rude buster hit someone"""
class Rudebuster(bs.Actor):

    def __init__(self,
                position: tuple[float, float, float], 
                velocity: float,
                source_player = None

        ):
        super().__init__()
        from bascenev1lib.gameutils import SharedObjects
        self.source_player = source_player
        velocity = list(velocity)
        if velocity[0] == 0 and velocity[2]==0:
            velocity[0] = 1
        velocity = tuple(velocity)
        speed = 20
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
                'mesh_scale': 1.0,
                'body': 'landMine',
                'body_scale': 2.5,
                'shadow_size': 0.44,
                'materials': [SharedObjects.get().rude_buster_material]
            }
        )

        # Automatically die after,, i dunno 10 seconds
        bs.timer(10, bs.Call(self.handlemessage, bs.DieMessage(True)))
        bs.getsound('snd_rudebuster_swing').play()
        self.arg()
    
    def arg(self):
        if not self.exists():
            return
        self.node.velocity = (
            self.node.velocity[0],
            -5,
            self.node.velocity[2]
        )
        bs.timer(0.121, self.arg2)
    def arg2(self):
        if not self.exists():
            return
        self.node.velocity = (
            self.node.velocity[0],
            5,
            self.node.velocity[2]
        )
        bs.timer(0.121, self.arg3)
        
    def arg3(self):
        if not self.exists():
            return
        self.node.velocity = (
            self.node.velocity[0],
            0,
            self.node.velocity[2]
        )
 
    def exists(self):
        return bool(self.node)
    
    def handlemessage(self, msg):
        if isinstance(msg, RudeBusterHitMessage):
            if not self.node:
                return None
            
            bs.getsound('snd_rudebuster_hit').play()
            node = bs.getcollision().opposingnode

            if not node:
                return

            punch_momentum_angular = (
                1.0
            )
            punch_power = 0.45
            ppos = self.node.position
            punchdir = self.node.velocity
            vel = self.node.velocity

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
                    hit_type='blast',
                    hit_subtype='rudebuster'
                ),
            )
            self.handlemessage(bs.DieMessage())
            for _ in range(random.randint(3, 7)):
                    Partical(
                        position=self.node.position,
                        texture=ParticalFactory.get().rudebuster_tex, 
                        mesh=ParticalFactory.get().rudebuster_mesh,
                        body_scale=0.5,
                        mesh_scale=0.25,
                        random_vel = True,
                        random_range=8.5,
                        body='landMine',
                        gravity_scale=1.0,
                    ).autoretain()

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