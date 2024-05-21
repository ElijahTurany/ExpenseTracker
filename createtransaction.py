from random import random
from datetime import datetime
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
from kivymd.app import MDApp
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.pickers import MDDatePicker
import sql
import dropdown
		
class CreateTransaction(GridLayout):
    def __init__(self, **kwargs):

        super(CreateTransaction, self).__init__(**kwargs)
        self.cols = 2
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        self.exit = Button(text='Exit')
        self.add_widget(self.exit)

        self.add_widget(Label(text='Create a Transaction'))

        incomeExpenseLayout = GridLayout(cols=2)
        self.income = CheckBox(group = 'incomeExpense', allow_no_selection=False, active = True)
        self.expense = CheckBox(group = 'incomeExpense', allow_no_selection=False)
        incomeExpenseLayout.add_widget(Label(text='Income'))
        incomeExpenseLayout.add_widget(self.income)
        incomeExpenseLayout.add_widget(Label(text='Expense'))
        incomeExpenseLayout.add_widget(self.expense)

        self.add_widget(incomeExpenseLayout)
        self.add_widget(Label())

        self.add_widget(Label(text='Amount'))
        self.amount = TextInput(multiline=False, input_filter="int")
        self.add_widget(self.amount)

        self.add_widget(Label(text='Description'))
        self.description = TextInput(multiline=False)
        self.add_widget(self.description)

        self.add_widget(Label(text='Account'))
        self.accountDropdown = dropdown.DynamicDropdown(self.connection, "accounts", ['N/A'], -1)
        self.add_widget(self.accountDropdown)

        self.add_widget(Label(text='Category'))
        self.categoryDropdown = dropdown.DynamicDropdown(self.connection, "categories", ['N/A'], -1)
        self.add_widget(self.categoryDropdown)

        self.add_widget(Label(text='Note'))
        self.note = TextInput(multiline=False)
        self.add_widget(self.note)

        self.add_widget(Label(text='Date'))
        dateLayout = GridLayout(cols=2)
        self.date = TextInput(multiline=False)
        self.calendar = Button(text='Date Picker')
        dateLayout.add_widget(self.date)
        dateLayout.add_widget(self.calendar)
        self.add_widget(dateLayout)

        self.add_widget(Label(text='Time'))
        timeLayout = GridLayout(cols=2)
        self.time = TextInput(multiline=False)
        self.clock = Button(text='Clock')
        timeLayout.add_widget(self.time)
        timeLayout.add_widget(self.clock)
        self.add_widget(timeLayout)

        self.add_widget(Label())
        createLayout = AnchorLayout(anchor_x='left')
        self.create = Button(text='Create', on_press=self.createTransaction)
        createLayout.add_widget(self.create)
        self.add_widget(createLayout)
    
    def createTransaction(self, instance):
        transactionId = random() * 100000    
        amount = int(self.amount.text)
        if(self.expense.active):
            amount *= -1
        description = self.description.text
        accountId = self.accountDropdown.value
        categoryId = self.categoryDropdown.value
        datetime = self.date.text + self.time.text
        note = self.note.text
        sql.addTransaction(self.connection, transactionId, amount, description, accountId, categoryId, datetime, note)