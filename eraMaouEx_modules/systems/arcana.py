from __future__ import annotations
import os
"""Module for ArcanaMixin - 秘技系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ArcanaMixin:
    """Mixin providing 秘技系统 methods for GameEngine"""

    def _advance_arcana_fort_menu(self, area: Dict[str, Any]) -> Optional[bool]:
        fort_choice = self._prompt_arcana_fort_target(area)
        if fort_choice is None:
            return None
        hero = self._prompt_arcana_fort_hero()
        if hero is None:
            return False
        ok, message = self._run_arcana_fort_assault(area, fort_choice, hero)
        print(f"\n{message}")
        self._pause()
        return ok






    def _apply_arcana_fort_battle_restore(self, hero: Character, enemy: Character) -> List[str]:
        messages: List[str] = []
        self._clear_arcana_fort_temporary_state(hero)
        self._clear_arcana_fort_temporary_state(enemy)
        messages.extend(self._apply_character_dungeon_battle_restore(hero))
        messages.extend(self._apply_character_dungeon_battle_restore(enemy))
        return messages






    def _apply_arcana_fort_capture_measurements(self, fort_id: int, captured: Character) -> None:
        physical_age = self._get_arcana_fort_capture_physical_age(fort_id)
        if physical_age <= 0:
            return
        if not (self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15)):
            return
        profile = self._generate_character_body_profile(captured, physical_age)
        self._apply_generated_character_body_profile(captured, profile, overwrite_existing=True)






    def _apply_arcana_fort_defeat(self, hero: Character) -> List[str]:
        if self._get_flag_bit(5, 7):
            self._set_character_ntr_captive_state(hero)
            return [f"{hero.name}战败后被敌方俘虏了。"]
        self._set_character_invasion_retreat_standby_state(hero)
        return [f"{hero.name}战败后撤退了回来。"]






    def _apply_arcana_fort_element_damage_bonus(self, damage: int, profile: Dict[str, int]) -> int:
        for key in ("fire", "ice", "thunder"):
            if int(profile.get(key, 0)):
                damage += max(1, damage // 5)
        return damage






    def _apply_arcana_fort_preemptive_attacks(
        self,
        hero: Character,
        enemy: Character,
        hero_hp: int,
        hero_mp: int,
        hero_atk: int,
        hero_def: int,
        hero_ammo: int,
        enemy_hp: int,
        enemy_mp: int,
        enemy_atk: int,
        enemy_def: int,
        enemy_ammo: int,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, List[str]]:
        messages: List[str] = []
        if int(hero.talent.get(252, 0)) == 1:
            enemy_hp, enemy_mp, enemy_atk, enemy_def, enemy_ammo, round_messages = self._apply_arcana_fort_single_attack(
                hero,
                enemy,
                hero_atk,
                enemy_def,
                enemy_hp,
                enemy_mp,
                enemy_ammo,
                attack_mode=2,
            )
            messages.extend(round_messages)
        if enemy_hp > 0 and enemy_mp > 0 and int(enemy.talent.get(252, 0)) == 1:
            hero_hp, hero_mp, hero_atk, hero_def, hero_ammo, round_messages = self._apply_arcana_fort_single_attack(
                enemy,
                hero,
                enemy_atk,
                hero_def,
                hero_hp,
                hero_mp,
                hero_ammo,
                attack_mode=2,
            )
            messages.extend(round_messages)
        return hero_hp, hero_mp, hero_atk, hero_def, hero_ammo, enemy_hp, enemy_mp, enemy_atk, enemy_def, enemy_ammo, messages






    def _apply_arcana_fort_single_attack(
        self,
        attacker: Character,
        defender: Character,
        attack: int,
        defense: int,
        hp: int,
        mp: int,
        ammo: int,
        *,
        attack_mode: int = 1,
    ) -> tuple[int, int, int, int, int, List[str]]:
        profile = self._get_arcana_fort_weapon_profile(attacker)
        working_defense = max(0, int(defense))
        messages: List[str] = []
        if attack_mode == 0 and int(attacker.talent.get(243, 0)) == 1:
            working_defense //= 2
            messages.append("偷袭成功！！")
        miss_rate = max(0, int(profile["miss_rate"]))
        if random.randint(0, 99) < miss_rate:
            messages.append(f"{attacker.name}的攻击落空了……")
            return hp, mp, int(defender.cflag.get(11, 0)), working_defense, ammo, messages
        mp_delta = int(profile["mp_delta"])
        attacker_max_mp = max(1, int(attacker.maxbase.get(1, attacker.base.get(1, 0) or 1)))
        attacker_next_mp = min(attacker_max_mp, max(0, int(mp) + mp_delta))
        attacker.base[1] = attacker_next_mp
        damage_base = attack - working_defense
        if damage_base <= 0:
            reduced_defense = max(0, working_defense * 2 // 3)
            if reduced_defense >= working_defense and working_defense > 0:
                reduced_defense = max(0, working_defense - 1)
            messages.append(f"{defender.name}承受住了{attacker.name}的攻击。")
            return hp, attacker_next_mp, int(defender.cflag.get(11, 0)), reduced_defense, ammo, messages
        defense_damage_rate = max(0, int(profile["defense_damage_rate"]))
        defense_loss = max(1, working_defense // 3) * defense_damage_rate // 100
        next_defense = max(0, working_defense - max(1, defense_loss))
        damage = max(1, damage_base * 2)
        damage = max(1, damage * max(1, int(profile["damage_rate"])) // 100)
        if ammo > 0:
            ammo -= max(0, int(profile["ammo_cost"]))
        else:
            empty_mode = int(profile["empty_ammo_mode"])
            if empty_mode == 1:
                damage = max(1, damage // 2)
            elif empty_mode == 2:
                messages.append("弹药用尽了，只能干瞪眼！")
                return hp, attacker_next_mp, int(defender.cflag.get(11, 0)), next_defense, ammo, messages
        if random.randint(0, 99) < max(0, int(profile["combo_rate"])):
            damage *= 2
            ammo -= max(0, int(profile["ammo_cost"]))
            messages.append(f"{attacker.name}发出了迅捷的2连击！！")
        if attack_mode == 0:
            damage += max(1, damage // 5)
        elif attack_mode == 2:
            damage *= 2
        damage, followup_messages = self._apply_arcana_fort_weapon_followup_effects(attacker, defender, damage, profile)
        messages.extend(followup_messages)
        hp -= damage
        mp_damage_rate = max(0, int(profile["mp_damage_rate"]))
        defender_next_mp = max(0, mp - max(1, damage * mp_damage_rate // 100))
        next_attack = int(defender.cflag.get(11, 0))
        if int(defender.talent.get(251, 0)) == 0:
            next_attack = max(1, next_attack - max(1, damage_base // 100 + 1))
            defender.cflag[11] = next_attack
        messages.append(f"{attacker.name}对{defender.name}造成了{damage}点伤害。")
        return hp, defender_next_mp, next_attack, next_defense, ammo, messages






    def _apply_arcana_fort_victory(self, area: Dict[str, Any], fort_id: int, enemy: Character) -> List[str]:
        reward = 1000 * max(1, int(enemy.cflag.get(9, 0)))
        self._add_global_money(reward)
        self.interpreter.vars.set_flag(92, self._get_arcana_fort_conquered_mask() | self._get_arcana_fort_bit(fort_id))
        captured = self._append_character(enemy)
        if captured is not None:
            self._set_character_captured_standby_state(captured)
            self._apply_arcana_fort_capture_measurements(fort_id, captured)
        return self._build_arcana_fort_victory_messages(fort_id, enemy.name, reward)






    def _apply_arcana_fort_weapon_followup_effects(
        self,
        attacker: Character,
        defender: Character,
        damage: int,
        profile: Dict[str, int],
    ) -> tuple[int, List[str]]:
        messages: List[str] = []
        damage = self._apply_arcana_fort_element_damage_bonus(damage, profile)
        if int(profile.get("poison", 0)) and random.randint(0, 1) == 1:
            if self._get_character_flag_bit(defender, 503, ARCANA_BATTLE_POISON_BIT):
                damage *= 2
                messages.append("毒素不断侵蚀！！")
            else:
                self._set_character_flag_bit(defender, 503, ARCANA_BATTLE_POISON_BIT, True)
                messages.append("毒素增加了！！")
        return damage, messages






    def _build_arcana_fort_enemy(self, fort_id: int) -> Optional[Character]:
        template_id = {
            0: 22,
            1: 23,
            2: 21,
            3: 20,
        }.get(int(fort_id))
        if template_id is None:
            return None
        enemy = self._instantiate_character_from_template(template_id)
        if enemy is None:
            return None
        self._prepare_spawned_invading_hero(
            enemy,
            clamp_karma=False,
            assign_spawn_position=False,
            apply_initial_funds=False,
            apply_base_level_bonus=True,
        )
        enemy.base[0] = int(enemy.maxbase.get(0, enemy.base.get(0, 0)))
        enemy.base[1] = int(enemy.maxbase.get(1, enemy.base.get(1, 0)))
        return enemy






    def _build_arcana_fort_intro_messages(self, fort_id: int, hero: Character) -> List[str]:
        intros = {
            0: "在东方堡垒遇到了黑方片，黑亮的大剑已经出鞘。",
            1: "在西方堡垒遇到了白梅花，雪白的魔杖开始放出强烈的魔力波动。",
            2: "在南方堡垒遇到了银黑桃，分身术的残影已经笼罩了战场。",
            3: "在北方堡垒遇到了作为亲卫队长的金红桃，金色铠甲闪烁着太阳般的光芒。",
        }
        return [intros.get(int(fort_id), "圣灵骑士现身了。"), f"{hero.name}上前迎战。"]






    def _build_arcana_fort_overview_messages(self, conquered: int) -> List[str]:
        if conquered == 15:
            return [
                "圣灵骑士全部都被打倒了，四个据点也都被攻陷了。",
                "圣灵骑士的卖春堡垒已经完全落入了魔王的支配。",
            ]
        if conquered in {14, 13, 11, 7}:
            return ["最后只剩下一位圣灵骑士，决战时刻临近了……"]
        if conquered in {3, 5, 6, 9, 10, 12}:
            return ["现在已经打倒了两位圣灵骑士，还剩下两个堡垒……"]
        if conquered in {1, 2, 4, 8}:
            return ["你的奴隶已经打倒了一位伟大的圣灵骑士，还剩下三位……"]
        return [
            "有俘虏说，狂王的亲卫队【圣灵骑士】正在东南西北四个堡垒里特训着。",
            "看起来，要把这样的猛士抓回来调教，必须派遣刺客才行……",
        ]






    def _build_arcana_fort_victory_messages(self, fort_id: int, enemy_name: str, reward: int) -> List[str]:
        card_messages = {
            0: "获得了黑方片持有的【方片A】牌。",
            1: "获得了白梅花持有的【梅花A】牌。",
            2: "获得了银黑桃持有的【黑桃A】牌。",
            3: "获得了金红桃持有的【红桃A】牌。",
        }
        quote_messages = {
            0: "「我居然输了………」",
            1: "「战败也是我的命运么？…我那无法解读的预言，见到了魔王的话，会明白吗………」",
            2: "「真是的………放开我！」",
            3: "「怎么这样……狂王大人！救救我啊！！」",
        }
        return [
            f"圣灵骑士{enemy_name}战败了……",
            f"获得了{reward}G！",
            card_messages.get(int(fort_id), "获得了一张圣灵骑士持有的王牌。"),
            f"然后，被俘虏了的{enemy_name}被带到你的地下城了………",
            quote_messages.get(int(fort_id), ""),
        ]






    def _check_arcana_fort_duel_end(
        self,
        hero: Character,
        enemy: Character,
        hero_hp: int,
        hero_mp: int,
        enemy_hp: int,
        enemy_mp: int,
    ) -> tuple[Optional[bool], List[str]]:
        if enemy_hp <= 0:
            return True, [f"{enemy.name}徒劳地奋战着，力竭了。"]
        if enemy_hp <= 300:
            return True, [f"{enemy.name}感觉到生命垂危，投降求饶了。"]
        if enemy_mp <= 0:
            return True, [f"{enemy.name}失去了战意，丢掉武器投降了。"]

        if self._get_flag_bit(5, 7):
            if hero_hp <= 0:
                return False, [f"{hero.name}在圣灵骑士前力竭倒下了。", f"{enemy.name}把她抱起来并带回了狂王的城堡。"]
            if hero_hp <= 300:
                return False, [f"{hero.name}感觉到生命垂危，投降求饶了。", f"{enemy.name}把她绑起来并带回了狂王的城堡。"]
            if hero_mp <= 0:
                return False, [f"{hero.name}失去了战意，丢掉武器投降了。", f"{enemy.name}把她绑起来并带回了狂王的城堡。"]
            return None, []

        if hero_hp <= 0:
            return False, [f"{hero.name}在圣灵骑士前力竭倒下了。"]
        if hero_hp <= 300:
            return False, [f"{hero.name}感觉到生命垂危，投降求饶了。", f"{enemy.name}怜悯着倒下的她，把她赶到了堡垒外。"]
        if hero_mp <= 0:
            return False, [f"{hero.name}失去了战意，丢掉武器投降了。", f"{enemy.name}怜悯着倒下的她，把她赶到了堡垒外。"]
        return None, []






    def _cleanup_arcana_fort_enemy(self, enemy: Optional[Character]) -> None:
        self._remove_last_character_if_matches(enemy)






    def _clear_arcana_fort_temporary_state(self, actor: Character) -> None:
        self._set_character_flag_bit(actor, 503, ARCANA_BATTLE_POISON_BIT, False)






    def _get_arcana_fort_bit(self, fort_id: int) -> int:
        return {
            0: 1,
            1: 4,
            2: 2,
            3: 8,
        }.get(int(fort_id), 0)






    def _get_arcana_fort_capture_physical_age(self, fort_id: int) -> int:
        return {
            0: 21,
            1: 27,
            2: 24,
            3: 18,
        }.get(int(fort_id), 0)






    def _get_arcana_fort_conquered_mask(self) -> int:
        return int(self.interpreter.vars.get_flag(92, 0))






    def _get_arcana_fort_labels(self) -> List[tuple[int, str]]:
        return [
            (0, "东方堡垒"),
            (1, "西方堡垒"),
            (2, "南方堡垒"),
            (3, "北方堡垒"),
        ]






    def _get_arcana_fort_speed_roll(self, char: Character) -> int:
        roll = random.randint(0, 5)
        if int(char.talent.get(243, 0)) == 1:
            roll += 1
        if int(char.talent.get(245, 0)) == 1:
            roll += 1
        if int(char.talent.get(258, 0)) == 1:
            roll += 1
        race = int(char.talent.get(314, 0))
        if race == 10:
            roll += 1
        elif race == 11:
            roll -= 1
        return roll






    def _get_arcana_fort_weapon_profile(self, attacker: Character) -> Dict[str, int]:
        equip_code = int(attacker.cflag.get(550, 40))
        if equip_code <= 0:
            equip_code = 40
        base_code, enhance, prefix = self._decode_equipment_code(equip_code)
        profile: Dict[str, int] = {
            "damage_rate": 100,
            "ammo_cost": 0,
            "miss_rate": 0,
            "mp_delta": 0,
            "combo_rate": 0,
            "defense_damage_rate": 100,
            "empty_ammo_mode": 0,
            "mp_damage_rate": 100,
            "poison": 0,
            "fire": 0,
            "ice": 0,
            "thunder": 0,
        }
        weapon_defaults: Dict[int, Dict[str, int]] = {
            40: {"damage_rate": 100},
            41: {"damage_rate": 80, "mp_delta": 20},
            42: {"damage_rate": 80, "defense_damage_rate": 120},
            43: {"damage_rate": 70, "combo_rate": 30},
            44: {"damage_rate": 100, "ammo_cost": 1, "combo_rate": 30, "empty_ammo_mode": 1},
            45: {"damage_rate": 150, "ammo_cost": 1, "empty_ammo_mode": 2},
            46: {"damage_rate": 120, "miss_rate": 10},
            47: {"damage_rate": 150, "miss_rate": 30},
            48: {"damage_rate": 100, "miss_rate": 10, "mp_delta": 20},
            49: {"damage_rate": 100, "mp_delta": -10, "mp_damage_rate": 120},
            50: {"damage_rate": 80, "combo_rate": 50},
            51: {"damage_rate": 135, "miss_rate": 20},
            52: {"damage_rate": 65, "combo_rate": 40},
        }
        profile.update(weapon_defaults.get(base_code, weapon_defaults[40]))
        if prefix == 1:
            profile["damage_rate"] += 30
            profile["miss_rate"] += 20
        elif prefix == 2:
            profile["damage_rate"] -= 10
            profile["poison"] = 1
        elif prefix == 3:
            profile["damage_rate"] += 40
            profile["mp_delta"] -= 30
        elif prefix == 4:
            profile["damage_rate"] -= 10
            profile["combo_rate"] += 20
        elif prefix == 5:
            profile["miss_rate"] += 10
            profile["fire"] = 1
        elif prefix == 6:
            profile["mp_delta"] -= 10
            profile["ice"] = 1
        elif prefix == 7:
            profile["damage_rate"] += 20
            profile["miss_rate"] += 10
            profile["mp_delta"] -= 10
            profile["thunder"] = 1
        elif prefix == 8:
            profile["damage_rate"] -= 10
            profile["mp_delta"] += 20
        elif prefix == 9:
            profile["mp_delta"] -= 10
            profile["mp_damage_rate"] += 20
        profile["damage_rate"] += max(0, enhance) * 5
        if int(attacker.talent.get(246, 0)) == 1:
            profile["damage_rate"] += 10
        if int(attacker.talent.get(247, 0)) == 1:
            profile["mp_damage_rate"] += 10
        if int(attacker.talent.get(259, 0)) == 1:
            profile["damage_rate"] += 10
            profile["miss_rate"] += 10
        if int(attacker.talent.get(260, 0)) == 1:
            profile["mp_damage_rate"] += 10
            profile["mp_delta"] -= 10
        if int(attacker.talent.get(264, 0)) == 1:
            profile["damage_rate"] += 10
            profile["mp_delta"] -= 10
        race = int(attacker.talent.get(314, 0))
        if base_code == 45 and race == 1:
            profile["combo_rate"] += 10
        if race == 6:
            profile["mp_delta"] += 10
        elif race == 7:
            profile["mp_damage_rate"] += 10
        elif race == 8:
            profile["combo_rate"] += 10
        elif race == 9:
            profile["defense_damage_rate"] += 10
        if int(attacker.talent.get(275, 0)):
            profile["fire"] = 1
        if int(attacker.talent.get(276, 0)):
            profile["combo_rate"] += 10
            profile["ice"] = 1
        if int(attacker.talent.get(277, 0)):
            profile["combo_rate"] += 5
            profile["damage_rate"] += 5
            profile["thunder"] = 1
        if int(attacker.talent.get(278, 0)):
            if profile["mp_delta"] > 0:
                profile["combo_rate"] += 5
                profile["damage_rate"] += 5
                profile["mp_delta"] += 5
            else:
                profile["mp_delta"] += 10
        if int(attacker.talent.get(279, 0)):
            if profile["mp_damage_rate"] > 0:
                profile["combo_rate"] += 5
                profile["damage_rate"] += 5
                profile["mp_damage_rate"] += 5
            else:
                profile["mp_damage_rate"] += 10
        return profile






    def _list_arcana_fort_attack_candidates(self) -> List[tuple[int, Character]]:
        return list(self._list_invasion_hero_candidates(raid_mode=False))






    def _prompt_arcana_fort_hero(self) -> Optional[Character]:
        candidates = self._list_arcana_fort_attack_candidates()
        if not candidates:
            print("\n*没有可以攻击的勇士*")
            self._pause()
            return None
        print("\n派遣谁去攻击呢？")
        for idx, char in candidates:
            print(
                f" [{idx}] {char.name} LV{int(char.cflag.get(9, 0))}"
                f" 攻击{int(char.cflag.get(11, 0)):>4} 防御{int(char.cflag.get(12, 0)):>4}"
            )
        print(" [999] 返回")
        choice = self._prompt_choice()
        if choice == "999":
            return None
        try:
            selected_idx = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        return next((char for idx, char in candidates if idx == selected_idx), None)






    def _prompt_arcana_fort_target(self, area: Dict[str, Any]) -> Optional[int]:
        conquered = self._get_arcana_fort_conquered_mask()
        messages = self._build_arcana_fort_overview_messages(conquered)
        print(f"\n【{self._get_invasion_area_display_name(area)}】")
        for line in messages:
            print(line)
        print("-" * 30)
        for fort_id, label in self._get_arcana_fort_labels():
            if conquered & self._get_arcana_fort_bit(fort_id):
                print(f" [*] {label}（已攻占）")
            else:
                print(f" [{fort_id}] {label}")
        print(" [4] 撤退")
        while True:
            choice = self._prompt_choice()
            if choice == "4":
                return None
            try:
                fort_id = int(choice)
            except ValueError:
                print("\nInvalid selection.")
                self._pause()
                return None
            if fort_id not in {0, 1, 2, 3}:
                print("\nInvalid selection.")
                self._pause()
                return None
            if conquered & self._get_arcana_fort_bit(fort_id):
                print("\n该堡垒已经攻占。")
                self._pause()
                return None
            return fort_id






    def _resolve_arcana_fort_duel(self, hero: Character, enemy: Character) -> tuple[bool, List[str]]:
        hero_hp = max(1, int(hero.base.get(0, 0)))
        hero_mp = max(0, int(hero.base.get(1, 0)))
        enemy_hp = max(1, int(enemy.base.get(0, 0)))
        enemy_mp = max(0, int(enemy.base.get(1, 0)))
        hero_atk = max(1, int(hero.cflag.get(11, 0)))
        hero_def = max(0, int(hero.cflag.get(12, 0)))
        enemy_atk = max(1, int(enemy.cflag.get(11, 0)))
        enemy_def = max(0, int(enemy.cflag.get(12, 0)))
        hero_ammo = 15
        enemy_ammo = 15
        messages: List[str] = []
        timed_out = False
        hero_hp, hero_mp, hero_atk, hero_def, hero_ammo, enemy_hp, enemy_mp, enemy_atk, enemy_def, enemy_ammo, opening_messages = self._apply_arcana_fort_preemptive_attacks(
            hero,
            enemy,
            hero_hp,
            hero_mp,
            hero_atk,
            hero_def,
            hero_ammo,
            enemy_hp,
            enemy_mp,
            enemy_atk,
            enemy_def,
            enemy_ammo,
        )
        messages.extend(opening_messages)
        duel_result, result_messages = self._check_arcana_fort_duel_end(hero, enemy, hero_hp, hero_mp, enemy_hp, enemy_mp)
        messages.extend(result_messages)
        if duel_result is not None:
            hero.base[0] = max(1, hero_hp)
            hero.base[1] = max(0, hero_mp)
            return duel_result, messages
        for _ in range(16):
            hero_speed = self._get_arcana_fort_speed_roll(hero)
            enemy_speed = self._get_arcana_fort_speed_roll(enemy)
            if hero_speed >= enemy_speed:
                enemy_hp, enemy_mp, enemy_atk, enemy_def, enemy_ammo, round_messages = self._apply_arcana_fort_single_attack(
                    hero,
                    enemy,
                    hero_atk,
                    enemy_def,
                    enemy_hp,
                    enemy_mp,
                    enemy_ammo,
                    attack_mode=0,
                )
                messages.extend(round_messages)
                duel_result, result_messages = self._check_arcana_fort_duel_end(hero, enemy, hero_hp, hero_mp, enemy_hp, enemy_mp)
                messages.extend(result_messages)
                if duel_result is not None:
                    break
                hero_hp, hero_mp, hero_atk, hero_def, hero_ammo, round_messages = self._apply_arcana_fort_single_attack(
                    enemy,
                    hero,
                    enemy_atk,
                    hero_def,
                    hero_hp,
                    hero_mp,
                    hero_ammo,
                    attack_mode=1,
                )
                messages.extend(round_messages)
            else:
                hero_hp, hero_mp, hero_atk, hero_def, hero_ammo, round_messages = self._apply_arcana_fort_single_attack(
                    enemy,
                    hero,
                    enemy_atk,
                    hero_def,
                    hero_hp,
                    hero_mp,
                    hero_ammo,
                    attack_mode=0,
                )
                messages.extend(round_messages)
                duel_result, result_messages = self._check_arcana_fort_duel_end(hero, enemy, hero_hp, hero_mp, enemy_hp, enemy_mp)
                messages.extend(result_messages)
                if duel_result is not None:
                    break
                enemy_hp, enemy_mp, enemy_atk, enemy_def, enemy_ammo, round_messages = self._apply_arcana_fort_single_attack(
                    hero,
                    enemy,
                    hero_atk,
                    enemy_def,
                    enemy_hp,
                    enemy_mp,
                    enemy_ammo,
                    attack_mode=1,
                )
                messages.extend(round_messages)
            hero_mp = max(0, hero_mp - random.randint(0, 19))
            enemy_mp = max(0, enemy_mp - random.randint(0, 19))
            duel_result, result_messages = self._check_arcana_fort_duel_end(hero, enemy, hero_hp, hero_mp, enemy_hp, enemy_mp)
            messages.extend(result_messages)
            if duel_result is not None:
                break
        else:
            timed_out = True
            hero_mp = max(0, hero_mp - random.randint(0, 29))
            messages.append(f"{hero.name}久战不下，最终抽身撤离了……")
        hero.base[0] = max(1, hero_hp)
        hero.base[1] = max(0, hero_mp)
        victory = duel_result is True and not timed_out
        if victory:
            messages.append(f"{hero.name}击败了{enemy.name}。")
        elif not timed_out and not result_messages:
            messages.append(f"{hero.name}被{enemy.name}击败了……")
        return victory, messages






    def _run_arcana_fort_assault(self, area: Dict[str, Any], fort_id: int, hero: Character) -> tuple[bool, str]:
        enemy = self._build_arcana_fort_enemy(fort_id)
        if enemy is None:
            return False, "缺少对应的圣灵骑士模板。"
        try:
            intro_messages = self._build_arcana_fort_intro_messages(fort_id, hero)
            victory, battle_messages = self._resolve_arcana_fort_duel(hero, enemy)
            result_messages = intro_messages + battle_messages
            result_messages.extend(self._apply_arcana_fort_battle_restore(hero, enemy))
            if victory:
                result_messages.extend(self._apply_arcana_fort_victory(area, fort_id, enemy))
                return True, "\n".join(result_messages)
            result_messages.extend(self._apply_arcana_fort_defeat(hero))
            return False, "\n".join(result_messages)
        finally:
            self._cleanup_arcana_fort_enemy(enemy)






    def _show_arcana_fort_menu(self, area: Dict[str, Any]) -> None:
        while True:
            completed = self._advance_arcana_fort_menu(area)
            if completed is None:
                return
            if completed:
                self.advance_time()
                return





