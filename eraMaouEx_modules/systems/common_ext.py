from __future__ import annotations
"""Module for CommonExtMixin - 通用功能"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CommonExtMixin:
    """Mixin providing 通用功能 methods for GameEngine"""

    def _get_common_order_score(self, target: Character, player: Optional[Character]) -> int:
        score = self._get_common_order_score_base(target)
        score += self._get_common_order_score_pair_bonus(target, player)
        score += self._get_common_order_score_mark_bonus(target)
        score += self._get_common_order_score_palam_bonus(target)
        score += self._get_common_order_score_talent_bonus(target)
        score += self._get_common_order_score_player_bonus(player)
        return score






    def _get_common_order_score_base(self, target: Character) -> int:
        return target.abl.get(10, 0) * 4 + target.abl.get(21, 0) * 2






    def _get_common_order_score_mark_bonus(self, target: Character) -> int:
        score = target.mark.get(0, 0) * 5
        mark_scale = 4 if target.talent.get(15, 0) else 1 if target.talent.get(17, 0) else 2
        score += target.mark.get(2, 0) * 3 * mark_scale
        score -= target.mark.get(3, 0) * 2 * mark_scale
        return score






    def _get_common_order_score_pair_bonus(self, target: Character, player: Optional[Character]) -> int:
        score = 0
        if self._is_same_sex_pair(player, target):
            score += target.abl.get(22, 0) * 3
            score += target.abl.get(33, 0) * 3
            if target.talent.get(81, 0):
                score += 10
            if target.talent.get(23, 0):
                score += 7
            if target.talent.get(24, 0):
                score -= 13
        else:
            if target.talent.get(23, 0):
                score += 5
            if target.talent.get(24, 0):
                score -= 10
        return score






    def _get_common_order_score_palam_bonus(self, target: Character) -> int:
        return self._get_palam_level(target.palam.get(4, 0)) * 3 + self._get_palam_level(target.palam.get(10, 0)) * 3






    def _get_common_order_score_player_bonus(self, player: Optional[Character]) -> int:
        if player is None:
            return 0
        score = 0
        if player.talent.get(91, 0):
            score += 6
        if player.talent.get(92, 0):
            score += 6
        if player.talent.get(93, 0):
            score += 6
        if player.talent.get(83, 0):
            score += 3
        if player.talent.get(118, 0):
            score += 1
        return score






    def _get_common_order_score_talent_bonus(self, target: Character) -> int:
        score = 0
        if target.talent.get(11, 0):
            score -= 5
        if target.talent.get(12, 0):
            score -= 5
        if target.talent.get(13, 0):
            score += 5
        if target.talent.get(15, 0):
            score -= 15
        if target.talent.get(17, 0):
            score += 5
        if target.talent.get(28, 0):
            score += 2
        if target.talent.get(32, 0):
            score -= 10
        if target.talent.get(34, 0):
            score -= 10
        if target.talent.get(37, 0):
            score += 12
        if target.talent.get(73, 0):
            score += 10
        if target.talent.get(76, 0):
            score += 5
        if target.talent.get(86, 0):
            score += 8
        return score





