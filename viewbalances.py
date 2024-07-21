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
from kivy.uix.screenmanager import Screen, ScreenManager 
import numpy as np
import dropdown
import viewaccount as va
import sql

class ViewBalances(BoxLayout):
    def __init__(self, screenmanager, **kwargs):
        super(ViewBalances, self).__init__(**kwargs)
        #self.createAccountScreens() 
        self.screenmanager = screenmanager       
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
        self.orientation='vertical'

        back = Button(text='Back', on_press=lambda *args: self.screen('home', 'right'))
        self.add_widget(back)

        self.balances = sql.viewBalances(self.connection)
        total = 0

        balanceLayout = GridLayout(cols=2)
        for i in self.balances:
            #Creates a button with text and id of each value
            btn = Button(text=i[1])
            btn.id = i[0]
            #Binds button to viewAccount function and adds it to layout
            btn.bind(on_release=lambda btn: self.viewAccount(btn))
            balanceLayout.add_widget(btn)
            balanceLayout.add_widget(Label(text=str(i[2])))
            #Increments total
            total += i[2]

        balanceLayout.add_widget(Label(text="Total"))
        balanceLayout.add_widget(Label(text=str(total)))
        self.add_widget(balanceLayout)

    def viewAccount(self, button):
        name= 'account' + str(button.id)

        #Checks if an screen for the account has been created
        screenCreated = False
        for i in self.screenmanager.screens:
            if name == i.name:
                screenCreated = True

        #Creates a new screen of the account and adds it to the screen manager
        if not screenCreated:
            accountScreen = Screen(name=name)
            accountScreen.add_widget(va.ViewAccount(self.screenmanager, button.id))
            self.screenmanager.add_widget(accountScreen)
            
        #Changes to new screen
        self.screenmanager.transition.direction = 'left'
        self.screenmanager.current = name

    #Switches to screenName in a given direction
    def screen(self, screenName, direction, *args):
        self.screenmanager.transition.direction = direction
        self.screenmanager.current = screenName