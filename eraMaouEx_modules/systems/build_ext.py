from __future__ import annotations
"""Module for BuildExtMixin - 构建与选择"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class BuildExtMixin:
    """Mixin providing 构建与选择 methods for GameEngine"""

    def _build_birth_delivery_line(self, target: Character, source: int) -> str:
        if source == 1:
            child_desc = "魔王的孩子"
        elif source == 4:
            child_desc = "不知道是谁的孩子"
        elif source == 5:
            child_desc = "野狗的孩子"
        elif source == 6:
            child_desc = "怪物的孩子"
        elif source == 7:
            child_desc = "狂王的孩子"
        elif int(target.cflag.get(111, 0)) > 0:
            child_desc = f"{target.cstr.get(2, '').strip() or '地下城内某人'}的孩子"
        else:
            child_desc = "没有父亲的孩子"
        place_desc = self._get_birth_place_description(target)
        if place_desc:
            return f"{target.name} 平安地{place_desc}生下了{child_desc}。"
        return f"{target.name} 平安地生下了{child_desc}。"

    def _build_dog_walk_event_line(self, walker: Character, play: int, no_sex: bool) -> str:
        if no_sex:
            walker.exp[22] = walker.exp.get(22, 0) + 1
            walker.exp[20] = walker.exp.get(20, 0) + 1
            walker.juel[5] = walker.juel.get(5, 0) + 5 * play
            return f"{walker.name} 在散步途中对着野狗发情，最后替它口交来发泄。"

        walker.exp[5] = walker.exp.get(5, 0) + 1
        walker.exp[0] = walker.exp.get(0, 0) + 1
        walker.juel[0] = walker.juel.get(0, 0) + 5 * play
        walker.juel[5] = walker.juel.get(5, 0) + 5 * play
        walker.juel[1] = walker.juel.get(1, 0) + 4 * play
        return f"{walker.name} 在散步途中被野狗挑起欲情，最终和它交配了。"

    def _build_equipment_detail_section(
        self,
        target: Character,
        slot_flag: int,
        label: str,
        name_getter,
    ) -> List[str]:
        equip_code = int(target.cflag.get(slot_flag, -1))
        if equip_code < 0:
            return [f" {label}: {'空手' if slot_flag == 550 else '无'}"]
        lines = [f" {label}: {name_getter(equip_code)}"]
        _, enhance, prefix = self._decode_equipment_code(equip_code)
        detail_parts: List[str] = []
        if enhance:
            detail_parts.append(f"强化+{enhance}")
        if prefix:
            detail_parts.append(f"前缀{prefix}")
        if detail_parts:
            lines.append("  " + " / ".join(detail_parts))
        return lines

    def _build_former_life_prefix(self, *parts: str) -> str:
        filtered = [part for part in parts if part]
        return "".join(filtered) if filtered else "下落不明"

    def _build_general_ending_branch_event(self, flag_id: int, event_key: str, label: str, rise_text: str, fall_text: str, threshold: int, main_flag_delta: int) -> tuple[int, str, str, str, str, int, int]:
        return (flag_id, event_key, label, rise_text, fall_text, threshold, main_flag_delta)

    def _build_general_ending_branch_events(self) -> List[tuple[int, str, str, str, str, int, int]]:
        return self._get_general_ending_branch_events()

    def _build_hand_service_stimulation(self, target: Character, player: Character) -> int:
        stimulation = self._level_value(target.abl.get(12, 0), [450, 1000, 1600, 2200, 2700, 3200])
        stimulation = self._scale_value(stimulation, self._level_value(target.abl.get(10, 0), [80, 90, 100, 110, 120, 130]) / 100.0)
        stimulation = self._scale_value(stimulation, self._level_value(target.abl.get(13, 0), [50, 80, 120, 150, 180, 240]) / 100.0)
        stimulation = self._scale_value(stimulation, self._level_value(player.abl.get(0, 0), [100, 150, 200, 250, 350, 500]) / 100.0)
        return stimulation

    def _build_main_menu_daily_panel_lines(self) -> List[str]:
        lines: List[str] = []
        prestige = self._get_prestige_value()
        prestige_text, _ = self._get_invasion_prestige_state()
        lines.append(f" 威望值: {prestige} 【{prestige_text}】")
        support_income, support_text = self._get_tax_support_income()
        dungeon_income = self._get_tax_dungeon_income()
        land_income, land_messages = self._get_tax_land_income()
        brothel_income, brothel_messages = self._get_tax_brothel_income()
        lines.append(f" 下次征税预估: 支援{support_income} / 地城{dungeon_income} / 领地{land_income} / 设施{brothel_income}")
        if support_text:
            lines.append(f" {support_text}")
        if land_messages:
            lines.extend(f" {message}" for message in land_messages if message)
        if brothel_messages:
            lines.extend(f" {message}" for message in brothel_messages if message)
        return lines

    def _build_main_menu_items_panel_lines(self) -> List[str]:
        lines: List[str] = []
        player = self._get_player()
        if player is None:
            return [" 没有可显示的魔王数据。"]

        knowledge_names = []
        for talent_id, label in ((55, "调合知识"), (325, "魔界知识"), (327, "淫魔知识"), (328, "魔虫知识")):
            if player.talent.get(talent_id, 0):
                knowledge_names.append(label)
        knowledge_text = " / ".join(knowledge_names) if knowledge_names else "无"
        lines.append(f" 技巧Lv: {player.abl.get(12, 0)}")
        lines.append(f" 所持知识: {knowledge_text}")

        item_groups = [
            self._get_owned_catalog_item_ids([item_id for item_id in range(0, 59) if item_id in self.item_catalog]),
            self._get_owned_catalog_item_ids(([91] if 91 in self.item_catalog else []) + [item_id for item_id in range(300, 340) if item_id in self.item_catalog]),
        ]
        for group in item_groups:
            if not group:
                continue
            group_lines: List[str] = []
            for item_id in group:
                group_lines.append(f"{self._get_item_name(item_id)}({self._get_item_count(player, item_id)})")
            for start in range(0, len(group_lines), 5):
                lines.append("  " + "  ".join(group_lines[start:start + 5]))
        if len(lines) <= 2:
            lines.append(" 当前没有常规道具或装备。")
        return lines

    def _build_main_menu_panel_lines(self) -> List[str]:
        mode = self._get_main_menu_panel_mode()
        if mode == 1:
            return self._build_main_menu_traps_panel_lines()
        if mode == 4:
            return self._build_main_menu_dungeon_overview_lines()
        if mode == 5:
            return self._build_main_menu_daily_panel_lines()
        return self._build_main_menu_items_panel_lines()

    def _build_main_menu_target_assistant_lines(self) -> List[str]:
        lines: List[str] = []
        target = self._get_target()
        assi_idx = self.interpreter.vars.assi
        assistant = self.interpreter.vars.chars[assi_idx] if 0 <= assi_idx < len(self.interpreter.vars.chars) else None
        target_label = target.name if target is not None and self.interpreter.vars.target > 0 else "未选择"
        assistant_label = assistant.name if assistant is not None and assi_idx > 0 else "未选择"
        lines.append(f" [496] 调教目标: {target_label}")
        lines.append(f" [497] 助手: {assistant_label}")
        if target is not None and self.interpreter.vars.target > 0:
            lines.append(f" [498] 查看目标详情: {target.name}")
        if assistant is not None and assi_idx > 0:
            lines.append(f" [499] 查看助手详情: {assistant.name}")
        return lines

    def _build_main_menu_traps_panel_lines(self) -> List[str]:
        player = self._get_player()
        if player is None:
            return [" 没有可显示的陷阱数据。"]
        trap_ids = self._get_owned_catalog_item_ids([item_id for item_id in range(59, 90) if item_id in self.item_catalog])
        if not trap_ids:
            return [" 当前没有持有陷阱。"]
        lines: List[str] = []
        trap_lines = [f"{self._get_item_name(item_id)}({self._get_item_count(player, item_id)})" for item_id in trap_ids]
        for start in range(0, len(trap_lines), 5):
            lines.append("  " + "  ".join(trap_lines[start:start + 5]))
        return lines

    def _build_meat_toilet_overview_lines(self) -> List[str]:
        count = self.interpreter.vars.get_flag(83, 0)
        if count <= 0:
            return ["还没放置过肉便器。"]
        seed_type = self.interpreter.vars.get_flag(613, 0)
        hide_records = self._get_flag_bit(614, 0)
        auto_sell_children = self._get_flag_bit(614, 1)
        return [
            f"地下城内现在有 {count} 台肉便器。",
            f"播种者：{self._get_meat_toilet_seed_name(seed_type)}",
            f"人类牧场记录：{'不显示' if hide_records else '显示'}",
            f"卖掉产出的孩子：{'出售' if auto_sell_children else '不出售'}",
        ]

    def _build_reincarnation_candidates(self, target: Character) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        level = self._get_character_level(target)
        current_race = target.talent.get(322, 0)
        for group in self._get_reincarnation_groups():
            group_id = int(group["group_id"])
            for slot, monster_id in enumerate(group["monster_ids"]):
                if monster_id == current_race:
                    continue
                required_level = max(int(group.get("required_level", 0)), int(self._get_item_definition(monster_id).get("price", 0) // 20) if self._get_item_definition(monster_id) else 0)
                required_talents = [int(talent_id) for talent_id in group["required_talents"]]
                missing = [talent_id for talent_id in required_talents if not target.talent.get(talent_id, 0)]
                candidates.append({
                    "menu_id": group_id * 10 + slot,
                    "group_id": group_id,
                    "monster_id": monster_id,
                    "name": self._get_item_name(monster_id),
                    "required_level": required_level,
                    "required_talents": required_talents,
                    "missing_talents": missing,
                    "available": level >= required_level and not missing,
                })
        return candidates

    def _build_sabbath_day_former_goddess_label(self, target: Character, former_life: int) -> str:
        if int(target.talent.get(250, 0)):
            return "向潜藏地底的死亡女神"
        if int(target.talent.get(242, 0)):
            return "向纯洁的神圣女神"
        if former_life == 11:
            return "向丰饶的大地女神"
        if former_life == 12:
            return "向包容一切的大海女神"
        return ""

    def _build_sex_stimulation_gain(self, actor: Character, receiver: Character) -> int:
        gain = self._level_value(receiver.abl.get(12, 0), [50, 300, 800, 1500, 2000, 3200])
        gain = self._scale_value(gain, self._level_value(receiver.abl.get(10, 0), [80, 90, 100, 110, 120, 130]) / 100.0)
        gain = self._scale_value(gain, self._level_value(receiver.abl.get(14, 0), [50, 80, 120, 150, 180, 240]) / 100.0)
        gain = self._scale_value(gain, self._level_value(actor.abl.get(0, 0), [100, 150, 200, 250, 350, 500]) / 100.0)
        return gain

    def _build_stage_lines(self, stage: int, mapping: Dict[int, List[str]]) -> List[str]:
        return list(mapping.get(stage, []))

    def _build_story_branch_prompt(self, branch_name: str, accept_text: str, reject_text: str) -> List[str]:
        return [
            f"要进入{branch_name}吗？（剧情选择是不可逆的，选择之后就无法进入其它人的故事线了）",
            f" [1] {accept_text}",
            f" [2] {reject_text}",
            " [3] 让我先存个档",
        ]

    def _build_trap_shop_groups(self) -> List[Dict[str, Union[str, List[int]]]]:
        player = self._get_player()
        trap_items = [60, 61, 62, 63, 69, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86]
        knowledge_succubus = player is not None and bool(player.talent.get(327, 0))
        knowledge_bug = player is not None and bool(player.talent.get(328, 0))
        if knowledge_succubus:
            trap_items.extend([64, 65, 66, 67, 68, 70, 71, 79])
        else:
            trap_items.append(54)
        if not knowledge_bug:
            trap_items.append(56)
        else:
            trap_items.extend([65, 79, 80])
        trap_items = [item_id for item_id in sorted(set(trap_items)) if item_id in self.item_catalog]
        trap_groups: List[Dict[str, Union[str, List[int]]]] = [{"title": "陷阱", "items": trap_items}]
        if 91 in self.item_catalog:
            trap_groups.append({"title": "戒指", "items": [91]})
        if 55 in self.item_catalog and player is not None and self.interpreter.vars.get_flag(85, 0) < player.cflag.get(9, 0):
            trap_groups.append({"title": "陷阱强化", "items": [55]})
        return trap_groups

    def _build_turn_end_heat_body_fluid_message(self, target: Character) -> str:
        parts: List[str] = []
        if int(target.talent.get(122, 0)) != 0 or int(target.talent.get(121, 0)) != 0:
            parts.append("龟头")
        if int(target.talent.get(121, 0)) != 0:
            parts.append("私处")
        elif int(target.talent.get(122, 0)) == 0:
            parts.append("私处")
        return f"{target.name} 的{'和'.join(parts)}总是有透明的爱液滚滚涌出……"

    def _choose_alive_character(self, allow_master: bool = True, assistant_only: bool = False) -> Optional[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if char.base.get(0, 0) < 1:
                continue
            if not allow_master and idx == 0:
                continue
            if assistant_only and char.cflag.get(0, 0) < 2:
                continue
            candidates.append((idx, char))
        if not candidates:
            return None
        print("\n请选择对象：")
        for idx, char in candidates:
            print(f" [{idx}] {char.name}")
        print(" [999] Back")
        choice = self._prompt_choice()
        if choice == "999":
            return None
        try:
            selected = int(choice)
        except ValueError:
            return None
        return next(((idx, char) for idx, char in candidates if idx == selected), None)

    def _choose_birth_child_template_id(self, mother: Character, father_source: int) -> Optional[int]:
        human_template_ids = self._get_available_human_birth_template_ids()
        if not human_template_ids:
            return None
        mother_template_id = self._get_character_template_id(mother)
        if father_source == 1:
            normalized = self._normalize_birth_template_id(mother_template_id)
            if normalized is not None:
                return normalized
            generic_ids = [template_id for template_id in range(1, 17) if template_id in human_template_ids]
            if generic_ids:
                return random.choice(generic_ids)
            return random.choice(human_template_ids)
        if father_source in (2, 3):
            normalized = self._normalize_birth_template_id(mother_template_id)
            if normalized is not None:
                return normalized
            return random.choice([template_id for template_id in range(1, 17) if template_id in human_template_ids])
        if father_source in (4, 7):
            normalized = self._normalize_birth_template_id(mother_template_id)
            if normalized is not None:
                return normalized
            return random.choice([template_id for template_id in range(1, 17) if template_id in human_template_ids])
        if mother_template_id in human_template_ids:
            return mother_template_id
        return random.choice(human_template_ids)

    def _choose_block_feeling_part(self, target: Character) -> Optional[int]:
        part_options = [
            (0, "阴核感觉", 101, 0),
            (1, "私处感觉", 103, 2),
            (2, "肛门感觉", 105, 3),
            (3, "乳房感觉", 107, 1),
        ]
        print(f"\n封锁 {target.name} 哪个部位？")
        for part_id, label, talent_id, abl_id in part_options:
            locked = bool(target.talent.get(talent_id, 0) & 2)
            note = " 已经封锁" if locked else ""
            print(f" [{part_id}] {label}{note}")
        print(" [9] 重新选择角色")
        print(" [999] 取消")
        choice = self._prompt_choice()
        if choice == "999":
            return None
        if choice == "9":
            return -1
        try:
            selected = int(choice)
        except ValueError:
            return None
        return selected if selected in (0, 1, 2, 3) else None

    def _choose_equipment_enhancement(self) -> Optional[int]:
        max_affordable = self.interpreter.vars.money // 10000
        if max_affordable > 10:
            max_affordable = 10
        options = self._get_equipment_enhance_options(max_affordable)
        print("\n可选强化等级: " + " ".join(f"[{value}]" for value in options))
        print(" [999] 返回")
        return self._prompt_choice_int_in_options(options)

    def _choose_life_cradle_template(self) -> Optional[Dict[str, Any]]:
        templates = self._build_life_cradle_templates()
        if not templates:
            return None
        print("\n【生命摇篮】")
        print("-" * 30)
        for template in templates:
            hp = template["character"].maxbase.get(0, 0)
            mp = template["character"].maxbase.get(1, 0)
            print(f" [{template['id']}] {template['category']} {template['name']} HP {hp} MP {mp}")
        print(" [999] Back")
        choice = self._prompt_choice()
        if choice == "999":
            return None
        try:
            template_id = int(choice)
        except ValueError:
            return None
        return next((template for template in templates if int(template["id"]) == template_id), None)

    def _choose_reincarnation_candidate(self, target: Character) -> Optional[Dict[str, Any]]:
        candidates = self._build_reincarnation_candidates(target)
        if not candidates:
            return None

        print("\n可转生的魔族：")
        print("-" * 30)
        for candidate in candidates:
            req_names = self._get_reincarnation_required_talent_names(int(candidate["group_id"]))
            req_text = ""
            if req_names:
                req_text = " / 条件:" + "、".join(req_names)
            status = "" if candidate["available"] else " [条件不足]"
            print(f" [{candidate['menu_id']:>3}] {candidate['name']} Lv{candidate['required_level']}{req_text}{status}")
        print(" [999] Back")

        choice = self._prompt_choice()
        if choice == "999":
            return None
        try:
            menu_id = int(choice)
        except ValueError:
            return None
        return next((candidate for candidate in candidates if int(candidate["menu_id"]) == menu_id), None)

    def _choose_select_item_target(self, candidates: List[tuple[int, Character]], choice: str, allow_master: bool = True) -> Optional[Character]:
        if choice == "100":
            return None
        try:
            selected = int(choice)
        except ValueError:
            print("Invalid selection.")
            return None

        for idx, char in candidates:
            if idx != selected:
                continue
            blocked_reason = self._can_select_item_target(idx, char, allow_master=allow_master)
            if blocked_reason is not None:
                print(blocked_reason)
                return None
            return char

        print("Invalid selection.")
        return None

    def _choose_threesome_mode(self) -> Optional[tuple[int, int]]:
        print("\n【3P 形式】")
        print(" [0] 私处和肛门一起插")
        print(" [1] 性交同时口交")
        print(" [2] 肛交同时口交")
        print(" [100] 取消")
        choice = self._prompt_choice()
        if choice == "100":
            return None
        if choice == "0":
            return 1, 2
        if choice == "1":
            return 1, 3
        if choice == "2":
            return 2, 3
        print("Invalid selection.")
        return None

    def _choose_weapon_prefix(self) -> Optional[int]:
        print("\n可以设定强化的前缀")
        prefix_names = {
            0: "无",
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
        for prefix_id, name in prefix_names.items():
            print(f" [{prefix_id}] {name}")
        print(" [999] 返回")
        return self._prompt_choice_int_in_options(list(prefix_names.keys()))

    def _format_ability_upgrade_costs(self, costs: Dict[int, int], cost_types: Optional[Dict[int, str]] = None) -> str:
        juel_names = {
            0: "阴蒂珠",
            1: "私处珠",
            2: "快V珠",
            4: "恭顺珠",
            5: "欲情珠",
            6: "屈服珠",
            7: "习得珠",
            8: "耻情珠",
            10: "恐怖珠",
            11: "露出珠",
            14: "快B珠",
            15: "自由珠",
        }
        exp_names = {
            0: "V经验",
            1: "A经验",
            20: "精液经验",
            30: "苦痛经验",
            40: "百合经验",
            41: "断背经验",
            50: "异常经验",
            56: "兽奸经验",
            73: "调教会话经验",
            74: "卖淫经验",
        }
        parts = []
        for idx, value in costs.items():
            resource_type = (cost_types or {}).get(idx, "juel")
            if resource_type == "exp":
                name = exp_names.get(idx, f"EXP:{idx}")
            else:
                name = juel_names.get(idx, f"JUEL:{idx}")
            parts.append(f"{name}:{value}")
        return ", ".join(parts)

    def _format_autotrain(self, target: Character) -> None:
        """自动调教前格式化 - 对应 @FORMAT_AUTOTRAIN
        射精フラグ、BASE、LOSEBASE、TFLAG、PALAM等のリセット
        """
        v = self.interpreter.vars
        player = self._get_player()

        if player is not None:
            player.base[2] = 0
        target.base[2] = 0
        target.base[3] = 0
        if player is not None:
            player.base[4] = 0

        target.losebase[0] = 0
        target.losebase[1] = 0

        for i in range(200):
            v.tflag[i] = 0

        for i in range(17):
            target.palam[i] = 0

        self._before_autotrain(target)

        if int(target.talent.get(271, 0)):
            target.palam[3] = 3000
            target.palam[5] = 3000

        v.tflag[402] = 0

    def _format_character_body_measurement(self, value: int, metric: str) -> str:
        value = max(0, int(value))
        if value <= 0:
            return "0"
        legacy_thresholds = {
            "height": 300,
            "weight": 200,
            "bust": 300,
            "waist": 300,
            "hip": 300,
        }
        if value >= legacy_thresholds.get(metric, 300):
            whole = value // 10
            frac = value % 10
            return f"{whole}.{frac}"
        return str(value)

    def _format_day_text(self) -> str:
        year, month, day = self.interpreter.vars.day[:3]
        return f"Y{year} M{month} D{day}"

    def _format_life_cradle_field_value(self, talent_id: int, value: int) -> str:
        if talent_id in {300, 301, 303, 304, 305, 306, 307, 309, 312, 313, 315, 316, 317, 319}:
            return f"{self._get_talent_name(talent_id)}:{value}"
        if talent_id == 302:
            if value <= 2:
                return "短"
            if value <= 102:
                return "半长"
            return "长"
        if talent_id == 308:
            if value <= 2:
                return "纤细"
            if value <= 102:
                return "标准"
            return "丰满"
        if talent_id == 310:
            if value == 1:
                return "白虎"
            if value <= 20:
                return "胎毛"
            if value <= 50:
                return "新长的"
            if value <= 100:
                return "稀薄"
            if value <= 150:
                return "标准"
            if value <= 200:
                return "浓密"
            return "硬毛"
        if talent_id == 314:
            return f"种族{value}"
        return str(value)

    def _format_progress_bar(self, value: int, maximum: int = 10000, width: int = 20) -> str:
        maximum = max(1, maximum)
        clamped = max(0, min(value, maximum))
        filled = int(clamped * width / maximum)
        return "[" + "#" * filled + "-" * (width - filled) + f"] {clamped}/{maximum}"

    def _format_spawned_hero_entry_message(self, hero: Character, origin: str = "standard", prefix: Optional[str] = None) -> str:
        parts: List[str] = []
        if prefix:
            parts.append(prefix)
        if origin == "maounet":
            parts.append("异国的")
        if hero.talent.get(1000, 0):
            parts.append("异界的")
        parts.append(self._get_spawned_hero_role_label(hero))
        origin_text = "".join(parts)
        if not origin_text:
            origin_text = "勇者"
        return f"{origin_text} {hero.name} 开始进攻地下城了。"

    def _prepare_ability_up_from_shop(self) -> bool:
        target = self._get_target()
        if self._can_open_ability_up_for_target(self.interpreter.vars.target, target) is None:
            return True
        if not self._select_ability_up_target_from_roster():
            return False
        target = self._get_target()
        if target is None:
            return False
        return (
            self._can_open_ability_up_slave_target(self.interpreter.vars.target, target) is None
            or self._can_open_ability_up_hero_target(self.interpreter.vars.target, target) is None
        )

    def _prepare_ability_up_menu(self) -> tuple[Optional[Character], List[int]]:
        target = self._get_target()
        blocked_reason = self._can_open_ability_up_for_target(self.interpreter.vars.target, target)
        if blocked_reason is not None:
            if not self._select_ability_up_target_from_roster():
                return None, []
            target = self._get_target()
            if target is None:
                return None, []

        ability_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 30, 31, 32, 33, 37, 39, 40]
        return target, ability_ids

    def _prepare_life_cradle_character(self, selected: Dict[str, Any]) -> Optional[Character]:
        new_char = self._instantiate_life_cradle_character(int(selected["id"]))
        if new_char is None:
            return None
        print("\n新建角色的性别是？")
        print(" [1] 男性")
        print(" [2] 女性")
        print(" [3] 扶她")
        gender = self._prompt_choice()
        if gender not in {"1", "2", "3"}:
            return None
        self._apply_life_cradle_gender(new_char, gender)
        return new_char

    def _prepare_purchase_catalog_item(self, item_id: int) -> Optional[Dict[str, Union[Character, int, str]]]:
        player = self._get_player()
        item_def = self._get_item_definition(item_id)
        if player is None or item_def is None:
            print("\nItem data is missing.")
            return None

        price = int(item_def["price"])
        item_name = str(item_def["name"])
        if self.interpreter.vars.money < price:
            print("\nYou do not have enough money.")
            return None

        return {
            "player": player,
            "price": price,
            "item_name": item_name,
            "mode": self._get_purchase_catalog_item_mode(item_id),
        }

    def _prepare_spawned_invading_hero(
        self,
        hero: Character,
        reset_import_level: bool = False,
        apply_base_level_bonus: bool = False,
        clamp_karma: bool = True,
        assign_spawn_position: bool = True,
        apply_initial_funds: bool = True,
    ):
        self._normalize_spawned_hero_identity(hero)
        self._apply_spawned_hero_template_overrides(hero)
        self._reset_invading_hero_runtime_state(hero, assign_spawn_position=assign_spawn_position)
        if reset_import_level:
            hero.cflag[9] = 1
            hero.exp[80] = 0
        if apply_base_level_bonus:
            self._apply_hero_base_level_bonus(hero)
        hero.base[0] = int(hero.maxbase.get(0, hero.base.get(0, 0)))
        hero.base[1] = int(hero.maxbase.get(1, hero.base.get(1, 0)))
        if clamp_karma and int(hero.cflag.get(151, 0)) < -100:
            hero.cflag[151] = -100
        if apply_initial_funds:
            self._initialize_spawned_hero_party_funds(hero)

    def _prepare_training_assistant(self, target_idx: int) -> None:
        self.interpreter.vars.assi = -1
        if not self._has_assistable_candidates(exclude_idx=target_idx):
            return
        selected_assistant = self._select_assistant_from_roster()
        if selected_assistant == -2:
            self.interpreter.vars.assi = -1
            return
        self.interpreter.vars.assi = selected_assistant
        if self.interpreter.vars.assi == self.interpreter.vars.target:
            self.interpreter.vars.assi = -1

    def _prepare_training_from_shop(self) -> tuple[bool, bool]:
        blocked_reason = self._can_start_training_from_shop()
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            self._pause()
            return False, False

        target_idx = self.interpreter.vars.target
        target = self._get_target()
        if not self._ensure_training_target(target_idx, target):
            return False, False
        self._prepare_training_assistant(target_idx)
        if self.interpreter.vars.target <= 0:
            return False, False
        if self.interpreter.vars.target == self.interpreter.vars.assi:
            self.interpreter.vars.assi = -1
        return True, True
