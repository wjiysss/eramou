from __future__ import annotations
"""Module for SellFollowupMixin - 出售后续剧情"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SellFollowupMixin:
    """Mixin providing 出售后续剧情 methods for GameEngine"""

    def _build_lewd_black_market_context(self, target: Character) -> Dict[str, Any]:
        return {
            "busty": self._is_sell_busty_target(target),
            "warrior_like": self._has_sell_job_talent(target, 200, 203),
            "knight_ninja_like": self._has_sell_job_talent(target, 205, 207),
            "priest_like": self._has_sell_job_talent(target, 202, 206),
            "meat_toilet": bool(target.talent.get(204, 0)),
            "vagina_sense": int(target.abl.get(2, 0)),
            "level": int(target.cflag.get(9, 0)),
            "thief_like": bool(target.talent.get(203, 0)),
        }






    def _build_lewd_black_market_party_context(self, target: Character) -> Dict[str, Any]:
        context = self._build_lewd_black_market_context(target)
        context["is_demon"] = int(target.talent.get(314, 0)) == 9
        return context






    def _build_normal_end_lines(self) -> List[str]:
        return [
            "-" * 48,
            "自从魔王被解开封印已经过了整整500天。",
            "尽管各界源源不断地派遣勇者讨伐魔王，",
            "但都要么成为了魔王的收藏品，",
            "要么被倒卖到大陆各个龌龊的角落，",
            "要么成为了魔王力量的一部分，帮助魔王为祸人间。",
            "",
            "这块大陆的人们渐渐也习惯于魔王地下城的存在，想要寻找财富或者冒险……",
            "或者……期待着女性最本能的渴望……",
            "各种心思的女孩子们，依然在源源不断地走进这个魔窟。",
            "……",
            "……",
            "大概，已经不会有尽头了吧。",
            "达成了【Normal End】。",
        ]






    def _build_normal_shop_groups(self) -> List[Dict[str, Union[str, List[int]]]]:
        groups = self._build_shop_groups()
        return [group for group in groups if str(group["title"]) != "陷阱"]





