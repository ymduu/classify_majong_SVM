#coding: utf-8
from svmutil import *
import os
from PIL import Image
from numpy import *
import sys
from pylab import *
from matplotlib.pyplot import *
import cv2

#整数ラベルと文字列ラベルの間の辞書
transl={}

#下処理で縮小と境界の削除が終わっているので、compute_featureはflattenのみ
def compute_feature(im):
    return im.flatten()

def str2int(s):
    ls=["1m","2m","3m","4m","5m","6m","7m","8m","9m","1p","2p","3p","4p","5p","6p","7p","8p","9p","1s","2s","3s","4s","5s","6s","7s","8s","9s","tn","nn","sh","pe","hk","ht","ch","dm"]

    return ls.index(s)

def trans_label(n):
    return transl[n]

def load_ocr_data(path):
    #パスの中のすべての画像についてラベルとOCR画像を返す
    #jpgで終わるファイルを列挙
    imlist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
    #先頭2文字が麻雀牌を表すラベル
    labels=[imfile.split('/')[-1][0:2] for imfile in imlist]
    for i in labels:
        transl[i]=str2int(i)
        transl[str2int(i)]=i
    labels=map(str2int,labels)
    #特徴量の生成
    features=[]
    #print imlist
    for imname in imlist:
        #print imname
        im=array(Image.open(imname).convert("L"))
        features.append(compute_feature(im))
    return array(features),labels

def load_ocr_data_file(filepath):
    features=[]
    im=array(Image.open(filepath).convert("L"))
    features.append(compute_feature(im))
    return array(features)
features,labels=load_ocr_data("./traindata/")
test_features,test_labels=load_ocr_data("./testcase/")
if len(sys.argv)<2:
    print "Usage:python main.py filepath"
    sys.exit(1)
fpath=sys.argv[1]
loaded_features=load_ocr_data_file(fpath)




#SVM分類器の訓練
features=map(list,features)
test_features=map(list,test_features)
loaded_features=map(list,loaded_features)

#print labels

prob=svm_problem(labels,features)
param=svm_parameter("-t 0")

m=svm_train(prob,param)

svm_save_model('test.model', m)
'''
print "teacher"
res=svm_predict(labels,features,m)
print "testcase"
res=svm_predict(test_labels,test_features,m)[0]
'''
print "input file:"+fpath
#print len(loaded_features)
res=svm_predict([0]*len(loaded_features),loaded_features,m)[0]
print fpath+" looks like:"+trans_label(res[0])

img=cv2.imread(fpath,0)
imshow(img, cmap = 'gray', interpolation = 'bicubic')
xticks([]), yticks([])  # to hide tick values on X and Y axis
title("it looks like:"+trans_label(res[0]))
show()

#print res[0]

#print transl

#print res
