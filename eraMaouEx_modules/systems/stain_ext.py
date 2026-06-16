from __future__ import annotations
"""Module for StainExtMixin - 污垢系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class StainExtMixin:
    """Mixin providing 污垢系统 methods for GameEngine"""

    def _apply_finger_stain_transfer(self, target: Character, player: Optional[Character], target_stain_idx: int):
        if player is None:
            return
        target.stain[target_stain_idx] = target.stain.get(target_stain_idx, 0) | player.stain.get(1, 0)
        player.stain[1] = player.stain.get(1, 0) | target.stain.get(target_stain_idx, 0)






    def _apply_mouth_stain_transfer(self, target: Character, player: Optional[Character]):
        if player is None:
            return
        target.stain[0] = target.stain.get(0, 0) | player.stain.get(0, 0)
        player.stain[0] = player.stain.get(0, 0) | target.stain.get(0, 0)






    def _apply_self_stain_transfer(self, target: Character):
        target.stain[1] = target.stain.get(1, 0) | target.stain.get(5, 0)
        target.stain[5] = target.stain.get(5, 0) | target.stain.get(1, 0)
        target.stain[1] = target.stain.get(1, 0) | target.stain.get(3, 0)
        target.stain[3] = target.stain.get(3, 0) | target.stain.get(1, 0)






    def _apply_standing_rear_stain_transfer(self, target: Character, player: Character):
        target.stain[0] = target.stain.get(0, 0) | player.stain.get(0, 0)
        player.stain[0] = player.stain.get(0, 0) | target.stain.get(0, 0)
        target.stain[3] = target.stain.get(3, 0) | player.stain.get(1, 0)
        player.stain[1] = player.stain.get(1, 0) | target.stain.get(3, 0)






    def _mouth_stain_score(self, owner: Optional[Character]) -> int:
        if owner is None:
            return 0

        score = 0
        mouth_stain = owner.stain.get(0, 0)
        if mouth_stain & 1:
            score += 1
        if mouth_stain & 4:
            score += 3
        if mouth_stain & 8:
            score += 7
        if mouth_stain & 16:
            score += 1
        if mouth_stain & 32:
            score += 3
        return score





