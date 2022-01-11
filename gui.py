# KV Libraries
import json
from time import sleep

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser
from kivy.uix.popup import Popup

# Noobdy Libraries

from utils.setup import setup
from utils import JykuoSession


# s = None


class SetupPopup(Popup):
    def __init__(self, **kwargs):
        super(SetupPopup, self).__init__(**kwargs)

    def genUserData(self, acc, psw, firstTime = False):
        if acc == psw == '':
            return
        setup(acc, psw)
        if firstTime:
            print('\n'*10)
            print("Please Re-Run The Program")
        self.dismiss()
        exit(0)


class FileChooser(Popup):
    def __init__(self, **kwargs):
        super(FileChooser, self).__init__(**kwargs)

    def select(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass

    def sel(self, path, filename: list):
        if len(filename) == 0:
            return
        temp = filename[0].replace('\\', '/')
        print(temp)
        s.delete(currentIndex)
        s.submit(currentIndex, temp)
        self.dismiss()

        # s.get_test_status() TODO: await nobody debug
        # currentIndex be like "012"
        # filename[0] be like "D:\0.0\Homework-ProJYKt\hwp.py"


class mainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(mainWindow, self).__init__(**kwargs)

    def chooseFile(self):
        pop = FileChooser()
        pop.open()

    def generateUserData(self):
        pop = SetupPopup()
        pop.open()

    def search(self):
        global currentIndex
        currentIndex = self.ids.index.text.rjust(3, '0')
        self.ids.content.text = s.get(currentIndex)
        # self.ids.testResult.text = s.get_test_status #TODO: await nobody to debug


class guiApp(App):
    def build(self, **kwargs):
        super(guiApp, self).build(**kwargs)
        return mainWindow()


class setupping(GridLayout):
    def __init__(self, **kwargs):
        super(setupping, self).__init__(**kwargs)
        pop = SetupPopup()
        pop.open()


class setupApp(App):
    def build(self, **kwargs):
        super(setupApp, self).build(**kwargs)
        return setupping()


if __name__ == "__main__":
    try:
        with open("./config.json", "r") as file:
            login_data = json.load(file)
            base_url = login_data.pop("base_url")
    except:
        setupApp().run()
        print("Please Re-Run the Program")
    with JykuoSession(base_url) as s:
        currentIndex = ''
        s.login(login_data)
        guiApp().run()
