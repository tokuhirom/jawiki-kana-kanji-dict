import re

# https://note.nkmk.me/python-re-regex-character-type/
HIRAGANA_BLOCK = r'\u3041-\u309Fー'

# https://www.ncbi.nlm.nih.gov/staff/beck/charents/unicode/30A0-30FF.html
# 30FB  ・ は除外。
KATAKANA_BLOCK = r'\u30A1-\u30FA\u30FC-\u30FFー'

KANJI_BLOCK = r'\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF'
# KANJI_BLOCK = r'\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u21000-\u213FF\U00020000-\U0002EBEF'

HIRAGANA_PATTERN = re.compile(r'^[' + HIRAGANA_BLOCK + ']+$')
KATAKANA_PATTERN = re.compile(r'^[' + KATAKANA_BLOCK + ']+$')
KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN = re.compile(r'^[ 　' + KATAKANA_BLOCK + HIRAGANA_BLOCK + '・]+$')
KANJI_PATTERN = re.compile(r'^[' + KANJI_BLOCK + ']+$')

KANJI_NORMALIZER = str.maketrans('亞惡壓圍爲醫壹稻飮隱營榮衞驛悅閱圓緣艷鹽奧應橫歐毆黃溫穩假價畫會囘壞懷繪槪擴殼覺學嶽樂渴鐮勸卷寬歡罐觀閒關陷巖顏歸氣龜僞戲犧卻糺舊據擧虛峽挾敎强狹鄕堯曉區驅勳薰羣徑惠揭攜溪經繼莖螢輕鷄藝擊缺儉劍圈檢權獻縣硏險顯驗嚴吳娛效廣恆鑛號國黑歲濟碎齋劑冱櫻册雜產參慘棧蠶贊殘絲姊齒兒辭濕實舍寫釋壽收從澁獸縱肅處緖敍尙奬將牀涉燒稱證乘剩壤孃條淨狀疊穰讓釀囑觸寢愼晉眞刄盡圖粹醉隨髓數樞瀨淸靑聲靜齊稅蹟說攝竊絕專戰淺潛纖踐錢禪曾瘦雙遲壯搜插巢爭窗總聰莊裝騷增臟藏卽屬續墮體對帶滯臺瀧擇澤單擔膽團彈斷癡晝蟲鑄廳徵聽敕鎭脫遞鐵轉點傳黨盜燈當鬭德獨讀屆繩貳姙黏惱腦霸廢拜賣麥發髮拔晚蠻祕彥姬濱甁拂佛倂竝變邊辨瓣辯舖步穗寶萠襃豐沒飜槇每萬滿麵默餠歷戀戾彌藥譯豫餘與譽搖樣謠遙瑤慾來賴亂覽畧龍兩獵綠鄰凜壘淚勵禮隸靈齡曆鍊爐勞樓郞祿錄亙灣', '亜悪圧囲為医壱稲飲隠営栄衛駅悦閲円縁艶塩奥応横欧殴黄温穏仮価画会回壊懐絵概拡殻覚学岳楽渇鎌勧巻寛歓缶観間関陥巌顔帰気亀偽戯犠却糾旧拠挙虚峡挟教強狭郷尭暁区駆勲薫群径恵掲携渓経継茎蛍軽鶏芸撃欠倹剣圏検権献県研険顕験厳呉娯効広恒鉱号国黒歳済砕斎剤冴桜冊雑産参惨桟蚕賛残糸姉歯児辞湿実舎写釈寿収従渋獣縦粛処緒叙尚奨将床渉焼称証乗剰壌嬢条浄状畳穣譲醸嘱触寝慎晋真刃尽図粋酔随髄数枢瀬清青声静斉税跡説摂窃絶専戦浅潜繊践銭禅曽双痩遅壮捜挿巣争窓総聡荘装騒増臓蔵即属続堕体対帯滞台滝択沢単担胆団弾断痴昼虫鋳庁徴聴勅鎮脱逓鉄転点伝党盗灯当闘徳独読届縄弐妊粘悩脳覇廃拝売麦発髪抜晩蛮秘彦姫浜瓶払仏併並変辺弁弁弁舗歩穂宝萌褒豊没翻槙毎万満麺黙餅歴恋戻弥薬訳予余与誉揺様謡遥瑶欲来頼乱覧略竜両猟緑隣凛塁涙励礼隷霊齢暦錬炉労楼郎禄録亘湾')

# 新字 → 旧字
def kanji_normalize(s):
    return s.translate(KANJI_NORMALIZER)

def is_katakana_or_hiragana_or_nakaguro_or_space(s):
    if KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN.match(s):
        return True
    else:
        return False

def is_hiragana(s):
    if HIRAGANA_PATTERN.match(s):
        return True
    else:
        return False

def is_katakana(s):
    if KATAKANA_PATTERN.match(s):
        return True
    else:
        return False

def is_kanji(s):
    if KANJI_PATTERN.match(s):
        return True
    else:
        return False

