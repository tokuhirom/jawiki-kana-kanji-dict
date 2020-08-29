# 処理の流れ

* wget
* 基本的な抜き出し処理
* 除外フィルタ
* ソート
* SKK-JISYO.L にあるものを除外
* euc-jp 版辞書の書き出し

TODO: KKC に utf-8 辞書をよむ能力あるか確認

## Requirements

 * python 3.4+
    * jaconv
    * pytests
    * Levenshtein
 * bunzip2
 * gnu make
 * gnu grep

## How to contribute

 * 余計な単語が登録されている場合
   * check.py に除外条件を追加する(これにより、デグレしづらくなります)
   * jawiki/*.py のルールを変更します

## どう動いているのか

`.github/workflows/python-app.yml` が github actions の定義ファイルです。これにより、定期的に辞書ファイルが再生成されます。

処理のフローは以下の通りです。試行錯誤/途中のステップのバグ発見しやすいように、複数ステップに分割されています。


![image](https://user-images.githubusercontent.com/21084/91639588-abdfa500-ea52-11ea-879e-dfb364627c4d.png)

 * `make` を実行すれば、一通りファイルが実行されます。
 * `make check` を実行すると、辞書ファイルを生成し、辞書ファイルの正当性を確認します。
 * `make test` を実行すると、テストスイートを実行します。
