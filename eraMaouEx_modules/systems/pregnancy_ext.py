from __future__ import annotations
"""Module for PregnancyExtMixin - 怀孕系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class PregnancyExtMixin:
    """Mixin providing 怀孕系统 methods for GameEngine"""

    def _add_pregnancy_source_amount(self, target: Optional[Character], source: int, amount: int):
        if target is None or amount <= 0:
            return
        flag_id = self._get_pregnancy_source_flag_id(source)
        target.cflag[flag_id] = max(0, int(target.cflag.get(flag_id, 0))) + max(0, int(amount))






    def _apply_marriage_daily_conception_followup(self, char: Character):
        marriage_state = int(char.cflag.get(601, 0))
        amount = int(char.cflag.get(107, 0))
        if amount <= 0:
            return
        if marriage_state == 900:
            self._add_pregnancy_source_amount(char, 5, amount)
            return
        if marriage_state not in (901, 902):
            self._add_pregnancy_source_amount(char, 4, amount)
            char.cflag[112] = int(marriage_state)






    def _apply_pregnancy_breast_growth(self, target: Character):
        if target.talent.get(116, 0):
            target.talent[116] = 0
            target.talent[109] = 1
            return
        if target.talent.get(109, 0):
            target.talent[109] = 0
            return
        if target.talent.get(110, 0):
            target.talent[110] = 0
            target.talent[114] = 1
            return
        if target.talent.get(114, 0):
            target.talent[114] = 0
            target.talent[119] = 1
            return
        if target.talent.get(119, 0):
            return
        target.talent[110] = 1






    def _apply_pregnancy_room_transfer_daily_state(self, target: Character, today: int, status: int, due_day: int, allow_late_month_training: bool) -> List[str]:
        if 0 <= due_day - today <= 3 and not allow_late_month_training and status == 0:
            self._move_character_to_nursery(target, previous_state=status)
            return [f"{target.name} 被移动到了育儿室中……"]
        if target.talent.get(154, 0):
            messages = [f"{target.name} 在育儿室照顾孩子……"]
            messages.extend(self._get_child_care_visit_kojo_lines(target))
            target.cflag[273] = 1
            return messages
        if status == 10 and target.talent.get(153, 0):
            messages = [f"{target.name} 在育儿室里等待生产……"]
            messages.extend(self._get_child_care_visit_kojo_lines(target))
            target.cflag[273] = 1
            return messages
        return []






    def _apply_pregnancy_room_transfer_due_in_three_days(self, target: Character, status: int, allow_late_month_training: bool) -> List[str]:
        target_idx = next((idx for idx, char in enumerate(self.interpreter.vars.chars) if char is target), -1)

        def clear_active_slots() -> None:
            if self.interpreter.vars.target == target_idx:
                self.interpreter.vars.target = -1
            if self.interpreter.vars.assi == target_idx:
                self.interpreter.vars.assi = -1

        if status == 9:
            return [f"为了准备生产，{target.name} 被移动到了狂王的育儿室。"]
        if status == 3:
            messages = [f"为了准备生产，迎击中的{target.name}开始了返回。"]
            target.cflag[507] = 0
            if allow_late_month_training:
                target.cflag[1] = 3
            else:
                self._move_character_to_nursery(target, previous_state=status)
                target.cflag[1] = 10
            clear_active_slots()
            return messages
        if status not in (3, 7, 8):
            self._move_character_to_nursery(target, previous_state=status)
            clear_active_slots()
            return [f"为了准备生产，{target.name} 被移动到了育儿室。"]
        return []






    def _apply_pregnancy_room_transfer_for_target(self, target: Character, today: int, allow_late_month_training: bool) -> List[str]:
        due_day = self._get_pregnancy_due_day(target)
        if due_day <= 0:
            return []
        status = int(target.cflag.get(1, 0))
        if due_day - 3 == today:
            return self._apply_pregnancy_room_transfer_due_in_three_days(target, status, allow_late_month_training)
        return self._apply_pregnancy_room_transfer_daily_state(target, today, status, due_day, allow_late_month_training)






    def _apply_pregnancy_status_change(self, target: Character) -> List[str]:
        messages: List[str] = []
        target.maxbase[0] = max(1, int(target.maxbase.get(0, 0)) - 500)
        target.base[0] = min(int(target.base.get(0, 0)), int(target.maxbase.get(0, 0)))
        messages.append(f"由于怀孕，{target.name} 的胸部变大了。")
        if not target.talent.get(130, 0):
            target.talent[130] = 1
            messages.append(f"{target.name} 开始分泌母乳了。")
        stress = self._get_pregnancy_stress_value(target)
        if stress < 100 or self._is_player_character(target):
            messages.append(f"{target.name} 高兴地爱抚着自己的肚子……")
        elif int(target.talent.get(9, 0)) == 0:
            messages.extend(
                [
                    f"{target.name} 呆如木鸡，",
                    f"{target.name} 的心中，有什么东西坏掉了……",
                    f"{target.name} 的精神变成【崩坏】了。",
                ]
            )
            if int(target.talent.get(85, 0)) != 0:
                target.talent[85] = 0
                messages.append(f"{target.name} 失去了【爱慕】。")
            if int(target.talent.get(76, 0)) != 0:
                target.talent[76] = 0
                messages.append(f"{target.name} 失去了【淫乱】。")
            target.talent[9] = 1
        return messages






    def _apply_turn_end_conception_cycle(self) -> None:
        original_target = int(self.interpreter.vars.target)
        original_assi = int(self.interpreter.vars.assi)
        try:
            for idx, _char in enumerate(self.interpreter.vars.chars):
                self.interpreter.vars.target = idx
                self._apply_turn_end_conception_rolls()
                self._apply_turn_end_conception_resolution()
        finally:
            self.interpreter.vars.target = original_target
            self.interpreter.vars.assi = original_assi




    def _apply_turn_end_conception_resolution(self):
        player = self._get_player()
        target = self._get_target()
        assistant = self.interpreter.vars.chars[self.interpreter.vars.assi] if 0 <= self.interpreter.vars.assi < len(self.interpreter.vars.chars) else None

        self._apply_target_due_birth_resolution(target, assistant)
        self._apply_assistant_due_birth_resolution(assistant, target)
        self._apply_player_due_birth_resolution(player, target)
        self._apply_party_due_birth_resolution()




    def _apply_turn_end_conception_rolls(self):
        player = self._get_player()
        target = self._get_target()
        assistant = self.interpreter.vars.chars[self.interpreter.vars.assi] if 0 <= self.interpreter.vars.assi < len(self.interpreter.vars.chars) else None

        if self._can_apply_pregnancy_flow(target, self.interpreter.vars.target):
            self._roll_pregnancy_source(target, 1)
            if assistant is not None:
                self._roll_pregnancy_source(target, 2)
            if target.equipt.get(89, 0) > 0:
                self._roll_pregnancy_source(target, 5)
            if target.equipt.get(90, 0) > 0:
                self._roll_pregnancy_source(target, 6)

        if self._can_apply_pregnancy_flow(assistant, self.interpreter.vars.assi):
            self._roll_pregnancy_source(assistant, 1)
            if self._can_apply_pregnancy_flow(target, self.interpreter.vars.target):
                self._roll_pregnancy_source(assistant, 3)

        if player is not None:
            self._roll_pregnancy_source(player, 3)
            self._roll_pregnancy_source(player, 6)
            self._roll_pregnancy_source(player, 7)




    def _build_pregnancy_awareness_lines(self, target: Character, source: int) -> tuple[List[str], bool]:
        lines = [f"{target.name} 的样子有点奇怪……"]
        clear_monster_father = False
        if source == 1:
            lines.append(f"{target.name} 好像怀上了魔王的孩子。")
        elif source in (2, 3):
            father_name = target.cstr.get(2, "").strip() or "地下城内的某人"
            lines.append(f"{target.name} 好像怀上了 {father_name} 的孩子。")
        elif source == 4:
            lines.append(f"{target.name} 好像怀上了不知名男人的孩子。")
        elif source == 5:
            lines.append(f"{target.name} 好像怀上了野狗的孩子。")
        elif source == 6:
            clear_monster_father = int(target.cflag.get(112, 0)) > 0 and random.randint(0, 2) == 0
            father_name = self._get_item_name(int(target.cflag.get(112, 0))) if clear_monster_father else "怪物"
            lines.append(f"{target.name} 好像怀上了{father_name}的孩子。")
        elif source == 7:
            lines.append(f"{target.name} 好像怀上了狂王的孩子。")
        return lines, clear_monster_father






    def _clear_pregnancy_tracking_flags(self, target: Character):
        if int(target.cflag.get(1, 0)) == 10:
            target.cflag[1] = 0
        for flag_id in range(101, 110):
            target.cflag[flag_id] = 0
        target.cflag[110] = 0
        target.cflag[111] = 0
        target.cstr[2] = ""






    def _conception_check_all(self, target) -> List[str]:
        """妊娠確定時 - 对应 @CONCEPTION_CHECK_ALL"""
        messages: List[str] = []
        return messages




    def _conception_check_extra(self, target) -> List[str]:
        """売春妊娠確定 - 对应 @CONCEPTION_CHECK_EXTRA"""
        messages: List[str] = []
        return messages




    def _conception_check_kyouou_to_t(self, target) -> List[str]:
        """狂王妊娠確定 - 对应 @CONCEPTION_CHECK_KYOUOU_TO_T"""
        messages: List[str] = []
        return messages




    def _conception_check_ntrd_to_t(self, target) -> List[str]:
        """NTRD妊娠確定 - 对应 @CONCEPTION_CHECK_NTRD_TO_T"""
        messages: List[str] = []
        return messages



    def _fail_pregnancy_source_roll(self, target: Character, flag_id: int) -> bool:
        target.cflag[flag_id] = 0
        return False






    def _find_pregnancy_father_character(self, target: Character, source: int) -> Optional[Character]:
        if source == 1:
            return self._get_player()
        father_flag = int(target.cflag.get(111, 0))
        if father_flag > 0:
            father_name = target.cstr.get(2, "").strip()
            for char in self.interpreter.vars.chars:
                if char is not None and char.name == father_name:
                    return char
        return None






    def _get_pregnancy_awareness_kojo_lines(self, target: Character, source: int) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        first_time = int(target.cflag.get(271, 0)) == 0
        if kojo_num == 100:
            if first_time:
                if int(target.talent.get(9, 0)):
                    return ["「啊哈～啊哈～……肚子里到底进去了什么不得了的东西呢……♪」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return [
                        "「啊啊……该怎么办呢……难道，要生下主人的孩子了吗……」",
                        f"{target.name} 含情脉脉地抚摸着自己的肚子。",
                    ]
                if source in (2, 3):
                    return ["「啊啊……难道……被其他勇者弄怀孕什么的……」"]
                if source == 4:
                    return ["「不、不要……怀孕什么的……我还没做好准备………」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return [
                        "「怀上了吗……狗狗大人的孩子，神明大人谢谢你～♪」",
                        f"{target.name} 含情脉脉地抚摸着小腹，脸上满是发自心底的幸福。",
                    ]
                if source == 5:
                    return ["「不会吧……被野狗……弄怀孕什么的………」"]
                if source == 7:
                    return ["「难、难道……是狂王大人的孩子………」"]
            else:
                if int(target.talent.get(9, 0)):
                    return ["「啊哈……又有厉害的家伙进到肚子里了呢……♪」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return [
                        "「这就又怀上了呢，狗狗大人还真是精力充沛啊。」",
                        f"{target.name} 摸着肚子无奈地摇了摇头，脸上的笑却完全停不下来。",
                    ]
                if source == 7:
                    return ["「难、难道……是狂王大人的孩子………」"]
                return ["「啊、啊咧……难、难道……又怀上了魔物的孩子吗……」"]
        if kojo_num == 101:
            if first_time:
                if int(target.talent.get(9, 0)):
                    return ["「啊……哈……我的孩子啊……会是什么样的孩子呢……」"]
                if source == 6 and int(target.cflag.get(602, 0)) > 40:
                    return ["「好开心……子宫完全屈服于那家伙的精液了呢……」"]
                if source == 6:
                    return ["「怎么会……有了怪物的孩子……？」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「难道……魔族的孩子什么的……不过心情也不差……」"]
            else:
                if int(target.talent.get(9, 0)):
                    return ["「啊……哈……又有孩子了啊……会是什么样的孩子呢……」"]
                if source == 6 and int(target.cflag.get(602, 0)) > 40:
                    return ["「呜呼……又怀上了吗……子宫已经完全输给那家伙的精液了呢……」"]
                if source == 6:
                    return ["「怎么会……又有了怪物的孩子……？」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「又是你的孩子吗……真是，已经离不开你了呢……」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return ["「有了个可爱的宝宝……♪」"]
                if source == 7:
                    return ["「呜呼呜……难、难道……这是狂王大人的孩子……？」"]
                return ["「咕呜……咕呜……欸……又、又怀孕了………？」"]
        if kojo_num == 103 and first_time:
            if int(target.talent.get(9, 0)):
                return [
                    "「啊哈哈……啊哈哈……为什么……为什么肚子居然膨胀成这么大了呢？」",
                    f"{target.name} 发狂地笑着。",
                ]
            if int(target.talent.get(85, 0)) and source == 1:
                return [
                    "「啊啊……真、真是困扰了呢……那个人的孩子，居然怀上了……」",
                    "「怎么可能会怀上呢……都要放弃了来着……」",
                ]
            if source in (2, 3):
                return [
                    "「啊啊……骗人……我、我居然怀孕了什么的……」",
                    f"{target.name} 似乎对腹中孩子的父亲是谁有些头绪。",
                ]
            if source == 5 and int(target.talent.get(136, 0)):
                return ["「怎、怎么办……居然真的怀上了可爱的狗宝宝……♪」"]
            if source == 5:
                return ["「怎么会……我居然怀上了那个野狗的孩子……」"]
            if source == 7:
                return ["「我、我居然怀上了狂王的孩子……怎么会……」"]
            return [
                "「啊啊……骗人……我、我居然怀孕了什么的……」",
                "「但是……该怎么跟主人说才好呢……」",
            ]
        if kojo_num == 105 and first_time:
            if int(target.talent.get(9, 0)):
                return [
                    "「欸嘿嘿……啊哈……啊哈……魔族的孩子，在我的肚子里哦……」",
                    f"可怜的{target.name} 似乎没能接受怀孕的事实。",
                ]
            if int(target.talent.get(85, 0)) and source == 1:
                return [
                    "「啊……那个……我、我好像怀上主人的孩子了呢……」",
                    f"{target.name} 害羞地抚摸着腹部看着你。",
                ]
            return [
                "「啊……怎么这样……我、我怀孕了啊……怎么办……好害怕……」",
                f"{target.name} 无助地抱住了双肩。",
            ]
        if kojo_num == 119 and first_time:
            if source == 7:
                return ["「难道……怀上了狂王的孩子……？」"]
            if int(target.talent.get(85, 0)) and source == 1:
                return ["「……是你的孩子吗？」"]
        return []






    def _get_pregnancy_beast_parent_stress(self, target: Character) -> int:
        if int(target.talent.get(85, 0)) != 0:
            stress = 100
        elif int(target.talent.get(76, 0)) != 0:
            stress = 80
        else:
            stress = 40
        if int(target.talent.get(136, 0)) != 0:
            stress -= 40
        if int(target.cflag.get(601, 0)) == 900:
            stress -= 40
        return stress






    def _get_pregnancy_current_day(self) -> int:
        return self._get_total_day_count()






    def _get_pregnancy_due_day(self, target: Character) -> int:
        return int(target.cflag.get(110, 0))






    def _get_pregnancy_hairanzai_factor(self, target: Character) -> int:
        factor = 3 - (2 if int(target.cflag.get(109, 0)) else 0)
        today = self._get_pregnancy_current_day()
        if int(target.talent.get(314, 0)) == 2 and 14 <= today <= 16:
            factor = 1 if int(target.cflag.get(109, 0)) else 2
        return max(1, factor)






    def _get_pregnancy_monster_parent_stress(self, target: Character) -> int:
        if int(target.talent.get(85, 0)) != 0:
            stress = 100
        elif int(target.talent.get(76, 0)) != 0:
            stress = 80
        else:
            stress = 40
        if int(target.talent.get(314, 0)) == 9:
            stress -= 40
        partner_token = int(target.cflag.get(601, 0))
        if 1 <= partner_token <= 12:
            stress -= 40
        return stress






    def _get_pregnancy_related_parent_stress(self, target: Character, father: Optional[Character], source: int) -> int:
        if int(target.talent.get(85, 0)) != 0:
            base = 20
        elif int(target.talent.get(76, 0)) != 0:
            base = 10
        else:
            return 0
        relation = self._get_pregnancy_relation_rate(target, father)
        if relation <= 0:
            return base
        if int(target.talent.get(85, 0)) != 0:
            return 10 * ((200 - relation) // 100) + 10
        return 10 * ((200 - relation) // 100)






    def _get_pregnancy_relation_rate(self, target: Character, father: Optional[Character]) -> int:
        if father is None:
            return 0
        if father is self._get_player():
            return 0
        try:
            father_idx = self.interpreter.vars.chars.index(father)
        except ValueError:
            return 0
        relation_value = int(target.cflag.get(600 + father_idx, 0))
        if relation_value <= 0:
            return 0
        return relation_value






    def _get_pregnancy_source_flag_id(self, source: int) -> int:
        return 101 if int(source) == 1 else 101 + int(source)






    def _get_pregnancy_source_roll_profile(self, amount: int) -> tuple[int, int]:
        if amount >= 25:
            return 1, 3
        if amount >= 20:
            return 2, 2
        if amount >= 15:
            return 3, 2
        if amount >= 10:
            return 4, 2
        if amount >= 5:
            return 5, 2
        return 6, 2






    def _get_pregnancy_stress_value(self, target: Character) -> int:
        stress = 0
        source = int(target.cflag.get(102, 0))
        father = self._find_pregnancy_father_character(target, source)
        if int(target.talent.get(85, 0)) != 0 and source == 1:
            stress += 0
        elif int(target.talent.get(76, 0)) != 0 and source == 1:
            stress += 30
        if source in (2, 3):
            stress += self._get_pregnancy_related_parent_stress(target, father, source)
        elif int(target.talent.get(85, 0)) != 0 and source == 4:
            stress += 80
        elif int(target.talent.get(76, 0)) != 0 and source == 4:
            stress += 50
        elif source == 5:
            stress += self._get_pregnancy_beast_parent_stress(target)
        elif source == 6:
            stress += self._get_pregnancy_monster_parent_stress(target)
        elif int(target.talent.get(85, 0)) != 0 and source == 7:
            stress += 80
        elif int(target.talent.get(76, 0)) != 0 and source == 7:
            stress += 30
        if int(target.talent.get(85, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            stress += 50
            if int(target.exp.get(60, 0)) > 0:
                stress += int(target.exp.get(60, 0)) * 5
        if int(target.talent.get(12, 0)) != 0:
            stress -= 20
        if int(target.talent.get(155, 0)) != 0:
            stress -= 40
        if int(target.talent.get(134, 0)) != 0:
            stress += 20
        if int(target.exp.get(60, 0)) > 0:
            stress -= 20
        return stress






    def _grant_pregnancy_talents(self, target: Character) -> List[str]:
        messages: List[str] = []
        preg_type = int(target.cflag.get(113, 0))
        if preg_type == 1:
            target.talent[341] = 1
            messages.append(f"{target.name} 获得了乳内妊娠。")
        elif preg_type == 2:
            target.talent[342] = 1
            messages.append(f"{target.name} 获得了精巢妊娠。")
        elif preg_type == 3:
            target.talent[343] = 1
            messages.append(f"{target.name} 获得了肛内妊娠。")
        target.talent[153] = 1
        target.cflag[113] = 0
        messages.append(f"{target.name} 获得了妊娠。")
        return messages






    def _is_pregnancy_aware_now(self, target: Character) -> bool:
        source = int(target.cflag.get(102, 0))
        due_day = self._get_pregnancy_due_day(target)
        today = int(self.interpreter.vars.day[2])
        if source == 1:
            return due_day > 0 and due_day <= today + 10
        if source in (2, 3, 4):
            return due_day > 0 and due_day <= today + 54
        if source in (5, 6, 7):
            return due_day > 0 and due_day <= today + 24
        return False






    def _is_pregnancy_source_roll_success(self, amount: int, pregnancy_bonus: int, hairanzai: int) -> bool:
        base, success_limit = self._get_pregnancy_source_roll_profile(amount)
        threshold = max(1, (base + pregnancy_bonus) * hairanzai)
        return random.randrange(threshold) <= success_limit






    def _iter_pregnancy_daily_targets(self) -> List[Character]:
        return [char for char in self.interpreter.vars.chars if char is not None]






    def _ninsin_main(self) -> List[str]:
        """妊娠/出産/育児室関連处理 - 对应 @NINSIN_MAIN"""
        messages: List[str] = []
        v = self.interpreter.vars
        current_day = self._get_total_day_count()

        for target in v.chars[1:]:
            if target.cflag.get(110, 0) > 0:
                due_day = target.cflag.get(110, 0)
                if current_day >= due_day:
                    messages.extend(self._childbirth(target))
                else:
                    remaining = due_day - current_day
                    if remaining <= 7 and remaining > 0:
                        messages.append(f"{target.savestr}的预产期还有{remaining}天。")

            if target.cflag.get(111, 0) > 0:
                target.cflag[111] = target.cflag.get(111, 0) + 1

            if target.cflag.get(112, 0) > 0:
                target.cflag[112] = target.cflag.get(112, 0) + 1

        return messages




    def _reset_pregnancy_state(self, target: Character) -> List[str]:
        messages: List[str] = []
        if not target.talent.get(119, 0):
            self._apply_post_pregnancy_breast_recovery(target)
            messages.append(f"由于不再给孩子哺乳，{target.name} 的胸部变小了。")
        else:
            messages.append(f"{target.name} 的超乳仍然淫乱地胀大着缩不回去了。")
        if target.talent.get(130, 0):
            target.talent[130] = 0
            messages.append(f"{target.name} 不再分泌母乳了。")
        target.talent[153] = 0
        target.talent[154] = 0
        target.maxbase[0] = int(target.maxbase.get(0, 0)) + 500
        self._clear_pregnancy_tracking_flags(target)
        return messages






    def _roll_pregnancy_source(self, target: Character, source: int) -> bool:
        flag_id = self._get_pregnancy_source_flag_id(source)
        amount = max(0, int(target.cflag.get(flag_id, 0)))
        if amount <= 0:
            return False
        if not self._get_flag_bit(5, 2):
            return self._fail_pregnancy_source_roll(target, flag_id)
        if not self._can_character_conceive_now(target, source):
            return self._fail_pregnancy_source_roll(target, flag_id)

        hairanzai = self._get_pregnancy_hairanzai_factor(target)
        pregnancy_bonus = max(0, int(target.talent.get(100, 0))) * 2
        success = self._is_pregnancy_source_roll_success(amount, pregnancy_bonus, hairanzai)
        target.cflag[flag_id] = 0
        if success:
            target.cflag[102] = int(source)
        return success






    def _set_pregnancy_due_day(self, target: Character, days_from_now: int) -> None:
        target.cflag[110] = self._get_pregnancy_current_day() + max(0, int(days_from_now))





