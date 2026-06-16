from __future__ import annotations
"""Module for TemptationExtMixin - 诱惑系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class TemptationExtMixin:
    """Mixin providing 诱惑系统 methods for GameEngine"""

    def _add_temptation_gain(self, target: Character, gain: int) -> int:
        target.cflag[2] = int(target.cflag.get(2, 0)) + gain
        return gain






    def _apply_temptation_base_ratio_bonus(self, target: Character, success: int) -> int:
        for base_idx in (0, 1):
            current = max(0, int(target.base.get(base_idx, 0)))
            maximum = max(1, int(target.maxbase.get(base_idx, 0)))
            ratio = current * 100 // maximum
            if ratio >= 75:
                continue
            if ratio >= 50:
                success = success * 3 // 2
            elif ratio >= 25:
                success *= 3
            elif ratio >= 10:
                success = success * 9 // 2
            else:
                success *= 6
        return success






    def _apply_temptation_heal(self, target: Character, attr: int, power: int) -> int:
        current = int(target.base.get(attr, 0))
        maximum = int(target.maxbase.get(attr, 0))
        gain = self._get_temptation_heal_gain(current, maximum)
        target.base[attr] = min(maximum, current + power * 50)
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_0(self, target: Character) -> int:
        print(f"*梦魔的快乐袭击了{target.name}！*")
        gain = 10 * (1 + sum(int(target.abl.get(idx, 0)) for idx in range(4)))
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_1(self, target: Character) -> int:
        print(f"*自己隐藏着的兽欲袭击了{target.name}！*")
        gain = 15 * (1 + int(target.abl.get(10, 0)) + int(target.abl.get(11, 0)))
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_2(self, target: Character) -> int:
        print(f"*自己心中的黑暗面袭击了{target.name}！*")
        mark_bonus = 1 + int(target.mark.get(0, 0)) + int(target.mark.get(1, 0)) + int(target.mark.get(2, 0))
        gain = 10 * mark_bonus // max(1, 1 + int(target.mark.get(3, 0)))
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_3(self, target: Character) -> int:
        print(f"*魔王的甜蜜诱惑袭击了{target.name}！*")
        gain = 40
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_4(self, target: Character) -> int:
        print("*可以和你平分这个世界哦……*")
        gain = 50
        return self._add_temptation_gain(target, gain)






    def _apply_temptation_trial_choice_5(self, target: Character, power: int) -> int:
        print(f"*魔界的波动，治愈了{target.name}…*")
        return self._apply_temptation_heal(target, 0, power)






    def _apply_temptation_trial_choice_6(self, target: Character, power: int) -> int:
        print(f"*魔界的波动，治愈了{target.name}的心灵…*")
        return self._apply_temptation_heal(target, 1, power)






    def _apply_temptation_trial_effect(self, target: Character) -> int:
        power = self._get_temptation_power()
        choice = random.randrange(9)
        result = self._resolve_temptation_trial_choice(target, choice, power)
        if result is not None:
            return result
        print("诱惑被切断了！")
        return 0






    def _get_temptation_heal_gain(self, current: int, maximum: int) -> int:
        ratio = max(0, current) * 100 // max(1, maximum)
        if ratio >= 75:
            return 5
        if ratio >= 50:
            return 25
        if ratio >= 25:
            return 50
        if ratio >= 10:
            return 75
        return 200






    def _get_temptation_power(self) -> int:
        player = self._get_player()
        if player is None:
            return 1
        return max(1, int(player.cflag.get(9, 0)))






    def _is_temptation_try_successful(self, target: Character, success: int, failure: int) -> bool:
        if target.talent.get(73, 0) or target.talent.get(76, 0) or target.talent.get(85, 0) or target.talent.get(204, 0):
            return True

        ring_a = int(target.cflag.get(551, -1)) % 1000
        ring_b = int(target.cflag.get(552, -1)) % 1000
        if random.randrange(20) < 5 and (ring_a == 20 or ring_b == 20):
            return True
        if random.randrange(10) < 5 and (ring_a == 18 or ring_b == 18):
            return False

        return random.randrange(max(1, success + failure)) < success






    def _prepare_temptation_base_success(self, target: Character, player_level: int) -> int:
        success = 99 + player_level
        success += int(self.interpreter.vars.get_flag(30, 0))
        success += int(self.interpreter.vars.get_flag(31, 0))
        success += int(self.interpreter.vars.get_flag(32, 0))
        success += (
            int(target.exp.get(2, 0))
            + int(target.exp.get(5, 0))
            + int(target.exp.get(20, 0))
            + int(target.exp.get(55, 0))
            + int(target.exp.get(56, 0))
            + int(target.exp.get(57, 0))
            + int(target.exp.get(74, 0))
        ) // 3
        success += 5 * sum(int(target.abl.get(idx, 0)) for idx in range(4))
        success += 10 * (int(target.abl.get(10, 0)) + int(target.abl.get(11, 0)))
        return success






    def _prepare_temptation_success_weights(self, target: Character) -> tuple[int, int]:
        player = self._get_player()
        player_level = int(player.cflag.get(9, 0)) if player is not None else 1
        success = self._prepare_temptation_base_success(target, player_level)
        success = self._apply_temptation_base_ratio_bonus(target, success)

        failure = max(0, 50 + int(target.cflag.get(9, 0)) + int(target.cflag.get(151, 0)))
        failure *= 1 + int(target.mark.get(3, 0))
        seal_power = 1 + int(target.mark.get(0, 0)) + int(target.mark.get(1, 0)) + int(target.mark.get(2, 0))
        failure //= max(1, seal_power * seal_power)
        return max(1, success), max(0, failure)






    def _resolve_temptation_trial_choice(self, target: Character, choice: int, power: int) -> Optional[int]:
        if choice == 0:
            return self._apply_temptation_trial_choice_0(target)
        if choice == 1:
            return self._apply_temptation_trial_choice_1(target)
        if choice == 2:
            return self._apply_temptation_trial_choice_2(target)
        if choice == 3:
            return self._apply_temptation_trial_choice_3(target)
        if choice == 4:
            return self._apply_temptation_trial_choice_4(target)
        if choice == 5:
            return self._apply_temptation_trial_choice_5(target, power)
        if choice == 6:
            return self._apply_temptation_trial_choice_6(target, power)
        return None





