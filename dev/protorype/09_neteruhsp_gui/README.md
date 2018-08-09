[トップに戻る](https://github.com/dolphilia/tinyhsp)

---

# neteruhspにGUIを実装する

プロトタイプ9号は「neteruhspにGUIを実装する」です。

exrdさんの[neteruhsp](https://github.com/exrd/neteruhsp)の出来が素晴らしく、
かつNYSLライセンスで公開してくださっているので、
早速TinyHSPに利用させていただきました。

neteruhspをベースに、
次の命令を追加しました。

|-|書式|説明|
|---|---|---|
|wait|wait p1| p1ミリ秒待つ|
|stop|stop|クローズされるまで待つ|
|title|title p1|タイトルバーに文字列p1を表示する|
|pset|pset p1,p2|位置p1,p2にドットを描画する。p1,p2が省略された場合はカレントポジションに描画する|
|line|line p1,p2,p3,p4|位置p1,p2から位置p3,p4まで線を描画する|
|boxf|line p1,p2,p3,p4|位置p1,p2から位置p3,p4まで矩形を塗りつぶす|
|redraw|redraw p1|p1が0なら再描画スイッチをオフに、1ならオンにする。p1が省略されたらオンにする|
|pos|pos p1,p2|位置p1,p2をカレントポジションに設定する|
|color|color p1,p2,p3|RGBカラーp1,p2,p3をカレントカラーに設定する|
|stick|stick p1|数値変数p1にキー情報を格納する。本家HSPの stick p1,1+2+4+8+16+32+64+128+256+512+1024 相当の動作をする|

また、次のシステム変数を追加しました。

|-|説明|
|---|---|
|mousex|マウスのx座標|
|mousey|マウスのy座標|
|mousel|マウスの左ボタンが押されていれば1、押されていなけば0|
|mouser|マウスの右ボタンが押されていれば1、押されていなけば0|

## その他の仕様

スクリプトファイルの末尾まで実行したら、
自動的に終了するようになっています。

すぐにウィンドウを閉じないようにするためには、
HSP2.xのようにソースの末尾にstopを書く必要があります。

## ソースコードのコンパイル

GLFWとOpenGLを使用しているので、
導入していない場合はインストールします。

ソースコードのコンパイルは、
環境によりそれぞれ以下のようにします。

MinGW
`$ g++ tinyhsp.cpp -o tinyhsp -std=c++11 -lglfw3dll -lopengl32`

macOS
`$ clang++ tinyhsp.cpp -o tinyhsp -std=c++11 -lglfw -framework OpenGL`

Linux
`$ g++ tinyhsp.cpp -o tinyhsp -std=c++11 -lm -ldl -lglfw3 -lGL -lX11 -lXxf86vm -lXrandr -lXinerama -lXcursor -lpthread -lXi`

上記の`-std=c++11`はコンパイラのバージョンによっては、あるいは`-std=gnu++11`、あるいは`-std=c++0x`、あるいは`-std=gnu++0x`と書くのが正しい可能性もあります。

## 実行

`$ ./tinyhsp`
のようにコマンドラインのオプションに何も指定がない場合は、
実行ファイルと同じディレクトリにある`start.hsp`を読み込みます。

明示的に、
`$ ./tinyhsp -f start.hsp`
のように`-f`オプションを使って指定することもできます。

## サンプルスクリプト（簡易お絵かき）

```
title "TinyPaint"

old_x = -1
old_y = -1
now_x = 0
now_y = 0

repeat
    stick key
    if key & 256 {
        now_x = mousex
        now_y = mousey
        line now_x, now_y, old_x, old_y
        old_x = now_x
        old_y = now_y
    } else {
        old_x = mousex
        old_y = mousey
    }
    wait 5
loop

stop
```

## サンプルのスクリーンショット
![tinypaint](https://cloud.githubusercontent.com/assets/13228693/22679200/833b9b1e-ed43-11e6-80c2-94f5711863de.png)

---

[トップに戻る](https://github.com/dolphilia/tinyhsp)