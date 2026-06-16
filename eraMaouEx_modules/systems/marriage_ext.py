from __future__ import annotations
"""Module for MarriageExtMixin - 婚姻系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class MarriageExtMixin:
    """Mixin providing 婚姻系统 methods for GameEngine"""

    def _apply_marriage_daily_intimacy(self, idx: int, char: Character) -> List[str]:
        marriage_state = int(char.cflag.get(601, 0))
        days = int(char.cflag.get(602, 0))
        roll = random.randint(1, 6)
        char.cflag[107] = 0
        char.cflag[112] = 0
        return self._apply_marriage_daily_intimacy_state(idx, char, marriage_state, days, roll)






    def _apply_marriage_daily_intimacy_state(self, idx: int, char: Character, marriage_state: int, days: int, roll: int) -> List[str]:
        if marriage_state == 902:
            return self._apply_dungeon_town_lover_visit(idx, char)
        if marriage_state == 901:
            return self._apply_marriage_daily_intimacy_state_901(char, roll)
        if marriage_state == 900:
            return self._apply_marriage_daily_intimacy_state_900(char, days, roll)
        if marriage_state < 900:
            return self._apply_marriage_daily_intimacy_state_below_900(char, days, roll)
        return [f"{char.name} 和伴侣一起平淡地过着婚后生活。"]






    def _apply_marriage_daily_intimacy_state_900(self, char: Character, days: int, roll: int) -> List[str]:
        messages: List[str] = []
        special_case = bool(
            char.talent.get(273, 0)
            or (int(char.cflag.get(42, 0)) == 79 and bool(int(char.cflag.get(40, 0)) & 64) and int(self.interpreter.vars.get_flag(37, 0)) != 0)
            or char.talent.get(122, 0)
        )

        if int(char.abl.get(39, 0)) <= 1 or days < 50:
            if special_case:
                messages.append(f"{char.name} 和野狗在日常里平静地相处着。")
                char.exp[1] = int(char.exp.get(1, 0)) + roll
                char.exp[56] = int(char.exp.get(56, 0)) + roll
            else:
                messages.append(f"{char.name} 和野狗一起生活，关系慢慢发生了变化。")
                char.exp[0] = int(char.exp.get(0, 0)) + roll
                char.exp[56] = int(char.exp.get(56, 0)) + roll
                char.cflag[106] = int(char.cflag.get(106, 0)) + roll
            return messages

        if char.talent.get(136, 0):
            messages.append(f"{char.name} 和野狗交配了一整天。")
            if special_case:
                char.exp[1] = int(char.exp.get(1, 0)) + roll
                char.exp[56] = int(char.exp.get(56, 0)) + roll
                char.juel[2] = int(char.juel.get(2, 0)) + (int(char.cflag.get(602, 0)) * 10 * roll + 10)
                char.exp[2] = int(char.exp.get(2, 0)) + roll
            else:
                char.exp[0] = int(char.exp.get(0, 0)) + roll
                char.exp[56] = int(char.exp.get(56, 0)) + roll
                char.cflag[107] = roll
                char.cflag[106] = int(char.cflag.get(106, 0)) + roll
                char.juel[1] = int(char.juel.get(1, 0)) + (int(char.cflag.get(602, 0)) * 10 * roll + 10)
                char.exp[2] = int(char.exp.get(2, 0)) + roll
            return messages

        messages.append(f"{char.name} 和野狗一起住在狗屋里。")
        char.juel[6] = int(char.juel.get(6, 0)) + (int(char.cflag.get(602, 0)) * 2 * roll + 2)
        return messages






    def _apply_marriage_daily_intimacy_state_901(self, char: Character, roll: int) -> List[str]:
        messages: List[str] = []
        if char.talent.get(85, 0):
            messages.append(f"{char.name} 常常柔情似水地凝望着你，在身边努力做个好妃子。")
            char.exp[0] = int(char.exp.get(0, 0)) + roll
            char.exp[1] = int(char.exp.get(1, 0)) + roll
            char.exp[5] = int(char.exp.get(5, 0)) + roll
            char.exp[20] = int(char.exp.get(20, 0)) + max(1, roll // 2)
            char.exp[10] = int(char.exp.get(10, 0)) + roll
            char.exp[11] = int(char.exp.get(11, 0)) + roll
            return messages
        if char.talent.get(76, 0):
            messages.append(f"{char.name} 在你身边露出淫媚的笑容，心里盘算着新的欢愉。")
            gain = max(1, roll // 2)
            char.exp[0] = int(char.exp.get(0, 0)) + gain
            char.exp[1] = int(char.exp.get(1, 0)) + gain
            char.exp[5] = int(char.exp.get(5, 0)) + gain
            char.exp[20] = int(char.exp.get(20, 0)) + gain
            char.exp[56] = int(char.exp.get(56, 0)) + gain
            char.exp[74] = int(char.exp.get(74, 0)) + gain
            return messages
        if int(char.abl.get(10, 0)) >= 3:
            messages.append(f"{char.name} 勉为其难地陪侍在你身边，作为勇者陷落的象征继续生活着。")
            char.juel[4] = int(char.juel.get(4, 0)) + (int(char.abl.get(11, 0)) * roll * 8 + int(char.abl.get(10, 0)) * roll * 8 + 8)
            char.juel[5] = int(char.juel.get(5, 0)) + (int(char.abl.get(11, 0)) * roll * 8 + int(char.abl.get(10, 0)) * roll * 8 + 8)
            return messages
        messages.append(f"{char.name} 被束缚在婚姻生活中，半是放弃地消磨着一天。")
        char.juel[6] = int(char.juel.get(6, 0)) + (int(char.abl.get(11, 0)) * roll * 2 + int(char.abl.get(10, 0)) * roll * 2 + 2)
        return messages






    def _apply_marriage_daily_intimacy_state_below_900(self, char: Character, days: int, roll: int) -> List[str]:
        messages: List[str] = []
        messages.append(f"{char.name} 和伴侣一起度过了婚后的日常生活。")
        if days > 30:
            char.exp[0] = int(char.exp.get(0, 0)) + roll
            char.exp[20] = int(char.exp.get(20, 0)) + roll
            char.cflag[107] = roll
        else:
            char.exp[22] = int(char.exp.get(22, 0)) + roll
            char.exp[20] = int(char.exp.get(20, 0)) + roll
        return messages






    def _apply_marriage_daily_lactation_income(self, char: Character) -> List[str]:
        if not char.talent.get(130, 0):
            return []
        income = random.randint(1, 5) * 100
        self._add_global_money(income)
        return [f"{char.name} 多余的奶水被卖掉了，获得了 {income} pts。"]






    def _apply_marriage_daily_pregnancy_pause(self, char: Character) -> List[str]:
        if char.talent.get(153, 0):
            return [f"{char.name} 和伴侣一起期待着孩子的出生。"]
        if char.talent.get(154, 0):
            return [f"{char.name} 和伴侣一起期待着孩子的成长。"]
        return []






    def _get_marriage_slave_candidates(self, idx: int, char: Character) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for other_idx, other in enumerate(self.interpreter.vars.chars):
            if other_idx <= 0 or other is char:
                continue
            if int(other.cflag.get(1, 0)) != 0:
                continue
            if int(other.cflag.get(601, 0)) != 0:
                continue
            if int(other.cflag.get(0, 0)) == 0:
                continue
            candidates.append((other_idx, other))
        return candidates






    def _lovers_check(self, target: Character) -> List[str]:
        """Check/update lover status based on LOVERS.ERB logic."""
        lines: List[str] = []
        name = target.name or "她"

        # CFLAG:606 = assigned lover ID, CFLAG:607 = love level
        lover_id = target.cflag.get(606, 0)
        love_lv = target.cflag.get(607, 0)
        marriage = target.cflag.get(601, 0)

        if lover_id <= 0:
            lines.append(f"{name}目前没有恋人。")
            return lines

        lover_name = self._LOVER_NAME_MAP.get(lover_id, f"未知人物({lover_id})")

        if marriage == 902:
            lines.append(f"{name}已经和{lover_name}结婚了。")
        else:
            lines.append(f"{name}正在和{lover_name}交往中。")

        # Love level display
        if love_lv >= 500:
            lines.append(f"爱情度：深爱（{love_lv}）")
        elif love_lv >= 200:
            lines.append(f"爱情度：热恋（{love_lv}）")
        elif love_lv >= 50:
            lines.append(f"爱情度：好感（{love_lv}）")
        elif love_lv > 0:
            lines.append(f"爱情度：初识（{love_lv}）")
        else:
            lines.append(f"爱情度：{love_lv}")

        return lines

    # ------------------------------------------------------------------
    # MAGIC (魔法系统)
    # ------------------------------------------------------------------

    _SPELL_NAMES: Dict[int, str] = {
        1: "瞬间移动", 2: "催眠术", 3: "能量弹", 4: "能量吸收",
        5: "火球术", 6: "治愈术", 7: "诅咒术", 8: "精神吸取",
        9: "等级吸取",
    }



    def _marry_character_to_dog(self, idx: int, char: Character) -> tuple[bool, str]:
        if int(char.cflag.get(601, 0)) > 0:
            return False, f"{char.name} 已经结婚了。"
        if int(self.interpreter.vars.items.get(22, 0)) <= 0:
            return False, "当前没有可供结婚的野狗。"
        char.cflag[601] = 900
        char.cflag[602] = 0
        return True, f"{char.name} 和野狗结婚了。"






    def _marry_character_to_lover(self, idx: int, char: Character) -> tuple[bool, str]:
        if int(char.cflag.get(601, 0)) > 0:
            return False, f"{char.name} 已经结婚了。"
        partner_pair = self._resolve_dungeon_town_lover_partner(idx, char)
        if partner_pair is None:
            return False, f"{char.name} 当前没有可以结婚的恋人。"
        partner_idx, partner = partner_pair
        char.cflag[601] = 902
        char.cflag[602] = 0
        partner.cflag[601] = 902
        partner.cflag[602] = 0
        return True, f"{char.name} 和 {partner.name} 结婚了。"






    def _marry_character_to_player(self, idx: int, char: Character) -> tuple[bool, str]:
        if idx == 0:
            return False, "魔王大人还是别和自己结婚了。"
        if int(char.cflag.get(601, 0)) > 0:
            return False, f"{char.name} 已经结婚了。"
        char.cflag[601] = 901
        char.cflag[602] = 0
        return True, f"{char.name} 和魔王结婚了。"






    def _marry_character_to_slave(self, idx: int, char: Character) -> tuple[bool, str]:
        if int(char.cflag.get(601, 0)) > 0:
            return False, f"{char.name} 已经结婚了。"
        candidates = self._get_marriage_slave_candidates(idx, char)
        if not candidates:
            return False, "当前没有可供结婚的奴隶对象。"
        print("\n请选择结婚对象：")
        for other_idx, other in candidates:
            print(f" [{other_idx}] {other.name}")
        print(" [100] 返回")
        choice = self._prompt_choice()
        if choice == "100":
            return False, "已取消结婚。"
        try:
            selected_idx = int(choice)
        except ValueError:
            return False, "输入无效。"
        pair = next(((other_idx, other) for other_idx, other in candidates if other_idx == selected_idx), None)
        if pair is None:
            return False, "没有选中有效的结婚对象。"
        other_idx, other = pair
        char.cflag[601] = int(self._get_character_identity_token(other_idx, other) + 9)
        char.cflag[602] = 0
        char.cflag[609] = int(other.cflag.get(6, 0))
        if idx == 0:
            other.cflag[601] = 901
        else:
            other.cflag[601] = int(self._get_character_identity_token(idx, char) + 9)
        other.cflag[602] = 0
        other.cflag[609] = int(char.cflag.get(6, 0))
        return True, f"{char.name} 和 {other.name} 结婚了。"

    def _marriage(self):
        return self.call_erb_function('MARRIAGE')

    def _marriage_day_slave(self):
        return self.call_erb_function('MARRIAGE_DAY_SLAVE')

    def _marriage_dog(self):
        return self.call_erb_function('MARRIAGE_DOG')

    def _marriage_lovers(self):
        return self.call_erb_function('MARRIAGE_LOVERS')

    def _marriage_you(self):
        return self.call_erb_function('MARRIAGE_YOU')





