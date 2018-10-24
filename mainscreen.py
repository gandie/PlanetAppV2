'''
Screen shown when the game is played. Contains gamezone and control widgets.
Divides touch events between control widgets and gamezone and hands them down
accordingly.
'''

# KIVY
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

# CUSTOM
import mainscreen_ui


class MainScreen(Screen):
    '''
    see kv file for background path
    '''

    # GUI
    menupanel = ObjectProperty(None)
    gamezone = ObjectProperty(None)
    add_menupanel = ObjectProperty(None)

    # label for tutorial texts
    tutorial_label = ObjectProperty(None)

    # showing infos about selected planets
    infobox = ObjectProperty(None)

    # buttons for selected planet
    modpanel = ObjectProperty(None)

    # ticks ahead and time sliders
    slider_panel = ObjectProperty(None)

    # add touchable widgets to interface for touch-handling
    interface = ReferenceListProperty(
        menupanel, gamezone, tutorial_label, infobox,
        modpanel, add_menupanel, slider_panel
    )

    # LOGIC
    logic = ObjectProperty(None)

    def __init__(self, logic, iconsize, iconratio_x, iconratio_y, **kwargs):

        super(MainScreen, self).__init__(**kwargs)

        self.logic = logic
        # TODO: check this method, its not neccessary, just set the attribute
        self.logic.register_mainscreen(self)

        self.iconsize = iconsize
        self.iconratio_x = iconratio_x
        self.iconratio_y = iconratio_y

        self.build_interface()

        # get background rect from canvas
        self.background = self.canvas.get_group('background')[0]

    def on_enter(self):
        self.allign_gamezone()

        # TODO: maybe avoid this "hacky" way to apply background setting?
        # check for background
        if self.logic.settings['background']:
            self.background.size = self.size
        else:
            self.background.size = (0, 0)

        # TODO: why is paused saved in menupanel? put to logic?
        if not self.menupanel.paused:
            self.logic.start_game()

        # check tutorial setting
        '''
        if self.logic.settings['show_tutorial']:
            if self.tutorial_label not in self.children:
                self.add_widget(self.tutorial_label)
        else:
            if self.tutorial_label in self.children:
                self.remove_widget(self.tutorial_label)
        '''

    def add_modpanel(self):
        '''called from logic when planet is selected'''
        if self.modpanel not in self.children:
            self.add_widget(self.modpanel)

    def remove_modpanel(self):
        '''called from logic when planet is UNselected'''
        if self.modpanel in self.children:
            self.remove_widget(self.modpanel)

    def add_infobox(self):
        '''called from logic when planet is selected -- DEACTIVATED'''
        if self.infobox not in self.children:
            self.add_widget(self.infobox)

    def remove_infobox(self):
        '''called from logic when planet is UNselected -- DEACTIVATED'''
        if self.infobox in self.children:
            self.remove_widget(self.infobox)

    def on_leave(self):
        self.logic.stop_game()
        '''
        if self.logic.tutorial_mode:
            self.remove_widget(self.tutorial_label)
            self.logic.tutorial_mode = False
        '''

    def allign_gamezone(self):
        # TODO: maybe check for pinned / heaviest body (if found) and align to
        # it instead of center
        # center gamezone widget so simulation starts in the middle
        self.gamezone.center_x = self.center_x
        self.gamezone.center_y = self.center_y

    def on_touch_down(self, touch):
        # hand down touch events, hand to gamezone if nothing else matches
        for widget in self.interface:
            # dont check invisible widgets
            if widget not in self.children:
                continue
            # gamezone is last
            if widget == self.gamezone:
                continue

            # we check dynamic layouts for children here, these layouts can not
            # be trusted to handle touch events correctly. This misbehaviour is
            # caused by widgets having children outside their own border due to
            # show / hide toggle mechanics
            for child in widget.children:
                if child.collide_point(touch.x, touch.y):
                    child.on_touch_down(touch)
                    return

        self.gamezone.on_touch_down(touch)

    def on_touch_move(self, touch):
        # hand down touch events, hand to gamezone if nothing else matches
        for widget in self.interface:
            if widget not in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x, touch.y):
                widget.on_touch_move(touch)
                return
        self.gamezone.on_touch_move(touch)

    def on_touch_up(self, touch):
        # hand down touch events, hand to gamezone if nothing else matches
        for widget in self.interface:
            if widget not in self.children:
                continue
            if widget == self.gamezone:
                continue
            if widget.collide_point(touch.x, touch.y):
                widget.on_touch_up(touch)
                return
        self.gamezone.on_touch_up(touch)

    def build_interface(self):

        '''
        self.tutorial_label = Tutorial_Label(
            self.iconsize,
            self.iconratio_x,
            size_hint=(None, None),
            size=(8 * self.iconsize, self.iconsize),
            pos_hint={'x': 1 - 8 * self.iconratio_x - 0.2, 'y': 0.875}
        )

        self.infobox = Infobox(
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.8, 'y': 0.8}
        )
        '''

        self.modpanel = mainscreen_ui.ModPanel(
            self.iconsize,
            self.iconratio_x,
            size_hint=(None, None),
            size=(7 * self.iconsize, self.iconsize),
            pos_hint={'x': 1 - 7 * self.iconratio_x, 'y': 0}
        )

        self.gamezone = mainscreen_ui.Gamezone(
            # zooming stuff can be deactivated:
            # do_rotation=False,
            # do_translation_y=False,
            # do_translation_x=False,
            auto_bring_to_front=False,
            scale_min=0.15,
            scale_max=10,
            size_hint=(25, 25)
        )
        self.add_widget(self.gamezone)

        self.menupanel = mainscreen_ui.MenuPanel(
            self.iconsize,
            self.iconratio_y,
            size_hint=(None, None),
            size=(self.iconsize, 3.0 * (Window.height / 8)),
            pos_hint={'x': 0, 'y': 0}
        )

        # self.tutorial_label.register_menupanel(self.menupanel)
        self.add_widget(self.menupanel)

        self.add_menupanel = mainscreen_ui.AddMenuPanel(
            self.iconsize,
            self.iconratio_y,
            size_hint=(None, None),
            size=(self.iconsize * 4, self.iconsize),
            pos_hint={'x': 0, 'y': 7 * self.iconratio_y}
        )

        self.add_widget(self.add_menupanel)

        self.slider_panel = mainscreen_ui.SliderPanel(
            self.iconsize,
            self.iconratio_y,
            size_hint=(None, None),
            size=(self.iconsize * 5, self.iconsize),
            pos_hint={'x': 1-self.iconratio_x * 5, 'y': 0.5}
        )

        self.add_widget(self.slider_panel)
