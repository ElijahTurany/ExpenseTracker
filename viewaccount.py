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

class ViewAccount(BoxLayout):
    def __init__(self, screenmanager, accountId, **kwargs):
        super(ViewAccount, self).__init__(**kwargs)
        self.accountId = accountId
        self.orientation='vertical'
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        self.transactionLayout = GridLayout(cols = 7)

        self.headerValues = ["transactionNum", "amount", "description", "account", "category", "timestamp", "note"]

        transactions = sql.advancedViewTransactions(self.connection, None, None, None, [self.accountId], None, None, None, None, None, None, True)

        for value in self.headerValues:
            self.transactionLayout.add_widget(Label(text=str(value)))

        for transaction in transactions:
            for value in transaction:
                self.transactionLayout.add_widget(Label(text=str(value)))

        self.add_widget(self.transactionLayout)