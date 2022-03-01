# KV Libraries
import json
from time import sleep

from kivy.app import App
from kivy.lang import Builder
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

    def genUserData(self, acc, psw, firstTime=False):
        if acc == psw == '':
            return
        setup(acc, psw)
        if firstTime:
            print('\n' * 10)
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
        fonther = App._running_app.root
        res = s.get_test_status(login_data["name"], currentIndex)
        fonther.ids.testResult.text = ''
        for i in res.values():
            succeed = str(i[0])
            testResult = i[1]
            fonther.ids.testResult.text += succeed + " || " + testResult[14:] + '\n'

        self.dismiss()


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
        res = s.get_test_status(login_data["name"], currentIndex)
        self.ids.testResult.text = ''
        for i in res.values():
            succeed = str(i[0])
            testResult = i[1]
            self.ids.testResult.text += succeed + " || " + testResult[14:] + '\n'


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
        Builder.load_file("./setup.kv")
        # comment the line above to avoid reading .kv file twice
        print("Please Re-Run the Program")
    with JykuoSession(base_url) as s:
        currentIndex = ''
        Builder.load_file("./gui.kv")
        # comment the line above to avoid reading .kv file twice
        s.login(login_data)
        guiApp().run()
