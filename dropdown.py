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

class StaticDropdown(Button):
    #Callback function called when text is selected
    def callback(self, text):
        #Updates dropdown text to text selected
        self.dropList.select(text)
        #Sets dropdown value to index of text selected
        self.value = self.values.index(text)

        #self.dropList.select(str(self.value))

    def __init__(self, values, initVal, **kwargs):
        super(StaticDropdown, self).__init__(**kwargs)
        self.dropList = DropDown()

        #Creates button for each value passed in
        self.values = values
        for i in self.values:
            #Creates a button with text of each value
            btn = Button(text=i, size_hint_y=None, height=50)
            #Binds button to callback function and adds button to dropdown
            btn.bind(on_release=lambda btn: self.callback(btn.text))
            self.dropList.add_widget(btn)

        #Binds button to open dropdown when clicked
        self.bind(on_release=self.dropList.open)
        self.dropList.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        #Sets the initial value if passed in
        if (initVal != None):
            self.callback(values[initVal])

class DynamicDropdown(Button):
    #Callback function called when text is selected
    def callback(self, btn):
        #Updates dropdown text to text of selected button
        self.dropList.select(btn.text)
        #Sets dropdown value to id of selected button
        self.value = btn.id

    def __init__(self, connection, table, otherVals, initVal, offset, **kwargs):
        super(DynamicDropdown, self).__init__(**kwargs)
        self.dropList = DropDown()

        #Gets values from given table name
        if (table == "categories"):
            self.values = sql.viewCategories(connection)
        elif (table == "accounts"):
            self.values = sql.viewAccounts(connection)

        buttons = []
        #Adds buttons for otherVals passed in first
        if otherVals != None:
            #J is used as the id for otherVals, and starts at -1
            j = -1
            for i in otherVals:
                #Creates a button with text of each value
                btn = Button(text=i, size_hint_y=None, height=50)
                #id is assigned to j, j decrements
                btn.id = j
                j -= 1
                #Binds button to callback function and adds button to dropdown and buttons array
                btn.bind(on_release=lambda btn: self.callback(btn))
                self.dropList.add_widget(btn)
                buttons.append(btn)

        skippedValues = 0

        for i in self.values:
            if skippedValues < offset:
                skippedValues += 1
                break
            #Creates a button with text and id of each value
            btn = Button(text=i[1], size_hint_y=None, height=50)
            btn.id = i[0]
            #Binds button to callback function and adds button to dropdown and buttons array
            btn.bind(on_release=lambda btn: self.callback(btn))
            self.dropList.add_widget(btn)
            buttons.append(btn)

        #Binds button to open dropdown when clicked
        self.bind(on_release=self.dropList.open)
        self.dropList.bind(on_select=lambda instance, x: setattr(self, 'text', x))

        #Sets the initial value if passed in
        if (initVal != None):
            #Adding length of otherVals aligns negative values passed in with buttons array
            self.callback(buttons[initVal + len(otherVals)])