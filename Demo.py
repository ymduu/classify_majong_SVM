#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
import classify
from numpy import *
import cv
import commands


ls=["dm0","1m","2m","3m","4m","5m","6m","7m","8m","9m","dm1","1p","2p","3p","4p","5p","6p","7p","8p","9p","dm2","1s","2s","3s","4s","5s","6s","7s","8s","9s","dm3","tn","nn","sh","pe","hk","ht","ch","dm"]
mtx=array([[  3.21057970e+03 ,  0.00000000e+00 ,  5.54643996e+02],[  0.00000000e+00 ,  3.21780801e+03 ,  3.02428784e+02], [  0.00000000e+00 ,  0.00000000e+00  , 1.00000000e+00]])
dist=array([  7.08698548e-02 , -1.86319657e+01  , 5.04192020e-03  , 9.54354904e-03 ,-6.39007528e+01])
print mtx
print dist


class DemoApp(QMainWindow):
    
    def main(self):
        self.window = QWidget()
        
            
        # ボタン配置
        #よこ1行目
        rb_label=QLabel(u"描画モード:")
        self.rb_picture_bin=QRadioButton("binary")
        self.rb_picture_nomal=QRadioButton("nomal")
        self.rb_picture_nomal.setChecked(True)
        self.picture_ButtonGroup=QButtonGroup()
        self.picture_ButtonGroup.addButton(self.rb_picture_bin)
        self.picture_ButtonGroup.addButton(self.rb_picture_nomal)
        hbox = QHBoxLayout()
        hbox.addWidget(rb_label)
        hbox.addWidget(self.rb_picture_bin)
        hbox.addWidget(self.rb_picture_nomal)

        #よこ2行目
        rg_label=QLabel(u"認識モード:")
        self.rg_mode_one=QRadioButton(u"一枚")
        self.rg_mode_calc=QRadioButton(u"点数計算")
        self.rg_mode_one.setChecked(True)
        self.mode_ButtonGroup=QButtonGroup()
        self.mode_ButtonGroup.addButton(self.rg_mode_one)
        self.mode_ButtonGroup.addButton(self.rg_mode_calc)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(rg_label)
        hbox2.addWidget(self.rg_mode_one)
        hbox2.addWidget(self.rg_mode_calc)
        #よこ3行目
        self.threshold=140
        self.threshold_plus=QPushButton("+5",self)
        self.threshold_minus=QPushButton("-5",self)
        self.threth_label=QLabel("threshold: "+str(self.threshold))
        self.connect(self.threshold_plus, SIGNAL('clicked()'), self.threshold_p5)
        self.connect(self.threshold_minus, SIGNAL('clicked()'), self.threshold_m5)
        hbox3=QHBoxLayout()
        hbox3.addWidget(self.threth_label)
        hbox3.addWidget(self.threshold_plus)
        hbox3.addWidget(self.threshold_minus)

        #よこ4行目
        """
        self.size_slider=QSlider(Qt.Horizontal)
        self.size_slider.setRange(30,40)
        self.size_slider.setValue(35)  #初期値は35,sizeは1/10して使ってください
        self.size_label=QLabel("size: "+str(self.size_slider.value()))
        self.connect(self.size_slider, SIGNAL('valueChanged(int)'), self.size_change)
        """
        self.size=26 #初期値は30,sizeは1/10して使ってください
        self.size_plus=QPushButton("+1",self)
        self.size_minus=QPushButton("-1",self)
        self.size_label=QLabel("size: "+str(self.size))
        self.connect(self.size_plus, SIGNAL('clicked()'), self.size_p1)
        self.connect(self.size_minus, SIGNAL('clicked()'), self.size_m1)
        hbox4=QHBoxLayout()
        hbox4.addWidget(self.size_label)
        hbox4.addWidget(self.size_plus)
        hbox4.addWidget(self.size_minus)

        #よこ5行目
        
        self.info_label=QLabel(u"場情報(一枚のみ認識時は使いません)")
        hbox5=QHBoxLayout()
        hbox5.addWidget(self.info_label)

        #よこ6行目
        ba_label=QLabel(u"場風:")
        self.ba_button_tn=QRadioButton(u"東")
        self.ba_button_nn=QRadioButton(u"南")
        self.ba_button_sh=QRadioButton(u"西")
        self.ba_button_pe=QRadioButton(u"北")
        self.ba_button_tn.setChecked(True)
        self.ba_ButtonGroup=QButtonGroup()
        self.ba_ButtonGroup.addButton(self.ba_button_tn)
        self.ba_ButtonGroup.addButton(self.ba_button_nn)
        self.ba_ButtonGroup.addButton(self.ba_button_sh)
        self.ba_ButtonGroup.addButton(self.ba_button_pe)
        
        hbox6 = QHBoxLayout()
        hbox6.addWidget(ba_label)
        hbox6.addWidget(self.ba_button_tn)
        hbox6.addWidget(self.ba_button_nn)
        hbox6.addWidget(self.ba_button_sh)
        hbox6.addWidget(self.ba_button_pe)
        #よこ7行目
        ji_label=QLabel(u"自風:")
        self.ji_button_tn=QRadioButton(u"東")
        self.ji_button_nn=QRadioButton(u"南")
        self.ji_button_sh=QRadioButton(u"西")
        self.ji_button_pe=QRadioButton(u"北")
        self.ji_button_tn.setChecked(True)
        self.ji_ButtonGroup=QButtonGroup()
        self.ji_ButtonGroup.addButton(self.ji_button_tn)
        self.ji_ButtonGroup.addButton(self.ji_button_nn)
        self.ji_ButtonGroup.addButton(self.ji_button_sh)
        self.ji_ButtonGroup.addButton(self.ji_button_pe)
        
        hbox7 = QHBoxLayout()
        hbox7.addWidget(ji_label)
        hbox7.addWidget(self.ji_button_tn)
        hbox7.addWidget(self.ji_button_nn)
        hbox7.addWidget(self.ji_button_sh)
        hbox7.addWidget(self.ji_button_pe)
        
        #よこ8行目
        self.dorabox=QLineEdit(self)
        dora_label=QLabel(u"ドラ")
        hbox8=QHBoxLayout()
        hbox8.addWidget(dora_label)
        hbox8.addWidget(self.dorabox)
        
        #よこ9行目
        
        self.honba_slider=QSlider(Qt.Horizontal)
        self.honba_slider.setRange(0,20)
        self.honba_slider.setValue(0)  #初期値は0
        self.honba_label=QLabel(u"本場: "+str(self.honba_slider.value()))
        self.connect(self.honba_slider, SIGNAL('valueChanged(int)'), self.honba_change)
        hbox9=QHBoxLayout()
        hbox9.addWidget(self.honba_label)
        hbox9.addWidget(self.honba_slider)

        #画像情報からはわからない役
        #よこ10行目
        
        self.info_label=QLabel(u"画像情報からはわからない役(一枚のみ認識時は使いません)")
        hbox10=QHBoxLayout()
        hbox10.addWidget(self.info_label)
        #よこ11列目
        self.b_reach=QCheckBox(u"立直")
        self.b_ippatu=QCheckBox(u"一発")
        self.b_tumo=QCheckBox(u"ツモ")
        self.b_haitei=QCheckBox(u"海底摸月")
        hbox11=QHBoxLayout()
        hbox11.addWidget(self.b_reach)
        hbox11.addWidget(self.b_ippatu)
        hbox11.addWidget(self.b_tumo)
        hbox11.addWidget(self.b_haitei)
        #よこ12列目
        self.b_houtei=QCheckBox(u"河底撈魚")
        self.b_rinsyan=QCheckBox(u"嶺上開花")
        self.b_chankan=QCheckBox(u"槍槓")
        hbox12=QHBoxLayout()
        hbox12.addWidget(self.b_houtei)
        hbox12.addWidget(self.b_rinsyan)
        hbox12.addWidget(self.b_chankan)
        #よこ13行目
        self.CaptureButton=QPushButton("Capture!",self)
        self.connect(self.CaptureButton, SIGNAL('clicked()'), self.ClassifyHai)
        hbox13=QHBoxLayout()
        hbox13.addWidget(self.CaptureButton)
        #よこ14行目
        
        self.opt_label=QLabel(u"読み込み結果修正/オプション")
        hbox14=QHBoxLayout()
        hbox14.addWidget(self.opt_label)
        #よこ15列目
        self.opt_Detail=QCheckBox(u"麻雀牌読み込み結果を詳細表示する(点数計算時)")
        hbox15=QHBoxLayout()
        hbox15.addWidget(self.opt_Detail)
        #よこ16行目
        self.tehaibox=QLineEdit(self)
        tehai_label=QLabel(u"手牌")
        hbox16=QHBoxLayout()
        hbox16.addWidget(tehai_label)
        hbox16.addWidget(self.tehaibox)
        #よこ17行目
        self.calcButton=QPushButton(u"点数計算",self)
        self.connect(self.calcButton, SIGNAL('clicked()'), self.calc_point)
        hbox17=QHBoxLayout()
        hbox17.addWidget(self.calcButton)
        #たて
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox9)
        vbox.addLayout(hbox10)
        vbox.addLayout(hbox11)
        vbox.addLayout(hbox12)
        vbox.addLayout(hbox13)
        vbox.addLayout(hbox14)
        vbox.addLayout(hbox15)
        vbox.addLayout(hbox16)
        vbox.addLayout(hbox17)
        #vbox.addWidget(button3)
        
        
        self.window.setLayout(vbox)

        #GUI準備完了,ビデオキャプチャ等準備
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1200);
        self.cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 900);

        self.syakin=cv2.imread("./pu.png")
        timer = QTimer(self)
        timer.timeout.connect(self.DrawCapturedPicture)
        timer.start(33) #msec   
        
        self.window.show()
        
    def threshold_p5(self):
        self.threshold+=5
        self.threth_label.setText("threshold: "+str(self.threshold))
    def threshold_m5(self):
        self.threshold-=5
        self.threth_label.setText("threshold: "+str(self.threshold))
    def size_p1(self):
        self.size+=1
        self.size_label.setText("size: "+str(self.size))
    def size_m1(self):
        self.size-=1
        self.size_label.setText("size: "+str(self.size))
    def size_change(self):
        self.size_label.setText("size: "+str(self.size_slider.value()))
    def honba_change(self):
        self.honba_label.setText(u"本場: "+str(self.honba_slider.value()))
    def DrawCapturedPicture(self):
        ret, self.frame = self.cap.read()
        if self.rg_mode_calc.isChecked():
            self.frame=cv2.undistort(self.frame,mtx,dist)
        self.frame=cv2.flip(self.frame,-1)
        height=(26*self.size)/10.0
        width=(19*self.size)/10.0
        x,y=575,380
        yy=290
        binary=cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        binary=cv2.threshold(binary, self.threshold, 255, cv2.THRESH_BINARY)[1]
        cv2.rectangle(binary,(x,y),(int(x+width),int(y+height)),(0,0,255),1)
        cv2.rectangle(self.frame,(x,y),(int(x+width),int(y+height)),(0,0,255),1)

        self.hais=[]
        '''
        for i in range(5):
            for j in range(3):
                #print yy+int(i*height)
                cv2.rectangle(binary,(int(480+width*j),yy+int(i*height)),(int(480+width*j+width),int(yy+height+int(i*height))),(0,0,255),1)
                cv2.rectangle(self.frame,(int(480+width*j),yy+int(i*height)),(int(480+width*j+width),int(yy+height+int(i*height))),(0,0,255),1)
                self.hais.append(self.frame[yy+int(i*height):int(yy+height+int(i*height)),int(480+width*j):int(480+width*j+width)])
        '''
        left=250
        for i in range(14):
            cv2.rectangle(binary,(int(left+width*i),yy),(int(left+width*i+width),int(yy+height)),(0,0,255),1)
            cv2.rectangle(self.frame,(int(left+width*i),yy),(int(left+width*i+width),int(yy+height)),(0,0,255),1)
            self.hais.append(self.frame[yy:int(yy+height),int(left+width*i):int(left+width*i+width)])

        if self.rb_picture_bin.isChecked():
            cv2.imshow('camera capture', binary)
        else:
            cv2.imshow('camera capture', self.frame)
        self.hai=self.frame[y:int(y+height),x:int(x+width)]
    def ClassifyHai(self):
        #cv2.imwrite("im.png",self.frame)
        if self.rg_mode_one.isChecked():
            cv2.imwrite("tmp.png",self.hai)
            cv2.imshow('camera capture', self.frame)
            tin=cv2.waitKey(10)
            print "captured."

            res=classify.classify_majang("./tmp.png",self.threshold)
            classify.show_result("./tmp.png",res)
        elif self.rg_mode_calc.isChecked():
            cou=0
            #点数計算バイナリに流し込む入力作成
            haistr=""
            str_forbox=""
            #各麻雀牌画像の取得
            for i in self.hais:
                cv2.imwrite("tmp"+str(cou)+".png",i)
                cv2.imshow('camera capture', self.frame)
                tin=cv2.waitKey(10)
                print "captured."
                #牌の識別
                res=classify.classify_majang("tmp"+str(cou)+".png",self.threshold)
                if self.opt_Detail.isChecked():
                    classify.show_result("tmp"+str(cou)+".png",res)
                cou+=1
                #結果をテキストボックス書き込み用文字列に追記
                str_forbox+=classify.trans_label(res)
                if(cou!=14):
                    str_forbox+=","
                #結果をテキストボックスに反映
            self.tehaibox.setText(str_forbox)

            #テキストボックスの数値を使って計算
            self.calc_point()
    def calc_point(self):
        haistr=""
        lstehai=self.tehaibox.text().split(",")
        for tehai in lstehai:
            haistr+=str(ls.index(tehai))
            haistr+="\n"
        
        #ドラ
        s=self.dorabox.text()
        ldr=s.split(",")
        for i in ldr:
            haistr+=str(ls.index(i))
            haistr+="\n"
        haistr+="99\n"
            #手牌からはわからない役
        if  self.b_reach.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        if  self.b_ippatu.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        if  self.b_chankan.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        if  self.b_rinsyan.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        if  self.b_haitei.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        #場風
        if  self.ba_button_tn.isChecked():
            haistr+="31\n"
        elif self.ba_button_nn.isChecked():
            haistr+="32\n"
        elif self.ba_button_sh.isChecked():
            haistr+="33\n"
        elif self.ba_button_pe.isChecked():
            haistr+="34\n"
        #自風
        if  self.ji_button_tn.isChecked():
            haistr+="31\n"
        elif self.ji_button_nn.isChecked():
            haistr+="32\n"
        elif self.ji_button_sh.isChecked():
            haistr+="33\n"
        elif self.ji_button_pe.isChecked():
            haistr+="34\n"
        #ツモ
        if  self.b_tumo.isChecked():
            haistr+="1\n"
        else:
            haistr+="0\n"
        hon=self.honba_slider.value()
        haistr+=str(hon)+"\n"
        #print commands.getoutput("echo  "+'"'+haistr+'"')
        print commands.getoutput("echo  "+'"'+haistr+'"'+"| ./a.out")

            
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = DemoApp()
    mainApp.main()
    app.exec_()
