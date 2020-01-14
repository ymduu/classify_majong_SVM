#coding: utf-8
import cv2
import cv
import numpy as np
import sys

def lookimg(img):
    for i in img:
        for j in i:
            if str(j)=="255":
                sys.stdout.write("1")
            else:
                sys.stdout.write(str("0"))
        sys.stdout.write("\n")



def cut_threshold(imgdata,thresh):
    #imgdata:cv2.imreadで読んだもの
    #threth:二値化のしきい値 デフォルトで140
    #高さ、横幅の取得
    if len(imgdata.shape) == 3:
        height, width, channels = imgdata.shape[:3]
    else:
        height, width = imgdata.shape[:2]
        channels = 1

    print height,width
    y=int(height*0.05)
    hy=int(y/2/2)
    x=int(width*0.05)
    hx=int(x/2)
    print x*2
    out=imgdata[y+y:height-y-y-hy,x+x:width-x-x]   #端を切り捨て
    out=cv2.threshold(out, thresh, 255, cv2.THRESH_BINARY)[1]
  

    up,down,left,right=-1,-1,100000000,-1

    for i in range(len(out)):
        #縦
        for j in range(len(out[0])):
            #横
            if out[i][j]==0:
                if up==-1:
                    up=i    #初めて見つかった黒点がup
                if down<i:
                    down=i  #黒点が下に見つかるたびに更新
                if left>j:
                    left=j  #黒点が左に見つかるたびに更新
                if right<j:
                    right=j #黒点が右に見つかるたびに更新
    print up , down,left,right
    out=out[up:down,left:right]
    #切り出してから縮小を行うと二値画像でなくなってしまうので注意
    #入力画像が白の場合は例外処理
    if (up,down,left,right)==(-1,-1,100000000,-1):
        out = np.zeros((40, 40, 3), np.uint8)
        for i in range(40):
            for j in range(40):
                out[i,j] = [255, 255, 255]
    return out

def prep_image(imgdata,thresh):
    #imgdata:cv2.imreadで読んだオブジェクト
    #thresh:二値化のしきい値
    
    #読み込んだ画像を二値化、麻雀牌の絵部分切り出し
    out=cut_threshold(imgdata,thresh)

    #画像を規定サイズに潰す
    out=cv2.resize(out,(40,40))
    #潰すと2値画像でなくなってしまうので再度2値化
    out=cv2.threshold(out, 185, 255, cv2.THRESH_BINARY)[1]
    return out

if __name__ == "__main__":
    arg=sys.argv
    if len(arg)<3:
        print "usage:preprocess.py filename testid"
        sys.exit(1)
    filename=arg[1]
    imgdata = cv2.imread(filename,0)
    
    #指定したファイルを読み込み下処理を行う
    out=prep_image(imgdata,140)
    #教師ケースの下処理を行う場合に使うlist
    fnamearray=["1s_","2s_","3s_","4s_","5s_","6s_","7s_","8s_","9s_","1p_","2p_","3p_","4p_","5p_","6p_","7p_","8p_","9p_","1m_","2m_","3m_","4m_","5m_","6m_","7m_","8m_","9m_","tn_","nn_","sh_","pe_","hk_","ht_","ch_","dm1_","dm2_"]
    
    testid=arg[2]
    outfilename="test"+testid+".jpg"

    cv2.imwrite("./processed/"+outfilename, out)
