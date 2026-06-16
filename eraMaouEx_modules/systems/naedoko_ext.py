from __future__ import annotations
"""Module for NaedokoExtMixin - Naedoko系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class NaedokoExtMixin:
    """Mixin providing Naedoko系统 methods for GameEngine"""

    def _naedoko_bridge(self, target: Character) -> List[str]:
        """苗床桥接 - 对应 NAEDOKO.ERB

        优先尝试ERB函数，然后回退到NaedokoSystem模块。
        """
        # 1. 尝试ERB
        if "NAEDOKO" in self.interpreter.functions:
            try:
                output = self.interpreter.call_erb_function("NAEDOKO")
                if output:
                    return output
            except Exception:
                pass

        # 2. 回退到Python模块
        try:
            from eraMaouEx_modules.systems.naedoko import NaedokoSystem
            ns = NaedokoSystem(self)
            # 查找角色索引
            chars = self.interpreter.vars.chars
            char_idx = -1
            for i, c in enumerate(chars):
                if c is target:
                    char_idx = i
                    break
            if char_idx >= 0:
                result = ns.convert_to_naedoko(char_idx)
                return [result.get('message', '')]
        except Exception:
            pass

        name = target.name or "她"
        return [f"{name}的苗床处理完成"]

    def _naedoko(self):
        return self.call_erb_function('NAEDOKO')

    def _naedoko_man(self):
        return self.call_erb_function('NAEDOKO_MAN')

    def _naedoko_not_v(self):
        return self.call_erb_function('NAEDOKO_NOT_V')


