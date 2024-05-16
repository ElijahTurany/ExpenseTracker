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

class DropdownButton(Button):
    def __init__(self, **kwargs):
        super(DropdownButton, self).__init__(**kwargs)
        self.dropList = DropDown()

        types = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6']

        for i in types:
            btn = Button(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.dropList.select(btn.text))
           
            self.dropList.add_widget(btn)

        self.bind(on_release=self.dropList.open)
        self.dropList.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.text = 'Select'

class StaticDropdown(Button):
    #Callback function called when text is selected
    def callback(self, text):
        #Updates dropdown text to text selected
        self.dropList.select(text)
        #Sets dropdown value to index of text selected
        setattr(self, 'value', self.values.index(text))

    def __init__(self, values, initVal, **kwargs):
        super(StaticDropdown, self).__init__(**kwargs)
        self.dropList = DropDown()

        #Creates button for each value passed in
        self.values = values
        for i in self.values:
            btn = Button(text=i, size_hint_y=None, height=50)
            #Binds button to callback function and adds button to dropdown
            btn.bind(on_release=lambda btn: self.callback(btn.text))
            self.dropList.add_widget(btn)

        #Binds button to open dropdown when clicked
        self.bind(on_release=self.dropList.open)
        self.dropList.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        #Sets the initial value if positive value is passed in
        if (initVal >= 0):
            self.callback(values[initVal])    