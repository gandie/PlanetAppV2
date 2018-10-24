# KIVY
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# CUSTOM
from realbutton import RealButton
from slot import SettingsSlot

'''
screen to alter settings. basically a scrollview containing settings slots.
also access kivy settings from here.
'''


class SettingsScreen(Screen):

    logic = ObjectProperty(None)
    mainlayout = ObjectProperty(None)
    menubutton = ObjectProperty(None)
    settingsbutton = ObjectProperty(None)
    settingsview = ObjectProperty(None)

    def __init__(self, logic, iconsize, iconratio_x, iconratio_y, **kwargs):

        super(SettingsScreen, self).__init__(**kwargs)

        self.logic = logic

        self.iconsize = iconsize
        self.iconratio_x = iconratio_x
        self.iconratio_y = iconratio_y

        self.setting_items = {}

        self.build_interface()

    def on_enter(self):
        '''
        get settings from logic
        '''
        # logic_settings = self.logic.settings
        # for key in logic_settings.keys():
        for key in self.logic.settings:
            if key in self.setting_items:
                self.setting_items[key].value = self.logic.settings[key]

    def on_leave(self):
        '''
        write setting to logic and save to file
        '''
        # logic_settings = self.logic.settings
        # for key in logic_settings.keys():
        for key in self.logic.settings:
            if key in self.setting_items:
                self.logic.settings[key] = self.setting_items[key].value
        self.logic.apply_settings()
        App.get_running_app().settings.save()

    def build_interface(self):

        self.mainlayout = FloatLayout()

        self.settingsview = ScrollView(
            size_hint=(0.7, 0.7),
            pos_hint={'x': 0.15, 'y': 0.15}
        )

        # use gridlayout to put items into scrollview
        self.settingslayout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=80
        )

        # magic binding
        self.settingslayout.bind(
            minimum_height=self.settingslayout.setter('height')
        )

        controller = self.logic.settings
        model = controller.model

        # sort items by seqnum
        itemlist = [
            item for item in sorted(model, key=lambda x: model[x].seqnum)
        ]

        for settings_item in itemlist:
            item = model[settings_item]
            if not item.show:
                continue
            settings_type = item.settings_type
            widget = None
            if settings_type == 'select':
                widget = SettingsSlot(
                    size_hint=(1, None),
                    setting_type='select',
                    label_text=item.label,
                    items=item.values
                )
            elif settings_type == 'bool':
                widget = SettingsSlot(
                    size_hint=(1, None),
                    setting_type='bool',
                    label_text=item.label
                )
            elif settings_type == 'number':
                widget = SettingsSlot(
                    size_hint=(1, None),
                    setting_type='number',
                    label_text=item.label,
                    setting_max=item.max_value,
                    setting_min=item.min_value,
                    setting_value=item.value
                )

            if not widget:
                continue

            self.setting_items[settings_item] = widget
            self.settingslayout.add_widget(widget)

        self.settingsbutton = Button(
            text='KivySettings',
            size_hint=(1, None),
            on_press=self.switchto_kivysettings
        )
        self.settingslayout.add_widget(self.settingsbutton)

        self.menubutton = RealButton(
            './media/icons/arrowleft.png',
            './media/icons/arrowleft.png',
            self.switchto_menu,
            size_hint=(None, None),
            size=(self.iconsize, self.iconsize),
            pos_hint={'x': 0, 'y': 0},
            source='./media/icons/arrowleft.png',
            always_release=True
        )

        # add settingslayout to scrollview
        self.settingsview.add_widget(self.settingslayout)
        self.mainlayout.add_widget(self.menubutton)
        self.mainlayout.add_widget(self.settingsview)
        self.add_widget(self.mainlayout)

    def switchto_menu(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

    def switchto_credits(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'credits'

    def switchto_kivysettings(self, instance):
        App.get_running_app().open_settings()
