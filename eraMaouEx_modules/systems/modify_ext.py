from __future__ import annotations
"""Module for ModifyExtMixin - 状态修改"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ModifyExtMixin:
    """Mixin providing 状态修改 methods for GameEngine"""

    def _add_chara_ex(self, char_idx: int) -> None:
        """角色添加时设置EX素质"""
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return
        target = self.interpreter.vars.chars[char_idx]
        self.interpreter.vars.target = char_idx

        cflag6 = int(target.cflag.get(6, 0))

        # 口上添加
        if cflag6 == 10031:
            self._set_character_ex_talent(target, 101, 1)
        if cflag6 == 10032:
            self._set_character_ex_talent(target, 102, 1)
        if cflag6 == 10033:
            self._set_character_ex_talent(target, 103, 1)
        if cflag6 == 10035:
            self._set_character_ex_talent(target, 104, 1)

        # 魔王素质
        if char_idx == self.interpreter.vars.master:
            self._set_character_ex_talent(target, 200, 1)

        # 特殊战斗素质
        if cflag6 == 10034:
            self._set_character_ex_talent(target, 801, 1)
            self._set_character_ex_talent(target, 901, 1)

        # 角色专属EX素质
        no = getattr(target, 'no', 0)
        if no >= 17 or no == 0:
            method_name = f"_chara_ex_{no}"
            method = getattr(self, method_name, None)
            if method and callable(method):
                method()

    def _add_exp_delta(self, target: Character, exp_delta: Dict[int, int]):
        for key, value in exp_delta.items():
            if value:
                target.exp[key] = target.exp.get(key, 0) + value

    def _add_global_money(self, amount: int):
        amount = int(amount)
        self.interpreter.vars.money += amount
        self.interpreter.vars.globals[4444] = self.interpreter.vars.globals.get(4444, 0) + amount

    def _add_juel(self, idx: int, value: int):
        if value <= 0:
            return
        self.interpreter.vars.juel[idx] = self._get_juel(idx) + int(value)

    def _add_level_up_growth(self, char: Character, cflag_id: int, amount: int):
        char.cflag[cflag_id] = int(char.cflag.get(cflag_id, 0)) + int(amount)

    def _add_love_exp(self, exp_delta: Dict[int, int], target: Character, value: int, condition: bool = True):
        if condition and value and target.cflag.get(2, 0) >= 1000:
            exp_delta[23] = exp_delta.get(23, 0) + value

    def _add_prestige_value(self, delta: int):
        self._set_prestige_value(self._get_prestige_value() + int(delta))

    def _add_same_sex_exp(self, exp_delta: Dict[int, int], player: Optional[Character], target: Character, female_value: int, male_value: Optional[int] = None):
        if player is None:
            return
        if target.talent.get(122, 0) == 0 and player.talent.get(122, 0) == 0 and female_value:
            exp_delta[40] = exp_delta.get(40, 0) + female_value
        elif target.talent.get(122, 0) == 1 and player.talent.get(122, 0) == 1:
            value = female_value if male_value is None else male_value
            if value:
                exp_delta[41] = exp_delta.get(41, 0) + value

    def _add_sexskill(self, target: Character, exp_1: int, exp_2: int, exp_3: int) -> List[str]:
        messages: List[str] = []
        char_name = getattr(target, 'savestr', target.name or target.callname or "")
        player = self._get_player()
        player_name = getattr(player, 'savestr', "主人") if player else "主人"

        if (target.abl.get(0, 0) >= 4 and target.exp.get(11, 0) >= 100
                and target.exp.get(2, 0) >= 100 and target.talent.get(74, 0) == 0):
            messages.append(f"总觉得最近，{char_name}连呼吸都变得色情了起来…")
            organ = "阴茎" if target.talent.get(121, 0) or target.talent.get(122, 0) else "阴蒂"
            messages.append(f"调教结束之后，{char_name}当着{player_name}的面，肆无忌惮地继续玩弄着自己的{organ}。")
            messages.append(f"{char_name}获得了【自慰狂】。")
            target.talent[74] = 1
            return messages

        if (target.abl.get(2, 0) >= 4 and target.exp.get(0, 0) >= 300
                and target.exp.get(2, 0) >= 100 and target.talent.get(75, 0) == 0):
            messages.append(f"{char_name}最近对私处的运用，越来越炉火纯青…")
            messages.append(f"调教结束之后，{char_name}依依不舍地抱着{player_name}，恳求着欢好。")
            messages.append(f"{char_name}获得了【性爱狂】。")
            target.talent[75] = 1
            return messages

        if (target.talent.get(122, 0) and target.abl.get(0, 0) >= 4
                and target.exp.get(5, 0) >= 300 and target.exp.get(2, 0) >= 100
                and target.talent.get(74, 0) == 0):
            messages.append(f"{char_name}最近对性器的运用，越来越炉火纯青…")
            messages.append(f"调教结束之后，{char_name}依依不舍地抱着{player_name}，恳求着欢好。")
            messages.append(f"{char_name}获得了【性爱狂】。")
            target.talent[75] = 1
            return messages

        if (target.abl.get(3, 0) >= 4 and target.exp.get(32, 0) >= 300
                and target.exp.get(2, 0) >= 100 and target.talent.get(77, 0) == 0):
            messages.append(f"{char_name}最近好像学会了控制直肠的蠕动…")
            messages.append(f"调教结束之后，{char_name}一边摆弄自己的肛门，一边用勾引的眼神目送{player_name}。")
            messages.append(f"{char_name}获得了【尻穴狂】。")
            target.talent[77] = 1
            return messages

        if (target.abl.get(1, 0) >= 4 and target.exp.get(54, 0) >= 100
                and target.exp.get(2, 0) >= 100 and target.talent.get(78, 0) == 0
                and target.talent.get(122, 0) == 0):
            messages.append(f"最近，总觉得{char_name}的胸部，好像有着神奇的引力一般…")
            messages.append(f"调教结束之后，{char_name}用尖立的乳头直直地对着{player_name}，眼里充满了勾人的销魂神色。")
            messages.append(f"{char_name}获得了【弄乳狂】。")
            target.talent[78] = 1
            return messages

        if (target.abl.get(1, 0) >= 4 and target.juel.get(14, 0) >= 100
                and target.exp.get(2, 0) >= 100 and target.talent.get(78, 0) == 0
                and target.talent.get(122, 0)):
            messages.append(f"最近，{char_name}总觉得胸部越发敏感…")
            messages.append(f"调教结束之后，{char_name}用尖立的乳头直直地对着{player_name}，眼里充满了渴望。")
            messages.append(f"{char_name}获得了【弄乳狂】。")
            target.talent[78] = 1
            return messages

        return messages

    def _add_training_palam_gain(self, palam_delta: Dict[int, int], idx: int, value: int) -> None:
        if value:
            palam_delta[idx] = int(palam_delta.get(idx, 0)) + value

    def _clear_active_campaign(self):
        self.interpreter.vars.set_flag(400, 0)
        self.interpreter.vars.set_flag(401, 0)

    def _clear_birth_body_markers(self, target: Character) -> None:
        target.talent[341] = 0
        target.talent[342] = 0
        target.talent[343] = 0

    def _clear_current_character_selection(self, target: Character) -> None:
        target_idx = self._find_character_index(target)
        if target_idx < 0:
            return
        if self.interpreter.vars.target == target_idx:
            self.interpreter.vars.target = -1
        if self.interpreter.vars.assi == target_idx:
            self.interpreter.vars.assi = -1

    def _clear_daily_ovulation_drug_effects(self) -> List[str]:
        messages: List[str] = []
        for char in self.interpreter.vars.chars:
            if int(char.cflag.get(109, 0)) == 0:
                continue
            messages.append(f"{char.name}的排卵诱发剂的效果消失了。")
            char.cflag[109] = 0
        return messages

    def _clear_life_cradle_first_history(self, target: Character):
        target.cflag[15] = 0
        target.cflag[16] = 0
        target.cstr[3] = ""
        target.cstr[4] = ""

    def _clear_life_cradle_mutually_exclusive_talents(self, target: Character, talent_id: int, talent_group: List[int]) -> None:
        keep = target.talent.get(talent_id, 0)
        for other in talent_group:
            target.talent[other] = 0
        target.talent[talent_id] = keep

    def _clear_party_leader_slots(self, char: Character):
        char.cflag[530] = 0
        char.cflag[531] = 0
        char.cflag[532] = 0
        char.cflag[533] = 0

    def _clear_party_member_slots(self, char: Character):
        char.cflag[530] = 0
        char.cflag[533] = 0

    def _clear_turn_end_selection_state(self) -> None:
        self.interpreter.vars.target = -1
        self.interpreter.vars.assi = -1

    def _clear_turn_end_talents(self, target: Character, talent_ids: List[int], *, halve_juel_100: bool = False) -> List[str]:
        cleared = [talent_id for talent_id in talent_ids if int(target.talent.get(talent_id, 0)) != 0]
        if not cleared:
            return []
        for talent_id in cleared:
            target.talent[talent_id] = 0
        messages = [f"{target.name} 失去了" + " ".join(f"【{self._get_talent_name(talent_id)}】" for talent_id in cleared) + "。"]
        if halve_juel_100:
            target.juel[100] = int(target.juel.get(100, 0)) // 2
            messages.append("否定点数减半。")
        return messages

    def _create_ability_upgrade_option(self, ability_id: int, level: int) -> Dict[str, Any]:
        return {
            "id": ability_id,
            "name": self._get_ability_upgrade_name(ability_id),
            "level": level,
            "available": False,
            "costs": {},
            "cost_types": {},
            "reasons": [],
            "paths": [],
        }

    def _create_birth_child(self, mother: Character, father_source: int) -> Optional[Character]:
        template_id = self._choose_birth_child_template_id(mother, father_source)
        if template_id is None:
            return None
        child = self._create_character_from_template(template_id)
        if child is None:
            return None
        self._initialize_birth_child_from_parents(child, mother, father_source)
        father = self._find_birth_father_character(mother, father_source)
        self._inherit_birth_child_talents(child, mother, father)
        return child

    def _create_captive(self, name: str, hp: int, mp: int) -> Character:
        captive = Character()
        captive.name = name
        captive.base[0] = hp
        captive.base[1] = mp
        captive.maxbase[0] = hp
        captive.maxbase[1] = mp
        captive.cflag[0] = 0
        captive.cflag[16] = -1
        return captive

    def _create_enemy_character_from_template(self, template_id: int) -> Optional[Character]:
        """从模板创建勇者角色"""
        char = Character()
        char.template_id = template_id

        # 基础设置
        char.no = template_id
        char.cflag[9] = 1  # 等级
        char.cflag[0] = 0  # 状态：未调教
        char.cflag[1] = 2  # 侵攻中
        char.cflag[120] = 1  # 卖春积极性

        # 随机性别
        if random.randint(0, 59) == 0:
            char.talent[121] = 1  # 扶她
        elif random.randint(0, 5) == 0 and self._get_flag_bit(8, 0):
            char.talent[122] = 1  # 男性
        else:
            char.talent[122] = 0  # 女性

        # 随机名字
        char.name = self._generate_random_hero_name(template_id)
        char.callname = char.name

        # 随机性格
        personality_id = self._generate_random_personality()
        char.talent[personality_id] = 1

        # 随机种族
        race_id = self._generate_random_race()
        char.talent[314] = race_id

        # 处女设定
        if int(char.talent.get(122, 0)) == 1:
            char.talent[1] = 1 if random.randint(0, 2) > 0 else 0  # 童贞
        else:
            char.talent[0] = 1 if random.randint(0, 7) == 0 else 0  # 处女

        # 基础属性
        char.base[0] = 1000 + random.randint(0, 500)  # HP
        char.base[1] = 1000 + random.randint(0, 500)  # MP
        char.maxbase[0] = char.base[0]
        char.maxbase[1] = char.base[1]

        # 随机素质
        self._apply_random_talents_to_character(char)

        return char

    def _create_otherworld_hero_template_character(self) -> Optional[Character]:
        return self._instantiate_character_from_template(211)

    def _ensure_all_character_body_profiles(self, overwrite_existing: bool = False) -> int:
        updated = 0
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx == 0:
                continue
            if self._ensure_character_body_profile(char, overwrite_existing=overwrite_existing):
                updated += 1
        return updated

    def _ensure_character_body_profile(self, char: Optional[Character], overwrite_existing: bool = False) -> bool:
        if char is None:
            return False
        if not overwrite_existing and all(int(char.cflag.get(key, 0)) > 0 for key in range(451, 458)):
            return False
        human_age = self._resolve_character_body_profile_age(char)
        if human_age <= 0:
            return False
        profile = self._generate_character_body_profile(char, human_age)
        self._apply_generated_character_body_profile(char, profile, overwrite_existing=overwrite_existing)
        return True

    def _ensure_player_ejaculation_gauge(self, player: Character):
        if player.maxbase.get(2, 0) == 0:
            player.maxbase[2] = 5000 if player.talent.get(133, 0) else 10000
        player.base[2] = player.base.get(2, 0)

    def _ensure_shadow_servant_lifetime(self, char: Character):
        if not char.talent.get(292, 0):
            return
        if 820 not in char.cflag:
            char.cflag[820] = 666666

    def _ensure_training_target(self, target_idx: int, target: Optional[Character]) -> bool:
        if self._can_open_trainable_target(target_idx, target) is None:
            return True
        if not self._select_target_from_roster():
            return False
        return True

    def _finalize_character_job_change(self, target: Character, selected_job: tuple[int, int, str]) -> tuple[bool, str]:
        _, talent_id, label = selected_job
        target.cflag[1] = 0
        self._clear_character_job_talents(target)
        target.talent[talent_id] = 1
        target.cflag[9] = 1

        self._apply_character_job_talent_flags(target, talent_id)
        self._apply_character_job_post_effects(target)

        return True, f"{target.name}转职为{label}了！"

    def _finalize_character_temptation_state(self, target: Character, player: Character) -> None:
        target.cflag[2] = min(1000, int(target.cflag.get(2, 0)))
        print(f"\n好感度：{target.cflag.get(2, 0)}/1000")
        print(f"你的魔力：{player.base.get(1, 0)}/{player.maxbase.get(1, 0)}")

    def _finalize_life_cradle_character(self, new_char: Character, price: int) -> tuple[bool, str]:
        print(f"\n{new_char.name} 的最终价格是 {price} 点，可以吗？")
        print(" [1] 确定")
        print(" [2] 取消")
        confirm = self._prompt_choice()
        if confirm != "1":
            return False, "已取消。"
        if self.interpreter.vars.money < price:
            return False, "钱不够，还是重新设定吧！"
        self._ensure_labo_cost_accounting()
        self._charge_labo_cost(price)
        return True, ""

    def _finalize_otherworld_hero_preview(self, preview_char: Optional[Character]) -> tuple[bool, str]:
        if preview_char is None or not self.interpreter.vars.chars or self.interpreter.vars.chars[-1] is not preview_char:
            return False, "当前没有可确认的异界勇者。"
        if self.interpreter.vars.money <= 1500:
            return False, "金钱不够！"
        if self._get_medal_count() < 1:
            return False, "勋章不够！"
        if not self._consume_medals(1):
            return False, "勋章不够！"
        self._spend_global_money(1500)
        preview_char.cflag[999] = 1
        return True, f"{preview_char.name} 完成了异界召唤。"

    def _finalize_otherworld_hero_template_character(self, new_char: Character, sex_choice: int) -> tuple[bool, str]:
        self._spend_global_money(1500)
        new_char.cflag[999] = 1
        sex_label = {1: "男性", 2: "女性", 3: "扶她"}.get(sex_choice, "女性")
        return True, f"{new_char.name} 完成了异界召唤。性别: {sex_label}，消耗 1500 点金钱与 1 枚勋章。"

    def _finalize_train_effects(
        self,
        target: Character,
        losebase: Dict[int, int],
        source: Dict[int, int],
        exp_delta: Dict[int, int],
        origin_label: str,
    ):
        source = self._apply_soul_dislocation_source_debuff(target, source)
        source = self._apply_training_source_talent_modifiers(target, source)
        losebase, source = self._apply_training_zero_energy_modifiers(target, losebase, source)
        self._apply_training_source_followup_effects(target, source, exp_delta)
        losebase, source = self._apply_training_target_ejaculation_followup(target, losebase, source, exp_delta)
        losebase, source = self._apply_training_milk_followup(target, losebase, source, exp_delta)
        losebase, source = self._apply_training_wormbirth_followup(target, losebase, source)
        self._apply_training_master_followup(target, source)
        palam_delta = self._apply_training_derived_palam_effects(target, source)
        self._apply_source_to_character(target, source)
        self._apply_palam_delta_to_character(target, palam_delta)
        self._apply_losebase_to_character(target, losebase)
        self._store_train_snapshot(target, losebase, source)
        self._add_exp_delta(target, exp_delta)
        self._apply_training_easy_fall_checks(target, source)
        self._apply_training_omorashi_followup(target, source)
        print(origin_label)
        self._print_delta_summary("LOSEBASE", losebase)
        self._print_delta_summary("SOURCE", source)
        self._print_delta_summary("PALAM", palam_delta)
        self._print_delta_summary("EXP", exp_delta)
        self._apply_training_heat_accumulation(target)
        self._apply_training_autotrain_progress(target)
        for line in self._apply_campaign_exp_pillory(target):
            print(line)

    def _finalize_train_video_sale(self, target: Character, player: Optional[Character]) -> List[str]:
        if self._is_train_video_recording(target):
            self._stop_train_video_recording(target, player)

        frame_count = int(target.cflag.get(491, 0))
        if frame_count <= 0:
            return []

        score = self._calculate_train_video_score(target, player)
        if score <= 0:
            return []

        title = self._build_train_video_title(target)
        target.cstr[6] = title
        self._backup_video_title(title)
        self._add_global_money(score)
        self._clear_train_video_frames(target)
        target.cflag[491] = 0
        return [f"调教时的视频有着{score}点的观赏价值。", f"卖录像的{score}点到手了。"]

    def _finalize_turn_end_cycle(self, new_day: bool, early_messages: List[str]) -> None:
        if not new_day:
            return
        self._process_turn_end_new_day(early_messages)

    def _generate_human_age_from_race_age(self, race_age: int, race_talent_id: int) -> int:
        race_age = max(0, int(race_age))
        if race_talent_id == 9:
            return race_age

        rule = self._resolve_race_age_rule(int(race_talent_id))
        rule_class = int(rule["class"])
        deg = int(rule["deg"])
        num = int(rule["num"])
        scale = num * (10 ** deg)

        if rule_class == 0:
            if scale <= 0:
                return race_age
            return race_age // scale
        if rule_class == 1:
            divisor = deg * 10 + num
            if divisor <= 0:
                return race_age
            return (race_age * 10 + 5) // divisor
        return race_age

    def _generate_random_hero_name(self, template_id: int) -> str:
        """生成随机勇者名字"""
        # 基于模板 ID 的基础名字
        base_names = {
            1: "艾莉丝", 2: "莉娜", 3: "芙蕾雅", 4: "希尔维亚",
            5: "米娅", 6: "嘉德", 7: "菲娅", 8: "安娜",
            9: "露娜", 10: "塞西莉亚", 11: "莉莉", 12: "伊芙",
            13: "薇拉", 14: "克拉拉", 15: "娜塔莎", 16: "索菲亚"
        }
        base_name = base_names.get(template_id, "勇者")

        # 添加随机后缀
        suffixes = ["·法尔", "·贝尔", "·洛斯", "·维亚", ""]
        suffix = random.choice(suffixes)

        return base_name + suffix

    def _generate_random_personality(self) -> int:
        """生成随机性格 ID"""
        personalities = [160, 161, 162, 163, 164, 166, 172, 173, 174, 175]
        return random.choice(personalities)

    def _generate_random_race(self) -> int:
        """生成随机种族 ID"""
        races = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        return random.choice(races)

    def _initialize_birth_child_from_parents(self, child: Character, mother: Character, father_source: int):
        father = self._find_birth_father_character(mother, father_source)
        child.cflag[1] = 0
        child.exp[80] = 0
        child.cflag[9] = self._resolve_birth_child_level(mother, father_source, father)
        child.cflag[190] = int(getattr(child, "template_id", 0) or 0)
        if father_source == 1:
            child.talent[220] = 1
            self._initialize_guard_birth_race(child, mother)
        elif father_source in (2, 3, 4, 7):
            child.talent[220] = 0
            self._initialize_slave_birth_race(child, mother)
            if int(mother.cflag.get(1, 0)) in (2, 9):
                child.cflag[1] = 2
        if mother.talent.get(121, 0):
            child.talent[121] = 1
            child.talent[122] = 0
        elif mother.talent.get(122, 0):
            child.talent[122] = 1
            child.talent[121] = 0

    def _initialize_guard_birth_race(self, child: Character, mother: Character):
        child.talent[314] = 9
        child.talent[321] = max(0, int(mother.talent.get(321, 0))) or max(0, int(mother.talent.get(314, 0))) or 9
        if self._is_birth_elite_template_id(self._get_character_template_id(child)):
            child.talent[322] = int(getattr(child, "template_id", 0) or 0)
        elif int(child.talent.get(322, 0)) < 190:
            child.talent[322] = random.choice([191, 192, 193])

    def _initialize_new_game_state(self) -> None:
        self.interpreter.vars = ERBVariable()

        player = Character()
        player.name = "魔王"
        player.base[0] = 1000
        player.base[1] = 1000
        player.maxbase[0] = 1000
        player.maxbase[1] = 1000
        player.base[2] = 0
        player.maxbase[2] = 10000
        player.talent[320] = 1
        player.cflag[16] = -1
        self._append_character(player)

        slave = Character()
        slave.name = "勇者"
        slave.base[0] = 500
        slave.base[1] = 300
        slave.maxbase[0] = 500
        slave.maxbase[1] = 300
        slave.cflag[40] = 0
        slave.cflag[16] = -1
        self._append_character(slave)

        self.interpreter.vars.target = 1
        self.interpreter.vars.money = 10000
        self.interpreter.vars.day = [1, 1, 1, 0]
        self.interpreter.vars.time = 0
        if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
            self._ensure_race_age_defaults()
            self._ensure_all_character_body_profiles()

    def _initialize_slave_birth_race(self, child: Character, mother: Character):
        mother_race = max(0, int(mother.talent.get(314, 0)))
        mother_original_race = max(0, int(mother.talent.get(321, 0))) or mother_race
        mother_current_race = max(0, int(mother.talent.get(322, 0)))
        child.talent[314] = mother_race
        child.talent[321] = mother_original_race
        if self._is_birth_elite_template_id(self._get_character_template_id(child)):
            child.talent[322] = int(getattr(child, "template_id", 0) or 0)
        else:
            child.talent[322] = mother_current_race

    def _initialize_spawned_hero_party_funds(self, hero: Character):
        current_funds = max(0, int(hero.cflag.get(580, 0)))
        funds = 0
        if hero.talent.get(126, 0):
            funds += 1000

        former_life = int(hero.talent.get(315, 0))
        if former_life in {7, 9}:
            funds -= 500
        elif former_life in {8, 12, 19}:
            funds += 1500

        motive = int(hero.talent.get(316, 0))
        if motive in {2, 11}:
            funds -= 500
        elif motive in {9, 13}:
            funds += 500

        funds += max(0, int(hero.cflag.get(9, 0)))
        self._add_dungeon_party_funds(hero, max(0, funds))

    def _instantiate_character_from_template(self, template_id: int) -> Optional[Character]:
        char = self._load_character_template(template_id)
        if char is None:
            return None
        self._apply_character_template_post_load(char, int(template_id))
        return char

    def _instantiate_life_cradle_character(self, template_id: int) -> Optional[Character]:
        template = self._get_character_template_baseline(template_id)
        if template is None:
            return None
        char = Character()
        char.name = template.name
        char.callname = template.callname
        char.nick_name = template.nick_name
        char.base = dict(template.base)
        char.maxbase = dict(template.maxbase)
        char.abl = dict(template.abl)
        char.exp = dict(template.exp)
        char.juel = dict(template.juel)
        char.talent = dict(template.talent)
        char.mark = dict(template.mark)
        char.palam = dict(template.palam)
        char.source = dict(template.source)
        char.losebase = dict(template.losebase)
        char.equipt = dict(template.equipt)
        char.stain = dict(template.stain)
        char.cflag = dict(template.cflag)
        char.cstr = dict(template.cstr)
        char.item = dict(template.item)
        return char

    def _process_event_newday(self) -> List[str]:
        return self._process_morning_events()

    def _process_general_story_branch_event(
        self,
        messages: List[str],
        stage_flag: int,
        event_key: str,
        branch_name: str,
        accept_text: str,
        reject_text: str,
        expected_stage: int,
        main_flag_delta: int = 2,
    ):
        current_stage = int(self.interpreter.vars.get_flag(stage_flag, 0)) if stage_flag == 2815 else int(self.interpreter.vars.globals.get(stage_flag, 0))
        if current_stage != expected_stage:
            return
        if self._has_seen_ending_event(event_key):
            return
        self._queue_post_message_action(
            {
                "kind": "story_branch_prompt",
                "event_key": event_key,
                "global_flag": stage_flag,
                "main_flag_delta": main_flag_delta,
                "lines": self._build_story_branch_prompt(branch_name, accept_text, reject_text),
            }
        )

    def _process_morning_events(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_morning_fellatio_event())
        messages.extend(self._apply_onesho_events())
        messages.extend(self._apply_dog_walk_event())
        messages.extend(self._apply_endcheck_minimal())
        return messages

    def _process_new_day(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_new_day_character_state_pre_flows())
        self._reset_daily_shop_flags()
        messages.extend(self._apply_new_day_family_state_flows())
        messages.extend(self._process_next_day_events())
        messages.extend(self._apply_new_day_world_flows())
        messages.extend(self._apply_new_day_character_role_flows())
        messages.extend(self._apply_post_new_day_economic_flows())
        return messages

    def _process_next_day_events(self) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_offervirgin_events())
        messages.extend(self._apply_night_stalking_messages())
        return messages

    def _process_square_ending_events(self, messages: List[str]):
        stage = int(self.interpreter.vars.globals.get(2811, 0))
        event_key = self._get_square_ending_event_key(stage)
        if not event_key or self._has_seen_ending_event(event_key):
            return
        if self._queue_square_ending_prompt(stage, event_key):
            return
        for line in self._build_square_event_lines(stage):
            messages.append(line)
        self._apply_square_ending_stage_effects(stage)
        if stage == 310:
            self.interpreter.vars.globals[2811] = 0
        self._mark_ending_event_seen(event_key)

    def _process_turn_end_new_day(self, early_messages: List[str]) -> None:
        self._print_turn_end_new_day_messages()
        self._advance_calendar_day()
        self._apply_turn_end_new_day_cycle()
        for message in self._apply_daily_enter_enemy():
            print(message)
        self._mark_pending_morning_events()
        self._run_turn_end_post_message_actions()

    def _resolve_birth_child_level(self, mother: Character, father_source: int, father: Optional[Character] = None) -> int:
        mother_level = max(1, int(mother.cflag.get(9, 1)))
        if father_source == 1:
            player = self._get_player()
            father_level = max(1, int(player.cflag.get(9, 1))) if player is not None else mother_level
            base_level = (mother_level + father_level) // 2
            return max(1, (base_level * 6 + random.randint(0, 7)) // 10)

        if father is not None and father_source in (2, 3):
            father_level = max(1, int(father.cflag.get(9, 1)))
            base_level = (mother_level + father_level) // 2
            return max(1, (base_level * 6 + random.randint(0, max(1, base_level * 2 - 1))) // 10)

        if father_source in (4, 7):
            return max(1, (mother_level * 6 + random.randint(0, max(1, mother_level * 2 - 1))) // 10)

        return max(1, (mother_level * 6 + random.randint(0, 7)) // 10)

    def _resolve_child_care_depart(self, target: Character) -> List[str]:
        messages: List[str] = []
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            messages.extend(self._apply_birth_overflow_fallback(target, int(target.cflag.get(102, 0))))
            return messages

        child = self._create_birth_child(target, int(target.cflag.get(102, 0)))
        if child is None:
            return messages

        messages.append(f"{target.name}带着起名为{child.name}的孩子离开了育儿室。")
        target.cflag[1] = 0
        child.cflag[1] = 0
        return messages

    def _resolve_conquest_gift_selection(self, config: Dict[str, Any]) -> tuple[bool, str]:
        template_id = int(config["template_id"])
        label = str(config.get("label", "贡品角色"))
        retry_text = str(config.get("retry_text", "回去要原角色"))
        random_title = str(config.get("random_title", "挑选少女作为贡品……"))
        if self._find_character_by_template_id(template_id) is not None:
            return True, "对应角色已经在队伍中了。"
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            return False, "奴隶太多了！"

        while True:
            fixed_candidate = self._get_character_template_baseline(template_id)
            if fixed_candidate is None:
                return False, "角色模板不存在。"
            fixed_candidate.cflag[1] = 0
            action_result = self._handle_conquest_fixed_gift_candidate(
                fixed_candidate,
                label,
                random_title,
                retry_text,
            )
            if action_result is None:
                continue
            ok, message = action_result
            if ok:
                return True, message
            if message:
                return False, message

    def _resolve_life_cradle_custom_partner_selection(self, target: Character) -> Optional[tuple[bool, str]]:
        partner_name = self._prompt_life_cradle_custom_partner_name("初吻对象")
        if partner_name is None:
            return None
        if partner_name == "":
            return self._apply_life_cradle_first_kiss_random(target)
        site_code = self._prompt_life_cradle_first_kiss_site([1, 201, 301, 401], {1: "唇", 201: "阴茎", 301: "私处", 401: "肛门"})
        if site_code is None:
            return None
        return self._finish_life_cradle_first_kiss(target, site_code, partner_name)

    def _resolve_life_cradle_first_kiss_selection(
        self,
        target: Character,
        player: Optional[Character],
        selection: int,
    ) -> Optional[tuple[bool, str]]:
        if selection == 998:
            self._apply_life_cradle_first_kiss(target, -2)
            return True, self._summarize_life_cradle_first_kiss(target)
        if selection == 996:
            return self._apply_life_cradle_first_kiss_random(target)
        if selection in {0, 993, 994, 999}:
            return self._finish_life_cradle_first_kiss(target, selection)
        if selection == 995:
            return self._apply_life_cradle_first_kiss_wild_option(target)
        if selection == 1:
            return self._resolve_life_cradle_master_kiss_selection(target, player)
        if selection == 997:
            return self._resolve_life_cradle_custom_partner_selection(target)
        print("输入错误，请重新开始。")
        return None

    def _resolve_life_cradle_master_kiss_selection(self, target: Character, player: Optional[Character]) -> Optional[tuple[bool, str]]:
        options = self._get_life_cradle_master_kiss_sites()
        labels = {1: "唇", 201: "阴茎", 301: "私处", 401: "肛门"}
        site_code = self._prompt_life_cradle_first_kiss_site(options, labels)
        if site_code is None:
            return None
        return self._finish_life_cradle_first_kiss(target, site_code, player.name if player is not None else "魔王")

    def _resolve_square_black_early_stage(self, char: Character, current: int, favor: int) -> Optional[int]:
        if favor >= 5000 and current < 110:
            return 110
        if 110 <= current < 120:
            if favor <= 8000 and int(char.cflag.get(515, 0)) >= 70:
                return 120
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            return None
        if 120 <= current < 130:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            if favor >= 10000:
                return 130
            return None
        if 130 <= current < 140:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            if int(char.abl.get(10, 0)) + int(char.abl.get(16, 0)) >= 14:
                return 140
            return None
        if 140 <= current < 150:
            if int(char.cflag.get(515, 0)) >= 150 and self._get_total_day_count() >= 350 and self._find_character_by_template_id(34) is not None:
                return 150
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            return None

        return None

    def _resolve_square_black_late_stage(self, char: Character, current: int) -> Optional[int]:
        if current == 300 and self._advance_story_wait_counter(char, 300, 310):
            return 310
        return None

    def _resolve_square_black_middle_stage(self, char: Character, current: int, favor: int) -> Optional[int]:
        if 160 <= current < 170:
            if int(char.cflag.get(515, 0)) >= 200 and self._get_total_day_count() >= 350 and self._find_character_by_template_id(33) is not None:
                return 170
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            return None
        if 170 <= current < 180:
            if int(char.cflag.get(515, 0)) >= 220 and self._get_total_day_count() >= 350 and self._find_character_by_template_id(33) is not None:
                return 180
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            return None
        if 180 <= current < 190:
            if int(char.cflag.get(515, 0)) >= 250 and self._get_total_day_count() >= 350 and self._find_character_by_template_id(33) is not None:
                return 190
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1
            return None

        return None

    def _resolve_square_black_next_stage(self, char: Character, current: int, favor: int) -> Optional[int]:
        next_stage = self._resolve_square_black_early_stage(char, current, favor)
        if next_stage is not None:
            return next_stage
        next_stage = self._resolve_square_black_middle_stage(char, current, favor)
        if next_stage is not None:
            return next_stage
        return self._resolve_square_black_late_stage(char, current)

    def _set_active_campaign(self, campaign_id: int):
        self.interpreter.vars.set_flag(400, int(campaign_id))
        self.interpreter.vars.set_flag(401, 0)

    def _set_flag_bit(self, flag_idx: int, bit: int, enabled: bool):
        value = self.interpreter.vars.get_flag(flag_idx, 0)
        if enabled:
            value |= (1 << bit)
        else:
            value &= ~(1 << bit)
        self.interpreter.vars.set_flag(flag_idx, value)

    def _set_last_training_target_index(self, idx: int) -> None:
        self.interpreter.vars.items["_last_training_target"] = max(0, int(idx))

    def _set_main_menu_panel_mode(self, mode: int):
        if mode in (0, 1, 4, 5):
            self.interpreter.vars.set_flag(36, mode)

    def _set_nick_selfcall(self, target: Character, start: int = -1) -> int:
        """Set self-call based on nickname patterns from character name.
        Corresponds to ERB @SET_NICK_SELFCALL.
        Returns the case index or -1 if no match.
        """
        import random
        local = start
        locals_str = getattr(target, 'savestr', '') or target.name or ''
        name_len = len(locals_str)

        while True:
            local += 1

            # Determine if Japanese-style name (NID_GET_TYPE == 0)
            is_jp_name = self._is_character_jp_name(target)

            if is_jp_name:
                # 和名
                if local == 0:
                    # 皐月 -> 皐月 (1-2 char name used as-is)
                    if name_len > 2:
                        continue
                    target.cstr[60] = locals_str
                elif local == 1:
                    # 佳奈美 -> 佳奈 || 佳美; 纪美子 -> 纪美
                    if name_len <= 2:
                        continue
                    work_str = locals_str
                    if work_str.endswith("子"):
                        work_str = work_str[:-1]
                    if len(work_str) >= 2:
                        target.cstr[60] = work_str[0] + work_str[random.randint(1, len(work_str) - 1)]
                    else:
                        continue
                elif local == 2:
                    # 樱 -> 小樱
                    work_str = locals_str
                    if name_len > 1:
                        work_str = work_str[0]
                    target.cstr[60] = "小" + work_str
                elif local == 3:
                    # 樱 -> 樱子; 佳奈美 -> 佳子
                    work_str = locals_str
                    if name_len > 1:
                        work_str = work_str[0]
                    target.cstr[60] = work_str + "子"
                elif local == 4:
                    # 樱 -> 樱酱
                    work_str = locals_str
                    if name_len > 1:
                        work_str = work_str[0]
                    target.cstr[60] = work_str + "酱"
                elif local == 5:
                    # 樱 -> 樱子樱子; 菊枝 -> 菊枝菊枝; 佳奈美 -> 佳奈佳奈
                    work_str = locals_str
                    if name_len <= 1:
                        work_str = work_str + "子"
                    elif name_len > 2:
                        if work_str.endswith("子"):
                            work_str = work_str[:-1]
                        if len(work_str) >= 2:
                            work_str = work_str[0] + work_str[random.randint(1, len(work_str) - 1)]
                    target.cstr[60] = work_str * 2
                else:
                    return -1
            else:
                # 洋名
                if local == 0:
                    # 艾莉 -> 艾莉 (1-3 char name used as-is)
                    if name_len > 3:
                        continue
                    target.cstr[60] = locals_str
                elif local == 1:
                    # 索菲亚 -> 索菲 || 索亚
                    if name_len <= 2:
                        continue
                    if len(locals_str) >= 2:
                        target.cstr[60] = locals_str[0] + locals_str[random.randint(1, name_len - 1)]
                    else:
                        continue
                elif local == 2:
                    work_str = locals_str
                    if name_len > 1:
                        work_str = work_str[0]
                    target.cstr[60] = "小" + work_str
                elif local == 3:
                    # 艾提卡 -> 艾儿
                    if name_len < 2:
                        continue
                    if name_len == 2 and locals_str[1] == "儿":
                        continue
                    valid_prefixes = ("爱", "艾", "安", "薇", "夏", "菲", "伊", "珍", "若", "索", "佩", "洛", "露", "莎")
                    if locals_str[0] not in valid_prefixes:
                        continue
                    target.cstr[60] = locals_str[0] + "儿"
                elif local == 4:
                    # 艾提卡 -> 艾卡儿
                    if name_len < 2:
                        continue
                    if locals_str[-1] == "儿":
                        continue
                    valid_prefixes = ("爱", "艾", "安", "薇", "夏", "菲", "伊", "珍", "若", "索", "佩", "洛", "露", "莎")
                    if locals_str[0] not in valid_prefixes:
                        continue
                    target.cstr[60] = locals_str[0] + locals_str[-1] + "儿"
                else:
                    return -1

            return local

    def _set_prestige_value(self, value: int):
        self.interpreter.vars.set_flag(99, max(0, min(100, int(value))))

    def _set_ptj_level(self, target: Character, ptj_pos: int, level: int) -> None:
        """设置角色打工等级"""
        ex_cflag = getattr(target, 'ex_cflag', None)
        if ex_cflag is None:
            ex_cflag = {}
            setattr(target, 'ex_cflag', ex_cflag)
        ex_cflag[ptj_pos] = level

    def _set_random_characteristic(self, target: Character, characteristic_ids: List[int]) -> Optional[int]:
        for tid in characteristic_ids:
            target.talent[tid] = 0

        available = [tid for tid in characteristic_ids if tid != 174]
        if not available:
            return None

        chosen = random.choice(available)
        target.talent[chosen] = 1
        return chosen

    def _set_self_call(self, target: Character, call: str) -> None:
        """Set character's self-reference.
        Corresponds to ERB @RANDOM_SELF_CALL with MODE=1 (custom input).
        Sets CSTR:60 and resets CFLAG:450 to 0.
        """
        if call:
            target.cstr[60] = call
            target.cflag[450] = 0
        else:
            self._random_self_call(target, mode=0)

    def _set_suit_selfcall(self, target: Character, start: int = -1) -> int:
        """Set self-call based on suit (education/posture/openness factors).
        Corresponds to ERB @SET_SUIT_SELFCALL.
        Returns the case index (0-3) or -1 if no match.
        """
        import random
        l_education, l_posture, l_openness = self._calc_selfcall_factor(target)
        is_male = bool(target.talent.get(122, 0))

        local = start

        while True:
            local += 1

            if local == 0:
                if l_openness < -2 and l_education > 0:
                    if l_openness <= -5:
                        target.cstr[60] = "吾辈" if random.randint(0, 1) else "老身"
                    else:
                        if l_posture < -3:
                            target.cstr[60] = "在下" if is_male else "奴家"
                        else:
                            target.cstr[60] = "鄙人" if is_male else "妾身"
                else:
                    continue
            elif local == 1:
                if l_education < -2:
                    if l_posture >= 5:
                        if is_male:
                            target.cstr[60] = "老子"
                        else:
                            target.cstr[60] = "老娘"
                    else:
                        target.cstr[60] = "俺"
                else:
                    continue
            elif local == 2:
                if l_education > 2:
                    if l_posture >= 5:
                        target.cstr[60] = "本宫"
                    elif l_posture > 2:
                        target.cstr[60] = "本少爷" if is_male else "本小姐"
                    elif l_posture < -2:
                        target.cstr[60] = "小人" if is_male else "小女子"
                    elif l_posture <= -5:
                        target.cstr[60] = "在下"
                    else:
                        continue
                else:
                    continue
            elif local == 3:
                if (abs(l_education) <= 2 and abs(l_posture) <= 2 and abs(l_openness) <= 2):
                    target.cstr[60] = "鄙人" if is_male else "人家"
                else:
                    continue
            else:
                return -1

            return local

    def _spawn_conquest_random_candidate(self, hair_color: Optional[int] = None, personality_id: Optional[int] = None) -> Optional[Character]:
        candidate_ids = [
            template_id
            for template_id in range(1, 17)
            if self._instantiate_character_from_template(template_id) is not None
        ]
        if not candidate_ids:
            return None
        template_id = random.choice(candidate_ids)
        candidate = self._instantiate_character_from_template(template_id)
        if candidate is None:
            return None
        self._apply_conquest_random_candidate_style(candidate, hair_color=hair_color, personality_id=personality_id)
        candidate.cflag[1] = 0
        return candidate

    def _spawn_crazylord_special_enemy(self) -> Optional[str]:
        if not self._can_spawn_crazylord_special_enemy():
            return None
        hero = self._create_character_from_template(34)
        if hero is None:
            return None
        flag500 = int(self.interpreter.vars.get_flag(500, 0))
        if flag500 == 1:
            hero.talent[121] = 0
            hero.talent[122] = 0
        elif flag500 in (0, 2):
            hero.talent[121] = 1
            hero.talent[122] = 0
        self._prepare_spawned_invading_hero(
            hero,
            clamp_karma=False,
            assign_spawn_position=True,
            apply_initial_funds=False,
        )
        hero.cflag[508] = 3
        hero.cflag[6] = random.randint(0, 79)
        self.interpreter.vars.set_flag(224, 1)
        return self._format_spawned_hero_entry_message(hero, prefix="特殊")

    def _spawn_daily_enemy_once(self) -> Optional[str]:
        message = self._spawn_maounet_pool_hero()
        if message is not None:
            return message
        return self._spawn_standard_daily_hero()

    def _spawn_lily_special_enemy(self) -> Optional[str]:
        if not self._can_spawn_lily_special_enemy():
            return None
        hero = self._create_character_from_template(24)
        if hero is None:
            return None
        hero.cflag[550] = 40
        self._prepare_spawned_invading_hero(
            hero,
            clamp_karma=False,
            assign_spawn_position=False,
            apply_initial_funds=False,
        )
        self.interpreter.vars.set_flag(223, 1)
        return self._format_spawned_hero_entry_message(hero, prefix="特殊")

    def _spawn_standard_daily_hero(self) -> Optional[str]:
        if not self._can_spawn_daily_enemy():
            return None
        template_ids = self._get_daily_enemy_spawn_template_ids()
        if not template_ids:
            return None
        template_id = random.choice(template_ids)
        hero = self._create_character_from_template(template_id)
        if hero is None:
            return None
        self._prepare_spawned_invading_hero(hero, apply_base_level_bonus=True)
        self._apply_spawned_hero_level_progression()
        return self._format_spawned_hero_entry_message(hero)

    def _use_curse_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """诅咒术 - 对应 @CURSE_MAGIC"""
        damage = char_lv
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 200)
            def_reduction = random.randint(0, max(damage, 1)) // 2
            target.cflag[12] = target.cflag.get(12, 0) - def_reduction
            if target.cflag[12] < 0:
                target.cflag[12] = 0
                return {
                    "effect": "curse",
                    "damage": def_reduction,
                    "message": f"{target.name}完全被诅咒了…",
                }
            elif damage == 0:
                return {
                    "effect": "curse",
                    "damage": 0,
                    "message": "诅咒效果消失了",
                }
            else:
                return {
                    "effect": "curse",
                    "damage": def_reduction,
                    "message": f"{target.name}仍然被诅咒着…",
                }
        else:
            damage = self._magic_bonus_c_to_m(char, damage)
            return {
                "effect": "curse",
                "damage": damage,
                "message": f"{char.name}咏唱了诅咒术！",
            }

    def _use_energy_bolt_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """魔法箭 - 对应 @ENERGY_BOLT_MAGIC"""
        damage = char_lv * 5
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 600)
            target.base[0] = target.base.get(0, 0) - damage
            return {
                "effect": "damage_hp",
                "damage": damage,
                "message": f"魔法箭对{target.name}造成了{damage}伤害！",
            }
        else:
            damage = self._magic_bonus_c_to_m(char, damage)
            return {
                "effect": "damage_hp",
                "damage": damage,
                "message": f"{char.name}咏唱了魔法箭！",
            }

    def _use_energy_drain_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """魔法吸取 - 对应 @ENERGY_DRAIN_MAGIC"""
        damage = char_lv * 5
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 500)
            target.base[1] = target.base.get(1, 0) - damage
            char.base[0] = char.base.get(0, 0) + damage
            return {
                "effect": "drain_hp",
                "damage": damage,
                "heal": damage,
                "message": f"魔法吸取了{target.name} {damage}气力！恢复了HP{damage}点！",
            }
        else:
            damage = self._magic_bonus_c_to_m(char, damage)
            char.base[0] = char.base.get(0, 0) + damage
            return {
                "effect": "drain_hp",
                "damage": damage,
                "heal": damage,
                "message": f"{char.name}咏唱了魔法吸取！恢复了HP{damage}点！",
            }

    def _use_fireball_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """火球术 - 对应 @FIREBALL_MAGIC"""
        if target is not None:
            damage = char_lv * 10
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 800)
            target.base[0] = target.base.get(0, 0) - damage
            return {
                "effect": "damage_hp",
                "damage": damage,
                "message": f"火球术对{target.name}造成了{damage}伤害！",
            }
        else:
            damage = char_lv * 10
            damage = self._magic_bonus_c_to_m(char, damage)
            return {
                "effect": "damage_hp_aoe",
                "damage": damage,
                "message": f"{char.name}咏唱了火球术！",
            }

    def _use_heal_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """治疗术 - 对应 @HEAL_MAGIC"""
        # 检查目标HP是否低于60%
        heal_target = target if target is not None else char
        max_hp = heal_target.maxbase.get(0, 1000)
        current_hp = heal_target.base.get(0, 0)
        if max_hp > 0 and current_hp * 100 // max_hp >= 60:
            return {
                "effect": "none",
                "heal": 0,
                "message": "没有需要治疗的目标",
            }

        damage = char_lv * 5
        damage = self._magic_bonus_c_to_c(char, damage, None)
        heal_target.base[0] = heal_target.base.get(0, 0) + damage
        return {
            "effect": "heal",
            "heal": damage,
            "message": f"{heal_target.name}的HP恢复了{damage}点！",
        }

    def _use_lv_drain_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """经验吸取 - 对应 @LV_DRAIN_MAGIC"""
        damage = char_lv * 10
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 400)
            exp_drain = damage
            target.exp[80] = target.exp.get(80, 0) - exp_drain
            target.base[0] = target.base.get(0, 0) - damage * 10
            char.exp[80] = char.exp.get(80, 0) + exp_drain // 2
            # 经验为负则降级
            if target.exp[80] < 0:
                target.cflag[9] = target.cflag.get(9, 0) - 1
                target.exp[80] = target.cflag.get(9, 0) * 10
                target.cflag[11] = target.cflag.get(11, 0) - 1
                target.cflag[12] = target.cflag.get(12, 0) - 1
                target.cflag[13] = target.cflag.get(13, 0) - 1
                target.cflag[14] = target.cflag.get(14, 0) - 1
                return {
                    "effect": "drain_exp",
                    "damage": damage,
                    "exp_drain": exp_drain,
                    "level_down": True,
                    "message": f"吸取{target.name} {exp_drain}点经验值并造成了{damage*10}点HP的伤害！{target.name}的等级下降了1级。",
                }
            return {
                "effect": "drain_exp",
                "damage": damage,
                "exp_drain": exp_drain,
                "message": f"吸取{target.name} {exp_drain}点经验值并造成了{damage*10}点HP的伤害！{char.name}得到{exp_drain//2}经验值！",
            }
        else:
            damage = self._magic_bonus_c_to_m(char, damage)
            exp_gain = damage // 20
            char.exp[80] = char.exp.get(80, 0) + exp_gain
            return {
                "effect": "drain_exp",
                "damage": damage,
                "exp_drain": exp_gain,
                "message": f"{char.name}咏唱了经验吸取！得到了{exp_gain}点经验！",
            }

    def _use_mind_drain_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """精神吸收 - 对应 @MIND_DRAIN_MAGIC"""
        damage = char_lv * 5
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 500)
            target.base[1] = target.base.get(1, 0) - damage
            char.base[1] = char.base.get(1, 0) + damage
            return {
                "effect": "drain_mp",
                "damage": damage,
                "heal": damage,
                "message": f"精神吸收了{target.name} {damage}点气力！气力恢复{damage}点！",
            }
        else:
            damage = self._magic_bonus_c_to_m(char, damage)
            char.base[1] = char.base.get(1, 0) + damage
            return {
                "effect": "drain_mp",
                "damage": damage,
                "heal": damage,
                "message": f"{char.name}咏唱了精神吸收！气力恢复{damage}点！",
            }

    def _use_sleep_magic(self, char, target, char_lv: int) -> Dict[str, Any]:
        """睡眠咒语 - 对应 @SLEEP_MAGIC"""
        damage = char_lv
        if target is not None:
            damage = self._magic_bonus_c_to_c(char, damage, target)
            target_lv = target.cflag.get(9, 0)
            damage = self._magic_damage_cap(char_lv, target_lv, damage, 300)
            sleep_reduction = random.randint(0, max(damage, 1))
            target.cflag[11] = target.cflag.get(11, 0) - sleep_reduction
            if target.cflag[11] < 0:
                target.cflag[11] = 0
                return {
                    "effect": "sleep",
                    "damage": sleep_reduction,
                    "message": f"{target.name}完全睡着了…",
                }
            elif damage <= 0:
                return {
                    "effect": "sleep",
                    "damage": 0,
                    "message": "咒语的效果消失了",
                }
            else:
                return {
                    "effect": "sleep",
                    "damage": sleep_reduction,
                    "message": f"{target.name}还在沉睡着…",
                }
        else:
            # 对怪物使用
            damage = self._magic_bonus_c_to_m(char, damage)
            return {
                "effect": "sleep",
                "damage": damage,
                "message": f"{char.name}咏唱了睡眠咒语！",
            }

    def _use_teleport_magic(self, char, target) -> Dict[str, Any]:
        """传送术 - 对应 @TELEPORT_MAGIC"""
        # 检查自身是否重伤 (HP <= 600)
        if char.base.get(0, 0) <= 600:
            return {
                "effect": "escape",
                "message": f"{char.name}在危机关头使出传送术脱离了！",
                "escaped": True,
            }
        # 检查队友是否重伤
        for ally_idx in (531, 532, 533):
            ally_no = char.cflag.get(ally_idx, 0)
            if ally_no > 0:
                # 简化：无法直接访问其他角色，标记需要检查
                return {
                    "effect": "escape",
                    "message": f"{char.name}在危机关头使出传送术脱离了！",
                    "escaped": True,
                }
        return {"effect": "none", "message": "没有人处于危险状态", "escaped": False}

    def _validate_ability_upgrade_option(self, option: Dict[str, Any], target: Character, rules: Dict[str, Any]) -> None:
        abnormal_exp = rules.get("abnormal_exp", lambda _: 0)(target)
        if abnormal_exp > target.exp.get(50, 0):
            option["reasons"].append(f"异常经验不足({target.exp.get(50, 0)}/{abnormal_exp})")

        if option["paths"]:
            self._validate_ability_upgrade_paths(option, target)
            return

        for shortfall in self._collect_ability_upgrade_resource_shortfalls(target, option["costs"], option["cost_types"]):
            option["reasons"].append(f"资源不足 {shortfall}")

    def _validate_ability_upgrade_paths(self, option: Dict[str, Any], target: Character) -> None:
        available_paths = []
        path_descriptions: List[str] = []
        for path in option["paths"]:
            path_reasons = self._collect_ability_upgrade_resource_shortfalls(target, path["costs"], option["cost_types"])
            path["available"] = not path_reasons
            path["reasons"] = path_reasons
            if path["available"]:
                available_paths.append(path)
            else:
                path_descriptions.append(f"{path['label']}不可用({'/'.join(path_reasons)})")
        if not available_paths:
            option["reasons"].append("；".join(path_descriptions) if path_descriptions else "没有可用升级路线")
        else:
            option["costs"] = dict(available_paths[0]["costs"])

    def _validate_character_temptation_player(self, player: Optional[Character]) -> Optional[str]:
        if player is None:
            return "当前没有魔王角色。"
        if int(player.base.get(1, 0)) < 2000:
            return "你的魔力耗尽了"
        return None

    def _validate_life_cradle_talents(self, target: Character) -> tuple[bool, List[str]]:
        messages: List[str] = []
        has_personality = any(target.talent.get(talent_id, 0) for talent_id in list(range(160, 165)) + [166, 172, 173, 174])
        has_job = any(target.talent.get(talent_id, 0) for talent_id in range(200, 220))
        if not has_personality:
            messages.append("需要设定性格（口上）")
        if not has_job:
            messages.append("需要有【近卫】及【后代】之外的职业设定")
        required_exact = {
            300: "需要设定发色",
            301: "需要设定头发状态",
            303: "需要设定头发修剪方式",
            304: "需要设定发型",
            305: "需要设定眼型",
            306: "需要设定瞳色",
            307: "需要设定唇型",
            309: "需要设定乳头",
            310: "需要设定阴毛状态",
            312: "需要设定魅力点",
            313: "需要设定癖好",
            317: "需要设定喜欢的东西",
        }
        for talent_id, message in required_exact.items():
            if not target.talent.get(talent_id, 0):
                messages.append(message)
        if target.talent.get(220, 0) and not target.talent.get(319, 0):
            messages.append("精英需要设定精英种族")
        return not messages, messages
