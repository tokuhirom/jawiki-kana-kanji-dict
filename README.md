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

## knownn issues

### todo

- さんばーすと /GibsonLesPaulStandard1959HistoricCollection/
- おめが /冥王計画ゼオライマーΩ/闘神都市Ω/
- しょうぼうじ -> ['大梅拈華山円通正法寺', '太子山正法寺', '妙高山正法寺', '岩間山正法寺', '巌殿山正法寺', '徳迎山正法寺', '法寿山正法寺', '知見山正法寺', '石鈇山正法寺', '竹養山正法寺']
- いんすとぅるめんたる /DYINGROSES/OpenTheParade/ThemeofGenji/クロニック・ラヴ/バットマン/思い出さないで/約束の絆/記憶の図形/雨だれ/青空/
- さんてぃあーご -> ['アジャリス', 'アルテイショ', 'ア・カペーラ', 'ア・ペローシャ', 'オ・サンティアーゴ・ド・デアン・オウ・カステーロ', 'カルボス', 'パドロン', ]
- さい -> ['島ぜんぶでおーきな祭']
- きゅーぶ /CUBE/Q部!!/大切な者との記憶/
- ぼーこーどあるいはぼどーこーど /Baudotcode/
- あなたはぺとろ /"Tu es Petrus et super hanc petram aedificabo Ecclesiam"/
- しきもりよだゆう /10代式守与太夫/
- +あすーすいーぱっどとらんすふぉーまーてぃーえふいちまるいち /ASUS Eee Pad Transformer TF101/
- +あすーすいーぱっどとらんすふぉーまーぷらいむ /ASUS Eee Pad Transformer Prime TF201/
- +あすーすぱっど /ASUS Pad TF700T/
- あなたはぺとろ /"Tu es Petrus et super hanc petram aedificabo Ecclesiam"/
- あめりか /IPTP LLC/NO TOY GETS LEFT BEHIND/ベンジャミン/レコード・ワールド/一般的受容方式/
- あしたはすこしわらってみよう /ストーリーアルバム 『明日は少し笑ってみよう』/
- ごうめいりん /呉 メイリン（呉美鈴）/呉美鈴/
- いろこい /UH-1/
- けいようぎんこう /KEIYOGINKOGRANDCOUNTDOWNREAL/京葉銀行/
- あーけーどすてぃっく /本来はジョイスティック/


### waiting confirm

- さいとうのぶとし /斎藤 信利'/
  - wikipedia 側を修正した

### resolved

- あむすてるだむ /IPTP Limited/オランダのコーヒーショップ/
- こうりょうい /高 凌霨/
- ぼーなすとらっく /AllYouMiss/AnswertoThisFlower/CircleofLife/DreamingStar/Ican'tfollowyou/KeepInThePockets[Remix]/
- またはなき /7 - シチケン/
- ものくろ /MONOQLO/monokuro/第43話 - 第45話/
- いぷしろんでるたろんぽう /&epsilon;-&delta;論法/
- いけのたいらすのーぱーく /池の平スノーパーク（旧白樺リゾートスキー場）/
- がちりんだいし /月輪大師&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;/
- えむあんどえーそうごうけんきゅうじょ /M&amp;A総合研究所/
- いからしかおる /Keyboard/kAoruikArAshi/五十嵐馨/
- おかみまさみ /岡見正美&lt;refgroup=&quot;注&quot;&gt;『陸海軍将官人事総覧陸軍篇』42頁や『日本陸軍将官辞典』172頁では政美とあるが公文書では正美とある。&lt;/ref&gt;/
- あやせがわ /'綾瀬川/綾瀬川/
- あんままつさーじしあつし /あん摩マツサージ指圧師、はり師、きゆう師等に関する法律/
- あんばっく /{{lang|en|AMBAC}}/
- あんぼすぎーにょいっせい /安保&quot;Suginho&quot;一生/
- あんどろめだざおめがせい /アンドロメダ座&amp;omega;星/
- あんどろめだざふぁいせい /アンドロメダ座&amp;phi;星/
- KANJI:<<<ポンペイ、ヘルクラネウム及びトッレ・アンヌンツィアータの遺跡地域>>> YOMI:<<<ぽんぺい>>>                TITLE:<<<ポンペイ、ヘルクラネウム及びトッレ・アンヌンツィアータの遺跡地域>>>
- かいじょう /{{mvar|n}}の階乗/開成/
- うじょう /{{Vanchor|羽状}}/
- いとうすけのぶ /伊東彦兵衛尉藤原祐信（すけのぶ）伊東祐信/
- おかあさんといっしょ /佐藤弘道/坂田おさむ/
- しちへんげたぬきごてん /10.『七変化狸御殿』/
- どらむ /DAISUKE/DAVE/DUTTCH/GrantGerathy/HAYATO/HERA/HIRO/JxRxDx/KAZUO/KEIGO/KI-YAN/KOBA♥YOUNG/Kaz/Kentarou/MATSUMURA（Y.MATSUMURA）/MATTO/MI-CHAN/MasaoMiki/Masataka/
- ぎたー /8P/AYA/Aki/CAT/EBBY/EDDIE/GAK/GENTA/Goro Shimizu/HIROSHI/Hirohito Hirohashi/JJ/K5/KAZU-O/KEIKO/Kick/LARRY/LINA/MURAMOTO/MoCky/NAOKI/O.K.Z./OKUNO/Pegeot（ペジョ）/RAITA/RED/RICO/ROKU/SENSHO1500/SIN/Shoji Yokoi/TAKI/Takahiro Kido/The K(堀口馨)/Wata/YASU/YOSHIO/Yasuhiro Amano/Yasunori Yokomizo/アベチャン/アンディ・コックス/オオハシヒロユキ/オノチン/カズト/クロセノブヒロ/ゴロー/セイエイヨシムラ/タッチャメン/ダテ/トレイ・アザトース/ナカソカズオ/ピューク・アンド・スピット/フジタレイ/マコト/モモ/モモリン/ヨコ/ライト/レイジ/一輝/上中丈弥/中川暁生/仲原克彦/俊介/力武啓一/加藤昭彦/加藤智之/古城マサミ/和嶋慎治/大倉健/天佑（中村天佑）/天願ハジメ/守谷京子/小井手仁徳/小島翔/尾島秀紀/山中芳典/山田武郎/岡田志郎/日高コウセイ/春やん/智平/本間"RAT"章浩/東冬木/松居徹/松田健美/横山達郎/橘あつや/比賀江隆男/洪栄龍/渡邉美佳/発地伸夫/白井智廣/石橋光太郎/神田研司/福井利男/筒井朋哉/藤原貴志/豊島“ペリー来航”渉/近藤正樹/鎌田ジョージ/高杉大地/高橋大地/
- ただし /CSS等の保護技術を回避してのDVDのリッピングは私的複製の対象外となり違法行為となる/KS/MBSサタデーパーティー/ゲルググ/スネアを叩く時はハイハットを叩かない/ネコアルクにも当たる/ハイキッ
- しんこう -> ['キノミヤ信仰']
- あかね /AKANE/akane/明音/朱音/瀬野朱音/紅音/茜音/
- さっくす /朝本千可/柴田康平/石井淳/
- もしくは /ボルダー/N階マルコフ連鎖/{{ill2|モンジョワ、サン＝ドニ！|en|MontjoieSaintDenis!}}/
- おりんぴっくのらぐびーきょうぎ /オリンピックのラグビー競技/
- くらっしゅ /Krush/Scattorbrain/堕落/
- +いま /ベスト女優部門第1位/主演女優賞/伊麻/優秀主演女優賞/口頭性/
- しょくぎょうくんれんしどういん /職業訓練指導員/職業訓練指導員 (さく井科)/職業訓練指導員 (ほうろう製品科)/職業訓練指導員 (インテリア科)/職業訓練指導員 (ガラス科)/職業訓練指導員 (クレーン科

- かの /鹿野町(山口県)/
- ぐりん /夏でSUKA?/
- きむらひろし /木村 浩 (ロシア文学者)/木村寛/木村広/木村弘/木村汎/木村浩/木村碩志/木村裕主/
- あおやませいずせんもんがっこう /・青山製図専門学校/
- くどみなら /・久富 奈良/
- にほんのびじゅつがっこう /日本の美術学校 (近代期)/
- あぷり /じぶん通帳/世紀末麻雀伝説北斗/北斗の拳 〜世紀末麻雀伝説〜/北斗の拳GPS/北斗の拳〜世紀末覇者麻雀バトル〜/北斗の拳スマートショック/北斗の拳早拳伝/
- あいどんとらいくまんでいず /IDon'tLikeMondays./
- えっくす /400X/EX/○ごとX/
- おーすとらりあ /（英語）/
- さん /ぴろし3/天井/
- あべもとひさ /阿部 元壽 （元寿）/
- なんばーず /Numbers/
- にほんのがっこうせいどのへんせん /日本の学校制度の変遷/
- きゃっつ /CATS, Cats/
