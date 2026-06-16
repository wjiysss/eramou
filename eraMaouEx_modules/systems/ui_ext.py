from __future__ import annotations
"""Module for UIExtMixin - UI交互"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class UIExtMixin:
    """Mixin providing UI交互 methods for GameEngine"""

    def _advance_age_measurement_menu(self) -> Optional[tuple[bool, str]]:
        age_enabled = self._get_flag_bit(5, 12)
        race_age_enabled = self._get_flag_bit(5, 13)
        human_age_enabled = self._get_flag_bit(5, 14)
        measurements_enabled = self._get_flag_bit(5, 15)

        print("\n【年龄 / 三围显示】")
        print("-" * 30)
        print(f" [0] 年龄的显示 : {'ON' if age_enabled else 'OFF'}")
        print(f" [{'1' if age_enabled else '-'}] 使用不同种族的年龄设定 : {'ON' if race_age_enabled else 'OFF'}")
        print(f" [{'2' if race_age_enabled else '-'}] 显示换算成人类的年龄 : {'ON' if human_age_enabled else 'OFF'}")
        print(f" [3] 显示三围数据 : {'ON' if measurements_enabled else 'OFF'}")
        print(" [9] 详细设定")
        print(" [100] 返回")
        return self._handle_age_measurement_choice()

    def _advance_assistant_selection(self, candidates: List[tuple[int, Character]]) -> Optional[int]:
        self._render_assistant_selection_screen(candidates)
        choice = self._prompt_assistant_selection_choice()
        if choice == "100":
            return -2
        if choice == "0":
            return -1
        return self._handle_assistant_selection_choice(candidates, choice)

    def _advance_calendar_day(self) -> None:
        self.interpreter.vars.time = 0
        self.interpreter.vars.day[0] += 1
        self.interpreter.vars.day[2] += 1
        self.interpreter.vars.day[3] = (int(self.interpreter.vars.day[3]) + 1) % 7

        if self._is_calendar_month_overflow():
            for message in self._advance_calendar_month():
                print(message)

    def _advance_calendar_month(self) -> List[str]:
        messages: List[str] = []
        self.interpreter.vars.day[2] = 1
        self.interpreter.vars.day[1] += 1
        if self.interpreter.vars.day[1] > 12:
            self.interpreter.vars.day[1] = 1
            self.interpreter.vars.day[0] += 1
            messages.append("明天就是新一年的开始了，再努力地把邪恶传播到各处吧！")
            self._advance_character_age_year()
            return messages
        messages.append(f"明天就是{self.interpreter.vars.day[1]}月了，是个适合调教的月份呢……")
        return messages

    def _advance_communication_menu(self) -> bool:
        self._render_communication_menu()
        choice = self._prompt_communication_choice()
        if choice == "9":
            return True
        if self._handle_maounet_direct_choice(choice):
            return False

        print("\nInvalid selection.")
        self._pause()
        return False

    def _advance_departed_story_aftermath_flags(self) -> None:
        square_stage = int(self.interpreter.vars.globals.get(2811, 0))
        if square_stage == 300 and random.randint(0, 4) == 0:
            self.interpreter.vars.globals[2811] = 310

    def _advance_floor_status_menu(self) -> bool:
        return self._show_floor_status_page()

    def _advance_game_state(self, state: str) -> str:
        handler = self._get_game_state_handler(state)
        if handler is not None:
            return handler()
        return self._handle_unknown_game_state(state)

    def _advance_game_state_safely(self, state: str) -> str:
        try:
            return self._advance_game_state_with_fallback(state)
        except KeyboardInterrupt:
            return self._handle_game_state_keyboard_interrupt()
        except Exception as e:
            return self._handle_game_state_exception(e)

    def _advance_game_state_with_fallback(self, state: str) -> str:
        return self._advance_game_state(state)

    def _advance_life_cradle_first_experience(self, target: Character) -> Optional[tuple[bool, str]]:
        self._render_life_cradle_first_experience_menu()
        choice = self._prompt_choice_int()
        try:
            selection = int(choice)
        except TypeError:
            return False, "已取消。"

        if selection == 996:
            return self._apply_life_cradle_first_experience_random(target)
        if selection == 998:
            self._apply_life_cradle_first_experience(target, 998)
            return True, self._summarize_life_cradle_first_experience(target)
        if selection in {1, 101, 102, 103, 104, 105}:
            self._apply_life_cradle_first_experience(target, selection)
            return True, self._summarize_life_cradle_first_experience(target)
        if selection == 997:
            partner_name = self._prompt_life_cradle_custom_partner_name("初体验对象")
            if partner_name is None:
                return None
            if not partner_name:
                return self._apply_life_cradle_first_experience_random(target)
            self._apply_life_cradle_first_experience(target, 997, partner_name)
            return True, self._summarize_life_cradle_first_experience(target)
        print("输入错误，请重新开始。")
        return None

    def _advance_life_cradle_first_kiss(self, target: Character) -> Optional[tuple[bool, str]]:
        player = self._get_player()
        if player is None:
            return False, "没有可用的魔王角色。"
        selection = self._prompt_life_cradle_first_kiss_selection()
        if selection is None:
            return False, "已取消。"
        return self._resolve_life_cradle_first_kiss_selection(target, player, selection)

    def _advance_main_menu_character_detail(self, idx: int, char: Character) -> bool:
        self._render_main_menu_character_detail(idx, char)
        detail_choice = self._prompt_choice()
        if detail_choice == "100":
            return True
        try:
            action_id = int(detail_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        ok, message = self._apply_character_detail_action(idx, char, action_id)
        print(f"\n{message}")
        self._pause()
        return False

    def _advance_meat_toilet_menu(self) -> bool:
        self._render_meat_toilet_menu()
        if self.interpreter.vars.get_flag(83, 0) <= 0:
            self._pause()
            return True
        choice = self._prompt_meat_toilet_choice()
        return self._handle_meat_toilet_menu_choice(choice)

    def _advance_mod_switch_menu(self) -> Optional[tuple[bool, str]]:
        self._render_mod_switch_menu()
        choice = self._prompt_choice()
        if choice == "100":
            return True, "已返回设置菜单。"
        return self._handle_mod_switch_menu_choice(choice)

    def _advance_story_flag_if_matches(self, flag_id: int, stage: int) -> None:
        current_stage = int(self.interpreter.vars.globals.get(flag_id, 0))
        if current_stage == stage:
            self.interpreter.vars.globals[flag_id] = stage + 1

    def _advance_story_wait_counter(self, char: Character, target_value: int, next_stage: int) -> bool:
        current = int(char.cflag.get(515, 0))
        if current >= target_value:
            char.cflag[515] = current
            return True
        char.cflag[515] = current + 1
        return False

    def _advance_time_to_next_day_if_needed(self) -> bool:
        return self.interpreter.vars.time >= 2

    def _advance_trap_shop_menu(self) -> Optional[str]:
        return self._show_shop_group_menu(
            "陷阱黑市",
            self._build_trap_shop_groups(),
            switch_label="普通物品",
            switch_code="997",
        )

    def _handle_age_measurement_choice(self) -> Optional[tuple[bool, str]]:
        choice = self._prompt_choice()

        if choice == "100":
            if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
                self._ensure_race_age_defaults()
                self._ensure_all_character_body_profiles()
            return True, "已返回设置菜单。"
        if choice == "0":
            enabled = self._toggle_flag_bit(5, 12)
            if enabled:
                self._ensure_race_age_defaults()
                self._ensure_all_character_body_profiles()
            return None
        if choice == "1":
            self._toggle_flag_bit(5, 13)
            return None
        if choice == "2":
            self._toggle_flag_bit(5, 14)
            return None
        if choice == "3":
            enabled = self._toggle_flag_bit(5, 15)
            if enabled:
                self._ensure_race_age_defaults()
                self._ensure_all_character_body_profiles()
            return None
        if choice == "9":
            self._ensure_race_age_defaults()
            self._ensure_all_character_body_profiles()
            return self._show_race_age_config_menu()
        print("\nInvalid selection.")
        return None

    def _handle_assistant_selection_choice(
        self,
        candidates: List[tuple[int, Character]],
        choice: str,
    ) -> Optional[int]:
        try:
            selected = int(choice)
        except ValueError:
            print("Invalid selection.")
            return -2

        selected_pair = next(((idx, char) for idx, char in candidates if idx == selected), None)
        if selected_pair is None:
            print("Invalid selection.")
            return -2
        return selected_pair[0]

    def _handle_conquest_fixed_gift_candidate(
        self,
        fixed_candidate: Character,
        label: str,
        random_title: str,
        retry_text: str,
    ) -> Optional[tuple[bool, str]]:
        print(f"\n{label}被作为贡品献了上来……")
        self._show_conquest_candidate_summary(fixed_candidate)
        choice = self._prompt_conquest_fixed_gift_choice(label)
        if choice == "0":
            return self._append_conquest_candidate(fixed_candidate)
        if choice != "1":
            return None
        return self._run_conquest_random_candidate_picker(random_title, retry_text)

    def _handle_conquest_random_candidate_choice(
        self,
        sub_choice: str,
        candidate: Character,
        personality_id: Optional[int],
        hair_color: Optional[int],
    ) -> tuple[bool, Optional[tuple[bool, str]]]:
        if sub_choice == "0":
            return True, self._append_conquest_candidate(candidate)
        if sub_choice == "1":
            return True, None
        if sub_choice == "2":
            return True, (False, "")
        if sub_choice == "3":
            _ = self._prompt_conquest_random_personality(personality_id)
            return True, None
        if sub_choice == "4":
            _ = self._prompt_conquest_random_hair_color(hair_color)
            return True, None
        return False, None

    def _handle_floor_status_choice(self) -> bool:
        choice = self._prompt_choice()
        if choice == "100":
            return True
        try:
            selected = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        if 1 <= selected <= 9:
            print()
            for line in self._get_floor_status_lines(selected):
                print(line)
            self._pause()
            return False
        if selected == 10:
            print()
            for line in self._get_guard_status_lines():
                print(line)
            self._pause()
            return False
        print("\nInvalid selection.")
        self._pause()
        return False

    def _handle_game_state_exception(self, error: Exception) -> str:
        print(f"\nError occurred: {error}")
        print("Returning to title...")
        return "TITLE"

    def _handle_game_state_keyboard_interrupt(self) -> str:
        print("\n\nGame paused. Returning to title...")
        return "TITLE"

    def _handle_life_cradle_talent_choice(self, target: Character, page_index: int) -> Optional[int]:
        choice = self._prompt_choice()
        if choice == "998":
            return -1
        if choice == "997":
            return -2
        if choice == "996":
            return -3
        if choice == "999":
            return -4
        try:
            talent_id = int(choice)
        except ValueError:
            print("\n无效值")
            self._pause()
            return None
        if talent_id not in self._iter_life_cradle_page_ids(page_index):
            print("\n无效值")
            self._pause()
            return None
        return talent_id

    def _handle_meat_toilet_menu_choice(self, choice: str) -> bool:
        if choice == "999":
            return True
        if choice == "0":
            self._handle_meat_toilet_seed_selection()
            return False
        if choice == "1":
            self._toggle_flag_bit(614, 0)
            print(f"\n人类牧场记录现在为：{'不显示' if self._get_flag_bit(614, 0) else '显示'}。")
            self._pause()
            return False
        if choice == "2":
            self._toggle_flag_bit(614, 1)
            print(f"\n卖掉产出的孩子现在为：{'出售' if self._get_flag_bit(614, 1) else '不出售'}。")
            self._pause()
            return False
        print("\nInvalid selection.")
        self._pause()
        return False

    def _handle_meat_toilet_seed_selection(self):
        self._render_meat_toilet_seed_menu()
        seed_choice = self._prompt_meat_toilet_seed_choice()
        try:
            seed_type = int(seed_choice)
        except ValueError:
            seed_type = 0
        if seed_type not in (0, 1, 2, 3):
            seed_type = 0
        self.interpreter.vars.set_flag(613, seed_type)
        print(f"\n播种者设为{self._get_meat_toilet_seed_name(seed_type)}了。")
        self._pause()

    def _handle_mod_switch_menu_choice(self, choice: str) -> Optional[tuple[bool, str]]:
        try:
            mod_id = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            return None
        ok, message = self._apply_mod_switch_entry(mod_id)
        print(f"\n{message}")
        return None

    def _handle_otherworld_hero_template_missing_template(self, finalize: bool) -> None:
        if not finalize:
            return
        player = self._get_player()
        if player is not None:
            player.exp[81] = int(player.exp.get(81, 0)) + 1

    def _handle_purchase_catalog_item_knowledge(self, item_id: int, price: int, item_name: str) -> bool:
        blocked_reason = self._can_purchase_catalog_item(item_id, self._get_player())
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            return False
        if not self._confirm_catalog_item_purchase(item_name):
            return False
        self._charge_shop_cost(price)
        applied = self._apply_knowledge_item(item_id)
        if not applied:
            self._refund_shop_cost(price)
            print("\nThe item could not be applied.")
            return False
        print(f"\nPurchased and applied {item_name}.")
        return True

    def _handle_purchase_catalog_item_plural(self, item_id: int, quantity: int, item_name: str, total_cost: int) -> bool:
        special_result = self._apply_plural_purchase_effect(item_id, quantity, item_name)
        if special_result is not None:
            if special_result:
                return True
            self._refund_shop_cost(total_cost)
            return False
        player = self._get_player()
        if player is None:
            self._refund_shop_cost(total_cost)
            return False
        self._add_item(player, item_name, quantity)
        if quantity == 1:
            print(f"\nPurchased {item_name}.")
        else:
            print(f"\nPurchased {quantity} x {item_name}.")
        return True

    def _handle_purchase_catalog_item_plural_purchase(self, item_id: int, player: Character, price: int, item_name: str) -> bool:
        max_buyable = self._get_max_buyable_quantity(item_id, player, price)
        if max_buyable <= 0:
            print("\nYou cannot carry or afford any more of this item.")
            return False

        quantity = self._get_item_purchase_quantity(item_id, item_name, max_buyable)
        if quantity is None:
            return False
        if item_id not in self._get_buy_plural_ids() and not self._confirm_catalog_item_purchase(item_name):
            return False

        total_cost = price * quantity
        self._charge_shop_cost(total_cost)
        return self._handle_purchase_catalog_item_plural(item_id, quantity, item_name, total_cost)

    def _handle_purchase_catalog_item_use_now(self, item_id: int, price: int, item_name: str) -> bool:
        target = self._select_item_target()
        if target is None:
            return False
        blocked_reason = self._can_use_item_on_target(item_id, target)
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            return False
        self._charge_shop_cost(price)
        applied = self._apply_use_now_item(item_id, target)
        if not applied:
            self._refund_shop_cost(price)
            print("\nThe item could not be used.")
            return False
        print(f"\nPurchased and used {item_name}.")
        return True

    def _handle_target_roster_choice(self, captives: List[tuple[int, Character]]) -> bool:
        choice = self._prompt_choice_raw()
        if choice == "100":
            return False
        try:
            selected = int(choice)
        except ValueError:
            print("Invalid selection.")
            return False

        selected_pair = next(((idx, char) for idx, char in captives if idx == selected), None)
        if selected_pair is not None:
            idx, char = selected_pair
            blocked_reason = self._can_open_trainable_target(idx, char)
            if blocked_reason is not None:
                print(blocked_reason)
                return False
            self.interpreter.vars.target = selected
            print(f"Current target changed to {self.interpreter.vars.chars[selected].name}.")
            return True

        print("Invalid selection.")
        return False

    def _handle_title_choice(self, choice: str) -> str:
        if choice == "1":
            return self._start_new_game_from_title()
        if choice == "0":
            return self.run_load_game()
        return "TITLE"

    def _handle_unknown_game_state(self, state: str) -> str:
        print(f"Unknown state: {state}")
        return "EXIT"

    def _prompt_aphrodisiac_withdrawal_item_use(self, target: Character) -> bool:
        player = self._get_player()
        if player is None or player.item.get("媚药", 0) <= 0:
            return False
        print(f"给予{target.name}媚药吗？")
        print(" [0] - 好的")
        print(" [1] - 不要")
        choice = self._prompt_choice()
        if choice == "0":
            self._use_item(player, "媚药", 1)
            if int(target.cflag.get(1, 0)) == 2:
                self._apply_aphrodisiac_target_fall(target)
            else:
                target.cflag[32] = 0
            messages.extend(
                [
                    f"{target.name} 抢过了装着浓缩媚药的瓶子，",
                    f"马上如饥似渴地一饮而尽，放心地叹了一口气。",
                ]
            )
            target.cflag[31] = int(target.cflag.get(31, 0)) + 1
            return True
        return False

    def _prompt_assistant_selection_choice(self) -> str:
        return self._prompt_choice()

    def _prompt_choice(self, prompt: str = "Select >> ") -> str:
        return self._read_input_stripped(prompt)

    def _prompt_choice_int(self, prompt: str = "Select >> ", offset: int = 0) -> Optional[int]:
        return self._parse_choice_int(self._prompt_choice(prompt), offset=offset)

    def _prompt_choice_int_in_options(self, options: List[int], prompt: str = "Select >> ", offset: int = 0) -> Optional[int]:
        value = self._prompt_choice_int(prompt, offset=offset)
        if value is None or value not in options:
            return None
        return value

    def _prompt_choice_raw(self, prompt: str = "Select >> ") -> str:
        return self._read_input(prompt)

    def _prompt_communication_choice(self):
        return self._prompt_choice()

    def _prompt_conquest_fixed_gift_choice(self, label: str) -> str:
        print(f"要收下{label}吗？")
        print(" [0] 收下她吧")
        print(" [1] 另外挑选")
        return self._prompt_choice()

    def _prompt_conquest_random_candidate_choice(self, candidate: Character, random_title: str, retry_text: str) -> str:
        print(f"\n{random_title}")
        self._show_conquest_candidate_summary(candidate)
        print(" [0] 就是她了")
        print(" [1] 再换一个")
        print(f" [2] {retry_text}")
        print(" [3] 调整性格")
        print(" [4] 调整发色")
        return self._prompt_choice()

    def _prompt_conquest_random_hair_color(self, current_hair_color: Optional[int]) -> Optional[int]:
        print("请选择发色。")
        colors = self._get_conquest_random_hair_colors()
        for color_id in colors:
            print(f" [{color_id}] {self._format_life_cradle_field_value(300, color_id)}")
        hair_choice = self._prompt_choice()
        try:
            selected_hair = int(hair_choice)
        except ValueError:
            return current_hair_color
        if selected_hair in colors:
            return selected_hair
        return current_hair_color

    def _prompt_conquest_random_personality(self, current_personality: Optional[int]) -> Optional[int]:
        print("请选择偏好的性格。")
        options = self._get_conquest_random_personality_ids()
        for idx, talent_id in enumerate(options):
            print(f" [{idx}] {self._get_talent_name(talent_id)}")
        personality_choice = self._prompt_choice()
        try:
            personality_index = int(personality_choice)
        except ValueError:
            return current_personality
        if 0 <= personality_index < len(options):
            return options[personality_index]
        return current_personality

    def _prompt_human_conquest_followup(self):
        print("人间界已经陷落了，不过世上还有很多其它地方，要继续游戏吗？")
        print(" [0] 世界这么大，我想再去看看！")
        print(" [1] 我已经……不想做魔王了……")
        while True:
            choice = self._prompt_choice()
            if choice == "0":
                print("世界还很大，魔王的征服仍将继续。")
                self._pause()
                return
            if choice == "1":
                self.running = False
                return

    def _prompt_life_cradle_custom_partner_name(self, label: str) -> Optional[str]:
        partner_name = self._prompt_choice(f"输入{label}（留空将会随机生成）>> ")
        if len(partner_name) > 16:
            print("太长，请使用全角八字以下。")
            return None
        return partner_name

    def _prompt_life_cradle_first_kiss_selection(self) -> Optional[int]:
        self._render_life_cradle_first_kiss_menu()
        return self._prompt_choice_int()

    def _prompt_life_cradle_first_kiss_site(self, options: list[int], labels: Dict[int, str]) -> Optional[int]:
        print(" 初吻位置: " + " ".join(f"[{value}] {labels[value]}" for value in options))
        site_code = self._prompt_choice_int()
        if site_code is None or site_code not in options:
            print("输入错误，请重新开始。")
            return None
        return site_code

    def _prompt_meat_toilet_choice(self):
        return self._prompt_choice()

    def _prompt_meat_toilet_seed_choice(self):
        return self._prompt_choice()

    def _prompt_normal_end_followup(self):
        print(" [1] 结束游戏")
        print(" [2] 继续游戏")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                self.running = False
                return
            if choice == "2":
                print("魔王的传说，还将继续……")
                self._pause()
                return

    def _prompt_story_branch_selection(self, event_key: str, global_flag: int, main_flag_delta: int = 2):
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                print("此处剧情尚未完全做好，先保留为已进入该故事线。")
                self.interpreter.vars.globals[global_flag] = int(self.interpreter.vars.globals.get(global_flag, 0)) + 100
                self.interpreter.vars.globals[2801] = int(self.interpreter.vars.globals.get(2801, 0)) + main_flag_delta
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("你跳过了本故事线。")
                self.interpreter.vars.globals[global_flag] = int(self.interpreter.vars.globals.get(global_flag, 0)) + 100
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("那就明天再问吧。")
                self._pause()
                return

    def _prompt_title_choice(self) -> str:
        return self._prompt_choice_raw()

    def _render_assistant_selection_screen(self, candidates: List[tuple[int, Character]]) -> None:
        print("\nSelect Assistant")
        print("-" * 30)
        for idx, char in candidates:
            print(f" [{idx}] {char.name}  HP {char.base.get(0, 0)}/{char.maxbase.get(0, 0)}")
        print(" [0] 不带助手")
        print(" [100] 返回")

    def _render_communication_menu(self):
        print("\n【MAOUNET】")
        print("-" * 30)
        print(" [0] 将奴隶共享到其他存档")
        print(" [1] 从其他存档共享勇者")
        print(" [2] 去除从其他存档共享的勇者")
        print(f" [3] 设定通信勇者的等级上限(现在:Lv{self.interpreter.vars.get_flag(76, 0)})")
        print(f" [4] 通信勇者登场时为等级1(现在:{'ON' if self.interpreter.vars.get_flag(77, 0) else 'OFF'})")
        if self._is_makai_bank_enabled():
            print(f" [5] 连接到魔界银行(目前存款{self._get_makai_bank_deposit()})")
        print(f" 当前通信池: {self._summarize_maounet_pool()}")
        print(" [9] 返回")

    def _render_floor_status_page(self) -> None:
        print("\n【楼层状态】")
        print("-" * 30)
        for floor in range(1, 10):
            room_name = self._get_dungeon_room_name(self._get_dungeon_floor_room(floor))
            print(f" [{floor}] 第{floor}阶层 ({room_name})")
        print(" [10] 近卫兵 / 迎击状态")
        print(" [100] 返回")

    def _render_life_cradle_first_experience_menu(self):
        print("\n设定初体验")
        print(" [1] 魔王")
        print(" [101] 蠕虫")
        print(" [102] 触手生物")
        print(" [103] 野狗")
        print(" [104] 怪物")
        print(" [105] 狂王")
        print(" [996] 随机")
        print(" [997] 自定义输入")
        print(" [998] 无")

    def _render_life_cradle_first_kiss_menu(self):
        print("\n设定初吻")
        print(" [0] 不明")
        print(" [1] 魔王")
        print(" [993] 狂王")
        print(" [994] 怪物")
        print(" [995] 野狗")
        print(" [999] 触手")
        print(" [996] 随机")
        print(" [997] 自定义输入")
        print(" [998] 无")

    def _render_meat_toilet_menu(self):
        print("\n【肉便器 / 人类牧场】")
        print("-" * 30)
        for line in self._build_meat_toilet_overview_lines():
            print(line)
        print(" [0] 设定播种者")
        print(f" [1] 人类牧场记录: {'不显示' if self._get_flag_bit(614, 0) else '显示'}")
        print(f" [2] 卖掉产出的孩子: {'出售' if self._get_flag_bit(614, 1) else '不出售'}")
        print(" [999] 返回")

    def _render_meat_toilet_seed_menu(self):
        print("\n请选择播种者")
        print(" [0] 怪物")
        print(" [1] 俘虏的中年")
        print(" [2] 俘虏的少年")
        print(" [3] 扶她淫魔")

    def _render_mod_switch_menu(self) -> None:
        print("\n【MOD开关】")
        print("-" * 30)
        for entry in self._get_mod_switch_entries():
            enabled = self._get_flag_bit(9000, int(entry["id"]))
            print(f" [{entry['id']}] {entry['label']} : {'ON' if enabled else 'OFF'}")
        print(" [100] Back")

    def _render_resistance_mark_reduction_option(self, target: Character) -> None:
        resistance_level = int(target.mark.get(3, 0))
        cost = self._get_resistance_mark_reduction_cost(target)
        marker = "*" if self._can_reduce_resistance_mark(target) else "-"
        print(f" [99] {marker} 反抗刻印 LV{resistance_level} -> LV{max(0, resistance_level - 1)}")
        print(f"      Cost: 屈服珠:{cost}")
        reasons = self._get_resistance_mark_reduction_reasons(target)
        if reasons:
            print(f"      Block: {'；'.join(reasons)}")

    def _render_select_item_target_menu(self, candidates: List[tuple[int, Character]]) -> None:
        print("\nSelect Item Target")
        print("-" * 30)
        for idx, char in candidates:
            label = "Master" if idx == 0 else "Target"
            print(f" [{idx}] {char.name} ({label}) HP {char.base.get(0, 0)}/{char.maxbase.get(0, 0)}")
        print(" [100] Back")

    def _render_target_roster(self, captives: List[tuple[int, Character]]) -> None:
        print("\nSelect Target")
        print("-" * 30)
        for idx, char in captives:
            submission = self._get_submission_level(char)
            blocked_reason = self._can_open_trainable_target(idx, char)
            status = f"  - {blocked_reason}" if blocked_reason is not None else ""
            print(f" [{idx}] {char.name}  HP {char.base.get(0, 0)}/{char.maxbase.get(0, 0)}  SUB {submission}{status}")
        print(" [100] Back")

    def _show_age_measurement_menu(self) -> tuple[bool, str]:
        while True:
            result = self._advance_age_measurement_menu()
            if result is not None:
                return result

    def _show_all_exhibits(self) -> List[str]:
        """全部展品一览"""
        v = self.interpreter.vars
        messages = ["═══ 博物馆全展品一览 ═══"]

        total = 0
        for ftype, (name, flag_key, _) in sorted(self._INFRASTRUCTURE_TYPES.items()):
            flag_num = int(flag_key.split(':')[1])
            count = v.flag.get(flag_num, 0)
            if count > 0:
                messages.append(f"  {name}: {count}个")
                total += count

        # 调度品合计
        messages.append(f"─────────────")
        messages.append(f"  展品合计: {total}个")
        messages.append(f"  调度品合计: {v.flag.get(84, 0)}个")

        if total == 0:
            messages = ["博物馆内还没有任何展品。"]

        return messages

    def _show_benki(self) -> List[str]:
        """肉便器展示"""
        v = self.interpreter.vars
        count = v.flag.get(83, 0)
        if count == 0:
            return ["还没有肉便器。"]

        messages = [f"现在有 {count} 个肉便器。"]
        # 列出肉便器角色
        for idx, char in enumerate(v.chars):
            if idx == 0:
                continue
            if char.talent.get(203, 0):  # 肉便器素质
                messages.append(f"  {char.savestr}")
        return messages

    def _show_conquest_candidate_summary(self, target: Character):
        print("-" * 40)
        print(f" 名字: {target.name}")
        print(f" 模板ID: {int(getattr(target, 'template_id', 0) or 0)}")
        print(f" 性格: {', '.join(self._get_talent_name(tid) for tid in self._get_conquest_random_personality_ids() if target.talent.get(tid, 0)) or '未设定'}")
        print(f" 发色: {self._format_life_cradle_field_value(300, int(target.talent.get(300, 0)))}")
        print(f" HP {target.maxbase.get(0, 0)} / MP {target.maxbase.get(1, 0)}")
        print("-" * 40)

    def _show_ending(self, ending_id: str) -> List[str]:
        """Show the ending text.
        Corresponds to ERB @ENDING_1 through @ENDING_N.
        """
        lines: List[str] = []
        lines.append("───────────────────────────────────────")

        ending_text = self._ENDING_TEXTS.get(ending_id, [])
        if ending_text:
            lines.extend(ending_text)
        else:
            defn = self._ENDING_DEFINITIONS.get(ending_id, {})
            lines.append(f"达成了结局：{defn.get('name', ending_id)}")
            lines.append(defn.get('description', ''))

        lines.append("───────────────────────────────────────")

        # Handle special ending effects
        if ending_id == "1":
            # Good End - add princess character
            lines.append("")
            lines.append("*人类皇族公主菲娅，被你抓获了*")
            self.interpreter.vars.flags[82] = 1
        elif ending_id == "2":
            # Castle fall - game over
            target_name = ""
            target_idx = self.interpreter.vars.target
            if 0 <= target_idx < len(self.interpreter.vars.chars):
                target_name = self.interpreter.vars.chars[target_idx].name or "勇者"
            lines.insert(1, f"*勇者{target_name}封印了魔王，被歌颂为传说中的勇者*")
        elif ending_id == "3":
            # Elf conquest
            self.interpreter.vars.flags[87] = 1
        elif ending_id == "4":
            # Dragon conquest
            self.interpreter.vars.flags[89] = 1
        elif ending_id == "5":
            # Heaven conquest
            self.interpreter.vars.flags[91] = 1

        return lines

    def _show_equip(self, target: Character) -> List[str]:
        """Show character equipment.
        Corresponds to ERB @EQUIP_ST_SHOW.
        """
        lines: List[str] = []
        lines.append(f"【{target.name} 的装备】")
        lines.append("───────────────────────────────────────")

        # Weapon slot (CFLAG:550)
        weapon_code = int(target.cflag.get(550, -1))
        if weapon_code >= 0:
            weapon_name = self._get_equipment_weapon_name(weapon_code)
            lines.append(f"  武器：{weapon_name}")
            weapon_stats = self._get_single_equip_stats(weapon_code, is_weapon=True, target=target)
            for stat_line in weapon_stats:
                lines.append(f"    {stat_line}")
        else:
            lines.append("  武器：无")

        # Ring slot A (CFLAG:551)
        ring_a_code = int(target.cflag.get(551, -1))
        if ring_a_code >= 0:
            ring_a_name = self._get_equipment_ring_name(ring_a_code)
            lines.append(f"  装饰A：{ring_a_name}")
            ring_a_stats = self._get_single_equip_stats(ring_a_code, is_weapon=False, target=target)
            for stat_line in ring_a_stats:
                lines.append(f"    {stat_line}")
        else:
            lines.append("  装饰A：无")

        # Ring slot B (CFLAG:552)
        ring_b_code = int(target.cflag.get(552, -1))
        if ring_b_code >= 0:
            ring_b_name = self._get_equipment_ring_name(ring_b_code)
            lines.append(f"  装饰B：{ring_b_name}")
            ring_b_stats = self._get_single_equip_stats(ring_b_code, is_weapon=False, target=target)
            for stat_line in ring_b_stats:
                lines.append(f"    {stat_line}")
        else:
            lines.append("  装饰B：无")

        lines.append("───────────────────────────────────────")

        # Total stats
        total_stats = self._get_equip_stats(target)
        if total_stats:
            lines.append("  装备合计效果：")
            if total_stats.get("damage", 0) != 0:
                lines.append(f"    打击力：{total_stats['damage']}")
            if total_stats.get("miss", 0) != 0:
                lines.append(f"    打偏率：{total_stats['miss']}％")
            if total_stats.get("spirit_recover", 0) > 0:
                lines.append(f"    气力恢复：{total_stats['spirit_recover']}")
            if total_stats.get("spirit_recover", 0) < 0:
                lines.append(f"    气力消费：{abs(total_stats['spirit_recover'])}")
            if total_stats.get("combo", 0) != 0:
                lines.append(f"    二连击概率：{total_stats['combo']}％")
            if total_stats.get("def_dmg", 0) != 100:
                lines.append(f"    打击防御：{total_stats['def_dmg']}％")
            if total_stats.get("spirit_dmg", 0) != 100:
                lines.append(f"    打击气力：{total_stats['spirit_dmg']}％")
            if total_stats.get("cursed", False):
                lines.append("    *带有诅咒")
            if total_stats.get("poison", False):
                lines.append("    *带有毒液")
            if total_stats.get("fire", False):
                lines.append("    *带火")
            if total_stats.get("ice", False):
                lines.append("    *带寒冰")
            if total_stats.get("thunder", False):
                lines.append("    *带电")

        return lines

    def _show_floor_status_menu(self):
        while True:
            if self._advance_floor_status_menu():
                return

    def _show_floor_status_page(self) -> bool:
        self._render_floor_status_page()
        return self._handle_floor_status_choice()

    def _show_hero_list(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars
        chars = v.chars

        messages.append("=" * 40)
        messages.append("勇者一览")
        messages.append("=" * 40)

        for idx, char in enumerate(chars[1:], 1):
            if char.cflag.get(1, 0) != 2:
                continue
            char_name = getattr(char, 'savestr', char.name or "")
            hp = char.base.get(0, 0)
            max_hp = char.maxbase.get(0, 0)
            floor = char.cflag.get(501, 0)
            messages.append(f"[{idx:>2}] {char_name:<12} HP:{hp}/{max_hp} {floor}F")

        messages.append("-" * 40)
        messages.append("[999] 返  回")
        return messages

    def _show_invalid_selection(self) -> None:
        print("\nInvalid selection.")
        self._pause()

    def _show_job_names(self) -> List[str]:
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        for idx in range(len(chars)):
            char = chars[idx]
            name = getattr(char, 'savestr', char.name or "???")
            job = self._get_job_name_for_char(idx)
            lines.append(f"[{idx:2d}] {name} - {job}")
        return lines

    def _show_list_assistable(self) -> List[str]:
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        for idx in range(1, len(chars)):
            char = chars[idx]
            if self._is_assistable_check(idx) != 0:
                continue
            name = getattr(char, 'savestr', char.name or "???")
            job = self._get_job_name_for_char(idx)
            lv = char.cflag.get(9, 0)
            hp = char.base.get(0, 0)
            max_hp = char.maxbase.get(0, 0)

            if char.talent.get(85, 0):
                status = "<爱  慕>"
            elif char.talent.get(76, 0):
                status = "<淫  乱>"
            else:
                status = "<未沦陷>"

            tags = ""
            if char.talent.get(64, 0):
                tags += "[脏]"
            if char.talent.get(83, 0):
                tags += "[虐]"
            if char.talent.get(87, 0):
                tags += "[恶]"
            if char.talent.get(91, 0):
                tags += "[魅]"
            if char.talent.get(92, 0):
                tags += "[迷]"
            if char.talent.get(93, 0):
                tags += "[威]"

            bar = self._bar_str(hp, max_hp, 8)
            lines.append(f"[{idx:2d}] {name:12s} {job:6s} LV{lv:4d} HP{bar} {status}{tags}")
        return lines

    def _show_list_trainable(self) -> List[str]:
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        for idx in range(1, len(chars)):
            char = chars[idx]
            if self._is_trainable_check(idx) != 0:
                continue
            name = getattr(char, 'savestr', char.name or "???")
            job = self._get_job_name_for_char(idx)
            lv = char.cflag.get(9, 0)
            hp = char.base.get(0, 0)
            max_hp = char.maxbase.get(0, 0)
            train_count = char.cflag.get(10, 0)

            if char.talent.get(85, 0):
                status = "<爱  慕>"
            elif char.talent.get(76, 0):
                status = "<淫  乱>"
            else:
                status = "<未沦陷>"

            tags = ""
            if char.cflag.get(700, 0):
                tags += "[☆]"
            if char.talent.get(73, 0):
                tags += "[陷]"
            if char.talent.get(72, 0):
                tags += "[瘾]"
            if char.talent.get(135, 0):
                tags += "[未]"

            bar = self._bar_str(hp, max_hp, 8)
            lines.append(f"[{idx:2d}] {name:12s} {job:6s} LV{lv:4d} HP{bar} 调教回数:{train_count:3d} {status}{tags}")
        return lines

    def _show_long_goodbye_witness_reaction(self, witness: Character, target: Character) -> None:
        print("")
        print(f"那天，{witness.name} 望着被卖掉的 {target.name} 坐上了马车。")
        print(f"{witness.name} 一直目送着她，直到彻底看不见为止。")

    def _show_look(self, target) -> List[str]:
        """Show complete character appearance.
        Corresponds to ERB @LOOK_INFO.
        Returns a list of display lines.
        """
        lines: List[str] = []
        name = target.name or "???"

        # 种族信息
        race_name = self._get_race_name(target)
        race_str = f"[{race_name}"
        if int(target.talent.get(220, 0)):
            race2_name = self._get_race2_name(target)
            if race2_name:
                race_str += f"·{race2_name}"
        race_str += "]"
        lines.append(f"{name} {race_str}")

        # 发色与头发状态
        hair_color = int(target.talent.get(300, 0))
        hair_state = int(target.talent.get(301, 0))
        if hair_color and hair_state:
            lines.append(f"[发色：{self._get_hair_color_name(target)}]"
                         f"[头发状态：{self._get_hair_state_name(target)}]")

        # 头发长度・修剪・发型
        hair_length = int(target.talent.get(302, 0))
        hair_cut = int(target.talent.get(303, 0))
        hair_style = int(target.talent.get(304, 0))
        if hair_length and hair_cut and hair_style:
            lines.append(f"[头发长度：{self._get_hair_length_name(target)}]"
                         f"[修剪：{self._get_hair_cut_name(target)}]"
                         f"[发型：{self._get_hair_style_name(target)}]")

        # 眼形・瞳色・唇
        face_desc = self._get_face_desc(target)
        if face_desc:
            lines.append(face_desc)

        # 体型・乳头・阴毛
        body_desc = self._get_body_desc(target)
        if body_desc:
            lines.append(body_desc)

        # 魅力点・癖好
        charm = int(target.talent.get(312, 0))
        habit = int(target.talent.get(313, 0))
        if charm and habit:
            lines.append(f"[魅力点：{self._get_charm_point_name(target)}]"
                         f"[癖好：{self._get_habit_name(target)}]")

        # 服装
        cloth_desc = self._get_cloth_desc(target)
        if cloth_desc:
            lines.append(f"[服装：{cloth_desc}]")

        # 过去
        past_life = int(target.talent.get(315, 0))
        if past_life:
            template_id = target.template_id
            if template_id is not None and template_id >= 200 and template_id != 222:
                lines.append(f"[来到据点之前：{self._get_past_life_name(target)}]")
            elif int(target.talent.get(220, 0)) == 1:
                lines.append(f"[出生是因为：{self._get_past_life_name(target)}]")
            elif target is not self._get_player() and not int(target.talent.get(122, 0)):
                lines.append(f"[成为勇者之前：{self._get_past_life_name(target)}]")
            elif target is not self._get_player():
                lines.append(f"[成为冒险者之前：{self._get_past_life_name(target)}]")
            else:
                lines.append(f"[成为魔王之前：{self._get_past_life_name(target)}]")

        # 契机
        hero_reason = int(target.talent.get(316, 0))
        if hero_reason:
            template_id = target.template_id
            if template_id is not None and template_id >= 200 and template_id != 222:
                lines.append(f"[回应召唤的理由：{self._get_hero_reason_name(target)}]")
            elif int(target.talent.get(220, 0)) == 1:
                lines.append(f"[选择留下的理由：{self._get_hero_reason_name(target)}]")
            elif target is not self._get_player() and not int(target.talent.get(122, 0)):
                lines.append(f"[成为勇者的契机：{self._get_hero_reason_name(target)}]")
            elif target is not self._get_player():
                lines.append(f"[成为冒险者的契机：{self._get_hero_reason_name(target)}]")
            else:
                lines.append(f"[成为魔王的契机：{self._get_hero_reason_name(target)}]")

        # 妊娠适性
        if int(target.talent.get(158, 0)):
            lines.append("[妊娠适性：只能异种族]")

        # 所持金
        money = int(target.cflag.get(580, 0))
        if money <= 0:
            lines.append("[所持金：身无分文]")
        else:
            lines.append(f"[所持金：{money}]")

        # 借金
        debt = int(target.cflag.get(582, 0))
        if debt < 0:
            lines.append(f"[借金：{0 - debt}]")

        # 信仰
        has_faith = (int(target.talent.get(242, 0)) or int(target.talent.get(250, 0))
                     or int(target.talent.get(315, 0)) == 11
                     or int(target.talent.get(315, 0)) == 12)
        faith_val = int(target.cflag.get(152, 0))
        if has_faith and faith_val >= 10 and target is not self._get_player():
            faith_name = ""
            if int(target.talent.get(85, 0)):
                faith_name = "魔王大人♡♡♡"
            elif int(target.cflag.get(0, 0)) != 0:
                faith_name = "无名的淫荡女神♡♡♡"
            elif int(target.talent.get(220, 0)):
                faith_name = "混沌的魔界女神"
            elif int(target.talent.get(250, 0)):
                faith_name = "潜藏地底的死亡女神"
            elif int(target.talent.get(242, 0)):
                faith_name = "纯洁的神圣女神"
            elif int(target.talent.get(315, 0)) == 11:
                faith_name = "丰饶的大地女神"
            elif int(target.talent.get(315, 0)) == 12:
                faith_name = "包容一切的大海女神"
            if faith_name:
                lines.append(f"[信仰：{faith_name}（信仰値：{faith_val}）]")

        # 喜欢的东西
        love_prefs = self._get_love_preferences(target)
        if love_prefs:
            lines.append("[喜欢的东西]")
            # 6个一行
            for i in range(0, len(love_prefs), 6):
                chunk = love_prefs[i:i + 6]
                lines.append("  " + "  ".join(chunk))
            lines.append(f"[共{len(love_prefs)}个喜欢的东西]")

        return lines

    def _show_main_menu_character_detail(self, idx: int):
        if idx < 0 or idx >= len(self.interpreter.vars.chars):
            print("\n当前没有可查看的对象。")
            self._pause()
            return
        char = self.interpreter.vars.chars[idx]
        while True:
            if self._advance_main_menu_character_detail(idx, char):
                return

    def _show_meat_toilet_menu(self):
        while True:
            if self._advance_meat_toilet_menu():
                return

    def _show_mod_status(self) -> List[str]:
        """Show compact MOD status line (for CONFIG display)."""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))

        bank_on = self._get_bit(ex_flag_9000, 0)
        iron_on = self._get_bit(ex_flag_9000, 1)
        ptj_on = self._get_bit(ex_flag_9000, 2)

        # Return as a single line like the ERB does
        return [f"[银行]　" if bank_on else "[银行]　",
                f"[铁心]　" if iron_on else "[铁心]　",
                f"[打工]　" if ptj_on else "[打工]　"]

    def _show_mod_switch(self) -> List[str]:
        """Show MOD switch menu."""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))
        lines: List[str] = []

        bank_on = self._get_bit(ex_flag_9000, 0)
        iron_on = self._get_bit(ex_flag_9000, 1)
        ptj_on = self._get_bit(ex_flag_9000, 2)

        lines.append(f"[0]魔界银行\t　　 现在：{'ON' if bank_on else 'OFF'}")
        lines.append(f"[1]铁石心肠（后代可处刑、可迎击）现在：{'ON' if iron_on else 'OFF'}")
        lines.append(f"[2]打工系统\t　　 现在：{'ON' if ptj_on else 'OFF'}")
        lines.append("────────────────────────────────")
        lines.append("[100] 返回")

        return lines

    def _show_mod_switch_menu(self) -> tuple[bool, str]:
        while True:
            result = self._advance_mod_switch_menu()
            if result is not None:
                return result

    def _show_ptj_status(self, target: Character) -> List[str]:
        """显示角色打工状态"""
        lines: List[str] = []
        cflag120 = int(target.cflag.get(120, 0))
        ptj_info = self._get_ptj_info(target)

        if cflag120 == 0 and ptj_info["count"] > 0:
            lines.append("[18] 打工")
        elif ptj_info["highest_pos"] > 0:
            job_name = ptj_info["name"]
            level = ptj_info["highest_level"]
            ex_cflag = getattr(target, 'ex_cflag', {})
            raw_val = int(ex_cflag.get(ptj_info["highest_pos"], 0))
            if raw_val == 0:
                motivation = "没有"
            elif raw_val == 1:
                motivation = "普通"
            else:
                motivation = f"{raw_val}等级"
            lines.append(f"[18] {job_name}积极性 - {motivation}")
        return lines

    def _show_result_message(self, result: tuple[bool, str]) -> None:
        _, message = result
        print(f"\n{message}")
        self._pause()

    def _show_slave_list(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars
        chars = v.chars

        messages.append("=" * 40)
        messages.append("奴隶一览")
        messages.append("=" * 40)

        for idx, char in enumerate(chars[1:], 1):
            if char.cflag.get(1, 0) != 0:
                continue
            char_name = getattr(char, 'savestr', char.name or "")
            status = "待命" if char.cflag.get(1, 0) == 0 else "出勤中"
            sell_flag = "可卖" if char.cflag.get(0, 0) >= 1 else "不可卖"
            hp = char.base.get(0, 0)
            max_hp = char.maxbase.get(0, 0)
            messages.append(f"[{idx:>2}] {char_name:<12} HP:{hp}/{max_hp} {status} {sell_flag}")

        messages.append("-" * 40)
        messages.append("[999] 返  回")
        return messages

    def _show_specific_floor_status(self, floor_code: int):
        print()
        if floor_code == 10:
            for line in self._get_guard_status_lines():
                print(line)
        else:
            for line in self._get_floor_status_lines(floor_code):
                print(line)
        self._pause()
