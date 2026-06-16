from __future__ import annotations
"""Module for ConfigMixin - 配置/设置"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ConfigMixin:
    """Mixin providing 配置/设置 methods for GameEngine"""

    def _advance_settings_filter_menu(self) -> Optional[tuple[bool, str]]:
        self._render_settings_filter_menu()
        choice = self._prompt_choice()
        if choice == "100":
            return True, "已返回过滤器菜单。"
        try:
            bit = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            return None
        if bit < 0 or bit > 4:
            print("\nInvalid selection.")
            return None
        print(f"\n{self._toggle_filter_bit(bit)}")
        return None




    def _advance_settings_menu(self, page: int) -> tuple[bool, int]:
        return self._handle_settings_page_choice(self._prompt_settings_page_choice(page), page)




    def _apply_offervirgin_check(self) -> List[str]:
        messages: List[str] = []
        target_idx = int(self.interpreter.vars.target)
        if target_idx <= 0 or target_idx >= len(self.interpreter.vars.chars):
            return messages
        target = self.interpreter.vars.chars[target_idx]
        if not self._can_trigger_offervirgin_check(target_idx, target):
            return messages
        score = -2
        if target.talent.get(85, 0):
            score += 1 if int(target.abl.get(10, 0)) == 4 else 2 if int(target.abl.get(10, 0)) == 5 else 3 if int(target.abl.get(10, 0)) >= 6 else 0
        if target.talent.get(76, 0):
            score += 1 if int(target.abl.get(11, 0)) == 4 else 2 if int(target.abl.get(11, 0)) == 5 else 3 if int(target.abl.get(11, 0)) >= 6 else 0
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and self._get_palam_level(int(target.palam.get(5, 0))) >= 4:
            score += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(16, 0)) >= 4 and self._get_palam_level(int(target.palam.get(5, 0))) >= 4:
            score += 1
        if target.talent.get(70, 0):
            score += 1
        elif target.talent.get(71, 0):
            score -= 2
        if target.talent.get(30, 0):
            score -= 2
        elif target.talent.get(31, 0):
            score += 1
        if target.talent.get(27, 0):
            score += 1
        if target.talent.get(28, 0):
            score -= 2
        player = self._get_player()
        if player is None:
            return messages
        target.talent[0] = 0
        if target.talent.get(273, 0):
            target.talent[273] = 0
            messages.append("守护贞操的封印破碎了……")
        target.exp[0] = int(target.exp.get(0, 0)) + 2
        target.exp[5] = int(target.exp.get(5, 0)) + 1
        target.exp[20] = int(target.exp.get(20, 0)) + 1
        target.juel[1] = int(target.juel.get(1, 0)) + score * 400
        target.juel[4] = int(target.juel.get(4, 0)) + score * 1000
        target.juel[5] = int(target.juel.get(5, 0)) + score * 500
        target.juel[6] = int(target.juel.get(6, 0)) + score * 1000
        target.juel[9] = int(target.juel.get(9, 0)) + score * 1000
        if int(target.abl.get(10, 0)) < 2:
            target.abl[10] = 2
        if int(target.cflag.get(15, 0)) == 0:
            player_template_id = self._get_character_template_id(player)
            target.cflag[15] = (int(player_template_id) + 1) if player_template_id is not None else 1
            target.cstr[3] = player.name
        if int(player.talent.get(1, 0)) != 0:
            player.talent[1] = 0
            if int(player.cflag.get(15, 0)) == 0:
                target_template_id = self._get_character_template_id(target)
                player.cflag[15] = (int(target_template_id) + 1) if target_template_id is not None else 1
                player.cstr[3] = target.name
        if int(target.cflag.get(49, 0)) != 0:
            target.cflag[49] = 0
            target.cflag[40] = int(target.cflag.get(40, 0)) & ~64
            target.cflag[50] = 0
            target.cflag[42] = 0
        target.cflag[101] = max(30, int(target.cflag.get(101, 0)))
        self._add_pregnancy_source_amount(target, 1, 1)
        messages.extend(
            [
                f"{target.name} 把自己的处女献给了魔王。",
                "【处女丧失】",
            ]
        )
        return messages






    def _apply_offervirgin_events(self) -> List[str]:
        messages: List[str] = []
        saved_target = self.interpreter.vars.target
        saved_assi = self.interpreter.vars.assi
        try:
            for idx in range(1, len(self.interpreter.vars.chars)):
                target = self.interpreter.vars.chars[idx]
                if int(target.talent.get(0, 0)) == 0:
                    continue
                self.interpreter.vars.target = idx
                messages.extend(self._apply_offervirgin_check())
        finally:
            self.interpreter.vars.target = saved_target
            self.interpreter.vars.assi = saved_assi
        return messages






    def _apply_settings_entry(self, entry_id: int) -> tuple[bool, str]:
        all_entries = self._get_settings_page_entries(0) + self._get_settings_page_entries(1)
        entry = next((item for item in all_entries if int(item["id"]) == entry_id), None)
        if entry is None:
            return False, "Invalid selection."

        entry_type = entry["type"]
        if entry_type == "bit":
            enabled = self._toggle_flag_bit(int(entry["flag"]), int(entry["bit"]))
            return True, f"{entry['label']} 已切换为 {'ON' if enabled else 'OFF'}。"
        if entry_type == "toggle":
            flag = int(entry["flag"])
            self.interpreter.vars.set_flag(flag, 0 if self.interpreter.vars.get_flag(flag, 0) else 1)
            return True, f"{entry['label']} 已切换。"
        if entry_type == "filter":
            return self._show_settings_filter_menu()
        if entry_type == "dualbit":
            for bit in entry["bits"]:
                self._toggle_flag_bit(int(entry["flag"]), int(bit))
            return True, f"{entry['label']} 已整体切换。"
        if entry_type == "age_measurements":
            return self._show_age_measurement_menu()
        if entry_type == "penis":
            return self._show_settings_penis_menu()
        if entry_type == "autoup":
            return True, self._cycle_auto_ability_up_setting()
        if entry_type == "virgin":
            return self._show_settings_virgin_menu()
        if entry_type == "modlist":
            return self._show_settings_modlist_menu()
        return False, "未接入该配置项。"






    def _apply_sex_virgin_break(self, target: Character, partner: Character, exp_delta: Dict[int, int], submission_floor: int):
        if not target.talent.get(0, 0):
            return
        target.talent[0] = 0
        target.exp[50] = target.exp.get(50, 0) + 1
        if int(target.abl.get(10, 0)) < submission_floor:
            target.abl[10] = submission_floor
        if int(target.cflag.get(15, 0)) == 0:
            template_id = self._get_character_template_id(partner)
            target.cflag[15] = (template_id + 1) if template_id is not None else 1
            target.cstr[3] = partner.name
        exp_delta[50] = exp_delta.get(50, 0) + 1






    def _can_trigger_offervirgin_check(self, idx: int, target: Character) -> bool:
        if int(self.interpreter.vars.get_flag(38, -1)) <= -1:
            return False
        if target.talent.get(151, 0):
            return False
        if target.talent.get(135, 0):
            return False
        if target.talent.get(0, 0) == 0 or target.talent.get(122, 0):
            return False
        player = self._get_player()
        if player is None or (player.talent.get(122, 0) == 0 and player.talent.get(121, 0) == 0):
            return False
        if target.talent.get(85, 0) == 0 and target.talent.get(76, 0) == 0:
            return False
        if int(target.exp.get(23, 0)) < 200:
            return False
        if int(target.abl.get(10, 0)) + int(target.abl.get(11, 0)) + int(target.abl.get(16, 0)) <= 10:
            return False
        if int(target.base.get(0, 0)) < 500:
            return False
        if target.cflag.get(71, 0) > 0:
            return False
        if int(target.cflag.get(42, 0)) == 79 and bool(target.cflag.get(40, 0) & 64):
            if int(target.cflag.get(49, 0)) == 0 or int(target.cflag.get(50, 0)) == 0:
                return False
        if int(target.cflag.get(1, 0)) != 0:
            return False
        if self._get_last_training_target_index() != int(idx):
            return False
        if int(self.interpreter.vars.get_flag(38, 0)) == 0 and int(target.cflag.get(62, 0)) != 0:
            return False
        score = -2
        if target.talent.get(85, 0):
            if int(target.abl.get(10, 0)) == 4:
                score += 1
            elif int(target.abl.get(10, 0)) == 5:
                score += 2
            elif int(target.abl.get(10, 0)) >= 6:
                score += 3
        if target.talent.get(76, 0):
            if int(target.abl.get(11, 0)) == 4:
                score += 1
            elif int(target.abl.get(11, 0)) == 5:
                score += 2
            elif int(target.abl.get(11, 0)) >= 6:
                score += 3
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and self._get_palam_level(int(target.palam.get(5, 0))) >= 4:
            score += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(16, 0)) >= 4 and self._get_palam_level(int(target.palam.get(5, 0))) >= 4:
            score += 1
        if target.talent.get(70, 0):
            score += 1
        elif target.talent.get(71, 0):
            score -= 2
        if target.talent.get(30, 0):
            score -= 2
        elif target.talent.get(31, 0):
            score += 1
        if target.talent.get(27, 0):
            score += 1
        if target.talent.get(28, 0):
            score -= 2
        return score > 0






    def _cm_virgin(self, char: Character, is_descendant: bool = False) -> None:
        """处女设定 (对应 @CM_VIRGIN)"""
        is_male = char.talent.get(122, 0) == 1
        is_futa = char.talent.get(121, 0) == 1
        
        if is_male:
            # 男性
            char.talent[0] = 0  # 非处女
            if random.randint(0, 2) > 0:
                char.talent[1] = 1  # 童贞
                char.cflag[15] = -1  # 初体验
                char.cflag[16] = -1  # 初吻
            else:
                char.cflag[15] = 0
                char.cflag[16] = 0
        elif is_descendant:
            # 后代
            char.talent[0] = 1  # 处女
            char.cflag[16] = -1
        elif is_futa:
            # 扶她
            if random.randint(0, 7) != 0:
                char.talent[0] = 1  # 处女
            if random.randint(0, 2) > 0:
                char.talent[1] = 1  # 童贞
                char.cflag[16] = -1
            else:
                char.cflag[16] = 0
            # 初体验
            if char.talent.get(0, 0) and char.talent.get(1, 0):
                char.cflag[15] = -1
            elif char.talent.get(0, 0) == 0 or char.talent.get(1, 0) == 0:
                char.cflag[15] = 0
        elif self.interpreter.vars.get_flag(82, 0) == 1 and random.randint(0, 1) == 0:
            char.talent[0] = 1
            char.cflag[16] = -1
        elif random.randint(0, 7) != 0:
            char.talent[0] = 1
            char.cflag[16] = -1
        
        # 处女时初吻未定
        if char.talent.get(0, 0) == 1:
            char.cflag[16] = -1
        
        # 处女随机贞操封印
        if char.talent.get(0, 0) == 1 and random.randint(0, 4) == 0 and not char.talent.get(220, 0):
            char.talent[273] = 1
        
        # 人妻设定 (非男性、非后代)
        if random.randint(0, 11) == 0 and not is_male and not is_descendant:
            char.talent[157] = 1
            char.talent[0] = 0






    def _config_filter_setting(self, filter_bit: int) -> None:
        """Toggle a filter bit in FLAG:25.
        Corresponds to ERB @CONFIG_FILTER_SETTING.
        filter_bit: 0-4 for the five filter categories.
        """
        if 0 <= filter_bit <= 4:
            flag25 = int(self.interpreter.vars.get_flag(25, 0))
            flag25 ^= (1 << filter_bit)
            self.interpreter.vars.set_flag(25, flag25)




    def _config_get_penis_status(self) -> str:
        """Get penis status text.
        Corresponds to ERB @CONFIG_PENIS_YOU_SETTING display.
        """
        if self.interpreter.vars.chars:
            penis_type = int(self.interpreter.vars.chars[0].talent.get(318, 0))
        else:
            penis_type = 0
        status_map = {
            0: "普通",
            1: "巨根",
            2: "短小包茎",
            3: "包茎",
            4: "马阴茎",
        }
        return status_map.get(penis_type, "普通")




    def _config_modlist_status(self) -> str:
        """Show MOD list status as a single line.
        Corresponds to ERB @CONFIG_MODLIST display.
        """
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))
        parts = []
        parts.append(f"魔界银行:{'ON' if self._get_bit(ex_flag_9000, 0) else 'OFF'}")
        parts.append(f"铁石心肠:{'ON' if self._get_bit(ex_flag_9000, 1) else 'OFF'}")
        parts.append(f"打工系统:{'ON' if self._get_bit(ex_flag_9000, 2) else 'OFF'}")
        return " ".join(parts)

    # =========================================================================
    # LABO (实验室系统)
    # =========================================================================



    def _config_set_penis(self, value: int) -> None:
        """Set penis type.
        Corresponds to ERB @CONFIG_PENIS_YOU_SETTING.
        value: 0=普通, 1=巨根, 2=短小包茎, 3=包茎, 4=马阴茎
        """
        if 0 <= value <= 4 and self.interpreter.vars.chars:
            self.interpreter.vars.chars[0].talent[318] = value




    def _config_set_virgin_conceded(self, value: int) -> None:
        """Set virgin conceded setting.
        Corresponds to ERB @CONFIG_VIRGIN_CONCEDED_SETTING.
        value: 0=从不发生, 1=每人一次, 2=持续触发
        """
        if 0 <= value <= 2:
            self.interpreter.vars.set_flag(38, value - 1)




    def _config_show_filter_status(self) -> str:
        """Show filter status as a single line.
        Corresponds to ERB @CONFIG_SHOW_FILTER_STATUS.
        """
        flag25 = int(self.interpreter.vars.get_flag(25, 0))
        parts = []
        parts.append("爱抚" if not self._get_bit(flag25, 0) else "　　")
        parts.append("器具" if not self._get_bit(flag25, 1) else "　　")
        parts.append("私处类" if not self._get_bit(flag25, 2) else "　　　")
        parts.append("肛门类" if not self._get_bit(flag25, 3) else "　　　")
        parts.append("SM系" if not self._get_bit(flag25, 4) else "　　 ")
        return "　".join(parts)




    def _config_virgin_conceded_status(self) -> str:
        """Show virgin conceded status.
        Corresponds to ERB @CONFIG_VIRGIN_CONCEDED_STATUS.
        """
        flag38 = int(self.interpreter.vars.get_flag(38, 0))
        if flag38 <= -1:
            return "从不发生"
        elif flag38 == 0:
            return "每人一次"
        else:
            return "持续触发"




    def _configure_otherworld_hero_template_character(self, new_char: Character, sex_choice: int) -> None:
        self._append_character(new_char)
        new_char.cflag[1] = 0
        new_char.talent[122] = 1 if sex_choice == 1 else 0
        new_char.talent[121] = 1 if sex_choice == 3 else 0
        if new_char.cflag.get(151, 0) < -100:
            new_char.cflag[151] = -100




    def _cycle_auto_ability_up_setting(self) -> str:
        first = self._get_flag_bit(5, 35)
        second = self._get_flag_bit(5, 36)
        if not first:
            self._set_flag_bit(5, 35, True)
            self._set_flag_bit(5, 36, False)
            return "自动提升角色能力已切换为 ON。"
        if not second:
            self._set_flag_bit(5, 36, True)
            return "自动提升角色能力已切换为 仅主要。"
        self._set_flag_bit(5, 35, False)
        self._set_flag_bit(5, 36, False)
        return "自动提升角色能力已切换为 OFF。"






    def _format_settings_entry_status(self, entry: Dict[str, Any]) -> str:
        entry_type = entry["type"]
        handler_name = SETTINGS_ENTRY_STATUS_HANDLERS.get(entry_type)
        if handler_name is None:
            return "-"
        handler = getattr(self, handler_name, None)
        if handler is None:
            return "-"
        return handler(entry)






    def _format_settings_entry_status_age_measurements(self, entry: Dict[str, Any]) -> str:
        return f"{'ON' if self._get_flag_bit(5, 12) else 'OFF'}/{'ON' if self._get_flag_bit(5, 15) else 'OFF'}"






    def _format_settings_entry_status_autoup(self, entry: Dict[str, Any]) -> str:
        first = self._get_flag_bit(5, 35)
        second = self._get_flag_bit(5, 36)
        if not first:
            return "OFF"
        return "仅主要" if second else "ON"






    def _format_settings_entry_status_bit(self, entry: Dict[str, Any]) -> str:
        enabled = self._get_flag_bit(int(entry["flag"]), int(entry["bit"]))
        return entry["on"] if enabled else entry["off"]






    def _format_settings_entry_status_dualbit(self, entry: Dict[str, Any]) -> str:
        bits = entry["bits"]
        return f"{'ON' if self._get_flag_bit(int(entry['flag']), bits[0]) else 'OFF'}/{'ON' if self._get_flag_bit(int(entry['flag']), bits[1]) else 'OFF'}"






    def _format_settings_entry_status_filter(self, entry: Dict[str, Any]) -> str:
        return self._get_filter_status_text()






    def _format_settings_entry_status_modlist(self, entry: Dict[str, Any]) -> str:
        return self._get_mod_switch_status_text()






    def _format_settings_entry_status_penis(self, entry: Dict[str, Any]) -> str:
        return self._get_player_penis_status_text()






    def _format_settings_entry_status_toggle(self, entry: Dict[str, Any]) -> str:
        return "ON" if self.interpreter.vars.get_flag(int(entry["flag"]), 0) else "OFF"






    def _format_settings_entry_status_virgin(self, entry: Dict[str, Any]) -> str:
        return self._get_virgin_conceded_status_text()






    def _get_config(self, key: int) -> int:
        """Get a configuration value.
        key: the menu option number (0-26)
        Returns the current value for the given config key.
        """
        flag5 = int(self.interpreter.vars.get_flag(5, 0))
        flag8 = int(self.interpreter.vars.get_flag(8, 0))

        if 0 <= key <= 10:
            return 1 if self._get_bit(flag5, key) else 0
        elif key == 11:
            return int(self.interpreter.vars.get_flag(37, 0))
        elif key == 12:
            return int(self.interpreter.vars.get_flag(35, 0))
        elif key == 13:
            return int(self.interpreter.vars.get_flag(25, 0))
        elif key == 14:
            return 1 if self._get_bit(flag5, 11) else 0
        elif key == 15:
            return (1 if self._get_bit(flag5, 12) else 0) | ((1 if self._get_bit(flag5, 15) else 0) << 1)
        elif key == 16:
            return 1 if self._get_bit(flag5, 32) else 0
        elif key == 17:
            return 1 if self._get_bit(flag5, 33) else 0
        elif key == 18:
            return 1 if self._get_bit(flag5, 34) else 0
        elif key == 19:
            if self.interpreter.vars.chars:
                return int(self.interpreter.vars.chars[0].talent.get(318, 0))
            return 0
        elif key == 20:
            result = 0
            if self._get_bit(flag5, 35):
                result |= 1
            if self._get_bit(flag5, 36):
                result |= 2
            return result
        elif key == 21:
            return int(self.interpreter.vars.get_flag(38, 0))
        elif 22 <= key <= 25:
            bit = key - 22
            return 1 if self._get_bit(flag8, bit) else 0
        elif key == 26:
            return 0
        return 0






    def _get_filter_status_text(self) -> str:
        labels = ["爱抚", "器具", "私处类", "肛门类", "SM系"]
        parts = [f"{label}:{'ON' if self._get_flag_bit(25, bit) else 'OFF'}" for bit, label in enumerate(labels)]
        return " ".join(parts)






    def _get_penis_state_name(self, target) -> str:
        """获取阴茎状态名称 (TALENT:318)"""
        v = int(target.talent.get(318, 0))
        return self._PENIS_STATE_NAMES.get(v, "普通")






    def _get_player_penis_status_text(self) -> str:
        player = self._get_player()
        if player is None:
            return "普通"
        value = player.talent.get(318, 0)
        labels = {
            0: "普通",
            1: "巨根",
            2: "短小包茎",
            3: "包茎",
            4: "马阴茎",
        }
        return labels.get(value, "普通")






    def _get_settings_page_entries(self, page: int) -> List[Dict[str, Any]]:
        return SETTINGS_PAGE_ENTRIES.get(int(page), SETTINGS_PAGE_ENTRIES[1])






    def _get_virgin_conceded_status_text(self) -> str:
        value = self.interpreter.vars.get_flag(38, -1)
        if value <= -1:
            return "从不发生"
        if value == 0:
            return "每人一次"
        return "持续触发"






    def _handle_settings_navigation_choice(self, choice: str, page: int) -> tuple[bool, tuple[bool, int]]:
        page_result = self._handle_settings_page_switch_choice(choice, page)
        if page_result is not None:
            return page_result
        command_result = self._handle_settings_page_command_choice(choice, page)
        if command_result is not None:
            return command_result
        return False, (False, page)




    def _handle_settings_page_choice(self, choice: str, page: int) -> tuple[bool, int]:
        handled, result = self._handle_settings_navigation_choice(choice, page)
        if handled:
            return result
        entry_id = self._parse_choice_int(choice)
        if entry_id is None:
            self._show_invalid_selection()
            return False, page
        ok, message = self._apply_settings_entry(entry_id)
        print(f"\n{message}")
        self._pause()
        return False, page




    def _handle_settings_page_command_choice(self, choice: str, page: int) -> Optional[tuple[bool, int]]:
        if choice == "200":
            self._select_target_from_roster()
            self._pause()
            return False, page
        if choice == "201":
            print(f"\nSave directory: {self.paths.save_dir}")
            self._pause()
            return False, page
        return None




    def _handle_settings_page_switch_choice(self, choice: str, page: int) -> Optional[tuple[bool, int]]:
        if choice == "100":
            return True, page
        if choice == "101":
            return False, (page + 1) % 2
        if choice == "102":
            return False, (page - 1) % 2
        return None




    def _handle_settings_penis_choice(self, choice: str, player: Character) -> tuple[bool, str]:
        try:
            value = int(choice)
        except ValueError:
            return False, "Invalid selection."
        if value < 0 or value > 4:
            return False, "Invalid selection."
        player.talent[318] = value
        return True, f"已将魔王的兵器状态设为 {self._get_player_penis_status_text()}。"




    def _handle_settings_virgin_choice(self, choice: str) -> tuple[bool, str]:
        try:
            value = int(choice)
        except ValueError:
            return False, "Invalid selection."
        if value < 0 or value > 2:
            return False, "Invalid selection."
        self.interpreter.vars.set_flag(38, value - 1)
        return True, f"已设为 {self._get_virgin_conceded_status_text()}。"




    def _offer_virgin_check(self, target) -> List[str]:
        """处女献上チェック - 对应 @OFFERVIRGIN_CHECK"""
        messages: List[str] = []
        return messages






    def _prompt_settings_page_choice(self, page: int) -> str:
        self._show_settings_page(page)
        return self._prompt_choice()




    def _render_settings_filter_menu(self) -> None:
        print("\n【调教过滤器】")
        for bit, label in enumerate(["爱抚系", "器具系", "私处性交系", "肛门性交系", "SM系"]):
            print(f" [{bit}] {label} : {'ON' if self._get_flag_bit(25, bit) else 'OFF'}")
        print(" [100] Back")




    def _render_settings_page(self, page: int, entries: List[Dict[str, Any]]) -> None:
        print("\n【Settings】")
        print("-" * 30)
        print(f" Page {page + 1}/2")
        for entry in entries:
            status = self._format_settings_entry_status(entry)
            print(f" [{entry['id']}] {entry['label']} : {status}")
        print("-" * 30)
        print(" [102] 上一页")
        print(" [100] 返回")
        print(" [101] 下一页")
        print(" [200] 更改当前目标")
        print(" [201] 查看存档目录")




    def _render_settings_penis_menu(self) -> None:
        print("\n【魔王的兵器状态】")
        print(" [0] 普通")
        print(" [1] 巨根")
        print(" [2] 短小包茎")
        print(" [3] 包茎")
        print(" [4] 马阴茎")
        print(" [999] Back")




    def _render_settings_virgin_menu(self) -> None:
        print("\n【陷落后处女主动献身】")
        print(" [0] 从不发生")
        print(" [1] 每人一次")
        print(" [2] 持续触发")
        print(" [100] Back")




    def _set_config(self, key: int, value: int) -> None:
        """Set a configuration value.
        Corresponds to ERB @CONFIG input handling.
        key: the menu option number (0-26)
        value: unused for toggle options, used for specific settings
        """
        flag5 = int(self.interpreter.vars.get_flag(5, 0))

        if 0 <= key <= 10:
            # Toggle bit in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << key))
        elif key == 11:
            # 服装系统: toggle FLAG:37
            current_flag37 = int(self.interpreter.vars.get_flag(37, 0))
            self.interpreter.vars.set_flag(37, 0 if current_flag37 else 1)
        elif key == 12:
            # 濒死时自动结束调教: toggle FLAG:35
            current_flag35 = int(self.interpreter.vars.get_flag(35, 0))
            self.interpreter.vars.set_flag(35, 0 if current_flag35 else 1)
        elif key == 13:
            # 调教时的过滤: handled by _config_filter_setting
            pass
        elif key == 14:
            # 自我介绍式的角色信息: toggle bit 11 in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << 11))
        elif key == 15:
            # 显示角色的年龄/三围: toggle bit 12 in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << 12))
        elif key == 16:
            # 解除勇者登录限制: toggle bit 32 in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << 32))
        elif key == 17:
            # 新探索模式: toggle bit 33 in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << 33))
        elif key == 18:
            # 显示高级调教指令的名称: toggle bit 34 in FLAG:5
            self.interpreter.vars.set_flag(5, flag5 ^ (1 << 34))
        elif key == 19:
            # 你那宝贝兵器的现状: set TALENT:0:318
            if 0 <= value <= 4 and self.interpreter.vars.chars:
                self.interpreter.vars.chars[0].talent[318] = value
        elif key == 20:
            # 自动提升角色能力: cycle through bits 35,36 in FLAG:5
            flag5 = int(self.interpreter.vars.get_flag(5, 0))
            if not self._get_bit(flag5, 35):
                flag5 |= (1 << 35)
            elif not self._get_bit(flag5, 36):
                flag5 |= (1 << 36)
            else:
                flag5 &= ~((1 << 35) | (1 << 36))
            self.interpreter.vars.set_flag(5, flag5)
        elif key == 21:
            # 陷落之后处女主动献身: set FLAG:38
            self.interpreter.vars.set_flag(38, value - 1)
        elif 22 <= key <= 25:
            # FLAG:8 bits
            flag8 = int(self.interpreter.vars.get_flag(8, 0))
            bit = key - 22
            self.interpreter.vars.set_flag(8, flag8 ^ (1 << bit))
        elif key == 26:
            # MOD开关: handled by _toggle_mod_switch
            pass






    def _show_config(self) -> List[str]:
        """Show configuration menu.
        Corresponds to ERB @CONFIG.
        Returns list of display lines for the config menu.
        """
        lines: List[str] = []
        flag5 = int(self.interpreter.vars.get_flag(5, 0))
        flag8 = int(self.interpreter.vars.get_flag(8, 0))
        flag25 = int(self.interpreter.vars.get_flag(25, 0))
        flag35 = int(self.interpreter.vars.get_flag(35, 0))
        flag37 = int(self.interpreter.vars.get_flag(37, 0))

        # Page 0
        lines.append(f"[0] 勇者投降后的凌辱　　　　　现在：{'许可' if self._get_bit(flag5, 0) else '禁止'}")
        lines.append(f"[1] 勇者强化　　　　　　　　　现在：{'新的勇者会随游戏天数按比例增强' if self._get_bit(flag5, 1) else '勇者等级维持'}")
        lines.append(f"[2] 怀孕分娩机能　　　　　　　现在：{'ON' if self._get_bit(flag5, 2) else 'OFF'}")
        lines.append(f"[3] 勇者自动处刑机能　　　　　现在：{'ON' if self._get_bit(flag5, 3) else 'OFF'}")
        lines.append(f"[4] 禁止怪物迎击　　　　　　　现在：{'ON (+怪物会和迎击的奴隶进行训练)' if self._get_bit(flag5, 4) else 'OFF'}")
        lines.append(f"[5] 显示战斗记录　　　　　　　现在：{'ON' if self._get_bit(flag5, 5) else 'OFF'}")
        lines.append(f"[6] 自动补充陷阱　　　　　　　现在：{'ON' if self._get_bit(flag5, 6) else 'OFF'}")
        lines.append(f"[7] NTR机能　 　　　　　　　　现在：{'ON' if self._get_bit(flag5, 7) else 'OFF'}")
        lines.append(f"[8] 素质分类显示　　　　　　　现在：{'ON' if self._get_bit(flag5, 8) else 'OFF'}")
        lines.append(f"[9] 战斗记录的SKIP中断　　　　现在：{'ON' if self._get_bit(flag5, 9) else 'OFF'}")
        lines.append(f"[10] 怀孕时的迎击・临月调教　 现在：{'许可' if self._get_bit(flag5, 10) else '禁止'}")
        lines.append(f"[11] 服装系统 　　　　　　　　现在：{'ON' if flag37 else 'OFF'}")
        lines.append(f"[12] 濒死时自动结束调教 　　　现在：{'ON' if flag35 else 'OFF'}")
        lines.append(f"[13] 调教时的过滤　　　　　　 现在：{self._config_show_filter_status()}")
        # Page 1
        lines.append(f"[14] 自我介绍式的角色信息　　 现在：{'ON' if self._get_bit(flag5, 11) else 'OFF'}")
        lines.append(f"[15] 显示角色的年龄/三围　　  现在：{'ON' if self._get_bit(flag5, 12) else 'OFF'}/{'ON' if self._get_bit(flag5, 15) else 'OFF'}")
        lines.append(f"[16] 解除勇者登录限制   　 　 现在：{'ON' if self._get_bit(flag5, 32) else 'OFF'}")
        lines.append(f"[17] 新探索模式         　 　 现在：{'ON' if self._get_bit(flag5, 33) else 'OFF'}")
        lines.append(f"[18] 显示高级调教指令的名称   现在：{'ON' if self._get_bit(flag5, 34) else 'OFF'}")
        lines.append(f"[19] 你那宝贝兵器的现状 　　　现在：{self._config_get_penis_status()}")
        lines.append(f"[20] 自动提升角色能力         现在：{'ON' if self._get_bit(flag5, 35) else 'OFF'} {'(仅主要)' if self._get_bit(flag5, 36) else ''}")
        lines.append(f"[21] 陷落之后处女主动献身　　 现在：{self._config_virgin_conceded_status()}")
        lines.append(f"[22] 男冒险者许可 　　　　　　现在：{'许可' if self._get_bit(flag8, 0) else '禁止'}")
        lines.append(f"[23] 勇者出現时的素质表示　　 现在：{'ON' if self._get_bit(flag8, 1) else 'OFF'}")
        lines.append(f"[24] 勇者的恋爱发展　　　　　 现在：{'许可' if self._get_bit(flag8, 2) else '禁止'}")
        lines.append(f"[25] 勇者的任务揭示板  　　　 现在：{'许可' if self._get_bit(flag8, 3) else '禁止'}")
        lines.append(f"[26]　MOD开关　　　　　 　　　現在：{self._config_modlist_status()}")
        lines.append("────────────────────────────────")
        lines.append("[100] 返回")

        return lines






    def _show_settings_filter_menu(self) -> tuple[bool, str]:
        while True:
            result = self._advance_settings_filter_menu()
            if result is not None:
                return result
        return True, "过滤器已更新。"




    def _show_settings_modlist_menu(self) -> tuple[bool, str]:
        return self._show_mod_switch_menu()




    def _show_settings_page(self, page: int):
        entries = self._get_settings_page_entries(page)
        self._render_settings_page(page, entries)




    def _show_settings_penis_menu(self) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "当前没有魔王角色。"
        self._render_settings_penis_menu()
        choice = self._prompt_choice()
        if choice == "999":
            return True, "已取消设置。"
        return self._handle_settings_penis_choice(choice, player)




    def _show_settings_virgin_menu(self) -> tuple[bool, str]:
        self._render_settings_virgin_menu()
        choice = self._prompt_choice()
        if choice == "100":
            return True, "已取消设置。"
        return self._handle_settings_virgin_choice(choice)




    def _toggle_filter_bit(self, bit: int) -> str:
        enabled = self._toggle_flag_bit(25, bit)
        labels = ["爱抚系", "器具系", "私处性交系", "肛门性交系", "SM系"]
        return f"{labels[bit]} 过滤已切换为 {'ON' if enabled else 'OFF'}。"






    def show_settings(self):
        """CONFIG menu aligned to the original multi-page flag structure."""
        page = 0
        while True:
            exit_menu, page = self._advance_settings_menu(page)
            if exit_menu:
                return

    def _config(self):
        """设置 - 桥接ERB CONFIG"""
        return self.call_erb_function('CONFIG')





