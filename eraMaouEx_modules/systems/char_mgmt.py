from __future__ import annotations
import os
import random
import re
from collections import defaultdict
"""Module for CharMgmtMixin - 角色管理"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CharMgmtMixin:
    """Mixin providing 角色管理 methods for GameEngine"""

    def _add_character_faith(self, target: Character, delta: int):
        if target.talent.get(292, 0):
            return
        target.cflag[152] = max(0, min(100, int(target.cflag.get(152, 0)) + int(delta)))




    def _add_character_karma(self, target: Character, delta: int):
        if target.talent.get(292, 0):
            return
        target.cflag[151] = max(-200, min(200, int(target.cflag.get(151, 0)) + int(delta)))




    def _advance_character_age_year(self) -> None:
        for char in self.interpreter.vars.chars[1:]:
            if int(char.cflag.get(451, 0)) <= 0:
                self._ensure_character_body_profile(char)
            char.cflag[452] = int(char.cflag.get(452, 0)) + 1
            char.cflag[451] = self._generate_human_age_from_race_age(char.cflag[452], int(char.talent.get(314, 0)))






    def _advance_character_info_detail(self, selected_idx: int, char: Character) -> bool:
        print("\n【Character Detail】")
        print("-" * 30)
        for line in self._build_character_detail_lines(selected_idx, char):
            print(line)
        print("-" * 30)
        action_lines = self._build_character_detail_action_lines(selected_idx, char)
        if action_lines:
            for line in action_lines:
                print(line)
        print(" [100] 返回列表")
        detail_choice = self._prompt_choice()
        return self._handle_character_info_detail_action(selected_idx, char, detail_choice)




    def _advance_character_info_list(self, page: int, sort_mode: int, status_cycle: int, page_size: int) -> tuple[int, int, int, Optional[int]]:
        total_chars = max(0, len(self.interpreter.vars.chars) - 1)
        max_page = max(0, (total_chars - 1) // page_size) if total_chars else 0
        self._render_character_info_list(page, total_chars, sort_mode, status_cycle)
        sort_entries = self._get_character_info_sort_entries()
        choice = self._prompt_character_info_list_choice(sort_entries)
        return self._handle_character_info_list_choice(choice, page, max_page, sort_mode, status_cycle)



    def _advance_character_info_menu(self, page: int, sort_mode: int, status_cycle: int, page_size: int) -> tuple[int, int, int, Optional[int]]:
        return self._show_character_info_list(page, sort_mode, status_cycle, page_size)




    def _advance_character_info_selection(self, selected_idx: Optional[int]) -> bool:
        if selected_idx == -1:
            return True
        if selected_idx is None:
            return False
        char = self.interpreter.vars.chars[selected_idx]
        self._show_character_info_detail(selected_idx, char)
        return False




    def _apply_character_bitch_level_action(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._can_show_character_bitch_level(idx, char):
            return False, "当前无法设定这名角色的积极性。"
        if self._is_part_time_job_system_enabled():
            return self._set_character_part_time_level(char)
        return self._set_character_bitch_level(char)






    def _apply_character_daily_faith_adjustment(self, target: Character) -> None:
        former_life = int(target.talent.get(315, 0))
        if former_life == 12 or target.talent.get(202, 0) or target.talent.get(206, 0):
            self._add_character_faith(target, 1)
            return
        if int(target.cflag.get(152, 0)) < 30:
            self._add_character_faith(target, -1)
            return
        if random.randint(0, 3) == 0:
            self._add_character_faith(target, 1)
        elif random.randint(0, 2) == 0:
            self._add_character_faith(target, -1)






    def _apply_character_daily_karma_adjustment(self, target: Character) -> None:
        if target.talent.get(0, 0) == 0 and random.randint(0, 2) == 0:
            self._add_character_karma(target, 1)
        if target.talent.get(85, 0) and random.randint(0, 2) == 0:
            self._add_character_karma(target, 1)
        if int(target.cflag.get(1, 0)) == 2 and random.randint(0, 2) == 0:
            self._add_character_karma(target, 1)
        if random.randint(0, 1) == 0:
            self._add_character_karma(target, 1)
        else:
            self._add_character_karma(target, -1)






    def _apply_character_daily_ring_effects(self, target: Character) -> List[str]:
        messages: List[str] = []
        ring_effects = (
            self._apply_character_pink_ring_effect(target),
            self._apply_character_growth_ring_effect(target),
            self._apply_character_weakness_ring_effect(target),
            self._apply_character_domination_ring_effect(target),
            self._apply_character_gray_ring_effect(target),
        )
        for effect_messages in ring_effects:
            messages.extend(effect_messages)
        return messages






    def _apply_character_day_role_events(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_character_daily_pillory_event(target))
        messages.extend(self._apply_character_sabbath_event(target))
        messages.extend(self._apply_character_ntr_video_event(target))
        messages.extend(self._apply_character_event_video_day(target))
        self._apply_character_daily_karma_adjustment(target)
        self._apply_character_daily_faith_adjustment(target)
        return messages






    def _apply_character_detail_action(self, idx: int, char: Character, action_id: int) -> tuple[bool, str]:
        handler = self._get_character_detail_action_handler(idx, char, action_id)
        if handler is None:
            return False, "当前无法执行该操作。"
        return handler()






    def _apply_character_domination_ring_effect(self, target: Character) -> List[str]:
        strength = self._get_ring_effect_strength(target, 9)
        if strength <= 0:
            target.cflag[570] = 0
            return []
        if int(target.cflag.get(1, 0)) != 3:
            target.cflag[570] = 0
            return []

        floor = max(1, int(target.cflag.get(501, 1)))
        monster_id = (floor - 1) * 10 + 100 + random.randint(0, 4)
        if floor >= 8 and random.randint(0, 9) == 0:
            boss_id = 191 + random.randint(0, 2)
            if self._get_item_count(boss_id) > 0:
                monster_id = boss_id
        target.cflag[570] = monster_id
        return []






    def _apply_character_event_video_day(self, target: Character) -> List[str]:
        title = str(target.cstr.get(6, "")).strip()
        if int(target.cflag.get(497, 0)) == 0:
            return []
        view = int(target.cflag.get(493, 0)) // 10
        maniac = int(target.cflag.get(494, 0))
        if 0 < maniac < 100:
            view = view * (100 - maniac) // 100 + 1
        fav = (view // 100) + random.randint(0, 1)
        fav *= (maniac // 2) + 1
        if fav > view:
            fav = view
        target.cflag[495] = int(target.cflag.get(495, 0)) + view
        target.cflag[496] = int(target.cflag.get(496, 0)) + fav
        if title:
            self._add_global_money(view)
            if fav > 0:
                return [f"录制于水晶中的「{title}」在黑市上流通了起来，收入 {view} G，粉丝信 {fav} 封。"]
            return [f"录制于水晶中的「{title}」在黑市上流通了起来，收入 {view} G。"]
        return []






    def _apply_character_force_recall(self, char: Character) -> tuple[bool, str]:
        idx = self._find_character_index(char)
        if idx > 0:
            self._remove_character_from_party(idx)
        self._set_character_dungeon_return_standby_state(
            char,
            floor=max(1, int(char.cflag.get(501, 1))),
            success=bool(int(char.cflag.get(505, 0)) > 0),
        )
        return True, f"{char.name} 已被强制召回。"






    def _apply_character_gray_ring_effect(self, target: Character) -> List[str]:
        strength = self._get_ring_effect_strength(target, 15)
        if strength <= 0:
            return []

        messages = [f"{target.name} 手上的灰色戒指发出奇异的魔法波动。"]
        if int(target.talent.get(152, 0)):
            messages.extend(
                [
                    f"一个声音在 {target.name} 的脑海中不断重复，服从……服从……服从……",
                    f"然而 {target.name} 凭借强大的意志力无视了戒指的魔法。",
                ]
            )
            return messages

        if int(target.cflag.get(1, 0)) == 2:
            self._set_character_captured_standby_state(target)
            self._split_character_from_party(target)
            target.abl[10] = int(target.abl.get(10, 0)) + 1
            messages.extend(
                [
                    f"一个声音在 {target.name} 的脑海中不断重复，服从……服从……服从……",
                    f"{target.name} 的眼神变得空洞，完全忘记了讨伐魔王的事，自动向魔王军投降了。",
                    f"{target.name} 成了魔王的俘虏。",
                ]
            )
            return messages

        if int(target.abl.get(10, 0)) < strength:
            target.abl[10] = int(target.abl.get(10, 0)) + 1
            messages.extend(
                [
                    f"一个声音在 {target.name} 的脑海中不断重复，服从……服从……服从……",
                    f"{target.name} 对魔王的顺从程度增加了。",
                ]
            )
            return messages

        messages.append(f"但是戒指的魔力似乎不足以再提升 {target.name} 的顺从程度了。")
        return messages






    def _apply_character_growth_ring_effect(self, target: Character) -> List[str]:
        strength = self._get_ring_effect_strength(target, 10)
        if strength <= 0:
            return []
        target.exp[80] = int(target.exp.get(80, 0)) + strength * 10
        return [f"{target.name} 受到成长戒指的影响，积累了 {strength * 10} 点经验。"]






    def _apply_character_job_change(self, idx: int, target: Character) -> tuple[bool, str]:
        blocked_reason = self._can_change_character_job(idx, target)
        if blocked_reason is not None:
            return False, blocked_reason

        job_options = self._get_character_job_options(target)
        choice = self._prompt_character_job_change_choice(job_options)
        if choice is None:
            return False, "输入无效。"
        if choice == -1:
            return False, "已取消转职。"

        selected_job = self._find_character_job_option(job_options, choice)
        if selected_job is None:
            return False, "输入无效。"

        return self._finalize_character_job_change(target, selected_job)




    def _apply_character_job_post_effects(self, target: Character):
        self._set_character_job_stats(target)
        if target.talent.get(202, 0) or target.talent.get(206, 0):
            target.talent[117] = 1
            target.cflag[152] = max(int(target.cflag.get(152, 0)), 20)
        elif target.talent.get(200, 0) or target.talent.get(205, 0):
            target.talent[118] = 1




    def _apply_character_job_talent_flags(self, target: Character, talent_id: int):
        if talent_id == 200:
            target.talent[240] = 1
        elif talent_id == 201:
            target.talent[241] = 1
        elif talent_id == 202:
            target.talent[242] = 1
        elif talent_id == 203:
            target.talent[243] = 1
        elif talent_id == 205:
            target.talent[249] = 1
        elif talent_id == 206:
            target.talent[250] = 1
        elif talent_id == 207:
            target.talent[251] = 1
        elif talent_id == 208:
            target.talent[252] = 1
        elif talent_id == 209:
            target.cflag[1] = 7




    def _apply_character_lover_action(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._can_show_character_marriage_action(idx, char):
            return False, "当前无法处理这名角色的恋人关系。"
        if self._has_dungeon_town_lover(idx):
            return self._break_character_lover(idx, char)
        if int(char.cflag.get(1, 0)) == 2:
            return self._set_character_lover(idx, char)
        if int(char.cflag.get(1, 0)) == 0:
            return self._marry_character_to_dog(idx, char)
        return False, "当前没有可执行的恋人操作。"






    def _apply_character_marriage_action(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._can_show_character_marriage_action(idx, char):
            return False, "当前无法处理这名角色的婚姻关系。"
        if int(char.cflag.get(601, 0)) > 0:
            return self._divorce_character(idx, char)
        if self._has_dungeon_town_lover(idx):
            return self._marry_character_to_lover(idx, char)
        return self._marry_character_to_player(idx, char)






    def _apply_character_ntr_video_event(self, target: Character) -> List[str]:
        if int(target.cflag.get(1, 0)) != 9:
            return []
        if int(target.talent.get(153, 0)) == 0 and random.randint(0, 5) == 0 and self._find_character_index(target) > 0:
            self._restore_character_as_invading_hero_from_ntr_video(target)
            return []
        messages = self._apply_ntr_video_play(target)
        messages.extend(self._apply_ntr_growth_checks(target))
        return messages






    def _apply_character_part_time_level(
        self,
        target: Character,
        job_options: List[tuple[int, str]],
        selected_flag: int,
        selected_label: str,
        level: int,
    ) -> tuple[bool, str]:
        if level == 0:
            target.cflag[120] = 0
            for flag_id, _ in job_options:
                target.cflag[flag_id] = 0
            return True, "打工积极性已清空。"

        target.cflag[120] = max(1, int(target.cflag.get(120, 0)))
        for flag_id, _ in job_options:
            if flag_id != selected_flag and int(target.cflag.get(flag_id, 0)) == level:
                target.cflag[flag_id] = max(0, level - 1)
        target.cflag[selected_flag] = level
        if level == 1:
            return True, f"{selected_label}积极性变成普通了"
        return True, f"{selected_label}积极性变为等级{level}了"




    def _apply_character_pink_ring_effect(self, target: Character) -> List[str]:
        strength = self._get_ring_effect_strength(target, 6)
        if strength <= 0:
            return []

        messages = [f"{target.name} 手上的粉红色戒指发出诡异的粉色光芒。"]
        if int(target.talent.get(69, 0)):
            messages.extend(
                [
                    f"然而戒指的魔力对 {target.name} 完全没有产生任何效果。",
                    f"{target.name} 只是轻蔑地看了一眼戒指。",
                ]
            )
            return messages

        gain = max(0, strength // 2)
        if int(target.talent.get(73, 0)) == 0:
            target.talent[73] = 1
            messages.extend(
                [
                    f"戒指的魔力永久地改变了 {target.name} 的身体和心灵。",
                    f"{target.name} 的身体变得敏感，心中充满了欲望。",
                ]
            )
            if int(target.juel.get(5, 0)) < 10000 and gain > 0:
                target.juel[5] = min(10000, int(target.juel.get(5, 0)) + gain)
            return messages

        if int(target.juel.get(5, 0)) < 10000 and gain > 0:
            target.juel[5] = min(10000, int(target.juel.get(5, 0)) + gain)
            messages.append(f"{target.name} 对情欲的渴求变得更强了。")
            return messages

        return []






    def _apply_character_sabbath_day_event(self, target: Character) -> List[str]:
        if int(self.interpreter.vars.day[2]) % 3 != 0:
            return []
        if int(target.talent.get(242, 0)) == 0 and int(target.talent.get(250, 0)) == 0:
            return []
        if int(target.cflag.get(0, 0)) == 0:
            return []
        if int(target.cflag.get(152, 0)) < 40:
            return []

        messages = [f"{target.name} 参与了献给无名的淫荡女神的仪式，"]
        sabbath_user = random.randint(0, 3)
        faith = int(target.cflag.get(152, 0))
        has_dog = int(self.interpreter.vars.items.get(22, 0)) > 0
        former_life = int(target.talent.get(315, 0))
        had_former_faith = int(target.talent.get(17, 0)) != 0 or int(target.talent.get(282, 0)) != 0

        if sabbath_user == 0 and has_dog:
            messages.append(
                random.choice(
                    [
                        "祭坛前，信徒的少女和山羊交配了起来……",
                        "为了收集狗的精液的女信徒用嘴巴不停收集着……",
                        "祭坛前，信徒的人妻和狗交配着……",
                    ]
                )
            )
            return messages

        if sabbath_user == 1 and faith > 80:
            messages.append(
                random.choice(
                    [
                        "祭坛前，信众们开始做起了爱……",
                        "新婚的信众夫妇们玩起了交换Play……",
                        "祭坛前年轻的信众们乱交了起来……",
                    ]
                )
            )
            return messages

        if sabbath_user == 2 and faith > 60 and had_former_faith:
            former_goddess = self._build_sabbath_day_former_goddess_label(target, former_life)
            if former_goddess:
                messages.append(
                    former_goddess
                    + random.choice(
                        [
                            "献上了她被侵犯着的淫荡画像……",
                            "的圣器里自慰发泄着……",
                        ]
                        if former_goddess == "向潜藏地底的死亡女神"
                        else [
                            "唱起了她被人侵犯着的歌词……",
                            "展示着她的信徒在野外被玷污的画面……",
                        ]
                        if former_goddess == "向纯洁的神圣女神"
                        else [
                            "展示着她的信徒被兽人侵犯的模样……",
                            "献上了装满精液的圣杯……",
                        ]
                        if former_goddess == "向丰饶的大地女神"
                        else [
                            "的神像上喷上了精液……",
                            "献上了穿着淫荡改造的神官服并穿着它跳起了淫荡的舞蹈……",
                        ]
                    )
                )
                return messages

        messages.append(
            random.choice(
                [
                    "祭坛前，信徒的女孩自慰了起来……",
                    "献上了淫荡的雕像，信徒的少年在那上面喷上了精液……",
                    "献上了信徒的女精灵和兽人做爱的模样……",
                ]
            )
        )
        return messages






    def _apply_character_sabbath_event(self, target: Character) -> List[str]:
        if int(target.cflag.get(1, 0)) != 0:
            return []
        if int(self.interpreter.vars.day[2]) <= 14 or int(self.interpreter.vars.day[2]) >= 16:
            return []
        if int(target.talent.get(242, 0)) == 0 and int(target.talent.get(250, 0)) == 0:
            return []
        if int(target.talent.get(76, 0)) == 0:
            return []

        messages: List[str] = [f"{target.name} 参加了月祭仪式。"]
        count_a = 0
        count_v = 0
        count_s = 0
        count_z = 0

        if int(target.talent.get(122, 0)):
            pass
        elif int(target.talent.get(121, 0)):
            if int(target.talent.get(0, 0)) or int(target.talent.get(273, 0)):
                if int(target.talent.get(77, 0)):
                    count_a += 1
                count_a += random.randint(1, 10)
                count_s += count_a + random.randint(0, 9)
            else:
                count_v += random.randint(1, 10)
                count_a += random.randint(1, 10)
                count_s += count_a + count_v + random.randint(0, 9)
        elif int(target.talent.get(0, 0)):
            if int(target.talent.get(77, 0)):
                count_a += 1
            count_a += random.randint(1, 10)
            count_s += count_a + random.randint(0, 9)
        elif int(target.talent.get(273, 0)):
            if int(target.talent.get(77, 0)):
                count_a += 1
            count_a += random.randint(1, 10)
            count_s += count_a + random.randint(0, 9)
        elif int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64) and self.interpreter.vars.get_flag(37, 0):
            if int(target.talent.get(77, 0)):
                count_a += 1
            count_a += random.randint(1, 10)
            count_s += count_a + random.randint(0, 9)
        elif int(target.abl.get(39, 0)) >= 1 and random.randint(0, 1) == 0:
            if int(target.abl.get(17, 0)) >= 1:
                count_v += int(target.abl.get(17, 0))
                count_a += int(target.abl.get(17, 0))
            if int(target.talent.get(75, 0)):
                count_v += 1
            if int(target.talent.get(77, 0)):
                count_a += 1
            count_v += random.randint(1, 10) + int(target.abl.get(39, 0))
            count_a += random.randint(1, 10) + int(target.abl.get(39, 0))
            count_s += count_a + count_v + random.randint(0, 9)
            count_z += count_s
        else:
            if int(target.abl.get(17, 0)) >= 1:
                count_v += int(target.abl.get(17, 0))
                count_a += int(target.abl.get(17, 0))
            if int(target.abl.get(16, 0)) >= 1:
                count_v += int(target.abl.get(16, 0))
                count_a += int(target.abl.get(16, 0))
            if int(target.talent.get(75, 0)):
                count_v += 1
            if int(target.talent.get(77, 0)):
                count_a += 1
            count_v += random.randint(1, 10) + 1
            count_a += random.randint(1, 10) + 1
            count_s += count_a + count_v + random.randint(0, 9)

        if count_a > 0:
            target.exp[1] = int(target.exp.get(1, 0)) + count_a
        if count_v > 0:
            target.exp[0] = int(target.exp.get(0, 0)) + count_v
        local = count_a + count_v
        if local > 0:
            target.exp[5] = int(target.exp.get(5, 0)) + local
        if count_s > 0:
            target.exp[20] = int(target.exp.get(20, 0)) + count_s
        if count_z > 0:
            target.exp[56] = int(target.exp.get(56, 0)) + count_z
        if count_a > 0:
            self._add_juel(2, count_a)
        if count_v > 0:
            self._add_juel(1, count_v)
        juel_bonus = (count_a + count_v + count_s + count_z) * 10
        if juel_bonus > 0:
            self._add_juel(5, juel_bonus)
            self._add_juel(8, juel_bonus)
        if int(target.talent.get(1, 0)):
            messages.append("【童贞丧失】")
            target.talent[1] = 0
        return messages






    def _apply_character_set_assistant(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_select_standby_slave(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        self.interpreter.vars.assi = idx
        return True, f"{char.name} 成为了助手。"






    def _apply_character_set_training_target(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_open_trainable_target(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        self.interpreter.vars.target = idx
        return True, f"{char.name} 成为了调教对象。"






    def _apply_character_slave_marriage_action(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._can_show_character_marriage_action(idx, char):
            return False, "当前无法处理这名角色的婚姻关系。"
        if int(char.cflag.get(1, 0)) == 0 and int(char.cflag.get(601, 0)) == 0:
            return self._marry_character_to_slave(idx, char)
        return False, "当前无法与奴隶结婚。"






    def _apply_character_standby_level_up(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_open_character_standby_service(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        return self._level_up_character(idx, char)






    def _apply_character_standby_recovery(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_open_character_standby_service(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        return self._recover_character(char)






    def _apply_character_template_csv_abl_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            abl_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.abl[abl_id] = value






    def _apply_character_template_csv_base_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            base_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.base[base_id] = value
        char.maxbase[base_id] = max(char.maxbase.get(base_id, 0), value)






    def _apply_character_template_csv_callname_row(self, char: Character, row: List[str]) -> None:
        if len(row) > 1:
            char.callname = row[1].strip()






    def _apply_character_template_csv_cstr_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 1:
            return
        try:
            cstr_id = int(row[1])
        except ValueError:
            return
        value = row[2] if len(row) > 2 else ""
        char.cstr[cstr_id] = value






    def _apply_character_template_csv_exp_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            exp_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.exp[exp_id] = value






    def _apply_character_template_csv_flag_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            flag_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.cflag[flag_id] = value






    def _apply_character_template_csv_juel_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            juel_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.juel[juel_id] = value






    def _apply_character_template_csv_mark_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 2:
            return
        try:
            mark_id = int(row[1])
            value = int((row[2] or "0").split(";")[0])
        except ValueError:
            return
        char.mark[mark_id] = value






    def _apply_character_template_csv_name_row(self, char: Character, row: List[str]) -> None:
        if len(row) > 1:
            char.name = row[1].strip()






    def _apply_character_template_csv_row(self, char: Character, row: List[str]) -> None:
        if not row or not row[0]:
            return
        key = row[0].strip()
        if key == "名前":
            self._apply_character_template_csv_name_row(char, row)
        elif key == "呼び名":
            self._apply_character_template_csv_callname_row(char, row)
        elif key == "基礎":
            self._apply_character_template_csv_base_row(char, row)
        elif key == "素質":
            self._apply_character_template_csv_talent_row(char, row)
        elif key == "フラグ":
            self._apply_character_template_csv_flag_row(char, row)
        elif key == "CFLAG":
            self._apply_character_template_csv_flag_row(char, row)
        elif key == "ABL":
            self._apply_character_template_csv_abl_row(char, row)
        elif key == "MARK":
            self._apply_character_template_csv_mark_row(char, row)
        elif key == "CSTR":
            self._apply_character_template_csv_cstr_row(char, row)
        elif key == "経験":
            self._apply_character_template_csv_exp_row(char, row)
        elif key == "JUEL":
            self._apply_character_template_csv_juel_row(char, row)






    def _apply_character_template_csv_talent_row(self, char: Character, row: List[str]) -> None:
        if len(row) <= 1:
            return
        try:
            talent_id = int(row[1])
        except ValueError:
            return
        raw_value = row[2] if len(row) > 2 and row[2] != "" else "1"
        raw_value = raw_value.split(";")[0]
        try:
            value = int(raw_value)
        except ValueError:
            value = 1
        char.talent[talent_id] = value






    def _apply_character_template_post_load(self, char: Character, template_id: int) -> None:
        if template_id == 34:
            self.interpreter.vars.set_flag(224, 1)
            if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
                self._ensure_character_body_profile(char, overwrite_existing=True)






    def _apply_character_temptation(self, idx: int, target: Character) -> tuple[bool, str]:
        state = self._check_able_to_temptation(idx, target)
        if state == 1:
            return False, "只有侵攻中的勇者才能进行魔的诱惑。"
        if state == 2:
            return False, "狂王无法被诱惑。"

        player = self._get_player()
        cost_error = self._validate_character_temptation_player(player)
        if cost_error is not None:
            return False, cost_error

        self._spend_character_temptation_cost(player)
        success, failure = self._prepare_temptation_success_weights(target)
        total_gain = self._run_character_temptation_trials(target, success, failure)
        self._finalize_character_temptation_state(target, player)
        return self._build_character_temptation_result(idx, target, total_gain)




    def _apply_character_weakness_ring_effect(self, target: Character) -> List[str]:
        strength = self._get_ring_effect_strength(target, 14)
        if strength <= 0:
            return []

        old_attack = int(target.cflag.get(13, 0))
        old_defense = int(target.cflag.get(14, 0))
        new_attack = max(15, old_attack - strength)
        new_defense = max(15, old_defense - strength)
        target.cflag[13] = new_attack
        target.cflag[14] = new_defense

        if new_attack == old_attack and new_defense == old_defense:
            return []
        return [f"{target.name} 被衰弱戒指侵蚀，攻击和防御下降了。"]






    def _build_character_body_age_lines(self, char: Character) -> List[str]:
        if not self._get_flag_bit(5, 12):
            return []
        physical_age = int(char.cflag.get(451, 0))
        race_age = int(char.cflag.get(452, 0))
        if physical_age <= 0:
            return []
        age_text = f" 肉体年龄: {physical_age} 岁"
        if self._get_flag_bit(5, 13) and race_age > 0:
            age_text += f"   种族年龄: {race_age} 岁"
            if self._get_flag_bit(5, 14):
                age_text += f"   换算人类年龄: {physical_age} 岁"
        return [age_text]






    def _build_character_body_info_lines(self, char: Character) -> List[str]:
        lines: List[str] = []
        lines.extend(self._build_character_body_age_lines(char))
        lines.extend(self._build_character_body_measurement_lines(char))
        return lines






    def _build_character_body_measurement_lines(self, char: Character) -> List[str]:
        if not self._get_flag_bit(5, 15):
            return []
        height = int(char.cflag.get(453, 0))
        weight = int(char.cflag.get(454, 0))
        bust = int(char.cflag.get(455, 0))
        waist = int(char.cflag.get(456, 0))
        hip = int(char.cflag.get(457, 0))
        lines: List[str] = []
        if height > 0 or weight > 0:
            lines.append(
                f" 身高: {self._format_character_body_measurement(height, 'height')} cm"
                f"   体重: {self._format_character_body_measurement(weight, 'weight')} kg"
            )
        if bust > 0 or waist > 0 or hip > 0:
            lines.append(
                " 三围: "
                f"B{self._format_character_body_measurement(bust, 'bust')} / "
                f"W{self._format_character_body_measurement(waist, 'waist')} / "
                f"H{self._format_character_body_measurement(hip, 'hip')}"
            )
        return lines






    def _build_character_detail_action_lines(self, idx: int, char: Character) -> List[str]:
        actions: List[str] = []
        if idx <= 0:
            return actions
        actions.extend(self._build_character_detail_action_lines_core(idx, char))
        actions.extend(self._build_character_detail_action_lines_marriage(idx, char))
        actions.extend(self._build_character_detail_action_lines_standby(char))
        actions.extend(self._build_character_detail_action_lines_special_states(char))
        return actions






    def _build_character_detail_action_lines_core(self, idx: int, char: Character) -> List[str]:
        actions: List[str] = []
        if int(char.cflag.get(1, 0)) in (0, 3):
            actions.append(" [0] 改名")
            actions.append(" [1] 还原名字")
        if int(char.cflag.get(1, 0)) != 2:
            actions.append(" [2] 转职")
        if self._can_show_character_temptation(idx, char):
            actions.append(" [3] 魔的诱惑")
        actions.append(" [8] 一人称重设")
        actions.append(f" [9] {'取消收藏' if char.cflag.get(700, 0) else '收藏'}")
        actions.append(" [10] 提升能力")
        if self._can_show_character_equipment(idx, char):
            actions.append(" [16] 装备查看")
        if self._can_show_character_bitch_level(idx, char):
            actions.append(f" [18] {self._get_character_bitch_action_label(char)}")
        return actions






    def _build_character_detail_action_lines_marriage(self, idx: int, char: Character) -> List[str]:
        actions: List[str] = []
        if not self._can_show_character_marriage_action(idx, char):
            return actions
        if int(char.cflag.get(601, 0)) > 0:
            actions.append(" [19] 离婚")
        elif self._has_dungeon_town_lover(idx):
            actions.append(" [19] 与恋人结婚")
            actions.append(" [20] 与恋人分手")
        else:
            actions.append(" [19] 与魔王结婚")
            if int(char.cflag.get(1, 0)) == 2:
                actions.append(" [20] 恋人设定")
            elif int(char.cflag.get(1, 0)) == 0:
                actions.append(" [20] 与野狗结婚")
                actions.append(" [21] 与奴隶结婚")
        return actions






    def _build_character_detail_action_lines_special_states(self, char: Character) -> List[str]:
        actions: List[str] = []
        if int(char.cflag.get(1, 0)) == 8:
            actions.append(" [12] 解除固定")
        if int(char.cflag.get(1, 0)) == 3:
            actions.append(" [13] 强制召回")
        return actions






    def _build_character_detail_action_lines_standby(self, char: Character) -> List[str]:
        if int(char.cflag.get(1, 0)) != 0:
            return []
        actions = [" [6] 设为目标", " [7] 设为助手", " [11] 更换服装"]
        if char.base.get(0, 0) < char.maxbase.get(0, 0) or char.base.get(1, 0) < char.maxbase.get(1, 0):
            actions.append(" [14] 恢复体力")
        actions.append(" [15] 提升等级")
        return actions






    def _build_character_detail_identity_lines(self, char: Character) -> List[str]:
        lines = [f" HP: {char.base.get(0, 0)}/{char.maxbase.get(0, 0)}   MP: {char.base.get(1, 0)}/{char.maxbase.get(1, 0)}"]
        lines.append(f" 攻击: {char.cflag.get(13, 0)}   防御: {char.cflag.get(14, 0)}   善恶值: {char.cflag.get(151, 0)}")
        lines.append(f" 一人称: {self._get_character_self_call_text(char)}")
        lines.extend(self._build_character_body_info_lines(char))
        lines.append(f" 外衣: {self._get_dress_main_cloth_name(char.cflag.get(41, 0))}   饰品: {self._get_dress_accessory_name(char.cflag.get(42, 0))}")
        return lines






    def _build_character_detail_inventory_lines(self, char: Character) -> List[str]:
        if not char.item:
            return []
        lines = [" 持有物品:"]
        lines.extend(self._list_inventory(char))
        return lines






    def _build_character_detail_lines(self, idx: int, char: Character) -> List[str]:
        lines: List[str] = []
        lines.extend(self._build_character_detail_title_lines(idx, char))
        lines.extend(self._build_character_detail_status_lines(idx, char))
        lines.extend(self._build_character_detail_quest_lines(char))
        lines.extend(self._build_character_detail_identity_lines(char))
        lines.extend(self._build_character_detail_inventory_lines(char))
        lines.extend(self._build_character_detail_summary_lines(char))
        return lines






    def _build_character_detail_quest_lines(self, char: Character) -> List[str]:
        quest_tag = self._get_character_dungeon_quest_tag(char)
        if not quest_tag:
            return []
        lines = [f" 任务: {quest_tag.removeprefix('<任务:').removesuffix('>')}"]
        lines.extend(self._build_dungeon_quest_detail_lines(char))
        return lines






    def _build_character_detail_status_lines(self, idx: int, char: Character) -> List[str]:
        lines = [f" 状态: {self._get_character_status_text(char)} / LV{self._get_character_level(char)} / 顺从{self._get_submission_level(char)}"]
        lines.append(f" 婚恋: {self._get_character_marriage_summary(idx, char)}")
        return lines






    def _build_character_detail_summary_lines(self, char: Character) -> List[str]:
        lines: List[str] = []
        if char.abl:
            abl_summary = ", ".join(f"ABL:{k}={v}" for k, v in sorted(char.abl.items())[:12])
            lines.append(f" 能力: {abl_summary}")
        if char.exp:
            exp_summary = ", ".join(f"EXP:{k}={v}" for k, v in sorted(char.exp.items())[:10])
            lines.append(f" 经验: {exp_summary}")
        if char.source:
            lines.append(" 最新 SOURCE: " + ", ".join(f"{k}:+{v}" for k, v in sorted(char.source.items())))
        if char.losebase:
            lines.append(" 最新 LOSEBASE: " + ", ".join(f"{k}:+{v}" for k, v in sorted(char.losebase.items())))
        return lines






    def _build_character_detail_title_lines(self, idx: int, char: Character) -> List[str]:
        title = f"[{idx}] {char.name}"
        if idx == 0:
            title += " (魔王)"
        return [title]






    def _build_character_equipment_detail_lines(self, target: Character) -> List[str]:
        lines: List[str] = []
        lines.extend(self._build_equipment_detail_section(target, 550, "武器", self._get_equipment_weapon_name))
        lines.extend(self._build_equipment_detail_section(target, 551, "装饰A", self._get_equipment_ring_name))
        lines.extend(self._build_equipment_detail_section(target, 552, "装饰B", self._get_equipment_ring_name))
        return lines




    def _build_character_list_lines(self, page: int, sort_mode: int, status_cycle: int = 0) -> List[str]:
        lines: List[str] = []
        indices = self._sort_character_indices(sort_mode, status_cycle=status_cycle)
        page_size = 24
        start = page * page_size
        end = start + page_size
        if self.interpreter.vars.chars:
            master = self.interpreter.vars.chars[0]
            lines.append(f" [0] {master.name} LV{self._get_character_level(master)} HP {master.base.get(0,0)}/{master.maxbase.get(0,0)} MP {master.base.get(1,0)}/{master.maxbase.get(1,0)}")
        for idx in indices[start:end]:
            char = self.interpreter.vars.chars[idx]
            line = (
                f" [{idx}] {self._get_character_status_text(char):<6} {char.name} LV{self._get_character_level(char)} "
                f"攻{char.cflag.get(13, 0)}/防{char.cflag.get(14, 0)} 善恶{char.cflag.get(151, 0)} "
                f"HP {char.base.get(0,0)}/{char.maxbase.get(0,0)} MP {char.base.get(1,0)}/{char.maxbase.get(1,0)} "
                f"{self._get_character_list_love_tag(char)}"
            )
            if char.cflag.get(700, 0):
                line += " [☆]"
            party_tag = self._get_character_party_tag(idx, char)
            if party_tag:
                line += f" {party_tag}"
            return_tag = self._get_character_return_tag(char)
            if return_tag:
                line += f" {return_tag}"
            quest_tag = self._get_character_dungeon_quest_tag(char)
            if quest_tag:
                line += f" {quest_tag}"
            lines.append(line)
        return lines






    def _build_character_template_catalog(self) -> Dict[str, Any]:
        catalog: Dict[str, Any] = {
            "templates": {},
            "values": defaultdict(set),
        }
        chara_root = self._find_csv_path("CSV", "Chara")
        if not chara_root:
            return catalog

        for root, _, files in os.walk(chara_root):
            for filename in files:
                if not filename.lower().startswith("chara") or not filename.lower().endswith(".csv"):
                    continue
                csv_path = os.path.join(root, filename)
                try:
                    template_id = int(os.path.splitext(filename)[0][5:])
                except ValueError:
                    continue
                char = self._load_character_template_from_path(csv_path, template_id)
                if char is None:
                    continue
                catalog["templates"][template_id] = char
                for tracked_id in [300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 312, 313, 314, 315, 316, 317, 319]:
                    value = char.talent.get(tracked_id, 0)
                    if value:
                        catalog["values"][tracked_id].add(int(value))
        return catalog




    def _build_character_temptation_result(self, idx: int, target: Character, total_gain: int) -> tuple[bool, str]:
        if int(target.cflag.get(2, 0)) >= 1000:
            self._set_character_captured_standby_state(target)
            self._remove_character_from_party(idx)
            return True, f"*{target.name}被你诱惑，投诚了！*"

        if total_gain <= 0:
            return True, f"{target.name}暂时没有被你诱惑。"
        return True, f"{target.name}的诱惑进度增加了{total_gain}。"



    def _can_character_awaken_pregnancy(self, target: Character) -> bool:
        if target.talent.get(153, 0) or target.talent.get(154, 0) or target.talent.get(341, 0) or target.talent.get(342, 0):
            return False
        if (self.interpreter.vars.get_flag(5, 0) & (1 << 2)) == 0:
            return False
        if (self.interpreter.vars.get_flag(5, 0) & (1 << 12)) and int(target.cflag.get(451, 0)) <= 9:
            self._clear_pregnancy_tracking_flags(target)
            return False
        preg_type = int(target.cflag.get(113, 0))
        if preg_type == 1 and not target.talent.get(340, 0):
            return False
        if preg_type in (2, 3):
            if not target.talent.get(340, 0):
                return False
            if not (target.talent.get(121, 0) or target.talent.get(122, 0)):
                return False
        if int(target.cflag.get(451, 0)) <= 14 and random.randint(0, 4) > 1:
            self._clear_pregnancy_tracking_flags(target)
            return False
        return self._is_pregnancy_aware_now(target)






    def _can_character_conceive_now(self, target: Character, source: int) -> bool:
        if target.talent.get(135, 0):
            return False
        if int(source) == 5 and not target.talent.get(124, 0):
            return False
        if int(target.cflag.get(110, 0)) > 0:
            return False
        if target.talent.get(153, 0) or target.talent.get(154, 0):
            return False
        preg_type = int(target.cflag.get(113, 0))
        if preg_type == 1 and not target.talent.get(340, 0):
            return False
        if preg_type in (2, 3):
            if not target.talent.get(340, 0):
                return False
            if not (target.talent.get(121, 0) or target.talent.get(122, 0)):
                return False
        return True






    def _cleanup_character_links_before_removal(self, idx: int, char: Character):
        self._remove_character_from_party(idx)

        lover_partner_pair = self._resolve_dungeon_town_lover_partner(idx, char) if self._has_dungeon_town_lover(idx) else None
        marriage_state = int(char.cflag.get(601, 0))
        marriage_partner_pair = None
        if marriage_state == 902:
            marriage_partner_pair = lover_partner_pair
        elif marriage_state > 902:
            marriage_partner_pair = self._resolve_character_marriage_partner(idx, char)

        if self._has_dungeon_town_lover(idx):
            self._clear_character_lover_relation(idx, char)

        if marriage_state == 902:
            if marriage_partner_pair is not None:
                partner = marriage_partner_pair[1]
                partner.cflag[601] = 0
                partner.cflag[602] = 0
                partner.cflag[609] = 0
        elif marriage_state > 902:
            if marriage_partner_pair is not None:
                partner = marriage_partner_pair[1]
                partner.cflag[601] = 0
                partner.cflag[602] = 0
                partner.cflag[609] = 0




    def _clear_character_job_talents(self, target: Character):
        for talent_id in range(200, 212):
            target.talent[talent_id] = 0
        target.talent[281] = 0




    def _clear_character_lover_relation(self, idx: int, char: Character):
        partner_pair = self._resolve_dungeon_town_lover_partner(idx, char)
        self._clear_dungeon_town_lover_entry(idx)
        if partner_pair is not None:
            self._clear_dungeon_town_lover_entry(partner_pair[0])






    def _create_character_from_template(self, template_id: int) -> Optional[Character]:
        char = self._instantiate_character_from_template(template_id)
        return self._append_character(char)






    def _find_character_by_template_id(self, template_id: int) -> Optional[Character]:
        for char in self.interpreter.vars.chars:
            raw_template_id = getattr(char, "template_id", None)
            if raw_template_id is None:
                raw_template_id = char.cflag.get(190, 0) or 0
            if int(raw_template_id) == int(template_id):
                return char
        return None






    def _find_character_index(self, target: Character) -> int:
        return next((idx for idx, char in enumerate(self.interpreter.vars.chars) if char is target), -1)






    def _find_character_job_option(self, job_options: List[tuple[int, int, str]], selected: int) -> Optional[tuple[int, int, str]]:
        return next((entry for entry in job_options if entry[0] == selected), None)




    def _generate_character_body_bust_top_cm(self, char: Character, human_age: int) -> int:
        if int(char.talent.get(116, 0)):
            bust_top = 10 + random.randint(0, 39)
        elif int(char.talent.get(109, 0)):
            bust_top = 70 + random.randint(0, 59)
        elif int(char.talent.get(110, 0)) or int(char.talent.get(114, 0)) or int(char.talent.get(119, 0)):
            bust_top = 200 + random.randint(0, 24)
            if int(char.talent.get(114, 0)):
                bust_top += 50 + random.randint(0, 49)
                if random.randint(0, 1) == 0:
                    bust_top += 180 + random.randint(0, 19) + random.randint(0, 19) + random.randint(0, 29)
            elif int(char.talent.get(119, 0)):
                bust_top += 50 + random.randint(0, 49)
                bust_top += 180 + random.randint(0, 19) + random.randint(0, 19) + random.randint(0, 29)
        else:
            bust_top = 132 + random.randint(0, 39)

        if int(char.talent.get(100, 0)) and int(char.talent.get(110, 0)):
            bust_top += 15 + random.randint(0, 9)
        if int(char.talent.get(99, 0)):
            bust_top -= 20 + random.randint(0, 9)
        if int(char.exp.get(60, 0)) > 0:
            bust_top += 2 + random.randint(0, 7)
        if int(char.talent.get(130, 0)) and int(char.talent.get(119, 0)):
            bust_top += 85 + random.randint(0, 39)
        if human_age < 16:
            bust_top = max(10, bust_top - max(0, 20 - human_age))
        return max(1, bust_top)






    def _generate_character_body_height_cm(self, char: Character, human_age: int) -> int:
        height_min = 1400
        height_max = 1800
        if int(char.talent.get(122, 0)):
            height_max += 250
        if int(char.talent.get(99, 0)):
            height_min = 1700
            height_max = 9990
        elif int(char.talent.get(100, 0)):
            height_min = 0
            height_max = 1600

        while True:
            if int(char.talent.get(122, 0)):
                height = 1150
            else:
                height = 1100 + random.randint(0, 133) + random.randint(0, 133) + random.randint(0, 132)
                if random.randint(0, 4) == 0:
                    height += random.randint(0, 99)
                if random.randint(0, 4) == 0:
                    height -= random.randint(0, 99)

            race_talent = int(char.talent.get(314, 0))
            if race_talent in (1, 7):
                height += random.randint(0, 7) * 10
            elif race_talent == 5:
                height += random.randint(0, 15) * 10
            elif race_talent in (10, 11):
                height -= random.randint(0, 7) * 10

            if human_age < 13:
                height = height * (18 + human_age) // 32
            elif human_age == 13:
                height = height * 77 // 80
            elif human_age < 18:
                height = height * (160 - human_age) // 160

            height += 250 + sum(random.randint(0, 19) for _ in range(5))
            if height_min < height < height_max:
                return max(100, height)






    def _generate_character_body_hip_cm(self, char: Character, human_age: int, height_cm: int, waist_cm: int, bust_cm: int) -> int:
        hip = height_cm * (5300 + int(char.talent.get(308, 0))) // 10000
        if int(char.talent.get(91, 0)):
            hip += 15
        if int(char.talent.get(248, 0)):
            hip = hip * 102 // 100
        if int(char.talent.get(256, 0)):
            hip = hip * 98 // 100
        if int(char.talent.get(100, 0)):
            hip = hip * 96 // 100
        if int(char.talent.get(122, 0)):
            hip = hip * 90 // 100
        if int(char.talent.get(115, 0)):
            hip = hip * 115 // 100
        if human_age < 16:
            hip = max(min(hip, bust_cm + max(0, human_age - 12) * 10), waist_cm)
        return max(1, hip)






    def _generate_character_body_profile(self, char: Character, human_age: int) -> Dict[int, int]:
        human_age = max(1, int(human_age))
        height_raw = self._generate_character_body_height_cm(char, human_age)
        waist_raw = self._generate_character_body_waist_cm(char, height_raw)
        bust_under_raw = self._generate_character_body_under_bust_cm(char, height_raw)
        bust_top_raw = self._generate_character_body_bust_top_cm(char, human_age)
        bust_raw = bust_under_raw + bust_top_raw
        hip_raw = self._generate_character_body_hip_cm(char, human_age, height_raw, waist_raw, bust_raw)
        weight_raw = self._generate_character_body_weight_kg(char, height_raw, bust_under_raw, bust_top_raw)
        race_age = self._generate_race_age(human_age, int(char.talent.get(314, 0)))
        return {
            451: human_age,
            452: race_age,
            453: max(1, (height_raw + 5) // 10),
            454: max(1, (weight_raw + 5) // 10),
            455: max(1, (bust_raw + 5) // 10),
            456: max(1, (waist_raw + 5) // 10),
            457: max(1, (hip_raw + 5) // 10),
            458: max(1, (bust_top_raw + 5) // 10),
            459: max(1, (bust_under_raw + 5) // 10),
        }






    def _generate_character_body_under_bust_cm(self, char: Character, height_cm: int) -> int:
        under_bust = height_cm * (43100 + int(char.talent.get(308, 0))) // 100000
        if int(char.talent.get(248, 0)):
            under_bust = under_bust * 105 // 100
        if int(char.talent.get(256, 0)):
            under_bust = under_bust * 98 // 100
        return max(1, under_bust)






    def _generate_character_body_waist_cm(self, char: Character, height_cm: int) -> int:
        waist = height_cm * (3700 + int(char.talent.get(308, 0))) // 10000
        if int(char.talent.get(122, 0)):
            waist += 80
            waist -= random.randint(0, 39)
        if waist > 600:
            waist = waist * 983 // 1000
        if int(char.talent.get(91, 0)):
            waist = waist * 96 // 100
        if int(char.talent.get(248, 0)):
            waist = waist * 102 // 100
        if int(char.talent.get(248, 0)) and int(char.talent.get(122, 0)):
            waist = waist * 105 // 100
        if int(char.talent.get(115, 0)):
            waist = waist * 115 // 100
        if int(char.talent.get(256, 0)):
            waist = waist * 98 // 100
        if int(char.talent.get(314, 0)) == 11:
            waist = waist * 104 // 100
        return max(1, waist)






    def _generate_character_body_weight_kg(self, char: Character, height_cm: int, bust_under_cm: int, bust_top_cm: int) -> int:
        weight = height_cm * height_cm * 21 // max(1, 1250 - int(char.talent.get(308, 0))) // 100
        bust_mass = (bust_under_cm * bust_under_cm * bust_top_cm * bust_top_cm) // 100000000
        weight += bust_mass * 25 // 10
        return max(1, weight)






    def _get_character_age_expectation_delta(self, char: Character) -> int:
        delta = 0
        if int(char.talent.get(99, 0)):
            delta += 1
        if int(char.talent.get(100, 0)):
            delta -= 1
        if int(char.talent.get(100, 0)):
            delta -= 3
        if int(char.talent.get(109, 0)):
            delta -= 1
        if int(char.talent.get(110, 0)):
            delta += 1
        if int(char.talent.get(114, 0)):
            delta += 1
        if int(char.talent.get(119, 0)):
            delta += 1
        if int(char.talent.get(116, 0)):
            delta -= 1
        if int(char.talent.get(132, 0)):
            delta -= 2
        if int(char.talent.get(135, 0)):
            delta -= 2
        if int(char.talent.get(140, 0)) or int(char.talent.get(141, 0)):
            delta -= 2
        if int(char.talent.get(142, 0)) or int(char.talent.get(143, 0)):
            delta += 2
        if int(char.talent.get(157, 0)):
            delta += 6
        if int(char.talent.get(248, 0)):
            delta += 1

        occupation = int(char.talent.get(315, 0))
        if occupation in {1, 6, 7, 20}:
            delta -= 4
        elif occupation in {11, 12}:
            delta -= 1
        elif occupation in {2, 19}:
            delta += 4
        elif occupation == 21:
            delta += 6

        if int(char.talent.get(316, 0)) == 6:
            delta += 2
        if int(char.talent.get(317, 0)) in {4, 11}:
            delta += 2

        if int(char.exp.get(60, 0)) > 0:
            delta += 6
        elif int(char.exp.get(5, 0)) > 0:
            delta += 4
        elif int(char.exp.get(10, 0)) > 0:
            delta += 2
        elif not int(char.talent.get(0, 0)) and not int(char.talent.get(1, 0)):
            delta += 1
        return delta






    def _get_character_bitch_action_label(self, target: Character) -> str:
        if self._is_part_time_job_system_enabled():
            return self._get_character_part_time_level_text(target)
        return f"卖春积极性 - {self._get_character_bitch_level_text(target)}"




    def _get_character_bitch_level_text(self, target: Character) -> str:
        level = int(target.cflag.get(120, 0))
        if level <= 0:
            return "没有"
        if level == 1:
            return "普通"
        return f"{level}等级"




    def _get_character_by_template_id(self, template_id: int) -> Optional[Character]:
        return self._find_character_by_template_id(template_id)




    def _get_character_debt_value(self, char: Character) -> int:
        return int(max(0, -char.cflag.get(151, 0)))






    def _get_character_detail_action_handler(self, idx: int, char: Character, action_id: int):
        handlers = {
            0: lambda: self._rename_character(idx, char, reset=False) if idx > 0 else None,
            1: lambda: self._rename_character(idx, char, reset=True) if idx > 0 else None,
            2: lambda: self._apply_character_job_change(idx, char) if idx > 0 else None,
            3: lambda: self._apply_character_temptation(idx, char) if idx > 0 else None,
            6: lambda: self._apply_character_set_training_target(idx, char) if idx > 0 else None,
            7: lambda: self._apply_character_set_assistant(idx, char) if idx > 0 else None,
            8: lambda: self._set_character_self_call(idx, char),
            9: lambda: self._toggle_character_favorite(idx, char) if idx > 0 else None,
            10: lambda: self._open_character_ability_up_menu(idx, char) if idx > 0 else None,
            11: lambda: self._open_character_dress_menu(idx, char) if idx > 0 else None,
            12: lambda: self._apply_character_release_from_pillory(char) if char.cflag.get(1, 0) == 8 else None,
            13: lambda: self._apply_character_force_recall(char) if char.cflag.get(1, 0) == 3 else None,
            14: lambda: self._apply_character_standby_recovery(idx, char) if char.cflag.get(1, 0) == 0 else None,
            15: lambda: self._apply_character_standby_level_up(idx, char) if char.cflag.get(1, 0) == 0 else None,
            16: lambda: self._open_character_equipment_detail(idx, char) if idx > 0 else None,
            18: lambda: self._apply_character_bitch_level_action(idx, char) if idx > 0 else None,
            19: lambda: self._apply_character_marriage_action(idx, char) if idx > 0 else None,
            20: lambda: self._apply_character_lover_action(idx, char) if idx > 0 else None,
            21: lambda: self._apply_character_slave_marriage_action(idx, char) if idx > 0 else None,
        }
        return handlers.get(action_id)






    def _get_character_domination_slave_power(self, char: Character) -> int:
        strength = self._get_ring_effect_strength(char, 9)
        slave_monster_id = int(char.cflag.get(570, 0))
        if strength <= 0 or slave_monster_id < 100:
            return 0

        baseline = self._get_monster_data_baseline(slave_monster_id)
        if baseline is None:
            return 0

        attack = int(baseline.get(2, 0))
        defense = int(baseline.get(3, 0))
        power = max(1, attack + defense + int(baseline.get(4, 0)))
        return max(1, power * max(1, strength) // 2)






    def _get_character_ex_talent(self, target: Character, talent_id: int) -> int:
        return int(self._get_character_ex_talent_store(target).get(int(talent_id), 0))






    def _get_character_ex_talent_store(self, target: Character) -> Dict[int, int]:
        store = getattr(target, "ex_talent", None)
        if not isinstance(store, dict):
            store = {}
            setattr(target, "ex_talent", store)
        return store






    def _get_character_flag_bit(self, char: Character, flag_idx: int, bit: int) -> bool:
        return bool(int(char.cflag.get(flag_idx, 0)) & (1 << bit))






    def _get_character_identity_token(self, idx: int, char: Character) -> int:
        return int(idx * 1000 + int(char.cflag.get(6, 0)))






    def _get_character_index_name(self, idx: int) -> str:
        if 0 <= idx < len(self.interpreter.vars.chars):
            return self.interpreter.vars.chars[idx].name
        return str(idx)






    def _get_character_info_sort_entries(self) -> List[tuple[int, str]]:
        return [
            (1200, "编号"),
            (1300, "状态"),
            (1400, "所持金"),
            (1500, "借金"),
        ]






    def _get_character_job_options(self, target: Character) -> List[tuple[int, int, str]]:
        job_options = [
            (0, 200, "战士"),
            (1, 201, "魔法师"),
            (2, 202, "神官"),
            (3, 203, "盗贼"),
            (4, 204, "肉便器"),
            (5, 205, "骑士"),
            (6, 206, "巫女"),
            (7, 207, "忍者"),
            (8, 208, "弓手"),
            (9, 209, "苗床"),
        ]
        if int(target.exp.get(81, 0)) > 9:
            job_options.extend([
                (10, 210, "魔界将军"),
                (11, 211, "魔导神官"),
            ])
        return job_options




    def _get_character_level(self, char: Character) -> int:
        return max(
            int(char.cflag.get(9, 0)),
            1 + max((int(level) for level in char.abl.values()), default=0)
        )




    def _get_character_level_up_exp_gap(self, idx: int, char: Character) -> int:
        level = int(char.cflag.get(9, 0))
        if idx == 0:
            required_exp = level * 100 + 10
        elif char.talent.get(220, 0):
            required_exp = level * 20 + 10
        else:
            required_exp = level * 10 + 10
        return max(0, required_exp - int(char.exp.get(80, 0)))




    def _get_character_list_love_tag(self, char: Character) -> str:
        if char.talent.get(85, 0):
            return "<爱慕>"
        if char.talent.get(76, 0):
            return "<淫乱>"
        return "<未陷落>"






    def _get_character_lover_name(self, idx: int, char: Character) -> str:
        partner_pair = self._resolve_dungeon_town_lover_partner(idx, char)
        if partner_pair is not None:
            return partner_pair[1].name
        if self._has_dungeon_town_lover(idx):
            return "恋人"
        return "无"






    def _get_character_marriage_summary(self, idx: int, char: Character) -> str:
        marriage_state = int(char.cflag.get(601, 0))
        if marriage_state == 0:
            if self._has_dungeon_town_lover(idx):
                return f"恋人: {self._get_character_lover_name(idx, char)} / 交往{int(self._get_dungeon_town_lover_entry(idx).get('love_lv', 0))}天"
            return "未婚"
        if marriage_state == 900:
            return f"结婚对象: 野狗 / 婚后{int(char.cflag.get(602, 0))}天"
        if marriage_state == 901:
            return f"结婚对象: 魔王 / 婚后{int(char.cflag.get(602, 0))}天"
        if marriage_state == 902:
            return f"结婚对象: {self._get_character_lover_name(idx, char)} / 婚后{int(char.cflag.get(602, 0))}天"
        if marriage_state < 900:
            return f"结婚对象: {self._get_item_name(marriage_state)} / 婚后{int(char.cflag.get(602, 0))}天"
        partner_pair = self._resolve_character_marriage_partner(idx, char)
        if partner_pair is not None:
            return f"结婚对象: {partner_pair[1].name} / 婚后{int(char.cflag.get(602, 0))}天"
        if int(char.cflag.get(609, 0)) > 0:
            return f"结婚对象编号: {int(char.cflag.get(609, 0))} / 婚后{int(char.cflag.get(602, 0))}天"
        return f"已婚 / 婚后{int(char.cflag.get(602, 0))}天"






    def _get_character_money_value(self, char: Character) -> int:
        return int(char.cflag.get(580, 0) + char.cflag.get(581, 0))






    def _get_character_part_time_focus(self, target: Character) -> Optional[int]:
        focus_flag: Optional[int] = None
        highest_level = 0
        for flag_id in range(400, 410):
            level = int(target.cflag.get(flag_id, 0))
            if level > highest_level:
                highest_level = level
                focus_flag = flag_id
        return focus_flag




    def _get_character_part_time_job_options(self) -> List[tuple[int, str]]:
        return [(flag_id, self._get_part_time_job_name(flag_id)) for flag_id in range(400, 410)]




    def _get_character_part_time_level_text(self, target: Character) -> str:
        focus_flag = self._get_character_part_time_focus(target)
        if focus_flag is None or int(target.cflag.get(120, 0)) == 0:
            return "打工"
        level = int(target.cflag.get(focus_flag, 0))
        if level <= 0:
            return "打工"
        if level == 1:
            return f"{self._get_part_time_job_name(focus_flag)}积极性 - 普通"
        return f"{self._get_part_time_job_name(focus_flag)}积极性 - {level}等级"




    def _get_character_party_tag(self, idx: int, char: Character) -> str:
        if char.cflag.get(533, 0) > 0 and char.cflag.get(531, 0) == 0 and char.cflag.get(532, 0) == 0 and char.cflag.get(533, 0) != idx:
            leader_idx = int(char.cflag.get(533, 0))
            return f"队员<{self._get_character_index_name(leader_idx)}>"
        if char.cflag.get(533, 0) > 0:
            leader_idx = int(char.cflag.get(533, 0))
            return f"队长<{self._get_character_index_name(leader_idx)}>"
        return ""






    def _get_character_pre_hero_life(self, target: Character) -> str:
        """Get character's pre-hero life from talent data."""
        life_talent = int(target.talent.get(300, 0))
        life_map = {
            0: "学生", 1: "修女", 2: "巫女", 3: "预言家", 4: "占卜师",
            5: "隐士", 6: "小偷", 7: "乞丐", 8: "贫民", 9: "商人",
            10: "军人", 11: "贵族",
        }
        return life_map.get(life_talent, "")






    def _get_character_race2_name(self, target: Character) -> str:
        """Get character's sub-race name from talent data."""
        race2_talent = int(target.talent.get(320, 0))
        race2_map = {
            0: "", 1: "植物", 2: "妖精", 3: "史莱姆", 4: "魔兽", 5: "魔兽",
        }
        return race2_map.get(race2_talent, "")






    def _get_character_race_name(self, target: Character) -> str:
        """Get character's race name from talent data.
        Maps talent IDs for race to race names per LOOK.ERB.
        """
        race_talent = int(target.talent.get(319, 0))
        race_map = {
            0: "人类", 1: "精灵", 2: "暗精灵", 3: "天使", 4: "堕天使",
            5: "吸血鬼", 6: "龙族", 7: "魔族", 8: "矮人", 9: "妖精",
        }
        return race_map.get(race_talent, "人类")






    def _get_character_recover_cost(self, char: Character) -> int:
        hp_gap = max(0, int(char.maxbase.get(0, 0)) - int(char.base.get(0, 0)))
        mp_gap = max(0, int(char.maxbase.get(1, 0)) - int(char.base.get(1, 0)))
        return hp_gap * 10 // 3 + mp_gap * 5 // 3






    def _get_character_relation(self, char: Character) -> int:
        if char is None:
            return 0
        idx = self._find_character_index(char)
        if idx < 0:
            return 0
        relation = self.interpreter.vars.relation
        if idx < len(relation):
            return int(relation[idx])
        return 0






    def _get_character_return_tag(self, char: Character) -> str:
        return "<归还中>" if char.cflag.get(507, 0) else ""






    def _get_character_self_call_text(self, target: Character) -> str:
        return str(target.cstr.get(60, "")).strip() or "我"




    def _get_character_status_text(self, char: Character) -> str:
        status_map = {
            0: "待机",
            2: "侵攻中",
            3: "迎击中",
            7: "待处刑",
            8: "固定示众",
            9: "NTR中",
            12: "迷宫探索",
        }
        return status_map.get(char.cflag.get(1, 0), f"状态{char.cflag.get(1, 0)}")






    def _get_character_template_baseline(self, template_id: Optional[int]) -> Optional[Character]:
        if template_id is None:
            return None
        return self._load_character_template(int(template_id))






    def _get_character_template_baseline_for_target(self, target: Optional[Character]) -> Optional[Character]:
        return self._get_character_template_baseline(self._get_character_template_id(target))






    def _get_character_template_id(self, target: Optional[Character]) -> Optional[int]:
        if target is None:
            return None
        template_id = getattr(target, "template_id", None)
        if isinstance(template_id, int) and template_id > 0:
            return template_id
        return None






    def _get_character_vanish_flag_id(self, template_id: int) -> int:
        return 1000 + int(template_id)




    def _handle_character_info_detail_action(self, selected_idx: int, char: Character, detail_choice: str) -> bool:
        if detail_choice == "100":
            return True
        try:
            action_id = int(detail_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        ok, message = self._apply_character_detail_action(selected_idx, char, action_id)
        print(f"\n{message}")
        self._pause()
        return False






    def _handle_character_info_invalid_choice(
        self,
        page: int,
        sort_mode: int,
        status_cycle: int,
    ) -> tuple[int, int, int, Optional[int]]:
        print("\nInvalid selection.")
        self._pause()
        return page, sort_mode, status_cycle, None






    def _handle_character_info_list_choice(
        self,
        choice: str,
        page: int,
        max_page: int,
        sort_mode: int,
        status_cycle: int,
    ) -> tuple[int, int, int, Optional[int]]:
        special_result = self._handle_character_info_special_choice(choice, page, max_page, sort_mode, status_cycle)
        if special_result is not None:
            return special_result
        try:
            selected_idx = int(choice)
        except ValueError:
            return self._handle_character_info_invalid_choice(page, sort_mode, status_cycle)
        if selected_idx < 0 or selected_idx >= len(self.interpreter.vars.chars):
            return self._handle_character_info_invalid_choice(page, sort_mode, status_cycle)
        return page, sort_mode, status_cycle, selected_idx






    def _handle_character_info_selection(self, selected_idx: Optional[int]) -> bool:
        return self._advance_character_info_selection(selected_idx)






    def _handle_character_info_special_choice(
        self,
        choice: str,
        page: int,
        max_page: int,
        sort_mode: int,
        status_cycle: int,
    ) -> Optional[tuple[int, int, int, Optional[int]]]:
        if choice == "999":
            return page, sort_mode, status_cycle, -1
        if choice == "997":
            if page > 0:
                page -= 1
            return page, sort_mode, status_cycle, None
        if choice == "998":
            if page < max_page:
                page += 1
            return page, sort_mode, status_cycle, None
        if choice in {"1200", "1300", "1400", "1500"}:
            new_sort = int(choice)
            if sort_mode == new_sort and new_sort == 1300:
                status_cycle += 1
            else:
                sort_mode = new_sort
                status_cycle = 0
            page = 0
            return page, sort_mode, status_cycle, None
        return None






    def _init_character_names(self, char_idx: int) -> Dict[str, Any]:
        """初始化角色名称 - 对应 @CHARA_NAME_INIT"""
        v = self.interpreter.vars
        if char_idx < 0 or char_idx >= len(v.chars):
            return {'success': False, 'message': "无效角色"}

        char = v.chars[char_idx]
        result = {'success': True, 'names': {}}

        # 自称初始化
        if not char.callname:
            char.callname = self._get_default_callname(char)

        result['names'] = {
            'name': char.savestr,
            'callname': char.callname or "",
            'nickname': char.nickname or "",
        }

        return result






    def _is_character_in_active_campaign(self, char: Character) -> bool:
        return (
            self._get_active_campaign_id() > 0
            and int(char.cflag.get(1, 0)) == 12
            and int(char.cflag.get(521, 0)) == 1
        )




    def _is_character_jp_name(self, target: Character) -> bool:
        """Determine if character has a Japanese-style name (NID_GET_TYPE == 0).
        Simplified heuristic based on character template.
        """
        template_id = target.template_id
        if template_id is not None and template_id >= 80000:
            return False
        return True

    # =========================================================================
    # CONFIG (配置系统)
    # =========================================================================






    def _mark_character_public_video(self, target: Character, title: str) -> None:
        target.cflag[497] = 1
        target.cflag[493] = max(int(target.cflag.get(493, 0)), max(100, len(title) * 10))
        target.cflag[494] = max(0, min(int(target.cflag.get(494, 0)), 90))




    def _mark_character_vanished(self, target: Optional[Character]):
        template_id = self._get_character_template_id(target)
        if template_id is None:
            return
        flag_id = self._get_character_vanish_flag_id(template_id)
        current = int(self.interpreter.vars.get_flag(flag_id, 0))
        if current > -2:
            self.interpreter.vars.set_flag(flag_id, -2)




    def _move_character_to_nursery(self, char: Character, previous_state: Optional[int] = None):
        char.cflag[1] = 10




    def _open_character_ability_up_menu(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_open_ability_up_for_target(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        previous_target = self.interpreter.vars.target
        self.interpreter.vars.target = idx
        self.show_ability_up()
        self.interpreter.vars.target = previous_target
        return True, "已打开能力提升菜单。"






    def _open_character_dress_menu(self, idx: int, char: Character) -> tuple[bool, str]:
        blocked_reason = self._can_select_standby_slave(idx, char)
        if blocked_reason is not None:
            return False, blocked_reason
        previous_target = self.interpreter.vars.target
        self.interpreter.vars.target = idx
        self.show_dress()
        self.interpreter.vars.target = previous_target
        return True, "已打开换装菜单。"






    def _open_character_equipment_detail(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._can_show_character_equipment(idx, char):
            return False, "当前还无法查看这名角色的装备信息。"
        self._show_character_equipment_detail(char)
        return True, "已打开装备查看菜单。"






    def _prompt_character_info_list_choice(self, sort_entries: List[tuple[int, str]]) -> str:
        return self._prompt_choice()






    def _prompt_character_job_change_choice(self, job_options: List[tuple[int, int, str]]) -> int:
        print("\n请选择转职目标")
        for menu_id, _, label in job_options:
            print(f" [{menu_id}] {label}")
        print(" [999] 停止")
        choice = self._prompt_choice()
        if choice == "999":
            return -1
        try:
            return int(choice)
        except ValueError:
            return None




    def _prompt_character_part_time_job(self, job_options: List[tuple[int, str]]) -> Optional[tuple[int, str]]:
        print("\n请选择打工项目")
        for index, (_, label) in enumerate(job_options):
            print(f" [{index}] {label}")
        print(" [100] 返回")
        choice = self._prompt_choice()
        if choice == "100":
            return None
        try:
            selected_index = int(choice)
        except ValueError:
            return None
        if selected_index < 0 or selected_index >= len(job_options):
            return None
        return job_options[selected_index]




    def _prompt_character_part_time_level(self) -> Optional[int]:
        print("\n请设定等级")
        print(" [0] [1] [2] [3] [4] [5]")
        level_choice = self._prompt_choice()
        try:
            return int(level_choice)
        except ValueError:
            return None




    def _remap_character_index_after_removal(self, ref_idx: int, removed_idx: int, missing_value: int = 0) -> int:
        ref_idx = int(ref_idx)
        if ref_idx == removed_idx:
            return int(missing_value)
        if ref_idx > removed_idx:
            return ref_idx - 1
        return ref_idx




    def _remap_character_index_token_after_removal(self, token: int, removed_idx: int) -> int:
        token = int(token)
        partner_idx = token // 1000
        if partner_idx == removed_idx:
            return 0
        if partner_idx <= removed_idx:
            return token
        look_id = token % 1000
        return (partner_idx - 1) * 1000 + look_id




    def _remap_character_indices_after_removal(self, removed_idx: int):
        for char in self.interpreter.vars.chars:
            self._remap_character_indices_after_removal_for_leader_flags(char, removed_idx)
            self._remap_character_indices_after_removal_for_marriage(char, removed_idx)
            self._remap_character_indices_after_removal_for_father(char, removed_idx)

        self._remap_character_indices_after_removal_for_lover_store(removed_idx)
        self._remap_character_indices_after_removal_for_globals(removed_idx)




    def _remap_character_indices_after_removal_for_father(self, char: Character, removed_idx: int):
        father_token = int(char.cflag.get(112, 0))
        if father_token > 902:
            remapped_father_token = self._remap_character_index_token_after_removal(father_token - 9, removed_idx)
            char.cflag[112] = remapped_father_token + 9 if remapped_father_token > 0 else 0




    def _remap_character_indices_after_removal_for_globals(self, removed_idx: int):
        for global_id in (3, 2803):
            ref_idx = int(self.interpreter.vars.globals.get(global_id, 0))
            self.interpreter.vars.globals[global_id] = self._remap_character_index_after_removal(
                ref_idx,
                removed_idx,
                missing_value=0,
            )




    def _remap_character_indices_after_removal_for_leader_flags(self, char: Character, removed_idx: int):
        for flag_id in (531, 532, 533):
            ref_idx = int(char.cflag.get(flag_id, 0))
            char.cflag[flag_id] = self._remap_character_index_after_removal(ref_idx, removed_idx, missing_value=0)




    def _remap_character_indices_after_removal_for_lover_store(self, removed_idx: int):
        lover_store = self._get_dungeon_town_lover_store()
        remapped_store: Dict[int, Dict[str, int]] = {}
        for raw_idx, raw_entry in lover_store.items():
            entry_idx = int(raw_idx)
            if entry_idx == removed_idx:
                continue
            if not isinstance(raw_entry, dict):
                continue
            new_idx = entry_idx - 1 if entry_idx > removed_idx else entry_idx
            entry = dict(raw_entry)
            if int(entry.get("lover_flag", 0)) == 200:
                remapped_partner_token = self._remap_character_index_token_after_removal(
                    int(entry.get("partner_token", 0)),
                    removed_idx,
                )
                if remapped_partner_token <= 0:
                    continue
                entry["partner_token"] = remapped_partner_token
            remapped_store[new_idx] = entry
        self.interpreter.vars.items["dungeon_town_lovers"] = remapped_store




    def _remap_character_indices_after_removal_for_marriage(self, char: Character, removed_idx: int):
        marriage_state = int(char.cflag.get(601, 0))
        if marriage_state > 902:
            partner_token = marriage_state - 9
            remapped_partner_token = self._remap_character_index_token_after_removal(partner_token, removed_idx)
            if remapped_partner_token > 0:
                char.cflag[601] = remapped_partner_token + 9
            else:
                char.cflag[601] = 0
                char.cflag[602] = 0
                char.cflag[609] = 0




    def _remove_character_at(self, idx: int):
        if idx < 0 or idx >= len(self.interpreter.vars.chars):
            return
        removed = self.interpreter.vars.chars[idx]
        self._cleanup_character_links_before_removal(idx, removed)
        self._mark_character_vanished(removed)
        self.interpreter.vars.chars.pop(idx)
        self._remap_character_indices_after_removal(idx)

        remapped_target = self._remap_character_index_after_removal(
            self.interpreter.vars.target,
            idx,
            missing_value=-1,
        )
        if self.interpreter.vars.target == idx:
            self.interpreter.vars.target = -1
        else:
            self.interpreter.vars.target = remapped_target

        self.interpreter.vars.assi = self._remap_character_index_after_removal(
            self.interpreter.vars.assi,
            idx,
            missing_value=-1,
        )




    def _remove_character_by_template_id(self, template_id: int, departure_slot: Optional[int] = None):
        for idx, char in enumerate(self.interpreter.vars.chars):
            raw_template_id = getattr(char, "template_id", None)
            if raw_template_id is None:
                raw_template_id = char.cflag.get(190, 0) or 0
            if int(raw_template_id) != int(template_id):
                continue
            if departure_slot is not None:
                self._store_departed_character(int(departure_slot), char)
            self._remove_character_from_party(idx)
            self._remove_character_at(idx)
            return




    def _remove_character_from_party(self, idx: int):
        if idx <= 0 or idx >= len(self.interpreter.vars.chars):
            return
        target = self.interpreter.vars.chars[idx]
        leader = int(target.cflag.get(533, 0))
        if leader <= 0 or leader >= len(self.interpreter.vars.chars):
            return

        rest_a = int(self.interpreter.vars.chars[leader].cflag.get(531, 0))
        rest_b = int(self.interpreter.vars.chars[leader].cflag.get(532, 0))
        if idx == leader:
            self._clear_party_leader_slots(self.interpreter.vars.chars[leader])
            if 0 < rest_a < len(self.interpreter.vars.chars):
                self._clear_party_member_slots(self.interpreter.vars.chars[rest_a])
            if 0 < rest_b < len(self.interpreter.vars.chars):
                self._clear_party_member_slots(self.interpreter.vars.chars[rest_b])
            return
        if idx == rest_a:
            self.interpreter.vars.chars[leader].cflag[531] = 0
            self._clear_party_member_slots(target)
            return
        if idx == rest_b:
            self.interpreter.vars.chars[leader].cflag[532] = 0
            self._clear_party_member_slots(target)
            return

        self._clear_party_leader_slots(self.interpreter.vars.chars[leader])
        if 0 < rest_a < len(self.interpreter.vars.chars):
            self._clear_party_member_slots(self.interpreter.vars.chars[rest_a])
        if 0 < rest_b < len(self.interpreter.vars.chars):
            self._clear_party_member_slots(self.interpreter.vars.chars[rest_b])




    def _render_character_info_list(self, page: int, total_chars: int, sort_mode: int, status_cycle: int) -> None:
        print("\n【Character Info】")
        print("-" * 30)
        print(f" 请选择一个角色以了解详细信息。 <第{page + 1}页> (总计{total_chars}人)")
        for line in self._build_character_list_lines(page, sort_mode, status_cycle=status_cycle):
            print(line)
        print("-" * 30)
        sort_entries = self._get_character_info_sort_entries()
        print(" ".join(f"[{menu_id}] {label}" for menu_id, label in sort_entries))
        print(" [997] 上一页")
        print(" [998] 下一页")
        print(" [999] 返回")






    def _reset_character_location_state_if_needed(self, target: Character) -> None:
        if int(target.cflag.get(1, 0)) in (2, 3, 7, 8, 9, 10, 11, 12):
            return
        target.cflag[1] = 0






    def _reset_character_name(self, target: Character) -> tuple[bool, str]:
        template = self._get_character_template_baseline_for_target(target)
        if template is not None:
            target.name = template.name
            target.callname = template.callname or template.name
            target.nick_name = template.nick_name
            if int(target.cflag.get(450, 0)) >= 99:
                self._reset_character_self_call(target)
            return True, f"{target.callname}恢复了原来的名字……"
        target.callname = target.name or target.callname
        if int(target.cflag.get(450, 0)) >= 99:
            self._reset_character_self_call(target)
        return True, f"{target.callname}恢复了原来的名字……"




    def _reset_character_self_call(self, target: Character):
        template = self._get_character_template_baseline_for_target(target)
        if template is not None:
            template_self_call = str(template.cstr.get(60, "")).strip()
            if template_self_call:
                target.cstr[60] = template_self_call
                target.cflag[450] = 0
                return
        target.cstr[60] = "我"
        target.cflag[450] = 9






    def _resolve_character_body_profile_age(self, char: Character) -> int:
        existing_age = int(char.cflag.get(451, 0))
        if existing_age > 0:
            return existing_age

        template_id = self._get_character_template_id(char)
        if template_id == 17:
            return 12 + random.randint(0, 1)
        if template_id == 24:
            return 17 + random.randint(0, 1)

        expected_age = max(12, min(35, 17 + self._get_character_age_expectation_delta(char)))
        return max(10, self._normal_point_pickup(expected_age))






    def _resolve_character_marriage_partner(self, idx: int, char: Character) -> Optional[tuple[int, Character]]:
        marriage_state = int(char.cflag.get(601, 0))
        if marriage_state <= 902:
            return None
        partner_idx = (marriage_state - 9) // 1000
        if partner_idx <= 0 or partner_idx >= len(self.interpreter.vars.chars):
            return None
        partner = self.interpreter.vars.chars[partner_idx]
        if partner is char:
            return None
        return partner_idx, partner






    def _run_character_temptation_trials(self, target: Character, success: int, failure: int) -> int:
        total_gain = 0
        print("\n【魔的诱惑】")
        for _ in range(7):
            if self._is_temptation_try_successful(target, success, failure):
                total_gain += self._apply_temptation_trial_effect(target)
            else:
                print("诱惑被切断了！")
        return total_gain




    def _set_character_bitch_level(self, target: Character) -> tuple[bool, str]:
        print("\n请设定等级")
        print(" [0] [1] [2] [3] [4] [5]")
        choice = self._prompt_choice()
        try:
            level = int(choice)
        except ValueError:
            return False, "已取消设置。"
        if level < 0 or level > 5:
            return False, "输入无效。"

        target.cflag[120] = level
        if level == 0:
            return True, "卖春积极性变成没有了"
        if level == 1:
            return True, "卖春积极性变成普通了"
        return True, f"卖春积极性变为等级{level}了"




    def _set_character_campaign_standby_state(self, char: Character) -> None:
        char.cflag[1] = 0
        char.cflag[500] = 0
        self._reset_dungeon_floor_progress(char, floor=1, return_flag=0)
        char.cflag[520] = 0
        char.cflag[521] = 0




    def _set_character_captured_standby_state(self, char: Character):
        char.cflag[1] = 0
        char.cflag[500] = 0
        self._reset_dungeon_floor_progress(char, floor=max(1, int(char.cflag.get(501, 1))), return_flag=0)
        char.cflag[506] = 1




    def _set_character_due_birth(self, target: Character, source: int, father_flag: int = 0, father_name: str = "", monster_father_id: int = 0):
        if target.talent.get(153, 0) or int(target.cflag.get(110, 0)) > 0 or int(target.cflag.get(102, 0)) != int(source):
            return
        self._set_pregnancy_due_day(target, 10 + random.randint(0, 5))
        target.cflag[111] = int(father_flag)
        target.cflag[112] = int(monster_father_id)
        if father_name:
            target.cstr[2] = father_name






    def _set_character_ex_talent(self, target: Character, talent_id: int, value: int) -> None:
        store = self._get_character_ex_talent_store(target)
        normalized = max(0, int(value))
        if normalized <= 0:
            store.pop(int(talent_id), None)
            return
        store[int(talent_id)] = normalized






    def _set_character_flag_bit(self, char: Character, flag_idx: int, bit: int, enabled: bool) -> None:
        value = int(char.cflag.get(flag_idx, 0))
        if enabled:
            value |= (1 << bit)
        else:
            value &= ~(1 << bit)
        char.cflag[flag_idx] = value






    def _set_character_job_stats(self, target: Character):
        if target.talent.get(200, 0) or target.talent.get(205, 0):
            values = (20, 20, 20, 20)
        elif target.talent.get(201, 0) or target.talent.get(206, 0):
            values = (15, 15, 15, 15)
        elif target.talent.get(202, 0) or target.talent.get(207, 0):
            values = (15, 20, 15, 20)
        elif target.talent.get(203, 0) or target.talent.get(208, 0):
            values = (20, 15, 20, 15)
        elif target.talent.get(210, 0) or target.talent.get(211, 0):
            values = (40, 40, 40, 40)
        else:
            values = (15, 15, 15, 15)
        target.cflag[11], target.cflag[12], target.cflag[13], target.cflag[14] = values
        target.maxbase[0] = 2500 if (target.talent.get(210, 0) or target.talent.get(211, 0)) else 2000
        target.maxbase[1] = 2500 if (target.talent.get(210, 0) or target.talent.get(211, 0)) else 2000
        target.base[0] = target.maxbase[0]
        target.base[1] = target.maxbase[1]




    def _set_character_lover(self, idx: int, char: Character) -> tuple[bool, str]:
        if self._has_dungeon_town_lover(idx):
            return False, f"{char.name} 已经有恋人了。"
        messages = self._ensure_dungeon_town_lover(idx, char)
        if not messages:
            return False, f"{char.name} 当前没能找到合适的恋人对象。"
        return True, "\n".join(messages)






    def _set_character_ntr_captive_state(self, char: Character) -> None:
        char.cflag[1] = 9
        char.cflag[500] = 0
        self._reset_dungeon_floor_progress(char, floor=max(1, int(char.cflag.get(501, 1))), return_flag=0)
        char.cflag[506] = 0




    def _set_character_part_time_level(self, target: Character) -> tuple[bool, str]:
        job_options = self._get_character_part_time_job_options()
        selected = self._prompt_character_part_time_job(job_options)
        if selected is None:
            return False, "已取消设置。"
        selected_flag, selected_label = selected
        level = self._prompt_character_part_time_level()
        if level is None:
            return False, "已取消设置。"
        if level < 0 or level > 5:
            return False, "输入无效。"
        return self._apply_character_part_time_level(target, job_options, selected_flag, selected_label, level)




    def _set_character_self_call(self, idx: int, target: Character) -> tuple[bool, str]:
        if not self._can_reset_character_self_call(idx, target):
            return False, "无效对象"
        print("\n请输入想设定的第一人称，若不输入则恢复默认")
        new_self_call = self._prompt_choice("Self Call >> ")
        if new_self_call:
            target.cstr[60] = new_self_call
            target.cflag[450] = 0
            return True, f"{target.name} 的第一人称变成了「{new_self_call}」。"
        self._reset_character_self_call(target)
        return True, f"{target.name} 的第一人称恢复为「{self._get_character_self_call_text(target)}」。"




    def _show_character_equipment_detail(self, target: Character):
        print("\n【装备情报】")
        print("-" * 30)
        print(f" 角色: {target.name}")
        for line in self._build_character_equipment_detail_lines(target):
            print(line)




    def _show_character_info_detail(self, selected_idx: int, char: Character):
        while True:
            if self._advance_character_info_detail(selected_idx, char):
                return




    def _show_character_info_list(self, page: int, sort_mode: int, status_cycle: int, page_size: int) -> tuple[int, int, int, Optional[int]]:
        return self._advance_character_info_list(page, sort_mode, status_cycle, page_size)




    def _toggle_character_favorite(self, idx: int, char: Character) -> tuple[bool, str]:
        char.cflag[700] = 0 if char.cflag.get(700, 0) else 1
        return True, f"{char.name} {'已取消收藏' if char.cflag.get(700, 0) == 0 else '已加入收藏'}。"






    def show_character_info(self):
        """Character info menu aligned to the current CHARA_INFO list/detail scope."""
        page = 0
        sort_mode = 1200
        status_cycle = 0
        page_size = 24
        while True:
            page, sort_mode, status_cycle, selected_idx = self._advance_character_info_menu(page, sort_mode, status_cycle, page_size)
            if self._advance_character_info_selection(selected_idx):
                return





