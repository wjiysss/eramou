# eraMaouEx Python Implementation
# An ERB interpreter and game implementation for eraMaouEx

# Game version
VERSION = "0.92 Ex 2.1"
VERSION_NAME = "Python Edition"

import re
import os
import sys
import json
import csv
import pickle
import random
import math
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from collections import defaultdict

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except:
        pass

GODNESS_EVENT_LINES = {
    110: [
        "半梦半醒之间，你感觉到有人偷偷潜入房间，轻手轻脚爬上了床。",
        "睁眼之后映入视野的，正是嘉德那带着坏笑的美丽脸庞。",
        "她一边侍奉着你，一边像宣示主权般说会把你一滴不剩地榨干，免得你去祸害其他人。",
        "如今的她，显然已经和最初那个高贵决绝的身影判若两人。",
    ],
    120: [
        "你偶然撞见嘉德正在和兽人们展开淫乱到极致的群交。",
        "如今的她早已不像曾经那样高贵圣洁，脑海里只剩下对肉棒与快感的渴望。",
        "不论你是亲自加入还是冷眼旁观，最终她都会在欲望中被彻底推向更深处。",
        "嘉德越来越像一头被情欲支配的淫兽了。",
    ],
    130: [
        "回到房间时，你发现被子里竟然藏着赤裸的嘉德。",
        "她抱着你的枕头、闻着你的气息偷偷自慰，被抓个正着后反而露出了强烈的渴望。",
        "在她毫不掩饰地向你索求之后，你也顺势让她在床上彻底迎来了满足。",
        "嘉德对你的依赖，显然已经深入到了连呼吸都离不开的程度。",
    ],
    140: [
        "调教结束后，嘉德少见地主动在你门口等你。",
        "她贴在你背上，直白地承认自己已经一天不被你欺负就会饥渴难耐。",
        "而她那副一边口交一边把你的精液一点不剩吞下的模样，也再次证明了这话半点不假。",
        "对现在的嘉德来说，夜晚显然才刚刚开始。",
    ],
    150: [
        "「呐，魔王大人，那个老头子死了哟。」",
        "嘉德告诉你，曾把她献给魔王的旧天神已经死去，而她这个候选人打算亲自回天界去争那个位子。",
        "你刚意识到不妙，她就爆发出庞大的魔力把你震开，趁乱冲出了地下城。",
        "即使你立刻派出部下追截，最终也还是没能把她拦下。",
        "魔物损失近半，金库也在混乱中被毁去了一角，奴隶们或多或少都受了些伤。",
    ],
    160: [
        "当你突破层层包围攻入天界广场时，首先看到的就是遍体鳞伤、被六名审判者围在中央的嘉德。",
        "你指挥魔物军团扑向天界十字军，自己则亲手杀入包围圈，来到那个满身鲜血却依旧嘴硬的天使身边。",
        "嘉德喘息着嘲笑自己的狼狈，而你拔出魔剑直指剩下的审判者。",
        "战斗，从这一刻起彻底爆发了。",
    ],
    170: [
        "把天界暂时交给嘉德打理后过了一段时间，你心血来潮去视察她这个新任天界之主。",
        "推门时，她正端坐在办公桌前处理堆积如山的公文，身边还有一位天使少女帮忙整理文件。",
        "可等助手退下之后，这位看似知书达理的新天神很快又被你按在办公桌上狠狠干到失神。",
        "即使坐上了位子，嘉德骨子里也依旧是那个会因你的侵犯而彻底发情的淫乱天使。",
    ],
    180: [
        "某天来到地下城的嘉德忽然从背后蒙住你的眼睛，带着一贯恶作剧般的语调让你猜她是谁。",
        "在你把她搂进怀里之后，她忽然认真起来，说和你相识相恋已经过了很长时间。",
        "于是她神秘兮兮地宣布，等到一周年时要送你一份特别的礼物。",
        "至于那份礼物究竟是什么，她只肯笑着说现在还要保密。",
    ],
    190: [
        "天界某个房间里，嘉德把自己的助手安吉尔剥得一丝不挂，按在床上细细欣赏。",
        "那个偷看过你们宣淫的天使少女，在嘉德的威压、挑逗与手指开发下很快被逼到第一次高潮。",
        "嘉德一边审问她曾否自慰，一边像对待猎物一样享受她的羞耻与颤抖。",
        "到最后，安吉尔已经被调教成了一个连自己都不知该如何面对欲望的坏孩子。",
    ],
    200: [
        "约定的日子到了，嘉德穿着若隐若现的轻纱在房间里等你，还先把一把金色小钥匙塞进了你手中。",
        "随后她带你去见所谓的礼物: 那个同样披着轻纱、戴着贞操带、满脸羞红的助手安吉尔。",
        "嘉德把她作为一周年礼物献给你，而你也当着嘉德的面亲手解开贞操带，占有了这个被她调教好的天使少女。",
        "后来你与嘉德、安吉尔三人沉溺在漫长的白日宣淫中，而嘉德也作为淫乱的天界之主彻底坐稳了自己的位子。",
        "～嘉德 淫乱天神 Ending～",
    ],
    540: [
        "嘉德逃回天界后，迎接她的并不是鲜花和掌声，而是天界评议会与十二审判者设下的围杀。",
        "与此同时，你也彻底整合了自己的部队，带着怒火下令全军出击，目标直指天神宫。",
        "从这一刻起，天神宫终于成为了可以直接侵略的战场。",
    ],
}

DRESS_MAIN_CLOTH_NAMES = {
    0: "未穿外衣",
    1: "日常着装·裙子",
    101: "日常着装·裤子",
    2: "护胸＆裙甲",
    22: "童装",
    3: "锁甲",
    4: "皮甲＆裙甲",
    108: "护胸＆短裤式护甲",
    207: "神官服",
    111: "胸甲＆南瓜裙",
    206: "长袍",
    131: "睡衣",
    201: "连衣裙",
    110: "忍者装",
    203: "妓女装",
    104: "巫女装",
    205: "孕妇装",
    251: "紧身装甲",
    254: "兔女郎装",
    5: "紧身服＆裙甲",
    6: "胸甲＆裙子",
    7: "尖刺铠＆裙子",
    209: "女仆装",
    103: "冒险装",
    105: "骑士铠",
    253: "混沌护甲",
    292: "贴身甲",
    193: "比基尼铠甲",
    194: "性感内衣",
    195: "梦魔式比基尼",
    294: "恶魔紧身衣",
    241: "拘束衣",
    213: "挂满避孕套的圣女服",
    113: "冒险服＆丁字裤",
    8: "乳贴＆迷你短裙铠甲",
    9: "胸甲＆透视裙子",
    114: "袒胸露乳的巫女装",
    115: "暴露的女忍者装",
    116: "胸甲＆丁字裤",
    210: "挂满避孕套的妓女服装",
    211: "淫荡暴露的神官服",
    212: "露出乳头与私处的紧身衣",
    295: "连身泳装",
    196: "分体泳装",
    214: "旗袍",
    17: "高中制服",
    18: "初中制服",
    19: "水手服",
    20: "私立贵族学院制服",
    21: "西装",
    204: "浴衣",
    23: "名牌服装",
    24: "护士服",
    25: "女性用军服",
    26: "女侍制服",
    27: "便利店制服",
    28: "事务员制服",
    29: "岛屿女孩服装",
    30: "演出服",
    31: "运动服",
    32: "丧服",
    33: "拉拉队服",
    34: "网球服",
    35: "女警服",
    102: "狩衣",
    106: "军服",
    109: "体操服",
    112: "骑马服",
    120: "滑雪服",
    202: "和服",
    208: "晚礼服",
    221: "幼稚园服",
    240: "婚礼裙装",
}

DRESS_ACCESSORY_NAMES = {
    0: "未佩戴饰品",
    1: "围裙",
    2: "外套",
    3: "白衣",
    4: "男装衬衣",
    10: "朴素的背心",
    12: "斗篷",
    13: "长袍",
    52: "护额",
    53: "护士帽",
    54: "女警帽",
    55: "牛仔帽",
    56: "土著帽子",
    57: "腕带",
    58: "串珠手镯",
    59: "长手套",
    60: "阶级章",
    61: "名牌",
    62: "蝴蝶结",
    63: "银手镯",
    64: "护身符",
    65: "拉拉队彩球",
    69: "尿布",
    71: "狗项圈",
    72: "龟甲缚用的绳子",
    73: "牛铃和鼻环",
    74: "手枷",
    75: "足枷",
    76: "首枷",
    77: "涂鸦",
    78: "魔法纹身",
    79: "贞操带",
    80: "绳子印",
    81: "头饰",
    82: "发饰",
    83: "眼镜",
    84: "墨镜",
    87: "银吊坠",
    88: "珍珠项链",
    89: "勾玉项链",
    90: "项链",
    91: "头环",
    92: "戒指",
    98: "神秘的尿道导管",
}

DRESS_ACCESSORY_DEFINITIONS = [
    {"menu_id": 1, "cloth_id": 1, "name": "围裙", "cost": 10000},
    {"menu_id": 2, "cloth_id": 2, "name": "外套", "cost": 10000},
    {"menu_id": 3, "cloth_id": 3, "name": "白衣", "cost": 10000},
    {"menu_id": 4, "cloth_id": 4, "name": "男装衬衣", "cost": 10000},
    {"menu_id": 5, "cloth_id": 10, "name": "朴素的背心", "cost": 10000},
    {"menu_id": 6, "cloth_id": 12, "name": "斗篷", "cost": 10000},
    {"menu_id": 7, "cloth_id": 81, "name": "头饰", "cost": 10000},
    {"menu_id": 8, "cloth_id": 52, "name": "护额", "cost": 10000},
    {"menu_id": 9, "cloth_id": 53, "name": "护士帽", "cost": 10000},
    {"menu_id": 10, "cloth_id": 54, "name": "女警帽", "cost": 10000},
    {"menu_id": 11, "cloth_id": 55, "name": "牛仔帽", "cost": 10000},
    {"menu_id": 12, "cloth_id": 56, "name": "土著帽子", "cost": 10000},
    {"menu_id": 13, "cloth_id": 82, "name": "发饰", "cost": 10000},
    {"menu_id": 14, "cloth_id": 83, "name": "眼镜", "cost": 10000},
    {"menu_id": 15, "cloth_id": 84, "name": "墨镜", "cost": 10000},
    {"menu_id": 16, "cloth_id": 87, "name": "银吊坠", "cost": 10000},
    {"menu_id": 17, "cloth_id": 88, "name": "珍珠项链", "cost": 10000},
    {"menu_id": 18, "cloth_id": 89, "name": "勾玉项链", "cost": 10000},
    {"menu_id": 19, "cloth_id": 60, "name": "阶级章", "cost": 10000},
    {"menu_id": 20, "cloth_id": 61, "name": "名牌", "cost": 10000},
    {"menu_id": 21, "cloth_id": 90, "name": "项链", "cost": 10000},
    {"menu_id": 22, "cloth_id": 62, "name": "蝴蝶结", "cost": 10000},
    {"menu_id": 23, "cloth_id": 63, "name": "银手镯", "cost": 10000},
    {"menu_id": 24, "cloth_id": 64, "name": "护身符", "cost": 10000},
    {"menu_id": 25, "cloth_id": 65, "name": "拉拉队彩球", "cost": 10000},
    {"menu_id": 26, "cloth_id": 57, "name": "腕带", "cost": 10000},
    {"menu_id": 27, "cloth_id": 58, "name": "串珠手镯", "cost": 10000},
    {"menu_id": 28, "cloth_id": 59, "name": "长手套", "cost": 10000},
    {"menu_id": 29, "cloth_id": 71, "name": "狗项圈", "cost": 10000},
    {"menu_id": 30, "cloth_id": 72, "name": "龟甲缚用的绳子", "cost": 10000},
    {"menu_id": 31, "cloth_id": 73, "name": "牛铃和鼻环", "cost": 10000},
    {"menu_id": 32, "cloth_id": 74, "name": "手枷", "cost": 10000},
    {"menu_id": 33, "cloth_id": 75, "name": "足枷", "cost": 10000},
    {"menu_id": 34, "cloth_id": 76, "name": "首枷", "cost": 10000},
    {"menu_id": 35, "cloth_id": 77, "name": "涂鸦", "cost": 100},
    {"menu_id": 36, "cloth_id": 80, "name": "绳子印", "cost": 100},
    {"menu_id": 37, "cloth_id": 78, "name": "魔法纹身", "cost": 500},
    {"menu_id": 38, "cloth_id": 69, "name": "尿布", "cost": 100},
    {"menu_id": 39, "cloth_id": 79, "name": "贞操带", "cost": 100},
    {"menu_id": 40, "cloth_id": 13, "name": "长袍", "cost": 10000},
    {"menu_id": 41, "cloth_id": 91, "name": "头环", "cost": 10000},
    {"menu_id": 42, "cloth_id": 92, "name": "戒指", "cost": 100000},
    {"menu_id": 43, "cloth_id": 98, "name": "神秘的尿道导管", "cost": 3000},
]

DRESS_NORMAL_OPTIONS = [
    {"menu_id": 1, "slot": "main", "name": "护胸＆裙甲", "cloth_id": 2, "cost": 1000, "req": 0},
    {"menu_id": 2, "slot": "main", "name": "童装", "cloth_id": 22, "cost": 1000, "req": 5},
    {"menu_id": 3, "slot": "main", "name": "锁甲", "cloth_id": 3, "cost": 1000, "req": 0},
    {"menu_id": 4, "slot": "main", "name": "皮甲＆裙甲", "cloth_id": 4, "cost": 1000, "req": 0},
    {"menu_id": 5, "slot": "main", "name": "护胸＆短裤式护甲", "cloth_id": 108, "cost": 1000, "req": 0},
    {"menu_id": 6, "slot": "main", "name": "神官服", "cloth_id": 207, "cost": 1000, "req": 0},
    {"menu_id": 7, "slot": "main", "name": "胸甲＆南瓜裙", "cloth_id": 111, "cost": 1000, "req": 0},
    {"menu_id": 8, "slot": "main", "name": "长袍", "cloth_id": 206, "cost": 1000, "req": 3},
    {"menu_id": 9, "slot": "main", "name": "睡衣", "cloth_id": 131, "cost": 1000, "req": 0},
    {"menu_id": 10, "slot": "main", "name": "连衣裙", "cloth_id": 201, "cost": 1000, "req": 0},
    {"menu_id": 11, "slot": "main", "name": "忍者装", "cloth_id": 110, "cost": 1000, "req": 0},
    {"menu_id": 12, "slot": "main", "name": "妓女装", "cloth_id": 203, "cost": 1000, "req": 1},
    {"menu_id": 13, "slot": "main", "name": "巫女装", "cloth_id": 104, "cost": 1000, "req": 0},
    {"menu_id": 14, "slot": "main", "name": "孕妇装", "cloth_id": 205, "cost": 1000, "req": 4},
    {"menu_id": 15, "slot": "main", "name": "紧身装甲", "cloth_id": 251, "cost": 1000, "req": 0},
    {"menu_id": 16, "slot": "main", "name": "兔女郎装", "cloth_id": 254, "cost": 1000, "req": 3},
    {"menu_id": 17, "slot": "main", "name": "紧身服＆裙甲", "cloth_id": 5, "cost": 1000, "req": 0},
    {"menu_id": 18, "slot": "main", "name": "胸甲＆裙子", "cloth_id": 6, "cost": 1000, "req": 0},
    {"menu_id": 19, "slot": "main", "name": "尖刺铠＆裙子", "cloth_id": 7, "cost": 1000, "req": 2},
    {"menu_id": 20, "slot": "main", "name": "女仆装", "cloth_id": 209, "cost": 1000, "req": 0},
    {"menu_id": 21, "slot": "main", "name": "冒险装", "cloth_id": 103, "cost": 1000, "req": 0},
    {"menu_id": 22, "slot": "main", "name": "骑士铠", "cloth_id": 105, "cost": 1000, "req": 0},
    {"menu_id": 23, "slot": "main", "name": "混沌护甲", "cloth_id": 253, "cost": 1000, "req": 3},
    {"menu_id": 24, "slot": "main", "name": "贴身甲", "cloth_id": 292, "cost": 1000, "req": 0},
    {"menu_id": 25, "slot": "main", "name": "比基尼铠甲", "cloth_id": 193, "cost": 1000, "req": 0},
    {"menu_id": 26, "slot": "main", "name": "性感内衣", "cloth_id": 194, "cost": 1000, "req": 3},
    {"menu_id": 27, "slot": "main", "name": "梦魔式比基尼", "cloth_id": 195, "cost": 1000, "req": 3},
    {"menu_id": 28, "slot": "main", "name": "恶魔紧身衣", "cloth_id": 294, "cost": 1000, "req": 3},
    {"menu_id": 29, "slot": "main", "name": "拘束衣", "cloth_id": 241, "cost": 1000, "req": 3},
    {"menu_id": 30, "slot": "main", "name": "挂满避孕套的圣女服", "cloth_id": 213, "cost": 1000, "req": 3},
    {"menu_id": 31, "slot": "main", "name": "冒险服＆丁字裤", "cloth_id": 113, "cost": 1000, "req": 3},
    {"menu_id": 32, "slot": "main", "name": "乳贴＆迷你短裙铠甲", "cloth_id": 8, "cost": 1000, "req": 3},
    {"menu_id": 33, "slot": "main", "name": "胸甲＆透视裙子", "cloth_id": 9, "cost": 1000, "req": 3},
    {"menu_id": 34, "slot": "main", "name": "袒胸露乳的巫女装", "cloth_id": 114, "cost": 1000, "req": 3},
    {"menu_id": 35, "slot": "main", "name": "暴露的女忍者装", "cloth_id": 115, "cost": 1000, "req": 3},
    {"menu_id": 36, "slot": "main", "name": "胸甲＆丁字裤", "cloth_id": 116, "cost": 1000, "req": 3},
    {"menu_id": 37, "slot": "main", "name": "挂满避孕套的妓女服装", "cloth_id": 210, "cost": 1000, "req": 3},
    {"menu_id": 38, "slot": "main", "name": "淫荡暴露的神官服", "cloth_id": 211, "cost": 1000, "req": 3},
    {"menu_id": 39, "slot": "main", "name": "露出乳头与私处的紧身衣", "cloth_id": 212, "cost": 1000, "req": 3},
    {"menu_id": 40, "slot": "main", "name": "连身泳装", "cloth_id": 295, "cost": 1000, "req": 1},
    {"menu_id": 41, "slot": "main", "name": "分体泳装", "cloth_id": 196, "cost": 1000, "req": 1},
    {"menu_id": 42, "slot": "main", "name": "旗袍", "cloth_id": 214, "cost": 1000, "req": 0},
    {"menu_id": 996, "slot": "submenu", "name": "服装黑市", "cloth_id": 0, "cost": 0, "req": 0},
]

ERB_ANALYSIS_KEY_TERMS = {
    "TITLE": "Title screen",
    "SHOP": "Shop system",
    "TRAIN": "Training system",
    "ABLUP": "Ability upgrade",
    "ITEM": "Item system",
    "EQUIP": "Equipment",
    "PALAM": "Parameter system",
    "MARK": "Mark system",
    "SOURCE": "Source system",
    "CHAR": "Character system",
    "SAVE": "Save/Load",
    "TIME": "Time system",
    "DAY": "Day system",
    "DUNGEON": "Dungeon",
    "FLAG": "Flag system",
}

SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES = {
    75: {
        3: f"{{name}} 被稀奇的异种收藏家高价买走，成了专门繁殖与取乐的珍贵活体藏品。",
        2: f"{{name}} 被当成珍稀异种玩物收藏起来，身体被不断拿去做各种下流试验。",
        1: f"{{name}} 被卖给了好奇心旺盛的异族饲主，日夜都在陌生的欲望里挣扎。",
        0: f"{{name}} 被当成稀奇货色低价甩卖，从此过上了被反复转手的生活。",
    },
    76: {
        3: f"{{name}} 被高价转卖后，似乎作为某位强大魔族的专属玩物活了下去。",
        2: f"{{name}} 被当作珍贵的玩赏奴隶收藏起来，过着被人反复享用的生活。",
        1: f"{{name}} 被送进了娼馆，很快就学会了如何迎合各式各样的客人。",
        0: f"{{name}} 被廉价卖给了奴隶主，往后的人生大概只剩下无穷无尽的侵犯。",
    },
    85: {
        3: f"{{name}} 被卖给了位高权重之人，听说后来彻底沦为了不见天日的私宠。",
        2: f"{{name}} 被卖给了富有的魔族，尊严早已在一次次展示与玩弄中消失殆尽。",
        1: f"{{name}} 被送进了娼馆，幼小的身体很快就被训练成了招揽客人的商品。",
        0: f"{{name}} 被卖去做杂役与性奴，往后的生活只剩下忍耐与哭泣。",
    },
}

SELL_FOLLOWUP_KOJO_119_TIER_LINES = {
    76: {
        3: "就这样，她被卖给了魔族的大将，作为宠姬沉溺在永无止尽的欢愉之中。",
        2: "就这样，她被卖给了魔界的艺术家，既作为模特也作为床上的玩物被反复使用。",
        1: "就这样，她被卖给了魔王城的娼馆，很快就成了最受欢迎的商品之一。",
        0: "就这样，她被卖给了奴隶主，夜夜都作为泄欲工具被轮流使用。",
    },
    85: {
        3: "就这样，她被卖给了当政的人类国王，听说后来彻底沦为了不见天日的玩物。",
        2: "就这样，她被卖给了魔族富豪，尊严在一次次展示与玩弄中被彻底碾碎。",
        1: "就这样，她被卖给了魔王城的娼馆，幼小的身体成了最受追捧的商品。",
        0: "就这样，她被卖给了商人做女仆，往后的生活只剩下杂役与被侵犯。",
    },
}

SELL_FOLLOWUP_DEFAULT_TIER_LINES = {
    76: {
        3: f"{{name}} 被高价转卖后，似乎作为某位强大魔族的专属玩物活了下去。",
        2: f"{{name}} 被当作珍贵的玩赏奴隶收藏起来，过着被人反复享用的生活。",
        1: f"{{name}} 被送进了娼馆，很快就学会了如何迎合各式各样的客人。",
        0: f"{{name}} 被廉价卖给了奴隶主，往后的生活只剩下无穷无尽的侵犯。",
    },
    85: {
        3: f"{{name}} 被卖给了位高权重之人，听说后来彻底沦为了不见天日的私宠。",
        2: f"{{name}} 被卖给了富有的魔族，尊严早已在一次次展示与玩弄中消失殆尽。",
        1: f"{{name}} 被送进了娼馆，幼小的身体很快就被训练成了招揽客人的商品。",
        0: f"{{name}} 被卖去做杂役与性奴，往后的生活只剩下忍耐与哭泣。",
    },
}

SELL_FOLLOWUP_REBELLIOUS_TIER_ONE_LINES = {
    5: {
        "default": [
            f"{{name}} 被当成珍贵异族关进研究设施。",
            "她被养在充满法师与魔女的设施里，每天都有人定时采集血液与排泄物，灌肠后在桶里哭着排泄几乎成了日常。",
        ],
        "warrior_high": [
            f"{{name}} 被卖给兽人的佣兵团后，反而成了能把兽人们踢得满地打滚的大姐头。",
            "靠着武艺与嘴皮子，她有时在训练时甚至会一脚踢飞兽人，让那群家伙苦笑着怀疑到底谁才是奴隶。",
        ],
        "warrior_low": [
            f"{{name}} 被卖给兽人的佣兵团，慢慢适应了那种拳头解决问题的生活。",
            "她开始学着兽人的嚣张语气说话，用木剑狠狠干训练对象，辛劳过后还会和兽人们一起裸体洗澡，最后几乎成了佣兵团不可或缺的一员。",
        ],
        "priest": [
            f"{{name}} 被吸血鬼洗礼后，成了暗黑之神的信徒。",
            "邪恶仪式与药物让她被洗脑得忠诚又得心应手，只是经常会在失禁之后顺势绝顶，样子可悲又滑稽。",
        ],
        "fallback": [
            f"{{name}} 最终成了吸血鬼的饮料机。",
            "全身被紧紧拘束的她只能通过管子吃喝与排泄，唯一还能称作乐趣的，只剩睡前那一次被爱抚到绝顶。",
        ],
    },
    9: {
        "default": [
            f"{{name}} 被当成珍贵异族关进研究设施。",
            "她被养在充满法师与魔女的设施里，每天都有人定时采集血液与排泄物，灌肠后在桶里哭着排泄几乎成了日常。",
        ],
        "warrior_high": [
            f"{{name}} 被卖给兽人的佣兵团后，反而成了能把兽人们踢得满地打滚的大姐头。",
            "靠着武艺与嘴皮子，她有时在训练时甚至会一脚踢飞兽人，让那群家伙苦笑着怀疑到底谁才是奴隶。",
        ],
        "warrior_low": [
            f"{{name}} 被卖给兽人的佣兵团，慢慢适应了那种拳头解决问题的生活。",
            "她开始学着兽人的嚣张语气说话，用木剑狠狠干训练对象，辛劳过后还会和兽人们一起裸体洗澡，最后几乎成了佣兵团不可或缺的一员。",
        ],
        "priest": [
            f"{{name}} 被吸血鬼洗礼后，成了暗黑之神的信徒。",
            "邪恶仪式与药物让她被洗脑得忠诚又得心应手，只是经常会在失禁之后顺势绝顶，样子可悲又滑稽。",
        ],
        "fallback": [
            f"{{name}} 最终成了吸血鬼的饮料机。",
            "全身被紧紧拘束的她只能通过管子吃喝与排泄，唯一还能称作乐趣的，只剩睡前那一次被爱抚到绝顶。",
        ],
    },
}

INVASION_EVENT_THRESHOLD_TABLES = {
    81: [
        {"level": 0, "rise": 2000, "fall": 500, "rise_text": "占领了村庄", "fall_text": "人间界的军队占领了村庄"},
        {"level": 1, "rise": 4000, "fall": 2000, "rise_text": "占领了港口", "fall_text": "人间界的军队占领了港口"},
        {"level": 2, "rise": 6000, "fall": 4000, "rise_text": "攻陷了堡垒", "fall_text": "人间界的军队攻陷了堡垒"},
        {"level": 3, "rise": 8000, "fall": 6000, "rise_text": "占领了街道", "fall_text": "人间界的军队占领了街道"},
        {"level": 4, "rise": 10000, "fall": 8000, "rise_text": "占领了城市", "fall_text": "人间界的军队占领了城市"},
    ],
    86: [
        {"level": 0, "rise": 2000, "fall": 500, "rise_text": "精灵领域的侵略加深了", "fall_text": "精灵族夺回了外围领地"},
        {"level": 1, "rise": 4000, "fall": 2000, "rise_text": "精灵领域的侵略进一步扩大了", "fall_text": "精灵族夺回了部分据点"},
        {"level": 2, "rise": 6000, "fall": 4000, "rise_text": "精灵领域的防线被击穿了", "fall_text": "精灵族重建了部分防线"},
        {"level": 3, "rise": 8000, "fall": 6000, "rise_text": "精灵领域几近沦陷", "fall_text": "精灵族收复了前线阵地"},
        {"level": 4, "rise": 10000, "fall": 8000, "rise_text": "精灵领域被完全支配", "fall_text": "精灵族重新夺回了大片领土"},
    ],
    88: [
        {"level": 0, "rise": 2000, "fall": 500, "rise_text": "龙之山脉的侵略加深了", "fall_text": "群龙夺回了外围地带"},
        {"level": 1, "rise": 4000, "fall": 2000, "rise_text": "龙之山脉的侵略进一步扩大了", "fall_text": "群龙重新夺回了部分巢穴"},
        {"level": 2, "rise": 6000, "fall": 4000, "rise_text": "龙之山脉的防线被攻破了", "fall_text": "群龙重建了部分防线"},
        {"level": 3, "rise": 8000, "fall": 6000, "rise_text": "龙之山脉几近沦陷", "fall_text": "群龙重新收复了前线阵地"},
        {"level": 4, "rise": 10000, "fall": 8000, "rise_text": "龙之山脉被完全支配", "fall_text": "群龙重新夺回了大片领地"},
    ],
    90: [
        {"level": 0, "rise": 2000, "fall": 500, "rise_text": "天界的侵略加深了", "fall_text": "天界军收复了外围领地"},
        {"level": 1, "rise": 4000, "fall": 2000, "rise_text": "天界的侵略进一步扩大了", "fall_text": "天界军重新夺回了部分据点"},
        {"level": 2, "rise": 6000, "fall": 4000, "rise_text": "天界的防线被击穿了", "fall_text": "天界军重建了部分防线"},
        {"level": 3, "rise": 8000, "fall": 6000, "rise_text": "天界几近沦陷", "fall_text": "天界军重新收复了前线阵地"},
        {"level": 4, "rise": 10000, "fall": 8000, "rise_text": "天界被完全支配", "fall_text": "天界军重新夺回了大片领地"},
    ],
}

DRESS_NORMAL_SPECIAL_OPTIONS = [
    {"menu_id": 1, "slot": "main", "name": "高中制服", "cloth_id": 17, "cost": 30000, "req": 0},
    {"menu_id": 2, "slot": "main", "name": "初中制服", "cloth_id": 18, "cost": 30000, "req": 0},
    {"menu_id": 3, "slot": "main", "name": "水手服", "cloth_id": 19, "cost": 30000, "req": 0},
    {"menu_id": 4, "slot": "main", "name": "私立贵族学院制服", "cloth_id": 20, "cost": 30000, "req": 0},
    {"menu_id": 5, "slot": "main", "name": "西装", "cloth_id": 21, "cost": 30000, "req": 0},
    {"menu_id": 6, "slot": "main", "name": "浴衣", "cloth_id": 204, "cost": 30000, "req": 0},
    {"menu_id": 7, "slot": "main", "name": "名牌服装", "cloth_id": 23, "cost": 30000, "req": 0},
    {"menu_id": 8, "slot": "main", "name": "护士服", "cloth_id": 24, "cost": 30000, "req": 0},
    {"menu_id": 9, "slot": "main", "name": "女性用军服", "cloth_id": 25, "cost": 30000, "req": 0},
    {"menu_id": 10, "slot": "main", "name": "女侍制服", "cloth_id": 26, "cost": 30000, "req": 0},
    {"menu_id": 11, "slot": "main", "name": "便利店制服", "cloth_id": 27, "cost": 30000, "req": 0},
    {"menu_id": 12, "slot": "main", "name": "事务员制服", "cloth_id": 28, "cost": 30000, "req": 0},
    {"menu_id": 13, "slot": "main", "name": "岛屿女孩服装", "cloth_id": 29, "cost": 30000, "req": 2},
    {"menu_id": 14, "slot": "main", "name": "演出服", "cloth_id": 30, "cost": 30000, "req": 0},
    {"menu_id": 15, "slot": "main", "name": "运动服", "cloth_id": 31, "cost": 30000, "req": 3},
    {"menu_id": 16, "slot": "main", "name": "丧服", "cloth_id": 32, "cost": 30000, "req": 0},
    {"menu_id": 17, "slot": "main", "name": "拉拉队服", "cloth_id": 33, "cost": 30000, "req": 3},
    {"menu_id": 18, "slot": "main", "name": "网球服", "cloth_id": 34, "cost": 30000, "req": 3},
    {"menu_id": 19, "slot": "main", "name": "女警服", "cloth_id": 35, "cost": 30000, "req": 2},
    {"menu_id": 20, "slot": "main", "name": "狩衣", "cloth_id": 102, "cost": 30000, "req": 0},
    {"menu_id": 21, "slot": "main", "name": "巫女装束", "cloth_id": 104, "cost": 30000, "req": 0},
    {"menu_id": 22, "slot": "main", "name": "军服", "cloth_id": 106, "cost": 30000, "req": 0},
    {"menu_id": 23, "slot": "main", "name": "体操服", "cloth_id": 109, "cost": 30000, "req": 3},
    {"menu_id": 24, "slot": "main", "name": "忍者装束", "cloth_id": 110, "cost": 30000, "req": 2},
    {"menu_id": 25, "slot": "main", "name": "骑马服", "cloth_id": 112, "cost": 30000, "req": 0},
    {"menu_id": 26, "slot": "main", "name": "滑雪服", "cloth_id": 120, "cost": 30000, "req": 2},
    {"menu_id": 27, "slot": "main", "name": "和服", "cloth_id": 202, "cost": 30000, "req": 0},
    {"menu_id": 28, "slot": "main", "name": "晚礼服", "cloth_id": 208, "cost": 30000, "req": 5},
    {"menu_id": 29, "slot": "main", "name": "幼稚园服", "cloth_id": 221, "cost": 30000, "req": 5},
    {"menu_id": 30, "slot": "main", "name": "婚礼裙装", "cloth_id": 240, "cost": 30000, "req": 5},
]

DUNGEON_QUEST_SUBJECT_NAME_MAP = {
    1: {
        0: "村娘",
        1: "千金",
        2: "女学生",
        3: "街娘",
        4: "女冒险者",
    },
    2: {
        0: "人妻",
        1: "女神官",
        2: "大小姐",
        3: "女学者",
        4: "女冒险者",
    },
    3: {
        0: "魔女",
        1: "魔法女学生",
        2: "女魔法骑士",
        3: "女魔法学者",
        4: "女冒险者",
    },
}

DUNGEON_QUEST_RESULT_TEXT_TEMPLATES = {
    1: {
        "success": "将被{target_name}掳走的{subject}安全救出了。",
        "failure": "被{target_name}掳走的{subject}没能救回来。",
    },
    2: {
        "success": "将被{target_name}诱惑了的{subject}安全救出了。",
        "failure": "被{target_name}诱惑了的{subject}已经彻底失陷。",
    },
    3: {
        "success": "将{target_name}的肝打包送回，治好了{subject}的异状。",
        "failure": "因变异魔法而暴走的{subject}没能得到救治。",
    },
}

DUNGEON_QUEST_CONDITION_LABELS = {
    0: "BOSS战",
    1: "陷阱",
    2: "时限",
    3: "大量敌人",
    4: "性要求",
}

DUNGEON_QUEST_SUBJECT_PREFIXES = {
    1: "被掳走的",
    2: "受魔诱惑的",
    3: "因变异魔法而暴走的",
}

DUNGEON_STATE_CAMP_BIT = 0
DUNGEON_STATE_CURSE_BIT = 1
DUNGEON_STATE_SLIPPERY_BIT = 3
DUNGEON_STATE_PREEMPT_BLOCKED_BIT = 5
DUNGEON_STATE_FALL_BIT = 6
DUNGEON_STATE_INVISIBLE_BIT = 7
DUNGEON_STATE_HERO_BIT = 8
DUNGEON_STATE_AROUSAL_BIT = 9
ARCANA_BATTLE_POISON_BIT = 4

USE_NOW_ITEM_EFFECT_HANDLERS = {
    29: "_apply_use_now_item_clear_parasite",
    30: "_apply_use_now_item_restore_hp",
    31: "_apply_use_now_item_reduce_stress",
    33: "_apply_use_now_item_remove_lifespan_limit",
    40: "_apply_use_now_item_increase_pregnancy_chance",
    41: "_apply_use_now_item_body_hair_growth",
}

DRESS_ACCESSORY_REQUIREMENT_RULES = {
    12: ("fixed", 1),
    4: ("fixed", 1),
    53: ("talent", 63, 2, 122, 3),
    71: ("group", {71, 74, 75, 76}, 21, 10, 124, 5, 136, 3),
    72: ("group", {72, 77, 80}, 21, 8, 88, 3),
    73: ("special", 6, 110, 114, 130),
    69: ("binary", 57, 1, 6),
    92: ("binary", 85, 1, 6),
    98: ("fixed", 3),
}

RUNNING_COST_DIFFICULTY_BONUSES = {
    1: 0,
    2: 100,
    3: 200,
    4: 300,
    5: 400,
    9: 0,
}

RUNNING_COST_DIFFICULTY_MULTIPLIERS = {
    1: [(None, 80)],
    3: [(20, 120), (40, 150), (60, 200), (None, 250)],
    4: [(20, 140), (30, 180), (40, 300), (None, 500)],
    5: [(15, 200), (25, 400), (35, 800), (None, 1600)],
}

RUNNING_COST_POPULARITY_MULTIPLIERS = [
    (50, 110),
    (70, 120),
    (90, 130),
]

RUNNING_COST_CONTRIBUTION_MULTIPLIERS = [
    (3000, 10),
    (2000, 30),
    (1200, 50),
    (700, 60),
    (400, 70),
    (200, 80),
    (100, 90),
]

PILLORY_DAILY_COUNTER_FIELDS = {
    "vaginal": (661, 0, 0, 0),
    "anal": (662, 1, 0, 0),
    "oral": (663, 22, 0, 0),
    "breast": (664, 3, 0, 0),
    "other": (665, None, 0, 0),
}

POST_MESSAGE_ACTION_KIND_METHODS = {
    "normal_end_followup": "_handle_post_message_normal_end_followup",
    "story_branch_prompt": "_handle_post_message_story_branch_prompt",
    "princess_stage_20_prompt": "_handle_post_message_princess_stage_20_prompt",
    "princess_stage_50_prompt": "_handle_post_message_princess_stage_50_prompt",
    "princess_ending_prompt": "_handle_post_message_princess_ending_prompt",
    "princess_witch_ending_prompt": "_handle_post_message_princess_witch_ending_prompt",
    "square_love_ending_prompt": "_handle_post_message_square_love_ending_prompt",
    "spade_love_ending_prompt": "_handle_post_message_spade_love_ending_prompt",
    "spade_milk_ending_prompt": "_handle_post_message_spade_milk_ending_prompt",
    "square_departure_prompt": "_handle_post_message_square_departure_prompt",
    "spade_departure_prompt": "_handle_post_message_spade_departure_prompt",
    "godness_stage_120_prompt": "_handle_post_message_godness_stage_120_prompt",
    "human_conquest_followup": "_handle_post_message_human_conquest_followup",
}

SHOP_GROUP_DEFINITIONS = [
    {"title": "调教道具", "kind": "range", "range": (0, 24), "filter_stock": True},
    {"title": "消耗道具", "kind": "consumables"},
    {"title": "知识与强化", "kind": "knowledge"},
    {"title": "陷阱", "kind": "trap"},
]

SETTINGS_PAGE_ENTRIES = {
    0: [
        {"id": 0, "label": "勇者投降后的凌辱", "type": "bit", "flag": 5, "bit": 0, "on": "许可", "off": "禁止"},
        {"id": 1, "label": "勇者强化", "type": "bit", "flag": 5, "bit": 1, "on": "按游戏天数增强", "off": "等级维持"},
        {"id": 2, "label": "怀孕分娩机能", "type": "bit", "flag": 5, "bit": 2, "on": "ON", "off": "OFF"},
        {"id": 3, "label": "勇者自动处刑机能", "type": "bit", "flag": 5, "bit": 3, "on": "ON", "off": "OFF"},
        {"id": 4, "label": "禁止怪物迎击", "type": "bit", "flag": 5, "bit": 4, "on": "ON", "off": "OFF"},
        {"id": 5, "label": "显示战斗记录", "type": "bit", "flag": 5, "bit": 5, "on": "ON", "off": "OFF"},
        {"id": 6, "label": "自动补充陷阱", "type": "bit", "flag": 5, "bit": 6, "on": "ON", "off": "OFF"},
        {"id": 7, "label": "NTR机能", "type": "bit", "flag": 5, "bit": 7, "on": "ON", "off": "OFF"},
        {"id": 8, "label": "素质分类显示", "type": "bit", "flag": 5, "bit": 8, "on": "ON", "off": "OFF"},
        {"id": 9, "label": "战斗记录的SKIP中断", "type": "bit", "flag": 5, "bit": 9, "on": "ON", "off": "OFF"},
        {"id": 10, "label": "怀孕时的迎击/临月调教", "type": "bit", "flag": 5, "bit": 10, "on": "许可", "off": "禁止"},
        {"id": 11, "label": "服装系统", "type": "toggle", "flag": 37},
        {"id": 12, "label": "濒死时自动结束调教", "type": "toggle", "flag": 35},
        {"id": 13, "label": "调教过滤器", "type": "filter"},
    ],
    1: [
        {"id": 14, "label": "自我介绍式角色信息", "type": "bit", "flag": 5, "bit": 11, "on": "ON", "off": "OFF"},
        {"id": 15, "label": "显示角色年龄/三围", "type": "age_measurements", "flag": 5, "bits": [12, 15]},
        {"id": 16, "label": "解除勇者登录限制", "type": "bit", "flag": 5, "bit": 32, "on": "ON", "off": "OFF"},
        {"id": 17, "label": "新探索模式", "type": "bit", "flag": 5, "bit": 33, "on": "ON", "off": "OFF"},
        {"id": 18, "label": "显示高级调教指令名", "type": "bit", "flag": 5, "bit": 34, "on": "ON", "off": "OFF"},
        {"id": 19, "label": "你的宝贝兵器现状", "type": "penis"},
        {"id": 20, "label": "自动提升角色能力", "type": "autoup"},
        {"id": 21, "label": "陷落后处女主动献身", "type": "virgin"},
        {"id": 22, "label": "男冒险者许可", "type": "bit", "flag": 8, "bit": 0, "on": "许可", "off": "禁止"},
        {"id": 23, "label": "勇者出现时的素质表示", "type": "bit", "flag": 8, "bit": 1, "on": "ON", "off": "OFF"},
        {"id": 24, "label": "勇者的恋爱发展", "type": "bit", "flag": 8, "bit": 2, "on": "许可", "off": "禁止"},
        {"id": 25, "label": "勇者的任务揭示板", "type": "bit", "flag": 8, "bit": 3, "on": "许可", "off": "禁止"},
        {"id": 26, "label": "MOD开关", "type": "modlist"},
    ],
}

SETTINGS_ENTRY_STATUS_HANDLERS = {
    "bit": "_format_settings_entry_status_bit",
    "toggle": "_format_settings_entry_status_toggle",
    "filter": "_format_settings_entry_status_filter",
    "dualbit": "_format_settings_entry_status_dualbit",
    "age_measurements": "_format_settings_entry_status_age_measurements",
    "penis": "_format_settings_entry_status_penis",
    "autoup": "_format_settings_entry_status_autoup",
    "virgin": "_format_settings_entry_status_virgin",
    "modlist": "_format_settings_entry_status_modlist",
}

INVASION_CONQUEST_REWARD_CONFIG_TRIBUTE = {
    86: {
        "title": "魔王终于征服了精灵族的领域。",
        "summary": "你向精灵族的长老提出了要求。",
        "demand": "要求献上秘藏的精灵族圣女。",
        "template_id": 31,
        "start_flag": 87,
        "final_flag": 87,
        "final_value": 2,
        "gain_text": "精灵族圣女被作为贡品献上了。",
        "label": "精灵族圣女",
        "retry_text": "去要圣女",
        "random_title": "精灵族挑选少女作为贡品……",
    },
    88: {
        "title": "魔王终于征服了龙族的山脉。",
        "summary": "你向龙族的长老提出了要求。",
        "demand": "要求献上有着最悠久血统的龙族公主。",
        "template_id": 32,
        "start_flag": 89,
        "final_flag": 89,
        "final_value": 2,
        "gain_text": "龙族公主被作为贡品献上了。",
        "label": "龙族公主",
        "retry_text": "去要公主",
        "random_title": "龙族挑选少女作为贡品……",
    },
    90: {
        "title": "魔王终于征服了天界。",
        "summary": "你向天界提出了要求。",
        "demand": "命令献上被选为下一代主神的天使。",
        "template_id": 33,
        "start_flag": 91,
        "final_flag": 91,
        "final_value": 2,
        "gain_text": "天使族的下任主神被作为贡品献上了。",
        "label": "天使族的下任主神",
        "retry_text": "去要主神候补",
        "random_title": "天使族挑选少女作为贡品……",
    },
}

ABILITY_UPGRADE_COST_TABLE_10_13 = {
    10: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10_without_love",
        "cost_types": {10: "juel", 4: "juel", 5: "juel", 6: "juel"},
        "costs": (
            (0, {10: 10, 4: 10, 5: 300, 6: 200}),
            (1, {10: 150, 4: 100, 5: 1000, 6: 1200}),
            (2, {10: 1000, 4: 800, 5: 2000, 6: 3000}),
            (3, {10: 3000, 4: 3000, 6: 12000}),
            (4, {10: 8000, 4: 5000}),
            (5, {10: 12000, 4: 10000}),
            (6, {10: 25000, 4: 20000}),
            (7, {4: 40000}),
            (8, {4: 80000}),
            (9, {4: 150000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_10",
    },
    11: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_11_without_support",
        "cost_types": {5: "juel"},
        "costs": (
            (0, {5: 5}),
            (1, {5: 50}),
            (2, {5: 1000}),
            (3, {5: 5000}),
            (4, {5: 12000}),
            (5, {5: 20000}),
            (6, {5: 30000}),
            (7, {5: 50000}),
            (8, {5: 80000}),
            (9, {5: 150000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_11",
    },
    12: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10",
        "cost_types": {7: "juel"},
        "costs": (
            (0, {7: 1}),
            (1, {7: 25}),
            (2, {7: 200}),
            (3, {7: 3000}),
            (4, {7: 8000}),
            (5, {7: 12000}),
            (6, {7: 16000}),
            (7, {7: 22000}),
            (8, {7: 28000}),
            (9, {7: 35000}),
        ),
        "prereq": "_build_ability_upgrade_prereq_12_15_cap",
    },
    13: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_13",
        "cost_types": {7: "juel"},
        "costs": (
            (0, {7: 5}),
            (1, {7: 400}),
            (2, {7: 1000}),
            (3, {7: 3000}),
            (4, {7: 6000}),
            (5, {7: 9000}),
            (6, {7: 12000}),
            (7, {7: 16000}),
            (8, {7: 20000}),
            (9, {7: 25000}),
        ),
        "prereq": "_build_ability_upgrade_prereq_13",
    },
}

ABILITY_UPGRADE_COST_TABLE_14_17 = {
    14: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10",
        "cost_types": {7: "juel", 5: "exp"},
        "costs": (
            (0, {7: 1, 5: 3}),
            (1, {7: 10, 5: 10}),
            (2, {7: 100, 5: 30}),
            (3, {7: 1500, 5: 80}),
            (4, {7: 4000, 5: 100}),
            (5, {7: 5000, 5: 130}),
            (6, {7: 6500, 5: 160}),
            (7, {7: 8000, 5: 200}),
            (8, {7: 10000, 5: 250}),
            (9, {7: 15000, 5: 300}),
        ),
        "prereq": "_build_ability_upgrade_prereq_14",
    },
    15: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10",
        "cost_types": {7: "juel", 73: "exp"},
        "costs": (
            (0, {7: 1, 73: 3}),
            (1, {7: 10, 73: 10}),
            (2, {7: 100, 73: 30}),
            (3, {7: 1500, 73: 50}),
            (4, {7: 3000, 73: 100}),
            (5, {7: 4000, 73: 120}),
            (6, {7: 5200, 73: 150}),
            (7, {7: 7500, 73: 180}),
            (8, {7: 9000, 73: 220}),
            (9, {7: 13000, 73: 250}),
        ),
        "prereq": "_build_ability_upgrade_prereq_12_15_cap",
    },
    16: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10",
        "cost_types": {2: "juel", 20: "exp"},
        "costs": (
            (0, {2: 1, 20: 1}),
            (1, {2: 4, 20: 4}),
            (2, {2: 20, 20: 20}),
            (3, {2: 50, 20: 50}),
            (4, {2: 100, 20: 100}),
            (5, {2: 300, 20: 300}),
            (6, {2: 600, 20: 600}),
            (7, {2: 1200, 20: 1200}),
            (8, {2: 2500, 20: 2500}),
            (9, {2: 5000, 20: 5000}),
        ),
        "prereq": "_build_ability_upgrade_prereq_16",
    },
    17: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_10",
        "cost_types": {8: "juel", 2: "exp", 11: "exp"},
        "costs": (
            (0, {8: 100, 2: 1}),
            (1, {8: 1000, 11: 1}),
            (2, {8: 3000}),
            (3, {8: 6000}),
            (4, {8: 12000}),
            (5, {8: 25000}),
            (6, {8: 50000}),
            (7, {8: 80000}),
            (8, {8: 120000}),
            (9, {8: 150000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_17",
        "prereq": "_build_ability_upgrade_prereq_17",
    },
}

ABILITY_UPGRADE_COST_TABLE_37_40 = {
    37: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_37",
        "cost_types": {4: "juel", 5: "juel", 6: "juel", 74: "exp"},
        "costs": (
            (0, {4: 2000, 5: 3000, 6: 1000, 74: 50}),
            (1, {4: 5000, 5: 8000, 6: 2500, 74: 100}),
            (2, {4: 8000, 5: 15000, 6: 5500, 74: 150}),
            (3, {4: 14000, 5: 30000, 6: 10000, 74: 250}),
            (4, {4: 22000, 5: 50000, 6: 20000, 74: 400}),
            (5, {4: 34000, 5: 80000, 6: 30000, 74: 500}),
            (6, {4: 55000, 5: 120000, 6: 50000, 74: 800}),
            (7, {4: 80000, 5: 180000, 6: 60000, 74: 1200}),
            (8, {4: 150000, 5: 300000, 6: 90000, 74: 2000}),
            (9, {4: 300000, 5: 600000, 6: 150000, 74: 3000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_37",
        "prereq": "_build_ability_upgrade_prereq_37",
    },
    39: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_39",
        "cost_types": {5: "juel", 6: "juel", 56: "exp"},
        "costs": (
            (0, {5: 2000, 6: 2000, 56: 30}),
            (1, {5: 5000, 6: 5000, 56: 100}),
            (2, {5: 10000, 6: 10000, 56: 220}),
            (3, {5: 20000, 6: 20000, 56: 400}),
            (4, {5: 30000, 6: 30000, 56: 800}),
            (5, {5: 45000, 6: 45000, 56: 1600}),
            (6, {5: 75000, 6: 75000, 56: 2000}),
            (7, {5: 100000, 6: 100000, 56: 2800}),
            (8, {5: 200000, 6: 200000, 56: 4000}),
            (9, {5: 300000, 6: 300000, 56: 6000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_39",
        "prereq": "_build_ability_upgrade_prereq_39",
    },
    40: {
        "max_level": 10,
        "soft_cap": "_build_ability_upgrade_soft_cap_40",
        "cost_types": {15: "juel"},
        "costs": (
            (0, {15: 2000}),
            (1, {15: 5000}),
            (2, {15: 10000}),
            (3, {15: 20000}),
            (4, {15: 30000}),
            (5, {15: 45000}),
            (6, {15: 75000}),
            (7, {15: 100000}),
            (8, {15: 200000}),
            (9, {15: 300000}),
        ),
        "abnormal_exp": "_build_ability_upgrade_abnormal_exp_40",
        "prereq": "_build_ability_upgrade_prereq_40",
    },
}

LABO_PAGES = [
    {
        "title": "肉体改造 I",
        "items": [
            {"id": 0, "name": "丰胸改造", "cost": 20000, "kind": "bustup"},
            {"id": 1, "name": "平胸改造", "cost": 10000, "kind": "bustdown"},
            {"id": 2, "name": "加入母乳体质", "cost": 50000, "kind": "bonyu"},
            {"id": 3, "name": "扶她化", "cost": 50000, "kind": "futanari"},
            {"id": 4, "name": "去扶她化", "cost": 10000, "kind": "futanari_erase"},
            {"id": 5, "name": "附上动物耳朵", "cost": 2000, "kind": "animal"},
            {"id": 6, "name": "去除动物耳朵", "cost": 1000, "kind": "animal_erase"},
            {"id": 7, "name": "性成熟", "cost": 10000, "kind": "dematurity"},
            {"id": 8, "name": "记忆消去", "cost": 100000, "kind": "amnesia"},
            {"id": 9, "name": "阴部永久脱毛", "cost": 5000, "kind": "remove_hair"},
            {"id": 10, "name": "消去母乳体质", "cost": 10000, "kind": "bonyu_erase"},
            {"id": 11, "name": "消除漏尿癖", "cost": 10000, "kind": "omorashi_erase"},
        ],
    },
    {
        "title": "肉体改造 II",
        "items": [
            {"id": 12, "name": "处女膜再生术", "cost": 100000, "kind": "shojo_saisei"},
            {"id": 13, "name": "施加私处封印", "cost": 10000, "kind": "shojo_seal"},
            {"id": 14, "name": "解除私处封印", "cost": 10000, "kind": "shojo_seal_off"},
            {"id": 15, "name": "刺青的刻印/消去", "cost": 10000, "kind": "tattoo"},
            {"id": 16, "name": "头发颜色改变", "cost": 5000, "kind": "hair_color"},
            {"id": 17, "name": "肤色改变", "cost": 5000, "kind": "skin_color"},
            {"id": 18, "name": "感觉封锁", "cost": 20000, "kind": "block_feeling"},
            {"id": 19, "name": "异常妊娠体质", "cost": 20000, "kind": "extra_preg_mark"},
            {"id": 20, "name": "消除异常妊娠体质", "cost": 35000, "kind": "extra_preg_erase"},
            {"id": 21, "name": "变性", "cost": 200000, "kind": "trans_sex"},
            {"id": 22, "name": "自由局部调教设定", "cost": 20000, "kind": "free_train"},
            {"id": 23, "name": "淫乱爱慕互换", "cost": 500000, "kind": "love_corruption_swap"},
        ],
    },
    {
        "title": "其他研究",
        "items": [
            {"id": 50, "name": "购买触手生物", "cost": 50000, "kind": "item"},
            {"id": 51, "name": "死者苏生", "cost": 0, "kind": "resurrection"},
            {"id": 52, "name": "赋予生命", "cost": 0, "kind": "grant_human_life"},
            {"id": 54, "name": "安抚崩坏的心", "cost": 0, "kind": "cure_insane"},
            {"id": 55, "name": "寻访贞操带钥匙", "cost": 0, "kind": "recover_chastity_key"},
            {"id": 56, "name": "召唤影之仆从", "cost": 100000, "kind": "summon"},
            {"id": 59, "name": "赋予犄角", "cost": 20000, "kind": "horn"},
            {"id": 60, "name": "恶魔体征改造", "cost": 20000, "kind": "demon_trait"},
            {"id": 64, "name": "转生的秘法", "cost": 50000, "kind": "reincarnate"},
            {"id": 65, "name": "魂缚的诅咒", "cost": 10000, "kind": "soulbound"},
            {"id": 66, "name": "魂缚的解咒", "cost": 50000, "kind": "soulbound_erase"},
            {"id": 67, "name": "狂王俘虏的消去", "cost": 50000, "kind": "erase_encharmed"},
            {"id": 68, "name": "生命摇篮", "cost": 500000, "kind": "life_cradle"},
        ],
    },
    {
        "title": "战斗 / 洗脑",
        "items": [
            {"id": 70, "name": "HP＋10", "cost": 5000, "kind": "stat", "stat": 0, "amount": 10},
            {"id": 71, "name": "气力＋10", "cost": 5000, "kind": "stat", "stat": 1, "amount": 10},
            {"id": 72, "name": "攻击＋1", "cost": 5000, "kind": "battle_stat", "stat": 13, "amount": 1},
            {"id": 73, "name": "防御＋1", "cost": 5000, "kind": "battle_stat", "stat": 14, "amount": 1},
            {"id": 74, "name": "赋予魔法耐性", "cost": 50000, "kind": "talent", "talent": 257},
            {"id": 30, "name": "无视污垢", "cost": 5000, "kind": "brainwash", "talent": 64},
            {"id": 31, "name": "早泄", "cost": 8000, "kind": "brainwash", "talent": 133},
            {"id": 32, "name": "幼稚", "cost": 10000, "kind": "brainwash", "talent": 132},
            {"id": 33, "name": "抖S", "cost": 10000, "kind": "brainwash", "talent": 83},
        ],
    },
]

DAILY_INVASION_DECAY_RULES = [
    {
        "area_flag": 81,
        "conquer_flag": 82,
        "resist_name": "人间界的军队",
        "area_name": "人间界的侵略度",
        "conquered_area_name": "地上的魔界领土的侵略度",
        "recover_threshold": 6,
    },
    {
        "area_flag": 86,
        "conquer_flag": 87,
        "resist_name": "精灵族的抵抗组织",
        "area_name": "精灵领域的侵略度",
        "conquered_area_name": "黑暗精灵的领土的侵略度",
        "recover_threshold": 5,
    },
    {
        "area_flag": 88,
        "conquer_flag": 89,
        "resist_name": "成群的龙",
        "area_name": "龙之山脉的侵略度",
        "conquered_area_name": "混沌龙之山的侵略度",
        "recover_threshold": 4,
    },
    {
        "area_flag": 90,
        "conquer_flag": 91,
        "resist_name": "天界的军队",
        "area_name": "天界的侵略度",
        "conquered_area_name": "堕天使的淫界的侵略度",
        "recover_threshold": 3,
    },
]

def safe_input(prompt: str = "") -> str:
    """Safe input function that handles encoding issues"""
    try:
        return input(prompt)
    except EOFError:
        return ""
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            return input(prompt.encode('cp932', errors='ignore').decode('cp932'))
        except:
            return ""

# ==================== ERB Interpreter Core ====================

class ERBVariable:
    """ERB Variable class supporting various types"""
    def __init__(self):
        self.flags = {}       # FLAG array
        self.d_flags = {}     # %D% flags
        self.globals = {}     # GLOBAL array
        self.juel = {}        # JUEL array
        self.chars = []       # Character arrays
        self.items = {}       # Item array
        self.departed_chars = {}  # EVENT_CHARA_LEAVE style serialized character storage
        self.suisei_str = {}  # SUISEI_STR array (video crystal shelf)
        self.money = 10000    # Money
        self.day = [1, 1, 1, 0]  # DAY:0=year, DAY:1=month, DAY:2=day, DAY:3=weekday
        self.time = 0        # TIME: 0=morning, 1=afternoon
        
        # 数组变量 (用于 VARSET/ARRAYSHIFT 等操作)
        self.local = [0] * 1000      # LOCAL 数组
        self.locals = [""] * 1000    # LOCALS 数组
        self.flag = [0] * 1000       # FLAG 数组 (数值版本)
        self.item = [0] * 1000       # ITEM 数组
        self.itemsales = [0] * 1000  # ITEMSALES 数组
        self.lastsave_no = [0] * 100  # LASTSAVE_NO 数组
        self.count = 0               # COUNT 循环变量

        # Game state
        self.target = -1      # Current training target
        self.assi = -1       # Assistant
        self.master = 0       # Master (always 0)
        self.q = 0
        self.s = 0
        self.n = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.tflag = {}

    def get_flag(self, idx: int, default: int = 0) -> int:
        return self.flags.get(idx, default)

    def set_flag(self, idx: int, value: int):
        self.flags[idx] = value

    def get_char_flag(self, char_idx: int, flag_idx: int, default: int = 0) -> int:
        if char_idx >= len(self.chars):
            return default
        return self.chars[char_idx].get("FLAG", {}).get(flag_idx, default)

    def set_char_flag(self, char_idx: int, flag_idx: int, value: int):
        while char_idx >= len(self.chars):
            self.chars.append(Character())
        self.chars[char_idx].set_flag(flag_idx, value)


class Character:
    """Character class for player and NPCs"""
    def __init__(self):
        self.name = ""
        self.callname = ""
        self.nick_name = ""
        self.template_id: Optional[int] = None
        self.base = {}       # BASE array (HP, MP, etc.)
        self.maxbase = {}    # MAXBASE array
        self.abl = {}        # ABL array (abilities)
        self.exp = {}        # EXP array (experience)
        self.juel = {}       # JUEL array
        self.talent = {}     # TALENT array
        self.mark = {}        # MARK array
        self.palam = {}      # PALAM array (parameters)
        self.source = {}     # SOURCE array
        self.losebase = {}   # LOSEBASE snapshot from the latest command
        self.equipt = {}    # TEQUIP array
        self.stain = {}      # STAIN array
        self.cflag = {}      # CFLAG array
        self.cstr = {}       # CSTR array (strings)
        self.item = {}       # ITEM held

    def get(self, key: str, default: Any = 0) -> Any:
        return getattr(self, key, default)

    def set_flag(self, idx: int, value: int):
        self.cflag[idx] = value

    def get_flag(self, idx: int, default: int = 0) -> int:
        return self.cflag.get(idx, default)

    # ---- 类型化属性访问方法 ----
    def get_abl(self, key: int, default: int = 0) -> int:
        """获取能力值"""
        return int(self.abl.get(key, default))

    def set_abl(self, key: int, value: int) -> None:
        """设置能力值"""
        self.abl[key] = value

    def get_talent(self, key: int, default: int = 0) -> int:
        """获取素质值"""
        return int(self.talent.get(key, default))

    def has_talent(self, key: int) -> bool:
        """是否拥有素质"""
        return int(self.talent.get(key, 0)) != 0

    def get_exp(self, key: int, default: int = 0) -> int:
        """获取经验值"""
        return int(self.exp.get(key, default))

    def add_exp(self, key: int, amount: int) -> None:
        """增加经验值"""
        self.exp[key] = int(self.exp.get(key, 0)) + amount

    def get_juel(self, key: int, default: int = 0) -> int:
        """获取宝珠值"""
        return int(self.juel.get(key, default))

    def get_palam(self, key: int, default: int = 0) -> int:
        """获取参数值"""
        return int(self.palam.get(key, default))

    def get_base(self, key: int, default: int = 0) -> int:
        """获取基础值"""
        return int(self.base.get(key, default))

    def get_stain(self, key: int, default: int = 0) -> int:
        """获取污渍值"""
        return int(self.stain.get(key, default))

    def get_tequip(self, key: int, default: int = 0) -> int:
        """获取装备值"""
        return int(self.equipt.get(key, default))

    def get_cflag(self, key: int, default: int = 0) -> int:
        """获取角色标志"""
        return int(self.cflag.get(key, default))

    def get_source(self, key: int, default: int = 0) -> int:
        """获取SOURCE值"""
        return int(self.source.get(key, default))

    def set_source(self, key: int, value: int) -> None:
        """设置SOURCE值"""
        self.source[key] = value

    def get_mark(self, key: int, default: int = 0) -> int:
        """获取刻印值"""
        return int(self.mark.get(key, default))


class ERBInterpreter:
    """Main ERB Interpreter class"""

    def __init__(self):
        self.vars = ERBVariable()
        self.functions = {}  # User-defined functions
        self.globals = {}
        self.paths = None
        self.current_line = 0
        self.lines = []
        self.labels = {}
        self.output_buffer = []
        self.input_buffer = []
        self.input_ptr = 0
        self.running = True
        self.current_state = "TITLE"
        self._loop_stack = []  # 循环控制栈 (REPEAT/FOR/WHILE/DO)
        self.result = 0  # RESULT 返回值
        self.results = ""  # RESULTS 返回字符串
        self._self_kojo_source_cache: Dict[int, List[str]] = {}

        # Built-in functions
        self._init_builtins()

    def _init_builtins(self):
        """Initialize built-in functions"""
        self.builtins = {}
        self.builtins.update(self._build_print_builtin_map())
        self.builtins.update(self._build_control_flow_builtin_map())
        self.builtins.update(self._build_input_builtin_map())
        self.builtins.update(self._build_data_builtin_map())
        self.builtins.update(self._build_variable_builtin_map())
        self.builtins.update(self._build_array_builtin_map())
        self.builtins.update(self._build_ui_builtin_map())
        self.builtins.update(self._build_character_builtin_map())
        self.builtins.update(self._build_system_builtin_map())
        self.builtins.update(self._build_other_builtin_map())

    def _build_print_builtin_map(self) -> Dict[str, Any]:
        return {
            "PRINT": self._cmd_print,
            "PRINTL": self._cmd_printl,
            "PRINTV": self._cmd_printv,
            "PRINTFORML": self._cmd_printforml,
            "PRINTFORM": self._cmd_printform,
            "PRINTFORMS": self._cmd_printforms,
            "PRINTFORMC": self._cmd_printforc,
            "PRINTBUTTON": self._cmd_printbutton,
            "PRINTBUTTONFORML": self._cmd_printbuttonforml,
            "PRINTS": self._cmd_prints,
            "PRINTC": self._cmd_printc,
            "PRINTW": self._cmd_printw,
            "PRINTFORMW": self._cmd_printformw,
            "PRINTLC": self._cmd_printlc,
            "PRINTVL": self._cmd_printvl,
        }

    def _build_control_flow_builtin_map(self) -> Dict[str, Any]:
        return {
            "IF": self._cmd_if,
            "ELSE": self._cmd_else,
            "ELSEIF": self._cmd_elseif,
            "ENDIF": self._cmd_endif,
            "GOTO": self._cmd_goto,
            "CALL": self._cmd_call,
            "RETURN": self._cmd_return,
            "RESTART": self._cmd_restart,
            "BEGIN": self._cmd_begin,
            "REPEAT": self._cmd_repeat,
            "REND": self._cmd_rend,
            "FOR": self._cmd_for,
            "NEXT": self._cmd_next,
            "CONTINUE": self._cmd_continue,
            "BREAK": self._cmd_break,
            "DO": self._cmd_do,
            "LOOP": self._cmd_loop,
            "WHILE": self._cmd_while,
            "ENDWHILE": self._cmd_endwhile,
        }

    def _build_input_builtin_map(self) -> Dict[str, Any]:
        return {
            "INPUT": self._cmd_input,
            "INPUTS": self._cmd_inputs,
            "TINPUT": self._cmd_tinput,
            "TINPUTS": self._cmd_tinputs,
            "ONEINPUT": self._cmd_oneinput,
            "WAIT": self._cmd_wait,
            "FORCEWAIT": self._cmd_forcewait,
        }

    def _build_data_builtin_map(self) -> Dict[str, Any]:
        return {
            "SAVEDATA": self._cmd_savedata,
            "LOADDATA": self._cmd_loaddata,
            "SAVEGLOBAL": self._cmd_saveglobal,
            "LOADGLOBAL": self._cmd_loadglobal,
        }

    def _build_variable_builtin_map(self) -> Dict[str, Any]:
        return {
            "SET": self._cmd_set,
            "ADD": self._cmd_add,
            "SUB": self._cmd_sub,
            "TIMES": self._cmd_times,
            "RAND": self._cmd_rand,
            "SWAP": self._cmd_swap,
        }

    def _build_array_builtin_map(self) -> Dict[str, Any]:
        return {
            "ARRAYSHIFT": self._cmdArrayshift,
            "ARRAYREMOVE": self._cmd_arrayremove,
            "VARSET": self._cmd_varset,
        }

    def _build_ui_builtin_map(self) -> Dict[str, Any]:
        return {
            "DRAWLINE": self._cmd_drawline,
            "CLEARLINE": self._cmd_clearline,
            "RESETCOLOR": self._cmd_resetcolor,
            "SETCOLOR": self._cmd_setcolor,
            "ALIGNMENT": self._cmd_alignment,
            "HTML_PRINT": self._cmd_html_print,
            "SETFONT": self._cmd_setfont,
        }

    def _build_character_builtin_map(self) -> Dict[str, Any]:
        return {
            "ADDCHARA": self._cmd_addchara,
            "DELCHARA": self._cmd_delchara,
            "RESETDATA": self._cmd_resetdata,
            "CHARAMADE": self._cmd_charamade,
        }

    def _build_system_builtin_map(self) -> Dict[str, Any]:
        return {
            "SIF": self._cmd_sif,
            "SELECTCASE": self._cmd_selectcase,
            "CASE": self._cmd_case,
            "ENDSELECT": self._cmd_endselect,
        }

    def _build_other_builtin_map(self) -> Dict[str, Any]:
        return {
            "LOCALS": self._cmd_locals,
            "CHKDATA": self._cmd_chkdata,
            "SAVENOS": self._cmd_savenos,
            "GETTIMES": self._cmd_gettimes,
            "STRLENS": self._cmd_strlens,
            "GETBIT": self._cmd_getbit,
            "SETBIT": self._cmd_setbit,
            "CLEARBIT": self._cmd_clearbit,
            "INRANGE": self._cmd_inrange,
            "LIMIT": self._cmd_limit,
            "MIN": self._cmd_min,
            "MAX": self._cmd_max,
            "ABS": self._cmd_abs,
            "SIGN": self._cmd_sign,
            "POWER": self._cmd_power,
            "SQRT": self._cmd_sqrt,
            "LOG": self._cmd_log,
            "EXP": self._cmd_exp,
            "SUM": self._cmd_sum,
            "FINDELEMENT": self._cmd_findelement,
            "FINDCHARA": self._cmd_findchara,
            "STRLEN": self._cmd_strlen,
            "STRLENU": self._cmd_strlenu,
            "SUBSTRING": self._cmd_substring,
            "SUBSTRINGU": self._cmd_substringu,
            "STRFIND": self._cmd_strfind,
            "STRFINDU": self._cmd_strfindu,
            "STRREPLACE": self._cmd_strreplace,
            "SPLIT": self._cmd_split,
            "REPLACE": self._cmd_replace,
            "UNICODE": self._cmd_unicode,
            "GETBIT": self._cmd_getbit,
            "SETBIT": self._cmd_setbit,
            "CLEARBIT": self._cmd_clearbit,
            "INRANGE": self._cmd_inrange,
            "LIMIT": self._cmd_limit,
            "BAR": self._cmd_bar,
            "BARSTR": self._cmd_barstr,
            "CUSTOMDRAWLINE": self._cmd_customdrawline,
        }

    def load_file(self, filepath: str):
        """Load ERB file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self._parse_erb(content)
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp932') as f:
                content = f.read()
                self._parse_erb(content)

    def _parse_erb(self, content: str):
        """Parse ERB content"""
        lines = content.split('\n')
        current_function = None

        for i, line in enumerate(lines):
            # Remove comments
            if ';' in line:
                line = line[:line.index(';')]

            line = line.strip()
            if not line:
                continue

            # Check for function definition
            if line.startswith('@'):
                func_match = re.match(r'@(\w+)', line)
                if func_match:
                    current_function = func_match.group(1)
                    self.functions[current_function] = len(self.lines)

            self.lines.append((current_function, line))

    def _get_paths(self):
        """Resolve game filesystem paths lazily."""
        if self.paths is None:
            self.paths = GamePaths(os.getcwd())
        self.paths.ensure_dirs()
        return self.paths


    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate ERB expression"""
        expr = expr.strip()

        try:
            literal = self._evaluate_expression_literal(expr)
            if literal is not None:
                return literal

            var_value = self._evaluate_expression_variable_reference(expr)
            if var_value is not None:
                return var_value

            ternary_value = self._evaluate_expression_ternary(expr)
            if ternary_value is not None:
                return ternary_value

            expr = self._replace_variables(expr)
            return self._evaluate_expression_arithmetic(expr)
        except:
            return expr

    def _evaluate_expression_literal(self, expr: str) -> Optional[str]:
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if expr.startswith("'") and expr.endswith("'"):
            return expr[1:-1]
        return None

    def _evaluate_expression_variable_reference(self, expr: str) -> Optional[Any]:
        if expr.startswith('%') and expr.endswith('%'):
            return self._get_variable(expr[1:-1])
        return None

    def _evaluate_expression_ternary(self, expr: str) -> Optional[Any]:
        if '?' not in expr or ':' not in expr:
            return None
        parts = expr.split('?')
        condition = parts[0].strip()
        rest = parts[1].split(':')
        true_val = rest[0].strip()
        false_val = rest[1].strip() if len(rest) > 1 else ""
        if self._evaluate_condition(condition):
            return self.evaluate_expression(true_val)
        return self.evaluate_expression(false_val)

    def _evaluate_expression_arithmetic(self, expr: str) -> Any:
        if '/' in expr and expr.count('/') == 1:
            parts = expr.split('/')
            left = self._eval_simple(parts[0])
            right = self._eval_simple(parts[1])
            if right == 0:
                return 0
            return int(left / right)

        if '*' in expr:
            parts = expr.split('*')
            result = 1
            for p in parts:
                result *= self._eval_simple(p)
            return result

        if '+' in expr:
            parts = expr.split('+')
            result = 0
            for p in parts:
                result += self._eval_simple(p)
            return result

        if '-' in expr and expr[0] != '-':
            parts = expr.split('-')
            result = self._eval_simple(parts[0])
            for p in parts[1:]:
                result -= self._eval_simple(p)
            return result

        return self._eval_simple(expr)

    def _eval_simple(self, expr: str) -> int:
        """Evaluate simple expression"""
        expr = expr.strip()
        try:
            return int(expr)
        except:
            pass

        try:
            return float(expr)
        except:
            pass

        # Handle operators like %, //, etc.
        if '%' in expr:
            parts = expr.split('%')
            left = self._eval_simple(parts[0])
            right = self._eval_simple(parts[1])
            return left % right

        if '//' in expr:
            parts = expr.split('//')
            left = self._eval_simple(parts[0])
            right = self._eval_simple(parts[1])
            return left // right

        return 0

    def _replace_variables(self, expr: str) -> str:
        """Replace ERB variable references with values"""
        expr = self._replace_variables_for_flags(expr)
        expr = self._replace_variables_for_global_state(expr)
        expr = self._replace_variables_for_character_values(expr)
        expr = self._replace_variables_for_identity_tokens(expr)
        expr = self._replace_variables_for_random_and_string_helpers(expr)
        return expr

    def _replace_variables_for_flags(self, expr: str) -> str:
        expr = re.sub(r'FLAG:(\d+)', r'self.vars.get_flag(\1)', expr)
        expr = re.sub(r'FLAG:(\d+):(\d+)', r'self.vars.get_char_flag(\1, \2)', expr)
        return expr

    def _replace_variables_for_global_state(self, expr: str) -> str:
        expr = re.sub(r'GLOBAL:(\d+)', r'self.globals.get(\1, 0)', expr)
        expr = re.sub(r'DAY:(\d+)', r'self.vars.day[\1]', expr)
        expr = re.sub(r'\bTIME\b', r'self.vars.time', expr)
        expr = re.sub(r'\bMONEY\b', r'self.vars.money', expr)
        return expr

    def _replace_variables_for_character_values(self, expr: str) -> str:
        expr = re.sub(r'TALENT:(\d+):(\d+)', r'self.vars.chars[\1].talent.get(\2, 0)', expr)
        expr = re.sub(r'ABL:(\d+):(\d+)', r'self.vars.chars[\1].get_abl(\2, 0)', expr)
        expr = re.sub(r'CFLAG:(\d+):(\d+)', r'self.vars.chars[\1].get_flag(\2, 0)', expr)
        expr = re.sub(r'BASE:(\d+):(\d+)', r'self.vars.chars[\1].base.get(\2, 0)', expr)
        expr = re.sub(r'MAXBASE:(\d+):(\d+)', r'self.vars.chars[\1].maxbase.get(\2, 0)', expr)
        expr = re.sub(r'EXP:(\d+):(\d+)', r'self.vars.chars[\1].exp.get(\2, 0)', expr)
        expr = re.sub(r'SOURCE:(\d+):(\d+)', r'self.vars.chars[\1].source.get(\2, 0)', expr)
        expr = re.sub(r'PALAM:(\d+):(\d+)', r'self.vars.chars[\1].palam.get(\2, 0)', expr)
        expr = re.sub(r'TEQUIP:(\d+):(\d+)', r'self.vars.chars[\1].equipt.get(\2, 0)', expr)
        expr = re.sub(r'TALENT:0:(\d+)', r'self.vars.chars[0].talent.get(\1, 0)', expr)
        expr = re.sub(r'CSTR:MASTER:(\d+)', r'self.vars.chars[0].cstr.get(\1, "")', expr)
        expr = re.sub(r'CSTR:(\d+):(\d+)', r'self.vars.chars[\1].cstr.get(\2, "")', expr)
        return expr

    def _replace_variables_for_identity_tokens(self, expr: str) -> str:
        expr = re.sub(r'\bTARGET\b', r'self.vars.target', expr)
        expr = re.sub(r'\bASSI\b', r'self.vars.assi', expr)
        expr = re.sub(r'\bMASTER\b', r'self.vars.master', expr)
        expr = re.sub(r'\bCHARANUM\b', r'len(self.vars.chars)', expr)
        expr = re.sub(r'\bRESULT\b', r'self.result', expr)
        return expr

    def _replace_variables_for_random_and_string_helpers(self, expr: str) -> str:
        expr = re.sub(r'RAND:(\d+)', r'random.randint(0, \1-1)', expr)
        expr = re.sub(r'STRLENS\((\w+)\)', r'len(str(\1))', expr)
        return expr

    def _get_variable(self, expr: str) -> Any:
        """Get variable value"""
        expr = expr.strip()

        flag_value = self._get_variable_flag_value(expr)
        if flag_value is not None:
            return flag_value

        talent_value = self._get_variable_talent_value(expr)
        if talent_value is not None:
            return talent_value

        abl_value = self._get_variable_ability_value(expr)
        if abl_value is not None:
            return abl_value

        base_value = self._get_variable_base_value(expr)
        if base_value is not None:
            return base_value

        return 0

    def _get_variable_flag_value(self, expr: str) -> Optional[int]:
        if not expr.startswith('FLAG:'):
            return None
        parts = expr[5:].split(':')
        if len(parts) == 1:
            return self.vars.get_flag(int(parts[0]))
        if len(parts) == 2:
            return self.vars.get_char_flag(int(parts[0]), int(parts[1]))
        return None

    def _get_variable_talent_value(self, expr: str) -> Optional[int]:
        if not expr.startswith('TALENT:'):
            return None
        parts = expr[7:].split(':')
        char_idx = 0 if parts[0] == 'MASTER' else int(parts[0])
        talent_idx = int(parts[1])
        if char_idx < len(self.vars.chars):
            return self.vars.chars[char_idx].talent.get(talent_idx, 0)
        return 0

    def _get_variable_ability_value(self, expr: str) -> Optional[int]:
        if not expr.startswith('ABL:'):
            return None
        parts = expr[4:].split(':')
        char_idx = int(parts[0])
        abl_idx = int(parts[1])
        if char_idx < len(self.vars.chars):
            return self.vars.chars[char_idx].get_abl(abl_idx, 0)
        return 0

    def _get_variable_base_value(self, expr: str) -> Optional[int]:
        if not expr.startswith('BASE:'):
            return None
        parts = expr[5:].split(':')
        char_idx = int(parts[0])
        base_idx = int(parts[1])
        if char_idx < len(self.vars.chars):
            return self.vars.chars[char_idx].base.get(base_idx, 0)
        return 0

    def _set_self_kojo_context(self, target: Character, tflag_13: int) -> None:
        self.vars.target = self._find_character_index(target)
        self.vars.q = 0
        self.vars.s = 0
        self.vars.n = 0
        self.vars.a = 0
        self.vars.b = 0
        self.vars.c = 0
        self.vars.tflag[13] = int(tflag_13)

    def _get_self_kojo_source_text(self, kojo_num: int) -> List[str]:
        if kojo_num not in self._self_kojo_source_cache:
            self._self_kojo_source_cache[kojo_num] = self._load_self_kojo_source_text(kojo_num)
        return self._self_kojo_source_cache[kojo_num]

    def _get_self_kojo_source_variants(self, kojo_num: int) -> List[tuple[str, int]]:
        if kojo_num == 1003:
            return [("903", 903)]
        if kojo_num == 1004:
            return [("904", 904)]
        if kojo_num in (903, 904):
            return [(str(kojo_num), kojo_num)]
        if 100 <= kojo_num <= 119:
            file_num = kojo_num - 100
            return [(str(file_num), file_num)]
        return [(str(kojo_num), kojo_num)]

    def _resolve_kojo_file_path(self, suffix: str) -> Optional[str]:
        """共享的 K 文件路径查找 - 用于 SELF_KOJO 和 NTR_KOUJO 等不同口上入口"""
        erb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ERB")
        candidates = [
            os.path.join(erb_dir, f"EVENT_K{suffix}.ERB"),
            os.path.join(erb_dir, f"EVENT_K{suffix}.erb"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        pattern = f"EVENT_K{suffix}_"
        for f in os.listdir(erb_dir):
            if f.upper().startswith(pattern.upper()) and f.lower().endswith(".erb"):
                return os.path.join(erb_dir, f)
        return None

    def _read_kojo_file_content(self, path: str) -> str:
        """共享的 K 文件读取（utf-8 优先，cp932 兜底）"""
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="cp932") as file:
                return file.read()

    def _load_self_kojo_source_text(self, kojo_num: int) -> List[str]:
        lines: List[str] = []
        for suffix, block_kojo_num in self._get_self_kojo_source_variants(kojo_num):
            path = self._resolve_kojo_file_path(suffix)
            if path is None:
                continue
            content = self._read_kojo_file_content(path)
            lines.extend(self._extract_self_kojo_block_lines(content, block_kojo_num))
        return lines

    def _extract_self_kojo_block_lines(self, content: str, kojo_num: int) -> List[str]:
        marker = f"@SELF_KOJO_K{kojo_num}"
        start = content.find(marker)
        if start < 0:
            return []
        block_start = content.find("\n", start) + 1
        if block_start == 0:
            block_start = start + len(marker)
        end = len(content)
        next_label = content.find("\n@", block_start)
        if next_label > block_start:
            end = next_label
        block = content[block_start:end]
        lines: List[str] = []
        for raw_line in block.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(";") or stripped.startswith("@"):
                continue
            lines.append(stripped)
        return lines

    def _format_self_kojo_string(self, text: str, target: Character, assistant: Optional[Character]) -> str:
        player = self._get_player()
        target_name = target.name or target.callname or "角色"
        master_name = player.name if player is not None and player.name else "主人"
        assistant_name = assistant.name if assistant is not None and assistant.name else "助手"
        target_call = target.callname or target.name or target_name
        assistant_call = assistant.callname if assistant is not None and assistant.callname else assistant_name
        target_index = self._find_character_index(target)
        target_cflag_261 = target.cflag.get(261, 0)
        target_cflag_262 = target.cflag.get(262, 0)
        target_cflag_263 = target.cflag.get(263, 0)
        target_cflag_264 = target.cflag.get(264, 0)
        target_cflag_265 = target.cflag.get(265, 0)
        replacements = [
            (r"%SAVESTR:TARGET%", target_name),
            (r"%SAVESTR:ASSI%", assistant_name),
            (r"%SAVESTR:MASTER%", master_name),
            (r"%SAVESTR:\(EX_FLAG:3\)%", target_name),
            (r"%SELF_CALL\(TARGET\)%", target_call),
            (r"%SELF_CALL\(ASSI\)%", assistant_call),
            (r"%CALLNAME:TARGET%", target_call),
            (r"%CALLNAME:ASSI%", assistant_call),
            (r"%CALLNAME:MASTER%", master_name),
            (r"%CALLNAME:0%", master_name),
            (r"%CALLNAME:ASSI%", assistant_call),
            (r"%NAME:TARGET%", target_name),
            (r"%NAME:ASSI%", assistant_name),
            (r"%NAME:MASTER%", master_name),
            (r"%UNICODE\(0x([0-9A-Fa-f]+)\) \*1%", lambda m: chr(int(m.group(1), 16))),
            (r"%UNICODE\((\d+)\) \*1%", lambda m: chr(int(m.group(1)))),
            (r"%UNICODE\(0x([0-9A-Fa-f]+)\) \*3%", lambda m: chr(int(m.group(1), 16)) * 3),
            (r"%UNICODE\((\d+)\) \*3%", lambda m: chr(int(m.group(1))) * 3),
            (r"%UNICODE\(0x([0-9A-Fa-f]+)\)%", lambda m: chr(int(m.group(1), 16))),
            (r"%UNICODE\((\d+)\)%", lambda m: chr(int(m.group(1)))),
        ]
        result = text
        for pattern, replacement in replacements:
            if callable(replacement):
                result = re.sub(pattern, replacement, result)
            else:
                result = re.sub(pattern, replacement, result)
        result = result.replace("%Q%", str(self.vars.q))
        result = result.replace("%S%", str(self.vars.s))
        result = result.replace("%N%", str(self.vars.n))
        result = result.replace("%A%", str(self.vars.a))
        result = result.replace("%B%", str(self.vars.b))
        result = result.replace("%C%", str(self.vars.c))
        result = result.replace("%CFLAG:261%", str(target_cflag_261))
        result = result.replace("%CFLAG:262%", str(target_cflag_262))
        result = result.replace("%CFLAG:263%", str(target_cflag_263))
        result = result.replace("%CFLAG:264%", str(target_cflag_264))
        result = result.replace("%CFLAG:265%", str(target_cflag_265))
        result = result.replace("%TARGET%", target_name)
        result = result.replace("%MASTER%", master_name)
        result = re.sub(r'%[^%]+%', '', result)
        return result

    def _parse_self_kojo_block(self, lines: List[str], target: Character) -> List[str]:
        assistant = self._get_current_assistant()
        parsed: List[str] = []
        index = 0
        while index < len(lines):
            raw_line = lines[index].strip()
            index += 1
            if not raw_line or raw_line.startswith(";") or raw_line.startswith("@"):
                continue
            if raw_line == "RETURN" or raw_line.startswith("RETURN "):
                break
            if raw_line.startswith("SIF "):
                cond = raw_line[4:].strip()
                if index < len(lines):
                    next_line = lines[index].strip()
                    index += 1
                    if self._evaluate_self_kojo_condition(cond, target, assistant):
                        if next_line == "RETURN" or next_line.startswith("RETURN "):
                            break
                        sub_parsed = self._parse_self_kojo_block([next_line], target)
                        parsed.extend(sub_parsed)
                continue
            if raw_line.startswith("IF "):
                block_lines, next_index = self._collect_self_kojo_branch(lines, index)
                branch = self._evaluate_self_kojo_branch(raw_line, block_lines, target, assistant)
                parsed.extend(branch)
                index = next_index
                continue
            if raw_line.startswith("ELSE") or raw_line == "ENDIF":
                continue
            self._apply_self_kojo_assignment(raw_line, target, assistant)
            rendered = self._render_self_kojo_command(raw_line, target, assistant)
            if rendered is not None:
                parsed.extend(rendered)
        return parsed

    def _collect_self_kojo_branch(self, lines: List[str], start_index: int) -> tuple[List[tuple[str, List[str]]], int]:
        blocks: List[tuple[str, List[str]]] = []
        current_header = ""
        current_lines: List[str] = []
        depth = 0
        index = start_index
        while index < len(lines):
            line = lines[index].strip()
            index += 1
            if not line or line.startswith(";"):
                continue
            if line.startswith("IF "):
                if depth == 0 and current_header == "":
                    current_header = line
                    current_lines = []
                    depth = 1
                    continue
                depth += 1
                current_lines.append(line)
                continue
            if line.startswith("SIF "):
                current_lines.append(line)
                if index < len(lines):
                    current_lines.append(lines[index].strip())
                    index += 1
                continue
            if line.startswith("ELSEIF ") and depth == 1:
                blocks.append((current_header, current_lines))
                current_header = line
                current_lines = []
                continue
            if line == "ELSE" and depth == 1:
                blocks.append((current_header, current_lines))
                current_header = line
                current_lines = []
                continue
            if line == "ENDIF":
                if depth == 1:
                    blocks.append((current_header, current_lines))
                    return blocks, index
                depth = max(0, depth - 1)
                current_lines.append(line)
                continue
            current_lines.append(line)
        if current_header:
            blocks.append((current_header, current_lines))
        return blocks, index

    def _evaluate_self_kojo_branch(self, header: str, blocks: List[tuple[str, List[str]]], target: Character, assistant: Optional[Character]) -> List[str]:
        header = header.strip()
        if header.startswith("SIF "):
            cond = header[4:].strip()
            return self._parse_self_kojo_block(blocks[0][1], target) if self._evaluate_self_kojo_condition(cond, target, assistant) else []
        for branch_header, branch_lines in blocks:
            if branch_header == "ELSE":
                return self._parse_self_kojo_block(branch_lines, target)
            if branch_header.startswith("IF "):
                cond = branch_header[3:].strip()
                if self._evaluate_self_kojo_condition(cond, target, assistant):
                    return self._parse_self_kojo_block(branch_lines, target)
            elif branch_header.startswith("ELSEIF "):
                cond = branch_header[7:].strip()
                if self._evaluate_self_kojo_condition(cond, target, assistant):
                    return self._parse_self_kojo_block(branch_lines, target)
        return []

    def _evaluate_self_kojo_condition(self, cond: str, target: Character, assistant: Optional[Character]) -> bool:
        cond = self._expand_self_kojo_condition(cond, target, assistant)
        try:
            return bool(eval(cond, {"__builtins__": {}}, {"random": random}))
        except Exception:
            return False

    def _expand_self_kojo_condition(self, cond: str, target: Character, assistant: Optional[Character]) -> str:
        target_idx = self._find_character_index(target)
        assistant_idx = self.interpreter.vars.assi if assistant is not None else -1
        target_indexed = self.interpreter.vars.target
        replacements = [
            (r"\bTARGET\b", str(target_idx)),
            (r"\bASSI\b", str(assistant_idx)),
            (r"\bMASTER\b", "0"),
            (r"\bQ\b", str(self.vars.q)),
            (r"\bS\b", str(self.vars.s)),
            (r"\bN\b", str(self.vars.n)),
            (r"\bA\b", str(self.vars.a)),
            (r"\bB\b", str(self.vars.b)),
            (r"\bC\b", str(self.vars.c)),
            (r"TALENT:ASSI:(\d+)", lambda m: str(assistant.talent.get(int(m.group(1)), 0) if assistant is not None else 0)),
            (r"ABL:ASSI:(\d+)", lambda m: str(assistant.abl.get(int(m.group(1)), 0) if assistant is not None else 0)),
            (r"TALENT:TARGET:(\d+)", lambda m: str(target.talent.get(int(m.group(1)), 0))),
            (r"ABL:TARGET:(\d+)", lambda m: str(target.abl.get(int(m.group(1)), 0))),
            (r"TALENT:MASTER:(\d+)", lambda m: str(self.vars.chars[0].talent.get(int(m.group(1)), 0) if self.vars.chars else 0)),
            (r"ABL:MASTER:(\d+)", lambda m: str(self.vars.chars[0].abl.get(int(m.group(1)), 0) if self.vars.chars else 0)),
            (r"CFLAG:TARGET:(\d+)", lambda m: str(target.cflag.get(int(m.group(1)), 0))),
            (r"CFLAG:ASSI:(\d+)", lambda m: str(assistant.cflag.get(int(m.group(1)), 0) if assistant is not None else 0)),
            (r"CFLAG:MASTER:(\d+)", lambda m: str(self.vars.chars[0].cflag.get(int(m.group(1)), 0) if self.vars.chars else 0)),
            (r"EXP:TARGET:(\d+)", lambda m: str(target.exp.get(int(m.group(1)), 0))),
            (r"MARK:TARGET:(\d+)", lambda m: str(target.mark.get(int(m.group(1)), 0) if hasattr(target, 'mark') else 0)),
            (r"JUEL:TARGET:(\d+)", lambda m: str(target.juel.get(int(m.group(1)), 0) if hasattr(target, 'juel') else 0)),
            (r"TALENT:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].talent.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"ABL:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].abl.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"CFLAG:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].cflag.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"BASE:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].base.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"EXP:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].exp.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"PALAM:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].palam.get(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"TFLAG:(\d+):(\d+)", lambda m: str(self.vars.tflag.get(int(m.group(2)), 0) if int(m.group(1)) == 0 else 0)),
            (r"TFLAG:(\d+)", lambda m: str(self.vars.tflag.get(int(m.group(1)), 0))),
            (r"FLAG:(\d+):(\d+)", lambda m: str(self.vars.chars[int(m.group(1))].get_flag(int(m.group(2)), 0)) if int(m.group(1)) < len(self.vars.chars) else "0"),
            (r"FLAG:(\d+)", lambda m: str(self.vars.get_flag(int(m.group(1)), 0))),
            (r"CFLAG:(\d+)", lambda m: str(target.cflag.get(int(m.group(1)), 0))),
            (r"TALENT:(\d+)", lambda m: str(target.talent.get(int(m.group(1)), 0))),
            (r"ABL:(\d+)", lambda m: str(target.abl.get(int(m.group(1)), 0))),
            (r"EXP:(\d+)", lambda m: str(target.exp.get(int(m.group(1)), 0))),
            (r"MARK:(\d+)", lambda m: str(target.mark.get(int(m.group(1)), 0) if hasattr(target, 'mark') else 0)),
            (r"JUEL:(\d+)", lambda m: str(target.juel.get(int(m.group(1)), 0) if hasattr(target, 'juel') else 0)),
            (r"NOWEX:(\d+)", lambda m: str(target.nowex.get(int(m.group(1)), 0) if hasattr(target, 'nowex') else 0)),
            (r"RESULT", lambda m: str(self.result)),
            (r"DAY:(\d+)", lambda m: str(self.vars.day[int(m.group(1))])),
            (r"TIME", lambda m: str(self.vars.time)),
            (r"ITEM:(\d+)", lambda m: str(self.vars.item[int(m.group(1))] if int(m.group(1)) < len(self.vars.item) else 0)),
            (r"RAND:(\d+)", lambda m: str(random.randint(0, max(0, int(m.group(1)) - 1)))),
            (r"CALLNAME:MASTER", lambda m: str(self.vars.chars[0].callname if self.vars.chars and self.vars.chars[0].callname else "主人")),
            (r"CALLNAME:ASSI", lambda m: str(assistant.callname if assistant is not None and assistant.callname else assistant.name if assistant is not None else "助手")),
            (r"CALLNAME:TARGET", lambda m: str(target.callname if target.callname else target.name)),
            (r"SAVESTR:TARGET", lambda m: str(target.name or target.callname or "角色")),
            (r"SAVESTR:ASSI", lambda m: str(assistant.name if assistant is not None else "助手")),
            (r"SAVESTR:MASTER", lambda m: str(self.vars.chars[0].name if self.vars.chars and self.vars.chars[0].name else "主人")),
            (r"SELF_CALL\(TARGET\)", lambda m: str(target.callname or target.name or "角色")),
            (r"SELF_CALL\(ASSI\)", lambda m: str(assistant.callname if assistant is not None and assistant.callname else assistant.name if assistant is not None else "助手")),
        ]
        result = cond
        for pattern, replacement in replacements:
            if callable(replacement):
                result = re.sub(pattern, replacement, result)
            else:
                result = re.sub(pattern, replacement, result)
        result = result.replace("CALLNAME:MASTER", str(self.vars.chars[0].callname if self.vars.chars and self.vars.chars[0].callname else "主人"))
        result = result.replace("CALLNAME:ASSI", str(assistant.callname if assistant is not None and assistant.callname else assistant.name if assistant is not None else "助手"))
        result = result.replace("CALLNAME:TARGET", str(target.callname if target.callname else target.name))
        result = result.replace("&&", " and ").replace("||", " or ")
        result = re.sub(r'!(?![=])', ' not ', result)
        return result

    def _apply_self_kojo_assignment(self, line: str, target: Character, assistant: Optional[Character]) -> None:
        if "=" not in line:
            return
        left, right = [part.strip() for part in line.split("=", 1)]
        try:
            value = int(self.evaluate_expression(right))
        except Exception:
            value = 0
        if left == "Q":
            self.vars.q = value
        elif left == "S":
            self.vars.s = value
        elif left == "N":
            self.vars.n = value
        elif left == "A":
            self.vars.a = value
        elif left == "B":
            self.vars.b = value
        elif left == "C":
            self.vars.c = value
        else:
            self._apply_self_kojo_target_assignment(left, value, target, assistant)

    def _apply_self_kojo_target_assignment(self, left: str, value: int, target: Character, assistant: Optional[Character]) -> None:
        """处理 SELF_KOJO 里的 CFLAG/TALENT/ABL/TFLAG 等赋值"""
        import re
        m = re.match(r"CFLAG:TARGET:(\d+)", left)
        if m:
            target.cflag[int(m.group(1))] = value
            return
        m = re.match(r"CFLAG:ASSI:(\d+)", left)
        if m and assistant is not None:
            assistant.cflag[int(m.group(1))] = value
            return
        m = re.match(r"CFLAG:MASTER:(\d+)", left)
        if m and self.vars.chars:
            self.vars.chars[0].cflag[int(m.group(1))] = value
            return
        m = re.match(r"CFLAG:(\d+):(\d+)", left)
        if m:
            idx = int(m.group(1))
            if idx < len(self.vars.chars):
                self.vars.chars[idx].cflag[int(m.group(2))] = value
            return
        m = re.match(r"CFLAG:(\d+)", left)
        if m:
            target.cflag[int(m.group(1))] = value
            return
        m = re.match(r"TALENT:TARGET:(\d+)", left)
        if m:
            target.talent[int(m.group(1))] = value
            return
        m = re.match(r"TALENT:(\d+)", left)
        if m:
            target.talent[int(m.group(1))] = value
            return
        m = re.match(r"ABL:TARGET:(\d+)", left)
        if m:
            target.abl[int(m.group(1))] = value
            return
        m = re.match(r"ABL:(\d+)", left)
        if m:
            target.abl[int(m.group(1))] = value
            return
        m = re.match(r"EXP:TARGET:(\d+)", left)
        if m:
            target.exp[int(m.group(1))] = value
            return
        m = re.match(r"TFLAG:(\d+)", left)
        if m:
            self.vars.tflag[int(m.group(1))] = value
            return
        m = re.match(r"FLAG:(\d+)", left)
        if m:
            self.vars.set_flag(int(m.group(1)), value)
            return

    def _render_self_kojo_command(self, line: str, target: Character, assistant: Optional[Character]) -> List[str]:
        if line.startswith("DRAWLINE"):
            return ["-" * 50]
        if line.startswith("PRINTFORML ") or line.startswith("PRINTFORMW ") or line.startswith("PRINTFORM "):
            text = line.split(" ", 1)[1] if " " in line else ""
            formatted = self._format_self_kojo_string(text, target, assistant)
            return [formatted]
        if line.startswith("PRINTL ") or line.startswith("PRINTW "):
            text = line.split(" ", 1)[1] if " " in line else ""
            formatted = self._format_self_kojo_string(text, target, assistant)
            return [formatted]
        if line == "PRINTL" or line == "PRINTW" or line == "PRINTFORMW":
            return [""]
        if line.startswith("PRINT "):
            text = line.split(" ", 1)[1] if " " in line else ""
            formatted = self._format_self_kojo_string(text, target, assistant)
            return [formatted]
        if line.startswith("CALL "):
            return []
        return []

    def _evaluate_condition(self, cond: str) -> bool:
        """Evaluate condition"""
        cond = cond.strip()
        cond = self._replace_variables(cond)
        comparison = self._evaluate_condition_comparison(cond)
        if comparison is not None:
            return comparison
        logic = self._evaluate_condition_logic(cond)
        if logic is not None:
            return logic
        return self._evaluate_condition_truthiness(cond)

    def _evaluate_condition_comparison(self, cond: str) -> Optional[bool]:
        operators = ["==", "!=", ">=", "<=", ">", "<"]
        for operator in operators:
            if operator not in cond:
                continue
            parts = cond.split(operator)
            left = self._eval_simple(parts[0])
            right = self._eval_simple(parts[1])
            if operator == "==":
                return left == right
            if operator == "!=":
                return left != right
            if operator == ">=":
                return left >= right
            if operator == "<=":
                return left <= right
            if operator == ">":
                return left > right
            if operator == "<":
                return left < right
        return None

    def _evaluate_condition_logic(self, cond: str) -> Optional[bool]:
        upper = cond.upper()
        if ' && ' in cond or ' AND ' in upper:
            parts = re.split(r' && | AND ', cond, flags=re.IGNORECASE)
            return all(self._evaluate_condition(p) for p in parts)
        if ' || ' in cond or ' OR ' in upper:
            parts = re.split(r' \|\| | OR ', cond, flags=re.IGNORECASE)
            return any(self._evaluate_condition(p) for p in parts)
        return None

    def _evaluate_condition_truthiness(self, cond: str) -> bool:
        try:
            return bool(self._eval_simple(cond))
        except:
            return False

    # ==================== Built-in Commands ====================

    def _cmd_print(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printl(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text + "\n")

    def _cmd_printv(self, args):
        val = self.evaluate_expression(args[0] if args else "0")
        self.output_buffer.append(str(val))

    def _cmd_printforml(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text + "\n")

    def _cmd_printform(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printforms(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printforc(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printbutton(self, args):
        if len(args) >= 2:
            text = self._format_string(args[0])
            self.output_buffer.append(f"[{args[1]}] {text}")
        elif args:
            self.output_buffer.append(args[0])

    def _cmd_printbuttonforml(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(f"[{args[1]}] {text}\n")

    def _cmd_prints(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printc(self, args):
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_printw(self, args):
        """PRINTW - 打印并等待按键"""
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text + "\n")
        self.output_buffer.append("[等待按键...]")

    def _cmd_printformw(self, args):
        """PRINTFORMW - 格式化打印并等待按键"""
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text + "\n")
        self.output_buffer.append("[等待按键...]")

    def _cmd_printlc(self, args):
        """PRINTLC - 左对齐打印（不换行）"""
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text.ljust(20))

    def _cmd_printvl(self, args):
        """PRINTVL - 打印变量并换行"""
        val = self.evaluate_expression(args[0]) if args else ""
        self.output_buffer.append(str(val) + "\n")

    def _format_string(self, s: str) -> str:
        """Format string with variables"""
        # Handle %VAR% format
        def replace_var(m):
            var = m.group(1)
            return str(self._get_variable(var))

        # Handle {expr} format
        def replace_expr(m):
            expr = m.group(1)
            return str(self.evaluate_expression(expr))

        # Handle {expr:format} format
        def replace_format(m):
            expr = m.group(1)
            fmt = m.group(2)
            val = self.evaluate_expression(expr)
            if ',' in fmt:
                parts = fmt.split(',')
                width = int(parts[0])
                return str(val).rjust(width)
            return str(val)

        s = re.sub(r'%([^%]+)%', replace_var, s)
        s = re.sub(r'\{(\d+)\}', replace_expr, s)
        s = re.sub(r'\{([^:}]+):([^}]+)\}', replace_format, s)

        return s

    def _cmd_drawline(self, args):
        self.output_buffer.append("-" * 50 + "\n")

    def _cmd_clearline(self, args):
        if args:
            lines = int(self.evaluate_expression(args[0]))
            # Clear from buffer
            for _ in range(min(lines, len(self.output_buffer))):
                if self.output_buffer and self.output_buffer[-1].endswith('\n'):
                    self.output_buffer.pop()
        else:
            if self.output_buffer and self.output_buffer[-1].endswith('\n'):
                self.output_buffer.pop()

    def _cmd_resetcolor(self, args):
        self.output_buffer.append("\033[0m")

    def _cmd_setcolor(self, args):
        # Simple color support
        pass

    def _cmd_alignment(self, args):
        # Alignment - just pass through
        pass

    def _cmd_html_print(self, args):
        # HTML print - just show text
        text = self._format_string(args[0] if args else "")
        self.output_buffer.append(text)

    def _cmd_setfont(self, args):
        pass

    def _cmd_if(self, args):
        cond = args[0] if args else ""
        return self._evaluate_condition(cond)

    def _cmd_else(self, args):
        return True

    def _cmd_elseif(self, args):
        cond = args[0] if args else ""
        return self._evaluate_condition(cond)

    def _cmd_endif(self, args):
        return True

    def _cmd_goto(self, args):
        label = args[0] if args else ""
        # Find label position
        for i, (func, line) in enumerate(self.lines):
            if line.startswith(f'${label}'):
                return i
        return None

    def _cmd_call(self, args):
        func_name = args[0] if args else ""
        if func_name in self.functions:
            return self.functions[func_name]
        return None

    def call_erb_function(self, func_name: str, *args) -> List[str]:
        """Call an ERB function by name and return its output.
        
        This enables Python code to directly invoke ERB-defined functions
        (like EVENT_K dialogue events) without translating them to Python.
        """
        if func_name not in self.functions:
            return [f"[ERB函数未找到: {func_name}]"]
        
        saved_line = self.current_line
        saved_output = self.output_buffer
        self.output_buffer = []
        
        # Set ARG/ARGS if provided
        for i, arg in enumerate(args):
            if isinstance(arg, int):
                self.vars.set_arg(i, arg)
            elif isinstance(arg, str):
                self.vars.set_args(i, arg)
        
        # Execute from function start until RETURN
        start_idx = self.functions[func_name]
        self.current_line = start_idx
        max_lines = len(self.lines)
        if_stack = []
        skip_depth = 0
        
        while self.current_line < max_lines:
            try:
                _, line = self.lines[self.current_line]
            
                # Stop at next function definition
                if line.startswith('@') and self.current_line > start_idx:
                    break
            
                self.current_line += 1
            
                # Handle IF/ELSEIF/ELSE/ENDIF
                if line.startswith('IF '):
                    cond = self._evaluate_condition(line[3:])
                    if_stack.append((cond, skip_depth))
                    if not cond or skip_depth > 0:
                        skip_depth += 1
                    continue
            
                if line.startswith('ELSEIF '):
                    if if_stack:
                        prev_cond, base_skip = if_stack[-1]
                        if base_skip > 0:
                            # Already in a skipped branch, stay skipped
                            pass
                        elif prev_cond:
                            # Previous branch was taken, skip this one
                            skip_depth = base_skip + 1
                            if_stack[-1] = (False, base_skip)
                        else:
                            # Check this condition
                            cond = self._evaluate_condition(line[7:])
                            if_stack[-1] = (cond, base_skip)
                            if cond:
                                skip_depth = base_skip
                            else:
                                skip_depth = base_skip + 1
                    continue
            
                if line == 'ELSE':
                    if if_stack:
                        prev_cond, base_skip = if_stack[-1]
                        if prev_cond and base_skip == skip_depth - 1:
                            skip_depth = base_skip
                        else:
                            skip_depth = base_skip + 1
                        if_stack[-1] = (not prev_cond, base_skip)
                    continue
            
                if line == 'ENDIF':
                    if if_stack:
                        _, base_skip = if_stack.pop()
                        skip_depth = base_skip
                    continue
            
                # Skip lines in false IF branches
                if skip_depth > 0:
                    continue
            
                # Handle RETURN
                if line.startswith('RETURN') and not line.startswith('RETURNF'):
                    if len(line) > 6 and line[6] != ' ':
                        pass  # Not a plain RETURN
                    else:
                        ret_val = line[7:].strip() if len(line) > 6 else ""
                        if ret_val:
                            try:
                                self.result = int(self.evaluate_expression(ret_val))
                            except:
                                self.result = 0
                        break
            
                # Handle PRINT commands
                if line.startswith('PRINTL'):
                    text = line[6:].strip() if len(line) > 6 else ""
                    text = self._interpolate_text(text)
                    self.output_buffer.append(text)
                    continue
            
                if line.startswith('PRINTFORML'):
                    text = line[10:].strip() if len(line) > 10 else ""
                    text = self._interpolate_text(text)
                    self.output_buffer.append(text)
                    continue
            
                if line.startswith('PRINTW'):
                    text = line[6:].strip() if len(line) > 6 else ""
                    text = self._interpolate_text(text)
                    self.output_buffer.append(text)
                    continue
            
                if line.startswith('PRINTFORMW'):
                    text = line[10:].strip() if len(line) > 10 else ""
                    text = self._interpolate_text(text)
                    self.output_buffer.append(text)
                    continue
            
                if line.startswith('PRINT '):
                    text = line[6:].strip()
                    text = self._interpolate_text(text)
                    if self.output_buffer:
                        self.output_buffer[-1] += text
                    else:
                        self.output_buffer.append(text)
                    continue
            
                if line.startswith('PRINTFORM '):
                    text = line[10:].strip()
                    text = self._interpolate_text(text)
                    if self.output_buffer:
                        self.output_buffer[-1] += text
                    else:
                        self.output_buffer.append(text)
                    continue
            
                # Handle CALL (recursive)
                if line.startswith('CALL '):
                    parts = line[5:].strip().split(',')
                    sub_func = parts[0].strip()
                    sub_args = [p.strip() for p in parts[1:]]
                    sub_output = self.call_erb_function(sub_func, *sub_args)
                    self.output_buffer.extend(sub_output)
                    continue
            
                # Handle SIF (single-line if)
                if line.startswith('SIF '):
                    cond_part = line[4:].strip()
                    if not self._evaluate_condition(cond_part):
                        self.current_line += 1  # Skip next line
                    continue
            
                # Handle SELECTCASE / CASE / CASEELSE / ENDSELECT
                if line.startswith('SELECTCASE '):
                    select_expr = line[11:].strip()
                    select_val = self.evaluate_expression(select_expr)
                    if_stack.append(('SELECT', select_val, skip_depth))
                    continue

                if line.startswith('CASE '):
                    if if_stack and if_stack[-1][0] == 'SELECT':
                        _, select_val, base_skip = if_stack[-1]
                        case_vals = [v.strip() for v in line[5:].split(',')]
                        matched = any(str(select_val) == str(self.evaluate_expression(cv)) for cv in case_vals)
                        if matched:
                            skip_depth = base_skip
                        else:
                            skip_depth = base_skip + 1
                    continue

                if line == 'CASEELSE':
                    if if_stack and if_stack[-1][0] == 'SELECT':
                        _, select_val, base_skip = if_stack[-1]
                        if skip_depth == base_skip + 1:
                            skip_depth = base_skip
                        else:
                            skip_depth = base_skip + 1
                    continue

                if line == 'ENDSELECT':
                    if if_stack and if_stack[-1][0] == 'SELECT':
                        _, _, base_skip = if_stack.pop()
                        skip_depth = base_skip
                    continue

                # Handle GOTO label
                if line.startswith('GOTO '):
                    label = line[5:].strip()
                    for i in range(self.current_line, min(self.current_line + 1000, len(self.lines))):
                        if self.lines[i][1].startswith(f'${label}'):
                            self.current_line = i
                            break
                    continue

                # Handle STRFORM
                if line.startswith('STRFORM '):
                    parts = line[8:].split('=', 1)
                    if len(parts) == 2:
                        var_name = parts[0].strip()
                        text = parts[1].strip().strip('"')
                        text = self._interpolate_text(text)
                        self._set_variable(var_name, text)
                    continue

                # Skip LOCAL / LOCALS declarations and #DIM / #DIMS
                if line.startswith('LOCAL ') or line.startswith('LOCALS ') or line.startswith('#DIM') or line.startswith('#DIMS'):
                    continue

                # Skip SPLIT
                if line.startswith('SPLIT '):
                    continue

                # Skip REUSELASTLINE
                if line.startswith('REUSELASTLINE'):
                    continue

                # Skip TINPUT / INPUT (auto-respond in ERB execution mode)
                if line.startswith('TINPUT') or line.startswith('INPUT'):
                    continue

                # Handle CONTINUE (loop continue)
                if line == 'CONTINUE':
                    continue

                # Handle BREAK (loop break)
                if line == 'BREAK':
                    break

                # Handle JUMP (replace current execution)
                if line.startswith('JUMP '):
                    target_func = line[5:].strip()
                    if target_func in self.functions:
                        self.current_line = self.functions[target_func]
                    continue

                # Handle TRYCALL
                if line.startswith('TRYCALL '):
                    func = line[8:].strip()
                    if func in self.functions:
                        sub_output = self.call_erb_function(func)
                        self.output_buffer.extend(sub_output)
                    continue

                # Handle TRYJUMP
                if line.startswith('TRYJUMP '):
                    func = line[8:].strip()
                    if func in self.functions:
                        self.current_line = self.functions[func]
                    continue

                # Handle CALLEVENT
                if line.startswith('CALLEVENT '):
                    func = line[10:].strip()
                    if func in self.functions:
                        sub_output = self.call_erb_function(func)
                        self.output_buffer.extend(sub_output)
                    continue

                # Handle DO-LOOP
                if line.startswith('DO '):
                    loop_start = self.current_line - 1
                    if_stack.append(('DO', loop_start, skip_depth))
                    continue

                if line == 'LOOP':
                    if if_stack and if_stack[-1][0] == 'DO':
                        _, loop_start, base_skip = if_stack[-1]
                        if skip_depth > base_skip:
                            # Skip this iteration
                            pass
                        else:
                            # Loop back
                            self.current_line = loop_start
                            continue
                    continue

                # Handle FOR-NEXT
                if line.startswith('FOR '):
                    # FOR COUNT, 0, 10
                    parts = line[4:].split(',')
                    if len(parts) >= 3:
                        var_name = parts[0].strip()
                        start_val = int(self.evaluate_expression(parts[1].strip()))
                        end_val = int(self.evaluate_expression(parts[2].strip()))
                        step = int(self.evaluate_expression(parts[3].strip())) if len(parts) > 3 else 1
                        self._set_variable(var_name, start_val)
                        if_stack.append(('FOR', var_name, end_val, step, self.current_line - 1, skip_depth))
                        if start_val >= end_val:
                            skip_depth += 1
                    continue

                if line == 'NEXT':
                    if if_stack and if_stack[-1][0] == 'FOR':
                        _, var_name, end_val, step, loop_start, base_skip = if_stack[-1]
                        current_val = int(self._get_variable(var_name) or 0)
                        current_val += step
                        self._set_variable(var_name, current_val)
                        if current_val < end_val:
                            self.current_line = loop_start
                        else:
                            if_stack.pop()
                            skip_depth = base_skip
                    continue

                # Handle STRLEN
                if line.startswith('STRLEN '):
                    var_expr = line[7:].strip()
                    val = self._get_variable(var_expr)
                    self.result = len(str(val)) if val else 0
                    continue

                # Handle STRLENS
                if line.startswith('STRLENS '):
                    var_expr = line[8:].strip()
                    val = self._get_variable(var_expr)
                    self.result = len(str(val)) if val else 0
                    continue

                # Handle SUBSTRINGU
                if line.startswith('SUBSTRINGU '):
                    # SUBSTRINGU var, start, length
                    parts = line[11:].split(',')
                    if len(parts) >= 3:
                        val = str(self._get_variable(parts[0].strip()) or "")
                        start = int(self.evaluate_expression(parts[1].strip()))
                        length = int(self.evaluate_expression(parts[2].strip()))
                        self._set_variable(parts[0].strip(), val[start:start+length])
                    continue

                # Handle DRAWLINE
                if line == 'DRAWLINE':
                    self.output_buffer.append("-" * 40)
                    continue

                # Handle CLEARLINE
                if line.startswith('CLEARLINE'):
                    continue

                # Handle WAIT / WAITANYKEY
                if line.startswith('WAIT'):
                    continue

                # Handle FONTSTYLE
                if line.startswith('FONTSTYLE'):
                    continue

                # Handle SETCOLOR
                if line.startswith('SETCOLOR'):
                    continue

                # Handle RESETCOLOR
                if line == 'RESETCOLOR':
                    continue

                # Handle SETBGCOLOR
                if line.startswith('SETBGCOLOR'):
                    continue

                # Handle BAR
                if line.startswith('BAR '):
                    continue

                # Handle variable assignments (TALENT:X = Y, etc.)
                if '=' in line and not line.startswith('PRINT'):
                    self._execute_assignment(line)
                    continue
            
                # Handle TIMES
                if line.startswith('TIMES '):
                    self._execute_times(line)
                    continue
        
            except Exception as e:
                # Log error but continue execution
                self.output_buffer.append(f"[ERB Error at line {self.current_line}: {str(e)[:100]}]")
                continue
        result = self.output_buffer[:]
        self.output_buffer = saved_output
        self.current_line = saved_line
        return result

    def _interpolate_text(self, text: str) -> str:
        """Replace ERB variable references in text with their values."""
        # Replace %VAR% patterns
        import re
        def replace_var(m):
            var_expr = m.group(1)
            try:
                val = self._get_variable(var_expr)
                return str(val) if val is not None else m.group(0)
            except:
                return m.group(0)
        text = re.sub(r'%([^%]+)%', replace_var, text)
        
        # Replace {expression} patterns
        def replace_expr(m):
            expr = m.group(1)
            try:
                return str(self.evaluate_expression(expr))
            except:
                return m.group(0)
        text = re.sub(r'\{([^}]+)\}', replace_expr, text)
        
        return text

    def _execute_assignment(self, line: str):
        """Execute a variable assignment line like TALENT:0 = 1"""
        if '==' in line or '!=' in line or '>=' in line or '<=' in line:
            return  # Comparison, not assignment
        parts = line.split('=', 1)
        if len(parts) != 2:
            return
        var_expr = parts[0].strip()
        val_expr = parts[1].strip()
        try:
            val = self.evaluate_expression(val_expr)
            self._set_variable(var_expr, val)
        except:
            pass

    def _execute_times(self, line: str):
        """Execute TIMES B, 0.80 style multiplication"""
        parts = line[6:].split(',')
        if len(parts) != 2:
            return
        var_expr = parts[0].strip()
        mult = float(parts[1].strip())
        try:
            current = self._get_variable(var_expr)
            if current is not None:
                new_val = int(float(current) * mult)
                self._set_variable(var_expr, new_val)
        except:
            pass

    def _cmd_return(self, args):
        if args:
            self.result = self.evaluate_expression(args[0])
        return -1

    def _cmd_restart(self, args):
        self.vars = ERBVariable()
        self.running = True
        return -2

    def _cmd_begin(self, args):
        state = args[0] if args else "SHOP"
        self.current_state = state
        return -3

    # ========================================
    # 循环控制指令 (REPEAT/FOR/CONTINUE/BREAK/DO/LOOP/WHILE)
    # ========================================
    def _cmd_repeat(self, args):
        """REPEAT n - 开始循环，循环变量为 COUNT，从 0 到 n-1"""
        if args:
            count = int(self.evaluate_expression(args[0]))
            self._loop_stack.append({
                'type': 'REPEAT',
                'count': count,
                'current': 0,
                'start_line': self.current_line
            })
            self.vars.count = 0
        return None

    def _cmd_rend(self, args):
        """REND - 结束 REPEAT 循环"""
        if self._loop_stack:
            loop = self._loop_stack[-1]
            loop['current'] += 1
            if loop['current'] < loop['count']:
                self.vars.count = loop['current']
                return loop['start_line']  # 返回到循环开始
            else:
                self._loop_stack.pop()
        return None

    def _cmd_for(self, args):
        """FOR var, start, end[, step] - 增强循环"""
        var_name = args[0] if args else 'COUNT'
        start = int(self.evaluate_expression(args[1])) if len(args) > 1 else 0
        end = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        step = int(self.evaluate_expression(args[3])) if len(args) > 3 else 1
        
        self._loop_stack.append({
            'type': 'FOR',
            'var': var_name,
            'start': start,
            'end': end,
            'step': step,
            'current': start,
            'start_line': self.current_line
        })
        self._set_variable(var_name, start)
        return None

    def _cmd_next(self, args):
        """NEXT - 结束 FOR 循环"""
        if self._loop_stack:
            loop = self._loop_stack[-1]
            loop['current'] += loop['step']
            if (loop['step'] > 0 and loop['current'] < loop['end']) or \
               (loop['step'] < 0 and loop['current'] > loop['end']):
                self._set_variable(loop['var'], loop['current'])
                return loop['start_line']
            else:
                self._loop_stack.pop()
        return None

    def _cmd_continue(self, args):
        """CONTINUE - 跳过当前循环迭代"""
        if self._loop_stack:
            loop = self._loop_stack[-1]
            if loop['type'] == 'REPEAT':
                loop['current'] += 1
                if loop['current'] < loop['count']:
                    self.vars.count = loop['current']
                    return ('continue', loop['start_line'])
                else:
                    self._loop_stack.pop()
            elif loop['type'] == 'FOR':
                loop['current'] += loop['step']
                if (loop['step'] > 0 and loop['current'] < loop['end']) or \
                   (loop['step'] < 0 and loop['current'] > loop['end']):
                    self._set_variable(loop['var'], loop['current'])
                    return ('continue', loop['start_line'])
                else:
                    self._loop_stack.pop()
        return None

    def _cmd_break(self, args):
        """BREAK - 跳出循环"""
        if self._loop_stack:
            self._loop_stack.pop()
        return ('break', None)

    def _cmd_do(self, args):
        """DO - 开始 DO-LOOP 循环"""
        self._loop_stack.append({
            'type': 'DO',
            'start_line': self.current_line,
            'condition': None,
            'check_end': False
        })
        return None

    def _cmd_loop(self, args):
        """LOOP [condition] - 结束 DO 循环"""
        if self._loop_stack and self._loop_stack[-1]['type'] == 'DO':
            loop = self._loop_stack[-1]
            if args:
                cond = args[0]
                if self._evaluate_condition(cond):
                    self._loop_stack.pop()
                    return None
            return loop['start_line']
        return None

    def _cmd_while(self, args):
        """WHILE condition - 开始 WHILE 循环"""
        cond = args[0] if args else "1"
        self._loop_stack.append({
            'type': 'WHILE',
            'condition': cond,
            'start_line': self.current_line
        })
        if not self._evaluate_condition(cond):
            self._loop_stack.pop()
            return ('break', None)
        return None

    def _cmd_endwhile(self, args):
        """ENDWHILE - 结束 WHILE 循环"""
        if self._loop_stack and self._loop_stack[-1]['type'] == 'WHILE':
            loop = self._loop_stack[-1]
            if self._evaluate_condition(loop['condition']):
                return loop['start_line']
            else:
                self._loop_stack.pop()
        return None

    def _cmd_input(self, args):
        return self._get_input()

    def _cmd_inputs(self, args):
        return self._get_input_str()

    def _cmd_tinput(self, args):
        default = int(args[0]) if args else 0
        return self._get_input(default)

    def _cmd_tinputs(self, args):
        default = args[0] if args else ""
        return self._get_input_str(default)

    def _cmd_oneinput(self, args):
        """ONEINPUT - 单字符输入"""
        return self._get_input()

    def _cmd_wait(self, args):
        """WAIT - 等待按键"""
        self.output_buffer.append("[等待按键...]")
        return None

    def _cmd_forcewait(self, args):
        """FORCEWAIT - 强制等待按键"""
        self.output_buffer.append("[强制等待按键...]")
        return None

    def _cmd_swap(self, args):
        """SWAP var1, var2 - 交换两个变量的值"""
        if len(args) < 2:
            return None
        var1 = args[0]
        var2 = args[1]
        val1 = self._get_variable(var1)
        val2 = self._get_variable(var2)
        self._set_variable(var1, val2)
        self._set_variable(var2, val1)
        return None

    def _read_input(self, prompt: str = "") -> str:
        return safe_input(prompt)

    def _read_input_stripped(self, prompt: str = "") -> str:
        return self._read_input(prompt).strip()

    def _get_input(self, default: int = 0) -> int:
        """Get numeric input from user"""
        self._display_output()
        try:
            user_input = self._read_input(">> ")
            if user_input.strip():
                return int(user_input)
        except:
            pass
        return default

    def _get_input_str(self, default: str = "") -> str:
        """Get string input from user"""
        self._display_output()
        user_input = self._read_input(">> ")
        if user_input.strip():
            return user_input
        return default

    def _cmd_savedata(self, args):
        slot = int(args[0]) if args else 0
        text = self._format_string(args[1]) if len(args) > 1 else ""
        # Save game
        save_path = self._get_paths().save_slot_path(slot)
        save_data = {
            "vars": self.vars,
            "text": text,
            "date": datetime.now().isoformat()
        }
        with open(save_path, 'wb') as f:
            pickle.dump(save_data, f)
        return 1

    def _cmd_loaddata(self, args):
        slot = int(args[0]) if args else 0
        save_path = self._get_paths().save_slot_path(slot)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)
                self.vars = save_data["vars"]
            return 1
        return 0

    def _cmd_saveglobal(self, args):
        with open(self._get_paths().global_path, 'wb') as f:
            pickle.dump(self.globals, f)

    def _cmd_loadglobal(self, args):
        global_path = self._get_paths().global_path
        if os.path.exists(global_path):
            with open(global_path, 'rb') as f:
                self.globals = pickle.load(f)

    def _cmd_set(self, args):
        if len(args) >= 2:
            var = args[0]
            val = self.evaluate_expression(args[1])
            self._set_variable(var, val)

    def _cmd_add(self, args):
        if len(args) >= 2:
            var = args[0]
            val = self.evaluate_expression(args[1])
            current = self._get_variable(var)
            self._set_variable(var, current + val)

    def _cmd_sub(self, args):
        if len(args) >= 2:
            var = args[0]
            val = self.evaluate_expression(args[1])
            current = self._get_variable(var)
            self._set_variable(var, current - val)

    def _cmd_times(self, args):
        if len(args) >= 2:
            var = args[0]
            val = self.evaluate_expression(args[1])
            current = self._get_variable(var)
            self._set_variable(var, current * val)

    def _cmd_rand(self, args):
        if args:
            val = int(self.evaluate_expression(args[0]))
            return random.randint(0, val - 1) if val > 0 else 0
        return random.randint(0, 999)

    def _cmdArrayshift(self, args):
        """ARRAYSHIFT array, shift_amount, fill_value[, start_idx[, count]]
        将数组元素从 start_idx 开始移动 shift_amount 位，空出的位置用 fill_value 填充
        ERB 原版: ARRAYSHIFT array, shift, value, start, num
        """
        if len(args) < 3:
            return None
        # 解析参数
        array_name = args[0]
        shift_amount = int(self.evaluate_expression(args[1]))
        fill_value = self.evaluate_expression(args[2])
        start_idx = int(self.evaluate_expression(args[3])) if len(args) > 3 else 0
        count = int(self.evaluate_expression(args[4])) if len(args) > 4 else -1
        
        # 获取数组
        array = self._get_array_variable(array_name)
        if array is None:
            return None
        
        # 执行移位
        if shift_amount > 0:
            # 向后移位
            if count < 0:
                count = len(array) - start_idx
            end_idx = start_idx + count
            for i in range(end_idx - 1, start_idx - 1, -1):
                if i + shift_amount < len(array):
                    array[i + shift_amount] = array[i]
            for i in range(start_idx, start_idx + shift_amount):
                if i < len(array):
                    array[i] = fill_value
        elif shift_amount < 0:
            # 向前移位
            shift_amount = abs(shift_amount)
            if count < 0:
                count = len(array) - start_idx
            end_idx = start_idx + count
            for i in range(start_idx + shift_amount, end_idx):
                if i - shift_amount >= start_idx:
                    array[i - shift_amount] = array[i]
            for i in range(end_idx - shift_amount, end_idx):
                if i < len(array):
                    array[i] = fill_value
        return None

    def _cmd_arrayremove(self, args):
        """ARRAYREMOVE array, start_idx, count
        从数组中删除从 start_idx 开始的 count 个元素
        """
        if len(args) < 3:
            return None
        array_name = args[0]
        start_idx = int(self.evaluate_expression(args[1]))
        count = int(self.evaluate_expression(args[2]))
        
        array = self._get_array_variable(array_name)
        if array is None:
            return None
        
        # 删除元素
        for i in range(start_idx, len(array) - count):
            array[i] = array[i + count]
        for i in range(len(array) - count, len(array)):
            array[i] = 0  # 清空末尾
        return None

    def _get_array_variable(self, array_name: str) -> Optional[list]:
        """获取数组变量的引用"""
        # 处理带索引的数组名 (如 LOCAL:0)
        if ':' in array_name:
            parts = array_name.split(':')
            base_name = parts[0]
            indices = [int(self.evaluate_expression(p)) for p in parts[1:]]
            
            # 尝试获取基础数组
            if base_name == 'LOCAL':
                return self.vars.local
            elif base_name == 'LOCALS':
                return self.vars.locals
            elif base_name == 'FLAG':
                return self.vars.flag
            elif base_name == 'GLOBAL':
                return self.globals.get('GLOBAL', [])
            # 角色数组
            if base_name in ('CFLAG', 'BASE', 'MAXBASE', 'ABL', 'TALENT', 'EXP', 'MARK', 'JUEL', 'CSTR'):
                char_idx = indices[0]
                if 0 <= char_idx < len(self.vars.chars):
                    char = self.vars.chars[char_idx]
                    if base_name == 'CFLAG':
                        return char.cflag
                    elif base_name == 'BASE':
                        return char.base
                    elif base_name == 'MAXBASE':
                        return char.maxbase
                    elif base_name == 'ABL':
                        return char.abl
                    elif base_name == 'TALENT':
                        return char.talent
                    elif base_name == 'EXP':
                        return char.exp
                    elif base_name == 'MARK':
                        return char.mark
                    elif base_name == 'JUEL':
                        return char.juel
                    elif base_name == 'CSTR':
                        return char.cstr
            return None
        else:
            # 无索引的数组名
            if array_name == 'LOCAL':
                return self.vars.local
            elif array_name == 'LOCALS':
                return self.vars.locals
            elif array_name == 'FLAG':
                return self.vars.flag
            elif array_name == 'DAY':
                return self.vars.day
            elif array_name == 'ITEM':
                return self.vars.item
            elif array_name == 'ITEMSALES':
                return self.vars.itemsales
            elif array_name == 'LASTSAVE_NO':
                return self.vars.lastsave_no
            return None

    def _cmd_resetdata(self, args):
        """Reset game data"""
        self.vars = ERBVariable()
        self.vars.chars = []

    def _cmd_addchara(self, args):
        char_id = int(args[0]) if args else 0
        new_char = Character()
        new_char.name = f"Character{char_id}"
        self.vars.chars.append(new_char)
        return len(self.vars.chars) - 1

    def _cmd_delchara(self, args):
        char_id = int(args[0]) if args else 0
        if 0 <= char_id < len(self.vars.chars):
            del self.vars.chars[char_id]

    def _cmd_charamade(self, args):
        # CHARAMADE - character made
        pass

    def _cmd_sif(self, args):
        # SIF condition, true_val
        if len(args) >= 2:
            cond = self._evaluate_condition(args[0])
            if cond:
                return self._format_string(args[1])
        return ""

    def _cmd_selectcase(self, args):
        return self.evaluate_expression(args[0]) if args else 0

    def _cmd_case(self, args):
        return True

    def _cmd_endselect(self, args):
        return True

    def _cmd_locals(self, args):
        if args:
            return args[0]
        return ""

    def _cmd_varset(self, args):
        """VARSET array[, value[, start_idx[, count]]
        将数组从 start_idx 开始的 count 个元素设置为 value
        ERB 原版: VARSET var, value, start, num
        """
        if len(args) < 1:
            return None
        array_name = args[0]
        value = self.evaluate_expression(args[1]) if len(args) > 1 else 0
        start_idx = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        count = int(self.evaluate_expression(args[3])) if len(args) > 3 else -1
        
        array = self._get_array_variable(array_name)
        if array is None:
            return None
        
        if count < 0:
            count = len(array) - start_idx
        
        for i in range(start_idx, min(start_idx + count, len(array))):
            array[i] = value
        return None

    def _cmd_chkdata(self, args):
        slot = int(args[0]) if args else 0
        save_path = self._get_paths().save_slot_path(slot)
        if os.path.exists(save_path):
            return 0  # Save exists
        return -1  # No save

    def _cmd_savenos(self, args):
        return 20  # Number of save slots

    def _cmd_gettimes(self, args):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _cmd_strlens(self, args):
        s = args[0] if args else ""
        return len(str(s))

    # ========================================
    # 位操作函数 (GETBIT/SETBIT/CLEARBIT)
    # ========================================
    def _cmd_getbit(self, args):
        """GETBIT(value, bit_index) - 获取指定位的值 (0 或 1)"""
        if len(args) < 2:
            return 0
        value = int(self.evaluate_expression(args[0]))
        bit_idx = int(self.evaluate_expression(args[1]))
        return (value >> bit_idx) & 1

    def _cmd_setbit(self, args):
        """SETBIT(var, bit_index) - 设置指定位为 1"""
        if len(args) < 2:
            return None
        var_name = args[0]
        bit_idx = int(self.evaluate_expression(args[1]))
        current = int(self._get_variable(var_name))
        self._set_variable(var_name, current | (1 << bit_idx))
        return None

    def _cmd_clearbit(self, args):
        """CLEARBIT(var, bit_index) - 设置指定位为 0"""
        if len(args) < 2:
            return None
        var_name = args[0]
        bit_idx = int(self.evaluate_expression(args[1]))
        current = int(self._get_variable(var_name))
        self._set_variable(var_name, current & ~(1 << bit_idx))
        return None

    # ========================================
    # 范围与极值函数 (INRANGE/LIMIT/MIN/MAX/ABS/SIGN)
    # ========================================
    def _cmd_inrange(self, args):
        """INRANGE(value, min, max) - 检查 value 是否在 [min, max] 范围内"""
        if len(args) < 3:
            return 0
        value = int(self.evaluate_expression(args[0]))
        min_val = int(self.evaluate_expression(args[1]))
        max_val = int(self.evaluate_expression(args[2]))
        return 1 if min_val <= value <= max_val else 0

    def _cmd_limit(self, args):
        """LIMIT(value, min, max) - 将 value 限制在 [min, max] 范围内"""
        if len(args) < 3:
            return 0
        value = int(self.evaluate_expression(args[0]))
        min_val = int(self.evaluate_expression(args[1]))
        max_val = int(self.evaluate_expression(args[2]))
        return max(min_val, min(value, max_val))

    def _cmd_min(self, args):
        """MIN(a, b, ...) - 返回最小值"""
        if not args:
            return 0
        values = [int(self.evaluate_expression(arg)) for arg in args]
        return min(values)

    def _cmd_max(self, args):
        """MAX(a, b, ...) - 返回最大值"""
        if not args:
            return 0
        values = [int(self.evaluate_expression(arg)) for arg in args]
        return max(values)

    def _cmd_abs(self, args):
        """ABS(value) - 返回绝对值"""
        if not args:
            return 0
        return abs(int(self.evaluate_expression(args[0])))

    def _cmd_sign(self, args):
        """SIGN(value) - 返回符号 (-1, 0, 1)"""
        if not args:
            return 0
        value = int(self.evaluate_expression(args[0]))
        if value > 0:
            return 1
        elif value < 0:
            return -1
        return 0

    # ========================================
    # 数学函数 (POWER/SQRT/LOG/EXP)
    # ========================================
    def _cmd_power(self, args):
        """POWER(base, exponent) - 返回 base^exponent"""
        if len(args) < 2:
            return 0
        base = int(self.evaluate_expression(args[0]))
        exp = int(self.evaluate_expression(args[1]))
        return int(math.pow(base, exp))

    def _cmd_sqrt(self, args):
        """SQRT(value) - 返回平方根"""
        if not args:
            return 0
        value = int(self.evaluate_expression(args[0]))
        return int(math.sqrt(value))

    def _cmd_log(self, args):
        """LOG(value) - 返回自然对数"""
        if not args:
            return 0
        value = int(self.evaluate_expression(args[0]))
        return int(math.log(value)) if value > 0 else 0

    def _cmd_exp(self, args):
        """EXP(value) - 返回 e^value"""
        if not args:
            return 1
        value = int(self.evaluate_expression(args[0]))
        return int(math.exp(value))

    # ========================================
    # 数组查找函数 (SUM/FINDELEMENT/FINDCHARA)
    # ========================================
    def _cmd_sum(self, args):
        """SUM(array, start, end) - 返回数组元素之和"""
        if not args:
            return 0
        array = self._get_array_variable(args[0])
        if array is None:
            return 0
        start = int(self.evaluate_expression(args[1])) if len(args) > 1 else 0
        end = int(self.evaluate_expression(args[2])) if len(args) > 2 else len(array)
        return sum(array[start:end])

    def _cmd_findelement(self, args):
        """FINDELEMENT(array, value[, start_idx]) - 查找数组中第一个等于 value 的元素索引"""
        if len(args) < 2:
            return -1
        array = self._get_array_variable(args[0])
        if array is None:
            return -1
        value = self.evaluate_expression(args[1])
        start_idx = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        for i in range(start_idx, len(array)):
            if array[i] == value:
                return i
        return -1

    def _cmd_findchara(self, args):
        """FINDCHARA(var_name, value[, start_idx]) - 查找角色数组中第一个等于 value 的角色索引"""
        if len(args) < 2:
            return -1
        var_name = args[0]  # 如 NO, NAME 等
        value = self.evaluate_expression(args[1])
        start_idx = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        
        for i in range(start_idx, len(self.vars.chars)):
            char = self.vars.chars[i]
            if var_name == 'NO':
                if char.no == value:
                    return i
            elif var_name == 'NAME' or var_name == 'CALLNAME':
                if char.name == value:
                    return i
            # 其他属性查找
        return -1

    # ========================================
    # 字符串函数 (STRLEN/SUBSTRING/STRFIND/STRREPLACE)
    # ========================================
    def _cmd_strlen(self, args):
        """STRLEN(str) - 返回字符串长度"""
        if not args:
            return 0
        s = self._format_string(args[0])
        return len(s)

    def _cmd_strlenu(self, args):
        """STRLENU(str) - 返回 Unicode 字符串长度"""
        if not args:
            return 0
        s = self._format_string(args[0])
        return len(s)

    def _cmd_substring(self, args):
        """SUBSTRING(str, start, length) - 截取子字符串"""
        if len(args) < 3:
            return ""
        s = self._format_string(args[0])
        start = int(self.evaluate_expression(args[1]))
        length = int(self.evaluate_expression(args[2]))
        return s[start:start + length]

    def _cmd_substringu(self, args):
        """SUBSTRINGU(str, start, length) - 截取 Unicode 子字符串"""
        if len(args) < 3:
            return ""
        s = self._format_string(args[0])
        start = int(self.evaluate_expression(args[1]))
        length = int(self.evaluate_expression(args[2]))
        return s[start:start + length]

    def _cmd_strfind(self, args):
        """STRFIND(str, search[, start]) - 查找子字符串位置"""
        if len(args) < 2:
            return -1
        s = self._format_string(args[0])
        search = self._format_string(args[1])
        start = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        idx = s.find(search, start)
        return idx

    def _cmd_strfindu(self, args):
        """STRFINDU(str, search[, start]) - 查找 Unicode 子字符串位置"""
        if len(args) < 2:
            return -1
        s = self._format_string(args[0])
        search = self._format_string(args[1])
        start = int(self.evaluate_expression(args[2])) if len(args) > 2 else 0
        idx = s.find(search, start)
        return idx

    def _cmd_strreplace(self, args):
        """STRREPLACE(str, search, replace) - 替换字符串"""
        if len(args) < 3:
            return ""
        s = self._format_string(args[0])
        search = self._format_string(args[1])
        replace = self._format_string(args[2])
        return s.replace(search, replace)

    def _cmd_split(self, args):
        """SPLIT(str, delimiter, array) - 分割字符串到数组"""
        if len(args) < 3:
            return None
        s = self._format_string(args[0])
        delimiter = self._format_string(args[1])
        array_name = args[2]
        
        parts = s.split(delimiter)
        array = self._get_array_variable(array_name)
        if array is None:
            return None
        
        for i, part in enumerate(parts):
            if i < len(array):
                array[i] = part
        return len(parts)

    def _cmd_replace(self, args):
        """REPLACE(str, pattern, replacement) - 正则替换"""
        if len(args) < 3:
            return ""
        s = self._format_string(args[0])
        pattern = self._format_string(args[1])
        replacement = self._format_string(args[2])
        return re.sub(pattern, replacement, s)

    def _cmd_unicode(self, args):
        """UNICODE(code) - 返回 Unicode 字符"""
        if not args:
            return ""
        code = int(self.evaluate_expression(args[0]))
        try:
            return chr(code)
        except:
            return ""

    # ========================================
    # 进度条函数 (BAR/BARSTR/CUSTOMDRAWLINE)
    # ========================================
    def _cmd_bar(self, args):
        """BAR(value, max, length) - 打印进度条"""
        if len(args) < 3:
            return None
        value = int(self.evaluate_expression(args[0]))
        max_val = int(self.evaluate_expression(args[1]))
        length = int(self.evaluate_expression(args[2]))
        
        if max_val <= 0:
            max_val = 1
        
        filled = int((value / max_val) * length)
        filled = max(0, min(filled, length))
        
        bar_str = '[' + '*' * filled + '.' * (length - filled) + ']'
        self.output_buffer.append(bar_str)
        return None

    def _cmd_barstr(self, args):
        """BARSTR(value, max, length) - 返回进度条字符串"""
        if len(args) < 3:
            return ""
        value = int(self.evaluate_expression(args[0]))
        max_val = int(self.evaluate_expression(args[1]))
        length = int(self.evaluate_expression(args[2]))
        
        if max_val <= 0:
            max_val = 1
        
        filled = int((value / max_val) * length)
        filled = max(0, min(filled, length))
        
        return '[' + '*' * filled + '.' * (length - filled) + ']'

    def _cmd_customdrawline(self, args):
        """CUSTOMDRAWLINE char - 打印自定义分隔线"""
        char = args[0] if args else "-"
        line = char * 60
        self.output_buffer.append(line)
        return None

    def _set_variable(self, var: str, value: Any):
        """Set variable value"""
        if self._set_variable_flag_value(var, value):
            return
        if self._set_variable_global_value(var, value):
            return
        if self._set_variable_character_value(var, value):
            return

    def _set_variable_flag_value(self, var: str, value: Any) -> bool:
        if not var.startswith('FLAG:'):
            return False
        parts = var[5:].split(':')
        if len(parts) == 1:
            self.vars.set_flag(int(parts[0]), int(value))
            return True
        if len(parts) == 2:
            self.vars.set_char_flag(int(parts[0]), int(parts[1]), int(value))
            return True
        return False

    def _set_variable_global_value(self, var: str, value: Any) -> bool:
        if var == 'MONEY':
            self.vars.money = int(value)
            return True
        if var.startswith('DAY:'):
            idx = int(var[4:])
            if 0 <= idx < len(self.vars.day):
                self.vars.day[idx] = int(value)
            return True
        if var == 'TIME':
            self.vars.time = int(value)
            return True
        if var == 'TARGET':
            self.vars.target = int(value)
            return True
        if var == 'ASSI':
            self.vars.assi = int(value)
            return True
        return False

    def _set_variable_character_value(self, var: str, value: Any) -> bool:
        if var.startswith('TALENT:'):
            parts = var[7:].split(':')
            char_idx = 0 if parts[0] == 'MASTER' else int(parts[0])
            talent_idx = int(parts[1])
            self._ensure_character_index(char_idx)
            self.vars.chars[char_idx].talent[talent_idx] = int(value)
            return True
        if var.startswith('ABL:'):
            parts = var[4:].split(':')
            char_idx = int(parts[0])
            abl_idx = int(parts[1])
            self._ensure_character_index(char_idx)
            self.vars.chars[char_idx].set_abl(abl_idx, int(value))
            return True
        if var.startswith('BASE:'):
            parts = var[5:].split(':')
            char_idx = int(parts[0])
            base_idx = int(parts[1])
            self._ensure_character_index(char_idx)
            self.vars.chars[char_idx].base[base_idx] = int(value)
            return True
        if var.startswith('CFLAG:'):
            parts = var[6:].split(':')
            char_idx = int(parts[0])
            cflag_idx = int(parts[1])
            self._ensure_character_index(char_idx)
            self.vars.chars[char_idx].set_flag(cflag_idx, int(value))
            return True
        return False

    def _ensure_character_index(self, char_idx: int):
        while char_idx >= len(self.vars.chars):
            self.vars.chars.append(Character())

    def _display_output(self):
        """Display output buffer"""
        if self.output_buffer:
            output = "".join(self.output_buffer)
            print(output, end="")
            self.output_buffer = []


class GamePaths:
    """Filesystem paths used by the Python reimplementation."""

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.preferred_save_dir = os.path.join(root_dir, "sav")
        self.fallback_save_dir = os.path.join(tempfile.gettempdir(), "eraMaouEx", "sav")
        self.save_dir = self._resolve_save_dir()
        self.global_path = os.path.join(self.save_dir, "global.dat")

    def _can_write_dir(self, directory: str) -> bool:
        try:
            os.makedirs(directory, exist_ok=True)
            probe_path = os.path.join(directory, ".write_test")
            with open(probe_path, "w", encoding="utf-8") as probe_file:
                probe_file.write("ok")
            os.remove(probe_path)
            return True
        except OSError:
            return False

    def _resolve_save_dir(self) -> str:
        if self._can_write_dir(self.preferred_save_dir):
            return self.preferred_save_dir
        os.makedirs(self.fallback_save_dir, exist_ok=True)
        return self.fallback_save_dir

    def ensure_dirs(self):
        os.makedirs(self.save_dir, exist_ok=True)

    def save_slot_path(self, slot: int) -> str:
        return os.path.join(self.save_dir, f"save{slot}.dat")



# Mixin imports - 原始Mixin
from eraMaouEx_modules.core.game_state import GameState
from eraMaouEx_modules.systems.comf import ComfMixin
from eraMaouEx_modules.systems.ablup_full import AblupFullMixin
from eraMaouEx_modules.systems.equip import EquipMixin
from eraMaouEx_modules.systems.source import SourceMixin
from eraMaouEx_modules.systems.event_daily import EventDailyMixin
from eraMaouEx_modules.systems.dungeon_ext import DungeonExtMixin
from eraMaouEx_modules.systems.event_kojo import EventKojoMixin
from eraMaouEx_modules.systems.invasion import InvasionMixin
from eraMaouEx_modules.systems.ending import EndingMixin
from eraMaouEx_modules.systems.chara_ext import CharaExtMixin
from eraMaouEx_modules.systems.shop_ext import ShopExtMixin
from eraMaouEx_modules.systems.game_loop import GameLoopMixin
from eraMaouEx_modules.systems.misc import MiscMixin
# Mixin imports - 新拆分Mixin
from eraMaouEx_modules.systems.sell_ext import SellExtMixin
from eraMaouEx_modules.systems.sell_followup import SellFollowupMixin
from eraMaouEx_modules.systems.execution import ExecutionMixin
from eraMaouEx_modules.systems.turn_end import TurnEndMixin
from eraMaouEx_modules.systems.save_load import SaveLoadMixin
from eraMaouEx_modules.systems.ntr_ext import NtrExtMixin
from eraMaouEx_modules.systems.marriage_ext import MarriageExtMixin
from eraMaouEx_modules.systems.temptation_ext import TemptationExtMixin
from eraMaouEx_modules.systems.char_mgmt import CharMgmtMixin
from eraMaouEx_modules.systems.config_mixin import ConfigMixin
from eraMaouEx_modules.systems.lab import LabMixin
from eraMaouEx_modules.systems.train_ext import TrainExtMixin
from eraMaouEx_modules.systems.communication import CommunicationMixin
from eraMaouEx_modules.systems.data_load import DataLoadMixin
from eraMaouEx_modules.systems.dress import DressMixin
from eraMaouEx_modules.systems.infrastructure import InfrastructureMixin
from eraMaouEx_modules.systems.pregnancy_ext import PregnancyExtMixin
from eraMaouEx_modules.systems.museum_ext import MuseumExtMixin
from eraMaouEx_modules.systems.tax_ext import TaxExtMixin
from eraMaouEx_modules.systems.lvup_ext import LvupExtMixin
from eraMaouEx_modules.systems.summon_ext import SummonExtMixin
from eraMaouEx_modules.systems.ability_ext import AbilityExtMixin
from eraMaouEx_modules.systems.invasion_ext import InvasionExtMixin
from eraMaouEx_modules.systems.interception import InterceptionMixin
from eraMaouEx_modules.systems.campaign import CampaignMixin
from eraMaouEx_modules.systems.arcana import ArcanaMixin
from eraMaouEx_modules.systems.princess import PrincessMixin
from eraMaouEx_modules.systems.spade import SpadeMixin
from eraMaouEx_modules.systems.shop_ext2 import ShopExt2Mixin
from eraMaouEx_modules.systems.godness import GodnessMixin
from eraMaouEx_modules.systems.monster_ext import MonsterExtMixin
from eraMaouEx_modules.systems.video_ext import VideoExtMixin
from eraMaouEx_modules.systems.sense_ext import SenseExtMixin
from eraMaouEx_modules.systems.hair_ext import HairExtMixin
from eraMaouEx_modules.systems.race_ext import RaceExtMixin
from eraMaouEx_modules.systems.item_ext import ItemExtMixin
from eraMaouEx_modules.systems.face_ext import FaceExtMixin
from eraMaouEx_modules.systems.magic_ext import MagicExtMixin
from eraMaouEx_modules.systems.post_ext import PostExtMixin
from eraMaouEx_modules.systems.special_ext import SpecialExtMixin
from eraMaouEx_modules.systems.common_ext import CommonExtMixin
from eraMaouEx_modules.systems.square_ext import SquareExtMixin
from eraMaouEx_modules.systems.stain_ext import StainExtMixin
from eraMaouEx_modules.systems.source_sub_ext import SourceSubExtMixin
from eraMaouEx_modules.systems.draw_ext import DrawExtMixin
from eraMaouEx_modules.systems.agent_ext import AgentExtMixin
from eraMaouEx_modules.systems.enemy_ext import EnemyExtMixin
from eraMaouEx_modules.systems.makai_ext import MakaiExtMixin
from eraMaouEx_modules.systems.cm_ext import CmExtMixin
from eraMaouEx_modules.systems.self_ext import SelfExtMixin
from eraMaouEx_modules.systems.comable_ext import ComableExtMixin
from eraMaouEx_modules.systems.usercom_ext import UserComExtMixin
from eraMaouEx_modules.systems.excom_ext import ExComExtMixin
from eraMaouEx_modules.systems.naedoko_ext import NaedokoExtMixin
from eraMaouEx_modules.systems.benki_ext import BenkiExtMixin
from eraMaouEx_modules.systems.seiin_ext import SeiinExtMixin
from eraMaouEx_modules.systems.passout_ext import PassoutExtMixin
from eraMaouEx_modules.systems.tatoo_ext import TatooExtMixin
from eraMaouEx_modules.systems.relation_ext import RelationExtMixin
from eraMaouEx_modules.systems.family_ext import FamilyExtMixin
from eraMaouEx_modules.systems.ex_item_ext import ExItemExtMixin
from eraMaouEx_modules.systems.naming_ext import NamingExtMixin
from eraMaouEx_modules.systems.aftertrain_ext import AftertrainMixin
from eraMaouEx_modules.systems.event_apply_ext import EventApplyMixin
from eraMaouEx_modules.systems.pregnancy_apply_ext import PregnancyApplyMixin
from eraMaouEx_modules.systems.data_query_ext import DataQueryMixin
from eraMaouEx_modules.systems.condition_ext import ConditionMixin
from eraMaouEx_modules.systems.ui_ext import UIExtMixin
from eraMaouEx_modules.systems.apply_ext2 import ApplyExt2Mixin
from eraMaouEx_modules.systems.build_ext import BuildExtMixin
from eraMaouEx_modules.systems.game_logic_ext import GameLogicMixin
from eraMaouEx_modules.systems.modify_ext import ModifyExtMixin

class GameEngine(
    # 新拆分的Mixin（优先级高，可能覆盖旧方法）
    SellExtMixin, SellFollowupMixin, ExecutionMixin, TurnEndMixin,
    SaveLoadMixin, NtrExtMixin, MarriageExtMixin, TemptationExtMixin,
    CharMgmtMixin, ConfigMixin, LabMixin, TrainExtMixin,
    CommunicationMixin, DataLoadMixin, DressMixin, InfrastructureMixin,
    PregnancyExtMixin, MuseumExtMixin, TaxExtMixin, LvupExtMixin,
    SummonExtMixin, AbilityExtMixin, InvasionExtMixin, InterceptionMixin,
    CampaignMixin, ArcanaMixin, PrincessMixin, SpadeMixin, ShopExt2Mixin,
    GodnessMixin, MonsterExtMixin, VideoExtMixin, SenseExtMixin,
    HairExtMixin, RaceExtMixin, ItemExtMixin, FaceExtMixin, MagicExtMixin,
    PostExtMixin, SpecialExtMixin, CommonExtMixin, SquareExtMixin,
    StainExtMixin, SourceSubExtMixin, DrawExtMixin, AgentExtMixin,
    EnemyExtMixin, MakaiExtMixin, CmExtMixin, SelfExtMixin,
    ComableExtMixin, UserComExtMixin, ExComExtMixin, NaedokoExtMixin,
    BenkiExtMixin, SeiinExtMixin, PassoutExtMixin, TatooExtMixin,
    RelationExtMixin, FamilyExtMixin, ExItemExtMixin, NamingExtMixin,
    AftertrainMixin, EventApplyMixin, PregnancyApplyMixin,
    DataQueryMixin, ConditionMixin, UIExtMixin, ApplyExt2Mixin,
    BuildExtMixin, GameLogicMixin, ModifyExtMixin,
    # 原始Mixin
    ComfMixin, AblupFullMixin, EquipMixin, SourceMixin, EventDailyMixin,
    DungeonExtMixin, EventKojoMixin, InvasionMixin, EndingMixin,
    CharaExtMixin, ShopExtMixin, GameLoopMixin, MiscMixin
):
    """Main game engine that orchestrates the interpreter"""

    def __init__(self, erb_dir: str):
        self.erb_dir = erb_dir
        self.paths = GamePaths(erb_dir)
        self.paths.ensure_dirs()
        self.interpreter = ERBInterpreter()
        self.interpreter.paths = self.paths
        self.state = GameState(self.interpreter.vars)
        self.palam_level_thresholds, self.exp_level_thresholds = self._load_level_thresholds()
        self.train_commands = self._load_train_commands()
        self.item_catalog = self._load_item_catalog()
        self.talent_catalog = self._load_talent_catalog()
        self.character_template_catalog = self._build_character_template_catalog()
        self.running = True
def _resolve_erb_dir(argv):
    """Resolve ERB directory from argv, ignoring --llm and similar flags."""
    for arg in argv[1:]:
        if arg.startswith("-"):
            continue
        return arg
    return os.path.dirname(os.path.abspath(__file__))


def run_llm_mode(erb_dir):
    """Start the LLM-driven interactive game mode."""
    from eraMaouEx_modules.llm.config import load_config
    from eraMaouEx_modules.llm.client import LLMClient
    from eraMaouEx_modules.llm.context import ContextBuilder
    from eraMaouEx_modules.llm.skills import SkillRegistry
    from eraMaouEx_modules.llm.loop import LLMGameLoop

    config = load_config()
    if config is None:
        print("[LLM] 配置缺失，回退到终端模式。")
        engine = GameEngine(erb_dir)
        engine.run()
        return

    print(f"Game directory: {erb_dir}")
    print("[LLM] 初始化游戏引擎...")
    engine = GameEngine(erb_dir)
    try:
        engine._bootstrap_game_runtime()
        engine._system_init()
        if not engine.interpreter.vars.chars:
            engine.interpreter.vars.chars.append(Character())
            engine.interpreter.vars.chars[0].name = "魔王"
    except Exception as e:
        print(f"[LLM] 初始化失败: {e}")
        return

    client = LLMClient(config)
    context_builder = ContextBuilder(engine)
    skill_registry = SkillRegistry(engine, context_builder)
    loop = LLMGameLoop(engine, client, context_builder, skill_registry)
    loop.run()


def main():
    """Main entry point"""
    use_llm = "--llm" in sys.argv

    erb_dir = _resolve_erb_dir(sys.argv)
    game_dir = r"F:\code\eraMaouEx"
    if os.path.exists(game_dir):
        erb_dir = game_dir

    if use_llm:
        run_llm_mode(erb_dir)
        return

    print(f"Game directory: {erb_dir}")

    engine = GameEngine(erb_dir)
    engine.run()


if __name__ == "__main__":
    main()
