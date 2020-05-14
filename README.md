
![demo](https://user-images.githubusercontent.com/50105514/81907526-dcfeab80-9602-11ea-8c8b-eb21e79de845.gif)

# 導入方法
OSはLinux、Python3はインストールされているとする。

1. PIL(GUI用モジュール)をインストールする
    + `pip install Pillow`
    + `sudo apt-get install python3-pil python3-pil.imagetk`
2. python-shogi(棋譜管理用モジュール)をインストールする
    + `sudo pip install python-shogi`
3. 将棋ソフトをダウンロードする
    + 実行ファイルのインストールは[やねうら王](https://github.com/yaneurao/YaneuraOu/tree/master/source)を例にあげる
    + 上記のリンク先を適当なところにダウンロードした後、 `/YaneuraOh/source`ディレクトリで[解説](https://github.com/yaneurao/YaneuraOu/blob/master/docs/%E8%A7%A3%E8%AA%AC.txt)にかかれているmakeコマンドを実行すると実行ファイルが生成される
    + 評価関数は水匠2など
4. 将棋ソフトを適切な場所に置く
    + 将棋ソフトの実行ファイルをgui.pyと同じディレクトリに置く
    + (もしやねうら王以外を使う場合は、`\config.py`の2行目を実行ファイルの名前と同じにする)
    + 評価関数はevalフォルダに入れる