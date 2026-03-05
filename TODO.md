# TODO: コード品質改善

## バグ修正

- [ ] `jawiki/file_processor.py:43` リスト走査中の `remove()` によるスキップバグ修正
- [ ] `jawiki/romkan.py:429,469` `_kanpat_cmp` の比較対象が同じ変数になっているバグ修正
- [ ] `jawiki/pre_validate.py:26` ログメッセージの `yomi_prefix` 参照が不正確
- [ ] `jawiki/post_validate.py:105` エラーメッセージ `<2` → `>=20` の修正
- [ ] `bin/scanner.py:30-31` 令和のデバッグ print 除去

## パフォーマンス改善

- [ ] `jawiki/converter.py` `yomi_filter` 内の regex プリコンパイル
- [ ] `jawiki/scanner.py:7` 文字列結合を list + join に変更
- [ ] `jawiki/jachars.py` 等のインライン regex プリコンパイル

## コードスタイル

- [ ] `jawiki/romkan.py` Python 2 互換コード除去 (`__future__`, `cmp_to_key` フォールバック等)
- [ ] `jawiki/post_validate.py` 名前マングリング `__method` → `_method` に統一
- [ ] `jawiki/jachars.py` `if match: return True else: return False` → `return bool(match)`
- [ ] `bin/makedict.py` `set([...])` → set リテラル、`IGNORE_YOMIS` 重複除去

## 安全性

- [ ] `jawiki/post_validate.py:210` `re.sub` でユーザ由来テキストをパターンに使用 → `str.replace()` に変更
