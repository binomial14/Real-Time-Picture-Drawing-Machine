#import necessary library 匯入RPi.GPIO與time時間函式庫
import RPi.GPIO as GPIO   
import time   
from picamera import PiCamera
from time import sleep
import sys
import os

image_outpath = sys.argv[1]
camera = PiCamera()
#camera.start_preview()
#sleep(5)
#camera.capture(image_outpath)
#camera.stop_preview()
# to use Raspberry Pi board pin numbers 使用板上定義的腳位號碼
GPIO.setmode(GPIO.BOARD)   

# set up pin 11 as an output  將P1接頭的11腳位設定為輸入 
GPIO.setup(11, GPIO.IN)
camera.start_preview()
# enter while loop unitl exit 隨著時間迴圈會重複執行，直到強制離開
while True:
    # set up input value as GPIO.11 將P1接頭的11腳位的值設定為inputValue
    inputValue = GPIO.input(11)
    # when user press the btn 如果是真 (玩家按下按鈕)
    if inputValue== False:
        # show string on screen   顯示被按下
        #camera.start_preview()
        print("Button pressed ")
        print("3")
        sleep(1)
        print("2")
        sleep(1)
        print("1")
        sleep(1)
        camera.capture(image_outpath)
        print("Finish!")
        camera.stop_preview()
        quit()
        # while inputValue ==  False:  
        # Set time interval as 0.3 second delay 設定延遲間隔為零點三秒鐘
            # time.sleep(0.3)   

