import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import dropdown
import sql

class Home(BoxLayout):
    def __init__(self, screenmanager, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation='vertical'
        self.screenmanager = screenmanager
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        viewBalances = Button(text='View Balances', on_press=lambda *args: self.screen('balances', *args))
        self.add_widget(viewBalances)

    def screen(self, screenName, *args):
        self.screenmanager.current = screenName