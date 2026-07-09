import bascenev1 as bs
import _bascenev1
import babase
import bauiv1 as bui
from typing import Sequence
import re

class SurveyUI(bui.MainWindow):
    def __init__(self):
        super().__init__(
            root_widget=bui.containerwidget(
                size=(800, 600), background=False,toolbar_visibility=  'no_menu_minimal'
                
                ),
                origin_widget=None, transition=None
                )
        bs.apptimer(2, self.start)
    
    def start(self):
       
   
        self.dialouge(
            lines=[
                "HELLO.{pause:2}", 
                "ARE YOU\n{pause:0.5}THERE?{pause:2}", 
                "ARE WE{pause:0.5}\nCONNECTED?{pause:2}", 
                "...{pause:0.5}EXCELLENT.{pause:2.0}",
                "TRULY\n{pause:0.5}EXCELLENT.{pause:2.0}",
                "NOW.{pause:2.0}",
                "WE MAY\n{pause:0.5}BEGIN.{pause:1.0}",
            ],
            position=(400, 300),
            on_complete=self.cool_bg
        )
        
    
    def cool_bg(self):
        with bs.get_foreground_host_activity().context:
            bs.get_foreground_host_activity().cool_bg()

        
        self.dialouge(
            lines=[
                "{pause:1}FIRST.{pause:2}",
                "YOU MUST SHAPE\n{pause:0.5}THIS VESSEL.{pause:2}", 
                "ITS MIND.{pause:2.5}",               
            ],
            position=(400, 500),
            on_complete=lambda: (self.add_options(
                    question="WHAT IS ITS FAVORITE FOOD?",
                    config='food',
                    options=[
                        {'text': 'SWEET', 'choice': 'sweet'},
                        {'text': 'SOFT', 'choice': 'soft'},
                        {'text': 'SOUR', 'choice': 'sour'},
                        {'text': 'SALTY', 'choice': 'salty'},
                        {'text': 'PAIN', 'choice': 'pain'},
                        {'text': 'COLD', 'choice': 'cold'},
                    ],
                    on_complete=lambda: (
                        self.add_options(
                            question="YOUR FAVORITE BLOOD TYPE?",
                            config='blood_type',
                            options=[
                                {'text': 'A', 'choice': 'A'},
                                {'text': 'AB', 'choice': 'AB'},
                                {'text': 'B', 'choice': 'B'},
                                {'text': 'C', 'choice': 'C'},
                                {'text': 'D', 'choice': 'D'},
                            ],
                            on_complete=lambda: (
                                self.add_options(
                                    question="WHAT COLOR DOES IT LIKE MOST?",
                                    config='color',
                                    options=[
                                        {'text': 'RED', 'choice': 'red'},
                                        {'text': 'BLUE', 'choice': 'blue'},
                                        {'text': 'GREEN', 'choice': 'green'},
                                        {'text': 'CYAN', 'choice': 'cyan'},
                                    ],
                                    on_complete=lambda: (
                                        self.add_options(
                                            question="PLEASE GIVE IT A GIFT.",
                                            config='gift',
                                            options=[
                                                {'text': 'KINDNESS', 'choice': 'kindness'},
                                                {'text': 'MIND', 'choice': 'mind'},
                                                {'text': 'AMBITION', 'choice': 'ambition'},
                                                {'text': 'BRAVERY', 'choice': 'bravery'},
                                                {'text': 'VOICE', 'choice': 'voice'},
                                            ],
                                            on_complete=lambda: (
                                                self.add_options(
                                                    "HOW DO YOU FEEL ABOUT YOUR CREATION?\n(IT WILL NOT HEAR.)",
                                                    config='feelings',
                                                    options=[
                                                        {'text': 'LOVE', 'choice': 'love'},
                                                        {'text': 'HOPE', 'choice': 'hope'},
                                                        {'text': 'DISGUST', 'choice': 'disgust'},
                                                        {'text': 'FEAR', 'choice': 'fear'},
                                                    ],
                                                    on_complete=lambda: (
                                                        self.add_options(
                                                            question="HAVE YOU ANSWERED HONESTLY?",
                                                            config='honesty',
                                                            options=[
                                                                {'text': 'YES', 'choice': 'yes'},
                                                                {'text': 'NO', 'choice': 'no'},
                                                            ],
                                                            on_complete=lambda: (
                                                                self.add_options(
                                                                    question="YOU ACKNOWLEDGE THE POSSIBILITY\nOF PAIN AND SEIZURE.",
                                                                    config='acknowledge',
                                                                    options=[
                                                                        {'text': 'YES', 'choice': 'yes'},
                                                                        {'text': 'NO', 'choice': 'no'},
                                                                    ],
                                                                on_complete=self.vessel_done
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )      
                )
            )
        )
    

        

        return
    

    def vessel_done(self):
        self.dialouge(
            lines=[
                "UNDERSTOOD.{pause:3}", 

            ],
            position=(400, 500),
            on_complete=lambda: (
                self.add_text_input(
                    "NAME YOUR VESSEL.",
                    config='vessel_name',
                    on_complete=lambda: (

                        self.dialouge(
                            [(
                                "WE CALLED IT\n{pause:0.5}"
                                f"\"{babase.app.classic.startup.gameconfig['SurveyChoices']['vessel_name']}.\""
                                 "{pause:2.0}"
                                 ),
                                "EXCELLENT.{pause:0.5}\n{pause:0.5}TRULY, TRULY EXCELLENT.{pause:2}",
                                "YOUR NAME IS UNNECESSARY,\n{pause:0.3}AS I WAS ALREADY TOLD.{pause:2}",
                                "NOW.{pause:0.5}",
                                "THANK YOU\n{pause:0.5}FOR YOUR TIME.{pause:2}",
                                "YOUR ANSWERS.\n{pause:0.5}YOUR WONDERFUL CREATION.{pause:2}",
                                "WILL NOW BE PUT\n{pause:0.5}TO GOOD USE.{pause:2}",
                                "ENJOY YOURSELF\n{pause:1.0}AND FAREWELL.{pause:2.0}",
                            ],
                        on_complete=self.end
                        )
                    )
                )
            )
        )
        
    def end(self):
        with bs.get_foreground_host_activity().context:
            bs.get_foreground_host_activity().die()
       
        
    def add_options(self, question: str, options: list[dict], config: str, on_complete):
        container = bui.containerwidget(
            parent=self._root_widget,
            size=(500, 300),
            position=(150, 150),
            background=False
        )
        
        bui.textwidget(
            parent=container,
            position=(250, 400),
            size=(0, 0),
            text=question,
            h_align='center'
        )
        
        for i, opt in enumerate(options):
            bui.buttonwidget(
                parent=container,
                size=(300, 50),
                position=(-100, 180 - (i * 60)),
                label=opt['text'],
                on_activate_call=lambda c=opt['choice']: self._handle_choice(c, config, container, on_complete),
                texture=bui.gettexture('empty'),
            )
        
    def add_text_input(self, question: str, config: str,on_complete):
        container = bui.containerwidget(
            parent=self._root_widget,
            size=(500, 200),
            position=(150, 200),
            background=False
        )
        
        bui.textwidget(
            parent=container,
            position=(250, 150),
            size=(0, 0),
            text=question,
            h_align='center'
        )
        
        txt_input = bui.textwidget(
            parent=container,
            position=(100, 50),
            size=(300, 50),
            text="",
            editable=True,
            h_align='left',
            v_align='center',
            max_chars=10
        )
        
        bui.buttonwidget(
            parent=container,
            size=(100, 20),
            position=(200, 20),
            label="OK",
            on_activate_call=lambda: self._handle_choice(bui.textwidget(query=txt_input).strip().upper(), config, container, on_complete),
            texture=bui.gettexture('empty')
        )

    def _handle_choice(self, choice, config, container, on_complete):
        bui.app.classic.startup.gameconfig.setdefault('SurveyChoices', {})
        bui.app.classic.startup.gameconfig['SurveyChoices'][config] = choice
        bui.app.config.apply_and_commit()
        
        container.delete()
        
        if on_complete:
            on_complete()
        



    def dialouge(self, lines: list[str], position: tuple = (400, 500), on_complete=None):
        txt = bui.textwidget(parent=self._root_widget, position=position, 
                             size=(0, 0), text="", h_align='center')
        
        current_delay = 0.0
        
        for line in lines:
            bs.apptimer(current_delay, lambda: bui.textwidget(edit=txt, text=""))
            
            full_text = ""
            parts = re.split(r'({pause:\d+\.?\d*})', line)
            
            for part in parts:
                if part.startswith('{pause:'):
                    current_delay += float(part[7:-1])
                else:
                    for char in part:
                        full_text += char
                        bs.apptimer(current_delay, lambda s=full_text: bui.textwidget(edit=txt, text=s))
                        current_delay += 0.1
        
       
        bs.apptimer(current_delay, lambda: bui.textwidget(edit=txt, text=""))
        if on_complete:
            bs.apptimer(current_delay, on_complete)
class SurveySession(bs.Session):
    def __init__(self):
        depsets: Sequence[bs.DependencySet] = [] 
        super().__init__(depsets)
        self.setactivity(bs.newactivity(SurveyActivity))
    
    def die(self):
        babase.app.classic.startup.gameconfig['firstLaunch'] = False
        babase.app.config.apply_and_commit()
        _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())
    

    def on_player_request(self, player: bs.SessionPlayer) -> bool:
        # Reject all player requests.
        return False

class SurveyActivity(bs.Activity[bs.Player, bs.Team]):
    def __init__(self, settings):
        super().__init__(settings)
        self.music = {
            'anotherhim': bs.getsound('music/anotherhim'),
            'audiodrone': bs.getsound('music/AUDIO_DRONE'),
        }
    def die(self):
        self.session.die()
    def cool_bg(self):
        self.mnode.delete()
        self.mnode =bs.newnode('sound', attrs={'sound': self.music['anotherhim'], 'music': True})
        
    def on_begin(self):
        super().on_begin()
        
        bs.newnode('image', attrs={'texture': bs.gettexture('black'), 'fill_screen': True})
        self.mnode =bs.newnode('sound', attrs={'sound': self.music['audiodrone'], 'music': True})
        with bs.ContextRef.empty():
            babase.app.ui_v1.set_main_window(
                SurveyUI(), from_window=None, is_top_level=True, suppress_warning=True)


   