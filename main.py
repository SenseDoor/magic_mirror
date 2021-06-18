# -*- coding: utf-8 -*-
import paho.mqtt.client as pahomqtt
import time
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys, os
from mirrorUI import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import requests
from bs4 import BeautifulSoup
import urllib
import re
import Adafruit_ADS1x15
from w1thermsensor import W1ThermSensor
import glob
from bottle import get,post,run,request,template,route
#from face import FaceFunction
#from speech import SpeechFunction

from faceClass import Face_Recognizer
import threading
import time
GAIN = 1
adc1 = Adafruit_ADS1x15.ADS1115(address=0x48)

# 本类用于执行一些循环、耗时的函数，并通过信号发射到UI界面
class ExQThread(QThread):

    timeSignal = pyqtSignal(str, str, str)
    tempSignal = pyqtSignal(str)
    lightSignal = pyqtSignal(str)
    
    def __init__(self):
        super(ExQThread, self).__init__()
        #self.thirdPart = ThirdPartInfo()
        self.running = True

    def updateTime(self):
        datetime = QDateTime.currentDateTime()
        time = datetime.toString('hh:mm:ss')
        date = datetime.toString('yyyy年MM月dd日')
        week = datetime.toString('dddd')
        self.timeSignal.emit(time, date, week)

    def updateTemp(self):
        
        
        onewire_dir = '/sys/bus/w1/devices/'
        sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,str(glob.glob(onewire_dir + '28*')[0])[23:])
        temperature = str(sensor1.get_temperature()-10)+"°"
        self.tempSignal.emit(temperature)
        
    def updateLight(self):
        
        
        temp_val = adc1.read_adc(3, gain=GAIN, data_rate=128)
        if temp_val > 4000:
            temp_val = 4000
        light = "当前室内光强"+str(100 - (temp_val / 40))
        self.lightSignal.emit(light)



    def run(self):
        cnt = 0
        while self.running:
            try:
                if cnt % 1 == 0:
                    self.updateTime()
                    print('updateTime')
                
                if cnt % 1 == 0:
                    self.updateTemp()
                    print('updateTemp')
                    
                if cnt % 1 == 0:
                    self.updateLight()
                    print('updateLight')
            
                if cnt >= 600:
                    cnt = 0
            except Exception as e:
                print(e)
            cnt += 1
            time.sleep(1)



class FaceThread(QThread):

    FaceSignal = pyqtSignal(str)
    
    def __init__(self):
        super(FaceThread, self).__init__()
        #self.thirdPart = ThirdPartInfo()
        self.running = True
        self.Face_Recognizer_con= Face_Recognizer()
        self.faceRec=threading.Thread(target=self.Face_Recognizer_con.run)
        self.faceRec.start()

    def updateFace(self):
        
        face=self.Face_Recognizer_con.return_anwser()
        print(face)
        self.FaceSignal.emit(face)

    def run(self):
        cnt = 0
        while self.running:
            try:
                if cnt % 2 == 0:
                    self.updateFace()
                    print('updateFace')
                
            except Exception as e:
                print(e)
            cnt += 1
            time.sleep(1)

txt=""
order=""
flag1=1
flag2=0
flag3=0
flag4=0
app = QtWidgets.QApplication(sys.argv)                          # 定义Qt应用
@get("/")
def index():
    return template("index")
@post("/cmd")
def cmd():
    global order
    print("按下了按钮: "+request.body.read().decode())
    order = request.body.read().decode()
    return "OK"

@route('/new',method='GET')
def memory():
    global txt
    if request.GET.save:
        txt=request.GET.task.strip()
        print(txt)

    return template("index")


class WebThread(QThread):

    
    ControlSignal = pyqtSignal(str)
    TextSignal =pyqtSignal(str)
    
    def __init__(self):
        super(WebThread, self).__init__()
        #self.thirdPart = ThirdPartInfo()
        self.running = True

        
    def run(self):
        run(host="192.168.43.81",port=8080)


   
# 本类用于界面UI处理，主要为槽函数，接收信号。
class MagicUI(Ui_MainWindow, QObject):
    
    def __init__(self):
        self.todo_string = ''
        self.todo_cnt = 0
        super(MagicUI, self).__init__()

    def setupUi(self, MainWindow):
        super(MagicUI, self).setupUi(MainWindow)
        self.gif = QMovie("source/洛天依_黑.gif")
        self.label_gif.setMovie(self.gif)
        self.gif.start()

    # 强制刷新界面
    def refresh(self):
        # 实时刷新界面
        QApplication.processEvents()

    # 更新时间、日期等，定时高频更新
    def updateTime(self, time, date, week):
        global txt,order,flag1,flag2,flag3,flag4,app
        self.label_time.setText(time)
        self.label_date.setText(date)
        self.label_week.setText(week)
        if order == "up":
            flag1=not flag1
        if order == "left":
            flag2=not flag2
        
        
            
        
        self.label_headlinesmsg.setText(txt)
        
    # 获取温湿度传感器信息，这部分获取可能很慢，定时低频更新
    def updateTemp(self, temperature):

        self.label_temperature.setText(temperature)
        
    def updateLight(self, light):

        self.label_humidity.setText(light)
    
    def updateFace(self,face):
            
        self.label_todomsg.setText(face)
        


def main():


    MainWindow = QtWidgets.QMainWindow()                            # 窗口实例
    ui = MagicUI()                                                  # 界面UI实例

    ui.setupUi(MainWindow)                                          # 绘制界面
    exQthread = ExQThread()                                         # 线程实例
    exQthread.tempSignal.connect(ui.updateTemp)                     # 信号连接槽函数
    exQthread.timeSignal.connect(ui.updateTime)                     # 信号连接槽函数
    exQthread.lightSignal.connect(ui.updateLight)                     # 信号连接槽函数
    exQthread.start()                                               # 线程开始运行

    facethread = FaceThread()
    facethread.FaceSignal.connect(ui.updateFace)
    facethread.start()
    
    
    webthread = WebThread()
    webthread.start()
    

    
    
    MainWindow.showFullScreen()                                               # 显示窗口
    sys.exit(app.exec_())                                           # 应用关闭
    
# 程序从此开始执行
if __name__ == '__main__':
    main()
