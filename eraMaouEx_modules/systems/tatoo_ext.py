from __future__ import annotations
"""Module for TatooExtMixin - 纹身系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class TatooExtMixin:
    """Mixin providing 纹身系统 methods for GameEngine"""

    def _tatoo_bridge(self, target: Character) -> List[str]:
        """纹身桥接 - 对应 TATOO.ERB

        优先尝试ERB函数，然后回退到TatooSystem模块。
        """
        # 1. 尝试ERB
        if "GET_TATOO" in self.interpreter.functions:
            try:
                output = self.interpreter.call_erb_function("GET_TATOO")
                if output:
                    return output
            except Exception:
                pass

        # 2. 回退到Python模块
        try:
            from eraMaouEx_modules.systems.tatoo import TatooSystem
            ts = TatooSystem(self)
            info = ts.get_tatoo_info(target)
            tatoo_names = {0: "无", 1: "主人的印记", 2: "淫纹", 3: "屈辱纹身", 4: "信息纹身"}
            tatoo_type = info.get('type', 0)
            tatoo_text = info.get('text', '')
            name = tatoo_names.get(tatoo_type, f"纹身{tatoo_type}")
            if tatoo_text:
                return [f"纹身: {name} - {tatoo_text}"]
            elif tatoo_type > 0:
                return [f"纹身: {name}"]
            else:
                return ["没有纹身"]
        except Exception:
            pass

        return ["纹身信息获取失败"]


