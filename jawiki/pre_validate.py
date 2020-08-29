import logging


class PreValidator:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def validate(self, title, kanji, yomi):
        for yomi_prefix in ['[[', 'いま、', 'あるいは', 'もしくは', '▢']:
            if yomi.startswith(yomi_prefix):
                self.logger.info(f'ignorable yomi prefix: {yomi_prefix}. ' +
                                 f'title={title}, kanji={kanji}, yomi={yomi}')
                return False

        for kanji_prefix in ['』', '[[']:
            if kanji.startswith(kanji_prefix):
                self.logger.info(f'ignorable kanji prefix: {kanji_prefix}.' +
                                 f'title={title}, kanji={kanji}, yomi={yomi}')
                return False

        # 「または」で始まるものは基本的に除外したほうがいいが、いくつかだけキャッチアップしよう。
        if yomi.startswith('または'):
            if len([1 for n in ['またはちろう', 'またはりひゃっかてん', 'またはり'] if yomi.startswith(n)]) == 0:
                self.logger.info(
                    f'ignorable yomi prefix: {yomi_prefix}. title={title}, kanji={kanji}, yomi={yomi}')
                return False

        if title in [
            # カッコ内に元になったマイクロンが入っているので無視。
            'トランスフォーマー ギャラクシーフォース',
            # 読み仮名が中途半端に入っている。古いアプリの情報なので一次情報をたどるのが難しくwikipedia川を修正するのが困難なので無視。
            'アイドル・ジェネレーション 第2次・萌えっ子大戦争!!',
            # ライトノベル独自用語
            'Dクラッカーズ',
        ]:
            self.logger.info(f'Title is in the blacklist. title={title}, kanji={kanji}, yomi={yomi}')
            return False

        return True
