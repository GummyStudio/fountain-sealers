import bascenev1 as bs
import _bascenev1
import babase
import bauiv1 as bui
from typing import Sequence
import random
import re


class ShopUI(bui.MainWindow):
    def __init__(self):
        super().__init__(
            root_widget=bui.containerwidget(
                size=(800, 600), background=False,toolbar_visibility=  'no_menu_minimal'
                
                ),
                origin_widget=None, transition=None
                )
        self.menu_container = None
        self.empty_texture = bui.gettexture('empty')

        

        self.seam_sprites = {
            'idle': [bui.gettexture('seam/seam_idle1'), bui.gettexture('seam/seam_idle2'), bui.gettexture('seam/seam_idle3'),  bui.gettexture('seam/seam_idle4')],
            'annoyed': [bui.gettexture('seam/seam_impatient1'), bui.gettexture('seam/seam_impatient2')],
            'laugh': [bui.gettexture('seam/seam_laugh1'), bui.gettexture('seam/seam_laugh2')],
            'suprised': [bui.gettexture('seam/seam_surprised1')],
            'talk': [bui.gettexture('seam/seam_talk1'), bui.gettexture('seam/seam_talk2'), bui.gettexture('seam/seam_talk3')]
        }
        self.animation_frame = 0
        self.animate_type = 0
        self.animation_frames_past = 0
        bgscale=3.5
        
        bui.imagewidget(
            parent=self._root_widget,
            position=(-500, 228), 
            size=(512 * bgscale, 128 * bgscale),
            texture=bui.gettexture('seam/seam_shop'),
        )
        seamscale=3
        self.seam = bui.imagewidget(
            parent=self._root_widget,
            position=(0, 255),
            size=(256 * seamscale, 128 * seamscale),
            texture=bui.gettexture('seam/seam_idle1'),
        )
        self.full_dialouge = bui.imagewidget(
            parent=self._root_widget,
            position=(-300, -570),
            size=(1400, 1400),
            texture=bui.gettexture('diabox'),
        )
        self.split_dialouge = bui.imagewidget(
            parent=self._root_widget,
            position=(-300, -570),
            size=(1400, 1400),
            texture=bui.gettexture('deltasplit'),
        )
        self.talk_sound = bui.getsound('talksounds/default')
        self.dialouge_mode = 'seperate' # seperate, merged or reversed, changing how dialouge is rendered
        self.animate_seam('laugh')
        self.next_frame()


        self.dark_dollars = bui.textwidget(
            parent=self._root_widget,
            position=(720, 0),
            h_align='left',

            text=f'${babase.app.classic.startup.gameconfig.get('dark_dollars', 0)}',
        )
        self._dialogue_txt = bui.textwidget(
                parent=self._root_widget,
                text="",
                v_align='top',
                size=(500, 250)
        )
    
        self.show_main_menu()
        self._tick()
        self.say(
            '* YO HIT THE SPLITS!', expression='suprised'
        )
        
        
    
    def _tick(self):
        if self.dialouge_mode == 'merged':
            bui.textwidget(edit=self.dark_dollars, text='')

        
        else:
            bui.textwidget(edit=self.dark_dollars, text=f'${babase.app.classic.startup.gameconfig.get('dark_dollars', 0)}')
            
        bs.apptimer(0.1, self._tick)
    
    def show_main_menu(self):
        self.split()
        if self.menu_container is not None:
            self.menu_container.delete()
            
            
            
        self.menu_container = bui.containerwidget(
            parent=self._root_widget,
            size=(200, 300),
            position=(450, 100),
            background=False
        )
        
        
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 110), 
                         label='BUY', on_activate_call=None, texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 40), 
                         label='TALK', on_activate_call=self.show_talk_menu, texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, -30), 
                         label='EXIT', on_activate_call=self.leave, texture=self.empty_texture)
    
    def show_talk_menu(self):
        self.split()
        if self.menu_container is not None:
            self.menu_container.delete()
            
            
            
        self.menu_container = bui.containerwidget(
            parent=self._root_widget,
            size=(200, 300),
            position=(450, 100),
            background=False
        )
        
        
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 110), 
                         label='About yourself', on_activate_call=bs.Call(self.talk, 'about'), texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 90), 
                         label='How to earn money', on_activate_call=bs.Call(self.talk, 'howtoearn'), texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 0), 
                         label='dik', on_activate_call=self.leave, texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, -30), 
                         label='BACK', on_activate_call=self.show_main_menu, texture=self.empty_texture)
    def talk(self, topic: str):
        self.merge()
        if self.menu_container is not None:
            self.menu_container.delete()
            
        if topic == 'about':
            self.say((
                "* The name's Seam. Pronounced \"Shawm.\"{pause:2.0}\n"
                "* And this is my little Seap. Ha ha ha ha...{pause:2.0}\n"
                "* Over the years, I've collected odds and ends.{pause:2.0}\n"
                "* 'Course, I've no attachment to any of it. It's just a hobby of mine.{pause:2.0}\n"
                "* Around here, you learn to find ways to pass the time... ... or go mad like everyone else.{pause:2.0}\n"
                ), 
                expression='talk'
            )
        if topic == 'howtoearn':
            self.say(
                '* I am Seam, the one and only.{pause:1.0} I am the shopkeeper of this fine establishment.{pause:1.0}', 
                expression='talk'
            )

    def leave(self):
        if self.menu_container is not None:
            self.menu_container.delete()
        self.merge()
        self.say(
            '* Goodbye stranger.{pause:1.0}', 
            expression='talk',
            on_complete=babase.app.classic.return_to_main_menu_session_gracefully
        )
        
       
    def split(self):
        self.dialouge_mode = 'seperate'
        bui.imagewidget(edit=self.full_dialouge, opacity=0.0)
        bui.imagewidget(edit=self.split_dialouge, opacity=1.0)
    def split_reverse(self):
        self.dialouge_mode = 'reversed'
        bui.imagewidget(edit=self.full_dialouge, opacity=0.0)
        bui.imagewidget(edit=self.split_dialouge, opacity=1.0)
    def merge(self):
        self.dialouge_mode = 'merged'
        bui.imagewidget(edit=self.full_dialouge, opacity=1.0)
        bui.imagewidget(edit=self.split_dialouge, opacity=0.0)

    def animate_seam(self, animation_type: str):
        if animation_type in self.seam_sprites:
            self.animate_type = animation_type
            self.animation_frame = 0
            self.animation_frames_past = 0
           
        else:
            print('dawg.')
    
    def advance(self, text: str):
        bui.textwidget(edit=self._dialogue_txt, text=text)
        self.talk_sound.play()

    def say(self, text: str, expression: str = 'talk', on_complete=None):
        if self.dialouge_mode == 'reversed':
            pos = (700, 0)
        else:
            pos = (-180, 0)
       
        bui.textwidget(
            edit=self._dialogue_txt,
            position=pos,
            text="" 
        )
        
        self.animate_seam(expression)
        
        full_text = ""
        current_delay = 0.0
        
        parts = re.split(r'({pause:\d+\.?\d*})', text)
        
        for part in parts:
            if part.startswith('{pause:'):
                current_delay += float(part[7:-1])
                
            else:
                for char in part:
                    full_text += char
                    
                    bs.apptimer(current_delay, lambda s=full_text:self.advance(s))
                    current_delay += 0.025
        
        bs.apptimer(current_delay, lambda: self.animate_seam('idle'))
        if on_complete:
            bui.apptimer(current_delay+0.01, on_complete)
    
    
    def next_frame(self):
        if self.animate_type in self.seam_sprites:
            self.animation_frames_past += 1
            if self.animate_type == 'idle':
                
                if (not self.animation_frames_past % 30 == 0) and (self.animation_frame == 0):
                    bs.apptimer(0.2, self.next_frame)
                    return
                    
                

                
            frames = self.seam_sprites[self.animate_type]
            self.animation_frame = (self.animation_frame + 1) % len(frames)
            bui.imagewidget(edit=self.seam, texture=frames[self.animation_frame])
            bs.apptimer(0.2, self.next_frame)
        else:
            print('dawg.')
        
     
class ShopSession(bs.Session):
    def __init__(self):
        depsets: Sequence[bs.DependencySet] = [] 
        super().__init__(depsets)
        self.setactivity(bs.newactivity(ShopActivity))
    
    def die(self):
        babase.app.classic.return_to_main_menu_session_gracefully()

    def on_player_request(self, player: bs.SessionPlayer) -> bool:
        # Reject all player requests.
        return False

class ShopActivity(bs.Activity[bs.Player, bs.Team]):
    def __init__(self, settings):
        super().__init__(settings)
       
        
    def on_begin(self):
        super().on_begin()
        
        bs.newnode('image', attrs={'texture': bs.gettexture('black'), 'fill_screen': True})
        self.mnode =bs.newnode('sound', attrs={'sound': bs.getsound('music/lantern'), 'music': True})
        with bui.ContextRef.empty():
            babase.app.ui_v1.set_main_window(
                ShopUI(), from_window=None, is_top_level=True, suppress_warning=True)


       
   