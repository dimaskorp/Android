from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.config import Config
from kivy.uix.button import Button
from parsing import f_departments


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
        sm.current = "create"

    def reset(self):
        self.login.text = ""
        self.password.text = ""



class MainWindow(Screen):
    login = ObjectProperty(None)
    created = ObjectProperty(None)
    grid = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        self.buttons = []
        names = f_departments().keys()
        name, created = db.get_user(self.current)
        self.login.text = "Имя учетной записи: " + name
        self.created.text = "Создано: " + created
        i = 1
        for n in names:
            self.but = Button(text=n,
                              size_hint=(0.5, 0.5),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              font_size=(self.grid.width ** 2 + self.grid.height ** 2) / 10 ** 4,
                              #font_size='16sp',
                              on_press=self.open_webbrowser)
            self.buttons.append(self.but)
            self.grid.add_widget(self.but)
            i += 1

    def open_webbrowser(self, instance):
        import webbrowser
        url = 'https://igis.ru/online' + instance.text
        webbrowser.open(url)

    def clearGrid(self):
        self.buttons.clear()


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

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
