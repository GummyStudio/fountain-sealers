# Released under the MIT License. See LICENSE for details.
#
"""Implements the main menu window."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
import logging

import bauiv1 as bui
import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any, Callable


class MainMenuWindow(bui.MainWindow):
    """The main menu window."""

    def __init__(
        self,
        transition: str | None = 'in_left',
        origin_widget: bui.Widget | None = None,
    ):

        # Preload some modules we use in a background thread so we won't
        # have a visual hitch when the user taps them.
        bui.app.threadpool.submit_no_wait(self._preload_modules)

        bui.set_analytics_screen('Main Menu')
        self._show_remote_app_info_on_first_launch()

        uiscale = bui.app.ui_v1.uiscale

        # Make a vanilla container; we'll modify it to our needs in
        # refresh.
        super().__init__(
            root_widget=bui.containerwidget(
                toolbar_visibility=('menu_minimal'),
            ),
            transition=transition,
            origin_widget=origin_widget,
            # We're affected by screen size only at small ui-scale.
            refresh_on_screen_size_changes=uiscale is bui.UIScale.SMALL,
        )

        # Grab this stuff in case it changes.
        # self._is_demo = bui.app.env.demo
        # self._is_arcade = bui.app.env.arcade

        self._tdelay = 0.0
        self._t_delay_inc = 0.02
        self._t_delay_play = 1.7
        self._use_autoselect = True
        self._button_width = 200.0
        self._button_height = 45.0
        self._width = 100.0
        self._height = 100.0
        self._demo_menu_button: bui.Widget | None = None
        self._gather_button: bui.Widget | None = None
        self._play_button: bui.Widget | None = None
        self._watch_button: bui.Widget | None = None
        self._how_to_play_button: bui.Widget | None = None
        self._credits_button: bui.Widget | None = None

        self._refresh()

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

    @staticmethod
    def _preload_modules() -> None:
        """Preload modules we use; avoids hitches (called in bg thread)."""
        # pylint: disable=cyclic-import
        import bauiv1lib.getremote as _unused
        import bauiv1lib.confirm as _unused2
        import bauiv1lib.account.settings as _unused5
        import bauiv1lib.store.browser as _unused6
        import bauiv1lib.credits as _unused7
        import bauiv1lib.help as _unused8
        import bauiv1lib.settings.allsettings as _unused9
        import bauiv1lib.gather as _unused10
        import bauiv1lib.watch as _unused11
        import bauiv1lib.play as _unused12

    def _show_remote_app_info_on_first_launch(self) -> None:
        app = bui.app
        assert app.classic is not None

        # The first time the non-in-game menu pops up, we might wanna
        # show a 'get-remote-app' dialog in front of it.
        if app.classic.first_main_menu:
            app.classic.first_main_menu = False
            try:
                force_test = False
                bs.get_local_active_input_devices_count()
                if (
                    (app.env.tv or app.classic.platform == 'mac')
                    and bui.app.config.get('launchCount', 0) <= 1
                ) or force_test:

                    def _check_show_bs_remote_window() -> None:
                        try:
                            from bauiv1lib.getremote import GetBSRemoteWindow

                            bui.getsound('swish').play()
                            GetBSRemoteWindow()
                        except Exception:
                            logging.exception(
                                'Error showing get-remote window.'
                            )

                    bui.apptimer(2.5, _check_show_bs_remote_window)
            except Exception:
                logging.exception('Error showing get-remote-app info.')

    def get_play_button(self) -> bui.Widget | None:
        """Return the play button."""
        return self._play_button

    def _refresh(self) -> None:
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals

        classic = bui.app.classic
        assert classic is not None

        # Clear everything that was there.
        children = self._root_widget.get_children()
        for child in children:
            child.delete()

        self._tdelay = 0.0
        self._t_delay_inc = 0.0
        self._t_delay_play = 0.0
        self._button_width = 200.0
        self._button_height = 45.0

        self._r = 'mainMenu'

        app = bui.app
        assert app.classic is not None
        uiscale = app.ui_v1.uiscale
        thistdelay = 0.3

        self._have_quit_button = app.classic.platform in (
            'windows',
            'mac',
            'linux',
        )

        if not classic.did_menu_intro:
            self._tdelay = 1.6
            self._t_delay_inc = 0.03
            classic.did_menu_intro = True

        self._width = 420
        self._height = 800.0

        if uiscale is bui.UIScale.SMALL:
            # We're a generally widescreen shaped window, so bump our
            # overall scale up a bit when screen width is wider than safe
            # bounds to take advantage of the extra space.
            screensize = bui.get_virtual_screen_size()
            safesize = bui.get_virtual_safe_area_size()
            root_widget_scale = min(1.55, 1.3 * screensize[0] / safesize[0])
            button_y_offs = -20.0
            self._button_height *= 1.3
        elif uiscale is bui.UIScale.MEDIUM:
            root_widget_scale = 1.3
            button_y_offs = -55.0
            self._button_height *= 1.25
        else:
            root_widget_scale = 1.0
            button_y_offs = -90.0
            self._button_height *= 1.2

        bui.containerwidget(
            edit=self._root_widget,
            size=(self._width, self._height),
            background=False,
            scale=root_widget_scale,
            stack_offset=(400, 0),
        )
        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._quit,
        )

        self._demo_menu_button = None
        self._file_buttons = []
        # this ui fucking sucks code wise
        # but concept wise its fucking fine???
        # can someone just please remake this
        h = self._width * 0.5
        v = 570
        bui.textwidget(
            parent=self._root_widget,
            position=(h, self._height - 90),
            size=(0, 0),
            text=bui.Lstr(resource=f'{self._r}.selectText'),
            scale=0.8,
            color=(1, 1, 1, 0.7),
            h_align='center',
            v_align='center',
            transition_delay=thistdelay,
        )
        bui.textwidget(
            parent=self._root_widget,
            position=(h, self._height - 90 - 20),
            size=(0, 0),
            text='NOTE: should change button info text later to contain stats',
            scale=0.5,
            color=(1, 1, 1, 0.3),
            h_align='center',
            v_align='center',
            transition_delay=thistdelay,
        )
        v -= 20
        file_button_size = (300, 100)
        fb_width, fb_height = file_button_size
        file_button_scale = 1.3
        icon_size = fb_width * file_button_scale * 0.22
        file_buttons = [
            {
                'icon': 'startButton',
                'name': bui.Lstr(resource='localPlayText'),
                'info_text': bui.Lstr(resource=f'{self._r}.playInfoText'),
                'callback': self._play_press,
            },
            {
                'icon': 'usersButton',
                'name': bui.Lstr(resource='onlinePlayText'),
                'info_text': bui.Lstr(resource=f'{self._r}.gatherInfoText'),
                'callback': self._gather_press,
            },
            {
                'icon': 'tv',
                'name': bui.Lstr(resource='replaysText'),
                'info_text': bui.Lstr(resource=f'{self._r}.replayInfoText'),
                'callback': self._watch_press,
            },
        ]
        start_button = None
        for dict in file_buttons:
            callback = dict.get('callback')
            if not callback:
                raise RuntimeError('Main menu \'file\' button was made without callback')
            this_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(h - fb_width * 0.5 * file_button_scale, v),
                size=file_button_size,
                autoselect=self._use_autoselect,
                scale=file_button_scale,
                label='',
                on_activate_call=callback,
                transition_delay=thistdelay,
            )
            self._file_buttons.append(this_btn)
            if self._file_buttons.index(this_btn) == 0:
                start_button = this_btn
            bui.textwidget(
                parent=self._root_widget,
                position=(
                    h + (-fb_width + 70) + icon_size + 10, 
                    v + (fb_height * file_button_scale) - 47
                ),
                size=(0, 0),
                draw_controller=this_btn,
                maxwidth=fb_width * file_button_scale * 0.8,
                scale=0.87,
                text=dict.get('name'),
                h_align='left',
                v_align='center',
                transition_delay=thistdelay,
            )
            bui.textwidget(
                parent=self._root_widget,
                position=(
                    h + (-fb_width + 70) + icon_size + 10, 
                    v + (fb_height * file_button_scale) - 47 - 14,
                ),
                size=(0, 0),
                draw_controller=this_btn,
                maxwidth=fb_width * file_button_scale * 0.8,
                scale=0.75,
                text=dict.get('info_text'),
                h_align='left',
                v_align='top',
                color=(1, 1, 1, 0.7),
                transition_delay=thistdelay,
            )
            bui.imagewidget(
                parent=self._root_widget,
                size=(icon_size, icon_size),
                draw_controller=this_btn,
                transition_delay=thistdelay,
                position=(h + (-fb_width + 70), v + (fb_height * 0.5 - 28)),
                texture=bui.gettexture(dict.get('icon')),
            )
            v -= fb_height * file_button_scale - 7
        # ????? :sob:
        # someone PLEASE fix this math for me later
        v += fb_height * file_button_scale + 2 - 62
        bui.containerwidget(
            edit=self._root_widget,
            selected_child=start_button,
        )

        # Regular buttons.
        reg_button_size = (130, 60)
        reg_button_scale = 0.9
        hoffs = -70 * 2
        spacing = reg_button_size[0] + 8
        bui.buttonwidget(
            parent=self._root_widget,
            id='howtoplay',
            position=(h + hoffs, v),
            autoselect=self._use_autoselect,
            size=reg_button_size,
            scale=reg_button_scale,
            label=bui.Lstr(resource=f'{self._r}.howToPlayText'),
            on_activate_call=self._howtoplay,
            transition_delay=thistdelay,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(h + hoffs + spacing, v),
            size=reg_button_size,
            scale=reg_button_scale,
            autoselect=self._use_autoselect,
            label=bui.Lstr(resource=f'{self._r}.creditsText'),
            on_activate_call=self._credits,
            transition_delay=thistdelay,
        )
        hoffs = -70 * 2
        v -= reg_button_size[1] + 2
        bui.buttonwidget(
            parent=self._root_widget,
            position=(h + hoffs, v),
            size=reg_button_size,
            scale=reg_button_scale,
            autoselect=self._use_autoselect,
            label=bui.Lstr(resource=f'{self._r}.storeText'),
            on_activate_call=bui.app.mode._root_ui_store_press, # just use the legacy method
            transition_delay=thistdelay,
        )
        bui.buttonwidget(
            parent=self._root_widget,
            position=(h + hoffs + spacing, v),
            size=reg_button_size,
            scale=reg_button_scale,
            autoselect=self._use_autoselect,
            label=bui.Lstr(resource=f'{self._r}.settingsText'),
            on_activate_call=self._settings,
            transition_delay=thistdelay,
        )

        self._quit_button: bui.Widget | None = None
        
    def _quit(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.confirm import QuitWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        # Note: Normally we should go through bui.quit(confirm=True) but
        # invoking the window directly lets us scale it up from the
        # button.
        QuitWindow(origin_widget=self._quit_button)

    def _credits(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.credits import CreditsWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            CreditsWindow(origin_widget=self._credits_button),
        )
    
    def _settings(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.settings.allsettings import AllSettingsWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            AllSettingsWindow(origin_widget=self._credits_button),
        )

    def _howtoplay(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.help import HelpWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            HelpWindow(origin_widget=self._how_to_play_button),
        )

    def _gather_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.gather import GatherWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            GatherWindow(origin_widget=self._gather_button)
        )

    def _watch_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.watch import WatchWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            WatchWindow(origin_widget=self._watch_button),
        )

    def _play_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.play import PlayWindow

        # no-op if we're not currently in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(PlayWindow(origin_widget=self._play_button))
