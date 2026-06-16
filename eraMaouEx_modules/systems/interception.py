from __future__ import annotations
"""Module for InterceptionMixin - 迎击系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class InterceptionMixin:
    """Mixin providing 迎击系统 methods for GameEngine"""

    def _advance_interception_menu(self) -> bool:
        candidates = self._list_interception_candidates()
        self._render_interception_menu(candidates)
        choice = self._prompt_interception_choice()
        if choice == "100":
            return True
        selected_pair = self._handle_interception_candidate_selection(choice, candidates)
        if selected_pair is None:
            return False

        idx, selected = selected_pair
        self._show_interception_target_menu(idx, selected)
        return False




    def _advance_interception_target_menu(
        self,
        selected_idx: int,
        selected_char: Character,
        state: Dict[str, Any],
    ) -> bool:
        self._render_interception_target_menu(selected_char, int(state["floor"]), int(state["work_id"]), bool(state["supply_enabled"]))
        sub_choice = self._prompt_interception_target_choice()
        return self._handle_interception_target_menu_choice(
            sub_choice,
            selected_idx,
            selected_char,
            state,
        )




    def _apply_interception_advance_result(self, leader: Character, floor_before: int, advanced: bool) -> tuple[bool, List[str]]:
        if leader.cflag.get(1, 0) != 3 or not advanced:
            return False, []
        if leader.cflag.get(500, 0) != 3:
            return False, []
        messages = [
            f"{leader.name} 企图扩张第{floor_before}阶层的设施，但是失败了。",
            f"{leader.name} 使用回城魔法撤回了。",
        ]
        self._set_character_dungeon_return_standby_state(leader, floor=1, success=False)
        return True, messages






    def _apply_interception_facility_expansion(self, floor: int, work_id: int) -> Optional[str]:
        if work_id != 3:
            return None
        level_flag = floor + 359
        current_level = self._get_interception_facility_level(floor)
        new_level = min(3, current_level + 1)
        self.interpreter.vars.set_flag(level_flag, new_level)
        facility_name = self._get_interception_facility_name(floor) or "设施"
        return f"{floor}层的{facility_name}扩张为等级{new_level}。"






    def _apply_interception_room_expansion(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if leader.cflag.get(1, 0) != 3 or leader.cflag.get(500, 0) != 3:
            return messages
        room_id = self._get_dungeon_floor_room(floor)
        if room_id <= 0:
            return messages
        extra = self._get_dungeon_floor_room_extra(floor)
        available_bits = [bit for bit in (1, 2) if (extra & bit) == 0]
        if not available_bits:
            return messages
        if random.randint(0, 3) == 0:
            bit = 1
        elif random.randint(0, 2) == 0:
            bit = 2
        else:
            return messages
        if bit not in available_bits:
            return messages
        extra |= bit
        self._set_dungeon_floor_room_extra(floor, extra)
        leader.cflag[500] = 0
        room_name = self._get_dungeon_room_name(room_id)
        messages.append(f"{leader.name} 成功扩张了第{floor}阶层的{room_name}。")
        messages.append(f"{leader.name} 的顺带工作变回了内职。")
        return messages






    def _apply_interception_spy_action(self, infiltrator_idx: int, infiltrator: Character, floor: int) -> tuple[bool, bool, List[str]]:
        if infiltrator.cflag.get(1, 0) != 3 or infiltrator.cflag.get(500, 0) != 4:
            return False, False, []
        targets = self._get_interception_target_candidates(floor, exclude_idx=infiltrator_idx)
        if not targets:
            return False, False, [f"{infiltrator.name} 在第{floor}阶层搜索勇者，但没有找到下手的机会。"]
        target_idx, target = random.choice(targets)
        same_work_count = 1 + sum(1 for idx, char in self._get_dungeon_party_candidates() if idx != infiltrator_idx and char.cflag.get(1, 0) == 3 and char.cflag.get(500, 0) == 4 and int(char.cflag.get(501, 1)) == floor)
        rate = self._get_interception_spy_betray_rate(infiltrator, target, same_work_count)
        if random.randint(0, 99) >= rate:
            return False, False, [f"{infiltrator.name} 窥探着 {target.name} 的行动，但一直没有找到背叛的机会。"]

        reward = 100 * self._get_character_level(target)
        self._add_global_money(reward)
        infiltrator.cflag[505] = infiltrator.cflag.get(505, 0) + 1
        self._set_character_captured_standby_state(target)
        self._remove_character_from_party(target_idx)
        messages = [
            f"{infiltrator.name} 在第{floor}阶层成功背叛并擒获了 {target.name}。",
            f"获得了 {reward} pts。",
        ]
        if random.randint(0, 1) == 0:
            self._set_character_dungeon_return_standby_state(
                infiltrator,
                floor=max(1, int(infiltrator.cflag.get(501, 1))),
                success=True,
            )
            messages.append(f"{infiltrator.name} 使用回城魔法撤回了。")
        return True, True, messages






    def _apply_interception_supply(self, char: Character) -> tuple[int, int]:
        player = self._get_player()
        if player is None:
            return 0, 0
        stocked = 0
        for _ in range(4):
            reward_pool = self._get_available_dungeon_equip_reward_pool()
            if not reward_pool:
                break
            item_id = random.choice(reward_pool)
            self._add_item(player, self._get_item_name(item_id), 1)
            stocked += 1
        refund = 2000 if stocked == 0 else 0
        return stocked, refund






    def _apply_interception_training_bonus(self, leader: Character) -> List[str]:
        if leader.cflag.get(1, 0) != 3 or leader.cflag.get(500, 0) != 5:
            return []
        bonus = self._get_interception_master_level()
        if bonus <= 0:
            return []
        leader.exp[80] = leader.exp.get(80, 0) + bonus
        return [f"{leader.name} 在迎击途中和怪物们进行了训练，经验值 +{bonus}。"]






    def _apply_interception_trap_restock(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if leader.cflag.get(1, 0) != 3 or leader.cflag.get(500, 0) != 2:
            return messages
        player = self._get_player()
        if player is None:
            return messages
        gained = 0
        sold = 0
        for flag_id in self._get_dungeon_floor_trap_flag_ids(floor):
            trap_id = int(self.interpreter.vars.get_flag(flag_id, -1))
            if trap_id <= 0 or trap_id >= 99 or trap_id not in self.item_catalog:
                continue
            trap_name = self._get_item_name(trap_id)
            if self._get_item_count(player, trap_id) < 99:
                self._add_item(player, trap_name, 1)
                gained += 1
            else:
                price = max(1, self._get_dungeon_treasure_reward(trap_id))
                self._add_global_money(price)
                sold += price
        if gained > 0:
            messages.append(f"{leader.name} 补充了第{floor}阶层的陷阱库存，共回收 {gained} 件。")
        if sold > 0:
            messages.append(f"{leader.name} 将多余的陷阱换成了 {sold} pts。")
        return messages






    def _assign_interception_reward_request(self, char: Character):
        if char.talent.get(136, 0):
            char.cflag[504] = random.randint(1, 3) if random.randint(0, 2) == 0 else 0
            return
        if char.talent.get(85, 0):
            wish = random.randint(4, 6)
            player = self._get_player()
            if wish == 6 and player is not None and not (player.talent.get(121, 0) or player.talent.get(122, 0)):
                wish = 4
            char.cflag[504] = wish
            return
        if char.talent.get(76, 0):
            char.cflag[504] = random.randint(7, 9)
            return
        char.cflag[504] = 0






    def _build_interception_status_line(self, idx: int, char: Character) -> str:
        cost = self._get_interception_dispatch_cost(char)
        tags: List[str] = [f"LV{self._get_character_level(char)}"]
        if char.cflag.get(0, 0) > 0:
            tags.append("可卖")
        elif char.talent.get(254, 0):
            tags.append("洗脑服从")
        if char.talent.get(153, 0):
            tags.append("怀孕")
        if self._is_maou_shadow(char):
            tags.append("近卫")
        if char.talent.get(291, 0):
            tags.append("后代")
        cost_text = "免费" if cost == 0 else f"{cost}pts"
        return f"[{idx}] {char.name} {' '.join(tags)} 派遣费:{cost_text}"






    def _create_interception_target_state(self, selected_char: Character) -> Dict[str, Any]:
        work_id = int(selected_char.cflag.get(500, 0))
        if work_id not in self._get_interception_work_options():
            work_id = 0
        return {"floor": 9, "work_id": work_id, "supply_enabled": False}






    def _dispatch_interception(
        self,
        idx: int,
        char: Character,
        floor: int,
        work_id: int,
        supply_enabled: bool,
    ) -> tuple[bool, str]:
        blocked_reason = self._get_interception_work_blocked_reason(floor, work_id)
        if blocked_reason is not None:
            return False, blocked_reason
        cost = self._get_interception_dispatch_cost(char)
        total_cost = cost + self._get_interception_extra_cost(floor, work_id, supply_enabled)
        if self.interpreter.vars.money < total_cost:
            return False, "资金不足，无法完成这次迎击派遣。"

        self._spend_global_money(total_cost)
        self._set_dungeon_assignment_state(char, state=3, work_id=work_id, floor=floor, progress=90, fatigue=0, return_flag=0)
        self._assign_interception_reward_request(char)

        messages = [f"{char.name} 被派去第{floor}阶层迎击勇者。", f"顺带工作: {self._get_interception_work_name(work_id)}"]
        expansion_message = self._apply_interception_facility_expansion(floor, work_id)
        if expansion_message:
            messages.append(expansion_message)
        if supply_enabled:
            stocked, refund = self._apply_interception_supply(char)
            if refund > 0:
                self._add_global_money(refund)
                messages.append("补给已满，2000 pts 已退回。")
            else:
                messages.append(f"已为队伍补给 {stocked} 件道具。")
        return True, "\n".join(messages)






    def _get_interception_blocked_reason(self, idx: int, char: Optional[Character]) -> Optional[str]:
        if idx < 0 or char is None:
            return "无效对象"
        if char.base.get(0, 0) < 1:
            return "濒死中，无法选择"
        if idx == 0:
            return "魔王大人，亲自迎击的话，这几天就不能爱爱了哦！才不要！"
        if char.cflag.get(1, 0) != 0:
            return "不能选择非待命状态的奴隶"
        if char.cflag.get(0, 0) == 0 and not char.talent.get(254, 0):
            return f"{char.name}还未被驯服，拒绝你的命令了。"
        if char.cflag.get(0, 0) == 0 and char.talent.get(254, 0) and self.interpreter.vars.money < self._get_interception_dispatch_cost(char):
            return f"金钱不足，{char.name}无视了你的命令"
        if char.talent.get(153, 0) and self.interpreter.vars.get_flag(5, 0) & (1 << 10) == 0:
            return f"{char.name}怀孕了，派孕妇打仗是违反月内瓦条约的～"
        if self._is_maou_shadow(char):
            return "待着身边的才叫近卫嘛。"
        if char.talent.get(291, 0) and not self._has_interception_child_lock_override():
            return "毕竟是自己的孩子，怎么忍心随意放手嘛。"
        return None






    def _get_interception_dispatch_cost(self, char: Character) -> int:
        return 0 if char.cflag.get(0, 0) > 0 else 6000






    def _get_interception_extra_cost(self, floor: int, work_id: int, supply_enabled: bool) -> int:
        extra_cost = 2000 if work_id == 3 else 0
        if supply_enabled:
            extra_cost += 2000
        return extra_cost






    def _get_interception_facility_level(self, floor: int) -> int:
        if floor < 1 or floor > 9:
            return 0
        return max(0, int(self.interpreter.vars.get_flag(floor + 359, 0)))






    def _get_interception_facility_name(self, floor: int) -> str:
        if floor < 1 or floor > 9:
            return ""
        room_id = max(0, int(self.interpreter.vars.get_flag(floor + 349, 0)))
        if room_id <= 0:
            return ""
        return self._get_item_name(room_id)






    def _get_interception_master_level(self) -> int:
        player = self._get_player()
        if player is None:
            return 0
        return max(0, int(player.cflag.get(9, 0)))






    def _get_interception_spy_betray_rate(self, infiltrator: Character, target: Character, same_work_count: int) -> int:
        hp_max = max(1, int(target.maxbase.get(0, 0)))
        mp_max = max(1, int(target.maxbase.get(1, 0)))
        hp_ratio = int(target.base.get(0, 0)) * 100 // hp_max
        mp_ratio = int(target.base.get(1, 0)) * 100 // mp_max
        weakness = max(0, 100 - hp_ratio) + max(0, 100 - mp_ratio)
        level_gap = max(-5, min(5, self._get_character_level(infiltrator) - self._get_character_level(target)))
        rate = weakness // 4
        rate += max(0, infiltrator.cflag.get(2, 0)) // 50
        rate += max(0, infiltrator.abl.get(20, 0)) * 3
        rate += level_gap * 3
        if same_work_count >= 2:
            rate *= 2
        return max(5, min(90, rate // 2))






    def _get_interception_target_candidates(self, floor: int, exclude_idx: Optional[int] = None) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if exclude_idx is not None and idx == exclude_idx:
                continue
            if char.base.get(0, 0) < 1:
                continue
            if char.cflag.get(1, 0) != 2:
                continue
            if int(char.cflag.get(501, 1)) != floor:
                continue
            candidates.append((idx, char))
        return candidates






    def _get_interception_work_blocked_reason(self, floor: int, work_id: int) -> Optional[str]:
        if work_id != 3:
            return None
        facility_name = self._get_interception_facility_name(floor)
        if not facility_name:
            return f"{floor}层没有任何设施"
        if self._get_interception_facility_level(floor) >= 3:
            return f"{floor}层的{facility_name}已经扩张到极限了。"
        return None






    def _get_interception_work_name(self, work_id: int) -> str:
        names = {
            0: "内职",
            1: "卖淫",
            2: "补充陷阱",
            3: "扩张设施",
            4: "潜入敌方",
            5: "训练",
        }
        return names.get(work_id, f"工作{work_id}")






    def _get_interception_work_options(self) -> List[int]:
        master_level = self._get_interception_master_level()
        return [work_id for work_id in [0, 1, 2, 3, 4, 5] if master_level >= self._get_interception_work_required_level(work_id)]






    def _get_interception_work_required_level(self, work_id: int) -> int:
        requirements = {
            0: 0,
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50,
        }
        return requirements.get(work_id, 0)






    def _handle_interception_candidate_selection(self, choice: str, candidates: List[tuple[int, Character]]) -> Optional[tuple[int, Character]]:
        try:
            selected_idx = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None

        selected_char = self.interpreter.vars.chars[selected_idx] if 0 <= selected_idx < len(self.interpreter.vars.chars) else None
        blocked_reason = self._get_interception_blocked_reason(selected_idx, selected_char)
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            self._pause()
            return None

        selected_pair = next(((idx, char) for idx, char in candidates if idx == selected_idx), None)
        if selected_pair is None:
            print("\nInvalid selection.")
            self._pause()
            return None
        return selected_pair






    def _handle_interception_target_menu_choice(
        self,
        sub_choice: str,
        selected_idx: int,
        selected_char: Character,
        state: Dict[str, Any],
    ) -> bool:
        handled, exit_menu = self._handle_interception_target_menu_command_choice(
            sub_choice,
            selected_idx,
            selected_char,
            state,
        )
        if handled:
            return exit_menu
        print("\nInvalid selection.")
        self._pause()
        return False






    def _handle_interception_target_menu_command_choice(
        self,
        sub_choice: str,
        selected_idx: int,
        selected_char: Character,
        state: Dict[str, Any],
    ) -> tuple[bool, bool]:
        if sub_choice == "999":
            return True, True
        if sub_choice == "0":
            return self._handle_interception_target_menu_floor_command(state)
        if sub_choice == "1":
            return self._handle_interception_target_menu_work_command(state)
        if sub_choice == "2":
            return self._handle_interception_target_menu_supply_command(selected_char, state)
        if sub_choice == "998":
            return self._handle_interception_target_menu_dispatch_command(selected_idx, selected_char, state)
        return False, False






    def _handle_interception_target_menu_dispatch_command(
        self,
        selected_idx: int,
        selected_char: Character,
        state: Dict[str, Any],
    ) -> tuple[bool, bool]:
        ok, message = self._dispatch_interception(
            selected_idx,
            selected_char,
            int(state["floor"]),
            int(state["work_id"]),
            bool(state["supply_enabled"]),
        )
        print(f"\n{message}")
        self._pause()
        return True, True






    def _handle_interception_target_menu_floor_choice(self, floor_choice: str, work_id: int) -> Optional[int]:
        try:
            new_floor = int(floor_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        if new_floor < 1 or new_floor > 9:
            print("\nInvalid selection.")
            self._pause()
            return None
        if work_id not in self._get_interception_work_options():
            return 0
        return new_floor






    def _handle_interception_target_menu_floor_command(self, state: Dict[str, Any]) -> tuple[bool, bool]:
        floor_choice = self._prompt_choice("出发层(1-9) >> ")
        new_floor = self._handle_interception_target_menu_floor_choice(floor_choice, int(state["work_id"]))
        if new_floor is not None:
            state["floor"] = new_floor
        return True, False






    def _handle_interception_target_menu_supply_choice(
        self,
        selected_char: Character,
        floor: int,
        work_id: int,
        supply_enabled: bool,
    ) -> Optional[bool]:
        if not supply_enabled:
            projected_cost = self._get_interception_dispatch_cost(selected_char) + self._get_interception_extra_cost(floor, work_id, True)
            if self.interpreter.vars.money < projected_cost:
                print("\n* 魔王大人，你怎么这么穷 *")
                self._pause()
                return None
        return not supply_enabled






    def _handle_interception_target_menu_supply_command(
        self,
        selected_char: Character,
        state: Dict[str, Any],
    ) -> tuple[bool, bool]:
        new_supply = self._handle_interception_target_menu_supply_choice(
            selected_char,
            int(state["floor"]),
            int(state["work_id"]),
            bool(state["supply_enabled"]),
        )
        if new_supply is not None:
            state["supply_enabled"] = new_supply
        return True, False






    def _handle_interception_target_menu_work_choice(self, floor: int, current_work_id: int) -> Optional[int]:
        if not self._show_interception_work_selection(floor, current_work_id):
            return None
        work_choice = self._prompt_choice()
        try:
            new_work = int(work_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        if new_work not in self._get_interception_work_options():
            print("\nInvalid selection.")
            self._pause()
            return None
        blocked_reason = self._get_interception_work_blocked_reason(floor, new_work)
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            self._pause()
            return None
        return new_work






    def _handle_interception_target_menu_work_command(self, state: Dict[str, Any]) -> tuple[bool, bool]:
        new_work = self._handle_interception_target_menu_work_choice(int(state["floor"]), int(state["work_id"]))
        if new_work is not None:
            state["work_id"] = new_work
        return True, False






    def _has_interception_child_lock_override(self) -> bool:
        return bool(self.interpreter.vars.globals.get(9000, 0) & (1 << 1))






    def _is_interception_candidate(self, idx: int, char: Character) -> bool:
        return self._get_interception_blocked_reason(idx, char) is None






    def _list_interception_candidates(self) -> List[tuple[int, Character]]:
        return [
            (idx, char)
            for idx, char in enumerate(self.interpreter.vars.chars)
            if self._is_interception_candidate(idx, char)
        ]






    def _prompt_interception_choice(self) -> str:
        if not self._list_interception_candidates():
            self._pause()
            return "100"
        return self._prompt_choice()






    def _prompt_interception_target_choice(self) -> str:
        return self._prompt_choice()






    def _render_interception_menu(self, candidates: List[tuple[int, Character]]) -> None:
        print("\n【Interception】")
        print("-" * 30)
        print(" 派遣谁前去迎击勇者？")
        print(" 状态若非[可卖]，则需要 6000 pts 派遣费。")
        for idx, char in candidates:
            print(" " + self._build_interception_status_line(idx, char))
        print(" [100] Back")
        if not candidates:
            print(" 当前没有可派遣的迎击人选。")






    def _render_interception_target_menu(self, selected_char: Character, floor: int, work_id: int, supply_enabled: bool):
        blocked_work_reason = self._get_interception_work_blocked_reason(floor, work_id)
        print(f"\n【Interception: {selected_char.name}】")
        print("-" * 30)
        print(f" [0] 出发阶层 - {floor}层")
        print(f" [1] 迎击时顺带 - {self._get_interception_work_name(work_id)}")
        print(f" [2] 道具补给 - {'全副整装(2000G)' if supply_enabled else '裸奔吧，奴隶！'}")
        if blocked_work_reason is not None:
            print(f" 当前顺带工作限制: {blocked_work_reason}")
        print(" [998] 去吧！")
        print(" [999] Back")






    def _show_interception_target_menu(self, selected_idx: int, selected_char: Character):
        state = self._create_interception_target_state(selected_char)

        while True:
            if self._advance_interception_target_menu(selected_idx, selected_char, state):
                return




    def _show_interception_work_selection(self, floor: int, current_work_id: int) -> bool:
        print("\n选择顺带工作")
        master_level = self._get_interception_master_level()
        for work in [0, 1, 2, 3, 4, 5]:
            required_level = self._get_interception_work_required_level(work)
            suffix = " (需2000G)" if work == 3 else ""
            if master_level < required_level:
                print(f" [---] {self._get_interception_work_name(work)} (魔王等级不足)")
                continue
            line = f" [{work}] {self._get_interception_work_name(work)}{suffix}"
            blocked_reason = self._get_interception_work_blocked_reason(floor, work)
            if blocked_reason is not None:
                line += f" - {blocked_reason}"
            print(line)
        return True



    def show_interception(self):
        """Interception menu aligned to SHOP_2.ERB interception dispatch flow."""
        while True:
            if self._advance_interception_menu():
                return





