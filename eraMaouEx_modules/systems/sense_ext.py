from __future__ import annotations
"""Module for SenseExtMixin - 感官系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SenseExtMixin:
    """Mixin providing 感官系统 methods for GameEngine"""

    def _apply_sense_lock_scaling(self, base_cost: int, exp_cost: int, level: int, lock_count: int, base_denominator: int, exp_denominator: int) -> tuple[int, int]:
        if level > 5 and level <= 10 and lock_count > 0:
            return (
                base_cost * (base_denominator - lock_count) // base_denominator,
                exp_cost * (exp_denominator - lock_count) // exp_denominator,
            )
        if level <= 15 and lock_count > 1:
            return (
                base_cost * (base_denominator + 1 - lock_count) // base_denominator,
                exp_cost * (exp_denominator + 1 - lock_count) // exp_denominator,
            )
        if level <= 20 and lock_count > 2:
            return (
                base_cost * (base_denominator + 2 - lock_count) // base_denominator,
                exp_cost * (exp_denominator + 2 - lock_count) // exp_denominator,
            )
        return base_cost, exp_cost






    def _apply_sense_special_talent_multiplier(self, target: Character, base_cost: int, exp_cost: int, level: int) -> tuple[int, int]:
        if target.talent.get(27, 0):
            if level == 4:
                return self._scale_sense_costs(base_cost, exp_cost, 200, 200)
            if level == 5:
                return self._scale_sense_costs(base_cost, exp_cost, 250, 250)
            if level >= 6:
                return self._scale_sense_costs(base_cost, exp_cost, 300, 300)
        return base_cost, exp_cost






    def _get_sense_lock_count(self, target: Character, ability_id: int) -> int:
        lock_map = {
            0: [103, 105, 107],
            1: [101, 103, 105],
            2: [101, 105, 107],
            3: [101, 103, 107],
        }
        return sum(1 for talent_id in lock_map.get(ability_id, []) if target.talent.get(talent_id, 0) & 2)






    def _get_sense_upgrade_base_cost(self, level: int) -> int:
        if level == 0:
            return 1
        if level == 1:
            return 20
        if level == 2:
            return 400
        if level == 3:
            return 8000
        if level == 4:
            return 20000
        if level == 5:
            return 40000
        if level == 6:
            return 60000
        if level == 7:
            return 90000
        if level == 8:
            return 120000
        if level == 9:
            return 180000
        return self._get_sense_upgrade_progressive_cost(
            level,
            {9: (180000, 125), 14: (362000, 120), 19: (583000, 115)},
        )






    def _get_sense_upgrade_costs(self, target: Character, ability_id: int, level: int) -> Dict[int, int]:
        base_cost = self._get_sense_upgrade_base_cost(level)
        exp_cost = self._get_sense_upgrade_exp_cost(level)
        lock_count = self._get_sense_lock_count(target, ability_id)
        base_cost, exp_cost = self._apply_sense_special_talent_multiplier(target, base_cost, exp_cost, level)

        if ability_id == 0:
            return self._get_sense_upgrade_costs_for_clit(target, level, base_cost, lock_count)

        if ability_id == 1:
            return self._get_sense_upgrade_costs_for_breast(target, level, base_cost, lock_count)

        if ability_id == 2:
            return self._get_sense_upgrade_costs_for_pussy(target, level, base_cost, exp_cost, lock_count)

        return self._get_sense_upgrade_costs_for_ass(target, level, base_cost, exp_cost, lock_count)






    def _get_sense_upgrade_costs_for_ass(self, target: Character, level: int, base_cost: int, exp_cost: int, lock_count: int) -> Dict[int, int]:
        if target.talent.get(105, 0):
            base_cost = base_cost * 120 // 100
            exp_cost = exp_cost * 110 // 100
        base_cost, exp_cost = self._apply_sense_lock_scaling(base_cost, exp_cost, level, lock_count, 15, 20)
        if target.talent.get(76, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        if target.talent.get(77, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        if target.talent.get(106, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        return {2: max(1, base_cost), 1: max(1, exp_cost)}






    def _get_sense_upgrade_costs_for_breast(self, target: Character, level: int, base_cost: int, lock_count: int) -> Dict[int, int]:
        if target.talent.get(107, 0):
            base_cost = base_cost * 120 // 100
        if target.talent.get(110, 0):
            base_cost = base_cost * 110 // 100
        if target.talent.get(114, 0):
            base_cost = base_cost * 120 // 100
        if target.talent.get(119, 0):
            base_cost = base_cost * 130 // 100
        if target.talent.get(108, 0):
            base_cost = base_cost * 80 // 100
        base_cost, _ = self._apply_sense_lock_scaling(base_cost, 0, level, lock_count, 15, 20)
        if target.talent.get(76, 0):
            base_cost = base_cost * 80 // 100
        if target.talent.get(78, 0):
            base_cost = base_cost * 80 // 100
        if target.talent.get(109, 0):
            base_cost = base_cost * 80 // 100
        if target.talent.get(116, 0):
            base_cost = base_cost * 65 // 100
        return {14: max(1, base_cost)}






    def _get_sense_upgrade_costs_for_clit(self, target: Character, level: int, base_cost: int, lock_count: int) -> Dict[int, int]:
        if target.talent.get(101, 0):
            base_cost = base_cost * 120 // 100
        if target.talent.get(102, 0):
            base_cost = base_cost * 80 // 100
        base_cost, _ = self._apply_sense_lock_scaling(base_cost, 0, level, lock_count, 15, 20)
        if target.talent.get(76, 0):
            base_cost = base_cost * 80 // 100
        if target.talent.get(74, 0):
            base_cost = base_cost * 80 // 100
        return {0: max(1, base_cost)}






    def _get_sense_upgrade_costs_for_pussy(self, target: Character, level: int, base_cost: int, exp_cost: int, lock_count: int) -> Dict[int, int]:
        if target.talent.get(103, 0):
            base_cost = base_cost * 120 // 100
            exp_cost = exp_cost * 110 // 100
        base_cost, exp_cost = self._apply_sense_lock_scaling(base_cost, exp_cost, level, lock_count, 15, 20)
        if target.talent.get(76, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        if target.talent.get(75, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        if target.talent.get(104, 0):
            base_cost = base_cost * 80 // 100
            exp_cost = exp_cost * 80 // 100
        return {1: max(1, base_cost), 0: max(1, exp_cost)}






    def _get_sense_upgrade_exp_cost(self, level: int) -> int:
        if level == 0:
            return 2
        if level == 1:
            return 10
        if level == 2:
            return 30
        if level == 3:
            return 75
        if level == 4:
            return 150
        if level == 5:
            return 180
        if level == 6:
            return 250
        if level == 7:
            return 350
        if level == 8:
            return 500
        if level == 9:
            return 600
        return self._get_sense_upgrade_progressive_cost(
            level,
            {9: (600, 115), 14: (966, 120), 19: (1942, 125)},
        )






    def _get_sense_upgrade_progressive_cost(
        self,
        level: int,
        base_values: Dict[int, tuple[int, int]],
    ) -> int:
        for base_level in sorted(base_values.keys(), reverse=True):
            if level >= base_level:
                cost, growth_percent = base_values[base_level]
                if level == base_level:
                    return cost
                for _ in range(level - base_level):
                    cost = cost * growth_percent // 100
                return cost
        first_key = min(base_values.keys())
        return base_values[first_key][0]






    def _progressive_sense_cost(self, level: int, base_values: Dict[int, int], growth_ranges: List[tuple[int, int, int]], default_cost: int) -> int:
        if level in base_values:
            return base_values[level]
        for upper, factor, offset in growth_ranges:
            if level < upper:
                cost = default_cost
                start_level = max(max(base_values), upper - 1)
                for _ in range(level - start_level):
                    cost = cost * factor // 100
                return cost + offset
        return default_cost






    def _scale_sense_costs(self, base_cost: int, exp_cost: int, base_percent: int = 100, exp_percent: int = 100) -> tuple[int, int]:
        return base_cost * base_percent // 100, exp_cost * exp_percent // 100





