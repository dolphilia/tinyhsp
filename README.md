# TinyHSP

TinyHSPは**最軽量のHSPを作成する**ことを目標にしたプロジェクトです。

## 更新履歴

- 2021-12-30 ＜M1 Mac＞動作を確認。Homebrewインストール説明の追記。EXTバージョンでの不具合あり。
- 2018-08-09 リポジトリを新しいアカウントに移動
- 2017-11-04 README.mdを更新
- 2017-07-08 README.mdを更新。デフォルトの解像度を640x480に戻す
- 2017-06-14 README.mdを更新
- 2017-05-24 v1.0.7をリリース。デフォルトの解像度を160x120に変更
- 2017-05-17 paint命令を実装
- 2017-04-29 v1.0.6をリリース。簡易的な音声ファイル系命令を追加
- 2017-04-14 macOSのRetinaモードに暫定対応
- 2017-04-10 v1.0.5をリリース。circle命令を追加（塗りつぶしのみ）。不具合を修正。
- 2017-04-07 v1.0.4をリリース
- 2017-04-06 v1.0.3をリリース
- 2017-04-04 リポジトリを整理。[プロトタイプを専用リポジトリに移動](https://github.com/dolphilia/tinyhsp-prototype)。v1.0.2をリリース
- 2017-04-03 wave命令を修正。v1.0.1をリリース
- 2017-04-01 TinyHSPのC言語に移植。v1.0.0をリリース
- 2017-03-31 neteruhspをC言語に移植
- 2017-02-10 プロジェクト完了
- 2017-02-09 neteruhspにGUIを実装する3
- 2017-02-08 neteruhspにGUIを実装する2
- 2017-02-07 neteruhspにGUIを実装する
- 2017-02-05 stb\_image.hを使って画像を描画する
- 2017-01-31 空白文字を考慮して文字列を描画する
- 2017-01-30 Unicode文字列を描画するプロトタイプ
- 2017-01-28 stb\_truetype.hを使って文字を描画するテスト／README.mdにイラストを追加
- 2017-01-27 wait命令が使えるプロトタイプ
- 2017-01-26 改行方式でpset命令も使えるプロトタイプ
- 2017-01-25 改行方式でprint命令のみ使えるプロトタイプ
- 2017-01-24 作り直しを始める／ヘッダー画像を追加／start.hspを読み込むだけのプロトタイプ
- 2017-01-23 作り直しを検討／これ以前のプログラムを1つのディレクトリにまとめた
- 2017-01-22 ディレクトリ構成を変更
- 2017-01-21 README.mdにイラストを追加
- 2017-01-18 パーサを修正
- 2017-01-17 テスト用のMakefileを作成
- 2017-01-16 パーサにテスト用コードを追加
- 2017-01-15 命令トークンを識別するように変更
- 2017-01-14 ピクセル操作のためのファイルを追加
- 2017-01-13 字句解析器を修正（長い関数を分割）
- 2017-01-12 ファイル読み込み用のユーティリティを追加
- 2017-01-11 ディレクトリ構成およびMakefileの変更
- 2017-01-10 字句解析器を修正／仕様を変更（wait命令を追加）
- 2017-01-09 電卓を実装（未対応：丸括弧・負の数）
- 2016-12-29 リポジトリを開設

## 仕様

TinyHSPの本体は`tinyhsp.c`のみで構成されており、ソースコードは5600行ほどです。ソースコードはC言語で書かれています。

TinyHSPはコンパイルフラグにより３通りのバイナリを作ることができます。

- `__HSPCUI__` : コンソール版
- `__HSPSTD__` : 標準版
- `__HSPEXT__` : 拡張版

[exrd / neteruhsp](https://github.com/exrd/neteruhsp)をベースにしており、文法や変数の規則などは基本的に同じです。ウィンドウの表示などGUI処理は[GLFW3](http://www.glfw.org)を使用しています。画像・フォント・OGGファイルの読み込みに[nothings / stb](https://github.com/nothings/stb)を使用しています。使用フォントは[M+ FONTS](http://mplus-fonts.osdn.jp)と[Mgen+](http://jikasei.me/font/mgenplus/)です。音声再生に[OpenAL](https://openal.org/)を使用しています。エラーメッセージの英文およびpoke命令・peek関数は[kikeroga3/tinyhsp](https://github.com/kikeroga3/tinyhsp)を使用しています。WAVファイルの読み込みに[mackron / dr_libs](https://github.com/mackron/dr_libs)を使用しています。

### 共通の追加命令・関数

３種類のバイナリで共通に追加した命令です。

|-|書式|説明|
|---|---|---|
|bload|bload p1, p2| p2で指定した変数にp1ファイルデータを読み込みます |
|poke|-|-|

３種類のバイナリで共通に追加した関数です。

|-|書式|説明|
|---|---|---|
|peek|-|-|
|powf|-|-|

### 標準版の命令

以下は標準版に追加した命令です。

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

以下は標準版で省かれる命令です。

- mes
- input

### 拡張版の命令

拡張版は標準版に加えて、以下の命令を追加しています。

|-|書式|説明|
|---|---|---|
|mes|mes p1|カレントポジションに文字列p1を画面に描画します。描画後にカレントポジションを文字サイズ分Y方向にずらします|
|font|font p1,p2,p3|フォントの設定をします。p1には使用するTTFファイルのパスを拡張子.ttfも含めて記述します。p2にはフォントサイズを指定します。フォントサイズは上限が100です。p3にはフォントのスムージングを行うか行わないかを指定します。0でスムージングを行わず、16でスムージングを行うように設定します|
|picload|picload p1|カレントポジションにp1で指定した画像を描画します。p1には使用する画像ファイルのパスの拡張子も含めて記述します|
|wave|wave p1,p2,p3,p4|特定の周波数で波形を再生します。p1は周波数、p2は再生する長さをミリ秒で、p3は波形の種類を、p4はボリュームを0～30000程度で指定します。|
|mmload|mmload p1|p1に拡張子を含めたファイルを指定する。拡張子は.wavか.oggを使用できる。p2はループ再生するかをしていする。0がループなしで1がループ再生。デフォルトは0。|
|mmplay|mmplay|mmloadで読み込んだファイルを再生する。mmloadで読み込んでいない場合はエラー。パラメーターはなし。|
|mmstop|mmstop|再生中の音声を停止する。パラメーターはなし。|


以下は拡張版で省かれる命令です。

- input

### 追加したシステム変数

|-|説明|
|---|---|
|strsize|bload命令の戻り値などに使用されます|
|mousex|マウスのx座標|
|mousey|マウスのy座標|
|mousel|マウスの左ボタンが押されていれば1、押されていなけば0|
|mouser|マウスの右ボタンが押されていれば1、押されていなけば0|

### その他の仕様

TinyHSPはスクリプトファイルの末尾まで実行したら、自動的に終了するようになっています。すぐにウィンドウを閉じないようにするためには、HSP2.xのようにソースの末尾にstopを書く必要があります。

## 開発環境の導入

標準版はOpenGLとGLFW3ライブラリを使用しています。拡張版ではそれに加えてOpenALライブラリを使用しています。導入する手順は以下の通りです。

### Windows(MinGW)の場合

MinGWにはOpenGLが最初から入っています。
MinGWにGLFW3を導入するには、次の手順で導入します。

1. **GLFWをダウンロードする**: **GLFWライブラリは[GLFWのダウンロードページ](http://www.glfw.org/download.html)から入手**します。GLFWには32bit版と64bit版があります。仮に32bit版をダウンロードしたとして話を進めます。
2. **include内のGLFWフォルダをMinGW内のincludeフォルダにコピーする**: ダウンロードしたフォルダの中に、`include` というフォルダが入っています。この中に `GLFW` というフォルダがあるので、その**GLFWフォルダをMinGWのincludeフォルダにコピー**します。
3. **2つの.aファイルをMinGW内のlibフォルダにコピーする**: ダウンロードしたフォルダの中に、`lib-mingw-w32` というフォルダが入っているので、この中にある、`libglfw3.a`、`libglfw3dll.a`という**2つの.aファイルをMinGWのlibフォルダにコピー**します。
4. **glfw3.dllをプロジェクトのフォルダにコピーする**: 上と同じ `lib-mingw-w32` フォルダ内に`glfw3.dll`というファイルがあるので、作成したいプロジェクト用のフォルダ内にコピーします。例えば、**glfw3.dllをtinyhsp.cがあるフォルダと同じ場所にコピー**します。

MinGWにOpenALを導入する方法は以下のとおりです。

1. [OpenALを入手](https://openal.org/downloads/)します。（OpenAL 1.1 Core SDK と OpenAL 1.1 Windows Installer）
2. 上記の２つのファイルを解凍、インストーラを実行してインストールします。
3. `C:\Program Files(x86)\OpenAL 1.1 SDK` にある `include` 内を `MinGW\include` にコピーします。
4. `C:\Program Files(x86)\OpenAL 1.1 SDK` にある `libs\Win32` 内を `MinGWlib` にコピーします。
5. `C:\Windows\SysWOW64OpenAL32.dll` を作業中のプロジェクトフォルダにコピーします。

※ フォルダ `Program Files(x86)` は `Program Files` かもしれません。また、`C:\Windows\System32` にも `OpenAL32.dll` がインストールされています。どちらを使用すべきなのかは、現状不明です。

#### Windows(VisualStudio)の場合

VisualStudioにOpenGLを設定する方法は以下のとおりです。

1. VisualStudioの「プロジェクト」メニューから「プロパティ」を選択します。
2. 「構成プロパティ」内の「リンカー」内の「入力」を選択します。
3. 「追加の依存ファイル」項目を編集して `opengl32.lib` を追加します。

VisualStudioにGLFW3を導入する手順は以下のとおりです。

1. VisualStudioの「プロジェクト」メニューから「NuGetパッケージの管理」をクリックします。
2. 「参照」をクリックして、検索ボックスに「glfw」と書いて検索します。
3. 検索結果から「glfw」を選択して、「インストール」ボタンをクリックします。

※ NuGetで入手するGLFW3は、2017年4月4日の時点でVisual Studio 2010, 2012, 2013, 2015に対応しています。

VisualStudioにOpenALを導入する方法は以下のとおりです。

1. [OpenALを入手](https://openal.org/downloads/)します。（OpenAL 1.1 Core SDK と OpenAL 1.1 Windows Installer）
2. 上記の２つのファイルを解凍、インストーラを実行してインストールします。
3. VisualStudioの「プロジェクト」メニューから「プロパティ」を選択します。
4. 「構成プロパティ」内の「VC++ ディレクトリ」を選択します。
5. 「インクルードディレクトリ」項目を編集して `C:\Program Files (x86)\OpenAL 1.1 SDK\include` を追加します。
6. 「ライブラリディレクトリ」項目を編集して `C:\Program Files (x86)\OpenAL 1.1 SDK\libs\Win32` を追加します。
7. 「構成プロパティ」内の「リンカー」内の「入力」を選択します。
8. 「追加の依存ファイル」項目を編集して `OpenAL32.lib` を追加します。

#### macOSの場合

macOSにはOpenGLが最初から入っています。またOpenALも最初から入っています。
macOSにGLFW3を導入する手順は以下のとおりです。

1. Homebrewを導入します。（[Homebrew](http://brew.sh/index_ja.html)のウェブサイトにあるスクリプトをターミナルに貼り付け実行してください）
2. ターミナルで `$ brew install glfw3` を実行します。

追記：m1 macの場合

m1 macの場合はHomebrewの指示通りに追加のコードを実行します。現時点では `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/ユーザー名/.zprofile` 及び `eval "$(/opt/homebrew/bin/brew shellenv)"` を実行する、となっています。

作者の環境ではインクルードパスとライブラリパスが通らなかったので、別途`export CPATH=$CPATH:/opt/homebrew/include` 及び `export LIBRARY_PATH=$LIBRARY_PATH:/opt/homebrew/lib`を実行してパスを通しました。

#### Linux（Ubuntu）の場合

GLFW3を導入する手順は以下のとおりです。

1. 端末で `sudo apt-get build-dep glfw3` を実行します。

あるいは、

1. 端末で `sudo apt-get install cmake xorg-dev libglu1-mesa-dev` を実行します。
2. 端末で次のコマンドを実行します。

```
$ git clone https://github.com/glfw/glfw.git
$ mkdir build
$ cd build/
$ cmake ..
$ make -j 8
$ sudo make install
```

OpenALを導入する手順は以下のとおりです。

1. 端末で、 `sudo apt-get install libopenal-dev` を実行します。

## TinyHSPソースコードの入手

当ページの右のほうにある「Clone or Download」ボタンを押して、現れた吹き出しの「Download ZIP」を選択すると入手できます。

![downloadzip](https://cloud.githubusercontent.com/assets/13228693/22812768/0e262fa8-ef8a-11e6-9a4d-93729a206f2a.png)

TinyHSP本体のソースコードは `_source` ディレクトリに入っています。

## コンパイル

`tinyhsp.c` の先頭には、コンパイルフラグのための記号定数が記述されてあります。

```c
#define __HSPCUI__
//#define __HSPSTD__
//#define __HSPEXT__
```

それぞれ `__HSPCUI__` がコンソール版、 `__HSPSTD__` が標準版、 `_HSPEXT__` が拡張版を表しています。**どれか１つをコメントアウトしてください**。

環境によりそれぞれ以下のようにコンパイルします。

※ `tinyhsp.c`の文字コードはUTF-8である必要があります。

### コンソール版のコンパイル

- MinGW: `$ gcc tinyhsp.c -o tinyhsp_cui`
- macOS: `$ clang tinyhsp.c -o tinyhsp_cui`
- Linux: `$ gcc tinyhsp.c -o tinyhsp_cui`

### 標準版のコンパイル

- MinGW: `$ gcc tinyhsp.c -o tinyhsp_std -lopengl32 -lglfw3dll -mwindows`
- macOS: `$ clang tinyhsp.c -o tinyhsp_std -lglfw -framework OpenGL`
- Linux: `$ gcc tinyhsp.c -o tinyhsp_std -lm -ldl -lglfw3 -lGL -lX11 -lXxf86vm -lXrandr -lXinerama -lXcursor -lpthread -lXi`

### 拡張版のコンパイル

- MinGW:
    - `$ gcc -c tinyhsp.c stb_vorbis.c`
    - `$ gcc tinyhsp.o stb_vorbis.o -o tinyhsp_ext -lopengl32 -lglfw3dll -lopenal32 -mwindows`
- macOS:
    - `$ clang -c tinyhsp.c stb_vorbis.c`
    - `$ clang tinyhsp.o stb_vorbis.o -o tinyhsp_ext -lglfw -framework OpenGL -framework OpenAL`
- Linux:
    - `$ gcc -c tinyhsp.c stb_vorbis.c`
    - `$ gcc tinyhsp.o stb_vorbis.o -o tinyhsp_ext -lm -ldl -lglfw3 -lGL -lX11 -lXxf86vm -lXrandr -lXinerama -lXcursor -lpthread -lXi -lopenal`

## macOSで静的ビルドする

clangを使用でき、GLFWをhomebrewでインストール済みの環境を想定しています。

1. GLFWを公式ウェブサイトからソースコードを入手する
2. CMakeが入っていなければ入れる `$ brew install cmake` あるいは `$ brew upgrade cmake`
3. TinyHSPをコンパイルする `clang tinyhsp.c -o tinyhsp -lglfw3 -framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo`

コンパイルオプションを `-lglfw ` とした場合はHomebrewでインストールしたGLFWの動的ライブラリが使用され、 `-lglfw3` とした場合はソースコードからインストールしたGLFWの静的ライブラリ `libglfw3.a` が使用されます。

### macOSの実行権限

macOSで静的ビルドしたバイナリを別なMacで動作させたい場合、パーミッション（実行権限）の設定が必要かもしれません。その場合には以下のように設定します。

`$ chmod 777 tinyhsp_std`

## 実行

`$ ./tinyhsp_cui` のようにコマンドラインのオプションに何も指定がない場合は、実行ファイルと同じディレクトリにある `start.hsp` を読み込んで実行します。

また `$ ./tinyhsp -f start.hsp` のように `-f` オプションを使って指定することもできます。

### サンプルスクリプト

標準版・拡張版で動作するお絵かきスクリプトです。

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

## リンク

- きっかけ
    - [TinyHSPの提案](http://hsp.tv/play/pforum.php?mode=all&num=77515)
- 使用しているライブラリ・フォント
    - [OpenAL](https://openal.org/)
    - [GLFW3](http://www.glfw.org)
    - [kikeroga3 / tinyhsp](https://github.com/kikeroga3/tinyhsp)
    - [exrd / neteruhsp](https://github.com/exrd/neteruhsp)
    - [nothings / stb](https://github.com/nothings/stb)
    - [mackron / dr_libs](https://github.com/mackron/dr_libs)
    - [M+ FONTS](http://mplus-fonts.osdn.jp)
    - [Mgen+](http://jikasei.me/font/mgenplus/)

## ライセンス

TinyHSPはMITライセンスです。
