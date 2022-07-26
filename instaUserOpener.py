from encodings import utf_8
from http.client import USE_PROXY
from itertools import count
from pickletools import uint1
from weakref import proxy
import undetected_chromedriver.v2 as uc
import _thread
import threading
from threading import *
import time
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
from selenium.common.exceptions import NoSuchElementException        
from random import randrange
from selenium.webdriver.support.ui import Select
import random 
from selenium.webdriver.common.action_chains import ActionChains
import string
import os 
import zipfile
import parallelTestModule

def startInsta():
    
    mails = open("mail.txt", "r",encoding="utf8")
    for mail in mails:
        currentUser = mail.split(":")
        username = currentUser[0]
        password = currentUser[1]
        createInstagram(username,password)
        time.sleep(45)
    mails.close()

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

def createInstagram(yandexMail,yandexPass):
    use_proxy=True
    user_agent=False

    proxyList = open('proxy.txt').read().splitlines()
    myProxy =random.choice(proxyList)
    splitMyProxy = myProxy.split(":")
    PROXY_HOST = splitMyProxy[0]
    PROXY_PORT = splitMyProxy[1]
    PROXY_USER = splitMyProxy[2]
    PROXY_PASS = splitMyProxy[3]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--disable-popup-blocking')
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = uc.Chrome(chrome_options=chrome_options)

    url = "https://www.instagram.com/accounts/emailsignup/?hl=tr"
    #get random instagram username;
    words = yandexMail.split("@");
    username = random_char(1) + words[0] + random_char(1) + str(random.randint(10,99))
    #get random fullname from txt
    lines = open("fullname.txt", "r",encoding="utf8").read().splitlines()
    myline =random.choice(lines)

    instagramUsername = username.lower()
    instagramPassword = yandexPass
    instagramName = myline.lower()

    try:
        ## go and register instagram
        driver.get(url)
        time.sleep(10)
        try:
            mail = driver.find_element_by_name("emailOrPhone")
            mail.send_keys(yandexMail)
        except:
            driver.refresh();
            time.sleep(10);
            mail = driver.find_element_by_name("emailOrPhone")
            mail.send_keys(yandexMail)
        time.sleep(1)
        fullName = driver.find_element_by_name("fullName")
        fullName.send_keys(instagramName.lower())
        time.sleep(1)
        instaUsername = driver.find_element_by_name("username")
        instaUsername.send_keys(instagramUsername)
        time.sleep(1)
        instaPassword = driver.find_element_by_name("password")
        instaPassword.send_keys(instagramPassword)
        time.sleep(1)
        ## go date page
        try:
            buttonRegister = driver.find_element_by_xpath("//button[text()='Kaydol']");
            buttonRegister.click()
        except:
            time.sleep(1)
        time.sleep(3)
        
        #set date
        allDate = driver.find_elements_by_class_name("h144Z")
        
        selectMonth = Select(allDate[0])
        selectMonth.select_by_index(random.randint(1,11))
        time.sleep(1)

        selectDay = Select(allDate[1])
        selectDay.select_by_index(random.randint(1,27))
        time.sleep(1)

        selectYear = Select(allDate[2])
        selectYear.select_by_index(random.randint(22,50))
        time.sleep(1)
        #end date

        buttonRegister2 = driver.find_element_by_class_name("lC6p0")
        buttonRegister2.click()

        ##Login yandex 
        driver.execute_script("window.open('https://google.com','_blank')") 
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])

        driver.get("https://passport.yandex.com.tr/auth?from=mail&origin=hostroot_homer_auth_tr&retpath=https%3A%2F%2Fmail.yandex.com.tr%2F&backpath=https%3A%2F%2Fmail.yandex.com.tr%3Fnoretpath%3D1")
        time.sleep(10)
            
        yandexMailLogin = driver.find_element_by_id("passp-field-login")
        yandexMailLogin.send_keys(yandexMail)
        time.sleep(2)

        buttonLoginYandex = driver.find_element_by_id("passp:sign-in")
        buttonLoginYandex.click()
        time.sleep(4)

        yandexMailPass = driver.find_element_by_id("passp-field-passwd")
        yandexMailPass.send_keys(yandexPass)
        time.sleep(2)

        try:
            buttonLoginYandexFinal = driver.find_element_by_id("passp:sign-in")
            buttonLoginYandexFinal.click()
            time.sleep(5)
        except:
            time.sleep(2)
        try: 
            driver.get("https://mail.yandex.com.tr/#tabs/social")
            time.sleep(10)
        except:
            driver.get("https://mail.yandex.com.tr/#tabs/social")
            time.sleep(10)
            
        try: 
            #if popup is available
            popupClose = driver.find_element_by_css_selector("div.b-popup__close.ns-action")
            popupClose.click()
            time.sleep(2)
        except:
            time.sleep(1)
            
        #click mail
        selectHrefCode = driver.find_elements_by_class_name("mail-MessageSnippet-Wrapper")
        selectHrefCode[0].click()
        time.sleep(5)

        #get verification code
        yandexCodeGet = driver.find_elements_by_tag_name("td")
        yandexCode = ""
        yandexCode = yandexCodeGet[16].text
        time.sleep(2)
        ##end yandex 
        driver.switch_to.window(driver.window_handles[0])

        #send verification code 

        emailConfirmation = driver.find_element_by_name("email_confirmation_code")
        emailConfirmation.send_keys(yandexCode)

        time.sleep(1)
        #final: click register 
        registerButtonLast = driver.find_element_by_class_name("L3NKy")
        registerButtonLast.click()

        #wait for result -- it will be changed 15-20 seconds
        time.sleep(30)

        if yandexCode != "":
            file_object = open('openedUser.txt', 'a+')
            file_object.write("\n")
            # Append text at the end of file
            file_object.write(instagramUsername + ":" + instagramPassword + ":" + instagramName + ":" + yandexMail + ":" + yandexPass)
            file_object.close()

    except:
        print("a")
    finally:
        driver.quit()

    
if __name__ == '__main__':    
    extractor = parallelTestModule.ParallelExtractor()
    extractor.runInParallel(numProcesses=2, numThreads=4)
    startInsta()

