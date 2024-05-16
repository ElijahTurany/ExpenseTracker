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
import sql

class CreateTransaction(GridLayout):
    def __init__(self, **kwargs):
        super(CreateTransaction, self).__init__(**kwargs)
        self.cols = 2

        self.exit = Button(text='Exit')
        self.add_widget(self.exit)

        self.add_widget(Label(text='Create a Transaction'))

        incomeExpenseLayout = GridLayout(cols=2)
        income = CheckBox(group = 'incomeExpense', active = True)
        expense = CheckBox(group = 'incomeExpense')
        incomeExpenseLayout.add_widget(Label(text='Income'))
        incomeExpenseLayout.add_widget(income)
        incomeExpenseLayout.add_widget(Label(text='Expense'))
        incomeExpenseLayout.add_widget(expense)

        self.add_widget(incomeExpenseLayout)
        self.add_widget(Label())

        self.add_widget(Label(text='Amount'))
        self.amount = TextInput(multiline=False)
        self.add_widget(self.amount)

        self.add_widget(Label(text='Description'))
        self.description = TextInput(multiline=False)
        self.add_widget(self.description)

        self.add_widget(Label(text='Account'))
        dropdown = DropDown()
        for i in range(3):
            button = Button(text=str(i), size_hint_y=None, height=44)
            button.bind(on_release=lambda button: dropdown.select(button.text))
            dropdown.add_widget(button)
        self.account = Button(text='Account')
        self.account.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.account, 'text', x))
        self.add_widget(self.account)

        self.add_widget(Label(text='Category'))
        self.category = TextInput(multiline=False)
        self.add_widget(self.category)

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
        amount = self.amount.text
        description = self.description.text
        accountId = self.account.text
        categoryId = self.category.text
        datetime = self.date.text + self.time.text
        note = self.note.text
        connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
        sql.addTransaction(connection, transactionId, amount, description, accountId, categoryId, datetime, note)