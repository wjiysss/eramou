from __future__ import annotations
"""Module for ComfMixin - COMF (command function) methods for training commands"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


COMF_SOURCE_TABLE = {

}

# =====================================================================
# COMF_SIDE_EFFECTS - 调教命令副作用数据表
# 从ERB COMF*.ERB文件提取的LOSEBASE/STAIN/EXP数据
# 格式: {com_id: {"losebase": [体力, 气力], "stain": [...], "exp": [...]}}
# stain规则: (target_part, source) - source为"PLAYER:N"表示调教者部位，整数表示自身部位
# STAIN部位: 0=口, 1=指, 2=ペニス, 3=V, 4=アナル, 5=B
# EXP类型: 0=性交, 1=肛门, 10=自慰, 11=调教自慰, 23=爱情, 40=百合, 41=ホモ, 50=异常
# =====================================================================
COMF_SIDE_EFFECTS: Dict[int, Dict[str, Any]] = {
    # COMF0 爱抚 - 已在方法内联处理，此处仅作记录
    0: {"losebase": [5, 50], "stain": [(0, "PLAYER:0"), (3, "PLAYER:1"), (5, "PLAYER:1")], "exp": [(40, 5), (23, 2)], "note": "inline_kiss_check"},
    # COMF1 舔阴
    1: {"losebase": [5, 50], "stain": [(3, "PLAYER:0")], "exp": [(40, 3), (23, 1)], "note": "player_first_kiss"},
    # COMF2 肛门爱抚
    2: {"losebase": [20, 100], "stain": [(4, "PLAYER:1")], "exp": [(1, 1), (40, 2), (23, 1)], "note": "exp_dynamic"},
    # COMF3 自慰 - 已在方法内联处理
    3: {"losebase": [5, 50], "stain": [(1, 5), (5, 1), (1, 3), (3, 1)], "exp": [(10, 1), (11, 1)], "note": "inline"},
    # COMF4 口交
    4: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 3), (23, 1)], "note": "player_first_kiss"},
    # COMF5 胸爱抚
    5: {"losebase": [5, 50], "stain": [(5, "PLAYER:1")], "exp": [(40, 3), (23, 1)], "note": ""},
    # COMF6 ローター
    6: {"losebase": [5, 30], "stain": [(3, "PLAYER:1")], "exp": [(40, 2), (23, 1)], "note": ""},
    # COMF7 クリキャップ
    7: {"losebase": [5, 30], "stain": [], "exp": [(40, 2), (23, 1)], "note": ""},
    # COMF8 指挿入れ
    8: {"losebase": [5, 50], "stain": [(3, "PLAYER:1")], "exp": [(0, 1), (40, 2), (23, 1)], "note": ""},
    # COMF9 アナル舐め
    9: {"losebase": [5, 50], "stain": [(4, "PLAYER:0"), (0, "PLAYER:4")], "exp": [(1, 1), (40, 2), (23, 1)], "note": ""},
    # COMF10 振動の宝石
    10: {"losebase": [5, 30], "stain": [], "exp": [(40, 2), (23, 1)], "note": ""},
    # COMF11 バイブ
    11: {"losebase": [5, 50], "stain": [(3, 2)], "exp": [(0, 1), (40, 2), (23, 1)], "note": ""},
    # COMF12 振動の杖
    12: {"losebase": [5, 50], "stain": [(4, 2)], "exp": [(1, 1), (40, 2), (23, 1)], "note": ""},
    # COMF13 アナルバイブ
    13: {"losebase": [5, 50], "stain": [(4, 2)], "exp": [(1, 1), (40, 2), (23, 1)], "note": ""},
    # COMF14-19 道具系
    14: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    15: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    16: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    17: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    18: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    19: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    # COMF20-29 性交系
    20: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    21: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    22: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    23: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    24: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    25: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    26: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    27: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    28: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    29: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    # COMF30-49 奉仕/SM系
    30: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2), (23, 1)], "note": ""},
    31: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2), (23, 1)], "note": ""},
    32: {"losebase": [5, 50], "stain": [(5, "PLAYER:2")], "exp": [(40, 2), (23, 1)], "note": ""},
    33: {"losebase": [5, 50], "stain": [(3, "PLAYER:2")], "exp": [(40, 2), (23, 1)], "note": ""},
    34: {"losebase": [5, 50], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 2), (23, 1)], "note": ""},
    35: {"losebase": [5, 50], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 2), (23, 1)], "note": ""},
    36: {"losebase": [5, 50], "stain": [(4, "PLAYER:2")], "exp": [(1, 1), (40, 2), (23, 1)], "note": ""},
    37: {"losebase": [5, 50], "stain": [(4, "PLAYER:2"), (0, "PLAYER:4")], "exp": [(1, 1), (40, 2), (23, 1)], "note": ""},
    38: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    # COMF40-49
    40: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    41: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    42: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    43: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    44: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    45: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    46: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    47: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    48: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    49: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    # COMF50-73 特殊系
    50: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    51: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    52: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    53: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    54: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    55: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    56: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    57: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    58: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    59: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    60: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    61: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    62: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    63: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    64: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    65: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    66: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    67: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    68: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    69: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    70: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    71: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    72: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    73: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    # COMF80-90 特殊系
    80: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    81: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    82: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    83: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    84: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    85: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    87: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    89: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    90: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    # COMF100+ 触手/斗兽场/助手系
    100: {"losebase": [5, 50], "stain": [(1, 2), (1, 4), (5, 2), (5, 4)], "exp": [(40, 2)], "note": "tentacle"},
    110: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    111: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    120: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    121: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    122: {"losebase": [5, 50], "stain": [(3, "PLAYER:2"), (0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    123: {"losebase": [5, 50], "stain": [(0, "PLAYER:2"), (5, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    124: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    125: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    126: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    127: {"losebase": [5, 50], "stain": [(0, "PLAYER:2")], "exp": [(40, 2)], "note": ""},
    128: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    129: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    130: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    131: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    132: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    133: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    134: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    135: {"losebase": [10, 80], "stain": [(3, "PLAYER:2")], "exp": [(0, 1), (40, 3), (23, 1)], "note": ""},
    150: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    200: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    201: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    202: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    203: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    204: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    205: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    206: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    207: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
    208: {"losebase": [5, 50], "stain": [], "exp": [(40, 2)], "note": ""},
}


class ComfMixin:
    """Mixin providing COMF (command function) methods for training commands"""

    def _comf_losebase(self, com_id: int, target: "Character") -> None:
        """处理LOSEBASE（体力/气力消耗）"""
        entry = COMF_SIDE_EFFECTS.get(com_id, {})
        lb = entry.get("losebase", [0, 0])
        if lb[0] > 0 or lb[1] > 0:
            target.losebase[0] = int(target.losebase.get(0, 0)) + lb[0]
            target.losebase[1] = int(target.losebase.get(1, 0)) + lb[1]

    def _comf_stain(self, com_id: int, target: "Character") -> None:
        """处理STAIN（污渍移动）"""
        entry = COMF_SIDE_EFFECTS.get(com_id, {})
        player = self._get_player()
        for rule in entry.get("stain", []):
            if len(rule) != 2:
                continue
            target_part, source = rule
            if isinstance(source, str) and source.startswith("PLAYER:"):
                if player is None:
                    continue
                p_part = int(source.split(":")[1])
                t_val = int(target.stain.get(target_part, 0))
                p_val = int(player.stain.get(p_part, 0))
                target.stain[target_part] = t_val | p_val
                player.stain[p_part] = p_val | t_val
            elif isinstance(source, int):
                # 自身部位间移动
                t_val = int(target.stain.get(target_part, 0))
                s_val = int(target.stain.get(source, 0))
                target.stain[target_part] = t_val | s_val
                target.stain[source] = s_val | t_val

    def _comf_exp(self, com_id: int, target: "Character") -> None:
        """处理EXP（经验增加）- 基础版本，不含条件判断"""
        entry = COMF_SIDE_EFFECTS.get(com_id, {})
        v = self.interpreter.vars
        assiplay = self.state.assiplay
        player = self._get_player()
        for exp_type, amount in entry.get("exp", []):
            # 百合/ホモ经验需要性别检查
            if exp_type == 40 and player is not None:
                # 百合经验: 双方都是女性
                if not target.has_talent(122) and not player.has_talent(122):
                    target.add_exp(40, amount)
            elif exp_type == 41 and player is not None:
                # ホモ经验: 双方都是男性
                if target.has_talent(122) and player.has_talent(122):
                    target.add_exp(41, amount)
            elif exp_type == 23:
                # 爱情经验: 需要好感度>=1000且非助手操作
                if target.get_cflag(2) >= 1000 and assiplay == 0:
                    target.add_exp(23, amount)
            else:
                target.add_exp(exp_type, amount)

    def _comf_apply_side_effects(self, com_id: int, target: "Character") -> None:
        """应用所有副作用（LOSEBASE + STAIN + EXP）"""
        self._comf_losebase(com_id, target)
        self._comf_stain(com_id, target)
        self._comf_exp(com_id, target)

    def _calc_comf_source(self, com_id: int, target: "Character") -> Dict[str, int]:
        """Calculate COMF source from COMF_SOURCE_TABLE."""
        entry = COMF_SOURCE_TABLE.get(com_id)
        if entry is None:
            return {}
        source: Dict[str, int] = dict(entry.get("base", {}))

        # Apply ABL scale (set / add)
        for abl_id, src_map in entry.get("abl_scale", {}).items():
            abl_val = min(target.get_abl(abl_id), 5)
            for src_key, values in src_map.items():
                val = values[abl_val] if abl_val < len(values) else values[-1] if values else 0
                if src_key.startswith("+"):
                    real_key = src_key[1:]
                    source[real_key] = int(source.get(real_key, 0)) + val
                else:
                    source[src_key] = val

        # Apply ABL multipliers
        for abl_id, src_map in entry.get("abl_mult", {}).items():
            abl_val = min(target.get_abl(abl_id), 5)
            for src_key, values in src_map.items():
                mult = values[abl_val] if abl_val < len(values) else values[-1] if values else 1.0
                if mult != 1.0:
                    source[src_key] = self._scale_value(int(source.get(src_key, 0)), mult)

        # Apply talent multipliers
        for talent_id, mult_map in entry.get("talent_mult", {}).items():
            if target.has_talent(talent_id):
                for src_key, mult in mult_map.items():
                    if src_key in source:
                        source[src_key] = self._scale_value(int(source.get(src_key, 0)), mult)

        # Apply talent additions
        for talent_id, add_map in entry.get("talent_add", {}).items():
            if target.has_talent(talent_id):
                for src_key, add_val in add_map.items():
                    if src_key.startswith("+"):
                        real_key = src_key[1:]
                        source[real_key] = int(source.get(real_key, 0)) + add_val
                    else:
                        source[src_key] = int(source.get(src_key, 0)) + add_val

        return source


    def _comf0(self, target: Character) -> Dict[str, int]:
        """爱抚 SOURCE计算 - 基于ERB COMF0_愛撫.ERB"""
        source: Dict[str, int] = {}
        v = self.interpreter.vars
        player = self._get_player()
        assiplay = self.state.assiplay

        # LOSEBASE
        target.losebase[0] = target.losebase.get(0, 0) + 5
        target.losebase[1] = target.losebase.get(1, 0) + 50

        # 基础SOURCE
        source[0] = 0    # 快C
        source[17] = 0   # 快B
        source[3] = 0    # 情爱
        source[4] = 60   # 性行動
        source[8] = 30   # 不洁
        source[12] = 100 # 露出

        # ABL:0 阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            source[0] = 20; source[3] = 25
        elif abl0 == 1:
            source[0] = 100; source[3] = 50
        elif abl0 == 2:
            source[0] = 500; source[3] = 80
        elif abl0 == 3:
            source[0] = 1200; source[3] = 100
        elif abl0 == 4:
            source[0] = 2000; source[3] = 115
        else:
            source[0] = 2800; source[3] = 125

        # ABL:1 乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            source[17] = 15; source[3] += 25
        elif abl1 == 1:
            source[17] = 50; source[3] += 50
        elif abl1 == 2:
            source[17] = 300; source[3] += 80
        elif abl1 == 3:
            source[17] = 700; source[3] += 100
        elif abl1 == 4:
            source[17] = 1100; source[3] += 115
        else:
            source[17] = 1600; source[3] += 125

        # 口的污渍检查和口塞/初吻检查
        stain0 = int(target.stain.get(0, 0))
        if (stain0 & 1 or stain0 & 4 or stain0 & 8 or stain0 & 32) and assiplay:
            # 助手操作时口脏且助手反感污臭
            pass  # TODO: 需要助手数据
        elif int(target.tequip.get(45, 0)):
            # 口塞使用中
            source[8] = 0
            source[0] = source[0] // 2
            source[3] = source[3] // 4
            source[10] = source.get(10, 0) // 2
        elif int(target.cflag.get(16, 0)) == -1:
            # 初吻未体验
            source[8] = 0
            source[0] = source[0] // 2
            source[3] = source[3] // 4
            source[10] = source.get(10, 0) // 2
        else:
            # 不怕污臭 TALENT:61
            if int(target.talent.get(61, 0)):
                source[8] = source[8] // 4
            # 反感污臭 TALENT:62
            if int(target.talent.get(62, 0)):
                source[8] = source[8] * 3
            # 自尊心 TALENT:15
            if int(target.talent.get(15, 0)):
                source[8] = source[8] * 2
            # 爱慕 TALENT:85
            if int(target.talent.get(85, 0)) and assiplay == 0:
                source[3] = source[3] * 2
                source[8] = source[8] // 10
            # 主人的口有污渍
            if player is not None and int(player.stain.get(0, 0)):
                source[8] = source[8] * 3 // 2
            # STAIN移动: 口⇔口
            if player is not None:
                s0 = int(target.stain.get(0, 0))
                sp0 = int(player.stain.get(0, 0))
                target.stain[0] = s0 | sp0
                player.stain[0] = sp0 | s0

        # 兽奸检查
        if int(target.tequip.get(89, 0)):
            return source

        # STAIN处理
        if int(target.tequip.get(90, 0)):
            # 触手
            target.stain[1] = int(target.stain.get(1, 0)) | 2 | 4
            target.stain[5] = int(target.stain.get(5, 0)) | 2 | 4
        elif player is not None:
            # V⇔调教者指
            s3 = int(target.stain.get(3, 0))
            sp1 = int(player.stain.get(1, 0))
            target.stain[3] = s3 | sp1
            player.stain[1] = sp1 | s3
            # B⇔调教者指
            s5 = int(target.stain.get(5, 0))
            target.stain[5] = s5 | sp1
            player.stain[1] = sp1 | s5

        # EXP处理
        if player is not None:
            # 百合经验/ホモ经验
            t122 = int(target.talent.get(122, 0))
            p122 = int(player.talent.get(122, 0))
            if t122 == 0 and p122 == 0:
                target.exp[40] = int(target.exp.get(40, 0)) + 5
            elif t122 == 1 and p122 == 1:
                target.exp[41] = int(target.exp.get(41, 0)) + 5
            # 爱情经验
            if int(target.cflag.get(2, 0)) >= 1000 and assiplay == 0:
                target.exp[23] = int(target.exp.get(23, 0)) + 2

        return source


    def _comf1(self, target: Character) -> Dict[str, int]:
        """舔阴 SOURCE计算"""
        self._comf_apply_side_effects(1, target)
        source: Dict[str, int] = {}

        abl0 = target.get_abl(0)  # 阴蒂感觉

        # 基础SOURCE
        source[7] = 100
        source[12] = 220
        source[13] = 50

        # ABL:阴蒂感觉
        if abl0 == 0:
            source[0] = 40
        elif abl0 == 1:
            source[0] = 160
        elif abl0 == 2:
            source[0] = 700
        elif abl0 == 3:
            source[0] = 1500
        elif abl0 == 4:
            source[0] = 2400
        else:
            source[0] = 3300

        # 调教者擅用舌头 TALENT:PLAYER:52
        player = self._get_player()
        if player is not None and int(player.talent.get(52, 0)):
            source[0] = self._scale_value(int(source.get(0, 0)), 2.00)
            source[11] = int(source.get(0, 0)) // 20

        return source




    def _comf2(self, target: Character) -> Dict[str, int]:
        """肛门爱抚 SOURCE计算"""
        self._comf_apply_side_effects(2, target)
        source: Dict[str, int] = {}

        abl3 = target.get_abl(3)  # 肛门感觉
        exp1 = int(target.exp.get(1, 0))  # 肛门经验
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0  # 润滑
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0  # 欲情

        # 基础SOURCE
        source[12] = 850
        source[13] = 200

        # ABL:肛门感觉
        if abl3 == 0:
            source[2] = 20
            source[5] = 300
        elif abl3 == 1:
            source[2] = 75
            source[5] = 350
        elif abl3 == 2:
            source[2] = 300
            source[5] = 400
        elif abl3 == 3:
            source[2] = 700
            source[5] = 650
        elif abl3 == 4:
            source[2] = 1100
            source[5] = 1000
        else:
            source[2] = 1500
            source[5] = 1500

        # EXP:肛门经验
        exp_lv = self._get_exp_level(exp1)
        if exp_lv < 1:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.20)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.20)
            source[6] = 500
            source[13] = int(source.get(13, 0)) + 200
        elif exp_lv < 2:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.50)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.50)
            source[6] = 400
            source[13] = int(source.get(13, 0)) + 100
        elif exp_lv < 3:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.00)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.00)
            source[6] = 300
            source[13] = int(source.get(13, 0)) + 50
        elif exp_lv < 4:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.20)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.20)
            source[6] = 200
        elif exp_lv < 5:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.60)
            source[6] = 100
        else:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.80)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.80)
            source[6] = 50

        # PALAM:润滑
        palam3_lv = self._get_palam_level(palam3)
        if palam3_lv < 1:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.10)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.10)
            source[6] = self._scale_value(int(source.get(6, 0)), 3.00)
        elif palam3_lv < 2:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.20)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.20)
            source[6] = self._scale_value(int(source.get(6, 0)), 2.00)
        elif palam3_lv < 3:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.60)
            source[6] = self._scale_value(int(source.get(6, 0)), 1.00)
        elif palam3_lv < 4:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.00)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.00)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.50)
        else:
            source[2] = self._scale_value(int(source.get(2, 0)), 2.00)
            source[5] = self._scale_value(int(source.get(5, 0)), 2.00)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.10)

        # PALAM:欲情
        palam5_lv = self._get_palam_level(palam5)
        if palam5_lv < 1:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.30)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.30)
        elif palam5_lv < 2:
            source[2] = self._scale_value(int(source.get(2, 0)), 0.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.60)
        elif palam5_lv < 3:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.00)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.00)
        elif palam5_lv < 4:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.30)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.30)
        else:
            source[2] = self._scale_value(int(source.get(2, 0)), 1.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.60)

        # 小人体型 TALENT:263
        if int(target.talent.get(263, 0)):
            source[2] = self._scale_value(int(source.get(2, 0)), 1.50)

        # 肛门敏感 TALENT:105 / 肛门钝感 TALENT:106
        if int(target.talent.get(105, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 1.50)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.50)
            source[13] = self._scale_value(int(source.get(13, 0)), 1.50)
        elif int(target.talent.get(106, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 0.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.60)
            source[13] = self._scale_value(int(source.get(13, 0)), 0.60)

        # 处女+看重贞操 TALENT:0 & TALENT:30
        if int(target.talent.get(0, 0)) and int(target.talent.get(30, 0)):
            source[5] = self._scale_value(int(source.get(5, 0)), 0.80)
            source[13] = self._scale_value(int(source.get(13, 0)), 0.50)

        # 未熟 TALENT:135
        if int(target.talent.get(135, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 2.00)

        return source




    def _comf3(self, target: Character) -> Dict[str, int]:
        """自慰 SOURCE计算 - 基于ERB COMF3_自慰.ERB
        TODO: バイブ/アナルバイブ/沐浴/ビデオ撮影装备分支尚未实现
        """
        source: Dict[str, int] = {}
        v = self.interpreter.vars
        player = self._get_player()

        # LOSEBASE
        target.losebase[0] = target.losebase.get(0, 0) + 5
        target.losebase[1] = target.losebase.get(1, 0) + 50

        # 基础SOURCE
        source[14] = 400  # 抑郁

        # ビデオ撮影中
        if int(target.tequip.get(53, 0)):
            source[10] = 50   # 中毒充足
            source[11] = 100  # 发育

        # ABL:0 阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            source[0] = 15; source[12] = 2000; source[13] = 500
        elif abl0 == 1:
            source[0] = 50; source[12] = 2300; source[13] = 800
        elif abl0 == 2:
            source[0] = 300; source[12] = 2600; source[13] = 1200
        elif abl0 == 3:
            source[0] = 700; source[12] = 2900; source[13] = 1900
        elif abl0 == 4:
            source[0] = 1100; source[12] = 3200; source[13] = 2500
        else:
            source[0] = 1600; source[12] = 3500; source[13] = 3000

        # ABL:1 乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            source[17] = 15
        elif abl1 == 1:
            source[17] = 50
        elif abl1 == 2:
            source[17] = 300
        elif abl1 == 3:
            source[17] = 700
        elif abl1 == 4:
            source[17] = 1100
        else:
            source[17] = 1600

        # TODO: バイブ挿入中 (TEQUIP:11) 的V感觉计算
        # TODO: アナルバイブ挿入中 (TEQUIP:13) 的A感觉计算
        # TODO: 沐浴使用中 (TEQUIP:18) 的特殊计算

        # ABL:12 技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            source[4] = 100
            source[0] = self._scale_value(source.get(0, 0), 0.30)
            source[17] = self._scale_value(source.get(17, 0), 0.30)
        elif abl12 == 1:
            source[4] = 160
            source[0] = self._scale_value(source.get(0, 0), 0.70)
            source[17] = self._scale_value(source.get(17, 0), 0.70)
        elif abl12 == 2:
            source[4] = 220
        elif abl12 == 3:
            source[4] = 280
            source[0] = self._scale_value(source.get(0, 0), 1.20)
            source[17] = self._scale_value(source.get(17, 0), 1.20)
        elif abl12 == 4:
            source[4] = 340
            source[0] = self._scale_value(source.get(0, 0), 1.40)
            source[17] = self._scale_value(source.get(17, 0), 1.40)
        else:
            source[4] = 400
            source[0] = self._scale_value(source.get(0, 0), 1.60)
            source[17] = self._scale_value(source.get(17, 0), 1.60)

        # ABL:31 自慰中毒
        abl31 = target.get_abl(31)
        if abl31 == 0:
            source[7] = 0
        elif abl31 == 1:
            source[7] = 100
            source[0] = self._scale_value(source.get(0, 0), 1.10)
            source[17] = self._scale_value(source.get(17, 0), 1.10)
        elif abl31 == 2:
            source[7] = 300
            source[0] = self._scale_value(source.get(0, 0), 1.20)
            source[17] = self._scale_value(source.get(17, 0), 1.20)
        elif abl31 == 3:
            source[7] = 800
            source[0] = self._scale_value(source.get(0, 0), 1.30)
            source[17] = self._scale_value(source.get(17, 0), 1.30)
        elif abl31 == 4:
            source[7] = 1500
            source[0] = self._scale_value(source.get(0, 0), 1.50)
            source[17] = self._scale_value(source.get(17, 0), 1.50)
        else:
            source[7] = 2500
            source[0] = self._scale_value(source.get(0, 0), 1.70)
            source[17] = self._scale_value(source.get(17, 0), 1.70)

        # STAIN处理
        s1 = int(target.stain.get(1, 0))
        s5 = int(target.stain.get(5, 0))
        s3 = int(target.stain.get(3, 0))
        target.stain[1] = s1 | s5
        target.stain[5] = s5 | s1
        target.stain[1] = int(target.stain.get(1, 0)) | s3
        target.stain[3] = s3 | int(target.stain.get(1, 0))

        # EXP处理
        if int(target.tequip.get(53, 0)) or int(target.tequip.get(54, 0)):
            target.exp[10] = int(target.exp.get(10, 0)) + 2
            target.exp[11] = int(target.exp.get(11, 0)) + 2
        else:
            target.exp[10] = int(target.exp.get(10, 0)) + 1
            target.exp[11] = int(target.exp.get(11, 0)) + 1

        # 屈服刻印
        v.tflag[200] = 2

        return source


    def _comf4(self, target: Character) -> Dict[str, int]:
        """口交 SOURCE计算"""
        self._comf_apply_side_effects(4, target)
        source: Dict[str, int] = {}

        abl0 = target.get_abl(0)  # 阴蒂感觉

        # 基础SOURCE
        source[12] = 220
        source[13] = 50

        # ABL:阴蒂感觉
        if abl0 == 0:
            source[0] = 50
        elif abl0 == 1:
            source[0] = 200
        elif abl0 == 2:
            source[0] = 800
        elif abl0 == 3:
            source[0] = 1600
        elif abl0 == 4:
            source[0] = 2400
        else:
            source[0] = 3200

        # 调教者擅用舌头 TALENT:PLAYER:52
        player = self._get_player()
        if player is not None and int(player.talent.get(52, 0)):
            source[0] = self._scale_value(int(source.get(0, 0)), 2.00)
            source[11] = int(source.get(0, 0)) // 20

        return source




    def _comf5(self, target: Character) -> Dict[str, int]:
        """胸爱抚 SOURCE计算"""
        self._comf_apply_side_effects(5, target)
        source: Dict[str, int] = {}

        abl1 = target.get_abl(1)  # 乳房感觉

        # 基础SOURCE
        source[4] = 60
        source[8] = 20
        source[12] = 100

        # ABL:乳房感觉
        if abl1 == 0:
            source[17] = 20
            source[3] = 50
        elif abl1 == 1:
            source[17] = 100
            source[3] = 100
        elif abl1 == 2:
            source[17] = 500
            source[3] = 160
        elif abl1 == 3:
            source[17] = 1200
            source[3] = 200
        elif abl1 == 4:
            source[17] = 2000
            source[3] = 230
        else:
            source[17] = 2800
            source[3] = 250

        # 调教者擅用舌头 TALENT:PLAYER:52
        player = self._get_player()
        if player is not None and int(player.talent.get(52, 0)):
            source[17] = self._scale_value(int(source.get(17, 0)), 1.40)
            source[11] = int(source.get(17, 0)) // 20

        return source




    def _comf6(self, target: Character) -> Dict[str, int]:
        """接吻 SOURCE计算"""
        self._comf_apply_side_effects(6, target)
        source: Dict[str, int] = {}

        abl16 = target.get_abl(16)  # 侍奉精神
        abl12 = target.get_abl(12)  # 技巧

        # 基础不洁SOURCE (Y*20+10, Y简化为0)
        source[8] = 10

        # ABL:侍奉精神
        if abl16 == 0:
            source[4] = 50
            source[6] = 10
            source[8] = self._scale_value(int(source.get(8, 0)), 4.00)
        elif abl16 == 1:
            source[4] = 150
            source[6] = 50
            source[8] = self._scale_value(int(source.get(8, 0)), 2.50)
        elif abl16 == 2:
            source[4] = 200
            source[6] = 100
            source[8] = self._scale_value(int(source.get(8, 0)), 1.50)
        elif abl16 == 3:
            source[4] = 250
            source[6] = 180
        elif abl16 == 4:
            source[4] = 300
            source[6] = 300
            source[8] = self._scale_value(int(source.get(8, 0)), 0.50)
        else:
            source[4] = 350
            source[6] = 500
            source[8] = self._scale_value(int(source.get(8, 0)), 0.10)

        # ABL:技巧
        if abl12 == 0:
            source[4] = self._scale_value(int(source.get(4, 0)), 0.50)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.50)
        elif abl12 == 1:
            source[4] = self._scale_value(int(source.get(4, 0)), 0.80)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.80)
        elif abl12 == 2:
            pass  # 1.00
        elif abl12 == 3:
            source[4] = self._scale_value(int(source.get(4, 0)), 1.50)
            source[6] = self._scale_value(int(source.get(6, 0)), 1.50)
        elif abl12 == 4:
            source[4] = self._scale_value(int(source.get(4, 0)), 2.50)
            source[6] = self._scale_value(int(source.get(6, 0)), 2.50)
        else:
            source[4] = self._scale_value(int(source.get(4, 0)), 4.00)
            source[6] = self._scale_value(int(source.get(6, 0)), 4.00)

        # 调教者技巧 ABL:PLAYER:12
        player = self._get_player()
        if player is not None:
            player_abl12 = int(player.abl.get(12, 0))
            if player_abl12 == 0:
                source[3] = 100
            elif player_abl12 == 1:
                source[3] = 150
            elif player_abl12 == 2:
                source[3] = 200
            elif player_abl12 == 3:
                source[3] = 300
                source[7] = 50
            elif player_abl12 == 4:
                source[3] = 500
                source[7] = 100
            else:
                source[3] = 800
                source[7] = 200

        # 爱慕 TALENT:85
        if int(target.talent.get(85, 0)):
            source[3] = self._scale_value(int(source.get(3, 0)), 2.00)

        return source




    def _comf7(self, target: Character) -> Dict[str, int]:
        """自己扒开 SOURCE计算"""
        self._comf_apply_side_effects(7, target)
        return self._calc_comf_source(7, target)


    def _comf8(self, target: Character) -> Dict[str, int]:
        """插入手指 SOURCE计算"""
        self._comf_apply_side_effects(8, target)
        source: Dict[str, int] = {}

        abl2 = target.get_abl(2)  # 私处感觉
        exp0 = int(target.exp.get(0, 0))  # 私处经验
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0  # 润滑
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0  # 欲情

        # 基础SOURCE
        source[12] = 300
        source[13] = 200

        # ABL:私处感觉
        if abl2 == 0:
            source[1] = 10
            source[5] = 150
        elif abl2 == 1:
            source[1] = 50
            source[5] = 250
        elif abl2 == 2:
            source[1] = 250
            source[5] = 400
        elif abl2 == 3:
            source[1] = 600
            source[5] = 700
        elif abl2 == 4:
            source[1] = 1200
            source[5] = 1300
        else:
            source[1] = 1800
            source[5] = 2000

        # EXP:私处经验
        exp_lv = self._get_exp_level(exp0)
        if exp_lv < 1:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.20)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.20)
            source[6] = 300
        elif exp_lv < 2:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.50)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.50)
            source[6] = 180
        elif exp_lv < 3:
            source[5] = self._scale_value(int(source.get(5, 0)), 0.80)
            source[6] = 80
        elif exp_lv < 4:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.20)
            source[6] = 30
        elif exp_lv < 5:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.20)
        else:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.80)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.50)

        # 小人体型 TALENT:263
        if int(target.talent.get(263, 0)):
            source[1] = self._scale_value(int(source.get(1, 0)), 1.50)

        # PALAM:润滑
        palam3_lv = self._get_palam_level(palam3)
        if palam3_lv < 1:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.10)
            source[6] = int(source.get(6, 0)) + 700
            source[6] = self._scale_value(int(source.get(6, 0)), 3.00)
        elif palam3_lv < 2:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.20)
            source[6] = int(source.get(6, 0)) + 200
        elif palam3_lv < 3:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.60)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.80)
        elif palam3_lv < 4:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.00)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.50)
        else:
            source[1] = self._scale_value(int(source.get(1, 0)), 2.00)
            source[6] = self._scale_value(int(source.get(6, 0)), 0.10)

        # PALAM:欲情
        palam5_lv = self._get_palam_level(palam5)
        if palam5_lv < 1:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.50)
        elif palam5_lv < 2:
            source[1] = self._scale_value(int(source.get(1, 0)), 0.80)
        elif palam5_lv < 3:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.20)
        elif palam5_lv < 4:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.50)
        else:
            source[1] = self._scale_value(int(source.get(1, 0)), 1.80)

        # 私处敏感 TALENT:103 / 私处钝感 TALENT:104
        if int(target.talent.get(103, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 1.50)
            source[5] = self._scale_value(int(source.get(5, 0)), 1.50)
            source[13] = self._scale_value(int(source.get(13, 0)), 1.50)
        elif int(target.talent.get(104, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 0.60)
            source[5] = self._scale_value(int(source.get(5, 0)), 0.60)
            source[13] = self._scale_value(int(source.get(13, 0)), 0.60)

        # 处女+看重贞操
        if exp0 == 0 and int(target.talent.get(30, 0)):
            source[5] = self._scale_value(int(source.get(5, 0)), 2.00)

        # 未熟 TALENT:135
        if int(target.talent.get(135, 0)):
            source[6] = self._scale_value(int(source.get(6, 0)), 2.00)

        return source




    def _comf9(self, target: Character) -> Dict[str, int]:
        """舔肛 SOURCE计算"""
        self._comf_apply_side_effects(9, target)
        source: Dict[str, int] = {}

        abl3 = target.get_abl(3)  # 肛门感觉

        # 基础SOURCE
        source[7] = 50
        source[12] = 300
        source[13] = 500

        # ABL:肛门感觉
        if abl3 == 0:
            source[2] = 5
        elif abl3 == 1:
            source[2] = 50
        elif abl3 == 2:
            source[2] = 200
        elif abl3 == 3:
            source[2] = 500
        elif abl3 == 4:
            source[2] = 1000
        else:
            source[2] = 1800

        # 调教者擅用舌头 TALENT:PLAYER:52
        player = self._get_player()
        if player is not None and int(player.talent.get(52, 0)):
            source[2] = self._scale_value(int(source.get(2, 0)), 2.00)
            source[11] = int(source.get(2, 0)) // 20

        return source




    def _comf10(self, target: Character) -> Dict[str, int]:
        """振动宝石 SOURCE计算"""
        self._comf_apply_side_effects(10, target)
        return self._calc_comf_source(10, target)


    def _comf11(self, target: Character) -> Dict[str, int]:
        """バイブ SOURCE计算"""
        self._comf_apply_side_effects(11, target)
        source = {}
        # ABL:私处感觉(2)をみる
        abl2 = target.get_abl(2)
        if abl2 == 0:
            source[1] = 80
        elif abl2 == 1:
            source[1] = 250
        elif abl2 == 2:
            source[1] = 600
        elif abl2 == 3:
            source[1] = 1000
        elif abl2 == 4:
            source[1] = 1300
        else:
            source[1] = 1700
        # EXP:私处经验(0)をみる
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 50:
            source[1] = int(source[1] * 0.20)
            source[12] = 5500
        elif exp0 < 200:
            source[1] = int(source[1] * 0.60)
            source[12] = 300
        elif exp0 < 500:
            source[1] = int(source[1] * 1.00)
            source[12] = 50
        elif exp0 < 1000:
            source[1] = int(source[1] * 1.20)
            source[12] = 10
        elif exp0 < 3000:
            source[1] = int(source[1] * 1.40)
            source[12] = 0
        else:
            source[1] = int(source[1] * 1.60)
            source[12] = 0
        # PALAM:润滑(3)をみる
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            source[1] = int(source[1] * 0.10)
            source[12] = source.get(12, 0) + 1000
            source[12] = int(source[12] * 3.00)
        elif palam3 < 300:
            source[1] = int(source[1] * 0.40)
            source[12] = source.get(12, 0) + 400
            source[12] = int(source[12] * 1.00)
        elif palam3 < 1000:
            source[1] = int(source[1] * 1.00)
            source[12] = int(source.get(12, 0) * 0.50)
        elif palam3 < 3000:
            source[1] = int(source[1] * 1.40)
            source[12] = int(source.get(12, 0) * 0.20)
        else:
            source[1] = int(source[1] * 1.80)
            source[12] = int(source.get(12, 0) * 0.10)
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[1] = int(source[1] * 0.80)
        elif palam5 < 300:
            source[1] = int(source[1] * 0.90)
        elif palam5 < 1000:
            source[1] = int(source[1] * 1.00)
        elif palam5 < 3000:
            source[1] = int(source[1] * 1.10)
        else:
            source[1] = int(source[1] * 1.20)
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[1] = int(source[1] * 0.80)
        elif abl10 == 1:
            source[1] = int(source[1] * 0.90)
        elif abl10 == 2:
            source[1] = int(source[1] * 1.00)
        elif abl10 == 3:
            source[1] = int(source[1] * 1.10)
        elif abl10 == 4:
            source[1] = int(source[1] * 1.20)
        else:
            source[1] = int(source[1] * 1.30)
        # 魁梧(99)
        if int(target.talent.get(99, 0)):
            source[12] = int(source.get(12, 0) * 0.80)
        # 娇小(100)
        if int(target.talent.get(100, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 未熟(135)
        if int(target.talent.get(135, 0)):
            source[12] = int(source.get(12, 0) * 4.00)
        return source




    def _comf12(self, target: Character) -> Dict[str, int]:
        """振動の杖 SOURCE计算"""
        self._comf_apply_side_effects(12, target)
        return self._calc_comf_source(12, target)


    def _comf13(self, target: Character) -> Dict[str, int]:
        """アナルワーム SOURCE计算"""
        self._comf_apply_side_effects(13, target)
        source = {}
        source[3] = 300
        # ABL:肛门感觉(3)をみる
        abl3 = target.get_abl(3)
        if abl3 == 0:
            source[2] = 80
            source[5] = 300
        elif abl3 == 1:
            source[2] = 250
            source[5] = 800
        elif abl3 == 2:
            source[2] = 600
            source[5] = 1400
        elif abl3 == 3:
            source[2] = 1000
            source[5] = 1800
        elif abl3 == 4:
            source[2] = 1300
            source[5] = 2100
        else:
            source[2] = 1700
            source[5] = 2400
        # EXP:肛门经验(1)をみる
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 50:
            source[2] = int(source[2] * 0.50)
            source[12] = 2000
            source[3] = source.get(3, 0) + 200
        elif exp1 < 200:
            source[2] = int(source[2] * 1.00)
            source[12] = 300
            source[3] = source.get(3, 0) + 100
        elif exp1 < 500:
            source[2] = int(source[2] * 1.10)
            source[12] = 50
            source[3] = source.get(3, 0) + 50
        elif exp1 < 1000:
            source[2] = int(source[2] * 1.20)
            source[12] = 10
        elif exp1 < 3000:
            source[2] = int(source[2] * 1.40)
            source[12] = 0
        else:
            source[2] = int(source[2] * 1.60)
            source[12] = 0
        # PALAM:润滑(3)をみる
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            source[2] = int(source[2] * 0.40)
            source[12] = source.get(12, 0) + 800
        elif palam3 < 300:
            source[2] = int(source[2] * 0.80)
            source[12] = source.get(12, 0) + 500
        elif palam3 < 1000:
            source[2] = int(source[2] * 1.00)
            source[12] = source.get(12, 0) + 300
        elif palam3 < 3000:
            source[2] = int(source[2] * 1.40)
            source[12] = source.get(12, 0) + 120
        else:
            source[2] = int(source[2] * 1.80)
            source[12] = source.get(12, 0) + 100
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[2] = int(source[2] * 0.80)
        elif palam5 < 300:
            source[2] = int(source[2] * 0.90)
        elif palam5 < 1000:
            source[2] = int(source[2] * 1.00)
        elif palam5 < 3000:
            source[2] = int(source[2] * 1.10)
        else:
            source[2] = int(source[2] * 1.20)
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[2] = int(source[2] * 0.80)
            source[3] = int(source.get(3, 0) * 2.00)
        elif abl10 == 1:
            source[2] = int(source[2] * 0.90)
            source[3] = int(source.get(3, 0) * 1.50)
        elif abl10 == 2:
            source[3] = int(source.get(3, 0) * 1.00)
        elif abl10 == 3:
            source[3] = int(source.get(3, 0) * 0.80)
        elif abl10 == 4:
            source[3] = int(source.get(3, 0) * 0.60)
        else:
            source[3] = int(source.get(3, 0) * 0.30)
        # 魁梧(99)
        if int(target.talent.get(99, 0)):
            source[12] = int(source.get(12, 0) * 0.80)
        # 娇小(100)
        if int(target.talent.get(100, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 未熟(135)
        if int(target.talent.get(135, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 肛门敏感(105)/肛门迟钝(106)
        if int(target.talent.get(105, 0)):
            source[12] = int(source.get(12, 0) * 1.50)
            source[5] = int(source.get(5, 0) * 1.50)
            source[3] = int(source.get(3, 0) * 1.50)
        elif int(target.talent.get(106, 0)):
            source[12] = int(source.get(12, 0) * 0.60)
            source[5] = int(source.get(5, 0) * 0.60)
            source[3] = int(source.get(3, 0) * 0.60)
        # 处女で看重贞操
        exp0 = int(target.exp.get(0, 0))
        if exp0 == 0 and int(target.talent.get(30, 0)):
            source[5] = source.get(5, 0) // 3
        return source




    def _comf14(self, target: Character) -> Dict[str, int]:
        """クリキャップ SOURCE计算"""
        self._comf_apply_side_effects(14, target)
        return self._calc_comf_source(14, target)


    def _comf15(self, target: Character) -> Dict[str, int]:
        """二プルキャップ SOURCE计算"""
        self._comf_apply_side_effects(15, target)
        return self._calc_comf_source(15, target)


    def _comf16(self, target: Character) -> Dict[str, int]:
        """搾乳器 SOURCE计算"""
        self._comf_apply_side_effects(16, target)
        return self._calc_comf_source(16, target)


    def _comf17(self, target: Character) -> Dict[str, int]:
        """オナホール SOURCE计算"""
        self._comf_apply_side_effects(17, target)
        return self._calc_comf_source(17, target)


    def _comf18(self, target: Character) -> Dict[str, int]:
        """シャワー SOURCE计算"""
        self._comf_apply_side_effects(18, target)
        source = {}
        source[3] = 50
        source[6] = 400
        source[11] = 200
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[15] = 10
        elif palam5 < 300:
            source[15] = 30
        elif palam5 < 1000:
            source[15] = 60
        elif palam5 < 3000:
            source[15] = 100
        else:
            source[15] = 150
        # 侍奉精神(16)をみる
        abl16 = target.get_abl(16)
        if abl16 == 0:
            source[17] = 0
        elif abl16 == 1:
            source[17] = 20
        elif abl16 == 2:
            source[17] = 40
        elif abl16 == 3:
            source[17] = 70
        elif abl16 == 4:
            source[17] = 110
        else:
            source[17] = 150
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[6] = int(source.get(6, 0) * 0.80)
        elif abl10 == 1:
            source[6] = int(source.get(6, 0) * 0.90)
        elif abl10 == 2:
            source[6] = int(source.get(6, 0) * 1.00)
        elif abl10 == 3:
            source[6] = int(source.get(6, 0) * 1.10)
        elif abl10 == 4:
            source[6] = int(source.get(6, 0) * 1.20)
        else:
            source[6] = int(source.get(6, 0) * 1.30)
        # 动物耳朵(124)
        if int(target.talent.get(124, 0)):
            source[3] = int(source.get(3, 0) * 1.60)
            source[5] = int(source.get(5, 0) * 1.50) if source.get(5, 0) else 0
            source[14] = int(source.get(14, 0) * 2.00) if source.get(14, 0) else 0
        return source




    def _comf19(self, target: Character) -> Dict[str, int]:
        """アナルビーズ SOURCE计算"""
        self._comf_apply_side_effects(19, target)
        source = {}
        # ABL:肛门感觉(3)をみる
        abl3 = target.get_abl(3)
        if abl3 == 0:
            source[2] = 80
            source[5] = 300
        elif abl3 == 1:
            source[2] = 250
            source[5] = 800
        elif abl3 == 2:
            source[2] = 600
            source[5] = 1400
        elif abl3 == 3:
            source[2] = 1000
            source[5] = 1800
        elif abl3 == 4:
            source[2] = 1300
            source[5] = 2100
        else:
            source[2] = 1700
            source[5] = 2400
        # EXP:肛门经验(1)をみる
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 50:
            source[2] = int(source[2] * 0.50)
            source[12] = 2000
        elif exp1 < 200:
            source[2] = int(source[2] * 1.00)
            source[12] = 300
        elif exp1 < 500:
            source[2] = int(source[2] * 1.10)
            source[12] = 50
        elif exp1 < 1000:
            source[2] = int(source[2] * 1.20)
            source[12] = 10
        elif exp1 < 3000:
            source[2] = int(source[2] * 1.40)
            source[12] = 0
        else:
            source[2] = int(source[2] * 1.60)
            source[12] = 0
        # PALAM:润滑(3)をみる
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            source[2] = int(source[2] * 0.40)
            source[12] = source.get(12, 0) + 1200
        elif palam3 < 300:
            source[2] = int(source[2] * 0.80)
            source[12] = source.get(12, 0) + 700
        elif palam3 < 1000:
            source[2] = int(source[2] * 1.00)
            source[12] = source.get(12, 0) + 400
        elif palam3 < 3000:
            source[2] = int(source[2] * 1.40)
            source[12] = source.get(12, 0) + 150
        else:
            source[2] = int(source[2] * 1.80)
            source[12] = source.get(12, 0) + 100
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[2] = int(source[2] * 0.80)
        elif palam5 < 300:
            source[2] = int(source[2] * 0.90)
        elif palam5 < 1000:
            source[2] = int(source[2] * 1.00)
        elif palam5 < 3000:
            source[2] = int(source[2] * 1.10)
        else:
            source[2] = int(source[2] * 1.20)
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[2] = int(source[2] * 0.80)
        elif abl10 == 1:
            source[2] = int(source[2] * 0.90)
        elif abl10 == 2:
            source[2] = int(source[2] * 1.00)
        elif abl10 == 3:
            source[2] = int(source[2] * 1.10)
        elif abl10 == 4:
            source[2] = int(source[2] * 1.20)
        else:
            source[2] = int(source[2] * 1.30)
        # 魁梧(99)
        if int(target.talent.get(99, 0)):
            source[12] = int(source.get(12, 0) * 0.80)
        # 娇小(100)
        if int(target.talent.get(100, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 未熟(135)
        if int(target.talent.get(135, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 肛门敏感(105)/肛门迟钝(106)
        if int(target.talent.get(105, 0)):
            source[12] = int(source.get(12, 0) * 1.50)
            source[5] = int(source.get(5, 0) * 1.50)
            source[3] = int(source.get(3, 0) * 1.50) if source.get(3, 0) else 0
        elif int(target.talent.get(106, 0)):
            source[12] = int(source.get(12, 0) * 0.60)
            source[5] = int(source.get(5, 0) * 0.60)
            source[3] = int(source.get(3, 0) * 0.60) if source.get(3, 0) else 0
        # 处女で看重贞操
        exp0 = int(target.exp.get(0, 0))
        if exp0 == 0 and int(target.talent.get(30, 0)):
            source[5] = source.get(5, 0) // 3
        return source




    def _comf20(self, target: Character) -> Dict[str, int]:
        """正常位 SOURCE计算"""
        self._comf_apply_side_effects(20, target)
        source = {}
        source[12] = 400
        # ABL:私处感觉(2)をみる
        abl2 = target.get_abl(2)
        if abl2 == 0:
            source[1] = 40
            source[3] = 150
        elif abl2 == 1:
            source[1] = 150
            source[3] = 250
        elif abl2 == 2:
            source[1] = 400
            source[3] = 350
        elif abl2 == 3:
            source[1] = 1000
            source[3] = 500
        elif abl2 == 4:
            source[1] = 1700
            source[3] = 700
        else:
            source[1] = 2200
            source[3] = 1000
        # EXP:私处经验(0)をみる
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 50:
            source[1] = int(source[1] * 0.20)
            source[6] = 5500
        elif exp0 < 200:
            source[1] = int(source[1] * 0.60)
            source[6] = 300
        elif exp0 < 500:
            source[1] = int(source[1] * 1.00)
            source[6] = 50
        elif exp0 < 1000:
            source[1] = int(source[1] * 1.20)
            source[6] = 10
        elif exp0 < 3000:
            source[1] = int(source[1] * 1.30)
            source[6] = 0
        else:
            source[1] = int(source[1] * 1.80)
            source[6] = 0
        # PALAM:润滑(3)をみる
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            source[1] = int(source[1] * 0.10)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source.get(6, 0) * 3.00)
        elif palam3 < 300:
            source[1] = int(source[1] * 0.40)
            source[6] = source.get(6, 0) + 300
            source[6] = int(source.get(6, 0) * 1.00)
        elif palam3 < 1000:
            source[1] = int(source[1] * 1.00)
            source[6] = int(source.get(6, 0) * 0.50)
        elif palam3 < 3000:
            source[1] = int(source[1] * 1.40)
            source[6] = int(source.get(6, 0) * 0.20)
        else:
            source[1] = int(source[1] * 1.80)
            source[6] = int(source.get(6, 0) * 0.10)
        # 魁梧(99)
        if int(target.talent.get(99, 0)):
            source[6] = int(source.get(6, 0) * 0.80)
        # 娇小(100)
        if int(target.talent.get(100, 0)):
            source[6] = int(source.get(6, 0) * 2.00)
        # 未熟(135)
        if int(target.talent.get(135, 0)):
            source[6] = int(source.get(6, 0) * 4.00)
        # 看重贞操(30)/看轻贞操(31)
        if int(target.talent.get(30, 0)):
            if exp0 == 0:
                source[3] = int(source.get(3, 0) * 0.60)
                source[15] = 10000
            else:
                source[3] = int(source.get(3, 0) * 0.60)
                source[15] = 1000
        elif int(target.talent.get(31, 0)):
            if exp0 == 0:
                source[3] = int(source.get(3, 0) * 0.60)
                source[15] = 300
        else:
            if exp0 == 0:
                source[15] = 3000
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[1] = int(source[1] * 0.60)
            source[3] = int(source.get(3, 0) * 0.30)
        elif palam5 < 300:
            source[1] = int(source[1] * 0.80)
            source[3] = int(source.get(3, 0) * 0.60)
        elif palam5 < 1000:
            source[1] = int(source[1] * 1.00)
            source[3] = int(source.get(3, 0) * 1.00)
        elif palam5 < 3000:
            source[1] = int(source[1] * 1.20)
            source[3] = int(source.get(3, 0) * 1.50)
        else:
            source[1] = int(source[1] * 1.50)
            source[3] = int(source.get(3, 0) * 1.80)
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[1] = int(source[1] * 0.50)
            source[3] = int(source.get(3, 0) * 0.60)
            source[15] = int(source.get(15, 0) * 2.00)
        elif abl10 == 1:
            source[1] = int(source[1] * 0.80)
            source[3] = int(source.get(3, 0) * 0.80)
            source[15] = int(source.get(15, 0) * 1.50)
        elif abl10 == 2:
            source[1] = int(source[1] * 1.00)
            source[3] = int(source.get(3, 0) * 1.00)
            source[15] = int(source.get(15, 0) * 1.00)
        elif abl10 == 3:
            source[1] = int(source[1] * 1.30)
            source[3] = int(source.get(3, 0) * 1.20)
            source[15] = int(source.get(15, 0) * 0.80)
        elif abl10 == 4:
            source[1] = int(source[1] * 1.60)
            source[3] = int(source.get(3, 0) * 1.40)
            source[15] = int(source.get(15, 0) * 0.60)
        else:
            source[1] = int(source[1] * 2.00)
            source[3] = int(source.get(3, 0) * 1.60)
            source[15] = int(source.get(15, 0) * 0.30)
        return source




    def _comf21(self, target: Character) -> Dict[str, int]:
        """後背位 SOURCE计算"""
        self._comf_apply_side_effects(21, target)
        source = {}
        source[15] = 800
        # ABL:私处感觉(2)をみる
        abl2 = target.get_abl(2)
        if abl2 == 0:
            source[1] = 40
            source[17] = 50
        elif abl2 == 1:
            source[1] = 150
            source[17] = 150
        elif abl2 == 2:
            source[1] = 400
            source[17] = 250
        elif abl2 == 3:
            source[1] = 1000
            source[17] = 350
        elif abl2 == 4:
            source[1] = 1700
            source[17] = 600
        else:
            source[1] = 2200
            source[17] = 850
        # EXP:私处经验(0)をみる
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 50:
            source[1] = int(source[1] * 0.20)
            source[12] = 5000
        elif exp0 < 200:
            source[1] = int(source[1] * 0.60)
            source[12] = 220
        elif exp0 < 500:
            source[1] = int(source[1] * 1.00)
            source[12] = 30
        elif exp0 < 1000:
            source[1] = int(source[1] * 1.20)
            source[12] = 5
        elif exp0 < 3000:
            source[1] = int(source[1] * 1.30)
            source[12] = 0
        else:
            source[1] = int(source[1] * 1.80)
            source[12] = 0
        # PALAM:润滑(3)をみる
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            source[1] = int(source[1] * 0.10)
            source[12] = source.get(12, 0) + 900
            source[12] = int(source.get(12, 0) * 3.00)
        elif palam3 < 300:
            source[1] = int(source[1] * 0.40)
            source[12] = source.get(12, 0) + 250
            source[12] = int(source.get(12, 0) * 1.00)
        elif palam3 < 1000:
            source[1] = int(source[1] * 1.00)
            source[12] = int(source.get(12, 0) * 0.50)
        elif palam3 < 3000:
            source[1] = int(source[1] * 1.40)
            source[12] = int(source.get(12, 0) * 0.20)
        else:
            source[1] = int(source[1] * 1.80)
            source[12] = int(source.get(12, 0) * 0.10)
        # 魁梧(99)
        if int(target.talent.get(99, 0)):
            source[12] = int(source.get(12, 0) * 1.80)
        # 娇小(100)
        if int(target.talent.get(100, 0)):
            source[12] = int(source.get(12, 0) * 2.00)
        # 看重贞操(30)/看轻贞操(31)
        if int(target.talent.get(30, 0)):
            if exp0 == 0:
                source[17] = int(source.get(17, 0) * 0.60)
                source[14] = 10000
            else:
                source[17] = int(source.get(17, 0) * 0.60)
                source[14] = 1000
        elif int(target.talent.get(31, 0)):
            if exp0 == 0:
                source[17] = int(source.get(17, 0) * 0.60)
                source[14] = 300
        else:
            if exp0 == 0:
                source[14] = 3000
        # PALAM:欲情(5)をみる
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            source[1] = int(source[1] * 0.60)
            source[17] = int(source.get(17, 0) * 0.30)
        elif palam5 < 300:
            source[1] = int(source[1] * 0.80)
            source[17] = int(source.get(17, 0) * 0.60)
        elif palam5 < 1000:
            source[1] = int(source[1] * 1.00)
            source[17] = int(source.get(17, 0) * 1.00)
        elif palam5 < 3000:
            source[1] = int(source[1] * 1.20)
            source[17] = int(source.get(17, 0) * 1.50)
        else:
            source[1] = int(source[1] * 1.50)
            source[17] = int(source.get(17, 0) * 1.80)
        # ABL:顺从(10)をみる
        abl10 = target.get_abl(10)
        if abl10 == 0:
            source[1] = int(source[1] * 0.50)
            source[17] = int(source.get(17, 0) * 0.60)
            source[14] = int(source.get(14, 0) * 2.00)
        elif abl10 == 1:
            source[1] = int(source[1] * 0.80)
            source[17] = int(source.get(17, 0) * 0.80)
            source[14] = int(source.get(14, 0) * 1.50)
        elif abl10 == 2:
            source[1] = int(source[1] * 1.00)
            source[17] = int(source.get(17, 0) * 1.00)
            source[14] = int(source.get(14, 0) * 1.00)
        elif abl10 == 3:
            source[1] = int(source[1] * 1.30)
            source[17] = int(source.get(17, 0) * 1.20)
            source[14] = int(source.get(14, 0) * 0.80)
        elif abl10 == 4:
            source[1] = int(source[1] * 1.60)
            source[17] = int(source.get(17, 0) * 1.40)
            source[14] = int(source.get(14, 0) * 0.60)
        else:
            source[1] = int(source[1] * 2.00)
            source[17] = int(source.get(17, 0) * 1.60)
            source[14] = int(source.get(14, 0) * 0.30)
        return source

    # =====================================================================
    # COMF22-COMF42 SOURCE计算
    # =====================================================================




    def _comf22(self, target: Character) -> Dict[str, int]:
        """对面座位 SOURCE计算"""
        self._comf_apply_side_effects(22, target)
        s: Dict[str, int] = {}
        s["屈辱"] = 100
        s["反感"] = 100
        abl2 = target.get_abl(2)
        if abl2 == 0:
            s["快V"] = 40; s["快B"] = 150
        elif abl2 == 1:
            s["快V"] = 150; s["快B"] = 250
        elif abl2 == 2:
            s["快V"] = 300; s["快B"] = 350
        elif abl2 == 3:
            s["快V"] = 700; s["快B"] = 500
        elif abl2 == 4:
            s["快V"] = 1100; s["快B"] = 700
        else:
            s["快V"] = 1500; s["快B"] = 1000
        # EXP:私处经验
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 1:
            s["快V"] = int(s["快V"] * 0.20); s["露出"] = 3500
        elif exp0 < 4:
            s["快V"] = int(s["快V"] * 0.60); s["露出"] = 250
        elif exp0 < 20:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = 50
        elif exp0 < 50:
            s["快V"] = int(s["快V"] * 1.10); s["露出"] = 10
        elif exp0 < 200:
            s["快V"] = int(s["快V"] * 1.20); s["露出"] = 0
        else:
            s["快V"] = int(s["快V"] * 1.30); s["露出"] = 0
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 50; s["恐怖"] = 10; s["发育"] = 100; s["不洁"] = int(s.get("不洁", 0) * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 150; s["恐怖"] = 50; s["发育"] = 300; s["不洁"] = int(s.get("不洁", 0) * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 300; s["恐怖"] = 100; s["发育"] = 700; s["不洁"] = int(s.get("不洁", 0) * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 400; s["恐怖"] = 200; s["发育"] = 1200; s["不洁"] = int(s.get("不洁", 0) * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 500; s["恐怖"] = 300; s["发育"] = 1800; s["不洁"] = int(s.get("不洁", 0) * 0.50)
        else:
            s["痛苦"] = 800; s["恐怖"] = 500; s["发育"] = 2500; s["不洁"] = int(s.get("不洁", 0) * 0.10)
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快V"] = int(s["快V"] * 0.50); s["露出"] = s.get("露出", 0) + 1000; s["露出"] = int(s["露出"] * 2.50)
        elif palam3 < 500:
            s["快V"] = int(s["快V"] * 0.80); s["露出"] = s.get("露出", 0) + 300; s["露出"] = int(s["露出"] * 1.00)
        elif palam3 < 3000:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = int(s.get("露出", 0) * 0.50)
        elif palam3 < 10000:
            s["快V"] = int(s["快V"] * 1.20); s["露出"] = int(s.get("露出", 0) * 0.20)
        else:
            s["快V"] = int(s["快V"] * 1.50); s["露出"] = int(s.get("露出", 0) * 0.10)
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 4.00)
        # 看重贞操/看轻贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 0.60)
            if exp0 == 0:
                s["压抑"] = 10000
            else:
                s["压抑"] = 1000
        elif int(target.talent.get(31, 0)):
            if exp0 == 0:
                s["快B"] = int(s["快B"] * 0.60); s["压抑"] = 300
        else:
            if exp0 == 0:
                s["压抑"] = 3000
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快V"] = int(s["快V"] * 0.80); s["快B"] = int(s["快B"] * 0.90); s["压抑"] = int(s.get("压抑", 0) * 2.00)
        elif abl10 == 1:
            s["快V"] = int(s["快V"] * 1.10); s["快B"] = int(s["快B"] * 1.20); s["压抑"] = int(s.get("压抑", 0) * 1.60)
        elif abl10 == 2:
            s["快V"] = int(s["快V"] * 1.50); s["快B"] = int(s["快B"] * 1.60); s["压抑"] = int(s.get("压抑", 0) * 1.20)
        elif abl10 == 3:
            s["快V"] = int(s["快V"] * 1.80); s["快B"] = int(s["快B"] * 1.90); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        elif abl10 == 4:
            s["快V"] = int(s["快V"] * 2.40); s["快B"] = int(s["快B"] * 2.60); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        else:
            s["快V"] = int(s["快V"] * 3.00); s["快B"] = int(s["快B"] * 3.60); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        # 爱慕
        if int(target.talent.get(85, 0)):
            s["快B"] = int(s["快B"] * 3.00); s["屈辱"] = int(s["屈辱"] * 2.00); s["发育"] = int(s["发育"] * 2.00)
        return s




    def _comf23(self, target: Character) -> Dict[str, int]:
        """背面座位 SOURCE计算"""
        self._comf_apply_side_effects(23, target)
        s: Dict[str, int] = {}
        s["反感"] = 200
        abl2 = target.get_abl(2)
        if abl2 == 0:
            s["快V"] = 50; s["快B"] = 50
        elif abl2 == 1:
            s["快V"] = 150; s["快B"] = 100
        elif abl2 == 2:
            s["快V"] = 300; s["快B"] = 200
        elif abl2 == 3:
            s["快V"] = 600; s["快B"] = 300
        elif abl2 == 4:
            s["快V"] = 1000; s["快B"] = 500
        else:
            s["快V"] = 1500; s["快B"] = 700
        # EXP:私处经验
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 1:
            s["快V"] = int(s["快V"] * 0.20); s["露出"] = 3000
        elif exp0 < 4:
            s["快V"] = int(s["快V"] * 0.60); s["露出"] = 240
        elif exp0 < 20:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = 30
        elif exp0 < 50:
            s["快V"] = int(s["快V"] * 1.20); s["露出"] = 5
        elif exp0 < 200:
            s["快V"] = int(s["快V"] * 1.40); s["露出"] = 0
        else:
            s["快V"] = int(s["快V"] * 1.60); s["露出"] = 0
        # ABL:乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            s["损腐"] = 50; s["快B"] = s.get("快B", 0) + 50
        elif abl1 == 1:
            s["损腐"] = 200; s["快B"] = s.get("快B", 0) + 200
        elif abl1 == 2:
            s["损腐"] = 500; s["快B"] = s.get("快B", 0) + 400
        elif abl1 == 3:
            s["损腐"] = 800; s["快B"] = s.get("快B", 0) + 600
        elif abl1 == 4:
            s["损腐"] = 1300; s["快B"] = s.get("快B", 0) + 1000
        else:
            s["损腐"] = 1800; s["快B"] = s.get("快B", 0) + 1400
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 40
        elif abl0 == 1:
            s["快C"] = 160
        elif abl0 == 2:
            s["快C"] = 500
        elif abl0 == 3:
            s["快C"] = 900
        elif abl0 == 4:
            s["快C"] = 1400
        else:
            s["快C"] = 2100
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快V"] = int(s["快V"] * 0.40); s["露出"] = s.get("露出", 0) + 600; s["露出"] = int(s["露出"] * 2.60)
        elif palam3 < 500:
            s["快V"] = int(s["快V"] * 0.70); s["露出"] = s.get("露出", 0) + 180; s["露出"] = int(s["露出"] * 1.00)
        elif palam3 < 3000:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = int(s.get("露出", 0) * 0.50)
        elif palam3 < 10000:
            s["快V"] = int(s["快V"] * 1.20); s["露出"] = int(s.get("露出", 0) * 0.20)
        else:
            s["快V"] = int(s["快V"] * 1.60); s["露出"] = int(s.get("露出", 0) * 0.10)
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 4.00)
        # 看重贞操/看轻贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 0.60)
            if exp0 == 0:
                s["压抑"] = 10000
            else:
                s["压抑"] = 1000
        elif int(target.talent.get(31, 0)):
            if exp0 == 0:
                s["快B"] = int(s["快B"] * 0.60); s["压抑"] = 300
        else:
            if exp0 == 0:
                s["压抑"] = 3000
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快V"] = int(s["快V"] * 1.50); s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 2.00)
        elif abl10 == 1:
            s["快V"] = int(s["快V"] * 1.50); s["快B"] = int(s["快B"] * 1.30); s["压抑"] = int(s.get("压抑", 0) * 1.80)
        elif abl10 == 2:
            s["快V"] = int(s["快V"] * 1.50); s["快B"] = int(s["快B"] * 1.50); s["压抑"] = int(s.get("压抑", 0) * 1.60)
        elif abl10 == 3:
            s["快V"] = int(s["快V"] * 1.80); s["快B"] = int(s["快B"] * 1.90); s["压抑"] = int(s.get("压抑", 0) * 1.40)
        elif abl10 == 4:
            s["快V"] = int(s["快V"] * 2.10); s["快B"] = int(s["快B"] * 2.20); s["压抑"] = int(s.get("压抑", 0) * 1.20)
        else:
            s["快V"] = int(s["快V"] * 2.50); s["快B"] = int(s["快B"] * 2.60); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        # 爱慕
        if int(target.talent.get(85, 0)):
            s["快B"] = int(s["快B"] * 2.00)
        return s




    def _comf24(self, target: Character) -> Dict[str, int]:
        """逆レイプ SOURCE计算"""
        self._comf_apply_side_effects(24, target)
        s: Dict[str, int] = {}
        s["反感"] = 220
        s["情爱"] = 50
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 50
        elif abl0 == 1:
            s["快C"] = 200
        elif abl0 == 2:
            s["快C"] = 800
        elif abl0 == 3:
            s["快C"] = 1600
        elif abl0 == 4:
            s["快C"] = 2400
        else:
            s["快C"] = 3200
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快C"] = 800; s["痛苦"] = 1600; s["恐怖"] = 200
        elif abl16 == 1:
            s["快C"] = 1400; s["痛苦"] = 1900; s["恐怖"] = 400
        elif abl16 == 2:
            s["快C"] = 2000; s["痛苦"] = 2300; s["恐怖"] = 750
        elif abl16 == 3:
            s["快C"] = 2500; s["痛苦"] = 2700; s["恐怖"] = 1150
        elif abl16 == 4:
            s["快C"] = 2900; s["痛苦"] = 3100; s["恐怖"] = 1750
        else:
            s["快C"] = 3200; s["痛苦"] = 3500; s["恐怖"] = 2500
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        elif abl12 == 4:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        elif abl12 == 5:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 2.50); s["恐怖"] = int(s["恐怖"] * 2.50)
        elif abl12 == 6:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 3.00); s["恐怖"] = int(s["恐怖"] * 3.00)
        elif abl12 == 7:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 3.50); s["恐怖"] = int(s["恐怖"] * 3.50)
        else:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 4.00); s["恐怖"] = int(s["恐怖"] * 4.00)
        # 百合气质/ホモっ気
        if int(target.talent.get(122, 0)) == 0:
            abl22 = int(target.abl.get(22, 0))
            if abl22 == 0:
                s["痛苦"] = int(s["痛苦"] * 0.20); s["恐怖"] = int(s["恐怖"] * 0.20)
            elif abl22 == 1:
                s["痛苦"] = int(s["痛苦"] * 0.40); s["恐怖"] = int(s["恐怖"] * 0.40)
            elif abl22 == 2:
                s["痛苦"] = int(s["痛苦"] * 0.60); s["恐怖"] = int(s["恐怖"] * 0.60)
            elif abl22 == 3:
                s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
            elif abl22 == 4:
                s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
            else:
                s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif int(target.talent.get(122, 0)) == 1:
            abl23 = int(target.abl.get(23, 0))
            if abl23 == 0:
                s["痛苦"] = int(s["痛苦"] * 0.20); s["恐怖"] = int(s["恐怖"] * 0.20)
            elif abl23 == 1:
                s["痛苦"] = int(s["痛苦"] * 0.40); s["恐怖"] = int(s["恐怖"] * 0.40)
            elif abl23 == 2:
                s["痛苦"] = int(s["痛苦"] * 0.60); s["恐怖"] = int(s["恐怖"] * 0.60)
            elif abl23 == 3:
                s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
            elif abl23 == 4:
                s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
            else:
                s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        return s




    def _comf25(self, target: Character) -> Dict[str, int]:
        """逆アナルレイプ SOURCE计算"""
        self._comf_apply_side_effects(25, target)
        s: Dict[str, int] = {}
        s["反感"] = 220
        s["情爱"] = 50
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 50
        elif abl0 == 1:
            s["快C"] = 200
        elif abl0 == 2:
            s["快C"] = 800
        elif abl0 == 3:
            s["快C"] = 1600
        elif abl0 == 4:
            s["快C"] = 2400
        else:
            s["快C"] = 3200
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快C"] = 800; s["痛苦"] = 1600; s["恐怖"] = 200
        elif abl16 == 1:
            s["快C"] = 1400; s["痛苦"] = 1900; s["恐怖"] = 400
        elif abl16 == 2:
            s["快C"] = 2000; s["痛苦"] = 2300; s["恐怖"] = 750
        elif abl16 == 3:
            s["快C"] = 2500; s["痛苦"] = 2700; s["恐怖"] = 1150
        elif abl16 == 4:
            s["快C"] = 2900; s["痛苦"] = 3100; s["恐怖"] = 1750
        else:
            s["快C"] = 3200; s["痛苦"] = 3500; s["恐怖"] = 2500
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        elif abl12 == 4:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        elif abl12 == 5:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 2.50); s["恐怖"] = int(s["恐怖"] * 2.50)
        elif abl12 == 6:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 3.00); s["恐怖"] = int(s["恐怖"] * 3.00)
        elif abl12 == 7:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 3.50); s["恐怖"] = int(s["恐怖"] * 3.50)
        else:
            s["快C"] = int(s["快C"] * 0.50); s["痛苦"] = int(s["痛苦"] * 4.00); s["恐怖"] = int(s["恐怖"] * 4.00)
        # 百合气质/ホモっ気
        if int(target.talent.get(122, 0)) == 0:
            abl22 = int(target.abl.get(22, 0))
            if abl22 == 0:
                s["痛苦"] = int(s["痛苦"] * 0.20); s["恐怖"] = int(s["恐怖"] * 0.20)
            elif abl22 == 1:
                s["痛苦"] = int(s["痛苦"] * 0.40); s["恐怖"] = int(s["恐怖"] * 0.40)
            elif abl22 == 2:
                s["痛苦"] = int(s["痛苦"] * 0.60); s["恐怖"] = int(s["恐怖"] * 0.60)
            elif abl22 == 3:
                s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
            elif abl22 == 4:
                s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
            else:
                s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif int(target.talent.get(122, 0)) == 1:
            abl23 = int(target.abl.get(23, 0))
            if abl23 == 0:
                s["痛苦"] = int(s["痛苦"] * 0.20); s["恐怖"] = int(s["恐怖"] * 0.20)
            elif abl23 == 1:
                s["痛苦"] = int(s["痛苦"] * 0.40); s["恐怖"] = int(s["恐怖"] * 0.40)
            elif abl23 == 2:
                s["痛苦"] = int(s["痛苦"] * 0.60); s["恐怖"] = int(s["恐怖"] * 0.60)
            elif abl23 == 3:
                s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
            elif abl23 == 4:
                s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
            else:
                s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        return s




    def _comf26(self, target: Character) -> Dict[str, int]:
        """正常位アナル SOURCE计算"""
        self._comf_apply_side_effects(26, target)
        s: Dict[str, int] = {}
        s["反感"] = 400
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 10; s["快B"] = 10; s["习得"] = 100
        elif abl3 == 1:
            s["快A"] = 30; s["快B"] = 30; s["习得"] = 500
        elif abl3 == 2:
            s["快A"] = 400; s["快B"] = 150; s["习得"] = 1200
        elif abl3 == 3:
            s["快A"] = 900; s["快B"] = 300; s["习得"] = 2400
        elif abl3 == 4:
            s["快A"] = 1600; s["快B"] = 500; s["习得"] = 3600
        else:
            s["快A"] = 2100; s["快B"] = 900; s["习得"] = 5000
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 1:
            s["快A"] = int(s["快A"] * 0.10); s["露出"] = 20000
        elif exp1 < 4:
            s["快A"] = int(s["快A"] * 0.30); s["露出"] = 12000
        elif exp1 < 20:
            s["快A"] = int(s["快A"] * 0.50); s["露出"] = 5000
        elif exp1 < 50:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = 1800
        elif exp1 < 200:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = 1000
        else:
            s["快A"] = int(s["快A"] * 1.60); s["露出"] = 600
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = int(s["快A"] * 0.40); s["露出"] = s.get("露出", 0) + 10000
        elif palam3 < 500:
            s["快A"] = int(s["快A"] * 0.80); s["露出"] = s.get("露出", 0) + 3600
        elif palam3 < 3000:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = s.get("露出", 0) + 1200
        elif palam3 < 10000:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = s.get("露出", 0) + 200
        else:
            s["快A"] = int(s["快A"] * 1.80); s["露出"] = s.get("露出", 0) + 100
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 看重贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 1.20); s["发育"] = int(s.get("发育", 0) * 1.10)
            if exp1 == 0:
                s["压抑"] = 500
            else:
                s["压抑"] = 0
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快B"] = int(s["快B"] * 0.60); s["压抑"] = int(s.get("压抑", 0) * 2.00)
        elif abl10 == 1:
            s["快B"] = int(s["快B"] * 0.80); s["压抑"] = int(s.get("压抑", 0) * 1.50)
        elif abl10 == 2:
            s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        elif abl10 == 3:
            s["快B"] = int(s["快B"] * 1.20); s["压抑"] = int(s.get("压抑", 0) * 0.80)
        elif abl10 == 4:
            s["快B"] = int(s["快B"] * 1.40); s["压抑"] = int(s.get("压抑", 0) * 0.60)
        else:
            s["快B"] = int(s["快B"] * 1.60); s["压抑"] = int(s.get("压抑", 0) * 0.30)
        # 肛门敏感/肛门钝感
        if int(target.talent.get(105, 0)):
            s["露出"] = int(s.get("露出", 0) * 1.50); s["习得"] = int(s["习得"] * 1.50); s["情爱"] = int(s.get("情爱", 0) * 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.60); s["习得"] = int(s["习得"] * 0.60); s["情爱"] = int(s.get("情爱", 0) * 0.60)
        return s




    def _comf27(self, target: Character) -> Dict[str, int]:
        """後背位アナル SOURCE计算"""
        self._comf_apply_side_effects(27, target)
        s: Dict[str, int] = {}
        s["反感"] = 1200
        s["情爱"] = 1200
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 10; s["快B"] = 10; s["习得"] = 100
        elif abl3 == 1:
            s["快A"] = 30; s["快B"] = 30; s["习得"] = 700
        elif abl3 == 2:
            s["快A"] = 500; s["快B"] = 100; s["习得"] = 1500
        elif abl3 == 3:
            s["快A"] = 1000; s["快B"] = 200; s["习得"] = 3000
        elif abl3 == 4:
            s["快A"] = 1700; s["快B"] = 450; s["习得"] = 5000
        else:
            s["快A"] = 2200; s["快B"] = 750; s["习得"] = 8000
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 1:
            s["快A"] = int(s["快A"] * 0.10); s["露出"] = 20000
        elif exp1 < 4:
            s["快A"] = int(s["快A"] * 0.30); s["露出"] = 12000
        elif exp1 < 20:
            s["快A"] = int(s["快A"] * 0.50); s["露出"] = 5000
        elif exp1 < 50:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = 1800
        elif exp1 < 200:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = 1000
        else:
            s["快A"] = int(s["快A"] * 1.60); s["露出"] = 600
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = int(s["快A"] * 0.40); s["露出"] = s.get("露出", 0) + 10000
        elif palam3 < 500:
            s["快A"] = int(s["快A"] * 0.80); s["露出"] = s.get("露出", 0) + 3600
        elif palam3 < 3000:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = s.get("露出", 0) + 1200
        elif palam3 < 10000:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = s.get("露出", 0) + 200
        else:
            s["快A"] = int(s["快A"] * 1.80); s["露出"] = s.get("露出", 0) + 100
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 肛门敏感/肛门钝感
        if int(target.talent.get(105, 0)):
            s["露出"] = int(s.get("露出", 0) * 1.50); s["习得"] = int(s["习得"] * 1.50); s["情爱"] = int(s["情爱"] * 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.60); s["习得"] = int(s["习得"] * 0.60); s["情爱"] = int(s["情爱"] * 0.60)
        # 处女で看重贞操
        exp0 = int(target.exp.get(0, 0))
        if exp0 == 0 and int(target.talent.get(30, 0)):
            s["习得"] = s["习得"] // 3
        return s




    def _comf28(self, target: Character) -> Dict[str, int]:
        """対面座位アナル SOURCE计算"""
        self._comf_apply_side_effects(28, target)
        s: Dict[str, int] = {}
        s["快B"] = 100
        s["屈辱"] = 100
        s["反感"] = 100
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 10; s["快B"] = s.get("快B", 0) + 10; s["习得"] = 80
        elif abl3 == 1:
            s["快A"] = 30; s["快B"] = s.get("快B", 0) + 130; s["习得"] = 300
        elif abl3 == 2:
            s["快A"] = 200; s["快B"] = s.get("快B", 0) + 500; s["习得"] = 700
        elif abl3 == 3:
            s["快A"] = 500; s["快B"] = s.get("快B", 0) + 1000; s["习得"] = 1500
        elif abl3 == 4:
            s["快A"] = 900; s["快B"] = s.get("快B", 0) + 1500; s["习得"] = 2600
        else:
            s["快A"] = 1400; s["快B"] = s.get("快B", 0) + 2000; s["习得"] = 4000
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 1:
            s["快A"] = int(s["快A"] * 0.10); s["露出"] = 18000
        elif exp1 < 4:
            s["快A"] = int(s["快A"] * 0.30); s["露出"] = 10000
        elif exp1 < 20:
            s["快A"] = int(s["快A"] * 0.50); s["露出"] = 4500
        elif exp1 < 50:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = 1500
        elif exp1 < 200:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = 700
        else:
            s["快A"] = int(s["快A"] * 1.60); s["露出"] = 300
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 50; s["恐怖"] = 10; s["发育"] = 100; s["不洁"] = int(s.get("不洁", 0) * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 150; s["恐怖"] = 50; s["发育"] = 300; s["不洁"] = int(s.get("不洁", 0) * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 300; s["恐怖"] = 100; s["发育"] = 700; s["不洁"] = int(s.get("不洁", 0) * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 400; s["恐怖"] = 200; s["发育"] = 1200; s["不洁"] = int(s.get("不洁", 0) * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 500; s["恐怖"] = 300; s["发育"] = 1800; s["不洁"] = int(s.get("不洁", 0) * 0.50)
        else:
            s["痛苦"] = 800; s["恐怖"] = 500; s["发育"] = 2500; s["不洁"] = int(s.get("不洁", 0) * 0.10)
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = int(s["快A"] * 0.40); s["露出"] = s.get("露出", 0) + 10000
        elif palam3 < 500:
            s["快A"] = int(s["快A"] * 0.80); s["露出"] = s.get("露出", 0) + 3600
        elif palam3 < 3000:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = s.get("露出", 0) + 1200
        elif palam3 < 10000:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = s.get("露出", 0) + 200
        else:
            s["快A"] = int(s["快A"] * 1.80); s["露出"] = s.get("露出", 0) + 100
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 肛门敏感/肛门钝感
        if int(target.talent.get(105, 0)):
            s["露出"] = int(s.get("露出", 0) * 1.50); s["习得"] = int(s["习得"] * 1.50); s["情爱"] = int(s.get("情爱", 0) * 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.60); s["习得"] = int(s["习得"] * 0.60); s["情爱"] = int(s.get("情爱", 0) * 0.60)
        # 看重贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 1.20); s["发育"] = int(s.get("发育", 0) * 1.10)
            if exp1 == 0:
                s["压抑"] = 500
            else:
                s["压抑"] = 0
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快B"] = int(s["快B"] * 0.60); s["压抑"] = int(s.get("压抑", 0) * 2.00)
        elif abl10 == 1:
            s["快B"] = int(s["快B"] * 0.80); s["压抑"] = int(s.get("压抑", 0) * 1.50)
        elif abl10 == 2:
            s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        elif abl10 == 3:
            s["快B"] = int(s["快B"] * 1.20); s["压抑"] = int(s.get("压抑", 0) * 0.80)
        elif abl10 == 4:
            s["快B"] = int(s["快B"] * 1.40); s["压抑"] = int(s.get("压抑", 0) * 0.60)
        else:
            s["快B"] = int(s["快B"] * 1.60); s["压抑"] = int(s.get("压抑", 0) * 0.30)
        # 爱慕
        if int(target.talent.get(85, 0)):
            s["快B"] = int(s["快B"] * 3.00); s["屈辱"] = int(s["屈辱"] * 2.00); s["发育"] = int(s["发育"] * 2.00)
        return s




    def _comf29(self, target: Character) -> Dict[str, int]:
        """背面座位アナル SOURCE计算"""
        self._comf_apply_side_effects(29, target)
        s: Dict[str, int] = {}
        s["反感"] = 200
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 10; s["快B"] = 10; s["习得"] = 80
        elif abl3 == 1:
            s["快A"] = 30; s["快B"] = 130; s["习得"] = 300
        elif abl3 == 2:
            s["快A"] = 200; s["快B"] = 500; s["习得"] = 700
        elif abl3 == 3:
            s["快A"] = 500; s["快B"] = 1000; s["习得"] = 1500
        elif abl3 == 4:
            s["快A"] = 900; s["快B"] = 1500; s["习得"] = 2600
        else:
            s["快A"] = 1400; s["快B"] = 2000; s["习得"] = 4000
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 1:
            s["快A"] = int(s["快A"] * 0.10); s["露出"] = 18000
        elif exp1 < 4:
            s["快A"] = int(s["快A"] * 0.30); s["露出"] = 10000
        elif exp1 < 20:
            s["快A"] = int(s["快A"] * 0.50); s["露出"] = 4500
        elif exp1 < 50:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = 1500
        elif exp1 < 200:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = 700
        else:
            s["快A"] = int(s["快A"] * 1.60); s["露出"] = 300
        # ABL:乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            s["损腐"] = 50; s["快B"] = s.get("快B", 0) + 50
        elif abl1 == 1:
            s["损腐"] = 200; s["快B"] = s.get("快B", 0) + 200
        elif abl1 == 2:
            s["损腐"] = 500; s["快B"] = s.get("快B", 0) + 400
        elif abl1 == 3:
            s["损腐"] = 800; s["快B"] = s.get("快B", 0) + 600
        elif abl1 == 4:
            s["损腐"] = 1300; s["快B"] = s.get("快B", 0) + 1000
        else:
            s["损腐"] = 1800; s["快B"] = s.get("快B", 0) + 1400
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 40
        elif abl0 == 1:
            s["快C"] = 160
        elif abl0 == 2:
            s["快C"] = 500
        elif abl0 == 3:
            s["快C"] = 900
        elif abl0 == 4:
            s["快C"] = 1400
        else:
            s["快C"] = 2100
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = int(s["快A"] * 0.40); s["露出"] = s.get("露出", 0) + 10000
        elif palam3 < 500:
            s["快A"] = int(s["快A"] * 0.80); s["露出"] = s.get("露出", 0) + 3600
        elif palam3 < 3000:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = s.get("露出", 0) + 1200
        elif palam3 < 10000:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = s.get("露出", 0) + 200
        else:
            s["快A"] = int(s["快A"] * 1.80); s["露出"] = s.get("露出", 0) + 100
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 肛门敏感/肛门钝感
        if int(target.talent.get(105, 0)):
            s["露出"] = int(s.get("露出", 0) * 1.50); s["习得"] = int(s["习得"] * 1.50); s["情爱"] = int(s.get("情爱", 0) * 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.60); s["习得"] = int(s["习得"] * 0.60); s["情爱"] = int(s.get("情爱", 0) * 0.60)
        # 看重贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 1.20); s["发育"] = int(s.get("发育", 0) * 1.10)
            if exp1 == 0:
                s["压抑"] = 500
            else:
                s["压抑"] = 0
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快A"] = int(s["快A"] * 1.50); s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 2.00)
        elif abl10 == 1:
            s["快A"] = int(s["快A"] * 1.50); s["快B"] = int(s["快B"] * 1.30); s["压抑"] = int(s.get("压抑", 0) * 1.80)
        elif abl10 == 2:
            s["快A"] = int(s["快A"] * 1.50); s["快B"] = int(s["快B"] * 1.50); s["压抑"] = int(s.get("压抑", 0) * 1.60)
        elif abl10 == 3:
            s["快A"] = int(s["快A"] * 1.80); s["快B"] = int(s["快B"] * 1.90); s["压抑"] = int(s.get("压抑", 0) * 1.40)
        elif abl10 == 4:
            s["快A"] = int(s["快A"] * 2.10); s["快B"] = int(s["快B"] * 2.20); s["压抑"] = int(s.get("压抑", 0) * 1.20)
        else:
            s["快A"] = int(s["快A"] * 2.50); s["快B"] = int(s["快B"] * 2.60); s["压抑"] = int(s.get("压抑", 0) * 1.00)
        # 爱慕
        if int(target.talent.get(85, 0)):
            s["快B"] = int(s["快B"] * 1.50)
        return s




    def _comf30(self, target: Character) -> Dict[str, int]:
        """手淫 SOURCE计算"""
        self._comf_apply_side_effects(30, target)
        s: Dict[str, int] = {}
        s["习得"] = 500
        s["情爱"] = 100
        s["不洁"] = 60
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 250; s["恐怖"] = 50; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 300; s["恐怖"] = 100; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 350; s["恐怖"] = 200; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 400; s["恐怖"] = 300; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 450; s["恐怖"] = 500; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 500; s["恐怖"] = 750; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        return s




    def _comf31(self, target: Character) -> Dict[str, int]:
        """フェラチオ SOURCE计算"""
        self._comf_apply_side_effects(31, target)
        s: Dict[str, int] = {}
        s["习得"] = 1500
        s["情爱"] = 500
        s["不洁"] = 100
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 420; s["恐怖"] = 150; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 500; s["恐怖"] = 300; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 580; s["恐怖"] = 600; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 660; s["恐怖"] = 900; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 740; s["恐怖"] = 1500; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 820; s["恐怖"] = 2200; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        return s




    def _comf32(self, target: Character) -> Dict[str, int]:
        """パイズリ SOURCE计算"""
        self._comf_apply_side_effects(32, target)
        s: Dict[str, int] = {}
        s["习得"] = 1800
        s["情爱"] = 900
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 420; s["恐怖"] = 150; s["不洁"] = 400
        elif abl16 == 1:
            s["痛苦"] = 500; s["恐怖"] = 300; s["不洁"] = 300
        elif abl16 == 2:
            s["痛苦"] = 580; s["恐怖"] = 600; s["不洁"] = 150
        elif abl16 == 3:
            s["痛苦"] = 660; s["恐怖"] = 900; s["不洁"] = 50
        elif abl16 == 4:
            s["痛苦"] = 740; s["恐怖"] = 1500; s["不洁"] = 20
        else:
            s["痛苦"] = 820; s["恐怖"] = 2200; s["不洁"] = 0
        # ABL:乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            a = 100
        elif abl1 == 1:
            a = 200
        elif abl1 == 2:
            a = 400
        elif abl1 == 3:
            a = 800
        elif abl1 == 4:
            a = 1200
        else:
            a = 1500
        # 巨乳
        if int(target.talent.get(110, 0)):
            a = int(a * 1.20)
        if int(target.talent.get(108, 0)):
            a = int(a * 1.20)
        elif int(target.talent.get(107, 0)):
            a = int(a * 0.70)
        s["损腐"] = s.get("损腐", 0) + a
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        return s




    def _comf33(self, target: Character) -> Dict[str, int]:
        """素股 SOURCE计算"""
        self._comf_apply_side_effects(33, target)
        s: Dict[str, int] = {}
        s["习得"] = 1200
        s["情爱"] = 400
        s["不洁"] = 60
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 200; s["恐怖"] = 100; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 250; s["恐怖"] = 180; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 300; s["恐怖"] = 250; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 350; s["恐怖"] = 350; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 400; s["恐怖"] = 500; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 450; s["恐怖"] = 800; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.70); s["恐怖"] = int(s["恐怖"] * 0.70)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.90); s["恐怖"] = int(s["恐怖"] * 0.90)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.40); s["恐怖"] = int(s["恐怖"] * 1.40)
        else:
            s["痛苦"] = int(s["痛苦"] * 1.60); s["恐怖"] = int(s["恐怖"] * 1.60)
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 0
        elif abl0 == 1:
            s["快C"] = 10
        elif abl0 == 2:
            s["快C"] = 50
        elif abl0 == 3:
            s["快C"] = 200
        elif abl0 == 4:
            s["快C"] = 600
        else:
            s["快C"] = 2000
        return s




    def _comf34(self, target: Character) -> Dict[str, int]:
        """骑乗位 SOURCE计算"""
        self._comf_apply_side_effects(34, target)
        s: Dict[str, int] = {}
        s["反感"] = 900
        s["不洁"] = 60
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 200; s["恐怖"] = 50; s["情爱"] = 300; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 250; s["恐怖"] = 200; s["情爱"] = 100; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 350; s["恐怖"] = 550; s["情爱"] = 30; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 450; s["恐怖"] = 900; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 600; s["恐怖"] = 1500; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 750; s["恐怖"] = 2200; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:私处感觉
        abl2 = target.get_abl(2)
        if abl2 == 0:
            s["快V"] = 20; s["快B"] = 25; s["痛苦"] = int(s["痛苦"] * 0.50)
        elif abl2 == 1:
            s["快V"] = 75; s["快B"] = 75; s["痛苦"] = int(s["痛苦"] * 0.80)
        elif abl2 == 2:
            s["快V"] = 200; s["快B"] = 125; s["痛苦"] = int(s["痛苦"] * 1.00)
        elif abl2 == 3:
            s["快V"] = 500; s["快B"] = 175; s["痛苦"] = int(s["痛苦"] * 1.20)
        elif abl2 == 4:
            s["快V"] = 850; s["快B"] = 300; s["痛苦"] = int(s["痛苦"] * 1.50)
        else:
            s["快V"] = 1100; s["快B"] = 425; s["痛苦"] = int(s["痛苦"] * 2.00)
        # EXP:私处经验
        exp0 = int(target.exp.get(0, 0))
        if exp0 < 1:
            s["快V"] = int(s["快V"] * 0.20); s["露出"] = 5000; s["反感"] = 12000; s["情爱"] = 120000
        elif exp0 < 4:
            s["快V"] = int(s["快V"] * 0.60); s["露出"] = 220
        elif exp0 < 20:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = 30
        elif exp0 < 50:
            s["快V"] = int(s["快V"] * 1.20); s["露出"] = 5
        elif exp0 < 200:
            s["快V"] = int(s["快V"] * 1.40); s["露出"] = 0
        else:
            s["快V"] = int(s["快V"] * 1.50)
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快V"] = int(s["快V"] * 0.20); s["露出"] = s.get("露出", 0) + 900; s["露出"] = int(s["露出"] * 3.00); s["反感"] = s.get("反感", 0) + 2000
        elif palam3 < 500:
            s["快V"] = int(s["快V"] * 0.60); s["露出"] = s.get("露出", 0) + 250; s["露出"] = int(s["露出"] * 1.00); s["反感"] = s.get("反感", 0) + 400
        elif palam3 < 3000:
            s["快V"] = int(s["快V"] * 1.00); s["露出"] = int(s.get("露出", 0) * 0.50)
        elif palam3 < 10000:
            s["快V"] = int(s["快V"] * 1.30); s["露出"] = int(s.get("露出", 0) * 0.30)
        elif palam3 < 50000:
            s["快V"] = int(s["快V"] * 1.60); s["露出"] = int(s.get("露出", 0) * 0.20)
        else:
            s["快V"] = int(s["快V"] * 2.00); s["露出"] = int(s.get("露出", 0) * 0.10)
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 4.00)
        # 看重贞操/看轻贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 0.60); s["情爱"] = int(s.get("情爱", 0) * 15.00)
            if exp0 == 0:
                s["压抑"] = 10000
            else:
                s["压抑"] = 1000
        elif int(target.talent.get(31, 0)):
            s["情爱"] = int(s.get("情爱", 0) * 0.50)
            if exp0 == 0:
                s["压抑"] = 300
        else:
            if exp0 == 0:
                s["压抑"] = 3000
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快V"] = int(s["快V"] * 0.50); s["快B"] = int(s["快B"] * 0.60); s["压抑"] = int(s.get("压抑", 0) * 2.00); s["习得"] = s.get("习得", 0) + 700
        elif abl10 == 1:
            s["快V"] = int(s["快V"] * 0.80); s["快B"] = int(s["快B"] * 0.80); s["压抑"] = int(s.get("压抑", 0) * 1.50); s["习得"] = s.get("习得", 0) + 500
        elif abl10 == 2:
            s["快V"] = int(s["快V"] * 1.00); s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 1.00); s["习得"] = s.get("习得", 0) + 300
        elif abl10 == 3:
            s["快V"] = int(s["快V"] * 1.30); s["快B"] = int(s["快B"] * 1.20); s["压抑"] = int(s.get("压抑", 0) * 0.80); s["习得"] = s.get("习得", 0) + 100
        elif abl10 == 4:
            s["快V"] = int(s["快V"] * 1.60); s["快B"] = int(s["快B"] * 1.40); s["压抑"] = int(s.get("压抑", 0) * 0.60); s["习得"] = s.get("习得", 0) + 30
        else:
            s["快V"] = int(s["快V"] * 2.00); s["快B"] = int(s["快B"] * 1.60); s["压抑"] = int(s.get("压抑", 0) * 0.30)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["快V"] = int(s["快V"] * 0.50); s["快B"] = int(s["快B"] * 0.60)
        elif abl12 == 1:
            s["快V"] = int(s["快V"] * 0.80); s["快B"] = int(s["快B"] * 0.80)
        elif abl12 == 2:
            s["快V"] = int(s["快V"] * 1.00); s["快B"] = int(s["快B"] * 1.00)
        elif abl12 == 3:
            s["快V"] = int(s["快V"] * 1.30); s["快B"] = int(s["快B"] * 1.20)
        elif abl12 == 4:
            s["快V"] = int(s["快V"] * 1.60); s["快B"] = int(s["快B"] * 1.40)
        else:
            s["快V"] = int(s["快V"] * 2.00); s["快B"] = int(s["快B"] * 1.60)
        return s




    def _comf35(self, target: Character) -> Dict[str, int]:
        """泡踊り SOURCE计算"""
        self._comf_apply_side_effects(35, target)
        s: Dict[str, int] = {}
        s["习得"] = 2000
        s["情爱"] = 1500
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 500; s["恐怖"] = 300; s["不洁"] = 200
        elif abl16 == 1:
            s["痛苦"] = 700; s["恐怖"] = 500; s["不洁"] = 150
        elif abl16 == 2:
            s["痛苦"] = 900; s["恐怖"] = 800; s["不洁"] = 100
        elif abl16 == 3:
            s["痛苦"] = 1100; s["恐怖"] = 1200; s["不洁"] = 50
        elif abl16 == 4:
            s["痛苦"] = 1300; s["恐怖"] = 1800; s["不洁"] = 20
        else:
            s["痛苦"] = 1500; s["恐怖"] = 2500; s["不洁"] = 0
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 0
        elif abl0 == 1:
            s["快C"] = 50
        elif abl0 == 2:
            s["快C"] = 200
        elif abl0 == 3:
            s["快C"] = 400
        elif abl0 == 4:
            s["快C"] = 1000
        else:
            s["快C"] = 2000
        # ABL:乳房感觉
        abl1 = target.get_abl(1)
        if abl1 == 0:
            a = 200
        elif abl1 == 1:
            a = 300
        elif abl1 == 2:
            a = 500
        elif abl1 == 3:
            a = 1000
        elif abl1 == 4:
            a = 1500
        else:
            a = 1800
        if int(target.talent.get(110, 0)):
            a = int(a * 1.20)
        if int(target.talent.get(108, 0)):
            a = int(a * 1.20)
        elif int(target.talent.get(107, 0)):
            a = int(a * 0.70)
        s["损腐"] = s.get("损腐", 0) + a
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.30); s["恐怖"] = int(s["恐怖"] * 1.30)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.60); s["恐怖"] = int(s["恐怖"] * 1.60)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.90); s["恐怖"] = int(s["恐怖"] * 1.90)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.30); s["恐怖"] = int(s["恐怖"] * 2.30)
        return s




    def _comf36(self, target: Character) -> Dict[str, int]:
        """骑乗位アナル SOURCE计算"""
        self._comf_apply_side_effects(36, target)
        s: Dict[str, int] = {}
        s["反感"] = 900
        s["不洁"] = 60
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 200; s["恐怖"] = 50; s["情爱"] = 300; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 250; s["恐怖"] = 200; s["情爱"] = 100; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 350; s["恐怖"] = 550; s["情爱"] = 30; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 450; s["恐怖"] = 900; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 600; s["恐怖"] = 1500; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 750; s["恐怖"] = 2200; s["情爱"] = 0; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 10; s["快B"] = 10; s["习得"] = 80; s["痛苦"] = int(s["痛苦"] * 0.50)
        elif abl3 == 1:
            s["快A"] = 20; s["快B"] = 50; s["习得"] = 300; s["痛苦"] = int(s["痛苦"] * 0.80)
        elif abl3 == 2:
            s["快A"] = 200; s["快B"] = 100; s["习得"] = 700; s["痛苦"] = int(s["痛苦"] * 1.00)
        elif abl3 == 3:
            s["快A"] = 450; s["快B"] = 180; s["习得"] = 1500; s["痛苦"] = int(s["痛苦"] * 1.20)
        elif abl3 == 4:
            s["快A"] = 850; s["快B"] = 300; s["习得"] = 2600; s["痛苦"] = int(s["痛苦"] * 1.50)
        else:
            s["快A"] = 1300; s["快B"] = 450; s["习得"] = 4000; s["痛苦"] = int(s["痛苦"] * 2.00)
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0))
        if exp1 < 1:
            s["快A"] = int(s["快A"] * 0.10); s["露出"] = 18000
        elif exp1 < 4:
            s["快A"] = int(s["快A"] * 0.30); s["露出"] = 10000
        elif exp1 < 20:
            s["快A"] = int(s["快A"] * 0.50); s["露出"] = 4500
        elif exp1 < 50:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = 1500
        elif exp1 < 200:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = 700
        else:
            s["快A"] = int(s["快A"] * 1.60); s["露出"] = 300
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = int(s["快A"] * 0.40); s["露出"] = s.get("露出", 0) + 10000
        elif palam3 < 500:
            s["快A"] = int(s["快A"] * 0.80); s["露出"] = s.get("露出", 0) + 3600
        elif palam3 < 3000:
            s["快A"] = int(s["快A"] * 1.00); s["露出"] = s.get("露出", 0) + 1200
        elif palam3 < 10000:
            s["快A"] = int(s["快A"] * 1.40); s["露出"] = s.get("露出", 0) + 200
        else:
            s["快A"] = int(s["快A"] * 1.80); s["露出"] = s.get("露出", 0) + 100
        # 魁梧
        if int(target.talent.get(99, 0)):
            s["露出"] = int(s.get("露出", 0) * 0.80)
        # 小柄体形
        if int(target.talent.get(100, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 未熟
        if int(target.talent.get(135, 0)):
            s["露出"] = int(s.get("露出", 0) * 2.00)
        # 看重贞操
        if int(target.talent.get(30, 0)):
            s["快B"] = int(s["快B"] * 1.20); s["发育"] = int(s.get("发育", 0) * 1.10)
            if exp1 == 0:
                s["压抑"] = 500
            else:
                s["压抑"] = 0
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快A"] = int(s["快A"] * 0.50); s["快B"] = int(s["快B"] * 0.60); s["压抑"] = int(s.get("压抑", 0) * 2.00); s["习得"] = s.get("习得", 0) + 700
        elif abl10 == 1:
            s["快A"] = int(s["快A"] * 0.80); s["快B"] = int(s["快B"] * 0.80); s["压抑"] = int(s.get("压抑", 0) * 1.50); s["习得"] = s.get("习得", 0) + 500
        elif abl10 == 2:
            s["快A"] = int(s["快A"] * 1.00); s["快B"] = int(s["快B"] * 1.00); s["压抑"] = int(s.get("压抑", 0) * 1.00); s["习得"] = s.get("习得", 0) + 300
        elif abl10 == 3:
            s["快A"] = int(s["快A"] * 1.30); s["快B"] = int(s["快B"] * 1.20); s["压抑"] = int(s.get("压抑", 0) * 0.80); s["习得"] = s.get("习得", 0) + 100
        elif abl10 == 4:
            s["快A"] = int(s["快A"] * 1.60); s["快B"] = int(s["快B"] * 1.40); s["压抑"] = int(s.get("压抑", 0) * 0.60); s["习得"] = s.get("习得", 0) + 30
        else:
            s["快A"] = int(s["快A"] * 2.00); s["快B"] = int(s["快B"] * 1.60); s["压抑"] = int(s.get("压抑", 0) * 0.30)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["快A"] = int(s["快A"] * 0.50); s["快B"] = int(s["快B"] * 0.60)
        elif abl12 == 1:
            s["快A"] = int(s["快A"] * 0.80); s["快B"] = int(s["快B"] * 0.80)
        elif abl12 == 2:
            s["快A"] = int(s["快A"] * 1.00); s["快B"] = int(s["快B"] * 1.00)
        elif abl12 == 3:
            s["快A"] = int(s["快A"] * 1.30); s["快B"] = int(s["快B"] * 1.20)
        elif abl12 == 4:
            s["快A"] = int(s["快A"] * 1.60); s["快B"] = int(s["快B"] * 1.40)
        else:
            s["快A"] = int(s["快A"] * 2.00); s["快B"] = int(s["快B"] * 1.60)
        return s




    def _comf37(self, target: Character) -> Dict[str, int]:
        """アナル奉仕 SOURCE计算"""
        self._comf_apply_side_effects(37, target)
        s: Dict[str, int] = {}
        s["习得"] = 3000
        s["情爱"] = 5000
        s["不洁"] = 50
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 420; s["恐怖"] = 150; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 500; s["恐怖"] = 300; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 580; s["恐怖"] = 600; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 660; s["恐怖"] = 900; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 740; s["恐怖"] = 1500; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 820; s["恐怖"] = 2200; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 2.50); s["恐怖"] = int(s["恐怖"] * 2.50)
        else:
            s["痛苦"] = int(s["痛苦"] * 4.00); s["恐怖"] = int(s["恐怖"] * 4.00)
        return s




    def _comf38(self, target: Character) -> Dict[str, int]:
        """足コキ SOURCE计算"""
        self._comf_apply_side_effects(38, target)
        s: Dict[str, int] = {}
        s["习得"] = 550
        s["情爱"] = 400
        s["不洁"] = 50
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 300; s["恐怖"] = 50; s["不洁"] = int(s["不洁"] * 4.00)
        elif abl16 == 1:
            s["痛苦"] = 350; s["恐怖"] = 100; s["不洁"] = int(s["不洁"] * 2.50)
        elif abl16 == 2:
            s["痛苦"] = 400; s["恐怖"] = 150; s["不洁"] = int(s["不洁"] * 1.50)
        elif abl16 == 3:
            s["痛苦"] = 450; s["恐怖"] = 200; s["不洁"] = int(s["不洁"] * 1.00)
        elif abl16 == 4:
            s["痛苦"] = 500; s["恐怖"] = 250; s["不洁"] = int(s["不洁"] * 0.50)
        else:
            s["痛苦"] = 580; s["恐怖"] = 300; s["不洁"] = int(s["不洁"] * 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = int(s["痛苦"] * 0.50); s["恐怖"] = int(s["恐怖"] * 0.50)
        elif abl12 == 1:
            s["痛苦"] = int(s["痛苦"] * 0.80); s["恐怖"] = int(s["恐怖"] * 0.80)
        elif abl12 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl12 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl12 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.50); s["恐怖"] = int(s["恐怖"] * 1.50)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        # ABL:抖S气质
        abl20 = int(target.abl.get(20, 0))
        if abl20 == 0:
            s["痛苦"] = int(s["痛苦"] * 1.00); s["恐怖"] = int(s["恐怖"] * 1.00)
        elif abl20 == 1:
            s["痛苦"] = int(s["痛苦"] * 1.20); s["恐怖"] = int(s["恐怖"] * 1.20)
        elif abl20 == 2:
            s["痛苦"] = int(s["痛苦"] * 1.40); s["恐怖"] = int(s["恐怖"] * 1.40)
        elif abl20 == 3:
            s["痛苦"] = int(s["痛苦"] * 1.60); s["恐怖"] = int(s["恐怖"] * 1.60)
        elif abl20 == 4:
            s["痛苦"] = int(s["痛苦"] * 1.80); s["恐怖"] = int(s["恐怖"] * 1.80)
        else:
            s["痛苦"] = int(s["痛苦"] * 2.00); s["恐怖"] = int(s["恐怖"] * 2.00)
        return s




    def _comf40(self, target: Character) -> Dict[str, int]:
        """スパンキング SOURCE计算"""
        self._comf_apply_side_effects(40, target)
        s: Dict[str, int] = {}
        s["反感"] = 200
        s["情爱"] = 500
        # PALAM:苦痛
        palam9 = int(target.palam.get(9, 0)) if hasattr(target, 'palam') else 0
        if palam9 < 100:
            s["露出"] = 300
        elif palam9 < 500:
            s["露出"] = 500
        elif palam9 < 3000:
            s["露出"] = 800
        elif palam9 < 10000:
            s["露出"] = 1200
        else:
            s["露出"] = 1800
        return s




    def _comf41(self, target: Character) -> Dict[str, int]:
        """鞭 SOURCE计算"""
        self._comf_apply_side_effects(41, target)
        s: Dict[str, int] = {}
        s["情爱"] = 1000
        # PALAM:苦痛
        palam9 = int(target.palam.get(9, 0)) if hasattr(target, 'palam') else 0
        if palam9 < 100:
            s["露出"] = 1000
        elif palam9 < 500:
            s["露出"] = 1500
        elif palam9 < 3000:
            s["露出"] = 2200
        elif palam9 < 10000:
            s["露出"] = 3000
        else:
            s["露出"] = 4000
        return s




    def _comf42(self, target: Character) -> Dict[str, int]:
        """针 SOURCE计算"""
        self._comf_apply_side_effects(42, target)
        s: Dict[str, int] = {}
        s["情爱"] = 1000
        # PALAM:苦痛
        palam9 = int(target.palam.get(9, 0)) if hasattr(target, 'palam') else 0
        if palam9 < 100:
            s["露出"] = 3000
        elif palam9 < 500:
            s["露出"] = 3300
        elif palam9 < 3000:
            s["露出"] = 3600
        elif palam9 < 10000:
            s["露出"] = 4000
        else:
            s["露出"] = 4500
        return s




    def _comf43(self, target: Character) -> Dict[str, int]:
        """眼罩 SOURCE计算"""
        self._comf_apply_side_effects(43, target)
        s: Dict[str, int] = {}
        s["中毒充足"] = 250
        s["反感"] = 1000
        s["情爱"] = 500
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif palam5 < 500:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.90)
        elif palam5 < 3000:
            pass  # 1.00
        elif palam5 < 10000:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.10)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.20)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.40)
        elif abl10 == 1:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.60)
        elif abl10 == 2:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif abl10 == 3:
            pass  # 1.00
        elif abl10 == 4:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.10)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.20)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif abl21 == 1:
            pass  # 1.00
        elif abl21 == 2:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.30)
        elif abl21 == 3:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.60)
        elif abl21 == 4:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.00)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 3.00)
        # 倒错的 TALENT:80
        if int(target.talent.get(80, 0)):
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.00)
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 2.00)
        return s




    def _comf44(self, target: Character) -> Dict[str, int]:
        """绳子 SOURCE计算"""
        self._comf_apply_side_effects(44, target)
        s: Dict[str, int] = {}
        s["露出"] = 800
        s["中毒充足"] = 800
        s["习得"] = 500
        s["情爱"] = 500
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif palam5 < 500:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.90)
        elif palam5 < 3000:
            pass  # 1.00
        elif palam5 < 10000:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.10)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.20)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.40)
        elif abl10 == 1:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.60)
        elif abl10 == 2:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif abl10 == 3:
            pass  # 1.00
        elif abl10 == 4:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.10)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.20)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif abl21 == 1:
            pass  # 1.00
        elif abl21 == 2:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.30)
        elif abl21 == 3:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.60)
        elif abl21 == 4:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.00)
        else:
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 3.00)
        # 倒错的 TALENT:80
        if int(target.talent.get(80, 0)):
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.00)
        return s




    def _comf45(self, target: Character) -> Dict[str, int]:
        """口塞 SOURCE计算"""
        self._comf_apply_side_effects(45, target)
        s: Dict[str, int] = {}
        s["露出"] = 50
        s["屈辱"] = 50
        s["反感"] = 80
        s["习得"] = 150
        s["情爱"] = 80
        s["发育"] = 80
        return s




    def _comf46(self, target: Character) -> Dict[str, int]:
        """灌肠+肛塞 SOURCE计算"""
        self._comf_apply_side_effects(46, target)
        s: Dict[str, int] = {}
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 80
            s["习得"] = 300
        elif abl3 == 1:
            s["快A"] = 250
            s["习得"] = 800
        elif abl3 == 2:
            s["快A"] = 600
            s["习得"] = 1400
        elif abl3 == 3:
            s["快A"] = 1000
            s["习得"] = 1800
        elif abl3 == 4:
            s["快A"] = 1300
            s["习得"] = 2100
        else:
            s["快A"] = 1700
            s["习得"] = 2400
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 < 1:
            s["露出"] = 2000
            s["不洁"] = 1000
            s["习得"] = 200
            s["情爱"] = 1000
            s["压抑"] = 2000
        elif abl21 < 2:
            s["露出"] = 1600
            s["不洁"] = 2000
            s["习得"] = 500
            s["情爱"] = 1000
            s["压抑"] = 1000
        elif abl21 < 3:
            s["露出"] = 1200
            s["不洁"] = 1000
            s["习得"] = 800
            s["情爱"] = 1000
            s["压抑"] = 500
        elif abl21 < 4:
            s["露出"] = 800
            s["不洁"] = 1000
            s["习得"] = 1200
            s["情爱"] = 1000
            s["压抑"] = 100
        elif abl21 < 5:
            s["露出"] = 600
            s["不洁"] = 1000
            s["习得"] = 1500
            s["情爱"] = 1000
            s["压抑"] = 0
        else:
            s["露出"] = 400
            s["不洁"] = 1000
            s["习得"] = 2000
            s["情爱"] = 1000
            s["压抑"] = 0
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.40)
            s["露出"] = int(s.get("露出", 0)) + 800
        elif palam3 < 500:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
            s["露出"] = int(s.get("露出", 0)) + 500
        elif palam3 < 3000:
            pass  # 1.00
            s["露出"] = int(s.get("露出", 0)) + 300
        elif palam3 < 10000:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.40)
            s["露出"] = int(s.get("露出", 0)) + 120
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.80)
            s["露出"] = int(s.get("露出", 0)) + 100
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
        elif palam5 < 500:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.90)
        elif palam5 < 3000:
            pass  # 1.00
        elif palam5 < 10000:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
        elif abl10 == 1:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.90)
        elif abl10 == 2:
            pass  # 1.00
        elif abl10 == 3:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
        elif abl10 == 4:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.30)
        # 魁梧 TALENT:99
        if int(target.talent.get(99, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 0.80)
        # 娇小 TALENT:100
        if int(target.talent.get(100, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 2.00)
        # 未熟 TALENT:135
        if int(target.talent.get(135, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 2.00)
        # 肛门敏感 TALENT:105 / 肛门钝感 TALENT:106
        if int(target.talent.get(105, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 1.50)
            s["习得"] = self._scale_value(int(s.get("习得", 0)), 1.50)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 0.60)
            s["习得"] = self._scale_value(int(s.get("习得", 0)), 0.60)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.60)
        return s




    def _comf47(self, target: Character) -> Dict[str, int]:
        """束缚衣 SOURCE计算"""
        self._comf_apply_side_effects(47, target)
        s: Dict[str, int] = {}
        a = 300
        # PALAM:恐怖
        palam10 = int(target.palam.get(10, 0)) if hasattr(target, 'palam') else 0
        if palam10 < 100:
            pass  # 1.00
        elif palam10 < 500:
            a = self._scale_value(a, 1.10)
        elif palam10 < 3000:
            a = self._scale_value(a, 1.20)
        elif palam10 < 10000:
            a = self._scale_value(a, 1.30)
        else:
            a = self._scale_value(a, 1.40)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            s["抑郁"] = 0
            s["中毒充足"] = 0
            s["压抑"] = 100
            a = self._scale_value(a, 0.60)
        elif abl21 == 1:
            s["抑郁"] = 50
            s["中毒充足"] = 150
            a = self._scale_value(a, 1.00)
        elif abl21 == 2:
            s["抑郁"] = 100
            s["中毒充足"] = 300
            a = self._scale_value(a, 1.60)
        elif abl21 == 3:
            s["抑郁"] = 150
            s["中毒充足"] = 600
        elif abl21 == 4:
            s["抑郁"] = 200
            s["中毒充足"] = 1000
        else:
            s["抑郁"] = 300
            s["中毒充足"] = 2000
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            a = self._scale_value(a, 2.00)
        s["情爱"] = a
        return s




    def _comf48(self, target: Character) -> Dict[str, int]:
        """践踏 SOURCE计算"""
        self._comf_apply_side_effects(48, target)
        s: Dict[str, int] = {}
        s["反感"] = 150
        s["情爱"] = 400
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 30
        elif abl0 == 1:
            s["快C"] = 100
        elif abl0 == 2:
            s["快C"] = 200
        elif abl0 == 3:
            s["快C"] = 500
        elif abl0 == 4:
            s["快C"] = 1000
        else:
            s["快C"] = 1500
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            pass  # 1.00 for 快C and 情爱
        elif abl21 == 1:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 1.20)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.80)
        elif abl21 == 2:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 1.50)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.60)
        elif abl21 == 3:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 1.80)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.40)
        elif abl21 == 4:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 2.20)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.20)
        else:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 3.00)
            s["情爱"] = 0
        return s




    def _comf49(self, target: Character) -> Dict[str, int]:
        """肛门电极 SOURCE计算"""
        self._comf_apply_side_effects(49, target)
        s: Dict[str, int] = {}
        # ABL:肛门感觉
        abl3 = target.get_abl(3)
        if abl3 == 0:
            s["快A"] = 200
            s["习得"] = 1000
        elif abl3 == 1:
            s["快A"] = 500
            s["习得"] = 2000
        elif abl3 == 2:
            s["快A"] = 900
            s["习得"] = 3000
        elif abl3 == 3:
            s["快A"] = 1800
            s["习得"] = 5000
        elif abl3 == 4:
            s["快A"] = 2400
            s["习得"] = 8000
        else:
            s["快A"] = 3800
            s["习得"] = 12000
        # EXP:肛门经验
        exp1 = int(target.exp.get(1, 0)) if hasattr(target, 'exp') else 0
        if exp1 < 1:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.50)
            s["露出"] = 2000
        elif exp1 < 2:
            s["露出"] = 300
        elif exp1 < 12:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
            s["露出"] = 50
        elif exp1 < 37:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
            s["露出"] = 10
        elif exp1 < 100:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.40)
            s["露出"] = 0
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.60)
            s["露出"] = 0
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.40)
            s["露出"] = int(s.get("露出", 0)) + 800
        elif palam3 < 500:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
            s["露出"] = int(s.get("露出", 0)) + 500
        elif palam3 < 3000:
            pass
            s["露出"] = int(s.get("露出", 0)) + 300
        elif palam3 < 10000:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.40)
            s["露出"] = int(s.get("露出", 0)) + 120
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.80)
            s["露出"] = int(s.get("露出", 0)) + 100
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
        elif palam5 < 500:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.90)
        elif palam5 < 3000:
            pass
        elif palam5 < 10000:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.80)
        elif abl10 == 1:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.90)
        elif abl10 == 2:
            pass
        elif abl10 == 3:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
        elif abl10 == 4:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
        else:
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.30)
        # 魁梧 TALENT:99
        if int(target.talent.get(99, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 0.80)
        # 娇小 TALENT:100
        if int(target.talent.get(100, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 2.00)
        # 未熟 TALENT:135
        if int(target.talent.get(135, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 2.00)
        # 肛门敏感 TALENT:105 / 肛门钝感 TALENT:106
        if int(target.talent.get(105, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 1.50)
            s["习得"] = self._scale_value(int(s.get("习得", 0)), 1.50)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 1.50)
        elif int(target.talent.get(106, 0)):
            s["露出"] = self._scale_value(int(s.get("露出", 0)), 0.60)
            s["习得"] = self._scale_value(int(s.get("习得", 0)), 0.60)
            s["情爱"] = self._scale_value(int(s.get("情爱", 0)), 0.60)
        return s




    def _comf50(self, target: Character) -> Dict[str, int]:
        """润滑液 SOURCE计算"""
        self._comf_apply_side_effects(50, target)
        s: Dict[str, int] = {}
        s["中毒充足"] = 10000
        s["反感"] = 300
        return s




    def _comf51(self, target: Character) -> Dict[str, int]:
        """媚药 SOURCE计算"""
        self._comf_apply_side_effects(51, target)
        s: Dict[str, int] = {}
        # しあわせ草中毒かどうか
        if int(target.talent.get(46, 0)):
            s["屈辱"] = 500
            s["情爱"] = 1000
            s["抑郁"] = 10000
        else:
            s["情爱"] = 2000
            s["抑郁"] = 5000
        return s




    def _comf52(self, target: Character) -> Dict[str, int]:
        """利尿剂 SOURCE计算"""
        self._comf_apply_side_effects(52, target)
        s: Dict[str, int] = {}
        s["情爱"] = 2000
        s["压抑"] = 150
        return s




    def _comf53(self, target: Character) -> Dict[str, int]:
        """水晶球 SOURCE计算"""
        self._comf_apply_side_effects(53, target)
        s: Dict[str, int] = {}
        # 水晶球本身不设SOURCE，EQUIP_COM53中设置
        return s




    def _comf54(self, target: Character) -> Dict[str, int]:
        """野外PLAY SOURCE计算"""
        self._comf_apply_side_effects(54, target)
        s: Dict[str, int] = {}
        a = 500
        b = 500
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            a = self._scale_value(a, 0.80)
        elif palam5 < 500:
            a = self._scale_value(a, 0.90)
        elif palam5 < 3000:
            pass
        elif palam5 < 10000:
            a = self._scale_value(a, 1.10)
        else:
            a = self._scale_value(a, 1.20)
        # ABL:露出癖
        abl17 = int(target.abl.get(17, 0))
        if abl17 == 0:
            s["屈辱"] = 0
            s["中毒充足"] = 0
        elif abl17 == 1:
            s["屈辱"] = 50
            s["中毒充足"] = 50
            a = self._scale_value(a, 1.20)
        elif abl17 == 2:
            s["屈辱"] = 150
            s["中毒充足"] = 150
            a = self._scale_value(a, 1.40)
        elif abl17 == 3:
            s["屈辱"] = 400
            s["中毒充足"] = 400
            a = self._scale_value(a, 1.60)
        elif abl17 == 4:
            s["屈辱"] = 750
            s["中毒充足"] = 750
            a = self._scale_value(a, 2.00)
        else:
            s["屈辱"] = 1300
            s["中毒充足"] = 1300
            a = self._scale_value(a, 3.00)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            a = self._scale_value(a, 0.80)
        elif abl21 == 1:
            pass
        elif abl21 == 2:
            a = self._scale_value(a, 1.30)
        elif abl21 == 3:
            a = self._scale_value(a, 1.60)
        elif abl21 == 4:
            a = self._scale_value(a, 2.00)
        else:
            a = self._scale_value(a, 3.00)
        # 爱表现 TALENT:28
        if int(target.talent.get(28, 0)):
            a = self._scale_value(a, 1.50)
        # 开放 TALENT:33
        if int(target.talent.get(33, 0)):
            a = self._scale_value(a, 1.50)
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            b = self._scale_value(b, 2.00)
        # 害羞 TALENT:35
        if int(target.talent.get(35, 0)):
            b = self._scale_value(b, 2.00)
        # 露出狂 TALENT:89
        if int(target.talent.get(89, 0)):
            a = self._scale_value(a, 2.00)
            b = self._scale_value(b, 0.50)
        s["反感"] = a
        s["情爱"] = b
        s["发育"] = a // 2
        return s




    def _comf55(self, target: Character) -> Dict[str, int]:
        """什么都不做 SOURCE计算"""
        self._comf_apply_side_effects(55, target)
        s: Dict[str, int] = {}
        s["情爱"] = 50
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            s["反感"] = 10
        elif palam5 < 500:
            s["反感"] = 30
        elif palam5 < 3000:
            s["反感"] = 60
        elif palam5 < 10000:
            s["反感"] = 100
        else:
            s["反感"] = 150
        # 侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快B"] = 0
        elif abl16 == 1:
            s["快B"] = 20
        elif abl16 == 2:
            s["快B"] = 40
        elif abl16 == 3:
            s["快B"] = 70
        elif abl16 == 4:
            s["快B"] = 110
        else:
            s["快B"] = 150
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.80)
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 0.80)
            s["中毒充足"] = 0
            s["抑郁"] = 0
        elif abl21 == 1:
            pass  # 1.00 for both
            s["中毒充足"] = 20
            s["抑郁"] = 30
        elif abl21 == 2:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.30)
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.20)
            s["中毒充足"] = 40
            s["抑郁"] = 70
        elif abl21 == 3:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.40)
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.40)
            s["中毒充足"] = 70
            s["抑郁"] = 120
        elif abl21 == 4:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.70)
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.50)
            s["中毒充足"] = 110
            s["抑郁"] = 180
        else:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 2.00)
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.70)
            s["中毒充足"] = 150
            s["抑郁"] = 250
        return s




    def _comf56(self, target: Character) -> Dict[str, int]:
        """交谈 SOURCE计算"""
        self._comf_apply_side_effects(56, target)
        s: Dict[str, int] = {}
        # 爱慕与顺从决定SOURCE
        abl10 = target.get_abl(10)
        if int(target.talent.get(85, 0)):
            s["发育"] = 60
        elif abl10 >= 5:
            s["压抑"] = 10
            s["发育"] = 50
        elif abl10 >= 4:
            s["压抑"] = 20
            s["发育"] = 40
        elif abl10 >= 3:
            s["压抑"] = 30
            s["发育"] = 30
        elif abl10 >= 2:
            s["压抑"] = 40
            s["发育"] = 20
        else:
            s["压抑"] = 50
            s["发育"] = 10
        # PALAM:恭顺
        palam4 = int(target.palam.get(4, 0)) if hasattr(target, 'palam') else 0
        if palam4 < 100:
            s["发育"] = int(s.get("发育", 0)) + 10
        elif palam4 < 500:
            s["发育"] = int(s.get("发育", 0)) + 30
        elif palam4 < 3000:
            s["发育"] = int(s.get("发育", 0)) + 60
        elif palam4 < 10000:
            s["发育"] = int(s.get("发育", 0)) + 100
        else:
            s["发育"] = int(s.get("发育", 0)) + 150
        # 侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            pass
        elif abl16 == 1:
            s["发育"] = int(s.get("发育", 0)) + 20
        elif abl16 == 2:
            s["发育"] = int(s.get("发育", 0)) + 40
        elif abl16 == 3:
            s["发育"] = int(s.get("发育", 0)) + 70
        elif abl16 == 4:
            s["发育"] = int(s.get("发育", 0)) + 110
        else:
            s["发育"] = int(s.get("发育", 0)) + 150
        # 话术
        abl15 = int(target.abl.get(15, 0))
        if abl15 == 0:
            s["发育"] = self._scale_value(int(s.get("发育", 0)), 0.90)
        elif abl15 == 1:
            pass
        elif abl15 == 2:
            s["发育"] = self._scale_value(int(s.get("发育", 0)), 1.10)
        elif abl15 == 3:
            s["发育"] = self._scale_value(int(s.get("发育", 0)), 1.20)
        elif abl15 == 4:
            s["发育"] = self._scale_value(int(s.get("发育", 0)), 1.30)
        else:
            s["发育"] = self._scale_value(int(s.get("发育", 0)), 1.40)
        return s




    def _comf57(self, target: Character) -> Dict[str, int]:
        """羞耻PLAY SOURCE计算"""
        self._comf_apply_side_effects(57, target)
        s: Dict[str, int] = {}
        a = 500
        b = 500
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            pass  # 1.00
        elif palam5 < 500:
            a = self._scale_value(a, 1.10)
        elif palam5 < 3000:
            a = self._scale_value(a, 1.20)
        elif palam5 < 10000:
            a = self._scale_value(a, 1.30)
        else:
            a = self._scale_value(a, 1.40)
        # ABL:露出癖
        abl17 = int(target.abl.get(17, 0))
        if abl17 == 0:
            s["屈辱"] = 0
            s["中毒充足"] = 0
            s["习得"] = 600
            s["情爱"] = 1000
            s["压抑"] = 1000
            a = self._scale_value(a, 0.60)
        elif abl17 == 1:
            s["屈辱"] = 150
            s["中毒充足"] = 150
            s["习得"] = 500
        elif abl17 == 2:
            s["屈辱"] = 300
            s["中毒充足"] = 300
            s["习得"] = 400
            a = self._scale_value(a, 1.60)
        elif abl17 == 3:
            s["屈辱"] = 600
            s["中毒充足"] = 600
            s["习得"] = 300
            a = self._scale_value(a, 2.00)
        elif abl17 == 4:
            s["屈辱"] = 1000
            s["中毒充足"] = 1000
            s["习得"] = 200
            a = self._scale_value(a, 2.60)
        else:
            s["屈辱"] = 1800
            s["中毒充足"] = 1800
            s["习得"] = 100
            a = self._scale_value(a, 3.80)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            pass  # 1.00
        elif abl21 == 1:
            a = self._scale_value(a, 1.20)
        elif abl21 == 2:
            a = self._scale_value(a, 1.40)
        elif abl21 == 3:
            a = self._scale_value(a, 1.60)
        elif abl21 == 4:
            a = self._scale_value(a, 1.80)
        else:
            a = self._scale_value(a, 2.00)
        # 冷漠 TALENT:21
        if int(target.talent.get(21, 0)):
            a = self._scale_value(a, 0.80)
        # 感情淡薄 TALENT:22
        if int(target.talent.get(22, 0)):
            a = self._scale_value(a, 0.80)
        # 好奇心 TALENT:23
        if int(target.talent.get(23, 0)):
            a = self._scale_value(a, 2.50)
        # 开放 TALENT:33
        if int(target.talent.get(33, 0)):
            a = self._scale_value(a, 1.50)
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            b = self._scale_value(b, 1.50)
        # 害羞 TALENT:35
        if int(target.talent.get(35, 0)):
            b = self._scale_value(b, 3.00)
        # 倒错的 TALENT:80
        if int(target.talent.get(80, 0)):
            a = self._scale_value(a, 1.50)
            b = self._scale_value(b, 1.20)
        # 魅力 TALENT:113
        if int(target.talent.get(113, 0)):
            s["快B"] = int(s.get("快B", 0)) + 500
            s["发育"] = int(s.get("发育", 0)) + 500
            a = self._scale_value(a, 1.50)
            b = self._scale_value(b, 1.20)
        s["反感"] = a
        s["情爱"] = b
        s["发育"] = int(s.get("发育", 0)) + a // 2
        return s




    def _comf58(self, target: Character) -> Dict[str, int]:
        """浴室PLAY SOURCE计算"""
        self._comf_apply_side_effects(58, target)
        s: Dict[str, int] = {}
        a = 100
        b = 50
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            a = self._scale_value(a, 0.80)
        elif palam5 < 500:
            a = self._scale_value(a, 0.90)
        elif palam5 < 3000:
            pass
        elif palam5 < 10000:
            a = self._scale_value(a, 1.10)
        else:
            a = self._scale_value(a, 1.20)
        # ABL:露出癖
        abl17 = int(target.abl.get(17, 0))
        if abl17 == 0:
            s["屈辱"] = 0
            s["中毒充足"] = 0
        elif abl17 == 1:
            s["屈辱"] = 50
            s["中毒充足"] = 50
            a = self._scale_value(a, 1.10)
        elif abl17 == 2:
            s["屈辱"] = 80
            s["中毒充足"] = 80
            a = self._scale_value(a, 1.20)
        elif abl17 == 3:
            s["屈辱"] = 100
            s["中毒充足"] = 100
            a = self._scale_value(a, 1.30)
        elif abl17 == 4:
            s["屈辱"] = 200
            s["中毒充足"] = 200
            a = self._scale_value(a, 1.40)
        else:
            s["屈辱"] = 300
            s["中毒充足"] = 300
            a = self._scale_value(a, 1.50)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            pass
        elif abl21 == 1:
            a = self._scale_value(a, 1.10)
        elif abl21 == 2:
            a = self._scale_value(a, 1.20)
        elif abl21 == 3:
            a = self._scale_value(a, 1.30)
        elif abl21 == 4:
            a = self._scale_value(a, 1.40)
        else:
            a = self._scale_value(a, 1.50)
        # 爱表现 TALENT:28
        if int(target.talent.get(28, 0)):
            a = self._scale_value(a, 1.50)
        # 开放 TALENT:33
        if int(target.talent.get(33, 0)):
            a = self._scale_value(a, 1.50)
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            b = self._scale_value(b, 1.10)
        # 害羞 TALENT:35
        if int(target.talent.get(35, 0)):
            b = self._scale_value(b, 1.20)
        s["反感"] = a
        s["情爱"] = b
        s["发育"] = a // 2
        return s




    def _comf59(self, target: Character) -> Dict[str, int]:
        """新妻PLAY SOURCE计算"""
        self._comf_apply_side_effects(59, target)
        s: Dict[str, int] = {}
        a = 500
        b = 100
        # PALAM:欲情
        palam5 = int(target.palam.get(5, 0)) if hasattr(target, 'palam') else 0
        if palam5 < 100:
            pass
        elif palam5 < 500:
            a = self._scale_value(a, 1.10)
        elif palam5 < 3000:
            a = self._scale_value(a, 1.20)
        elif palam5 < 10000:
            a = self._scale_value(a, 1.30)
        else:
            a = self._scale_value(a, 1.40)
        # ABL:露出癖
        abl17 = int(target.abl.get(17, 0))
        if abl17 == 0:
            s["抑郁"] = 0
            s["中毒充足"] = 0
            s["反感"] = 100
            s["情爱"] = 100
            s["压抑"] = 100
            a = self._scale_value(a, 0.60)
        elif abl17 == 1:
            s["抑郁"] = 50
            s["中毒充足"] = 150
            s["反感"] = 500
            s["情爱"] = 300
        elif abl17 == 2:
            s["抑郁"] = 100
            s["中毒充足"] = 300
            s["反感"] = 100
            s["情爱"] = 50
            a = self._scale_value(a, 1.60)
        elif abl17 == 3:
            s["抑郁"] = 150
            s["中毒充足"] = 600
            s["反感"] = 50
            a = self._scale_value(a, 2.00)
        elif abl17 == 4:
            s["抑郁"] = 200
            s["中毒充足"] = 1000
            s["反感"] = 0
            s["情爱"] = 0
            a = self._scale_value(a, 2.60)
        else:
            s["抑郁"] = 300
            s["中毒充足"] = 2000
            s["反感"] = 0
            s["情爱"] = 0
            a = self._scale_value(a, 3.80)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            pass
        elif abl10 == 1:
            a = self._scale_value(a, 1.20)
        elif abl10 == 2:
            a = self._scale_value(a, 1.40)
        elif abl10 == 3:
            a = self._scale_value(a, 1.60)
        elif abl10 == 4:
            a = self._scale_value(a, 1.80)
        else:
            a = self._scale_value(a, 2.00)
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            pass
        elif abl16 == 1:
            a = self._scale_value(a, 1.20)
        elif abl16 == 2:
            a = self._scale_value(a, 1.40)
        elif abl16 == 3:
            a = self._scale_value(a, 1.60)
        elif abl16 == 4:
            a = self._scale_value(a, 1.80)
        else:
            a = self._scale_value(a, 2.00)
        # 冷漠 TALENT:21
        if int(target.talent.get(21, 0)):
            a = self._scale_value(a, 0.80)
        # 感情淡薄 TALENT:22
        if int(target.talent.get(22, 0)):
            a = self._scale_value(a, 0.80)
        # 好奇心 TALENT:23
        if int(target.talent.get(23, 0)):
            a = self._scale_value(a, 1.50)
        # 献身的 TALENT:63
        if int(target.talent.get(63, 0)):
            a = self._scale_value(a, 1.50)
        # 胆怯 TALENT:10
        if int(target.talent.get(10, 0)):
            b = self._scale_value(b, 1.50)
        # 害羞 TALENT:35
        if int(target.talent.get(35, 0)):
            b = self._scale_value(b, 1.20)
        # 看重贞操 TALENT:33 (note: ERB uses TALENT:33 for 看重贞操 in COM59)
        if int(target.talent.get(33, 0)):
            a = self._scale_value(a, 0.50)
        # 高姿态 TALENT:15
        if int(target.talent.get(15, 0)):
            b = self._scale_value(b, 2.00)
        # 恋慕 TALENT:85
        if int(target.talent.get(85, 0)):
            a = self._scale_value(a, 2.50)
        # 淫乱 TALENT:76
        if int(target.talent.get(76, 0)):
            a = self._scale_value(a, 1.80)
        s["快B"] = int(s.get("快B", 0)) + a
        s["情爱"] = int(s.get("情爱", 0)) + b
        s["发育"] = int(s.get("发育", 0)) + a
        return s




    def _comf60(self, target: Character) -> Dict[str, int]:
        """助手接吻 SOURCE计算"""
        self._comf_apply_side_effects(60, target)
        s: Dict[str, int] = {}
        s["习得"] = 100
        s["情爱"] = 10
        s["不洁"] = 10  # Y*20+10 simplified, Y depends on stain
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 50
            s["恐怖"] = 0
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["痛苦"] = 150
            s["恐怖"] = 50
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["痛苦"] = 200
            s["恐怖"] = 100
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["痛苦"] = 250
            s["恐怖"] = 180
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["痛苦"] = 300
            s["恐怖"] = 300
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["痛苦"] = 350
            s["恐怖"] = 500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.50)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 4.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 4.00)
        return s




    def _comf61(self, target: Character) -> Dict[str, int]:
        """强制舔阴 SOURCE计算"""
        self._comf_apply_side_effects(61, target)
        s: Dict[str, int] = {}
        s["习得"] = 1000
        s["情爱"] = 500
        s["不洁"] = 50  # Y*80+50 simplified
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 420
            s["恐怖"] = 150
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["痛苦"] = 500
            s["恐怖"] = 300
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["痛苦"] = 580
            s["恐怖"] = 600
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["痛苦"] = 660
            s["恐怖"] = 900
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["痛苦"] = 740
            s["恐怖"] = 1500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["痛苦"] = 820
            s["恐怖"] = 2200
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.50)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 4.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 4.00)
        return s




    def _comf62(self, target: Character) -> Dict[str, int]:
        """侵犯助手 SOURCE计算"""
        self._comf_apply_side_effects(62, target)
        s: Dict[str, int] = {}
        s["快B"] = 1500
        s["情爱"] = 800
        # ABL:欲望
        abl11 = int(target.abl.get(11, 0))
        if abl11 == 0:
            s["中毒充足"] = 200
            s["习得"] = 1600
        elif abl11 == 1:
            s["中毒充足"] = 400
            s["习得"] = 1900
        elif abl11 == 2:
            s["中毒充足"] = 750
            s["习得"] = 2300
        elif abl11 == 3:
            s["中毒充足"] = 1200
            s["习得"] = 2700
        elif abl11 == 4:
            s["中毒充足"] = 1700
            s["习得"] = 3100
        else:
            s["中毒充足"] = 2500
            s["习得"] = 3500
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.10)
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.50)
        elif abl16 == 1:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.40)
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 0.80)
        elif abl16 == 2:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.70)
        elif abl16 == 3:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.00)
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 1.50)
        elif abl16 == 4:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.60)
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.00)
        else:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 2.00)
            s["中毒充足"] = self._scale_value(int(s.get("中毒充足", 0)), 2.50)
        return s




    def _comf63(self, target: Character) -> Dict[str, int]:
        """磨镜 SOURCE计算"""
        self._comf_apply_side_effects(63, target)
        s: Dict[str, int] = {}
        s["反感"] = 250
        s["习得"] = 400
        s["情爱"] = 300
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["抑郁"] = 200
        elif abl10 == 1:
            s["抑郁"] = 120
        elif abl10 == 2:
            s["抑郁"] = 60
        elif abl10 == 3:
            s["抑郁"] = 20
        else:
            s["抑郁"] = 0
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 20
            s["痛苦"] = 0
            s["恐怖"] = 0
            s["习得"] = 20
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 0.80)
        elif abl0 == 1:
            s["快C"] = 80
            s["痛苦"] = 10
            s["恐怖"] = 50
            s["习得"] = 20
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 0.90)
        elif abl0 == 2:
            s["快C"] = 350
            s["痛苦"] = 50
            s["恐怖"] = 100
            s["习得"] = 20
        elif abl0 == 3:
            s["快C"] = 750
            s["痛苦"] = 100
            s["恐怖"] = 300
            s["习得"] = 20
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.10)
        elif abl0 == 4:
            s["快C"] = 1200
            s["痛苦"] = 700
            s["恐怖"] = 600
            s["习得"] = 20
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.20)
        else:
            s["快C"] = 1750
            s["痛苦"] = 2000
            s["恐怖"] = 1000
            s["习得"] = 20
            s["反感"] = self._scale_value(int(s.get("反感", 0)), 1.30)
        # ABL:技巧 (all levels same multiplier in ERB)
        s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.00)
        s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.60)
        s["习得"] = self._scale_value(int(s.get("习得", 0)), 0.50)
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl16 == 1:
            pass
        elif abl16 == 2:
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.20)
        elif abl16 == 3:
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.40)
        elif abl16 == 4:
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.70)
        else:
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.00)
        return s




    def _comf64(self, target: Character) -> Dict[str, int]:
        """3P SOURCE计算"""
        self._comf_apply_side_effects(64, target)
        s: Dict[str, int] = {}
        s["抑郁"] = 1500
        s["反感"] = 2500
        s["情爱"] = 1500
        s["快V"] = 0
        s["快A"] = 0
        s["快B"] = 0
        s["痛苦"] = 0
        s["恐怖"] = 0
        s["露出"] = 0
        s["习得"] = 0
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快V"] = self._scale_value(int(s.get("快V", 0)), 0.50)
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.70)
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.60)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.60)
            s["抑郁"] = self._scale_value(int(s.get("抑郁", 0)), 2.00)
        elif abl10 == 1:
            s["快V"] = self._scale_value(int(s.get("快V", 0)), 0.80)
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 0.90)
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.80)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["抑郁"] = self._scale_value(int(s.get("抑郁", 0)), 1.20)
        elif abl10 == 2:
            pass
        elif abl10 == 3:
            s["快V"] = self._scale_value(int(s.get("快V", 0)), 1.20)
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.10)
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.20)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
            s["抑郁"] = self._scale_value(int(s.get("抑郁", 0)), 0.60)
        elif abl10 == 4:
            s["快V"] = self._scale_value(int(s.get("快V", 0)), 1.40)
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.20)
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.40)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.40)
            s["抑郁"] = self._scale_value(int(s.get("抑郁", 0)), 0.30)
        else:
            s["快V"] = self._scale_value(int(s.get("快V", 0)), 1.70)
            s["快A"] = self._scale_value(int(s.get("快A", 0)), 1.30)
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.60)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.60)
            s["抑郁"] = self._scale_value(int(s.get("抑郁", 0)), 0.10)
        return s




    def _comf65(self, target: Character) -> Dict[str, int]:
        """逆侵犯助手 SOURCE计算"""
        self._comf_apply_side_effects(65, target)
        s: Dict[str, int] = {}
        s["习得"] = 1500
        s["情爱"] = 800
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快C"] = 800
            s["痛苦"] = 1600
            s["恐怖"] = 200
        elif abl16 == 1:
            s["快C"] = 1400
            s["痛苦"] = 1900
            s["恐怖"] = 400
        elif abl16 == 2:
            s["快C"] = 2000
            s["痛苦"] = 2300
            s["恐怖"] = 750
        elif abl16 == 3:
            s["快C"] = 2500
            s["痛苦"] = 2700
            s["恐怖"] = 1150
        elif abl16 == 4:
            s["快C"] = 2900
            s["痛苦"] = 3100
            s["恐怖"] = 1750
        else:
            s["快C"] = 3200
            s["痛苦"] = 3500
            s["恐怖"] = 2500
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
        elif abl12 == 3:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        elif abl12 == 4:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.00)
        else:
            s["快C"] = self._scale_value(int(s.get("快C", 0)), 0.50)
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 4.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 4.00)
        return s




    def _comf66(self, target: Character) -> Dict[str, int]:
        """双枪口交 SOURCE计算"""
        self._comf_apply_side_effects(66, target)
        s: Dict[str, int] = {}
        s["习得"] = 6000
        s["情爱"] = 600
        s["不洁"] = 100  # Y*40+100 simplified
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 800
            s["恐怖"] = 600
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["痛苦"] = 1200
            s["恐怖"] = 900
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["痛苦"] = 1400
            s["恐怖"] = 1000
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["痛苦"] = 1600
            s["恐怖"] = 1200
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["痛苦"] = 1800
            s["恐怖"] = 1500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["痛苦"] = 2000
            s["恐怖"] = 2200
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 1:
            pass
        elif abl12 == 2:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.20)
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.00)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.20)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.20)
        return s




    def _comf67(self, target: Character) -> Dict[str, int]:
        """践踏奴隶 SOURCE计算"""
        self._comf_apply_side_effects(67, target)
        s: Dict[str, int] = {}
        s["情爱"] = 100
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 40
            s["习得"] = 40
        elif abl0 == 1:
            s["快C"] = 160
            s["习得"] = 160
        elif abl0 == 2:
            s["快C"] = 700
            s["习得"] = 700
        elif abl0 == 3:
            s["快C"] = 1500
            s["习得"] = 1500
        elif abl0 == 4:
            s["快C"] = 2400
            s["习得"] = 2400
        else:
            s["快C"] = 3300
            s["习得"] = 3300
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            s["恐怖"] = 150
        elif abl21 == 1:
            s["恐怖"] = 300
        elif abl21 == 2:
            s["恐怖"] = 600
        elif abl21 == 3:
            s["恐怖"] = 900
        elif abl21 == 4:
            s["恐怖"] = 1500
        else:
            s["恐怖"] = 2200
        # 倒错的 TALENT:80
        if int(target.talent.get(80, 0)):
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.80)
        return s




    def _comf68(self, target: Character) -> Dict[str, int]:
        """双人口交 SOURCE计算"""
        self._comf_apply_side_effects(68, target)
        s: Dict[str, int] = {}
        s["习得"] = 1500
        s["情爱"] = 500
        s["不洁"] = 100  # Y*40+100 simplified
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["快B"] = 300
            s["痛苦"] = 420
            s["恐怖"] = 150
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["快B"] = 400
            s["痛苦"] = 500
            s["恐怖"] = 300
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["快B"] = 550
            s["痛苦"] = 580
            s["恐怖"] = 600
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["快B"] = 700
            s["痛苦"] = 660
            s["恐怖"] = 900
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["快B"] = 900
            s["痛苦"] = 740
            s["恐怖"] = 1500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["快B"] = 1000
            s["痛苦"] = 820
            s["恐怖"] = 2200
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.50)
        elif abl10 == 1:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 0.80)
        elif abl10 == 2:
            pass
        elif abl10 == 3:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.20)
        elif abl10 == 4:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 1.50)
        else:
            s["快B"] = self._scale_value(int(s.get("快B", 0)), 2.00)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.20)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.00)
        return s




    def _comf69(self, target: Character) -> Dict[str, int]:
        """六九式 SOURCE计算"""
        self._comf_apply_side_effects(69, target)
        s: Dict[str, int] = {}
        s["中毒充足"] = 1000
        s["反感"] = 1400
        s["习得"] = 1300
        s["情爱"] = 800
        s["不洁"] = 50  # Y*80+50 simplified
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 40
        elif abl0 == 1:
            s["快C"] = 160
        elif abl0 == 2:
            s["快C"] = 700
        elif abl0 == 3:
            s["快C"] = 1500
        elif abl0 == 4:
            s["快C"] = 2400
        else:
            s["快C"] = 3300
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 620
            s["恐怖"] = 150
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["痛苦"] = 700
            s["恐怖"] = 300
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["痛苦"] = 820
            s["恐怖"] = 600
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["痛苦"] = 940
            s["恐怖"] = 900
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["痛苦"] = 1100
            s["恐怖"] = 1500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["痛苦"] = 1260
            s["恐怖"] = 2200
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.50)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 4.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 4.00)
        return s




    def _comf70(self, target: Character) -> Dict[str, int]:
        """双人股间性交 SOURCE计算"""
        self._comf_apply_side_effects(70, target)
        s: Dict[str, int] = {}
        s["习得"] = 1500
        s["情爱"] = 600
        s["不洁"] = 60  # Y*10+60 simplified
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 200
            s["恐怖"] = 100
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 4.00)
        elif abl16 == 1:
            s["痛苦"] = 250
            s["恐怖"] = 180
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 2.50)
        elif abl16 == 2:
            s["痛苦"] = 300
            s["恐怖"] = 250
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.50)
        elif abl16 == 3:
            s["痛苦"] = 350
            s["恐怖"] = 350
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 1.00)
        elif abl16 == 4:
            s["痛苦"] = 400
            s["恐怖"] = 500
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.50)
        else:
            s["痛苦"] = 450
            s["恐怖"] = 800
            s["不洁"] = self._scale_value(int(s.get("不洁", 0)), 0.10)
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.70)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.70)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.90)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.90)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.20)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.40)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.40)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.60)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.60)
        # ABL:阴蒂感觉
        abl0 = target.get_abl(0)
        if abl0 == 0:
            s["快C"] = 20
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
        elif abl0 == 1:
            s["快C"] = 80
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.90)
        elif abl0 == 2:
            s["快C"] = 350
        elif abl0 == 3:
            s["快C"] = 750
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.10)
        elif abl0 == 4:
            s["快C"] = 1200
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
        else:
            s["快C"] = 1750
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.30)
        return s




    def _comf71(self, target: Character) -> Dict[str, int]:
        """双人乳交 SOURCE计算"""
        self._comf_apply_side_effects(71, target)
        s: Dict[str, int] = {}
        s["习得"] = 1800
        s["情爱"] = 900
        # ABL:侍奉精神
        abl16 = target.get_abl(16)
        if abl16 == 0:
            s["痛苦"] = 420
            s["恐怖"] = 150
            s["不洁"] = 400
        elif abl16 == 1:
            s["痛苦"] = 500
            s["恐怖"] = 300
            s["不洁"] = 300
        elif abl16 == 2:
            s["痛苦"] = 580
            s["恐怖"] = 600
            s["不洁"] = 150
        elif abl16 == 3:
            s["痛苦"] = 660
            s["恐怖"] = 900
            s["不洁"] = 50
        elif abl16 == 4:
            s["痛苦"] = 740
            s["恐怖"] = 1500
            s["不洁"] = 20
        else:
            s["痛苦"] = 820
            s["恐怖"] = 2200
            s["不洁"] = 0
        # ABL:乳房感觉
        abl1 = target.get_abl(1)
        a = 0
        if abl1 == 0:
            a = 100
        elif abl1 == 1:
            a = 200
        elif abl1 == 2:
            a = 400
        elif abl1 == 3:
            a = 800
        elif abl1 == 4:
            a = 1200
        else:
            a = 1500
        # 巨乳 TALENT:110
        if int(target.talent.get(110, 0)):
            a = self._scale_value(a, 1.20)
        # 乳房敏感 TALENT:108 / 乳房钝感 TALENT:107
        if int(target.talent.get(108, 0)):
            a = self._scale_value(a, 1.20)
        elif int(target.talent.get(107, 0)):
            a = self._scale_value(a, 0.70)
        s["损腐"] = int(s.get("损腐", 0)) + a
        # ABL:技巧
        abl12 = target.get_abl(12)
        if abl12 == 0:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.50)
        elif abl12 == 1:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 0.80)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 0.80)
        elif abl12 == 2:
            pass
        elif abl12 == 3:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.20)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.20)
        elif abl12 == 4:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 1.50)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 1.50)
        else:
            s["痛苦"] = self._scale_value(int(s.get("痛苦", 0)), 2.00)
            s["恐怖"] = self._scale_value(int(s.get("恐怖", 0)), 2.00)
        return s




    def _comf72(self, target: Character) -> Dict[str, int]:
        """刮阴毛 SOURCE计算"""
        self._comf_apply_side_effects(72, target)
        s: Dict[str, int] = {}
        a = 500
        s["恐怖"] = 750
        s["屈辱"] = 500
        s["反感"] = 1000
        s["情爱"] = 1200
        # PALAM:润滑
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam3 < 100:
            s["露出"] = 600
        elif palam3 < 500:
            s["露出"] = 250
        elif palam3 < 3000:
            s["露出"] = 100
        elif palam3 < 10000:
            s["露出"] = 30
        # ABL:露出癖
        abl7 = int(target.abl.get(7, 0))
        if abl7 == 0:
            a = self._scale_value(a, 0.80)
        elif abl7 == 1:
            pass
        elif abl7 == 2:
            a = self._scale_value(a, 1.20)
        elif abl7 == 3:
            a = self._scale_value(a, 1.50)
        elif abl7 == 4:
            a = self._scale_value(a, 2.00)
        else:
            a = self._scale_value(a, 2.60)
        # ABL:抖M气质
        abl21 = int(target.abl.get(21, 0))
        if abl21 == 0:
            a = self._scale_value(a, 0.80)
        elif abl21 == 1:
            pass
        elif abl21 == 2:
            a = self._scale_value(a, 1.20)
        elif abl21 == 3:
            a = self._scale_value(a, 1.40)
        elif abl21 == 4:
            a = self._scale_value(a, 1.70)
        else:
            a = self._scale_value(a, 2.00)
        s["屈辱"] = int(s.get("屈辱", 0)) + a
        s["抑郁"] = a
        s["反感"] = int(s.get("反感", 0)) + a
        return s




    def _comf73(self, target: Character) -> Dict[str, int]:
        """拨弄发型 SOURCE计算"""
        self._comf_apply_side_effects(73, target)
        s: Dict[str, int] = {}
        # ABL:顺从
        abl10 = target.get_abl(10)
        if abl10 == 0:
            s["习得"] = 100
        elif abl10 == 1:
            s["快B"] = 10
            s["习得"] = 250
        elif abl10 == 2:
            s["快B"] = 100
            s["习得"] = 500
        elif abl10 == 3:
            s["快B"] = 250
            s["习得"] = 1000
        elif abl10 == 4:
            s["快B"] = 500
            s["习得"] = 1500
        else:
            s["快B"] = 1000
            s["习得"] = 2000
        # ABL:露出癖
        abl17 = int(target.abl.get(17, 0))
        if abl17 == 0:
            s["反感"] = 500
        elif abl17 == 1:
            s["反感"] = 250
        elif abl17 == 2:
            s["反感"] = 100
        elif abl17 == 3:
            s["反感"] = 50
        elif abl17 == 4:
            s["反感"] = 25
        else:
            s["反感"] = 10
        # 调教者技巧 (simplified: assume player ABL:12 <= 3)
        s["露出"] = 100
        return s

    # =====================================================================
    # COMF 80-208 高级指令
    # =====================================================================




    def _comf80(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(80, target)
        s = {}
        s["痛苦"] = 300 + int(target.abl.get(10, 0)) * 50
        s["恐怖"] = 200
        s["屈辱"] = 300
        s["不洁"] = 200
        s["习得"] = 50
        if int(target.talent.get(76, 0)):
            s["中毒充足"] = 100
        return s




    def _comf81(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(81, target)
        s = {}
        s["快V"] = 500 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 800
        s["恐怖"] = 500
        s["不洁"] = 300
        s["屈辱"] = 400
        s["损腐"] = 200
        return s




    def _comf82(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(82, target)
        s = {}
        s["快A"] = 500 + int(target.abl.get(2, 0)) * 200
        s["痛苦"] = 800
        s["恐怖"] = 500
        s["不洁"] = 400
        s["屈辱"] = 400
        s["损腐"] = 200
        return s




    def _comf83(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(83, target)
        s = {}
        s["快V"] = 600 + int(target.abl.get(1, 0)) * 200
        s["快A"] = 600 + int(target.abl.get(2, 0)) * 200
        s["痛苦"] = 1000
        s["恐怖"] = 600
        s["不洁"] = 500
        s["屈辱"] = 500
        s["损腐"] = 300
        return s




    def _comf84(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(84, target)
        s = {}
        s["快V"] = 400 + int(target.abl.get(1, 0)) * 150
        s["情爱"] = 100
        s["习得"] = 50
        return s




    def _comf85(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(85, target)
        s = {}
        s["露出"] = 500
        s["屈辱"] = 400
        s["不洁"] = 300
        if int(target.talent.get(76, 0)):
            s["中毒充足"] = 100
        return s




    def _comf87(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(87, target)
        s = {}
        s["痛苦"] = 500
        s["恐怖"] = 300
        s["屈辱"] = 200
        s["损腐"] = 100
        return s




    def _comf89(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(89, target)
        s = {}
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 80
        s["痛苦"] = 200
        s["恐怖"] = 300
        s["不洁"] = 800
        s["屈辱"] = 500
        s["损腐"] = 100
        return s




    def _comf90(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(90, target)
        s = {}
        s["快B"] = 300 + int(target.abl.get(3, 0)) * 100
        s["痛苦"] = 200
        s["不洁"] = 100
        s["习得"] = 50
        return s




    def _comf100(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(100, target)
        s = {}
        s["恐怖"] = 200 + int(target.exp.get(55, 0)) * 10
        s["快C"] = 100
        s["快V"] = 100
        s["不洁"] = 200
        s["屈辱"] = 200
        return s




    def _comf110(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(110, target)
        s = {}
        s["露出"] = 100
        s["恭顺"] = 50
        return s




    def _comf111(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(111, target)
        s = {}
        s["露出"] = 300
        s["恐怖"] = 100
        s["屈辱"] = 200
        return s




    def _comf120(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(120, target)
        s = {}
        s["快V"] = 500 + int(target.abl.get(1, 0)) * 200
        s["情爱"] = 200
        s["习得"] = 100
        return s




    def _comf121(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(121, target)
        s = {}
        s["快V"] = 600 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 200
        s["恐怖"] = 100
        s["情爱"] = 100
        s["习得"] = 100
        return s




    def _comf122(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(122, target)
        s = {}
        s["快C"] = 200 + int(target.abl.get(0, 0)) * 80
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 80
        s["情爱"] = 200
        s["习得"] = 50
        return s




    def _comf123(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(123, target)
        s = {}
        s["快B"] = 200 + int(target.abl.get(3, 0)) * 80
        s["快C"] = 200 + int(target.abl.get(0, 0)) * 80
        s["不洁"] = 100
        s["习得"] = 50
        return s




    def _comf124(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(124, target)
        s = {}
        s["痛苦"] = 300
        s["恐怖"] = 200
        s["不洁"] = 300
        s["屈辱"] = 300
        s["习得"] = 50
        return s




    def _comf125(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(125, target)
        s = {}
        s["快C"] = 300 + int(target.abl.get(0, 0)) * 100
        s["快B"] = 100 + int(target.abl.get(3, 0)) * 50
        s["不洁"] = 100
        s["露出"] = 100
        return s




    def _comf126(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(126, target)
        s = {}
        s["快C"] = 200 + int(target.abl.get(0, 0)) * 80
        s["习得"] = 50
        s["不洁"] = 100
        s["情爱"] = 50
        return s




    def _comf127(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(127, target)
        s = {}
        s["快C"] = 300 + int(target.abl.get(0, 0)) * 100
        s["不洁"] = 200
        s["屈辱"] = 100
        s["习得"] = 50
        return s




    def _comf128(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(128, target)
        s = {}
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 150
        s["快C"] = 100 + int(target.abl.get(0, 0)) * 50
        s["情爱"] = 300
        s["习得"] = 50
        return s




    def _comf129(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(129, target)
        s = {}
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 150
        s["快B"] = 200 + int(target.abl.get(3, 0)) * 80
        s["情爱"] = 200
        s["习得"] = 50
        return s




    def _comf130(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(130, target)
        s = {}
        s["快V"] = 400 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 100
        s["恐怖"] = 50
        s["情爱"] = 100
        s["习得"] = 50
        return s




    def _comf131(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(131, target)
        s = {}
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 150
        s["快B"] = 200 + int(target.abl.get(3, 0)) * 80
        s["情爱"] = 200
        s["习得"] = 50
        return s




    def _comf132(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(132, target)
        s = {}
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 150
        s["痛苦"] = 200
        s["恐怖"] = 100
        s["习得"] = 50
        return s




    def _comf133(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(133, target)
        s = {}
        s["快V"] = 400 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 100
        s["露出"] = 100
        s["情爱"] = 50
        s["习得"] = 50
        return s




    def _comf134(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(134, target)
        s = {}
        s["快V"] = 400 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 100
        s["恐怖"] = 50
        s["习得"] = 50
        return s




    def _comf135(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(135, target)
        s = {}
        s["快C"] = 200 + int(target.abl.get(0, 0)) * 80
        s["不洁"] = 200
        s["露出"] = 200
        s["屈辱"] = 100
        return s




    def _comf150(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(150, target)
        return {}




    def _comf200(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(200, target)
        s = {}
        s["痛苦"] = 300
        s["恐怖"] = 300
        s["屈辱"] = 300
        s["快C"] = 100
        s["快V"] = 100
        s["不洁"] = 200
        return s




    def _comf201(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(201, target)
        s = {}
        s["快C"] = 100 + int(target.abl.get(0, 0)) * 50
        s["情爱"] = 100
        s["习得"] = 50
        return s




    def _comf202(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(202, target)
        s = {}
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 100
        s["不洁"] = 500
        s["屈辱"] = 400
        s["恐怖"] = 200
        s["损腐"] = 100
        return s




    def _comf203(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(203, target)
        s = {}
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 100
        s["不洁"] = 600
        s["屈辱"] = 500
        s["恐怖"] = 300
        s["损腐"] = 100
        return s




    def _comf204(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(204, target)
        s = {}
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 150
        s["痛苦"] = 200
        s["不洁"] = 500
        s["屈辱"] = 400
        s["恐怖"] = 200
        s["损腐"] = 100
        return s




    def _comf205(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(205, target)
        s = {}
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 100
        s["不洁"] = 700
        s["屈辱"] = 600
        s["恐怖"] = 300
        s["损腐"] = 200
        return s




    def _comf206(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(206, target)
        s = {}
        s["快V"] = 400 + int(target.abl.get(1, 0)) * 200
        s["痛苦"] = 300
        s["不洁"] = 500
        s["屈辱"] = 400
        s["恐怖"] = 300
        s["损腐"] = 200
        return s




    def _comf207(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(207, target)
        s = {}
        s["快V"] = 200 + int(target.abl.get(1, 0)) * 100
        s["快C"] = 200 + int(target.abl.get(0, 0)) * 100
        s["不洁"] = 400
        s["屈辱"] = 300
        s["中毒充足"] = 200
        return s




    def _comf208(self, target: Character) -> Dict[str, int]:
        self._comf_apply_side_effects(208, target)
        s = {}
        s["快C"] = 300 + int(target.abl.get(0, 0)) * 100
        s["快V"] = 300 + int(target.abl.get(1, 0)) * 100
        s["快A"] = 200 + int(target.abl.get(2, 0)) * 80
        s["快B"] = 200 + int(target.abl.get(3, 0)) * 80
        s["恐怖"] = 200
        s["不洁"] = 300
        s["屈辱"] = 200
        return s

    # =====================================================================
    # COMF 特殊指令
    # =====================================================================




    def _comf_analsex(self, target: Character) -> Dict[str, int]:
        s = {}
        abl2 = target.get_abl(2)
        s["快A"] = 500 + abl2 * 200
        s["不洁"] = 200
        s["屈辱"] = 200
        s["习得"] = 50
        if abl2 == 0:
            s["痛苦"] = 500
            s["恐怖"] = 300
        if int(target.talent.get(76, 0)):
            s["快A"] = int(s["快A"] * 1.5)
            s["中毒充足"] = 100
        return s




    def _comf_condom(self, target: Character) -> Dict[str, int]:
        return {}

    # ------------------------------------------------------------------
    # ABLUP99 - 反抗刻印消去
    # ------------------------------------------------------------------





    def _comf_jump(self, target: Character) -> Dict[str, int]:
        s = {}
        abl1 = target.get_abl(1)
        s["快V"] = 600 + abl1 * 250
        s["情爱"] = 300
        s["露出"] = 200
        s["习得"] = 50
        if int(target.talent.get(76, 0)):
            s["快V"] = int(s["快V"] * 1.5)
        if int(target.talent.get(85, 0)):
            s["情爱"] = int(s["情爱"] * 2)
        return s




    def _comf_vaginasex(self, target: Character) -> Dict[str, int]:
        s = {}
        abl1 = target.get_abl(1)
        s["快V"] = 500 + abl1 * 200
        s["情爱"] = 200
        s["不洁"] = 100
        s["习得"] = 50
        if int(target.talent.get(0, 0)):
            s["恐怖"] = 500
            s["痛苦"] = 500
        if int(target.talent.get(76, 0)):
            s["快V"] = int(s["快V"] * 1.5)
            s["中毒充足"] = 200
        if int(target.talent.get(85, 0)):
            s["情爱"] = int(s["情爱"] * 2)
        return s

