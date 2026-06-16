from __future__ import annotations
"""Module for TurnEndMixin - 回合结束处理"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class TurnEndMixin:
    """Mixin providing 回合结束处理 methods for GameEngine"""

    def _apply_daily_aphrodisiac_addiction_checks(self) -> List[str]:
        messages: List[str] = []
        weekly_decay = self._is_aphrodisiac_weekly_decay_day()
        for target in self.interpreter.vars.chars[1:]:
            residue = max(0, int(target.cflag.get(31, 0)))
            if weekly_decay and residue > 0:
                residue = max(0, residue - 1)
                target.cflag[31] = residue
            if weekly_decay and int(target.talent.get(46, 0)) != 0 and int(target.cflag.get(1, 0)) != 9:
                if int(target.cflag.get(32, 0)) != 0:
                    target.cflag[32] = 0
                else:
                    messages.extend(self._apply_daily_aphrodisiac_withdrawal(target, residue))
            if residue <= 0 and int(target.talent.get(46, 0)) != 0:
                target.talent[46] = 0
                messages.extend(
                    [
                        f"{target.name} 的样子变了……",
                        f"体内的媚药效果被根除了，{target.name} 的药瘾消失了。",
                        f"{target.name} 的【媚药中毒】消除了。",
                    ]
                )
            easy_addicted = int(target.talent.get(72, 0)) != 0
            if int(target.talent.get(46, 0)) == 0 and (
                (not easy_addicted and residue >= 12) or (easy_addicted and residue >= 9)
            ):
                target.talent[46] = 1
                if residue < 15:
                    residue = 15
                    target.cflag[31] = residue
                messages.extend(
                    [
                        f"{target.name} 的样子有点奇怪……",
                        f"媚药的过量使用，令{target.name} 沾上药瘾了。",
                        f"{target.name} 获得了【媚药中毒】。",
                    ]
                )
            if int(target.talent.get(123, 0)) == 0 and (
                residue >= 40 or (easy_addicted and residue >= 30)
            ):
                target.talent[123] = 1
                messages.extend(
                    [
                        f"{target.name} 的样子有点奇怪……",
                        f"{target.name} 随着媚药的过量使用，人也变得暴躁了。",
                        f"{target.name} 获得了【疯狂】。",
                    ]
                )
            if int(target.talent.get(9, 0)) == 0 and (
                residue >= 100 or (easy_addicted and residue >= 75)
            ):
                target.talent[9] = 1
                messages.extend(
                    [
                        f"{target.name} 的样子有点奇怪……",
                        f"{target.name} 随着媚药的过量使用，完全变成了废人。",
                        f"{target.name} 的精神变成【崩坏】了。",
                    ]
                )
        return messages






    def _apply_daily_aphrodisiac_withdrawal(self, target: Character, residue: int) -> List[str]:
        messages = [
            f"{target.name} 在诉说着自己身体的不适。",
            "看来，春药中毒的禁断症状出现了……",
        ]
        if self._prompt_aphrodisiac_withdrawal_item_use(target):
            return messages
        if int(target.cflag.get(1, 0)) == 2:
            target.base[0] = max(1, int(target.base.get(0, 0)) - 300)
            messages.append(f"数小时后，{target.name} 身体的颤抖终于停了下来。")
            return messages

        supporters = self._count_standby_withdrawal_supporters()
        severity_checks = max(1, min(10, residue // 10 + 1 - supporters))
        suffered = any(random.randint(0, 99) < 40 for _ in range(severity_checks))
        if suffered:
            target.maxbase[0] = max(600, int(target.maxbase.get(0, 0)) - 50)
            target.maxbase[1] = max(100, int(target.maxbase.get(1, 0)) - 50)
            target.base[0] = min(int(target.base.get(0, 0)), int(target.maxbase.get(0, 0)))
            target.base[1] = min(int(target.base.get(1, 0)), int(target.maxbase.get(1, 0)))
            target.base[0] = max(1, int(target.base.get(0, 0)) - 500)
            messages.extend(
                [
                    f"被禁断症状折磨着的{target.name} 痛苦地在地上打滚，持续数小时后才终于平静下来。",
                    f"{target.name} 的体力和气力衰退了。",
                ]
            )
            nurse_loss = 200
        else:
            target.base[0] = max(1, int(target.base.get(0, 0)) - 300)
            messages.extend(
                [
                    f"数小时后，{target.name} 身体的颤抖终于停止了。",
                    "护理人员也辛苦了，这次总算平安度过了……",
                ]
            )
            nurse_loss = 100

        for char in self.interpreter.vars.chars[1:]:
            if int(char.cflag.get(1, 0)) != 0:
                continue
            guaranteed = int(char.talent.get(117, 0)) or int(char.talent.get(63, 0))
            if guaranteed or random.randint(0, 2) == 0:
                char.base[0] = max(1, int(char.base.get(0, 0)) - nurse_loss)
        return messages






    def _apply_daily_body_hair_growth(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            hair_message = self._apply_daily_head_hair_growth(target)
            if hair_message:
                messages.append(hair_message)
            pubic_message = self._apply_daily_pubic_hair_growth(target)
            if pubic_message:
                messages.append(pubic_message)
        return messages






    def _apply_daily_character_daily_state_flows(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            self._reset_character_location_state_if_needed(target)
            messages.extend(self._apply_character_daily_ring_effects(target))
        return messages






    def _apply_daily_character_hp_recovery(self, target: Character) -> None:
        current_hp = max(1, int(target.base.get(0, 0)))
        target.base[0] = current_hp

        max_hp = max(1, int(target.maxbase.get(0, 1)))
        heal = max_hp // 10 if int(self.interpreter.vars.time) == 1 else max_hp // 2
        heal = self._apply_ring_recovery_multiplier(heal, target, 4)
        heal = self._apply_ring_recovery_divider(heal, target, 13)

        if int(target.talent.get(314, 0)) == 3:
            heal *= 3
        if int(target.cflag.get(1, 0)) == 2:
            heal //= 30
        if self._get_character_flag_bit(target, 503, DUNGEON_STATE_CAMP_BIT):
            heal *= 2
            self._set_character_flag_bit(target, 503, DUNGEON_STATE_CAMP_BIT, False)

        target.cflag[4] = 0
        if int(target.talent.get(111, 0)):
            heal *= 2
        elif int(target.talent.get(112, 0)) or int(target.talent.get(256, 0)):
            heal //= 2

        target.base[0] = min(max_hp, current_hp + max(0, heal))






    def _apply_daily_character_mp_recovery(self, target: Character) -> None:
        max_mp = max(1, int(target.maxbase.get(1, 1)))
        if int(target.cflag.get(1, 0)) != 2:
            target.base[1] = max_mp
            return

        heal = max_mp // 40
        heal = self._apply_ring_recovery_multiplier(heal, target, 5)
        heal = self._apply_ring_recovery_divider(heal, target, 13)

        if int(target.talent.get(12, 0)):
            heal *= 2
        elif int(target.talent.get(10, 0)):
            heal //= 2

        current_mp = int(target.base.get(1, 0))
        target.base[1] = min(max_mp, current_mp + max(0, heal))






    def _apply_daily_child_care_departures(self) -> List[str]:
        messages: List[str] = []
        today = self._get_pregnancy_current_day()
        for target in self._iter_pregnancy_daily_targets():
            if not target.talent.get(154, 0):
                continue
            due_day = self._get_pregnancy_due_day(target)
            if due_day <= 0 or due_day + 5 != today:
                continue
            messages.extend(self._apply_child_care_depart(target))
        return messages






    def _apply_daily_cursed_ring_conversion(self) -> List[str]:
        player = self._get_player()
        if player is None:
            return []
        plain_ring_name = self._get_item_name(300)
        plain_ring_count = min(10, self._get_item_count(player, 300))
        if plain_ring_count <= 0:
            return []

        messages: List[str] = []
        for _ in range(plain_ring_count):
            if not self._use_item(player, plain_ring_name, 1):
                break
            base_code = self._roll_daily_cursed_ring_base_code()
            cursed_item_id = 300 + base_code
            self._add_item(player, self._get_item_name(cursed_item_id), 1)
            messages.append(f"你把装饰戒指制造成了 {self._get_item_name(cursed_item_id)}。")
        return messages






    def _apply_daily_dematurity_checks(self) -> List[str]:
        removable_talents = [20, 21, 22, 24, 26, 27, 30, 32, 34, 35, 37, 55, 93]
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            if not self._should_apply_daily_dematurity_check(target):
                continue
            if not self._can_daily_dematurity_regress(target):
                continue
            messages.extend(self._apply_daily_dematurity_regression_state(target, removable_talents))
        return messages






    def _apply_daily_dematurity_regression_state(self, target: Character, removable_talents: List[int]) -> List[str]:
        messages = [
            "（呃……这是什么？）",
            f"{target.name} 的样子有点奇怪……",
            f"{target.name} 再也无法接受严厉的调教，获得了【{self._get_talent_name(131)}】…",
        ]
        target.talent[131] = 1
        for talent_id in removable_talents:
            if int(target.talent.get(talent_id, 0)) != 0:
                target.talent[talent_id] = 0
                messages.append(f"【{self._get_talent_name(talent_id)}】消失了。")
        if not target.talent.get(57, 0):
            target.talent[57] = 1
            messages.append(f"获得了【{self._get_talent_name(57)}】。")
        target.mark[3] = 0
        messages.append(f"【{self._get_mark_name(3)}】变为0。")
        return messages






    def _apply_daily_due_birth_event(
        self,
        target: Character,
        player: Optional[Character],
        today: int,
        messages: List[str],
    ) -> None:
        if not self._should_apply_daily_due_birth_event(target, today):
            return

        source = int(target.cflag.get(102, 0))
        status = int(target.cflag.get(1, 0))
        target.exp[60] = int(target.exp.get(60, 0)) + 1
        target.exp[61] = int(target.exp.get(61, 0)) + 1

        if status in (2, 3) and source not in (5, 6):
            messages.extend(self._apply_daily_due_birth_miscarriage(target))
            return

        messages.extend(self._apply_daily_due_birth_success(target, source, status, player))






    def _apply_daily_due_birth_events(self) -> List[str]:
        messages: List[str] = []
        today = self._get_pregnancy_current_day()
        player = self._get_player()
        for target in self._iter_pregnancy_daily_targets():
            self._apply_daily_due_birth_event(target, player, today, messages)
        return messages






    def _apply_daily_due_birth_miscarriage(self, target: Character) -> List[str]:
        messages = [f"{target.name} 在地下城内突然感到一阵剧痛，随后流产了……"]
        target.maxbase[0] = max(1, int(target.maxbase.get(0, 1)) // 3)
        target.base[0] = max(1, int(target.base.get(0, 0)) // 6)
        target.base[1] = max(0, int(target.base.get(1, 0)) // 6)
        messages.extend(self._reset_pregnancy_state(target))
        return messages






    def _apply_daily_due_birth_success(self, target: Character, source: int, status: int, player: Optional[Character]) -> List[str]:
        if int(target.cflag.get(1, 0)) == 9:
            return self._apply_ntr_child_birth(target)
        messages = [self._build_birth_delivery_line(target, source)]
        messages.extend(self._get_childbirth_kojo_lines(target, source))
        target.cflag[272] = 1
        if target.talent.get(0, 0) and not (target.talent.get(341, 0) or target.talent.get(342, 0) or target.talent.get(343, 0)):
            target.talent[0] = 0
            messages.append(f"{target.name} 再生的处女膜因为生产而破损了……")
        if source in (5, 6):
            self._apply_monster_birth_status_reset(target)
            if status in (2, 3):
                target.base[0] = max(1, int(target.base.get(0, 0)) // 3)
                target.base[1] = max(0, int(target.base.get(1, 0)) // 3)
            messages.extend(self._apply_monster_birth_result(target))
            messages.extend(self._reset_pregnancy_state(target))
            return messages

        if target.talent.get(85, 0) and source == 1 and player is not None and player.talent.get(122, 0) and not player.talent.get(156, 0):
            count = int(self.interpreter.vars.get_flag(32, 0)) + 1
            self.interpreter.vars.set_flag(32, count)
            if count >= 3:
                player.talent[156] = 1
                messages.append(f"{player.name} 的父性觉醒了。")
        target.talent[153] = 0
        self._clear_birth_body_markers(target)
        messages.extend(self._apply_child_care_begin_flow(target))
        return messages






    def _apply_daily_enemy_reinforcement(self) -> List[str]:
        messages: List[str] = self._apply_special_daily_enemy_entries()
        for _ in range(self._get_daily_enemy_spawn_attempts()):
            message = self._spawn_daily_enemy_once()
            if message is None:
                continue
            messages.append(message)
        return messages






    def _apply_daily_enter_enemy(self) -> List[str]:
        """每天生成勇者/冒险者来侵攻地下城 (对应 ERB 的 ENTER_ENEMY)"""
        messages: List[str] = []
        total_days = self._get_total_day_count()
        ex_flag_9012 = int(self.interpreter.vars.globals.get(9012, 0))

        messages.extend(self._enter_enemy_character())
        if total_days >= 100:
            messages.extend(self._enter_enemy_character())
        if total_days >= 300:
            messages.extend(self._enter_enemy_character())
        if total_days >= 500:
            messages.extend(self._enter_enemy_character())

        extra_calls = self._get_daily_enter_enemy_loop_count(total_days, ex_flag_9012)
        for _ in range(extra_calls):
            messages.extend(self._enter_enemy_character())
        return messages






    def _apply_daily_faith_adjustments(self) -> List[str]:
        for target in self.interpreter.vars.chars[1:]:
            self._apply_character_daily_faith_adjustment(target)
        return []






    def _apply_daily_futanari_transformation_checks(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            if not target.talent.get(326, 0):
                continue
            if int(target.exp.get(20, 0)) < 150:
                continue
            messages.extend(self._apply_futanari_transformation_prompt(target))
        return messages






    def _apply_daily_head_hair_growth(self, target: Character) -> Optional[str]:
        current = int(target.talent.get(302, 0))
        if current > 201:
            return None
        target.talent[302] = current + 1
        updated = int(target.talent.get(302, 0))
        if updated == 51:
            return f"{target.name} 的头发变长到肩膀附近了。"
        if updated == 201:
            return f"{target.name} 的头发已经长到了腰间。"
        return None






    def _apply_daily_invading_hero_favor_decay(self) -> List[str]:
        for target in self.interpreter.vars.chars[1:]:
            if int(target.cflag.get(1, 0)) != 2:
                continue
            current_favor = int(target.cflag.get(2, 0))
            if current_favor <= 100:
                continue
            target.cflag[2] = max(0, current_favor - random.randint(0, 99))
        return []






    def _apply_daily_karma_adjustments(self) -> List[str]:
        for target in self.interpreter.vars.chars[1:]:
            self._apply_character_daily_karma_adjustment(target)
        return []






    def _apply_daily_marriage_life(self) -> List[str]:
        messages: List[str] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if not self._can_apply_marriage_daily(idx, char):
                continue
            char.cflag[602] = int(char.cflag.get(602, 0)) + 1
            messages.append(f"{char.name} 的结婚生活又向前推进了一天。")
            pause_messages = self._apply_marriage_daily_pregnancy_pause(char)
            if pause_messages:
                messages.extend(pause_messages)
                continue
            messages.extend(self._apply_marriage_daily_intimacy(idx, char))
            self._apply_marriage_daily_conception_followup(char)
            messages.extend(self._apply_marriage_daily_lactation_income(char))
        return messages






    def _apply_daily_mazoku_transformation_checks(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            if target.talent.get(274, 0):
                continue
            if int(target.talent.get(314, 0)) == 9:
                continue
            if not all(target.talent.get(talent_id, 0) for talent_id in [244, 245, 246, 247]):
                continue
            target.talent[321] = int(target.talent.get(314, 0))
            if int(target.abl.get(11, 0)) >= 3:
                target.talent[322] = 152 if target.talent.get(76, 0) else 132
                target.talent[91] = 1
                target.talent[481] = 1
                target.talent[314] = 9
                messages.extend(
                    [
                        "全身充满了浓厚的魔力………",
                        f"{target.name}被深度改造，舍弃了原来的种族，",
                        f"成为出色的【魔族・{self._get_item_name(target.talent[322])}】了。",
                        f"{target.name}的肉体上散发出致命的诱惑，获得了【魅惑】……",
                        f"{target.name}学会了如何用自己的肉体作为武器。获得了【诱惑】。",
                        "",
                    ]
                )
            else:
                target.talent[322] = 140
                target.talent[482] = 1
                target.talent[314] = 9
                messages.extend(
                    [
                        "全身充满了浓厚的魔力………",
                        f"{target.name}被深度改造，舍弃了原来的种族，",
                        f"成为出色的【魔族・{self._get_item_name(target.talent[322])}】了。",
                        f"{target.name}学会了如何破坏敌人防护。获得了【铠破坏】。",
                        "",
                    ]
                )
        return messages






    def _apply_daily_monster_summon_event(self) -> List[str]:
        ok, message = self._apply_monster_summon(weak_mode=False)
        return [message] if ok and message else []






    def _apply_daily_omorashi_talent_checks(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            if target.talent.get(57, 0):
                continue
            threshold = 15 if target.talent.get(132, 0) else 40
            if int(target.exp.get(31, 0)) < threshold:
                continue
            messages.extend(self._apply_omorashi_talent_award(target))
        return messages






    def _apply_daily_pregnancy_awareness(self) -> List[str]:
        messages: List[str] = []
        for target in self._iter_pregnancy_daily_targets():
            if not self._can_character_awaken_pregnancy(target):
                continue
            source = int(target.cflag.get(102, 0))
            awareness_lines, clear_monster_father = self._build_pregnancy_awareness_lines(target, source)
            messages.extend(awareness_lines)
            messages.extend(self._get_pregnancy_awareness_kojo_lines(target, source))
            if source in (5, 6):
                target.exp[62] = int(target.exp.get(62, 0)) + 1
                if not clear_monster_father:
                    target.cflag[112] = 0
            messages.extend(self._grant_pregnancy_talents(target))
            self._apply_pregnancy_breast_growth(target)
            messages.extend(self._apply_pregnancy_status_change(target))
            target.cflag[271] = 1
        return messages






    def _apply_daily_pregnancy_main_flow(self) -> List[str]:
        messages: List[str] = []
        today = self._get_pregnancy_current_day()
        player = self._get_player()
        allow_late_month_training = bool(self.interpreter.vars.get_flag(5, 0) & (1 << 10))

        for target in self._iter_pregnancy_daily_targets():
            if self._can_character_awaken_pregnancy(target):
                source = int(target.cflag.get(102, 0))
                awareness_lines, clear_monster_father = self._build_pregnancy_awareness_lines(target, source)
                messages.extend(awareness_lines)
                messages.extend(self._get_pregnancy_awareness_kojo_lines(target, source))
                if source in (5, 6):
                    target.exp[62] = int(target.exp.get(62, 0)) + 1
                    if not clear_monster_father:
                        target.cflag[112] = 0
                messages.extend(self._grant_pregnancy_talents(target))
                self._apply_pregnancy_breast_growth(target)
                messages.extend(self._apply_pregnancy_status_change(target))
                target.cflag[271] = 1
                continue

            if not (target.talent.get(153, 0) or target.talent.get(154, 0)):
                continue

            due_day = self._get_pregnancy_due_day(target)
            if due_day <= 0:
                continue

            status = int(target.cflag.get(1, 0))
            if due_day - 3 == today:
                messages.extend(self._apply_pregnancy_room_transfer_due_in_three_days(target, status, allow_late_month_training))
                continue

            if due_day == today:
                self._apply_daily_due_birth_event(target, player, today, messages)
                continue

            if 0 <= due_day - today <= 3 and not allow_late_month_training and status == 0:
                self._move_character_to_nursery(target, previous_state=status)
                messages.append(f"{target.name} 被移动到了育儿室中……")
                continue

            if due_day + 5 == today:
                messages.extend(self._apply_child_care_depart(target))
                continue

            if target.talent.get(154, 0):
                messages.append(f"{target.name} 在育儿室照顾孩子……")
                messages.extend(self._get_child_care_visit_kojo_lines(target))
                target.cflag[273] = 1
                continue

            if status == 10 and target.talent.get(153, 0):
                messages.append(f"{target.name} 在育儿室里等待生产……")
                messages.extend(self._get_child_care_visit_kojo_lines(target))
                target.cflag[273] = 1

        return messages






    def _apply_daily_pregnancy_room_transfers(self) -> List[str]:
        messages: List[str] = []
        allow_late_month_training = bool(self.interpreter.vars.get_flag(5, 0) & (1 << 10))
        today = self._get_pregnancy_current_day()
        for target in self._iter_pregnancy_daily_targets():
            if not self._should_process_pregnancy_room_transfer(target):
                continue
            messages.extend(self._apply_pregnancy_room_transfer_for_target(target, today, allow_late_month_training))
        return messages






    def _apply_daily_prestige_decay(self) -> List[str]:
        previous = self._get_prestige_value()
        self._add_prestige_value(-2)
        current = self._get_prestige_value()
        if current == previous:
            return []
        return [f"威望值自然变化为 {current}。"]






    def _apply_daily_pubic_hair_growth(self, target: Character) -> Optional[str]:
        current = int(target.talent.get(310, 0))
        maximum = int(target.talent.get(311, 0))
        if current >= maximum or int(target.talent.get(125, 0)) != 0 or current > 200:
            return None

        target.talent[310] = current + 1
        updated = int(target.talent.get(310, 0))
        if updated >= maximum:
            target.talent[310] = maximum
            updated = maximum

        growth_messages = {
            2: f"{target.name} 的阴部开始长出汗毛。",
            21: f"{target.name} 的阴部汗毛变得更明显了。",
            51: f"{target.name} 的阴部逐渐覆上了细毛。",
            101: f"{target.name} 的阴部已经长出了成片的嫩毛。",
            151: f"{target.name} 的阴部开始长出更硬的毛发。",
            201: f"{target.name} 的阴毛已经完全茂盛起来了。",
        }
        return growth_messages.get(updated)






    def _apply_daily_soul_dislocation_checks(self) -> List[str]:
        messages: List[str] = []
        for target in self.interpreter.vars.chars[1:]:
            level = self._get_character_ex_talent(target, 0)
            if level <= 0:
                continue
            decay_roll = min(3, level)
            if random.randint(0, decay_roll) != 0:
                continue
            next_level = max(0, level - 1)
            self._set_character_ex_talent(target, 0, next_level)
            if next_level == 0:
                messages.append(f"{target.name} 从【灵魂错位】中恢复了。")
        return messages






    def _apply_endcheck_character_flags(self):
        messages: List[str] = []
        tracked = self._get_endcheck_tracked_character_flags()
        self._apply_endcheck_tracked_character_flags(tracked)
        self._advance_departed_story_aftermath_flags()
        spade = self._find_character_by_template_id(21)
        if spade is not None:
            self._apply_spade_endcheck(spade, messages)
        square = self._find_character_by_template_id(22)
        if square is not None:
            self._apply_square_endcheck(square)
        godness = self._find_character_by_template_id(33)
        if godness is not None or int(self.interpreter.vars.globals.get(2810, 0)) >= 500:
            if godness is not None:
                self._apply_godness_endcheck(godness)
            else:
                self._sync_godness_post_escape_progress()
        princess = self._find_character_by_template_id(35)
        if princess is not None:
            self._apply_princess_endcheck(princess)
        return messages






    def _apply_endcheck_characters(self):
        """Apply character-specific ending checks.
        Corresponds to ERB @ENDCHECKCHARA and its subroutines.
        """
        v = self.interpreter.vars

        # Character template IDs to their flag mappings
        char_checks = [
            (17, 2805),  # 玛奥
            (20, 2813),  # 金红桃
            (21, 2814),  # 银黑桃
            (22, 2811),  # 黑方片
            (23, 2812),  # 白梅花
            (24, 2806),  # 莉莉
            (31, 2808),  # 琼
            (32, 2809),  # 普林希斯
            (35, 2807),  # 菲娅
        ]

        for template_id, flag_id in char_checks:
            char = self._find_character_by_template_id(template_id)
            if char is None:
                continue
            current = int(v.globals.get(flag_id, 0))

            # Check love/lust talent to set initial route
            if current == 0:
                if char.talent.get(85, 0) == 1:
                    v.globals[flag_id] = 10
                elif char.talent.get(76, 0) == 1:
                    v.globals[flag_id] = 20

        # Special handling for 嘉德 (template 33)
        char_33 = self._find_character_by_template_id(33)
        if char_33 is not None:
            current_2810 = int(v.globals.get(2810, 0))
            if char_33.talent.get(76, 0) == 1 and int(char_33.cflag.get(2, 0)) >= 2000 and current_2810 < 10:
                v.globals[2810] = 110
                char_33.cflag[515] = 0

        # Special handling for 葵希罗 (template 34, uses FLAG not GLOBAL)
        char_34 = self._find_character_by_template_id(34)
        if char_34 is not None:
            current_2815 = int(v.flags.get(2815, 0))
            if current_2815 == 0:
                if char_34.talent.get(85, 0) == 1:
                    v.flags[2815] = 10
                elif char_34.talent.get(76, 0) == 1:
                    v.flags[2815] = 20

        # Special handling for 菲娅 (template 35)
        char_35 = self._find_character_by_template_id(35)
        if char_35 is not None:
            current_2807 = int(v.globals.get(2807, 0))
            if current_2807 == 0:
                v.globals[2807] = 10

    # =====================================================================
    # EQUIP (装备系统)
    # Corresponds to ERB EQUIP.ERB
    # =====================================================================

    _EQUIP_RING_NAMES = {
        0: "装饰戒指",
        1: "破坏戒指",
        2: "守护戒指",
        3: "加速戒指",
        4: "再生戒指",
        5: "意志戒指",
        6: "欲望戒指",
        7: "怪力戒指",
        8: "强韧戒指",
        9: "支配戒指",
        10: "成长戒指",
        11: "虚弱戒指",
        12: "钝重戒指",
        13: "死亡戒指",
        14: "衰弱戒指",
        15: "洗脑戒指",
        16: "陷阱回避戒指",
        17: "侵攻戒指",
        18: "结界戒指",
        19: "试炼戒指",
        20: "不幸戒指",
    }

    _EQUIP_WEAPON_NAMES = {
        40: "剑",
        41: "法杖",
        42: "鞭",
        43: "匕首",
        44: "手里剑",
        45: "箭",
        46: "权杖",
        47: "战锤",
        48: "镰刀",
        49: "触手",
        50: "细剑",
        51: "偃月刀",
        52: "指虎",
    }

    _EQUIP_PREFIX_NAMES = {
        1: "巨型",
        2: "剧毒",
        3: "致命",
        4: "强击",
        5: "烈火",
        6: "寒冰",
        7: "雷霆",
        8: "魔导",
        9: "暗黑",
    }

    _EQUIP_EFFECT_NAMES = {
        0: "无",
        1: "伤害增加",
        2: "装备强化",
        3: "速度UP",
        4: "HP回复",
        5: "气力回复",
        6: "容易陷落",
        7: "攻击变动",
        8: "防御变动",
        9: "支配",
        10: "经验值增加",
        11: "装备劣化",
        12: "速度减少",
        13: "HP·气力减少",
        14: "攻击·防御减少",
        15: "洗脑",
        16: "陷阱回避",
        17: "侵攻强化",
        18: "结界",
        19: "侵攻弱化＆结界禁止",
        20: "陷阱诱发",
    }

    _EQUIP_WEAPON_DATABASE = {
        40: {"damage": 100, "ammo": 0, "miss": 0, "spirit_recover": 0, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        41: {"damage": 80, "ammo": 0, "miss": 0, "spirit_recover": 20, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        42: {"damage": 80, "ammo": 0, "miss": 0, "spirit_recover": 0, "combo": 0, "def_dmg": 120, "ammo_empty": 0, "spirit_dmg": 100},
        43: {"damage": 70, "ammo": 0, "miss": 0, "spirit_recover": 0, "combo": 30, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        44: {"damage": 100, "ammo": 1, "miss": 0, "spirit_recover": 0, "combo": 30, "def_dmg": 100, "ammo_empty": 1, "spirit_dmg": 100},
        45: {"damage": 150, "ammo": 1, "miss": 0, "spirit_recover": 0, "combo": 0, "def_dmg": 100, "ammo_empty": 2, "spirit_dmg": 100},
        46: {"damage": 120, "ammo": 0, "miss": 10, "spirit_recover": 0, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        47: {"damage": 150, "ammo": 0, "miss": 30, "spirit_recover": 0, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        48: {"damage": 100, "ammo": 0, "miss": 10, "spirit_recover": 20, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        49: {"damage": 100, "ammo": 0, "miss": 0, "spirit_recover": -10, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 120},
        50: {"damage": 80, "ammo": 0, "miss": 0, "spirit_recover": 0, "combo": 50, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        51: {"damage": 135, "ammo": 0, "miss": 20, "spirit_recover": 0, "combo": 0, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
        52: {"damage": 65, "ammo": 0, "miss": 0, "spirit_recover": 0, "combo": 40, "def_dmg": 100, "ammo_empty": 0, "spirit_dmg": 100},
    }

    _EQUIP_RING_DATABASE = {
        0: {"effect": 0, "price": 100, "cursed": False, "special": 0},
        1: {"effect": 1, "price": 10000, "cursed": False, "special": 0},
        2: {"effect": 2, "price": 10000, "cursed": False, "special": 0},
        3: {"effect": 3, "price": 50000, "cursed": False, "special": 0},
        4: {"effect": 4, "price": 20000, "cursed": False, "special": 0},
        5: {"effect": 5, "price": 20000, "cursed": False, "special": 0},
        6: {"effect": 6, "price": 5000, "cursed": True, "special": 0},
        7: {"effect": 7, "price": 8000, "cursed": False, "special": 0},
        8: {"effect": 8, "price": 8000, "cursed": False, "special": 0},
        9: {"effect": 9, "price": 100000, "cursed": False, "special": 0},
        10: {"effect": 10, "price": 70000, "cursed": False, "special": 0},
        11: {"effect": 11, "price": 1000, "cursed": True, "special": 0},
        12: {"effect": 12, "price": 1000, "cursed": True, "special": 0},
        13: {"effect": 13, "price": 1000, "cursed": True, "special": 0},
        14: {"effect": 14, "price": 1000, "cursed": True, "special": 0},
        15: {"effect": 15, "price": 1000, "cursed": True, "special": 0},
        16: {"effect": 16, "price": 1000, "cursed": False, "special": 0},
        17: {"effect": 17, "price": 1000, "cursed": False, "special": 0},
        18: {"effect": 18, "price": 1000, "cursed": False, "special": 0},
        19: {"effect": 19, "price": 1000, "cursed": True, "special": 0},
        20: {"effect": 20, "price": 1000, "cursed": True, "special": 0},
    }






    def _apply_endcheck_main_flags(self):
        total_days = self._get_total_day_count()
        current_2801 = int(self.interpreter.vars.globals.get(2801, 0))
        if total_days == 500 and (current_2801 == 0 or current_2801 >= 90):
            self.interpreter.vars.globals[2801] = 99

        if self.interpreter.vars.money > int(self.interpreter.vars.globals.get(4444, 0)) + 8766:
            self.interpreter.vars.globals[2802] = 10

        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx < 0:
                continue
            if int(char.cflag.get(9, 0)) >= 5000 and int(char.cflag.get(1, 0)) == 0:
                self.interpreter.vars.globals[2803] = idx

        player = self._get_player()
        if player is not None and int(player.cflag.get(9, 0)) >= 1500:
            self.interpreter.vars.globals[2804] = 10

        if self._get_prestige_value() <= 0:
            self.interpreter.vars.set_flag(2816, 10)






    def _apply_endcheck_minimal(self) -> List[str]:
        self._refresh_story_presence_flags()
        self._apply_endcheck_main_flags()
        messages = self._apply_endcheck_character_flags()
        self._apply_ending_event_triggers(messages)
        if int(self.interpreter.vars.get_flag(2816, 0)) == 10:
            messages.append("威望值已经降到危险区域，反叛主线标记被触发。")
        return messages






    def _apply_endcheck_tracked_character_flags(self, tracked: Dict[int, int]) -> None:
        for template_id, flag_id in tracked.items():
            current = int(self.interpreter.vars.get_flag(flag_id, 0)) if flag_id == 2815 else int(self.interpreter.vars.globals.get(flag_id, 0))
            if current != 0:
                continue
            char = self._find_character_by_template_id(template_id)
            if char is None:
                continue
            if char.talent.get(85, 0) == 1:
                if flag_id == 2815:
                    self.interpreter.vars.set_flag(flag_id, 10)
                else:
                    self.interpreter.vars.globals[flag_id] = 10
            elif char.talent.get(76, 0) == 1:
                if flag_id == 2815:
                    self.interpreter.vars.set_flag(flag_id, 20)
                else:
                    self.interpreter.vars.globals[flag_id] = 20






    def _apply_level_up(self, idx: int) -> int:
        if idx < 0 or idx >= len(self.interpreter.vars.chars):
            return 0

        char = self.interpreter.vars.chars[idx]
        leveled = 0
        while True:
            required_exp = self._get_level_up_required_exp(idx, char)
            if int(char.exp.get(80, 0)) < required_exp:
                break
            char.exp[80] = int(char.exp.get(80, 0)) - required_exp
            self._apply_single_level_up(idx, char)
            leveled += 1

        if leveled > 0 and char.talent.get(291, 0) and int(char.cflag.get(9, 0)) >= 30:
            char.talent[291] = 0
        return leveled






    def _apply_level_up_growth_pair(self, char: Character, amount: int):
        self._add_level_up_growth(char, 13, amount)
        self._add_level_up_growth(char, 14, amount)






    def _apply_level_up_maxbase_growth(self, char: Character):
        char.maxbase[0] = int(char.maxbase.get(0, 0)) + 10
        char.maxbase[1] = int(char.maxbase.get(1, 0)) + 10






    def _apply_level_up_random_growth(self, char: Character, upper: int):
        self._apply_level_up_growth_pair(char, random.randrange(upper))






    def _apply_level_up_species_growth(self, char: Character):
        species_id = int(char.talent.get(314, 0))
        if species_id == 5:
            self._apply_level_up_random_growth(char, 2)
        if species_id == 11:
            self._add_level_up_growth(char, 14, random.randrange(2))






    def _apply_level_up_talent_growth(self, char: Character, talent_id: int, upper: int):
        if char.talent.get(talent_id, 0):
            self._apply_level_up_random_growth(char, upper)






    def _apply_life_cradle_conflict_rules(self, target: Character, talent_id: int):
        conflict_pairs = [
            (0, 75), (30, 75), (10, 12), (11, 13), (13, 18), (14, 16), (15, 17), (17, 18),
            (20, 23), (21, 23), (22, 23), (20, 63), (21, 63), (22, 63), (23, 24), (25, 26),
            (27, 28), (30, 31), (32, 33), (35, 36), (40, 41), (42, 43), (44, 45), (50, 51),
            (61, 62), (62, 64), (70, 71), (74, 150), (76, 85), (74, 75), (74, 77), (74, 78),
            (75, 77), (75, 78), (77, 78), (122, 78), (79, 80), (79, 81), (79, 82), (79, 122),
            (80, 81), (80, 82), (81, 82), (99, 100), (101, 102), (103, 104), (105, 106),
            (103, 122), (104, 122), (107, 108), (111, 112), (109, 110), (109, 114), (109, 116),
            (119, 109), (119, 116), (119, 114), (119, 110), (122, 109), (122, 110), (122, 114),
            (122, 116), (122, 119), (110, 114), (110, 116), (114, 116), (121, 122), (153, 154),
            (99, 263), (153, 122), (154, 122), (130, 122), (155, 122), (157, 122), (155, 156),
            (10, 161), (26, 161), (60, 150), (0, 122), (248, 256), (244, 253), (244, 255),
            (253, 255), (259, 260),
        ]
        for left, right in conflict_pairs:
            if talent_id not in (left, right):
                continue
            if target.talent.get(left, 0) and target.talent.get(right, 0):
                target.talent[left] = 0
                target.talent[right] = 0
                target.talent[talent_id] = 1






    def _apply_life_cradle_custom_name(self, new_char: Character) -> tuple[bool, str]:
        custom_name = self._prompt_choice("新建人物的名字（留空保留模板名）>> ")
        if not custom_name:
            return True, ""
        if len(custom_name) > 16:
            return False, "名字太长，请使用全角八字以下的名字。"
        new_char.name = custom_name
        new_char.callname = custom_name
        return True, ""






    def _apply_life_cradle_first_experience(self, target: Character, code: int, partner_name: str = ""):
        target.cflag[15] = code
        target.cstr[3] = partner_name if code > 0 else ""






    def _apply_life_cradle_first_experience_random(self, target: Character) -> tuple[bool, str]:
        self._apply_life_cradle_first_experience(target, -1)
        return True, "初体验对象：随机生成"






    def _apply_life_cradle_first_kiss(self, target: Character, code: int, partner_name: str = ""):
        target.cflag[16] = code
        target.cstr[4] = partner_name if code > 0 else ""






    def _apply_life_cradle_first_kiss_random(self, target: Character) -> tuple[bool, str]:
        self._apply_life_cradle_first_kiss(target, -1)
        return True, "初吻对象：随机生成"






    def _apply_life_cradle_first_kiss_wild_option(self, target: Character) -> Optional[tuple[bool, str]]:
        print(" 初吻位置: [1] 肛门 [2] 阴茎 [3] 嘴")
        site = self._prompt_choice()
        if site == "1":
            self._apply_life_cradle_first_kiss(target, 996)
        elif site == "2":
            self._apply_life_cradle_first_kiss(target, 997)
        elif site == "3":
            self._apply_life_cradle_first_kiss(target, 998)
        else:
            print("输入错误，请重新开始。")
            return None
        return True, self._summarize_life_cradle_first_kiss(target)






    def _apply_life_cradle_gender(self, target: Character, gender_choice: str):
        target.talent[121] = 1 if gender_choice == "3" else 0
        target.talent[122] = 1 if gender_choice == "1" else 0
        if not target.talent.get(121, 0) and not target.talent.get(122, 0):
            target.talent[1] = 0






    def _apply_life_cradle_look_field(self, target: Character, field_id: int) -> tuple[bool, str]:
        for page in self._get_life_cradle_look_pages():
            for field in page["fields"]:
                if int(field["field_id"]) != field_id:
                    continue
                talent_id = int(field["talent_id"])
                options = self._get_life_cradle_field_options(talent_id)
                if not options:
                    return False, "当前字段没有可用选项。"
                print(f"\n设置 {field['name']}")
                for value in options:
                    print(f" [{value}] {self._format_life_cradle_field_value(talent_id, value)}")
                choice = self._prompt_choice()
                try:
                    selected = int(choice)
                except ValueError:
                    return False, "已取消。"
                if selected not in options:
                    return False, "无效值"
                target.talent[talent_id] = selected
                if talent_id == 314 and selected != 9:
                    target.talent[220] = 0
                return True, f"{field['name']} 已更新。"
        return False, "无效值"






    def _apply_life_cradle_post_creation(self, new_char: Character):
        new_char.cflag[1] = 0
        new_char.cflag[9] = 1
        new_char.exp[80] = 0
        if new_char.talent.get(153, 0) or new_char.talent.get(341, 0) or new_char.talent.get(342, 0) or new_char.talent.get(343, 0):
            self._set_pregnancy_due_day(new_char, 10 + random.randint(0, 5))
            new_char.cflag[111] = 0
        self._append_character(new_char)






    def _apply_life_cradle_post_toggle_talent_rules(self, target: Character, talent_id: int) -> None:
        if talent_id in {109, 110, 114, 116, 119}:
            self._clear_life_cradle_mutually_exclusive_talents(target, talent_id, [109, 110, 114, 116, 119])

        if 160 <= talent_id <= 174 or talent_id in {166, 172, 173, 174}:
            self._clear_life_cradle_mutually_exclusive_talents(target, talent_id, [160, 161, 162, 163, 164, 166, 172, 173, 174])

        if 200 <= talent_id <= 220:
            self._clear_life_cradle_mutually_exclusive_talents(target, talent_id, list(range(200, 221)))

        if talent_id == 220:
            target.talent[314] = 9
        elif target.talent.get(314, 0) != 9:
            target.talent[220] = 0

        if target.talent.get(314, 0) == 5:
            target.talent[264] = 1
        if not target.talent.get(121, 0) and not target.talent.get(122, 0):
            target.talent[1] = 0
        if target.talent.get(308, 0) <= 100:
            target.talent[115] = 0






    def _apply_life_cradle_talent_toggle(self, target: Character, talent_id: int) -> tuple[bool, str]:
        if talent_id < 0 or talent_id > 500:
            return False, "无效值"
        target.talent[talent_id] = 0 if target.talent.get(talent_id, 0) else 1
        self._apply_life_cradle_conflict_rules(target, talent_id)
        self._apply_life_cradle_post_toggle_talent_rules(target, talent_id)
        return True, f"{self._get_talent_name(talent_id)} 已切换。"






    def _apply_new_day_character_role_flows(self) -> List[str]:
        messages: List[str] = []
        for idx, target in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            messages.extend(self._apply_character_day_role_events(target))
        return messages






    def _apply_new_day_character_state_post_flows(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_daily_invading_hero_favor_decay())
        messages.extend(self._apply_daily_body_hair_growth())
        messages.extend(self._apply_daily_auto_execution())
        return messages






    def _apply_new_day_character_state_pre_flows(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._cleanup_invalid_dungeon_town_lover_links())
        messages.extend(self._cleanup_invalid_marriage_links())
        for char in self.interpreter.vars.chars:
            messages.extend(self._clear_disabled_dungeon_quest_states(char))
        messages.extend(self._apply_daily_character_daily_state_flows())
        messages.extend(self._apply_daily_marriage_life())
        messages.extend(self._process_dungeon_return_events())
        messages.extend(self._apply_daily_futanari_transformation_checks())
        messages.extend(self._apply_daily_omorashi_talent_checks())
        messages.extend(self._apply_daily_dematurity_checks())
        messages.extend(self._apply_daily_mazoku_transformation_checks())
        messages.extend(self._apply_daily_aphrodisiac_addiction_checks())
        messages.extend(self._apply_daily_soul_dislocation_checks())
        messages.extend(self._clear_daily_ovulation_drug_effects())
        return messages






    def _apply_new_day_family_state_flows(self) -> List[str]:
        return self._apply_daily_pregnancy_main_flow()






    def _apply_new_day_global_state_flows(self) -> List[str]:
        return []






    def _apply_new_day_operational_flows(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_daily_cursed_ring_conversion())
        messages.extend(self._apply_daily_monster_summon_event())
        messages.extend(self._apply_daily_dungeon_room_operations())
        return messages






    def _apply_new_day_world_flows(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_new_day_operational_flows())
        messages.extend(self._apply_new_day_global_state_flows())
        return messages






    def _apply_onesho_bedwetting_event(self, char: Character, messages: List[str]) -> None:
        messages.append(f"{char.name} 尿床了。")
        char.exp[31] = char.exp.get(31, 0) + 1
        self._apply_onesho_cloth_soiling(char)
        if char.cflag.get(1, 0) != 0:
            return
        if char.abl.get(17, 0) + char.abl.get(21, 0) >= 8:
            char.juel[8] = char.juel.get(8, 0) + 1000
            if len(self.interpreter.vars.chars) >= 3:
                messages.append(f"{char.name} 甚至把自己尿床的事在早餐时向众人坦白了。")
            else:
                messages.append(f"{char.name} 主动把自己尿床的事报告给了你。")






    def _apply_onesho_catheter_event(self, char: Character, messages: List[str]) -> None:
        obedience = int(char.abl.get(10, 0))
        if obedience < 3:
            gain = random.choice((10, 20))
            jewel_id = random.choice((8, 9))
            char.juel[jewel_id] = char.juel.get(jewel_id, 0) + gain
            messages.append(f"{char.name} 装着导尿配件过夜时漏尿了，感到强烈屈辱。")
            return
        if obedience < 6:
            messages.append(f"{char.name} 装着导尿配件时漏尿了，但因为没有弄脏周围而很快平静下来。")
            return
        gain = random.choice((10, 20, 30))
        char.juel[4] = char.juel.get(4, 0) + gain
        messages.append(f"{char.name} 借助导尿配件平稳度过了一夜，对这种状态的抗拒又淡了一些。")
        if any(char.talent.get(tid, 0) == 1 for tid in (72, 80, 88, 89)):
            if char.talent.get(60, 0) == 1:
                char.exp[10] = char.exp.get(10, 0) + 1
                char.juel[5] = char.juel.get(5, 0) + 800
                char.juel[8] = char.juel.get(8, 0) + 800
                messages.append(f"{char.name} 甚至因为导尿带来的异样刺激而自慰了一次。")
            else:
                char.juel[8] = char.juel.get(8, 0) + 300
                messages.append(f"{char.name} 羞耻地报告了这次漏尿。")






    def _apply_onesho_cloth_soiling(self, char: Character):
        char.cflag[47] = char.cflag.get(47, 0) + 1
        char.cflag[48] = max(1, char.cflag.get(48, 0))
        char.stain[3] = char.stain.get(3, 0) | 1
        char.stain[5] = char.stain.get(5, 0) | 1






    def _apply_onesho_event_for_character(self, char: Character, clothes_enabled: bool, messages: List[str]) -> None:
        if self._has_onesho_catheter_setup(char, clothes_enabled):
            if char.cflag.get(1, 0) < 2:
                self._apply_onesho_catheter_event(char, messages)
            return
        self._apply_onesho_bedwetting_event(char, messages)






    def _apply_onesho_events(self) -> List[str]:
        messages: List[str] = []
        clothes_enabled = self.interpreter.vars.get_flag(37, 0) != 0
        for idx, char in enumerate(self.interpreter.vars.chars):
            if not self._should_apply_onesho_event(idx, char):
                continue
            self._apply_onesho_event_for_character(char, clothes_enabled, messages)
        return messages






    def _build_life_cradle_look_page_field_lines(self, target: Character, page: Dict[str, Any]) -> List[str]:
        lines: List[str] = []
        for field in page["fields"]:
            talent_id = int(field["talent_id"])
            current = int(target.talent.get(talent_id, 0))
            lines.append(f" {field['name']} [{field['field_id']}] 当前: {self._format_life_cradle_field_value(talent_id, current)}")
            option_parts = [f"{value}={self._format_life_cradle_field_value(talent_id, value)}" for value in self._get_life_cradle_field_options(talent_id)[:8]]
            if option_parts:
                lines.append("   选项: " + " / ".join(option_parts))
        return lines






    def _build_life_cradle_look_page_header_lines(self, target: Character, page_index: int, price: int, total_pages: int) -> List[str]:
        return [
            f"【生命摇篮外观】 {target.name} 价值:{price} <{page_index + 1}/{total_pages}>",
            "-" * 30,
        ]






    def _build_life_cradle_look_page_lines(self, target: Character, page_index: int, price: int) -> List[str]:
        pages = self._get_life_cradle_look_pages()
        return self._build_life_cradle_paginated_page_lines(
            target,
            pages,
            page_index,
            price,
            self._build_life_cradle_look_page_header_lines,
            self._build_life_cradle_look_page_field_lines,
        )






    def _build_life_cradle_page_footer_lines(self) -> List[str]:
        return [
            " [997] 上一页",
            " [998] 下一页",
            " [999] 完成",
            " [996] 取消",
        ]






    def _build_life_cradle_page_header_lines(self, target: Character, page_index: int, price: int, total_pages: int) -> List[str]:
        return [
            f"【生命摇篮自定义】 {target.name} 价值:{price} <{page_index + 1}/{total_pages}>",
            "-" * 30,
        ]






    def _build_life_cradle_page_lines(self, target: Character, page_index: int, price: int) -> List[str]:
        pages = self._get_life_cradle_talent_pages()
        return self._build_life_cradle_paginated_page_lines(
            target,
            pages,
            page_index,
            price,
            self._build_life_cradle_page_header_lines,
            self._build_life_cradle_page_section_lines,
        )






    def _build_life_cradle_page_section_lines(self, target: Character, page: Dict[str, Any]) -> List[str]:
        lines: List[str] = []
        for section in page["sections"]:
            lines.append(section["title"])
            row: List[str] = []
            for talent_id in section["ids"]:
                marker = "ON" if target.talent.get(talent_id, 0) else "--"
                row.append(f"[{talent_id}] {self._get_talent_name(talent_id)}({marker})")
                if len(row) == 3:
                    lines.append("  " + " | ".join(row))
                    row = []
            if row:
                lines.append("  " + " | ".join(row))
        return lines






    def _build_life_cradle_paginated_page_lines(
        self,
        target: Character,
        pages: List[Dict[str, Any]],
        page_index: int,
        price: int,
        header_builder,
        content_builder,
    ) -> List[str]:
        page = pages[page_index]
        lines = header_builder(target, page_index, price, len(pages))
        lines.extend(content_builder(target, page))
        lines.extend(self._build_life_cradle_page_footer_lines())
        return lines






    def _build_life_cradle_talent_page(self, title: str, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"title": title, "sections": sections}






    def _build_life_cradle_talent_section(self, title: str, ids: List[int]) -> Dict[str, Any]:
        return {"title": title, "ids": ids}






    def _build_life_cradle_templates(self) -> List[Dict[str, Any]]:
        templates: List[Dict[str, Any]] = []
        for template_id in self._get_life_cradle_template_ids():
            char = self._get_character_template_baseline(template_id)
            if char is None:
                continue
            category = "勇者" if 1 <= template_id <= 16 else "精英"
            templates.append({
                "id": template_id,
                "name": char.name,
                "category": category,
                "character": char,
            })
        return templates






    def _get_daily_cursed_ring_base_codes(self) -> List[int]:
        return [13, 14, 19, 20, 12, 11, 6, 15]






    def _get_daily_enemy_spawn_attempts(self) -> int:
        total_days = self._get_total_day_count()
        attempts = 1
        if total_days >= 100:
            attempts += 1
        if total_days >= 300:
            attempts += 1
        if total_days >= 500:
            attempts += 1
        active_effect = max(0, self._get_video_campaign_active_count())
        if active_effect <= 0:
            return attempts

        if total_days >= 500:
            reduction = 4
            max_extra = 8
        elif total_days >= 300:
            reduction = 3
            max_extra = 9
        elif total_days >= 100:
            reduction = 2
            max_extra = 10
        else:
            reduction = 2
            max_extra = 11

        extra = active_effect - reduction
        if extra <= 0:
            extra = 1
        if extra > max_extra:
            extra = max_extra
        attempts += extra
        return attempts






    def _get_daily_enemy_spawn_template_ids(self) -> List[int]:
        candidates: List[int] = []
        duplicate_allowed = self._is_duplicate_hero_entry_allowed()
        for template_id in range(1, 17):
            if not self._has_character_template(template_id):
                continue
            if not duplicate_allowed and self._find_character_by_template_id(template_id) is not None:
                continue
            candidates.append(template_id)
        return candidates






    def _get_daily_enter_enemy_loop_count(self, total_days: int, ex_flag_9012: int) -> int:
        if ex_flag_9012 <= 0:
            return 0

        if total_days >= 100:
            sengen = ex_flag_9012 - 2
            sengen_max = 12 - 2
        elif total_days >= 300:
            sengen = ex_flag_9012 - 3
            sengen_max = 12 - 3
        elif total_days >= 500:
            sengen = ex_flag_9012 - 4
            sengen_max = 12 - 4
        else:
            sengen = ex_flag_9012 - 2
            sengen_max = 12 - 1

        if sengen > sengen_max:
            sengen = sengen_max

        if sengen <= 0:
            return 1
        return sengen






    def _get_life_cradle_capacity_limit(self) -> int:
        if self.interpreter.vars.get_flag(82, 0) == 0:
            return 60
        if self.interpreter.vars.get_flag(87, 0) == 0 and self.interpreter.vars.get_flag(89, 0) == 0 and self.interpreter.vars.get_flag(91, 0) == 0:
            return 65
        if (
            self.interpreter.vars.get_flag(87, 0) * self.interpreter.vars.get_flag(89, 0) == 0
            and self.interpreter.vars.get_flag(89, 0) * self.interpreter.vars.get_flag(91, 0) == 0
            and self.interpreter.vars.get_flag(91, 0) * self.interpreter.vars.get_flag(87, 0) == 0
        ):
            return 70
        if (
            self.interpreter.vars.get_flag(87, 0) == 0
            or self.interpreter.vars.get_flag(89, 0) == 0
            or self.interpreter.vars.get_flag(91, 0) == 0
        ):
            return 75
        if self.interpreter.vars.get_flag(92, 0) < 15:
            return 80
        return 999






    def _get_life_cradle_field_options(self, talent_id: int) -> List[int]:
        values = sorted(int(value) for value in self.character_template_catalog.get("values", {}).get(talent_id, set()) if int(value) >= 0)
        if talent_id == 302 and not values:
            values = [2, 102, 202]
        if talent_id == 308 and not values:
            values = [2, 102, 202]
        if not values and talent_id in self.talent_catalog:
            values = [0, 1]
        return values






    def _get_life_cradle_look_pages(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "外观页 1/2",
                "fields": [
                    {"field_id": 1100, "talent_id": 300, "name": "发色"},
                    {"field_id": 1200, "talent_id": 304, "name": "发型"},
                    {"field_id": 1300, "talent_id": 302, "name": "头发长度"},
                    {"field_id": 1400, "talent_id": 301, "name": "头发状态"},
                    {"field_id": 1500, "talent_id": 303, "name": "头发修剪方式"},
                    {"field_id": 2100, "talent_id": 305, "name": "眼型"},
                    {"field_id": 2200, "talent_id": 306, "name": "瞳色"},
                    {"field_id": 2300, "talent_id": 307, "name": "唇型"},
                    {"field_id": 2400, "talent_id": 308, "name": "体型"},
                    {"field_id": 2500, "talent_id": 310, "name": "阴毛状态"},
                    {"field_id": 2600, "talent_id": 309, "name": "乳头"},
                ],
            },
            {
                "title": "外观页 2/2",
                "fields": [
                    {"field_id": 3100, "talent_id": 312, "name": "魅力点"},
                    {"field_id": 3200, "talent_id": 313, "name": "癖好"},
                    {"field_id": 3300, "talent_id": 317, "name": "喜欢的东西"},
                    {"field_id": 4100, "talent_id": 315, "name": "成为勇者前的生活"},
                    {"field_id": 4200, "talent_id": 316, "name": "成为勇者的契机"},
                    {"field_id": 100, "talent_id": 314, "name": "种族"},
                    {"field_id": 200, "talent_id": 319, "name": "精英种族"},
                ],
            },
        ]






    def _get_life_cradle_master_kiss_sites(self) -> List[int]:
        player = self._get_player()
        options = [1]
        if player is not None and (player.talent.get(121, 0) or player.talent.get(122, 0)):
            options.append(201)
        if player is None or not player.talent.get(122, 0):
            options.append(301)
        options.append(401)
        return options






    def _get_life_cradle_talent_pages(self) -> List[Dict[str, Any]]:
        return [
            self._build_life_cradle_talent_page(
                "素质页 1/3",
                [
                    self._build_life_cradle_talent_section("基本素质", list(range(0, 10))),
                    self._build_life_cradle_talent_section("性格", list(range(10, 20))),
                    self._build_life_cradle_talent_section("性态度", list(range(20, 30))),
                    self._build_life_cradle_talent_section("少女心", list(range(30, 40))),
                    self._build_life_cradle_talent_section("体质", list(range(40, 50))),
                    self._build_life_cradle_talent_section("技术", list(range(50, 60))),
                    self._build_life_cradle_talent_section("洁癖度", list(range(60, 65))),
                    self._build_life_cradle_talent_section("正直度", list(range(69, 74))),
                    self._build_life_cradle_talent_section("特殊性癖", list(range(74, 79))),
                ],
            ),
            self._build_life_cradle_talent_page(
                "素质页 2/3",
                [
                    self._build_life_cradle_talent_section("性癖", list(range(79, 90))),
                    self._build_life_cradle_talent_section("魅力", list(range(91, 99))),
                    self._build_life_cradle_talent_section("身体特征", list(range(99, 117)) + [119]),
                    self._build_life_cradle_talent_section("混杂", [117, 118, 121] + list(range(122, 160))),
                    self._build_life_cradle_talent_section("性格（口上）", list(range(160, 165)) + [166, 172, 173, 174]),
                    self._build_life_cradle_talent_section("卖春相关", list(range(180, 190))),
                ],
            ),
            self._build_life_cradle_talent_page(
                "素质页 3/3",
                [
                    self._build_life_cradle_talent_section("体调不良", list(range(190, 200))),
                    self._build_life_cradle_talent_section("职业", list(range(200, 230))),
                    self._build_life_cradle_talent_section("强化素质", list(range(230, 240))),
                    self._build_life_cradle_talent_section("战斗技能", list(range(240, 270))),
                    self._build_life_cradle_talent_section("特殊素质", [talent_id for talent_id in range(270, 289) if talent_id not in {280, 281, 283}]),
                    self._build_life_cradle_talent_section("境遇", [talent_id for talent_id in range(290, 300) if talent_id != 292]),
                    self._build_life_cradle_talent_section("精英", list(range(471, 490))),
                ],
            ),
        ]






    def _get_life_cradle_template_ids(self) -> List[int]:
        return list(range(1, 17)) + list(range(201, 211))






    def advance_time(self):
        """Advance time to next turn"""
        self.interpreter.vars.time += 1
        crossed_day = self._advance_time_to_next_day_if_needed()
        if crossed_day:
            self.interpreter.vars.time = 1
        self.turn_end_processing(crossed_day)




    def turn_end_processing(self, new_day: bool = False):
        """Process end of turn"""
        day = self.interpreter.vars.day
        day_repr = f"{day[0]}:{day[1]}:{day[2]}" if isinstance(day, (list, tuple)) and len(day) >= 3 else str(day)
        print(f"【DEBUG】回合结束 - Day:{day_repr}, Time:{self.interpreter.vars.time}, MONEY:{self.interpreter.vars.money}, 角色数:{len(self.interpreter.vars.chars)}")
        campaign_active = self._get_active_campaign_id() > 0
        early_messages = self._collect_turn_end_early_messages(new_day)
        self._print_turn_end_early_messages(early_messages)
        self._clear_turn_end_rest_flag()
        self._apply_turn_end_cycle(campaign_active)
        self._finalize_turn_end_cycle(new_day, early_messages)
        self._apply_turn_end_auto_buying()
        self._clear_turn_end_selection_state()

    def do_rest(self):
        """Rest by ending the turn with the special tax bonus."""
        self._apply_rest_turn_end()



