[トップに戻る](https://github.com/dolphilia/tinyhsp)

---

# 改行方式でpset命令も使える

TinyHSPプロトタイプ3号です。実用性はありません。

## 実装

- 実行ファイルと同じディレクトリにあるstart.hspを読み込みます
- 構文は改行方式です
    - １トークンにつき１行です
- print命令：文字列をコンソールに出力します
- pset命令：画面上にドットを描画します
- エラー処理は省いています

## サンプル

```
print
Hello world!
pset
0
0
pset
1
1
pset
2
2
pset
3
3
pset
4
4
pset
5
5
pset
6
6
pset
7
7
pset
8
8
pset
9
9
pset
10
10
```
## 実行結果

![v003](https://cloud.githubusercontent.com/assets/13228693/22358842/db6dab72-e485-11e6-980a-b0ef1f56db42.png)

---

[トップに戻る](https://github.com/dolphilia/tinyhsp)
