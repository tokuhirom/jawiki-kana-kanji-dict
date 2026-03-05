# jawiki-kana-kanji-dict

Wikipedia日本語版から抽出したかな漢字辞書。

## 開発コマンド

- テスト: `uv run pytest`
- リント: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- 辞書生成: `uv run python3 bin/makedict.py /usr/share/skk/SKK-JISYO.L /usr/share/skk/SKK-JISYO.jinmei /usr/share/skk/SKK-JISYO.geo`

## 不正エントリの修正手順

辞書に不正なエントリを見つけた場合の対応手順:

1. **1件ごとに個別のPRにする** (複数の修正を1つのPRにまとめない)
2. エントリの原因を調査する (`dat/post_validated.tsv` や `SKK-JISYO.jawiki` を grep)
3. 修正方法を選択する:
   - **特定の読みが不正な場合**: `bin/makedict.py` の `IGNORE_YOMIS` に追加
   - **読みのパターンが不正な場合** (例: 「ー」始まり): `preproc` 関数にフィルタを追加
4. 辞書を再生成して確認: `uv run python3 bin/makedict.py ...`
5. テスト実行: `uv run ruff check . && uv run ruff format --check . && uv run pytest`
6. ブランチ名は `fix/` プレフィックスを使う
