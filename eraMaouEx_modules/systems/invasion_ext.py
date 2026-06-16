from __future__ import annotations
"""Module for InvasionExtMixin - 入侵系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class InvasionExtMixin:
    """Mixin providing 入侵系统 methods for GameEngine"""

    def _advance_global_invasion_completion_story(self, area: Dict[str, Any]) -> None:
        if int(area.get("area_flag", 0)) != 101:
            return
        current = int(self.interpreter.vars.globals.get(2810, 0))
        if 541 <= current < 560:
            self.interpreter.vars.globals[2810] = current + 5






    def _advance_invasion_area_menu(self, area: Dict[str, Any]) -> bool:
        monster_count = self._get_monster_count()
        self._render_invasion_area_menu(area, monster_count)
        mode_choice = self._prompt_invasion_area_mode_choice()
        if mode_choice == "999":
            return True

        result = self._handle_invasion_area_mode_choice(area, mode_choice, monster_count)
        if result is None:
            return False
        power, hero, mode = result
        ok, message = self._apply_invasion_result(area, power, mode, hero)
        print(f"\n{message}")
        self._pause()
        if ok:
            self.advance_time()
            return True
        return False






    def _advance_invasion_elite_battle_enemy_phase(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        enemy_atk: int,
        hero_def: int,
        hero_hp: int,
        hero_mp: int,
        hero_surrender: bool,
        messages: List[str],
    ) -> tuple[tuple[int, int, int, int], Optional[tuple[int, int, int, int, int, int, tuple[int, List[str], bool]]]]:
        hero_state = self._apply_invasion_elite_battle_enemy_round_state(hero, sinkou, enemy_atk, hero_def, hero_hp, hero_mp)
        round_result = self._resolve_invasion_elite_battle_enemy_turn_result(
            hero,
            enemy,
            sinkou,
            hero_state,
            hero_surrender,
            messages,
        )
        if round_result is not None:
            return hero_state, round_result
        return hero_state, None






    def _advance_invasion_elite_battle_hero_phase(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        enemy_hp: int,
        enemy_mp: int,
        enemy_atk: int,
        enemy_def: int,
        messages: List[str],
    ) -> tuple[tuple[int, int, int, int], Optional[tuple[int, int, int, int, int, int, tuple[int, List[str], bool]]]]:
        enemy_state = self._apply_invasion_elite_battle_hero_round_state(hero, enemy, sinkou, hero_atk, enemy_def, enemy_hp, enemy_mp)
        round_result = self._resolve_invasion_elite_battle_hero_turn_result(
            hero,
            enemy,
            sinkou,
            hero_hp,
            hero_mp,
            hero_atk,
            hero_def,
            enemy_state,
            messages,
        )
        if round_result is not None:
            return enemy_state, round_result
        return enemy_state, None






    def _advance_invasion_menu(self, areas: List[Dict[str, Any]]) -> bool:
        self._render_invasion_menu(areas)
        choice = self._prompt_invasion_choice()
        handled, exit_menu = self._handle_invasion_menu_choice(choice, areas)
        if handled:
            return exit_menu
        print("\nInvalid selection.")
        self._pause()
        return False






    def _append_invasion_completion_line(self, detail: str, area: Dict[str, Any]) -> str:
        if area.get("global_area"):
            return detail + f"\n{area['name']} 的侵攻已经抵达尽头。"
        return detail + f"\n{area['name']} 已被征服。"






    def _apply_daily_invasion_decay(self) -> List[str]:
        messages: List[str] = []
        for rule in DAILY_INVASION_DECAY_RULES:
            self._apply_daily_invasion_decay_rule(rule, messages)
        return messages






    def _apply_daily_invasion_decay_rule(self, rule: Dict[str, Any], messages: List[str]) -> None:
        area_flag = int(rule["area_flag"])
        progress = int(self.interpreter.vars.get_flag(area_flag, 0))
        conquer_state = int(self.interpreter.vars.get_flag(int(rule["conquer_flag"]), 0))
        if conquer_state == 0:
            if progress <= 0:
                return
            reduced = random.randint(0, 99)
            updated = max(0, progress - reduced)
            self.interpreter.vars.set_flag(area_flag, updated)
            messages.append(f"{rule['resist_name']} 反抗着魔王军……")
            messages.append(f"*{rule['area_name']}减少了*")
            messages.extend(self._apply_invasion_stage_events(area_flag, updated))
            return
        if random.randint(0, int(rule["recover_threshold"]) - 1) != 0:
            return
        if progress <= 100:
            return
        reduced = random.randint(0, 99)
        updated = max(100, progress - reduced)
        self.interpreter.vars.set_flag(area_flag, updated)
        messages.append(f"{rule['resist_name']} 为了夺回领地、反抗着魔王军……")
        messages.append(f"*{rule['conquered_area_name']}减少了*")
        messages.extend(self._apply_invasion_stage_events(area_flag, updated))






    def _apply_invasion_action_cost(self, mode: int) -> None:
        player = self._get_player()
        if mode in (1, 3) and player is not None:
            player.base[1] = max(0, player.base.get(1, 0) // 2)
        if mode == 0:
            stock = self._get_monster_stock()
            for key in list(stock.keys()):
                stock[key] = max(0, int(stock[key]) // 2)
        elif mode == 2:
            stock = self._get_monster_stock()
            for key in list(stock.keys()):
                stock[key] = max(0, int(stock[key]) * 2 // 3)






    def _apply_invasion_challenge_hero_duel(self, area: Dict[str, Any], mode: int, sinkou: int, hero: Character) -> tuple[int, List[str], bool]:
        context = self._get_invasion_challenge_context(area)
        roll = random.randint(0, 9)
        messages = [f"{hero.name}与{context['enemy_name']}开始了战斗。"]
        if roll < 2:
            return self._finish_invasion_challenge_hero_duel_minor_win(hero, messages, sinkou)
        if roll < 6:
            return self._finish_invasion_challenge_hero_duel_minor_loss(hero, messages, sinkou)
        if mode == 2:
            return self._finish_invasion_challenge_hero_duel_leaderless_retreat(messages)
        return self._finish_invasion_challenge_hero_duel_escape_or_capture(area, hero, messages)






    def _apply_invasion_challenge_ignore(self, area: Dict[str, Any], sinkou: int) -> tuple[int, List[str], bool]:
        context = self._get_invasion_challenge_context(area)
        if random.randint(0, 1) != 0:
            return 0, [f"由于{context['pass_name']}地形狭窄，魔王军损失惨重，只好撤退。"], True
        return max(0, sinkou * 4 // 5), [f"由于{context['pass_name']}地形狭窄，魔王军损失了不少魔物。魔物数量-20%。"], False






    def _apply_invasion_challenge_maou_duel(self, area: Dict[str, Any], sinkou: int, hero: Optional[Character]) -> tuple[int, List[str], bool]:
        context = self._get_invasion_challenge_context(area)
        player = self._get_player()
        if player is None:
            return sinkou, [], False
        use_cash = self.interpreter.vars.money >= 3000 and self._prompt_invasion_challenge_maou_duel_cash_choice()
        can_capture = self._can_capture_challenge_target(area)
        roll = random.randint(0, 9)
        messages = [f"魔王回应了挑战，与{context['enemy_name']}展开了决斗。"]
        action_result = self._resolve_invasion_challenge_maou_duel_action(area, hero, player, sinkou, use_cash, can_capture, roll, messages, context)
        if action_result is not None:
            return action_result
        return self._finish_invasion_challenge_maou_duel_defeat(player, messages)






    def _apply_invasion_character_medal_bonus(self, sinkou: int, char: Character) -> tuple[int, Optional[str]]:
        medal_bonus, medal_message = self._get_invasion_medal_bonus(char)
        if medal_bonus == 100:
            return sinkou, medal_message
        return max(0, sinkou * medal_bonus // 100), medal_message






    def _apply_invasion_completion_check(self, freshly_conquered: Optional[set[int]] = None) -> List[str]:
        messages: List[str] = []
        for area in self._get_invasion_area_definitions():
            progress = self._get_invasion_area_progress(area)
            conquer_state = self._get_invasion_conquer_state(area)
            just_finished = int(area["area_flag"]) in (freshly_conquered or set())
            if progress < 10000:
                continue
            stage_messages = self._apply_invasion_completion_stage(area, conquer_state, just_finished)
            if stage_messages:
                messages.extend(stage_messages)
        return messages






    def _apply_invasion_completion_global_area(
        self,
        area: Dict[str, Any],
        conquer_state: int,
        just_finished: bool,
    ) -> List[str]:
        if not just_finished or conquer_state != 0:
            return []
        self._advance_global_invasion_completion_story(area)
        self._apply_invasion_prestige_gain(10)
        return [f"{area['name']} 的侵攻抵达了终点，威望值增加 10。"]






    def _apply_invasion_completion_local_area(
        self,
        area: Dict[str, Any],
        conquer_state: int,
        just_finished: bool,
    ) -> List[str]:
        if conquer_state != 0 and not just_finished:
            return []
        self.interpreter.vars.set_flag(int(area["conquer_flag"]), 1)
        self._apply_invasion_prestige_gain(10)
        messages = [f"{area['name']} 已进入征服阶段，威望值增加 10。"]
        messages.extend(self._grant_invasion_conquest_reward(int(area["area_flag"])))
        return messages






    def _apply_invasion_completion_stage(
        self,
        area: Dict[str, Any],
        conquer_state: int,
        just_finished: bool,
    ) -> List[str]:
        if area.get("global_area"):
            return self._apply_invasion_completion_global_area(area, conquer_state, just_finished)
        return self._apply_invasion_completion_local_area(area, conquer_state, just_finished)






    def _apply_invasion_elite_battle_enemy_round_state(
        self,
        hero: Character,
        sinkou: int,
        enemy_atk: int,
        hero_def: int,
        hero_hp: int,
        hero_mp: int,
    ) -> tuple[int, int, int, int]:
        return self._apply_invasion_elite_battle_enemy_turn(
            hero,
            sinkou,
            enemy_atk,
            hero_def,
            hero_hp,
            hero_mp,
        )






    def _apply_invasion_elite_battle_enemy_turn(
        self,
        hero: Character,
        sinkou: int,
        enemy_atk: int,
        hero_def: int,
        hero_hp: int,
        hero_mp: int,
    ) -> tuple[int, int, int, int]:
        damage_base = enemy_atk - hero_def
        if damage_base > 0:
            damage = damage_base * 5
            hero_hp -= damage
            hero_mp -= damage
            if hero.talent.get(251, 0) == 0:
                hero_atk = max(1, int(hero.cflag.get(11, 0)) - max(0, damage_base // 100))
                hero.cflag[11] = hero_atk
        else:
            hero_def = max(0, hero_def * 2 // 3)
        return hero_hp, hero_mp, int(hero.cflag.get(11, 0)), hero_def






    def _apply_invasion_elite_battle_hero_round_state(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_atk: int,
        enemy_def: int,
        enemy_hp: int,
        enemy_mp: int,
    ) -> tuple[int, int, int, int]:
        return self._apply_invasion_elite_battle_hero_turn(
            hero,
            enemy,
            sinkou,
            hero_atk,
            enemy_def,
            enemy_hp,
            enemy_mp,
        )






    def _apply_invasion_elite_battle_hero_turn(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_atk: int,
        enemy_def: int,
        enemy_hp: int,
        enemy_mp: int,
    ) -> tuple[int, int, int, int]:
        damage_base = hero_atk * (sinkou // 1024 + 1) - enemy_def
        if damage_base > 0:
            crit = random.randint(0, 4) == 0
            damage = damage_base * (4 if crit else 2)
            enemy_hp -= damage
            enemy_mp -= damage
            if enemy.talent.get(251, 0) == 0:
                enemy_atk = max(1, int(enemy.cflag.get(11, 0)) - max(0, damage_base // 100))
                enemy.cflag[11] = enemy_atk
        else:
            enemy_def //= 2
        return enemy_hp, enemy_mp, int(enemy.cflag.get(11, 0)), enemy_def






    def _apply_invasion_fort_assault(self, mode: int, sinkou: int, hero: Optional[Character], context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        roll = random.randint(0, 9)
        messages = self._build_invasion_fort_assault_intro_messages(context)
        if roll >= 6:
            return self._apply_invasion_fort_assault_minor_breakthrough(mode, sinkou, hero, context, messages)
        if roll >= 2:
            return self._apply_invasion_fort_assault_major_breakthrough(mode, sinkou, hero, context, messages)
        return self._apply_invasion_fort_assault_stalemate(mode, hero, context, messages)






    def _apply_invasion_fort_assault_major_breakthrough(
        self,
        mode: int,
        sinkou: int,
        hero: Optional[Character],
        context: Dict[str, Any],
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        messages.extend([
            f"{context['fort_name']}的防御极其坚固，让魔王军损失惨重。",
            f"在付出巨大的代价后，魔王军才攻下了{context['fort_name']}。",
        ])
        if mode == 2 and hero is not None:
            exp_gain = max(0, sinkou // 5)
            hero.exp[80] = hero.exp.get(80, 0) + exp_gain
            hero.base[0] = max(0, hero.base.get(0, 0) // 2)
            messages.append(f"{hero.name}获得了{exp_gain}点经验值！")
            messages.append(f"{hero.name}的体力减少了一半！")
        messages.append("怪物数量减少了50%。")
        return max(0, sinkou // 2), messages, False






    def _apply_invasion_fort_assault_minor_breakthrough(
        self,
        mode: int,
        sinkou: int,
        hero: Optional[Character],
        context: Dict[str, Any],
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        messages.extend([
            f"在付出较小的代价后攻破了{context['fort_name']}的一角。",
            f"{context['fort_name']}中的{context['army_name']}仓皇外逃，被城外的魔王军尽数剿灭。",
        ])
        if mode == 2 and hero is not None:
            exp_gain = max(0, sinkou // 5)
            hero.exp[80] = hero.exp.get(80, 0) + exp_gain
            messages.append(f"{hero.name}获得了{exp_gain}点经验值！")
        messages.append("怪物数量减少了10%。")
        return max(0, sinkou * 9 // 10), messages, False






    def _apply_invasion_fort_assault_stalemate(
        self,
        mode: int,
        hero: Optional[Character],
        context: Dict[str, Any],
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        messages.extend([
            f"{context['fort_name']}的防御极其坚固，令魔王军久攻不下，陷入僵局。",
            f"突然出现的{context['army_name']}援军击溃了魔王军。",
            "侵攻中止。",
        ])
        if mode == 2 and hero is not None:
            hero.base[0] = max(0, hero.base.get(0, 0) * 3 // 10)
            self._set_character_invasion_retreat_standby_state(hero)
        return 0, messages, True






    def _apply_invasion_fort_detour(self, mode: int, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        if mode == 2:
            return self._apply_invasion_fort_detour_for_army(sinkou, context)
        return self._apply_invasion_fort_detour_for_hero(sinkou, hero, context)






    def _apply_invasion_fort_detour_for_army(self, sinkou: int, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        roll = random.randint(0, 9)
        if roll > 0:
            return max(0, sinkou * 9 // 10), [f"魔王军绕开{context['fort_name']}继续前进，怪物数量减少了10%。"], False
        return max(0, sinkou * 5 // 10), [f"魔王军绕开{context['fort_name']}时遭遇埋伏，怪物数量减少了50%。"], False






    def _apply_invasion_fort_detour_for_hero(self, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        roll = random.randint(0, 9)
        if roll > 0:
            hero.base[0] = max(1, hero.base.get(0, 0) * 9 // 10)
            return sinkou, [f"{hero.name}绕开{context['fort_name']}继续前进，耗费了一些体力。"], False
        if self._get_flag_bit(5, 7):
            self._set_character_ntr_captive_state(hero)
            return 0, [f"{hero.name}绕路时遭遇埋伏并被活捉了。"], True
        self._set_character_invasion_retreat_standby_state(hero)
        return 0, [f"{hero.name}绕路时遭遇埋伏，最终逃了回来。"], True






    def _apply_invasion_fort_infiltration(self, mode: int, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        roll = random.randint(0, 9)
        has_wings = bool(hero.talent.get(245, 0))
        race = int(hero.talent.get(314, 0))
        if has_wings or race in (6, 8):
            return self._apply_invasion_fort_infiltration_airborne(mode, sinkou, hero, context)
        if roll >= 5 or bool(context.get("race_match")):
            return self._apply_invasion_fort_infiltration_disguised(mode, sinkou, hero, context)
        if roll >= 2 or not self._get_flag_bit(5, 7):
            return self._apply_invasion_fort_infiltration_escape(mode, sinkou, hero, context)
        return self._apply_invasion_fort_infiltration_captured(hero, context)






    def _apply_invasion_fort_infiltration_airborne(self, mode: int, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        if mode == 2:
            return self._apply_invasion_fort_infiltration_success_reward(
                sinkou,
                hero,
                context,
                f"{hero.name}趁着夜色从空中潜入了{context['fort_name']}，打开了大门。",
            )
        return sinkou, [f"{hero.name}趁着夜色从空中穿过了{context['fort_name']}。"], False






    def _apply_invasion_fort_infiltration_captured(self, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        self._set_character_ntr_captive_state(hero)
        return 0, [f"{hero.name}潜入失败后被{context['army_name']}生擒，被俘虏后侵攻中止。"], True






    def _apply_invasion_fort_infiltration_disguised(self, mode: int, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        if mode == 2:
            return self._apply_invasion_fort_infiltration_success_reward(
                sinkou,
                hero,
                context,
                f"{hero.name}乔装打扮成功混进了{context['fort_name']}里。",
            )
        return sinkou, [f"{hero.name}乔装打扮成功通过了{context['fort_name']}。"], False






    def _apply_invasion_fort_infiltration_escape(self, mode: int, sinkou: int, hero: Character, context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        hero.base[0] = 1
        if mode == 2:
            return max(0, sinkou * 7 // 10), [
                f"{hero.name}潜入失败后杀出一条血路，勉强逃回了魔王军。",
                f"{hero.name}的体力归零。",
                "怪物数量减少了30%。",
            ], False
        self._set_character_invasion_retreat_standby_state(hero)
        return 0, [f"{hero.name}潜入失败后杀出一条血路，勉强逃了回去。"], True






    def _apply_invasion_fort_infiltration_success_reward(
        self,
        sinkou: int,
        hero: Character,
        context: Dict[str, Any],
        first_message: str,
    ) -> tuple[int, List[str], bool]:
        exp_gain = max(0, sinkou // 5)
        hero.exp[80] = hero.exp.get(80, 0) + exp_gain
        self.interpreter.vars.set_flag(83, self.interpreter.vars.get_flag(83, 0) + 5)
        return sinkou, [
            first_message,
            f"{hero.name}获得了{exp_gain}点经验值！",
            "人间牧场肉便器数量+5。",
        ], False






    def _apply_invasion_karma_effect(self, hero: Optional[Character], mode: int) -> Optional[str]:
        if hero is None:
            return None
        if mode == 2:
            self._add_character_karma(hero, -50)
            return f"{hero.name} 的善恶值减少了 50。"
        if mode == 3:
            self._add_character_karma(hero, -5)
            return f"{hero.name} 的善恶值减少了 5。"
        return None






    def _apply_invasion_knowledge_bonus(self, sinkou: int) -> tuple[int, List[str]]:
        messages: List[str] = []
        player = self._get_player()
        if player is None:
            return sinkou, messages
        current = max(0, int(sinkou))
        if player.talent.get(325, 0) == 1:
            current = current * 150 // 100
            messages.append("魔界知识补正 x1.50")
        if player.talent.get(327, 0) == 1:
            current = current * 120 // 100
            messages.append("淫魔知识补正 x1.20")
        if player.talent.get(328, 0) == 1:
            current = current * 110 // 100
            messages.append("魔虫知识补正 x1.10")
        return current, messages






    def _apply_invasion_master_level_bonus(self, sinkou: int) -> tuple[int, Optional[str]]:
        player = self._get_player()
        if player is None:
            return sinkou, None
        level_bonus = self._get_invasion_level_bonus_percent(player)
        return max(0, sinkou * level_bonus // 100), f"魔王补正 x{level_bonus / 100:.2f}"






    def _apply_invasion_mode_prestige_context(self, power: int, mode: int) -> tuple[int, str]:
        if mode in (0, 1):
            return self._apply_invasion_prestige_modifier(power)
        state, _percent = self._get_invasion_prestige_state()
        return max(0, power), state






    def _apply_invasion_prestige_gain(self, amount: int = 2):
        self._add_prestige_value(amount)






    def _apply_invasion_prestige_modifier(self, base_power: int) -> tuple[int, str]:
        state, percent = self._get_invasion_prestige_state()
        if percent <= 0:
            return 0, state
        return max(0, base_power * percent // 100), state






    def _apply_invasion_result(self, area: Dict[str, Any], power: int, mode: int, hero: Optional[Character]) -> tuple[bool, str]:
        self._apply_invasion_action_cost(mode)
        sinkou, prestige_state, detail_parts = self._prepare_invasion_result_context(power, mode, hero)
        if sinkou <= 0:
            return False, f"威望值是【{prestige_state}】，侵攻失败。"
        sinkou, event_messages, interrupted = self._run_invasion_event(area, mode, sinkou, hero)
        if event_messages:
            detail_parts.extend(event_messages)
        if interrupted:
            return False, "\n".join(detail_parts)

        return self._finish_invasion_result(area, mode, sinkou, hero, detail_parts)






    def _apply_invasion_rewards(self, area: Dict[str, Any], mode: int, sinkou: int, hero: Optional[Character]) -> List[str]:
        reward_sinkou = self._get_invasion_reward_sinkou(area, sinkou)
        loot = self._get_invasion_loot_value(mode, reward_sinkou)
        exp_gain = self._get_invasion_exp_gain(mode, reward_sinkou)
        conquered = self._get_invasion_conquer_state(area) != 0
        messages: List[str] = []
        if loot > 0:
            self._add_global_money(loot)
            messages.append(self._build_invasion_loot_message(mode, loot, conquered))

        if exp_gain > 0:
            messages.extend(self._apply_invasion_rewards_exp_gain(mode, exp_gain, hero))

        karma_message = self._apply_invasion_karma_effect(hero, mode)
        if karma_message:
            messages.append(karma_message)
        capture_message = self._maybe_apply_invasion_capture_reward(mode)
        if capture_message:
            messages.append(capture_message)

        return messages






    def _apply_invasion_rewards_exp_gain(self, mode: int, exp_gain: int, hero: Optional[Character]) -> List[str]:
        player = self._get_player()
        if mode == 1 and player is not None:
            player.exp[80] = player.exp.get(80, 0) + exp_gain
            return [f"{player.name} 获得了 {exp_gain} 点经验值。"]
        if hero is not None and mode in (2, 3):
            hero.exp[80] = hero.exp.get(80, 0) + exp_gain
            return [f"{hero.name} 获得了 {exp_gain} 点经验值。"]
        return []






    def _apply_invasion_stage_events(self, area_flag: int, progress: int) -> List[str]:
        event_flag = self._get_invasion_event_flag(area_flag)
        if event_flag is None:
            return []
        current_stage = int(self.interpreter.vars.get_flag(event_flag, 0))
        thresholds = self._get_invasion_event_thresholds(area_flag)
        rise_banner = self._find_invasion_stage_rise_banner(event_flag, progress, current_stage, thresholds)
        if rise_banner is not None:
            return rise_banner
        fall_banner = self._find_invasion_stage_fall_banner(event_flag, progress, current_stage, thresholds)
        if fall_banner is not None:
            return fall_banner
        return []






    def _build_hero_invasion_flavor_messages(self, area: Dict[str, Any], hero: Optional[Character]) -> List[str]:
        if hero is None:
            return []
        messages = [f"{hero.name}带着怪物到达了{area['name']}，尽可能地施暴着。"]
        talent_message = self._get_hero_invasion_talent_message(hero)
        if talent_message:
            messages.append(talent_message)
        return messages






    def _build_invasion_conquest_reward_lines(self, config: Dict[str, Any]) -> List[str]:
        return [
            "┌─────────────────────────────┐",
            f"｜{str(config['title']):^29}｜",
            f"｜{str(config['summary']):^29}｜",
            f"｜{str(config['demand']):^29}｜",
            "└─────────────────────────────┘",
        ]






    def _build_invasion_elite_battle_round_continue_result(
        self,
        hero_state: tuple[int, int, int, int],
        enemy_state: tuple[int, int, int, int],
    ) -> tuple[int, int, int, int, int, int, None]:
        return hero_state[0], hero_state[1], hero_state[2], hero_state[3], enemy_state[0], enemy_state[1], None






    def _build_invasion_elite_enemy(self) -> Character:
        enemy = Character()
        enemy.name = random.choice(["防御型精锐部队", "攻击型精锐部队"])
        enemy.callname = enemy.name
        defense_type = "防御型" in enemy.name
        enemy.base[0] = 9000 if defense_type else 7500
        enemy.base[1] = 9000 if defense_type else 7500
        enemy.maxbase[0] = enemy.base[0]
        enemy.maxbase[1] = enemy.base[1]
        enemy.cflag[11] = 150 if defense_type else 200
        enemy.cflag[12] = 200 if defense_type else 150
        return enemy






    def _build_invasion_event_banner(self, text: str) -> List[str]:
        edge = "*" * 91
        middle = f"*********{text:^74}**********"
        return [edge, edge, middle, edge, edge]






    def _build_invasion_fort_assault_intro_messages(self, context: Dict[str, Any]) -> List[str]:
        return [f"魔王军向着{context['fort_name']}发起了最为猛烈的进攻。"]






    def _build_invasion_fort_event_context(self, area: Dict[str, Any], hero: Optional[Character]) -> Dict[str, Any]:
        if area.get("global_area"):
            return self._get_invasion_fort_context({"area_flag": 101, "name": area["name"]}, hero)
        return self._get_invasion_fort_context(area, hero)






    def _build_invasion_loot_message(self, mode: int, loot: int, conquered: bool) -> str:
        if mode == 0:
            return f"{'强制征收了' if conquered else '得到了'} {loot} 点！"
        if mode == 3:
            return f"{'强行征收到了' if conquered else '获得了'} {loot} 点的战利品！"
        return f"{'强制征收了' if conquered else '得到了'} {loot} 点战利品！"






    def _build_invasion_mode_flavor_messages(
        self,
        area: Dict[str, Any],
        mode: int,
        sinkou: int,
        hero: Optional[Character],
    ) -> List[str]:
        if mode == 1:
            return self._build_magic_invasion_flavor_messages(sinkou)
        if mode == 2:
            return self._build_hero_invasion_flavor_messages(area, hero)
        if mode == 3:
            return self._build_raid_invasion_flavor_messages(area, hero)
        return []






    def _build_invasion_progress_message(self, gain: int) -> str:
        if gain > 0:
            return f"侵攻度提升 {gain} 点。"
        return "侵攻度没有提升。"






    def _build_magic_invasion_flavor_messages(self, sinkou: int) -> List[str]:
        player = self._get_player()
        player_name = player.name if player is not None and player.name else "魔王"
        if sinkou < 100:
            effect = f"{sinkou}点魔力形成飓风，将大树吹倒了！"
        elif sinkou < 300:
            effect = f"{sinkou}点魔力形成火焰，将平原焚烧殆尽！"
        elif sinkou < 600:
            effect = f"{sinkou}点魔力形成雷霆，将附近的村庄彻底摧毁！"
        elif sinkou < 900:
            effect = f"{sinkou}点魔力形成洪水，将城镇淹没！"
        elif sinkou < 1200:
            effect = f"{sinkou}点魔力形成剧毒气体，令骑士团窒息！"
        else:
            effect = f"{sinkou}点魔力形成纯粹能量，将城市吞没！"
        return [f"{player_name}的魔力爆发出来了！", effect]






    def _build_raid_invasion_flavor_messages(self, area: Dict[str, Any], hero: Optional[Character]) -> List[str]:
        if hero is None:
            return []
        return [f"{hero.name}得到了魔王的力量！{area['name']}被掠夺了。"]






    def _can_capture_invasion_enemy(self, area: Optional[Dict[str, Any]] = None) -> bool:
        if not self._can_spawn_daily_enemy():
            return False
        if area is None:
            return True
        if int(area.get("area_flag", 0) or 0) != 101:
            return True
        return len(self.interpreter.vars.chars) <= 90






    def _capture_invasion_enemy(self) -> Optional[Character]:
        if not self._can_capture_invasion_enemy():
            return None
        template_ids = self._get_daily_enemy_spawn_template_ids()
        if not template_ids:
            return None
        captured = self._create_character_from_template(random.choice(template_ids))
        if captured is None:
            return None
        self._prepare_captured_invasion_enemy(captured)
        return captured






    def _compose_invasion_result_message(
        self,
        area: Dict[str, Any],
        gain: int,
        updated: int,
        detail_parts: List[str],
        flavor_messages: List[str],
        reward_messages: List[str],
        completion_messages: List[str],
    ) -> str:
        message_parts = list(detail_parts)
        if flavor_messages:
            message_parts.extend(flavor_messages)
        if reward_messages:
            message_parts.extend(reward_messages)
        message_parts.append(self._build_invasion_progress_message(gain))
        if not area.get("global_area"):
            stage_messages = self._get_invasion_stage_messages(area, updated)
            if stage_messages:
                message_parts.extend(stage_messages)
        detail = "\n".join(message_parts)
        if updated >= 10000:
            detail = self._append_invasion_completion_line(detail, area)
        if completion_messages:
            detail += "\n" + "\n".join(completion_messages)
        return detail






    def _estimate_hero_invasion_power(self, hero: Character, raid_mode: bool = False) -> int:
        base_power = self._estimate_magic_invasion_power() if raid_mode else self._estimate_monster_invasion_power("third")
        level_bonus = self._get_invasion_level_bonus_percent(hero)
        return max(0, base_power * level_bonus // 100)






    def _estimate_magic_invasion_power(self) -> int:
        player = self._get_player()
        if player is None:
            return 0
        return max(0, player.base.get(1, 0) // 25)






    def _estimate_monster_invasion_power(self, mode: str) -> int:
        stock = self._get_monster_stock()
        if not stock:
            return 0
        divisor = 2 if mode == "half" else 3
        sinkou = 0
        for monster_id, count in stock.items():
            current_count = max(0, int(count))
            if current_count <= 0:
                continue
            remaining_count = current_count // divisor
            monster_attack = self._get_invasion_monster_attack_value(int(monster_id))
            sinkou += monster_attack * ((remaining_count // 9) + 1)
        return max(0, sinkou // 20)






    def _find_invasion_stage_fall_banner(
        self,
        event_flag: int,
        progress: int,
        current_stage: int,
        thresholds: List[Dict[str, Any]],
    ) -> Optional[List[str]]:
        for entry in thresholds:
            level = int(entry["level"])
            fall = int(entry["fall"])
            if progress <= fall and current_stage == level + 1:
                self.interpreter.vars.set_flag(event_flag, level)
                return self._build_invasion_event_banner(str(entry["fall_text"]))
        return None






    def _find_invasion_stage_rise_banner(
        self,
        event_flag: int,
        progress: int,
        current_stage: int,
        thresholds: List[Dict[str, Any]],
    ) -> Optional[List[str]]:
        for entry in reversed(thresholds):
            level = int(entry["level"])
            rise = int(entry["rise"])
            if progress >= rise and current_stage == level:
                self.interpreter.vars.set_flag(event_flag, level + 1)
                return self._build_invasion_event_banner(str(entry["rise_text"]))
        return None






    def _finish_invasion_challenge_hero_duel_escape_or_capture(
        self,
        area: Dict[str, Any],
        hero: Character,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        if self._get_flag_bit(5, 7) and self._get_invasion_conquer_state(area) == 0:
            self._set_character_ntr_captive_state(hero)
            messages.append(f"晕过去的{hero.name}成为了敌方的俘虏。")
        else:
            self._set_character_invasion_retreat_standby_state(hero)
            messages.append(f"{hero.name}苏醒后原路返回了。")
        return 0, messages, True






    def _finish_invasion_challenge_hero_duel_leaderless_retreat(self, messages: List[str]) -> tuple[int, List[str], bool]:
        messages.append("失去指挥官的魔王军只好撤退了。")
        return 0, messages, True






    def _finish_invasion_challenge_hero_duel_minor_loss(
        self,
        hero: Character,
        messages: List[str],
        sinkou: int,
    ) -> tuple[int, List[str], bool]:
        hero.base[0] = max(0, hero.base.get(0, 0) // 10)
        messages.append(f"{hero.name}体力-90%，但仍继续前进。")
        return sinkou, messages, False






    def _finish_invasion_challenge_hero_duel_minor_win(
        self,
        hero: Character,
        messages: List[str],
        sinkou: int,
    ) -> tuple[int, List[str], bool]:
        hero.exp[80] = hero.exp.get(80, 0) + 500
        hero.base[0] = max(0, hero.base.get(0, 0) // 2)
        messages.append(f"{hero.name}经验+500，体力-50%。")
        return sinkou, messages, False






    def _finish_invasion_challenge_maou_duel_capture(
        self,
        area: Dict[str, Any],
        sinkou: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        captured = self._spawn_invasion_challenge_captive(area)
        self._spend_global_money(3000)
        self.interpreter.vars.globals[95] = int(self.interpreter.vars.globals.get(95, 0)) | self._get_invasion_challenge_flag_mask(area)
        if captured is not None:
            messages.append(f"{captured.name}被魔王抓住了。金钱-3000。")
        else:
            messages.append("挑战者被魔王抓住了。金钱-3000。")
        return sinkou, messages, False






    def _finish_invasion_challenge_maou_duel_defeat(self, player: Character, messages: List[str]) -> tuple[int, List[str], bool]:
        player.base[0] = 0
        player.base[1] = 0
        messages.append("魔王在决斗中重伤倒下，体力与气力清空，侵攻中止。")
        return 0, messages, True






    def _finish_invasion_challenge_maou_duel_safe_exit(self, sinkou: int, messages: List[str]) -> tuple[int, List[str], bool]:
        return sinkou, messages, False






    def _finish_invasion_challenge_maou_duel_victory(
        self,
        player: Character,
        hero: Optional[Character],
        sinkou: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        player.base[1] = max(0, player.base.get(1, 0) // 2)
        player.exp[80] = player.exp.get(80, 0) + 500
        messages.append("魔王堂堂正正地取得了胜利。魔王气力减半，魔王经验+500。")
        return sinkou, messages, False






    def _finish_invasion_elite_battle_defeat(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        if self._get_flag_bit(5, 7):
            self._set_character_ntr_captive_state(hero)
        else:
            self._set_character_invasion_retreat_standby_state(hero)
        self._sync_invasion_elite_battle_state(hero, sinkou, hero_hp, hero_mp, hero_atk, hero_def)
        messages.append(f"魔王军被{enemy.name}击溃了，{hero.name}{'也被俘虏了' if hero.cflag.get(1, 0) == 9 else '逃了回来'}。")
        return 0, messages, True






    def _finish_invasion_elite_battle_surrender(
        self,
        hero: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        self._set_character_ntr_captive_state(hero)
        self._sync_invasion_elite_battle_state(hero, sinkou, hero_hp, hero_mp, hero_atk, hero_def)
        messages.append(f"被狂王俘虏过的{hero.name}丧失了战意，抛下武器投降了。")
        return 0, messages, True






    def _finish_invasion_elite_battle_timeout(
        self,
        hero: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        exp_gain = max(0, sinkou // 10)
        hero.exp[80] = hero.exp.get(80, 0) + exp_gain
        self._sync_invasion_elite_battle_state(hero, sinkou, hero_hp, hero_mp, hero_atk, hero_def)
        messages.extend([
            "………",
            "……",
            "…",
            "没有时间了，战线已经不可能再维持下去了！",
            f"{hero.name}的部队开始后退，怪物们在后退中溃散着。",
        ])
        if exp_gain > 0:
            messages.append(f"{hero.name}获得了{exp_gain}点经验值！")
        return 0, messages, True






    def _finish_invasion_elite_battle_victory(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        exp_gain = max(0, sinkou // 5)
        hero.exp[80] = hero.exp.get(80, 0) + exp_gain
        messages.append(f"{hero.name}率领的魔王军击溃了{enemy.name}。")
        if exp_gain > 0:
            messages.append(f"{hero.name}获得了{exp_gain}点经验值！")
        self._sync_invasion_elite_battle_state(hero, sinkou, hero_hp, hero_mp, hero_atk, hero_def)
        return sinkou, messages, False






    def _finish_invasion_result(
        self,
        area: Dict[str, Any],
        mode: int,
        sinkou: int,
        hero: Optional[Character],
        detail_parts: List[str],
    ) -> tuple[bool, str]:
        gain = self._get_invasion_progress_gain(mode, sinkou)
        current = self._get_invasion_area_progress(area)
        updated = min(10000, current + gain)
        self._set_invasion_area_progress(area, updated)

        flavor_messages = self._build_invasion_mode_flavor_messages(area, mode, sinkou, hero)
        reward_messages = self._apply_invasion_rewards(area, mode, sinkou, hero)
        self._apply_invasion_prestige_gain(2)
        freshly_conquered = self._mark_invasion_completion(area, updated)
        completion_messages = self._get_invasion_completion_check_messages(freshly_conquered)
        return True, self._compose_invasion_result_message(
            area,
            gain,
            updated,
            detail_parts,
            flavor_messages,
            reward_messages,
            completion_messages,
        )






    def _get_global_invasion_area_display_name(self, area_flag: int, conquer_state: int) -> Optional[str]:
        if area_flag != 101:
            return None
        godness_stage = int(self.interpreter.vars.globals.get(2810, 0))
        if self._is_global_invasion_area_conquered(area_flag, conquer_state):
            return "淫乱意志的神宫"
        if 1 <= conquer_state < 4:
            return "天神宫广场"
        if (501 <= godness_stage < 540) or (541 <= godness_stage < 560):
            return "天神宫"
        return None




    def _get_hero_invasion_talent_message(self, hero: Character) -> Optional[str]:
        player = self._get_player()
        player_name = player.name if player is not None and player.name else "魔王"
        if hero.talent.get(160, 0):
            return f"{hero.name}在侵略的时候依旧全程保持着慈爱的笑容，她终于明白到一切都是为了{player_name}而存在的……"
        if hero.talent.get(161, 0):
            return f"{hero.name}身先士卒，第一个飞跳入战场里，而且最后毫发无损。"
        if hero.talent.get(162, 0):
            return f"{hero.name}是优秀的指挥官，带领着怪物们侵略了。"
        if hero.talent.get(163, 0):
            return f"{hero.name}穿着{player_name}赐予的被诅咒的铠甲，高声大笑着率领怪物们突击了……"
        if hero.talent.get(164, 0):
            return f"{hero.name}冷哼着耻笑跪求饶命的草民，随手将他们交给饥饿的巨兽了。"
        if hero.talent.get(165, 0):
            return f"{hero.name}一边发出异样的笑声，一边用手中的火把将四周都点燃了……"
        if hero.talent.get(166, 0):
            return f"{hero.name}把侵略时所抢夺的金银财宝都献给了{player_name}……"
        return None






    def _get_invasion_area_definitions(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 0, "area_flag": 81, "conquer_flag": 82, "name": "地上的魔界领土", "conquered_name": "地上的魔界领土", "action": "巡视地上的魔界领土（已征服）"},
            {"menu_id": 1, "area_flag": 86, "conquer_flag": 87, "name": "精灵族的领域", "conquered_name": "黑暗精灵的领土", "action": "入侵精灵族的领域"},
            {"menu_id": 2, "area_flag": 88, "conquer_flag": 89, "name": "龙之山脉", "conquered_name": "混沌龙之山", "action": "入侵龙之山脉"},
            {"menu_id": 3, "area_flag": 90, "conquer_flag": 91, "name": "天界", "conquered_name": "堕天使的淫界", "action": "入侵天界"},
            {"menu_id": 4, "area_flag": 92, "conquer_flag": 92, "name": "圣灵骑士的堡垒", "conquered_name": "圣灵骑士的卖春堡垒", "action": "攻略圣灵骑士的堡垒", "fort_area": True},
            {"menu_id": 5, "area_flag": 101, "conquer_flag": 102, "name": "天神宫", "conquered_name": "淫乱意志的神宫", "action": "攻略天神宫", "global_area": True},
        ]






    def _get_invasion_area_display_name(self, area: Dict[str, Any], include_status: bool = False) -> str:
        conquer_state = self._get_invasion_conquer_state(area)
        area_flag = int(area["area_flag"])
        if area.get("fort_area"):
            display_name = str(area.get("conquered_name") if conquer_state >= 15 else area["name"])
            if include_status and conquer_state >= 15:
                return f"{display_name}（已征服）"
            return display_name
        if area.get("global_area"):
            display_name = self._get_global_invasion_area_display_name(area_flag, conquer_state)
            if display_name is None:
                return str(area["action"])
            if include_status and self._is_global_invasion_area_conquered(area_flag, conquer_state):
                return f"{display_name}（已征服）"
            return display_name
        if conquer_state:
            conquered_name = str(area.get("conquered_name") or area["name"])
            if include_status:
                return f"{conquered_name}（已征服）"
            return conquered_name
        return str(area["name"])






    def _get_invasion_area_label(self, area: Dict[str, Any]) -> str:
        return self._get_invasion_area_display_name(area, include_status=True)






    def _get_invasion_area_menu_action_text(self, area: Dict[str, Any]) -> str:
        if area.get("fort_area"):
            if self._get_invasion_conquer_state(area) >= 15:
                return "巡视圣灵骑士的卖春堡垒（已征服）"
            return "攻略圣灵骑士的堡垒"
        if area.get("global_area"):
            conquer_state = self._get_invasion_conquer_state(area)
            if self._is_global_invasion_area_conquered(int(area["area_flag"]), conquer_state):
                return "巡视淫乱意志的神宫（已征服）"
            if 1 <= conquer_state < 4:
                return "天神宫广场"
            return "攻略天神宫"
        if self._get_invasion_conquer_state(area):
            return str(area["action"])
        return f"入侵{self._get_invasion_area_display_name(area)}"






    def _get_invasion_area_progress(self, area: Dict[str, Any]) -> int:
        if area.get("fort_area"):
            return 10000 if self._get_invasion_conquer_state(area) >= 15 else 0
        if area.get("global_area"):
            return int(self.interpreter.vars.globals.get(int(area["area_flag"]), 0))
        return self.interpreter.vars.get_flag(int(area["area_flag"]), 0)






    def _get_invasion_capture_chance(self, mode: int) -> int:
        if mode == 0:
            return 5
        if mode == 2:
            return 9
        return 0






    def _get_invasion_challenge_context(self, area: Dict[str, Any]) -> Dict[str, Any]:
        area_flag = int(area["area_flag"])
        contexts = {
            81: {"area_name": "人间界", "pass_name": "一座河边的桥", "enemy_name": "女骑士", "leave_text": "骑上战马一骑绝尘离开了", "skill_text": "剑术非常高超", "template_ids": [9]},
            86: {"area_name": "精灵森林", "pass_name": "一条密林中的狭道", "enemy_name": "月之祭司", "leave_text": "遁入密林之中消失了", "skill_text": "箭术无比精准", "template_ids": [12, 16]},
            88: {"area_name": "龙之山脉", "pass_name": "一座山谷间的吊桥", "enemy_name": "龙族巫女", "leave_text": "吟唱了传送咒语凭空消失了", "skill_text": "龙语魔法无比犀利", "template_ids": [10, 14]},
            90: {"area_name": "天界", "pass_name": "一座天界的虹桥", "enemy_name": "女武神", "leave_text": "振起洁白的羽翅飞走了", "skill_text": "圣力极其雄厚", "template_ids": [1, 5]},
            101: {"area_name": "天神宫", "pass_name": "一座天界的虹桥", "enemy_name": "十字军", "leave_text": "振起洁白的羽翅飞走了", "skill_text": "圣力极其雄厚", "template_ids": [1, 5]},
        }
        return contexts.get(area_flag, {"area_name": str(area["name"]), "pass_name": "要道", "enemy_name": "挑战者", "leave_text": "转身离开了", "skill_text": "战技极其高超", "template_ids": [1]})






    def _get_invasion_challenge_flag_mask(self, area: Dict[str, Any]) -> int:
        return {
            81: 1,
            86: 2,
            88: 4,
            90: 8,
            101: 16,
        }.get(int(area["area_flag"]), 0)






    def _get_invasion_completion_check_messages(self, freshly_conquered: set[int]) -> List[str]:
        return self._apply_invasion_completion_check(freshly_conquered)






    def _get_invasion_conquer_state(self, area: Dict[str, Any]) -> int:
        if area.get("fort_area"):
            return int(self.interpreter.vars.get_flag(int(area["conquer_flag"]), 0))
        if area.get("global_area"):
            return int(self.interpreter.vars.globals.get(int(area["conquer_flag"]), 0))
        return int(self.interpreter.vars.get_flag(int(area["conquer_flag"]), 0))




    def _get_invasion_conquest_reward_config(self, area_flag: int) -> Optional[Dict[str, Any]]:
        configs = {
            **self._get_invasion_conquest_reward_config_primary(),
            **self._get_invasion_conquest_reward_config_tribute(),
        }
        return configs.get(int(area_flag))






    def _get_invasion_conquest_reward_config_primary(self) -> Dict[int, Dict[str, Any]]:
        return {
            81: {
                "title": "魔王终于再次掌握了世界。",
                "summary": "魔物们冲入皇宫，将还在熟睡中的年幼公主拖下床抓了起来。",
                "demand": "你命令人类继续派出勇者到地下城来讨伐自己。",
                "template_id": 35,
                "start_flag": 82,
                "final_flag": 82,
                "final_value": 1,
                "gain_text": "人类皇族公主菲娅，被你抓获了。",
                "label": "人类皇族公主",
            },
        }






    def _get_invasion_conquest_reward_config_tribute(self) -> Dict[int, Dict[str, Any]]:
        return INVASION_CONQUEST_REWARD_CONFIG_TRIBUTE






    def _get_invasion_elite_battle_enemy_turn_result(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        hero_surrender: bool,
        messages: List[str],
    ) -> Optional[tuple[int, List[str], bool]]:
        if hero_surrender and hero_mp <= 1000:
            return self._set_invasion_elite_battle_round_result(
                "surrender",
                hero,
                enemy,
                sinkou,
                hero_hp,
                hero_mp,
                hero_atk,
                hero_def,
                messages,
            )
        if hero_hp <= 300 or hero_mp <= 0:
            return self._set_invasion_elite_battle_round_result(
                "defeat",
                hero,
                enemy,
                sinkou,
                hero_hp,
                hero_mp,
                hero_atk,
                hero_def,
                messages,
            )
        return None






    def _get_invasion_elite_battle_hero_turn_result(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        enemy_hp: int,
        enemy_mp: int,
        messages: List[str],
    ) -> Optional[tuple[int, List[str], bool]]:
        if enemy_hp <= 100 or enemy_mp <= 0:
            return self._set_invasion_elite_battle_round_result(
                "victory",
                hero,
                enemy,
                sinkou,
                hero_hp,
                hero_mp,
                hero_atk,
                hero_def,
                messages,
            )
        return None






    def _get_invasion_event_flag(self, area_flag: int) -> Optional[int]:
        return {
            81: 93,
            86: 94,
            88: 95,
            90: 96,
        }.get(int(area_flag))






    def _get_invasion_event_thresholds(self, area_flag: int) -> List[Dict[str, Union[int, str]]]:
        return INVASION_EVENT_THRESHOLD_TABLES.get(int(area_flag), [])






    def _get_invasion_exp_gain(self, mode: int, sinkou: int) -> int:
        if mode == 1:
            return max(0, sinkou // 2)
        if mode == 2:
            return max(0, sinkou // 2)
        if mode == 3:
            return max(0, sinkou // 20)
        return 0






    def _get_invasion_fort_context(self, area: Dict[str, Any], hero: Optional[Character]) -> Dict[str, Any]:
        race = int(hero.talent.get(314, 0)) if hero is not None else -1
        area_flag = int(area["area_flag"])
        contexts = {
            81: {"area_name": "人间界", "army_name": "人类军队", "fort_name": "城堡", "race_match": race == 0},
            86: {"area_name": "精灵森林", "army_name": "精灵族战士", "fort_name": "精灵城寨", "race_match": race == 1},
            88: {"area_name": "龙之山脉", "army_name": "龙族战士", "fort_name": "战争堡垒", "race_match": race == 5},
            90: {"area_name": "天界", "army_name": "天界卫队", "fort_name": "天使要塞", "race_match": race == 6},
            101: {"area_name": "天神宫", "army_name": "十字军", "fort_name": "天使要塞", "race_match": race == 6},
        }
        return contexts.get(area_flag, {"area_name": str(area["name"]), "army_name": "守军", "fort_name": "要塞", "race_match": False})






    def _get_invasion_fort_context_fields(self, area: Dict[str, Any], hero: Optional[Character]) -> tuple[str, str, str, bool]:
        context = self._get_invasion_fort_context(area, hero)
        return (
            str(context["area_name"]),
            str(context["army_name"]),
            str(context["fort_name"]),
            bool(context.get("race_match")),
        )






    def _get_invasion_level_bonus_percent(self, char: Character) -> int:
        return 100 + max(0, int(char.cflag.get(9, 0)))






    def _get_invasion_loot_value(self, mode: int, sinkou: int) -> int:
        if mode == 0:
            return max(0, sinkou * 10)
        if mode == 2:
            return max(0, sinkou * 5)
        if mode == 3:
            return max(0, sinkou)
        return 0






    def _get_invasion_medal_bonus(self, hero: Optional[Character]) -> tuple[int, Optional[str]]:
        if hero is None:
            return 100, None
        medals = int(hero.exp.get(81, 0))
        if medals > 500:
            return 160, f"{hero.name}的勋章补正 x1.60"
        if medals > 250:
            return 150, f"{hero.name}的勋章补正 x1.50"
        if medals > 150:
            return 140, f"{hero.name}的勋章补正 x1.40"
        if medals > 100:
            return 130, f"{hero.name}的勋章补正 x1.30"
        if medals > 60:
            return 120, f"{hero.name}的勋章补正 x1.20"
        if medals > 40:
            return 110, f"{hero.name}的勋章补正 x1.10"
        if medals > 30:
            return 105, f"{hero.name}的勋章补正 x1.05"
        if medals > 20:
            return 104, f"{hero.name}的勋章补正 x1.04"
        if medals > 15:
            return 103, f"{hero.name}的勋章补正 x1.03"
        if medals > 10:
            return 102, f"{hero.name}的勋章补正 x1.02"
        if medals > 5:
            return 101, f"{hero.name}的勋章补正 x1.01"
        return 100, None






    def _get_invasion_mode_prestige_detail(self, mode: int, prestige_state: str) -> List[str]:
        if mode in (0, 1):
            return [f"威望值是【{prestige_state}】"]
        return []






    def _get_invasion_monster_attack_value(self, monster_id: int) -> int:
        data = self._get_monster_data_baseline(monster_id)
        if data is None:
            return 3
        attack = int(data.get(2, 0)) + int(data.get(3, 0)) + int(data.get(4, 0))
        if int(data.get(5, 0)) != 0:
            attack += int(data.get(1, 0))
        if int(data.get(6, 0)) != 0:
            attack += int(data.get(1, 0))
        return max(0, attack)






    def _get_invasion_prestige_state(self) -> tuple[str, int]:
        prestige = self._get_prestige_value()
        if prestige <= 20:
            return "岌岌可危", 0
        if prestige <= 40:
            return "动荡不安", 25
        if prestige <= 60:
            return "略受质疑", max(0, 100 + (prestige - 60) * 2)
        if prestige <= 80:
            return "相安无事", 100
        return "广受爱戴", 100 + (prestige - 80)






    def _get_invasion_progress_gain(self, mode: int, sinkou: int) -> int:
        if mode == 3:
            return max(0, sinkou // 20)
        return max(0, sinkou)






    def _get_invasion_reward_sinkou(self, area: Dict[str, Any], sinkou: int) -> int:
        if self._get_invasion_conquer_state(area) == 0:
            return max(0, sinkou)
        return min(max(0, sinkou), 10000 * 10)






    def _get_invasion_stage_messages(self, area: Dict[str, Any], updated: int) -> List[str]:
        return self._apply_invasion_stage_events(int(area["area_flag"]), updated)






    def _grant_invasion_conquest_character(self, template_id: int) -> tuple[bool, str]:
        if self._find_character_by_template_id(template_id) is not None:
            return True, "对应角色已经在队伍中了。"
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            return False, "奴隶太多了！"
        new_char = self._create_character_from_template(template_id)
        if new_char is None:
            return False, "角色模板不存在。"
        return True, f"{new_char.name} 加入了队伍。"






    def _grant_invasion_conquest_reward(self, area_flag: int) -> List[str]:
        return self._resolve_invasion_conquest_reward(area_flag)






    def _handle_invasion_area_mode_choice(
        self,
        area: Dict[str, Any],
        mode_choice: str,
        monster_count: int,
    ) -> Optional[tuple[int, Optional[Character], int]]:
        try:
            mode = int(mode_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None

        if mode not in (0, 1, 2, 3):
            print("\nInvalid selection.")
            self._pause()
            return None

        result = self._prepare_invasion_area_action(area, mode, monster_count)
        if result is None:
            return None
        power, hero = result
        return power, hero, mode






    def _handle_invasion_area_selection(self, choice: str, areas: List[Dict[str, Any]]) -> bool:
        try:
            menu_id = int(choice)
        except ValueError:
            return False

        area = next((entry for entry in areas if entry["menu_id"] == menu_id), None)
        if area is None:
            return False
        if not self._is_invasion_area_available(area):
            return False
        if area.get("fort_area"):
            self._show_arcana_fort_menu(area)
            return True

        self._prepare_invasion_area_entry(area)
        self._show_invasion_area_menu(area)
        return True






    def _handle_invasion_menu_choice(self, choice: str, areas: List[Dict[str, Any]]) -> tuple[bool, bool]:
        command_result = self._handle_invasion_menu_command_choice(choice)
        if command_result[0]:
            return command_result
        if self._handle_invasion_area_selection(choice, areas):
            return True, False
        return False, False






    def _handle_invasion_menu_command_choice(self, choice: str) -> tuple[bool, bool]:
        if choice == "999":
            return True, True
        if choice == "1000":
            self._show_video_campaign_menu()
            return True, False
        if choice == "9":
            self._show_campaign_menu()
            return True, False
        return False, False






    def _handle_shop_main_menu_invasion_choice(self, choice: str) -> Optional[tuple[bool, Optional[str]]]:
        if choice != "109":
            return None
        if self.show_invasion():
            return True, "SHOP"
        return True, None






    def _is_global_invasion_area_conquered(self, area_flag: int, conquer_state: int) -> bool:
        return area_flag == 101 and conquer_state >= 4




    def _is_invasion_area_available(self, area: Dict[str, Any]) -> bool:
        if area.get("fort_area"):
            return True
        if not area.get("global_area"):
            return True
        return self._get_global_invasion_area_display_name(int(area["area_flag"]), self._get_invasion_conquer_state(area)) is not None






    def _list_invasion_hero_candidates(self, raid_mode: bool = False) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        allow_pregnant = self._get_flag_bit(5, 10)
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0 or char.base.get(0, 0) < 1:
                continue
            if char.talent.get(153, 0) and not allow_pregnant:
                continue
            if raid_mode:
                if char.cflag.get(1, 0) != 0:
                    continue
                if char.cflag.get(0, 0) == 0 and not char.talent.get(254, 0):
                    continue
            else:
                if char.cflag.get(0, 0) != 2:
                    continue
                if char.cflag.get(1, 0) not in (0, 7):
                    continue
                if not (char.talent.get(85, 0) or char.talent.get(76, 0)):
                    continue
            candidates.append((idx, char))
        return candidates






    def _mark_invasion_completion(self, area: Dict[str, Any], updated: int) -> set[int]:
        freshly_conquered: set[int] = set()
        if updated >= 10000:
            if not area.get("global_area"):
                self._set_invasion_conquered(area, True)
            freshly_conquered.add(int(area["area_flag"]))
        return freshly_conquered






    def _maybe_apply_invasion_capture_reward(self, mode: int) -> Optional[str]:
        capture_chance = self._get_invasion_capture_chance(mode)
        if capture_chance <= 0 or random.randrange(100) >= capture_chance:
            return None
        if mode == 2:
            self._add_prestige_value(1)
        captured = self._capture_invasion_enemy()
        if captured is None:
            return "好像抓到了负隅顽抗的勇者……但俘虏被赏赐给部下了。"
        return f"好像抓到了负隅顽抗的勇者……{captured.name} 被带回了地下城。"






    def _maybe_run_invasion_elite_battle(
        self,
        area: Dict[str, Any],
        mode: int,
        sinkou: int,
        hero: Optional[Character],
        event_roll: int,
    ) -> tuple[int, List[str], bool]:
        if mode != 2 or hero is None or area.get("global_area") or event_roll != 8:
            return sinkou, [], False
        area_progress = self._get_invasion_area_progress(area)
        conquer_state = self._get_invasion_conquer_state(area)
        if conquer_state != 0:
            return sinkou, [], False
        if area_progress < 5000:
            return sinkou, ["………", "……", "…", "传闻中的精锐部队并没有出现…………"], False
        if random.randint(0, max(0, area_progress) - 1) <= 2000:
            return sinkou, ["………", "……", "…", "传闻中的精锐部队并没有出现…………"], False
        return self._resolve_invasion_elite_battle(hero, sinkou)






    def _prepare_captured_invasion_enemy(self, captured: Character) -> None:
        self._normalize_spawned_hero_identity(captured)
        self._apply_spawned_hero_template_overrides(captured)
        self._set_character_captured_standby_state(captured)
        captured.cflag[508] = 3
        self._assign_invading_hero_spawn_position(captured)
        captured.base[0] = int(captured.maxbase.get(0, captured.base.get(0, 0)))
        captured.base[1] = int(captured.maxbase.get(1, captured.base.get(1, 0)))






    def _prepare_invasion_area_action(
        self,
        area: Dict[str, Any],
        mode: int,
        monster_count: int,
    ) -> Optional[tuple[int, Optional[Character]]]:
        if mode in (0, 2) and monster_count < 600:
            print("\n怪物数量不足。至少需要 600 只。")
            self._pause()
            return None

        hero: Optional[Character] = None
        if mode == 0:
            power = self._estimate_monster_invasion_power("half")
        elif mode == 1:
            power = self._estimate_magic_invasion_power()
        else:
            raid_mode = mode == 3
            hero = self._prompt_invasion_hero(raid_mode=raid_mode)
            if hero is None:
                return None
            power = self._estimate_hero_invasion_power(hero, raid_mode=raid_mode)
        return power, hero






    def _prepare_invasion_area_entry(self, area: Dict[str, Any]) -> None:
        if not area.get("global_area"):
            return
        area_flag = int(area["area_flag"])
        conquer_flag = int(area["conquer_flag"])
        if area_flag != 101:
            return
        current_state = int(self.interpreter.vars.globals.get(conquer_flag, 0))
        if current_state >= 3:
            self.interpreter.vars.globals[conquer_flag] = current_state + 1






    def _prepare_invasion_elite_battle(self, hero: Character, sinkou: int) -> tuple[Character, Dict[str, int], List[str]]:
        enemy = self._build_invasion_elite_enemy()
        battle_state = {
            "hero_hp": max(1, int(hero.base.get(0, 0))) + sinkou,
            "hero_mp": max(1, int(hero.base.get(1, 0))) + sinkou,
            "hero_atk": max(1, int(hero.cflag.get(11, 0))),
            "hero_def": max(0, int(hero.cflag.get(12, 0))),
            "enemy_hp": max(1, int(enemy.base.get(0, 0))),
            "enemy_mp": max(1, int(enemy.base.get(1, 0))),
            "enemy_atk": max(1, int(enemy.cflag.get(11, 0))),
            "enemy_def": max(0, int(enemy.cflag.get(12, 0))),
            "hero_surrender": bool(hero.talent.get(280, 0) and self._get_flag_bit(5, 7)),
        }
        messages = ["………", "……", "…", "精锐部队出现了！"]
        return enemy, battle_state, messages






    def _prepare_invasion_result_context(
        self,
        power: int,
        mode: int,
        hero: Optional[Character],
    ) -> tuple[int, str, List[str]]:
        sinkou, prestige_state = self._apply_invasion_mode_prestige_context(power, mode)
        detail_parts = self._get_invasion_mode_prestige_detail(mode, prestige_state)
        if sinkou <= 0:
            return sinkou, prestige_state, detail_parts
        if hero is not None:
            sinkou, hero_medal_message = self._apply_invasion_character_medal_bonus(sinkou, hero)
            if hero_medal_message:
                detail_parts.append(hero_medal_message)
        sinkou, master_level_message = self._apply_invasion_master_level_bonus(sinkou)
        if master_level_message:
            detail_parts.append(master_level_message)
        sinkou, knowledge_messages = self._apply_invasion_knowledge_bonus(sinkou)
        detail_parts.extend(knowledge_messages)
        player = self._get_player()
        if player is not None:
            sinkou, master_medal_message = self._apply_invasion_character_medal_bonus(sinkou, player)
            if master_medal_message:
                detail_parts.append(master_medal_message)
        return sinkou, prestige_state, detail_parts






    def _prompt_invasion_area_mode_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_invasion_challenge_maou_duel_cash_choice(self) -> bool:
        print("但对方看起来也不是省油的灯，未必能稳操胜券。")
        print("好在魔王身上携带了些一次性魔法道具，虽然价格昂贵但威力巨大。")
        print("魔王考虑着是否要在决斗中使用这些道具……")
        print(" [1] 使用氪金道具")
        print(" [2] 堂堂正正一决胜负")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                return True
            if choice == "2":
                return False






    def _prompt_invasion_challenge_strategy(self, hero: Character, context: Dict[str, Any]) -> int:
        print()
        print(f"魔王军浩浩荡荡地向{context['area_name']}进发着，却在{context['pass_name']}前停下了脚步。")
        print(f"原来是一名{context['enemy_name']}在大军的前方挡住了道路。")
        print(f"面对{context['enemy_name']}的挑衅，{hero.name}决定……")
        print(" [1] 召唤魔王应战")
        print(" [2] 亲自上前处理")
        print(" [3] 无视，全军进攻")
        while True:
            choice = self._prompt_choice()
            if choice in {"1", "2", "3"}:
                return int(choice)






    def _prompt_invasion_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_invasion_fort_strategy(self, mode: int, hero: Character, context: Dict[str, Any]) -> int:
        print()
        if mode == 2:
            print(f"魔王军浩浩荡荡地向{context['area_name']}进发着。")
            print(f"早有准备的{context['army_name']}在必经之路上建起了一座{context['fort_name']}。")
            print(f"{context['fort_name']}看起来防御坚固防备森严，于是{hero.name}决定……")
            print(" [1] 全军强攻")
            print(" [2] 亲自潜入")
            print(" [3] 绕路")
            while True:
                choice = self._prompt_choice()
                if choice in {"1", "2", "3"}:
                    return int(choice)
        print(f"{hero.name}向{context['area_name']}进发着，却在必经之路上遇到了{context['army_name']}建起的一座{context['fort_name']}。")
        print(f"{context['fort_name']}看起来防御坚固防备森严，于是{hero.name}决定……")
        print(" [1] 偷偷潜入")
        print(" [2] 绕路")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                return 2
            if choice == "2":
                return 3






    def _prompt_invasion_hero(self, raid_mode: bool) -> Optional[Character]:
        candidates = self._list_invasion_hero_candidates(raid_mode=raid_mode)
        if not candidates:
            print("\n没有勇者可进行侵攻。")
            self._pause()
            return None
        print("\n派遣谁去侵攻呢？")
        for idx, char in candidates:
            print(f" [{idx}] {char.name}  LV{self._get_character_level(char)}")
        print(" [999] Back")
        hero_choice = self._prompt_choice()
        if hero_choice == "999":
            return None
        try:
            hero_idx = int(hero_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        selected = next(((idx, char) for idx, char in candidates if idx == hero_idx), None)
        if selected is None:
            print("\nInvalid selection.")
            self._pause()
            return None
        return selected[1]






    def _render_invasion_area_menu(self, area: Dict[str, Any], monster_count: int) -> None:
        print(f"\n【{self._get_invasion_area_label(area)}】")
        print("-" * 30)
        print(f" 侵攻度: {self._format_progress_bar(self._get_invasion_area_progress(area))}")
        player = self._get_player()
        if player is not None:
            print(f" 魔王气力: {player.base.get(1, 0)}/{player.maxbase.get(1, 0)}")
        print(f" 怪物数量: {monster_count}")
        print(" [0] 使用现有怪物的一半去进攻（资金・俘虏）")
        print(" [1] 使用魔王的魔力（经验值）")
        print(" [2] 派遣勇者带三分之一的怪物去进攻（资金・经验值・俘虏）")
        print(" [3] 派遣勇者前去掠夺资金（资金・经验值）")
        print(" [999] Back")






    def _render_invasion_menu(self, areas: List[Dict[str, Any]]) -> None:
        print("\n【Invasion】")
        print("-" * 30)
        for area in areas:
            if not self._is_invasion_area_available(area):
                continue
            progress = self._get_invasion_area_progress(area)
            action_text = self._get_invasion_area_menu_action_text(area)
            print(f" [{area['menu_id']}] {action_text}  {self._format_progress_bar(progress)}")
        print(" [9] 向著世界之外")
        print(f" [1000] 向城里投放水晶球 [{self._get_video_campaign_sent()}/{self._get_video_campaign_total()}]")
        print(" [999] Back")
        print("-" * 30)






    def _resolve_invasion_challenge_maou_duel_action(
        self,
        area: Dict[str, Any],
        hero: Optional[Character],
        player: Character,
        sinkou: int,
        use_cash: bool,
        can_capture: bool,
        roll: int,
        messages: List[str],
        context: Dict[str, Any],
    ) -> Optional[tuple[int, List[str], bool]]:
        if use_cash and can_capture and roll >= 2:
            return self._finish_invasion_challenge_maou_duel_capture(area, sinkou, messages)
        if use_cash:
            self._spend_global_money(3000)
            messages.append(f"{context['enemy_name']}提前察觉了魔王的动作并躲开了。金钱-3000。")
            return self._finish_invasion_challenge_maou_duel_safe_exit(sinkou, messages)
        if roll < 2:
            return self._finish_invasion_challenge_maou_duel_victory(player, hero, sinkou, messages)
        return None






    def _resolve_invasion_completion_messages(self, area: Dict[str, Any], updated: int) -> tuple[set[int], List[str]]:
        freshly_conquered: set[int] = set()
        if updated >= 10000:
            if not area.get("global_area"):
                self._set_invasion_conquered(area, True)
            freshly_conquered.add(int(area["area_flag"]))
        return freshly_conquered, self._get_invasion_completion_check_messages(freshly_conquered)






    def _resolve_invasion_conquest_reward(self, area_flag: int) -> List[str]:
        config = self._get_invasion_conquest_reward_config(area_flag)
        if config is None:
            return []
        messages = self._build_invasion_conquest_reward_lines(config)
        start_flag = int(config["start_flag"])
        final_flag = int(config["final_flag"])
        final_value = int(config["final_value"])
        if final_value > 1:
            self.interpreter.vars.set_flag(start_flag, 1)
        if final_value > 1:
            ok, result_message = self._resolve_conquest_gift_selection(config)
        else:
            ok, result_message = self._grant_invasion_conquest_character(int(config["template_id"]))
        if ok:
            self.interpreter.vars.set_flag(final_flag, final_value)
            messages.append(str(config["gain_text"]))
            if int(area_flag) == 81:
                self._queue_post_message_action({"kind": "human_conquest_followup"})
        else:
            messages.append(result_message)
        return messages






    def _resolve_invasion_elite_battle(self, hero: Character, sinkou: int) -> tuple[int, List[str], bool]:
        enemy, battle_state, messages = self._prepare_invasion_elite_battle(hero, sinkou)
        round_result = self._run_invasion_elite_battle_rounds(hero, enemy, sinkou, battle_state, messages)
        if round_result is not None:
            return round_result
        return self._finish_invasion_elite_battle_timeout(
            hero,
            sinkou,
            battle_state["hero_hp"],
            battle_state["hero_mp"],
            battle_state["hero_atk"],
            battle_state["hero_def"],
            messages,
        )






    def _resolve_invasion_elite_battle_enemy_turn_result(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_state: tuple[int, int, int, int],
        hero_surrender: bool,
        messages: List[str],
    ) -> Optional[tuple[int, List[str], bool]]:
        return self._get_invasion_elite_battle_enemy_turn_result(
            hero,
            enemy,
            sinkou,
            hero_state[0],
            hero_state[1],
            hero_state[2],
            hero_state[3],
            hero_surrender,
            messages,
        )






    def _resolve_invasion_elite_battle_hero_turn_result(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        enemy_state: tuple[int, int, int, int],
        messages: List[str],
    ) -> Optional[tuple[int, List[str], bool]]:
        return self._get_invasion_elite_battle_hero_turn_result(
            hero,
            enemy,
            sinkou,
            hero_hp,
            hero_mp,
            hero_atk,
            hero_def,
            enemy_state[0],
            enemy_state[1],
            messages,
        )






    def _resolve_invasion_elite_battle_round(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        enemy_hp: int,
        enemy_mp: int,
        enemy_atk: int,
        enemy_def: int,
        hero_surrender: bool,
        messages: List[str],
    ) -> Optional[tuple[int, int, int, int, int, int, tuple[int, List[str], bool]]]:
        enemy_state, round_result = self._advance_invasion_elite_battle_hero_phase(
            hero,
            enemy,
            sinkou,
            hero_hp,
            hero_mp,
            hero_atk,
            hero_def,
            enemy_hp,
            enemy_mp,
            enemy_atk,
            enemy_def,
            messages,
        )
        if round_result is not None:
            return round_result

        hero_state, round_result = self._advance_invasion_elite_battle_enemy_phase(
            hero,
            enemy,
            sinkou,
            enemy_state[2],
            hero_def,
            hero_hp,
            hero_mp,
            hero_surrender,
            messages,
        )
        if round_result is not None:
            return round_result
        return self._build_invasion_elite_battle_round_continue_result(hero_state, enemy_state)






    def _run_invasion_challenge_event(self, area: Dict[str, Any], mode: int, sinkou: int, hero: Optional[Character]) -> tuple[int, List[str], bool]:
        if mode not in (0, 2, 3):
            return sinkou, [], False
        flag_mask = self._get_invasion_challenge_flag_mask(area)
        if flag_mask and (int(self.interpreter.vars.globals.get(95, 0)) & flag_mask):
            return sinkou, [], False
        context = self._get_invasion_challenge_context(area)
        strategy = self._select_invasion_challenge_strategy(mode, hero, context)
        intro = [f"在前往{context['area_name']}的途中，{context['enemy_name']}挡在了{context['pass_name']}前。"]
        if strategy == 1:
            new_sinkou, messages, interrupted = self._apply_invasion_challenge_maou_duel(area, sinkou, hero)
            return new_sinkou, intro + messages, interrupted
        if strategy == 2 and hero is not None:
            new_sinkou, messages, interrupted = self._apply_invasion_challenge_hero_duel(area, mode, sinkou, hero)
            return new_sinkou, intro + messages, interrupted
        new_sinkou, messages, interrupted = self._apply_invasion_challenge_ignore(area, sinkou)
        return new_sinkou, intro + messages, interrupted






    def _run_invasion_elite_battle_rounds(
        self,
        hero: Character,
        enemy: Character,
        sinkou: int,
        battle_state: Dict[str, int],
        messages: List[str],
    ) -> Optional[tuple[int, List[str], bool]]:
        for _ in range(20):
            round_result = self._resolve_invasion_elite_battle_round(
                hero,
                enemy,
                sinkou,
                battle_state["hero_hp"],
                battle_state["hero_mp"],
                battle_state["hero_atk"],
                battle_state["hero_def"],
                battle_state["enemy_hp"],
                battle_state["enemy_mp"],
                battle_state["enemy_atk"],
                battle_state["enemy_def"],
                battle_state["hero_surrender"],
                messages,
            )
            if round_result is None:
                return 0, messages, True
            battle_state["hero_hp"], battle_state["hero_mp"], battle_state["hero_atk"], battle_state["hero_def"], battle_state["enemy_hp"], battle_state["enemy_mp"], result = round_result
            if result is not None:
                return result
        return None






    def _run_invasion_event(self, area: Dict[str, Any], mode: int, sinkou: int, hero: Optional[Character]) -> tuple[int, List[str], bool]:
        event_roll = random.randint(0, 9)
        if event_roll == 9:
            return self._run_invasion_fort_event(area, mode, sinkou, hero)
        if event_roll == 8:
            return self._run_invasion_challenge_event(area, mode, sinkou, hero)
        return self._maybe_run_invasion_elite_battle(area, mode, sinkou, hero, event_roll)






    def _run_invasion_fort_event(self, area: Dict[str, Any], mode: int, sinkou: int, hero: Optional[Character]) -> tuple[int, List[str], bool]:
        if mode not in (0, 2, 3):
            return sinkou, [], False
        context = self._build_invasion_fort_event_context(area, hero)
        if mode == 0:
            return self._run_invasion_fort_opening_event(mode, sinkou, hero, context)
        if hero is None:
            return sinkou, [], False
        strategy = self._select_invasion_fort_strategy(area, mode, hero)
        return self._run_invasion_fort_strategy_event(mode, sinkou, hero, context, strategy)






    def _run_invasion_fort_opening_event(self, mode: int, sinkou: int, hero: Optional[Character], context: Dict[str, Any]) -> tuple[int, List[str], bool]:
        intro = [
            f"魔王军浩浩荡荡地向{context['area_name']}进发着。",
            f"早有准备的{context['army_name']}在必经之路上建起了一座{context['fort_name']}。",
        ]
        new_sinkou, messages, interrupted = self._apply_invasion_fort_assault(mode, sinkou, hero, context)
        return new_sinkou, intro + messages, interrupted






    def _run_invasion_fort_strategy_event(
        self,
        mode: int,
        sinkou: int,
        hero: Character,
        context: Dict[str, Any],
        strategy: int,
    ) -> tuple[int, List[str], bool]:
        if strategy == 1:
            new_sinkou, messages, interrupted = self._apply_invasion_fort_assault(mode, sinkou, hero, context)
            return new_sinkou, [
                f"{hero.name if mode == 3 else '魔王军'}在{context['fort_name']}前选择了强攻。"
            ] + messages, interrupted
        if strategy == 2:
            new_sinkou, messages, interrupted = self._apply_invasion_fort_infiltration(mode, sinkou, hero, context)
            return new_sinkou, [
                f"{hero.name}决定亲自潜入{context['fort_name']}。"
            ] + messages, interrupted
        new_sinkou, messages, interrupted = self._apply_invasion_fort_detour(mode, sinkou, hero, context)
        return new_sinkou, [
            f"{hero.name}决定绕开{context['fort_name']}继续前进。"
        ] + messages, interrupted






    def _select_invasion_challenge_strategy(self, mode: int, hero: Optional[Character], context: Dict[str, Any]) -> int:
        if mode == 0:
            return 3
        if mode == 3:
            return 2
        if hero is None:
            return 3
        return self._prompt_invasion_challenge_strategy(hero, context)






    def _select_invasion_fort_strategy(self, area: Dict[str, Any], mode: int, hero: Optional[Character]) -> int:
        if mode == 0 or hero is None:
            return 1
        context = self._build_invasion_fort_event_context(area, hero)
        return self._prompt_invasion_fort_strategy(mode, hero, context)






    def _set_character_invasion_retreat_standby_state(self, char: Character) -> None:
        char.cflag[1] = 0
        char.cflag[500] = 0
        self._reset_dungeon_floor_progress(char, floor=max(1, int(char.cflag.get(501, 1))), return_flag=0)
        char.cflag[506] = 0




    def _set_invasion_area_progress(self, area: Dict[str, Any], value: int):
        if area.get("fort_area"):
            return
        if area.get("global_area"):
            self.interpreter.vars.globals[int(area["area_flag"])] = int(value)
            return
        self.interpreter.vars.set_flag(int(area["area_flag"]), int(value))






    def _set_invasion_conquered(self, area: Dict[str, Any], enabled: bool = True):
        if area.get("fort_area"):
            self.interpreter.vars.set_flag(int(area["conquer_flag"]), 15 if enabled else 0)
            return
        value = 1 if enabled else 0
        if area.get("global_area"):
            current = int(self.interpreter.vars.globals.get(int(area["conquer_flag"]), 0))
            self.interpreter.vars.globals[int(area["conquer_flag"])] = max(current, 4 if enabled else 0)
            return
        self.interpreter.vars.set_flag(int(area["conquer_flag"]), value)






    def _set_invasion_elite_battle_round_result(
        self,
        result: str,
        hero: Character,
        enemy: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        messages: List[str],
    ) -> tuple[int, List[str], bool]:
        if result == "victory":
            return self._finish_invasion_elite_battle_victory(hero, enemy, sinkou, hero_hp, hero_mp, hero_atk, hero_def, messages)
        elif result == "surrender":
            return self._finish_invasion_elite_battle_surrender(hero, sinkou, hero_hp, hero_mp, hero_atk, hero_def, messages)
        elif result == "defeat":
            return self._finish_invasion_elite_battle_defeat(hero, enemy, sinkou, hero_hp, hero_mp, hero_atk, hero_def, messages)
        return 0, messages, True






    def _show_invasion_area_menu(self, area: Dict[str, Any]):
        while True:
            if self._advance_invasion_area_menu(area):
                return






    def _spawn_invasion_challenge_captive(self, area: Dict[str, Any]) -> Optional[Character]:
        if not self._can_capture_invasion_enemy(area):
            return None
        context = self._get_invasion_challenge_context(area)
        template_ids = list(context["template_ids"])
        available_ids = [template_id for template_id in template_ids if self._has_character_template(int(template_id))]
        if not available_ids:
            available_ids = self._get_life_cradle_template_ids()
        if available_ids:
            template_id = random.choice(available_ids)
            new_char = self._instantiate_life_cradle_character(int(template_id))
        else:
            new_char = None
        if new_char is None:
            new_char = Character()
            new_char.name = str(context["enemy_name"])
            new_char.callname = new_char.name
            new_char.base[0] = 500
            new_char.base[1] = 300
            new_char.maxbase[0] = 500
            new_char.maxbase[1] = 300
            new_char.cflag[9] = 1
        self._prepare_captured_invasion_enemy(new_char)
        return self._append_character(new_char)






    def _sync_invasion_elite_battle_state(
        self,
        hero: Character,
        sinkou: int,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
    ):
        hero.base[0] = max(1, hero_hp - sinkou)
        hero.base[1] = max(0, hero_mp - sinkou)
        hero.cflag[11] = max(1, hero_atk)
        hero.cflag[12] = max(0, hero_def)






    def show_invasion(self) -> bool:
        """Invasion menu based on the original INVASION.ERB structure."""
        areas = self._get_invasion_area_definitions()
        while True:
            if self._advance_invasion_menu(areas):
                return False





