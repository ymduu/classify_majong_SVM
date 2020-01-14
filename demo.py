#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime
import cv2
import classify
from numpy import *
import cv

#値の初期化

cap = cv2.VideoCapture(0)

cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1200);
cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 900);

size=3.5
height=26*size
width=19*size
threth=140
syakin=cv2.imread("./pu.png")
hai=""

print size
def drawCVImage():
    ret, frame = cap.read()
    global size
    global height
    global width
    global threth
    global syakin
    global hai
	#10msecキー入力待ち
    k = cv2.waitKey(10)
	#Escキーを押されたら終了
	#if k == 27:
	#	break
    if k==ord("k"):
		size+=0.1
    if k==ord("s"):
		size-=0.1
		print size
    if k==ord("c"):
		cv2.imwrite("tmp.png",hai)
		for y in range(96):
			for x in range(369):
				frame[y+340,x+150]=syakin[y,x]
		cv2.imshow('camera capture', frame)
		tin=cv2.waitKey(10)
		print "captured."

		res=classify.classify_majang("./tmp.png")

		
		classify.show_result("./tmp.png",res)

    if k==ord("u"):
		threth+=5
		print threth
    if k==ord("d"):
		threth-=5
		print threth


	#frameを表示
    x,y=300,200
    height=26*size
    width=19*size
    binary=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    binary=cv2.threshold(binary, threth, 255, cv2.THRESH_BINARY)[1]
    cv2.rectangle(binary,(x,y),(int(x+width),int(y+height)),(0,0,255),2)
    cv2.rectangle(frame,(x,y),(int(x+width),int(y+height)),(0,0,255),2)
    cv2.imshow('camera capture', frame)
    hai=frame[y:int(y+height),x:int(x+width)]

class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.w = QWidget()               
        #self.setGeometry(300, 300, 250, 150)
        self.w.resize(640, 320)
        self.setWindowTitle('Statusbar')    
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(drawCVImage)
        timer.start(33) #33msecごとに描画       
       

    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")
        self.statusBar().showMessage(daystr)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    #キャプチャを終了
    cap.release()
    cv2.destroyAllWindows()