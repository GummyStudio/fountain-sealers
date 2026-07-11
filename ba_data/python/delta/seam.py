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
        self.exists = True
        self.did_clean_up = False
        self.menu_container = None
        self.empty_texture = bui.gettexture('empty')
        self.active_timers = []

        

        self.seam_sprites = {
            'idle': [bui.gettexture('seam/seam_idle1'), bui.gettexture('seam/seam_idle2'), bui.gettexture('seam/seam_idle3'),  bui.gettexture('seam/seam_idle4')],
            'annoyed': [bui.gettexture('seam/seam_impatient1'), bui.gettexture('seam/seam_impatient2')],
            'laugh': [bui.gettexture('seam/seam_laugh1'), bui.gettexture('seam/seam_laugh2')],
            'suprised': [bui.gettexture('seam/seam_surprised1')],
            'talk': [bui.gettexture('seam/seam_talk1'), bui.gettexture('seam/seam_talk2'), bui.gettexture('seam/seam_talk3')]
        }
        self.animation_frame = 0
        self.animate_type = 'idle'
        self.animation_frames_past = 0
        bgscale=3.5
        self.buy_sfx = bui.getsound('snd_locker')
        
        bui.imagewidget(
            parent=self._root_widget,
            position=(-500, 268), 
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
        
        
        
    
    def _tick(self):
        if not self.exists:
            if not self.did_clean_up:
                self.did_clean_up = True
                bui.textwidget(edit=self.dark_dollars, text='')
            return
        if self.dialouge_mode == 'merged':
            bui.textwidget(edit=self.dark_dollars, text='')

        
        else:
            bui.textwidget(edit=self.dark_dollars, text=f'${babase.app.classic.startup.gameconfig.get('dark_dollars', 0)}')
            
        bs.apptimer(0.1, self._tick)
    
    def show_main_menu(self):
        self.split()
        
        intro = [
            ('* Hee hee... Welcome, travellers.', 'talk'),
            ( '* Don\'t like the prices? Then get out.', 'laugh'),
        ]
        say = random.choice(intro)
        self.say(
           say[0], expression=say[1]
        )
        
        if self.menu_container is not None:
            self.menu_container.delete()
            
            
            
        self.menu_container = bui.containerwidget(
            parent=self._root_widget,
            size=(200, 300),
            position=(450, 100),
            background=False
        )
        
        
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 110), 
                         label='BUY', on_activate_call=self.show_buy_menu, texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 40), 
                         label='TALK', on_activate_call=self.show_talk_menu, texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, -30), 
                         label='EXIT', on_activate_call=self.leave, texture=self.empty_texture)
    
    def confirm_purchase(self, item_name: str):
        item = babase.app.classic.startup.store[item_name]
        current_money = babase.app.classic.startup.gameconfig.get('dark_dollars', 0)
        
        
        if current_money >= item['cost']:
            babase.app.classic.startup.gameconfig[item['config']] = True
            babase.app.classic.startup.increase_statistic('dd', -item['cost'] )
            self.show_buy_menu()
            
            
            self.say(f"* A fine choice.\n    It's yours.", expression='talk')
            self.buy_sfx.play(0.85)
        else:
            self.show_buy_menu()
            self.say("* You don't have\n    enough money for\n    that.", expression='annoyed')
        
    
    def purchase_item(self, item_name: str):
        self.split()
        item = bs.app.classic.startup.store[item_name]
        
  
        desc_text = item['description'][0]
        expression = item['description'][1]
        self.say(f"{desc_text}", expression=expression)

        if self.menu_container is not None:
            self.menu_container.delete()
        
        self.menu_container = bui.containerwidget(
            parent=self._root_widget,
            size=(200, 200),
            position=(450, 100),
            background=False
        )
        
        bui.buttonwidget(
            parent=self.menu_container, size=(180, 50), position=(210, 110), 
            label='YES', on_activate_call=bs.Call(self.confirm_purchase, item_name), 
            texture=self.empty_texture
        )
        bui.buttonwidget(
            parent=self.menu_container, size=(180, 50), position=(210, 40), 
            label='NO', on_activate_call=self.show_buy_menu, 
            texture=self.empty_texture
        )
        bui.textwidget(
            parent=self.menu_container, size=(180, 50), position=(280, -20), 
            text=f'COST: ${item['cost']}', h_align='left',
        )

    def show_buy_menu(self):
        self.split_reverse()
        store = bs.app.classic.startup.store
        if self.menu_container is not None:
            self.menu_container.delete()
        
        self.say("* What do you want\n   to buy?", expression='talk')

        self.menu_container = bui.scrollwidget(
            parent=self._root_widget,
            size=(730, 270),
            position=(-180, 0),
            background=False
        )
        

        row_container = bui.containerwidget(
            parent=self.menu_container,
            size=(500, 75*len(store.items())), 
            background=False
        )

        y_pos = (75*len(store.items()))-50
        for item_name, data in store.items():
            if bs.app.classic.startup.gameconfig[data['config']]:
                bui.buttonwidget(
                    parent=row_container, 
                    size=(260, 50), 
                    position=(10, y_pos), 
                    label=f"{item_name} (OWNED)",
                    on_activate_call=lambda: self.say(
                        '* You already own\n     this.',
                        expression='annoyed'
                    ),
                    texture=self.empty_texture
                )
            else:
                bui.buttonwidget(
                    parent=row_container, 
                    size=(260, 50), 
                    position=(10, y_pos), 
                    label=f"{item_name} (${data['cost']})",
                    on_activate_call=bs.Call(self.purchase_item, item_name),
                    texture=self.empty_texture
                )
            y_pos -= 60
       
        bui.buttonwidget(
            parent=row_container, size=(180, 50), position=(10, y_pos), 
            label='BACK', on_activate_call=self.show_main_menu, texture=self.empty_texture
        )
    


    def show_talk_menu(self):
        self.say(
            '* Don\'t have anything better to do.', expression='talk'
        )
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
                         label='About\nyourself', on_activate_call=bs.Call(self.talk, 'about'), texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, 38), 
                         label='Earn\nMoney', on_activate_call=bs.Call(self.talk, 'howtoearn'), texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, -28), 
                         label='Anything', on_activate_call=bs.Call(self.talk, 'anything'), texture=self.empty_texture)
        bui.buttonwidget(parent=self.menu_container, size=(180, 50), position=(210, -60), 
                         label='BACK', on_activate_call=self.show_main_menu, texture=self.empty_texture)
        
    def talk(self, topic: str):
        self.merge()
        if self.menu_container is not None:
            self.menu_container.delete()
            
        if topic == 'about':
            self.say(
                "* The name's Seam. Pronounced \"Shawm.\"{pause:1.0}\n", 
                expression='talk',
                on_complete=lambda: (
                    self.say(
                        "* And this is my little Seap. Ha ha ha ha...{pause:1.0}\n",
                        expression='laugh',
                        on_complete=lambda: (
                            self.say(
                                "* Over the years, I've collected odds and ends.{pause:1.0}\n",
                                expression='talk',
                                on_complete=lambda: (
                                    self.say(
                                        "* 'Course, I've no attachment to any of it. It's just a hobby of mine.{pause:1.0}\n",
                                        expression='talk',
                                        on_complete=lambda: (
                                            self.say(
                                                "* Around here, you learn to find ways to pass the time... ... or go mad like everyone else.{pause:2.0}\n",
                                                expression='laugh',
                                                on_complete=self.show_talk_menu
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        elif topic == 'howtoearn':
            self.say(
                '* How to earn cash you say?{pause:1.0}\n* Well...{pause:1.0}\n', 
                expression='talk',
                 on_complete=lambda: (
                    self.say((
                        "* You can play with your friends with the realm of the unknown.{pause:1.0}\n"
                        "* Doing tricks, defeating them or generally just playing can get you\n  some dollars!{pause:1.0}\n"
                        
                        ),
                        expression='talk',
                        on_complete=lambda: (
                            self.say(
                                "* Or well, what do I know. Ha ha ha...{pause:2.0}\n",
                                expression='laugh',
                                on_complete=self.show_talk_menu
                            )
                        )
                    )
                 )
            )
        elif topic == 'anything':
            options = [
                "* Do you ever look at a pile of scrap and see a masterpiece?{pause:1.0}\n* No?{pause:1.0}\n* Well, that's quite alright. Not everyone is cursed with my particular brand of vision.",
                "* You seem to be searching for something, traveler.{pause:1.0}\n* Just remember: the most valuable items aren't always the ones with a price tag attached.",
                "* Honestly, most days are exactly the same as the last.{pause:1.0}\n* But every now and then, someone interesting walks through that door.{pause:1.0}\n* ...I suppose you're one of them."
            ]
            
            self.say(
                random.choice(options) + "{pause:1.0}\n", 
                expression='talk',
                on_complete=self.show_talk_menu
            )
    def die(self):
        self.exists = False
        babase.app.classic.return_to_main_menu_session_gracefully()
    def leave(self):
        
        if self.menu_container is not None:
            self.menu_container.delete()
        self.merge()
        rando = random.randint(0, 1)
        if rando == 0:
            self.say(
                '* Take your time... Ain\'t like it\'s better spent.{pause:1.5}', 
                expression='talk',
                on_complete=self.die
            )
        elif rando == 1:
            

            self.say((
                '* See you again...\n{pause:0.5}'
                '* Or not.{pause:0.5}'
                ), 
                expression='talk',
                on_complete=lambda: self.say(
                    '* Ha ha ha ha...{pause:1.5}', 
                    expression='laugh',
                    on_complete=self.die
                )
            )
        else:
            self.die()

        
       
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
        if not self.exists:
            return
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

        for timer in self.active_timers:
            self.active_timers.clear()
        self.active_timers = []
       
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
                    
                    self.active_timers.append(bs.AppTimer(current_delay, lambda s=full_text:self.advance(s)))
                    current_delay += 0.02
        
        self.active_timers.append(bs.AppTimer(current_delay, lambda: self.animate_seam('idle')))
        if on_complete:
            self.active_timers.append(bui.AppTimer(current_delay+0.01, on_complete))
    
    
    def next_frame(self):
        try:
            if self.animate_type in self.seam_sprites:
                self.animation_frames_past += 1
                if self.animate_type == 'idle':
                    
                    if (not self.animation_frames_past % 10 == 0) and (self.animation_frame == 0):
                        bs.apptimer(0.2, self.next_frame)
                        return
                        
                    

                    
                frames = self.seam_sprites[self.animate_type]
                self.animation_frame = (self.animation_frame + 1) % len(frames)
                bui.imagewidget(edit=self.seam, texture=frames[self.animation_frame])
                bs.apptimer(0.2, self.next_frame)
            else:
                print('dawg.')
        except:
            pass
            
     
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


       
   