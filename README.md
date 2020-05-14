
![demo](https://user-images.githubusercontent.com/50105514/81907526-dcfeab80-9602-11ea-8c8b-eb21e79de845.gif)

## 導入方法
OSはLinuxを想定している。Python3はすでにインストールしてあるとする。

1. PIL(GUI用モジュール)をインストールする
    + `pip install Pillow`
    + `sudo apt-get install python3-pil python3-pil.imagetk`
2. python-shogi(棋譜管理用モジュール)をインストールする
    + `sudo pip install python-shogi`
3. 将棋ソフトをダウンロードする
    + 実行ファイルのインストールは[やねうら王](https://github.com/yaneurao/YaneuraOu/tree/master/source)が適切だと思う。
        + 上記のリンク先を適当なところにダウンロードした後、 `/YaneuraOh/source`ディレクトリで[解説](https://github.com/yaneurao/YaneuraOu/blob/master/docs/%E8%A7%A3%E8%AA%AC.txt)にかかれているmakeコマンドを実行すると実行ファイルが生成される。
    + 評価関数は[水匠2](https://drive.google.com/file/d/12TWZI4Xs_-lgGnNtAWbVjh8vyOEw0qhB/view)などがよいだろう。
4. 将棋ソフトを適切な場所に置く
    + 将棋ソフトの実行ファイルを`gui.py`と同じディレクトリに置く。
        + もしやねうら王以外を使う場合は、`\config.py`の2行目を実行ファイルの名前と同じにする。
    + `gui.py`と同じディレクトリに`eval`ディレクトリを作成して、評価関数(`nn.bin`)をevalに入れる。

## 使用方法
`python3 gui.py`で実行