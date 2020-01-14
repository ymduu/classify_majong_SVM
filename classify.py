#coding: utf-8
from svmutil import *
import os
from PIL import Image
from numpy import *
import sys
from pylab import *
from matplotlib.pyplot import *
import cv2
import preprocess

#整数ラベルと文字列ラベルの間の辞書
transl={}
#文字列ラベルのリスト
ls=["1m","2m","3m","4m","5m","6m","7m","8m","9m","1p","2p","3p","4p","5p","6p","7p","8p","9p","1s","2s","3s","4s","5s","6s","7s","8s","9s","tn","nn","sh","pe","hk","ht","ch","dm"]


#下処理で縮小と境界の削除が終わっているので、compute_featureはflattenのみ
def compute_feature(im):
    return im.flatten()

def str2int(s):
    return ls.index(s)

def trans_label(n):
    return transl[n]

#数値ラベルと文字列ラベルの変換辞書の準備
def prep_trans():
    for i in ls:
        transl[i]=str2int(i)
        transl[str2int(i)]=i

def load_ocr_data(path):
    #パスの中のすべての画像についてラベルとOCR画像を返す
    #jpgで終わるファイルを列挙
    imlist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
    #先頭2文字が麻雀牌を表すラベル
    labels=[imfile.split('/')[-1][0:2] for imfile in imlist]
    #ラベル変換辞書を作成
    prep_trans()
    labels=map(str2int,labels)
    #特徴量の生成
    features=[]
    #print imlist
    for imname in imlist:
        #print imname
        im=array(Image.open(imname).convert("L"))
        features.append(compute_feature(im))
    return array(features),labels

def load_ocr_data_file(filepath,thresh):
    features=[]
    
    im=array(Image.open(filepath).convert("L"))
    cvimage=cv2.imread(filepath,0)  #opencv画像として読み込み
    cv_processed=preprocess.prep_image(cvimage,thresh)    #下処理を行う
    cv2.imwrite("./preprocessed.jpg",cv_processed)      #画像を一度書き出し

    im=array(Image.open("./preprocessed.jpg").convert("L"))
    lookim=array(Image.open("./preprocessed.jpg").convert("L").convert("RGB"))
    subplot(131),
    imshow(lookim)
    title(u"prep_image")
    #show()

    features.append(compute_feature(im))
    return array(features)

def classify_majang(fpath,thresh):
    #入力をLibSVM用に整形
    #fpath:判別したい画像のパス
    #thresh:二値化の閾値
    loaded_features=load_ocr_data_file(fpath,thresh)
    loaded_features=map(list,loaded_features)
    print "input file:"+fpath

    res=svm_predict([0]*len(loaded_features),loaded_features,m)[0]
    print fpath+" looks like:"+trans_label(res[0])
    return res[0]

def show_result(fpath,result):
    #結果を適当に表示
    img=cv2.imread(fpath,0)
    im=array(Image.open(fpath).convert("RGB"))
    subplot(132)
    imshow(im)

    title("it looks like:"+trans_label(result))
    subplot(133)
    simg=array(Image.open("./resource/"+trans_label(result)+".png").convert("RGB"))
    imshow(simg)
    title(trans_label(result)+"'s sample image")
    show()

def train_majang():
    features,labels=load_ocr_data("./traindata/")
    test_features,test_labels=load_ocr_data("./testcase/")
    #SVM分類器の訓練
    features=map(list,features)
    test_features=map(list,test_features)
    prob=svm_problem(labels,features)
    param=svm_parameter("-t 0")

    m=svm_train(prob,param)
    print "teacher"
    res=svm_predict(labels,features,m)
    print "testcase"
    res=svm_predict(test_labels,test_features,m)[0]
    svm_save_model('test.model', m)
    print "svm model is saved in 'test.model'"
    return m

#インポート時に準備されてほしいコード群
#svmモデル
m=svm_load_model('test.model')

if m is None:
    #読み込み失敗
    print "model not found, I'm going to train svm..."
    m=train_majang()
#ラベル変換辞書の準備
prep_trans()

if __name__=="__main__":

    if len(sys.argv)<2:
        print "Usage:python main.py filepath"
        sys.exit(1)
    fpath=sys.argv[1]
    ret=classify_majang(fpath,140)
    show_result(fpath,ret)








#print labels





'''

'''




#print res[0]

#print transl

#print res
