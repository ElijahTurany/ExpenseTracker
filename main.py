import mysql.connector
from mysql.connector import Error
import pandas as pd
from random import random
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
from kivy.uix.screenmanager import ScreenManager, Screen
import createtransaction as ct
import viewtransaction as vt
import createaccount as ca
import viewbalances as vb
import viewaccount as va
import sql

def build():
    sql.createDatabase("expensetracker")
    connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
    sql.buildTables(connection)
    sql.populateTables(connection)

        
#build()

class KivyApp(App):
    def build(self):
        sm = ScreenManager()
        
        balancesScreen = Screen(name='balances')
        balancesScreen.add_widget(vb.ViewBalances(sm))
        accountScreen = Screen(name='account')
        accountScreen.add_widget(va.ViewAccount(sm, 1))
        sm.add_widget(balancesScreen)
        sm.add_widget(accountScreen)
        sm.current = 'balances'
        return sm
    
KivyApp().run()   
