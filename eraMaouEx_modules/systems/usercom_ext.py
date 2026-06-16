from __future__ import annotations
"""Module for UserComExtMixin - 用户指令"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class UserComExtMixin:
    """Mixin providing 用户指令 methods for GameEngine"""

    def _usercom_bridge(self, com_id: int) -> List[str]:
        """用户指令桥接 - 对应 USERCOM.ERB

        优先尝试ERB函数，然后回退到UserComSystem模块。
        """
        # 1. 尝试ERB
        if "SHOW_USERCOM" in self.interpreter.functions:
            try:
                output = self.interpreter.call_erb_function("SHOW_USERCOM")
                if output:
                    return output
            except Exception:
                pass

        # 2. 回退到Python模块
        try:
            from eraMaouEx_modules.systems.usercom import UserComSystem
            ucs = UserComSystem(self)
            result = ucs.usercom(com_id)
            msgs = []
            if result.get('message'):
                msgs.append(result['message'])
            if result.get('action') == 'end_train':
                msgs.append("结束调教")
            return msgs if msgs else [f"执行指令{com_id}"]
        except Exception:
            return [f"执行指令{com_id}"]


