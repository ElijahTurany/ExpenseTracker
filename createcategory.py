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

class CreateCategory(BoxLayout):
    def __init__(self, screenmanager, **kwargs):
        super(CreateCategory, self).__init__(**kwargs)
        self.screenmanager = screenmanager
        self.orientation='vertical'
        self.connection = sql.create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

        

        titleLayout = GridLayout(cols=2)
        back = Button(text='Back', on_press=lambda *args: self.screen('home', 'right'))
        titleLayout.add_widget(back)

        titleLayout.add_widget(Label(text='Create a Category'))

        self.add_widget(titleLayout)

        #Title
        createCategoryLayout = GridLayout(cols=2)
        createCategoryLayout.add_widget(Label(text='Title'))
        self.title = TextInput(multiline=False)
        createCategoryLayout.add_widget(self.title)

       #Create Button
        createCategoryLayout.add_widget(Label(text=''))
        createButton = Button(text='Create Category', on_press=self.createCategory)
        createCategoryLayout.add_widget(createButton)

        self.add_widget(createCategoryLayout)

    def createCategory(self, instance):
        sql.addCategory(self.connection, self.title.text)

    def screen(self, screenName, direction, *args):
        self.screenmanager.transition.direction = direction
        self.screenmanager.current = screenName