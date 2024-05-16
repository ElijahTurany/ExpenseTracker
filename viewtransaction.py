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
import dropdown as dropdown

class ViewTransaction(GridLayout):
    def __init__(self, **kwargs):
        super(ViewTransaction, self).__init__(**kwargs)
        self.cols = 3

        #Account
        accountLayout = BoxLayout(orientation='vertical')
        accountLayout.add_widget(Label(text='Account'))
        accountLayout.add_widget(dropdown.DropdownButton())

        #Category
        categoryLayout = BoxLayout(orientation='vertical')
        categoryLayout.add_widget(Label(text='Category'))
        categoryLayout.add_widget(dropdown.DropdownButton())

        #Sort
        sortLayout = BoxLayout(orientation='vertical')
        sortLayout.add_widget(Label(text='Sort By'))
        sortLayout.add_widget(dropdown.StaticDropdown(['Account', 'Amount', 'Category', 'Description', 'Note', 'Timeframe'], 5))
        

        #Order
        orderLayout = BoxLayout(orientation='vertical')
        orderLayout.add_widget(Label(text='Order'))
        orderLayout.add_widget(dropdown.StaticDropdown(['ASC', 'DESC'], 1))

        #Description
        descriptionLayout = BoxLayout(orientation='vertical')
        #Title
        descriptionTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        descriptionTitle.add_widget(Label(text='Description'))
        descriptionLayout.add_widget(descriptionTitle)
        #Input
        descriptionValue = BoxLayout(orientation='horizontal')
        descriptionValue.add_widget(dropdown.StaticDropdown(['N/A', 'Contains', 'Equals', 'Starts With', 'Ends With', 'Is Empty', 'Isn\'t Empty'], 0))
        description = TextInput(multiline=False)
        descriptionValue.add_widget(description)
        descriptionLayout.add_widget(descriptionValue)
        
        #Note
        noteLayout = BoxLayout(orientation='vertical')
        #Title
        noteTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        noteTitle.add_widget(Label(text='Note'))
        noteLayout.add_widget(noteTitle)
        #Input
        noteValue = BoxLayout(orientation='horizontal')
        noteValue.add_widget(dropdown.StaticDropdown(['N/A', 'Contains', 'Equals', 'Starts With', 'Ends With', 'Is Empty', 'Isn\'t Empty'], 0))
        note = TextInput(multiline=False)
        noteValue.add_widget(note)
        noteLayout.add_widget(noteValue)

        #Timeframe
        timeframeLayout = BoxLayout(orientation='vertical')
        #Title
        timeframeTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        timeframeTitle.add_widget(Label(text='Timeframe'))
        timeframeLayout.add_widget(timeframeTitle)
        #Input
        timeframeValue = BoxLayout(orientation='horizontal')
        timeframeValue.add_widget(dropdown.StaticDropdown(['N/A', 'Before', 'After', 'At', 'Between'], 0))
        timeframeStart = TextInput(multiline=False)
        timeframeEnd = TextInput(multiline=False)
        timeframeValue.add_widget(timeframeStart)
        timeframeValue.add_widget(Label(text='and'))
        timeframeValue.add_widget(timeframeEnd)
        timeframeLayout.add_widget(timeframeValue)

        #Amount
        amountLayout = BoxLayout(orientation='vertical')
        #Title
        amountTitle = AnchorLayout(anchor_x='left', anchor_y='center')
        amountTitle.add_widget(Label(text='Amount'))
        amountLayout.add_widget(amountTitle)
        #Input
        amountValue = BoxLayout(orientation='horizontal')
        amountValue.add_widget(dropdown.StaticDropdown(['N/A', 'Below', 'Above', 'Equal To', 'Between'], 0))
        amountLow = TextInput(multiline=False)
        amountHigh = TextInput(multiline=False)
        amountValue.add_widget(amountLow)
        amountValue.add_widget(Label(text='and'))
        amountValue.add_widget(amountHigh)
        amountLayout.add_widget(amountValue)

        self.add_widget(categoryLayout)
        self.add_widget(descriptionLayout)
        self.add_widget(timeframeLayout)
        self.add_widget(accountLayout)
        self.add_widget(noteLayout)
        self.add_widget(amountLayout)
        self.add_widget(sortLayout)
        self.add_widget(orderLayout)