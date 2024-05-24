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
import sql

#createDatabase("expensetracker")
connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
#deleteTables(connection)
buildTables(connection)
clearTables(connection)
#populateTables(connection)
#printTables(connection)
        
class KivyApp(App):
    def build(self):
        return vt.ViewTransaction()
KivyApp().run()  