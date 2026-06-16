from __future__ import annotations
"""Module for SourceMixin - SOURCE check methods for training source calculations"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SourceMixin:
    """Mixin providing SOURCE check methods for training source calculations"""
    def _source_check(self, target: Character, com_id: int) -> Dict[str, int]:
        v = self.interpreter.vars
        up: Dict[int, int] = {i: 0 for i in range(16)}

        assiplay = self.state.assiplay
        ejaculation_flags = [0, 1, 2, 4, 5, 7, 8, 9, 18]
        any_ejac = any(v.tflag.get(f, 0) for f in ejaculation_flags)

        if assiplay == 0 and target.equipt.get(35, 0) and any_ejac:
            target.equipt[35] = 0
            for f in ejaculation_flags:
                v.tflag[f] = 0
        elif assiplay and target.equipt.get(36, 0) and any_ejac:
            target.equipt[36] = 0
            for f in ejaculation_flags:
                v.tflag[f] = 0

        if target.equipt.get(36, 0) and v.tflag.get(6, 0) and int(v.assi) > 0:
            target.equipt[36] = 0
            v.tflag[6] = 0

        equip_ids = [11, 13, 14, 15, 16, 17, 18, 19, 43, 44, 45, 46, 47, 49, 53, 54, 57, 58, 59, 89, 90, 98]
        for eid in equip_ids:
            if target.equipt.get(eid, 0):
                pass

        up_c = self._source_check_up_c(target)
        up_v = self._source_check_up_v(target)
        up_a = self._source_check_up_a(target)
        up_b = self._source_check_up_b(target)
        up_f = self._source_check_up_free(target)

        for d in [up_c, up_v, up_a, up_b, up_f]:
            for key, val in d.items():
                up[key] = up.get(key, 0) + val

        prevcom = self.state.prevcom
        if com_id == prevcom and not self.state.is_first_training:
            for key in [0, 1, 2, 14]:
                up[key] = up.get(key, 0) // 2

        if target.base.get(1, 0) <= 0 and not self.state.is_first_training:
            for key in [0, 1, 2, 14]:
                up[key] = up.get(key, 0) // 2

        player = self._get_player()
        if player is not None:
            relation_val = self._get_relation_value(player)
            if relation_val != 0 and not self.state.is_first_training:
                for key in [0, 1, 2, 14]:
                    up[key] = up.get(key, 0) * relation_val // 100

        # LOVE_MOIST_CHECK_UP - modifies target.source[10]
        self._love_moist_check_up(target, up)

        # MOIST first (FLASHER depends on UP:3)
        up_moist = self._source_check_up_moist(target)
        for key, val in up_moist.items():
            up[key] = up.get(key, 0) + val

        # Remaining CHECK_UP functions
        up_love = self._source_check_up_love(target)
        up_impulsive = self._source_check_up_impulsive(target)
        up_achieve = self._source_check_up_achieve(target)
        up_pain = self._source_check_up_pain(target)
        up_poison = self._source_check_up_poison(target)
        up_dirty = self._source_check_up_dirty(target)
        up_desire = self._source_check_up_desire(target)
        up_flasher = self._source_check_up_flasher(target, up)
        up_submit = self._source_check_up_submit(target)
        up_deviate = self._source_check_up_deviate(target)
        up_anti = self._source_check_up_anti(target)
        up_like = self._source_check_up_like(target)

        for d in [up_love, up_impulsive, up_achieve, up_pain, up_poison, up_dirty,
                  up_desire, up_flasher, up_submit, up_deviate, up_anti, up_like]:
            for key, val in d.items():
                up[key] = up.get(key, 0) + val

        # PAIN_DAMAGE_CHECK_UP - adds to target.losebase
        self._pain_damage_check_up(target, up)

        return up


    def _source_check_up_c(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        v = self.interpreter.vars
        source_0 = target.source.get(0, 0)

        talent_101 = target.talent.get(101, 0)
        if talent_101 & 1:
            source_0 = int(source_0 * 0.50)
        if talent_101 & 2:
            source_0 = int(source_0 * 0.10)
        if target.talent.get(102, 0):
            source_0 = int(source_0 * 2.00)

        local_0 = source_0
        palam_5 = target.palam.get(5, 0)
        plt = self.palam_level_thresholds
        if self.state.is_first_training:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[1]:
            local_0 = int(local_0 * 0.50)
        elif palam_5 < plt[2]:
            local_0 = int(local_0 * 0.70)
        elif palam_5 < plt[3]:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[4]:
            local_0 = int(local_0 * 1.30)
        else:
            local_0 = int(local_0 * 1.80)

        local_1 = source_0
        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_1 = int(local_1 * 0.10)
        elif abl_11 == 1:
            local_1 = int(local_1 * 0.15)
        elif abl_11 == 2:
            local_1 = int(local_1 * 0.20)
        elif abl_11 == 3:
            local_1 = int(local_1 * 0.25)
        elif abl_11 == 4:
            local_1 = int(local_1 * 0.30)
        elif abl_11 == 5:
            local_1 = int(local_1 * 0.40)
        else:
            local_1 = int(local_1 * 0.50)

        local_2 = 0
        if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(71, 0):
            local_2 = source_0 // 3
            if abl_11 == 0:
                local_2 = int(local_2 * 1.00)
            elif abl_11 == 1:
                local_2 = int(local_2 * 0.85)
            elif abl_11 == 2:
                local_2 = int(local_2 * 0.70)
            elif abl_11 == 3:
                local_2 = int(local_2 * 0.40)
            elif abl_11 == 4:
                local_2 = int(local_2 * 0.30)
            elif abl_11 == 5:
                local_2 = int(local_2 * 0.10)
            else:
                local_2 = 0

        if target.talent.get(74, 0):
            local_0 = int(local_0 * 1.50)
            local_1 = int(local_1 * 1.20)
            local_2 = int(local_2 * 0.50)

        if target.talent.get(230, 0):
            local_0 = int(local_0 * 2.00)

        abl_0 = target.get_abl(0)
        if abl_0 > 5:
            local_0 = local_0 * (abl_0 + 5) // 10

        up[0] = local_0
        up[5] = up.get(5, 0) + local_1
        up[13] = up.get(13, 0) + local_2
        return up


    def _source_check_up_v(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        v = self.interpreter.vars
        source_1 = target.source.get(1, 0)

        talent_103 = target.talent.get(103, 0)
        if talent_103 & 1:
            source_1 = int(source_1 * 0.50)
        if talent_103 & 2:
            source_1 = int(source_1 * 0.10)
        if target.talent.get(104, 0):
            source_1 = int(source_1 * 2.00)

        local_0 = source_1
        palam_5 = target.palam.get(5, 0)
        plt = self.palam_level_thresholds
        if self.state.is_first_training:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[1]:
            local_0 = int(local_0 * 0.30)
        elif palam_5 < plt[2]:
            local_0 = int(local_0 * 0.50)
        elif palam_5 < plt[3]:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[4]:
            local_0 = int(local_0 * 1.50)
        else:
            local_0 = int(local_0 * 2.00)

        local_1 = source_1
        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_1 = int(local_1 * 0.10)
        elif abl_11 == 1:
            local_1 = int(local_1 * 0.15)
        elif abl_11 == 2:
            local_1 = int(local_1 * 0.20)
        elif abl_11 == 3:
            local_1 = int(local_1 * 0.25)
        elif abl_11 == 4:
            local_1 = int(local_1 * 0.30)
        elif abl_11 == 5:
            local_1 = int(local_1 * 0.40)
        else:
            local_1 = int(local_1 * 0.50)

        local_2 = 0
        if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(71, 0):
            local_2 = source_1 // 3
            if abl_11 == 0:
                local_2 = int(local_2 * 1.00)
            elif abl_11 == 1:
                local_2 = int(local_2 * 0.85)
            elif abl_11 == 2:
                local_2 = int(local_2 * 0.70)
            elif abl_11 == 3:
                local_2 = int(local_2 * 0.40)
            elif abl_11 == 4:
                local_2 = int(local_2 * 0.30)
            elif abl_11 == 5:
                local_2 = int(local_2 * 0.10)
            else:
                local_2 = 0

        if target.talent.get(75, 0):
            local_0 = int(local_0 * 1.50)
            local_1 = int(local_1 * 1.20)
            local_2 = int(local_2 * 0.50)

        if target.talent.get(232, 0):
            local_0 = int(local_0 * 1.50)

        abl_2 = target.get_abl(2)
        if abl_2 > 5:
            local_0 = local_0 * (abl_2 + 5) // 10

        up[1] = local_0
        up[4] = up.get(4, 0) + local_1
        up[5] = up.get(5, 0) + local_1
        up[13] = up.get(13, 0) + local_2
        return up


    def _source_check_up_a(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        v = self.interpreter.vars
        source_2 = target.source.get(2, 0)

        talent_105 = target.talent.get(105, 0)
        if talent_105 & 1:
            source_2 = int(source_2 * 0.50)
        if talent_105 & 2:
            source_2 = int(source_2 * 0.10)
        if target.talent.get(106, 0):
            source_2 = int(source_2 * 2.00)

        local_0 = source_2
        palam_5 = target.palam.get(5, 0)
        plt = self.palam_level_thresholds
        if self.state.is_first_training:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[1]:
            local_0 = int(local_0 * 0.60)
        elif palam_5 < plt[2]:
            local_0 = int(local_0 * 0.80)
        elif palam_5 < plt[3]:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[4]:
            local_0 = int(local_0 * 1.20)
        else:
            local_0 = int(local_0 * 1.40)

        local_1 = source_2
        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_1 = int(local_1 * 0.05)
        elif abl_11 == 1:
            local_1 = int(local_1 * 0.10)
        elif abl_11 == 2:
            local_1 = int(local_1 * 0.40)
        elif abl_11 == 3:
            local_1 = int(local_1 * 0.80)
        elif abl_11 == 4:
            local_1 = int(local_1 * 1.20)
        elif abl_11 == 5:
            local_1 = int(local_1 * 1.80)
        else:
            local_1 = int(local_1 * 2.00)

        local_2 = 0
        if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(71, 0):
            local_2 = source_2 // 3
            if abl_11 == 0:
                local_2 = int(local_2 * 1.00)
            elif abl_11 == 1:
                local_2 = int(local_2 * 0.85)
            elif abl_11 == 2:
                local_2 = int(local_2 * 0.70)
            elif abl_11 == 3:
                local_2 = int(local_2 * 0.40)
            elif abl_11 == 4:
                local_2 = int(local_2 * 0.30)
            elif abl_11 == 5:
                local_2 = int(local_2 * 0.10)
            else:
                local_2 = 0

        if target.talent.get(77, 0):
            local_0 = int(local_0 * 1.50)
            local_1 = int(local_1 * 1.20)
            local_2 = int(local_2 * 0.50)

        if target.talent.get(233, 0):
            local_0 = int(local_0 * 2.00)

        abl_3 = target.get_abl(3)
        if abl_3 > 5:
            local_0 = local_0 * (abl_3 + 5) // 10

        up[2] = local_0
        up[5] = up.get(5, 0) + local_1
        up[6] = up.get(6, 0) + local_1
        up[13] = up.get(13, 0) + local_2
        return up


    def _source_check_up_b(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        v = self.interpreter.vars
        source_17 = target.source.get(17, 0)
        source_1 = target.source.get(1, 0)

        talent_107 = target.talent.get(107, 0)
        if talent_107 & 1:
            source_17 = int(source_17 * 0.50)
        if talent_107 & 2:
            source_17 = int(source_17 * 0.10)
        if target.talent.get(108, 0):
            source_17 = int(source_17 * 2.00)

        if target.talent.get(253, 0):
            source_1 = int(source_1 * 2.50)
        elif target.talent.get(252, 0):
            source_1 = int(source_1 * 2.15)
        elif target.talent.get(251, 0):
            source_1 = int(source_1 * 1.80)
        elif target.talent.get(116, 0):
            source_1 = int(source_1 * 1.50)
        elif target.talent.get(109, 0):
            source_1 = int(source_1 * 1.20)
        elif target.talent.get(110, 0):
            source_1 = int(source_1 * 0.90)
        elif target.talent.get(114, 0):
            source_1 = int(source_1 * 0.80)
        elif target.talent.get(119, 0):
            source_1 = int(source_1 * 0.70)

        local_0 = source_17
        palam_5 = target.palam.get(5, 0)
        plt = self.palam_level_thresholds
        if self.state.is_first_training:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[1]:
            local_0 = int(local_0 * 0.50)
        elif palam_5 < plt[2]:
            local_0 = int(local_0 * 0.70)
        elif palam_5 < plt[3]:
            local_0 = int(local_0 * 1.00)
        elif palam_5 < plt[4]:
            local_0 = int(local_0 * 1.30)
        else:
            local_0 = int(local_0 * 1.80)

        local_1 = source_17
        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_1 = int(local_1 * 0.10)
        elif abl_11 == 1:
            local_1 = int(local_1 * 0.15)
        elif abl_11 == 2:
            local_1 = int(local_1 * 0.20)
        elif abl_11 == 3:
            local_1 = int(local_1 * 0.25)
        elif abl_11 == 4:
            local_1 = int(local_1 * 0.30)
        elif abl_11 == 5:
            local_1 = int(local_1 * 0.40)
        else:
            local_1 = int(local_1 * 0.50)

        local_2 = 0
        if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(71, 0):
            local_2 = source_17 // 3
            if abl_11 == 0:
                local_2 = int(local_2 * 1.00)
            elif abl_11 == 1:
                local_2 = int(local_2 * 0.85)
            elif abl_11 == 2:
                local_2 = int(local_2 * 0.70)
            elif abl_11 == 3:
                local_2 = int(local_2 * 0.40)
            elif abl_11 == 4:
                local_2 = int(local_2 * 0.30)
            elif abl_11 == 5:
                local_2 = int(local_2 * 0.10)
            else:
                local_2 = 0

        if target.talent.get(78, 0):
            local_0 = int(local_0 * 1.50)
            local_1 = int(local_1 * 1.20)
            local_2 = int(local_2 * 0.50)

        if target.talent.get(231, 0):
            local_0 = int(local_0 * 2.00)

        abl_1 = target.get_abl(1)
        if abl_1 > 5:
            local_0 = local_0 * (abl_1 + 5) // 10

        up[14] = local_0
        up[5] = up.get(5, 0) + local_1
        up[13] = up.get(13, 0) + local_2
        return up


    def _source_check_up_free(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        local_0 = target.source.get(18, 0)
        up[15] = local_0
        return up


    def _source_check_up_love(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_3 = target.source.get(3, 0)
        local_0 = source_3
        local_1 = source_3

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_0 = int(local_0 * 0.10)
        elif abl_10 == 1:
            local_0 = int(local_0 * 0.25)
        elif abl_10 == 2:
            local_0 = int(local_0 * 0.40)
        elif abl_10 == 3:
            local_0 = int(local_0 * 0.60)
        elif abl_10 == 4:
            local_0 = int(local_0 * 0.80)
        elif abl_10 == 5:
            local_0 = int(local_0 * 1.00)
        else:
            local_0 = int(local_0 * 1.20)

        abl_16 = target.get_abl(16)
        if abl_16 == 0:
            local_0 = int(local_0 * 0.95)
        elif abl_16 == 1:
            local_0 = int(local_0 * 1.00)
        elif abl_16 == 2:
            local_0 = int(local_0 * 1.05)
        elif abl_16 == 3:
            local_0 = int(local_0 * 1.10)
        elif abl_16 == 4:
            local_0 = int(local_0 * 1.15)
        elif abl_16 == 5:
            local_0 = int(local_0 * 1.20)
        else:
            local_0 = int(local_0 * 1.30)

        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_1 = int(local_1 * 0.00)
        elif abl_11 == 1:
            local_1 = int(local_1 * 0.05)
        elif abl_11 == 2:
            local_1 = int(local_1 * 0.10)
        elif abl_11 == 3:
            local_1 = int(local_1 * 0.20)
        elif abl_11 == 4:
            local_1 = int(local_1 * 0.30)
        elif abl_11 == 5:
            local_1 = int(local_1 * 0.40)
        else:
            local_1 = int(local_1 * 0.50)

        up[4] = up.get(4, 0) + local_0
        up[5] = up.get(5, 0) + local_1
        return up


    def _source_check_up_impulsive(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_4 = target.source.get(4, 0)
        local_0 = source_4

        abl_16 = target.get_abl(16)
        if abl_16 == 0:
            local_0 = int(local_0 * 0.60)
        elif abl_16 == 1:
            local_0 = int(local_0 * 0.80)
        elif abl_16 == 2:
            local_0 = int(local_0 * 1.00)
        elif abl_16 == 3:
            local_0 = int(local_0 * 1.20)
        elif abl_16 == 4:
            local_0 = int(local_0 * 1.40)
        elif abl_16 == 5:
            local_0 = int(local_0 * 1.70)
        else:
            local_0 = int(local_0 * 2.00)

        abl_13 = target.get_abl(13)
        if abl_13 == 0:
            local_0 = int(local_0 * 0.95)
        elif abl_13 == 1:
            local_0 = int(local_0 * 1.00)
        elif abl_13 == 2:
            local_0 = int(local_0 * 1.05)
        elif abl_13 == 3:
            local_0 = int(local_0 * 1.10)
        elif abl_13 == 4:
            local_0 = int(local_0 * 1.15)
        elif abl_13 == 5:
            local_0 = int(local_0 * 1.20)
        else:
            local_0 = int(local_0 * 1.30)

        local_1 = 0
        if target.talent.get(32, 0) or target.talent.get(34, 0):
            local_1 = source_4 // 5
            if abl_16 == 0:
                local_1 = int(local_1 * 1.80)
            elif abl_16 == 1:
                local_1 = int(local_1 * 1.30)
            elif abl_16 == 2:
                local_1 = int(local_1 * 0.90)
            elif abl_16 == 3:
                local_1 = int(local_1 * 0.70)
            elif abl_16 == 4:
                local_1 = int(local_1 * 0.50)
            elif abl_16 == 5:
                local_1 = int(local_1 * 0.30)
            else:
                local_1 = int(local_1 * 0.10)

        up[7] = up.get(7, 0) + local_0
        up[13] = up.get(13, 0) + local_1
        return up


    def _source_check_up_achieve(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_5 = target.source.get(5, 0)
        local_0 = source_5

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_0 = int(local_0 * 0.50)
        elif abl_10 == 1:
            local_0 = int(local_0 * 0.80)
        elif abl_10 == 2:
            local_0 = int(local_0 * 1.00)
        elif abl_10 == 3:
            local_0 = int(local_0 * 1.20)
        elif abl_10 == 4:
            local_0 = int(local_0 * 1.40)
        elif abl_10 == 5:
            local_0 = int(local_0 * 1.60)
        elif abl_10 == 6:
            local_0 = int(local_0 * 1.80)
        else:
            local_0 = int(local_0 * 2.00)

        abl_16 = target.get_abl(16)
        if abl_16 == 0:
            local_0 = int(local_0 * 0.00)
        elif abl_16 == 1:
            local_0 = int(local_0 * 0.40)
        elif abl_16 == 2:
            local_0 = int(local_0 * 0.80)
        elif abl_16 == 3:
            local_0 = int(local_0 * 1.20)
        elif abl_16 == 4:
            local_0 = int(local_0 * 1.60)
        elif abl_16 == 5:
            local_0 = int(local_0 * 2.00)
        else:
            local_0 = int(local_0 * 2.40)

        abl_13 = target.get_abl(13)
        if abl_13 == 0:
            local_0 = int(local_0 * 0.95)
        elif abl_13 == 1:
            local_0 = int(local_0 * 1.00)
        elif abl_13 == 2:
            local_0 = int(local_0 * 1.05)
        elif abl_13 == 3:
            local_0 = int(local_0 * 1.10)
        elif abl_13 == 4:
            local_0 = int(local_0 * 1.15)
        elif abl_13 == 5:
            local_0 = int(local_0 * 1.20)
        else:
            local_0 = int(local_0 * 1.30)

        up[4] = up.get(4, 0) + local_0
        return up


    def _source_check_up_pain(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_6 = target.source.get(6, 0)
        local_0 = source_6
        local_1 = source_6
        local_2 = source_6
        local_3 = source_6

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_1 = int(local_1 * 0.80)
            local_2 = int(local_2 * 0.80)
        elif abl_10 == 1:
            local_1 = int(local_1 * 0.70)
            local_2 = int(local_2 * 0.60)
        elif abl_10 == 2:
            local_1 = int(local_1 * 0.55)
            local_2 = int(local_2 * 0.50)
        elif abl_10 == 3:
            local_1 = int(local_1 * 0.45)
            local_2 = int(local_2 * 0.40)
        elif abl_10 == 4:
            local_1 = int(local_1 * 0.35)
            local_2 = int(local_2 * 0.20)
        elif abl_10 == 5:
            local_1 = int(local_1 * 0.25)
            local_2 = int(local_2 * 0.05)
        else:
            local_1 = int(local_1 * 0.15)
            local_2 = 0

        abl_21 = target.get_abl(21)
        if abl_21 == 0:
            local_2 = int(local_2 * 1.00)
            local_3 = 0
        elif abl_21 == 1:
            local_2 = int(local_2 * 0.80)
            local_3 = int(local_3 * 0.10)
        elif abl_21 == 2:
            local_2 = int(local_2 * 0.50)
            local_3 = int(local_3 * 0.20)
        elif abl_21 == 3:
            local_2 = int(local_2 * 0.30)
            local_3 = int(local_3 * 0.30)
        elif abl_21 == 4:
            local_2 = int(local_2 * 0.10)
            local_3 = int(local_3 * 0.45)
        elif abl_21 == 5:
            local_2 = int(local_2 * 0.05)
            local_3 = int(local_3 * 0.60)
        else:
            local_2 = 0
            local_3 = int(local_3 * 0.75)

        player = self._get_player()
        abl_20 = player.abl.get(20, 0) if player else 0
        if abl_20 == 0:
            local_3 = int(local_3 * 1.00)
        elif abl_20 == 1:
            local_3 = int(local_3 * 1.10)
        elif abl_20 == 2:
            local_3 = int(local_3 * 1.20)
        elif abl_20 == 3:
            local_3 = int(local_3 * 1.30)
        elif abl_20 == 4:
            local_3 = int(local_3 * 1.40)
        elif abl_20 == 5:
            local_3 = int(local_3 * 1.50)
        else:
            local_3 = int(local_3 * 1.60)

        if target.talent.get(88, 0):
            local_3 = int(local_3 * 2.00)

        if player and player.talent.get(83, 0):
            local_3 = int(local_3 * 2.00)

        if target.talent.get(40, 0):
            local_0 = int(local_0 * 1.50)
            local_3 = int(local_3 * 4.00)
        elif target.talent.get(41, 0):
            local_0 = int(local_0 * 0.80)
            local_3 = int(local_3 * 0.80)

        v = self.interpreter.vars
        assiplay = v.tflag.get(50, 0)
        if assiplay:
            local_2 = int(local_2 * 0.40)

        up[9] = up.get(9, 0) + local_0
        up[10] = up.get(10, 0) + local_1
        up[11] = up.get(11, 0) + local_2
        up[5] = up.get(5, 0) + local_3
        return up


    def _source_check_up_poison(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_7 = target.source.get(7, 0)
        local_0 = source_7
        local_1 = source_7

        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_0 = int(local_0 * 0.10)
            local_1 = int(local_1 * 0.20)
        elif abl_11 == 1:
            local_0 = int(local_0 * 0.15)
            local_1 = int(local_1 * 0.30)
        elif abl_11 == 2:
            local_0 = int(local_0 * 0.20)
            local_1 = int(local_1 * 0.40)
        elif abl_11 == 3:
            local_0 = int(local_0 * 0.25)
            local_1 = int(local_1 * 0.50)
        elif abl_11 == 4:
            local_0 = int(local_0 * 0.30)
            local_1 = int(local_1 * 0.60)
        elif abl_11 == 5:
            local_0 = int(local_0 * 0.35)
            local_1 = int(local_1 * 0.70)
        elif abl_11 == 6:
            local_0 = int(local_0 * 0.40)
            local_1 = int(local_1 * 0.80)
        elif abl_11 == 7:
            local_0 = int(local_0 * 0.45)
            local_1 = int(local_1 * 0.90)
        else:
            local_0 = int(local_0 * 0.50)
            local_1 = int(local_1 * 1.00)

        up[4] = up.get(4, 0) + local_0
        up[5] = up.get(5, 0) + local_1
        return up


    def _source_check_up_dirty(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_8 = target.source.get(8, 0)
        local_0 = source_8
        local_1 = source_8

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_0 = int(local_0 * 0.60)
            local_1 = int(local_1 * 1.00)
        elif abl_10 == 1:
            local_0 = int(local_0 * 0.40)
            local_1 = int(local_1 * 0.80)
        elif abl_10 == 2:
            local_0 = int(local_0 * 0.25)
            local_1 = int(local_1 * 0.60)
        elif abl_10 == 3:
            local_0 = int(local_0 * 0.10)
            local_1 = int(local_1 * 0.30)
        elif abl_10 == 4:
            local_0 = 0
            local_1 = int(local_1 * 0.10)
        else:
            local_0 = 0
            local_1 = 0

        up[11] = up.get(11, 0) + local_0
        up[12] = up.get(12, 0) + local_1
        return up


    def _source_check_up_moist(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        local_0 = target.source.get(10, 0)
        up[3] = up.get(3, 0) + local_0
        return up


    def _source_check_up_desire(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        local_0 = target.source.get(11, 0)
        up[5] = up.get(5, 0) + local_0
        return up


    def _source_check_up_flasher(self, target: Character, current_up: Dict[int, int]) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_12 = target.source.get(12, 0)

        if target.talent.get(35, 0):
            source_12 = int(source_12 * 2.00)
        if target.talent.get(36, 0):
            source_12 = int(source_12 * 0.50)

        source_12 += (current_up.get(3, 0) - target.source.get(10, 0)) // 2

        local_0 = source_12
        local_1 = source_12
        local_2 = source_12

        abl_17 = target.abl.get(17, 0)
        if abl_17 == 0:
            local_0 = 0
            local_2 = int(local_2 * 1.00)
        elif abl_17 == 1:
            local_0 = int(local_0 * 0.10)
            local_2 = int(local_2 * 0.90)
        elif abl_17 == 2:
            local_0 = int(local_0 * 0.20)
            local_2 = int(local_2 * 0.70)
        elif abl_17 == 3:
            local_0 = int(local_0 * 0.40)
            local_2 = int(local_2 * 0.50)
        elif abl_17 == 4:
            local_0 = int(local_0 * 0.60)
            local_2 = int(local_2 * 0.30)
        elif abl_17 == 5:
            local_0 = int(local_0 * 0.80)
            local_2 = int(local_2 * 0.10)
        else:
            local_0 = int(local_0 * 1.00)
            local_2 = 0

        palam_8 = target.palam.get(8, 0)
        plt = self.palam_level_thresholds
        if palam_8 < plt[1]:
            local_1 = int(local_1 * 1.00)
        elif palam_8 < plt[2]:
            local_1 = int(local_1 * 0.90)
        elif palam_8 < plt[3]:
            local_1 = int(local_1 * 0.70)
        elif palam_8 < plt[4]:
            local_1 = int(local_1 * 0.50)
        else:
            local_1 = int(local_1 * 0.30)

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_2 = int(local_2 * 0.50)
        elif abl_10 == 1:
            local_2 = int(local_2 * 0.30)
        elif abl_10 == 2:
            local_2 = int(local_2 * 0.15)
        elif abl_10 == 3:
            local_2 = int(local_2 * 0.05)
        else:
            local_2 = 0

        up[5] = up.get(5, 0) + local_0
        up[8] = up.get(8, 0) + local_1
        up[11] = up.get(11, 0) + local_2
        return up


    def _source_check_up_submit(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_13 = target.source.get(13, 0)
        local_0 = source_13
        local_1 = source_13

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_0 = int(local_0 * 0.12)
            local_1 = int(local_1 * 0.50)
        elif abl_10 == 1:
            local_0 = int(local_0 * 0.10)
            local_1 = int(local_1 * 0.80)
        elif abl_10 == 2:
            local_0 = int(local_0 * 0.05)
            local_1 = int(local_1 * 1.00)
        elif abl_10 == 3:
            local_0 = int(local_0 * 0.02)
            local_1 = int(local_1 * 1.10)
        elif abl_10 == 4:
            local_0 = 0
            local_1 = int(local_1 * 1.20)
        elif abl_10 == 5:
            local_0 = 0
            local_1 = int(local_1 * 1.30)
        elif abl_10 == 6:
            local_0 = 0
            local_1 = int(local_1 * 1.40)
        else:
            local_0 = 0
            local_1 = int(local_1 * 1.50)

        abl_39 = target.abl.get(39, 0)
        if abl_39 == 0:
            local_1 = int(local_1 * 1.00)
        elif abl_39 == 1:
            local_1 = int(local_1 * 1.10)
        elif abl_39 == 2:
            local_1 = int(local_1 * 1.20)
        elif abl_39 == 3:
            local_1 = int(local_1 * 1.50)
        elif abl_39 == 4:
            local_1 = int(local_1 * 2.00)
        elif abl_39 == 5:
            local_1 = int(local_1 * 3.00)
        else:
            local_1 = int(local_1 * 4.00)

        up[13] = up.get(13, 0) + local_0
        up[6] = up.get(6, 0) + local_1
        return up


    def _source_check_up_deviate(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        source_14 = target.source.get(14, 0)

        if target.talent.get(23, 0):
            source_14 = int(source_14 * 0.30)
        if target.talent.get(24, 0):
            source_14 = int(source_14 * 3.00)

        local_0 = source_14

        abl_10 = target.get_abl(10)
        if abl_10 == 0:
            local_0 = int(local_0 * 1.00)
        elif abl_10 == 1:
            local_0 = int(local_0 * 0.80)
        elif abl_10 == 2:
            local_0 = int(local_0 * 0.70)
        elif abl_10 == 3:
            local_0 = int(local_0 * 0.40)
        elif abl_10 == 4:
            local_0 = int(local_0 * 0.20)
        else:
            local_0 = 0

        abl_11 = target.get_abl(11)
        if abl_11 == 0:
            local_0 = int(local_0 * 0.90)
        elif abl_11 == 1:
            local_0 = int(local_0 * 0.70)
        elif abl_11 == 2:
            local_0 = int(local_0 * 0.50)
        elif abl_11 == 3:
            local_0 = int(local_0 * 0.30)
        elif abl_11 == 4:
            local_0 = int(local_0 * 0.10)
        else:
            local_0 = 0

        up[11] = up.get(11, 0) + local_0
        return up


    def _source_check_up_anti(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        local_0 = target.source.get(15, 0)
        up[11] = up.get(11, 0) + local_0
        return up


    def _source_check_up_like(self, target: Character) -> Dict[int, int]:
        up: Dict[int, int] = {}
        local_0 = target.source.get(16, 0)
        up[4] = up.get(4, 0) + local_0
        return up


    def _love_moist_check_up(self, target: Character, current_up: Dict[int, int]) -> None:
        local_0 = current_up.get(0, 0) + current_up.get(1, 0) + current_up.get(2, 0) + current_up.get(14, 0)
        if local_0 > 100 and target.talent.get(122, 0) == 0:
            if target.talent.get(42, 0):
                local_0 = int(local_0 * 3.00)
            if target.talent.get(43, 0):
                local_0 = int(local_0 * 0.40)
            if target.talent.get(170, 0):
                local_0 = int(local_0 * 0.10)
            target.source[10] = target.source.get(10, 0) + local_0 // 5


    def _pain_damage_check_up(self, target: Character, current_up: Dict[int, int]) -> None:
        dmg = current_up.get(9, 0) // 16
        abl_21 = target.get_abl(21)
        if abl_21 == 0:
            dmg = int(dmg * 1.00)
        elif abl_21 == 1:
            dmg = int(dmg * 0.95)
        elif abl_21 == 2:
            dmg = int(dmg * 0.90)
        elif abl_21 == 3:
            dmg = int(dmg * 0.80)
        elif abl_21 == 4:
            dmg = int(dmg * 0.65)
        else:
            dmg = int(dmg * 0.50)

        if target.talent.get(40, 0):
            dmg = int(dmg * 1.20)
        if target.talent.get(41, 0):
            dmg = int(dmg * 0.80)

        target.losebase[0] = target.losebase.get(0, 0) + dmg
        target.losebase[1] = target.losebase.get(1, 0) + dmg


    def _confirm_lost_virgin(self, target: Character) -> bool:
        if target.has_talent(0):
            return True
        return True


    def _com_ejac_player_sex(self, target: Character) -> int:
        b = 0
        abl12 = target.get_abl(12)
        if abl12 == 0:
            b = 1500
        elif abl12 == 1:
            b = 1600
        elif abl12 == 2:
            b = 1800
        elif abl12 == 3:
            b = 2000
        elif abl12 == 4:
            b = 2400
        else:
            b = 3000
        abl10 = target.get_abl(10)
        if abl10 == 0:
            b = int(b * 0.80)
        elif abl10 == 1:
            b = int(b * 0.90)
        elif abl10 == 2:
            b = int(b * 1.00)
        elif abl10 == 3:
            b = int(b * 1.10)
        elif abl10 == 4:
            b = int(b * 1.20)
        else:
            b = int(b * 1.30)
        if int(target.talent.get(76, 0)):
            b = int(b * 1.20)
        if target.has_talent(85):
            b = int(b * 1.20)
        return b


    def _com_ejac_player_analsex(self, target: Character) -> int:
        b = 0
        abl12 = target.get_abl(12)
        if abl12 == 0:
            b = 1500
        elif abl12 == 1:
            b = 1600
        elif abl12 == 2:
            b = 1800
        elif abl12 == 3:
            b = 2000
        elif abl12 == 4:
            b = 2400
        else:
            b = 3000
        abl10 = target.get_abl(10)
        if abl10 == 0:
            b = int(b * 0.80)
        elif abl10 == 1:
            b = int(b * 0.90)
        elif abl10 == 2:
            b = int(b * 1.00)
        elif abl10 == 3:
            b = int(b * 1.10)
        elif abl10 == 4:
            b = int(b * 1.20)
        else:
            b = int(b * 1.30)
        if int(target.talent.get(76, 0)):
            b = int(b * 1.10)
        return b

    # =====================================================================
    # EQUIP_COM 装备效果 (调教中)
    # =====================================================================


    def _source_sex_check(self, target: Character) -> Dict[str, int]:
        source = {}
        player = self._get_player()
        target_female = target.has_talent(1) or target.has_talent(2)
        player_female = player.has_talent(1) or player.has_talent(2)
        if target_female and player_female:
            if target.has_talent(81):
                source["情爱"] = source.get("情爱", 0) + 200
            elif target.has_talent(22):
                source["情爱"] = source.get("情爱", 0) + 100
            elif target.has_talent(23):
                source["情爱"] = source.get("情爱", 0) + 50
            elif target.has_talent(24):
                source["反感"] = source.get("反感", 0) + 200
        return source


    def _player_skill_check(self, target: Character) -> Dict[str, int]:
        source = {}
        player = self._get_player()
        abl14 = player.get_abl(14)
        if abl14 > 0:
            mult = 1.0 + abl14 * 0.05
            for key in ["快C", "快V", "快A", "快B"]:
                if key in source:
                    source[key] = int(source[key] * mult)
        return source


    def _master_skill_check(self, target: Character) -> Dict[str, int]:
        source = {}
        player = self._get_player()
        abl14 = player.get_abl(14)
        if abl14 >= 3:
            source["恭顺"] = source.get("恭顺", 0) + abl14 * 20
        return source


    def _lost_virgin_check(self, target: Character) -> List[str]:
        msgs = []
        if not target.has_talent(0):
            return msgs
        name = target.name
        msgs.append(f"夺取了{name}的处女。")
        target.talent[0] = 0
        target.add_exp(20, 1)
        if target.has_talent(85):
            msgs.append(f"{name}将最珍贵的东西献给了你…")
        elif target.has_talent(76):
            msgs.append(f"{name}淫荡地扭动着腰…")
        elif target.get_mark(3) >= 2:
            msgs.append(f"{name}流着泪承受着疼痛…")
        else:
            msgs.append(f"{name}痛苦地叫了出来…")
        return msgs


    def _incest_sex_check(self, target: Character) -> Dict[str, int]:
        source = {}
        family_idx = self._search_family(target)
        if family_idx >= 0:
            source["情爱"] = source.get("情爱", 0) + 500
            source["屈辱"] = source.get("屈辱", 0) + 200
        return source


    def _ex_check_up(self, target: Character) -> Dict[str, int]:
        ex = {}
        palam0 = int(target.palam.get(0, 0)) if hasattr(target, 'palam') else 0
        palam1 = int(target.palam.get(1, 0)) if hasattr(target, 'palam') else 0
        palam2 = int(target.palam.get(2, 0)) if hasattr(target, 'palam') else 0
        palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
        if palam0 >= 10000:
            ex["C绝顶"] = 1
        if palam1 >= 10000:
            ex["V绝顶"] = 1
        if palam2 >= 10000:
            ex["A绝顶"] = 1
        if palam3 >= 10000:
            ex["B绝顶"] = 1
        if sum(1 for k in ["C绝顶", "V绝顶", "A绝顶", "B绝顶"] if k in ex) >= 3:
            ex["强绝顶"] = 1
        return ex


    def _target_ejac_check(self, target: Character) -> Dict[str, int]:
        result = {}
        if target.has_talent(121) or target.has_talent(122):
            base2 = int(target.base.get(2, 0)) if hasattr(target, 'base') else 0
            if base2 >= 10000:
                result["射精"] = 1
        return result


    def _target_milk_check(self, target: Character) -> Dict[str, int]:
        result = {}
        if target.has_talent(158):
            palam3 = int(target.palam.get(3, 0)) if hasattr(target, 'palam') else 0
            if palam3 >= 5000:
                result["喷乳"] = 1
        return result


    def _love_moist_check(self, target: Character) -> Dict[str, int]:
        up = {}
        palam4 = int(target.palam.get(4, 0)) if hasattr(target, 'palam') else 0
        if palam4 >= 3000:
            up["润滑"] = palam4 // 100
        return up

    # =====================================================================
    # COMF SOURCE 计算 (COM0-COM10)
    # =====================================================================

    def _juel_check(self, target=None):
        """宝珠检查 - 桥接ERB JUEL_CHECK"""
        return self.call_erb_function('JUEL_CHECK')


