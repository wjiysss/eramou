from __future__ import annotations
"""Module for PassoutExtMixin - 昏迷系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class PassoutExtMixin:
    """Mixin providing 昏迷系统 methods for GameEngine"""

    def _passout_bridge(self, target: Character) -> List[str]:
        """气绝桥接 - 对应 PASSOUT.ERB

        优先尝试ERB函数，然后回退到PassoutSystem模块。
        """
        # 1. 尝试ERB
        if "PASSOUT_CHECK" in self.interpreter.functions:
            try:
                output = self.interpreter.call_erb_function("PASSOUT_CHECK")
                if output:
                    return output
            except Exception:
                pass

        # 2. 回退到Python模块
        try:
            from eraMaouEx_modules.systems.passout import PassoutSystem
            ps = PassoutSystem(self)
            tflag = self.interpreter.vars.tflag if hasattr(self.interpreter.vars, 'tflag') else {}
            nowex = {}
            # 从角色数据构建nowex
            for key in range(20):
                val = target.nowex.get(key, 0) if hasattr(target, 'nowex') else 0
                if val > 0:
                    nowex[key] = val

            is_passout = ps.check_passout(target, tflag, nowex)
            if is_passout:
                return ["失神", f"{target.name or '她'}失去了意识。"]
            return []
        except Exception:
            pass

        return []

    def _passout_check(self):
        return self.call_erb_function('PASSOUT_CHECK')

    def _passout_message(self):
        return self.call_erb_function('PASSOUT_MESSAGE')

    def _passout_palam_check(self):
        return self.call_erb_function('PASSOUT_PALAM_CHECK')

    def _passout_palam_up(self):
        return self.call_erb_function('PASSOUT_PALAM_UP')

    def _passout_text(self):
        return self.call_erb_function('PASSOUT_TEXT')

    def _passout_outdoor(self):
        return self.call_erb_function('PASSOUT_OUTDOOR')


