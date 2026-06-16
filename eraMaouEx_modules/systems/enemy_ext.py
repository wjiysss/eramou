from __future__ import annotations
"""Module for EnemyExtMixin - 敌人数据"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EnemyExtMixin:
    """Mixin providing 敌人数据 methods for GameEngine"""

    def _can_spawn_enter_enemy(self) -> bool:
        charanum = len(self.interpreter.vars.chars)
        max_charanum = self._get_max_charanum()
        if charanum >= max_charanum:
            return False

        flag_82 = int(self.interpreter.vars.get_flag(82, 0))
        flag_87 = int(self.interpreter.vars.get_flag(87, 0))
        flag_89 = int(self.interpreter.vars.get_flag(89, 0))
        flag_91 = int(self.interpreter.vars.get_flag(91, 0))
        flag_92 = int(self.interpreter.vars.get_flag(92, 0))
        if flag_82 == 0 and charanum > 60:
            return False
        if flag_87 == 0 and flag_89 == 0 and flag_91 == 0 and charanum > 65:
            return False
        if (flag_87 * flag_89 == 0) and (flag_89 * flag_91 == 0) and (flag_91 * flag_87 == 0) and charanum > 70:
            return False
        if (flag_87 == 0 or flag_89 == 0 or flag_91 == 0) and charanum > 75:
            return False
        if flag_92 < 15 and charanum > 80:
            return False
        return True






    def _enter_enemy(self) -> List[str]:
        """敌人入场事件处理 - ENTER_ENEMY.ERB"""
        output = []
        charanum = len(self.characters)
        flag82 = int(self.vars.flag.get(82, 0))
        flag87 = int(self.vars.flag.get(87, 0))
        flag89 = int(self.vars.flag.get(89, 0))
        flag91 = int(self.vars.flag.get(91, 0))
        flag92 = int(self.vars.flag.get(92, 0))
        max_charanum = int(self.vars.flag.get(999, 100))
        if flag82 == 0 and charanum > 60:
            return output
        elif flag87 == 0 and flag89 == 0 and flag91 == 0 and charanum > 65:
            return output
        elif ((flag87 * flag89 == 0) and (flag89 * flag91 == 0) and (flag91 * flag87 == 0)) and charanum > 70:
            return output
        elif (flag87 == 0 or flag89 == 0 or flag91 == 0) and charanum > 75:
            return output
        elif flag92 < 15 and charanum > 80:
            return output
        elif charanum >= max_charanum:
            return output
        output.append("*****************************************")
        output.append("新的勇者开始了地下城的攻略！")
        output.append("*****************************************")
        return output

    # ------------------------------------------------------------------
    # EVENT1 - 一般事件
    # ------------------------------------------------------------------



    def _enter_enemy_character(self) -> List[str]:
        """生成一个新的勇者角色"""
        messages: List[str] = []
        if not self._can_spawn_enter_enemy():
            return messages

        template_id = random.randint(1, 16)
        existing = self._find_character_by_template_id(template_id)
        if existing is not None and not self._get_flag_bit(5, 32):
            messages.append("出于对魔王的恐惧，勇者没有出现。")
            return messages

        new_char = self._create_enemy_character_from_template(template_id)
        if new_char is None:
            return messages

        self.interpreter.vars.chars.append(new_char)
        new_char.cflag[1] = 2  # 侵攻中

        if self._get_flag_bit(5, 1):
            flag_60 = int(self.interpreter.vars.get_flag(60, 0))
            self.interpreter.vars.set_flag(60, flag_60 + 1)
            messages.append(f"勇者基础等级校正后现在是等级{flag_60 + 1}")

        messages.extend([
            "*****************************************",
            f"{new_char.name} 开始了地下城的攻略！",
            "*****************************************"
        ])
        
        return messages



