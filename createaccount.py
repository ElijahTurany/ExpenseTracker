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

class CreateAccount(BoxLayout):
    def __init__(self, **kwargs):
        super(CreateAccount, self).__init__(**kwargs)
        self.orientation='vertical'
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        createAccountLayout = GridLayout(cols=2)

        #Title
        createAccountLayout.add_widget(Label(text='Title'))
        self.title = TextInput(multiline=False)
        createAccountLayout.add_widget(self.title)

        #Starting Balance
        createAccountLayout.add_widget(Label(text='Starting Balance'))
        self.startingBalance = TextInput(multiline=False, input_filter="int")
        createAccountLayout.add_widget(self.startingBalance)

       #Create Button
        createAccountLayout.add_widget(Label(text=''))
        createButton = Button(text='Create Account', on_press=self.createAccount)
        createAccountLayout.add_widget(createButton)

        self.add_widget(createAccountLayout)

    def createAccount(self, instance):
        sql.addAccount(self.connection, self.title.text, self.startingBalance.text)