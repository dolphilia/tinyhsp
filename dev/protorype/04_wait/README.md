[トップに戻る](https://github.com/dolphilia/tinyhsp)

---

# wait命令が使えるプロトタイプ

TinyHSPプロトタイプ4号です。wait命令が使えるようになりました。

## 実装

wait命令はGLFWの機能を使って実装しています。

- 実行ファイルと同じディレクトリにあるstart.hspを読み込みます
- 構文は改行方式です
    - １トークンにつき１行です
- print命令：文字列をコンソールに出力します
- pset命令：画面上にドットを描画します
- wait命令：10ミリ秒単位で処理を中断します
- エラー処理は省いています

## サンプル

```
print
Hello world!
pset
0
0
wait
100
pset
1
1
wait
100
pset
2
2
wait
100
pset
3
3
wait
100
pset
4
4
wait
100
pset
5
5
```

## 実行結果

スクリーンショットでは表現できませんが、１秒に１ドットずつを描画していきます。５ドット描画します。

---

[トップに戻る](https://github.com/dolphilia/tinyhsp)