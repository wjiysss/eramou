from __future__ import annotations
"""Module for ExComExtMixin - 扩展指令"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ExComExtMixin:
    """Mixin providing 扩展指令 methods for GameEngine"""

    def _excom(self, com_id: int) -> List[str]:
        """Extended command processing based on EXCOM.ERB.

        Handles EX-specific talent assignment and command extensions.
        """
        lines: List[str] = []
        chars = self.interpreter.vars.chars

        if com_id < 0:
            return lines

        # EX talent processing for characters
        # Based on CFLAG:6 personality codes
        for idx, char in enumerate(chars):
            cflag6 = char.cflag.get(6, 0)
            if cflag6 == 10031:
                char.talent[101] = 1  # 琼
            elif cflag6 == 10032:
                char.talent[102] = 1  # 普林希斯
            elif cflag6 == 10033:
                char.talent[103] = 1  # 嘉德
            elif cflag6 == 10035:
                char.talent[104] = 1  # 菲娅

            # Master gets 魔王 talent
            if idx == 0:
                char.talent[200] = 1

            # Special battle talents for CFLAG:6 == 10034
            if cflag6 == 10034:
                char.talent[801] = 1  # 无双
                char.talent[901] = 1  # 一人军团

        # Command-specific processing
        if com_id == 0:
            lines.append("扩展指令：无操作")
        elif com_id in self._EX_TALENT_NAMES:
            lines.append(f"扩展素质：{self._EX_TALENT_NAMES[com_id]}")

        return lines

    # =====================================================================
    # DUNGEON 凌辱系统
    # =====================================================================



    def _excom_process(self, com_id: int) -> List[str]:
        """扩展指令处理 - EXCOM.ERB"""
        output = []
        # EXCOM handles extended command processing
        # Currently a stub - specific command logic to be implemented
        return output

    # ------------------------------------------------------------------
    # SYSTEM_DEBUG_OUT - 调试输出
    # ------------------------------------------------------------------



