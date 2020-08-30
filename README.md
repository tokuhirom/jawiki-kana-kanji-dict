# jawiki-kana-kanji-dict

## これは何？

wikipedia 日本語版のデータを元に、SKK/MeCab の辞書をつくるスクリプトです。

github actions で wikipedia から定期的にデータを取得して https://github.com/tokuhirom/skk-jisyo-jawiki/blob/master/SKK-JISYO.jawiki を、定期的に更新するようにしています。
(github actions を利用することで、メンテナが何もしなくても自動的に更新されることを期待しています。)

## Requirements

 * python 3.4+
    * jaconv
    * pytests
    * Levenshtein
    * janome
    * romkan
 * bunzip2
 * gnu make
 * gnu grep

## How to contribute

 * check.py に条件を追加します(これにより、デグレしづらくなります)
 * 手元で `make check` を実行して、実行失敗することを確認します。
 * `grep 対象ワード dat/*` として、対象のワードの状態をみます。
 * `user_simpledic.csv` か `jawiki/*.py` のルールを変更します

## どう動いているのか

`.github/workflows/python-app.yml` が github actions の定義ファイルです。これにより、定期的に辞書ファイルが再生成されます。

処理のフローは以下の通りです。試行錯誤/途中のステップのバグ発見しやすいように、複数ステップに分割されています。


![image](https://user-images.githubusercontent.com/21084/91639588-abdfa500-ea52-11ea-879e-dfb364627c4d.png)

 * `make` を実行すれば、一通りファイルが実行されます。
 * `make check` を実行すると、辞書ファイルを生成し、辞書ファイルの正当性を確認します。
 * `make test` を実行すると、テストスイートを実行します。

## LICENSE

Python scripts are:

    The MIT License (MIT)

    Copyright © 2020 Tokuhiro Matsuno, http://64p.org/ <tokuhirom@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the “Software”), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

Wikipedia license is: https://ja.wikipedia.org/wiki/Wikipedia:%E3%82%A6%E3%82%A3%E3%82%AD%E3%83%9A%E3%83%87%E3%82%A3%E3%82%A2%E3%82%92%E4%BA%8C%E6%AC%A1%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B
