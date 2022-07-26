from itertools import count
from pickletools import uint1
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

#import tracemalloc

#tracemalloc.start()

_totalWatch = 0
_totalLike = 0
_totalSubscrib = 0


class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Youtube Watcher'
        self.left = 400
        self.top = 200
        self.width = 320
        self.height = 330
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labelWatch = QtWidgets.QLabel(self) 
        self.labelWatch.setText("Kaç dakika izlensin:")
        self.labelWatch.move(25, 27)

        self.textfieldWatch = QtWidgets.QLineEdit(self) 
        self.textfieldWatch.move(130, 25)

        self.labelWatchUrl = QtWidgets.QLabel(self) 
        self.labelWatchUrl.setText("Video linkini girin:")
        self.labelWatchUrl.move(25, 50)

        self.textfieldWatchUrl = QtWidgets.QLineEdit(self) 
        self.textfieldWatchUrl.move(130, 48)

        self.labelNext = QtWidgets.QLabel(self) 
        self.labelNext.setText("------------------------------------------------------------------------------")
        self.labelNext.move(25, 70)


        self.labelLike = QtWidgets.QLabel(self) 
        self.labelLike.setText("Kaç beğeni yapılsın:")
        self.labelLike.move(25, 97)

        self.textfieldLike = QtWidgets.QLineEdit(self) 
        self.textfieldLike.move(130, 95)

        self.labelLikeUrl = QtWidgets.QLabel(self) 
        self.labelLikeUrl.setText("Video linkini girin:")
        self.labelLikeUrl.move(25, 120)

        self.textfieldLikeUrl = QtWidgets.QLineEdit(self) 
        self.textfieldLikeUrl.move(130, 118)

        self.labelNext2 = QtWidgets.QLabel(self) 
        self.labelNext2.setText("------------------------------------------------------------------------------")
        self.labelNext2.move(25, 150)


        self.labelSubscrib = QtWidgets.QLabel(self) 
        self.labelSubscrib.setText("Kaç kişi abone olsun:")
        self.labelSubscrib.move(25, 177)

        self.textfieldSubscrib = QtWidgets.QLineEdit(self) 
        self.textfieldSubscrib.move(130, 175)

        self.labelSubscribUrl = QtWidgets.QLabel(self) 
        self.labelSubscribUrl.setText("Kanalın linkini girin:")
        self.labelSubscribUrl.move(25, 202)

        self.textfieldSubscribUrl = QtWidgets.QLineEdit(self) 
        self.textfieldSubscribUrl.move(130, 200)

        self.labelNext3 = QtWidgets.QLabel(self) 
        self.labelNext3.setText("------------------------------------------------------------------------------")
        self.labelNext3.move(25, 225)

        self.buton = QtWidgets.QPushButton(self) 
        self.buton.setText("Başla")
        self.buton.move(130, 250)

        self.buton.clicked.connect(self.thread) ##########

        self.statusLabel = QtWidgets.QLabel(self)
        self.statusLabel.setText("Bot durumu: pasif")
        self.statusLabel.move(110, 280)
        self.statusLabel.setMinimumSize(300, 10)
        self.mailLabel = QtWidgets.QLabel(self)
        self.mailLabel.move(110, 300)
        self.mailLabel.setText(str(self.countMail()) + " hesap bulundu.")
        self.show()

    @pyqtSlot()
    def thread(self):
        t1=Thread(target=self.start)
        t1.start()
    def updateWatchLabel(self):
        global _totalWatch
        self.labelWatch.setText("İzlenilen dakika: " + str(_totalWatch))
    def updateLikeLabel(self):
        global _totalLike
        self.labelLike.setText("Beğenilen sayısı: " + str(_totalLike))
    def updateSubscribLabel(self):
        global _totalSubscrib
        self.labelSubscrib.setText("Yapılan aboneler : " + str(_totalLike))

    def start(self):
        self.statusLabel.setText("Tarayıcı çalıştırılıyor...")
        mails = open("mail.txt", "r")
        for mail in mails:
            currentUser = mail.split(":")
            username = currentUser[0]
            password = currentUser[1]
            self.loginYoutube(username,password)
            time.sleep(31)
        mails.close()
    def countMail(self):
        fp = open("mail.txt", 'r')
        x = len(fp.readlines())
        fp.close()
        return x;
    def check_exists_by_css(self,cssSelector,webdriver):
        try:
            webdriver.find_element_by_css_selector(cssSelector)
        except NoSuchElementException:
            return False
        return True    
    def loginYoutube(self,username,password):
    
        #for remember what choice
        watch = 0;
        like = 0;
        subscrib = 0;

        if(str(self.textfieldWatch.text())!=""):
            watch = int(str(self.textfieldWatch.text()))
        if(str(self.textfieldLike.text())!=""):
            like = int(str(self.textfieldLike.text()))
        if(str(self.textfieldSubscrib.text())!=""):
            subscrib = int(str(self.textfieldSubscrib.text()))

        watchUrl = str(self.textfieldWatchUrl.text())
        likeUrl = str(self.textfieldLikeUrl.text())
        subscribUrl = str(self.textfieldSubscribUrl.text())

        choice = 0
        if watch > 0:
            choice = 1
        if like > 0:
            choice = 2
        if subscrib > 0:
            choice = 3
        
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options,use_subprocess=True)
        url = "https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dtr%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=tr&ec=65620"
        driver.get(url)
        self.statusLabel.setText("Google'a giriliyor...")

        time.sleep(1)
        mail = driver.find_element_by_id("identifierId")
        mail.send_keys(username)
        self.statusLabel.setText("Mail girildi...")
        time.sleep(2)

        nextButton = driver.find_element_by_css_selector("div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb")
        nextButton.click()
        time.sleep(6)

        googlePass = driver.find_element_by_name("password")
        googlePass.send_keys(password)
        self.statusLabel.setText("Şifre girildi...")
        time.sleep(5)

        #loginButton = driver.find_element_by_css_selector("div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb")
        #loginButton.click()
    
        self.statusLabel.setText("Giriş yapıldı...")
        #login success
        time.sleep(5)

        if choice == 1:
            self.statusLabel.setText("İzlenme başlıyor...")
            #start watching 
            global _totalWatch
            if _totalWatch < watch:
                print(_totalWatch) ###
                self.statusLabel.setText("Videoya gidiliyor...")
                driver.get(watchUrl)
                time.sleep(8)

                checkAds = self.check_exists_by_css("button.ytp-ad-skip-button.ytp-button",driver)
                if checkAds:
                    ads = driver.find_element_by_css_selector("button.ytp-ad-skip-button.ytp-button")
                    ads.click()
                #button.ytp-ad-skip-button.ytp-button -- reklam bypass

                self.statusLabel.setText("İzlenme başladı...")
                duration = driver.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text
                print(duration);
                durationSplit = duration.split(":")
                minutes=int(durationSplit[0])
                seconds=int(durationSplit[1])
                time.sleep(minutes*60 + float(seconds/60))
                _totalWatch = _totalWatch + minutes + float(seconds/60)
                self.statusLabel.setText("Sıradaki hesaba geçiliyor...")
                print(_totalWatch) ###

        if choice == 2:
            global _totalLike
            #start like
            if _totalLike < like:
                self.statusLabel.setText("Video beğeniliyor...")
                self.updateLikeLabel()
                driver.get(likeUrl)
                time.sleep(3)
                getLikeButton = driver.find_element_by_css_selector("yt-icon-button#button.style-scope.ytd-toggle-button-renderer.style-text")[0].text
                getLikeButton.Click()
                _totalLike = _totalLike + 1 
                time.sleep(1)
                self.statusLabel.setText("Sıradaki hesaba geçiliyor...")
                self.updateLikeLabel()

        if choice == 3:
            global _totalSubscrib
            #start subscrib
            if _totalSubscrib < subscrib:
                self.statusLabel.setText("Abone olunuyor...")
                self.updateSubscribLabel()
                driver.get(subscribUrl)
                time.sleep(3)
                getSubscribeButton = driver.find_element_by_css_selector("div#subscribe-button.style-scope.ytd-c4-tabbled-header-renderer")[0].text
                getSubscribeButton.Click()
                time.sleep(2)
                _totalSubscrib += 1
                self.updateSubscribLabel()
                self.statusLabel.setText("Sıradaki hesaba geçiliyor...")
        driver.quit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())