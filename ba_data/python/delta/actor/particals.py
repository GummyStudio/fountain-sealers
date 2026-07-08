
import bascenev1 as bs
import random


class Partical(bs.Actor):

    def __init__(self,
                position: tuple[float, float, float], 
                texture: str, 
                mesh: str,
                body_scale: str,
                mesh_scale: str,
                velocity: tuple[float, float, float] = (0, 0, 0), 
                random_vel: bool = False,
                random_range: float = 1.5,
                body: str = 'landMine',
                alive_for: float = 3.0,
                gravity_scale: int = 1.0,
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
                'color_texture': bs.gettexture(texture),
                'mesh': bs.getmesh(mesh),
                'mesh_scale': mesh_scale,
                'body': body,
                'body_scale': body_scale,
                'shadow_size': 0.44,
                'gravity_scale': gravity_scale,
                'materials': [SharedObjects.get().only_collide_with_floor_mat]
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