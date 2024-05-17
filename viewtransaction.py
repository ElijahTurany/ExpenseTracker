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

class ViewTransaction(GridLayout):
    def __init__(self, **kwargs):
        super(ViewTransaction, self).__init__(**kwargs)
        self.cols = 3
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        #Account
        accountLayout = BoxLayout(orientation='vertical')
        accountLayout.add_widget(Label(text='Account'))
        self.accountDropdown = dropdown.DynamicDropdown(self.connection, "accounts", ['N/A'], -1)
        accountLayout.add_widget(self.accountDropdown)

        #Category
        categoryLayout = BoxLayout(orientation='vertical')
        categoryLayout.add_widget(Label(text='Category'))
        self.categoryDropdown = dropdown.DynamicDropdown(self.connection, "categories", ['N/A'], -1)
        categoryLayout.add_widget(self.categoryDropdown)

        #Sort
        sortLayout = BoxLayout(orientation='vertical')
        sortLayout.add_widget(Label(text='Sort By'))
        self.sortDropdown = dropdown.StaticDropdown(['Account', 'Amount', 'Category', 'Description', 'Note', 'Timeframe'], 5)
        sortLayout.add_widget(self.sortDropdown)

        #Order
        orderLayout = BoxLayout(orientation='vertical')
        orderLayout.add_widget(Label(text='Order'))
        self.orderDropdown = dropdown.StaticDropdown(['ASC', 'DESC'], 1)
        orderLayout.add_widget(self.orderDropdown)

        #Description
        descriptionLayout = BoxLayout(orientation='vertical')
        #Title
        descriptionTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        descriptionTitle.add_widget(Label(text='Description'))
        descriptionLayout.add_widget(descriptionTitle)
        #Input
        descriptionValue = BoxLayout(orientation='horizontal')
        self.descriptionDropdown = dropdown.StaticDropdown(['N/A', 'Contains', 'Equals', 'Starts With', 'Ends With'], 0) 
        descriptionValue.add_widget(self.descriptionDropdown)
        self.description = TextInput(multiline=False)
        descriptionValue.add_widget(self.description)
        descriptionLayout.add_widget(descriptionValue)
        
        #Note
        noteLayout = BoxLayout(orientation='vertical')
        #Title
        noteTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        noteTitle.add_widget(Label(text='Note'))
        noteLayout.add_widget(noteTitle)
        #Input
        noteValue = BoxLayout(orientation='horizontal')
        self.noteDropdown = dropdown.StaticDropdown(['N/A', 'Contains', 'Equals', 'Starts With', 'Ends With', 'Is Empty', 'Isn\'t Empty'], 0)
        noteValue.add_widget(self.noteDropdown)
        self.note = TextInput(multiline=False)
        noteValue.add_widget(self.note)
        noteLayout.add_widget(noteValue)

        #Timeframe
        timeframeLayout = BoxLayout(orientation='vertical')
        #Title
        timeframeTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        timeframeTitle.add_widget(Label(text='Timeframe'))
        timeframeLayout.add_widget(timeframeTitle)
        #Input
        timeframeValue = BoxLayout(orientation='horizontal')
        self.timeframeDropdown = dropdown.StaticDropdown(['N/A', 'Before', 'After', 'Between', 'At'], 0)
        timeframeValue.add_widget(self.timeframeDropdown)
        self.timeframeStart = TextInput(multiline=False)
        self.timeframeEnd = TextInput(multiline=False)
        timeframeValue.add_widget(self.timeframeStart)
        timeframeValue.add_widget(Label(text='and'))
        timeframeValue.add_widget(self.timeframeEnd)
        timeframeLayout.add_widget(timeframeValue)

        #Amount
        amountLayout = BoxLayout(orientation='vertical')
        #Title
        amountTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        amountTitle.add_widget(Label(text='Amount'))
        amountLayout.add_widget(amountTitle)
        #Input
        amountValue = BoxLayout(orientation='horizontal')
        self.amountDropdown = dropdown.StaticDropdown(['N/A', 'Below', 'Above', 'Between', 'Equal To'], 0)
        amountValue.add_widget(self.amountDropdown)
        self.amountLow = TextInput(multiline=False)
        self.amountHigh = TextInput(multiline=False)
        amountValue.add_widget(self.amountLow)
        amountValue.add_widget(Label(text='and'))
        amountValue.add_widget(self.amountHigh)
        amountLayout.add_widget(amountValue)

        searchButton = Button(text='Search', on_press=self.viewTransactions)
        #Results
        resultLayout = GridLayout(cols = 7)

        self.add_widget(categoryLayout)
        self.add_widget(descriptionLayout)
        self.add_widget(timeframeLayout)
        self.add_widget(accountLayout)
        self.add_widget(noteLayout)
        self.add_widget(amountLayout)
        self.add_widget(sortLayout)
        self.add_widget(orderLayout)
        self.add_widget(searchButton)

        self.add_widget(resultLayout)

    def viewTransactions(self, instance):
        match(self.amountDropdown.value):
            #N/A
            case 0:
                amountLow = None
                amountHigh = None
            #Below
            case 1:
                amountLow = None
                amountHigh = self.amountLow
            #Above
            case 2:
                amountLow = self.amountLow
                amountHigh = None
            #Between
            case 3:
                amountLow = self.amountLow
                amountHigh = self.amountHigh
            #Equal To
            case 4:
                amountLow = self.amountLow
                amountHigh = self.amountLow
        
        match(self.descriptionDropdown.value):
            #N/A
            case 0:
                description = None
            #Contains
            case 1:
                description = '%' + self.description + '%'
            #Equals
            case 2:
                description = self.description
            #Starts With
            case 3:
                description = self.description + '%'
            #End With
            case 4:
                description = '%' + self.description

        #Add multiselect functionality
        accountIds = {self.accountDropdown.value}
        categoryIds = {self.categoryDropdown.value}

        match(self.timeframeDropdown.value):
            #N/A
            case 0:
                timeframeStart = None
                timeframeEnd = None
            #Before
            case 1:
                timeframeStart = None
                timeframeEnd = self.timeframeStart
            #After
            case 2:
                timeframeStart = self.timeframeStart
                timeframeEnd = None
            #Between
            case 3:
                timeframeStart = self.timeframeStart
                timeframeEnd = self.timeframeEnd
            #At
            case 4:
                timeframeStart = self.timeframeStart
                timeframeEnd = self.timeframeStart

        match(self.sortDropdown.value):
            #Make alphabetical
            case 0:
                orderBy = "accountId"
            case 1:
                orderBy = "amount"
            #Make alphabetical
            case 2:
                orderBy = "categoryId"
            case 3:
                orderBy = "description"
            case 4:
                orderBy = "note"
            case 5:
                orderBy = "timestamp"   

        match(self.orderDropdown.value):
            case 0:
                ascDesc = "ASC"    
            case 1:
                ascDesc = "DESC" 

        match(self.noteDropdown.value):
            #N/A
            case 0:
                note = None
            #Contains
            case 1:
                note = '%' + self.note + '%'
            #Equals
            case 2:
                note = self.note
            #Starts With
            case 3:
                note = self.note + '%'
            #Ends With
            case 4:
                note = '%' + self.note
            #Is Empty
            case 5:
                note = ''
            #Isn't Empty
            case 6:         
                note = '%_%'

        transactions = sql.advancedViewTransactions(self.connection, amountLow, amountHigh, description, accountIds, categoryIds, timeframeStart, timeframeEnd, orderBy, ascDesc, note)
