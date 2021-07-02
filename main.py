from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.config import Config
from kivy.uix.button import Button
from parsing import f_departments, budget_institutions




Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 500)

import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


class CreateAccountWindow(Screen):
    polis = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.polis.text != "" and self.password != "":
            db.add_user(self.polis.text, self.password.text)
            self.reset()
            sm.current = "login"
        else:
            invalidForm()

    def loginRes(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.password.text = ""
        self.polis.text = ""



class LoginWindow(Screen):
    login = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.login.text, self.password.text):
            MainWindow.current = self.login.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):

        self.reset()
        sm.current = "CREATE"

    def reset(self):
        self.login.text = ""
        self.password.text = ""


class MainWindow(Screen):
    login = ObjectProperty(None)
    created = ObjectProperty(None)
    grid = ObjectProperty(None)
    parsto = ObjectProperty(None)
    current = ""
    names = f_departments().keys()

    def on_pressed(self, index):
        number = index.id
        sm.current = "TOPARS"
        return number

    def logOut(self):
        sm.current = "LOGIN"

    def on_enter(self):
        name, created = db.get_user(self.current)
        self.login.text = "Имя учетной записи: " + name
        self.created.text = "Создано: " + created


class ToWindow(Screen):
    number = MainWindow.on_pressed
    grid = ObjectProperty(None)
    current = ""
    parsto = ObjectProperty(None)
    names = budget_institutions(2).keys()

    def logOut(self):
        sm.current = "TOPARS"

    def on_pressed(self, index):
        number = index.id
        sm.current = "login"
        return number



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Ошибка',
                content=Label(text='Неверное имя \nпользователя или пароль.', halign='center'),
                size_hint=(None, None), size=(300, 200))
    pop.open()


def invalidForm():
    pop = Popup(title='Ошибка',
                content=Label(text='Пожалуйста, заполните \nвсе входные данные \nдействительной информацией.', halign='center'),
                size_hint=(None, None), size=(300, 200))

    pop.open()


kv = Builder.load_file("my.kv", encoding='utf8')

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="LOGIN"), CreateAccountWindow(name="CREATE"), MainWindow(name="main"), ToWindow(name="TOPARS")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "LOGIN"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
