from __future__ import annotations
"""Module for PregnancyApplyMixin - pregnancy and birth effect apply methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class PregnancyApplyMixin:
    """Mixin providing pregnancy and birth effect apply methods"""
    def _apply_assistant_due_birth_resolution(self, assistant: Optional[Character], target: Optional[Character]) -> None:
        if assistant is None or self._can_open_trainable_target(self.interpreter.vars.assi, assistant) is not None:
            return
        source = int(assistant.cflag.get(102, 0))
        if source == 1:
            self._set_character_due_birth(assistant, 1, father_flag=0)
        elif source == 3 and target is not None and self._can_open_trainable_target(self.interpreter.vars.target, target) is None:
            self._set_character_due_birth(assistant, 3, father_flag=1, father_name=target.name)

    def _apply_birth_overflow_fallback(self, mother: Character, father_source: int) -> List[str]:
        messages: List[str] = [f"（当前登录角色数量超出最大数量{self._get_max_charanum()}）"]
        status = int(mother.cflag.get(1, 0))
        if mother is self._get_player():
            monster_id = random.choice([191, 192, 193])
            count = random.randint(1, 3)
            gained = self._add_monster_stock(monster_id, count)
            messages.append(f"{mother.name} 生下了 {gained} 只{self._get_item_name(monster_id)}。")
            return messages

        if father_source in (2, 3, 4, 7):
            if status == 9:
                messages.append(f"{mother.name} 生下的孩子被拿到不知何处了。")
            else:
                messages.append(f"{mother.name} 生下的孩子启程了。")
            return messages

        if father_source in (5, 6):
            messages.extend(self._apply_monster_birth_result(mother))
            return messages

        monster_id = random.choice([191, 192, 193])
        count = random.randint(1, 3)
        gained = self._add_monster_stock(monster_id, count)
        messages.append(f"由于人数已满，{mother.name} 的孩子转化为了 {gained} 只{self._get_item_name(monster_id)} 增加到战斗力里。")
        if int(mother.cflag.get(111, 0)) != -2 and int(mother.talent.get(314, 0)) in (3, 4) and count == 1 and random.randint(0, 1) == 0:
            twin_id = 172 if int(mother.talent.get(314, 0)) == 3 else 171
            extra = self._add_monster_stock(twin_id, 1)
            if extra > 0:
                messages.append(f"哦呀？！生了双胞胎呢！额外增加了 1 只{self._get_item_name(twin_id)}。")
        return messages

    def _apply_child_care_begin_flow(self, target: Character) -> List[str]:
        if target.talent.get(9, 0):
            return self._apply_child_care_change_nurse_flow(target)
        return self._begin_child_care_state(target)

    def _apply_child_care_change_nurse_flow(self, target: Character) -> List[str]:
        messages: List[str] = []
        if target.talent.get(9, 0):
            messages.append(f"崩坏了的{target.name}不能照顾孩子。")
        else:
            messages.append(f"现在的{target.name}不能照顾孩子。")
        candidates = self._get_child_care_nurse_candidates(target)
        if not candidates:
            messages.append("找不到照看孩子的人，魔王不得已将孩子遗弃了。")
            messages.extend(self._reset_pregnancy_state(target))
            return messages

        messages.append("要把孩子交给谁来照顾？")
        for idx, char in candidates:
            messages.append(f" [{idx}] {char.name}")
        messages.append(" [100] - 遗弃孩子")

        while True:
            choice = self._prompt_choice()
            if choice == "100":
                messages.append("魔王不得已将孩子遗弃了。")
                messages.extend(self._reset_pregnancy_state(target))
                return messages
            try:
                selected_idx = int(choice)
            except ValueError:
                continue

            nurse = next((char for idx, char in candidates if idx == selected_idx), None)
            if nurse is None:
                continue

            nurse.cflag[110] = int(target.cflag.get(110, 0))
            nurse.cflag[1] = 10
            nurse.talent[153] = 0
            nurse.talent[154] = 1
            self._clear_current_character_selection(nurse)
            if nurse.talent.get(130, 0) == 0 and not nurse.talent.get(122, 0):
                messages.append(f"{nurse.name}开始分泌母乳了。")
                nurse.talent[130] = 1
            if not nurse.talent.get(122, 0):
                messages.append(f"由于给孩子哺乳，{nurse.name}的胸部变大了。")
                self._apply_pregnancy_breast_growth(nurse)
            messages.append(f"{nurse.name}开始在育儿室照顾孩子。")
            messages.extend(self._reset_pregnancy_state(target))
            return messages

    def _apply_child_care_depart(self, target: Character) -> List[str]:
        messages: List[str] = [f"{target.name}照顾的孩子终于可以离开母亲了。"]
        messages.extend(self._get_child_care_depart_kojo_lines(target))
        messages.extend(self._resolve_child_care_depart(target))
        messages.extend(self._reset_pregnancy_state(target))
        return messages

    def _apply_party_due_birth_resolution(self) -> None:
        for char in self.interpreter.vars.chars[1:]:
            source = int(char.cflag.get(102, 0))
            if source == 4:
                self._set_character_due_birth(char, 4, father_flag=-1)
            elif source == 7:
                self._set_character_due_birth(char, 7, father_flag=-4)

    def _apply_player_due_birth_resolution(self, player: Optional[Character], target: Optional[Character]) -> None:
        if player is None:
            return
        source = int(player.cflag.get(102, 0))
        if source == 3 and target is not None and self._can_open_trainable_target(self.interpreter.vars.target, target) is None:
            self._set_character_due_birth(player, 3, father_flag=1, father_name=target.name)
        elif source == 6:
            self._set_character_due_birth(player, 6, father_flag=-3)
        elif source == 7:
            self._set_character_due_birth(player, 7, father_flag=-4)

    def _apply_post_pregnancy_breast_recovery(self, target: Character):
        if target.talent.get(119, 0):
            return
        if target.talent.get(114, 0):
            target.talent[114] = 0
            target.talent[110] = 1
            return
        if target.talent.get(110, 0):
            target.talent[110] = 0
            return
        if not target.talent.get(109, 0) and not target.talent.get(116, 0):
            target.talent[109] = 1

    def _apply_target_due_birth_resolution(self, target: Optional[Character], assistant: Optional[Character]) -> None:
        if target is None or self._can_open_trainable_target(self.interpreter.vars.target, target) is not None:
            return
        source = int(target.cflag.get(102, 0))
        if source == 1:
            self._set_character_due_birth(target, 1, father_flag=0)
        elif source == 2 and assistant is not None:
            self._set_character_due_birth(target, 2, father_flag=1, father_name=assistant.name)
        elif source == 5:
            self._set_character_due_birth(target, 5, father_flag=-2)
        elif source == 6:
            self._set_character_due_birth(target, 6, father_flag=-3)

