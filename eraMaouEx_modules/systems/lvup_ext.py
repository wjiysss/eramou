from __future__ import annotations
"""Module for LvupExtMixin - 升级系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class LvupExtMixin:
    """Mixin providing 升级系统 methods for GameEngine"""

    def _lvup_check(self, target: Character) -> Dict[str, Any]:
        """等级提升检查 - LVUP.ERB"""
        cflag9 = int(target.cflag.get(9, 0))
        local0 = cflag9 * 10 + 10
        level_ups = 0
        is_master = (target == self.characters.get(self.vars.flag.get(1, -1)))
        t220 = int(target.talent.get(220, 0))
        while True:
            if is_master:
                local = local0
            elif t220 == 1:
                local0_adj = local0 - 10
                local = local0_adj * 2 + 10
            else:
                local = local0
            exp80 = int(target.exp.get(80, 0))
            if exp80 >= local:
                target.exp[80] = exp80 - local
                # ST_UP: level up stat gains
                target.cflag[9] = int(target.cflag.get(9, 0)) + 1
                target.cflag[13] = int(target.cflag.get(13, 0)) + 1
                target.cflag[14] = int(target.cflag.get(14, 0)) + 1
                r = random.randint(0, 1)
                if r == 0:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + 1
                else:
                    target.cflag[14] = int(target.cflag.get(14, 0)) + 1
                day = int(self.vars.flag.get(0, 0))
                if day >= 100:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + random.randint(0, 2)
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 2)
                if int(target.talent.get(240, 0)) == 1:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + random.randint(0, 2)
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 2)
                if int(target.talent.get(248, 0)) == 1:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + random.randint(0, 1)
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 1)
                t314 = int(target.talent.get(314, 0))
                if t314 == 5:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + random.randint(0, 1)
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 1)
                if int(target.talent.get(314, 0)) == 11:
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 1)
                if int(target.talent.get(261, 0)) == 1:
                    target.cflag[14] = int(target.cflag.get(14, 0)) + random.randint(0, 1)
                if int(target.talent.get(262, 0)) == 1:
                    target.cflag[13] = int(target.cflag.get(13, 0)) + random.randint(0, 1)
                target.maxbase[0] = int(target.maxbase.get(0, 0)) + 10
                target.maxbase[1] = int(target.maxbase.get(1, 0)) + 10
                local0 = int(target.cflag.get(9, 0)) * 10 + 10
                level_ups += 1
            else:
                break
        result = {"level_ups": level_ups}
        if level_ups > 0:
            name = target.name if hasattr(target, 'name') else "角色"
            result["message"] = f"*{name}的等级提升为LV{int(target.cflag.get(9, 0))}*"
        if int(target.talent.get(291, 0)) and int(target.cflag.get(9, 0)) >= 30:
            result["remove_talent_291"] = True
            name = target.name if hasattr(target, 'name') else "角色"
            result["message2"] = f"{name}在战斗中越发成熟，终于成长成了真正的勇者……"
        return result

    # ------------------------------------------------------------------
    # ENTER_ENEMY - 敌人入场事件
    # ------------------------------------------------------------------


