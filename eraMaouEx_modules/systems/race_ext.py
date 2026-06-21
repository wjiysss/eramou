from __future__ import annotations
"""Module for RaceExtMixin - 种族系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
import random
if TYPE_CHECKING:
    from eraMaouEx import Character


class RaceExtMixin:
    """Mixin providing 种族系统 methods for GameEngine"""

    def _advance_race_age_config_menu(self, values: List[int]) -> bool:
        self._render_race_age_config_menu(values)
        return self._handle_race_age_config_choice(values)






    def _apply_race_age_rule_code(self, rule: Dict[str, int], code: int) -> bool:
        if int(rule["class"]) == 0 and code in self._get_race_age_integer_option_codes():
            rule["deg"], rule["num"] = self._decode_race_age_code(code)
            return True
        if int(rule["class"]) == 1 and code in self._get_race_age_decimal_option_codes():
            rule["deg"], rule["num"] = self._decode_race_age_code(code)
            return True
        if int(rule["class"]) in {2, 3, 4} and code in self._get_race_age_random_upper_option_codes():
            rule["deg"], rule["num"] = self._decode_race_age_code(code)
            return True
        return False






    def _apply_race_age_rule_mode(self, rule: Dict[str, int], mode_id: int):
        if mode_id == 101:
            rule["class"] = 0
            rule["deg"] = 0
            rule["num"] = 1
        elif mode_id == 102:
            rule["class"] = 0
        elif mode_id == 103:
            rule["class"] = 1
        elif mode_id == 104:
            rule["class"] = 2






    def _confirm_race_age_recalculate(self, values: List[int]) -> bool:
        self._save_race_age_settings(values)
        print("\n全种族的年龄按现在的设定重新计算。")
        print(" [0] 好的")
        print(" [1] 呃……年龄这个问题是个大事啊……让我再想想……")
        confirm = self._prompt_choice()
        if confirm == "0":
            updated = self._recalculate_all_character_race_ages()
            print(f"\n已按当前设定重算 {updated} 名角色的种族年龄。")
        return False






    def _confirm_race_age_reset(self, values: List[int]) -> bool:
        print("\n全种族的年龄均返回默认值。")
        print(" [0] 好的")
        print(" [1] 呃……年龄这个问题是个大事啊……让我再想想……")
        confirm = self._prompt_choice()
        if confirm == "0":
            self._reset_race_age_defaults()
            values[:] = self._unpack_race_age_settings()
            return True
        return False






    def _decode_race_age_code(self, code: int) -> tuple[int, int]:
        return code // 10, code % 10






    def _edit_race_age_rule(self, race_id: int, values: List[Dict[str, int]]):
        rule = values[race_id]
        race_name = self._get_race_age_entries()[race_id]["name"]
        while True:
            self._render_race_age_rule_editor(race_name, rule)
            self._show_race_age_rule_selection(rule)
            action = self._handle_race_age_rule_editor_choice(rule, values, race_id)
            if action == "return":
                return
            if action == "save":
                return






    def _ensure_race_age_defaults(self):
        if self.interpreter.vars.get_flag(26, 0) == 0:
            self._reset_race_age_defaults()






    def _format_race_age_decimal_option(self, code: int) -> str:
        if code == 0:
            return "0.0 倍"
        deg, num = self._decode_race_age_code(code)
        return f"{deg}.{num} 倍"






    def _format_race_age_human_reference(self, rule: Dict[str, int]) -> str:
        rule_class = int(rule["class"])
        deg = int(rule["deg"])
        num = int(rule["num"])
        scale = num * (10 ** deg)
        if rule_class == 0 and deg == 0 and num == 1:
            return "相当于人类 17 岁"
        if rule_class == 0:
            return f"相当于人类 {17 * scale} ～ {17 * scale + scale - 1} 岁"
        if rule_class == 1:
            return f"相当于人类 {17 * (deg * 10 + num) / 10:.1f} 岁"
        if rule_class == 2:
            return f"相当于人类 0 ～ {scale} 岁"
        if rule_class == 3:
            return f"相当于人类 {scale // 2} ～ {scale} 岁"
        if rule_class == 4:
            return f"相当于人类 17 ～ {scale} 岁"
        return "未设定"






    def _format_race_age_integer_option(self, code: int) -> str:
        deg, num = self._decode_race_age_code(code)
        return f"{num * (10 ** deg)} 倍"






    def _format_race_age_random_upper_option(self, code: int) -> str:
        deg, num = self._decode_race_age_code(code)
        return f"{num * (10 ** deg)} 岁"






    def _format_race_age_rule(self, rule: Dict[str, int]) -> str:
        rule_class = int(rule["class"])
        deg = int(rule["deg"])
        num = int(rule["num"])
        scale = num * (10 ** deg)
        if rule_class == 0 and deg == 0 and num == 1:
            return "和人类一样"
        if rule_class == 0:
            return f"换算成人类年龄的 {scale} 倍"
        if rule_class == 1:
            return f"换算成人类年龄的 {deg}.{num} 倍"
        if rule_class == 2:
            return f"0 ～ {scale} 的随机范围"
        if rule_class == 3:
            return f"{scale // 2} ～ {scale} 的随机范围"
        if rule_class == 4:
            return f"年龄 ～ {scale} 的随机范围"
        return "未设定"






    def _generate_race_age(self, human_age: int, race_talent_id: int) -> int:
        human_age = max(0, int(human_age))
        if race_talent_id == 9:
            return human_age

        rule = self._resolve_race_age_rule(int(race_talent_id))
        rule_class = int(rule["class"])
        deg = int(rule["deg"])
        num = int(rule["num"])
        scale = max(0, num * (10 ** deg))

        if rule_class == 0:
            return self._generate_race_age_class_0(human_age, scale)
        if rule_class == 1:
            return self._generate_race_age_class_1(human_age, deg, num)
        if rule_class == 2:
            return self._generate_race_age_class_2(scale)
        if rule_class == 3:
            return self._generate_race_age_class_3(scale)
        if rule_class == 4:
            return self._generate_race_age_class_4(human_age, scale)
        return human_age






    def _generate_race_age_class_0(self, human_age: int, scale: int) -> int:
        if scale <= 0:
            return human_age
        return human_age * scale + random.randrange(scale)






    def _generate_race_age_class_1(self, human_age: int, deg: int, num: int) -> int:
        return human_age * (deg * 10 + num) // 10






    def _generate_race_age_class_2(self, scale: int) -> int:
        if scale <= 0:
            return 0
        digits = len(str(scale))
        biased_upper = (10 ** random.randrange(digits + 1)) * 10
        upper = min(scale, biased_upper)
        upper = max(1, upper)
        return random.randrange(upper)






    def _generate_race_age_class_3(self, scale: int) -> int:
        if scale <= 0:
            return 0
        lower = scale // 2
        span = max(1, scale - lower)
        return lower + random.randrange(span)






    def _generate_race_age_class_4(self, human_age: int, scale: int) -> int:
        if scale <= 0:
            return human_age
        digits = len(str(scale))
        upper = 10
        for _ in range(digits + 1):
            if random.randrange(5) < 2:
                break
            upper *= 10
        upper = min(upper, scale)
        if human_age >= upper:
            upper = human_age + 1
        return human_age + random.randrange(max(1, upper - human_age))






    def _get_race_age_decimal_option_codes(self) -> List[int]:
        codes = [0]
        for lcount in range(31):
            if lcount % 10 > 4 and lcount % 10 != 9:
                continue
            codes.append(lcount + 1)
        return codes






    def _get_race_age_entries(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "name": "精灵"},
            {"id": 1, "name": "狼人"},
            {"id": 2, "name": "吸血鬼"},
            {"id": 3, "name": "无头骑士"},
            {"id": 4, "name": "龙族"},
            {"id": 5, "name": "天使"},
            {"id": 6, "name": "霍比特人"},
            {"id": 7, "name": "矮人"},
        ]






    def _get_race_age_integer_option_codes(self) -> List[int]:
        codes: List[int] = []
        for lcount in range(31):
            if lcount % 10 > 3 and lcount % 10 != 9:
                continue
            codes.append(lcount + 2)
        return codes






    def _get_race_age_random_upper_option_codes(self) -> List[int]:
        codes: List[int] = []
        for lcount in range(31):
            if lcount % 10 > 4:
                continue
            codes.append(lcount + 21)
        return codes






    def _get_race_name(self, target) -> str:
        """获取种族名称 (TALENT:314)"""
        v = int(target.talent.get(314, 0))
        return self._RACE_NAMES.get(v, "ERROR")






    def _handle_race_age_config_choice(self, values: List[int]) -> bool:
        choice = self._prompt_choice()
        if choice == "100":
            self._pack_race_age_settings(values)
            return True
        if choice == "98":
            return self._confirm_race_age_reset(values)
        if choice == "99":
            return self._confirm_race_age_recalculate(values)
        try:
            race_id = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            return False
        if race_id < 0 or race_id >= len(values):
            print("\nInvalid selection.")
            return False
        self._edit_race_age_rule(race_id, values)
        return False






    def _handle_race_age_rule_editor_choice(self, rule: Dict[str, int], values: List[Dict[str, int]], race_id: int) -> Optional[str]:
        choice = self._prompt_choice()
        if choice == "100":
            return "return"
        if choice == "999":
            values[race_id] = dict(rule)
            return "save"
        if choice in {"101", "102", "103", "104"}:
            self._apply_race_age_rule_mode(rule, int(choice))
            return None
        try:
            code = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            return None
        if self._apply_race_age_rule_code(rule, code):
            return None
        if choice in {"110", "111", "112"}:
            rule["class"] = {"110": 2, "111": 3, "112": 4}[choice]
            return None
        print("\nInvalid selection.")
        return None






    def _pack_race_age_settings(self, values: List[Dict[str, int]]):
        packed_a = 0
        for race_id in range(5, -1, -1):
            value = values[race_id]
            packed_a = packed_a * 1000 + int(value["class"]) * 100 + int(value["deg"]) * 10 + int(value["num"])
        packed_b = 0
        for race_id in range(7, 5, -1):
            value = values[race_id]
            packed_b = packed_b * 1000 + int(value["class"]) * 100 + int(value["deg"]) * 10 + int(value["num"])
        self.interpreter.vars.set_flag(26, packed_a)
        self.interpreter.vars.set_flag(27, packed_b)






    def _render_race_age_config_menu(self, values: List[int]) -> None:
        print("\n【种族年龄详细设定】")
        print("        种族        设定                相当于人类17岁的年龄")
        for entry in self._get_race_age_entries():
            race_id = int(entry["id"])
            rule = values[race_id]
            print(f" [{race_id}] {entry['name']:<8} {self._format_race_age_rule(rule):<28} {self._format_race_age_human_reference(rule)}")
        print(" [98] 使用默认设定")
        print(" [99] 重新设定种族年龄并保存")
        print(" [100] 返回")






    def _render_race_age_rule_editor(self, race_name: str, rule: Dict[str, int]) -> None:
        print(f"\n■ 种族 [{race_name}] 的年龄设定：")
        print(self._format_race_age_rule(rule))
        print(self._format_race_age_human_reference(rule))
        print(" [101] 和人类一样")
        print(" [102] 换算成人类年龄的整数倍")
        print(" [103] 换算成人类年龄的小数倍")
        print(" [104] 在一定范围内随机")
        print(" [999] 决定")
        print(" [100] 返回")






    def _reset_race_age_defaults(self):
        default_flag_26, default_flag_27 = self._get_default_race_age_flags()
        self.interpreter.vars.set_flag(26, default_flag_26)
        self.interpreter.vars.set_flag(27, default_flag_27)






    def _resolve_race_age_rule(self, race_talent_id: int) -> Dict[str, int]:
        self._ensure_race_age_defaults()
        if 7 <= race_talent_id < 10:
            if race_talent_id == 7:
                race_index = 0
            elif race_talent_id == 8:
                race_index = 5
            else:
                return {"class": 0, "deg": 0, "num": 1}
        else:
            race_index = race_talent_id - 1
            if race_index > 8:
                race_index -= 3
            if race_index < 0:
                return {"class": 0, "deg": 0, "num": 1}
        values = self._unpack_race_age_settings()
        if 0 <= race_index < len(values):
            return dict(values[race_index])
        return {"class": 0, "deg": 0, "num": 1}






    def _save_race_age_settings(self, values: List[Dict[str, int]]) -> tuple[int, int]:
        self._pack_race_age_settings(values)
        return (
            int(self.interpreter.vars.get_flag(26, 0)),
            int(self.interpreter.vars.get_flag(27, 0)),
        )



    def _show_race_age_config_menu(self) -> tuple[bool, str]:
        values = self._unpack_race_age_settings()
        while True:
            if self._advance_race_age_config_menu(values):
                return True, "已保存并返回。"






    def _show_race_age_decimal_selection(self, rule: Dict[str, int], selected_code: int) -> None:
        self._show_race_age_option_grid(
            " 小数倍选项",
            self._get_race_age_decimal_option_codes(),
            self._format_race_age_decimal_option,
            selected_code=selected_code,
            per_row=4,
        )






    def _show_race_age_integer_selection(self, rule: Dict[str, int], selected_code: int) -> None:
        self._show_race_age_option_grid(
            " 整数倍选项",
            self._get_race_age_integer_option_codes(),
            self._format_race_age_integer_option,
            selected_code=selected_code,
            per_row=4,
        )






    def _show_race_age_option_grid(
        self,
        title: str,
        codes: List[int],
        formatter,
        selected_code: Optional[int] = None,
        per_row: int = 5,
    ):
        print(title)
        row: List[str] = []
        for code in codes:
            marker = "*" if selected_code == code else " "
            row.append(f"{marker}[{code:>2}] {formatter(code):<10}")
            if len(row) >= per_row:
                print(" ".join(row))
                row = []
        if row:
            print(" ".join(row))






    def _show_race_age_random_upper_selection(self, rule: Dict[str, int], selected_code: int) -> None:
        lower_label = {
            2: "[110] 0 岁",
            3: "[111] 上限的1/2",
            4: "[112] 换算成人类年龄",
        }[int(rule["class"])]
        print(f" 当前下限: {lower_label}")
        self._show_race_age_option_grid(
            " 上限选项",
            self._get_race_age_random_upper_option_codes(),
            self._format_race_age_random_upper_option,
            selected_code=selected_code,
            per_row=5,
        )






    def _show_race_age_rule_selection(self, rule: Dict[str, int]):
        rule_class = int(rule["class"])
        selected_code = int(rule["deg"]) * 10 + int(rule["num"])
        if rule_class == 0:
            self._show_race_age_integer_selection(rule, selected_code)
            return
        if rule_class == 1:
            self._show_race_age_decimal_selection(rule, selected_code)
            return
        if rule_class in {2, 3, 4}:
            self._show_race_age_random_upper_selection(rule, selected_code)






    def _unpack_race_age_settings(self) -> List[Dict[str, int]]:
        self._ensure_race_age_defaults()
        packed_a = int(self.interpreter.vars.get_flag(26, 0))
        packed_b = int(self.interpreter.vars.get_flag(27, 0))
        values: List[Dict[str, int]] = []
        for race_id in range(8):
            source = packed_a if race_id <= 5 else packed_b
            offset = race_id if race_id <= 5 else race_id - 6
            chunk = source // (1000 ** offset) % 1000
            values.append({
                "class": int(chunk // 100),
                "deg": int(chunk % 100 // 10),
                "num": int(chunk % 10),
            })
        return values





