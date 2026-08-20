import bascenev1 as bs

class DamageText(bs.Actor):
    def __init__(self, position: tuple, text: str, color: tuple = (1, 1, 1), scl=1.0):
        super().__init__()
        self.node = bs.newnode(
            'text',
            attrs={
                'text': text,
                'position': position,
                'color': color,
                'h_align': 'center',
                'v_align': 'center',
                'shadow': 1.0,
                'flatness': 1.0,
                'in_world': True,
                'scale': 0.02*scl
            }
        )
        
       
 
        start_y = position[1]
        bs.animate_array(self.node, 'position', 3, {
            0: (position[0], start_y, position[2]),
            0.11: (position[0], start_y + 0.51, position[2]),
            0.351: (position[0]+0.6, start_y + 0.5, position[2]) ,
            0.451: (position[0]+0.6, start_y, position[2]) ,
            0.6: (position[0]+0.6, start_y+0.1, position[2]),
            0.7: (position[0]+0.6, start_y, position[2]),
            0.8: (position[0]+0.6, start_y+0.1, position[2]),
            0.9: (position[0]+0.6, start_y, position[2]),
            1.5: (position[0]+0.6, start_y, position[2]),
            2.0: (position[0]+0.6, start_y+2.0, position[2]),
        })
        
        bs.animate(self.node, 'opacity', {1.5: 1.0, 2.0: 0.0})
        
        # kill ourself
        self._die_timer = bs.Timer(
            2.0, bs.WeakCall(self.handlemessage, bs.DieMessage())
        )

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            super().handlemessage(msg)