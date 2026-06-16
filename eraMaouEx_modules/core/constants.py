"""
eraMaouEx 核心模块 - 常量定义
对应 ERB CSV 文件中的常量映射
"""

# ========================================
# 能力 (ABL) 常量 - 对应 Abl.csv
# ========================================
# 性感
ABL_C_SENS = 0      # 阴蒂感觉
ABL_B_SENS = 1      # 乳房感觉
ABL_V_SENS = 2      # 私处感觉
ABL_A_SENS = 3      # 肛门感觉
ABL_P_SENS = 4      # 局部感觉
# 技術
ABL_SUBMIT = 10     # 顺从
ABL_DESIRE = 11     # 欲望
ABL_TECH = 12       # 技巧
ABL_SERVE_TECH = 13 # 侍奉技术
ABL_SEX_TECH = 14   # 性交技术
ABL_SPEECH = 15     # 话术
ABL_SERVE = 16      # 侍奉精神
ABL_EXPOSE = 17     # 露出癖
# 特殊性癖
ABL_SAD = 20        # 抖S气质
ABL_MASO = 21       # 抖M气质
ABL_LES = 22        # 百合气质
ABL_HOMO = 23       # 断背气质
# 中毒
ABL_SEX_ADDICT = 30   # 性交中毒
ABL_SELF_MAST = 31    # 自慰中毒
ABL_SEMEN_ADDICT = 32 # 精液中毒
ABL_LES_ADDICT = 33   # 百合中毒
ABL_PROSTITUTE = 37   # 卖淫中毒
ABL_BEAST_ADDICT = 39 # 兽奸中毒
ABL_P_ADDICT = 40     # 局部中毒
# 異界関連
ABL_LEARN = 100     # 学习能力
ABL_ATHLETIC = 101  # 运动能力
ABL_BATTLE = 102    # 战斗能力
ABL_SENSIBILITY = 103 # 感性

# ========================================
# 素质 (TALENT) 常量
# ========================================
# 性别相关
TALENT_VIRGIN = 0       # 处女
TALENT_MALE_VIRGIN = 1  # 童贞
TALENT_COLLAPSE = 9     # 崩坏

# 性格相关 (160-179)
TALENT_KIND = 160       # 慈爱
TALENT_CONFIDENT = 161  # 自信家
TALENT_WEAK = 162       # 懦弱
TALENT_NOBLE = 163      # 高贵
TALENT_COOL = 164       # 冷静
TALENT_VILLAGE_A = 165  # 村娘A (玛奥专用)
TALENT_EVIL = 166       # 恶女
TALENT_HEART = 167      # 金红桃 (ユニーク)
TALENT_SPADE = 168      # 银黑桃 (ユニーク)
TALENT_DIAMOND = 169    # 黑方片 (ユニーク)
TALENT_CLUB = 170       # 白梅花 (ユニーク)
TALENT_VILLAGE_B = 171  # 村娘B (莉莉专用)
TALENT_SMART = 172      # 智慧
TALENT_GUARDIAN = 173   # 庇护者
TALENT_PRINCE = 174     # 贵公子
TALENT_CLEVER = 175     # 伶俐

# 売春関連 (180-188)
TALENT_PROSTITUTE = 180 # 妓女
TALENT_KEISEI = 181     # 倾城
TALENT_ELOQUENT = 182   # 巧言
TALENT_REGULAR = 183    # 有常客
TALENT_COURTED = 184    # 求爱
TALENT_SINGER = 185     # 歌姫
TALENT_DANCER = 186     # 舞姫
TALENT_BEAUTY = 187     # 美姫
TALENT_FIGHTER = 188    # 斗姬

# 体調不良系 (190-193)
TALENT_V_OVIPOSIT = 190 # 私处产卵
TALENT_A_OVIPOSIT = 191 # 直肠产卵
TALENT_WORM = 192       # 蠕虫
TALENT_A_WORM = 193     # 肛门虫

# 态度相关 (10-19)
TALENT_SHY = 10         # 胆怯
TALENT_REBEL = 11       # 反抗心
TALENT_STRONG = 12      # 刚强
TALENT_FRANK = 13       # 坦率
TALENT_CALM = 14        # 文静
TALENT_HAUGHTY = 15     # 高姿态
TALENT_BOAST = 16       # 嚣张
TALENT_HUMBLE = 17      # 低姿态
TALENT_TSUN = 18        # 傲娇

# 情感相关 (20-29)
TALENT_CONTROL = 20     # 克制
TALENT_APATHY = 21      # 冷漠
TALENT_EMOTIONLESS = 22 # 感情淡薄
TALENT_CURIOUS = 23     # 好奇心
TALENT_CONSERVE = 24    # 保守的
TALENT_OPTIMIST = 25    # 乐观的
TALENT_PESSIMIST = 26   # 悲观的
TALENT_ALERT = 27       # 戒备森严
TALENT_SHOWOFF = 28     # 爱表现

# 贞操相关 (30-34)
TALENT_CHASTE = 30      # 看重贞操
TALENT_UNCHASTE = 31    # 看轻贞操
TALENT_REPRESS = 32     # 压抑
TALENT_OPEN = 33        # 开放
TALENT_RESIST = 34      # 抵抗

# 羞耻相关 (35-37)
TALENT_SHAME = 35       # 害羞
TALENT_NO_SHAME = 36    # 不知羞耻
TALENT_LEVERAGE = 37    # 把柄

# 痛觉/体质相关 (40-48)
TALENT_FEAR_PAIN = 40   # 害怕疼痛
TALENT_NO_FEAR_PAIN = 41 # 不惧疼痛
TALENT_EASY_WET = 42    # 容易湿
TALENT_HARD_WET = 43    # 不易湿
TALENT_CRYBABY = 44     # 爱哭鬼
TALENT_NO_CRY = 45      # 不哭泣
TALENT_DRUG_ADDICT = 46 # 药物上瘾
TALENT_LOVE_SEMEN = 47  # 喜欢精液
TALENT_GLASSES = 48     # 眼镜

# 学习相关 (50-57)
TALENT_FAST_LEARN = 50  # 快速学习
TALENT_SLOW_LEARN = 51  # 学习缓慢
TALENT_TONGUE = 52      # 擅用舌头
TALENT_MIX_KNOW = 55    # 调合知识
TALENT_DRUG_RESIST = 56 # 抗药性
TALENT_PEE = 57         # 漏尿癖

# 洁癖度 (60-64)
TALENT_EASY_MAST = 60   # 容易自慰
TALENT_NO_SMELL = 61    # 不怕污臭
TALENT_HATE_SMELL = 62  # 反感污臭
TALENT_SERVE_MIND = 63  # 献身的
TALENT_NO_DIRTY = 64    # 不怕脏

# 正直度 (69-73)
TALENT_RESIST_TEMPT = 69 # 抵抗诱惑
TALENT_ACCEPT_PLEASURE = 70 # 接受快感
TALENT_DENY_PLEASURE = 71  # 否定快感
TALENT_ADDICT = 72      # 容易上瘾
TALENT_EASY_FALL = 73   # 容易陷落

# 特殊体质 (74-93)
TALENT_MAST_MANIAC = 74  # 自慰狂
TALENT_SEX_MANIAC = 75   # 性爱狂
TALENT_LEWD = 76         # 淫乱
TALENT_A_MANIAC = 77     # 尻穴狂
TALENT_B_MANIAC = 78     # 弄乳狂
TALENT_TOMBOY = 79       # 男人婆
TALENT_PERVERT = 80      # 倒错的
TALENT_BI = 81           # 双性恋
TALENT_HATE_MALE = 82    # 讨厌男人
TALENT_SADIST = 83       # 施虐狂
TALENT_JEALOUS = 84      # 嫉妒
TALENT_LOVE = 85         # 爱慕
TALENT_OBEY = 86         # 盲从
TALENT_DEVIL = 87        # 小恶魔
TALENT_MASOCHIST = 88    # 受虐狂
TALENT_EXHIBITIONIST = 89 # 露出狂
TALENT_CHARM = 91        # 魅惑
TALENT_MYSTERIOUS = 92   # 谜之魅力
TALENT_INTIMIDATE = 93   # 威圧感

# 身体特征 (99-119)
TALENT_BIG = 99         # 魁梧
TALENT_SMALL = 100      # 娇小
TALENT_C_DULL = 101     # 阴蒂钝感
TALENT_C_SENS = 102     # 阴蒂敏感
TALENT_V_DULL = 103     # 私处钝感
TALENT_V_SENS = 104     # 私处敏感
TALENT_A_DULL = 105     # 肛门钝感
TALENT_A_SENS = 106     # 肛门敏感
TALENT_B_DULL = 107     # 乳房钝感
TALENT_B_SENS = 108     # 乳房敏感
TALENT_SMALL_BREAST = 109 # 贫乳
TALENT_BIG_BREAST = 110  # 巨乳
TALENT_FAST_RECOVER = 111 # 快速回复
TALENT_SLOW_RECOVER = 112 # 回复缓慢
TALENT_ATTRACT = 113     # 魅力
TALENT_HUGE_BREAST = 114 # 爆乳
TALENT_OBESITY = 115     # 肥胖
TALENT_NO_BREAST = 116   # 绝壁
TALENT_SUPER_BREAST = 119 # 超乳

# 特殊状态 (121-157)
TALENT_FUTA = 121       # 扶她
TALENT_MALE = 122       # 男人
TALENT_CRAZY = 123      # 疯狂
TALENT_ANIMAL_EARS = 124 # 动物耳朵
TALENT_WHITE_TIGER = 125 # 白虎
TALENT_POPULAR = 126    # 高人气
TALENT_COUNTERATTACK = 127 # 逆袭
TALENT_BREAST_MILK = 130 # 母乳体质
TALENT_INFANT_REGRESS = 131 # 幼儿退行
TALENT_CHILDISH = 132    # 幼稚
TALENT_FAST_CUM = 133    # 早泄
TALENT_WEAK_MIND = 134   # 软弱
TALENT_IMMATURE = 135    # 未熟
TALENT_BITCH = 136       # 牝犬
TALENT_BEAST = 137       # 兽类
TALENT_MOTHER_COMPLEX = 140 # 恋母情结
TALENT_FATHER_COMPLEX = 141 # 恋父情结
TALENT_LOLICON = 142     # 萝莉控
TALENT_SHOTACON = 143    # 正太控
TALENT_NO_MAST = 150     # 从不自慰
TALENT_NO_SERVE = 151    # 绝不侍奉
TALENT_NO_BRAINWASH = 152 # 不受洗脑
TALENT_PREGNANT = 153    # 妊娠
TALENT_CHILDCARE = 154   # 育儿中
TALENT_MATERNAL = 155    # 母性
TALENT_PATERNAL = 156    # 父性
TALENT_WIFE = 157        # 人妻
TALENT_CROSS_STERILE = 158 # 同族不育

# 战斗技能 (200-260)
TALENT_WARRIOR = 200     # 战士
TALENT_MAGE = 201        # 魔法师
TALENT_PRIEST = 202      # 神官
TALENT_THIEF = 203       # 盗贼
TALENT_MEAT_TOILET = 204 # 肉便器
TALENT_KNIGHT = 205      # 骑士
TALENT_MIKO = 206        # 巫女
TALENT_NINJA = 207       # 忍者
TALENT_ARCHER = 208      # 弓手
TALENT_SEEDBED = 209     # 苗床
TALENT_DEMON_GENERAL = 210 # 魔界将军
TALENT_DEMON_PRIEST = 211 # 魔导神官
TALENT_ELITE = 220       # 精英

TALENT_HEAL = 117        # 治癒
TALENT_ENCOURAGE = 118   # 鼓舞
# 強化素質
TALENT_LEWD_C = 230      # 淫核
TALENT_LEWD_B = 231      # 淫乳
TALENT_LEWD_V = 232      # 淫壶
TALENT_LEWD_A = 233      # 淫肛
# 戦闘技能
TALENT_TACTICS = 240     # 战术
TALENT_MAGIC = 241       # 魔术
TALENT_FAITH = 242       # 法术
TALENT_SURPRISE = 243    # 奇袭
TALENT_DEMON_SKIN = 244  # 恶魔肌肤
TALENT_DEMON_WING = 245  # 恶魔翅膀
TALENT_DEMON_TAIL = 246  # 恶魔尾巴
TALENT_DEMON_EYE = 247   # 恶魔眼睛
TALENT_MUSCLE = 248      # 肌肉型
TALENT_IRON = 249        # 铁壁
TALENT_CURSE = 250       # 咒术
TALENT_NINJUTSU = 251    # 忍术
TALENT_FIRST = 252       # 先制
TALENT_DARK = 253        # 褐色肌肤
TALENT_DEMON_MARK = 254  # 魔之刻印
TALENT_PALE = 255        # 白皙
TALENT_FRAIL = 256       # 虚弱
TALENT_MAGIC_RESIST = 257 # 魔法耐性
TALENT_FAST_RUN = 258    # 俊足
TALENT_ONE_EYE = 259     # 独眼
TALENT_THIRD_EYE = 260   # 额头天眼
TALENT_SLIME = 261       # 史莱姆
TALENT_TENTACLE = 262    # 触手
TALENT_SMALL_BODY = 263  # 小人体型
TALENT_HORN = 264        # 角

# 特殊素質 (270-)
TALENT_ALWAYS_HEAT = 271  # 时常发情
TALENT_SEX_HERO = 272     # 性豪
TALENT_CHASTE_SEAL = 273  # 私处封印
TALENT_SOUL_BIND = 274    # 魂缚
TALENT_FIRE_USER = 275    # 火之能力者
TALENT_ICE_USER = 276     # 冰之能力者
TALENT_THUNDER_USER = 277 # 雷之能力者
TALENT_LIGHT_USER = 278   # 光之能力者
TALENT_DARK_USER = 279    # 暗之能力者
TALENT_CRAZY_LORD_CAP = 280 # 狂王俘虏
TALENT_COMMON_BATTLE = 281 # 常识改变【战斗】
TALENT_BLASPHEMER = 282   # 冒渎者
TALENT_COMMON_DAILY = 283 # 常识改变【日常】

# 境遇 (290-)
TALENT_GUARANTOR = 290    # 担保人
TALENT_NEWBIE = 291       # 初心者
TALENT_SHADOW = 292       # 魔王之影

# 外見 (300-)
TALENT_HAIR_COLOR = 300   # 头发颜色
TALENT_HAIR_STATE = 301   # 头发状态
TALENT_HAIR_LENGTH = 302  # 头发长度
TALENT_HAIR_TRIM = 303    # 头发修剪方式
TALENT_HAIR_STYLE = 304   # 发型
TALENT_EYE = 305          # 目
TALENT_EYE_COLOR = 306    # 瞳色
TALENT_LIP = 307          # 唇
TALENT_BODY_TYPE = 308    # 体型
TALENT_NIPPLE = 309       # 乳头
TALENT_PUBIC_HAIR = 310   # 阴毛状态
TALENT_PUBIC_MAX = 311    # 阴毛生长极限
TALENT_CHARM_POINT = 312  # 魅力点
TALENT_HABIT = 313        # 癖
TALENT_RACE = 314         # 种族
TALENT_PRE_HERO_LIFE = 315 # 成为勇者前的生活
TALENT_HERO_TRIGGER = 316 # 成为勇者的契机
TALENT_FAVORITE = 317     # 喜欢的东西
TALENT_PENIS_STATE = 318  # 阴茎的状态
TALENT_RACE2 = 319        # 种族2

# 家族・知識 (320-)
TALENT_FAMILY_STRUCT = 320 # 家族構成
TALENT_ORIG_RACE = 321    # 原种族
TALENT_CURR_RACE = 322    # 现种族
TALENT_FATHER_RACE = 323  # 父亲种族
TALENT_MOTHER_RACE = 324  # 母亲种族
TALENT_MAKAI_KNOW = 325   # 魔界知识
TALENT_MEAT_CURSE = 326   # 肉芽诅咒
TALENT_INMA_KNOW = 327    # 淫魔知识
TALENT_MACHU_KNOW = 328   # 魔虫知识

# 妊娠素质 (340-)
TALENT_ABNORMAL_PREG = 340 # 異常妊娠体质
TALENT_BREAST_PREG = 341   # 乳内妊娠
TALENT_TESTIS_PREG = 342   # 精巣妊娠

# 狂王
TALENT_CRAZY_LORD = 399  # 狂王

# ========================================
# 刻印 (MARK) 常量 - 对应 Mark.csv
# ========================================
MARK_PAIN = 0        # 苦痛刻印
MARK_PLEASURE = 1    # 快乐刻印
MARK_SUBMIT = 2      # 屈服刻印
MARK_REBEL = 3       # 反抗刻印
MARK_SYNDROME = 10   # 异界综合征

# ========================================
# 参数 (PALAM) 常量 - 对应 Palam.csv
# ========================================
PALAM_C = 0          # 阴核
PALAM_V = 1          # 私处
PALAM_A = 2          # 肛门
PALAM_LUB = 3        # 润滑
PALAM_SUBMIT = 4     # 恭顺
PALAM_YIELD = 5      # 屈服
PALAM_LEARN = 6      # 习得
PALAM_SHAME = 7      # 耻情
PALAM_PAIN = 8       # 苦痛
PALAM_FEAR = 9       # 恐怖
PALAM_DISGUST = 10   # 反感
PALAM_UNPLEASANT = 11 # 不快
PALAM_DEPRESS = 12   # 抑郁
PALAM_B = 13         # 乳房
PALAM_P = 14         # 局部
PALAM_NEGATE = 100   # 否定

# ========================================
# 来源 (SOURCE) 常量 - 对应 source.csv
# ========================================
SOURCE_C = 0         # 阴核快感
SOURCE_V = 1         # 私处快感
SOURCE_A = 2         # 肛门快感
SOURCE_LOVE = 3      # 情爱
SOURCE_SEX = 4       # 性行为
SOURCE_ACHIEVE = 5   # 达成感
SOURCE_PAIN = 6      # 疼痛
SOURCE_ADDICT = 7    # 成瘾追加
SOURCE_DISGUST = 8   # 不洁
SOURCE_LIQUID = 10   # 液体追加
SOURCE_LUST_ADD = 11 # 欲情追加
SOURCE_EXPOSE = 12   # 露出
SOURCE_SUBMIT = 13   # 屈从
SOURCE_ESCAPE = 14   # 逃离
SOURCE_HOSTILE = 15  # 反感追加
SOURCE_OBEY = 16     # 恭顺追加
SOURCE_B = 17        # 乳房快感
SOURCE_P = 18        # 局部快感

# ========================================
# 经验 (EXP) 常量 - 对应 exp.csv
# ========================================
EXP_V = 0            # 私处经验
EXP_A = 1            # 肛门经验
EXP_ORGASM = 2       # 绝顶经验
EXP_EJAC = 3         # 射精经验
EXP_SEX = 5          # 性交经验
EXP_ORGASM_SEMEN = 8 # 精饮绝顶经验
EXP_MAST = 10        # 自慰经验
EXP_TRAIN_MAST = 11  # 调教自慰经验
EXP_SEMEN = 20       # 精液经验
EXP_SERVE_PLEASURE = 21 # 侍奉快乐经验
EXP_ORAL = 22        # 口交经验
EXP_LOVE = 23        # 爱情经验
EXP_MASO_PLEASURE = 30  # 被虐快乐经验
EXP_PEE = 31         # 放尿经验
EXP_A_PLEASURE = 32  # 肛门快乐经验
EXP_SAD_PLEASURE = 33   # 施虐快乐经验
EXP_C = 34           # 阴蒂经验
EXP_B = 35           # 乳房经验
EXP_LES = 40         # 百合经验
EXP_HOMO = 41        # 断背经验
EXP_ABNORMAL = 50    # 异常经验
EXP_BIND = 51        # 紧缚经验
EXP_V_EXPAND = 52    # 私处扩张经验
EXP_A_EXPAND = 53    # 肛门扩张经验
EXP_MILK = 54        # 喷奶经验
EXP_TENTACLE = 55    # 触手经验
EXP_BEAST = 56       # 兽奸经验
EXP_DRUG = 57        # 药物经验
EXP_BIRTH = 60       # 生育经验
EXP_CROSS_PREG = 62  # 异种妊娠经验
EXP_TRAIN_FAINT = 65 # 调教失神经验
EXP_COOK = 61        # 料理经验
EXP_VIDEO = 70       # 拍摄经验
EXP_SING = 71        # 歌唱经验
EXP_DANCE = 72       # 舞蹈经验
EXP_TRAIN_TALK = 73  # 调教会话经验
EXP_PROSTITUTE = 74  # 卖淫经验
EXP_BUSI_LOVE = 75   # 营业爱情经验
EXP_COLOSSEUM = 76   # 斗技胜利经验
EXP_BATTLE = 80      # 战斗经验
EXP_MEDAL = 81       # 勋章经验
EXP_CRAZY_TRAIN = 66 # 狂王调教经验
EXP_IKAI = 99        # 异界经验

# ========================================
# 角色FLAG (CFLAG) 常量
# ========================================
CFLAG_STATE = 0          # 状态
CFLAG_LOCATION = 1       # 位置
CFLAG_FIRST_SEX = 15     # 初体验
CFLAG_FIRST_KISS = 16    # 初吻
CFLAG_LEVEL = 9          # 等级
CFLAG_STR = 11           # STR
CFLAG_VIT = 12           # VIT
CFLAG_INT = 13           # INT
CFLAG_AGI = 14           # AGI
CFLAG_SELL_ACTIVE = 120  # 卖春积极性
CFLAG_KIND = 151         # 善恶值
CFLAG_FAITH = 152        # 信仰值
CFLAG_INVASION_FLOOR = 501  # 侵攻楼层
CFLAG_INVASION_PROGRESS = 502 # 侵攻度
CFLAG_RESTART = 508      # 再起点
CFLAG_FAMILY = 605       # 家族
CFLAG_AGE = 600          # 年龄
CFLAG_HEIGHT = 601       # 身高
CFLAG_WEIGHT = 602       # 体重

# ========================================
# FLAG 常量
# ========================================
FLAG_DEBUG = 0           # 调试模式
FLAG_SENGEN_MAX = 9012   # 勇者生成上限

# ========================================
# 污秽 (STAIN) 常量
# ========================================
STAIN_LUB = 1            # 爱液
STAIN_V = 2              # V污秽
STAIN_SEED = 4           # 精液
STAIN_A = 8              # 肛门污秽
STAIN_MILK = 16          # 母乳
STAIN_PEE = 32           # 尿

# ========================================
# 装备 (EQUIP/TEQUIP) 常量
# ========================================
EQUIP_BLIND = 43         # 眼罩
EQUIP_ROPE = 44          # 绳索
EQUIP_GAG = 45           # 口塞
EQUIP_BONDAGE = 47       # 紧缚衣
EQUIP_VIDEO = 53         # 水晶球拍摄
EQUIP_OUTDOOR = 54       # 野外
EQUIP_COLISEUM = 55      # 死斗场
EQUIP_TENTACLE = 90      # 触手
EQUIP_BEAST = 89         # 兽奸

# ========================================
# 种族 ID - 对应 CHARA_MAKE.ERB ARG:2
# ========================================
RACE_ELF = 1             # 精灵
RACE_WEREWOLF = 2        # 人狼
RACE_VAMPIRE = 3         # 吸血鬼
RACE_DULLAHAN = 4        # 杜拉汉
RACE_DRAGON = 5          # 龙
RACE_FAIRY = 6           # 妖精
RACE_GIANT = 7           # 巨人
RACE_DARK_ELF = 8        # 黑精灵
RACE_FALLEN_ANGEL = 9    # 堕天使
RACE_DEMON = 10          # 魔族
RACE_HOBBIT = 11         # 霍比特
RACE_DWARF = 12          # 矮人
RACE_HUMAN = 13          # 人类

# 种族2 (TALENT:319 种族2) - 对应 CHARA_MAKE.ERB
RACE2_SLIME = 2          # 史莱姆
RACE2_INSECT = 3         # 昆虫
RACE2_PLANT = 4          # 植物
RACE2_TENTACLE = 5       # 触手
RACE2_FAIRY = 6          # 妖精
RACE2_GIANT = 7          # 巨人

# ========================================
# 调教指令 (TRAIN) 常量 - 对应 Train.csv
# ========================================
# 爱抚系 (0-9)
TRAIN_CARESS = 0       # 爱抚
TRAIN_CUNNI = 1        # 舔阴
TRAIN_A_CARESS = 2     # 肛门爱抚
TRAIN_MASTURBATE = 3   # 自慰
TRAIN_FELLA_M = 4      # 口交(主)
TRAIN_B_CARESS = 5     # 胸爱抚
TRAIN_KISS = 6         # 接吻
TRAIN_SPREAD = 7       # 自己扒开
TRAIN_FINGER = 8       # 插入手指
TRAIN_RIMMING = 9      # 舔肛

# 道具使用系 (10-19)
TRAIN_VIBRATOR = 10    # 振动宝石
TRAIN_POT_WORM = 11    # 壶虫
TRAIN_VIB_ROD = 12     # 振动杖
TRAIN_A_WORM = 13      # 肛门虫
TRAIN_C_CLAMP = 14     # 阴蒂夹
TRAIN_N_CLAMP = 15     # 乳头夹
TRAIN_MILKER = 16      # 榨乳器
TRAIN_ONAHOLE = 17     # 飞机杯
TRAIN_SHOWER = 18      # 淋浴
TRAIN_A_BEADS = 19     # 肛珠

# 性交系 (20-29)
TRAIN_MISSIONARY = 20  # 正常位
TRAIN_DOGGY = 21       # 背后位
TRAIN_FACE_RIDE = 22   # 对面座位
TRAIN_BACK_RIDE = 23   # 背面座位
TRAIN_REVERSE = 24     # 逆强奸
TRAIN_REVERSE_A = 25   # 逆肛门强奸
TRAIN_A_MISSIONARY = 26 # 正常位肛交
TRAIN_A_DOGGY = 27     # 背后位肛交
TRAIN_A_FACE_RIDE = 28 # 对面座位肛交
TRAIN_A_BACK_RIDE = 29 # 背面座位肛交

# 奉仕系 (30-38)
TRAIN_HAND_JOB = 30    # 手淫
TRAIN_FELLA_S = 31     # 口交(奴)
TRAIN_PAIZURI = 32     # 乳交
TRAIN_INTERCRURAL = 33 # 股间性交
TRAIN_COWGIRL = 34     # 骑乘位
TRAIN_BODY_WASH = 35   # 全身擦洗
TRAIN_A_COWGIRL = 36   # 骑乘位肛交
TRAIN_A_SERVE = 37     # 肛门侍奉
TRAIN_FOOT_JOB = 38    # 足交

# SM系 (40-49)
TRAIN_SPANKING = 40    # 打屁股
TRAIN_WHIP = 41        # 鞭
TRAIN_NEEDLE = 42      # 针
TRAIN_BLINDFOLD = 43   # 眼罩
TRAIN_ROPE = 44        # 绳子
TRAIN_GAG = 45         # 口塞
TRAIN_ENEMA = 46       # 灌肠+肛塞
TRAIN_BONDAGE = 47     # 拘束衣穿着
TRAIN_TRAMPLE = 48     # 践踏
TRAIN_A_ELECTRODE = 49 # 肛门电极

# 特殊系 (50-59)
TRAIN_LUBRICANT = 50   # 润滑液
TRAIN_APHRODISIAC = 51 # 媚药
TRAIN_DIURETIC = 52    # 利尿剂
TRAIN_VIDEO = 53       # 水晶球
TRAIN_OUTDOOR = 54     # 野外PLAY
TRAIN_ABANDON = 55     # 放置PLAY
TRAIN_TALK = 56        # 交谈
TRAIN_SHAME_PLAY = 57  # 羞耻PLAY
TRAIN_BATH = 58        # 浴室PLAY
TRAIN_BRIDE = 59       # 新妻PLAY

# 助手/百合系 (60-72)
TRAIN_ASSI_KISS = 60   # 助手接吻
TRAIN_FORCE_CUNNI = 61 # 强制舔阴
TRAIN_ASSI_SEX = 62    # 侵犯助手
TRAIN_TRIB = 63        # 磨镜
TRAIN_3P = 64          # 3P
TRAIN_REVERSE_ASSI = 65 # 逆侵犯助手
TRAIN_DUAL_FELLA = 66  # 双枪口交
TRAIN_TWIN_FELLA = 68  # 双人口交
TRAIN_DUAL_PAIZURI = 71 # 双人乳交
TRAIN_SHAVE = 72       # 刮阴毛
TRAIN_HAIR_PLAY = 73   # 拨弄发型

# ハード系 (80-90)
TRAIN_FORCE_FELLA = 80 # 强制口交
TRAIN_FIST = 81        # 拳交
TRAIN_A_FIST = 82      # 肛门拳交
TRAIN_DOUBLE_FIST = 83 # 两穴拳交
TRAIN_PEE = 85         # 放尿
TRAIN_PIERCE = 87      # 穿环
TRAIN_BEAST = 89       # 兽奸PLAY
TRAIN_B_INSERT = 90    # 乳房插入

# 触手系 (100-109)
TRAIN_T_SPAWN = 100    # 触手生物
TRAIN_T_INSERT = 101   # 触手插入
TRAIN_T_A_INSERT = 102 # 肛交触手
TRAIN_T_C_PLAY = 103   # 触手凌辱阴蒂
TRAIN_T_B_PLAY = 104   # 触手凌辱乳头
TRAIN_T_MILK = 105     # 触手榨乳
TRAIN_T_BIND = 106     # 触手紧缚
TRAIN_T_ENEMA = 107    # 触手灌肠
TRAIN_T_ORAL = 108     # 触手口辱
TRAIN_T_P_PLAY = 109   # 触手凌辱阴茎

# 着衣系 (110)
TRAIN_CHANGE_CLOTH = 110 # 穿脱衣服

# 追加系 (122-)
TRAIN_PENIS_DUEL = 122 # 阴茎互捅
TRAIN_SELF_LICK = 135  # 自助舔舐 (无头骑士专用)

# 自由・死斗场 (150, 200-)
TRAIN_FREE_P = 150     # 自由局部调教
TRAIN_COLOSSEUM = 200  # 死斗场

# ========================================
# PALAM 等级阈值
# ========================================
PALAMLV = [0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000, 500000, 1000000, 5000000, 10000000]

# ========================================
# 经验等级阈值
# ========================================
EXPLV = [0, 1, 4, 20, 50, 200, 1000, 5000]

# ========================================
# SOURCE 键常量
# ========================================
SRC_C_PLEASURE = "快C"    # 阴蒂快感
SRC_V_PLEASURE = "快V"    # 阴道快感
SRC_A_PLEASURE = "快A"    # 肛门快感
SRC_B_PLEASURE = "快B"    # 乳房快感
SRC_PAIN = "痛苦"
SRC_FEAR = "恐怖"
SRC_EXPOSE = "露出"
SRC_HUMILIATE = "屈辱"
SRC_DIRTY = "不洁"
SRC_OBEY = "恭顺"
SRC_SATISFY = "中毒充足"
SRC_DEPRESS = "抑郁"
SRC_REJECT = "反感"
SRC_LEARN = "习得"
SRC_LOVE = "情爱"
SRC_SUPPRESS = "压抑"
SRC_GROW = "发育"
SRC_DECAY = "损腐"
SRC_SEX_ACT = "性行動"

# ========================================
# 刻印 (MARK) 常量
# ========================================
MARK_PLEASURE = 0   # 快楽刻印
MARK_OBEY = 1       # 屈服刻印
MARK_TIME = 2       # 時紋刻印
MARK_REBEL = 3      # 反抗刻印
MARK_HATE = 4       # 憎悪刻印
MARK_APATHY = 5     # 無関心刻印
MARK_TERROR = 6     # 恐怖刻印

# ========================================
# 珠 (JUEL) 常量 - 编号与PALAM相同
# ========================================
JUEL_C_PLEASURE = 0   # 快Cの珠
JUEL_V_PLEASURE = 1   # 快Vの珠
JUEL_A_PLEASURE = 2   # 快Aの珠
JUEL_B_PLEASURE = 3   # 快Bの珠
JUEL_DESIRE = 4       # 欲情の珠
JUEL_OBEY = 5         # 恭順の珠
JUEL_HUMILIATE = 6    # 屈辱の珠
JUEL_FEAR = 7         # 恐怖の珠
JUEL_PAIN = 8         # 痛苦の珠
JUEL_EXPOSE = 9       # 露出の珠
JUEL_LEARN = 10       # 習得の珠
JUEL_DIRTY = 11       # 不潔の珠
JUEL_SUPPRESS = 12    # 圧抑の珠
JUEL_REJECT = 13      # 反発の珠
JUEL_LOVE = 14        # 情愛の珠
JUEL_GROW = 15        # 発育の珠
JUEL_DECAY = 16       # 損腐の珠
JUEL_NEGATE = 100     # 否定の珠

# ========================================
# 経験 (EXP) 常量
# ========================================
EXP_V_SEX = 0       # Ｖ性交経験
EXP_A_SEX = 1       # Ａ性交経験
EXP_ORAL = 2        # 口淫経験
EXP_PETTING = 3     # 愛撫経験
EXP_B_PETTING = 4   # 胸愛撫経験
EXP_ORGASM = 10     # 絶頂経験
EXP_V_ORGASM = 11   # Ｖ絶頂経験
EXP_A_ORGASM = 12   # Ａ絶頂経験
EXP_B_ORGASM = 13   # Ｂ絶頂経験
EXP_STRONG_ORGASM = 14  # 強絶頂経験
EXP_EJAC = 20       # 射精経験
EXP_SEX_SERVE = 30  # 性奉仕経験
EXP_M_SEX_SERVE = 31  # 性交奉仕経験
EXP_A_SEX_SERVE = 32  # 肛門奉仕経験
EXP_LACTATION = 40  # 噴乳経験
EXP_URINATION = 50  # 放尿経験
EXP_BESTIALITY = 55 # 獣姦経験
EXP_TENTACLE = 56   # 触手経験
EXP_LES = 60        # 百合経験
EXP_M_SEX = 70      # 性交経験
EXP_CONCEPTION = 80 # 妊娠経験
EXP_BIRTH = 81      # 出産経験

# ========================================
# パラメータ (PALAM) 常量
# ========================================
PALAM_C_PLEASURE = 0   # 快C
PALAM_V_PLEASURE = 1   # 快V
PALAM_A_PLEASURE = 2   # 快A
PALAM_B_PLEASURE = 3   # 快B
PALAM_DESIRE = 4       # 欲情
PALAM_OBEY = 5         # 恭順
PALAM_HUMILIATE = 6    # 屈辱
PALAM_FEAR = 7         # 恐怖
PALAM_PAIN = 8         # 痛苦
PALAM_EXPOSE = 9       # 露出
PALAM_LUBRICATE = 10   # 潤滑
PALAM_LEARN = 11       # 習得
PALAM_DIRTY = 12       # 不潔
PALAM_SUPPRESS = 13    # 圧抑
PALAM_LOVE = 14        # 情愛
PALAM_GROW = 15        # 発育
PALAM_DECAY = 16       # 損腐

# ========================================
# 調教装備 (TEQUIP) 常量
# ========================================
TEQUIP_VIBRATOR = 11        # 振動棒
TEQUIP_VIBRATOR_ROD = 12    # 振動の杖
TEQUIP_A_VIBRATOR = 13      # 肛門振動棒
TEQUIP_CLIT_CAP = 14        # クリキャップ
TEQUIP_NIPPLE_CAP = 15      # ニプルキャップ
TEQUIP_MILKER = 16          # 搾乳器
TEQUIP_ONAHOLE = 17         # オナホール
TEQUIP_SHOWER = 18          # シャワー
TEQUIP_A_BEADS = 19         # アナルビーズ
TEQUIP_CONDOM_P = 35        # 避妊套(主人)
TEQUIP_CONDOM_A = 36        # 避妊套(助手)
TEQUIP_BLINDFOLD = 43       # アイマスク
TEQUIP_ROPE = 44            # 縄
TEQUIP_BALLGAG = 45         # ボールギャグ
TEQUIP_ENEMA = 46           # 浣腸
TEQUIP_BONDAGE = 47         # 拘束衣
TEQUIP_A_ELECTRODE = 49     # 肛門電極
TEQUIP_VIDEO = 53           # ビデオ撮影
TEQUIP_OUTDOOR = 54         # 野外プレイ
TEQUIP_SHAME = 57           # 羞恥プレイ
TEQUIP_BATH = 58            # お風呂場
TEQUIP_BRIDE = 59           # 新妻プレイ
TEQUIP_BEAST = 89           # 獣姦
TEQUIP_TENTACLE = 90        # 触手
TEQUIP_TENTACLE_ORAL = 98   # 触手口辱

# ========================================
# 汚れ (STAIN) 常量
# ========================================
STAIN_NONE = 0       # なし
STAIN_V_SEX = 1      # Ｖ性交
STAIN_A_SEX = 2      # Ａ性交
STAIN_ORAL = 3       # 口淫
STAIN_SEMEN = 4      # 精液
STAIN_LACTATION = 5  # 母乳
STAIN_URINE = 6      # 尿
STAIN_BLOOD = 7      # 血
STAIN_BEAST = 8      # 獣
STAIN_TENTACLE = 9   # 触手

# ========================================
# キャラフラグ (CFLAG) 常量
# ========================================
CFLAG_ASSIST = 1          # 助手
CFLAG_SLAVE = 2           # 奴隷
CFLAG_HERO = 3            # 勇者
CFLAG_SEALED = 5          # 封印
CFLAG_LEVEL = 8           # レベル
CFLAG_AGE = 26            # 年齢
CFLAG_AGE_OUT = 27        # 外見年齢
CFLAG_DAILY = 35          # 日常フラグ
CFLAG_LOVER = 37          # 恋人
CFLAG_MARRIED = 38        # 既婚
CFLAG_JOB = 40            # 職業
CFLAG_CLOTH = 40          # 服装状態
CFLAG_TALENT_SEAL = 43    # 素質封印
CFLAG_MAGIC_CHAOS = 503   # 魔力暴走
CFLAG_SEX_COUNT = 600     # 性交回数
CFLAG_SEMEN_COUNT = 601   # 精液回数
CFLAG_KISS_COUNT = 602    # キス回数
CFLAG_BIRTH_COUNT = 603   # 出産回数
CFLAG_RYOUZYOKU = 130     # 畏怖記憶(敗北)
CFLAG_RYOUZYOKU_TYPE = 131 # 畏怖記憶(種類)
CFLAG_VIRGIN_SEALED = 500  # 処女封印
CFLAG_BENKI = 600          # 便器カウント
CFLAG_PROSTITUTE = 601     # 売春カウント
CFLAG_SELL_COUNT = 602     # 売却回数
CFLAG_NTR = 603            # NTR回数
CFLAG_FAMILY_ID = 606      # 家族ID
CFLAG_FAMILY_REL = 607     # 家族関係

# ========================================
# 基礎値 (BASE) 常量
# ========================================
BASE_HP = 0           # 体力
BASE_MP = 1           # 気力
BASE_EJAC = 2         # 射精
BASE_PREGNANCY = 3    # 妊娠進行