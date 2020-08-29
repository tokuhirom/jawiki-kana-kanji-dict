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
  * check.py に除外条件を追加する(これにより、)
