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
import createtransfer as ctf
import createcategory as cc
import home as h
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

        #Home screen
        homeScreen = Screen(name='home')
        homeScreen.add_widget(h.Home(sm))
        sm.add_widget(homeScreen)

        #View transaction screen
        viewTransactionScreen = Screen(name='viewTransaction')
        viewTransactionScreen.add_widget(vt.ViewTransaction(sm))
        sm.add_widget(viewTransactionScreen)

        #Balance screen
        balancesScreen = Screen(name='balances')
        balancesScreen.add_widget(vb.ViewBalances(sm))
        sm.add_widget(balancesScreen)

        #Create transaction screen
        createTransactionScreen = Screen(name='createTransaction')
        sm.createTransaction = ct.CreateTransaction(sm)
        createTransactionScreen.add_widget(sm.createTransaction)
        sm.add_widget(createTransactionScreen)

        #Create account screen
        createAccountScreen = Screen(name='createAccount')
        createAccountScreen.add_widget(ca.CreateAccount(sm))
        sm.add_widget(createAccountScreen)

        #Create transfer screen
        createTransferScreen = Screen(name='createTransfer')
        createTransferScreen.add_widget(ctf.CreateTransfer(sm))
        sm.add_widget(createTransferScreen)

        #Create category screen
        createCategoryScreen = Screen(name='createCategory')
        createCategoryScreen.add_widget(cc.CreateCategory(sm))
        sm.add_widget(createCategoryScreen)

        sm.current = 'home'
        return sm
KivyApp().run()   

# class KivyApp(App):
#     def build(self):
#         return vt.ViewTransaction()
# KivyApp().run()  