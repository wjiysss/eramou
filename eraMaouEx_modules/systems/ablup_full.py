from __future__ import annotations
"""Module for AblupFullMixin - ABLUP (ability upgrade) full methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaou import Character

from eraMaouEx_modules.core.constants import (
    JUEL_C_PLEASURE, JUEL_V_PLEASURE, JUEL_A_PLEASURE, JUEL_B_PLEASURE,
    JUEL_DESIRE, JUEL_OBEY, JUEL_HUMILIATE, JUEL_FEAR, JUEL_PAIN,
    JUEL_EXPOSE, JUEL_LEARN, JUEL_DIRTY, JUEL_SUPPRESS, JUEL_REJECT,
    JUEL_LOVE, JUEL_GROW, JUEL_DECAY,
    EXP_V_SEX, EXP_A_SEX, EXP_ORGASM, EXP_SEX, EXP_MAST, EXP_TRAIN_MAST,
    EXP_SEMEN, EXP_SERVE_PLEASURE, EXP_MASO_PLEASURE, EXP_SAD_PLEASURE,
    EXP_LES, EXP_HOMO, EXP_ABNORMAL, EXP_BESTIALITY, EXP_TENTACLE,
    EXP_TRAIN_TALK, EXP_PROSTITUTE, EXP_IKAI,
    TALENT_SHY, TALENT_REBEL, TALENT_STRONG, TALENT_FRANK, TALENT_CALM,
    TALENT_HAUGHTY, TALENT_BOAST, TALENT_HUMBLE,
    TALENT_CONTROL, TALENT_APATHY, TALENT_EMOTIONLESS, TALENT_CURIOUS,
    TALENT_CONSERVE, TALENT_ALERT, TALENT_SHOWOFF,
    TALENT_CHASTE, TALENT_UNCHASTE, TALENT_REPRESS, TALENT_OPEN, TALENT_RESIST,
    TALENT_SHAME, TALENT_NO_SHAME, TALENT_LEVERAGE,
    TALENT_MAST_MANIAC, TALENT_SEX_MANIAC, TALENT_LEWD, TALENT_A_MANIAC,
    TALENT_B_MANIAC, TALENT_TOMBOY, TALENT_PERVERT, TALENT_BI,
    TALENT_HATE_MALE, TALENT_SADIST, TALENT_JEALOUS, TALENT_LOVE, TALENT_OBEY,
    TALENT_DEVIL, TALENT_MASOCHIST, TALENT_EXHIBITIONIST,
    TALENT_C_DULL, TALENT_C_SENS, TALENT_V_DULL, TALENT_V_SENS,
    TALENT_A_DULL, TALENT_A_SENS, TALENT_B_DULL, TALENT_B_SENS,
    TALENT_SMALL_BREAST, TALENT_BIG_BREAST, TALENT_HUGE_BREAST, TALENT_NO_BREAST,
    TALENT_SUPER_BREAST,
    TALENT_FAST_LEARN, TALENT_SLOW_LEARN, TALENT_TONGUE,
    TALENT_EASY_MAST, TALENT_NO_SMELL, TALENT_HATE_SMELL,
    TALENT_SERVE_MIND, TALENT_NO_DIRTY,
    TALENT_ACCEPT_PLEASURE, TALENT_DENY_PLEASURE, TALENT_ADDICT, TALENT_EASY_FALL,
    TALENT_FUTA, TALENT_MALE, TALENT_CRAZY, TALENT_ANIMAL_EARS,
    TALENT_COUNTERATTACK, TALENT_BITCH,
    TALENT_PROSTITUTE, TALENT_KEISEI, TALENT_ELOQUENT, TALENT_REGULAR,
    TALENT_COURTED, TALENT_WIFE,
    TALENT_LOVE_SEMEN,
    ABL_C_SENS, ABL_B_SENS, ABL_V_SENS, ABL_A_SENS, ABL_P_SENS,
    ABL_SUBMIT, ABL_DESIRE, ABL_TECH, ABL_SERVE_TECH, ABL_SEX_TECH,
    ABL_SPEECH, ABL_SERVE, ABL_EXPOSE,
    ABL_SAD, ABL_MASO, ABL_LES, ABL_HOMO,
    ABL_SEX_ADDICT, ABL_SELF_MAST, ABL_SEMEN_ADDICT, ABL_LES_ADDICT,
    ABL_PROSTITUTE, ABL_BEAST_ADDICT, ABL_P_ADDICT,
)

# =====================================================================
# ABLUP_COST_TABLE - 能力升级基础成本表
# 从 ERB/ABLUP*.ERB 文件提取的基础数据
# 注意: 此表仅包含基础成本，实际成本受素质修正等因素影响
# 复杂的能力升级逻辑仍由 _ablupN 方法处理
# =====================================================================
ABLUP_COST_TABLE: Dict[int, Dict[str, Any]] = {
    # ------------------------------------------------------------------
    # ABL:0 - C感觉 (阴蒂感觉)
    # ERB: ABLUP0.ERB
    # 复杂度: 高 (感觉封锁动态上限, 多素质修正)
    # ------------------------------------------------------------------
    ABL_C_SENS: {
        "name": "C感觉",
        "max_level": 5,  # 基础上限; TALENT_MAST_MANIAC时10; 感觉封锁动态计算
        "talent_req": [TALENT_MAST_MANIAC],  # Lv5以上需要
        "talent_block": [],  # TALENT_C_DULL & 2 封锁
        "levels": [
            {"juel": {JUEL_C_PLEASURE: 1}, "exp": {}},           # 0→1
            {"juel": {JUEL_C_PLEASURE: 20}, "exp": {}},          # 1→2
            {"juel": {JUEL_C_PLEASURE: 400}, "exp": {}},         # 2→3
            {"juel": {JUEL_C_PLEASURE: 8000}, "exp": {}},        # 3→4
            {"juel": {JUEL_C_PLEASURE: 20000}, "exp": {}},       # 4→5
            {"juel": {JUEL_C_PLEASURE: 40000}, "exp": {}},       # 5→6
            {"juel": {JUEL_C_PLEASURE: 60000}, "exp": {}},       # 6→7
            {"juel": {JUEL_C_PLEASURE: 90000}, "exp": {}},       # 7→8
            {"juel": {JUEL_C_PLEASURE: 120000}, "exp": {}},      # 8→9
            {"juel": {JUEL_C_PLEASURE: 180000}, "exp": {}},      # 9→10
            # Lv10+ 使用递推公式: base*125/100 per level
        ],
        "note": "Lv10-14: base=180000*1.25^n; Lv15-19: base=362000*1.20^n; Lv20-24: base=583000*1.15^n; 感觉封锁数影响上限和成本",
    },

    # ------------------------------------------------------------------
    # ABL:1 - B感觉 (乳房感觉)
    # ERB: ABLUP1.ERB
    # 复杂度: 高 (感觉封锁动态上限, 多素质修正)
    # ------------------------------------------------------------------
    ABL_B_SENS: {
        "name": "B感觉",
        "max_level": 5,  # 基础上限; TALENT_B_MANIAC时10
        "talent_req": [TALENT_B_MANIAC],  # Lv5以上需要
        "talent_block": [],  # TALENT_B_DULL & 2 封锁
        "levels": [
            {"juel": {JUEL_LOVE: 1}, "exp": {}},                 # 0→1
            {"juel": {JUEL_LOVE: 20}, "exp": {}},                # 1→2
            {"juel": {JUEL_LOVE: 400}, "exp": {}},               # 2→3
            {"juel": {JUEL_LOVE: 8000}, "exp": {}},              # 3→4
            {"juel": {JUEL_LOVE: 20000}, "exp": {}},             # 4→5
            {"juel": {JUEL_LOVE: 40000}, "exp": {}},             # 5→6
            {"juel": {JUEL_LOVE: 60000}, "exp": {}},             # 6→7
            {"juel": {JUEL_LOVE: 90000}, "exp": {}},             # 7→8
            {"juel": {JUEL_LOVE: 120000}, "exp": {}},            # 8→9
            {"juel": {JUEL_LOVE: 180000}, "exp": {}},            # 9→10
        ],
        "note": "Lv10+同C感觉递推; 素质修正: B钝感x1.2, B敏感x0.8, 巨乳x1.1, 爆乳x1.2, 超乳x1.3, 贫乳x0.8, 绝壁x0.65, 淫乱x0.8, 弄乳狂x0.8",
    },

    # ------------------------------------------------------------------
    # ABL:2 - V感觉 (私处感觉)
    # ERB: ABLUP2.ERB
    # 复杂度: 高 (男人不可, 感觉封锁, 多素质修正)
    # ------------------------------------------------------------------
    ABL_V_SENS: {
        "name": "V感觉",
        "max_level": 5,  # TALENT_SEX_MANIAC时10
        "talent_req": [TALENT_SEX_MANIAC],  # Lv5以上需要
        "talent_block": [TALENT_MALE],  # 男人不可
        "levels": [
            {"juel": {JUEL_V_PLEASURE: 1}, "exp": {EXP_V_SEX: 2}},           # 0→1
            {"juel": {JUEL_V_PLEASURE: 20}, "exp": {EXP_V_SEX: 10}},         # 1→2
            {"juel": {JUEL_V_PLEASURE: 400}, "exp": {EXP_V_SEX: 30}},        # 2→3
            {"juel": {JUEL_V_PLEASURE: 8000}, "exp": {EXP_V_SEX: 75}},       # 3→4
            {"juel": {JUEL_V_PLEASURE: 20000}, "exp": {EXP_V_SEX: 150}},     # 4→5
            {"juel": {JUEL_V_PLEASURE: 40000}, "exp": {EXP_V_SEX: 180}},     # 5→6
            {"juel": {JUEL_V_PLEASURE: 60000}, "exp": {EXP_V_SEX: 250}},     # 6→7
            {"juel": {JUEL_V_PLEASURE: 90000}, "exp": {EXP_V_SEX: 350}},     # 7→8
            {"juel": {JUEL_V_PLEASURE: 120000}, "exp": {EXP_V_SEX: 500}},    # 8→9
            {"juel": {JUEL_V_PLEASURE: 180000}, "exp": {EXP_V_SEX: 600}},    # 9→10
        ],
        "note": "V封锁(TALENT_V_DULL&2)不可; 素质修正: V钝感x1.2/1.1, V敏感x0.8, 淫乱x0.8, 性爱狂x0.8",
    },

    # ------------------------------------------------------------------
    # ABL:3 - A感觉 (肛门感觉)
    # ERB: ABLUP3.ERB
    # 复杂度: 高 (感觉封锁, 多素质修正)
    # ------------------------------------------------------------------
    ABL_A_SENS: {
        "name": "A感觉",
        "max_level": 5,  # TALENT_A_MANIAC时10
        "talent_req": [TALENT_A_MANIAC],  # Lv5以上需要
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_A_PLEASURE: 1}, "exp": {EXP_A_SEX: 2}},           # 0→1
            {"juel": {JUEL_A_PLEASURE: 20}, "exp": {EXP_A_SEX: 10}},         # 1→2
            {"juel": {JUEL_A_PLEASURE: 400}, "exp": {EXP_A_SEX: 30}},        # 2→3
            {"juel": {JUEL_A_PLEASURE: 8000}, "exp": {EXP_A_SEX: 75}},       # 3→4
            {"juel": {JUEL_A_PLEASURE: 20000}, "exp": {EXP_A_SEX: 150}},     # 4→5
            {"juel": {JUEL_A_PLEASURE: 40000}, "exp": {EXP_A_SEX: 180}},     # 5→6
            {"juel": {JUEL_A_PLEASURE: 60000}, "exp": {EXP_A_SEX: 250}},     # 6→7
            {"juel": {JUEL_A_PLEASURE: 90000}, "exp": {EXP_A_SEX: 350}},     # 7→8
            {"juel": {JUEL_A_PLEASURE: 120000}, "exp": {EXP_A_SEX: 500}},    # 8→9
            {"juel": {JUEL_A_PLEASURE: 180000}, "exp": {EXP_A_SEX: 600}},    # 9→10
        ],
        "note": "A封锁(TALENT_A_DULL&2)不可; 素质修正: A钝感x1.2/1.1, A敏感x0.8, 淫乱x0.8, 尻穴狂x0.8",
    },

    # ------------------------------------------------------------------
    # ABL:4 - P感觉 (局部感觉)
    # ERB: ABLUP4.ERB
    # 复杂度: 低 (简单JUEL成本)
    # ------------------------------------------------------------------
    ABL_P_SENS: {
        "name": "局部感觉",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_GROW: 1}, "exp": {}},                  # 0→1
            {"juel": {JUEL_GROW: 50}, "exp": {}},                 # 1→2
            {"juel": {JUEL_GROW: 600}, "exp": {}},                # 2→3
            {"juel": {JUEL_GROW: 7000}, "exp": {}},               # 3→4 (戒备森严x2.0)
            {"juel": {JUEL_GROW: 45000}, "exp": {}},              # 4→5 (戒备森严x3.0)
        ],
        "note": "Lv3/4时戒备森严(TALENT_ALERT)分别x2.0/x3.0",
    },

    # ------------------------------------------------------------------
    # ABL:5 - 话术 (ERB中为A感觉相关, 实际是话术)
    # ERB: ABLUP5.ERB
    # 复杂度: 中 (EXP阈值可降低成本)
    # ------------------------------------------------------------------
    5: {
        "name": "话术",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_A_PLEASURE: 1}, "exp": {EXP_A_SEX: 2}},           # 0→1
            {"juel": {JUEL_A_PLEASURE: 50}, "exp": {EXP_A_SEX: 10}},         # 1→2 (EXP:A>=30时A=20)
            {"juel": {JUEL_A_PLEASURE: 600}, "exp": {EXP_A_SEX: 30}},        # 2→3 (EXP:A>=60时A=100)
            {"juel": {JUEL_A_PLEASURE: 7000}, "exp": {EXP_A_SEX: 150}},      # 3→4 (EXP:A>=120时A=500; 戒备森严x2.0)
            {"juel": {JUEL_A_PLEASURE: 45000}, "exp": {EXP_A_SEX: 300}},     # 4→5 (EXP:A>=120时A=8000; 戒备森严x3.0)
        ],
        "note": "EXP:A性交经验达到阈值时JUEL成本降低; Lv3/4时戒备森严修正",
    },

    # ------------------------------------------------------------------
    # ABL:6 - 性技
    # ERB: ABLUP6.ERB
    # 复杂度: 高 (三种支付选项, ABL:0前置, 异常经验需求)
    # ------------------------------------------------------------------
    6: {
        "name": "性技",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            # Option0: 屈辱+绝顶+精液经验, Option1: 欲情+侍奉快乐经验, Option2: 习得+绝顶经验
            {"juel": {JUEL_HUMILIATE: 100}, "exp": {EXP_ORGASM: 1, EXP_SEMEN: 1}},  # 0→1
            {"juel": {JUEL_HUMILIATE: 1200}, "exp": {EXP_ORGASM: 3, EXP_SEMEN: 3}},  # 1→2
            {"juel": {JUEL_HUMILIATE: 5000}, "exp": {EXP_ORGASM: 6, EXP_SEMEN: 6}},  # 2→3
            {"juel": {JUEL_HUMILIATE: 10000}, "exp": {EXP_ORGASM: 10, EXP_SEMEN: 10}},  # 3→4
            {"juel": {JUEL_HUMILIATE: 30000}, "exp": {EXP_ORGASM: 20, EXP_SEMEN: 20}},  # 4→5
        ],
        "note": "三种支付选项: [0]屈辱+绝顶+精液经验 [1]欲情+侍奉快乐经验 [2]习得+绝顶经验1; 需要ABL:0>=Lv+1; Lv3/4需异常经验(盲从除外); 倒错的x0.75",
    },

    # ------------------------------------------------------------------
    # ABL:7 - 性交
    # ERB: ABLUP7.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    7: {
        "name": "性交",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_PAIN: 100}, "exp": {EXP_ORGASM: 1}},              # 0→1
            {"juel": {JUEL_PAIN: 1000}, "exp": {EXP_ORGASM: 1}},             # 1→2
            {"juel": {JUEL_PAIN: 5000}, "exp": {EXP_TRAIN_MAST: 1}},         # 2→3
            {"juel": {JUEL_PAIN: 15000}, "exp": {EXP_TRAIN_MAST: 1}},        # 3→4 (戒备森严x2.0)
            {"juel": {JUEL_PAIN: 35000}, "exp": {EXP_TRAIN_MAST: 1}},        # 4→5 (戒备森严x3.0)
        ],
        "note": "需要ABL:1>=Lv+1; Lv<2需绝顶经验,Lv>=2需调教自慰经验; Lv3/4需异常经验(爱表现除外); 倒错的x0.75x0.50",
    },

    # ------------------------------------------------------------------
    # ABL:8 - 奉仕
    # ERB: ABLUP8.ERB
    # 复杂度: 高 (两种支付选项)
    # ------------------------------------------------------------------
    8: {
        "name": "奉仕",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            # Option0: 露出+欲情, Option1: 露出+屈服+绝顶经验
            {"juel": {JUEL_EXPOSE: 100, JUEL_DESIRE: 100}, "exp": {}},       # 0→1
            {"juel": {JUEL_EXPOSE: 500, JUEL_DESIRE: 500}, "exp": {}},       # 1→2
            {"juel": {JUEL_EXPOSE: 1200, JUEL_DESIRE: 1000}, "exp": {}},     # 2→3
            {"juel": {JUEL_EXPOSE: 3000, JUEL_HUMILIATE: 6000}, "exp": {EXP_MASO_PLEASURE: 10}},  # 3→4
            {"juel": {JUEL_EXPOSE: 5000, JUEL_HUMILIATE: 12000}, "exp": {EXP_MASO_PLEASURE: 50}},  # 4→5
        ],
        "note": "两种支付选项; 需要ABL:1>=Lv+1; Lv3/4需异常经验(开放除外); 开放x0.5, 倒错的x0.75",
    },

    # ------------------------------------------------------------------
    # ABL:9 - 露出
    # ERB: ABLUP9.ERB
    # 复杂度: 高 (两种支付选项)
    # ------------------------------------------------------------------
    9: {
        "name": "露出",
        "max_level": 5,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            # Option0: 欲情+百合经验, Option1: 快C+百合经验
            {"juel": {JUEL_DESIRE: 200}, "exp": {EXP_LES: 50}},              # 0→1
            {"juel": {JUEL_DESIRE: 1000}, "exp": {EXP_LES: 200}},            # 1→2
            {"juel": {JUEL_DESIRE: 3000, JUEL_HUMILIATE: 1000}, "exp": {EXP_LES: 500}},  # 2→3
            {"juel": {JUEL_DESIRE: 8000, JUEL_HUMILIATE: 2000}, "exp": {EXP_LES: 1000}},  # 3→4
            {"juel": {JUEL_DESIRE: 20000, JUEL_HUMILIATE: 5000}, "exp": {EXP_LES: 2000}},  # 4→5
        ],
        "note": "两种支付选项: [0]欲情(+屈服)+百合经验 [1]快C+百合经验; Lv3/4需异常经验(双性恋除外); 双性恋x0.25, 倒错的x0.75",
    },

    # ------------------------------------------------------------------
    # ABL:10 - 顺从
    # ERB: ABLUP10.ERB
    # 复杂度: 高 (四种支付选项, 多素质修正)
    # ------------------------------------------------------------------
    ABL_SUBMIT: {
        "name": "顺从",
        "max_level": 5,  # TALENT_LOVE/TALENT_OBEY时10
        "talent_req": [TALENT_LOVE, TALENT_OBEY],  # Lv5以上需要
        "talent_block": [],
        "levels": [
            # 四种选项: [0]习得 [1]欲情 [2]恭顺 [3]屈服
            {"juel": {JUEL_LEARN: 10, JUEL_DESIRE: 300, JUEL_OBEY: 10, JUEL_HUMILIATE: 200}, "exp": {}},  # 0→1
            {"juel": {JUEL_LEARN: 150, JUEL_DESIRE: 1000, JUEL_OBEY: 100, JUEL_HUMILIATE: 1200}, "exp": {}},  # 1→2
            {"juel": {JUEL_LEARN: 1000, JUEL_DESIRE: 2000, JUEL_OBEY: 800, JUEL_HUMILIATE: 3000}, "exp": {}},  # 2→3
            {"juel": {JUEL_LEARN: 3000, JUEL_OBEY: 3000, JUEL_HUMILIATE: 12000}, "exp": {}},  # 3→4
            {"juel": {JUEL_LEARN: 8000, JUEL_OBEY: 5000}, "exp": {}},  # 4→5
            {"juel": {JUEL_LEARN: 12000, JUEL_OBEY: 10000}, "exp": {}},  # 5→6
            {"juel": {JUEL_LEARN: 25000, JUEL_OBEY: 20000}, "exp": {}},  # 6→7
            {"juel": {JUEL_OBEY: 40000}, "exp": {}},  # 7→8
            {"juel": {JUEL_OBEY: 80000}, "exp": {}},  # 8→9
            {"juel": {JUEL_OBEY: 150000}, "exp": {}},  # 9→10
        ],
        "note": "四种支付选项任选; Lv4需异常经验1(Lv7需2)(胆怯/坦率/容易陷落/淫乱/爱慕/盲从除外); 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:11 - 欲望
    # ERB: ABLUP11.ERB
    # 复杂度: 中 (单一JUEL+异常经验)
    # ------------------------------------------------------------------
    ABL_DESIRE: {
        "name": "欲望",
        "max_level": 5,  # TALENT_EASY_FALL/TALENT_LEWD时10
        "talent_req": [TALENT_EASY_FALL, TALENT_LEWD],  # Lv5以上需要
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 5}, "exp": {}},                # 0→1
            {"juel": {JUEL_DESIRE: 50}, "exp": {}},               # 1→2
            {"juel": {JUEL_DESIRE: 1000}, "exp": {}},             # 2→3
            {"juel": {JUEL_DESIRE: 5000}, "exp": {}},             # 3→4 (戒备森严x1.5)
            {"juel": {JUEL_DESIRE: 12000}, "exp": {EXP_ABNORMAL: 1}},  # 4→5 (戒备森严x2.0; 需异常经验1)
            {"juel": {JUEL_DESIRE: 20000}, "exp": {}},            # 5→6 (戒备森严x2.5)
            {"juel": {JUEL_DESIRE: 30000}, "exp": {}},            # 6→7 (戒备森严x3.0)
            {"juel": {JUEL_DESIRE: 50000}, "exp": {EXP_ABNORMAL: 3}},  # 7→8 (需异常经验3)
            {"juel": {JUEL_DESIRE: 80000}, "exp": {}},            # 8→9
            {"juel": {JUEL_DESIRE: 150000}, "exp": {}},           # 9→10
        ],
        "note": "Lv4需异常经验1(开放/接受快感/容易陷落/淫乱/疯狂除外); Lv7需异常经验3; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:12 - 技巧
    # ERB: ABLUP12.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_TECH: {
        "name": "技巧",
        "max_level": 10,  # ABL:12+ABL:15<15
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_FEAR: 1}, "exp": {}},                  # 0→1
            {"juel": {JUEL_FEAR: 25}, "exp": {}},                 # 1→2
            {"juel": {JUEL_FEAR: 200}, "exp": {}},                # 2→3
            {"juel": {JUEL_FEAR: 3000}, "exp": {}},               # 3→4 (戒备森严x1.5)
            {"juel": {JUEL_FEAR: 8000}, "exp": {}},               # 4→5 (戒备森严x2.0)
            {"juel": {JUEL_FEAR: 12000}, "exp": {}},              # 5→6 (戒备森严x2.5)
            {"juel": {JUEL_FEAR: 16000}, "exp": {}},              # 6→7 (戒备森严x3.0)
            {"juel": {JUEL_FEAR: 22000}, "exp": {}},              # 7→8
            {"juel": {JUEL_FEAR: 28000}, "exp": {}},              # 8→9
            {"juel": {JUEL_FEAR: 35000}, "exp": {}},              # 9→10
        ],
        "note": "ABL:12+ABL:15合计上限15; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:13 - 自慰
    # ERB: ABLUP13.ERB
    # 复杂度: 中 (ABL前置需求)
    # ------------------------------------------------------------------
    ABL_SERVE_TECH: {
        "name": "自慰",
        "max_level": 10,  # ABL:13+ABL:14<10
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_FEAR: 5}, "exp": {}},                  # 0→1
            {"juel": {JUEL_FEAR: 400}, "exp": {}},                # 1→2
            {"juel": {JUEL_FEAR: 1000}, "exp": {}},               # 2→3 (戒备森严x1.5)
            {"juel": {JUEL_FEAR: 3000}, "exp": {}},               # 3→4 (戒备森严x2.0)
            {"juel": {JUEL_FEAR: 6000}, "exp": {}},               # 4→5 (戒备森严x2.5)
            {"juel": {JUEL_FEAR: 9000}, "exp": {}},               # 5→6 (戒备森严x3.0)
            {"juel": {JUEL_FEAR: 12000}, "exp": {}},              # 6→7
            {"juel": {JUEL_FEAR: 16000}, "exp": {}},              # 7→8
            {"juel": {JUEL_FEAR: 20000}, "exp": {}},              # 8→9
            {"juel": {JUEL_FEAR: 25000}, "exp": {}},              # 9→10
        ],
        "note": "ABL:13+ABL:14合计上限10; Lv>=5需ABL:16>=5; Lv<5需ABL:12>=Lv+1; Lv>=5需ABL:16>=Lv+1; ABL:16等级影响成本",
    },

    # ------------------------------------------------------------------
    # ABL:14 - 奉仕精神
    # ERB: ABLUP14.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_SEX_TECH: {
        "name": "奉仕精神",
        "max_level": 10,  # ABL:13+ABL:14<10
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_FEAR: 1}, "exp": {EXP_SEX: 3}},       # 0→1
            {"juel": {JUEL_FEAR: 10}, "exp": {EXP_SEX: 10}},     # 1→2
            {"juel": {JUEL_FEAR: 100}, "exp": {EXP_SEX: 30}},    # 2→3
            {"juel": {JUEL_FEAR: 1500}, "exp": {EXP_SEX: 80}},   # 3→4 (戒备森严x1.5)
            {"juel": {JUEL_FEAR: 4000}, "exp": {EXP_SEX: 100}},  # 4→5 (戒备森严x2.0)
            {"juel": {JUEL_FEAR: 5000}, "exp": {EXP_SEX: 130}},  # 5→6 (戒备森严x2.5)
            {"juel": {JUEL_FEAR: 6500}, "exp": {EXP_SEX: 160}},  # 6→7 (戒备森严x3.0)
            {"juel": {JUEL_FEAR: 8000}, "exp": {EXP_SEX: 200}},  # 7→8
            {"juel": {JUEL_FEAR: 10000}, "exp": {EXP_SEX: 250}}, # 8→9
            {"juel": {JUEL_FEAR: 15000}, "exp": {EXP_SEX: 300}}, # 9→10
        ],
        "note": "ABL:13+ABL:14合计上限10; 需ABL:12>=Lv+1(若ABL:12<5); ABL:30等级影响成本",
    },

    # ------------------------------------------------------------------
    # ABL:15 - 话术
    # ERB: ABLUP15.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_SPEECH: {
        "name": "话术",
        "max_level": 10,  # ABL:12+ABL:15<15
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_FEAR: 1}, "exp": {EXP_TRAIN_TALK: 3, EXP_PROSTITUTE: 5}},  # 0→1
            {"juel": {JUEL_FEAR: 10}, "exp": {EXP_TRAIN_TALK: 10, EXP_PROSTITUTE: 20}},  # 1→2
            {"juel": {JUEL_FEAR: 100}, "exp": {EXP_TRAIN_TALK: 30, EXP_PROSTITUTE: 50}},  # 2→3
            {"juel": {JUEL_FEAR: 1500}, "exp": {EXP_TRAIN_TALK: 50, EXP_PROSTITUTE: 100}},  # 3→4
            {"juel": {JUEL_FEAR: 3000}, "exp": {EXP_TRAIN_TALK: 100, EXP_PROSTITUTE: 150}},  # 4→5
            {"juel": {JUEL_FEAR: 4000}, "exp": {EXP_TRAIN_TALK: 120, EXP_PROSTITUTE: 180}},  # 5→6
            {"juel": {JUEL_FEAR: 5200}, "exp": {EXP_TRAIN_TALK: 150, EXP_PROSTITUTE: 250}},  # 6→7
            {"juel": {JUEL_FEAR: 7500}, "exp": {EXP_TRAIN_TALK: 180, EXP_PROSTITUTE: 320}},  # 7→8
            {"juel": {JUEL_FEAR: 9000}, "exp": {EXP_TRAIN_TALK: 220, EXP_PROSTITUTE: 350}},  # 8→9
            {"juel": {JUEL_FEAR: 13000}, "exp": {EXP_TRAIN_TALK: 250, EXP_PROSTITUTE: 400}},  # 9→10
        ],
        "note": "ABL:12+ABL:15合计上限15; EXP:73或EXP:74满足即可; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:16 - 侍奉精神
    # ERB: ABLUP16.ERB
    # 复杂度: 高 (三种支付选项, 大量素质修正)
    # ------------------------------------------------------------------
    ABL_SERVE: {
        "name": "侍奉精神",
        "max_level": 5,  # TALENT_SERVE_MIND/TALENT_LOVE/TALENT_OBEY时10
        "talent_req": [TALENT_SERVE_MIND, TALENT_LOVE, TALENT_OBEY],  # Lv5以上需要
        "talent_block": [],
        "levels": [
            # Option0: 屈辱+绝顶+精液, Option1: 欲情+侍奉快乐, Option2: 习得+绝顶
            {"juel": {JUEL_HUMILIATE: 100}, "exp": {EXP_ORGASM: 1, EXP_SEMEN: 1}},  # 0→1
            {"juel": {JUEL_HUMILIATE: 1200}, "exp": {EXP_ORGASM: 3, EXP_SEMEN: 3}},  # 1→2
            {"juel": {JUEL_HUMILIATE: 5000}, "exp": {EXP_ORGASM: 6, EXP_SEMEN: 6}},  # 2→3
            {"juel": {JUEL_HUMILIATE: 10000}, "exp": {EXP_ORGASM: 10, EXP_SEMEN: 10}},  # 3→4
            {"juel": {JUEL_HUMILIATE: 30000}, "exp": {EXP_ORGASM: 20, EXP_SEMEN: 20}},  # 4→5
            {"juel": {JUEL_HUMILIATE: 50000}, "exp": {EXP_ORGASM: 80, EXP_SEMEN: 80}},  # 5→6
            {"juel": {JUEL_HUMILIATE: 70000}, "exp": {EXP_ORGASM: 150, EXP_SEMEN: 150}},  # 6→7
            {"juel": {JUEL_HUMILIATE: 100000}, "exp": {EXP_ORGASM: 200, EXP_SEMEN: 200}},  # 7→8
            {"juel": {JUEL_HUMILIATE: 150000}, "exp": {EXP_ORGASM: 400, EXP_SEMEN: 400}},  # 8→9
            {"juel": {JUEL_HUMILIATE: 200000}, "exp": {EXP_ORGASM: 800, EXP_SEMEN: 800}},  # 9→10
        ],
        "note": "三种支付选项; 需ABL:10>=Lv+1; Lv>=3需异常经验(献身的/爱慕/盲从除外); 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:17 - 露出癖
    # ERB: ABLUP17.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_EXPOSE: {
        "name": "露出癖",
        "max_level": 5,  # TALENT_FRANK/TALENT_OPEN/TALENT_SHOWOFF/TALENT_EXHIBITIONIST时10
        "talent_req": [TALENT_FRANK, TALENT_OPEN, TALENT_SHOWOFF, TALENT_EXHIBITIONIST],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_PAIN: 100}, "exp": {EXP_ORGASM: 1}},              # 0→1
            {"juel": {JUEL_PAIN: 1000}, "exp": {EXP_TRAIN_MAST: 1}},         # 1→2
            {"juel": {JUEL_PAIN: 3000}, "exp": {}},                           # 2→3
            {"juel": {JUEL_PAIN: 6000}, "exp": {}},                           # 3→4 (戒备森严x1.5)
            {"juel": {JUEL_PAIN: 12000}, "exp": {}},                          # 4→5 (戒备森严x2.0)
            {"juel": {JUEL_PAIN: 25000}, "exp": {}},                          # 5→6 (戒备森严x2.5)
            {"juel": {JUEL_PAIN: 50000}, "exp": {}},                          # 6→7 (戒备森严x3.0)
            {"juel": {JUEL_PAIN: 80000}, "exp": {}},                          # 7→8
            {"juel": {JUEL_PAIN: 120000}, "exp": {}},                         # 8→9
            {"juel": {JUEL_PAIN: 150000}, "exp": {}},                         # 9→10
        ],
        "note": "需ABL:11或ABL:10>=Lv+1(爱慕时); Lv>=3需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:20 - 抖S气质 (施虐快乐)
    # ERB: ABLUP20.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_SAD: {
        "name": "施虐快乐",
        "max_level": 5,  # TALENT_PERVERT/TALENT_SADIST/TALENT_COUNTERATTACK时10
        "talent_req": [TALENT_PERVERT, TALENT_SADIST, TALENT_COUNTERATTACK],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 100}, "exp": {EXP_SAD_PLEASURE: 5}},      # 0→1
            {"juel": {JUEL_DESIRE: 500}, "exp": {EXP_SAD_PLEASURE: 20}},     # 1→2
            {"juel": {JUEL_DESIRE: 1500}, "exp": {EXP_SAD_PLEASURE: 50}},    # 2→3
            {"juel": {JUEL_DESIRE: 3000}, "exp": {EXP_SAD_PLEASURE: 120}},   # 3→4
            {"juel": {JUEL_DESIRE: 5000}, "exp": {EXP_SAD_PLEASURE: 300}},   # 4→5
            {"juel": {JUEL_DESIRE: 8000}, "exp": {EXP_SAD_PLEASURE: 600}},   # 5→6
            {"juel": {JUEL_DESIRE: 12000}, "exp": {EXP_SAD_PLEASURE: 1500}}, # 6→7
            {"juel": {JUEL_DESIRE: 15000}, "exp": {EXP_SAD_PLEASURE: 3000}}, # 7→8
            {"juel": {JUEL_DESIRE: 25000}, "exp": {EXP_SAD_PLEASURE: 5000}}, # 8→9
            {"juel": {JUEL_DESIRE: 30000}, "exp": {EXP_SAD_PLEASURE: 8000}}, # 9→10
        ],
        "note": "ABL:20+ABL:21合计上限20; 需ABL:11>=Lv+1; Lv3/4/7需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:21 - 抖M气质 (受虐快乐)
    # ERB: ABLUP21.ERB
    # 复杂度: 高 (两种支付选项)
    # ------------------------------------------------------------------
    ABL_MASO: {
        "name": "受虐快乐",
        "max_level": 5,  # TALENT_SHY/TALENT_CALM/TALENT_LEVERAGE/TALENT_MASOCHIST时10
        "talent_req": [TALENT_SHY, TALENT_CALM, TALENT_LEVERAGE, TALENT_MASOCHIST],
        "talent_block": [],
        "levels": [
            # Option0: 露出+欲情, Option1: 露出+屈服+绝顶经验
            {"juel": {JUEL_EXPOSE: 100, JUEL_DESIRE: 100}, "exp": {}},       # 0→1
            {"juel": {JUEL_EXPOSE: 500, JUEL_DESIRE: 500}, "exp": {}},       # 1→2
            {"juel": {JUEL_EXPOSE: 1200, JUEL_DESIRE: 1000}, "exp": {}},     # 2→3
            {"juel": {JUEL_EXPOSE: 2800, JUEL_HUMILIATE: 6000}, "exp": {EXP_MASO_PLEASURE: 30}},  # 3→4
            {"juel": {JUEL_EXPOSE: 4300, JUEL_HUMILIATE: 12000}, "exp": {EXP_MASO_PLEASURE: 80}},  # 4→5
            {"juel": {JUEL_EXPOSE: 6000, JUEL_HUMILIATE: 24000}, "exp": {EXP_MASO_PLEASURE: 150}},  # 5→6
            {"juel": {JUEL_EXPOSE: 8000, JUEL_HUMILIATE: 38000}, "exp": {EXP_MASO_PLEASURE: 200}},  # 6→7
            {"juel": {JUEL_EXPOSE: 11000, JUEL_HUMILIATE: 56000}, "exp": {EXP_MASO_PLEASURE: 300}},  # 7→8
            {"juel": {JUEL_EXPOSE: 15000, JUEL_HUMILIATE: 86000}, "exp": {EXP_MASO_PLEASURE: 450}},  # 8→9
            {"juel": {JUEL_EXPOSE: 20000, JUEL_HUMILIATE: 120000}, "exp": {EXP_MASO_PLEASURE: 600}},  # 9→10
        ],
        "note": "两种支付选项; ABL:20+ABL:21合计上限20; 需ABL:11>=Lv+1; Lv3/4/7需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:22 - 百合气质
    # ERB: ABLUP22.ERB
    # 复杂度: 高 (两种支付选项, 男人不可)
    # ------------------------------------------------------------------
    ABL_LES: {
        "name": "百合气质",
        "max_level": 5,  # TALENT_OPEN/TALENT_PERVERT/TALENT_BI/TALENT_HATE_MALE/TALENT_CRAZY时10
        "talent_req": [TALENT_OPEN, TALENT_PERVERT, TALENT_BI, TALENT_HATE_MALE, TALENT_CRAZY],
        "talent_block": [TALENT_MALE],  # 男人不可
        "levels": [
            # Option0: 欲情+屈服+百合经验, Option1: 快C+百合经验
            {"juel": {JUEL_DESIRE: 200}, "exp": {EXP_LES: 50}},              # 0→1
            {"juel": {JUEL_DESIRE: 1000}, "exp": {EXP_LES: 150}},            # 1→2
            {"juel": {JUEL_DESIRE: 3000, JUEL_HUMILIATE: 1000}, "exp": {EXP_LES: 300}},  # 2→3
            {"juel": {JUEL_DESIRE: 8000, JUEL_HUMILIATE: 2000}, "exp": {EXP_LES: 500}},  # 3→4
            {"juel": {JUEL_DESIRE: 20000, JUEL_HUMILIATE: 5000}, "exp": {EXP_LES: 800}},  # 4→5
            {"juel": {JUEL_DESIRE: 40000, JUEL_HUMILIATE: 10000}, "exp": {EXP_LES: 1200}},  # 5→6
            {"juel": {JUEL_DESIRE: 80000, JUEL_HUMILIATE: 13000}, "exp": {EXP_LES: 1800}},  # 6→7
            {"juel": {JUEL_DESIRE: 150000, JUEL_HUMILIATE: 18000}, "exp": {EXP_LES: 2600}},  # 7→8
            {"juel": {JUEL_DESIRE: 200000, JUEL_HUMILIATE: 30000}, "exp": {EXP_LES: 3600}},  # 8→9
            {"juel": {JUEL_DESIRE: 300000, JUEL_HUMILIATE: 50000}, "exp": {EXP_LES: 5000}},  # 9→10
        ],
        "note": "两种支付选项; 男人不可; 需ABL:11>=Lv+1; Lv>=3需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:23 - 断背气质
    # ERB: ABLUP23.ERB
    # 复杂度: 高 (两种支付选项, 需要男人素质)
    # ------------------------------------------------------------------
    ABL_HOMO: {
        "name": "断背气质",
        "max_level": 5,  # TALENT_OPEN/TALENT_PERVERT/TALENT_BI/TALENT_CRAZY时10
        "talent_req": [TALENT_OPEN, TALENT_PERVERT, TALENT_BI, TALENT_CRAZY],
        "talent_block": [],  # 非男人不可 (TALENT:122==0时不可)
        "levels": [
            # Option0: 欲情+屈服+断背经验, Option1: 快A+断背经验
            {"juel": {JUEL_DESIRE: 200}, "exp": {EXP_HOMO: 50}},             # 0→1
            {"juel": {JUEL_DESIRE: 1000}, "exp": {EXP_HOMO: 150}},           # 1→2
            {"juel": {JUEL_DESIRE: 3000, JUEL_HUMILIATE: 1000}, "exp": {EXP_HOMO: 300}},  # 2→3
            {"juel": {JUEL_DESIRE: 8000, JUEL_HUMILIATE: 2000}, "exp": {EXP_HOMO: 500}},  # 3→4
            {"juel": {JUEL_DESIRE: 20000, JUEL_HUMILIATE: 5000}, "exp": {EXP_HOMO: 800}},  # 4→5
            {"juel": {JUEL_DESIRE: 40000, JUEL_HUMILIATE: 10000}, "exp": {EXP_HOMO: 1200}},  # 5→6
            {"juel": {JUEL_DESIRE: 80000, JUEL_HUMILIATE: 13000}, "exp": {EXP_HOMO: 1800}},  # 6→7
            {"juel": {JUEL_DESIRE: 150000, JUEL_HUMILIATE: 18000}, "exp": {EXP_HOMO: 2600}},  # 7→8
            {"juel": {JUEL_DESIRE: 200000, JUEL_HUMILIATE: 30000}, "exp": {EXP_HOMO: 3600}},  # 8→9
            {"juel": {JUEL_DESIRE: 300000, JUEL_HUMILIATE: 50000}, "exp": {EXP_HOMO: 5000}},  # 9→10
        ],
        "note": "两种支付选项; 需要TALENT:122(男人); Lv>=3需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:30 - 性交中毒
    # ERB: ABLUP30.ERB
    # 复杂度: 高 (两种支付选项, 合计上限)
    # ------------------------------------------------------------------
    ABL_SEX_ADDICT: {
        "name": "性交中毒",
        "max_level": 5,  # TALENT_LOVE/TALENT_LEWD/TALENT_SERVE_MIND/TALENT_ACCEPT_PLEASURE/TALENT_SEX_MANIAC/TALENT_A_MANIAC时10
        "talent_req": [TALENT_LOVE, TALENT_LEWD, TALENT_SERVE_MIND, TALENT_ACCEPT_PLEASURE, TALENT_SEX_MANIAC, TALENT_A_MANIAC],
        "talent_block": [],
        "levels": [
            # Option0: 欲情+屈服+性交经验, Option1: 3xJUEL+半EXP
            {"juel": {JUEL_DESIRE: 3000, JUEL_HUMILIATE: 10000}, "exp": {EXP_SEX: 10}},  # 0→1
            {"juel": {JUEL_DESIRE: 8000, JUEL_HUMILIATE: 25000}, "exp": {EXP_SEX: 25}},  # 1→2
            {"juel": {JUEL_DESIRE: 15000, JUEL_HUMILIATE: 50000}, "exp": {EXP_SEX: 40}},  # 2→3
            {"juel": {JUEL_DESIRE: 30000, JUEL_HUMILIATE: 100000}, "exp": {EXP_SEX: 80}},  # 3→4
            {"juel": {JUEL_DESIRE: 55000, JUEL_HUMILIATE: 200000}, "exp": {EXP_SEX: 200}},  # 4→5
            {"juel": {JUEL_DESIRE: 70000, JUEL_HUMILIATE: 300000}, "exp": {EXP_SEX: 400}},  # 5→6
            {"juel": {JUEL_DESIRE: 90000, JUEL_HUMILIATE: 400000}, "exp": {EXP_SEX: 800}},  # 6→7
            {"juel": {JUEL_DESIRE: 120000, JUEL_HUMILIATE: 550000}, "exp": {EXP_SEX: 1200}},  # 7→8
            {"juel": {JUEL_DESIRE: 150000, JUEL_HUMILIATE: 700000}, "exp": {EXP_SEX: 1500}},  # 8→9
            {"juel": {JUEL_DESIRE: 200000, JUEL_HUMILIATE: 900000}, "exp": {EXP_SEX: 2000}},  # 9→10
        ],
        "note": "ABL:30+ABL:31合计上限20; 需ABL:16>=Lv+1; Option1: 3xJUEL+EXP//2; Lv>=2需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:31 - 自慰中毒
    # ERB: ABLUP31.ERB
    # 复杂度: 高 (两种支付选项, 合计上限)
    # ------------------------------------------------------------------
    ABL_SELF_MAST: {
        "name": "自慰中毒",
        "max_level": 5,  # TALENT_LOVE/TALENT_LEWD/TALENT_EASY_MAST/TALENT_ACCEPT_PLEASURE/TALENT_MAST_MANIAC/TALENT_B_MANIAC时10
        "talent_req": [TALENT_LOVE, TALENT_LEWD, TALENT_EASY_MAST, TALENT_ACCEPT_PLEASURE, TALENT_MAST_MANIAC, TALENT_B_MANIAC],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 3000, JUEL_C_PLEASURE: 10000, JUEL_PAIN: 1000}, "exp": {EXP_MAST: 100}},  # 0→1
            {"juel": {JUEL_DESIRE: 6000, JUEL_C_PLEASURE: 25000, JUEL_PAIN: 3000}, "exp": {EXP_MAST: 250}},  # 1→2
            {"juel": {JUEL_DESIRE: 12000, JUEL_C_PLEASURE: 50000, JUEL_PAIN: 6000}, "exp": {EXP_MAST: 500}},  # 2→3
            {"juel": {JUEL_DESIRE: 20000, JUEL_C_PLEASURE: 100000, JUEL_PAIN: 15000}, "exp": {EXP_MAST: 1000}},  # 3→4
            {"juel": {JUEL_DESIRE: 32000, JUEL_C_PLEASURE: 200000, JUEL_PAIN: 30000}, "exp": {EXP_MAST: 1500}},  # 4→5
            {"juel": {JUEL_DESIRE: 50000, JUEL_C_PLEASURE: 250000, JUEL_PAIN: 40000}, "exp": {EXP_MAST: 2000}},  # 5→6
            {"juel": {JUEL_DESIRE: 70000, JUEL_C_PLEASURE: 320000, JUEL_PAIN: 50000}, "exp": {EXP_MAST: 3000}},  # 6→7
            {"juel": {JUEL_DESIRE: 100000, JUEL_C_PLEASURE: 500000, JUEL_PAIN: 70000}, "exp": {EXP_MAST: 4000}},  # 7→8
            {"juel": {JUEL_DESIRE: 150000, JUEL_C_PLEASURE: 800000, JUEL_PAIN: 100000}, "exp": {EXP_MAST: 6000}},  # 8→9
            {"juel": {JUEL_DESIRE: 200000, JUEL_C_PLEASURE: 1000000, JUEL_PAIN: 150000}, "exp": {EXP_MAST: 8000}},  # 9→10
        ],
        "note": "ABL:30+ABL:31合计上限20; 需ABL:17和ABL:0>=Lv+1; Option0用自慰经验,Option1用调教自慰经验; Lv2需异常经验; 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:32 - 精液中毒
    # ERB: ABLUP32.ERB
    # 复杂度: 极高 (双支付路径, 三中毒合计上限, 大量素质修正)
    # ------------------------------------------------------------------
    ABL_SEMEN_ADDICT: {
        "name": "精液中毒",
        "max_level": 5,  # TALENT_LEWD/TALENT_LOVE_SEMEN/TALENT_NO_SMELL/TALENT_EASY_MAST时10
        "talent_req": [TALENT_LEWD, TALENT_LOVE_SEMEN, TALENT_NO_SMELL, TALENT_EASY_MAST],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 3000, JUEL_HUMILIATE: 10000}, "exp": {EXP_SEMEN: 10}},  # 0→1
            {"juel": {JUEL_DESIRE: 8000, JUEL_HUMILIATE: 20000}, "exp": {EXP_SEMEN: 25}},  # 1→2
            {"juel": {JUEL_DESIRE: 15000, JUEL_HUMILIATE: 35000}, "exp": {EXP_SEMEN: 40}},  # 2→3
            {"juel": {JUEL_DESIRE: 30000, JUEL_HUMILIATE: 60000}, "exp": {EXP_SEMEN: 80}},  # 3→4
            {"juel": {JUEL_DESIRE: 50000, JUEL_HUMILIATE: 130000}, "exp": {EXP_SEMEN: 200}},  # 4→5
            {"juel": {JUEL_DESIRE: 65000, JUEL_HUMILIATE: 190000}, "exp": {EXP_SEMEN: 500}},  # 5→6
            {"juel": {JUEL_DESIRE: 90000, JUEL_HUMILIATE: 300000}, "exp": {EXP_SEMEN: 800}},  # 6→7
            {"juel": {JUEL_DESIRE: 120000, JUEL_HUMILIATE: 500000}, "exp": {EXP_SEMEN: 1200}},  # 7→8
            {"juel": {JUEL_DESIRE: 200000, JUEL_HUMILIATE: 800000}, "exp": {EXP_SEMEN: 1500}},  # 8→9
            {"juel": {JUEL_DESIRE: 500000, JUEL_HUMILIATE: 1500000}, "exp": {EXP_SEMEN: 2000}},  # 9→10
        ],
        "note": "极复杂: 双支付路径(正常/3xJUEL+半EXP); ABL:32+33+39合计上限10; 需ABL:16或ABL:11>=Lv+1; Lv>=2需异常经验; 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:33 - 百合中毒
    # ERB: ABLUP33.ERB
    # 复杂度: 极高 (男人不可, 三中毒合计上限, 大量素质修正)
    # ------------------------------------------------------------------
    ABL_LES_ADDICT: {
        "name": "百合中毒",
        "max_level": 5,  # TALENT_LEWD/TALENT_PERVERT/TALENT_BI/TALENT_HATE_MALE时10
        "talent_req": [TALENT_LEWD, TALENT_PERVERT, TALENT_BI, TALENT_HATE_MALE],
        "talent_block": [TALENT_MALE],  # 男人不可
        "levels": [
            {"juel": {JUEL_C_PLEASURE: 1200, JUEL_DESIRE: 5000}, "exp": {EXP_LES: 300}},  # 0→1
            {"juel": {JUEL_C_PLEASURE: 3900, JUEL_DESIRE: 15000}, "exp": {EXP_LES: 600}},  # 1→2
            {"juel": {JUEL_C_PLEASURE: 6000, JUEL_DESIRE: 23000}, "exp": {EXP_LES: 1000}},  # 2→3
            {"juel": {JUEL_C_PLEASURE: 18000, JUEL_DESIRE: 50000}, "exp": {EXP_LES: 1400}},  # 3→4
            {"juel": {JUEL_C_PLEASURE: 30000, JUEL_DESIRE: 70000}, "exp": {EXP_LES: 2100}},  # 4→5
            {"juel": {JUEL_C_PLEASURE: 55000, JUEL_DESIRE: 120000}, "exp": {EXP_LES: 3000}},  # 5→6
            {"juel": {JUEL_C_PLEASURE: 70000, JUEL_DESIRE: 200000}, "exp": {EXP_LES: 4000}},  # 6→7
            {"juel": {JUEL_C_PLEASURE: 100000, JUEL_DESIRE: 350000}, "exp": {EXP_LES: 5200}},  # 7→8
            {"juel": {JUEL_C_PLEASURE: 150000, JUEL_DESIRE: 500000}, "exp": {EXP_LES: 6500}},  # 8→9
            {"juel": {JUEL_C_PLEASURE: 300000, JUEL_DESIRE: 800000}, "exp": {EXP_LES: 8000}},  # 9→10
        ],
        "note": "男人不可; ABL:32+33+39合计上限10; 需ABL:22>=Lv+1; Lv>=2需异常经验; 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:37 - 卖淫中毒
    # ERB: ABLUP37.ERB
    # 复杂度: 极高 (大量素质修正, 异常经验复杂计算)
    # ------------------------------------------------------------------
    ABL_PROSTITUTE: {
        "name": "卖淫中毒",
        "max_level": 5,  # TALENT_LEWD/TALENT_UNCHASTE/TALENT_PROSTITUTE时10
        "talent_req": [TALENT_LEWD, TALENT_UNCHASTE, TALENT_PROSTITUTE],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 2000, JUEL_OBEY: 3000, JUEL_HUMILIATE: 1000}, "exp": {EXP_PROSTITUTE: 50}},  # 0→1
            {"juel": {JUEL_DESIRE: 5000, JUEL_OBEY: 8000, JUEL_HUMILIATE: 2500}, "exp": {EXP_PROSTITUTE: 100}},  # 1→2
            {"juel": {JUEL_DESIRE: 8000, JUEL_OBEY: 15000, JUEL_HUMILIATE: 5500}, "exp": {EXP_PROSTITUTE: 150}},  # 2→3
            {"juel": {JUEL_DESIRE: 14000, JUEL_OBEY: 30000, JUEL_HUMILIATE: 10000}, "exp": {EXP_PROSTITUTE: 250}},  # 3→4
            {"juel": {JUEL_DESIRE: 22000, JUEL_OBEY: 50000, JUEL_HUMILIATE: 20000}, "exp": {EXP_PROSTITUTE: 400}},  # 4→5
            {"juel": {JUEL_DESIRE: 34000, JUEL_OBEY: 80000, JUEL_HUMILIATE: 30000}, "exp": {EXP_PROSTITUTE: 500}},  # 5→6
            {"juel": {JUEL_DESIRE: 55000, JUEL_OBEY: 120000, JUEL_HUMILIATE: 50000}, "exp": {EXP_PROSTITUTE: 800}},  # 6→7
            {"juel": {JUEL_DESIRE: 80000, JUEL_OBEY: 180000, JUEL_HUMILIATE: 60000}, "exp": {EXP_PROSTITUTE: 1200}},  # 7→8
            {"juel": {JUEL_DESIRE: 150000, JUEL_OBEY: 300000, JUEL_HUMILIATE: 90000}, "exp": {EXP_PROSTITUTE: 2000}},  # 8→9
            {"juel": {JUEL_DESIRE: 300000, JUEL_OBEY: 600000, JUEL_HUMILIATE: 150000}, "exp": {EXP_PROSTITUTE: 3000}},  # 9→10
        ],
        "note": "需ABL:11>=Lv+1; Lv>=2需异常经验(复杂计算); 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:39 - 兽奸中毒
    # ERB: ABLUP39.ERB
    # 复杂度: 极高 (三中毒合计上限, 大量素质修正)
    # ------------------------------------------------------------------
    ABL_BEAST_ADDICT: {
        "name": "兽奸中毒",
        "max_level": 5,  # TALENT_LEWD/TALENT_ANIMAL_EARS/TALENT_BITCH时10
        "talent_req": [TALENT_LEWD, TALENT_ANIMAL_EARS, TALENT_BITCH],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_DESIRE: 2000, JUEL_HUMILIATE: 2000}, "exp": {EXP_BESTIALITY: 30}},  # 0→1
            {"juel": {JUEL_DESIRE: 5000, JUEL_HUMILIATE: 5000}, "exp": {EXP_BESTIALITY: 100}},  # 1→2
            {"juel": {JUEL_DESIRE: 10000, JUEL_HUMILIATE: 10000}, "exp": {EXP_BESTIALITY: 220}},  # 2→3
            {"juel": {JUEL_DESIRE: 20000, JUEL_HUMILIATE: 20000}, "exp": {EXP_BESTIALITY: 400}},  # 3→4
            {"juel": {JUEL_DESIRE: 30000, JUEL_HUMILIATE: 30000}, "exp": {EXP_BESTIALITY: 800}},  # 4→5
            {"juel": {JUEL_DESIRE: 45000, JUEL_HUMILIATE: 45000}, "exp": {EXP_BESTIALITY: 1600}},  # 5→6
            {"juel": {JUEL_DESIRE: 75000, JUEL_HUMILIATE: 75000}, "exp": {EXP_BESTIALITY: 2000}},  # 6→7
            {"juel": {JUEL_DESIRE: 100000, JUEL_HUMILIATE: 100000}, "exp": {EXP_BESTIALITY: 2800}},  # 7→8
            {"juel": {JUEL_DESIRE: 200000, JUEL_HUMILIATE: 200000}, "exp": {EXP_BESTIALITY: 4000}},  # 8→9
            {"juel": {JUEL_DESIRE: 300000, JUEL_HUMILIATE: 300000}, "exp": {EXP_BESTIALITY: 6000}},  # 9→10
        ],
        "note": "ABL:32+33+39合计上限10; 需ABL:11>=Lv+1; Lv>=2需异常经验; 大量素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:40 - 局部中毒
    # ERB: ABLUP40.ERB
    # 复杂度: 中
    # ------------------------------------------------------------------
    ABL_P_ADDICT: {
        "name": "局部中毒",
        "max_level": 10,
        "talent_req": [],
        "talent_block": [],
        "levels": [
            {"juel": {JUEL_GROW: 2000}, "exp": {}},                # 0→1
            {"juel": {JUEL_GROW: 5000}, "exp": {}},                # 1→2
            {"juel": {JUEL_GROW: 10000}, "exp": {}},               # 2→3
            {"juel": {JUEL_GROW: 20000}, "exp": {}},               # 3→4
            {"juel": {JUEL_GROW: 30000}, "exp": {}},               # 4→5
            {"juel": {JUEL_GROW: 45000}, "exp": {}},               # 5→6
            {"juel": {JUEL_GROW: 75000}, "exp": {}},               # 6→7
            {"juel": {JUEL_GROW: 100000}, "exp": {}},              # 7→8
            {"juel": {JUEL_GROW: 200000}, "exp": {}},              # 8→9
            {"juel": {JUEL_GROW: 300000}, "exp": {}},              # 9→10
        ],
        "note": "需ABL:11>=Lv+1; Lv>=2需异常经验(容易上瘾/淫乱除外); 多素质修正",
    },

    # ------------------------------------------------------------------
    # ABL:99 - 反抗刻印消去 (特殊, 非标准升级)
    # ABL:100 - 异界综合征消去 (特殊, 非标准升级)
    # 这两个不是标准能力升级, 使用专用方法处理, 不放入表格
    # ------------------------------------------------------------------
}


class AblupFullMixin:
    """Mixin providing ABLUP (ability upgrade) full methods"""
    def _ablup99(self, target: Character) -> Dict[str, Any]:
        """反抗刻印消去处理 - ABLUP99.ERB"""
        mark3 = target.get_mark(3)
        if mark3 <= 0:
            return {"can_upgrade": False, "reason": "不存在反抗行为"}
        a = 0
        b = 0
        i = 0
        t = target.talent
        if mark3 == 1:
            a = 5000
        elif mark3 == 2:
            a = 10000
        elif mark3 == 3:
            a = 50000
        if int(t.get(12, 0)):
            a = int(a * 3.00)
        if int(t.get(16, 0)):
            a = int(a * 1.50)
        if int(t.get(13, 0)):
            a = int(a * 0.50)
        if int(t.get(85, 0)):
            a = int(a * 0.50)
        b = mark3 + 2
        mark2 = target.get_mark(2)
        if mark3 > mark2:
            i |= 2
        abl10 = target.get_abl(10)
        if b > abl10:
            i |= 4
        juel6 = target.get_juel(6)
        if juel6 < a:
            i |= 1
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {6: a} if can else {},
            "cost_exp": {},
            "new_mark3": mark3 - 1 if can else mark3,
            "state": i,
        }

    # ------------------------------------------------------------------
    # ABLUP100 - 异界综合征消去
    # ------------------------------------------------------------------


    def _ablup100(self, target: Character) -> Dict[str, Any]:
        """异界综合征消去处理 - ABLUP100.ERB"""
        mark10 = target.get_mark(10)
        if mark10 <= 0:
            return {"can_upgrade": False, "reason": "并没有异界异常反应"}
        a = 0
        b = 0
        c = 0
        i = 0
        t = target.talent
        if mark10 == 1:
            a = 2000
        elif mark10 == 2:
            a = 5000
        elif mark10 == 3:
            a = 15000
        elif mark10 == 4:
            a = 30000
        elif mark10 == 5:
            a = 50000
        if int(t.get(10, 0)):
            a = int(a * 1.20)
        if int(t.get(172, 0)):
            a = int(a * 0.80)
        if int(t.get(12, 0)):
            a = int(a * 1.80)
        if int(t.get(16, 0)):
            a = int(a * 1.20)
        if int(t.get(13, 0)):
            a = int(a * 0.50)
        if int(t.get(85, 0)):
            a = int(a * 0.50)
        if int(t.get(76, 0)):
            a = int(a * 0.70)
        c = (target.get_abl(0) + target.get_abl(1) +
             target.get_abl(2) + target.get_abl(3) +
             target.get_abl(4))
        m = 0
        if mark10 < c - 5:
            m += 1
        b = mark10 * 10
        cflag9 = target.get_cflag(9)
        if b > cflag9:
            m += 1
        if m == 2:
            i |= 4
        exp99 = target.get_exp(99)
        if exp99 < a:
            i |= 2
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {},
            "cost_exp": {99: a} if can else {},
            "new_mark10": mark10 - 1 if can else mark10,
            "state": i,
        }

    # ------------------------------------------------------------------
    # ABLUP37 - 卖淫中毒升级
    # ------------------------------------------------------------------


    def _ablup37(self, target: Character) -> Dict[str, Any]:
        """卖淫中毒升级处理 - ABLUP37.ERB"""
        abl37 = target.get_abl(37)
        t = target.talent
        if abl37 >= 5 and int(t.get(76, 0)) == 0 and int(t.get(31, 0)) == 0 and int(t.get(180, 0)) == 0:
            return {"can_upgrade": False, "reason": "需要特殊素质才能继续提升"}
        if abl37 >= 10:
            return {"can_upgrade": False, "reason": "已达最高级"}
        a = 0; b = 0; c = 0; d = 0; f = 0; i = 0
        if abl37 == 0: a = 2000; b = 3000; c = 1000; d = 50
        elif abl37 == 1: a = 5000; b = 8000; c = 2500; d = 100
        elif abl37 == 2: a = 8000; b = 15000; c = 5500; d = 150
        elif abl37 == 3: a = 14000; b = 30000; c = 10000; d = 250
        elif abl37 == 4: a = 22000; b = 50000; c = 20000; d = 400
        elif abl37 == 5: a = 34000; b = 80000; c = 30000; d = 500
        elif abl37 == 6: a = 55000; b = 120000; c = 50000; d = 800
        elif abl37 == 7: a = 80000; b = 180000; c = 60000; d = 1200
        elif abl37 == 8: a = 150000; b = 300000; c = 90000; d = 2000
        elif abl37 == 9: a = 300000; b = 600000; c = 150000; d = 3000
        # Talent modifiers
        if int(t.get(27, 0)):
            if abl37 == 3: a = int(a*1.50); b = int(b*1.50); c = int(c*1.50); d = int(d*1.50)
            elif abl37 == 4: a = int(a*2.00); b = int(b*2.00); c = int(c*2.00); d = int(d*2.00)
            elif abl37 == 5: a = int(a*2.50); b = int(b*2.50); c = int(c*2.50); d = int(d*2.50)
            elif abl37 >= 6: a = int(a*3.00); b = int(b*3.00); c = int(c*3.00); d = int(d*3.00)
        if int(t.get(11, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50); d = int(d*1.50)
        if int(t.get(12, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20); d = int(d*1.20)
        if int(t.get(20, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50); d = int(d*1.50)
        if int(t.get(24, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50); d = int(d*1.50)
        if int(t.get(26, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(28, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(30, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00); d = int(d*2.00)
        elif int(t.get(31, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(32, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20); d = int(d*1.20)
        elif int(t.get(33, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80); d = int(d*0.80)
        if int(t.get(34, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00); d = int(d*2.00)
        if int(t.get(35, 0)): a = int(a*1.10); b = int(b*1.10); c = int(c*1.10); d = int(d*1.10)
        elif int(t.get(36, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(63, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(72, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50); d = int(d*0.50)
        if int(t.get(76, 0)): a = int(a*0.80); b = int(b*0.50); c = int(c*0.80); d = int(d*0.80)
        if int(t.get(82, 0)): a = int(a*3.00); b = int(b*3.00); c = int(c*3.00); d = int(d*3.00)
        if int(t.get(85, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50); d = int(d*1.50)
        if int(t.get(153, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00); d = int(d*2.00)
        if int(t.get(123, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50); d = int(d*0.50)
        if int(t.get(9, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80); d = int(d*0.80)
        if int(t.get(180, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80); d = int(d*0.80)
        if int(t.get(181, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50); d = int(d*0.50)
        if int(t.get(183, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90); d = int(d*0.90)
        if int(t.get(184, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00); d = int(d*2.00)
        # 异常经验
        if abl37 >= 2 and int(t.get(123, 0)) == 0 and int(t.get(9, 0)) == 0:
            f = abl37 - 1
            if int(t.get(33, 0)): f -= 1
            if int(t.get(70, 0)): f -= 1
            if int(t.get(72, 0)): f -= 2
            if int(t.get(73, 0)): f -= 1
            if int(t.get(76, 0)): f -= 1
            if int(t.get(80, 0)): f -= 1
            if int(t.get(180, 0)): f -= 1
            if int(t.get(181, 0)): f -= 2
            if int(t.get(11, 0)): f += 1
            if int(t.get(20, 0)): f += 1
            if int(t.get(32, 0)): f += 1
            if int(t.get(34, 0)): f += 1
            if int(t.get(71, 0)): f += 1
            if int(t.get(85, 0)): f += 1
            if int(t.get(184, 0)): f += 2
            if f < 0: f = 0
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        if d < 1: d = 1
        abl11 = target.get_abl(11)
        exp50 = target.get_exp(50)
        exp74 = target.get_exp(74)
        juel4 = target.get_juel(4)
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        if f > 0 and exp50 < f:
            i |= 2
        if abl11 < abl37 + 1:
            i |= 4
        if juel4 < a: i |= 1
        if juel5 < b: i |= 1
        if juel6 < c: i |= 1
        if exp74 < d: i |= 2
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {4: a, 5: b, 6: c} if can else {},
            "cost_exp": {74: d, 50: f} if can and f > 0 else ({74: d} if can else {}),
            "state": i,
        }

    # ------------------------------------------------------------------
    # ABLUP39 - 兽奸中毒升级
    # ------------------------------------------------------------------


    def _ablup39(self, target: Character) -> Dict[str, Any]:
        """兽奸中毒升级处理 - ABLUP39.ERB"""
        abl39 = target.get_abl(39)
        t = target.talent
        if abl39 >= 5 and int(t.get(76, 0)) == 0 and int(t.get(124, 0)) == 0 and int(t.get(136, 0)) == 0:
            return {"can_upgrade": False, "reason": "需要特殊素质才能继续提升"}
        if abl39 >= 10:
            return {"can_upgrade": False, "reason": "已达最高级"}
        abl32 = target.get_abl(32)
        abl33 = target.get_abl(33)
        if abl32 + abl33 + abl39 >= 10:
            juel5 = target.get_juel(5)
            juel6 = target.get_juel(6)
            if juel5 < abl39 * abl39 * 4000 and juel6 < abl39 * abl39 * 4000:
                return {"can_upgrade": False, "reason": "精液中毒+百合中毒+兽奸中毒上限为10"}
        a = 0; b = 0; c = 0; f = 0; i = 0
        if abl39 == 0: a = 2000; b = 2000; c = 30
        elif abl39 == 1: a = 5000; b = 5000; c = 100
        elif abl39 == 2: a = 10000; b = 10000; c = 220
        elif abl39 == 3: a = 20000; b = 20000; c = 400
        elif abl39 == 4: a = 30000; b = 30000; c = 800
        elif abl39 == 5: a = 45000; b = 45000; c = 1600
        elif abl39 == 6: a = 75000; b = 75000; c = 2000
        elif abl39 == 7: a = 100000; b = 100000; c = 2800
        elif abl39 == 8: a = 200000; b = 200000; c = 4000
        elif abl39 == 9: a = 300000; b = 300000; c = 6000
        if abl32 + abl33 + abl39 >= 10:
            a = abl39 * abl39 * 4000
            b = abl39 * abl39 * 4000
        if int(t.get(27, 0)):
            if abl39 == 3: a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
            elif abl39 == 4: a = int(a*2.50); b = int(b*2.50); c = int(c*2.50)
            elif abl39 >= 5: a = int(a*3.00); b = int(b*3.00); c = int(c*3.00)
        if abl39 >= 2 and int(t.get(72, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(136, 0)) == 0:
            f = abl39 + 1
        if int(t.get(20, 0)): a = int(a*2.50); b = int(b*2.50); c = int(c*1.50)
        if int(t.get(70, 0)): a = int(a*0.75); b = int(b*0.75)
        elif int(t.get(71, 0)): a = int(a*1.75); b = int(b*1.75)
        if int(t.get(72, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(80, 0)): a = int(a*0.75); b = int(b*0.75); c = int(c*0.75)
        if int(t.get(123, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(124, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80)
        if int(t.get(136, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(85, 0)): a = int(a*1.80); b = int(b*1.80); c = int(c*1.50)
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        abl11 = target.get_abl(11)
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        exp56 = int(target.exp.get(56, 0))
        exp50 = target.get_exp(50)
        if abl11 < abl39 + 1: i |= 4
        if juel5 < a: i |= 1
        if juel6 < b: i |= 1
        if exp56 < c: i |= 2
        if exp50 < f: i |= 2
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {5: a, 6: b} if can else {},
            "cost_exp": {56: c, 50: f} if can and f > 0 else ({56: c} if can else {}),
            "state": i,
        }

    # ------------------------------------------------------------------
    # ABLUP40 - 自由中毒升级
    # ------------------------------------------------------------------


    def _ablup40(self, target: Character) -> Dict[str, Any]:
        """自由中毒升级处理 - ABLUP40.ERB"""
        abl40 = int(target.abl.get(40, 0))
        if abl40 >= 10:
            return {"can_upgrade": False, "reason": "已达到MAX"}
        t = target.talent
        a = 0; f = 0; i = 0
        if abl40 == 0: a = 2000
        elif abl40 == 1: a = 5000
        elif abl40 == 2: a = 10000
        elif abl40 == 3: a = 20000
        elif abl40 == 4: a = 30000
        elif abl40 == 5: a = 45000
        elif abl40 == 6: a = 75000
        elif abl40 == 7: a = 100000
        elif abl40 == 8: a = 200000
        elif abl40 == 9: a = 300000
        if abl40 >= 2 and int(t.get(72, 0)) == 0 and int(t.get(76, 0)) == 0:
            f = abl40 + 1
        if int(t.get(20, 0)): a = int(a * 2.50)
        if int(t.get(70, 0)): a = int(a * 0.75)
        elif int(t.get(71, 0)): a = int(a * 1.75)
        if int(t.get(72, 0)): a = int(a * 0.50)
        if int(t.get(80, 0)): a = int(a * 0.75)
        if int(t.get(123, 0)): a = int(a * 0.50)
        if a < 1: a = 1
        abl11 = target.get_abl(11)
        juel15 = int(target.juel.get(15, 0))
        exp50 = target.get_exp(50)
        if abl11 < abl40 + 1: i |= 4
        if juel15 < a: i |= 1
        if exp50 < f: i |= 2
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {15: a} if can else {},
            "cost_exp": {50: f} if can and f > 0 else {},
            "state": i,
        }

    # ------------------------------------------------------------------
    # ABLUP32 - 精液中毒升级
    # ------------------------------------------------------------------


    def _ablup32(self, target: Character) -> Dict[str, Any]:
        """精液中毒升级处理 - ABLUP32.ERB"""
        abl32 = target.get_abl(32)
        t = target.talent
        if abl32 >= 5 and int(t.get(76, 0)) == 0 and int(t.get(50, 0)) == 0 and int(t.get(61, 0)) == 0 and int(t.get(64, 0)) == 0 and int(t.get(47, 0)) == 0:
            return {"can_upgrade": False, "reason": "需要特殊素质才能继续提升"}
        if abl32 >= 10:
            return {"can_upgrade": False, "reason": "已达最高级"}
        abl33 = target.get_abl(33)
        abl39 = target.get_abl(39)
        if abl32 + abl33 + abl39 >= 10:
            juel5 = target.get_juel(5)
            juel6 = target.get_juel(6)
            if juel5 < abl32 * abl32 * 6500 and juel6 < abl32 * abl32 * 19000:
                return {"can_upgrade": False, "reason": "精液中毒+百合中毒+兽奸中毒上限为10"}
        a = 0; b = 0; c = 0; d = 0; i = 0; j = 0
        if abl32 == 0: a = 3000; b = 10000; c = 10
        elif abl32 == 1: a = 8000; b = 20000; c = 25
        elif abl32 == 2: a = 15000; b = 35000; c = 40
        elif abl32 == 3: a = 30000; b = 60000; c = 80
        elif abl32 == 4: a = 50000; b = 130000; c = 200
        elif abl32 == 5: a = 65000; b = 190000; c = 500
        elif abl32 == 6: a = 90000; b = 300000; c = 800
        elif abl32 == 7: a = 120000; b = 500000; c = 1200
        elif abl32 == 8: a = 200000; b = 800000; c = 1500
        elif abl32 == 9: a = 500000; b = 1500000; c = 2000
        if abl32 + abl33 + abl39 >= 10:
            a = abl32 * abl32 * 4000
            b = abl32 * abl32 * 19000
        if int(t.get(27, 0)):
            if abl32 == 3: a = int(a*1.50); b = int(b*1.50); c = int(c*1.50)
            elif abl32 == 4: a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
            elif abl32 == 5: a = int(a*2.50); b = int(b*2.50); c = int(c*2.50)
            elif abl32 >= 6: a = int(a*3.00); b = int(b*3.00); c = int(c*3.00)
        if abl32 >= 2 and int(t.get(61, 0)) == 0 and int(t.get(72, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(123, 0)) == 0 and int(t.get(47, 0)) == 0:
            d = abl32 - 1
        if int(t.get(11, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50)
        if int(t.get(22, 0)): a = int(a*0.95); b = int(b*0.95); c = int(c*0.95)
        if int(t.get(24, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20)
        if int(t.get(32, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20)
        elif int(t.get(33, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80)
        if int(t.get(34, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
        if int(t.get(47, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(52, 0)): a = int(a*0.95); b = int(b*0.95); c = int(c*0.95)
        if int(t.get(61, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        elif int(t.get(62, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
        if int(t.get(64, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(72, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(73, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(76, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(80, 0)): a = int(a*0.75); b = int(b*0.75); c = int(c*0.75)
        if int(t.get(87, 0)): a = int(a*0.95); b = int(b*0.95); c = int(c*0.95)
        if int(t.get(123, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(9, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        exp50 = target.get_exp(50)
        exp20 = int(target.exp.get(20, 0))
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        abl16 = int(target.abl.get(16, 0))
        abl11 = target.get_abl(11)
        if d > exp50: i |= 2; j |= 2
        if int(t.get(76, 0)) == 0:
            if abl16 < abl32 + 1: i |= 4; j |= 4
        else:
            if abl11 < abl32 + 1: i |= 4; j |= 4
        if juel5 < a: i |= 1
        if juel6 < b: i |= 1
        if exp20 < c: i |= 2
        if juel5 < a*3: j |= 1
        if juel6 < b*3: j |= 1
        if exp20 < c//2: j |= 2
        can = (i == 0 or j == 0)
        cost_juel = {}
        cost_exp = {}
        if can:
            if i == 0:
                cost_juel = {5: a, 6: b}
                cost_exp = {20: c}
            elif j == 0:
                cost_juel = {5: a*3, 6: b*3}
                cost_exp = {20: c//2}
            if d > 0 and 50 not in cost_exp:
                cost_exp[50] = d
        return {
            "can_upgrade": can,
            "cost_juel": cost_juel,
            "cost_exp": cost_exp,
            "state_i": i,
            "state_j": j,
        }

    # ------------------------------------------------------------------
    # ABLUP33 - 百合中毒升级
    # ------------------------------------------------------------------


    def _ablup33(self, target: Character) -> Dict[str, Any]:
        """百合中毒升级处理 - ABLUP33.ERB"""
        t = target.talent
        if int(t.get(122, 0)):
            return {"can_upgrade": False, "reason": "男人无法提升百合中毒"}
        abl33 = target.get_abl(33)
        if abl33 >= 5 and int(t.get(76, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(82, 0)) == 0:
            return {"can_upgrade": False, "reason": "需要特殊素质才能继续提升"}
        if abl33 >= 10:
            return {"can_upgrade": False, "reason": "已达最高级"}
        abl32 = target.get_abl(32)
        abl39 = target.get_abl(39)
        if abl32 + abl33 + abl39 >= 10:
            juel5 = target.get_juel(5)
            juel6 = target.get_juel(6)
            juel0 = int(target.juel.get(0, 0))
            if juel5 < abl33*abl33*4000 and juel6 < abl33*abl33*4000 and juel0 < abl33*abl33*10000:
                return {"can_upgrade": False, "reason": "精液中毒+百合中毒+兽奸中毒上限为10"}
        a = 0; b = 0; c = 0; d = 0; i = 0
        if abl33 == 0: a = 1200; b = 5000; c = 300
        elif abl33 == 1: a = 3900; b = 15000; c = 600
        elif abl33 == 2: a = 6000; b = 23000; c = 1000
        elif abl33 == 3: a = 18000; b = 50000; c = 1400
        elif abl33 == 4: a = 30000; b = 70000; c = 2100
        elif abl33 == 5: a = 55000; b = 120000; c = 3000
        elif abl33 == 6: a = 70000; b = 200000; c = 4000
        elif abl33 == 7: a = 100000; b = 350000; c = 5200
        elif abl33 == 8: a = 150000; b = 500000; c = 6500
        elif abl33 == 9: a = 300000; b = 800000; c = 8000
        if abl32 + abl33 + abl39 >= 10:
            a = abl33 * abl33 * 4000
            b = abl33 * abl33 * 10000
        if int(t.get(27, 0)):
            if abl33 == 3: a = int(a*1.50); b = int(b*1.50); c = int(c*1.50)
            elif abl33 == 4: a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
            elif abl33 == 5: a = int(a*2.50); b = int(b*2.50); c = int(c*2.50)
            elif abl33 >= 6: a = int(a*3.00); b = int(b*3.00); c = int(c*3.00)
        if abl33 >= 2 and int(t.get(72, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(82, 0)) == 0 and int(t.get(123, 0)) == 0:
            d = abl33 - 1
        if int(t.get(11, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50)
        if int(t.get(20, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20)
        if int(t.get(21, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20)
        if int(t.get(24, 0)): a = int(a*1.50); b = int(b*1.50); c = int(c*1.50)
        if int(t.get(32, 0)): a = int(a*1.20); b = int(b*1.20); c = int(c*1.20)
        elif int(t.get(33, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80)
        if int(t.get(34, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
        if int(t.get(52, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(61, 0)): a = int(a*0.95); b = int(b*0.95); c = int(c*0.95)
        if int(t.get(63, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(64, 0)): a = int(a*0.95); b = int(b*0.95); c = int(c*0.95)
        if int(t.get(70, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        elif int(t.get(71, 0)): a = int(a*1.10); b = int(b*1.10); c = int(c*1.10)
        if int(t.get(72, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(73, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(76, 0)): a = int(a*0.75); b = int(b*0.75); c = int(c*0.75)
        if int(t.get(79, 0)): a = int(a*2.00); b = int(b*2.00); c = int(c*2.00)
        if int(t.get(80, 0)): a = int(a*0.75); b = int(b*0.75); c = int(c*0.75)
        if int(t.get(81, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(82, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(87, 0)): a = int(a*0.90); b = int(b*0.90); c = int(c*0.90)
        if int(t.get(123, 0)): a = int(a*0.50); b = int(b*0.50); c = int(c*0.50)
        if int(t.get(9, 0)): a = int(a*0.80); b = int(b*0.80); c = int(c*0.80)
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        abl22 = int(target.abl.get(22, 0))
        exp50 = target.get_exp(50)
        exp40 = int(target.exp.get(40, 0))
        juel0 = int(target.juel.get(0, 0))
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        if d > exp50: i |= 2
        if abl22 < abl33 + 1: i |= 4
        if juel0 < b: i |= 1
        if juel5 < a: i |= 1
        if juel6 < a: i |= 1
        if exp40 < c: i |= 2
        can = (i == 0)
        return {
            "can_upgrade": can,
            "cost_juel": {0: b, 5: a, 6: a} if can else {},
            "cost_exp": {40: c, 50: d} if can and d > 0 else ({40: c} if can else {}),
            "state": i,
        }

    # ------------------------------------------------------------------
    # IKAI_BONUS - 异界奖励
    # ------------------------------------------------------------------


    def _ablup0(self, target: Character) -> Dict[str, int]:
        """C感觉升级判定 - 基于ERB DECIDE_ABLUP0"""
        abl = target.get_abl(0)
        juel0 = target.get_juel(0)
        t = target.talent
        # 各部位感觉封锁计数
        calc = 0
        if int(t.get(103, 0)) & 2: calc += 1  # V感觉封锁
        if int(t.get(105, 0)) & 2: calc += 1  # A感觉封锁
        if int(t.get(107, 0)) & 2: calc += 1  # B感觉封锁
        # 上限检查: Lv5以上需要自慰狂(TALENT:74)
        if abl >= 5 and int(t.get(74, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 动态上限: calc*5+10
        if abl >= calc * 5 + 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # C感觉封锁(TALENT:101 bit1)不可升级
        if int(t.get(101, 0)) & 2:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 基础JUEL成本
        a = 0
        if abl == 0: a = 1
        elif abl == 1: a = 20
        elif abl == 2: a = 400
        elif abl == 3: a = 8000
        elif abl == 4: a = 20000
        elif abl == 5: a = 40000
        elif abl == 6: a = 60000
        elif abl == 7: a = 90000
        elif abl == 8: a = 120000
        elif abl == 9: a = 180000
        elif abl < 15:
            a = 180000
            for _ in range(abl - 9):
                a = a * 125 // 100
        elif abl < 20:
            a = 362000
            for _ in range(abl - 14):
                a = a * 120 // 100
        elif abl < 25:
            a = 583000
            for _ in range(abl - 19):
                a = a * 115 // 100
        # 素质修正: 戒备森严(TALENT:27)
        if int(t.get(27, 0)):
            if abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        # 阴蒂钝感 TALENT:101 bit0
        if int(t.get(101, 0)) & 1:
            a = int(a * 1.20)
        # 阴蒂敏感 TALENT:102
        if int(t.get(102, 0)):
            a = int(a * 0.80)
        # 封锁数对成本的影响
        if abl > 5 and abl <= 10 and calc > 0:
            a = a * (15 - calc) // 15
        elif abl <= 15 and calc > 1:
            a = a * (16 - calc) // 15
        elif abl <= 20 and calc > 2:
            a = a * (17 - calc) // 15
        # 淫乱 TALENT:76
        if int(t.get(76, 0)):
            a = int(a * 0.80)
        # 自慰狂 TALENT:74
        if int(t.get(74, 0)):
            a = int(a * 0.80)
        # 最低1
        if a < 1: a = 1
        can = juel0 >= a
        return {"can_upgrade": can, "cost_juel": {0: a}, "cost_exp": {}}


    def _ablup1(self, target: Character) -> Dict[str, int]:
        """B感觉升级判定 - 基于ERB DECIDE_ABLUP1"""
        abl = target.get_abl(1)
        juel14 = target.get_juel(14)
        t = target.talent
        # 各部位感觉封锁计数
        calc = 0
        if int(t.get(101, 0)) & 2: calc += 1  # C感觉封锁
        if int(t.get(103, 0)) & 2: calc += 1  # V感觉封锁
        if int(t.get(105, 0)) & 2: calc += 1  # A感觉封锁
        # 上限检查: Lv5以上需要淫乳(TALENT:78)
        if abl >= 5 and int(t.get(78, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 动态上限: calc*5+10
        if abl >= calc * 5 + 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # B感觉封锁(TALENT:107 bit1)不可升级
        if int(t.get(107, 0)) & 2:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 基础JUEL成本 (B感觉只需JUEL:14情爱, 无EXP需求)
        a = 0
        if abl == 0: a = 1
        elif abl == 1: a = 20
        elif abl == 2: a = 400
        elif abl == 3: a = 8000
        elif abl == 4: a = 20000
        elif abl == 5: a = 40000
        elif abl == 6: a = 60000
        elif abl == 7: a = 90000
        elif abl == 8: a = 120000
        elif abl == 9: a = 180000
        elif abl < 15:
            a = 180000
            for _ in range(abl - 9):
                a = a * 125 // 100
        elif abl < 20:
            a = 362000
            for _ in range(abl - 14):
                a = a * 120 // 100
        elif abl < 25:
            a = 583000
            for _ in range(abl - 19):
                a = a * 115 // 100
        # 素质修正: 戒备森严(TALENT:27)
        if int(t.get(27, 0)):
            if abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        # B钝感 TALENT:107 bit0
        if int(t.get(107, 0)) & 1:
            a = int(a * 1.20)
        # 巨乳 TALENT:110
        if int(t.get(110, 0)):
            a = int(a * 1.10)
        # 爆乳 TALENT:114
        if int(t.get(114, 0)):
            a = int(a * 1.20)
        # 超乳 TALENT:119
        if int(t.get(119, 0)):
            a = int(a * 1.30)
        # B敏感 TALENT:108
        if int(t.get(108, 0)):
            a = int(a * 0.80)
        # 封锁数对成本的影响
        if abl > 5 and abl <= 10 and calc > 0:
            a = a * (15 - calc) // 15
        elif abl <= 15 and calc > 1:
            a = a * (16 - calc) // 15
        elif abl <= 20 and calc > 2:
            a = a * (17 - calc) // 15
        # 淫乱 TALENT:76
        if int(t.get(76, 0)):
            a = int(a * 0.80)
        # 淫乳 TALENT:78
        if int(t.get(78, 0)):
            a = int(a * 0.80)
        # 贫乳 TALENT:109
        if int(t.get(109, 0)):
            a = int(a * 0.80)
        # 绝壁 TALENT:116
        if int(t.get(116, 0)):
            a = int(a * 0.65)
        # 最低1
        if a < 1: a = 1
        can = juel14 >= a
        return {"can_upgrade": can, "cost_juel": {14: a}, "cost_exp": {}}


    def _ablup2(self, target: Character) -> Dict[str, int]:
        """V感觉升级判定 - 基于ERB DECIDE_ABLUP2"""
        abl = target.get_abl(2)
        juel1 = target.get_juel(1)
        exp0 = target.get_exp(0)
        t = target.talent
        # 各部位感觉封锁计数
        calc = 0
        if int(t.get(101, 0)) & 2: calc += 1  # C感觉封锁
        if int(t.get(105, 0)) & 2: calc += 1  # A感觉封锁
        if int(t.get(107, 0)) & 2: calc += 1  # B感觉封锁
        # 男人不可
        if int(t.get(122, 0)):
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 上限检查: Lv5以上需要性爱狂(TALENT:75)
        if abl >= 5 and int(t.get(75, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 动态上限: calc*5+10
        if abl >= calc * 5 + 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # V感觉封锁(TALENT:103 bit1)不可升级
        if int(t.get(103, 0)) & 2:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 基础JUEL成本(JUEL:1快V)和EXP成本(EXP:0性交经验)
        a = 0; b = 0
        if abl == 0: a = 1; b = 2
        elif abl == 1: a = 20; b = 10
        elif abl == 2: a = 400; b = 30
        elif abl == 3: a = 8000; b = 75
        elif abl == 4: a = 20000; b = 150
        elif abl == 5: a = 40000; b = 180
        elif abl == 6: a = 60000; b = 250
        elif abl == 7: a = 90000; b = 350
        elif abl == 8: a = 120000; b = 500
        elif abl == 9: a = 180000; b = 600
        elif abl < 15:
            a = 180000; b = 600
            for _ in range(abl - 9):
                a = a * 125 // 100; b = b * 115 // 100
        elif abl < 20:
            a = 362000; b = 966
            for _ in range(abl - 14):
                a = a * 120 // 100; b = b * 120 // 100
        elif abl < 25:
            a = 583000; b = 1942
            for _ in range(abl - 19):
                a = a * 115 // 100; b = b * 125 // 100
        # 素质修正: 戒备森严(TALENT:27)
        if int(t.get(27, 0)):
            if abl == 4: a = int(a * 2.00); b = int(b * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00)
        # V钝感 TALENT:103 bit0
        if int(t.get(103, 0)) & 1:
            a = int(a * 1.20); b = int(b * 1.10)
        # 封锁数对成本的影响
        if abl > 5 and abl <= 10 and calc > 0:
            a = a * (15 - calc) // 15; b = b * (20 - calc) // 20
        elif abl <= 15 and calc > 1:
            a = a * (16 - calc) // 15; b = b * (21 - calc) // 20
        elif abl <= 20 and calc > 2:
            a = a * (17 - calc) // 15; b = b * (22 - calc) // 20
        # 淫乱 TALENT:76
        if int(t.get(76, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # 性爱狂 TALENT:75
        if int(t.get(75, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # V敏感 TALENT:104
        if int(t.get(104, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # 最低1
        if a < 1: a = 1
        if b < 1: b = 1
        can = juel1 >= a and exp0 >= b
        return {"can_upgrade": can, "cost_juel": {1: a}, "cost_exp": {0: b}}


    def _ablup3(self, target: Character) -> Dict[str, int]:
        """A感觉升级判定 - 基于ERB DECIDE_ABLUP3"""
        abl = target.get_abl(3)
        juel2 = target.get_juel(2)
        exp1 = target.get_exp(1)
        t = target.talent
        # 各部位感觉封锁计数
        calc = 0
        if int(t.get(101, 0)) & 2: calc += 1  # C感觉封锁
        if int(t.get(103, 0)) & 2: calc += 1  # V感觉封锁
        if int(t.get(107, 0)) & 2: calc += 1  # B感觉封锁
        # 上限检查: Lv5以上需要尻穴狂(TALENT:77)
        if abl >= 5 and int(t.get(77, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 动态上限: calc*5+10
        if abl >= calc * 5 + 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # A感觉封锁(TALENT:105 bit1)不可升级
        if int(t.get(105, 0)) & 2:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        # 基础JUEL成本(JUEL:2快A)和EXP成本(EXP:1肛门经验)
        a = 0; b = 0
        if abl == 0: a = 1; b = 2
        elif abl == 1: a = 20; b = 10
        elif abl == 2: a = 400; b = 30
        elif abl == 3: a = 8000; b = 75
        elif abl == 4: a = 20000; b = 150
        elif abl == 5: a = 40000; b = 180
        elif abl == 6: a = 60000; b = 250
        elif abl == 7: a = 90000; b = 350
        elif abl == 8: a = 120000; b = 500
        elif abl == 9: a = 180000; b = 600
        elif abl < 15:
            a = 180000; b = 600
            for _ in range(abl - 9):
                a = a * 125 // 100; b = b * 115 // 100
        elif abl < 20:
            a = 362000; b = 966
            for _ in range(abl - 14):
                a = a * 120 // 100; b = b * 120 // 100
        elif abl < 25:
            a = 583000; b = 1942
            for _ in range(abl - 19):
                a = a * 115 // 100; b = b * 125 // 100
        # 素质修正: 戒备森严(TALENT:27)
        if int(t.get(27, 0)):
            if abl == 4: a = int(a * 2.00); b = int(b * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00)
        # A钝感 TALENT:105 bit0
        if int(t.get(105, 0)) & 1:
            a = int(a * 1.20); b = int(b * 1.10)
        # 封锁数对成本的影响
        if abl > 5 and abl <= 10 and calc > 0:
            a = a * (15 - calc) // 15; b = b * (20 - calc) // 20
        elif abl <= 15 and calc > 1:
            a = a * (16 - calc) // 15; b = b * (21 - calc) // 20
        elif abl <= 20 and calc > 2:
            a = a * (17 - calc) // 15; b = b * (22 - calc) // 20
        # 淫乱 TALENT:76
        if int(t.get(76, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # 尻穴狂 TALENT:77
        if int(t.get(77, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # A敏感 TALENT:106
        if int(t.get(106, 0)):
            a = int(a * 0.80); b = int(b * 0.80)
        # 最低1
        if a < 1: a = 1
        if b < 1: b = 1
        can = juel2 >= a and exp1 >= b
        return {"can_upgrade": can, "cost_juel": {2: a}, "cost_exp": {1: b}}


    def _ablup4(self, target: Character) -> Dict[str, int]:
        """技巧 upgrade cost"""
        abl = target.get_abl(4)
        juel15 = target.get_juel(15)
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0
        if abl == 0: a = 1
        elif abl == 1: a = 50
        elif abl == 2: a = 600
        elif abl == 3:
            a = 7000
            if int(t.get(27, 0)): a = int(a * 2.00)
        elif abl == 4:
            a = 45000
            if int(t.get(27, 0)): a = int(a * 3.00)
        can = juel15 >= a
        return {"can_upgrade": can, "cost_juel": {15: a}, "cost_exp": {}}


    def _ablup5(self, target: Character) -> Dict[str, int]:
        """话术 upgrade cost"""
        abl = target.get_abl(5)
        juel2 = target.get_juel(2)
        exp1 = target.get_exp(1)
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0
        if abl == 0: a = 1; b = 2
        elif abl == 1:
            a = 50; b = 10
            if exp1 >= 30: a = 20
        elif abl == 2:
            a = 600; b = 30
            if exp1 >= 60: a = 100
        elif abl == 3:
            a = 7000; b = 150
            if exp1 >= 120: a = 500
            if int(t.get(27, 0)): a = int(a * 2.00); b = int(b * 2.00)
        elif abl == 4:
            a = 45000; b = 300
            if exp1 >= 120: a = 8000
            if int(t.get(27, 0)): a = int(a * 3.00); b = int(b * 3.00)
        can = juel2 >= a and exp1 >= b
        return {"can_upgrade": can, "cost_juel": {2: a}, "cost_exp": {1: b}}


    def _ablup6(self, target: Character) -> Dict[str, int]:
        """性技 upgrade cost"""
        abl = target.get_abl(6)
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0
        if abl == 0: a = 100; b = 20; c = 100; d = 1; e = 1
        elif abl == 1: a = 1200; b = 100; c = 0; d = 1; e = 3
        elif abl == 2: a = 5000; b = 600; c = 0; d = 20; e = 6
        elif abl == 3:
            a = 10000; b = 2000; c = 0; d = 20; e = 10
            if int(t.get(27, 0)):
                a = int(a * 2.00); b = int(b * 2.00); d = int(d * 2.00)
        elif abl == 4:
            a = 30000; b = 8000; c = 0; d = 100; e = 20
            if int(t.get(27, 0)):
                a = int(a * 3.00); b = int(b * 3.00); d = int(d * 3.00)
        if int(t.get(80, 0)):
            a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75)
        abl0 = int(target.abl.get(0, 0))
        cost_juel = {}
        cost_exp = {}
        can = False
        juel6 = target.get_juel(6)
        juel4 = target.get_juel(4)
        juel7 = int(target.juel.get(7, 0))
        exp2 = int(target.exp.get(2, 0))
        exp20 = int(target.exp.get(20, 0))
        exp21 = int(target.exp.get(21, 0))
        exp50 = target.get_exp(50)
        # Option 0: 屈辱点数
        i0 = 0
        if abl0 < abl + 1: i0 |= 4
        if abl == 3 and int(t.get(86, 0)) == 0 and exp50 == 0: i0 |= 2
        if abl == 4 and int(t.get(86, 0)) == 0 and exp50 < 2: i0 |= 2
        if juel6 < a: i0 |= 1
        if exp2 < e: i0 |= 2
        if exp20 < e: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel[6] = a
            cost_exp[2] = e; cost_exp[20] = e
        # Option 1: 欲情点数
        if not can and b > 0:
            j1 = 0
            if abl0 < abl + 1: j1 |= 4
            if abl == 3 and int(t.get(86, 0)) == 0 and exp50 == 0: j1 |= 2
            if abl == 4 and int(t.get(86, 0)) == 0 and exp50 < 2: j1 |= 2
            if juel4 < b: j1 |= 1
            if exp21 < d: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {4: b}
                cost_exp = {21: d}
        # Option 2: 习得点数
        if not can and c > 0:
            k1 = 0
            if abl0 < abl + 1: k1 |= 4
            if abl == 3 and int(t.get(86, 0)) == 0 and exp50 == 0: k1 |= 2
            if abl == 4 and int(t.get(86, 0)) == 0 and exp50 < 2: k1 |= 2
            if juel7 < c: k1 |= 1
            if exp2 < 1: k1 |= 2
            if k1 == 0:
                can = True
                cost_juel = {7: c}
                cost_exp = {2: 1}
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup7(self, target: Character) -> Dict[str, int]:
        """性交 upgrade cost"""
        abl = int(target.abl.get(7, 0))
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0
        if abl == 0: a = 100
        elif abl == 1: a = 1000
        elif abl == 2: a = 5000
        elif abl == 3:
            a = 15000
            if int(t.get(27, 0)): a = int(a * 2.00)
        elif abl == 4:
            a = 35000
            if int(t.get(27, 0)): a = int(a * 3.00)
        if int(t.get(80, 0)): a = int(a * 0.75)
        if int(t.get(80, 0)): a = int(a * 0.50)
        abl1 = int(target.abl.get(1, 0))
        exp50 = target.get_exp(50)
        exp2 = int(target.exp.get(2, 0))
        exp11 = int(target.exp.get(11, 0))
        juel8 = int(target.juel.get(8, 0))
        i0 = 0
        if abl1 < abl + 1: i0 |= 4
        if abl == 3 and int(t.get(28, 0)) == 0 and exp50 == 0: i0 |= 2
        if abl == 4 and int(t.get(28, 0)) == 0 and exp50 < 2: i0 |= 2
        if juel8 < a: i0 |= 1
        if abl < 2:
            if exp2 == 0: i0 |= 2
        else:
            if exp11 == 0: i0 |= 2
        can = i0 == 0
        cost_exp = {}
        if abl < 2:
            cost_exp[2] = 1
        else:
            cost_exp[11] = 1
        return {"can_upgrade": can, "cost_juel": {8: a}, "cost_exp": cost_exp}


    def _ablup8(self, target: Character) -> Dict[str, int]:
        """奉仕 upgrade cost"""
        abl = int(target.abl.get(8, 0))
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0
        if abl == 0: a = 100; b = 100; c = 0; d = 100; e = 100
        elif abl == 1: a = 500; b = 500; c = 0; d = 500; e = 300
        elif abl == 2: a = 1200; b = 1000; c = 0; d = 1500; e = 1000
        elif abl == 3:
            a = 0; b = 0; c = 10; d = 3000; e = 6000
            if int(t.get(27, 0)):
                c = int(c * 2.00); d = int(d * 2.00); e = int(e * 2.00)
        elif abl == 4:
            a = 0; b = 0; c = 50; d = 5000; e = 12000
            if int(t.get(27, 0)):
                c = int(c * 3.00); d = int(d * 3.00); e = int(e * 3.00)
        if int(t.get(33, 0)):
            a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50)
            d = int(d * 0.50); e = int(e * 0.50)
        if int(t.get(80, 0)):
            a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75)
            d = int(d * 0.75); e = int(e * 0.75)
        abl1 = int(target.abl.get(1, 0))
        exp50 = target.get_exp(50)
        exp30 = int(target.exp.get(30, 0))
        exp2 = int(target.exp.get(2, 0))
        juel9 = int(target.juel.get(9, 0))
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 苦痛+欲情
        if b > 0:
            i0 = 0
            if abl1 < abl + 1: i0 |= 4
            if abl == 3 and int(t.get(33, 0)) == 0 and exp50 == 0: i0 |= 2
            if abl == 4 and int(t.get(33, 0)) == 0 and exp50 < 2: i0 |= 2
            if juel9 < a: i0 |= 1
            if juel5 < b: i0 |= 1
            if exp30 < c: i0 |= 2
            if i0 == 0:
                can = True
                cost_juel = {9: a, 5: b}
                cost_exp = {}
                if c > 0: cost_exp[30] = c
        # Option 1: 苦痛+屈服
        if not can and d > 0:
            j1 = 0
            if abl1 < abl + 1: j1 |= 4
            if abl == 3 and int(t.get(33, 0)) == 0 and exp50 == 0: j1 |= 2
            if abl == 4 and int(t.get(33, 0)) == 0 and exp50 < 2: j1 |= 2
            if juel9 < d: j1 |= 1
            if juel6 < e: j1 |= 1
            if exp30 < c: j1 |= 2
            if exp2 < 1: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {9: d, 6: e}
                cost_exp = {2: 1}
                if c > 0: cost_exp[30] = c
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup9(self, target: Character) -> Dict[str, int]:
        """露出 upgrade cost"""
        abl = int(target.abl.get(9, 0))
        t = target.talent
        if abl >= 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0
        if abl == 0: a = 200; b = 50; c = 0; d = 1000
        elif abl == 1: a = 1000; b = 200; c = 0; d = 5000
        elif abl == 2: a = 3000; b = 500; c = 1000; d = 0
        elif abl == 3:
            a = 8000; b = 1000; c = 2000; d = 0
            if int(t.get(27, 0)):
                a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00)
        elif abl == 4:
            a = 20000; b = 2000; c = 5000; d = 0
            if int(t.get(27, 0)):
                a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00)
        if int(t.get(81, 0)):
            a = int(a * 0.25); b = int(b * 0.25); c = int(c * 0.25); d = int(d * 0.25)
        if int(t.get(80, 0)):
            a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75)
        exp50 = target.get_exp(50)
        exp40 = int(target.exp.get(40, 0))
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        juel0 = int(target.juel.get(0, 0))
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 欲情+屈服+百合经验
        i0 = 0
        if abl == 3 and int(t.get(81, 0)) == 0 and exp50 == 0: i0 |= 2
        if abl == 4 and int(t.get(81, 0)) == 0 and exp50 < 2: i0 |= 2
        if juel5 < a: i0 |= 1
        if juel6 < c: i0 |= 1
        if exp40 < b: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel = {5: a}
            if c > 0: cost_juel[6] = c
            cost_exp = {40: b}
        # Option 1: 快C+百合经验
        if not can and d > 0:
            j1 = 0
            if abl == 3 and int(t.get(81, 0)) == 0 and exp50 == 0: j1 |= 2
            if abl == 4 and int(t.get(81, 0)) == 0 and exp50 < 2: j1 |= 2
            if juel0 < d: j1 |= 1
            if exp40 < b: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {0: d}
                cost_exp = {40: b}
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup10(self, target: Character) -> Dict[str, int]:
        """顺从 upgrade cost"""
        abl = int(target.abl.get(10, 0))
        t = target.talent
        if abl >= 5 and int(t.get(85, 0)) == 0 and int(t.get(86, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0
        if abl == 0: a = 10; b = 10; c = 300; d = 200
        elif abl == 1: a = 150; b = 100; c = 1000; d = 1200
        elif abl == 2: a = 1000; b = 800; c = 2000; d = 3000
        elif abl == 3: a = 3000; b = 3000; c = 0; d = 12000
        elif abl == 4: a = 8000; b = 5000; c = 0; d = 0
        elif abl == 5: a = 12000; b = 10000; c = 0; d = 0
        elif abl == 6: a = 25000; b = 20000; c = 0; d = 0
        elif abl == 7: a = 0; b = 40000; c = 0; d = 0
        elif abl == 8: a = 0; b = 80000; c = 0; d = 0
        elif abl == 9: a = 0; b = 150000; c = 0; d = 0
        if abl == 4 and int(t.get(10, 0)) == 0 and int(t.get(13, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(73, 0)) == 0 and int(t.get(85, 0)) == 0 and int(t.get(86, 0)) == 0:
            e = 1
        elif abl == 7 and int(t.get(10, 0)) == 0 and int(t.get(13, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(73, 0)) == 0 and int(t.get(85, 0)) == 0 and int(t.get(86, 0)) == 0:
            e = 2
        if int(t.get(10, 0)): a = int(a * 0.50); b = int(b * 0.90); d = int(d * 0.90)
        if int(t.get(11, 0)): a = int(a * 2.00); b = int(b * 1.50); c = int(c * 1.20); d = int(d * 1.50)
        if int(t.get(12, 0)): a = int(a * 3.00); b = int(b * 1.50); c = int(c * 1.20); d = int(d * 1.50)
        if int(t.get(13, 0)): b = int(b * 0.80); d = int(d * 0.90)
        if int(t.get(16, 0)): a = int(a * 1.20); b = int(b * 1.50); d = int(d * 1.20)
        if int(t.get(15, 0)): a = int(a * 1.20); b = int(b * 1.50); d = int(d * 2.00)
        elif int(t.get(17, 0)): b = int(b * 0.80); d = int(d * 0.80)
        if int(t.get(32, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 2.00); d = int(d * 1.20)
        elif int(t.get(33, 0)): c = int(c * 0.50)
        if int(t.get(34, 0)): a = int(a * 1.50); b = int(b * 1.50); c = int(c * 2.00); d = int(d * 2.00)
        if int(t.get(76, 0)): c = int(c * 0.50)
        if int(t.get(85, 0)): b = int(b * 0.75)
        if int(t.get(86, 0)): b = int(b * 0.20)
        if int(t.get(84, 0)): b = int(b * 5.00); c = int(c * 0.80); d = int(d * 2.00)
        if b < 1: b = 1
        juel10 = int(target.juel.get(10, 0))
        juel4 = target.get_juel(4)
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        exp50 = target.get_exp(50)
        cost_juel = {}
        cost_exp = {}
        can = False
        if a > 0:
            i0 = 0
            if juel10 < a: i0 |= 1
            if e > exp50: i0 |= 2
            if i0 == 0:
                can = True
                cost_juel = {10: a}
                if e > 0: cost_exp[50] = e
        if not can:
            j1 = 0
            if juel4 < b: j1 |= 1
            if e > exp50: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {4: b}
                if e > 0: cost_exp[50] = e
        if not can and c > 0:
            k1 = 0
            if juel5 < c: k1 |= 1
            if e > exp50: k1 |= 2
            if k1 == 0:
                can = True
                cost_juel = {5: c}
                if e > 0: cost_exp[50] = e
        if not can and d > 0:
            l1 = 0
            if juel6 < d: l1 |= 1
            if e > exp50: l1 |= 2
            if l1 == 0:
                can = True
                cost_juel = {6: d}
                if e > 0: cost_exp[50] = e
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup11(self, target: Character) -> Dict[str, int]:
        """欲望 upgrade cost"""
        abl = int(target.abl.get(11, 0))
        t = target.talent
        if abl >= 5 and int(t.get(73, 0)) == 0 and int(t.get(76, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; e = 0
        if abl == 0: a = 5
        elif abl == 1: a = 50
        elif abl == 2: a = 1000
        elif abl == 3: a = 5000
        elif abl == 4: a = 12000
        elif abl == 5: a = 20000
        elif abl == 6: a = 30000
        elif abl == 7: a = 50000
        elif abl == 8: a = 80000
        elif abl == 9: a = 150000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50)
            elif abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        if int(t.get(20, 0)): a = int(a * 1.20)
        if int(t.get(24, 0)): a = int(a * 1.10)
        if int(t.get(30, 0)): a = int(a * 1.50)
        elif int(t.get(31, 0)): a = int(a * 0.95)
        if int(t.get(32, 0)): a = int(a * 1.50)
        elif int(t.get(33, 0)): a = int(a * 0.90)
        if int(t.get(34, 0)): a = int(a * 1.50)
        if int(t.get(35, 0)): a = int(a * 1.10)
        elif int(t.get(36, 0)): a = int(a * 0.95)
        if int(t.get(70, 0)): a = int(a * 0.80)
        elif int(t.get(71, 0)): a = int(a * 1.50)
        if int(t.get(72, 0)): a = int(a * 0.95)
        if int(t.get(73, 0)): a = int(a * 0.50)
        if int(t.get(76, 0)): a = int(a * 0.70)
        if int(t.get(180, 0)): a = int(a * 0.90)
        if int(t.get(181, 0)): a = int(a * 0.80)
        if int(t.get(157, 0)): a = int(a * 0.80)
        if abl == 4 and int(t.get(33, 0)) == 0 and int(t.get(70, 0)) == 0 and int(t.get(73, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(123, 0)) == 0:
            e = 1
        elif abl == 7 and int(t.get(33, 0)) == 0 and int(t.get(70, 0)) == 0 and int(t.get(73, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(123, 0)) == 0:
            e = 3
        if a < 1: a = 1
        juel5 = target.get_juel(5)
        exp50 = target.get_exp(50)
        can = juel5 >= a and exp50 >= e
        cost_exp = {}
        if e > 0: cost_exp[50] = e
        return {"can_upgrade": can, "cost_juel": {5: a}, "cost_exp": cost_exp}


    def _ablup12(self, target: Character) -> Dict[str, int]:
        """技巧(12) upgrade cost"""
        abl = int(target.abl.get(12, 0))
        t = target.talent
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        abl15 = int(target.abl.get(15, 0))
        if abl + abl15 >= 15:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0
        if abl == 0: a = 1
        elif abl == 1: a = 25
        elif abl == 2: a = 200
        elif abl == 3: a = 3000
        elif abl == 4: a = 8000
        elif abl == 5: a = 12000
        elif abl == 6: a = 16000
        elif abl == 7: a = 22000
        elif abl == 8: a = 28000
        elif abl == 9: a = 35000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50)
            elif abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        if int(t.get(13, 0)): a = int(a * 0.95)
        if int(t.get(21, 0)): a = int(a * 1.05)
        if int(t.get(23, 0)): a = int(a * 0.95)
        if int(t.get(24, 0)): a = int(a * 1.10)
        if int(t.get(32, 0)): a = int(a * 1.10)
        elif int(t.get(33, 0)): a = int(a * 0.90)
        if int(t.get(34, 0)): a = int(a * 1.20)
        if int(t.get(35, 0)): a = int(a * 1.05)
        elif int(t.get(36, 0)): a = int(a * 0.95)
        if int(t.get(50, 0)): a = int(a * 0.80)
        elif int(t.get(51, 0)): a = int(a * 1.50)
        if int(t.get(52, 0)): a = int(a * 0.95)
        if int(t.get(63, 0)): a = int(a * 0.95)
        if int(t.get(64, 0)): a = int(a * 0.95)
        if a < 1: a = 1
        juel7 = int(target.juel.get(7, 0))
        can = juel7 >= a
        return {"can_upgrade": can, "cost_juel": {7: a}, "cost_exp": {}}


    def _ablup13(self, target: Character) -> Dict[str, int]:
        """自慰 upgrade cost"""
        abl = int(target.abl.get(13, 0))
        t = target.talent
        abl16 = int(target.abl.get(16, 0))
        abl14 = int(target.abl.get(14, 0))
        if abl >= 5 and abl16 < 5:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl14 >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0
        if abl == 0: a = 5
        elif abl == 1: a = 400
        elif abl == 2: a = 1000
        elif abl == 3: a = 3000
        elif abl == 4: a = 6000
        elif abl == 5: a = 9000
        elif abl == 6: a = 12000
        elif abl == 7: a = 16000
        elif abl == 8: a = 20000
        elif abl == 9: a = 25000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50)
            elif abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        if int(t.get(11, 0)): a = int(a * 1.20)
        if int(t.get(13, 0)): a = int(a * 0.95)
        if int(t.get(16, 0)): a = int(a * 1.20)
        if int(t.get(15, 0)): a = int(a * 1.20)
        elif int(t.get(17, 0)): a = int(a * 0.95)
        if int(t.get(21, 0)): a = int(a * 1.05)
        if int(t.get(22, 0)): a = int(a * 1.05)
        if int(t.get(23, 0)): a = int(a * 0.95)
        if int(t.get(24, 0)): a = int(a * 1.10)
        if int(t.get(32, 0)): a = int(a * 1.10)
        elif int(t.get(33, 0)): a = int(a * 0.90)
        if int(t.get(34, 0)): a = int(a * 1.20)
        if int(t.get(35, 0)): a = int(a * 1.05)
        elif int(t.get(36, 0)): a = int(a * 0.95)
        if int(t.get(37, 0)): a = int(a * 0.90)
        if int(t.get(50, 0)): a = int(a * 0.80)
        elif int(t.get(51, 0)): a = int(a * 1.50)
        if int(t.get(52, 0)): a = int(a * 0.90)
        if int(t.get(63, 0)): a = int(a * 0.90)
        if int(t.get(64, 0)): a = int(a * 0.90)
        if int(t.get(73, 0)): a = int(a * 0.90)
        if int(t.get(80, 0)): a = int(a * 0.95)
        if int(t.get(83, 0)): a = int(a * 1.10)
        if abl16 < 3: pass
        elif abl16 < 6: a = int(a * 0.95)
        elif abl16 < 8: a = int(a * 0.90)
        elif abl16 < 10: a = int(a * 0.85)
        else: a = int(a * 0.80)
        if a < 1: a = 1
        juel7 = int(target.juel.get(7, 0))
        abl12 = int(target.abl.get(12, 0))
        i0 = 0
        if juel7 < a: i0 |= 1
        if abl < 5 and abl12 < abl + 1: i0 |= 2
        if abl >= 5 and abl16 < abl + 1: i0 |= 2
        can = i0 == 0
        return {"can_upgrade": can, "cost_juel": {7: a}, "cost_exp": {}}


    def _ablup14(self, target: Character) -> Dict[str, int]:
        """奉仕精神 upgrade cost"""
        abl = int(target.abl.get(14, 0))
        t = target.talent
        abl13 = int(target.abl.get(13, 0))
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl13 >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0
        if abl == 0: a = 1; b = 3
        elif abl == 1: a = 10; b = 10
        elif abl == 2: a = 100; b = 30
        elif abl == 3: a = 1500; b = 80
        elif abl == 4: a = 4000; b = 100
        elif abl == 5: a = 5000; b = 130
        elif abl == 6: a = 6500; b = 160
        elif abl == 7: a = 8000; b = 200
        elif abl == 8: a = 10000; b = 250
        elif abl == 9: a = 15000; b = 300
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00)
        if int(t.get(13, 0)): a = int(a * 0.90); b = int(b * 0.95)
        if int(t.get(21, 0)): a = int(a * 1.10); b = int(b * 1.05)
        if int(t.get(22, 0)): a = int(a * 1.10); b = int(b * 1.05)
        if int(t.get(23, 0)): a = int(a * 0.95); b = int(b * 0.95)
        if int(t.get(24, 0)): a = int(a * 1.20); b = int(b * 1.10)
        if int(t.get(32, 0)): a = int(a * 1.10); b = int(b * 1.05)
        elif int(t.get(33, 0)): a = int(a * 0.90); b = int(b * 0.95)
        if int(t.get(34, 0)): a = int(a * 1.20); b = int(b * 1.10)
        if int(t.get(35, 0)): a = int(a * 1.10); b = int(b * 1.05)
        elif int(t.get(36, 0)): a = int(a * 0.95); b = int(b * 0.95)
        if int(t.get(50, 0)): a = int(a * 0.80); b = int(b * 0.80)
        elif int(t.get(51, 0)): a = int(a * 1.50); b = int(b * 1.20)
        if int(t.get(63, 0)): a = int(a * 0.95); b = int(b * 0.95)
        if int(t.get(64, 0)): a = int(a * 0.95); b = int(b * 0.95)
        abl30 = int(target.abl.get(30, 0))
        if abl30 < 3: pass
        elif abl30 < 6: a = int(a * 0.95); b = int(b * 0.95)
        elif abl30 < 8: a = int(a * 0.90); b = int(b * 0.90)
        elif abl30 < 10: a = int(a * 0.85); b = int(b * 0.85)
        else: a = int(a * 0.80); b = int(b * 0.80)
        if a < 1: a = 1
        if b < 1: b = 1
        juel7 = int(target.juel.get(7, 0))
        exp5 = int(target.exp.get(5, 0))
        abl12 = int(target.abl.get(12, 0))
        i0 = 0
        if juel7 < a: i0 |= 1
        if exp5 < b: i0 |= 2
        if abl12 < 5 and abl12 < abl + 1: i0 |= 4
        can = i0 == 0
        return {"can_upgrade": can, "cost_juel": {7: a}, "cost_exp": {5: b}}


    def _ablup15(self, target: Character) -> Dict[str, int]:
        """话术 upgrade cost"""
        abl = int(target.abl.get(15, 0))
        t = target.talent
        abl12 = int(target.abl.get(12, 0))
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl12 >= 15:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0
        if abl == 0: a = 1; b = 3; c = 5
        elif abl == 1: a = 10; b = 10; c = 20
        elif abl == 2: a = 100; b = 30; c = 50
        elif abl == 3: a = 1500; b = 50; c = 100
        elif abl == 4: a = 3000; b = 100; c = 150
        elif abl == 5: a = 4000; b = 120; c = 180
        elif abl == 6: a = 5200; b = 150; c = 250
        elif abl == 7: a = 7500; b = 180; c = 320
        elif abl == 8: a = 9000; b = 220; c = 350
        elif abl == 9: a = 13000; b = 250; c = 400
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.25); c = int(c * 1.25)
            elif abl == 4: a = int(a * 2.00); b = int(b * 1.50); c = int(c * 1.50)
            elif abl == 5: a = int(a * 2.50); b = int(b * 1.75); c = int(c * 1.75)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 2.00); c = int(c * 2.00)
        if int(t.get(11, 0)): a = int(a * 1.50); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(13, 0)): a = int(a * 0.90); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(16, 0)): a = int(a * 1.25); b = int(b * 1.15); c = int(c * 1.15)
        if int(t.get(15, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        if int(t.get(21, 0)): a = int(a * 1.50); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(22, 0)): a = int(a * 1.50); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(23, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(25, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        elif int(t.get(26, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        if int(t.get(28, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(32, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        elif int(t.get(33, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90)
        if int(t.get(34, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        if int(t.get(35, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        elif int(t.get(36, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(50, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80)
        elif int(t.get(51, 0)): a = int(a * 1.20); b = int(b * 1.10); c = int(c * 1.10)
        if int(t.get(92, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90)
        if int(t.get(87, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(182, 0)): a = int(a * 0.60); b = int(b * 0.80); c = int(c * 0.80)
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        juel7 = int(target.juel.get(7, 0))
        exp73 = int(target.exp.get(73, 0))
        exp74 = target.get_exp(74)
        can = juel7 >= a and (exp73 >= b or exp74 >= c)
        return {"can_upgrade": can, "cost_juel": {7: a}, "cost_exp": {73: b, 74: c}}


    def _ablup16(self, target: Character) -> Dict[str, int]:
        """奉仕快乐 upgrade cost"""
        abl = int(target.abl.get(16, 0))
        t = target.talent
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 5 and int(t.get(63, 0)) == 0 and int(t.get(85, 0)) == 0 and int(t.get(86, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0; f = 0
        if abl == 0: a = 100; b = 20; c = 100; d = 1; e = 1
        elif abl == 1: a = 1200; b = 400; c = 2000; d = 1; e = 3
        elif abl == 2: a = 5000; b = 2000; c = 10000; d = 20; e = 6
        elif abl == 3: a = 10000; b = 3000; c = 0; d = 20; e = 10
        elif abl == 4: a = 30000; b = 10000; c = 0; d = 100; e = 20
        elif abl == 5: a = 50000; b = 20000; c = 0; d = 200; e = 80
        elif abl == 6: a = 70000; b = 30000; c = 0; d = 350; e = 150
        elif abl == 7: a = 100000; b = 50000; c = 0; d = 500; e = 200
        elif abl == 8: a = 150000; b = 80000; c = 0; d = 700; e = 400
        elif abl == 9: a = 200000; b = 150000; c = 0; d = 1000; e = 800
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50); d = int(d * 1.50); e = int(e * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00); d = int(d * 2.00); e = int(e * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50); d = int(d * 2.50); e = int(e * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00); d = int(d * 3.00); e = int(e * 3.00)
        if abl >= 3 and int(t.get(63, 0)) == 0 and int(t.get(85, 0)) == 0 and int(t.get(86, 0)) == 0:
            f = abl - 2
        if int(t.get(11, 0)): a = int(a * 1.20); b = int(b * 1.40); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(12, 0)): a = int(a * 1.20); d = int(d * 1.20)
        if int(t.get(13, 0)): a = int(a * 0.90); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.70)
        if int(t.get(16, 0)): a = int(a * 1.10); b = int(b * 1.10)
        if int(t.get(15, 0)): a = int(a * 1.40); b = int(b * 1.30); d = int(d * 1.20); e = int(e * 1.20)
        elif int(t.get(17, 0)): a = int(a * 0.90); b = int(b * 0.80); d = int(d * 0.80); e = int(e * 0.80)
        if int(t.get(20, 0)): a = int(a * 1.20); b = int(b * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(21, 0)): a = int(a * 1.10); b = int(b * 1.10); d = int(d * 1.20); e = int(e * 1.10)
        if int(t.get(22, 0)): a = int(a * 1.20); b = int(b * 1.20); d = int(d * 1.40); e = int(e * 1.20)
        if int(t.get(24, 0)): a = int(a * 1.30); b = int(b * 1.30); c = int(c * 1.30); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(25, 0)): a = int(a * 0.90); b = int(b * 0.80); d = int(d * 0.70); e = int(e * 0.75)
        elif int(t.get(26, 0)): a = int(a * 0.80); b = int(b * 0.80); d = int(d * 0.80); e = int(e * 0.80)
        if int(t.get(28, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90)
        if int(t.get(32, 0)): a = int(a * 1.10); b = int(b * 1.10); d = int(d * 2.50); e = int(e * 3.00)
        elif int(t.get(33, 0)): a = int(a * 0.90); b = int(b * 0.90); d = int(d * 0.70); e = int(e * 0.60)
        if int(t.get(34, 0)): a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50); d = int(d * 2.00); e = int(e * 2.00)
        if int(t.get(37, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.50); e = int(e * 0.50)
        if int(t.get(50, 0)): c = int(c * 0.80)
        if int(t.get(51, 0)): c = int(c * 1.60)
        if int(t.get(52, 0)): c = int(c * 0.80)
        if int(t.get(63, 0)): a = int(a * 0.80); b = int(b * 0.70); d = int(d * 0.60); e = int(e * 0.80)
        if int(t.get(70, 0)): e = int(e * 0.70)
        elif int(t.get(71, 0)): e = int(e * 3.00)
        if int(t.get(73, 0)): a = int(a * 0.50); b = int(b * 0.50); d = int(d * 0.50); e = int(e * 0.50)
        if int(t.get(80, 0)): a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75); e = int(e * 0.75)
        if int(t.get(83, 0)): a = int(a * 1.20); b = int(b * 1.20); d = int(d * 1.50)
        if int(t.get(85, 0)): a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75)
        if int(t.get(86, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50); e = int(e * 0.50)
        if int(t.get(87, 0)): a = int(a * 1.10); b = int(b * 1.10); d = int(d * 1.20); e = int(e * 0.80)
        if int(t.get(123, 0)): a = int(a * 2.50); b = int(b * 3.00); c = int(c * 1.50); d = int(d * 0.80); e = int(e * 0.50)
        if int(t.get(9, 0)): a = int(a * 2.50); b = int(b * 2.50); c = int(c * 2.50); d = int(d * 0.50); e = int(e * 0.50)
        if a < 1: a = 1
        if b < 1: b = 1
        if d < 1: d = 1
        if e < 1: e = 1
        juel6 = target.get_juel(6)
        juel4 = target.get_juel(4)
        juel7 = int(target.juel.get(7, 0))
        exp21 = int(target.exp.get(21, 0))
        exp2 = int(target.exp.get(2, 0))
        exp20 = int(target.exp.get(20, 0))
        exp50 = target.get_exp(50)
        abl10 = target.get_abl(10)
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 屈服点数
        i0 = 0
        if juel6 < a: i0 |= 1
        if exp2 < e: i0 |= 2
        if exp20 < e: i0 |= 2
        if abl10 < abl + 1: i0 |= 4
        if f > exp50: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel = {6: a}
            cost_exp = {2: e, 20: e}
        # Option 1: 恭顺点数
        if not can and b > 0:
            j1 = 0
            if juel4 < b: j1 |= 1
            if exp21 < d: j1 |= 2
            if abl10 < abl + 1: j1 |= 4
            if f > exp50: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {4: b}
                cost_exp = {21: d}
        # Option 2: 习得点数
        if not can and c > 0:
            k1 = 0
            if juel7 < c: k1 |= 1
            if exp2 < 1: k1 |= 2
            if abl10 < abl + 1: k1 |= 4
            if f > exp50: k1 |= 2
            if k1 == 0:
                can = True
                cost_juel = {7: c}
                cost_exp = {2: 1}
        if f > 0 and 50 not in cost_exp:
            cost_exp[50] = f
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup17(self, target: Character) -> Dict[str, int]:
        """性爱 upgrade cost"""
        abl = int(target.abl.get(17, 0))
        t = target.talent
        if abl >= 5 and int(t.get(13, 0)) == 0 and int(t.get(33, 0)) == 0 and int(t.get(28, 0)) == 0 and int(t.get(89, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0
        if abl == 0: a = 100; c = 1
        elif abl == 1: a = 1000; d = 1
        elif abl == 2: a = 3000
        elif abl == 3: a = 6000
        elif abl == 4: a = 12000
        elif abl == 5: a = 25000
        elif abl == 6: a = 50000
        elif abl == 7: a = 80000
        elif abl == 8: a = 120000
        elif abl == 9: a = 150000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50)
            elif abl == 4: a = int(a * 2.00)
            elif abl == 5: a = int(a * 2.50)
            elif abl >= 6: a = int(a * 3.00)
        if abl >= 3 and int(t.get(28, 0)) == 0 and int(t.get(33, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(88, 0)) == 0 and int(t.get(123, 0)) == 0:
            b = abl - 2
        if int(t.get(9, 0)): a = int(a * 0.80)
        if int(t.get(10, 0)): a = int(a * 1.20)
        if int(t.get(11, 0)): a = int(a * 1.50)
        if int(t.get(12, 0)): a = int(a * 1.10)
        if int(t.get(16, 0)): a = int(a * 1.10)
        if int(t.get(20, 0)): a = int(a * 1.10)
        if int(t.get(21, 0)): a = int(a * 1.10)
        if int(t.get(22, 0)): a = int(a * 1.50)
        if int(t.get(28, 0)): a = int(a * 0.50)
        if int(t.get(30, 0)): a = int(a * 1.20)
        if int(t.get(31, 0)): a = int(a * 0.90)
        if int(t.get(32, 0)): a = int(a * 1.20)
        elif int(t.get(33, 0)): a = int(a * 0.80)
        if int(t.get(34, 0)): a = int(a * 1.50)
        if int(t.get(35, 0)): a = int(a * 1.10)
        elif int(t.get(36, 0)): a = int(a * 0.90)
        if int(t.get(37, 0)): a = int(a * 0.80)
        if int(t.get(60, 0)): a = int(a * 0.90)
        if int(t.get(70, 0)): a = int(a * 0.90)
        elif int(t.get(71, 0)): a = int(a * 1.20)
        if int(t.get(72, 0)): a = int(a * 0.90)
        if int(t.get(73, 0)): a = int(a * 0.50)
        if int(t.get(76, 0)): a = int(a * 0.80)
        if int(t.get(80, 0)): a = int(a * 0.75)
        if int(t.get(83, 0)): a = int(a * 1.20)
        if int(t.get(88, 0)): a = int(a * 0.75)
        if int(t.get(123, 0)): a = int(a * 0.50)
        abl11 = target.get_abl(11)
        abl10 = target.get_abl(10)
        if a < 1: a = 1
        juel8 = int(target.juel.get(8, 0))
        exp50 = target.get_exp(50)
        exp2 = int(target.exp.get(2, 0))
        exp11 = int(target.exp.get(11, 0))
        i0 = 0
        if int(t.get(85, 0)) == 0:
            if abl11 < abl + 1: i0 |= 4
        else:
            if abl10 < abl + 1: i0 |= 4
        if exp50 < b: i0 |= 2
        if exp2 < c: i0 |= 2
        if exp11 < d: i0 |= 2
        if juel8 < a: i0 |= 1
        can = i0 == 0
        cost_exp = {}
        if b > 0: cost_exp[50] = b
        if c > 0: cost_exp[2] = c
        if d > 0: cost_exp[11] = d
        return {"can_upgrade": can, "cost_juel": {8: a}, "cost_exp": cost_exp}


    def _ablup20(self, target: Character) -> Dict[str, int]:
        """精液中毒 upgrade cost"""
        abl = int(target.abl.get(20, 0))
        t = target.talent
        abl21 = int(target.abl.get(21, 0))
        if abl >= 5 and int(t.get(80, 0)) == 0 and int(t.get(83, 0)) == 0 and int(t.get(127, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl21 >= 20:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0
        if abl == 0: a = 100; b = 5
        elif abl == 1: a = 500; b = 20
        elif abl == 2: a = 1500; b = 50
        elif abl == 3: a = 3000; b = 120
        elif abl == 4: a = 5000; b = 300
        elif abl == 5: a = 8000; b = 600
        elif abl == 6: a = 12000; b = 1500
        elif abl == 7: a = 15000; b = 3000
        elif abl == 8: a = 25000; b = 5000
        elif abl == 9: a = 30000; b = 8000
        if (abl == 3 or abl == 4 or abl == 7) and int(t.get(80, 0)) == 0 and int(t.get(83, 0)) == 0 and int(t.get(84, 0)) == 0 and int(t.get(87, 0)) == 0:
            c = abl - 2
        if int(t.get(10, 0)): a = int(a * 1.50)
        if int(t.get(11, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(12, 0)): a = int(a * 0.90)
        if int(t.get(14, 0)): a = int(a * 1.20)
        if int(t.get(16, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(15, 0)): a = int(a * 0.90); b = int(b * 0.90)
        elif int(t.get(17, 0)): a = int(a * 1.10); b = int(b * 1.10)
        if int(t.get(20, 0)): a = int(a * 1.20); b = int(b * 1.20)
        if int(t.get(21, 0)): a = int(a * 1.20); b = int(b * 1.20)
        if int(t.get(22, 0)): a = int(a * 1.50); b = int(b * 1.20)
        if int(t.get(23, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(26, 0)): a = int(a * 1.10)
        if int(t.get(28, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(30, 0)): a = int(a * 1.10); b = int(b * 1.10)
        elif int(t.get(31, 0)): a = int(a * 0.95); b = int(b * 0.95)
        if int(t.get(32, 0)): a = int(a * 0.95); b = int(b * 0.95)
        elif int(t.get(33, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(79, 0)) or int(t.get(82, 0)): a = int(a * 0.95); b = int(b * 0.95)
        if int(t.get(40, 0)): a = int(a * 1.20); b = int(b * 1.20)
        elif int(t.get(41, 0)): a = int(a * 0.90); b = int(b * 0.90)
        if int(t.get(76, 0)): a = int(a * 0.80); b = int(b * 0.80)
        if int(t.get(80, 0)): a = int(a * 0.80); b = int(b * 0.80)
        if int(t.get(83, 0)): a = int(a * 0.50); b = int(b * 0.50)
        if int(t.get(88, 0)): a = int(a * 1.20); b = int(b * 1.20)
        if int(t.get(84, 0)): a = int(a * 0.80); b = int(b * 0.80)
        if int(t.get(87, 0)): a = int(a * 0.80); b = int(b * 0.80)
        if int(t.get(123, 0)): a = int(a * 0.50); b = int(b * 0.50)
        if int(t.get(9, 0)): a = int(a * 2.00); b = int(b * 2.00)
        juel5 = target.get_juel(5)
        exp33 = int(target.exp.get(33, 0))
        exp50 = target.get_exp(50)
        abl11 = target.get_abl(11)
        i0 = 0
        if juel5 < a: i0 |= 1
        if exp33 < b: i0 |= 2
        if exp50 < c: i0 |= 2
        if abl11 < abl + 1: i0 |= 4
        can = i0 == 0
        cost_exp = {}
        if b > 0: cost_exp[33] = b
        if c > 0: cost_exp[50] = c
        return {"can_upgrade": can, "cost_juel": {5: a}, "cost_exp": cost_exp}


    def _ablup21(self, target: Character) -> Dict[str, int]:
        """百合 upgrade cost"""
        abl = int(target.abl.get(21, 0))
        t = target.talent
        abl20 = int(target.abl.get(20, 0))
        if abl >= 5 and int(t.get(10, 0)) == 0 and int(t.get(14, 0)) == 0 and int(t.get(37, 0)) == 0 and int(t.get(88, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl20 >= 20:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0; f = 0; g = 1
        if abl == 0: a = 100; b = 100; c = 0; d = 100; e = 100
        elif abl == 1: a = 500; b = 500; c = 0; d = 500; e = 300
        elif abl == 2: a = 1200; b = 1000; c = 0; d = 1500; e = 1000
        elif abl == 3: a = 0; b = 0; c = 30; d = 2800; e = 6000
        elif abl == 4: a = 0; b = 0; c = 80; d = 4300; e = 12000
        elif abl == 5: a = 0; b = 0; c = 150; d = 6000; e = 24000
        elif abl == 6: a = 0; b = 0; c = 200; d = 8000; e = 38000
        elif abl == 7: a = 0; b = 0; c = 300; d = 11000; e = 56000
        elif abl == 8: a = 0; b = 0; c = 450; d = 15000; e = 86000
        elif abl == 9: a = 0; b = 0; c = 600; d = 20000; e = 120000
        if int(t.get(27, 0)):
            if abl == 3: c = int(c * 1.50); d = int(d * 1.50); e = int(e * 1.50)
            elif abl == 4: c = int(c * 2.00); d = int(d * 2.00); e = int(e * 2.00)
            elif abl == 5: c = int(c * 2.50); d = int(d * 2.50); e = int(e * 2.50)
            elif abl >= 6: c = int(c * 3.00); d = int(d * 3.00); e = int(e * 3.00)
        if (abl == 3 or abl == 4 or abl == 7) and int(t.get(33, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(88, 0)) == 0:
            f = abl - 2
        if int(t.get(10, 0)): a = int(a * 1.10); b = int(b * 1.10); c = int(c * 1.10); d = int(d * 1.10); e = int(e * 1.10)
        if int(t.get(11, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(12, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(16, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(15, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        elif int(t.get(17, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90); e = int(e * 0.90)
        if int(t.get(20, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(21, 0)): a = int(a * 1.10); b = int(b * 1.10); c = int(c * 1.10); d = int(d * 1.10); e = int(e * 1.10)
        if int(t.get(22, 0)): a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50); d = int(d * 1.50); e = int(e * 1.50)
        if int(t.get(24, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(26, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90); e = int(e * 0.90)
        if int(t.get(30, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        elif int(t.get(31, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90); e = int(e * 0.90)
        if int(t.get(32, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        elif int(t.get(33, 0)): a = int(a * 0.60); b = int(b * 0.60); c = int(c * 0.60); d = int(d * 0.60); e = int(e * 0.60)
        if int(t.get(34, 0)): a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00); d = int(d * 2.00); e = int(e * 2.00)
        if int(t.get(35, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90); e = int(e * 0.90)
        elif int(t.get(36, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(40, 0)): a = int(a * 1.10); b = int(b * 1.10); c = int(c * 1.10); d = int(d * 1.10); e = int(e * 1.10)
        elif int(t.get(41, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95); e = int(e * 0.95)
        if int(t.get(70, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90); d = int(d * 0.90); e = int(e * 0.90)
        elif int(t.get(71, 0)): a = int(a * 1.10); b = int(b * 1.10); c = int(c * 1.10); d = int(d * 1.10); e = int(e * 1.10)
        if int(t.get(76, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.80); e = int(e * 0.80)
        if int(t.get(80, 0)): a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75); e = int(e * 0.75)
        if int(t.get(83, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20); e = int(e * 1.20)
        if int(t.get(88, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50); e = int(e * 0.50)
        if int(t.get(123, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.80); e = int(e * 0.80)
        if int(t.get(9, 0)): a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00); d = int(d * 2.00); e = int(e * 2.00)
        abl11 = target.get_abl(11)
        juel9 = int(target.juel.get(9, 0))
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        exp30 = int(target.exp.get(30, 0))
        exp50 = target.get_exp(50)
        exp2 = int(target.exp.get(2, 0))
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 苦痛+欲情
        if b > 0:
            i0 = 0
            if abl11 < abl + 1: i0 |= 4
            if exp50 < f: i0 |= 2
            if juel9 < a: i0 |= 1
            if juel5 < b: i0 |= 1
            if exp30 < c: i0 |= 2
            if i0 == 0:
                can = True
                cost_juel = {9: a, 5: b}
                cost_exp = {}
                if c > 0: cost_exp[30] = c
        # Option 1: 苦痛+屈服
        if not can and d > 0:
            j1 = 0
            if abl11 < abl + 1: j1 |= 4
            if exp50 < f: j1 |= 2
            if juel9 < d: j1 |= 1
            if juel6 < e: j1 |= 1
            if exp30 < c: j1 |= 2
            if exp2 < g: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {9: d, 6: e}
                cost_exp = {2: g}
                if c > 0: cost_exp[30] = c
        if f > 0 and 50 not in cost_exp:
            cost_exp[50] = f
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup22(self, target: Character) -> Dict[str, int]:
        """调教者技巧 upgrade cost"""
        abl = int(target.abl.get(22, 0))
        t = target.talent
        if int(t.get(122, 0)):
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 5 and int(t.get(33, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(82, 0)) == 0 and int(t.get(123, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0
        if abl == 0: a = 200; b = 50; c = 0; d = 1000
        elif abl == 1: a = 1000; b = 150; c = 0; d = 5000
        elif abl == 2: a = 3000; b = 300; c = 1000; d = 0
        elif abl == 3: a = 8000; b = 500; c = 2000; d = 0
        elif abl == 4: a = 20000; b = 800; c = 5000; d = 0
        elif abl == 5: a = 40000; b = 1200; c = 10000; d = 0
        elif abl == 6: a = 80000; b = 1800; c = 13000; d = 0
        elif abl == 7: a = 150000; b = 2600; c = 18000; d = 0
        elif abl == 8: a = 200000; b = 3600; c = 30000; d = 0
        elif abl == 9: a = 300000; b = 5000; c = 50000; d = 0
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50); c = int(c * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00)
        if abl >= 3 and int(t.get(33, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(123, 0)) == 0:
            e = abl - 2
        if int(t.get(13, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(21, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(23, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(24, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(30, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        elif int(t.get(31, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(63, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(70, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        elif int(t.get(71, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(80, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.80)
        if int(t.get(79, 0)): a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00); d = int(d * 2.00)
        if int(t.get(81, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if int(t.get(82, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if int(t.get(123, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if a < 1: a = 1
        if b < 1: b = 1
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        juel0 = int(target.juel.get(0, 0))
        exp40 = int(target.exp.get(40, 0))
        exp50 = target.get_exp(50)
        abl11 = target.get_abl(11)
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 欲情+屈服+百合经验
        i0 = 0
        if exp50 < e: i0 |= 2
        if juel5 < a: i0 |= 1
        if juel6 < c: i0 |= 1
        if exp40 < b: i0 |= 2
        if abl11 < abl + 1: i0 |= 4
        if i0 == 0:
            can = True
            cost_juel = {5: a}
            if c > 0: cost_juel[6] = c
            cost_exp = {40: b}
        # Option 1: 快C+百合经验
        if not can and d > 0:
            j1 = 0
            if exp50 < e: j1 |= 2
            if juel0 < d: j1 |= 1
            if exp40 < b: j1 |= 2
            if abl11 < abl + 1: j1 |= 4
            if j1 == 0:
                can = True
                cost_juel = {0: d}
                cost_exp = {40: b}
        if e > 0 and 50 not in cost_exp:
            cost_exp[50] = e
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup23(self, target: Character) -> Dict[str, int]:
        """调教者性技 upgrade cost"""
        abl = int(target.abl.get(23, 0))
        t = target.talent
        if int(t.get(122, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 5 and int(t.get(33, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(123, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0
        if abl == 0: a = 200; b = 50; c = 0; d = 1000
        elif abl == 1: a = 1000; b = 150; c = 0; d = 5000
        elif abl == 2: a = 3000; b = 300; c = 1000; d = 0
        elif abl == 3: a = 8000; b = 500; c = 2000; d = 0
        elif abl == 4: a = 20000; b = 800; c = 5000; d = 0
        elif abl == 5: a = 40000; b = 1200; c = 10000; d = 0
        elif abl == 6: a = 80000; b = 1800; c = 13000; d = 0
        elif abl == 7: a = 150000; b = 2600; c = 18000; d = 0
        elif abl == 8: a = 200000; b = 3600; c = 30000; d = 0
        elif abl == 9: a = 300000; b = 5000; c = 50000; d = 0
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50); c = int(c * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00)
        if abl >= 3 and int(t.get(33, 0)) == 0 and int(t.get(80, 0)) == 0 and int(t.get(81, 0)) == 0 and int(t.get(123, 0)) == 0:
            e = abl - 2
        if int(t.get(13, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(21, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(23, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(24, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(30, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        elif int(t.get(31, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(82, 0)): a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00); d = int(d * 3.00)
        if int(t.get(63, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        if int(t.get(70, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95); d = int(d * 0.95)
        elif int(t.get(71, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20); d = int(d * 1.20)
        if int(t.get(80, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80); d = int(d * 0.80)
        if int(t.get(81, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if int(t.get(123, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if a < 1: a = 1
        if b < 1: b = 1
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        juel2 = int(target.juel.get(2, 0))
        exp41 = int(target.exp.get(41, 0))
        exp50 = target.get_exp(50)
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 欲情+屈服+断背经验
        i0 = 0
        if exp50 < e: i0 |= 2
        if juel5 < a: i0 |= 1
        if juel6 < c: i0 |= 1
        if exp41 < b: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel = {5: a}
            if c > 0: cost_juel[6] = c
            cost_exp = {41: b}
        # Option 1: 快A+断背经验
        if not can and d > 0:
            j1 = 0
            if exp50 < e: j1 |= 2
            if juel2 < d: j1 |= 1
            if exp41 < b: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {2: d}
                cost_exp = {41: b}
        if e > 0 and 50 not in cost_exp:
            cost_exp[50] = e
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup30(self, target: Character) -> Dict[str, int]:
        """战斗 upgrade cost"""
        abl = int(target.abl.get(30, 0))
        t = target.talent
        abl31 = int(target.abl.get(31, 0))
        if abl >= 5 and int(t.get(85, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(63, 0)) == 0 and int(t.get(70, 0)) == 0 and int(t.get(75, 0)) == 0 and int(t.get(77, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl31 >= 20:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; f = 0
        if abl == 0: a = 3000; b = 10000; c = 10
        elif abl == 1: a = 8000; b = 25000; c = 25
        elif abl == 2: a = 15000; b = 50000; c = 40
        elif abl == 3: a = 30000; b = 100000; c = 80
        elif abl == 4: a = 55000; b = 200000; c = 200
        elif abl == 5: a = 70000; b = 300000; c = 400
        elif abl == 6: a = 90000; b = 400000; c = 800
        elif abl == 7: a = 120000; b = 550000; c = 1200
        elif abl == 8: a = 150000; b = 700000; c = 1500
        elif abl == 9: a = 200000; b = 900000; c = 2000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50); c = int(c * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00)
        if int(t.get(12, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(20, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(21, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(24, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(30, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        elif int(t.get(31, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90)
        if int(t.get(32, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        elif int(t.get(33, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80)
        if int(t.get(34, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(35, 0)): a = int(a * 1.10); b = int(b * 1.10); c = int(c * 1.10)
        elif int(t.get(36, 0)): a = int(a * 0.95); b = int(b * 0.95); c = int(c * 0.95)
        if int(t.get(70, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90)
        elif int(t.get(71, 0)): a = int(a * 1.20); b = int(b * 1.20); c = int(c * 1.20)
        if int(t.get(72, 0)): a = int(a * 0.60); b = int(b * 0.60); c = int(c * 0.60)
        if int(t.get(73, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50)
        if int(t.get(76, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80)
        if int(t.get(87, 0)): a = int(a * 0.90); b = int(b * 0.90); c = int(c * 0.90)
        if int(t.get(123, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80)
        if int(t.get(9, 0)): a = int(a * 0.80); b = int(b * 0.80); c = int(c * 0.80)
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        if abl >= 2 and int(t.get(33, 0)) == 0 and int(t.get(72, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(123, 0)) == 0:
            f = abl - 1
        juel5 = target.get_juel(5)
        juel6 = target.get_juel(6)
        exp5 = int(target.exp.get(5, 0))
        exp50 = target.get_exp(50)
        abl16 = int(target.abl.get(16, 0))
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: normal cost
        i0 = 0
        if f > 0 and exp50 < f: i0 |= 2
        if abl16 < abl + 1: i0 |= 4
        if juel5 < a: i0 |= 1
        if juel6 < b: i0 |= 1
        if exp5 < c: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel = {5: a, 6: b}
            cost_exp = {5: c}
        # Option 1: 3x juel, half exp
        if not can:
            j1 = 0
            if f > 0 and exp50 < f: j1 |= 2
            if abl16 < abl + 1: j1 |= 4
            if juel5 < a * 3: j1 |= 1
            if juel6 < b * 3: j1 |= 1
            if exp5 < c // 2: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {5: a * 3, 6: b * 3}
                cost_exp = {5: c // 2}
        if f > 0 and 50 not in cost_exp:
            cost_exp[50] = f
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}


    def _ablup31(self, target: Character) -> Dict[str, int]:
        """战技 upgrade cost"""
        abl = int(target.abl.get(31, 0))
        t = target.talent
        abl30 = int(target.abl.get(30, 0))
        if abl >= 5 and int(t.get(85, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(60, 0)) == 0 and int(t.get(70, 0)) == 0 and int(t.get(74, 0)) == 0 and int(t.get(78, 0)) == 0:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl >= 10:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        if abl + abl30 >= 20:
            return {"can_upgrade": False, "cost_juel": {}, "cost_exp": {}}
        a = 0; b = 0; c = 0; d = 0; e = 0; f = 0
        if abl == 0: a = 3000; b = 10000; c = 1000; d = 100; e = 20
        elif abl == 1: a = 6000; b = 25000; c = 3000; d = 250; e = 40
        elif abl == 2: a = 12000; b = 50000; c = 6000; d = 500; e = 60
        elif abl == 3: a = 20000; b = 100000; c = 15000; d = 1000; e = 100
        elif abl == 4: a = 32000; b = 200000; c = 30000; d = 1500; e = 150
        elif abl == 5: a = 50000; b = 250000; c = 40000; d = 2000; e = 200
        elif abl == 6: a = 70000; b = 320000; c = 50000; d = 3000; e = 320
        elif abl == 7: a = 100000; b = 500000; c = 70000; d = 4000; e = 500
        elif abl == 8: a = 150000; b = 800000; c = 100000; d = 6000; e = 800
        elif abl == 9: a = 200000; b = 1000000; c = 150000; d = 8000; e = 1000
        if int(t.get(27, 0)):
            if abl == 3: a = int(a * 1.50); b = int(b * 1.50); c = int(c * 1.50); d = int(d * 1.50); e = int(e * 1.50)
            elif abl == 4: a = int(a * 2.00); b = int(b * 2.00); c = int(c * 2.00); d = int(d * 2.00); e = int(e * 2.00)
            elif abl == 5: a = int(a * 2.50); b = int(b * 2.50); c = int(c * 2.50); d = int(d * 2.50); e = int(e * 2.50)
            elif abl >= 6: a = int(a * 3.00); b = int(b * 3.00); c = int(c * 3.00); d = int(d * 3.00); e = int(e * 3.00)
        if abl == 2 and int(t.get(33, 0)) == 0 and int(t.get(60, 0)) == 0 and int(t.get(72, 0)) == 0 and int(t.get(76, 0)) == 0 and int(t.get(123, 0)) == 0:
            f = abl - 1
        if int(t.get(60, 0)): a = int(a * 0.25); b = int(b * 0.25); c = int(c * 0.25); d = int(d * 0.25)
        if int(t.get(72, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        if int(t.get(80, 0)): a = int(a * 0.75); b = int(b * 0.75); c = int(c * 0.75); d = int(d * 0.75)
        if int(t.get(76, 0)): a = int(a * 0.50); b = int(b * 0.50); c = int(c * 0.50); d = int(d * 0.50)
        abl17 = int(target.abl.get(17, 0))
        abl0 = int(target.abl.get(0, 0))
        if a < 1: a = 1
        if b < 1: b = 1
        if c < 1: c = 1
        if d < 1: d = 1
        if e < 1: e = 1
        juel5 = target.get_juel(5)
        juel0 = int(target.juel.get(0, 0))
        juel8 = int(target.juel.get(8, 0))
        exp10 = int(target.exp.get(10, 0))
        exp11 = int(target.exp.get(11, 0))
        exp50 = target.get_exp(50)
        cost_juel = {}
        cost_exp = {}
        can = False
        # Option 0: 自慰经验
        i0 = 0
        if f > exp50: i0 |= 2
        if abl17 < abl + 1: i0 |= 4
        if abl0 < abl + 1: i0 |= 4
        if juel5 < a: i0 |= 1
        if juel0 < b: i0 |= 1
        if juel8 < c: i0 |= 1
        if exp10 < d: i0 |= 2
        if i0 == 0:
            can = True
            cost_juel = {5: a, 0: b, 8: c}
            cost_exp = {10: d}
        # Option 1: 调教自慰经验
        if not can:
            j1 = 0
            if f > exp50: j1 |= 2
            if abl17 < abl + 1: j1 |= 4
            if abl0 < abl + 1: j1 |= 4
            if juel5 < a: j1 |= 1
            if juel0 < b: j1 |= 1
            if juel8 < c: j1 |= 1
            if exp11 < e: j1 |= 2
            if j1 == 0:
                can = True
                cost_juel = {5: a, 0: b, 8: c}
                cost_exp = {11: e}
        if f > 0 and 50 not in cost_exp:
            cost_exp[50] = f
        return {"can_upgrade": can, "cost_juel": cost_juel, "cost_exp": cost_exp}

    # =====================================================================
    # 通用 ABLUP 成本检查与扣除方法 (基于 ABLUP_COST_TABLE)
    # =====================================================================

    def _check_ablup_cost(self, target: Character, abl_id: int, current_level: int) -> bool:
        """检查目标角色是否满足指定能力升级的基础成本条件。

        仅检查 ABLUP_COST_TABLE 中的基础 JUEL/EXP 成本,
        不处理素质修正、前置能力等复杂逻辑。
        对于复杂能力, 应使用对应的 _ablupN 方法。

        Args:
            target: 目标角色
            abl_id: 能力ID
            current_level: 当前等级

        Returns:
            True 如果基础 JUEL 和 EXP 均满足
        """
        entry = ABLUP_COST_TABLE.get(abl_id)
        if entry is None:
            return False
        levels = entry.get("levels", [])
        if current_level < 0 or current_level >= len(levels):
            return False
        level_data = levels[current_level]
        # 检查 JUEL
        for juel_id, amount in level_data.get("juel", {}).items():
            if int(target.juel.get(juel_id, 0)) < amount:
                return False
        # 检查 EXP
        for exp_id, amount in level_data.get("exp", {}).items():
            if int(target.exp.get(exp_id, 0)) < amount:
                return False
        return True

    def _apply_ablup_cost(self, target: Character, abl_id: int, current_level: int) -> None:
        """扣除指定能力升级的基础 JUEL/EXP 成本。

        仅扣除 ABLUP_COST_TABLE 中的基础成本,
        不处理素质修正、前置能力等复杂逻辑。
        调用前应先通过 _check_ablup_cost 确认条件满足。

        Args:
            target: 目标角色
            abl_id: 能力ID
            current_level: 当前等级
        """
        entry = ABLUP_COST_TABLE.get(abl_id)
        if entry is None:
            return
        levels = entry.get("levels", [])
        if current_level < 0 or current_level >= len(levels):
            return
        level_data = levels[current_level]
        # 扣除 JUEL
        for juel_id, amount in level_data.get("juel", {}).items():
            current = int(target.juel.get(juel_id, 0))
            target.juel[juel_id] = current - amount
        # 扣除 EXP (注意: ERB原版中EXP通常不扣除, 仅检查阈值;
        # 但此方法提供扣除能力, 由调用方决定是否使用)
        for exp_id, amount in level_data.get("exp", {}).items():
            current = int(target.exp.get(exp_id, 0))
            target.exp[exp_id] = current - amount

    # =====================================================================
    # DUNGEON 剩余子系统
    # =====================================================================

    # ------------------------------------------------------------------
    # DUNGEON_DAILY (地城日常)
    # ------------------------------------------------------------------


