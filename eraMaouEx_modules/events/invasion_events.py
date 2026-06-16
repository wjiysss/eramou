"""
eraMaouEx 事件系统模块 - 侵略事件、回合结束、结局等
对应 ERB INVASION.ERB, INVASION_EVENT.ERB, EVENT_TURNEND.ERB, ENDING.ERB, ENTER_ENEMY.ERB
"""

import random
from typing import Dict, List, Optional, Any, Tuple


# ============================================================
# 常量定义 - 对应 ERB 中的 FLAG 编号
# ============================================================

# 侵攻度 FLAG 编号
FLAG_AREA_HUMAN = 81       # 人间界侵攻度
FLAG_AREA_ELF = 86         # 精灵领域侵攻度
FLAG_AREA_DRAGON = 88      # 龙之山脉侵攻度
FLAG_AREA_HEAVEN = 90      # 天界侵攻度
EX_FLAG_AREA_PALACE = 101  # 天神宫侵攻度 (EX_FLAG)

# 征服状态 FLAG 编号 (0=未征服, 1=征服中, 2=已征服)
FLAG_SINDO_HUMAN = 82      # 人间界征服状态
FLAG_SINDO_ELF = 87        # 精灵领域征服状态
FLAG_SINDO_DRAGON = 89     # 龙之山脉征服状态
FLAG_SINDO_HEAVEN = 91     # 天界征服状态
EX_FLAG_SINDO_PALACE = 102 # 天神宫征服状态 (EX_FLAG)

# 侵略事件阶段 FLAG 编号
FLAG_EVENT_HUMAN = 93      # 人间界事件阶段
FLAG_EVENT_ELF = 94        # 精灵领域事件阶段
FLAG_EVENT_DRAGON = 95     # 龙之山脉事件阶段
FLAG_EVENT_HEAVEN = 96     # 天界事件阶段

# 侵攻度阈值
THRESHOLDS = [2000, 4000, 6000, 8000, 10000]

# 侵攻类型
INV_TYPE_MONSTER = 0   # 使用现有怪物的一半去进攻（资金・俘虏）
INV_TYPE_MAGIC = 1     # 使用魔王的魔力（经验值）
INV_TYPE_HERO = 2      # 派遣勇者带三分之一的怪物去进攻（资金・经验值・俘虏）
INV_TYPE_PLUNDER = 3   # 派遣勇者前去掠夺资金（资金・经验值）

# 区域 ID 常量
AREA_HUMAN = 1    # 人间界
AREA_ELF = 2      # 精灵领域
AREA_DRAGON = 3   # 龙之山脉
AREA_HEAVEN = 4   # 天界
AREA_FORT = 5     # 圣灵骑士堡垒
AREA_PALACE = 6   # 天神宫

# 水晶球相关 EX_FLAG 编号
EX_FLAG_VIDEO_TOTAL = 9010     # 水晶球总数
EX_FLAG_VIDEO_DEPLOYED = 9011  # 已投放数
EX_FLAG_VIDEO_POPULAR = 9012   # 正流行的数量
EX_FLAG_VIDEO_DAYS = 9013      # 流行天数

# 声望值 EX_FLAG
EX_FLAG_FAME = 99

# 勇者基础等级补正
FLAG_HERO_LEVEL = 60

# 据点事件文本 - 对应 ERB KYOTEN_EVENT
KYOTEN_EVENT_TEXT = {
    # 人间界 (ARG:0 == 1)
    AREA_HUMAN: {
        "advance": {
            0: "占领了村庄",
            1: "占领了港口",
            2: "攻陷了堡垒",
            3: "占领了街道",
            4: "占领了城市",
        },
        "retreat": {
            1: "人间界的军队占领了村庄",
            2: "人间界的军队占领了港口",
            3: "人间界的军队攻陷了堡垒",
            4: "人间界的军队占领了街道",
            5: "人间界的军队占领了城市",
        },
        "retreat_thresholds": {1: 500, 2: 2000, 3: 4000, 4: 6000, 5: 8000},
    },
    # 精灵领域 (ARG:0 == 2)
    AREA_ELF: {
        "advance": {
            0: "进入了精灵森林",
            1: "占领了精灵村落",
            2: "攻陷了精灵堡垒",
            3: "占领了精灵王宫",
            4: "征服了精灵领域",
        },
        "retreat": {
            1: "精灵族的抵抗军夺回了精灵森林",
            2: "精灵族的抵抗军夺回了精灵村落",
            3: "精灵族的抵抗军夺回了精灵堡垒",
            4: "精灵族的抵抗军夺回了精灵王宫",
            5: "精灵族的抵抗军夺回了精灵领域",
        },
        "retreat_thresholds": {1: 500, 2: 2000, 3: 4000, 4: 6000, 5: 8000},
    },
    # 龙之山脉 (ARG:0 == 3)
    AREA_DRAGON: {
        "advance": {
            0: "进入了龙之山",
            1: "占领了龙穴入口",
            2: "攻陷了龙巢",
            3: "占领了龙神殿",
            4: "征服了龙之山脉",
        },
        "retreat": {
            1: "龙族夺回了龙穴入口",
            2: "龙族夺回了龙巢",
            3: "龙族夺回了龙神殿",
            4: "龙族夺回了龙之山脉",
            5: "龙族夺回了龙之山脉全境",
        },
        "retreat_thresholds": {1: 500, 2: 2000, 3: 4000, 4: 6000, 5: 8000},
    },
    # 天界 (ARG:0 == 4)
    AREA_HEAVEN: {
        "advance": {
            0: "进入了天界入口",
            1: "占领了天使城",
            2: "攻陷了圣殿",
            3: "占领了神殿",
            4: "征服了天界",
        },
        "retreat": {
            1: "天界的军队夺回了天界入口",
            2: "天界的军队夺回了天使城",
            3: "天界的军队夺回了圣殿",
            4: "天界的军队夺回了神殿",
            5: "天界的军队夺回了天界全境",
        },
        "retreat_thresholds": {1: 500, 2: 2000, 3: 4000, 4: 6000, 5: 8000},
    },
}

# 每日侵攻度衰减规则 - 对应 ERB SYSTEM.ERB 中的侵攻度减少逻辑
DAILY_INVASION_DECAY_RULES = {
    AREA_HUMAN: {
        "area_flag": FLAG_AREA_HUMAN,
        "sindo_flag": FLAG_SINDO_HUMAN,
        "event_flag": FLAG_EVENT_HUMAN,
        "area_id": AREA_HUMAN,
        "unconquered": {
            "condition": lambda sindo: sindo == 0,
            "decay_range": (0, 100),
            "min_after_decay": 0,
            "message": "人间界的军队反抗着魔王军的侵略………",
            "message_after": "*人间界的侵略度减少了*",
        },
        "conquered": {
            "condition": lambda sindo: sindo == 1,
            "decay_chance": 6,  # RAND:6 == 0
            "decay_range": (0, 100),
            "min_after_decay": 100,
            "message": "人间界的军队为了夺回领地、反抗着魔王军………",
            "message_after": "*地上的魔界领土的侵略度减少了*",
        },
    },
    AREA_ELF: {
        "area_flag": FLAG_AREA_ELF,
        "sindo_flag": FLAG_SINDO_ELF,
        "event_flag": FLAG_EVENT_ELF,
        "area_id": AREA_ELF,
        "unconquered": {
            "condition": lambda sindo: sindo == 0,
            "decay_range": (0, 100),
            "min_after_decay": 0,
            "message": "精灵族的抵抗组织反抗着魔王军………",
            "message_after": "*精灵领域的侵略度减少了*",
        },
        "conquered": {
            "condition": lambda sindo: sindo == 1,
            "decay_chance": 5,  # RAND:5 == 0
            "decay_range": (0, 100),
            "min_after_decay": 100,
            "message": "精灵族的抵抗组织为了夺回领地、反抗着魔王军………",
            "message_after": "*黑暗精灵的领土的侵略度减少了*",
        },
    },
    AREA_DRAGON: {
        "area_flag": FLAG_AREA_DRAGON,
        "sindo_flag": FLAG_SINDO_DRAGON,
        "event_flag": FLAG_EVENT_DRAGON,
        "area_id": AREA_DRAGON,
        "unconquered": {
            "condition": lambda sindo: sindo == 0,
            "decay_range": (0, 100),
            "min_after_decay": 0,
            "message": "成群的龙抵抗着魔王的军队………",
            "message_after": "*龙之山脉的侵略度减少了*",
        },
        "conquered": {
            "condition": lambda sindo: sindo == 1,
            "decay_chance": 4,  # RAND:4 == 0
            "decay_range": (0, 100),
            "min_after_decay": 100,
            "message": "成群的龙为了夺回领地、反抗着魔王军………",
            "message_after": "*混沌龙之山的侵略度减少了*",
        },
    },
    AREA_HEAVEN: {
        "area_flag": FLAG_AREA_HEAVEN,
        "sindo_flag": FLAG_SINDO_HEAVEN,
        "event_flag": FLAG_EVENT_HEAVEN,
        "area_id": AREA_HEAVEN,
        "unconquered": {
            "condition": lambda sindo: sindo == 0,
            "decay_range": (0, 100),
            "min_after_decay": 0,
            "message": "天界的军队抵抗着魔王军………",
            "message_after": "*天界的侵略度减少了*",
        },
        "conquered": {
            "condition": lambda sindo: sindo == 1,
            "decay_chance": 3,  # RAND:3 == 0
            "decay_range": (0, 100),
            "min_after_decay": 100,
            "message": "天界的军队为了夺回领地、反抗着魔王军………",
            "message_after": "*堕天使的淫界的侵略度减少了*",
        },
    },
}

# 征服贡品角色配置 - 对应 ERB CHAR_GIFT
INVASION_CONQUEST_REWARD_CONFIG_TRIBUTE = {
    AREA_ELF: {
        "char_no": 31,    # 精灵族圣女
        "race": 1,        # 精灵
        "message": "精灵族圣女被精灵族作为贡品献了上来………",
        "question": "要收下精灵族圣女作为贡品吗？",
    },
    AREA_DRAGON: {
        "char_no": 32,    # 龙族公主
        "race": 5,        # 龙族
        "message": "龙族公主被龙族长老作为贡品献了上来………",
        "question": "要收下龙族公主作为贡品吗？",
    },
    AREA_HEAVEN: {
        "char_no": 33,    # 天使族下任主神
        "race": 6,        # 天使
        "message": "天使族的下任主神被天使族作为贡品献了上来………",
        "question": "要收下天使族下任主神作为贡品吗？",
    },
}


# ============================================================
# InvasionManager - 侵略主逻辑 (对应 @INVASION)
# ============================================================

class InvasionManager:
    """侵略管理器 - 处理侵略主逻辑、侵攻点计算、威望值补正、水晶球系统"""

    # 区域选择映射: 选择编号 -> (area_flag, sindo_flag, area_id)
    AREA_SELECT_MAP = {
        0: (FLAG_AREA_HUMAN, FLAG_SINDO_HUMAN, AREA_HUMAN),
        1: (FLAG_AREA_ELF, FLAG_SINDO_ELF, AREA_ELF),
        2: (FLAG_AREA_DRAGON, FLAG_SINDO_DRAGON, AREA_DRAGON),
        3: (FLAG_AREA_HEAVEN, FLAG_SINDO_HEAVEN, AREA_HEAVEN),
        4: None,  # 圣灵骑士堡垒 -> ARCANA_FORT
        5: (EX_FLAG_AREA_PALACE, EX_FLAG_SINDO_PALACE, AREA_PALACE),
    }

    def __init__(self, game_engine):
        self.engine = game_engine
        self._hero_generator = HeroGenerator(game_engine)

    def _vars(self):
        return self.engine.interpreter.vars

    def get_flag(self, idx, default=0):
        return int(self._vars().get_flag(idx, default))

    def set_flag(self, idx, value):
        self._vars().set_flag(idx, value)

    def get_ex_flag(self, idx, default=0):
        return int(self._vars().get_ex_flag(idx, default))

    def set_ex_flag(self, idx, value):
        self._vars().set_ex_flag(idx, value)

    # ---- 区域信息显示 ----

    def get_area_display_info(self) -> Dict[str, Any]:
        """获取各区域侵攻度显示信息"""
        info = {}
        v = self._vars()

        # 人间界
        info["human"] = {
            "name": "地上的魔界领土" if self.get_flag(FLAG_SINDO_HUMAN) else "人间界",
            "progress": self.get_flag(FLAG_AREA_HUMAN),
            "conquered": self.get_flag(FLAG_SINDO_HUMAN) >= 1,
        }
        # 精灵领域
        info["elf"] = {
            "name": "黑暗精灵的领土" if self.get_flag(FLAG_SINDO_ELF) >= 1 else "精灵族的领域",
            "progress": self.get_flag(FLAG_AREA_ELF),
            "conquered": self.get_flag(FLAG_SINDO_ELF) >= 1,
        }
        # 龙之山脉
        info["dragon"] = {
            "name": "混沌龙之山" if self.get_flag(FLAG_SINDO_DRAGON) >= 1 else "龙之山脉",
            "progress": self.get_flag(FLAG_AREA_DRAGON),
            "conquered": self.get_flag(FLAG_SINDO_DRAGON) >= 1,
        }
        # 天界
        info["heaven"] = {
            "name": "堕天使的淫界" if self.get_flag(FLAG_SINDO_HEAVEN) >= 1 else "天界",
            "progress": self.get_flag(FLAG_AREA_HEAVEN),
            "conquered": self.get_flag(FLAG_SINDO_HEAVEN) >= 1,
        }
        # 圣灵骑士堡垒
        info["fort"] = {
            "name": "圣灵骑士的卖春堡垒" if self.get_flag(92) == 15 else "圣灵骑士的堡垒",
            "conquered": self.get_flag(92) == 15,
        }
        # 天神宫
        palace_progress = self.get_ex_flag(EX_FLAG_AREA_PALACE)
        palace_sindo = self.get_ex_flag(EX_FLAG_SINDO_PALACE)
        palace_visible = (
            (self.get_ex_flag(2810) >= 501 and self.get_ex_flag(2810) < 540) or
            (self.get_ex_flag(2810) >= 541 and self.get_ex_flag(2810) < 560) or
            palace_sindo >= 4
        )
        palace_name = "淫乱意志的神宫" if palace_sindo >= 4 else "天神宫"
        info["palace"] = {
            "name": palace_name,
            "progress": palace_progress,
            "conquered": palace_sindo >= 4,
            "visible": palace_visible,
        }
        return info

    # ---- 侵攻点计算 ----

    def calc_monster_invasion_points(self) -> Tuple[int, List[str]]:
        """
        怪物侵攻 (INV_TYPE == 0)
        计算怪物战斗力贡献，怪物数量减半
        返回 (侵攻点, 消息列表)
        """
        messages = []
        sinkou = 0
        v = self._vars()

        for mon_id in range(100, 190):
            item_count = v.get_item(mon_id, 0)
            if item_count < 1:
                continue

            mon_atk = 0
            # 调用 MONSTER_DATA 获取怪物数据 (stub)
            e_data = self._get_monster_data(mon_id)

            mon_atk += e_data.get(2, 0)  # 攻击
            mon_atk += e_data.get(3, 0)  # 防御
            mon_atk += e_data.get(4, 0)  # 速度

            if e_data.get(5, 0) != 0:  # 特殊1
                mon_atk += e_data.get(1, 0)
            if e_data.get(6, 0) != 0:  # 特殊2
                mon_atk += e_data.get(1, 0)

            # 怪物数量减半
            v.set_item(mon_id, item_count // 2)

            sinkou += mon_atk * ((item_count // 9) + 1)

        # 怪物カンストで最大約19万の1/20
        sinkou //= 20

        # 威望值补正
        sinkou, fame_msgs = self._apply_fame_modifier(sinkou)
        messages.extend(fame_msgs)

        messages.append(f"怪物的战斗力　{sinkou}点")
        return sinkou, messages

    def calc_magic_invasion_points(self) -> Tuple[int, List[str]]:
        """
        魔王魔力侵攻 (INV_TYPE == 1)
        使用魔王气力计算，气力减半
        返回 (侵攻点, 消息列表)
        """
        messages = []
        v = self._vars()

        # BASE:0:1 = 魔王气力
        mao_ki = v.chars[0].base.get(1, 0) if len(v.chars) > 0 else 0
        sinkou = mao_ki // 25

        # 气力减半
        if len(v.chars) > 0:
            v.chars[0].base[1] = mao_ki // 2

        # 威望值补正
        sinkou, fame_msgs = self._apply_fame_modifier(sinkou)
        messages.extend(fame_msgs)

        messages.append(f"战斗力　{sinkou}点")
        return sinkou, messages

    def calc_hero_invasion_points(self, hero_idx: int) -> Tuple[int, List[str]]:
        """
        勇者侵攻 (INV_TYPE == 2)
        派遣勇者带三分之一的怪物去进攻
        返回 (侵攻点, 消息列表)
        """
        messages = []
        sinkou = 0
        v = self._vars()

        for mon_id in range(100, 190):
            item_count = v.get_item(mon_id, 0)
            if item_count < 1:
                continue

            mon_atk = 0
            e_data = self._get_monster_data(mon_id, hero_idx=hero_idx)

            mon_atk += e_data.get(2, 0)
            mon_atk += e_data.get(3, 0)
            mon_atk += e_data.get(4, 0)

            if e_data.get(5, 0) != 0:
                mon_atk += e_data.get(1, 0)
            if e_data.get(6, 0) != 0:
                mon_atk += e_data.get(1, 0)

            # 怪物数量减少1/3
            v.set_item(mon_id, item_count // 3)
            sinkou += mon_atk * ((item_count // 9) + 1)
            # 恢复2/3
            v.set_item(mon_id, item_count * 2 // 3)

        # 最大约12万的1/20
        sinkou //= 20
        messages.append(f"怪物的战斗力　{sinkou}点")

        # 勇者补正
        hero_bonus = v.chars[hero_idx].cflag.get(9, 0) + 100 if hero_idx < len(v.chars) else 100
        messages.append(f"勇者补正　x{hero_bonus / 100:.2f}")
        sinkou = sinkou * hero_bonus // 100

        # 勋章补正
        medal_mult = self.calc_medal_bonus(hero_idx)
        sinkou = sinkou * medal_mult // 100

        return sinkou, messages

    def calc_plunder_invasion_points(self, hero_idx: int) -> Tuple[int, List[str]]:
        """
        掠夺侵攻 (INV_TYPE == 3)
        派遣勇者前去掠夺资金
        返回 (侵攻点, 消息列表)
        """
        messages = []
        v = self._vars()

        # 使用魔王气力
        mao_ki = v.chars[0].base.get(1, 0) if len(v.chars) > 0 else 0
        sinkou = mao_ki // 25

        # 气力减半
        if len(v.chars) > 0:
            v.chars[0].base[1] = mao_ki // 2

        messages.append(f"魔王的力量　{sinkou}点")

        # 勇者补正
        hero_bonus = v.chars[hero_idx].cflag.get(9, 0) + 100 if hero_idx < len(v.chars) else 100
        messages.append(f"勇者补正　x{hero_bonus / 100:.2f}")
        sinkou = sinkou * hero_bonus // 100

        # 勋章补正
        medal_mult = self.calc_medal_bonus(hero_idx)
        sinkou = sinkou * medal_mult // 100

        return sinkou, messages

    # ---- 共通补正 ----

    def _apply_fame_modifier(self, sinkou: int) -> Tuple[int, List[str]]:
        """威望值补正 - 对应 ERB INVASION.ERB 中的威望值 MOD"""
        messages = []
        fame = self.get_ex_flag(EX_FLAG_FAME)

        if fame <= 20:
            messages.append("威望值是【岌岌可危】")
            messages.append("侵攻失败")
            return 0, messages
        elif fame <= 40:
            messages.append("威望值是【动荡不安】")
            messages.append("侵攻战斗力减少")
            sinkou //= 4
        elif fame <= 60:
            messages.append("威望值是【略受质疑】")
            temp = fame - 60
            sinkou = sinkou * (100 + temp * 2) // 100
        elif fame <= 80:
            messages.append("威望值是【相安无事】")
        elif fame <= 100:
            messages.append("威望值是【广受爱戴】")
            temp = fame - 80
            sinkou = sinkou * (100 + temp) // 100

        return sinkou, messages

    def apply_common_bonuses(self, sinkou: int) -> Tuple[int, List[str]]:
        """
        共通补正处理 - 魔王补正、知识补正、勋章补正
        对应 ERB INVASION.ERB 共通処理部分
        """
        messages = []
        v = self._vars()

        # 魔王补正
        mao_bonus = v.chars[0].cflag.get(9, 0) + 100 if len(v.chars) > 0 else 100
        messages.append(f"魔王补正　　　x{mao_bonus / 100:.2f}")
        sinkou = sinkou * mao_bonus // 100

        # 魔界知识补正 (TALENT:0:325)
        if len(v.chars) > 0 and v.chars[0].talent.get(325, 0) == 1:
            messages.append("魔界知识补正　x1.50")
            sinkou = sinkou * 150 // 100

        # 淫魔知识补正 (TALENT:0:327)
        if len(v.chars) > 0 and v.chars[0].talent.get(327, 0) == 1:
            messages.append("淫魔知识补正　x1.20")
            sinkou = sinkou * 120 // 100

        # 魔虫知识补正 (TALENT:0:328)
        if len(v.chars) > 0 and v.chars[0].talent.get(328, 0) == 1:
            messages.append("魔虫知识补正　x1.10")
            sinkou = sinkou * 110 // 100

        # 魔王勋章补正
        medal_mult = self.calc_medal_bonus(0)
        sinkou = sinkou * medal_mult // 100

        messages.append(f"合计　{sinkou}点")
        return sinkou, messages

    def calc_medal_bonus(self, char_idx: int) -> int:
        """
        勋章补正计算 - 对应 @MEDAL_BONUS
        返回百分比乘数 (100=1.00x, 160=1.60x)
        """
        v = self._vars()
        if char_idx >= len(v.chars):
            return 100

        medal_exp = v.chars[char_idx].exp.get(81, 0)

        if medal_exp > 500:
            return 160
        elif medal_exp > 250:
            return 150
        elif medal_exp > 150:
            return 140
        elif medal_exp > 100:
            return 130
        elif medal_exp > 60:
            return 120
        elif medal_exp > 40:
            return 110
        elif medal_exp > 30:
            return 105
        elif medal_exp > 20:
            return 104
        elif medal_exp > 15:
            return 103
        elif medal_exp > 10:
            return 102
        elif medal_exp > 5:
            return 101
        return 100

    # ---- 侵攻结果处理 ----

    def apply_invasion_result(self, area_flag: int, sindo_flag: int,
                              inv_type: int, sinkou: int,
                              hero_idx: int = 0,
                              is_ex_flag: bool = False) -> Tuple[int, List[str]]:
        """
        侵攻结果共通处理 - 对应 ERB INVASION.ERB 侵攻結果共通
        返回 (新的侵攻度, 消息列表)
        """
        messages = []
        v = self._vars()

        # 掠夺侵攻力激减
        if inv_type == INV_TYPE_PLUNDER:
            new_progress = self._add_to_area(area_flag, sinkou // 20, is_ex_flag)
        else:
            new_progress = self._add_to_area(area_flag, sinkou, is_ex_flag)

        # 上限10000
        if new_progress > 10000:
            new_progress = 10000
            self._set_area(area_flag, 10000, is_ex_flag)

        sindo_val = self.get_ex_flag(sindo_flag, 0) if is_ex_flag else self.get_flag(sindo_flag, 0)

        # 根据侵攻类型处理奖励
        if inv_type == INV_TYPE_MONSTER:
            self._apply_monster_rewards(area_flag, sindo_flag, sindo_val, sinkou, is_ex_flag, messages)
        elif inv_type == INV_TYPE_MAGIC:
            self._apply_magic_rewards(area_flag, sindo_flag, sindo_val, sinkou, is_ex_flag, messages)
        elif inv_type == INV_TYPE_HERO:
            self._apply_hero_rewards(area_flag, sindo_flag, sindo_val, sinkou, hero_idx, is_ex_flag, messages)
        elif inv_type == INV_TYPE_PLUNDER:
            self._apply_plunder_rewards(area_flag, sindo_flag, sindo_val, sinkou, hero_idx, is_ex_flag, messages)

        # 声望+2
        self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 2)

        return new_progress, messages

    def _apply_monster_rewards(self, area_flag, sindo_flag, sindo_val, sinkou, is_ex_flag, messages):
        """怪物侵攻奖励 - 资金+俘虏"""
        v = self._vars()
        sinkou = min(sinkou, 10000 * 10)

        if sindo_val:
            messages.append(f"强制征收了{sinkou * 10}点！")
        else:
            messages.append(f"得到了{sinkou * 10}点的战利品！")

        v.money = v.money + sinkou * 10
        self.set_ex_flag(4444, self.get_ex_flag(4444) + sinkou * 10)

        # 5%概率捕获勇者
        if random.randint(0, 99) < 5:
            messages.append("好像抓到了负隅顽抗的勇者…………")
            # CALL GET_ENEMY
            captured_idx, enemy_msgs = self._hero_generator.get_enemy()
            messages.extend(enemy_msgs)
            if captured_idx is not None and captured_idx >= 0:
                messages.append(f"捕获了新的角色！")

    def _apply_magic_rewards(self, area_flag, sindo_flag, sindo_val, sinkou, is_ex_flag, messages):
        """魔力侵攻奖励 - 经验值"""
        v = self._vars()
        mao_name = v.chars[0].savestr if len(v.chars) > 0 else "魔王"

        # 魔力描述
        if sinkou < 100:
            messages.append(f"{sinkou}点魔力形成飓风，将大树吹倒了！")
        elif sinkou < 300:
            messages.append(f"{sinkou}点魔力形成火焰，将平原焚烧殆尽！")
        elif sinkou < 600:
            messages.append(f"{sinkou}点魔力形成雷霆，将附近的村庄彻底摧毁！")
        elif sinkou < 900:
            messages.append(f"{sinkou}点魔力形成洪水，将城镇淹没！")
        elif sinkou < 1200:
            messages.append(f"{sinkou}点魔力形成剧毒气体，令骑士团窒息！")
        else:
            messages.append(f"{sinkou}点魔力形成纯粹能量，将城市呑没！")

        sinkou = min(sinkou, 10000 * 10)
        exp_gain = sinkou // 2
        messages.append(f"{mao_name}得到了{exp_gain}点经验值！")
        if len(v.chars) > 0:
            v.chars[0].exp[80] = v.chars[0].exp.get(80, 0) + exp_gain

    def _apply_hero_rewards(self, area_flag, sindo_flag, sindo_val, sinkou, hero_idx, is_ex_flag, messages):
        """勇者侵攻奖励 - 资金+经验值+俘虏"""
        v = self._vars()
        if hero_idx >= len(v.chars):
            return

        hero = v.chars[hero_idx]
        hero_name = hero.savestr
        mao_name = v.chars[0].savestr if len(v.chars) > 0 else "魔王"

        # 善良值变化
        messages.append(f"{hero_name}带着怪物到达了，尽可能地施暴着。（善良值:-50）")

        # 性格相关文本
        if hero.talent.get(160, 0):  # 慈爱
            messages.append(f"{hero_name}在侵略的时候依旧全程保持着慈爱的笑容，她终于明白到一切都是为了{mao_name}而存在的………")
        elif hero.talent.get(161, 0):  # 自信家
            messages.append(f"{hero_name}身先士卒，第一个飞跳入战场里，而且最后毫发无损。")
        elif hero.talent.get(162, 0):  # 懦弱
            messages.append(f"{hero_name}是优秀的指挥官，带领着怪物们侵略了。")
        elif hero.talent.get(163, 0):  # 高贵
            messages.append(f"{hero_name}穿着{mao_name}赐予的被诅咒的铠甲，高声大笑着率领怪物们突击了………")
        elif hero.talent.get(164, 0):  # 冷静
            messages.append(f"{hero_name}冷哼着耻笑跪求饶命的草民，随手将他们交给饥饿的巨兽了。")
        elif hero.talent.get(165, 0):  # 村娘
            messages.append(f"{hero_name}一边发出异样的笑声，一边用手中的火把将四周都点燃了………")
        elif hero.talent.get(166, 0):  # 恶女
            messages.append(f"{hero_name}把侵略时所抢夺的金银财宝都献给了{mao_name}………")

        sinkou = min(sinkou, 10000 * 10)
        if sindo_val:
            messages.append(f"强制征收了{sinkou * 5}点！")
        else:
            messages.append(f"得到了{sinkou * 5}点的战利品！")

        v.money = v.money + sinkou * 5
        self.set_ex_flag(4444, self.get_ex_flag(4444) + sinkou * 5)

        exp_gain = sinkou // 2
        hero.exp[80] = hero.exp.get(80, 0) + exp_gain
        messages.append(f"{hero_name}获得了{exp_gain}点经验值！")

        # 9%概率捕获勇者
        if random.randint(0, 99) < 9:
            messages.append("好像抓到了负隅顽抗的勇者…………")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 1)
            # CALL GET_ENEMY
            captured_idx, enemy_msgs = self._hero_generator.get_enemy()
            messages.extend(enemy_msgs)
            if captured_idx is not None and captured_idx >= 0:
                messages.append(f"捕获了新的角色！")

    def _apply_plunder_rewards(self, area_flag, sindo_flag, sindo_val, sinkou, hero_idx, is_ex_flag, messages):
        """掠夺奖励 - 直接资金"""
        v = self._vars()
        if hero_idx >= len(v.chars):
            return

        hero = v.chars[hero_idx]
        hero_name = hero.savestr

        sinkou = min(sinkou, 10000 * 10)
        if sindo_val:
            messages.append(f"强行征收到了{sinkou}点！")
        else:
            messages.append(f"获得了{sinkou}点的战利品！")

        v.money = v.money + sinkou
        self.set_ex_flag(4444, self.get_ex_flag(4444) + sinkou)

        exp_gain = sinkou // 20
        hero.exp[80] = hero.exp.get(80, 0) + exp_gain
        messages.append(f"{hero_name}获得了{exp_gain}点经验值！")

    # ---- INVASION_CHECK ----

    def invasion_check(self) -> List[str]:
        """
        侵攻度检查 - 对应 @INVASION_CHECK
        当侵攻度达到10000且未征服时触发征服事件
        """
        messages = []

        # 人间界
        if self.get_flag(FLAG_AREA_HUMAN) >= 10000 and self.get_flag(FLAG_SINDO_HUMAN) == 0:
            messages.append("ENDING_1: 人间界征服")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 10)
            messages.append("声望+10")

        # 精灵领域
        if self.get_flag(FLAG_AREA_ELF) >= 10000 and self.get_flag(FLAG_SINDO_ELF) == 0:
            messages.append("ENDING_3: 精灵领域征服")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 10)
            messages.append("声望+10")

        # 龙之山脉
        if self.get_flag(FLAG_AREA_DRAGON) >= 10000 and self.get_flag(FLAG_SINDO_DRAGON) == 0:
            messages.append("ENDING_4: 龙之山脉征服")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 10)
            messages.append("声望+10")

        # 天界
        if self.get_flag(FLAG_AREA_HEAVEN) >= 10000 and self.get_flag(FLAG_SINDO_HEAVEN) == 0:
            messages.append("ENDING_5: 天界征服")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 10)
            messages.append("声望+10")

        # 天神宫
        if self.get_ex_flag(EX_FLAG_AREA_PALACE) >= 10000 and self.get_ex_flag(EX_FLAG_SINDO_PALACE) == 0:
            messages.append("END10_55: 天神宫征服")
            self.set_ex_flag(EX_FLAG_FAME, self.get_ex_flag(EX_FLAG_FAME) + 10)
            messages.append("声望+10")

        return messages

    # ---- 水晶球系统 ----

    def sengen_video_deploy(self, count: int, use_merchant: bool = False) -> Tuple[int, List[str]]:
        """
        投放水晶球 - 对应 @SENGEN_VIDEO / @SENGEN_VIDEO_BONUS
        返回 (实际投放数, 消息列表)
        """
        messages = []
        stock = self.get_ex_flag(EX_FLAG_VIDEO_TOTAL) - self.get_ex_flag(EX_FLAG_VIDEO_DEPLOYED)

        if count > stock:
            messages.append("超出数量，请重新输入")
            return 0, messages

        # 增加已投放数
        self.set_ex_flag(EX_FLAG_VIDEO_DEPLOYED, self.get_ex_flag(EX_FLAG_VIDEO_DEPLOYED) + count)

        # 计算实际效果
        result = count
        if use_merchant:
            # 商人模式加成
            result = int(result * 1.10)
            if random.randint(0, 1) == 0:
                result = int(result * 1.20)
            if random.randint(0, 2) == 0:
                result = int(result * 1.20)
            if random.randint(0, 3) == 0:
                result = int(result * 1.20)

        # 通用随机加成
        if random.randint(0, 1) == 0:
            result = int(result * 1.20)
        if random.randint(0, 2) == 0:
            result = int(result * 0.80)

        if result > count and use_merchant:
            messages.append("奸商们制作更多的版本提升了投放效果。")
        if use_merchant and result <= count:
            result = count
        if result > count and not use_merchant:
            messages.append("在投放过程中似乎传出了不同的版本，投放效果提升了。")
        if result < count:
            messages.append("似乎有些水晶球投放不是太成功。")

        if result >= 1:
            messages.append(f"成功投放{result}部水晶球")
            self.set_ex_flag(EX_FLAG_VIDEO_POPULAR, self.get_ex_flag(EX_FLAG_VIDEO_POPULAR) + result)
            self.set_ex_flag(EX_FLAG_VIDEO_DAYS, self.get_ex_flag(EX_FLAG_VIDEO_DAYS) + result)
        else:
            messages.append("投放，似乎失败了。")

        return result, messages

    def sengen_video_decay(self) -> List[str]:
        """
        水晶球流行衰减 - 对应 @SENGEN_VIDEO_DE
        每日调用
        """
        messages = []
        days = self.get_ex_flag(EX_FLAG_VIDEO_DAYS)
        popular = self.get_ex_flag(EX_FLAG_VIDEO_POPULAR)

        days -= 1
        if random.randint(0, 2) != 0:
            popular -= 1

        if days <= 0:
            days = 0
            popular = 0
        if popular <= 0:
            days = 0
            popular = 0

        self.set_ex_flag(EX_FLAG_VIDEO_DAYS, days)
        self.set_ex_flag(EX_FLAG_VIDEO_POPULAR, popular)
        return messages

    # ---- 辅助方法 ----

    def _get_monster_data(self, mon_id: int, hero_idx: int = 0) -> Dict[int, int]:
        """获取怪物数据 - 对接 SUMMON_MONSTER.ERB"""
        from ..systems.dungeon import DungeonSystem
        dungeon = DungeonSystem(self.engine)
        data = dungeon.get_monster_data(mon_id)
        if data:
            return data
        return {1: 10, 2: 10, 3: 10, 4: 10, 5: 0, 6: 0}

    def _add_to_area(self, area_flag: int, value: int, is_ex_flag: bool = False) -> int:
        """增加侵攻度"""
        if is_ex_flag:
            current = self.get_ex_flag(area_flag)
            new_val = current + value
            self.set_ex_flag(area_flag, new_val)
            return new_val
        else:
            current = self.get_flag(area_flag)
            new_val = current + value
            self.set_flag(area_flag, new_val)
            return new_val

    def _set_area(self, area_flag: int, value: int, is_ex_flag: bool = False):
        """设置侵攻度"""
        if is_ex_flag:
            self.set_ex_flag(area_flag, value)
        else:
            self.set_flag(area_flag, value)

    def get_total_monster_count(self) -> int:
        """获取怪物总数"""
        v = self._vars()
        total = 0
        for mon_id in range(100, 190):
            total += v.get_item(mon_id, 0)
        return total

    def get_eligible_heroes_for_invasion(self) -> List[int]:
        """获取可用于侵攻的勇者列表 (INV_TYPE == 2)"""
        v = self._vars()
        heroes = []
        for i, char in enumerate(v.chars):
            if i == 0:
                continue  # 排除魔王
            if char.base.get(0, 0) < 1:
                continue  # HP > 0
            if char.cflag.get(0, 0) != 2:
                continue  # 可助手
            if char.cflag.get(1, 0) not in (0, 7):
                continue  # 非调教中/苗床
            if not (char.talent.get(85, 0) == 1 or char.talent.get(76, 0) == 1):
                continue  # 爱慕或淫乱
            if char.talent.get(153, 0) == 1 and not (self.get_flag(5) & (1 << 10)):
                continue  # 妊娠中
            heroes.append(i)
        return heroes

    def get_eligible_heroes_for_plunder(self) -> List[int]:
        """获取可用于掠夺的勇者列表 (INV_TYPE == 3)"""
        v = self._vars()
        heroes = []
        for i, char in enumerate(v.chars):
            if i == 0:
                continue
            if char.base.get(0, 0) < 1:
                continue
            if char.cflag.get(1, 0) != 0:
                continue
            if char.cflag.get(0, 0) == 0 and char.talent.get(254, 0) == 0:
                continue
            if char.talent.get(153, 0) == 1 and not (self.get_flag(5) & (1 << 10)):
                continue
            heroes.append(i)
        return heroes


# ============================================================
# InvasionEventManager - 据点事件 + 侵略中途事件
# 对应 @KYOTEN_EVENT, @INVASION_EVENT_SEIEI, @INVASION_EVENT_FORT, @INVASION_EVENT_CHALLENGE
# ============================================================

class InvasionEventManager:
    """侵略事件管理器 - 处理各区域的侵略进度事件和侵略中途事件"""

    def __init__(self, game_engine):
        self.engine = game_engine
        self._invasion_mgr = InvasionManager(game_engine)

    def _vars(self):
        return self.engine.interpreter.vars

    def get_flag(self, idx, default=0):
        return int(self._vars().get_flag(idx, default))

    def set_flag(self, idx, value):
        self._vars().set_flag(idx, value)

    # ---- 据点事件 (KYOTEN_EVENT) ----

    def check_invasion_events(self) -> List[str]:
        """检查所有区域的侵略事件"""
        messages = []
        messages.extend(self._check_kyoten_event(AREA_HUMAN))
        messages.extend(self._check_kyoten_event(AREA_ELF))
        messages.extend(self._check_kyoten_event(AREA_DRAGON))
        messages.extend(self._check_kyoten_event(AREA_HEAVEN))
        return messages

    def _check_kyoten_event(self, area_id: int) -> List[str]:
        """
        据点事件检查 - 对应 @KYOTEN_EVENT
        侵攻度2000/4000/6000/8000/10000触发事件，一次のみ
        """
        messages = []

        # 获取对应 FLAG 编号
        area_flag, event_flag = self._get_area_and_event_flags(area_id)
        if area_flag is None:
            return messages

        progress = self.get_flag(area_flag)
        stage = self.get_flag(event_flag)

        event_data = KYOTEN_EVENT_TEXT.get(area_id)
        if event_data is None:
            return messages

        # 精灵领域需要检查征服状态
        if area_id == AREA_ELF and self.get_flag(FLAG_SINDO_ELF) != 0:
            return messages

        # 进攻事件
        for threshold_idx, threshold in enumerate(THRESHOLDS):
            if progress >= threshold and stage == threshold_idx:
                event_name = event_data["advance"].get(threshold_idx, "")
                messages.append(self._format_kyoten_event(event_name))
                self.set_flag(event_flag, threshold_idx + 1)
                break

        # 夺回事件
        if not messages:
            retreat_thresholds = event_data.get("retreat_thresholds", {})
            for stage_key, retreat_threshold in retreat_thresholds.items():
                if progress <= retreat_threshold and stage == stage_key:
                    event_name = event_data["retreat"].get(stage_key, "")
                    messages.append(self._format_kyoten_event(event_name))
                    self.set_flag(event_flag, stage_key - 1)
                    break

        return messages

    def _get_area_and_event_flags(self, area_id: int) -> Tuple[Optional[int], Optional[int]]:
        """获取区域对应的侵攻度FLAG和事件阶段FLAG"""
        mapping = {
            AREA_HUMAN: (FLAG_AREA_HUMAN, FLAG_EVENT_HUMAN),
            AREA_ELF: (FLAG_AREA_ELF, FLAG_EVENT_ELF),
            AREA_DRAGON: (FLAG_AREA_DRAGON, FLAG_EVENT_DRAGON),
            AREA_HEAVEN: (FLAG_AREA_HEAVEN, FLAG_EVENT_HEAVEN),
        }
        return mapping.get(area_id, (None, None))

    def _format_kyoten_event(self, event_name: str) -> str:
        """格式化据点事件消息 - 匹配 ERB 原始格式"""
        border = "*" * 91
        padding = "　"  # 全角空格
        # 匹配 ERB 原始格式: 91个*的边框 + 全角空格居中
        center_text = f"{padding * 15}{event_name}{padding * 15}"
        lines = [
            border,
            border,
            f"*********{center_text}**********",
            border,
            border,
        ]
        return "\n".join(lines)

    # ---- 侵略中途事件 ----

    def invasion_event(self, area_flag: int, sindo_flag: int,
                       inv_type: int, sinkou: int,
                       hero_idx: int = 0) -> Tuple[int, List[str]]:
        """
        侵略中途事件入口 - 对应 @INVASION_EVENT
        返回 (0=继续侵攻, 1=侵攻中止), 消息列表
        """
        roll = random.randint(0, 9)

        if roll == 9:
            return self.invasion_event_fort(area_flag, sindo_flag, inv_type, sinkou, hero_idx)
        elif roll == 8:
            return self.invasion_event_challenge(area_flag, sindo_flag, inv_type, sinkou, hero_idx)

        return self.invasion_event_seiei(area_flag, sindo_flag, inv_type, sinkou, hero_idx)

    def invasion_event_seiei(self, area_flag: int, sindo_flag: int,
                             inv_type: int, sinkou: int,
                             hero_idx: int = 0) -> Tuple[int, List[str]]:
        """
        精英部队战斗事件 - 对应 @INVASION_EVENT_SEIEI
        返回 (0=继续, 1=中止), 消息列表
        """
        messages = []
        sindo_val = self.get_flag(sindo_flag)

        if sindo_val != 0:
            return -1, messages

        progress = self.get_flag(area_flag)

        # 精锐部队情报
        if progress == 0 and sindo_val == 0:
            messages.append("根据传闻狂王为了应对魔王军的入侵已开始组织起了精锐部队。")
        elif 1 <= progress < 5000 and sindo_val == 0 and inv_type != INV_TYPE_MAGIC:
            messages.append("狂王组织的精锐部队似乎已经开始行动了。")
            messages.append("如果不尽快采取行动的话………")
        elif 1 <= progress < 10000 and sindo_val == 0 and inv_type != INV_TYPE_MAGIC:
            messages.append("根据斥候打探的消息，狂王的精锐部队似乎已经在前方的城镇中布下了防线。")
            messages.append("而且精锐部队的真正目的是要捕捉魔王麾下的勇者………")

        if inv_type != INV_TYPE_HERO:
            return -1, messages

        # 精锐部队战斗
        if progress >= 5000 and sindo_val == 0 and inv_type == INV_TYPE_HERO:
            local_roll = random.randint(0, progress - 1)
            if local_roll > 2000:
                messages.append("………")
                messages.append("……")
                messages.append("…")
                messages.append("精锐部队出现了！")

                # 简化的战斗模拟
                result, battle_msgs = self._simulate_seiei_battle(
                    area_flag, sinkou, hero_idx
                )
                messages.extend(battle_msgs)
                return result, messages

        # 精锐部队未出现
        messages.append("………")
        messages.append("……")
        messages.append("…")
        messages.append("传闻中的精锐部队并没有出现…………")

        return 0, messages

    def _simulate_seiei_battle(self, area_flag: int, sinkou: int,
                               hero_idx: int) -> Tuple[int, List[str]]:
        """
        精锐部队战斗模拟 - 对应 INVASION_EVENT_SEIEI 中的战斗逻辑
        简化版本，返回 (0=胜利继续, 1=败北中止)
        """
        messages = []
        v = self._vars()

        if hero_idx >= len(v.chars):
            return 0, messages

        hero = v.chars[hero_idx]
        hero_name = hero.savestr

        # 精锐部队类型随机
        if random.randint(0, 1) == 0:
            seiei_type = "防御型"  # 防御型: HP/MP 9000, 攻150 防200
            seiei_hp = 9000
            seiei_mp = 9000
            seiei_atk = 150
            seiei_def = 200
        else:
            seiei_type = "攻击型"  # 攻击型: HP/MP 7500, 攻200 防150
            seiei_hp = 7500
            seiei_mp = 7500
            seiei_atk = 200
            seiei_def = 150

        # 勇者基础等级补正
        hero_level_bonus = self.get_flag(FLAG_HERO_LEVEL)
        seiei_hp += 10 * hero_level_bonus
        seiei_mp += 10 * hero_level_bonus
        seiei_atk += hero_level_bonus
        seiei_def += hero_level_bonus

        # 勇者属性 + 侵攻点补正
        hero_hp = hero.base.get(0, 1000) + sinkou
        hero_mp = hero.base.get(1, 1000) + sinkou
        hero_atk = hero.cflag.get(11, 100)
        hero_def = hero.cflag.get(12, 100)

        messages.append(f"你的勇者{hero_name}率领着魔王军和精锐部队展开了战斗！")
        messages.append("（怪物的战斗力将被添加到攻击力和体力和气力上）")

        # 20回合战斗
        for turn in range(21):
            if turn > 19:
                messages.append("没有时间了，战线已经不可能再维持下去了！")
                messages.append(f"{hero_name}的部队开始了后退，怪物们在后退中溃散着。")
                messages.append("最终活着回来的怪物不到十只………")
                exp_gain = sinkou // 10
                hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                return 1, messages

            # 魔王军先制攻击
            hero_total_atk = hero_atk * (sinkou // 1024 + 1)
            if seiei_def < hero_total_atk:
                if random.randint(0, 4) == 0:  # 会心一击
                    damage = (hero_total_atk - seiei_def) * 4
                    messages.append("迅猛的一击！")
                else:
                    damage = (hero_total_atk - seiei_def) * 2
                seiei_hp -= damage
                seiei_mp -= damage
                seiei_def //= 2
                messages.append(f"{hero_name}率领魔王军的攻击使精锐部队受到了{damage}点伤害！")
            else:
                messages.append(f"精锐部队承受着{hero_name}的攻击。")
                seiei_def //= 2

            # 精锐部队死亡判定
            if seiei_hp <= 0 or seiei_hp <= 100 or seiei_mp <= 0:
                messages.append(f"精锐部队被{hero_name}率领的魔王军消灭了………")
                exp_gain = sinkou // 5
                hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                return 0, messages

            # 精锐部队攻击
            if hero_def < seiei_atk:
                damage = (seiei_atk - hero_def) * 5
                hero_hp -= damage
                hero_mp -= damage
                hero_def = hero_def * 2 // 3
                messages.append(f"精锐部队发起进攻使{hero_name}率领的魔王军受到了{damage}点伤害！")
            else:
                messages.append(f"{hero_name}率领的魔王军承受着精锐部队的攻击。")
                hero_def = hero_def * 2 // 3

            # 魔王军死亡判定
            if hero_hp <= 0 or hero_hp <= 300 or hero_mp <= 0:
                if hero_hp <= 0:
                    messages.append(f"魔王军被精锐部队消灭了，{hero_name}孤身逃了回来…………")
                elif hero_mp <= 0:
                    messages.append(f"被精锐部队包围的魔王军失去战斗的意志投降了………")
                hero.cflag[1] = 0
                return 1, messages

        return 0, messages

    def invasion_event_fort(self, area_flag: int, sindo_flag: int,
                            inv_type: int, sinkou: int,
                            hero_idx: int = 0) -> Tuple[int, List[str]]:
        """
        要塞攻略事件 - 对应 @INVASION_EVENT_FORT
        3个选择: 强攻/潜入/绕路
        返回 (0=继续, 1=中止), 消息列表
        """
        messages = []
        sindo_val = self.get_flag(sindo_flag)

        # 条件检查: 已征服或非怪物/勇者/掠夺类型不触发
        if sindo_val:
            return -1, messages
        if inv_type not in (INV_TYPE_MONSTER, INV_TYPE_HERO, INV_TYPE_PLUNDER):
            return -1, messages

        # 区域名称设定
        area_names = self._get_fort_area_names(area_flag)
        if area_names is None:
            return -1, messages

        area_name, army_name, fort_name = area_names

        # 根据侵攻类型显示选择
        # 这里简化为自动选择（因为Python版本暂无交互输入）
        if inv_type == INV_TYPE_HERO:
            choice = random.choice([1, 2, 3])  # 强攻/潜入/绕路
        elif inv_type == INV_TYPE_PLUNDER:
            choice = random.choice([2, 3])  # 潜入/绕路 (映射为2/3)
        else:  # INV_TYPE_MONSTER
            choice = 1  # 强攻

        # 处理选择结果
        return self._process_fort_choice(choice, inv_type, sinkou, hero_idx,
                                          area_name, army_name, fort_name)

    def _get_fort_area_names(self, area_flag: int) -> Optional[Tuple[str, str, str]]:
        """获取要塞事件的区域名称"""
        names = {
            FLAG_AREA_HUMAN: ("人间界", "人类军队", "城堡"),
            FLAG_AREA_ELF: ("精灵森林", "精灵族战士", "精灵城寨"),
            FLAG_AREA_DRAGON: ("龙之山脉", "龙族战士", "战争堡垒"),
            FLAG_AREA_HEAVEN: ("天界", "天界卫队", "天使要塞"),
        }
        return names.get(area_flag)

    def _process_fort_choice(self, choice: int, inv_type: int, sinkou: int,
                             hero_idx: int, area_name: str, army_name: str,
                             fort_name: str) -> Tuple[int, List[str]]:
        """处理要塞选择结果"""
        messages = []
        v = self._vars()
        hero = v.chars[hero_idx] if hero_idx < len(v.chars) else None
        hero_name = hero.savestr if hero else "勇者"

        if choice == 1:  # 强攻
            roll = random.randint(0, 9)
            if roll >= 6:  # 成功 40%
                messages.append(f"魔王军向着{fort_name}发起了最为猛烈的进攻，在付出较小的代价后攻破了{fort_name}的一角。")
                messages.append(f"获胜的魔王军高呼万岁，继续向{area_name}进发。")
                if inv_type == INV_TYPE_HERO and hero:
                    exp_gain = sinkou // 5
                    hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                    messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                messages.append("怪物数量减少了10%")
                sinkou = sinkou * 9 // 10
                return 0, messages
            elif roll >= 2:  # 惨胜 40%
                messages.append(f"魔王军向着{fort_name}发起了最为猛烈的进攻。")
                messages.append(f"{fort_name}的防御极其坚固，{army_name}凭借着掩体不断地攻击，让魔王军损失惨重。")
                if inv_type == INV_TYPE_HERO and hero:
                    messages.append(f"{hero_name}不得不亲自上阵，这才逆转了局面，攻下了{fort_name}。")
                    exp_gain = sinkou // 5
                    hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                    messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                    hero.base[0] = hero.base.get(0, 1000) // 2
                    messages.append(f"{hero_name}的体力减少了一半！")
                messages.append("怪物数量减少了50%")
                sinkou = sinkou // 2
                return 0, messages
            else:  # 惨败 20%
                messages.append(f"魔王军向着{fort_name}发起了最为猛烈的进攻。")
                messages.append(f"{fort_name}的防御极其坚固，令魔王军久攻不下，陷入僵局。")
                messages.append(f"打破僵局的是一支突然出现在魔王军背后的{army_name}援军。")
                messages.append(f"腹背受敌的魔王军一触即溃，随即被里应外合的两支军队尽数歼灭。")
                if inv_type == INV_TYPE_HERO and hero:
                    messages.append(f"率领魔王军的{hero_name}孤身一人逃了回来。")
                    hero.base[0] = hero.base.get(0, 1000) * 3 // 10
                    messages.append(f"{hero_name}的体力减少了70%！")
                    hero.cflag[1] = 0
                messages.append("侵攻中止。")
                return 1, messages

        elif choice == 2:  # 潜入
            roll = random.randint(0, 9)
            # 有天使/恶魔翼则100%成功
            has_wings = hero and (hero.talent.get("恶魔翅膀", 0) or
                                  hero.talent.get("种族", 0) == 6 or
                                  hero.talent.get("种族", 0) == 8) if hero else False

            if has_wings:
                messages.append(f"{hero_name}趁着夜色从空中潜入了{fort_name}，在躲过多支巡逻队后终于打开了{fort_name}的大门。")
                messages.append(f"获胜的魔王军高呼万岁，继续向{area_name}进发。")
                if inv_type == INV_TYPE_HERO and hero:
                    exp_gain = sinkou // 5
                    hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                    messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                self.set_flag(83, self.get_flag(83) + 5)
                messages.append("人间牧场肉便器数量+5。")
                return 0, messages
            elif roll >= 5:  # 潜入成功 50%
                messages.append(f"{hero_name}乔装打扮成功混进了{fort_name}里。")
                messages.append(f"当天夜里，{hero_name}杀死了大门的守卫，将等候多时的魔王军引入{fort_name}内。")
                messages.append(f"获胜的魔王军高呼万岁，继续向{area_name}进发。")
                if inv_type == INV_TYPE_HERO and hero:
                    exp_gain = sinkou // 5
                    hero.exp[80] = hero.exp.get(80, 0) + exp_gain
                    messages.append(f"{hero_name}获得了{exp_gain}点经验值！")
                self.set_flag(83, self.get_flag(83) + 5)
                messages.append("人间牧场肉便器数量+5。")
                return 0, messages
            elif roll >= 2:  # 失败逃窜 30%
                messages.append(f"{hero_name}乔装打扮试图混进{fort_name}里，但被大门的守卫识破。")
                messages.append(f"{hero_name}杀出一条血路，勉强逃回了魔王军。")
                messages.append(f"魔王军不得已只好发动强攻，在鏖战后最终惨胜。")
                if hero:
                    hero.base[0] = 1
                    messages.append(f"{hero_name}的体力归零")
                sinkou = sinkou * 7 // 10
                messages.append("怪物数量减少了30%")
                return 0, messages
            else:  # 失败被捕 20%
                messages.append(f"{hero_name}乔装打扮试图混进{fort_name}里，但却被大门的守卫识破。")
                messages.append(f"在一番激烈战斗后{hero_name}还是被{army_name}生擒。")
                messages.append(f"失去指挥官的魔王军随即被出城迎击的{army_name}击溃。")
                messages.append(f"{hero_name}被俘虏，侵攻中止。")
                if hero:
                    hero.cflag[1] = 9
                return 1, messages

        elif choice == 3:  # 绕路
            roll = random.randint(0, 9)
            if roll > 0:  # 平安到达 90%
                messages.append(f"魔王军绕开{fort_name}向{area_name}进发，因为路途遥远地形复杂损失了一些人马。")
                sinkou = sinkou * 9 // 10
                messages.append("怪物数量减少了10%")
                return 0, messages
            else:  # 被埋伏 10%
                messages.append(f"魔王军绕开{fort_name}向{area_name}进发，但却遇到了埋伏。")
                messages.append(f"在一番血战后，魔王军击退了伏军继续向{area_name}进发。")
                sinkou = sinkou // 2
                messages.append("怪物数量减少了50%")
                return 0, messages

        return 0, messages

    def invasion_event_challenge(self, area_flag: int, sindo_flag: int,
                                 inv_type: int, sinkou: int,
                                 hero_idx: int = 0) -> Tuple[int, List[str]]:
        """
        单挑事件 - 对应 @INVASION_EVENT_CHALLENGE
        3个选择: 召唤魔王/亲自应战/全军进攻
        返回 (0=继续, 1=中止), 消息列表
        """
        messages = []

        if inv_type not in (INV_TYPE_MONSTER, INV_TYPE_HERO, INV_TYPE_PLUNDER):
            return -1, messages

        # 获取区域信息
        challenge_data = self._get_challenge_area_data(area_flag)
        if challenge_data is None:
            return -1, messages

        area_name, location, challenger_name, escape_desc, skill_desc, ex_flag_bit = challenge_data

        # 检查是否已触发过
        ex_flag_95 = self._invasion_mgr.get_ex_flag(95)
        if ex_flag_95 & ex_flag_bit:
            return -1, messages

        v = self._vars()
        hero = v.chars[hero_idx] if hero_idx < len(v.chars) else None
        hero_name = hero.savestr if hero else "勇者"

        # 根据侵攻类型决定选择
        if inv_type == INV_TYPE_HERO:
            choice = random.choice([1, 2, 3])
        elif inv_type == INV_TYPE_PLUNDER:
            choice = 2  # 亲自应战
        else:  # INV_TYPE_MONSTER
            choice = 3  # 全军进攻

        if choice == 1:  # 召唤魔王应战
            return self._challenge_summon_mao(sinkou, hero_idx, area_name,
                                               challenger_name, escape_desc, skill_desc,
                                               ex_flag_bit)
        elif choice == 2:  # 亲自应战
            return self._challenge_hero_fight(inv_type, sinkou, hero_idx,
                                               area_name, challenger_name, escape_desc, skill_desc)
        else:  # 全军进攻
            return self._challenge_army_attack(sinkou, area_name,
                                                challenger_name, escape_desc, skill_desc)

    def _get_challenge_area_data(self, area_flag: int) -> Optional[Tuple]:
        """获取单挑事件的区域数据"""
        data = {
            FLAG_AREA_HUMAN: ("人间界", "一座河边的桥", "女骑士", "骑上战马一骑绝尘离开了",
                              "剑术非常高超", 1),
            FLAG_AREA_ELF: ("精灵森林", "一条密林中的狭道", "月之祭司", "遁入密林之中消失了",
                            "箭术无比精准", 2),
            FLAG_AREA_DRAGON: ("龙之山脉", "一座山谷间的吊桥", "龙族巫女", "吟唱了传送咒语凭空消失了",
                               "龙语魔法无比犀利", 4),
            FLAG_AREA_HEAVEN: ("天界", "一座天界的虹桥", "女武神", "振起洁白的羽翅飞走了",
                               "圣力极其雄厚", 8),
        }
        return data.get(area_flag)

    def _challenge_summon_mao(self, sinkou: int, hero_idx: int,
                               area_name: str, challenger_name: str,
                               escape_desc: str, skill_desc: str,
                               ex_flag_bit: int) -> Tuple[int, List[str]]:
        """召唤魔王应战"""
        messages = []
        v = self._vars()

        # 是否使用氪金道具
        use_item = v.money >= 3000 and random.choice([True, False])

        roll = random.randint(0, 9)

        # 角色数量限制检查
        char_num = len(v.chars)
        max_char_num = getattr(v, 'max_charnum', 100)
        if self.get_flag(FLAG_SINDO_HUMAN) == 0 and char_num > 60:
            roll = 0
        elif (self.get_flag(FLAG_SINDO_ELF) == 0 and self.get_flag(FLAG_SINDO_DRAGON) == 0
              and self.get_flag(FLAG_SINDO_HEAVEN) == 0 and char_num > 65):
            roll = 0
        elif char_num >= max_char_num:
            roll = 0

        if use_item and roll >= 2:  # 开挂取胜 80%
            messages.append(f"魔王和{challenger_name}的战斗开始了。")
            trap_type = random.choice([
                f"魔王趁{challenger_name}不备，向{challenger_name}扔出了高级泥沼卷轴。",
                f"魔王趁{challenger_name}不备，向{challenger_name}扔出了强效麻痹药水。",
                f"魔王趁{challenger_name}不备，向{challenger_name}祭起了邪能封印壶。",
            ])
            messages.append(trap_type)
            messages.append(f"魔王军高呼魔王万岁，继续向{area_name}进发。")
            v.money -= 3000
            self._invasion_mgr.set_ex_flag(4444, self._invasion_mgr.get_ex_flag(4444) - 3000)
            self._invasion_mgr.set_ex_flag(95, self._invasion_mgr.get_ex_flag(95) | ex_flag_bit)
            self._invasion_mgr.set_ex_flag(EX_FLAG_FAME, self._invasion_mgr.get_ex_flag(EX_FLAG_FAME) + 1)
            messages.append(f"金钱-3000")
            return 0, messages
        elif use_item:  # 开挂失败 20%
            messages.append(f"魔王和{challenger_name}的战斗开始了。")
            messages.append(f"然而{challenger_name}提前察觉了魔王的动作，躲闪掉了。")
            messages.append(f"在鄙夷地看了魔王一眼后，{challenger_name}{escape_desc}。")
            messages.append(f"虽然被人鄙视了，但腼着脸的魔王命令魔王军继续向{area_name}前进。")
            v.money -= 3000
            self._invasion_mgr.set_ex_flag(4444, self._invasion_mgr.get_ex_flag(4444) - 3000)
            messages.append("金钱-3000。")
            return 0, messages
        elif roll < 2:  # 不开挂取胜 20%
            messages.append(f"魔王和{challenger_name}的战斗开始了、")
            messages.append(f"尽管{challenger_name}的{skill_desc}、")
            messages.append(f"但还是敌不过魔王的邪恶魔法、")
            messages.append(f"很快就成为了一具尸体。")
            messages.append(f"魔王军高呼魔王万岁、继续向{area_name}进发。")
            messages.append("魔王魔力减少50%、魔王经验+500")
            if len(v.chars) > 0:
                v.chars[0].base[1] //= 2
                if hero_idx < len(v.chars):
                    v.chars[hero_idx].exp[80] = v.chars[hero_idx].exp.get(80, 0) + 500
            return 0, messages
        else:  # 不开挂失败 80%
            messages.append(f"魔王和{challenger_name}的战斗开始了、")
            messages.append(f"{challenger_name}的{skill_desc}、")
            messages.append(f"魔王左支右绌、招架不住、")
            messages.append(f"被{skill_desc}抓住空隙、达成了重伤。")
            messages.append(f"魔王军士气动摇、救下昏迷的魔王匆匆逃回魔王城。")
            messages.append("魔王体力魔力清空、侵攻中止")
            if len(v.chars) > 0:
                v.chars[0].base[0] = 0
                v.chars[0].base[1] = 0
            return 1, messages

    def _challenge_hero_fight(self, inv_type: int, sinkou: int,
                               hero_idx: int, area_name: str,
                               challenger_name: str, escape_desc: str,
                               skill_desc: str) -> Tuple[int, List[str]]:
        """亲自应战"""
        messages = []
        v = self._vars()
        hero = v.chars[hero_idx] if hero_idx < len(v.chars) else None
        hero_name = hero.savestr if hero else "勇者"

        roll = random.randint(0, 9)

        if roll < 2:  # 奴隶取胜 20%
            messages.append(f"{hero_name}与{challenger_name}开始了战斗。")
            messages.append(f"虽然{challenger_name}{skill_desc}，但却被{hero_name}抓住机会打伤了。")
            messages.append(f"{challenger_name}心有不甘地{escape_desc}。")
            if inv_type == INV_TYPE_HERO:
                messages.append(f"魔王军高呼万岁，继续向{area_name}进发。")
            else:
                messages.append(f"{hero_name}继续向{area_name}进发。")
            messages.append(f"{hero_name}经验+500，体力-50%")
            if hero:
                hero.exp[80] = hero.exp.get(80, 0) + 500
                hero.base[0] = hero.base.get(0, 1000) // 2
            return 0, messages
        elif roll < 6:  # 不分胜负 40%
            messages.append(f"{hero_name}与{challenger_name}开始了战斗。")
            messages.append(f"虽然{challenger_name}{skill_desc}，但{hero_name}也不遑多让。")
            messages.append(f"在大战几百回合之后，{challenger_name}心有不甘地{escape_desc}。")
            if inv_type == INV_TYPE_HERO:
                messages.append(f"魔王军高呼万岁，继续向{area_name}进发。")
            else:
                messages.append(f"{hero_name}继续向{area_name}进发。")
            messages.append(f"{hero_name}体力-90%")
            if hero:
                hero.base[0] = hero.base.get(0, 1000) // 10
            return 0, messages
        else:  # 奴隶失败 40%
            messages.append(f"{hero_name}与{challenger_name}激烈交战起来。")
            messages.append(f"{challenger_name}的{skill_desc}，没过多久，{hero_name}就被{challenger_name}打晕了过去。")
            messages.append(f"{challenger_name}轻蔑的一笑，{escape_desc}。")
            if inv_type == INV_TYPE_HERO:
                messages.append("失去指挥官的魔王军只好撤退了。")
            ntr_flag = self.get_flag(5) & 128
            sindo_val = 0  # 简化
            if ntr_flag and not sindo_val and hero:
                messages.append(f"晕过去的{hero_name}成为了狂王的俘虏。")
                hero.cflag[1] = 9
            else:
                if hero:
                    messages.append(f"不知道过了多久后才苏醒过来的{hero_name}原路返回了。")
                    hero.cflag[1] = 0
            return 1, messages

    def _challenge_army_attack(self, sinkou: int, area_name: str,
                                challenger_name: str, escape_desc: str,
                                skill_desc: str) -> Tuple[int, List[str]]:
        """全军进攻"""
        messages = []

        if random.randint(0, 1):  # 损失惨重撤退 50%
            messages.append(f"然而由于地形狭窄魔王军的数量优势无法发挥、")
            messages.append(f"并且{challenger_name}的{skill_desc}、")
            messages.append(f"在损失了大批魔物之后、")
            messages.append(f"{challenger_name}轻蔑的一笑、{escape_desc}。")
            messages.append("魔王军元气大伤只好撤退了。")
            messages.append("侵攻中止。")
            return 1, messages
        else:  # 损失一般继续进攻 50%
            messages.append(f"然而由于地形狭窄魔王军的数量优势无法发挥、")
            messages.append(f"并且{challenger_name}的{skill_desc}、")
            messages.append(f"导致损失了不少魔物、")
            messages.append(f"最后{challenger_name}体力不支、{escape_desc}。")
            messages.append(f"付出了不少代价的魔王军、继续向{area_name}进发。")
            messages.append("魔物数量-20%。")
            sinkou = sinkou * 4 // 5
            return 0, messages

    # ---- 每日侵攻度衰减 ----

    def apply_daily_invasion_decay(self) -> List[str]:
        """
        每日侵攻度衰减 - 对应 ERB SYSTEM.ERB 中的侵攻度减少逻辑
        在每日循环中调用
        """
        messages = []

        for area_key, rules in DAILY_INVASION_DECAY_RULES.items():
            area_flag = rules["area_flag"]
            sindo_flag = rules["sindo_flag"]
            event_flag = rules["event_flag"]
            area_id = rules["area_id"]

            progress = self.get_flag(area_flag)
            sindo_val = self.get_flag(sindo_flag)

            # 未征服状态
            if sindo_val == 0:
                if progress > 0:
                    decay = random.randint(*rules["unconquered"]["decay_range"])
                    new_progress = max(progress - decay, rules["unconquered"]["min_after_decay"])
                    self.set_flag(area_flag, new_progress)
                    messages.append(rules["unconquered"]["message"])
                    messages.append(rules["unconquered"]["message_after"])
                    # 检查据点事件
                    messages.extend(self._check_kyoten_event(area_id))

            # 已征服状态 (偶尔衰减)
            elif sindo_val == 1:
                decay_chance = rules["conquered"].get("decay_chance", 6)
                if random.randint(0, decay_chance - 1) == 0:
                    if progress > rules["conquered"]["min_after_decay"]:
                        decay = random.randint(*rules["conquered"]["decay_range"])
                        new_progress = max(progress - decay, rules["conquered"]["min_after_decay"])
                        self.set_flag(area_flag, new_progress)
                        messages.append(rules["conquered"]["message"])
                        messages.append(rules["conquered"]["message_after"])
                        messages.extend(self._check_kyoten_event(area_id))

        return messages


# ============================================================
# HeroGenerator - 勇者生成 (对应 @ENTER_ENEMY)
# ============================================================

class HeroGenerator:
    """勇者生成器 - 处理勇者/莉莉/狂王替身的出现逻辑"""

    def __init__(self, game_engine):
        self.engine = game_engine

    def _vars(self):
        return self.engine.interpreter.vars

    def get_flag(self, idx, default=0):
        return int(self._vars().get_flag(idx, default))

    def set_flag(self, idx, value):
        self._vars().set_flag(idx, value)

    def get_ex_flag(self, idx, default=0):
        return int(self._vars().get_ex_flag(idx, default))

    def set_ex_flag(self, idx, value):
        self._vars().set_ex_flag(idx, value)

    def enter_enemy(self, arg: int = 0) -> Tuple[bool, List[str]]:
        """
        勇者生成 - 对应 @ENTER_ENEMY
        ARG:0 = 0 通常 / ARG:0 > 0 知り合い・家族確定エントリー
        返回 (是否成功生成, 消息列表)
        """
        messages = []
        v = self._vars()

        # 莉莉出现检查
        if arg == 0:
            lily_result, lily_msgs = self.k_11_lily()
            messages.extend(lily_msgs)

        # 狂王替身出现检查
        crazylord_result, crazylord_msgs = self.k_34_crazylord()
        messages.extend(crazylord_msgs)

        # 角色数量限制检查
        char_num = len(v.chars)
        max_char_num = getattr(v, 'max_charnum', 100)

        if self.get_flag(FLAG_SINDO_HUMAN) == 0 and char_num > 60:
            return False, messages
        elif (self.get_flag(FLAG_SINDO_ELF) == 0 and self.get_flag(FLAG_SINDO_DRAGON) == 0
              and self.get_flag(FLAG_SINDO_HEAVEN) == 0 and char_num > 65):
            return False, messages
        elif ((self.get_flag(FLAG_SINDO_ELF) * self.get_flag(FLAG_SINDO_DRAGON) == 0)
              and (self.get_flag(FLAG_SINDO_DRAGON) * self.get_flag(FLAG_SINDO_HEAVEN) == 0)
              and (self.get_flag(FLAG_SINDO_HEAVEN) * self.get_flag(FLAG_SINDO_ELF) == 0)
              and char_num > 70):
            return False, messages
        elif (self.get_flag(FLAG_SINDO_ELF) == 0 or self.get_flag(FLAG_SINDO_DRAGON) == 0
              or self.get_flag(FLAG_SINDO_HEAVEN) == 0) and char_num > 75:
            return False, messages
        elif self.get_flag(92) < 15 and char_num > 80:
            return False, messages
        elif char_num >= max_char_num:
            return False, messages

        # 选择角色编号
        chara_no = random.randint(1, 16)

        # 检查是否已有该角色 (简化判断)
        # GETCHARA(キャラ番号, SPフラグ)でキャラが存在しない場合は-1
        flag_5_bit32 = self.get_flag(5) & (1 << 5)  # GETBIT(FLAG:5,32)
        existing = self._find_char_by_no(chara_no)

        if flag_5_bit32 or existing is None:
            if arg > 0:
                # 知り合い・家族確定エントリー
                messages.append(f"角色No.{chara_no}作为熟人/家属登场")
                new_char = self.engine._create_character_from_template(998)
            else:
                # 异国勇者判定 (简化)
                is_foreign = random.randint(0, 9) == 0
                new_char = self.engine._create_character_from_template(chara_no)

            border = "*" * 41
            messages.append(border)
            # 显示勇者类型和名字
            new_char_idx = len(v.chars) - 1
            if new_char_idx >= 0 and v.chars[new_char_idx].savestr:
                hero_type = "异国勇者" if is_foreign else "勇者"
                messages.append(f"{hero_type} {v.chars[new_char_idx].savestr}开始了地下城的攻略！")
            else:
                messages.append(f"勇者开始了地下城的攻略！")
            messages.append(border)

            # 勇者LVUP
            if self.get_flag(5) & 2:
                self.set_flag(FLAG_HERO_LEVEL, self.get_flag(FLAG_HERO_LEVEL) + 1)
                messages.append(f"勇者基础等级校正后现在是等级{self.get_flag(FLAG_HERO_LEVEL)}")
        else:
            messages.append("出于对魔王的恐惧，勇者没有出现。")
            return False, messages

        return True, messages

    def k_11_lily(self) -> Tuple[bool, List[str]]:
        """
        莉莉出现 - 对应 @K_11_LILY
        200日以上、玛奥存在且有爱/淫乱、莉莉不存在
        """
        messages = []
        v = self._vars()

        # 入口标记已设置
        if self.get_flag(223) == 1:
            return False, messages

        # 200日未满
        day = v.day[0] if hasattr(v, 'day') else 0
        if day < 200:
            return False, messages

        # 玛奥不存在
        mao_idx = self._find_char_by_no(17)
        if mao_idx is None or mao_idx < 0:
            return False, messages

        # 莉莉已存在
        lily_idx = self._find_char_by_no(24)
        if lily_idx is not None and lily_idx >= 0:
            return False, messages

        # 玛奥没有爱也没有淫乱
        mao = v.chars[mao_idx]
        if mao.talent.get(85, 0) == 0 and mao.talent.get(76, 0) == 0:
            return False, messages

        # 玛奥非待机中
        if mao.cflag.get(1, 0) != 0:
            return False, messages

        # 莉莉登场
        new_char = self.engine._create_character_from_template(24)
        self.set_flag(223, 1)

        border = "*" * 41
        messages.append("")
        messages.append(border)
        messages.append("魔王的地下城附近的村子里有一对姐妹。她们没有双亲，一起在亲戚的家里生活。")
        messages.append("某一天，魔王复活了，妹妹也同时下落不明。姐姐像是发疯一般地四处寻找，也拜托了勇者，却还是找不到妹妹。")
        messages.append("又过了半年，姐姐终于下定了决心，前往魔王的地下城。一只手拿着提灯，另一只手握着勇者丢弃的旧剑。")
        messages.append("")
        messages.append("村娘莉莉开始了地下城的攻略！")
        messages.append(border)

        return True, messages

    def k_34_crazylord(self) -> Tuple[bool, List[str]]:
        """
        狂王替身出现 - 对应 @K_34_crazylord
        350天以上、金红桃已陷落、四方堡垒全陷落
        """
        messages = []
        v = self._vars()

        # 入口标记已设置
        if self.get_flag(224) == 1:
            return False, messages

        # 350天未满
        day = v.day[0] if hasattr(v, 'day') else 0
        if day < 350:
            return False, messages

        # 金红桃不存在
        kin_idx = self._find_char_by_no(20)
        if kin_idx is None or kin_idx < 0:
            return False, messages

        # 替身已存在
        sub_idx = self._find_char_by_no(34)
        if sub_idx is not None and sub_idx >= 0:
            return False, messages

        # 金红桃没有爱也没有淫乱
        kin = v.chars[kin_idx]
        if kin.talent.get(85, 0) == 0 and kin.talent.get(76, 0) == 0:
            return False, messages

        # 金红桃调教中
        if kin.cflag.get(1, 0) != 0:
            return False, messages

        # 四方堡垒全陷落
        if self.get_flag(92) != 15:
            return False, messages

        # 狂王替身登场
        new_char = self.engine._create_character_from_template(34)
        self.set_flag(224, 1)

        border = "*" * 77
        messages.append("")
        messages.append("")
        messages.append(border)
        messages.append("狡猾的狂王，原来对作为情妇和亲卫队长的金红桃也不是推心置腹。")
        messages.append("在你已经唯命是从的金红桃身上，没有得到任何情报。")
        messages.append("其它的人也是对狂王的行踪一无所知，各地的魔物也没有找到狂王。")
        messages.append("正当你满脑疑惑和不安的时候，一个蓝发红眼的身影出现在地下城门口。")
        messages.append("迈着悠闲的步伐，一抬手就将守门的怪物全灭了，是狂王？！")
        messages.append("不对，这幽波纹的流动，证明了她只是狂王的替身！")
        messages.append("既是她，也不是她…………但不管如何，她带着再次封印你的斗志，向你冲过来了！！")
        messages.append("")
        messages.append("狂王的替身 葵希罗 开始了地下城的攻略！")
        messages.append(border)

        return True, messages

    def get_enemy(self) -> Tuple[Optional[int], List[str]]:
        """
        捕获勇者 - 对应 @GET_ENEMY
        侵攻时5%/9%概率触发
        返回 (角色索引或None, 消息列表)
        """
        messages = []
        v = self._vars()

        # 角色数量限制
        char_num = len(v.chars)
        max_char_num = getattr(v, 'max_charnum', 100)

        if self.get_flag(FLAG_SINDO_HUMAN) == 0 and char_num > 60:
            return None, messages
        elif char_num >= max_char_num:
            return None, messages

        # 生成俘虏角色
        chara_no = random.randint(1, 16)
        new_char = self.engine._create_character_from_template(chara_no)

        border = "*" * 41
        messages.append(border)
        messages.append(f"勇者被俘虏了！")
        messages.append(border)

        # 返回新生成角色的索引
        char_idx = len(v.chars) - 1
        return char_idx, messages

    def _find_char_by_no(self, char_no: int) -> Optional[int]:
        """根据角色编号查找角色索引 - 对应 GETCHARA"""
        v = self._vars()
        for i, char in enumerate(v.chars):
            if hasattr(char, 'no') and char.no == char_no:
                if char.cflag.get(0, 0) == 0:
                    return i
                else:
                    return -1  # 存在但已卖出/助手
        return None


# ============================================================
# TurnEndEventManager - 回合结束事件 (对应 @EVENTTURNEND)
# ============================================================

class TurnEndEventManager:
    """回合结束事件管理器 - 对应 @EVENTTURNEND"""

    def __init__(self, game_engine):
        self.engine = game_engine
        self._hero_gen = HeroGenerator(game_engine)

    def _vars(self):
        return self.engine.interpreter.vars

    def get_flag(self, idx, default=0):
        return int(self._vars().get_flag(idx, default))

    def set_flag(self, idx, value):
        self._vars().set_flag(idx, value)

    def process_turn_end(self) -> List[str]:
        """处理回合结束事件 - 对应 @EVENTTURNEND"""
        messages = []

        # 1. 卖出/助手判定
        messages.extend(self._check_sell_assiable())

        # 2. 特殊素质获得判定
        messages.extend(self._check_special_skill())

        # 3. 妊娠判定
        messages.extend(self._check_pregnancy())

        # 4. 休息标记解除
        self.set_flag(0, 0)

        # 5. 时间推进
        v = self._vars()
        time_val = v.time if hasattr(v, 'time') else 0

        if time_val == 1:
            # 午后 -> 次日
            # 妊娠追加判定 (卖春/狂王等)
            messages.extend(self._check_extra_pregnancy())

            # 日期变更事件
            messages.extend(self._event_nextday())

            # 日期推进
            v.day[0] += 1  # DAY:0 总天数
            v.day[2] += 1  # DAY:2 日期

            # 每月29日以上月替处理
            if v.day[2] > 28:
                messages.extend(self._event_nextmonth())
                v.day[2] = 1
                v.day[1] += 1  # 月份+1
                if v.day[1] > 12:
                    v.day[1] = 1
                    v.day[0] += 1  # 年份+1 (这里day[0]是年)
                    messages.append(f"新年到来，现在是 {v.day[0]} 年")

            v.day[3] += 1  # 星期
            if v.day[3] > 6:
                v.day[3] = 0

            v.time = 0

            # 勇者生成
            result, enemy_msgs = self._hero_gen.enter_enemy(0)
            messages.extend(enemy_msgs)

            # 根据天数额外生成勇者
            day_total = v.day[0] if hasattr(v, 'day') else 0
            sengen = self._vars().get_ex_flag(EX_FLAG_VIDEO_POPULAR, 0)
            sengenmax = 12

            if day_total >= 100:
                sengen_val = sengen - 2
                sengenmax_val = 12 - 2
                result, msgs = self._hero_gen.enter_enemy()
                messages.extend(msgs)
            if day_total >= 300:
                sengen_val = sengen - 3
                sengenmax_val = 12 - 3
                result, msgs = self._hero_gen.enter_enemy()
                messages.extend(msgs)
            if day_total >= 500:
                sengen_val = sengen - 4
                sengenmax_val = 12 - 4
                result, msgs = self._hero_gen.enter_enemy()
                messages.extend(msgs)

            # 水晶球宣言效果额外勇者
            if sengen > 0:
                for _ in range(min(sengen, sengenmax)):
                    result, msgs = self._hero_gen.enter_enemy()
                    messages.extend(msgs)

        else:
            # 午前 -> 午后
            v.time = 1

        # 6. 自动购买物品
        messages.extend(self._auto_buying())

        # 7. 侵攻度衰减 (在每日循环中)
        invasion_event_mgr = InvasionEventManager(self.engine)
        messages.extend(invasion_event_mgr.apply_daily_invasion_decay())

        # 8. 魔王恢复
        messages.extend(self._mao_recovery())

        return messages

    def _check_sell_assiable(self) -> List[str]:
        """卖出/助手判定 - 对应 CHECK_SELLASSIABLE"""
        from ..systems.dungeon import DungeonSystem
        messages = []
        dungeon = DungeonSystem(self.engine)
        v = self._vars()
        for char in v.chars:
            if char.cflag.get(0, 0) >= 2:
                continue
            is_assiable = False
            is_sellable = False

            submit = char.abl.get(10, 0)
            desire = char.abl.get(11, 0)
            if submit >= 4 and desire >= 3:
                is_assiable = True
            if submit + desire >= 6:
                is_sellable = True

            c_abl = char.abl.get(0, 0)  # C感觉
            v_abl = char.abl.get(2, 0)  # V感觉
            a_abl = char.abl.get(3, 0)  # A感觉
            b_abl = char.abl.get(1, 0)  # B感觉
            if c_abl >= 3 or v_abl >= 3 or a_abl >= 3 or b_abl >= 3:
                is_sellable = True

            has_resist = char.talent.get(12, 0) or char.talent.get(34, 0)
            has_resist = has_resist or char.talent.get(20, 0) or char.talent.get(32, 0)
            if has_resist and submit < 4:
                is_assiable = False
                is_sellable = False

            if is_assiable:
                char.cflag[0] = 2
                messages.append(f"{char.savestr or char.name}可以做调教助手了")
            elif is_sellable:
                char.cflag[0] = 1
                messages.append(f"{char.savestr or char.name}可以卖掉了")

        return messages

    def _check_special_skill(self) -> List[str]:
        """特殊素质获得判定 - 对应 CHECK_SPECIALSKIL"""
        from ..systems.dungeon import DungeonSystem
        messages = []
        dungeon = DungeonSystem(self.engine)
        v = self._vars()
        for char in v.chars:
            skills = dungeon._check_special_skill(char)
            if skills:
                char_name = char.savestr if hasattr(char, 'savestr') else "角色"
                messages.append(f"{char_name}获得了特殊技能: {', '.join(skills)}")
        return messages

    def _check_pregnancy(self) -> List[str]:
        """妊娠判定 - 对应 IN_VAGINA_ALL + CONCEPTION_CHECK_ALL"""
        from ..systems.dungeon import DungeonSystem
        messages = []
        dungeon = DungeonSystem(self.engine)
        v = self._vars()
        for char in v.chars:
            if dungeon._check_pregnancy(char):
                char_name = char.savestr if hasattr(char, 'savestr') else "角色"
                messages.append(f"{char_name}似乎怀孕了………")
                char.talent[153] = 1
        return messages

    def _check_extra_pregnancy(self) -> List[str]:
        """额外妊娠判定 (卖春/狂王等)"""
        from ..systems.dungeon import DungeonSystem
        messages = []
        dungeon = DungeonSystem(self.engine)
        v = self._vars()
        for char in v.chars:
            if dungeon._check_extra_pregnancy(char):
                char_name = char.savestr if hasattr(char, 'savestr') else "角色"
                messages.append(f"{char_name}发生了异常妊娠………")
                char.talent[153] = 1
        return messages

    def _event_nextday(self) -> List[str]:
        """每日事件 (对应 @EVENT_NEXTDAY)"""
        messages = []
        v = self._vars()
        # 角色恢复
        for char in v.chars:
            if char.base.get(0, 0) < char.maxbase.get(0, 0):  # HP recovery
                char.base[0] = min(char.base.get(0, 0) + 100, char.maxbase.get(0, 1000))
            if char.base.get(1, 0) < char.maxbase.get(1, 0):  # MP recovery
                char.base[1] = min(char.base.get(1, 0) + 50, char.maxbase.get(1, 500))
        # 侵攻度衰减
        invasion_event_mgr = InvasionEventManager(self.engine)
        messages.extend(invasion_event_mgr.apply_daily_invasion_decay())
        return messages

    def _event_nextmonth(self) -> List[str]:
        """每月事件 (对应 @EVENT_NEXTMONTH)"""
        messages = []
        v = self._vars()
        # 勇者生成
        result, enemy_msgs = self._hero_gen.enter_enemy()
        messages.extend(enemy_msgs)
        # 水晶球衰减
        invasion_mgr = InvasionManager(self.engine)
        messages.extend(invasion_mgr.sengen_video_decay())
        # 特殊月事件
        month = v.day[1] if hasattr(v, 'day') else 1
        if month == 1:  # 新年
            pass  # 新年事件
        elif month == 8:  # 魔王祭
            pass  # 魔王祭事件
        return messages

    def _auto_buying(self) -> List[str]:
        """自动购买物品 - 对应 @AUTO_BUYING"""
        messages = []
        v = self._vars()

        # 润滑液 (FLAG:34 & 1)
        if (self.get_flag(34) & 1) and v.money >= 200 and v.get_item(25, 0) == 0:
            v.set_item(25, 1)
            v.money -= 200
            self._vars().set_ex_flag(4444, self._vars().get_ex_flag(4444, 0) - 200)

        # 录像带 (FLAG:34 & 2)
        if (self.get_flag(34) & 2) and v.money >= 500 and v.get_item(6, 0) > 0 and v.get_item(28, 0) == 0:
            v.set_item(28, 1)
            v.money -= 500
            self._vars().set_ex_flag(4444, self._vars().get_ex_flag(4444, 0) - 500)

        # 安全套 (FLAG:34 & 8)
        if self.get_flag(34) & 8:
            for _ in range(10):
                if v.money >= 100 and v.get_item(24, 0) < 10:
                    v.set_item(24, v.get_item(24, 0) + 1)
                    v.money -= 100
                    self._vars().set_ex_flag(4444, self._vars().get_ex_flag(4444, 0) - 100)

        return messages

    def _mao_recovery(self) -> List[str]:
        """魔王恢复 - 对应 ERB SYSTEM.ERB 末尾"""
        v = self._vars()
        if len(v.chars) == 0:
            return []

        time_val = v.time if hasattr(v, 'time') else 0
        heal = 1400 if time_val == 0 else 1000

        # HP恢复
        mao = v.chars[0]
        mao.base[0] = min(mao.maxbase.get(0, 9999), mao.base.get(0, 0) + heal)

        # 气力恢复
        if self.get_flag(400) > 0:
            heal = -10
        mao.base[1] = min(mao.maxbase.get(1, 9999), mao.base.get(1, 0) + heal)

        return []


# ============================================================
# EndingManager - 结局管理 (对应 ENDING.ERB)
# ============================================================

class EndingManager:
    """结局管理器 - 对应 ENDING.ERB 中的所有结局"""

    # 结局类型
    ENDING_GOOD = 1          # 人间界征服 (ENDING_1)
    ENDING_CASTLE_FALLEN = 2 # 魔王城陷落 (ENDING_2)
    ENDING_ELF = 3           # 精灵领域征服 (ENDING_3)
    ENDING_DRAGON = 4        # 龙之山脉征服 (ENDING_4)
    ENDING_HEAVEN = 5        # 天界征服 (ENDING_5)
    ENDING_NORMAL = 6        # 500日Normal End (ENDING_N)
    ENDING_PALACE = 7        # 天神宫征服 (END10_55)

    # 结局数据
    ENDING_DATA = {
        1: {"name": "人间制霸", "condition": lambda ge: ge.interpreter.vars.get_flag(500, 0) >= 10000, "area": 0},
        2: {"name": "魔王城陷落", "condition": lambda ge: ge.interpreter.vars.get_flag(510, 0) >= 10000, "area": -1},
        3: {"name": "精灵领域征服", "condition": lambda ge: ge.interpreter.vars.get_flag(501, 0) >= 10000, "area": 1},
        4: {"name": "龙族山脉征服", "condition": lambda ge: ge.interpreter.vars.get_flag(502, 0) >= 10000, "area": 2},
        5: {"name": "天界征服", "condition": lambda ge: ge.interpreter.vars.get_flag(503, 0) >= 10000, "area": 3},
        6: {"name": "Normal End", "condition": lambda ge: ge.interpreter.vars.day[0] >= 500 if hasattr(ge.interpreter.vars, 'day') else False, "area": -2},
        7: {"name": "天神宫征服", "condition": lambda ge: ge.interpreter.vars.get_ex_flag(504, 0) >= 10000, "area": 4},
    }

    def __init__(self, game_engine):
        self.engine = game_engine

    def _vars(self):
        return self.engine.interpreter.vars

    def get_flag(self, idx, default=0):
        return int(self._vars().get_flag(idx, default))

    def set_flag(self, idx, value):
        self._vars().set_flag(idx, value)

    def get_ex_flag(self, idx, default=0):
        return int(self._vars().get_ex_flag(idx, default))

    def set_ex_flag(self, idx, value):
        self._vars().set_ex_flag(idx, value)

    def check_ending_conditions(self) -> Optional[int]:
        """
        检查结局条件 - 对应 ENDCHECK / INVASION_CHECK
        返回结局类型或None
        """
        # 人间界征服
        if self.get_flag(FLAG_AREA_HUMAN) >= 10000 and self.get_flag(FLAG_SINDO_HUMAN) == 0:
            return self.ENDING_GOOD

        # 精灵领域征服
        if self.get_flag(FLAG_AREA_ELF) >= 10000 and self.get_flag(FLAG_SINDO_ELF) == 0:
            return self.ENDING_ELF

        # 龙之山脉征服
        if self.get_flag(FLAG_AREA_DRAGON) >= 10000 and self.get_flag(FLAG_SINDO_DRAGON) == 0:
            return self.ENDING_DRAGON

        # 天界征服
        if self.get_flag(FLAG_AREA_HEAVEN) >= 10000 and self.get_flag(FLAG_SINDO_HEAVEN) == 0:
            return self.ENDING_HEAVEN

        # 天神宫征服
        if self.get_ex_flag(EX_FLAG_AREA_PALACE) >= 10000 and self.get_ex_flag(EX_FLAG_SINDO_PALACE) == 0:
            return self.ENDING_PALACE

        # 500日Normal End
        v = self._vars()
        day = v.day[0] if hasattr(v, 'day') else 0
        if day >= 500:
            return self.ENDING_NORMAL

        return None

    def get_ending_message(self, ending_type: int) -> str:
        """获取结局消息 - 匹配 ERB 原始文本"""
        if ending_type == self.ENDING_GOOD:
            return self._ending_1_message()
        elif ending_type == self.ENDING_CASTLE_FALLEN:
            return self._ending_2_message()
        elif ending_type == self.ENDING_ELF:
            return self._ending_3_message()
        elif ending_type == self.ENDING_DRAGON:
            return self._ending_4_message()
        elif ending_type == self.ENDING_HEAVEN:
            return self._ending_5_message()
        elif ending_type == self.ENDING_NORMAL:
            return self._ending_n_message()
        elif ending_type == self.ENDING_PALACE:
            return self._ending_palace_message()
        else:
            return "游戏结束"

    def process_ending(self, ending_type: int) -> List[str]:
        """
        处理结局 - 执行结局效果
        返回消息列表
        """
        messages = []

        if ending_type == self.ENDING_GOOD:
            messages.extend(self._process_ending_1())
        elif ending_type == self.ENDING_ELF:
            messages.extend(self._process_ending_3())
        elif ending_type == self.ENDING_DRAGON:
            messages.extend(self._process_ending_4())
        elif ending_type == self.ENDING_HEAVEN:
            messages.extend(self._process_ending_5())
        elif ending_type == self.ENDING_NORMAL:
            messages.extend(self._process_ending_n())

        return messages

    # ---- ENDING_1: 人间界征服 ----

    def _ending_1_message(self) -> str:
        return (
            "┌─────────────────────────────┐\n"
            "｜　　　　　　　　魔王终于再次掌握了世界　　　　　　　　　　｜\n"
            "｜　魔物们冲入皇宫，将还在熟睡中的年幼公主拖下床，抓了起来　｜\n"
            "｜　　　　　　而且，魔王还对人类提出了这样的要求　　　　　　｜\n"
            "｜　　　　　命令人类继续派出勇者到地下城来讨伐自己　　　　　｜\n"
            "｜　　　　　因为这样很有趣，哈哈哈哈。魔王这么说着　　　　　｜\n"
            "｜　　　　这些女孩实际上已经不是勇者，而是魔王的祭品　　　　｜\n"
            "└─────────────────────────────┘"
        )

    def _process_ending_1(self) -> List[str]:
        """ENDING_1 处理: 人间界征服后添加菲娅"""
        messages = []
        messages.append(self._ending_1_message())

        # 生成菲娅角色
        new_char = self.engine._create_character_from_template(35)

        messages.append("人间界已经陷落了，不过世上还有很多其它地方，要继续游戏吗？")
        messages.append("[0] - 世界这么大，我想再去看看！")
        messages.append("[1] - 我已经……不想做魔王了……")

        # 设置征服状态
        self.set_flag(FLAG_SINDO_HUMAN, 1)
        messages.append("*人类皇族公主菲娅，被你抓获了*")

        return messages

    # ---- ENDING_2: 魔王城陷落 ----

    def _ending_2_message(self) -> str:
        return (
            "┌─────────────────────────────┐\n"
            "｜　　　　　　新的女勇者，终于攻陷了魔王的地下城　　　　　　｜\n"
            "｜　　　　　　魔王将打倒自己的勇者的模样铭记于心　　　　　　｜\n"
            "｜　　　带着一丝不易察觉的微笑，再次陷入了封印的沉睡之中　　｜\n"
            "└─────────────────────────────┘"
        )

    # ---- ENDING_3: 精灵领域征服 ----

    def _ending_3_message(self) -> str:
        return (
            "┌─────────────────────────────┐\n"
            "｜　　　　　　　　魔王终于征服了精灵族的领域　　　　　　　　｜\n"
            "｜　　　　于是，魔王向精灵族的长老提出了这样的要求　　　　　｜\n"
            "｜　　　　　　　　要求献上秘藏的精灵族圣女　　　　　　　　　｜\n"
            "└─────────────────────────────┘"
        )

    def _process_ending_3(self) -> List[str]:
        """ENDING_3 处理: 精灵领域征服"""
        messages = []
        messages.append(self._ending_3_message())

        # 设置征服状态
        self.set_flag(FLAG_SINDO_ELF, 1)

        # 贡品角色生成
        tribute_msgs = self._char_gift(AREA_ELF)
        messages.extend(tribute_msgs)

        # 最终征服状态
        self.set_flag(FLAG_SINDO_ELF, 2)

        return messages

    # ---- ENDING_4: 龙之山脉征服 ----

    def _ending_4_message(self) -> str:
        return (
            "┌─────────────────────────────┐\n"
            "｜　　　　　　　　　魔王终于征服了龙族的山脉　　　　　　　　｜\n"
            "｜　　　　　于是，魔王向龙族的长老提出了这样的要求　　　　　｜\n"
            "｜　　　　　　　要求献上有着最悠久血统的龙族公主　　　　　　｜\n"
            "└─────────────────────────────┘"
        )

    def _process_ending_4(self) -> List[str]:
        """ENDING_4 处理: 龙之山脉征服"""
        messages = []
        messages.append(self._ending_4_message())

        self.set_flag(FLAG_SINDO_DRAGON, 1)
        tribute_msgs = self._char_gift(AREA_DRAGON)
        messages.extend(tribute_msgs)
        self.set_flag(FLAG_SINDO_DRAGON, 2)

        return messages

    # ---- ENDING_5: 天界征服 ----

    def _ending_5_message(self) -> str:
        return (
            "┌─────────────────────────────┐\n"
            "｜　　　　　　　　　　魔王终于征服了天界　　　　　　　　　　｜\n"
            "｜　　　　　　　　于是，魔王向天界提出了要求　　　　　　　　｜\n"
            "｜　　　　　　　命令献上被选为下一代主神的天使　　　　　　　｜\n"
            "└─────────────────────────────┘"
        )

    def _process_ending_5(self) -> List[str]:
        """ENDING_5 处理: 天界征服"""
        messages = []
        messages.append(self._ending_5_message())

        self.set_flag(FLAG_SINDO_HEAVEN, 1)
        tribute_msgs = self._char_gift(AREA_HEAVEN)
        messages.extend(tribute_msgs)
        self.set_flag(FLAG_SINDO_HEAVEN, 2)

        return messages

    # ---- ENDING_N: 500日Normal End ----

    def _ending_n_message(self) -> str:
        return (
            "自从魔王被解开封印已经过了整整500天。\n"
            "尽管各界源源不断地派遣勇者讨伐魔王，\n"
            "但都要么成为了魔王的收藏品，\n"
            "要么被倒卖到大陆各个龌龊的角落，\n"
            "要么成为了魔王力量的一部分，帮助魔王为祸人间。\n"
            "\n"
            "这块大陆的人们渐渐也习惯于魔王地下城的存在，想要寻找财富或者冒险...\n"
            "或者...期待着女性最本能的渴望．．．\n"
            "...各种心思的女孩子们，依然在源源不断地走进这个魔窟。\n"
            "...\n"
            "...\n"
            "大概，已经不会有尽头了吧。\n"
            "达成了【Normal End】。"
        )

    def _process_ending_n(self) -> List[str]:
        """ENDING_N 处理: 500日Normal End"""
        messages = []
        messages.append(self._ending_n_message())
        messages.append("[1] 结束游戏\t\t[2] 继续游戏")
        return messages

    # ---- END10_55: 天神宫征服 ----

    def _ending_palace_message(self) -> str:
        return "天神宫已被征服！"

    # ---- 贡品角色生成 ----

    def _char_gift(self, area_id: int) -> List[str]:
        """
        贡品角色生成 - 对应 @CHAR_GIFT
        征服某区域后生成贡品角色
        """
        messages = []
        config = INVASION_CONQUEST_REWARD_CONFIG_TRIBUTE.get(area_id)
        if config is None:
            return messages

        messages.append(config["message"])
        messages.append(config["question"])

        # 生成贡品角色
        new_char = self.engine._create_character_from_template(config["char_no"])
        # 简化: 生成角色信息
        messages.append(f"[0] 收下她吧  [1] 另外挑选")

        return messages

    # ---- ENDCHECK: 主线剧情检定 ----

    def endcheck(self) -> List[str]:
        """
        主线剧情检定 - 对应 @ENDCHECK
        使用 EX_FLAG:2801-2820 存储剧情进度
        """
        messages = []

        # 执行结局重置和检查
        self._endreset()
        self._endcheck_main()
        self._endcheck_chara()

        # 各角色路线事件 END{2-15}_{stage}
        messages.extend(self._check_chara_routes())

        # 500日Normal End检查
        ex_flag_2801 = self.get_ex_flag(2801)
        if ex_flag_2801 == 99:
            v = self._vars()
            day = v.day[0] if hasattr(v, 'day') else 0
            if day == 500:
                messages.extend(self._process_ending_n())

        return messages

    # ---- ENDLEGACY: 角色路线结局 ----

    def endlegacy(self) -> List[str]:
        """
        角色路线结局 - 对应 @ENDLEGACY
        各角色恋慕/淫乱路线选择
        """
        messages = []

        # 各角色路线进度
        char_routes = {
            5: ("玛奥", 2805),
            6: ("莉莉", 2806),
            7: ("菲娅", 2807),
            8: ("琼", 2808),
            9: ("普林希斯", 2809),
            10: ("嘉德", 2810),
            11: ("黑方片", 2811),
            12: ("白梅花", 2812),
            13: ("金红桃", 2813),
            14: ("银黑桃", 2814),
        }

        for route_id, (char_name, ex_flag_idx) in char_routes.items():
            stage = self.get_ex_flag(ex_flag_idx) % 100
            if stage > 0:
                # 角色路线已触发
                route_type = "恋慕" if stage == 1 else "淫乱" if stage == 2 else f"阶段{stage}"
                messages.append(f"【{char_name}】{route_type}线已触发 (阶段: {stage})")

                # 菲娅特殊处理
                if route_id == 7:
                    messages.extend(self._process_fia_route(stage))

        return messages

    def _process_fia_route(self, stage: int) -> List[str]:
        """菲娅路线事件处理"""
        messages = []
        ex_flag_2807 = self.get_ex_flag(2807)
        stage_hundreds = stage * 100

        if stage == 1 and ex_flag_2807 < stage_hundreds:
            messages.append("菲娅在床上迷糊的看着四周……似乎还没有对自己身上发生的事情有所认知……")
            messages.append("已经将幼女的人生完全掌握的魔王，在水晶球中俯视着影像。")
            messages.append("接下来……要怎么处置她好呢？")
            self.set_ex_flag(2807, ex_flag_2807 + 100)
        elif stage == 2 and ex_flag_2807 < stage_hundreds:
            messages.append("「啊，魔王大人～♪」")
            messages.append("看见魔王的菲娅，啪嗒啪嗒的迎了过来。")
            messages.append("「呐呐，今天也要一起玩吗？」")
            self.set_ex_flag(2807, ex_flag_2807 + 100)
        elif stage == -1:
            messages.append("菲娅的身体状况看起来不是很好的样子……")
            messages.append("似乎是刺激过大了的样子，产生了精神创伤……")
            messages.append("～Bad Ending～")
            self.set_ex_flag(2807, ex_flag_2807 - 1)
        elif stage == 3 and ex_flag_2807 < stage_hundreds:
            messages.append("要进入菲娅恋慕线吗？（剧情选择是不可逆的，选择之后就无法进入其它人的故事线了）")
            messages.append("[1] 菲娅！！菲娅！！\t[2] 不好萝莉这口！ [3] 啊？让我先存个档！")
        elif stage == 13 and ex_flag_2807 < stage_hundreds:
            messages.append("要进入菲娅淫乱线吗？（剧情选择是不可逆的，选择之后就无法进入其它人的故事线了）")
            messages.append("[1] 菲娅！！菲娅！！\t[2] 不好萝莉这口！ [3] 啊？让我先存个档！")

        return messages

    # ---- ENDRESET / ENDCHECK 辅助方法 ----

    def _endreset(self):
        """结局重置 - 对应 @ENDRESET"""
        v = self._vars()
        # 重置结局检查相关标记
        # EX_FLAG:999 用于标记是否已检查过结局
        self.set_ex_flag(999, 0)
        # 重置各角色结局触发标记
        for char_no in range(1, 17):
            ex_flag_idx = 2800 + char_no
            # 保留已触发的路线，只重置每日检查标记
            route_stage = self.get_ex_flag(ex_flag_idx)
            if route_stage > 0:
                # 触发了路线事件，保留路线状态
                self.set_ex_flag(ex_flag_idx, route_stage)
        # 重置每日结局触发标记 EX_FLAG:990
        self.set_ex_flag(990, 0)
        # 检查是否已经满足结局条件
        flag_val = v.get_flag(500, 0)
        if flag_val >= 10000:
            self.set_ex_flag(990, 1)

    def _endcheck_main(self):
        """主线结局检查 - 对应 @ENDCHECKMAIN"""
        v = self._vars()
        messages = []

        # 检查魔王城是否沦陷 (FLAG:510)
        if v.get_flag(510, 0) >= 10000:
            messages.append("魔王城陷落……")
            self.set_ex_flag(990, 1)

        # 检查全制霸 (FLAG:500)
        if v.get_flag(500, 0) >= 10000:
            messages.append("达成人间制霸！")
            self.set_ex_flag(990, 1)

        # 检查Normal End (DAY >= 500)
        day_count = v.day[0] if hasattr(v, 'day') else 0
        if day_count >= 500:
            messages.append("期限已到……")
            self.set_ex_flag(990, 1)

        return messages

    def _endcheck_chara(self):
        """角色路线结局检查 - 对应 @ENDCHECKCHARA"""
        v = self._vars()
        for i, char in enumerate(v.chars):
            if i == 0:
                continue  # 跳过魔王
            # 检查角色是否有爱慕/淫乱素质
            has_love = char.talent.get(85, 0) == 1
            has_lust = char.talent.get(76, 0) == 1
            if has_love or has_lust:
                char_no = char.template_id if hasattr(char, 'template_id') else -1
                if 1 <= char_no <= 16:
                    ex_flag_idx = 2800 + char_no
                    current = self.get_ex_flag(ex_flag_idx)
                    if current == 0:
                        route_type = 1 if has_love else 2
                        self.set_ex_flag(ex_flag_idx, route_type)

    def _check_chara_routes(self) -> List[str]:
        """检查各角色路线事件 - 对应 END{2-15}_{stage}"""
        messages = []
        v = self._vars()
        for i, char in enumerate(v.chars):
            if i == 0:
                continue
            char_no = char.template_id if hasattr(char, 'template_id') else -1
            if 1 <= char_no <= 16:
                ex_flag_idx = 2800 + char_no
                stage = self.get_ex_flag(ex_flag_idx) % 100
                if stage > 0:
                    char_name = char.savestr if hasattr(char, 'savestr') else f"角色{char_no}"
                    route_type = "恋慕" if stage == 1 else "淫乱" if stage == 2 else f"阶段{stage}"
                    messages.append(f"【{char_name}】{route_type}线 (阶段: {stage})")
        return messages
