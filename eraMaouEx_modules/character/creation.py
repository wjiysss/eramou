"""
eraMaouEx 角色模块 - 角色创建系统
对应 ERB CHARA_MAKE.ERB
"""

import random
import math
from typing import Dict, Optional, Any, List, Tuple


class CharacterCreator:
    """角色创建器 - 完整的角色生成流程"""

    # 冲突检查的素质对列表（来自 CMI_CONFLICT_CHECK）
    CONFLICT_PAIRS = [
        10, 12,   11, 13,   14, 16,   15, 17,   17, 18,
        20, 23,   21, 23,   22, 23,
        20, 63,   21, 63,   22, 63,
        23, 24,   25, 26,   27, 28,
        30, 31,   32, 33,
        35, 36,   40, 41,   42, 43,
        44, 45,   50, 51,   61, 62,   62, 64,
        70, 71,
        79, 80,   79, 81,   79, 82,   79, 122,
        80, 81,   80, 82,   81, 82,
        99, 100,      101, 102,
        103, 104,    105, 106,    103, 122,   104, 122,
        107, 108,    111, 112,
        109, 110,    109, 114,    109, 116,    119, 109,   119, 116,   119, 114,   119, 110,   122, 109,   122, 110,   122, 114,   122, 116,   122, 119,
        110, 114,    110, 116,    114, 116,
        121, 122,    153, 154,    99, 263,    153, 122,   154, 122,   130, 122,   155, 122,   157, 122,
        60, 150,     82, 143
    ]

    def __init__(self, game_engine):
        self.engine = game_engine

    # ===== 辅助方法 =====

    def _get_ex_talent(self, char, idx: int) -> int:
        """获取 EX_TALENT 值"""
        store = getattr(char, 'ex_talent', None)
        if not isinstance(store, dict):
            return 0
        return int(store.get(idx, 0))

    def _set_ex_talent(self, char, idx: int, value: int) -> None:
        """设置 EX_TALENT 值"""
        store = getattr(char, 'ex_talent', None)
        if not isinstance(store, dict):
            store = {}
            setattr(char, 'ex_talent', store)
        store[idx] = max(0, int(value))

    def _get_flag(self, idx: int, default: int = 0) -> int:
        """获取 FLAG 值"""
        return self.engine.interpreter.vars.flags.get(idx, default)

    def _get_flag_bit(self, flag_idx: int, bit: int) -> bool:
        """获取 FLAG 的某一位"""
        value = self._get_flag(flag_idx, 0)
        return bool(value & (1 << bit))

    def _get_master(self) -> int:
        """获取 MASTER 角色索引"""
        return self.engine.interpreter.vars.master

    def _get_chars(self):
        """获取角色列表"""
        return self.engine.interpreter.vars.chars

    def _get_char(self, idx: int):
        """获取指定索引的角色"""
        chars = self._get_chars()
        if 0 <= idx < len(chars):
            return chars[idx]
        return None

    def _get_day(self, idx: int = 0) -> int:
        """获取 DAY 值"""
        return self.engine.interpreter.vars.day[idx]

    def _inrange(self, val, lo, hi) -> bool:
        """INRANGE 判定"""
        return lo <= val <= hi

    # ===== 主流程 =====

    def create_character(self, char_idx: int, personality: int = 0, race: int = 0) -> None:
        """完整的角色创建流程 (对应 @CHARA_MAKE)

        ARG:1 = personality (性格设定)
        ARG:2 = race (种族设定)
        """
        char = self._get_chars()[char_idx]

        # 性别（后代不设定性别）
        if not self._get_ex_talent(char, 2):
            self._cm_gender(char)

        # 命名（后代不命名）
        if not self._get_ex_talent(char, 2):
            self._chara_name_random_define(char_idx)

        # Level・经验值设定
        char.cflag[9] = 1
        char.exp[80] = 0

        # 家族初期化
        char.cflag[605] = 0

        # 卖春への积極性
        char.cflag[120] = 1

        # 根据精英/后代标志分支
        is_elite_talent = char.talent.get(220, 0) == 1
        is_ex_talent_elite = self._get_ex_talent(char, 1) == 1
        is_descendant = self._get_ex_talent(char, 2) == 1

        if not is_elite_talent and not is_ex_talent_elite and not is_descendant:
            # 侵攻楼层
            self._cm_stp(char)
            # 职业、基础
            self._cm_base(char)
            # 勇者初始等级
            self._cm_st(char_idx)
        elif not is_descendant:
            # 初始位置
            char.cflag[1] = 0
            # 职业、基础
            self._cm_base(char)
            # 精英部下初始等级
            self._cm_st_ace(char_idx)
        else:
            # 后代
            # 初始位置
            char.cflag[1] = 0
            # 职业、基础
            self._cm_base(char)

        # 口上性格
        char_no = char.template_id if char.template_id is not None else -1
        if self._inrange(char_no, 1, 16) or self._inrange(char_no, 200, 211):
            self._cm_kj(char, personality)

        # 初心者的烙印
        if self._get_day(0) <= 60:
            char.talent[291] = 1

        # 处女
        self._cm_virgin(char_idx)

        # 素质
        self._cm_talent(char)

        # 战术技能
        self._cm_skill(char)

        # 外貌
        self._cm_look(char_idx, race)
        # 后代：阴毛状态 = 2
        if self._get_ex_talent(char, 2):
            char.talent[311] = 2

        # 善恶
        self._cm_kind(char)

        # 妊娠性交经验（后代不设定）
        if not self._get_ex_talent(char, 2):
            self._cm_ns_exp(char_idx)

        # 家族设定（后代不设定家族）
        if random.randint(0, 3) == 0 and not self._get_ex_talent(char, 2):
            self._family_register(char_idx)

        # 根据家族成员继承素质
        self._cm_family_talent(char_idx)

        # 服装
        self._cm_cloth(char)

        # 一人称の設定
        self._random_self_call(char_idx)

        # 年齢or身長などを表示する設定の場合は身体データを設定
        if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
            self._char_body_generate_wrapped(char_idx)

    # ===== 性别设定 =====

    def _cm_gender(self, char) -> None:
        """性别设定 (对应 @CM_GENDER)"""
        if random.randint(0, 59) == 0:
            char.talent[121] = 1  # 扶她
        elif random.randint(0, 5) == 0 and self._get_flag_bit(8, 0):
            char.talent[122] = 1  # 男人

    # ===== 侵攻楼层设定 =====

    def _cm_stp(self, char) -> None:
        """侵攻楼层设定 (对应 @CM_STP)"""
        char.cflag[501] = 1
        char.cflag[502] = 0
        char.cflag[1] = 2
        char.cflag[508] = 3

    # ===== 职业基础参数设定 =====

    def _cm_base(self, char) -> None:
        """职业基础参数设定 (对应 @CM_BASE)"""
        if char.talent.get(200, 0) or char.talent.get(205, 0):  # 战士/骑士
            char.cflag[11] = 20
            char.cflag[12] = 20
            char.cflag[13] = 20
            char.cflag[14] = 20
        elif char.talent.get(201, 0) or char.talent.get(206, 0):  # 魔法师/巫女
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15
        elif char.talent.get(202, 0) or char.talent.get(207, 0):  # 神官/忍者
            char.cflag[11] = 15
            char.cflag[12] = 20
            char.cflag[13] = 15
            char.cflag[14] = 20
        elif char.talent.get(203, 0) or char.talent.get(208, 0):  # 盗贼/弓手
            char.cflag[11] = 20
            char.cflag[12] = 15
            char.cflag[13] = 20
            char.cflag[14] = 15
        elif char.talent.get(220, 0):  # 精英
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15
        else:
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15

        # 神官和巫女有治癒技能 / 战士和骑士有鼓舞技能
        if char.talent.get(202, 0) == 1 or char.talent.get(206, 0) == 1:
            char.talent[117] = 1
            char.cflag[152] = 20
        elif char.talent.get(200, 0) == 1 or char.talent.get(205, 0) == 1:
            char.talent[118] = 1

        # 怪物种族加成 (种族2 = TALENT:319)
        race2 = char.talent.get(319, 0)
        if race2 == 2:  # 史莱姆
            char.cflag[12] += 5
            char.cflag[14] += 5
        elif race2 == 5:  # 触手
            char.cflag[11] += 5
            char.cflag[13] += 5
        elif race2 == 6:  # 妖精
            char.cflag[11] -= 4
            char.cflag[12] -= 4
            char.cflag[13] -= 4
            char.cflag[14] -= 4
        elif race2 == 7:  # 巨人
            char.cflag[11] += 5
            char.cflag[12] += 5
            char.cflag[13] += 5
            char.cflag[14] += 5

        # 精英有魔の刻印 / 神官巫女有治癒 / 战士骑士有鼓舞（二次检查）
        if char.talent.get(220, 0):
            char.talent[254] = 1
        elif char.talent.get(202, 0) or char.talent.get(206, 0):
            char.talent[117] = 1
        elif char.talent.get(200, 0) == 1 or char.talent.get(205, 0) == 1:
            char.talent[118] = 1

    # ===== 勇者初始等级 =====

    def _cm_st(self, char_idx: int) -> None:
        """勇者初始等级 (对应 @CM_ST)"""
        char = self._get_chars()[char_idx]
        flag60 = self._get_flag(60, 0)
        flag402 = self._get_flag(402, 0)

        if flag60 > 0 and flag402 == 0:
            for _ in range(flag60):
                self._st_up(char_idx)

        # HP/MP 设为最大值
        char.base[0] = char.maxbase.get(0, 0)
        char.base[1] = char.maxbase.get(1, 0)

    def _st_up(self, char_idx: int) -> None:
        """等级提升 (对应 @ST_UP)"""
        char = self._get_chars()[char_idx]
        char.cflag[9] = char.cflag.get(9, 0) + 1
        char.cflag[13] = char.cflag.get(13, 0) + 1
        char.cflag[14] = char.cflag.get(14, 0) + 1
        # 随机额外加成
        r = random.randint(0, 1)
        if r == 0:
            char.cflag[13] += 1
        else:
            char.cflag[14] += 1

    # ===== 精英初始等级 =====

    def _cm_st_ace(self, char_idx: int) -> None:
        """精英部下初始等级 (对应 @CM_ST_ACE)"""
        char = self._get_chars()[char_idx]
        flag60 = self._get_flag(60, 0)
        master_idx = self._get_master()
        master = self._get_char(master_idx)

        if master is not None and flag60 > 0 and master.cflag.get(9, 0) > 2:
            master_level = master.cflag.get(9, 0)
            local = master_level * 6
            local += random.randint(0, master_level - 1) * 2
            local //= 10
            for _ in range(local):
                self._st_up(char_idx)

    # ===== 口上性格设定 =====

    def _cm_kj(self, char, personality: int = 0) -> None:
        """口上性格设定 (对应 @CM_KJ)"""
        for i in range(160, 180):
            char.talent[i] = 0

        if 160 <= personality <= 180:
            char.talent[personality] = 1
        else:
            while True:
                x = random.randint(0, 8) + 160

                # ユニークは除外
                if x == 165:
                    continue
                # オトコなら悪女なれない
                if char.talent.get(122, 0) and x == 166:
                    continue
                # 高貴のオトコならきっと貴公子です
                if char.talent.get(122, 0) and x == 163:
                    x = 174
                if x == 167:
                    x = 175
                if 168 <= x <= 169:
                    x += 5
                    # 女で貴公子？いえ、高貴の女だわ
                    if char.talent.get(122, 0) == 0 and x == 174:
                        x = 163
                char.talent[x] = 1
                break

    # ===== 处女设定 =====

    def _cm_virgin(self, char_idx: int) -> None:
        """处女设定 (对应 @CM_VIRGIN)"""
        char = self._get_chars()[char_idx]
        is_male = char.talent.get(122, 0) == 1
        is_futa = char.talent.get(121, 0) == 1
        is_descendant = self._get_ex_talent(char, 2) == 1

        if is_male:
            char.talent[0] = 0
            if random.randint(0, 2) > 0:
                char.talent[1] = 1
                char.cflag[15] = -1
                char.cflag[16] = -1
            else:
                char.cflag[15] = 0
                char.cflag[16] = 0
        elif is_descendant:
            char.talent[0] = 1
            char.cflag[16] = -1
        elif is_futa:
            # 扶她处女
            if random.randint(0, 7) != 0:
                char.talent[0] = 1
            # 扶她初吻&童贞
            if random.randint(0, 2) > 0:
                char.talent[1] = 1
                char.cflag[16] = -1
            else:
                char.cflag[16] = 0
            # 扶她初体验
            if char.talent.get(0, 0) and char.talent.get(1, 0):
                char.cflag[15] = -1
            elif char.talent.get(0, 0) == 0 or char.talent.get(1, 0) == 0:
                char.cflag[15] = 0
        elif self._get_flag(82, 0) == 1 and random.randint(0, 1) == 0:
            char.talent[0] = 1
            char.cflag[16] = -1
        elif random.randint(0, 7) != 0:
            char.talent[0] = 1
            char.cflag[16] = -1

        # 处女の場合初吻はまだ
        if char.talent.get(0, 0) == 1:
            char.cflag[16] = -1

        # 处女の場合ランダムで贞操封印を行う
        if char.talent.get(0, 0) == 1 and random.randint(0, 4) == 0 and char.talent.get(220, 0) != 1:
            char.talent[273] = 1

        # 人妻
        if random.randint(0, 11) == 0 and char.talent.get(122, 0) == 0 and not is_descendant:
            char.talent[157] = 1
            char.talent[0] = 0

    # ===== 素质随机生成 =====

    def _cm_talent(self, char) -> None:
        """素质随机生成 (对应 @CM_TALENT)"""
        # 胆怯/刚强/文静
        x = random.randint(0, 2)
        if x == 0 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[10] = 1
        elif x == 1 and (char.talent.get(161, 0) or char.talent.get(163, 0) or
                         char.talent.get(164, 0) or char.talent.get(166, 0) or
                         char.talent.get(174, 0) or char.talent.get(175, 0)):
            char.talent[12] = 1
        elif x == 2 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[14] = 1

        # 反抗心/坦率/嚣张
        x = random.randint(0, 11)
        if x == 0:
            char.talent[11] = 1
            if random.randint(0, 7) == 0:
                char.talent[18] = 1
        elif x == 1:
            char.talent[13] = 1
        elif x == 2 and (char.talent.get(161, 0) or char.talent.get(163, 0) or
                         char.talent.get(164, 0) or char.talent.get(166, 0) or
                         char.talent.get(174, 0) or char.talent.get(175, 0)):
            char.talent[16] = 1

        # 高姿态/低姿态/傲娇
        x = random.randint(0, 11)
        if x == 0:
            char.talent[15] = 1
        elif x == 1 and char.talent.get(18, 0) == 0:
            char.talent[17] = 1
        elif x == 2 and char.talent.get(18, 0) == 0:
            char.talent[18] = 1

        # 克制/冷漠/感情淡薄/好奇心/献身的
        x = random.randint(0, 15)
        if x == 0:
            char.talent[21] = 1
        elif x == 1:
            char.talent[23] = 1
        elif x == 2:
            char.talent[22] = 1
        elif x == 3:
            char.talent[20] = 1
        elif x == 4:
            char.talent[63] = 1

        # 保守的/乐观的/悲观的
        x = random.randint(0, 11)
        if x == 0:
            char.talent[24] = 1
        elif x == 1:
            char.talent[25] = 1
        elif x == 2:
            char.talent[26] = 1

        # 戒备森严/爱表现
        x = random.randint(0, 7)
        if x == 0:
            char.talent[27] = 1
        elif x == 1:
            char.talent[28] = 1

        # 看重贞操/看轻贞操
        x = random.randint(0, 11)
        if x == 0:
            char.talent[30] = 1
        elif x == 1:
            char.talent[31] = 1

        # 压抑/开放
        x = random.randint(0, 11)
        if x == 0:
            char.talent[32] = 1
        elif x == 1:
            char.talent[33] = 1

        # 抵抗
        if random.randint(0, 11) == 0:
            char.talent[34] = 1

        # 害羞/不知羞耻
        x = random.randint(0, 11)
        if x == 0:
            char.talent[35] = 1
        elif x == 1:
            char.talent[36] = 1

        # 把柄
        if random.randint(0, 7) == 0:
            char.talent[37] = 1

        # 害怕疼痛/不惧疼痛
        x = random.randint(0, 11)
        if x == 0:
            char.talent[40] = 1
        elif x == 1:
            char.talent[41] = 1

        # 容易湿/不易湿
        x = random.randint(0, 11)
        if x == 0:
            char.talent[42] = 1
        elif x == 1:
            char.talent[43] = 1

        # 眼镜
        if random.randint(0, 11) == 0:
            char.talent[48] = 1

        # 快速学习/学习缓慢
        x = random.randint(0, 11)
        if x == 0:
            char.talent[50] = 1
        elif x == 1:
            char.talent[51] = 1

        # 擅用舌头
        if random.randint(0, 7) == 0:
            char.talent[52] = 1

        # 漏尿癖
        if random.randint(0, 49) == 0:
            char.talent[57] = 1

        # 容易自慰
        if random.randint(0, 7) == 0:
            char.talent[60] = 1

        # 不怕污臭/反感污臭
        x = random.randint(0, 11)
        if x == 0:
            char.talent[61] = 1
        elif x == 1:
            char.talent[62] = 1

        # 接受快感/否定快感
        x = random.randint(0, 11)
        if x == 0:
            char.talent[70] = 1
        elif x == 1:
            char.talent[71] = 1

        # 容易上瘾
        if random.randint(0, 7) == 0:
            char.talent[72] = 1

        # 容易陷落
        if random.randint(0, 29) == 0:
            char.talent[73] = 1

        # 抵抗诱惑
        if random.randint(0, 29) == 0:
            char.talent[69] = 1

        # 倒错的
        if random.randint(0, 7) == 0:
            char.talent[80] = 1

        # 双性恋/讨厌男人
        x = random.randint(0, 11)
        if x == 0:
            char.talent[81] = 1
        elif x == 1:
            char.talent[82] = 1

        # 抖S/抖M气质
        x = random.randint(0, 7)
        if x == 0:
            char.abl[20] = 3
        elif x == 1:
            char.abl[21] = 3

        # 嫉妒
        if random.randint(0, 9) == 0:
            char.talent[84] = 1

        # 小恶魔
        if random.randint(0, 7) == 0:
            char.talent[87] = 1

        # 露出癖
        if random.randint(0, 39) == 0:
            char.abl[17] = 3

        # 魅惑
        if random.randint(0, 19) == 0:
            char.talent[91] = 1

        # 魁梧/娇小 (种族2 = TALENT:319)
        x = random.randint(0, 11)
        race2 = char.talent.get(319, 0)
        if race2 == 7:
            if x <= 8:
                char.talent[99] = 1
            elif x == 11:
                char.talent[100] = 1
        else:
            if x == 0:
                char.talent[99] = 1
            elif x == 1:
                char.talent[100] = 1

        # 阴蒂钝感/敏感
        x = random.randint(0, 11)
        if x == 0:
            char.talent[101] = 1
        elif x == 1:
            char.talent[102] = 1

        # 私处钝感/敏感 (仅女性)
        x = random.randint(0, 11)
        if char.talent.get(122, 0) == 0:
            if x == 0:
                char.talent[103] = 1
            elif x == 1:
                char.talent[104] = 1

        # 肛门钝感/敏感
        x = random.randint(0, 11)
        if x == 0:
            char.talent[105] = 1
        elif x == 1:
            char.talent[106] = 1

        # 乳房钝感/敏感
        x = random.randint(0, 11)
        if x == 0:
            char.talent[107] = 1
        elif x == 1:
            char.talent[108] = 1

        # 超乳/爆乳/绝壁/贫乳/巨乳 (仅女性)
        if char.talent.get(122, 0) == 0:
            if random.randint(0, 49) == 0:
                char.talent[119] = 1
            elif random.randint(0, 24) == 0:
                char.talent[114] = 1
            elif random.randint(0, 23) == 0:
                char.talent[116] = 1
            elif random.randint(0, 7) == 0:
                char.talent[109] = 1
            elif random.randint(0, 6) == 0:
                char.talent[110] = 1

        # 快速回复/回复缓慢
        x = random.randint(0, 11)
        if x == 0:
            char.talent[111] = 1
        elif x == 1:
            char.talent[112] = 1

        # 魅力
        if random.randint(0, 7) == 0:
            char.talent[113] = 1

        # 早泄 (男性/扶她)
        if random.randint(0, 24) == 0 and (char.talent.get(122, 0) or char.talent.get(121, 0)):
            char.talent[133] = 1

        # 软弱 (慈爱/懦弱)
        if random.randint(0, 5) == 0 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[134] = 1

        # 未熟
        if random.randint(0, 11) == 0:
            char.talent[135] = 1
            if random.randint(0, 7) == 0:
                char.talent[132] = 1
            if random.randint(0, 7) == 0 and (char.talent.get(122, 0) or char.talent.get(121, 0)):
                char.talent[133] = 1

        # 各种情结
        x = random.randint(0, 99)
        if char.talent.get(122, 0):
            # 男人
            if x < 4:
                char.talent[140] = 1
            elif x < 8:
                char.talent[142] = 1
            elif x < 10:
                char.talent[141] = 1
            elif x < 12:
                char.talent[143] = 1
        elif char.talent.get(121, 0):
            # 扶她
            if x < 3:
                char.talent[140] = 1
            elif x < 6:
                char.talent[142] = 1
            elif x < 9:
                char.talent[141] = 1
            elif x < 12:
                char.talent[143] = 1
        else:
            # 女性
            if x < 4:
                char.talent[141] = 1
            elif x < 8:
                char.talent[143] = 1
            elif x < 10:
                char.talent[140] = 1
            elif x < 12:
                char.talent[142] = 1

        # 不受洗脑
        if random.randint(0, 29) == 0:
            char.talent[152] = 1

        # 担保人
        if char.talent.get(37, 0) and random.randint(0, 3) == 0:
            char.talent[290] = 1
        elif random.randint(0, 11) == 0:
            char.talent[290] = 1

    # ===== 战术技能设定 =====

    def _cm_skill(self, char) -> None:
        """战术技能设定 (对应 @CM_SKILL)"""
        race2 = char.talent.get(319, 0)

        # 战术
        if random.randint(0, 39) == 0:
            char.talent[240] = 1

        # 魔术
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[241] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[241] = 1

        # 法术
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[242] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[242] = 1

        # 奇袭
        if random.randint(0, 39) == 0:
            char.talent[243] = 1

        # 肌肉型/虚弱
        if race2 == 7:
            if random.randint(0, 9) == 0:
                char.talent[248] = 1
        elif random.randint(0, 29) == 0:
            char.talent[248] = 1
        elif random.randint(0, 28) == 0:
            char.talent[256] = 1

        # 铁壁
        if random.randint(0, 39) == 0:
            char.talent[249] = 1

        # 咒术
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[250] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[250] = 1

        # 忍术
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[251] = 1
        else:
            if random.randint(0, 29) == 0:
                char.talent[251] = 1

        # 先制
        if random.randint(0, 39) == 0:
            char.talent[252] = 1

        # 褐色/白皙
        if random.randint(0, 11) == 0:
            char.talent[253] = 1
        elif random.randint(0, 10) == 0:
            char.talent[255] = 1
        elif race2 == 8 or race2 == 9:
            if random.randint(0, 9) == 0:
                char.talent[244] = 1

        # 魔法耐性
        if random.randint(0, 39) == 0:
            char.talent[257] = 1

        # 妖精如果没有任何术则获得魔法耐性
        if race2 == 6 and not char.talent.get(241, 0) and not char.talent.get(242, 0) and \
           not char.talent.get(250, 0) and not char.talent.get(251, 0):
            char.talent[257] = 1

        # 俊足
        if random.randint(0, 39) == 0:
            char.talent[258] = 1

        # 独眼/额头天眼
        if random.randint(0, 59) == 0:
            char.talent[259] = 1
        elif random.randint(0, 58) == 0:
            char.talent[260] = 1

        # 能力者技能
        # 火之能力者
        if random.randint(0, 39) == 0:
            char.talent[275] = 1
        # 冰之能力者
        if random.randint(0, 39) == 0:
            char.talent[276] = 1
        # 雷之能力者
        if random.randint(0, 39) == 0:
            char.talent[277] = 1
        # 光之能力者
        if random.randint(0, 39) == 0:
            char.talent[278] = 1
        # 暗之能力者
        if random.randint(0, 39) == 0:
            char.talent[279] = 1

        # 額の目の場合、闇チャンス2回目
        if char.talent.get(260, 0) == 1 and random.randint(0, 39) == 0:
            char.talent[279] = 1

        # 冲突检查
        self._cmi_conflict_check(char)

    def _cmi_conflict_check(self, char) -> None:
        """冲突检查 (对应 @CMI_CONFLICT_CHECK)"""
        pairs = self.CONFLICT_PAIRS
        for ii in range(len(pairs) // 2):
            i = pairs[ii * 2]
            j = pairs[ii * 2 + 1]
            if char.talent.get(i, 0) and char.talent.get(j, 0):
                if random.randint(0, 1):
                    char.talent[i] = 0
                else:
                    char.talent[j] = 0

    # ===== 外貌设定 =====

    def _cm_look(self, char_idx: int, race: int = 0) -> None:
        """外貌设定 (对应 @CM_LOOK)"""
        char = self._get_chars()[char_idx]

        # 调用 LOOK_SET
        self._look_set(char, race)

        # 白虎
        if random.randint(0, 19) == 0:
            char.talent[125] = 1
            char.talent[310] = 5   # 阴毛状态 = 5 (白虎)
            char.talent[311] = 1

    def _look_set(self, char, race: int = 0) -> None:
        """外貌详细设定 (对应 @LOOK_SET)"""
        # 头发颜色
        if char.talent.get(300, 0) > 0:
            pass  # 已设定
        else:
            q = random.randint(0, 99)
            if q <= 4:
                char.talent[300] = 11   # 粉
            elif q <= 14:
                char.talent[300] = 8    # 紫
            elif q <= 20:
                char.talent[300] = 9    # 白
            elif q <= 30:
                char.talent[300] = 6    # 青
            elif q <= 40:
                char.talent[300] = 7    # 绿
            elif q <= 50:
                char.talent[300] = 2    # 栗
            elif q <= 60:
                char.talent[300] = 1    # 金
            elif q <= 79:
                char.talent[300] = 3    # 黑
            elif q <= 89:
                char.talent[300] = 4    # 赤
            elif q <= 94:
                char.talent[300] = 10   # 暗金
            else:
                char.talent[300] = 5    # 银

        # 头发状态
        q = random.randint(0, 11)
        if q <= 6:
            char.talent[301] = 1   # 直毛
        elif q == 7:
            char.talent[301] = 2   # カール
        elif q == 8:
            char.talent[301] = 3   # 内カール
        elif q == 9:
            char.talent[301] = 4   # 外カール
        elif q == 10:
            char.talent[301] = 5   # 癖毛
        else:
            char.talent[301] = 6   # ウェーブ

        # 头发长度
        q = random.randint(0, 5)
        if q <= 1 or char.talent.get(135, 0):
            char.talent[302] = 1       # ショート
        elif q == 4:
            char.talent[302] = 101     # セミロング
        else:
            char.talent[302] = 201     # ロング

        # 头发修剪方式
        q = random.randint(0, 5)
        if q >= 2:
            char.talent[303] = 1   # ベーシック
        elif q == 3:
            char.talent[303] = 2   # 切り揃え
        elif q == 4:
            char.talent[303] = 3   # レイヤー
        else:
            char.talent[303] = 4   # シャギー

        # 髪型
        hair_len = char.talent.get(302, 0)
        if 1 <= hair_len <= 100:
            q = random.randint(0, 2)
        elif 101 <= hair_len <= 200:
            q = random.randint(0, 9)
        else:
            q = random.randint(0, 11)
        char.talent[304] = q + 1

        # 目
        q = random.randint(0, 99)
        if q <= 10:
            char.talent[305] = 1   # 切れ長
        elif q <= 20:
            char.talent[305] = 2   # 大きい
        elif q <= 25:
            char.talent[305] = 3   # 神秘的
        elif q <= 35:
            char.talent[305] = 4   # 釣り目
        elif q <= 40:
            char.talent[305] = 5   # 潤み目
        elif q <= 45:
            char.talent[305] = 8   # たれ目
        elif q <= 48:
            char.talent[305] = 7   # 三白眼
        else:
            char.talent[305] = 6   # 標準

        # 瞳色
        q = random.randint(0, 99)
        if q <= 40:
            char.talent[306] = 1   # 碧
        elif q <= 60:
            char.talent[306] = 2   # ブラウン
        elif q <= 80:
            char.talent[306] = 6   # 黒
        elif q <= 97:
            char.talent[306] = 3   # グレー
        elif q <= 98:
            char.talent[306] = 4   # ゴールド
        else:
            char.talent[306] = 5   # クリムゾン

        # 唇
        q = random.randint(0, 5)
        if q == 0:
            char.talent[307] = 1   # 肉感的
        elif q == 1:
            char.talent[307] = 2   # 薄い
        elif q == 2:
            char.talent[307] = 3   # 瑞々しい
        else:
            char.talent[307] = 4   # 標準

        # 体型
        q = random.randint(0, 2)
        if q == 0:
            char.talent[308] = 300  # 丰满
        elif q == 1:
            char.talent[308] = 1    # 骨感
        else:
            char.talent[308] = 150  # 標準

        # 乳头
        q = random.randint(0, 5)
        if q == 0:
            char.talent[309] = 1   # ピンク
        elif q == 1:
            char.talent[309] = 2   # 褐色
        elif q == 2:
            char.talent[309] = 4   # 陥没
        else:
            char.talent[309] = 3   # 標準

        # 陰毛
        q = random.randint(0, 149)
        if q <= 20:
            char.talent[311] = 1       # 無
        elif q <= 45:
            char.talent[311] = 20      # 産毛
        elif q <= 70:
            char.talent[311] = 50      # 薄い
        elif q <= 100:
            char.talent[311] = 100     # 標準
        elif q <= 130:
            char.talent[311] = 150     # 濃い
        else:
            char.talent[311] = 201     # 剛毛
        char.talent[310] = char.talent[311]

        # ペニス
        q = random.randint(0, 149)
        if q <= 50:
            char.talent[318] = 0       # 普通
        elif q <= 100 or (char.talent.get(135, 0) and q <= 50):
            char.talent[318] = 3       # 包茎
        elif q <= 130 or (char.talent.get(135, 0) and q <= 100):
            char.talent[318] = 2       # 短小包茎
        else:
            char.talent[318] = 1       # 巨根

        # 包茎・短小包茎は早漏を得ることがある
        if (char.talent.get(318, 0) == 2 or char.talent.get(318, 0) == 3) and random.randint(0, 9) == 0:
            char.talent[133] = 1

        # 魅力点
        while True:
            q = random.randint(1, 28)
            # 贫乳は美乳になれない
            if char.talent.get(109, 0) and q == 12:
                continue
            # 自前のペニス持ちなら追加のふたなり獲得チャンス
            if q == 24:
                if random.randint(0, 39) == 0 and char.talent.get(122, 0) == 0:
                    char.talent[121] = 1
                if char.talent.get(121, 0) == 0 and char.talent.get(122, 0) == 0:
                    continue
            break
        char.talent[312] = q

        # 癖
        while True:
            q = random.randint(1, 34)
            # 話せないなら決め台詞はありえない
            if char.talent.get(167, 0) and q == 25:
                continue
            break
        char.talent[313] = q

        # 种族设定
        if char.talent.get(220, 0) != 1:
            # 非精英
            q = random.randint(0, 199)
            if (race == 0 and q <= 99) or race == -1:
                char.talent[314] = 0    # 人間
            elif (race == 0 and q <= 119) or race == 10:
                char.talent[314] = 10   # ホビット
                char.talent[100] = 1
                if char.talent.get(122, 0) == 0:
                    char.talent[109] = 1
                # ホビットには巨乳と大柄は付かない
                char.talent[116] = 0
                char.talent[114] = 0
                char.talent[119] = 0
                char.talent[110] = 0
                char.talent[99] = 0
                if random.randint(0, 9) <= 3:
                    char.talent[311] = 1
                    char.talent[310] = 1
            elif (race == 0 and q <= 139) or race == 11:
                char.talent[314] = 11   # ドワーフ
                char.talent[100] = 1
                if char.talent.get(122, 0) == 0:
                    char.talent[109] = 1
                char.talent[116] = 0
                char.talent[114] = 0
                char.talent[119] = 0
                char.talent[110] = 0
                char.talent[99] = 0
                if random.randint(0, 9) <= 3:
                    char.talent[311] = 201
                    char.talent[310] = 201
            elif (race == 0 and q <= 159) or race == 1:
                char.talent[314] = 1    # エルフ
                self._karma(char, 20)
            elif (race == 0 and q <= 169) or race == 2:
                char.talent[314] = 2    # 人狼
                char.talent[124] = 1
                self._karma(char, -20)
            elif (race == 0 and q <= 179) or race == 3:
                char.talent[314] = 3    # 吸血鬼
                self._karma(char, -40)
            elif (race == 0 and q <= 189) or race == 4:
                char.talent[314] = 4    # 无头骑士
                if random.randint(0, 39) == 0:
                    char.talent[279] = 1
                self._karma(char, -40)
            elif (race == 0 and q <= 197) or race == 5:
                char.talent[314] = 5    # ドラゴン
                char.talent[264] = 1
            elif race:
                char.talent[314] = race  # その他指定の種族
            else:
                char.talent[314] = 6    # 天使
                if random.randint(0, 39) == 0:
                    char.talent[278] = 1
                self._karma(char, 40)
        else:
            # 精英
            char.talent[314] = 9
            talent319 = char.talent.get(319, 0)
            if talent319 == 1:
                # 亜人
                if random.randint(0, 3) == 0:
                    char.talent[472] = 1
                if random.randint(0, 9) <= 3:
                    char.talent[311] = 201
                    char.talent[310] = 201
            elif talent319 == 2:
                # 史莱姆
                char.talent[261] = 1
                if random.randint(0, 3) == 0:
                    char.talent[471] = 1
                char.talent[311] = 1
                char.talent[310] = 1
            elif talent319 == 3:
                # 昆虫
                char.talent[240] = 1
                if random.randint(0, 3) == 0:
                    char.talent[474] = 1
            elif talent319 == 4:
                # 植物
                if random.randint(0, 9) == 0:
                    char.talent[262] = 1
                if random.randint(0, 3) == 0:
                    char.talent[473] = 1
            elif talent319 == 5 or talent319 == 11:
                # 触手＆脑奸
                char.talent[262] = 1
                if random.randint(0, 3) == 0:
                    char.talent[476] = 1
            elif talent319 == 6:
                # 妖精
                char.talent[263] = 1
                char.talent[99] = 0
                char.talent[100] = 0
                if random.randint(0, 3) == 0:
                    char.talent[478] = 1
                if random.randint(0, 3) != 0:
                    char.talent[132] = 1
                if random.randint(0, 9) <= 3:
                    char.talent[311] = 1
                    char.talent[310] = 1
            elif talent319 == 7:
                # 巨人
                char.talent[99] = 1   # 魁梧
                char.talent[100] = 0  # not 娇小
            elif talent319 == 8 or talent319 == 9:
                # 男＆女魔族
                char.talent[245] = 1
                char.talent[246] = 1
                char.talent[247] = 1
                if random.randint(0, 3) == 0:
                    if talent319 == 8:
                        char.talent[485] = 1
                    else:
                        char.talent[481] = 1
            elif talent319 == 10 or talent319 == 12:
                # 獣＆馬
                char.talent[244] = 0
                char.talent[253] = 0
                char.talent[255] = 0
                char.talent[137] = 1
                char.talent[258] = 1
                char.talent[124] = 1
                if random.randint(0, 3) == 0:
                    char.talent[479] = 1

        # 后代种族2设定
        if self._get_ex_talent(char, 2):
            char.talent[300] = 2

    def _karma(self, char, amount: int) -> None:
        """善恶值变动 (对应 @KARMA)"""
        if char.talent.get(254, 0):  # 魂缚
            return
        char.cflag[151] = char.cflag.get(151, 0) + amount
        if char.cflag[151] > 200:
            char.cflag[151] = 200
        if char.cflag[151] < -200:
            char.cflag[151] = -200

    # ===== 善恶值设定 =====

    def _cm_kind(self, char) -> None:
        """善恶值设定 (对应 @CM_KIND)"""
        # 善人
        if char.talent.get(160, 0) or char.talent.get(173, 0):
            char.cflag[3] = random.randint(0, 29) + 40   # 40-69
        # 悪人
        elif char.talent.get(166, 0) or char.talent.get(87, 0):
            char.cflag[3] = -(random.randint(0, 29) + 40)  # -69 to -40
        # 高貴・貴公子
        elif char.talent.get(163, 0) or char.talent.get(174, 0):
            char.cflag[3] = random.randint(0, 19) + 10   # 10-29
        # 冷静
        elif char.talent.get(164, 0):
            char.cflag[3] = random.randint(0, 39) - 20   # -20 to 19
        # 自信家
        elif char.talent.get(161, 0):
            char.cflag[3] = random.randint(0, 19) - 10   # -10 to 9
        # 懦弱
        elif char.talent.get(162, 0):
            char.cflag[3] = random.randint(0, 19) + 20   # 20-39
        # 伶俐
        elif char.talent.get(175, 0):
            char.cflag[3] = random.randint(0, 29) + 10   # 10-39
        # その他
        else:
            char.cflag[3] = random.randint(0, 59) - 30   # -30 to 29
        # 精英は善人寄り
        if char.talent.get(220, 0):
            char.cflag[3] = abs(char.cflag[3])
        # 狂王の影は悪人寄り
        if char.talent.get(292, 0):
            char.cflag[3] = -abs(char.cflag[3])

    # ===== 妊娠性交经验 =====

    def _cm_ns_exp(self, char_idx: int) -> None:
        """妊娠性交经验 (对应 @CM_NS_EXP)"""
        char = self._get_chars()[char_idx]

        # 出産経験
        p = 0
        local = char.talent.get(320, 0) % 10
        if local == 0 and char.talent.get(157, 0) == 1 and random.randint(0, 1) == 0:
            p += random.randint(0, 2)
        else:
            # 娘の数
            local1 = char.talent.get(320, 0) % 1000
            p += local1 // 100
            # 息子の数
            local1 = char.talent.get(320, 0) % 10000
            p += local1 // 1000

        char.exp[60] = char.exp.get(60, 0) + p

        # 性交経験
        if char.talent.get(0, 0) == 0:  # 非处女
            char.exp[0] = random.randint(0, 7) + 1 + p
            char.exp[5] = char.exp[0]
        elif p:
            # 処女であるのに出産経験がある
            char.exp[0] = random.randint(0, 3) + 1 + p
            char.exp[5] = char.exp[0]
            # 処女を消す
            char.talent[0] = 0

        # 自慰经验
        if random.randint(0, 29) == 0:
            # たまに猿みたいなオナニストが出現
            char.exp[10] = random.randint(0, 49)
        elif char.talent.get(121, 0) == 1 or char.talent.get(122, 0) == 1:
            # 扶她・男人は自慰しちゃうよね
            char.exp[10] = random.randint(0, 29)
        elif char.talent.get(60, 0) == 1:
            # 容易自慰
            char.exp[10] = random.randint(0, 19)
        elif random.randint(0, 9) == 0:
            # 比較的自慰しちゃってる
            char.exp[10] = random.randint(0, 9)

        # ただし善恶值が高いと自慰なんてしない
        if char.cflag.get(151, 0) > 150:
            char.exp[10] = 0

        # オトコにV経験はない
        if char.talent.get(122, 0):
            char.exp[0] = 0

        # 初体験
        self._chara_first_exp(char_idx)

    # ===== 初体验设定 =====

    def _chara_first_exp(self, char_idx: int) -> None:
        """初体验设定 - 对应 @CHARA_FIRST_EXP (完整版)

        涉及：兽奸经验 / 家族婚姻 / 职业 / 不幸事件 / 通用初吻场景
        设定 CFLAG:16(初吻), CFLAG:15(初体验), CSTR:4(初吻对象), CSTR:3(初体验对象)
        """
        char = self._get_chars()[char_idx]
        first_kiss = char.cflag.get(16, 0)
        first_sex = char.cflag.get(15, 0)
        kiss_point = 0
        men_or_girl = 0  # 1=男, 2=女, 3=扶她, 4=随机
        partner_name = ""
        sex_partner_name = ""

        # 非男性且非处女且未设定初体验 → 0(已体验)
        if char.talent.get(122, 0) == 0 and char.talent.get(0, 0) == 0 and first_sex == -1:
            first_sex = 0
        # 有性交或卖春经验且未设定初吻 → 0(已吻过)
        if (char.exp.get(5, 0) > 0 or char.exp.get(74, 0) > 0) and first_kiss == -1:
            first_kiss = 0

        # === 兽奸经验 ===
        if not partner_name and first_kiss == 0 and char.exp.get(56, 0) > 0:
            if random.randint(0, 19) == 0:
                first_kiss = 996  # 野良犬のアナル
                if char.talent.get(0, 0) == 0 and first_sex == 0 and random.randint(0, 1) == 0:
                    first_sex = 103
            elif random.randint(0, 9) == 0:
                first_kiss = 997  # 野良犬のペニス
                if char.talent.get(0, 0) == 0 and first_sex == 0 and random.randint(0, 1) == 0:
                    first_sex = 103
            elif random.randint(0, 4) == 0:
                first_kiss = 998  # 野良犬の口
                if char.talent.get(0, 0) == 0 and first_sex == 0 and random.randint(0, 1) == 0:
                    first_sex = 103

        # === 家族婚姻 ===
        talent_320 = char.talent.get(320, 0)
        family_flag = talent_320 % 10

        if family_flag == 1:
            husband_code = (talent_320 % 100000) // 10000
            soul_code = talent_320 % 10000000000

            if husband_code == 1:  # 已婚
                soul_base = soul_code // 1000000000
                if soul_base in (0, 4, 8):
                    partner_name = "丈夫"; men_or_girl = 1
                elif soul_base in (1, 5, 7):
                    partner_name = "扶她妻子"; men_or_girl = 3
                else:
                    partner_name = "妻子"; men_or_girl = 2
            elif husband_code == 2:  # 离婚
                soul_base = soul_code // 1000000000
                if soul_base in (0, 4, 8):
                    partner_name = "前夫"; men_or_girl = 1
                elif soul_base in (1, 5, 7):
                    partner_name = "前扶她妻子"; men_or_girl = 3
                else:
                    partner_name = "前妻"; men_or_girl = 2
            elif husband_code in (3, 4, 5):
                soul_base = soul_code // 1000000000
                labels = {3: ("丈夫", "扶她妻子", "妻子"),
                          4: ("前夫", "前扶她妻子", "前妻"),
                          5: ("亡夫", "亡妻（扶她）", "亡妻")}
                if soul_base in (0, 4, 8):
                    partner_name = labels[husband_code][0]; men_or_girl = 1
                elif soul_base in (1, 5, 7):
                    partner_name = labels[husband_code][1]; men_or_girl = 3
                else:
                    partner_name = labels[husband_code][2]; men_or_girl = 2

            if not partner_name:
                # 家族成员
                elder_brother = (talent_320 % 10000000) // 1000000
                if elder_brother > 0 and not partner_name and random.randint(0, 19) == 0:
                    partner_name = "亲哥哥"; men_or_girl = 1
                younger_brother = (talent_320 % 1000000000) // 100000000
                if younger_brother > 0 and not partner_name:
                    if random.randint(0, 19) == 0:
                        partner_name = "亲弟弟"; men_or_girl = 1
                    elif char.talent.get(143, 0) and random.randint(0, 4) == 0:
                        partner_name = "亲弟弟"; men_or_girl = 1
                elder_sister = (talent_320 % 1000000) // 100000
                if elder_sister > 0 and not partner_name and random.randint(0, 19) == 0:
                    partner_name = "亲姐姐"; men_or_girl = 2
                younger_sister = (talent_320 % 100000000) // 10000000
                if younger_sister > 0 and not partner_name:
                    if random.randint(0, 19) == 0:
                        partner_name = "亲妹妹"; men_or_girl = 2
                    elif char.talent.get(142, 0) and random.randint(0, 4) == 0:
                        partner_name = "亲妹妹"; men_or_girl = 2
                # 父
                if not partner_name:
                    if random.randint(0, 19) == 0:
                        partner_name = "亲爹"; men_or_girl = 1
                    elif char.talent.get(141, 0) and random.randint(0, 9) == 0:
                        partner_name = "亲爹"; men_or_girl = 1
                # 母
                if not partner_name:
                    if random.randint(0, 19) == 0:
                        partner_name = "亲妈"; men_or_girl = 2
                    elif char.talent.get(140, 0) and random.randint(0, 9) == 0:
                        partner_name = "亲妈"; men_or_girl = 2

            # 随机结婚对象=初吻/初体验
            if not partner_name and first_kiss == 0 and family_flag == 1 and random.randint(0, 1) == 0:
                pass  # LOCs override
            if char.talent.get(0, 0) == 0 and not sex_partner_name and first_sex == 0 and family_flag == 1 and random.randint(0, 1) == 0:
                sex_partner_name = partner_name

        # 故乡的恋人
        if char.talent.get(317, 0) == 4:
            partner_name = "故乡的恋人"
            men_or_girl = 4  # 随机

        # === 职业系初体验 ===
        life_code = char.talent.get(318, 0)  # 成为勇者前的生活
        # life_code: 1=学生 3=农家 4=渔师 6=盗人 8=贵族 15=商人 18=面包屋 19=军人 5=娼妇 20=奴隶

        is_male = char.talent.get(122, 0)
        is_futa = char.talent.get(121, 0)

        if not partner_name and first_kiss == 0:
            r = random.randint(0, 99)
            if is_male:
                partner_name = self._pick_partner_male(life_code)
                men_or_girl = 2
                if life_code in (5, 20):
                    if r < 33: kiss_point = 301  # ヴァギナ
                    elif r < 66: kiss_point = 401  # アナル
            elif is_futa:
                partner_name = self._pick_partner_futa(life_code)
                men_or_girl = 2
                if life_code in (5, 20):
                    if r < 33: kiss_point = 301
                    elif r < 66: kiss_point = 401
            else:  # 女性
                partner_name = self._pick_partner_female(life_code)
                men_or_girl = 1
                if life_code in (5, 20):
                    if r < 33: kiss_point = 101  # ペニス
                    elif r < 66: kiss_point = 401

        # 随机结婚对象=初吻
        if not partner_name and first_kiss == 0 and random.randint(0, 1) == 0:
            pass
        if char.talent.get(0, 0) == 0 and not sex_partner_name and first_sex == 0 and random.randint(0, 1) == 0:
            sex_partner_name = partner_name

        # === 不幸なキス ===
        if not partner_name and first_kiss == 0:
            r = random.randint(0, 99)
            if is_male or is_futa:
                partner_name = self._pick_unfortunate_male()
                men_or_girl = 2
                if r < 33: kiss_point = 301
                elif r < 66: kiss_point = 401
            else:
                partner_name = self._pick_unfortunate_female()
                men_or_girl = 1
                if r < 33: kiss_point = 101
                elif r < 66: kiss_point = 401

        if not partner_name and first_kiss == 0 and random.randint(0, 2) == 0:
            pass
        if kiss_point > 0 and partner_name and first_kiss == 0:
            first_kiss = kiss_point
        if char.talent.get(0, 0) == 0 and not sex_partner_name and first_sex == 0 and random.randint(0, 2) == 0:
            sex_partner_name = partner_name

        # === 谁都有过的初吻 ===
        if not partner_name and first_kiss == 0:
            if is_male or is_futa:
                partner_name = random.choice(["青梅竹马", "女朋友", "初恋"])
                men_or_girl = 2
            else:
                partner_name = random.choice(["青梅竹马", "男朋友", "初恋"])
                men_or_girl = 1

        # 初吻确定
        if not partner_name and first_kiss == 0:
            pass  # forces overwrite
        if char.talent.get(0, 0) == 0 and not sex_partner_name and first_sex == 0:
            sex_partner_name = partner_name

        if sex_partner_name and first_sex == 0:
            first_sex = 100

        # === MEN_OR_GIRL 随机解析 ===
        if men_or_girl == 4:
            r = random.randint(0, 99)
            if is_futa:
                if r < 10: men_or_girl = 2
                elif r < 50: men_or_girl = 3
                else: men_or_girl = 1
            elif is_male:
                if r < 5: men_or_girl = 1
                elif r < 12: men_or_girl = 3
                else: men_or_girl = 1
            else:  # female
                if r < 5: men_or_girl = 2
                elif r < 12: men_or_girl = 3
                else: men_or_girl = 1

        # 性别矛盾清除
        if first_kiss >= 100 and first_kiss < 300 and men_or_girl == 2:
            first_kiss = 0
        if first_kiss >= 300 and first_kiss < 400 and men_or_girl == 1:
            first_kiss = 0

        # 初吻部位确定 (0=唇1, 肛门401, 阴茎101, 阴道301)
        if partner_name and first_kiss == 0:
            r = random.randint(0, 29)
            if r > 0:
                first_kiss = 1  # 唇
            elif random.randint(0, 2) == 0:
                first_kiss = 401  # 肛门
            elif men_or_girl == 1:
                first_kiss = 101  # 阴茎
            elif men_or_girl == 2:
                first_kiss = 301  # 阴道
            elif men_or_girl == 3:
                first_kiss = 101 if random.randint(0, 1) == 0 else 301

        # 初次体验默认值
        if first_kiss == 0:
            first_kiss = 1
        if char.talent.get(0, 0) == 0 and first_sex == 0:
            first_sex = 100

        char.cflag[16] = first_kiss
        char.cflag[15] = first_sex
        if hasattr(char, 'cstr'):
            char.cstr[4] = partner_name if partner_name else ""
            char.cstr[3] = sex_partner_name if sex_partner_name else ""

    def _pick_partner_male(self, life_code: int) -> str:
        return self._pick_partner_by_occupation(life_code, "male")

    def _pick_partner_futa(self, life_code: int) -> str:
        return self._pick_partner_by_occupation(life_code, "futa")

    def _pick_partner_female(self, life_code: int) -> str:
        return self._pick_partner_by_occupation(life_code, "female")

    def _pick_partner_by_occupation(self, life_code: int, gender: str) -> str:
        """按职业返回可能的初吻对象名"""
        r = random.randint(0, 99)
        if life_code == 1:  # 学生
            if r < 25: return "学校的后辈"
            if r < 50: return "学校的先辈"
            if r < 75: return "女教师" if gender != "female" else "教师"
            return "同级生"
        elif life_code == 3:  # 农家
            return "农妇" if gender != "female" else "农夫"
        elif life_code == 4:  # 渔师
            return "港口的娼妇" if gender != "female" else "渔民"
        elif life_code == 6:  # 盗人
            return "街边的娼妇" if gender != "female" else "流氓"
        elif life_code == 8:  # 贵族
            if r < 5: return "家庭教师"
            if r < 10: return "小女仆" if gender != "female" else "佣人"
            return "家庭教师"
        elif life_code == 15:  # 商人
            if r < 33: return "女上司" if gender != "female" else "上司"
            if r < 66: return "客户"
            return "熟客"
        elif life_code == 18:  # 面包屋
            return "熟客"
        elif life_code == 19:  # 军人
            options_m = ["战地的少女", "战友", "长官", "部下", "部下的女儿", "长官的女儿"]
            options_f = ["战地的少年", "战友", "长官", "部下", "部下的儿子", "长官的儿子", "少年士兵"]
            return random.choice(options_m if gender != "female" else options_f)
        elif life_code == 5:  # 娼妇
            return "女客人" if gender != "female" else "中年客人"
        elif life_code == 20:  # 奴隶
            return "女奴隶主" if gender != "female" else "奴隶主"
        return "某人"

    def _pick_unfortunate_male(self) -> str:
        return random.choice(["狩猎少年的痴女", "淫乱女家教", "女暴露狂"])

    def _pick_unfortunate_female(self) -> str:
        return random.choice(["流氓", "窃贼", "强奸魔"])

    # ===== 家族注册 =====

    def _family_register(self, char_idx: int) -> None:
        """家族注册 (对应 @FAMILY_REGISTER)
        同种族角色之间随机建立家族关系
        CFLAG:601=父, CFLAG:602=母, CFLAG:603-605=子女, CFLAG:606-608=兄弟姐妹
        CFLAG:605=家族构成
        """
        char = self._get_chars()[char_idx]
        char_race = char.talent.get(314, 0)

        # 搜索同种族的现有角色
        same_race_chars = []
        chars = self._get_chars()
        for i, c in enumerate(chars):
            if i == char_idx:
                continue
            if c.talent.get(314, 0) == char_race:
                same_race_chars.append(i)

        if not same_race_chars:
            return

        # 随机选择一个同种族角色作为家族成员
        family_idx = random.choice(same_race_chars)
        family_char = chars[family_idx]

        # 随机决定家族关系类型
        rel_type = random.randint(0, 3)

        if rel_type == 0:
            # 被选角色成为当前角色的父母
            if family_char.talent.get(122, 0):
                # 男性 → 父亲
                char.cflag[601] = family_idx
            else:
                # 女性 → 母亲
                char.cflag[602] = family_idx
            # 反向：当前角色成为对方的子女
            for cflag_id in [603, 604, 605]:
                if family_char.cflag.get(cflag_id, -1) == -1:
                    family_char.cflag[cflag_id] = char_idx
                    break

        elif rel_type == 1:
            # 当前角色成为被选角色的父母
            if char.talent.get(122, 0):
                family_char.cflag[601] = char_idx
            else:
                family_char.cflag[602] = char_idx
            for cflag_id in [603, 604, 605]:
                if char.cflag.get(cflag_id, -1) == -1:
                    char.cflag[cflag_id] = family_idx
                    break

        elif rel_type == 2:
            # 兄弟姐妹关系
            char.cflag[606] = family_idx
            for cflag_id in [606, 607, 608]:
                if family_char.cflag.get(cflag_id, -1) == -1:
                    family_char.cflag[cflag_id] = char_idx
                    break

        else:
            # 被选角色成为当前角色的父母（另一种分配）
            if family_char.talent.get(122, 0):
                char.cflag[601] = family_idx
            else:
                char.cflag[602] = family_idx
            for cflag_id in [603, 604, 605]:
                if family_char.cflag.get(cflag_id, -1) == -1:
                    family_char.cflag[cflag_id] = char_idx
                    break

        # 设定家族构成 (CFLAG:605)
        # 0=不明, 1=両親あり, 2=片親, 3=兄弟あり, 4=一人
        has_father = char.cflag.get(601, -1) != -1
        has_mother = char.cflag.get(602, -1) != -1
        has_sibling = char.cflag.get(606, -1) != -1 or char.cflag.get(607, -1) != -1 or char.cflag.get(608, -1) != -1

        if has_father and has_mother:
            char.cflag[605] = 1  # 両親あり
        elif has_father or has_mother:
            char.cflag[605] = 2  # 片親
        elif has_sibling:
            char.cflag[605] = 3  # 兄弟あり
        else:
            char.cflag[605] = 4  # 一人

    # ===== 家族素质继承 =====

    def _cm_family_talent(self, char_idx: int) -> None:
        """家族素质继承 (对应 @CM_FAMILY_TALENT)"""
        char = self._get_chars()[char_idx]

        # 查找家族成员
        family_id = self._search_family(char_idx)

        if family_id > 0:
            family = self._get_char(family_id)
            if family is None:
                return

            family_age = family.cflag.get(451, 0)

            if family_age < 15:
                # 家族が15歳未満
                # 大柄なら体格を一段階大さくする
                if family.talent.get(99, 0) and random.randint(0, 2) == 0:
                    if char.talent.get(100, 0):
                        char.talent[100] = 0
                    else:
                        char.talent[99] = 1

                # 巨乳以上なら乳を一段階大さくする
                if ((family.talent.get(110, 0) and random.randint(0, 3) != 0) or
                    (family.talent.get(114, 0) and random.randint(0, 1) != 0) or
                    family.talent.get(119, 0) == 0) and char.talent.get(122, 0) == 0:
                    if char.talent.get(116, 0):
                        char.talent[116] = 0
                        char.talent[109] = 1
                    elif char.talent.get(109, 0):
                        char.talent[109] = 0
                    elif (char.talent.get(110, 0) == 0 and char.talent.get(114, 0) == 0 and
                          char.talent.get(119, 0) == 0):
                        char.talent[110] = 1
                    elif char.talent.get(110, 0):
                        char.talent[110] = 0
                        char.talent[114] = 1
                    else:
                        char.talent[114] = 0
                        char.talent[119] = 1

            elif family_age > 17:
                # 家族が18歳以上
                # 小柄体型なら体格を一段階小さくする
                if family.talent.get(100, 0) and random.randint(0, 2) == 0:
                    if char.talent.get(99, 0):
                        char.talent[99] = 0
                    else:
                        char.talent[100] = 1

                # 貧乳以下なら階乳を一段小さくする
                if ((family.talent.get(109, 0) and random.randint(0, 3) != 0) or
                    (family.talent.get(116, 0) and random.randint(0, 1) == 0)) and char.talent.get(122, 0) == 0:
                    if char.talent.get(119, 0):
                        char.talent[119] = 0
                        char.talent[114] = 1
                    elif char.talent.get(114, 0):
                        char.talent[114] = 0
                        char.talent[110] = 1
                    elif char.talent.get(110, 0):
                        char.talent[110] = 0
                    elif (char.talent.get(109, 0) == 0 and char.talent.get(116, 0) == 0):
                        char.talent[109] = 1
                    else:
                        char.talent[109] = 0
                        char.talent[116] = 1

            # 肌肉型/虚弱继承
            if (family.talent.get(248, 0) or family.talent.get(256, 0)) and random.randint(0, 2) == 0:
                char.talent[248] = family.talent.get(248, 0)
                char.talent[256] = family.talent.get(256, 0)

            # 肤色继承
            if (family.talent.get(253, 0) or family.talent.get(255, 0)) and random.randint(0, 1) == 0:
                char.talent[253] = family.talent.get(253, 0)
                char.talent[255] = family.talent.get(255, 0)

            # 额头天眼继承
            if family.talent.get(260, 0) and random.randint(0, 2) == 0:
                char.talent[260] = family.talent.get(260, 0)

            # 头发颜色继承
            if random.randint(0, 4) != 0:
                # 家族と「近い色」の髪になる可能性が高い
                hair_color_map = {
                    1: 130,   # 金
                    2: 160,   # 栗
                    3: 230,   # 黒
                    4: 150,   # 赤
                    5: 120,   # 銀
                    6: 210,   # 青
                    7: 200,   # 緑
                    8: 220,   # 紫
                    9: 110,   # 白
                    10: 170,  # 暗金
                    11: 140,  # 粉
                }
                family_hair = family.talent.get(300, 0)
                hair_color = hair_color_map.get(family_hair, 150)
                # 加上随机偏移
                hair_color = hair_color - 20 + sum(random.randint(0, 8) for _ in range(5))
                if hair_color > 225:
                    char.talent[300] = 3    # 黒
                elif hair_color > 215:
                    char.talent[300] = 8    # 紫
                elif hair_color > 205:
                    char.talent[300] = 6    # 青
                elif hair_color > 185:
                    char.talent[300] = 7    # 緑
                elif hair_color > 165:
                    char.talent[300] = 10   # 暗金
                elif hair_color > 155:
                    char.talent[300] = 2    # 栗
                elif hair_color > 145:
                    char.talent[300] = 4    # 赤
                elif hair_color > 135:
                    char.talent[300] = 11   # 粉
                elif hair_color > 125:
                    char.talent[300] = 1    # 金
                elif hair_color > 115:
                    char.talent[300] = 5    # 銀
                else:
                    char.talent[300] = 9    # 白

            # 瞳色继承
            if random.randint(0, 4) != 0:
                char.talent[306] = family.talent.get(306, 0)

            # 体型继承
            if random.randint(0, 2) == 0:
                char.talent[308] = family.talent.get(308, 0)

            # 乳头继承
            if random.randint(0, 2) == 0:
                char.talent[309] = family.talent.get(309, 0)

            # 阴毛状态继承
            if random.randint(0, 2) == 0:
                char.talent[311] = family.talent.get(311, 0)
                char.talent[310] = family.talent.get(310, 0)

    def _search_family(self, char_idx: int) -> int:
        """查找家族成员 (对应 @SEARCH_FAMILY)
        同种族角色中随机选择一个家族成员。
        返回家族成员索引，找不到返回 -1。
        """
        char = self._get_chars()[char_idx]
        race = char.talent.get(314, 13)
        candidates = []
        chars = self._get_chars()
        for i, other in enumerate(chars):
            if i == char_idx:
                continue
            if other.talent.get(314, 13) == race:
                candidates.append(i)
        if candidates:
            return random.choice(candidates)
        return -1

    # ===== 服装设定 =====

    def _cm_cloth(self, char) -> None:
        """服装设定 (对应 @CM_CLOTH)"""
        r = 0

        if char.talent.get(200, 0) and char.talent.get(122, 0):
            # オトコ戦士
            r = 3
            char.cflag[550] = 40
        elif char.talent.get(200, 0) == 1:
            # 战士
            if char.cflag.get(6, 0) >= 4500 and random.randint(0, 2) == 0:
                # チャイナドレス
                r = 214
                if random.randint(0, 1) == 0:
                    char.cflag[550] = 51   # クレセントブレード
                else:
                    char.cflag[550] = 52   # ナックル
            else:
                x = random.randint(0, 5)
                if x == 0:
                    r = 292
                elif x == 1:
                    r = 2
                elif x == 2:
                    r = 3
                elif x == 3:
                    r = 4
                elif x == 4:
                    r = 108
                else:
                    r = 193
                char.cflag[550] = 40   # 剑
        elif char.talent.get(201, 0) and char.talent.get(122, 0):
            # オトコ魔術師
            r = 103
            char.cflag[42] = 85
            char.cflag[550] = 41   # スタッフ
        elif char.talent.get(201, 0) == 1:
            # 魔法师
            x = random.randint(0, 2)
            if x == 0:
                r = 5
            elif x == 1:
                r = 251
            else:
                r = 103
            char.cflag[42] = 85
            char.cflag[550] = 41   # 法杖
        elif char.talent.get(202, 0) == 1:
            # 神官
            x = random.randint(0, 2)
            if x == 0:
                r = 5
            elif x == 1:
                r = 251
            else:
                r = 207
            char.cflag[550] = 46   # 权杖
        elif char.talent.get(203, 0) and char.talent.get(122, 0):
            # オトコ盗賊
            r = 103
            char.cflag[550] = 43   # ダガー
        elif char.talent.get(203, 0) == 1:
            # 盗贼
            x = random.randint(0, 2)
            if x == 0:
                r = 5
            elif x == 1:
                r = 251
            else:
                r = 103
            char.cflag[550] = 43   # 匕首
        elif char.talent.get(205, 0) and char.talent.get(122, 0):
            # オトコ騎士
            r = 105
            char.cflag[550] = 40   # ソード
        elif char.talent.get(205, 0) == 1:
            # 骑士
            x = random.randint(0, 2)
            if x == 0:
                r = 105
            elif x == 1:
                r = 6
            else:
                r = 111
            char.cflag[550] = 40   # 剑
        elif char.talent.get(206, 0) and char.talent.get(122, 0):
            # オトコ巫女
            r = 104
            char.cflag[550] = 41   # スタッフ
        elif char.talent.get(206, 0) == 1:
            # 巫女
            r = 104
            char.cflag[550] = 41   # 法杖
        elif char.talent.get(207, 0) and char.talent.get(122, 0):
            # オトコ忍者
            r = 110
            char.cflag[550] = 44   # シュリケン
        elif char.talent.get(207, 0) == 1:
            # 忍者
            r = 110
            char.cflag[550] = 44   # 手里剑
        elif char.talent.get(208, 0) and char.talent.get(122, 0):
            # オトコ弓師
            r = 103
            char.cflag[550] = 45   # アロー
        elif char.talent.get(208, 0) == 1:
            # 弓手
            x = random.randint(0, 2)
            if x == 0:
                r = 5
            elif x == 1:
                r = 251
            else:
                r = 103
            char.cflag[550] = 45   # 弓箭
        elif char.talent.get(319, 0) == 2 or char.talent.get(137, 0) == 1:
            # 史莱姆とFURRYは全裸
            r = 0
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(319, 0) == 3:
            # 昆虫
            x = random.randint(0, 5)
            if x == 0:
                r = 193
            elif x == 1:
                r = 0
            else:
                r = 293
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(319, 0) == 4:
            # 植物
            x = random.randint(0, 4)
            if x == 0:
                r = 201
            elif x == 1:
                r = 202
            elif x == 2:
                r = 204
            elif x == 3:
                r = 294
            else:
                r = 0
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(319, 0) == 5:
            # 触手
            x = random.randint(0, 4)
            if x == 0:
                r = 0
            elif x == 1:
                r = 19
            elif x == 2:
                r = 31
            elif x == 3:
                r = 201
            else:
                r = 203
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(319, 0) == 6:
            # 妖精
            x = random.randint(0, 4)
            if x == 0:
                r = 0
            elif x == 1:
                r = 122
            elif x == 2:
                r = 201
            elif x == 3:
                r = 241
            else:
                r = 294
            if char.talent.get(122, 0) and r == 201:
                r = 103
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(220, 0) == 1 and char.talent.get(122, 0):
            # 精英男性
            r = 103
            char.cflag[550] = 42   # 鞭
        elif char.talent.get(220, 0) == 1:
            # 精英
            x = random.randint(0, 5)
            if x == 0:
                r = 203
            elif x == 1:
                r = 2
            elif x == 2:
                r = 7
            elif x == 3:
                r = 4
            elif x == 4:
                r = 103
            else:
                r = 193
            char.cflag[550] = 42   # 鞭
        else:
            r = 1
            char.cflag[550] = 42   # 鞭

        # 初期装備接頭語
        char.cflag[550] = char.cflag.get(550, 0) + random.randint(0, 9) * 100000

        char.cflag[41] = r
        char.cflag[45] = 0
        char.cflag[46] = 0

        # 眼镜で眼鏡付き
        if char.talent.get(48, 0) == 1:
            char.cflag[42] = 83

    # ===== 一人称设定 =====

    def _random_self_call(self, char_idx: int) -> None:
        """一人称の設定 - 对应 @RANDOM_SELF_CALL (扩展版)

        根据性格素质+种族+前职+教育/姿态/开放度评分决定一人称
        存储在 CFLAG:700
        0=俺, 1=私, 2=わたくし, 3=あたし, 4=僕, 5=自分, 6=吾輩,
        7=老娘, 8=老子, 9=本宫, 10=本小姐, 11=本少爺, 12=小女子, 13=人家
        """
        char = self._get_chars()[char_idx]
        is_male = char.talent.get(122, 0) == 1
        is_futa = char.talent.get(121, 0) == 1
        race = char.talent.get(314, 13)
        life_code = char.talent.get(318, 0)

        edu_score = 0
        pose_score = 0
        open_score = 0

        # 种族加成
        if race == 1: edu_score += 15; pose_score += 5      # 精灵: 教育+姿态
        elif race == 2: edu_score -= 5                        # 人狼
        elif race == 3: pose_score += 10                      # 吸血鬼
        elif race == 5: pose_score += 15; edu_score += 5     # 龙族
        elif race == 7: edu_score -= 5; pose_score += 5      # 巨人
        elif race == 11: edu_score -= 5                       # 矮人
        elif race in (16, 17): open_score += 10               # 哥布林/兽人

        # 前职加成
        life_edu = {1: 10, 8: 15, 15: 5, 18: 3, 19: 5}
        life_pose = {5: 0, 8: 10, 19: 3}
        life_open = {3: -5, 4: 5, 5: 15, 6: 5, 20: 5}
        edu_score += life_edu.get(life_code, 0)
        pose_score += life_pose.get(life_code, 0)
        open_score += life_open.get(life_code, 0)

        # 性格加成 (16种性格)
        if char.talent.get(160, 0): edu_score += 5; pose_score += 5           # 慈爱
        if char.talent.get(161, 0): pose_score += 5                            # 自信家
        if char.talent.get(162, 0): pose_score -= 5; edu_score -= 3            # 懦弱
        if char.talent.get(163, 0): edu_score += 10; pose_score += 10          # 高贵
        if char.talent.get(164, 0): edu_score += 5                             # 冷静
        if char.talent.get(165, 0): pose_score += 5                            # 飒爽
        if char.talent.get(166, 0): pose_score += 5; open_score += 5           # 恶女
        if char.talent.get(167, 0): pose_score += 3                            # 温和
        if char.talent.get(168, 0): edu_score += 3; open_score -= 5            # 保守
        if char.talent.get(169, 0): open_score += 5                            # 好奇心
        if char.talent.get(170, 0): pose_score += 5; edu_score -= 3            # 霸道
        if char.talent.get(171, 0): edu_score += 3                             # 诚实
        if char.talent.get(172, 0): pose_score += 5; open_score += 3           # 奔放
        if char.talent.get(173, 0): pose_score += 3                            # 阴郁
        if char.talent.get(174, 0): edu_score += 8; pose_score += 5            # 贵公子
        if char.talent.get(175, 0): edu_score += 5                             # 伶俐
        if char.talent.get(176, 0): pose_score += 3; open_score -= 3           # 内向
        if char.talent.get(177, 0): pose_score += 5                            # 豪放

        # 基于评分选择一人称
        if edu_score >= 20 and pose_score >= 15:
            self_call = 2   # わたくし
        elif edu_score >= 15 and pose_score >= 10:
            self_call = 6   # 吾輩
        elif pose_score >= 15 and is_male:
            self_call = 0   # 俺
        elif pose_score >= 15 and is_futa:
            self_call = 8   # 老子
        elif pose_score >= 15:
            self_call = 7   # 老娘
        elif edu_score >= 12 and is_male:
            self_call = 5   # 自分
        elif edu_score >= 12:
            self_call = 9   # 本宫
        elif open_score >= 10 and edu_score >= 5:
            self_call = 10  # 本小姐 / 本少爺
        elif open_score >= 10:
            self_call = 13  # 人家
        elif edu_score <= -5:
            self_call = 3   # あたし
        elif is_male and pose_score >= 5:
            self_call = 4   # 僕
        elif is_male and edu_score >= 5:
            self_call = 11  # 本少爺
        elif edu_score >= 5:
            self_call = 12  # 小女子
        elif is_male:
            self_call = 0   # 俺
        else:
            self_call = 1   # 私

        char.cflag[700] = self_call

    # ===== 身体数据生成 =====

    def _char_body_generate_wrapped(self, char_idx: int) -> None:
        """身体数据生成 (对应 @CHAR_BODY_GENERATE_WAPPED)"""
        char = self._get_chars()[char_idx]

        # 村娘Ａ・Ｂのみ年齢を指定
        if char.talent.get(165, 0):
            age_param = random.randint(0, 1) + 12
            results = self._char_size_generate(char_idx, age_param)
        elif char.talent.get(171, 0):
            age_param = random.randint(0, 1) + 17
            results = self._char_size_generate(char_idx, age_param)
        else:
            results = self._char_size_generate(char_idx)

        char.cflag[451] = results[0]   # 年龄
        char.cflag[452] = results[1]   # 种族年龄
        char.cflag[453] = results[2]   # 身高
        char.cflag[454] = results[3]   # 体重
        char.cflag[455] = results[4]   # 胸围
        char.cflag[456] = results[5]   # 腰围
        char.cflag[457] = results[6]   # 臀围

    def _char_size_generate(self, char_idx: int, char_age: int = 0) -> List[int]:
        """身体尺寸生成 (对应 @CHAR_SIZE_GENERATE)"""
        char = self._get_chars()[char_idx]

        # 年齢の算出
        if char_age <= 0:
            age_result = self._char_age_generate(char_idx)
            char_age = age_result[0]
            race_age = age_result[1]
        else:
            race_age = char_age

        # 身高/体重生成
        height, weight = self._char_hweight_generate(char_age, char)

        # 腰围
        waist = (height * (3700 + char.talent.get(308, 0))) // 10000
        if char.talent.get(122, 0):
            waist += 8000
            waist -= random.randint(0, 3999)
        if waist > 60000:
            waist = waist * 983 // 1000
        if char.talent.get(91, 0):   # 魅惑
            waist = waist * 96 // 100
        if char.talent.get(248, 0):  # 肌肉型
            waist = waist * 102 // 100
        if char.talent.get(248, 0) and char.talent.get(122, 0):
            waist = waist * 105 // 100
        if char.talent.get(115, 0):  # 肥胖
            waist = waist * 115 // 100
        if char.talent.get(256, 0):  # 虚弱
            waist = waist * 98 // 100
        if char.talent.get(314, 0) == 11:  # ドワーフ
            waist = waist * 104 // 100

        # 胸围
        bust_u, bust_t = self._char_bust_generate(char_age, height, char)
        bust = bust_u + bust_t

        # 娇小+巨乳补正
        if char.talent.get(100, 0) and char.talent.get(110, 0):
            bust_t += 1500 + random.randint(0, 999)
        # 魁梧マイナス补正
        if char.talent.get(99, 0):
            bust_t -= 2000 + random.randint(0, 999)
        # 出産経験补正
        if char.exp.get(60, 0) > 0:
            bust_t += 200 + random.randint(0, 799)
        # 超乳+母乳
        if char.talent.get(130, 0) and char.talent.get(119, 0):
            bust_t += 8500 + random.randint(0, 3999)

        bust = bust_u + bust_t

        # 臀围
        hip = (height * (5300 + char.talent.get(308, 0))) // 10000
        if char.talent.get(91, 0):   # 魅惑
            hip += 1500
        if char.talent.get(248, 0):  # 肌肉型
            hip = hip * 102 // 100
        if char.talent.get(256, 0):  # 虚弱
            hip = hip * 98 // 100
        if char.talent.get(100, 0):  # 娇小
            hip = int(hip * 0.96)
        if char.talent.get(122, 0):  # 男性
            hip = int(hip * 0.90)
        if char.talent.get(115, 0):  # 肥胖
            hip = hip * 115 // 100

        # 修正年龄较小时大臀瘦胸的问题
        if char_age < 16:
            hip = max(min(hip, bust + max(char_age - 12, 0) * 1000), waist)

        # 体重加算（胸围による重量加算）
        cal_var = bust_u * bust_u // 100000000
        cal_var = cal_var * bust_t // 100000
        cal_var = cal_var * bust_t // 100000
        weight = weight + (cal_var * 250)

        # 种族年齢の設定
        if char.talent.get(314, 0) == 0:
            race_age = char_age

        return [char_age, race_age, height // 100, weight // 100, bust // 100, waist // 100, hip // 100]

    def _char_age_generate(self, char_idx: int) -> List[int]:
        """年龄生成 (对应 @CHAR_AGE_GENERATE)"""
        char = self._get_chars()[char_idx]

        # 根据经历推测年龄
        exp_age = self._char_age_expect(char_idx)
        exp_age = 17 + exp_age
        exp_age = max(12, min(35, exp_age))

        # 正态分布采样
        char_age = self._normal_point_pickup(exp_age)

        # 后代年龄按相当于人类10岁设定
        if self._get_ex_talent(char, 2):
            char_age = 10

        # 种族年龄
        race_age = self._race_age_generate(char_age, char.talent.get(314, 0))

        # 人类年龄低于14即为未熟
        if char_age <= 14:
            char.talent[135] = 1

        return [char_age, race_age]

    def _char_age_expect(self, char_idx: int) -> int:
        """根据经历推算相对年龄 (对应 @CHAR_AGE_EXPECT)"""
        char = self._get_chars()[char_idx]
        exp_age = 0

        if char.talent.get(99, 0):    exp_age += 1
        if char.talent.get(100, 0):   exp_age -= 1
        if char.talent.get(100, 0):   exp_age -= 3
        if char.talent.get(109, 0):   exp_age -= 1
        if char.talent.get(110, 0):   exp_age += 1
        if char.talent.get(114, 0):   exp_age += 1
        if char.talent.get(119, 0):   exp_age += 1
        if char.talent.get(116, 0):   exp_age -= 1
        if char.talent.get(132, 0):   exp_age -= 2
        if char.talent.get(135, 0):   exp_age -= 2
        if char.talent.get(140, 0) or char.talent.get(141, 0): exp_age -= 2
        if char.talent.get(142, 0) or char.talent.get(143, 0): exp_age += 2
        if char.talent.get(157, 0):   exp_age += 6
        if char.talent.get(248, 0):   exp_age += 1

        # 经历补正
        talent315 = char.talent.get(315, 0)
        if talent315 in (1, 6, 7, 20):
            exp_age -= 4
        elif talent315 in (11, 12):
            exp_age -= 1
        elif talent315 in (2, 19):
            exp_age += 4
        elif talent315 == 21:
            exp_age += 6

        if char.talent.get(316, 0) == 6:
            exp_age += 2
        if char.talent.get(317, 0) == 4 or char.talent.get(317, 0) == 11:
            exp_age += 2

        # 生育经验
        if char.exp.get(60, 0):
            exp_age += 6
        elif char.exp.get(5, 0):
            exp_age += 4
        elif char.exp.get(10, 0):
            exp_age += 2
        elif not char.talent.get(0, 0) and not char.talent.get(1, 0):
            exp_age += 1

        return exp_age

    def _normal_point_pickup(self, center: int) -> int:
        """正态分布采样 (对应 @NORMAL_POINT_PICKUP)"""
        # 简化的正态分布采样：使用多个均匀分布的和来近似
        result = center - 4 + sum(random.randint(0, 1) for _ in range(8))
        return max(12, min(35, result))

    def _race_age_generate(self, human_age: int, race_talent: int) -> int:
        """种族年龄生成 (对应 @RACE_AGE_GENERATE)"""
        # 魔族の場合は人間換算年齢を返す
        if 7 <= race_talent < 10:
            if race_talent == 9:
                return human_age
            # 简化：使用默认配置
            race_id = 0 if race_talent == 7 else 5
        else:
            race_id = race_talent - 1
            if race_id > 8:
                race_id -= 3

        # 从FLAG:26/27获取种族配置（简化实现）
        # 默认配置：精灵2.3倍，其他种族1倍
        if race_id == 0:
            return int(human_age * 2.3)
        return human_age

    def _char_hweight_generate(self, char_age: int, char) -> Tuple[int, int]:
        """身高体重生成 (对应 @CHAR_HWEIGHT_GENERATE)

        返回 (身高*100, 体重*100)
        """
        # 基础身高
        if char.talent.get(122, 0):
            char_height = 115000
        else:
            char_height = 110000 + (random.randint(0, 133) + random.randint(0, 133) + random.randint(0, 132)) * 100
            if random.randint(0, 4) == 0:
                char_height += random.randint(0, 99) * 100
            if random.randint(0, 4) == 0:
                char_height -= random.randint(0, 99) * 100

        # 种族身高补正
        race314 = char.talent.get(314, 0)
        if race314 == 1:    # 精灵
            char_height += random.randint(0, 7) * 1000
        elif race314 == 5:  # 龙族
            char_height += random.randint(0, 15) * 1000
        elif race314 == 7:  # 暗黑精灵
            char_height += random.randint(0, 7) * 1000
        elif race314 == 10: # 霍比特人
            char_height -= random.randint(0, 7) * 1000
        elif race314 == 11: # 矮人
            char_height -= random.randint(0, 7) * 1000

        # 年龄补正
        if char_age < 13:
            char_height = char_height * (18 + char_age) // 32
        elif char_age == 13:
            char_height = char_height * 77 // 80
        elif char_age < 18:
            char_height = char_height * (160 - char_age) // 160

        # 身高决定
        char_height += (250 + random.randint(0, 19) + random.randint(0, 19) + random.randint(0, 19) +
                        random.randint(0, 19) + random.randint(0, 19)) * 100

        # 体型限制
        height_max = 180000
        height_min = 140000
        if char.talent.get(122, 0):
            height_max += 25000
        if char.talent.get(99, 0):
            height_max = 999000
            height_min = 170000
        if char.talent.get(100, 0):
            height_max = 160000
            height_min = 0

        # 体重计算（BMI基准）
        char_weight = char_height * char_height * 21 // (1250 - char.talent.get(308, 0)) // 10000
        if char.talent.get(248, 0):
            char_weight = char_weight * 107 // 100
        if char.talent.get(256, 0):
            char_weight = char_weight * 98 // 100

        return char_height, char_weight

    def _char_bust_generate(self, char_age: int, char_height: int, char) -> Tuple[int, int]:
        """胸围生成 (对应 @CHAR_BUST_GENERATE)

        返回 (下胸围*100, トップ差分*100)
        """
        # 下胸围
        bust_u = char_height * (43100 + char.talent.get(308, 0)) // 100000
        if char.talent.get(248, 0):
            bust_u = bust_u * 105 // 100
        if char.talent.get(256, 0):
            bust_u = bust_u * 98 // 100

        # トップ差分
        if char.talent.get(116, 0):     # 绝壁
            bust_t = 1000 + random.randint(0, 39) * 100
        elif char.talent.get(109, 0):   # 贫乳
            bust_t = 7000 + random.randint(0, 59) * 100
        elif char.talent.get(110, 0) or char.talent.get(114, 0) or char.talent.get(119, 0):
            # 巨乳/爆乳/超乳
            bust_t = 20000 + random.randint(0, 2499)
            if char.talent.get(114, 0):
                bust_t += 5000 + random.randint(0, 4999)
                if random.randint(0, 1) == 0:
                    bust_t += 18000 + random.randint(0, 1999) + random.randint(0, 1999) + random.randint(0, 2999)
            elif char.talent.get(119, 0):
                bust_t += 5000 + random.randint(0, 4999)
                bust_t += 18000 + random.randint(0, 1999) + random.randint(0, 1999) + random.randint(0, 2999)
        else:
            # 普乳
            bust_t = 13200 + random.randint(0, 39) * 100

        # 年龄补正
        if char_age < 16:
            bust_t -= 2000 - char_age * 100

        return bust_u, bust_t

    # ===== 命名 =====

    def _chara_name_random_define(self, char_idx: int) -> None:
        """随机命名 (对应 @CHARA_NAME_RANDOM_DEFINE)"""
        char = self._get_chars()[char_idx]
        # Name generation based on race and gender
        race = char.talent.get(314, 13)  # 种族, default human
        is_male = char.talent.get(122, 0)

        # Name pools by race (simplified)
        male_names = {
            1: ["艾尔文", "莱恩", "希尔凡"],    # 精灵
            2: ["沃尔夫", "卢卡", "加尔"],       # 人狼
            3: ["弗拉德", "卡恩", "德古拉"],     # 吸血鬼
            5: ["龙牙", "赤焰", "苍鳞"],         # 龙
            13: ["亚瑟", "雷恩", "凯恩"],         # 人类
        }
        female_names = {
            1: ["艾拉", "希尔薇", "莱娜"],       # 精灵
            2: ["露娜", "米娅", "沃尔卡"],       # 人狼
            3: ["卡蜜拉", "莉莉丝", "伊丽莎白"], # 吸血鬼
            5: ["龙姬", "绯红", "翠鳞"],         # 龙
            13: ["菲娅", "莉莉", "艾米"],         # 人类
        }

        names = female_names if not is_male else male_names
        name_list = names.get(race, names[13])
        char.name = random.choice(name_list)
