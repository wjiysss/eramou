from __future__ import annotations
"""Module for ComableExtMixin - 指令可用性"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ComableExtMixin:
    """Mixin providing 指令可用性 methods for GameEngine"""

    def _comorder(self, target: Character) -> Dict[int, int]:
        result: Dict[int, int] = {}
        a = 0
        player = self._get_player()

        abl_10 = target.abl.get(10, 0)
        if abl_10:
            val = abl_10 * 4
            a += val
            result[10] = val

        abl_21 = target.abl.get(21, 0)
        if abl_21:
            val = abl_21 * 2
            a += val
            result[21] = val

        is_same_sex = (player is not None and
                       player.talent.get(122, 0) == 0 and
                       target.talent.get(122, 0) == 0)

        if is_same_sex:
            abl_22 = target.abl.get(22, 0)
            if abl_22:
                val = abl_22 * 3
                a += val
                result[22] = val

            abl_33 = target.abl.get(33, 0)
            if abl_33:
                val = abl_33 * 3
                a += val
                result[33] = val

            if target.talent.get(81, 0):
                a += 10
                result[81] = 10

            if target.talent.get(23, 0):
                a += 7
                result[23] = 7

            if target.talent.get(24, 0):
                a -= 13
                result[24] = -13
        else:
            if target.talent.get(23, 0):
                a += 5
                result[23] = 5

            if target.talent.get(24, 0):
                a -= 10
                result[24] = -10

        mark_0 = target.mark.get(0, 0)
        if mark_0:
            val = mark_0 * 5
            a += val
            result[100] = val

        if target.talent.get(15, 0):
            t = 4
        elif target.talent.get(17, 0):
            t = 1
        else:
            t = 2

        mark_2 = target.mark.get(2, 0)
        if mark_2:
            val = mark_2 * 3 * t
            a += val
            result[102] = val

        mark_3 = target.mark.get(3, 0)
        if mark_3:
            val = mark_3 * 2 * t
            a -= val
            result[103] = -val

        palam_4_level = self._get_palam_level(target.palam.get(4, 0))
        if palam_4_level:
            val = palam_4_level * 3
            a += val
            result[200] = val

        palam_10_level = self._get_palam_level(target.palam.get(10, 0))
        if palam_10_level:
            val = palam_10_level * 3
            a += val
            result[210] = val

        talent_effects = {
            11: -5, 12: -5, 13: 5, 15: -15, 17: 5,
            28: 2, 32: -10, 34: -10, 37: 12, 73: 10,
            76: 5, 86: 8
        }
        for tid, val in talent_effects.items():
            if target.talent.get(tid, 0):
                a += val
                result[300 + tid] = val

        if player is not None:
            player_talent_effects = {91: 6, 92: 6, 93: 6, 83: 3, 118: 1}
            for tid, val in player_talent_effects.items():
                if player.talent.get(tid, 0):
                    a += val
                    result[400 + tid] = val

        if player is not None:
            rel_val = 0
            if hasattr(target, 'relation') and isinstance(target.relation, dict):
                rel_val = target.relation.get(0, 0)
            else:
                rel_val = self._get_character_relation(player)

            if 0 < rel_val < 30:
                a -= 10
                result[500] = -10
            elif 0 < rel_val < 70:
                a -= 6
                result[500] = -6
            elif 0 < rel_val < 100:
                a -= 3
                result[500] = -3
            elif 100 <= rel_val < 130:
                a += 3
                result[500] = 3
            elif 100 <= rel_val < 170:
                a += 6
                result[500] = 6
            elif rel_val >= 170:
                a += 10
                result[500] = 10

        result[0] = a
        return result



    def _multi_comable(self, com_id: int) -> bool:
        if com_id < 0 or com_id >= 1000:
            return False
        com_name = self.train_commands.get(com_id, "")
        if not com_name:
            return False
        return True





