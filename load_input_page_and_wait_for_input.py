# run interface server on localhost, then run this
# the display var is set for raspi, maybe different on your machine


import os

os.environ['DISPLAY'] = ':0.0'

import pyautogui

from selenium import webdriver
driver = webdriver.Firefox()
driver.maximize_window()
pyautogui.press('f11')

driver.get('http://localhost:5000/getUserInput')

import time
while True:
    tag = (driver.current_url+'#').split('#')[1]
    if tag != '':
        print(tag)
        break
    else:
        time.sleep(1)

driver.close()
