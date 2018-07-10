from selenium import webdriver
import hashlib, binascii
import os

def setPath():
    d = ";" + os.getcwd() + "\\webdriver"
    os.environ['path'] = os.environ['path'] + d
    print(os.environ['path'])

def generateScreenshot(url, project_id):
    setPath()
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    driver.set_window_size(800, 600)
    filename = str(project_id) + '.png'
    screen = driver.save_screenshot('static/assets/thumbnails/'+ filename)
    return screen

def hashed(password):
    s = os.environ['FLASK_SECRET_KEY'].encode('ASCII')
    pw = password.encode('ASCII')
    h = hashlib.pbkdf2_hmac('sha256', pw, s, 100000)
    return h
