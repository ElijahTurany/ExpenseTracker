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
import createtransaction as ct
import viewtransaction as vt
import createaccount as ca
import sql

sql.createDatabase("expensetracker")
connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
sql.buildTables(connection)
#sql.populateTables(connection)

# sql.deleteTables(connection)
# sql.clearTables(connection)

#sql.addUser(connection, "first", "last", "abc@email.com", 15551239876, "city", "state", 12345, "street", 0, "title")
#sql.addAccount(connection, "Wallet", 0)
        
class KivyApp(App):
    def build(self):
        return ca.CreateAccount()
KivyApp().run()   
