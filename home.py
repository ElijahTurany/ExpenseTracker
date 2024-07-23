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

        #View transaction button
        viewTransaction = Button(text='View Transactions', on_press=lambda *args: self.screen('viewTransaction', 'left', *args))
        self.add_widget(viewTransaction)

        #View balances button
        viewBalances = Button(text='View Balances', on_press=lambda *args: self.screen('balances', 'left', *args))
        self.add_widget(viewBalances)

        #Create transaction button
        createTransaction = Button(text='Create Transaction', on_press=lambda *args: self.screen('createTransaction', 'left', *args))
        self.add_widget(createTransaction)

        #Create account button
        createAccount = Button(text='Create Account', on_press=lambda *args: self.screen('createAccount', 'left', *args))
        self.add_widget(createAccount)

        #Create transfer button
        createTransfer = Button(text='Create Transfer', on_press=lambda *args: self.screen('createTransfer', 'left', *args))
        self.add_widget(createTransfer)

        #Create category button
        createCategory = Button(text='Create Category', on_press=lambda *args: self.screen('createCategory', 'left', *args))
        self.add_widget(createCategory)

        

    #Switches to screenName in a given direction
    def screen(self, screenName, direction, *args):
        self.screenmanager.transition.direction = direction
        self.screenmanager.current = screenName