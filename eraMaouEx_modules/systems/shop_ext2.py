from __future__ import annotations
"""Module for ShopExt2Mixin - 商店系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ShopExt2Mixin:
    """Mixin providing 商店系统 methods for GameEngine"""

    def _advance_shop_group_menu(self, title: str, groups: List[Dict[str, Union[str, List[int]]]], switch_label: Optional[str] = None, switch_code: Optional[str] = None) -> Optional[str]:
        self._render_shop_group_menu(title, groups, switch_label=switch_label, switch_code=switch_code)
        choice = self._prompt_choice()
        return self._handle_shop_group_menu_choice(groups, choice, switch_code)




    def _advance_shop_group_page(self, group: Dict[str, Union[str, List[int]]], item_ids: List[int], page: int) -> tuple[bool, int]:
        page, page_items, page_count = self._prepare_shop_group_page(item_ids, page)
        self._render_shop_group_page(group, page, page_count, page_items)
        item_choice = self._prompt_choice()
        return self._handle_shop_group_item_choice(page_items, page, page_count, item_choice)




    def _advance_shop_main_menu(self):
        self._run_pending_morning_events_if_needed()
        self._normalize_shop_selection_state()
        self._render_shop_main_menu()
        choice = self._prompt_choice_raw()
        return self._handle_shop_main_menu_choice(choice)




    def _advance_shop_menu(self) -> Optional[str]:
        return self._show_shop_group_menu(
            "黑市商人",
            self._build_normal_shop_groups(),
            switch_label="陷阱",
            switch_code="998",
        )




    def _build_shop_command_lines(self) -> List[str]:
        labels = {
            100: "Training",
            101: "Character Info",
            102: "Dungeon" if self.interpreter.vars.get_flag(502, 0) == 0 else "场子",
            103: "Execution",
            104: "Interception",
            105: "Ability Up",
            106: "Sell",
            107: "Shop",
            108: "Dress",
            109: "Invasion",
            110: "Lab",
            111: "Facility",
            120: "Summon",
            199: "Rest",
            200: "Save",
            300: "Load",
            777: "Settings",
            888: "Communication",
        }
        command_order = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 120, 199, 200, 300, 777, 888]
        state = self._get_shop_command_state()
        lines: List[str] = []
        for command_id in command_order:
            if state.get(command_id, False):
                lines.append(f" [{command_id}] {labels[command_id]}")
            else:
                lines.append(f" [---] {labels[command_id]}")
        return lines






    def _build_shop_command_state(self, counts: Dict[str, int], player: Optional[Character], clothes_enabled: bool) -> Dict[int, bool]:
        standby_count = counts["standby"]
        sold_ready_count = counts["sold_ready"]
        char_count = counts["char_count"]
        return {
            100: standby_count > 0,
            101: char_count >= 1,
            102: True,
            103: standby_count > 0,
            104: standby_count > 0,
            105: True,
            106: sold_ready_count > 0,
            107: True,
            108: standby_count > 0 and clothes_enabled,
            109: True,
            110: bool(player is not None and player.talent.get(325, 0)),
            111: bool(self.interpreter.vars.get_flag(83, 0) or self.interpreter.vars.get_flag(84, 0)),
            120: True,
            199: True,
            200: True,
            300: True,
            777: True,
            888: True,
        }






    def _build_shop_group_consumables_items(self, player: Optional[Character], knowledge_alchemy: bool) -> List[int]:
        items = [24, 25, 34, 35]
        if player is not None and self._get_item_count(player, 6) > 0 and 28 in self.item_catalog:
            items.append(28)
        if knowledge_alchemy:
            items.extend([26, 27, 29, 30, 31, 40, 41])
        return [item_id for item_id in items if self._can_show_shop_item(item_id, player)]






    def _build_shop_group_items(
        self,
        definition: Dict[str, Any],
        player: Optional[Character],
        knowledge_alchemy: bool,
        knowledge_secret: bool,
        knowledge_succubus: bool,
        knowledge_bug: bool,
    ) -> Dict[str, Union[str, List[int]]]:
        title = str(definition["title"])
        kind = str(definition["kind"])
        if kind == "range":
            items = self._build_shop_group_range_items(definition, player)
        elif kind == "consumables":
            items = self._build_shop_group_consumables_items(player, knowledge_alchemy)
        elif kind == "knowledge":
            items = self._build_shop_group_knowledge_items(player, knowledge_secret, knowledge_succubus, knowledge_bug)
        elif kind == "trap":
            items = self._build_shop_group_trap_items()
        else:
            items = []
        return {"title": title, "items": items}






    def _build_shop_group_knowledge_items(
        self,
        player: Optional[Character],
        knowledge_secret: bool,
        knowledge_succubus: bool,
        knowledge_bug: bool,
    ) -> List[int]:
        items = [38, 39, 42, 52, 53]
        if self._can_show_shop_item(37, player):
            items.insert(0, 37)
        if knowledge_secret:
            items.append(33)
        return [item_id for item_id in items if self._can_show_shop_item(item_id, player)]






    def _build_shop_group_range_items(self, definition: Dict[str, Any], player: Optional[Character]) -> List[int]:
        start, end = definition["range"]
        items = [item_id for item_id in range(start, end) if item_id in self.item_catalog]
        if definition.get("filter_stock") and player is not None:
            items = [
                item_id for item_id in items
                if self._get_item_count(player, item_id) < self._get_item_stock_limit(item_id)
            ]
        return items






    def _build_shop_group_trap_items(self) -> List[int]:
        return [item_id for item_id in sorted(self.item_catalog) if 60 <= item_id < 90]






    def _build_shop_groups(self) -> List[Dict[str, Union[str, List[int]]]]:
        player = self._get_player()
        knowledge_alchemy = self._has_shop_knowledge(55)
        knowledge_secret = self._has_shop_knowledge(325)
        knowledge_succubus = self._has_shop_knowledge(327)
        knowledge_bug = self._has_shop_knowledge(328)
        groups: List[Dict[str, Union[str, List[int]]]] = []
        for definition in SHOP_GROUP_DEFINITIONS:
            groups.append(self._build_shop_group_items(definition, player, knowledge_alchemy, knowledge_secret, knowledge_succubus, knowledge_bug))
        return groups






    def _charge_shop_cost(self, cost: int):
        self._ensure_shop_cost_accounting()
        self._spend_global_money(cost)






    def _ensure_shop_cost_accounting(self):
        self.interpreter.vars.globals[4444] = self.interpreter.vars.globals.get(4444, 0)






    def _get_shop_assistant(self) -> Optional[Character]:
        return self._get_current_assistant()






    def _get_shop_command_counts(self) -> Dict[str, int]:
        standby_count = sum(1 for idx, char in enumerate(self.interpreter.vars.chars) if idx > 0 and char.cflag.get(1, 0) == 0)
        sold_ready_count = sum(1 for idx, char in enumerate(self.interpreter.vars.chars) if idx > 0 and char.cflag.get(0, 0) > 0)
        return {"standby": standby_count, "sold_ready": sold_ready_count, "char_count": len(self.interpreter.vars.chars)}






    def _get_shop_command_state(self) -> Dict[int, bool]:
        counts = self._get_shop_command_counts()
        player = self._get_player()
        clothes_enabled = self.interpreter.vars.get_flag(37, 0) == 1
        return self._build_shop_command_state(counts, player, clothes_enabled)






    def _get_shop_main_menu_handler(self, choice: str):
        simple_handlers = {
            "101": self.show_character_info,
            "102": self.show_dungeon,
            "103": self._handle_shop_command_103,
            "104": self._handle_shop_command_104,
            "105": self._handle_shop_command_105,
            "106": self._handle_shop_command_106,
            "107": self.show_shop,
            "108": self._handle_shop_command_108,
            "111": self._handle_shop_command_111,
            "120": self._handle_shop_command_120,
            "496": self._handle_shop_command_496,
            "497": self._handle_shop_command_497,
            "498": self._handle_shop_command_498,
            "499": self._handle_shop_command_499,
            "777": self._handle_shop_command_777,
            "888": self._handle_shop_command_888,
        }
        return simple_handlers.get(choice)






    def _handle_shop_command_103(self) -> None:
        if self._is_shop_command_available(103):
            self.show_execution()
        else:
            print("Invalid selection.")






    def _handle_shop_command_104(self) -> None:
        if self._is_shop_command_available(104):
            self.show_interception()
        else:
            print("Invalid selection.")






    def _handle_shop_command_105(self) -> None:
        if self._is_shop_command_available(105):
            if self._prepare_ability_up_from_shop():
                self.show_ability_up()
        else:
            print("Invalid selection.")






    def _handle_shop_command_106(self) -> None:
        if self._is_shop_command_available(106):
            self.show_sell()
        else:
            print("Invalid selection.")






    def _handle_shop_command_108(self) -> None:
        if self._is_shop_command_available(108):
            self.show_dress()
        else:
            print("Invalid selection.")






    def _handle_shop_command_110(self, player: Optional[Character]) -> None:
        if self._is_shop_command_available(110) and player is not None and player.talent.get(325, 0):
            self.show_lab()
        else:
            print("Invalid selection.")






    def _handle_shop_command_111(self) -> None:
        if self._is_shop_command_available(111):
            self.show_facility()
        else:
            print("Invalid selection.")






    def _handle_shop_command_120(self) -> None:
        if self._is_shop_command_available(120) and len(self.interpreter.vars.chars) < self._get_max_charanum():
            self.show_summon()
        else:
            print("奴隶太多了！")






    def _handle_shop_command_496(self) -> None:
        self._select_target_from_roster()






    def _handle_shop_command_497(self) -> None:
        selected_assistant = self._select_assistant_from_roster()
        if selected_assistant is not None and selected_assistant != -2:
            self.interpreter.vars.assi = selected_assistant






    def _handle_shop_command_498(self) -> None:
        if self.interpreter.vars.target > 0:
            self._show_main_menu_character_detail(self.interpreter.vars.target)
        else:
            print("Invalid selection.")






    def _handle_shop_command_499(self) -> None:
        if self.interpreter.vars.assi > 0:
            self._show_main_menu_character_detail(self.interpreter.vars.assi)
        else:
            print("Invalid selection.")






    def _handle_shop_command_777(self) -> None:
        self.show_settings()






    def _handle_shop_command_888(self) -> None:
        self.show_communication()






    def _handle_shop_group_choice(self, groups: List[Dict[str, Union[str, List[int]]]], choice: str) -> Optional[Union[str, tuple[int, Dict[str, Union[str, List[int]]]]]]:
        if choice == "100":
            return None
        group_index = self._parse_choice_int(choice, offset=-1)
        if group_index is None:
            self._show_invalid_selection()
            return "RETRY"
        if group_index < 0 or group_index >= len(groups):
            self._show_invalid_selection()
            return "RETRY"
        group = groups[group_index]
        item_ids = list(group["items"])
        if not item_ids:
            print("\nNothing is available in this category right now.")
            self._pause()
            return "RETRY"
        return group_index, group






    def _handle_shop_group_item_choice(self, page_items: List[int], page: int, page_count: int, choice: str) -> tuple[bool, int]:
        if choice == "100":
            return True, page
        if choice == "997":
            if page + 1 < page_count:
                return False, page + 1
            return False, page
        if choice == "998":
            if page > 0:
                return False, page - 1
            return False, page
        item_index = self._parse_choice_int(choice, offset=-1)
        if item_index is None:
            self._show_invalid_selection()
            return False, page
        if item_index < 0 or item_index >= len(page_items):
            self._show_invalid_selection()
            return False, page
        self._purchase_catalog_item(page_items[item_index])
        self._pause()
        return False, page






    def _handle_shop_group_menu_choice(self, groups: List[Dict[str, Union[str, List[int]]]], choice: str, switch_code: Optional[str]) -> Optional[str]:
        if choice == "100":
            return None
        if switch_code and choice == switch_code:
            return "SWITCH"
        choice_result = self._handle_shop_group_choice(groups, choice)
        if choice_result is None:
            return None
        if choice_result == "RETRY":
            return "RETRY"
        _, group = choice_result
        self._run_shop_group_item_loop(group)
        return "CONTINUE"






    def _handle_shop_main_menu_action_choice(self, choice: str, player: Optional[Character]) -> tuple[bool, Optional[str]]:
        if choice == "199":
            self._apply_rest_turn_end()
            return True, None
        if choice == "200":
            self.do_save()
            return True, None
        if choice == "110":
            self._handle_shop_command_110(player)
            return True, None
        return False, None






    def _handle_shop_main_menu_choice(self, choice: str):
        player = self._get_player()
        handled, result = self._handle_shop_main_menu_direct_choice(choice, player)
        if handled:
            return result
        if self._handle_shop_main_menu_routed_choice(choice):
            return None
        if choice == "999":
            print("Thanks for playing!")
            return "EXIT"
        print("Invalid selection.")
        return None






    def _handle_shop_main_menu_direct_choice(self, choice: str, player: Optional[Character]) -> tuple[bool, Optional[str]]:
        state_change = self._handle_shop_main_menu_state_change_choice(choice)
        if state_change is not None:
            return state_change
        return self._handle_shop_main_menu_action_choice(choice, player)






    def _handle_shop_main_menu_load_choice(self, choice: str) -> Optional[tuple[bool, Optional[str]]]:
        if choice != "300":
            return None
        return True, "LOAD"






    def _handle_shop_main_menu_routed_choice(self, choice: str) -> bool:
        handler = self._get_shop_main_menu_handler(choice)
        if handler is not None:
            handler()
            return True
        return self._handle_shop_panel_command(choice)






    def _handle_shop_main_menu_state_change_choice(self, choice: str) -> Optional[tuple[bool, Optional[str]]]:
        training_result = self._handle_shop_main_menu_training_choice(choice)
        if training_result is not None:
            return training_result
        invasion_result = self._handle_shop_main_menu_invasion_choice(choice)
        if invasion_result is not None:
            return invasion_result
        load_result = self._handle_shop_main_menu_load_choice(choice)
        if load_result is not None:
            return load_result
        return None






    def _handle_shop_main_menu_training_choice(self, choice: str) -> Optional[tuple[bool, Optional[str]]]:
        if choice != "100":
            return None
        prepared, should_enter = self._prepare_training_from_shop()
        if prepared and should_enter:
            return True, "TRAIN"
        return True, None






    def _handle_shop_panel_command(self, choice: str) -> bool:
        if self._handle_shop_panel_mode_choice(choice):
            return True
        if self._handle_shop_panel_floor_status_choice(choice):
            return True
        return self._handle_shop_panel_command_fallback(choice)






    def _handle_shop_panel_command_fallback(self, choice: str) -> bool:
        return False






    def _handle_shop_panel_floor_status_choice(self, choice: str) -> bool:
        floor = self._parse_choice_int(choice)
        if floor is None:
            return False
        if 521 <= floor <= 530:
            self._show_specific_floor_status(floor - 520)
            return True
        return False






    def _handle_shop_panel_mode_choice(self, choice: str) -> bool:
        mode_map = {
            "500": 0,
            "501": 1,
            "504": 4,
            "505": 5,
        }
        panel_mode = mode_map.get(choice)
        if panel_mode is None:
            return False
        self._set_main_menu_panel_mode(panel_mode)
        return True






    def _has_shop_knowledge(self, talent_id: int) -> bool:
        player = self._get_player()
        if player is not None and player.talent.get(talent_id, 0):
            return True
        assistant = self._get_shop_assistant()
        if assistant is not None and assistant.talent.get(talent_id, 0):
            return True
        return False






    def _is_shop_command_available(self, command_id: int) -> bool:
        return bool(self._get_shop_command_state().get(command_id, False))






    def _normalize_shop_selection_state(self):
        if self.interpreter.vars.target >= len(self.interpreter.vars.chars):
            self.interpreter.vars.target = -1
        if self.interpreter.vars.assi >= len(self.interpreter.vars.chars):
            self.interpreter.vars.assi = -1
        if self.interpreter.vars.assi == self.interpreter.vars.target:
            self.interpreter.vars.assi = -1

        target = self._get_target()
        if self.interpreter.vars.target >= 1 and target is not None:
            if target.cflag.get(1, 0) != 0:
                self.interpreter.vars.target = -1
                target = None

        if self.interpreter.vars.assi >= 1:
            assistant = self.interpreter.vars.chars[self.interpreter.vars.assi] if self.interpreter.vars.assi < len(self.interpreter.vars.chars) else None
            if assistant is None or assistant.cflag.get(1, 0) != 0:
                self.interpreter.vars.assi = -1






    def _prepare_shop_group_page(self, item_ids: List[int], page: int) -> tuple[int, List[int], int]:
        page_start = page * 20
        page_items = item_ids[page_start:page_start + 20]
        if not page_items:
            page = 0
            page_items = item_ids[:20]
        page_count = max(1, (len(item_ids) + 19) // 20)
        return page, page_items, page_count






    def _refund_shop_cost(self, cost: int):
        self._ensure_shop_cost_accounting()
        self._add_global_money(cost)






    def _render_shop_group_menu(self, title: str, groups: List[Dict[str, Union[str, List[int]]]], switch_label: Optional[str] = None, switch_code: Optional[str] = None) -> None:
        print("\n【%s】" % title)
        print("-" * 30)
        print(f" Money: {self.interpreter.vars.money} pts")
        for index, group in enumerate(groups, start=1):
            print(f" [{index}] {group['title']}")
        if switch_label and switch_code:
            print(f" [{switch_code}] {switch_label}")
        print(" [100] Back")
        print("-" * 30)






    def _render_shop_group_page(self, group: Dict[str, Union[str, List[int]]], page: int, page_count: int, page_items: List[int]) -> None:
        print(f"\n【{group['title']}】")
        print("-" * 30)
        if page_count > 1:
            print(f" 第{page + 1}/{page_count}页")
        for index, item_id in enumerate(page_items, start=1):
            item_def = self._get_item_definition(item_id)
            if item_def is None:
                continue
            print(f" [{index}] {item_def['name']} - {item_def['price']} pts")
        if page_count > 1:
            print(" [997] 下一页")
            print(" [998] 上一页")
        print(" [100] Back")
        print("-" * 30)






    def _render_shop_main_menu(self):
        self._render_main_menu_header()
        self._render_main_menu_target_panel()
        self._render_main_menu_sections()






    def _run_shop_group_item_loop(self, group: Dict[str, Union[str, List[int]]]) -> None:
        item_ids = list(group["items"])
        page = 0
        while True:
            exit_group, page = self._advance_shop_group_page(group, item_ids, page)
            if exit_group:
                return




    def _run_shop_loop(self):
        day = self.interpreter.vars.day
        day_repr = f"{day[0]}:{day[1]}:{day[2]}" if isinstance(day, (list, tuple)) and len(day) >= 3 else str(day)
        print(f"【DEBUG】进入商店 - Day:{day_repr}, Time:{self.interpreter.vars.time}, MONEY:{self.interpreter.vars.money}")
        while True:
            result = self._advance_shop_main_menu()
            if result in {"TRAIN", "LOAD", "EXIT"}:
                return result




    def run_shop(self):
        """Run main menu (shop)"""
        return self._run_shop_loop()






    def show_shop(self):
        """Show shop menu with source-like normal/trap switching."""
        while True:
            switched = self._advance_shop_menu()
            if switched is None:
                return
            if switched != "998":
                continue

            trap_switched = self._advance_trap_shop_menu()
            if trap_switched is None:
                return

    def _show_shop_chara(self):
        return self.call_erb_function('SHOW_SHOP_CHARA')

    def _show_shop_monster(self):
        return self.call_erb_function('SHOW_SHOP_MONSTER')

    def _shop_trap(self):
        return self.call_erb_function('SHOP_TRAP')

    def _usershop(self):
        """商店输入处理 - 桥接ERB USERSHOP"""
        return self.call_erb_function('USERSHOP')





