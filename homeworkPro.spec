# -*- mode: python ; coding: utf-8 -*-

import os
from os.path import join
from kivy_deps import sdl2, glew
import json
from time import sleep
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser
from kivy.uix.popup import Popup
from kivy.tools.packaging import pyinstaller_hooks as hooks
from kivy import kivy_data_dir
from typing import Dict, Tuple
from requests import Session
from time import time

import urllib3
from bs4 import BeautifulSoup
from dateutil import parser
from urllib3.exceptions import InsecureRequestWarning
from typing import Dict, List, Tuple
from time import time



block_cipher = None
kivy_deps_all = hooks.get_deps_all()
kivy_factory_modules = hooks.get_factory_modules()


datas = [("./utils/__init__.py", "classes"),
              ("./utils/get.py", "classes"),
              ("./utils/get_question_statuses.py", "classes"),
              ("./utils/get_test_status.py", "classes"),
              ("./utils/login.py", "classes"),
              ("./utils/submit.py", "classes"),
              ("./utils/submit.py", "classes"),
              ("./utils/msjh.ttc", "font"),
              ("gui.kv", "design"),
              ("setup.kv", "design")
              ]


excludes_a = ['Tkinter', '_tkinter', 'twisted', 'docutils', 'pygments']
hiddenimports = kivy_deps_all['hiddenimports'] + kivy_factory_modules + ['win32timezone']

sdl2_bin_tocs = [Tree(p) for p in sdl2.dep_bins]
glew_bin_tocs = [Tree(p) for p in glew.dep_bins]
bin_tocs = sdl2_bin_tocs + glew_bin_tocs

kivy_assets_toc = Tree(kivy_data_dir, prefix=join('kivy_install', 'data'))

assets_toc = [kivy_assets_toc]
tocs = bin_tocs + assets_toc
a = Analysis(['gui.py'],
             pathex=[os.getcwd()],
             binaries=None,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=excludes_a,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *tocs,
          name='HomeworkSysPro',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )


