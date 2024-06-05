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
import numpy as np
import dropdown
import sql

class ViewBalances(BoxLayout):
    def __init__(self, **kwargs):
        super(ViewBalances, self).__init__(**kwargs)
        self.orientation='vertical'
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        self.balances = sql.viewBalances(self.connection)
        total = 0

        for i in range(len(self.balances)):
            balanceLayout = GridLayout(cols=2)
            accountId = self.balances[i][0]
            balanceLayout.add_widget(Button(text=str(self.balances[i][1]), on_press=lambda *args: self.viewAccount(*args)))
            balanceLayout.add_widget(Label(text=str(self.balances[i][2])))
            total += self.balances[i][2]
            self.add_widget(balanceLayout)

        balanceLayout = GridLayout(cols=2)
        balanceLayout.add_widget(Label(text="Total"))
        balanceLayout.add_widget(Label(text=str(total)))
        self.add_widget(balanceLayout)

        #self.add_widget(balancesLayout)\

    def viewAccount(self, instance):
        pass
        #self.add_widget(Label(text=str(np.argwhere(self.balances == instance.text)[0])))
        #self.add_widget(Label(text=np.argwhere(self.balances == instance.text)[0][0]))