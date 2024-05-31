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

class ViewBalances(BoxLayout):
    def __init__(self, **kwargs):
        super(ViewBalances, self).__init__(**kwargs)
        self.orientation='vertical'
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        balancesLayout = GridLayout(cols=2)

        balances = sql.viewBalances(self.connection)
        total = 0

        for balance in balances:
            balancesLayout.add_widget(Label(text=str(balance[0])))
            balancesLayout.add_widget(Label(text=str(balance[1])))
            total += balance[1]

        balancesLayout.add_widget(Label(text="Total"))
        balancesLayout.add_widget(Label(text=str(total)))

        self.add_widget(balancesLayout)