# 麻雀牌画像認識デモ
2016年の工大祭で展示した麻雀牌を画像認識して点数計算するデモです。  
https://twitter.com/ymduu/status/784425894324473858

主に実践 コンピュータビジョン  
https://www.oreilly.co.jp/books/9784873116075/
の8章を参考に実装しています。  
# 注意事項
素材の出処がわからなくなってしまったため、工大祭で展示したものから画像を抜いてあります。  
動かすと実行時エラーが出るか画像が出ないかだと思うので参考程度にどうぞ。  
点数計算部分は http://cmj3.web.fc2.com/seisaku.html のコードをお借りしています。  
コンパイルした a.out を Demo.py と同じディレクトリに配置します。  
# 説明  
## Demo.py
デモを実行します。  
## main.py
traindata ディレクトリの正解データで学習し、testcase ディレクトリのテストケースの分類を試みます。  
学習結果をtest.modelに出力します。  
## classify.py
学習結果 test.model を用いて分類を行うための関数群が実装されています。
デモはこれらの関数を呼び出すことで実装されています。  
## preprocess.py
教師データを作成する際の下処理を行うためのスクリプトです。  
traindata 以下の画像はこのスクリプトにより作成されています。  
./makedata.sh  
で、そのディレクトリにあるすべてのpngに下処理を施し、./processed/に吐きます。  
下処理の内容は、以下を以下の順番で行います。  
・画像読み込み  
・画像の上下左右を一定割合で削除  
・二値化  
・ピクセルを走査して麻雀牌の絵部分の上下左右の座標を検出  
・その上下左右の座標に基づいて絵部分を切り出し  
・40*40に縮小  
・縮小アルゴリズムによって二値画像でなくなってしまうため、再度二値化  
・出力  
