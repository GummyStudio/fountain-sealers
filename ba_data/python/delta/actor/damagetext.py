import bascenev1 as bs

class DamageText(bs.Actor):
    def __init__(self, position: tuple, text: str, color: tuple = (1, 1, 1)):
        super().__init__()
        self.node = bs.newnode(
            'text',
            attrs={
                'text': text,
                'position': position,
                'color': color,
                'h_align': 'center',
                'v_align': 'center',
                'scale': 1.5,
                'shadow': 1.0,
                'flatness': 1.0,
            }
        )
        
       
        bs.animate(self.node, 'scale', {0: 0.5, 0.1: 2.0, 0.2: 1.5})
        
        # Fade out
        bs.animate(self.node, 'opacity', {0.4: 1.0, 0.6: 0.0})
        
        # kill ourself
        self._die_timer = bs.Timer(
            0.7, bs.WeakCall(self.handlemessage, bs.DieMessage())
        )

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            super().handlemessage(msg)