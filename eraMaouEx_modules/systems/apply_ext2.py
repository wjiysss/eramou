from __future__ import annotations
"""Module for ApplyExt2Mixin - 效果应用"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ApplyExt2Mixin:
    """Mixin providing 效果应用 methods for GameEngine"""

    def _apply_aphrodisiac_target_fall(self, target: Character) -> None:
        target_name = target.name
        target.cflag[1] = 0
        money_gain = 100 * int(target.cflag.get(9, 0))
        self._add_global_money(money_gain)
        target.cflag[506] = 1
        target.cflag[507] = 0
        target_idx = self._find_character_index(target)
        self._remove_character_from_party(target_idx)
        print(f"{target_name}为了获得媚药，诱惑着魔王军上下人众。")
        print("流下了贪欲的口水，完全忘记了作为勇者的使命。")
        print(f"{target_name}陷落了。")
        print(f"获得{money_gain}G！")
        return

    def _apply_auto_buying(self) -> List[str]:
        player = self._get_player()
        if player is None:
            return []

        messages: List[str] = []
        auto_flags = int(self.interpreter.vars.get_flag(34, 0))

        if auto_flags & 1 and self.interpreter.vars.money >= 200 and self._get_item_count(player, 25) == 0:
            self._add_item(player, self._get_item_name(25), 1)
            self._spend_global_money(200)
            messages.append("自动购买补充了 1 个润滑液。")

        if auto_flags & 2 and self.interpreter.vars.money >= 500 and self._get_item_count(player, 6) > 0 and self._get_item_count(player, 28) == 0:
            self._add_item(player, self._get_item_name(28), 1)
            self._spend_global_money(500)
            messages.append("自动购买补充了 1 盘录像带。")

        if auto_flags & 8:
            bought = 0
            while self.interpreter.vars.money >= 100 and self._get_item_count(player, 24) < 10:
                self._add_item(player, self._get_item_name(24), 1)
                self._spend_global_money(100)
                bought += 1
            if bought > 0:
                messages.append(f"自动购买补充了 {bought} 个安全套。")

        return messages

    def _apply_conquest_random_candidate_style(self, target: Character, hair_color: Optional[int] = None, personality_id: Optional[int] = None):
        selected_personality = personality_id if personality_id in self._get_conquest_random_personality_ids() else random.choice(self._get_conquest_random_personality_ids())
        for talent_id in [160, 161, 162, 163, 164, 166, 172, 173, 174]:
            target.talent[talent_id] = 1 if talent_id == selected_personality else 0
        selected_hair = hair_color if hair_color in self._get_conquest_random_hair_colors() else random.choice(self._get_conquest_random_hair_colors())
        target.talent[300] = selected_hair

    def _apply_data_fix(self) -> None:
        """存档数据修复 - 对应 ERB/DATA_FIX.ERB
        加载存档后执行数据迁移和修复
        """
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []

        for idx, char in enumerate(chars):
            # 魔王高贵标识
            if idx == 0:
                if hasattr(char, 'ex_talent'):
                    char.ex_talent[200] = 1

            # 来历修复补丁
            if char.talent.get(315, 0) > 999:
                char.talent[315] = char.talent[315] % 1000 + 90

            # 理由修复补丁
            if char.talent.get(316, 0) > 999:
                char.talent[316] = char.talent[316] % 1000 + 90

            # 菲娅修正补丁 (NO:35)
            if hasattr(char, 'no') and char.no == 35:
                char.talent[174] = 0
                char.talent[179] = 1

            # 最大体力/气力下限
            if char.maxbase.get(0, 0) < 600:
                char.maxbase[0] = 600
            if char.maxbase.get(1, 0) < 100:
                char.maxbase[1] = 100

            # EX口上素质转移
            if hasattr(char, 'no'):
                if char.no == 31:
                    char.talent[175] = 0
                    if hasattr(char, 'ex_talent'):
                        char.ex_talent[101] = 1
                elif char.no == 32:
                    char.talent[176] = 0
                    if hasattr(char, 'ex_talent'):
                        char.ex_talent[102] = 1
                elif char.no == 33:
                    char.talent[177] = 0
                    if hasattr(char, 'ex_talent'):
                        char.ex_talent[103] = 1
                elif char.no == 35:
                    char.talent[179] = 0
                    if hasattr(char, 'ex_talent'):
                        char.ex_talent[104] = 1

            # EX技能转移
            if hasattr(char, 'ex_talent'):
                if char.talent.get(265, 0):
                    char.talent[265] = 0
                    char.ex_talent[801] = 1
                for count in range(266, 270):
                    if char.talent.get(count, 0):
                        char.talent[count] = 0
                        local = count - 265 + 900
                        char.ex_talent[local] = 1

            # 近卫和后代素质转移
            if hasattr(char, 'ex_talent'):
                for count in range(221, 223):
                    if char.talent.get(count, 0):
                        char.talent[count] = 0
                        local = count - 220
                        char.ex_talent[local] = 1

            # CFLAG转移
            if hasattr(char, 'ex_cflag'):
                if char.cflag.get(800, 0):
                    char.ex_cflag[99] = char.cflag[800]
                    char.cflag[800] = 0

        # FLAG转移
        if hasattr(v, 'ex_flag'):
            if v.ex_flag.get(99, 0) <= 0 and v.flag.get(99, 0) > 0:
                v.ex_flag[99] = v.flag[99]
                v.flag[99] = 0

            for count in range(1000, 10000):
                if v.ex_flag.get(count, 0) == 0:
                    v.ex_flag[count] = v.flag.get(count, 0)
                if count in v.flag:
                    v.flag[count] = 0

        # 声望初始化
        if hasattr(v, 'ex_flag'):
            if v.flag.get(99, 0) <= 0 and v.ex_flag.get(99, 0) <= 0:
                v.ex_flag[99] = 70

        # 菲娅淫乱线剧情节点修复
        if v.flag.get(2807, 0) == 1400:
            v.flag[2807] = 140

    def _apply_equip_powerup(self, result: Dict[str, Any], target: Character):
        """Apply character talent-based equipment powerups.
        Corresponds to ERB @EQUIP_POWERUP.
        """
        # 初心者
        if target.talent.get(291, 0) == 1:
            result["damage"] = result.get("damage", 0) - 10
            result["miss"] = result.get("miss", 0) + 10

        # 恶魔尾巴
        if target.talent.get(246, 0) == 1:
            result["damage"] = result.get("damage", 0) + 10

        # 恶魔目
        if target.talent.get(247, 0) == 1:
            result["spirit_dmg"] = result.get("spirit_dmg", 100) + 10

        # 独眼
        if target.talent.get(259, 0) == 1:
            result["damage"] = result.get("damage", 0) + 10
            result["miss"] = result.get("miss", 0) + 10

        # 额头天眼
        if target.talent.get(260, 0) == 1:
            result["spirit_dmg"] = result.get("spirit_dmg", 100) + 10
            result["spirit_recover"] = result.get("spirit_recover", 0) - 10

        # 角
        if target.talent.get(264, 0) == 1:
            result["damage"] = result.get("damage", 0) + 10
            result["spirit_recover"] = result.get("spirit_recover", 0) - 10

        # 精灵族弓连击加成
        base_code = result.get("base_code", 0)
        if base_code == 45 and target.talent.get(314, 0) == 1:
            result["combo"] = result.get("combo", 0) + 10

        # 天使族气力恢复
        if target.talent.get(314, 0) == 6:
            result["spirit_recover"] = result.get("spirit_recover", 0) + 10

        # 暗精灵气力伤害
        if target.talent.get(314, 0) == 7:
            result["spirit_dmg"] = result.get("spirit_dmg", 100) + 10

        # 堕天使连击
        if target.talent.get(314, 0) == 8:
            result["combo"] = result.get("combo", 0) + 10

        # 魔族防御伤害
        if target.talent.get(314, 0) == 9:
            result["def_dmg"] = result.get("def_dmg", 100) + 10

        # 能力者效果
        special = result.get("special", 0)
        if target.talent.get(275, 0):  # 火之能力者
            if special & 2:
                result["damage"] = result.get("damage", 0) + 10
            else:
                result["special"] = special | 2
                special = result["special"]

        if target.talent.get(276, 0):  # 冰之能力者
            if special & 4:
                result["combo"] = result.get("combo", 0) + 10
            else:
                result["special"] = result.get("special", 0) | 4

        if target.talent.get(277, 0):  # 雷之能力者
            if special & 8:
                result["combo"] = result.get("combo", 0) + 5
                result["damage"] = result.get("damage", 0) + 5
            else:
                result["special"] = result.get("special", 0) | 8

        if target.talent.get(278, 0):  # 光之能力者
            if result.get("spirit_recover", 0) > 0:
                result["combo"] = result.get("combo", 0) + 5
                result["damage"] = result.get("damage", 0) + 5
                result["spirit_recover"] = result.get("spirit_recover", 0) + 5
            else:
                result["spirit_recover"] = result.get("spirit_recover", 0) + 10

        if target.talent.get(279, 0):  # 暗之能力者
            if result.get("spirit_dmg", 100) > 100:
                result["combo"] = result.get("combo", 0) + 5
                result["damage"] = result.get("damage", 0) + 5
                result["spirit_dmg"] = result.get("spirit_dmg", 100) + 5
            else:
                result["spirit_dmg"] = result.get("spirit_dmg", 100) + 10

    def _apply_equipment_upgrade(self, target: Character, slot_flag: int, is_weapon: bool) -> tuple[bool, str]:
        current_code = int(target.cflag.get(slot_flag, -1))
        if current_code < 0:
            return False, "当前没有可强化的装备。"
        enhance = self._choose_equipment_enhancement()
        if enhance is None:
            return False, "已取消。"
        if enhance <= 0:
            return True, "未进行强化。"
        cost = enhance * 10000
        if self.interpreter.vars.money < cost:
            return False, "钱不够！！"
        base_code, current_plus, prefix = self._decode_equipment_code(current_code)
        if current_plus >= 10:
            return False, "当前装备已经强化到上限。"
        actual_gain = min(enhance, 10 - current_plus)
        self._spend_global_money(actual_gain * 10000)
        target.cflag[slot_flag] = self._encode_equipment_code(base_code, current_plus + actual_gain, prefix)
        name = self._get_equipment_weapon_name(target.cflag[slot_flag]) if is_weapon else self._get_equipment_ring_name(target.cflag[slot_flag])
        return True, f"{target.name} 的装备强化完成：{name}"

    def _apply_experience_item(self, item_id: int, quantity: int = 1) -> bool:
        if item_id != 53:
            return False
        target = self._select_item_target()
        if target is None:
            return False
        gain = 10 * max(1, quantity)
        target.exp[80] = int(target.exp.get(80, 0)) + gain
        print(f"\n{target.name} 获得了 {gain} 点经验值。")
        return True

    def _apply_futanari_transformation_prompt(self, target: Character) -> List[str]:
        messages = ["（呃…这是什么？）"]
        while True:
            print(f"{target.name}要【扶她化】吗？")
            print(" [0] - 好的")
            print(" [1] - 不要")
            choice = self._prompt_choice()
            if choice == "0":
                target.talent[326] = 0
                target.talent[121] = 1
                target.talent[1] = 1
                messages.append(f"{target.name}获得了【扶她化】。")
                return messages
            if choice == "1":
                target.talent[326] = 0
                messages.append(f"{target.name}失去了【扶她化】。")
                return messages

    def _apply_generated_character_body_profile(self, char: Character, profile: Dict[int, int], overwrite_existing: bool = True) -> None:
        for key, value in profile.items():
            if overwrite_existing or int(char.cflag.get(key, 0)) <= 0:
                char.cflag[key] = int(value)

    def _apply_hero_base_level_bonus(self, hero: Character):
        base_bonus = max(0, int(self.interpreter.vars.get_flag(60, 0)))
        if base_bonus <= 0:
            return
        for _ in range(base_bonus):
            self._apply_single_level_up(-1, hero)

    def _apply_ikai_bonus(self, char, floor: int) -> List[str]:
        """异界奖励 - 对应 @IKAI_BONUS
        根据异界探索层数给予角色奖励
        """
        messages: List[str] = []

        # 异界综合征刻印检查 - 对应 @IKAI_SOURCE_CHECK
        ikai_mark = int(char.mark.get(10, 0))
        if ikai_mark <= 0:
            messages.append(f"{char.name} 没有异界异常反应，无法获得异界奖励。")
            return messages

        # 根据异界综合征等级计算源倍率 Y
        # MARK:10 == 5 → Y=60, 4 → Y=70, 3 → Y=80, 2 → Y=90, 1 → Y=95
        y_multiplier_map = {5: 60, 4: 70, 3: 80, 2: 90, 1: 95}
        y_multiplier = y_multiplier_map.get(ikai_mark, 100)

        # Y:0 ~ Y:5 均设为 100（百分比基准）
        # y_sub = [100] * 6  # 预留给子倍率使用

        # 金钱奖励：基础金额 × 层数系数
        # 基础金额根据异界综合征等级决定，与 @DECIDE_ABLUP100 中异界点数消耗对应
        base_money_map = {1: 2000, 2: 5000, 3: 15000, 4: 30000, 5: 50000}
        base_money = base_money_map.get(ikai_mark, 1000)

        # 层数系数：每层增加 10%，最低 1 层
        floor_factor = 1.0 + (max(1, floor) - 1) * 0.1

        # 综合倍率 = y_multiplier / 100（异界综合征越严重，奖励越少）
        ikai_factor = y_multiplier / 100.0

        money_reward = int(base_money * floor_factor * ikai_factor)
        if money_reward > 0:
            self._add_global_money(money_reward)
            messages.append(f"获得金钱 {money_reward}。")

        # 经验奖励：异界点数 (EXP:99) 按层数增加
        # 对应 @DECIDE_ABLUP100 中异界点数的消耗逻辑
        exp_reward = int(floor * 100 * ikai_factor)
        if exp_reward > 0:
            char.exp[99] = char.exp.get(99, 0) + exp_reward
            messages.append(f"异界点数 +{exp_reward}。")

        # 勋章经验奖励 (EXP:81) 按层数增加
        medal_reward = max(1, floor // 3)
        if medal_reward > 0:
            char.exp[81] = char.exp.get(81, 0) + medal_reward
            messages.append(f"勋章经验 +{medal_reward}。")

        # 特定层数给予特殊奖励
        if floor >= 9:
            # 第9层：魔王领域，获得特殊素质
            if not char.talent.get(1000, 0):
                char.talent[1000] = 1
                messages.append(f"{char.name} 获得了【{self._get_talent_name(1000)}】。")
        elif floor >= 6:
            # 第6层：深层区域，异界综合征加深
            if ikai_mark < 5:
                char.mark[10] = ikai_mark + 1
                messages.append(f"{char.name} 的异界综合征加深为 Lv{ikai_mark + 1}。")
        elif floor >= 3:
            # 第3层：中层区域，战斗等级提升
            combat_level = int(char.cflag.get(9, 0))
            char.cflag[9] = combat_level + 1
            messages.append(f"{char.name} 的战斗等级提升为 Lv{combat_level + 1}。")

        # 运动能力奖励 - 对应 @IKAI_UNDOU_BONUS（预留）
        # 感性奖励 - 对应 @IKAI_KANSEI_BONUS（预留）
        # 学习能力奖励 - 对应 @IKAI_BENKYOU_BONUS（预留）
        # 战斗奖励 - 对应 @IKAI_SENTOU_BONUS（预留）

        return messages

    def _apply_knowledge_item(self, item_id: int) -> bool:
        player = self._get_player()
        if player is None:
            print("\nNo master character available.")
            return False

        item_name = self._get_item_name(item_id)
        if item_id == 38:
            player.talent[91] = 1
            print(f"\n{item_name} granted Love Dynamics knowledge.")
            return True
        if item_id == 39:
            player.talent[325] = 1
            print(f"\n{item_name} granted 魔界知识.")
            return True
        if item_id == 42:
            player.talent[55] = 1
            print(f"\n{item_name} granted 调合知识.")
            return True
        if item_id == 52:
            player.abl[12] = min(10, player.abl.get(12, 0) + 1)
            print(f"\n{item_name} raised 技巧 to Lv{player.abl[12]}.")
            return True
        if item_id == 54:
            player.talent[327] = 1
            print(f"\n{item_name} granted 淫魔知识.")
            return True
        if item_id == 56:
            player.talent[328] = 1
            print(f"\n{item_name} granted 魔虫知识.")
            return True
        return False

    def _apply_long_goodbye_after_sale(self, sold_idx: int, target: Character):
        sold_identity = int(self._get_character_identity_token(sold_idx, target))
        for idx, witness in enumerate(self.interpreter.vars.chars):
            if idx <= 0 or witness is target:
                continue
            stress = self._get_long_goodbye_bond_score(sold_identity, witness)
            if stress <= 50:
                continue
            self._show_long_goodbye_witness_reaction(witness, target)
            stress = self._adjust_long_goodbye_witness_stress(witness, stress)
            self._apply_long_goodbye_witness_breakdown(witness, stress)

    def _apply_long_goodbye_witness_breakdown(self, witness: Character, stress: int) -> None:
        if stress >= 100 and not witness.talent.get(9, 0):
            print(f"{witness.name} 呆呆地站在原地，心里似乎有什么东西坏掉了……")
            witness.talent[9] = 1
            if witness.talent.get(85, 0):
                witness.talent[85] = 0
            if witness.talent.get(76, 0):
                witness.talent[76] = 0

    def _apply_losebase_to_character(self, target: Character, losebase: Dict[int, int]) -> None:
        if int(losebase.get(0, 0)) != 0:
            target.base[0] = max(1, int(target.base.get(0, 0)) - int(losebase.get(0, 0)))
        if int(losebase.get(1, 0)) != 0:
            target.base[1] = max(0, int(target.base.get(1, 0)) - int(losebase.get(1, 0)))

    def _apply_love_corruption_swap_corruption_reset(self, target: Character, rule: Dict[str, Any], result_talent_id: int) -> None:
        if result_talent_id != 76:
            return
        global_flag = int(rule["global_flag"])
        current_value = int(self.interpreter.vars.get_flag(global_flag, 0))
        for start, end in rule["corruption_ranges"]:
            if start <= current_value <= end:
                self.interpreter.vars.set_flag(global_flag, int(rule["corruption_reset_to"]))
                target.cflag[int(rule["cflag_reset"])] = 0
                break

    def _apply_love_corruption_swap_love_reset(self, target: Character, rule: Dict[str, Any], result_talent_id: int) -> None:
        if result_talent_id != 85:
            return
        global_flag = int(rule["global_flag"])
        current_value = int(self.interpreter.vars.get_flag(global_flag, 0))
        start, end = rule["love_reset_range"]
        if start <= current_value <= end:
            self.interpreter.vars.set_flag(global_flag, int(rule["love_reset_to"]))
            target.cflag[int(rule["cflag_reset"])] = 0

    def _apply_love_corruption_swap_story_reset(self, target: Character, result_talent_id: int):
        template_id = int(target.cflag.get(190, 0))
        rule = self._get_love_corruption_swap_reset_rules().get(template_id)
        if rule is None:
            return

        self._apply_love_corruption_swap_love_reset(target, rule, result_talent_id)
        self._apply_love_corruption_swap_corruption_reset(target, rule, result_talent_id)

    def _apply_maou_candidate_refresh(self) -> List[str]:
        candidate_idx = self._select_maou_candidate()
        if candidate_idx is None:
            return []
        self.interpreter.vars.globals[3] = candidate_idx
        candidate = self.interpreter.vars.chars[candidate_idx]
        return [f"新的魔王候补被记录为 {candidate.name}。"]

    def _apply_mod_switch_entry(self, mod_id: int) -> tuple[bool, str]:
        entry = next((item for item in self._get_mod_switch_entries() if int(item["id"]) == mod_id), None)
        if entry is None:
            return False, "Invalid selection."
        enabled = self._toggle_flag_bit(9000, mod_id)
        return True, f"{entry['label']} 已切换为 {'ON' if enabled else 'OFF'}。"

    def _apply_omorashi_talent_award(self, target: Character) -> List[str]:
        messages = [f"当晚，{target.name} 尿床了…", f"{target.name} 获得了【{self._get_talent_name(57)}】。"]
        target.talent[57] = 1
        return messages

    def _apply_otherworld_hero_template(self, sex_choice: int, finalize: bool = True) -> tuple[bool, str]:
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            return False, "奴隶太多了！"

        cost_check = self._check_otherworld_hero_template_finalize_costs(finalize)
        if cost_check is not None:
            return cost_check

        new_char = self._create_otherworld_hero_template_character()
        if new_char is None:
            self._handle_otherworld_hero_template_missing_template(finalize)
            return False, "缺少异界勇者模板。"

        self._configure_otherworld_hero_template_character(new_char, sex_choice)

        if not finalize:
            sex_label = {1: "男性", 2: "女性", 3: "扶她"}.get(sex_choice, "女性")
            return True, f"{new_char.name} 回应了你的召唤。性别: {sex_label}。"

        return self._finalize_otherworld_hero_template_character(new_char, sex_choice)

    def _apply_palam_delta_to_character(self, target: Character, palam_delta: Dict[int, int]) -> None:
        for idx, value in palam_delta.items():
            if value:
                target.palam[idx] = target.palam.get(idx, 0) + value

    def _apply_plural_purchase_effect(self, item_id: int, quantity: int, item_name: str) -> Optional[bool]:
        if item_id == 53:
            return self._apply_experience_item(item_id, quantity=quantity)
        if item_id == 55:
            self.interpreter.vars.set_flag(85, self.interpreter.vars.get_flag(85, 0) + quantity)
            print(f"\n购买了{quantity}个{item_name}。陷阱等级上升到 Lv{self.interpreter.vars.get_flag(85, 0)}。")
            return True
        ring_message = self._apply_ring_bundle_item(item_id, quantity)
        if ring_message is not None:
            print(f"\n购买了{quantity}个{item_name}。{ring_message}")
            return True
        return None

    def _apply_post_new_day_economic_flows(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_tax_collection())
        self._decay_video_campaign()
        messages.extend(self._apply_maou_candidate_refresh())
        return messages

    def _apply_prefix_effects(self, result: Dict[str, Any], prefix: int):
        """Apply weapon prefix enchantment effects.
        Corresponds to ERB prefix section of @EQUIP_DATABASE.
        """
        if prefix == 1:  # 巨型
            result["damage"] = result.get("damage", 0) + 30
            result["miss"] = result.get("miss", 0) + 20
        elif prefix == 2:  # 剧毒
            result["special"] = result.get("special", 0) | 1
            result["damage"] = result.get("damage", 0) - 10
        elif prefix == 3:  # 致命
            result["damage"] = result.get("damage", 0) + 40
            result["spirit_recover"] = result.get("spirit_recover", 0) - 30
        elif prefix == 4:  # 强击
            result["damage"] = result.get("damage", 0) - 10
            result["combo"] = result.get("combo", 0) + 20
        elif prefix == 5:  # 烈火
            result["special"] = result.get("special", 0) | 2
            result["miss"] = result.get("miss", 0) + 10
        elif prefix == 6:  # 寒冰
            result["special"] = result.get("special", 0) | 4
            result["spirit_recover"] = result.get("spirit_recover", 0) - 10
        elif prefix == 7:  # 雷霆
            result["special"] = result.get("special", 0) | 8
            result["damage"] = result.get("damage", 0) + 20
            result["miss"] = result.get("miss", 0) + 10
            result["spirit_recover"] = result.get("spirit_recover", 0) - 10
        elif prefix == 8:  # 魔导
            result["damage"] = result.get("damage", 0) - 10
            result["spirit_recover"] = result.get("spirit_recover", 0) + 20
        elif prefix == 9:  # 暗黑
            result["spirit_recover"] = result.get("spirit_recover", 0) - 10
            result["spirit_dmg"] = result.get("spirit_dmg", 100) + 20

    def _apply_random_reincarnation_hair_color(self, target: Character) -> Optional[str]:
        if random.randint(0, 2) != 0:
            return None
        new_color = random.randint(1, 7)
        if int(target.talent.get(300, 0)) == new_color:
            return None
        previous = self._get_hair_color_name(int(target.talent.get(300, 0)))
        target.talent[300] = new_color
        current = self._get_hair_color_name(new_color)
        return f"{target.name} 的头发颜色从{previous}变成了{current}。"

    def _apply_random_talents_to_character(self, char: Character) -> None:
        """为角色应用随机素质"""
        # 基础素质
        basic_talents = [2, 3, 4, 10, 11, 12, 13, 14, 15, 16]
        for talent_id in basic_talents:
            if random.randint(0, 9) == 0:
                char.talent[talent_id] = 1

        # 特殊素质
        special_talents = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        for talent_id in special_talents:
            if random.randint(0, 19) == 0:
                char.talent[talent_id] = 1

    def _apply_reincarnation_bonus(self, target: Character, monster_name: str) -> List[str]:
        messages: List[str] = []
        if monster_name in {"狗头人", "丧尸猎犬", "地狱猎犬", "奇美拉", "梦魇"}:
            if self._grant_labo_talent_once(target, 124):
                messages.append(f"{target.name} 头上长出【动物耳】了。")
        elif monster_name in {"魅魔", "莉莉丝"}:
            if self._grant_labo_talent_once(target, 91):
                messages.append(f"{target.name} 的肉体上散发出致命的诱惑，获得了【魅惑】。")
        elif monster_name in {"小仙子", "小精灵"}:
            if self._grant_labo_talent_once(target, 263):
                messages.append(f"{target.name} 的身体缩小，变成了【小人体型】。")
        elif monster_name in {"黏液怪", "史莱姆"}:
            if self._grant_labo_talent_once(target, 261):
                messages.append(f"{target.name} 的身体变成了黏稠的【史莱姆】。")
        elif monster_name in {"食铠者", "食脑魔", "藤蔓怪", "吸血树"}:
            if self._grant_labo_talent_once(target, 262):
                messages.append(f"{target.name} 的身上长出了【触手】。")
        elif monster_name in {"女忍", "忍者"}:
            if self._grant_labo_talent_once(target, 251):
                messages.append(f"{target.name} 学会了隐藏在影子暗处，获得了【忍术】。")
        elif monster_name in {"男祭司", "女祭司"}:
            if self._grant_labo_talent_once(target, 242):
                messages.append(f"{target.name} 得到了邪神的眷顾，获得了【法术】。")
        elif monster_name in {"女巫", "男巫"}:
            if self._grant_labo_talent_once(target, 241):
                messages.append(f"{target.name} 学会了操控魔力，获得了【魔术】。")
        elif monster_name == "黑暗骑士":
            if self._grant_labo_talent_once(target, 240):
                messages.append(f"{target.name} 获得了暗黑之力，学会了【战术】。")
        return messages

    def _apply_resistance_mark_reduction(self, target: Character) -> tuple[bool, str]:
        reasons = self._get_resistance_mark_reduction_reasons(target)
        if reasons:
            return False, "；".join(reasons)
        cost = self._get_resistance_mark_reduction_cost(target)
        target.mark[3] = max(0, int(target.mark.get(3, 0)) - 1)
        self._consume_juel(6, cost)
        return True, f"反抗刻印下降为LV{target.mark.get(3, 0)}。"

    def _apply_rest_turn_end(self):
        print("\n【Rest】")
        print("你专心于内政，稍作了休息……（税金+5%）")
        self.interpreter.vars.set_flag(9, self.interpreter.vars.get_flag(9, 0) + 5)
        self.advance_time()
        self._pause()

    def _apply_ring_bundle_item(self, item_id: int, quantity: int) -> Optional[str]:
        if item_id != 91:
            return None
        player = self._get_player()
        if player is None:
            return None
        ring_name = self._get_item_name(300)
        current_count = self._get_item_count(player, 300)
        actual_gain = min(max(0, quantity), max(0, 99 - current_count))
        overflow = max(0, quantity - actual_gain)
        if actual_gain > 0:
            self._add_item(player, ring_name, actual_gain)
        if overflow > 0:
            refund = overflow * int(self._get_item_definition(91).get("price", 100))
            self._refund_shop_cost(refund)
            return f"已转为 {ring_name} x{actual_gain}，多余的 {overflow} 个戒指已退款。"
        return f"已转为 {ring_name} x{actual_gain}。"

    def _apply_ring_recovery_divider(self, value: int, target: Character, effect_id: int) -> int:
        strength = self._get_ring_effect_strength(target, effect_id)
        if strength <= 0:
            return value
        return value // (strength + 1)

    def _apply_ring_recovery_multiplier(self, value: int, target: Character, effect_id: int) -> int:
        strength = self._get_ring_effect_strength(target, effect_id)
        if strength <= 0:
            return value
        return value * (strength + 1)

    def _apply_running_cost(self) -> List[str]:
        difficulty = int(self.interpreter.vars.get_flag(5, 0))
        if difficulty == 9:
            return []
        total_days = self._get_total_day_count()
        if not ((difficulty == 1 and total_days >= 20) or (difficulty >= 2 and total_days >= 10)):
            return []
        amount = self._get_running_cost_amount()
        if amount <= 0:
            return []
        self._spend_global_money(amount)
        return [f"调教中心的维持费和奴隶们的生活费花了 ${amount}……"]

    def _apply_running_cost_difficulty_adjustments(self, cost: int, difficulty: int, total_days: int, char_count: int) -> int:
        bonus = RUNNING_COST_DIFFICULTY_BONUSES.get(difficulty, 0)
        cost += char_count * bonus
        cost -= 100

        for upper, multiplier in RUNNING_COST_DIFFICULTY_MULTIPLIERS.get(difficulty, []):
            if upper is None or total_days <= upper:
                return cost * multiplier // 100
        return cost

    def _apply_running_cost_player_adjustments(self, cost: int, player: Character) -> int:
        popularity = int(player.exp.get(91, 0))
        cost = self._apply_threshold_multipliers(cost, popularity, RUNNING_COST_POPULARITY_MULTIPLIERS)

        contribution = int(player.exp.get(90, 0))
        cost = self._apply_threshold_multipliers(cost, contribution, RUNNING_COST_CONTRIBUTION_MULTIPLIERS)
        return cost

    def _apply_selected_dress_option(self, target: Character, selected_option: Dict[str, Any]) -> None:
        ok, message = self._apply_dress_option(target, selected_option)
        print(f"\n{message}")
        self._pause()

    def _apply_shadow_servant_lifetime_decay(self) -> List[str]:
        messages: List[str] = []
        idx = 0
        while idx < len(self.interpreter.vars.chars):
            char = self.interpreter.vars.chars[idx]
            if not char.talent.get(292, 0):
                idx += 1
                continue
            self._ensure_shadow_servant_lifetime(char)
            if char.cflag.get(1, 0) == 11:
                idx += 1
                continue
            char.cflag[820] = self._get_shadow_servant_lifetime(char) - 1
            messages.append(f"{char.name} 的寿命还有 {char.cflag[820]} 天。")
            if char.cflag.get(820, 0) > 0:
                idx += 1
                continue
            messages.extend(self._expire_shadow_servant(idx, char))
            idx = 1
        return messages

    def _apply_single_level_up(self, idx: int, char: Character):
        char.cflag[9] = int(char.cflag.get(9, 0)) + 1
        self._apply_level_up_growth_pair(char, 1)
        self._apply_level_up_growth_pair(char, random.randrange(2))

        current_day = 0
        try:
            current_day = int(self._get_total_day_count())
        except Exception:
            current_day = 0
        if current_day >= 100:
            self._apply_level_up_random_growth(char, 3)
        self._apply_level_up_talent_growth(char, 240, 3)
        self._apply_level_up_talent_growth(char, 248, 2)
        if char.talent.get(314, 0) == 5:
            self._apply_level_up_random_growth(char, 2)
        if char.talent.get(314, 0) == 11:
            self._add_level_up_growth(char, 14, random.randrange(2))
        self._apply_level_up_talent_growth(char, 261, 2)
        self._apply_level_up_talent_growth(char, 262, 2)

        self._apply_level_up_maxbase_growth(char)

    def _apply_sometimes_she_comes_back(self) -> List[str]:
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if int(char.base.get(0, 0)) != 0:
                continue
            max_hp = max(1, int(char.maxbase.get(0, 1)))
            max_mp = max(0, int(char.maxbase.get(1, 0)))
            char.base[0] = max(1, max_hp // 10)
            char.base[1] = max_mp
            return [
                f"早上，你睁开双眼，发现确实已经死掉了的 {char.name} 就站在面前。",
                "哎呦我的妈！葱油炒蛋花！",
                f"{char.name} 好像什么事都没发生一样，循例进行了上午的请安。",
                f"{char.name} 回归了……",
            ]
        return []

    def _apply_soul_dislocation_source_debuff(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        level = self._get_character_ex_talent(target, 0)
        if level <= 0:
            return source
        factor = max(0, 100 - 15 * int(level))
        adjusted = dict(source)
        for idx in range(20):
            value = int(adjusted.get(idx, 0))
            if value == 0:
                continue
            adjusted[idx] = value * factor // 100
        return adjusted

    def _apply_source_to_character(self, target: Character, source: Dict[int, int]):
        for idx, value in source.items():
            if value:
                target.palam[idx] = target.palam.get(idx, 0) + value
                self._add_juel(idx, value)

    def _apply_spawned_hero_level_progression(self):
        if not self._is_hero_level_scaling_enabled():
            return
        current_level = max(0, int(self.interpreter.vars.get_flag(60, 0)))
        self.interpreter.vars.set_flag(60, current_level + 1)

    def _apply_spawned_hero_template_overrides(self, hero: Character):
        template_id = self._get_character_template_id(hero)
        if template_id == 24:
            hero.cflag[550] = 40
            return
        if template_id == 22:
            hero.cflag[550] = self._encode_equipment_code(40, 9, 9)
            hero.cflag[6] = random.randint(0, 79)
            return
        if template_id == 23:
            hero.abl[31] = max(1, int(hero.abl.get(31, 0)))
            hero.exp[10] = max(30, int(hero.exp.get(10, 0)))
            hero.cflag[550] = self._encode_equipment_code(41, 9, 6)
            hero.cflag[6] = random.randint(0, 79)
            return
        if template_id == 21:
            hero.exp[10] = max(10, int(hero.exp.get(10, 0)))
            hero.cflag[550] = self._encode_equipment_code(44, 9, 3)
            hero.cflag[6] = random.randint(0, 79)
            return
        if template_id == 20:
            hero.exp[0] = max(20, int(hero.exp.get(0, 0)))
            if int(self.interpreter.vars.get_flag(500, 0)) in (0, 2):
                hero.exp[5] = max(int(hero.exp.get(5, 0)), int(hero.exp.get(0, 0)))
            hero.cflag[15] = 105
            hero.cflag[550] = self._encode_equipment_code(50, 10, 4)
            hero.cflag[6] = random.randint(0, 79)

    def _apply_threshold_multipliers(self, cost: int, value: int, thresholds: List[tuple[int, int]]) -> int:
        for threshold, multiplier in thresholds:
            if value >= threshold:
                return cost * multiplier // 100
        return cost

    def _apply_turn_end_aftercare_cycle(self, campaign_active: bool) -> None:
        self._apply_turn_end_recovery(campaign_active)

    def _apply_turn_end_anal_master_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(233, 0)) != 0:
            return []
        if int(target.abl.get(3, 0)) < 5 or int(target.exp.get(32, 0)) < 300 or int(target.exp.get(2, 0)) < 300:
            return []
        target.talent[233] = 1
        return [
            f"{target.name} 用舌头轻轻地舔着嘴唇……",
            f"{target.name}在调教结束之后依然哀求着你疼爱她的尻穴。但一插进去，她便全身夸张地痉挛了起来，直肠疯狂地蠕动，摩擦着阴茎……",
            f"{target.name} 获得了【{self._get_talent_name(233)}】。",
        ]

    def _apply_turn_end_anomaly_events(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_treasure_vault_anomaly())
        messages.extend(self._apply_turn_end_overlevel_slave_anomaly())
        messages.extend(self._apply_turn_end_player_overflow_anomaly())
        return messages

    def _apply_turn_end_auto_buying(self) -> None:
        for message in self._apply_auto_buying():
            print(message)

    def _apply_turn_end_bitch_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(136, 0)) != 0:
            return []
        if int(target.abl.get(11, 0)) < 5 or int(target.abl.get(39, 0)) < 3 or int(target.exp.get(56, 0)) < 300:
            return []
        target.talent[136] = 1
        return [
            f"{target.name} 的行为彻底变化了……",
            "整天喜欢四脚爬爬地在地上爬行，一边扭腰抬臀，一边仰视着你。",
            "完全像是一只发春的牝犬一样。",
            f"{target.name} 获得了【{self._get_talent_name(136)}】。",
        ]

    def _apply_turn_end_bodyshift_forced_changes(self, target: Character) -> List[str]:
        if int(target.exp.get(62, 0)) < 20:
            return []
        if int(target.talent.get(158, 0)) != 0:
            return []
        target.talent[158] = 1
        return [
            f"{target.name} 生育了太多异种的孩子，已经无法为同族生育了。",
            f"{target.name} 获得了【{self._get_talent_name(158)}】。",
        ]

    def _apply_turn_end_breast_master_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(231, 0)) != 0:
            return []
        if int(target.abl.get(1, 0)) < 5 or int(target.exp.get(54, 0)) < 100 or int(target.exp.get(2, 0)) < 300:
            return []
        target.talent[231] = 1
        return [
            f"{target.name} 主动引导你的手推拿自己的胸部……",
            f"{target.name}在调教结束之后依然哀求着你玩弄她的胸部。但一摸下去，她便昂首咬牙，爱液四射，高声娇喘起来了……",
            f"{target.name} 获得了【{self._get_talent_name(231)}】。",
        ]

    def _apply_turn_end_character_state_post_cycle(self) -> None:
        messages = self._apply_new_day_character_state_post_flows()
        for message in messages:
            print(message)

    def _apply_turn_end_clitoris_master_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(230, 0)) != 0:
            return []
        if int(target.abl.get(0, 0)) < 5 or int(target.exp.get(11, 0)) < 100 or int(target.exp.get(2, 0)) < 300:
            return []
        target.talent[230] = 1
        relieve = "他缓解" if int(target.talent.get(122, 0)) != 0 else "她解除"
        organ = "阴茎的肿涨。" if int(target.talent.get(121, 0)) != 0 or int(target.talent.get(122, 0)) != 0 else "阴蒂的肿痛。"
        reaction = "他便喘息了起来，" if int(target.talent.get(122, 0)) != 0 else "她便高声娇喘起来，"
        talent_name = "绝伦" if int(target.talent.get(122, 0)) != 0 else self._get_talent_name(230)
        return [
            f"{target.name} 好像无法停止娇媚的呻吟，",
            f"{target.name}在调教结束之后依然哀求着你为{relieve}{organ}",
            f"但一摸下去，{reaction}越来越亢奋了……",
            f"{target.name} 获得了【{talent_name}】。",
        ]

    def _apply_turn_end_corruption_brown_skin(self, target: Character) -> None:
        if int(target.talent.get(244, 0)) != 0:
            return
        self._apply_labo_skin_color_selection(target, 2)

    def _apply_turn_end_corruption_race_fall(self, target: Character) -> List[str]:
        race_id = int(target.talent.get(314, 0))
        if race_id == 1:
            target.talent[314] = 7
            self._apply_turn_end_corruption_brown_skin(target)
            return [f"{target.name} 从高洁的精灵，堕落为卑微的肉壶了。"]
        if race_id == 6:
            target.talent[314] = 8
            self._apply_turn_end_corruption_brown_skin(target)
            return [f"{target.name} 纯洁的灵魂完全堕落了，成为了被淫靡欲望所支配的下等性奴隶。"]
        return []

    def _apply_turn_end_corruption_talent_cleanup(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._clear_turn_end_talents(target, [20, 21], halve_juel_100=True))
        messages.extend(self._clear_turn_end_talents(target, [27]))
        messages.extend(self._clear_turn_end_talents(target, [32, 34, 84], halve_juel_100=True))
        messages.extend(self._clear_turn_end_talents(target, [71, 150]))
        return messages

    def _apply_turn_end_corruption_talent_gain(self, target: Character) -> List[str]:
        target.talent[76] = 1
        self.interpreter.vars.set_flag(30, int(self.interpreter.vars.get_flag(30, 0)) + 1)
        messages = [
            f"{target.name} 看你的眼神，好像忘记了你还有上半身……",
            f"{target.name} 沉迷于你给予的快感之中了……",
            f"{target.name} 获得了【{self._get_talent_name(76)}】。",
        ]
        messages.extend(self._apply_turn_end_corruption_talent_cleanup(target))
        messages.extend(self._apply_turn_end_corruption_talent_side_effects(target))
        self._apply_love_corruption_swap_story_reset(target, 76)
        return messages

    def _apply_turn_end_corruption_talent_side_effects(self, target: Character) -> List[str]:
        messages: List[str] = []
        if int(target.talent.get(274, 0)) == 0:
            messages.extend(self._apply_turn_end_corruption_race_fall(target))
        messages.extend(self._apply_turn_end_shojo_seal_release_prompt(target))
        messages.extend(self._apply_turn_end_maou_ex_talent_award(target))
        return messages

    def _apply_turn_end_courtesan_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(181, 0)) != 0 or int(target.talent.get(180, 0)) == 0:
            return []
        if int(target.mark.get(3, 0)) != 0:
            return []
        prostitution_exp = int(target.exp.get(74, 0))
        if int(target.talent.get(315, 0)) == 5:
            if prostitution_exp < 160:
                return []
        elif prostitution_exp < 200:
            return []
        target.talent[181] = 1
        return [
            f"{target.name} 热衷于从事分开双腿的工作……",
            f"{target.name} 获得了【{self._get_talent_name(181)}】。",
        ]

    def _apply_turn_end_cycle(self, campaign_active: bool) -> None:
        self._apply_turn_end_production_cycle()
        self._apply_turn_end_aftercare_cycle(campaign_active)

    def _apply_turn_end_enhanced_sex_talent_checks(self, target: Character) -> List[str]:
        if int(self.interpreter.vars.get_flag(73, 0)) > 0:
            return []
        messages: List[str] = []
        messages.extend(self._apply_turn_end_clitoris_master_talent_gain(target))
        messages.extend(self._apply_turn_end_vagina_master_talent_gain(target))
        messages.extend(self._apply_turn_end_anal_master_talent_gain(target))
        messages.extend(self._apply_turn_end_breast_master_talent_gain(target))
        messages.extend(self._apply_turn_end_sex_hero_talent_gain(target))
        return messages

    def _apply_turn_end_exhibitionism_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(89, 0)) != 0:
            return []
        if int(target.abl.get(17, 0)) < 4 or int(target.abl.get(21, 0)) < 2:
            return []
        if int(target.exp.get(11, 0)) + int(target.exp.get(31, 0)) + int(target.exp.get(54, 0)) < 200:
            return []
        target.talent[89] = 1
        return [
            f"{target.name} 的神情变得害羞……",
            "但是，却学会了将这份羞耻变成快感。将自己的被羞辱的姿态呈现他人，令她感到身心无比圆满。",
            f"{target.name} 获得了【{self._get_talent_name(89)}】。",
        ]

    def _apply_turn_end_forced_semen_fetish_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(47, 0)) != 0:
            return []
        threshold = self._get_forced_semen_fetish_threshold(target)
        if int(target.cflag.get(600, 0)) < threshold:
            return []
        target.talent[47] = 1
        messages = [
            f"{target.name} 最近一见到你，就感到舌干唇燥……",
            f"{target.name} 在没有任何性刺激的情况下，也渴望着饮精液了。",
            f"{target.name} 获得了【{self._get_talent_name(47)}】。",
        ]
        messages.extend(self._clear_turn_end_talents(target, [62]))
        if int(target.abl.get(32, 0)) < 3:
            target.abl[32] = 3
            messages.append(f"{target.name} 的精液中毒LV3了。")
        return messages

    def _apply_turn_end_gladiator_talent_check(self, target: Character) -> List[str]:
        if int(target.talent.get(188, 0)) != 0:
            return []
        if int(target.exp.get(76, 0)) < 60:
            return []
        target.talent[188] = 1
        return [
            f"{target.name} 在死斗场获得了超绝的人气……",
            f"{target.name} 获得【{self._get_talent_name(188)}】了",
        ]

    def _apply_turn_end_heat_talent_checks(self, target: Character) -> List[str]:
        if int(self.interpreter.vars.get_flag(75, 0)) > 0:
            return []
        if int(target.talent.get(271, 0)) != 0:
            return []
        if int(target.cflag.get(81, 0)) < 700 or int(target.cflag.get(82, 0)) < 2250:
            return []
        target.talent[271] = 1
        messages = [
            f"{target.name} 最近总是面带红霞……",
            self._build_turn_end_heat_body_fluid_message(target),
            f"{target.name} 获得了【{self._get_talent_name(271)}】。",
        ]
        messages.extend(self._apply_turn_end_heat_talent_side_effects(target))
        return messages

    def _apply_turn_end_heat_talent_side_effects(self, target: Character) -> List[str]:
        messages: List[str] = []
        if int(target.talent.get(43, 0)) == 0 and int(target.talent.get(42, 0)) == 0:
            target.talent[42] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(42)}】。")
        elif int(target.talent.get(43, 0)) != 0:
            target.talent[43] = 0
            messages.append(f"{target.name} 失去了【{self._get_talent_name(43)}】。")
        messages.extend(self._clear_turn_end_talents(target, [32, 34, 84], halve_juel_100=True))
        messages.extend(self._clear_turn_end_talents(target, [71, 30]))
        return messages

    def _apply_turn_end_hp_recovery(self, char: Character, recovery: int) -> None:
        self._apply_turn_end_stat_recovery(char, 0, recovery)

    def _apply_turn_end_love_talent_cleanup(self, target: Character) -> List[str]:
        messages: List[str] = []
        if int(target.talent.get(11, 0)) != 0 and int(target.talent.get(18, 0)) != 0:
            target.talent[11] = 0
            target.talent[13] = 1
            messages.append(f"{target.name} 失去了【{self._get_talent_name(11)}】，获得了【{self._get_talent_name(13)}】。")
        elif int(target.talent.get(11, 0)) != 0:
            target.talent[11] = 0
            messages.append(f"{target.name} 失去了【{self._get_talent_name(11)}】。")
        messages.extend(self._clear_turn_end_talents(target, [20, 21], halve_juel_100=True))
        messages.extend(self._clear_turn_end_talents(target, [27, 151, 84]))
        return messages

    def _apply_turn_end_love_talent_gain(self, target: Character) -> List[str]:
        target.talent[85] = 1
        self.interpreter.vars.set_flag(30, int(self.interpreter.vars.get_flag(30, 0)) + 1)
        messages = [
            f"{target.name} 柔情似水地看着你……",
            f"{target.name} 因你的行为而感到喜悦。想粘着你，想为你分忧，为你做些什么……渴望着你的宠爱。",
            f"{target.name} 获得了【{self._get_talent_name(85)}】。",
        ]
        messages.extend(self._apply_turn_end_love_talent_cleanup(target))
        messages.extend(self._apply_turn_end_love_talent_side_effects(target))
        self._apply_love_corruption_swap_story_reset(target, 85)
        return messages

    def _apply_turn_end_love_talent_side_effects(self, target: Character) -> List[str]:
        messages: List[str] = []
        if int(target.base.get(10, 0)) > 0:
            remaining_days = int(target.base.get(10, 0)) // 2
            messages.append(f"{target.name} 时日无多，生命还剩下{remaining_days}天。")
        if int(target.talent.get(274, 0)) != 0:
            target.talent[274] = 0
            messages.extend(
                [
                    f"{target.name} 被束缚的灵魂，在向自己的爱与欲望屈服时被解放了。",
                    f"{target.name} 失去了【魂缚】。",
                ]
            )
        messages.extend(self._apply_turn_end_shojo_seal_release_prompt(target))
        messages.extend(self._apply_turn_end_maou_ex_talent_award(target))
        return messages

    def _apply_turn_end_maou_ex_talent_award(self, target: Character) -> List[str]:
        if int(self._get_character_template_id(target) or 0) != 17:
            return []
        if int(self._get_character_ex_talent(target, 3)) != 0:
            return []
        self._set_character_ex_talent(target, 3, 1)
        return [f"{target.name} 一阵眩晕、似乎拥有了【替身】的素质……"]

    def _apply_turn_end_masochism_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(88, 0)) != 0:
            return []
        if int(target.abl.get(21, 0)) < 4 or int(target.abl.get(17, 0)) < 2 or int(target.exp.get(30, 0)) < 300:
            return []
        target.talent[88] = 1
        return [
            f"{target.name} 的眼神变得卑微了……",
            f"{target.name} 将痛楚和快感视为一体，学会了享受被支配，被凌辱的喜悦。",
            f"{target.name} 获得了【{self._get_talent_name(88)}】。",
        ]

    def _apply_turn_end_master_special_skill_checks(self) -> List[str]:
        player = self._get_player()
        if player is None:
            return []
        if int(self.interpreter.vars.get_flag(30, 0)) < 5:
            return []
        if int(player.talent.get(92, 0)) != 0:
            return []
        player.talent[92] = 1
        return [f"{player.name} 掌握了【{self._get_talent_name(92)}】。"]

    def _apply_turn_end_mp_recovery(self, char: Character, recovery: int, campaign_active: bool, player: Optional[Character]) -> None:
        if campaign_active and char is player:
            return
        self._apply_turn_end_stat_recovery(char, 1, recovery)

    def _apply_turn_end_negative_talent_cleanup(self, target: Character) -> List[str]:
        messages: List[str] = []
        if int(target.abl.get(16, 0)) >= 5:
            messages.extend(self._clear_turn_end_talents(target, [151]))
        if int(target.abl.get(31, 0)) >= 5:
            messages.extend(self._clear_turn_end_talents(target, [150]))
        return messages

    def _apply_turn_end_new_day_cycle(self) -> None:
        self._apply_turn_end_world_decay_cycle()
        self._apply_turn_end_character_state_post_cycle()

    def _apply_turn_end_overlevel_slave_anomaly(self) -> List[str]:
        overflow_idx = int(self.interpreter.vars.globals.get(2803, 0))
        if overflow_idx <= 0:
            return []
        if not self._can_apply_turn_end_anomaly_events():
            return []
        if overflow_idx >= len(self.interpreter.vars.chars):
            return []

        victim = self.interpreter.vars.chars[overflow_idx]
        if int(victim.cflag.get(1, 0)) != 0:
            return []
        self.interpreter.vars.globals[2803] = 0

        victim_name = victim.name
        messages = [
            "整个地下城，其实就是一个巨大的封印，",
            "封印着魔王的力量，也封印着勇者的力量。",
            "加上日常生活和战斗所需的魔力，连同地底不断涌出的魔力，",
            "组成了地下城里错综复杂的魔力流动。",
            "几只特别强大的怪物和你本人，会聚集大量的魔力。",
            "但还是有一些魔力，从封印和法师们的掌控中流出，聚集到奴隶的身边。",
            "你能感觉得到，有一个奴隶，与众不同，身边的魔力在不断聚集着。",
            "因为她的力量已经强于你施加于她的封印，魔力之间相互碰撞，越来越不稳定了。",
            "魔力失控！发生大爆炸！",
            f"{victim_name} 被自己暴走的魔力炸得粉碎！",
        ]
        self._remove_character_at(overflow_idx)

        side_victim_candidates = [
            idx
            for idx, char in enumerate(self.interpreter.vars.chars)
            if idx > 0 and char is not victim and int(char.cflag.get(1, 0)) == 0
        ]
        if side_victim_candidates:
            side_idx = random.choice(side_victim_candidates)
            side_victim = self.interpreter.vars.chars[side_idx]
            side_name = side_victim.name
            messages.extend(
                [
                    f"{side_name} 因为房间就在 {victim_name} 的隔壁，也被她暴走的魔力波及了。",
                    f"{side_name} 也被炸死了。",
                ]
            )
            self._remove_character_at(side_idx)
        return messages

    def _apply_turn_end_player_overflow_anomaly(self) -> List[str]:
        if not self._can_apply_turn_end_anomaly_events():
            return []
        player = self._get_player()
        if player is None or int(player.cflag.get(9, 0)) < 5000:
            return []
        self.interpreter.vars.globals[2804] = 0

        self.running = False
        return [
            "整个地下城，其实就是一个巨大的封印，",
            "封印着魔王的力量，也封印着勇者的力量。",
            "加上日常生活和战斗所需的魔力，连同地底不断涌出的魔力，",
            "组成了地下城里错综复杂的魔力流动。",
            "几只特别强大的怪物和你本人，会聚集大量的魔力。",
            "但最近，你感觉魔力在身边聚集越来越多，挥之不去。",
            "你能感觉得到，各式各样的魔力在体内不停汇聚着，相互冲击。",
            "好难受！！！",
            "终于有一天，你再也无法控制。感觉到一股暖流从身体喷涌而出！",
            "你的魔力失控！发生大爆炸！",
            "巨大的威力，将你本人和整个地下城都化为齑粉。",
            "四界都能感受到大地的颤抖，余波引起的海啸和地震，摧毁了无数地方。",
            "这次事件造成的伤亡，比你所有侵攻的造成的伤害还要多，世人将这次爆炸称为【大冲击】。",
            "-------------------------------GAMEOVER---------------------------------",
        ]

    def _apply_turn_end_production_cycle(self) -> None:
        self._apply_turn_end_conception_cycle()
        self._refresh_sell_assistant_flags()

    def _apply_turn_end_prostitute_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(180, 0)) != 0:
            return []
        prostitution_exp = int(target.exp.get(74, 0))
        if int(target.mark.get(3, 0)) != 0:
            return []
        if int(target.talent.get(315, 0)) == 5:
            if prostitution_exp < 80 or int(target.abl.get(11, 0)) < 1:
                return []
            intro = f"{target.name} 无法逃离作为妓女的生活方式……"
        else:
            if prostitution_exp < 100 or int(target.abl.get(11, 0)) < 2 or int(target.abl.get(12, 0)) < 1:
                return []
            intro = f"{target.name} 以出卖肉体为主要的生活方式……"
        target.talent[180] = 1
        return [intro, f"{target.name} 获得了【{self._get_talent_name(180)}】。"]

    def _apply_turn_end_prostitution_talent_checks(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_prostitute_talent_gain(target))
        messages.extend(self._apply_turn_end_courtesan_talent_gain(target))
        return messages

    def _apply_turn_end_recovery(self, campaign_active: bool) -> None:
        player = self._get_player()
        if player is None:
            return
        hp_recovery = 1400 if int(self.interpreter.vars.time) == 0 else 1000
        self._apply_turn_end_hp_recovery(player, hp_recovery)
        mp_recovery = -10 if int(self.interpreter.vars.get_flag(400, 0)) > 0 else hp_recovery
        self._apply_turn_end_mp_recovery(player, mp_recovery, campaign_active, player)

    def _apply_turn_end_sadism_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(83, 0)) != 0:
            return []
        if int(target.abl.get(20, 0)) < 4 or int(target.abl.get(12, 0)) < 4 or int(target.exp.get(33, 0)) < 300:
            return []
        target.talent[83] = 1
        return [
            f"{target.name} 的眼神变得凌厉了……",
            f"{target.name} 学会了将快乐建立在他人的痛苦之上。",
            f"{target.name} 获得了【{self._get_talent_name(83)}】。",
        ]

    def _apply_turn_end_semen_fetish_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(47, 0)) != 0:
            return []
        service_abl = int(target.abl.get(13, 0))
        technique_abl = int(target.abl.get(12, 0))
        oral_exp = int(target.exp.get(22, 0))
        if technique_abl >= 7 and service_abl >= 7 and oral_exp >= 2000 and int(target.talent.get(52, 0)) == 0 and int(target.cflag.get(600, 0)) >= 100:
            message = f"{target.name} 因为不断地强制精饮绝顶，终于完全适应了精液的味道……\n甚至还喜欢上了。"
        elif technique_abl >= 5 and service_abl >= 5 and oral_exp >= 1500 and int(target.talent.get(52, 0)) == 0 and int(target.cflag.get(600, 0)) >= 80:
            message = f"{target.name} 喜欢上了精液的味道……"
        elif technique_abl >= 5 and service_abl >= 5 and oral_exp >= 1000 and int(target.talent.get(52, 0)) != 0 and int(target.cflag.get(600, 0)) >= 50:
            message = f"{target.name} 感到似乎离不开精液了……"
        else:
            return []
        target.talent[47] = 1
        return [message, f"{target.name} 获得了【{self._get_talent_name(47)}】。"]

    def _apply_turn_end_sex_hero_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(272, 0)) != 0:
            return []
        if not all(int(target.talent.get(talent_id, 0)) != 0 for talent_id in (230, 231, 232, 233)):
            return []
        target.talent[272] = 1
        messages = [f"{target.name} 获得了【{self._get_talent_name(272)}】。"]
        messages.extend(self._clear_turn_end_talents(target, [101, 103, 105, 107]))
        return messages

    def _apply_turn_end_shojo_seal_release_prompt(self, target: Character) -> List[str]:
        if int(target.talent.get(273, 0)) == 0:
            return []
        messages = [
            f"{target.name} 的【{self._get_talent_name(273)}】的力量消失了……",
            "如果是现在的话，可以解开封印。要解开封印吗？",
            " [0] - 保留封印",
            " [1] - 解开封印",
        ]
        while True:
            choice = self._prompt_choice()
            if choice == "0":
                return messages
            if choice == "1":
                target.talent[273] = 0
                messages.append(f"{target.name} 失去了【{self._get_talent_name(273)}】。")
                return messages

    def _apply_turn_end_special_kink_talent_checks(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_sadism_talent_gain(target))
        messages.extend(self._apply_turn_end_masochism_talent_gain(target))
        messages.extend(self._apply_turn_end_exhibitionism_talent_gain(target))
        messages.extend(self._apply_turn_end_bitch_talent_gain(target))
        return messages

    def _apply_turn_end_special_sex_talent_checks(self, target: Character) -> List[str]:
        if all(int(target.talent.get(talent_id, 0)) != 0 for talent_id in (74, 75, 77, 78)):
            return []
        sexskill_count = sum(1 for talent_id in (74, 75, 77, 78) if int(target.talent.get(talent_id, 0)) != 0)
        if sexskill_count > 0 and not self._can_gain_additional_special_sex_talent(target, sexskill_count):
            return []
        return self._gain_next_special_sex_talent(target)

    def _apply_turn_end_special_skill_check_for_character(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_bodyshift_forced_changes(target))
        if int(target.mark.get(3, 0)) != 0:
            return messages
        messages.extend(self._apply_turn_end_special_skill_mastery_unlock(target))
        if self._can_gain_turn_end_love_talent(target):
            messages.extend(self._apply_turn_end_love_talent_gain(target))
        if self._can_gain_turn_end_corruption_talent(target):
            messages.extend(self._apply_turn_end_corruption_talent_gain(target))
        messages.extend(self._apply_turn_end_sperm_service_talent_checks(target))
        messages.extend(self._apply_turn_end_special_kink_talent_checks(target))
        messages.extend(self._apply_turn_end_special_sex_talent_checks(target))
        messages.extend(self._apply_turn_end_enhanced_sex_talent_checks(target))
        messages.extend(self._apply_turn_end_heat_talent_checks(target))
        messages.extend(self._apply_turn_end_special_skill_submission_cleanup(target))
        messages.extend(self._apply_turn_end_negative_talent_cleanup(target))
        messages.extend(self._apply_turn_end_prostitution_talent_checks(target))
        messages.extend(self._apply_turn_end_blind_faith_talent_check(target))
        messages.extend(self._apply_turn_end_gladiator_talent_check(target))
        return messages

    def _apply_turn_end_special_skill_checks(self) -> List[str]:
        messages: List[str] = []
        original_target = int(self.interpreter.vars.target)
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx == original_target:
                continue
            messages.extend(self._apply_turn_end_special_skill_check_for_character(char))
        messages.extend(self._apply_turn_end_master_special_skill_checks())
        return messages

    def _apply_turn_end_special_skill_mastery_unlock(self, target: Character) -> List[str]:
        if int(target.cflag.get(2, 0)) < 2000:
            return []
        if int(target.cflag.get(0, 0)) >= 2:
            return []
        if int(target.talent.get(76, 0)) == 0 and int(target.talent.get(85, 0)) == 0:
            return []
        messages = [f"{target.name} 带着崇敬的眼神看着你……", f"{target.name} 无论是灵魂还是肉体，都全心全意地献给你了……"]
        if int(target.abl.get(10, 0)) < 5:
            target.abl[10] = 5
            messages.append("顺从LV5了")
        if int(target.cflag.get(0, 0)) < 1:
            messages.append(f"{target.name} 可以被卖掉了。")
        messages.append(f"{target.name} 可以做助手了。")
        target.cflag[0] = 2
        return messages

    def _apply_turn_end_special_skill_submission_cleanup(self, target: Character) -> List[str]:
        if int(target.cflag.get(2, 0)) < 5000:
            return []
        if int(target.abl.get(10, 0)) < 5:
            return []
        if int(target.mark.get(1, 0)) != 3 or int(target.mark.get(2, 0)) != 3:
            return []
        return self._clear_turn_end_talents(target, [150, 151, 152])

    def _apply_turn_end_sperm_service_talent_checks(self, target: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_semen_fetish_talent_gain(target))
        messages.extend(self._apply_turn_end_tongue_skill_talent_gain(target))
        messages.extend(self._apply_turn_end_forced_semen_fetish_gain(target))
        return messages

    def _apply_turn_end_stat_recovery(self, char: Character, stat_index: int, recovery: int) -> None:
        if char.base.get(stat_index, 0) < char.maxbase.get(stat_index, 100):
            char.base[stat_index] = min(char.base.get(stat_index, 0) + recovery, char.maxbase.get(stat_index, 100))

    def _apply_turn_end_tongue_skill_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(52, 0)) != 0:
            return []
        technique_abl = int(target.abl.get(12, 0))
        service_abl = int(target.abl.get(13, 0))
        oral_exp = int(target.exp.get(22, 0))
        if int(target.talent.get(51, 0)) != 0:
            if technique_abl < 7 or service_abl < 7 or oral_exp < 1500:
                return []
            intro = f"{target.name} 通过持续的侍奉，侍奉技术获得了飞跃的进步……"
        else:
            if technique_abl < 5 or service_abl < 5 or oral_exp < 1000:
                return []
            intro = f"{target.name} 的侍奉技术精进了……"
        target.talent[52] = 1
        return [intro, f"{target.name} 获得了【{self._get_talent_name(52)}】。"]

    def _apply_turn_end_treasure_vault_anomaly(self) -> List[str]:
        if not self._can_apply_turn_end_anomaly_events():
            return []
        if self.interpreter.vars.money <= int(self.interpreter.vars.globals.get(4444, 0)) + 8766:
            return []
        self.interpreter.vars.globals[2802] = 0

        messages = [
            "一些贪婪的魔物们对宝库里的财宝动起了歪念头。",
            "趁着夜深人静，几只无法克制金钱欲望的哥布林企图炸开宝库大门，偷取财宝。",
            "【这是魔王大人的财宝，我们这么干不好吧？】其中一只哥布林担心地说到。",
            "【魔王大人努力得来的我们不偷，这些神力变出来的，我们拿一点也没什么吧！】为首的哥布林充满不屑。",
            "无奈宝库的大门太过结实，一般的炸药无法撼动。",
            "贪婪的绿皮们只能不断地添加当量，结果炸药过多，发生了大爆炸。",
            "肇事的哥布林们和宝库里的财富都被炸得粉碎了……",
        ]
        lost_money = max(0, int(self.interpreter.vars.money))
        if lost_money > 0:
            self._spend_global_money(lost_money)
        messages.append("资金清零了。")

        victim_candidates = [
            idx
            for idx, char in enumerate(self.interpreter.vars.chars)
            if idx > 0 and int(char.cflag.get(1, 0)) == 0
        ]
        if not victim_candidates:
            return messages

        victim_idx = random.choice(victim_candidates)
        victim = self.interpreter.vars.chars[victim_idx]
        victim_name = victim.name
        messages.extend(
            [
                f"{victim_name} 的房间，刚好在宝库的正上方。",
                "睡梦中的她没有任何防备，不幸地被猛烈的爆炸所淹没。",
                f"{victim_name} 被炸死了。",
            ]
        )
        self._remove_character_at(victim_idx)
        return messages

    def _apply_turn_end_vagina_master_talent_gain(self, target: Character) -> List[str]:
        if int(target.talent.get(232, 0)) != 0:
            return []
        if int(target.abl.get(2, 0)) < 5 or int(target.exp.get(0, 0)) < 300 or int(target.exp.get(2, 0)) < 300:
            return []
        target.talent[232] = 1
        return [
            f"{target.name} 不停地发出【唔～唔～唔……】的勾魂声音……",
            f"{target.name}在调教结束之后依然哀求着你疼爱她的子宫。但一插进去，她便全身夸张地痉挛了起来，子宫口依依不舍地紧紧吸啜着龟头……",
            f"{target.name} 获得了【{self._get_talent_name(232)}】。",
        ]

    def _apply_turn_end_world_decay_cycle(self) -> None:
        for message in self._apply_daily_invasion_decay():
            print(message)

    def _apply_use_now_item(self, item_id: int, target: Optional[Character] = None) -> bool:
        player = self._get_player()
        selected_target = target or self._get_target() or player
        if player is None or selected_target is None:
            print("\nNo valid target is available.")
            return False

        handler_name = USE_NOW_ITEM_EFFECT_HANDLERS.get(item_id)
        if handler_name is None:
            return False
        handler = getattr(self, handler_name, None)
        if handler is None:
            return False
        return handler(selected_target, item_id)

    def _apply_use_now_item_body_hair_growth(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        current_hair = int(selected_target.talent.get(311, 0))
        if current_hair > 200:
            selected_target.talent[311] = 201
            print(f"\n涂上 {item_name} 之后似乎没什么效果。")
            return True
        selected_target.talent[311] = current_hair + 50
        selected_target.talent[125] = 0
        print(f"\n{item_name} encouraged body-hair growth.")
        return True

    def _apply_use_now_item_clear_parasite(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        selected_target.cflag[200] = 0
        print(f"\n{item_name} removed parasitic effects.")
        return True

    def _apply_use_now_item_increase_pregnancy_chance(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        selected_target.cflag[109] = 1
        print(f"\n{item_name} increased pregnancy chance.")
        return True

    def _apply_use_now_item_reduce_stress(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        selected_target.palam[100] = max(0, selected_target.palam.get(100, 0) // 2)
        self.interpreter.vars.set_flag(61, self.interpreter.vars.get_flag(61, 0) + 1)
        print(f"\n{item_name} reduced denial-related stress.")
        return True

    def _apply_use_now_item_remove_lifespan_limit(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        selected_target.base[10] = 0
        print(f"\n{item_name} removed lifespan restrictions.")
        return True

    def _apply_use_now_item_restore_hp(self, selected_target: Character, item_id: int) -> bool:
        item_name = self._get_item_name(item_id)
        selected_target.base[0] = min(selected_target.maxbase.get(0, 0), selected_target.base.get(0, 0) + 300)
        print(f"\n{item_name} restored 300 HP.")
        return True
