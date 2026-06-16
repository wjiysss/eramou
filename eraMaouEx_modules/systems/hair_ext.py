from __future__ import annotations
"""Module for HairExtMixin - 发型系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class HairExtMixin:
    """Mixin providing 发型系统 methods for GameEngine"""

    def _get_hair_color_name(self, target) -> str:
        """获取发色名称 (TALENT:300)"""
        v = int(target.talent.get(300, 0))
        return self._HAIR_COLOR_NAMES.get(v, "黑发")






    def _get_hair_cut_name(self, target) -> str:
        """获取头发修剪方式名称 (TALENT:303)"""
        v = int(target.talent.get(303, 0))
        return self._HAIR_CUT_NAMES.get(v, "ERROR")






    def _get_hair_length_name(self, target) -> str:
        """获取头发长度名称 (TALENT:302)"""
        v = int(target.talent.get(302, 0))
        if 1 <= v <= 100:
            return "短"
        elif 101 <= v <= 200:
            return "半长"
        elif 201 <= v <= 300:
            return "长"
        return "ERROR"






    def _get_hair_state_name(self, target) -> str:
        """获取头发状态名称 (TALENT:301)"""
        v = int(target.talent.get(301, 0))
        return self._HAIR_STATE_NAMES.get(v, "ERROR")






    def _get_hair_style_name(self, target) -> str:
        """获取发型名称 (TALENT:304)"""
        v = int(target.talent.get(304, 0))
        return self._HAIR_STYLE_NAMES.get(v, "ERROR")





