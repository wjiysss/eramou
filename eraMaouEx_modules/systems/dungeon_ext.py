from __future__ import annotations
"""Module for DungeonExtMixin - 地牢系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class DungeonExtMixin:
    """Mixin providing 地牢系统 methods for GameEngine"""

    def _add_dungeon_party_debt(self, char: Character, amount: int):
        char.cflag[582] = int(char.cflag.get(582, 0)) + int(amount)




    def _add_dungeon_party_funds(self, char: Character, amount: int):
        char.cflag[580] = int(char.cflag.get(580, 0)) + int(amount)




    def _add_dungeon_party_loot(self, char: Character, amount: int):
        char.cflag[581] = int(char.cflag.get(581, 0)) + int(amount)




    def _advance_dungeon_menu(self) -> bool:
        return self._handle_dungeon_menu_choice(self._prompt_dungeon_menu_choice_with_render())






    def _advance_dungeon_party_flow(self, action: str, leader: Character):
        if action == "4":
            ok, message = self._run_dungeon_party_action(leader)
        else:
            ok, message = self._run_dungeon_harvest_action(leader)
        print(f"\n{message}")
        self._pause()






    def _advance_dungeon_quest_state(self, leader: Character) -> List[str]:
        if not self._is_dungeon_quest_board_enabled():
            return []
        if int(leader.cflag.get(1, 0)) != 2 or int(leader.cflag.get(534, 0)) != 1:
            return []
        messages: List[str] = []
        if self._apply_dungeon_quest_deadline_tick(leader, messages):
            return messages
        flags = int(leader.cflag.get(536, 0))
        if self._apply_dungeon_quest_hazard_effects(leader, flags, messages):
            return messages
        if self._apply_dungeon_quest_sex_requirement(leader, flags, messages):
            return messages
        if self._can_finish_dungeon_quest_exploration(leader):
            self._apply_dungeon_quest_exploration_result(leader, flags, messages)
        return messages






    def _apply_character_dungeon_battle_restore(self, actor: Character) -> List[str]:
        messages: List[str] = []
        base_attack = int(actor.cflag.get(13, actor.cflag.get(11, 0)))
        base_defense = int(actor.cflag.get(14, actor.cflag.get(12, 0)))
        actor.cflag[11] = max(0, base_attack)
        actor.cflag[12] = max(0, base_defense)

        max_mp = max(1, int(actor.maxbase.get(1, 1)))
        current_mp = max(0, int(actor.base.get(1, 0)))
        if current_mp * 100 // max_mp < 40 and int(actor.talent.get(249, 0)):
            level = max(0, int(actor.cflag.get(9, 0)))
            actor.cflag[11] = int(actor.cflag.get(11, 0)) + level
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + level
            actor.base[0] = min(int(actor.maxbase.get(0, actor.base.get(0, 0))), int(actor.base.get(0, 0)) + level * 10)
            messages.append(f"{actor.name} 在危急中重新稳住了架势，铁壁素质让战后状态恢复得更快。")

        medals = max(0, int(actor.exp.get(81, 0)))
        if int(actor.talent.get(210, 0)):
            actor.cflag[11] = int(actor.cflag.get(11, 0)) + medals * 2
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + medals
        elif int(actor.talent.get(211, 0)):
            actor.cflag[11] = int(actor.cflag.get(11, 0)) + medals
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + medals * 2

        if int(actor.talent.get(314, 0)) == 2 and 14 <= int(self.interpreter.vars.day[2]) <= 16:
            actor.cflag[11] = int(actor.cflag.get(11, 0)) * 10
            actor.cflag[12] = int(actor.cflag.get(12, 0)) * 10
        return messages






    def _apply_character_dungeon_battle_skill_extra_bonus(self, actor: Character) -> List[str]:
        if int(actor.cflag.get(9, 0)) < 100:
            return []

        messages: List[str] = []
        if int(actor.talent.get(240, 0)) and random.randint(0, 99) < 60:
            attack_bonus = 10
            defense_bonus = int(actor.cflag.get(9, 0)) // 5 + 10
            actor.cflag[11] = int(actor.cflag.get(11, 0)) * (100 + attack_bonus) // 100
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + defense_bonus
            messages.append(f"{actor.name} 在战后重新整理战术，攻击提高了 {attack_bonus}% ，防御提高了 {defense_bonus}。")

        if int(actor.talent.get(241, 0)) and random.randint(0, 99) < 40:
            mp_gain_rate = 10
            max_mp = max(1, int(actor.maxbase.get(1, 1)))
            before_mp = int(actor.base.get(1, 0))
            actor.base[1] = min(max_mp, before_mp + max_mp * mp_gain_rate // 100)
            messages.append(f"{actor.name} 通过魔术冥想恢复了 {int(actor.base.get(1, 0)) - before_mp} 点 MP。")

        if int(actor.talent.get(242, 0)) and random.randint(0, 99) < 40:
            hp_gain_rate = 8
            max_hp = max(1, int(actor.maxbase.get(0, 1)))
            before_hp = int(actor.base.get(0, 0))
            actor.base[0] = min(max_hp, before_hp + max_hp * hp_gain_rate // 100)
            messages.append(f"{actor.name} 借由法术再生恢复了 {int(actor.base.get(0, 0)) - before_hp} 点 HP。")

        if int(actor.talent.get(243, 0)) and random.randint(0, 99) < 20:
            attack_bonus = 60
            actor.cflag[11] = int(actor.cflag.get(11, 0)) * (100 + attack_bonus) // 100
            messages.append(f"{actor.name} 维持住了奇袭后的势头，攻击提高了 {attack_bonus}%。")

        if int(actor.talent.get(249, 0)) and random.randint(0, 99) < 60:
            defense_bonus = int(actor.cflag.get(9, 0)) // 10 + 20
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + defense_bonus
            messages.append(f"{actor.name} 的铁壁本能仍在发挥作用，防御提高了 {defense_bonus}。")

        if int(actor.talent.get(250, 0)) and random.randint(0, 99) < 20:
            defense_bonus = int(actor.cflag.get(9, 0)) // 3 + 60
            actor.cflag[12] = int(actor.cflag.get(12, 0)) + defense_bonus
            messages.append(f"{actor.name} 展开了咒术结界，防御提高了 {defense_bonus}。")
        return messages






    def _apply_daily_dungeon_farm_birth(self, stock: Dict[int, int], monster_id: int, meat_toilet_count: int) -> List[str]:
        current_count = max(0, int(stock.get(monster_id, 0)))
        produced = meat_toilet_count
        hide_records = self._get_flag_bit(614, 0)
        if self._get_flag_bit(614, 1):
            sale_income = meat_toilet_count * 10
            self._add_global_money(sale_income)
            if hide_records:
                return [f"人类牧场卖掉了新生怪物，现金收入 +{sale_income}。"]
            return [
                f"人类牧场卖掉了新生怪物，现金收入 +{sale_income}。",
                f"人类牧场的肉便器生下了 {produced} 只{self._get_item_name(monster_id)}。",
            ]

        stock[monster_id] = min(999, current_count + meat_toilet_count)
        produced = max(0, stock[monster_id] - current_count)
        if hide_records:
            return []
        return [f"人类牧场的肉便器生下了 {produced} 只{self._get_item_name(monster_id)}。"]






    def _apply_daily_dungeon_farm_extra_rewards(self, extra: int, meat_toilet_count: int) -> List[str]:
        messages: List[str] = []
        if extra & 1:
            milk_income = meat_toilet_count
            self._add_global_money(milk_income)
            messages.append(f"出售榨出的乳汁获得了 {milk_income} G。")
        if extra & 2:
            player = self._get_player()
            if player is not None:
                player.exp[80] = int(player.exp.get(80, 0)) + meat_toilet_count
                messages.append(f"原本是勇者的扶她奴隶侵犯着肉便器，淫欲转化成了 {meat_toilet_count} 点经验值。")
        return messages






    def _apply_daily_dungeon_farm_operation(self, extra: int) -> List[str]:
        meat_toilet_count = int(self.interpreter.vars.get_flag(83, 0))
        if meat_toilet_count <= 0:
            return []

        messages: List[str] = []
        hide_records = self._get_flag_bit(614, 0)
        stock = self._get_monster_stock()
        monster_id = self._get_random_monster_id()
        messages.extend(self._build_daily_dungeon_farm_narrative(extra, meat_toilet_count, hide_records))
        messages.extend(self._apply_daily_dungeon_farm_birth(stock, monster_id, meat_toilet_count))
        messages.extend(self._apply_daily_dungeon_farm_extra_rewards(extra, meat_toilet_count))
        return messages






    def _apply_daily_dungeon_room_operations(self) -> List[str]:
        messages: List[str] = []
        for floor in range(1, 10):
            room_id = self._get_dungeon_floor_room(floor)
            extra = self._get_dungeon_floor_room_extra(floor)
            if room_id == 500:
                income = self._get_daily_dungeon_shop_income(extra)
                self._add_global_money(income)
                messages.append(self._get_daily_dungeon_shop_prestige_text())
                messages.append(f"第{floor}阶层的商店街上缴了税金，现金收入 +{income}。")
            elif room_id == 502:
                messages.extend(self._apply_daily_dungeon_farm_operation(extra))
        return messages






    def _apply_dungeon_anal_worm_trap_state(self, leader: Character, floor: int) -> List[str]:
        if not self._get_character_flag_bit(leader, 503, DUNGEON_STATE_SLIPPERY_BIT):
            return []
        extra_mp = max(1, int((floor * 7 + 30) * 0.3))
        self._apply_dungeon_damage(leader, mp_damage=extra_mp)
        return [f"黏滑状态让肛门虫更轻易钻了进去，额外造成 MP-{extra_mp}。"]






    def _apply_dungeon_animal_relief(self, char: Character) -> List[str]:
        if char.cflag.get(1, 0) != 3:
            return []
        if char.talent.get(0, 0) or char.talent.get(122, 0):
            return []
        if char.exp.get(56, 0) < 50:
            return []
        player = self._get_player()
        if player is None or self._get_item_count(player, 22) <= 0:
            return []
        if char.base.get(0, 0) < 500:
            return []
        play = self._get_dungeon_animal_relief_play_count(char)
        if play <= 0:
            return []
        char.exp[56] = char.exp.get(56, 0) + play
        char.exp[0] = char.exp.get(0, 0) + play
        char.exp[5] = char.exp.get(5, 0) + play
        char.exp[80] = char.exp.get(80, 0) + play
        char.juel[1] = char.juel.get(1, 0) + play * 200
        char.juel[6] = char.juel.get(6, 0) + play * 300
        char.juel[8] = char.juel.get(8, 0) + play * 200
        self._add_character_karma(char, -2)
        return [f"{char.name} 在地下城深处抑制不住兽奸欲望，与魔物交合了 {play} 次。"]






    def _apply_dungeon_animal_relief_bonus_count(self, char: Character, play: int) -> int:
        if play <= 0:
            return 0
        if char.talent.get(17, 0):
            play += 1
        if char.talent.get(33, 0):
            play += 1
        if char.talent.get(124, 0):
            play += 1
        if char.talent.get(15, 0):
            play -= 1
        if char.talent.get(20, 0):
            play -= 1
        if char.talent.get(32, 0):
            play -= 1
        if char.talent.get(62, 0) and not char.talent.get(64, 0):
            play -= 2
        if char.talent.get(70, 0):
            play += 1
        elif char.talent.get(71, 0):
            play -= 2
        if char.talent.get(76, 0):
            play += 1
        if char.talent.get(136, 0):
            play = int(play * 1.5)
        return max(0, play)






    def _apply_dungeon_auto_consumables(self, char: Character, timing: str) -> List[str]:
        messages: List[str] = []
        for slot_id in self._get_dungeon_consumable_slot_ids():
            raw_item = int(char.cflag.get(slot_id, 0))
            if raw_item <= 0:
                continue
            item_id, appraise = self._decode_dungeon_consumable(raw_item)
            message = self._apply_dungeon_consumable_effect(char, item_id, appraise, timing)
            if message is None:
                continue
            self._consume_dungeon_consumable_slot(char, slot_id)
            messages.append(message)
        return messages






    def _apply_dungeon_bitch_ability_factor(self, char: Character, count: int) -> int:
        return count + (int(char.abl.get(15, 0)) + int(char.abl.get(17, 0)) + int(char.abl.get(37, 0))) // 6






    def _apply_dungeon_bitch_appearance_factor(self, char: Character, count: int) -> int:
        if char.talent.get(99, 0) and char.talent.get(248, 0):
            count += 1
        count += sum(int(char.talent.get(idx, 0)) for idx in [244, 245, 246, 247, 259, 260])
        return count






    def _apply_dungeon_bitch_customer_multipliers(self, char: Character, count: int) -> int:
        if char.cflag.get(500, 0) == 1:
            count = count * (10 + max(0, int(char.abl.get(10, 0)))) // 10
        elif char.talent.get(85, 0):
            count //= 2
        if char.talent.get(204, 0):
            count = count * 3 // 2
        return max(0, count)






    def _apply_dungeon_bitch_customer_round(self, char: Character, success_score: int, failure_score: int) -> Optional[tuple[str, int, int]]:
        if random.randint(0, max(1, success_score + failure_score) - 1) >= success_score:
            return None
        play_type = self._roll_dungeon_bitch_play_type(char)
        if play_type is None:
            return None
        play = self._get_dungeon_bitch_average_play_count(char)
        income = self._get_dungeon_bitch_pay_amount(char, play_type, play)
        self._apply_dungeon_bitch_play_effects(char, play_type, play)
        return play_type, play, income






    def _apply_dungeon_bitch_former_life_factor(self, char: Character, count: int) -> int:
        former_life = int(char.talent.get(315, 0))
        if former_life == 5:
            return count + 2
        if former_life == 7:
            return count + 1
        if former_life in {2, 8, 12}:
            return count - 1
        if int(target.abl.get(10, 0)) + int(target.abl.get(3, 0)) + int(target.abl.get(16, 0)) >= 13:
            print(f"{target.name}在依依不舍地拉着{player.name if player is not None else '主人'}的袖子，")
            print("但那只手还是被抖开，离开了房间…")
        return 1






    def _apply_dungeon_bitch_karma_factor(self, char: Character, count: int) -> int:
        karma = int(char.cflag.get(151, 0))
        if karma > 180:
            return count - 3
        if karma > 130:
            return count - 2
        if karma > 80:
            return count - 1
        if karma > -20:
            return count + 1
        if karma > -70:
            return count + 2
        if karma > -120:
            return count + 3
        return count + 4






    def _apply_dungeon_bitch_play_effects(self, char: Character, play_type: str, play_count: int):
        char.exp[74] = char.exp.get(74, 0) + play_count
        handler = self._get_dungeon_bitch_play_effects_handler(play_type)
        if handler is not None:
            handler(char, play_count)






    def _apply_dungeon_bitch_play_effects_anal(self, char: Character, play_count: int) -> None:
        char.exp[1] = char.exp.get(1, 0) + play_count
        char.exp[5] = char.exp.get(5, 0) + play_count
        char.juel[2] = char.juel.get(2, 0) + play_count * 200
        char.juel[5] = char.juel.get(5, 0) + play_count * 250






    def _apply_dungeon_bitch_play_effects_animal(self, char: Character, play_count: int) -> None:
        char.exp[56] = char.exp.get(56, 0) + play_count
        char.exp[0] = char.exp.get(0, 0) + play_count
        char.exp[5] = char.exp.get(5, 0) + play_count
        char.juel[1] = char.juel.get(1, 0) + play_count * 200
        char.juel[6] = char.juel.get(6, 0) + play_count * 300
        char.juel[8] = char.juel.get(8, 0) + play_count * 200






    def _apply_dungeon_bitch_play_effects_hand(self, char: Character, play_count: int) -> None:
        char.exp[20] = char.exp.get(20, 0) + play_count
        char.juel[7] = char.juel.get(7, 0) + play_count * 5






    def _apply_dungeon_bitch_play_effects_les(self, char: Character, play_count: int) -> None:
        char.exp[40] = char.exp.get(40, 0) + play_count
        char.exp[2] = char.exp.get(2, 0) + play_count * max(1, 1 + int(char.abl.get(10, 0)) // 5)
        char.juel[0] = char.juel.get(0, 0) + play_count * 100 * max(1, 1 + int(char.abl.get(10, 0)))
        char.juel[5] = char.juel.get(5, 0) + play_count * 200






    def _apply_dungeon_bitch_play_effects_oral(self, char: Character, play_count: int) -> None:
        char.exp[22] = char.exp.get(22, 0) + play_count
        char.exp[20] = char.exp.get(20, 0) + play_count
        char.juel[7] = char.juel.get(7, 0) + play_count * 10






    def _apply_dungeon_bitch_play_effects_sex(self, char: Character, play_count: int) -> None:
        char.exp[0] = char.exp.get(0, 0) + play_count
        char.exp[5] = char.exp.get(5, 0) + play_count
        char.juel[1] = char.juel.get(1, 0) + play_count * 200
        char.juel[5] = char.juel.get(5, 0) + play_count * 250






    def _apply_dungeon_bitch_species_factor(self, char: Character, count: int) -> int:
        if char.talent.get(100, 0):
            if char.talent.get(10, 0):
                count += 1
            if char.talent.get(109, 0):
                count += 1
            if char.talent.get(116, 0):
                count += 2
        return count






    def _apply_dungeon_bitch_talent_factor(self, char: Character, count: int) -> int:
        count += sum(int(char.talent.get(idx, 0)) for idx in [23, 28, 31, 33, 91, 92, 113, 83, 87, 88])
        count -= sum(int(char.talent.get(idx, 0)) for idx in [21, 22, 24, 27, 30])
        if char.talent.get(110, 0):
            count += 1
        if char.talent.get(114, 0):
            count += 2
        return count






    def _apply_dungeon_bitch_work(self, char: Character) -> List[str]:
        if not self._can_apply_dungeon_bitch_work(char):
            return []
        customer_count = self._get_dungeon_bitch_customer_count(char)
        success_score = self._get_dungeon_bitch_success_score(char)
        failure_score = self._get_dungeon_bitch_base_failure(char)
        success_count, total_income, total_play, play_totals, customer_kinds = self._build_dungeon_bitch_work_round_totals(
            char,
            customer_count,
            success_score,
            failure_score,
        )
        if success_count <= 0:
            return []
        return self._finalize_dungeon_bitch_work(char, total_income, total_play, play_totals, customer_kinds)






    def _apply_dungeon_consumable_effect(self, char: Character, item_id: int, appraise: int, timing: str) -> Optional[str]:
        hp = int(char.base.get(0, 0))
        max_hp = max(1, int(char.maxbase.get(0, 1)))
        mp = int(char.base.get(1, 0))
        max_mp = max(1, int(char.maxbase.get(1, 1)))

        if item_id == 400 and hp < (max_hp * 6) // 10:
            if appraise and random.randint(0, 1) == 0:
                char.juel[5] = int(char.juel.get(5, 0)) + 30
                return f"{char.name} 误食了奇怪的草，欲情点数 +30。"
            char.base[0] = min(max_hp, hp + 500)
            return f"{char.name} 吃下了草药，HP+{char.base[0] - hp}。"
        if item_id == 401 and mp < (max_mp * 6) // 10:
            if appraise and random.randint(0, 1) == 0:
                char.exp[20] = int(char.exp.get(20, 0)) + 1
                return f"{char.name} 喝下了可疑液体，精液经验 +1。"
            char.base[1] = min(max_mp, mp + 500)
            return f"{char.name} 喝下了恢复药水，MP+{char.base[1] - mp}。"
        if item_id == 402 and hp < (max_hp * 8) // 10:
            if appraise and random.randint(0, 1) == 0:
                char.exp[10] = int(char.exp.get(10, 0)) + 1
                char.juel[0] = int(char.juel.get(0, 0)) + 10
                char.juel[5] = int(char.juel.get(5, 0)) + 20
                return f"{char.name} 挥动了诅咒之杖，自慰经验 +1。"
            char.base[0] = min(max_hp, hp + 200)
            if not appraise and random.randint(0, 2) > 0:
                return None
            return f"{char.name} 使用了回复之杖，HP+{char.base[0] - hp}。"
        if item_id == 403 and mp < (max_mp * 8) // 10:
            cursed = appraise and random.randint(0, 1) == 0 and int(char.exp.get(1, 0)) > 0
            if cursed:
                char.exp[10] = int(char.exp.get(10, 0)) + 1
                char.exp[1] = int(char.exp.get(1, 0)) + 1
                char.juel[2] = int(char.juel.get(2, 0)) + 10
                char.juel[5] = int(char.juel.get(5, 0)) + 20
                return f"{char.name} 挥动了诅咒之杖，肛门经验 +1。"
            char.base[1] = min(max_mp, mp + 200)
            if not appraise and random.randint(0, 2) > 0:
                return None
            return f"{char.name} 使用了精神之杖，MP+{char.base[1] - mp}。"
        if item_id == 404:
            if appraise and random.randint(0, 3) == 0:
                if int(char.talent.get(101, 0)) == 1:
                    char.talent[101] = 0
                elif int(char.talent.get(101, 0)) == 0 and int(char.talent.get(102, 0)) == 0:
                    char.talent[102] = 1
                else:
                    char.juel[0] = int(char.juel.get(0, 0)) + 10
                return f"{char.name} 吃下了奇怪的种子，阴核相关素质发生了变化。"
            char.cflag[13] = int(char.cflag.get(13, 0)) + 1
            return f"{char.name} 吃下了力量种子，攻击力 +1。"
        if item_id == 405:
            if appraise and random.randint(0, 3) == 0:
                if int(char.talent.get(107, 0)) == 1:
                    char.talent[107] = 0
                elif int(char.talent.get(107, 0)) == 0 and int(char.talent.get(108, 0)) == 0:
                    char.talent[108] = 1
                else:
                    char.juel[14] = int(char.juel.get(14, 0)) + 10
                return f"{char.name} 吃下了奇怪的种子，胸部相关素质发生了变化。"
            char.cflag[14] = int(char.cflag.get(14, 0)) + 1
            return f"{char.name} 吃下了守护种子，防御力 +1。"
        if item_id == 406:
            if appraise and random.randint(0, 1) == 0:
                char.juel[4] = int(char.juel.get(4, 0)) + 10
                return f"{char.name} 使用了魔鬼硬币，恭顺点数 +10。"
            char.exp[80] = int(char.exp.get(80, 0)) + 50
            return f"{char.name} 使用了经验硬币，经验值 +50。"
        if item_id == 407:
            if appraise and random.randint(0, 3) == 0 and not char.talent.get(122, 0):
                if int(char.talent.get(103, 0)) == 1:
                    char.talent[103] = 0
                elif int(char.talent.get(103, 0)) == 0 and int(char.talent.get(104, 0)) == 0:
                    char.talent[104] = 1
                else:
                    char.juel[5] = int(char.juel.get(5, 0)) + 10
                return f"{char.name} 吃下了奇怪的种子，私处相关素质发生了变化。"
            char.maxbase[0] = int(char.maxbase.get(0, 0)) + 10
            return f"{char.name} 吃下了生命种子，最大HP +10。"
        if item_id == 408:
            if appraise and random.randint(0, 3) == 0:
                if int(char.talent.get(105, 0)) == 1:
                    char.talent[105] = 0
                elif int(char.talent.get(105, 0)) == 0 and int(char.talent.get(106, 0)) == 0:
                    char.talent[106] = 1
                else:
                    char.juel[2] = int(char.juel.get(2, 0)) + 10
                return f"{char.name} 吃下了奇怪的种子，肛门相关素质发生了变化。"
            char.maxbase[1] = int(char.maxbase.get(1, 0)) + 5
            return f"{char.name} 吃下了心之种子，最大MP +5。"
        if item_id == 409:
            if appraise and random.randint(0, 1) == 0:
                char.juel[6] = int(char.juel.get(6, 0)) + 30
                return f"{char.name} 使用了黑暗银币，屈服点数 +30。"
            char.exp[80] = int(char.exp.get(80, 0)) + 150
            return f"{char.name} 使用了经验银币，经验值 +150。"
        if item_id == 410:
            if appraise and random.randint(0, 1) == 0:
                if int(char.talent.get(316, 0)) == 12:
                    char.juel[6] = int(char.juel.get(6, 0)) + 10
                char.juel[5] = int(char.juel.get(5, 0)) + 15
                return f"{char.name} 喝下了可疑液体，欲情点数 +15。"
            if int(char.talent.get(316, 0)) == 12:
                char.cflag[13] = int(char.cflag.get(13, 0)) + 1
                char.cflag[14] = int(char.cflag.get(14, 0)) + 1
            self._add_character_karma(char, 1)
            return f"{char.name} 饮下了圣水，善恶值 +1。"
        if item_id == 411 and random.randint(0, 4) == 0:
            char.juel[6] = int(char.juel.get(6, 0)) + 5
            if int(char.cflag.get(1, 0)) == 3:
                return f"{char.name} 使用了堕落宝石箱，屈服点数 +5。"
            return None
        if item_id == 412 and timing == "战斗中" and not self._get_character_flag_bit(char, 503, DUNGEON_STATE_INVISIBLE_BIT):
            cursed = appraise and random.randint(0, 2) == 0
            if cursed:
                if int(char.talent.get(35, 0)):
                    char.juel[6] = int(char.juel.get(6, 0)) + 10
                char.juel[8] = int(char.juel.get(8, 0)) + 15
                return f"{char.name} 喝下了可疑液体，耻情点数 +15。"
            self._set_character_flag_bit(char, 503, DUNGEON_STATE_INVISIBLE_BIT, True)
            return f"{char.name} 喝下了透明化之药，进入透明状态。"
        if item_id == 413 and timing == "战斗中" and not self._get_character_flag_bit(char, 503, DUNGEON_STATE_HERO_BIT):
            up_value = self._get_character_level(char) // 10 + 10
            if appraise and random.randint(0, 2) == 0:
                char.juel[10] = int(char.juel.get(10, 0)) + 10
                return f"{char.name} 喝下了恐惧药水，恐怖点数 +10。"
            char.cflag[11] = int(char.cflag.get(11, 0)) + up_value
            char.cflag[12] = int(char.cflag.get(12, 0)) + up_value
            self._set_character_flag_bit(char, 503, DUNGEON_STATE_HERO_BIT, True)
            return f"{char.name} 喝下了英雄之药，攻击与防御暂时提升。"
        return None






    def _apply_dungeon_curse_trap_state(self, leader: Character, floor: int) -> List[str]:
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_CURSE_BIT):
            return [f"{leader.name} 身上的诅咒再次作响。"]
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_CURSE_BIT, True)
        return [f"{leader.name} 被诅咒了。"]






    def _apply_dungeon_damage(self, leader: Character, hp_damage: int = 0, mp_damage: int = 0):
        if hp_damage > 0:
            leader.base[0] = max(1, leader.base.get(0, 0) - hp_damage)
        if mp_damage > 0:
            leader.base[1] = max(0, leader.base.get(1, 0) - mp_damage)






    def _apply_dungeon_equip_reward(self, leader: Character) -> List[str]:
        messages: List[str] = []
        if leader.cflag.get(1, 0) != 2:
            return messages
        if random.randint(0, 3) != 0:
            return messages
        floor = max(1, int(leader.cflag.get(501, 1)))
        reward_id = int(self._get_dungeon_floor_treasure(floor))
        if reward_id < 300:
            return messages
        if self._get_active_campaign_id() <= 0:
            player = self._get_player()
            if player is None or not self._is_item_owned(player, reward_id):
                return messages
            self._use_item(player, self._get_item_name(reward_id), 1)
        ring_message = self._try_apply_dungeon_ring_reward(leader, reward_id)
        if ring_message is not None:
            messages.append(ring_message)
            return messages
        messages.append("似乎没什么好东西。")
        return messages






    def _apply_dungeon_fire_trap_state(self, leader: Character, floor: int) -> List[str]:
        if not self._get_character_flag_bit(leader, 503, DUNGEON_STATE_SLIPPERY_BIT):
            return []
        extra_damage = 30 + self._get_dungeon_master_level() * 5
        self._apply_dungeon_damage(leader, hp_damage=extra_damage)
        return [f"火焰点燃了她身上的油污，追加造成 HP-{extra_damage}。"]






    def _apply_dungeon_illusion_trap_state(self, leader: Character, floor: int) -> List[str]:
        roll = self._roll_dungeon_arousal_trap_check(leader)
        if int(leader.talent.get(122, 0)) and roll < 20:
            return [f"{leader.name} 从幻境里察觉到了破绽，提前挣脱了出来。"]
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
        return [f"{leader.name} 被幻境中的欲望景象扰乱了心神。"]






    def _apply_dungeon_imitator_room_trap_state(self, leader: Character, floor: int) -> List[str]:
        roll = random.randint(0, 99)
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            roll -= 10
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
        if roll < 10:
            leader.cflag[11] = 0
            leader.cflag[12] = 0
            return [f"{leader.name} 被拟态房间与媚药彻底压制，攻击和防御暂时降为 0。"]
        leader.cflag[11] = int(leader.cflag.get(11, 0)) // 2
        leader.cflag[12] = int(leader.cflag.get(12, 0)) // 2
        return [f"{leader.name} 在拟态房间里被媚药扰乱了心神，攻击和防御暂时减半。"]






    def _apply_dungeon_junk_loot(self, char: Character) -> List[str]:
        player_level = self._get_dungeon_master_level()
        char_level = max(0, self._get_character_level(char))
        loot = 100 + char_level * random.randint(0, max(1, int(math.sqrt(player_level + char_level + 1))))
        loot += self._get_dungeon_junk_loot_bonus(char)
        loot *= max(1, int(char.cflag.get(501, 1)))
        loot = max(1, loot)
        self._add_dungeon_party_loot(char, loot)
        return [f"{char.name} 找到了价值 {loot} 的财物。"]






    def _apply_dungeon_launch_trap_state(self, leader: Character, floor: int) -> List[str]:
        if int(leader.cflag.get(502, 0)) < 40:
            return []
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 20)
            messages.append("连续坠落让她再次被抛飞，额外损失 20 点气力。")
        else:
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT, True)
            messages.append(f"{leader.name} 突然被弹射了出去。")
        if random.randint(0, 2) > 0:
            next_floor = min(9, int(leader.cflag.get(501, floor)) + 1)
            leader.cflag[501] = next_floor
            leader.cflag[509] = 1
            messages.append(f"{leader.name} 被甩到了更深处的第{next_floor}层附近，并因此迷路了。")
            if self._split_character_from_party(leader):
                messages.append(f"{leader.name} 和同伴失散了。")
        return messages






    def _apply_dungeon_love_bath_trap_state(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 20)
            messages.append("坠落让她掉进了更深的媚药泥沼，额外损失 20 点气力。")
        if not self._get_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT):
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
            messages.append("大量媚药让她进入了发情状态。")
        return messages






    def _apply_dungeon_love_bug_trap_state(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 10)
            messages.append("坠落让她直接摔进了淫虫巢穴，额外损失 10 点气力。")
        if random.randint(0, 99) >= 80:
            messages.append(f"{leader.name} 在巢穴里扭伤了脚。")
        return messages






    def _apply_dungeon_love_gas_trap_state(self, leader: Character, floor: int) -> List[str]:
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
        return [f"{leader.name} 吸入催情气体后，明显进入了发情状态。"]






    def _apply_dungeon_oil_trap_state(self, leader: Character, floor: int) -> List[str]:
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_SLIPPERY_BIT):
            return [f"{leader.name} 身上本来就黏糊糊的。"]
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_SLIPPERY_BIT, True)
        return [f"{leader.name} 被油泼了一身，进入了黏滑状态。"]






    def _apply_dungeon_one_way_trap_state(self, leader: Character, floor: int) -> List[str]:
        if int(leader.cflag.get(502, 0)) < 40:
            return []
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 20)
            messages.append("坠落后的道路被彻底封死了，额外损失 20 点气力。")
        if random.randint(0, 2) <= 1:
            leader.cflag[509] = 1
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - (20 + self._get_dungeon_master_level()))
            messages.append(f"{leader.name} 在封闭通道里迷路了。")
        return messages






    def _apply_dungeon_party_equip_rewards(self, leader: Character) -> List[str]:
        messages: List[str] = []
        for member in self._iter_dungeon_treasure_candidates(leader):
            messages.extend(self._apply_dungeon_equip_reward(member))
        return messages






    def _apply_dungeon_party_night_rituals(self, leader: Character) -> List[str]:
        messages: List[str] = []
        party = self._get_dungeon_town_party(leader)
        for member in party[1:]:
            if member.cflag.get(1, 0) != 3:
                continue
            messages.append(f"{member.name} 在大家都熟睡后开始了奇妙的仪式……（同伴的善良值-1）")
            for target in party:
                if target is member:
                    continue
                self._add_character_karma(target, -1)
        return messages






    def _apply_dungeon_pit_trap_state(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 10)
            messages.append("连续坠落让她又损失了 10 点气力。")
        else:
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT, True)
            messages.append("这次坠落留下了坠落状态。")
        return messages






    def _apply_dungeon_post_battle_loot(self, leader: Character) -> List[str]:
        messages: List[str] = []
        loot_value = 100 + self._get_character_level(leader) * max(1, random.randint(1, max(1, int(math.sqrt(self._get_character_level(leader) + 1)))))
        loot_value *= max(1, leader.cflag.get(501, 1))
        loot_value = max(1, loot_value)
        self._add_dungeon_party_loot(leader, loot_value)
        messages.append(f"{leader.name} 搜刮到了价值 {loot_value} 的战利品。")
        return messages






    def _apply_dungeon_progress(self, leader: Character, delta: int) -> tuple[int, int, bool]:
        floor_before = max(1, leader.cflag.get(501, 1))
        progress = leader.cflag.get(502, 0) + delta
        advanced = False

        if delta >= 0:
            if progress >= 100:
                leader.cflag[502] = 0
                leader.cflag[501] = min(9, floor_before + 1)
                leader.cflag[508] = leader.cflag.get(508, 0) + 1
                advanced = True
            else:
                leader.cflag[502] = max(0, progress)
                leader.cflag[501] = floor_before
        else:
            if progress <= 0:
                leader.cflag[502] = 0
                leader.cflag[501] = max(1, floor_before - 1)
            else:
                leader.cflag[502] = min(100, progress)
                leader.cflag[501] = floor_before

        return floor_before, leader.cflag.get(501, 1), advanced






    def _apply_dungeon_punishment_choice_1(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被绑在电椅上，以较弱的电流接受了折磨。")
        char.juel[9] = char.juel.get(9, 0) + desire_power
        char.juel[6] = char.juel.get(6, 0) + desire_power
        if int(char.abl.get(21, 0)) >= 3:
            char.juel[5] = char.juel.get(5, 0) + obedience_power
        return messages






    def _apply_dungeon_punishment_choice_2(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被命令在地下城主干道中央当众自慰。")
        char.juel[6] = char.juel.get(6, 0) + desire_power
        if int(char.abl.get(17, 0)) >= 4:
            char.juel[5] = char.juel.get(5, 0) + obedience_power
            char.exp[10] = char.exp.get(10, 0) + 3
            char.exp[11] = char.exp.get(11, 0) + 3
        else:
            char.juel[8] = char.juel.get(8, 0) + desire_power
            char.exp[10] = char.exp.get(10, 0) + 1
            char.exp[11] = char.exp.get(11, 0) + 1
        return messages






    def _apply_dungeon_punishment_choice_3(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被命令在地下城主干道中央脱粪示众。")
        char.juel[6] = char.juel.get(6, 0) + desire_power
        if int(char.abl.get(17, 0)) >= 6:
            char.juel[5] = char.juel.get(5, 0) + obedience_power
            char.exp[10] = char.exp.get(10, 0) + 3
        else:
            char.juel[8] = char.juel.get(8, 0) + desire_power
        return messages






    def _apply_dungeon_punishment_choice_4(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被绑起来，受到了鞭打处罚。")
        char.juel[9] = char.juel.get(9, 0) + desire_power
        char.juel[6] = char.juel.get(6, 0) + desire_power
        if int(char.abl.get(21, 0)) >= 3:
            char.juel[5] = char.juel.get(5, 0) + obedience_power
        return messages






    def _apply_dungeon_punishment_choice_5(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被固定在小便器上，遭受了淋尿处罚。")
        char.juel[9] = char.juel.get(9, 0) + desire_power
        char.juel[6] = char.juel.get(6, 0) + desire_power
        if char.talent.get(88, 0) or char.talent.get(76, 0):
            char.juel[5] = char.juel.get(5, 0) + obedience_power
        return messages






    def _apply_dungeon_punishment_choice_6(self, char: Character, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 的处罚是打扫厕所。")
        char.juel[6] = char.juel.get(6, 0) + desire_power
        return messages






    def _apply_dungeon_punishment_choice_7(self, char: Character, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 的处罚是不给饭食。")
        char.juel[6] = char.juel.get(6, 0) + desire_power
        return messages






    def _apply_dungeon_punishment_choice_8(self, char: Character, obedience_power: int, desire_power: int, messages: List[str]) -> List[str]:
        messages.append(f"{char.name} 被固定后注射了危险剂量的媚药，接受了放置处罚。")
        char.juel[9] = char.juel.get(9, 0) + desire_power
        char.juel[5] = char.juel.get(5, 0) + obedience_power
        char.juel[6] = char.juel.get(6, 0) + desire_power
        char.exp[57] = char.exp.get(57, 0) + 10
        return messages






    def _apply_dungeon_punishment_event(self, char: Character) -> List[str]:
        choice = self._choose_dungeon_punishment_option(char)
        return self._apply_selected_dungeon_punishment(char, choice)






    def _apply_dungeon_quest_battle_actor_state_bonus(self, actor: Character, messages: List[str]) -> int:
        modifier = self._get_dungeon_quest_battle_actor_stat_modifier(actor)
        current_attack = int(actor.cflag.get(11, 0))
        current_defense = int(actor.cflag.get(12, 0))
        base_attack = int(actor.cflag.get(13, current_attack))
        base_defense = int(actor.cflag.get(14, current_defense))

        if self._get_character_flag_bit(actor, 503, DUNGEON_STATE_INVISIBLE_BIT):
            if self._get_character_flag_bit(actor, 503, DUNGEON_STATE_PREEMPT_BLOCKED_BIT):
                messages.append(f"{actor.name} 虽然保持着透明状态，但没能抢到先机。")
            else:
                modifier += 8
                messages.append(f"{actor.name} 借着透明状态抢到了先机。")

        if self._get_character_flag_bit(actor, 503, DUNGEON_STATE_HERO_BIT):
            messages.append(f"{actor.name} 身上的英雄药效果仍在持续。")
            modifier += 4

        if current_attack < base_attack:
            messages.append(f"{actor.name} 的攻击状态明显受到了压制。")
        elif current_attack > base_attack:
            messages.append(f"{actor.name} 的攻击状态比平时更好。")

        if current_defense < base_defense:
            messages.append(f"{actor.name} 的防御状态明显受到了压制。")
        elif current_defense > base_defense:
            messages.append(f"{actor.name} 的防御状态比平时更稳。")

        return modifier






    def _apply_dungeon_quest_battle_defeat_state(self, actor: Character) -> None:
        self._set_character_captured_standby_state(actor)
        self._split_character_from_party(actor)






    def _apply_dungeon_quest_battle_domination_capture(self, quest_party: List[Character], leader: Character, messages: List[str]) -> None:
        target_id = int(leader.cflag.get(538, 0))
        if target_id < 100:
            return

        candidates = [actor for actor in quest_party if self._get_ring_effect_strength(actor, 9) > 0]
        if not candidates:
            return

        current_best = max((int(actor.cflag.get(570, 0)) for actor in candidates), default=0)
        if target_id <= current_best:
            return

        captor = max(candidates, key=lambda actor: self._get_ring_effect_strength(actor, 9))
        captor.cflag[570] = target_id
        messages.append(f"{captor.name} 捕捉了濒死的{self._get_item_name(target_id)}，并支配了其精神。")






    def _apply_dungeon_quest_battle_loot(self, actor: Character) -> List[str]:
        if not self._should_character_loot_after_quest_battle(actor):
            return []
        loot = self._build_dungeon_quest_battle_loot_value(actor)
        self._add_character_karma(actor, -5)
        self._add_dungeon_party_loot(actor, loot)
        return [f"{actor.name} 在任务战后开始搜刮战利品，善恶值下降了。获得了价值 {loot} 的财物。"]






    def _apply_dungeon_quest_battle_party_loot(self, quest_party: List[Character], messages: List[str]) -> None:
        for actor in quest_party:
            messages.extend(self._apply_dungeon_quest_battle_loot(actor))






    def _apply_dungeon_quest_battle_party_recovery(self, quest_party: List[Character], messages: List[str]) -> None:
        for actor in quest_party:
            messages.extend(self._apply_character_dungeon_battle_restore(actor))
            messages.extend(self._apply_character_dungeon_battle_skill_extra_bonus(actor))






    def _apply_dungeon_quest_battle_party_state_bonus(self, quest_party: List[Character], messages: List[str]) -> int:
        total_modifier = 0
        for actor in quest_party:
            total_modifier += self._apply_dungeon_quest_battle_actor_state_bonus(actor, messages)
        return total_modifier






    def _apply_dungeon_quest_battle_prechecks(self, leader: Character, flags: int, quest_party: List[Character], messages: List[str]):
        for actor in quest_party:
            messages.extend(self._apply_dungeon_auto_consumables(actor, "战斗中"))
        if flags & (1 << 0):
            messages.append("这次任务战带着头目战的气息，敌方核心目标已经现身。")
        if flags & (1 << 3):
            messages.append("任务对象身边聚集了异常多的敌人。")
            for actor in quest_party:
                hp_damage = max(5, self._get_character_level(actor))
                self._apply_dungeon_damage(actor, hp_damage=hp_damage)
                messages.append(f"{actor.name} 在乱战中受伤，HP-{hp_damage}。")
        if flags & (1 << 1) and quest_party:
            trap_actor = random.choice(quest_party)
            messages.extend(self._apply_dungeon_quest_battle_trap(trap_actor))






    def _apply_dungeon_quest_battle_sex_request(self, leader: Character, flags: int, messages: List[str]) -> bool:
        if not (flags & (1 << 4)):
            return False
        score = 100
        if int(leader.exp.get(74, 0)) > 0:
            score += int(leader.exp.get(74, 0))
        if int(leader.cflag.get(151, 0)) < -30:
            score += 10
        if int(leader.cflag.get(151, 0)) < -60:
            score += 20
        messages.append("敌人提出了性方面的要求，双方短暂交涉了一轮。")
        if random.randint(0, max(100, score)) > 100:
            leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 1)
            leader.exp[74] = int(leader.exp.get(74, 0)) + 1
            self._add_character_karma(leader, -1)
            messages.append(f"{leader.name} 接受了任务战中的性要求，{self._build_dungeon_quest_name(leader)}直接完成了。")
            return True
        messages.append(f"{leader.name} 在任务战里拒绝了对方的性要求。")
        return False






    def _apply_dungeon_quest_battle_slave_monster_attack(self, quest_party: List[Character], messages: List[str]) -> int:
        total_bonus = 0
        for actor in quest_party:
            total_bonus += self._apply_single_dungeon_quest_slave_monster_attack(actor, messages)
        return total_bonus






    def _apply_dungeon_quest_battle_success_result(self, leader: Character, flags: int, messages: List[str]):
        leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 1)
        if flags & (1 << 0):
            messages.append(f"{leader.name} 在任务战中击破了头目。")
        messages.append(f"{leader.name} 通过任务战完成了{self._build_dungeon_quest_name(leader)}。")






    def _apply_dungeon_quest_battle_trap(self, actor: Character) -> List[str]:
        messages: List[str] = []
        hp_damage = max(6, self._get_character_level(actor) * 2)
        mp_damage = max(3, self._get_character_level(actor))
        progress_loss = 5
        trap_roll = random.randint(0, 2)
        if trap_roll == 0:
            hp_damage += 6
            messages.append(f"{actor.name} 在任务战前被箭雨压制，HP-{hp_damage}。")
            self._apply_dungeon_damage(actor, hp_damage=hp_damage)
        elif trap_roll == 1:
            hp_damage += 3
            mp_damage += 6
            messages.append(f"{actor.name} 在任务战前踩进了油坑，HP-{hp_damage} MP-{mp_damage}。")
            self._apply_dungeon_damage(actor, hp_damage=hp_damage, mp_damage=mp_damage)
        else:
            mp_damage += 10
            progress_loss += 5
            messages.append(f"{actor.name} 在任务战前遭到压制，MP-{mp_damage}，侵攻度-{progress_loss}。")
            self._apply_dungeon_damage(actor, mp_damage=mp_damage)
        actor.cflag[502] = max(0, int(actor.cflag.get(502, 0)) - progress_loss)
        return messages






    def _apply_dungeon_quest_deadline_tick(self, leader: Character, messages: List[str]) -> bool:
        if int(leader.cflag.get(539, 0)) > 0:
            leader.cflag[539] = int(leader.cflag.get(539, 0)) - 1
        if int(leader.cflag.get(539, 0)) < 1:
            leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 2)
            messages.append(f"{leader.name} 没能在期限内完成{self._build_dungeon_quest_name(leader)}。")
            return True
        return False






    def _apply_dungeon_quest_exploration_result(self, leader: Character, flags: int, messages: List[str]) -> None:
        success_roll = random.randint(0, 2)
        if flags & (1 << 0):
            success_roll = random.randint(0, 3)
        if success_roll != 0:
            return
        if flags & (1 << 5):
            leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 2)
            messages.append(f"{leader.name} 发现{self._build_dungeon_quest_name(leader)}只是个假委托。")
            return
        if flags & (1 << 0):
            messages.append(f"{leader.name} 艰难地击败了委托中的头目。")
        leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 1)
        messages.append(f"{leader.name} 在探索途中完成了{self._build_dungeon_quest_name(leader)}。")






    def _apply_dungeon_quest_hazard_effects(self, leader: Character, flags: int, messages: List[str]) -> bool:
        if flags & (1 << 3) and random.randint(0, 1) == 0:
            hp_damage = max(8, self._get_character_level(leader) * 3)
            self._apply_dungeon_damage(leader, hp_damage=hp_damage)
            messages.append(f"{leader.name} 被委托中的大量敌人围攻，HP-{hp_damage}。")
        if flags & (1 << 1) and random.randint(0, 2) == 0:
            hp_damage = max(5, self._get_character_level(leader) * 2)
            mp_damage = max(3, self._get_character_level(leader))
            self._apply_dungeon_damage(leader, hp_damage=hp_damage, mp_damage=mp_damage)
            messages.append(f"{leader.name} 在委托途中触发了额外陷阱，HP-{hp_damage} MP-{mp_damage}。")
        return False






    def _apply_dungeon_quest_sex_requirement(self, leader: Character, flags: int, messages: List[str]) -> bool:
        if not (flags & (1 << 4)):
            return False
        score = 100
        if int(leader.exp.get(74, 0)) > 0:
            score += int(leader.exp.get(74, 0))
        if int(leader.cflag.get(151, 0)) < -30:
            score += 10
        if int(leader.cflag.get(151, 0)) < -60:
            score += 20
        if random.randint(0, max(100, score)) > 100:
            leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 1)
            leader.exp[74] = int(leader.exp.get(74, 0)) + 1
            self._add_character_karma(leader, -1)
            messages.append(f"{leader.name} 接受了委托对象的性要求，委托直接完成了。")
            return True
        messages.append(f"{leader.name} 拒绝了委托中的性要求。")
        return False






    def _apply_dungeon_random_member_post_battle_effects(self, char: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_dungeon_bitch_work(char))
        messages.extend(self._apply_dungeon_animal_relief(char))
        messages.extend(self._apply_dungeon_self_relief(char))
        messages.extend(self._apply_dungeon_side_work(char))
        return messages






    def _apply_dungeon_rest_phase(self, leader: Character) -> List[str]:
        if leader.cflag.get(1, 0) == 2 and self._get_character_flag_bit(leader, 503, DUNGEON_STATE_CAMP_BIT) and leader.cflag.get(501, 1) > 1:
            return [f"{leader.name} 躲起来休息。"]
        return []






    def _apply_dungeon_retreat_decision(self, leader: Character, floor: int) -> List[str]:
        if leader.cflag.get(507, 0):
            return [f"{leader.name} 正在地下城内撤退中（当前第{floor}阶层）。"]
        grade = self._calculate_dungeon_status_grade(leader)
        should_retreat, retreat_goal, message = self._should_start_dungeon_retreat(leader, floor, grade)
        if not should_retreat:
            return [message] if message else []
        leader.cflag[507] = 1
        leader.cflag[520] = max(1, int(retreat_goal))
        return [message] if message else []






    def _apply_dungeon_reward_event(self, char: Character) -> List[str]:
        choice = self._choose_dungeon_reward_option(char)
        if choice == 0:
            messages = self._apply_dungeon_reward_refusal(char)
        elif choice == 1:
            messages = self._apply_dungeon_reward_medal(char)
        else:
            messages = [
                f"{char.name} 希望得到的奖励是：{self._build_dungeon_reward_request_text(char)}。",
            ]
            messages.extend(self._apply_dungeon_reward_request_effect(char))
        char.cflag[504] = 0
        return messages






    def _apply_dungeon_reward_medal(self, char: Character) -> List[str]:
        char.exp[81] = char.exp.get(81, 0) + 1
        return [
            f"{char.name} 被授予了一枚勋章。",
            "勋章经验 +1。",
        ]






    def _apply_dungeon_reward_refusal(self, char: Character) -> List[str]:
        refusal = max(0, int(char.cflag.get(9, 0)) * 60)
        char.juel[100] = char.juel.get(100, 0) + refusal
        return [
            f"{char.name} 嘟着嘴回到了自己的房间。",
            f"否定点数 +{refusal}。",
        ]






    def _apply_dungeon_reward_request_beast_reward(
        self,
        char: Character,
        messages: List[str],
        request_id: int,
        reward_power: int,
    ) -> List[str]:
        lust_key = 2 if char.talent.get(0, 0) else 1
        char.juel[lust_key] = char.juel.get(lust_key, 0) + reward_power
        char.juel[5] = char.juel.get(5, 0) + reward_power
        if request_id == 3:
            exp_key = 53 if char.talent.get(0, 0) else 52
            char.exp[exp_key] = char.exp.get(exp_key, 0) + 10
        char.exp[1 if char.talent.get(0, 0) else 0] = char.exp.get(1 if char.talent.get(0, 0) else 0, 0) + 10
        char.exp[2] = char.exp.get(2, 0) + 5
        char.exp[56] = char.exp.get(56, 0) + 10
        messages.append(f"{char.name} 得到了兽奸系的奖赏。")
        return messages






    def _apply_dungeon_reward_request_effect(self, char: Character) -> List[str]:
        messages: List[str] = []
        request_id = int(char.cflag.get(504, 0))
        reward_power = max(150, 150 * (2 ** max(0, min(10, int(char.abl.get(10, 0))))))
        if request_id == 0:
            return self._apply_dungeon_reward_request_refusal(char, messages)
        if request_id in {1, 2, 3}:
            return self._apply_dungeon_reward_request_beast_reward(char, messages, request_id, reward_power)
        if request_id == 4:
            return self._apply_dungeon_reward_request_loving_reward(char, messages)
        if request_id == 5:
            return self._apply_dungeon_reward_request_sex_reward(char, messages, reward_power)
        if request_id == 6:
            return self._apply_dungeon_reward_request_semen_reward(char, messages, reward_power)
        if request_id == 7:
            return self._apply_dungeon_reward_request_orgy_reward(char, messages, reward_power)
        if request_id == 8:
            return self._apply_dungeon_reward_request_urine_reward(char, messages, reward_power)
        if request_id == 9:
            return self._apply_dungeon_reward_request_virgin_hunt_reward(char, messages, reward_power)
        return messages






    def _apply_dungeon_reward_request_loving_reward(self, char: Character, messages: List[str]) -> List[str]:
        char.exp[23] = char.exp.get(23, 0) + 10
        messages.append(f"{char.name} 得到了温柔的接吻，爱情经验 +10。")
        return messages






    def _apply_dungeon_reward_request_orgy_reward(self, char: Character, messages: List[str], reward_power: int) -> List[str]:
        lust_key = 2 if char.talent.get(0, 0) else 1
        exp_key = 1 if char.talent.get(0, 0) else 0
        char.juel[lust_key] = char.juel.get(lust_key, 0) + reward_power
        char.juel[5] = char.juel.get(5, 0) + reward_power
        char.exp[exp_key] = char.exp.get(exp_key, 0) + 10
        char.exp[2] = char.exp.get(2, 0) + 5
        messages.append(f"{char.name} 得到了乱交派对式的奖赏。")
        return messages






    def _apply_dungeon_reward_request_refusal(self, char: Character, messages: List[str]) -> List[str]:
        amount = max(0, int(char.cflag.get(9, 0)) * 100)
        if amount > 0 and self.interpreter.vars.money >= amount:
            self._spend_global_money(amount)
            messages.append(f"你赐给了 {char.name} {amount} pts。")
        else:
            refusal = max(0, int(char.cflag.get(9, 0)) * 60)
            char.juel[100] = char.juel.get(100, 0) + refusal
            messages.append(f"金库不够支付 {char.name} 想要的报酬，否定点数 +{refusal}。")
        return messages






    def _apply_dungeon_reward_request_semen_reward(self, char: Character, messages: List[str], reward_power: int) -> List[str]:
        char.juel[5] = char.juel.get(5, 0) + reward_power
        char.exp[22] = char.exp.get(22, 0) + 10
        char.exp[20] = char.exp.get(20, 0) + 5
        messages.append(f"{char.name} 得到了精液奖赏。")
        return messages






    def _apply_dungeon_reward_request_sex_reward(self, char: Character, messages: List[str], reward_power: int) -> List[str]:
        lust_key = 2 if int(char.abl.get(3, 0)) > int(char.abl.get(2, 0)) else 1
        exp_key = 1 if lust_key == 2 else 0
        char.juel[lust_key] = char.juel.get(lust_key, 0) + reward_power
        char.juel[5] = char.juel.get(5, 0) + reward_power
        char.exp[exp_key] = char.exp.get(exp_key, 0) + 10
        char.exp[5] = char.exp.get(5, 0) + 10
        char.exp[2] = char.exp.get(2, 0) + 5
        messages.append(f"{char.name} 得到了性交奖赏。")
        return messages






    def _apply_dungeon_reward_request_urine_reward(self, char: Character, messages: List[str], reward_power: int) -> List[str]:
        char.juel[5] = char.juel.get(5, 0) + reward_power
        messages.append(f"{char.name} 得到了饮尿奖赏。")
        return messages






    def _apply_dungeon_reward_request_virgin_hunt_reward(self, char: Character, messages: List[str], reward_power: int) -> List[str]:
        lust_key = 2 if int(char.abl.get(3, 0)) > int(char.abl.get(2, 0)) else 1
        exp_key = 1 if lust_key == 2 else 0
        char.juel[lust_key] = char.juel.get(lust_key, 0) + reward_power
        char.juel[5] = char.juel.get(5, 0) + reward_power
        char.exp[exp_key] = char.exp.get(exp_key, 0) + 10
        char.exp[5] = char.exp.get(5, 0) + 10
        char.exp[2] = char.exp.get(2, 0) + 5
        messages.append(f"{char.name} 得到了狩猎处男式的奖赏。")
        return messages






    def _apply_dungeon_room_500_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        shop_result = self._apply_dungeon_room_500_shop_branch(leader, room_name, extra)
        if shop_result is not None:
            return shop_result

        cost = (self._get_character_level(leader) * 5) + 10
        if extra & 1:
            cost += 10
        if extra & 2:
            cost += 10
        if int(leader.cflag.get(580, 0)) < cost:
            return f"{leader.name} 在{room_name}里逛了一圈，但手头资金不够。"
        self._add_dungeon_party_funds(leader, -cost)
        self._add_global_money(cost)
        leader.base[0] = min(int(leader.maxbase.get(0, leader.base.get(0, 0))), int(leader.base.get(0, 0)) + 20)
        leader.base[1] = min(int(leader.maxbase.get(1, leader.base.get(1, 0))), int(leader.base.get(1, 0)) + 50)
        return f"{leader.name} 在{room_name}大吃大喝了一番，队伍资金 -{cost}，魔王军现金收入 +{cost}。"






    def _apply_dungeon_room_500_item_shop(self, leader: Character, room_name: str) -> Optional[str]:
        cost = (self._get_character_level(leader) * 6) + 20
        if int(leader.cflag.get(580, 0)) < cost:
            return f"{leader.name} 在{room_name}的道具店前看了很久，但钱不够。"
        if not self._grant_dungeon_room_shop_item(leader, range(560, 565), 400):
            return f"{leader.name} 在{room_name}的道具店没能再装下新道具。"
        self._add_dungeon_party_funds(leader, -cost)
        self._add_global_money(cost)
        return f"{leader.name} 在{room_name}的道具店买下了补给，队伍资金 -{cost}，魔王军现金收入 +{cost}。"






    def _apply_dungeon_room_500_shop_branch(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        if extra & 1 and random.randint(0, 2) == 0:
            return self._apply_dungeon_room_500_weapon_shop(leader, room_name)
        if extra & 2 and random.randint(0, 1) == 0:
            return self._apply_dungeon_room_500_item_shop(leader, room_name)
        return None






    def _apply_dungeon_room_500_weapon_shop(self, leader: Character, room_name: str) -> Optional[str]:
        cost = (self._get_character_level(leader) * 8) + 20
        if int(leader.cflag.get(580, 0)) < cost:
            return f"{leader.name} 在{room_name}的武器店前徘徊了一阵，但手头资金不够。"
        current_code = int(leader.cflag.get(550, 0))
        _, current_enhance, _ = self._decode_equipment_code(current_code)
        floor_strength = max(0, int(leader.cflag.get(501, 0)))
        if floor_strength <= current_enhance:
            return f"{leader.name} 看了看{room_name}武器店的陈列，觉得现有武器已经够用了。"
        new_base = 340 + random.randint(0, 10)
        if new_base == 349:
            new_base = 340
        new_base_code = new_base - 300
        if not self._is_weapon_usable_by_character(leader, new_base_code):
            return f"{leader.name} 在{room_name}看了半天，还是没找到趁手的新武器。"
        leader.cflag[550] = self._encode_equipment_code(new_base_code, floor_strength, random.randint(0, 9))
        self._add_dungeon_party_funds(leader, -cost)
        self._add_global_money(cost)
        weapon_name = self._get_equipment_weapon_name(leader.cflag[550])
        return f"{leader.name} 在{room_name}换上了{weapon_name}，队伍资金 -{cost}，魔王军现金收入 +{cost}。"






    def _apply_dungeon_room_501_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        damage = self._get_dungeon_master_level() + 10
        if extra & 1:
            damage += self._get_character_level(leader)
        if extra & 2:
            damage += self.interpreter.vars.get_flag(85, 0) * 2
        self._apply_dungeon_damage(leader, hp_damage=damage)
        return f"{leader.name} 经过{room_name}，HP-{damage}。"






    def _apply_dungeon_room_502_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        if self.interpreter.vars.get_flag(83, 0) > 0 and leader.cflag.get(1, 0) != 12:
            self.interpreter.vars.set_flag(83, max(0, self.interpreter.vars.get_flag(83, 0) - 1))
            return f"{leader.name} 在{room_name}救走了一名肉便器。"
        return None






    def _apply_dungeon_room_503_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        broken_item_name: Optional[str] = None
        if extra & 1 and random.randint(0, 5) == 0:
            equipment_slot = random.randint(560, 564)
            equip_id = int(leader.cflag.get(equipment_slot, 0))
            if equip_id > 0:
                broken_item_name = self._get_item_name(equip_id)
            leader.cflag[equipment_slot] = 0
        leader.cflag[11] = max(0, leader.cflag.get(11, 0) * 9 // 10)
        mp_damage = self._get_dungeon_master_level() + 2 if extra & 2 else 0
        self._apply_dungeon_damage(leader, mp_damage=mp_damage)
        fragments = [f"{leader.name} 在{room_name}中被冻得发抖，攻击力下降。"]
        if broken_item_name is not None:
            fragments.append(f"激烈的飞雪还毁掉了{broken_item_name}。")
        if mp_damage > 0:
            fragments.append(f"MP-{mp_damage}。")
        return " ".join(fragments)






    def _apply_dungeon_room_504_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        if extra & 1 and random.randint(0, 5) == 0:
            leader.base[1] = min(leader.maxbase.get(1, leader.base.get(1, 0)), leader.base.get(1, 0) + 50)
            leader.cflag[2] = int(leader.cflag.get(2, 0)) + 20
            leader.juel[6] = int(leader.juel.get(6, 0)) + self._get_dungeon_master_level() * 4
            return f"{leader.name} 在{room_name}找到了绿洲，MP+50，好感上升。"
        leader.cflag[12] = max(0, leader.cflag.get(12, 0) * 9 // 10)
        damage = self._get_character_level(leader) + 10 if extra & 2 else 0
        self._apply_dungeon_damage(leader, hp_damage=damage)
        if damage > 0:
            return f"{leader.name} 被{room_name}的热浪炙烤，防御下降，HP-{damage}。"
        return f"{leader.name} 被{room_name}的热浪炙烤，防御下降。"






    def _apply_dungeon_room_505_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        back = 0
        if extra & 1:
            back += 5
        if extra & 2:
            back += 5
        if random.randint(0, 2) != 0:
            leader.cflag[502] = max(0, leader.cflag.get(502, 0) - back)
            leader.cflag[509] = 1
            if back > 0:
                return f"{leader.name} 在{room_name}迷路了，侵攻度-{back}。"
            return f"{leader.name} 在{room_name}迷路了。"
        return None






    def _apply_dungeon_room_506_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        if self.interpreter.vars.get_flag(84, 0) <= 0:
            return None
        mp_damage = min(max(1, leader.maxbase.get(1, 0) // 4), self.interpreter.vars.get_flag(84, 0) * 5)
        hp_damage = self.interpreter.vars.get_flag(84, 0) * 2 if extra & 1 else 0
        self._apply_dungeon_damage(leader, hp_damage=hp_damage, mp_damage=mp_damage)
        blocked_preempt = False
        if extra & 2 and random.randint(0, 3) == 0:
            blocked_preempt = not self._get_character_flag_bit(leader, 503, DUNGEON_STATE_PREEMPT_BLOCKED_BIT)
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_PREEMPT_BLOCKED_BIT, True)
        fragments = [f"{leader.name} 在{room_name}看着那些展品，发自内心地颤抖起来了，MP-{mp_damage}。"]
        if hp_damage > 0:
            fragments.append(f"巡逻魔像又造成了HP-{hp_damage}。")
        if extra & 2 and blocked_preempt:
            fragments.append("陈列架妨碍了远程攻击，暂时无法先发制人。")
        return " ".join(fragments)






    def _apply_dungeon_room_507_effect(self, leader: Character, room_name: str, extra: int) -> Optional[str]:
        menu = 0
        karma = leader.cflag.get(151, 0)
        if karma < -20 and leader.talent.get(0, 0) == 0:
            menu = 3
        if karma < 0 and leader.abl.get(22, 0) > 0:
            menu = 4
        if karma < 30 and leader.talent.get(121, 0):
            menu = 4
        if karma < 10 and leader.talent.get(122, 0):
            menu = 4
        if leader.talent.get(143, 0):
            menu = 1
        if leader.talent.get(142, 0):
            menu = 2
        if menu <= 0:
            return None
        income = (self._get_character_level(leader) * 8) + 150
        if extra & 1:
            income = int(income * 1.1)
        if extra & 2:
            income = int(income * 1.1)
        if leader.cflag.get(580, 0) >= income:
            self._add_dungeon_party_funds(leader, -income)
            self._add_global_money(income)
            self._add_character_karma(leader, -1)
            partner = {
                1: "少年奴隶",
                2: "少女奴隶",
                3: "男淫魔",
                4: "女淫魔",
            }.get(menu, "娼馆街的服务者")
            return f"{leader.name} 在{room_name}与{partner}享乐了一番，队伍资金 -{income}，魔王军现金收入 +{income}。"
        return None






    def _apply_dungeon_room_effect(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_interception_room_expansion(leader, floor))
        room_id = self._get_dungeon_floor_room(floor)
        extra = self._get_dungeon_floor_room_extra(floor)
        if room_id <= 0:
            return messages

        room_name = self._get_dungeon_room_name(room_id)
        effect_messages = {
            500: self._apply_dungeon_room_500_effect,
            501: self._apply_dungeon_room_501_effect,
            502: self._apply_dungeon_room_502_effect,
            503: self._apply_dungeon_room_503_effect,
            504: self._apply_dungeon_room_504_effect,
            505: self._apply_dungeon_room_505_effect,
            506: self._apply_dungeon_room_506_effect,
            507: self._apply_dungeon_room_507_effect,
        }
        handler = effect_messages.get(room_id)
        if handler is None:
            return messages
        message = handler(leader, room_name, extra)
        if message is not None:
            messages.append(message)
        return messages






    def _apply_dungeon_room_setup(self, item_id: int, flags: List[int]) -> None:
        for floor in range(1, 10):
            if flags[0] & (1 << (floor - 1)):
                self.interpreter.vars.set_flag(350 + floor - 1, item_id)






    def _apply_dungeon_self_hypnosis_trap_state(self, leader: Character, floor: int) -> List[str]:
        roll = self._roll_dungeon_arousal_trap_check(leader)
        if roll > 60:
            return [f"{leader.name} 猛地捏了捏脸，总算从催眠里清醒了过来。"]
        if roll < 10:
            leader.cflag[11] = 0
            leader.cflag[12] = 0
            return [f"{leader.name} 被催眠得彻底沉迷于自慰，攻击和防御暂时降为 0。"]
        leader.cflag[11] = int(leader.cflag.get(11, 0)) // 2
        leader.cflag[12] = int(leader.cflag.get(12, 0)) // 2
        return [f"{leader.name} 被催眠得难以集中，攻击和防御暂时减半。"]






    def _apply_dungeon_self_relief(self, char: Character) -> List[str]:
        if char.cflag.get(1, 0) != 3:
            return []
        chance = int(char.abl.get(11, 0)) + int(char.abl.get(31, 0)) + int(char.talent.get(60, 0)) * 10
        if random.randint(0, 35) > chance:
            return []
        mode = self._get_dungeon_self_relief_mode(char)
        play = max(1, 1 + int(char.abl.get(31, 0)) // 2 + int(char.abl.get(17, 0)) // 3)
        char.exp[10] = char.exp.get(10, 0) + play
        char.exp[80] = char.exp.get(80, 0) + play
        char.juel[0] = char.juel.get(0, 0) + play * 500
        char.juel[4] = char.juel.get(4, 0) + play * 100
        char.juel[5] = char.juel.get(5, 0) + play * 250
        mode_text = {
            "les": "想象着与女人交合",
            "animal": "陷入了和野兽交尾的幻想",
            "master": "想起了魔王与调教时的事情",
            "obsessed": "彻底沉浸在欲望之中",
            "quiet": "努力压抑着声音",
        }.get(mode, "偷偷自慰")
        return [f"{char.name} 在地下城{mode_text}，自慰了 {play} 次。"]






    def _apply_dungeon_side_work(self, worker: Character) -> List[str]:
        if worker.cflag.get(1, 0) != 3 or worker.cflag.get(500, 0) != 0:
            return []
        income = self._get_dungeon_work_income(worker)
        self._add_global_money(income)
        return [f"{worker.name} 在地下城做了些内职，获得 {income} pts。"]






    def _apply_dungeon_slime_room_trap_state(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            messages.append("坠落让她直接掉进了史莱姆巢穴。")
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_SLIPPERY_BIT, True)
        messages.append(f"{leader.name} 被史莱姆的粘液包裹，进入了黏滑状态。")
        return messages






    def _apply_dungeon_succubus_trap_state(self, leader: Character, floor: int) -> List[str]:
        roll = self._roll_dungeon_arousal_trap_check(leader)
        if roll > 60:
            return [f"{leader.name} 察觉到了异常，没有理会那个可疑的少女。"]
        if roll < 10:
            leader.cflag[11] = 0
            leader.cflag[12] = 0
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
            return [f"{leader.name} 被梦魔诱惑得彻底失神，攻击和防御暂时降为 0。"]
        leader.cflag[11] = int(leader.cflag.get(11, 0)) // 2
        leader.cflag[12] = int(leader.cflag.get(12, 0)) // 2
        self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
        return [f"{leader.name} 被梦魔诱惑得心神不宁，攻击和防御暂时减半。"]






    def _apply_dungeon_teleport_trap_state(self, leader: Character, floor: int) -> List[str]:
        roll = random.randint(0, 99)
        if roll > 70:
            return [f"{leader.name} 敏捷地躲开了传送陷阱。"]
        if roll < 20:
            leader.cflag[502] = min(int(leader.cflag.get(502, 0)), 1)
            return [f"{leader.name} 被传送回了第{floor}层的起点附近。"]
        leader.cflag[502] = random.randint(0, 99)
        return [f"{leader.name} 被传送到了第{floor}层的其他位置。"]






    def _apply_dungeon_tentacle_floor_trap_state(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_FALL_BIT):
            leader.base[1] = max(0, int(leader.base.get(1, 0)) - 20)
            messages.append("坠落让她直接摔进了触手巢穴，额外损失 20 点气力。")
        if not self._get_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT):
            self._set_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT, True)
            messages.append("触手分泌物让她进入了发情状态。")
        return messages






    def _apply_dungeon_town_borrow_funds(self, leader: Character, messages: List[str]) -> None:
        if not self._should_dungeon_town_borrow_funds(leader):
            return
        if not self._roll_dungeon_town_borrow_funds(leader):
            return
        self._add_dungeon_party_debt(leader, -1000)
        self._add_dungeon_party_funds(leader, 1000)
        messages.append(f"{leader.name} 为了周转又借来了 1000 点资金。")






    def _apply_dungeon_town_dayevent(self, party: List[Character]) -> List[str]:
        messages: List[str] = []
        for member in party:
            idx = self._find_character_index(member)
            messages.extend(self._ensure_dungeon_town_lover(idx, member))
            messages.extend(self._apply_dungeon_town_lover_visit(idx, member))
            karma = int(member.cflag.get(151, 0))
            if karma >= 100 and random.randint(0, 3) == 0:
                self._add_character_karma(member, 1)
                messages.append(f"{member.name} 在城里度过了平静的一天，心境稍微安定了。")
            elif karma <= -50 and random.randint(0, 4) == 0:
                self._add_dungeon_party_funds(member, 200)
                messages.append(f"{member.name} 利用城里的灰色关系赚到了 200 点外快。")
        return messages






    def _apply_dungeon_town_debt_adjustment(self, leader: Character) -> List[str]:
        messages: List[str] = []
        self._apply_dungeon_town_debt_repayment(leader, messages)
        self._apply_dungeon_town_borrow_funds(leader, messages)
        return messages






    def _apply_dungeon_town_debt_repayment(self, leader: Character, messages: List[str]) -> None:
        money = int(leader.cflag.get(580, 0))
        debt = int(leader.cflag.get(582, 0))
        if debt >= -500 or money <= 0:
            return
        karma = int(leader.cflag.get(151, 0))
        repay = self._get_dungeon_town_debt_repay_amount(money, debt, karma)
        if repay <= 0:
            return
        self._add_dungeon_party_debt(leader, repay)
        self._add_dungeon_party_funds(leader, -repay)
        messages.append(f"{leader.name} 回城后偿还了 {repay} 点债务。")






    def _apply_dungeon_town_goal_plan(self, leader: Character, next_goal: int, start_floor: int) -> int:
        cost = next_goal * min(500 + self._get_character_level(leader) * 4, 900)
        if next_goal > 0:
            self._add_dungeon_party_debt(leader, -cost)
        leader.cflag[520] = next_goal
        leader.cflag[501] = max(1, min(7, start_floor))
        for member in self._get_dungeon_town_party(leader)[1:]:
            member.cflag[520] = next_goal
            member.cflag[501] = max(1, min(7, start_floor))
        return cost






    def _apply_dungeon_town_lover_visit(self, idx: int, char: Character) -> List[str]:
        partner_pair = self._resolve_dungeon_town_lover_partner(idx, char)
        if partner_pair is None:
            return []
        partner_idx, partner = partner_pair
        entry = self._get_dungeon_town_lover_entry(idx)
        love_lv = int(entry.get("love_lv", 0))
        marriage_state = int(char.cflag.get(601, 0))
        messages = self._build_dungeon_town_lover_visit_messages(char, partner, love_lv, marriage_state)
        if not messages:
            return []
        if marriage_state != 902:
            self._add_character_karma(char, -1)
        entry["love_lv"] = love_lv + 1
        partner_entry = self._get_dungeon_town_lover_entry(partner_idx)
        if int(partner_entry.get("lover_flag", 0)) == 200 and int(partner_entry.get("partner_token", 0)) == self._get_character_identity_token(idx, char):
            partner_entry["love_lv"] = max(int(partner_entry.get("love_lv", 0)), int(entry.get("love_lv", 0)))
            partner_entry["look_id"] = int(char.cflag.get(6, 0))
            partner_entry["partner_token"] = self._get_character_identity_token(idx, char)
        return messages






    def _apply_dungeon_town_lover_visit_state_effects(self, char: Character, partner: Character, visit_state: str) -> List[str]:
        messages: List[str] = []
        if visit_state == "same_room":
            messages.append(f"{char.name} 在地下城里偷偷亲吻了 {partner.name}。")
            char.exp[20] = int(char.exp.get(20, 0)) + 1
            return messages
        if visit_state == "married":
            messages.append(f"{char.name} 和 {partner.name} 过着和睦而又淫荡的新婚生活。")
            char.exp[0] = int(char.exp.get(0, 0)) + 2
            char.exp[5] = int(char.exp.get(5, 0)) + 2
            char.exp[20] = int(char.exp.get(20, 0)) + 1
            return messages
        if visit_state == "deep_love":
            messages.append(f"{char.name} 一见到 {partner.name}，两人就忍不住缠绵了起来。")
            char.exp[0] = int(char.exp.get(0, 0)) + 2
            char.exp[5] = int(char.exp.get(5, 0)) + 2
            char.exp[20] = int(char.exp.get(20, 0)) + 1
            return messages
        if visit_state == "dating":
            messages.append(f"{char.name} 和 {partner.name} 开始认真地约会了。")
            char.exp[0] = int(char.exp.get(0, 0)) + 1
            return messages
        if visit_state == "small_talk":
            messages.append(f"{char.name} 又和 {partner.name} 见面了，说着些毫无营养的话。")
            return messages
        if visit_state == "warming_up":
            messages.append(f"{char.name} 和 {partner.name} 的关系正在慢慢升温。")
            return messages
        return messages






    def _apply_dungeon_town_party_event(self, party: List[Character]) -> List[str]:
        costs: Dict[int, int] = {}
        for member in party:
            funds = int(member.cflag.get(580, 0))
            if funds >= 1000:
                costs[id(member)] = max(1, funds // 5)
        if not costs:
            return []
        messages: List[str] = ["队伍在回城后办了一场小型宴会，为下次冒险预祝成功。"]
        for member in party:
            cost = costs.get(id(member), 0)
            if cost <= 0:
                continue
            self._add_dungeon_party_funds(member, -cost)
            karma = int(member.cflag.get(151, 0))
            if karma > 50 or (karma > 80 and member.talent.get(122, 0)):
                messages.append(f"{member.name} 为了备战冒险早早休息了。")
            elif member.talent.get(315, 0) == 12 or member.talent.get(202, 0) or member.talent.get(206, 0):
                self._add_character_karma(member, 1)
                messages.append(f"{member.name} 在宴会后怀着祈祷入睡，善行值略有提升。")
            elif member.abl.get(22, 0) > 1 or member.talent.get(121, 0) or member.talent.get(122, 0) or member.talent.get(143, 0):
                member.exp[74] = int(member.exp.get(74, 0)) + 1
                self._add_character_karma(member, -1)
                messages.append(f"{member.name} 在宴会后去寻欢作乐了。")
            else:
                messages.append(f"{member.name} 醉醺醺地睡着了。")
        return messages






    def _apply_dungeon_town_rest(self, leader: Character) -> List[str]:
        messages: List[str] = []
        if int(leader.cflag.get(508, 0)) <= 0:
            return messages
        leader.cflag[508] = max(0, int(leader.cflag.get(508, 0)) - 1)
        leader.base[0] = leader.maxbase.get(0, leader.base.get(0, 0))
        leader.base[1] = leader.maxbase.get(1, leader.base.get(1, 0))
        messages.append(f"{leader.name} 在旅馆里进行了修整，恢复了体力与气力。")
        return messages






    def _apply_dungeon_town_return(self, leader: Character) -> List[str]:
        messages: List[str] = [f"{leader.name} 回到了地下城外。"]
        party = self._get_dungeon_town_party(leader)
        for member in party:
            self._mark_dungeon_return_event(member, success=bool(int(member.cflag.get(505, 0)) > 0))
            self._reset_dungeon_floor_progress(member, floor=1, return_flag=0)
            if member.cflag.get(1, 0) in (2, 3, 12):
                member.cflag[1] = 0
            messages.extend(self._apply_dungeon_town_rest(member))
            messages.extend(self._settle_dungeon_town_loot(member))
            messages.extend(self._apply_dungeon_town_debt_adjustment(member))
            messages.extend(self._clear_disabled_dungeon_quest_states(member))
            messages.extend(self._clear_dungeon_town_resolved_flags(member))
        messages.extend(self._apply_dungeon_town_dayevent(party))
        messages.extend(self._apply_dungeon_town_shopping(party))
        messages.extend(self._apply_dungeon_town_party_event(party))
        messages.extend(self._plan_next_dungeon_town_goal(leader))
        messages.extend(self._assign_dungeon_town_quest(leader))
        return messages






    def _apply_dungeon_town_shopping(self, party: List[Character]) -> List[str]:
        messages: List[str] = []
        for member in party:
            if int(member.cflag.get(580, 0)) < 3000:
                continue
            empty_slots = [slot for slot in range(560, 565) if int(member.cflag.get(slot, 0)) == 0]
            if not empty_slots:
                continue
            slot = empty_slots[0]
            member.cflag[slot] = 1
            self._add_dungeon_party_funds(member, -500)
            messages.append(f"{member.name} 为下次攻略补充了一件探索装备。")
        return messages






    def _apply_dungeon_trap_setup(self, item_id: int, flags: List[int]) -> None:
        for floor in range(1, 10):
            bit = 1 << (floor - 1)
            for slot in range(3):
                if flags[slot] & bit:
                    self.interpreter.vars.set_flag(300 + slot * 10 + floor - 1, item_id if item_id != 0 else -1)






    def _apply_dungeon_trap_state_effects(self, leader: Character, trap_id: int, floor: int) -> List[str]:
        handlers = {
            60: self._apply_dungeon_pit_trap_state,
            62: self._apply_dungeon_teleport_trap_state,
            63: self._apply_dungeon_one_way_trap_state,
            64: self._apply_dungeon_love_gas_trap_state,
            65: self._apply_dungeon_tentacle_floor_trap_state,
            66: self._apply_dungeon_love_bath_trap_state,
            67: self._apply_dungeon_self_hypnosis_trap_state,
            70: self._apply_dungeon_succubus_trap_state,
            71: self._apply_dungeon_slime_room_trap_state,
            75: self._apply_dungeon_launch_trap_state,
            76: self._apply_dungeon_curse_trap_state,
            77: self._apply_dungeon_oil_trap_state,
            78: self._apply_dungeon_fire_trap_state,
            79: self._apply_dungeon_anal_worm_trap_state,
            80: self._apply_dungeon_love_bug_trap_state,
            68: self._apply_dungeon_imitator_room_trap_state,
            86: self._apply_dungeon_illusion_trap_state,
        }
        handler = handlers.get(int(trap_id))
        if handler is None:
            return []
        return handler(leader, floor)






    def _apply_dungeon_traps(self, leader: Character, floor: int) -> List[str]:
        trap_ids = self._get_active_dungeon_floor_traps(floor)
        if not trap_ids:
            return self._apply_interception_trap_restock(leader, floor)

        trap_hits = self._get_dungeon_trap_hit_count(trap_ids)
        messages: List[str] = []
        for trap_id in trap_ids[:trap_hits]:
            messages.append(self._apply_single_dungeon_trap(leader, floor, trap_id))
        messages.extend(self._apply_interception_trap_restock(leader, floor))
        return messages






    def _apply_dungeon_treasure_setup(self, item_id: int, flags: List[int]) -> None:
        for floor in range(1, 10):
            if flags[0] & (1 << (floor - 1)):
                self.interpreter.vars.set_flag(340 + floor - 1, item_id if item_id != 0 else -1)






    def _apply_selected_dungeon_punishment(self, char: Character, choice: int) -> List[str]:
        obedience_power = self._get_dungeon_punishment_power(char, 10)
        desire_power = self._get_dungeon_punishment_power(char, 11)
        messages: List[str] = []
        if choice == 0:
            messages.append(f"{char.name} 露出了放心的表情，回到了自己的房间。")
            return messages
        if choice == 1:
            return self._apply_dungeon_punishment_choice_1(char, obedience_power, desire_power, messages)
        if choice == 2:
            return self._apply_dungeon_punishment_choice_2(char, obedience_power, desire_power, messages)
        if choice == 3:
            return self._apply_dungeon_punishment_choice_3(char, obedience_power, desire_power, messages)
        if choice == 4:
            return self._apply_dungeon_punishment_choice_4(char, obedience_power, desire_power, messages)
        if choice == 5:
            return self._apply_dungeon_punishment_choice_5(char, obedience_power, desire_power, messages)
        if choice == 6:
            return self._apply_dungeon_punishment_choice_6(char, desire_power, messages)
        if choice == 7:
            return self._apply_dungeon_punishment_choice_7(char, desire_power, messages)
        if choice == 8:
            return self._apply_dungeon_punishment_choice_8(char, obedience_power, desire_power, messages)
        return messages






    def _apply_single_dungeon_quest_slave_monster_attack(self, actor: Character, messages: List[str]) -> int:
        damage_bonus = self._get_character_domination_slave_power(actor)
        if damage_bonus <= 0:
            return 0
        slave_monster_id = int(actor.cflag.get(570, 0))
        messages.append(f"{actor.name} 支配的{self._get_item_name(slave_monster_id)}抢先扑向了任务目标。")
        return damage_bonus






    def _apply_single_dungeon_trap(self, leader: Character, floor: int, trap_id: int) -> str:
        hp_damage, mp_damage, progress_loss = self._get_dungeon_trap_damage_profile(floor, trap_id)
        extra_messages = self._apply_dungeon_trap_state_effects(leader, trap_id, floor)
        self._apply_dungeon_damage(leader, hp_damage=hp_damage, mp_damage=mp_damage)
        leader.cflag[502] = max(0, leader.cflag.get(502, 0) - progress_loss)
        base_message = f"{leader.name} 触发了 {self._get_item_name(trap_id)}，HP-{hp_damage} MP-{mp_damage}，侵攻度-{progress_loss}。"
        if not extra_messages:
            return base_message
        return " ".join([base_message] + extra_messages)






    def _assign_dungeon_town_quest(self, leader: Character) -> List[str]:
        if not self._is_dungeon_quest_board_enabled():
            return []
        if int(leader.cflag.get(534, 0)) != 0:
            return []
        goal_floor = max(1, int(leader.cflag.get(520, 0)))
        leader.cflag[535] = random.randint(1, 3)
        flags = 0
        for bit in range(6):
            if random.randint(0, 2) == 0:
                flags |= (1 << bit)
        leader.cflag[536] = flags
        leader.cflag[537] = random.randint(1, 3)
        local = random.randrange(max(1, goal_floor))
        leader.cflag[538] = local * 10 + random.randint(0, 4) + 100
        leader.cflag[539] = random.randint(1, 10) if (flags & (1 << 2)) else 99
        leader.cflag[540] = random.randint(0, 4)
        leader.cflag[534] = 1
        return [f"{leader.name} 接下了新的委托：{self._build_dungeon_quest_name(leader)}。"]






    def _build_daily_dungeon_farm_narrative(self, extra: int, meat_toilet_count: int, hide_records: bool) -> List[str]:
        if hide_records:
            return []

        messages: List[str] = []
        seed_message = self._get_daily_dungeon_farm_seed_message()
        if seed_message:
            messages.extend(seed_message)
        messages.extend(self._build_daily_dungeon_farm_talk_lines(extra, meat_toilet_count))
        return messages






    def _build_daily_dungeon_farm_talk_lines(self, extra: int, meat_toilet_count: int) -> List[str]:
        lines: List[str] = []
        max_lines = min(10, max(0, int(meat_toilet_count)))
        for _ in range(max_lines):
            lines.append(self._roll_daily_dungeon_farm_talk_line(extra, meat_toilet_count))
        return lines






    def _build_dungeon_animal_relief_base_count(self, char: Character) -> int:
        play = 0
        level = int(char.abl.get(39, 0))
        if level == 0:
            play -= 2
        elif level == 1:
            play -= 1
        elif level == 3:
            play += 1
        elif level == 4:
            play += 2
        elif level == 5:
            play += 3
        elif level >= 6:
            play += 4
        if char.talent.get(124, 0) and int(char.abl.get(11, 0)) >= 3:
            play += 1
        if int(char.talent.get(317, 0)) == 12 and int(char.abl.get(11, 0)) >= 4:
            play += 1
        if int(char.abl.get(11, 0)) >= 5 and int(char.abl.get(17, 0)) >= 4:
            play += 1
        if int(char.abl.get(11, 0)) >= 4 and int(char.abl.get(17, 0)) >= 3:
            play += 1
        if char.talent.get(136, 0):
            play += 2
        return play






    def _build_dungeon_bitch_customer_base_count(self, char: Character) -> int:
        count = random.randint(0, 5)
        count = self._apply_dungeon_bitch_karma_factor(char, count)
        count = self._apply_dungeon_bitch_former_life_factor(char, count)
        count = self._apply_dungeon_bitch_ability_factor(char, count)
        count = self._apply_dungeon_bitch_talent_factor(char, count)
        count = self._apply_dungeon_bitch_species_factor(char, count)
        count = self._apply_dungeon_bitch_appearance_factor(char, count)
        if int(target.abl.get(10, 0)) + int(target.abl.get(2, 0)) + int(target.abl.get(16, 0)) >= 13:
            print(f"{target.name}在依依不舍地拉着{player.name if player is not None else '主人'}的袖子，")
            print("但那只手还是被抖开，离开了房间。")
        return 1






    def _build_dungeon_bitch_work_round_totals(self, char: Character, customer_count: int, success_score: int, failure_score: int) -> tuple[int, int, int, Dict[str, int], Dict[str, int]]:
        success_count = 0
        total_income = 0
        total_play = 0
        play_totals: Dict[str, int] = {}
        customer_kinds = {"man": 0, "girl": 0, "animal": 0}
        for _ in range(customer_count):
            round_result = self._apply_dungeon_bitch_customer_round(char, success_score, failure_score)
            if round_result is None:
                continue
            play_type, play, income = round_result
            success_count += 1
            total_play += play
            total_income += income
            play_totals[play_type] = play_totals.get(play_type, 0) + play
            customer_kinds[self._get_dungeon_bitch_customer_kind(play_type)] += 1
        return success_count, total_income, total_play, play_totals, customer_kinds






    def _build_dungeon_bitch_work_summaries(
        self,
        play_totals: Dict[str, int],
        customer_kinds: Dict[str, int],
    ) -> tuple[str, str]:
        play_summary = "、".join(
            f"{self._get_dungeon_bitch_play_label(play_type)}x{count}"
            for play_type, count in sorted(play_totals.items())
        )
        customer_summary = []
        if customer_kinds["man"] > 0:
            customer_summary.append(f"男性客{customer_kinds['man']}")
        if customer_kinds["girl"] > 0:
            customer_summary.append(f"女性客{customer_kinds['girl']}")
        if customer_kinds["animal"] > 0:
            customer_summary.append(f"魔物{customer_kinds['animal']}")
        customer_text = "、".join(customer_summary) if customer_summary else "无人"
        return play_summary, customer_text






    def _build_dungeon_quest_battle_loot_value(self, actor: Character) -> int:
        level = max(0, self._get_character_level(actor))
        loot = 100 + level * random.randint(0, max(1, int(math.sqrt(self._get_dungeon_master_level() + level + 1))))
        loot += self._get_dungeon_junk_loot_bonus(actor)
        loot *= max(1, int(actor.cflag.get(501, 1)))
        return max(1, loot)






    def _build_dungeon_quest_battle_messages(self, leader: Character) -> List[str]:
        return [f"{leader.name} 遭遇了与{self._build_dungeon_quest_name(leader)}相关的任务战。"]






    def _build_dungeon_quest_condition_detail_lines(self, char: Character) -> List[str]:
        condition_names = self._get_dungeon_quest_condition_names(char)
        if condition_names:
            return [" 任务条件: " + "/".join(condition_names)]
        return []






    def _build_dungeon_quest_detail_lines(self, char: Character) -> List[str]:
        if int(char.cflag.get(534, 0)) != 1:
            return []
        lines: List[str] = []
        lines.append(f" 委托内容: {self._get_dungeon_quest_label(char)}")
        lines.extend(self._build_dungeon_quest_reward_detail_lines(char))
        lines.extend(self._build_dungeon_quest_condition_detail_lines(char))
        lines.extend(self._build_dungeon_quest_target_detail_lines(char))
        lines.extend(self._build_dungeon_quest_time_limit_detail_lines(char))
        return lines






    def _build_dungeon_quest_failure_text(self, char: Character) -> str:
        target_name = self._get_item_name(int(char.cflag.get(538, 0))) if int(char.cflag.get(538, 0)) > 0 else "目标"
        label = self._get_dungeon_quest_label(char)
        quest_type = int(char.cflag.get(537, 0))
        if quest_type in DUNGEON_QUEST_RESULT_TEXT_TEMPLATES:
            template = DUNGEON_QUEST_RESULT_TEXT_TEMPLATES[quest_type]["failure"]
            return template.format(target_name=target_name, subject=self._strip_dungeon_quest_label_prefix(label, quest_type))
        return f"{label}的委托已经失败。"






    def _build_dungeon_quest_name(self, char: Character) -> str:
        target_id = int(char.cflag.get(538, 0))
        target_name = self._get_item_name(target_id) if target_id > 0 else "目标"
        return f"任务[{self._get_dungeon_quest_label(char)}]{'[' + target_name + ']'}"






    def _build_dungeon_quest_reward_detail_lines(self, char: Character) -> List[str]:
        reward_type = int(char.cflag.get(535, 0))
        if reward_type > 0:
            return [f" 报酬类型: {self._get_dungeon_quest_reward_name(reward_type)}"]
        return []






    def _build_dungeon_quest_success_text(self, char: Character) -> str:
        target_name = self._get_item_name(int(char.cflag.get(538, 0))) if int(char.cflag.get(538, 0)) > 0 else "目标"
        label = self._get_dungeon_quest_label(char)
        quest_type = int(char.cflag.get(537, 0))
        if quest_type in DUNGEON_QUEST_RESULT_TEXT_TEMPLATES:
            template = DUNGEON_QUEST_RESULT_TEXT_TEMPLATES[quest_type]["success"]
            return template.format(target_name=target_name, subject=self._strip_dungeon_quest_label_prefix(label, quest_type))
        return f"{label}的委托顺利完成了。"






    def _build_dungeon_quest_target_detail_lines(self, char: Character) -> List[str]:
        target_id = int(char.cflag.get(538, 0))
        if target_id > 0:
            return [f" 讨伐对象: {self._get_item_name(target_id)}"]
        return []






    def _build_dungeon_quest_time_limit_detail_lines(self, char: Character) -> List[str]:
        limit = int(char.cflag.get(539, 0))
        if 0 < limit < 99:
            return [f" 剩余时限: {limit}"]
        return []






    def _build_dungeon_reward_request_text(self, char: Character) -> str:
        request_id = int(char.cflag.get(504, 0))
        mapping = {
            0: "赐予承诺的金币",
            1: "和狗进行兽奸",
            2: "和猪进行兽奸",
            3: "和马进行兽奸",
            4: "温柔的接吻",
            5: "奖励性交",
            6: "奖励精液",
            7: "参加乱交派对",
            8: "喝下小便",
            9: "去狩猎处男",
        }
        return mapping.get(request_id, "赐予承诺的东西")






    def _build_dungeon_ring_code(self, leader: Character, item_id: int, floor: int) -> int:
        base_code = item_id - 300
        if self._is_cursed_ring_code(base_code):
            return self._resolve_dungeon_cursed_ring_reward(leader, base_code, floor)
        return self._encode_equipment_code(base_code, floor, 0)






    def _build_dungeon_setup_floor_line(self, floor: int, mode: int, selection_flags: List[int]) -> str:
        if mode == 0:
            parts = []
            for slot in range(3):
                flag_id = 300 + slot * 10 + floor - 1
                item_id = int(self.interpreter.vars.get_flag(flag_id, -1))
                selected = bool(selection_flags[slot] & (1 << (floor - 1)))
                label = self._get_item_name(item_id) if item_id > 0 and self._get_item_count(item_id) > 0 else "无"
                parts.append(f"[{floor * 10 + slot + 100 + 1}]{'*' if selected else ''}陷阱：{label}")
            return f" [{floor * 10 + 100}] 第{floor}阶层　" + " / ".join(parts)
        if mode == 1:
            room_id = int(self.interpreter.vars.get_flag(350 + floor - 1, 0))
            if room_id < 500 or room_id > 507:
                room_id = 0
                self.interpreter.vars.set_flag(350 + floor - 1, 0)
            selected = bool(selection_flags[0] & (1 << (floor - 1)))
            label = self._get_item_name(room_id) if room_id else "通路"
            return f" [{floor * 10 + 100}] 第{floor}阶层　{'*' if selected else ''}设施：{label}"
        treasure_id = int(self.interpreter.vars.get_flag(340 + floor - 1, -1))
        selected = bool(selection_flags[0] & (1 << (floor - 1)))
        label = self._get_item_name(treasure_id) if treasure_id > 0 and self._get_item_count(treasure_id) > 0 else "无"
        return f" [{floor * 10 + 100}] 第{floor}阶层　{'*' if selected else ''}宝箱：{label}"






    def _build_dungeon_town_lover_visit_messages(
        self,
        char: Character,
        partner: Character,
        love_lv: int,
        marriage_state: int,
    ) -> List[str]:
        messages: List[str] = []
        visit_state = self._get_dungeon_town_lover_visit_state(char, partner, love_lv, marriage_state)
        if visit_state == "same_room_mismatch":
            return []
        return self._apply_dungeon_town_lover_visit_state_effects(char, partner, visit_state)






    def _build_dungeon_town_resolved_failure_messages(self, leader: Character) -> List[str]:
        return [
            f"{leader.name} 负责的{self._build_dungeon_quest_name(leader)}已经失败。",
            self._build_dungeon_quest_failure_text(leader),
        ]






    def _build_dungeon_town_resolved_success_messages(self, leader: Character) -> List[str]:
        reward_type = int(leader.cflag.get(535, 0))
        messages = [f"{leader.name} 完成了{self._build_dungeon_quest_name(leader)}。", self._build_dungeon_quest_success_text(leader)]
        if reward_type == 1:
            reward = int(leader.cflag.get(9, 0)) * 10 + 100
            self._add_dungeon_party_funds(leader, reward)
            messages.append(f"获得报酬：{self._get_dungeon_quest_reward_name(reward_type)} +{reward}。")
        elif reward_type == 2:
            self._add_character_karma(leader, 10)
            messages.append("获得报酬：善行值提升了。")
        elif reward_type == 3:
            loot = int(max(50, self._get_dungeon_treasure_reward(int(leader.cflag.get(538, 0)) or 24)))
            self._add_global_money(loot)
            messages.append(f"获得报酬：{loot} pts。")
        return messages






    def _build_main_menu_dungeon_overview_lines(self) -> List[str]:
        lines: List[str] = []
        player = self._get_player()
        trap_level = int(self.interpreter.vars.get_flag(85, 0))
        hero_level = int(self.interpreter.vars.get_flag(60, 0)) + 1
        if player is not None:
            lines.append(f" 迷宫Lv: {int(player.cflag.get(9, 0))} (经验值: {int(player.exp.get(80, 0))})  陷阱Lv: {trap_level}  当前勇者初期Lv: {hero_level}")
        total_monsters = self._get_monster_count()
        total_slaves = max(0, len(self.interpreter.vars.chars) - 1)
        active_heroes = 0
        active_interceptions = 0
        for _, char in self._get_standard_dungeon_party_candidates():
            if char.cflag.get(1, 0) == 2:
                active_heroes += 1
            elif char.cflag.get(1, 0) == 3:
                active_interceptions += 1
        for floor in range(1, 10):
            room_name = self._get_dungeon_room_name(self._get_dungeon_floor_room(floor))
            invasion, interception = self._get_floor_party_counts(floor)
            floor_monsters = sum(max(0, int(self._get_monster_stock().get(monster_id, 0))) for monster_id in self._get_floor_monster_ids(floor))
            lines.append(f" 第{floor}阶层: 部下{floor_monsters}只 / 勇者{invasion}人 / 迎击{interception}人 / 设施:{room_name}")
        lines.append(
            f" 总计: 部下{total_monsters}只 / 奴隶{total_slaves}人 / 勇者{active_heroes}人 / 迎击{active_interceptions}人 / 肉便器{self.interpreter.vars.get_flag(83, 0)}个 / 展品{self.interpreter.vars.get_flag(84, 0)}个"
        )
        return lines






    def _calculate_dungeon_status_grade(self, leader: Character) -> int:
        hp_max = max(1, leader.maxbase.get(0, 1))
        mp_max = max(1, leader.maxbase.get(1, 1))
        hp_ratio = leader.base.get(0, 0) * 100 / hp_max
        mp_ratio = leader.base.get(1, 0) * 100 / mp_max
        if hp_ratio < 20 and mp_ratio < 10:
            return 4
        if hp_ratio < 20:
            return 4
        if mp_ratio < 10:
            return 4
        if hp_ratio < 35 or mp_ratio < 30:
            return 3
        if hp_ratio < 60 or mp_ratio < 50:
            return 2
        return 1






    def _can_apply_dungeon_bitch_work(self, char: Character) -> bool:
        if char.cflag.get(1, 0) != 3:
            return False
        if char.base.get(0, 0) < 300 or char.base.get(1, 0) < 100:
            return False
        if self._get_dungeon_bitch_customer_count(char) <= 0:
            return False
        return self._get_dungeon_bitch_success_score(char) > 100






    def _can_do_dungeon_bitch_play(self, char: Character, play_type: str) -> bool:
        if char.base.get(0, 0) < 500:
            return False
        if play_type == "LES":
            return int(char.abl.get(33, 0)) >= 1
        if play_type == "ANIMAL":
            return int(char.exp.get(56, 0)) >= 50 and int(char.abl.get(39, 0)) >= 1
        if play_type == "ANAL":
            return int(char.abl.get(3, 0)) >= 1 or int(char.exp.get(5, 0)) > 0
        if play_type == "SEX":
            return int(char.talent.get(122, 0)) == 0
        return True






    def _can_dungeon_party_press_deeper(self, leader: Character) -> bool:
        max_hp = max(1, int(leader.maxbase.get(0, 1)))
        max_mp = max(1, int(leader.maxbase.get(1, 1)))
        hp_rate = int(leader.base.get(0, 0)) * 100 // max_hp
        mp_rate = int(leader.base.get(1, 0)) * 100 // max_mp
        return hp_rate >= 90 and mp_rate >= 90






    def _can_finish_dungeon_quest_exploration(self, leader: Character) -> bool:
        target_floor = self._get_dungeon_quest_target_floor(leader)
        return int(leader.cflag.get(501, 1)) >= target_floor






    def _can_replace_dungeon_ring_slot(self, leader: Character, slot_id: int, floor: int) -> bool:
        current_code = int(leader.cflag.get(slot_id, -1))
        if current_code < 0:
            return True
        _, current_enhance, _ = self._decode_equipment_code(current_code)
        return current_enhance < floor






    def _can_start_dungeon_town_lover(self, idx: int, char: Character) -> bool:
        if idx <= 0:
            return False
        if not self._get_flag_bit(8, 2):
            return False
        if self._has_dungeon_town_lover(idx):
            return False
        if int(char.cflag.get(601, 0)) > 0:
            return False
        return self._can_join_bedroom_daily_service(idx, char)






    def _choose_dungeon_punishment_option(self, char: Character) -> int:
        while True:
            print()
            print(f"{char.name} 没有发现勇者，或者战败后失败而归。")
            print(f"要处罚 {char.name} 吗？")
            print(" [0] 什么也不做")
            print(" [1] 低压电椅刑")
            print(" [2] 当街自慰刑")
            print(" [3] 当街脱粪刑")
            print(" [4] 鞭刑")
            print(" [5] 小便器刑")
            print(" [6] 打扫厕所刑")
            print(" [7] 不给吃饭刑")
            print(" [8] 媚药放置刑")
            choice = self._prompt_choice()
            try:
                selected = int(choice)
            except ValueError:
                continue
            if 0 <= selected <= 8:
                return selected






    def _choose_dungeon_reward_option(self, char: Character) -> int:
        while True:
            print()
            print(f"{char.name} 打倒了勇者，凯旋而归，来到你的身边。")
            print(f"{char.name} 请求奖赏。")
            print(" [0] 这是你应份的")
            print(" [1] 授予勋章")
            print(" [2] 赐予承诺的东西")
            choice = self._prompt_choice()
            try:
                selected = int(choice)
            except ValueError:
                continue
            if selected in (0, 1, 2):
                return selected






    def _choose_next_dungeon_town_goal(
        self,
        leader: Character,
        current_goal: int,
        debt: int,
        balance: int,
        karma: int,
    ) -> tuple[int, int, str]:
        loan_limits = self._get_dungeon_town_goal_debt_limits(karma)
        return self._choose_next_dungeon_town_goal_from_limits(leader, current_goal, debt, balance, loan_limits)






    def _choose_next_dungeon_town_goal_from_limits(
        self,
        leader: Character,
        current_goal: int,
        debt: int,
        balance: int,
        limits: tuple[int, int, int],
    ) -> tuple[int, int, str]:
        if debt <= limits[0] or balance <= limits[1]:
            next_goal = min(8, max(1, current_goal + 1))
            start_floor = next_goal
            plan_text = f"{leader.name} 因为欠债较重，决定以下一次更深的探索来翻本，目标改为第{next_goal + 1}阶层。"
        elif debt <= limits[1] or balance <= limits[2]:
            next_goal = max(1, current_goal // 2)
            start_floor = 1
            plan_text = f"{leader.name} 决定先在浅层周回，把下次目标调整到第{next_goal + 1}阶层。"
        elif random.randint(0, 2) == 0:
            next_goal = min(8, max(1, current_goal + 1))
            start_floor = next_goal
            plan_text = f"{leader.name} 计划以下一次更深的攻略为目标，瞄准第{next_goal + 1}阶层。"
        else:
            next_goal = max(1, current_goal)
            start_floor = max(1, min(7, next_goal))
            plan_text = f"{leader.name} 决定谨慎地沿用现有计划，继续以第{next_goal + 1}阶层为目标。"
        return next_goal, start_floor, plan_text






    def _choose_random_dungeon_party_member(self, leader: Character) -> Character:
        party = self._get_dungeon_town_party(leader)
        if len(party) <= 1:
            return leader
        if len(party) >= 2 and random.randint(0, 2) == 0:
            return party[1]
        if len(party) >= 3 and random.randint(0, 1) == 0:
            return party[2]
        return leader






    def _cleanup_invalid_dungeon_town_lover_links(self) -> List[str]:
        messages: List[str] = []
        store = self._get_dungeon_town_lover_store()
        for idx in list(store.keys()):
            if idx <= 0 or idx >= len(self.interpreter.vars.chars):
                store.pop(idx, None)
                continue
            char = self.interpreter.vars.chars[idx]
            entry = store.get(idx)
            if not isinstance(entry, dict):
                store.pop(idx, None)
                continue
            token = int(entry.get("partner_token", 0))
            partner_idx = token // 1000
            if partner_idx <= 0 or partner_idx >= len(self.interpreter.vars.chars):
                store.pop(idx, None)
                messages.append(f"{char.name} 的恋人关系因为对象消失而结束了。")
                continue
            partner_entry = store.get(partner_idx)
            if not isinstance(partner_entry, dict):
                store.pop(idx, None)
                messages.append(f"{char.name} 的恋人关系因为对象失联而结束了。")
                continue
            if int(partner_entry.get("partner_token", 0)) != self._get_character_identity_token(idx, char):
                store.pop(idx, None)
                messages.append(f"{char.name} 的恋人关系已经自然淡去了。")
        return messages






    def _clear_disabled_dungeon_quest_states(self, leader: Character) -> List[str]:
        if self._is_dungeon_quest_board_enabled():
            return []
        if int(leader.cflag.get(534, 0)) == 0 and all(int(leader.cflag.get(flag_id, 0)) == 0 for flag_id in (535, 536, 537, 538, 539, 540)):
            return []
        leader.cflag[534] = 0
        for flag_id in (535, 536, 537, 538, 539, 540):
            leader.cflag[flag_id] = 0
        return [f"{leader.name} 身上的地下城委托记录随着委托板关闭而被清空了。"]






    def _clear_dungeon_quest_record(self, char: Character):
        char.cflag[534] = 0
        for flag_id in (535, 536, 537, 538, 539, 540):
            char.cflag[flag_id] = 0




    def _clear_dungeon_return_event(self, char: Character):
        char.cflag[590] = 0
        char.cflag[591] = 0






    def _clear_dungeon_town_lover_entry(self, idx: int):
        store = self._get_dungeon_town_lover_store()
        store.pop(int(idx), None)






    def _clear_dungeon_town_resolved_flags(self, leader: Character) -> List[str]:
        messages: List[str] = []
        quest_state = int(leader.cflag.get(534, 0))
        if quest_state <= 1:
            return messages
        if self._is_dungeon_quest_board_enabled():
            if quest_state & 2:
                messages.extend(self._build_dungeon_town_resolved_success_messages(leader))
            elif quest_state & 4:
                messages.extend(self._build_dungeon_town_resolved_failure_messages(leader))
        self._clear_dungeon_quest_record(leader)
        messages.append(f"{leader.name} 回城后整理了这次探索留下的委托记录。")
        return messages






    def _compose_dungeon_party_progress_summary(self, summary: str, event_messages: List[str]) -> str:
        if event_messages:
            summary += "\n" + "\n".join(event_messages)
        return summary






    def _confirm_and_apply_dungeon_room_setup(self, item_id: int, flags: List[int]) -> None:
        floor_count = self._selected_dungeon_floor_count(flags)
        cost = 10000 * floor_count if item_id != 0 else 0
        room_name = self._get_item_name(item_id) if item_id else "通路"
        print(f"\n在 {floor_count} 个阶层修建 {room_name}")
        print(f"合计花费 {cost}p，确认执行吗？")
        print(" [0] - 好的　　[1] - 不要")
        if self._prompt_choice() != "0":
            return
        if self.interpreter.vars.money < cost:
            print("\n* 钱不够！！ *")
            self._pause()
            return
        self._apply_dungeon_room_setup(item_id, flags)
        if cost:
            self._spend_global_money(cost)
        flags[0] = 0






    def _consume_dungeon_consumable_slot(self, char: Character, slot_id: int) -> None:
        char.cflag[slot_id] = 0






    def _decode_dungeon_consumable(self, item_code: int) -> tuple[int, int]:
        item_id = int(item_code)
        appraise = 0
        if item_id > 1000:
            item_id -= 1000
            appraise = 1
        return item_id, appraise






    def _dungeon_town_lover(self, char_idx: int) -> List[str]:
        """城镇恋人事件 - 对应 @DUNGEON_TOWN_LOVER

        根据恋人类型和LOVE_LV(CFLAG:607)生成城镇恋人事件文本，
        并计算各项经验/珠变化。

        Args:
            char_idx: 角色索引

        Returns:
            事件消息列表
        """
        messages: List[str] = []
        if char_idx <= 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"
        lover = char.cflag.get(606, 0)
        love_lv = char.cflag.get(607, 0)
        marriage = char.cflag.get(601, 0)

        if lover <= 0:
            return messages

        lover_name = self._name_lover(lover)
        if not lover_name:
            return messages

        # LOVE_EXP 经验追踪数组
        # 0=接吻, 1=吸烟, 2=药物, 3=口交, 4=V性交, 5=A性交, 6=百合, 7=兽奸, 8=被拍, 9=前戏
        love_exp = [0] * 10

        # 根据恋人类型和LOVE_LV分支生成事件文本
        if lover == 1:
            # 温柔的青年
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{lover_name}越来越熟悉对方的身体……")
                love_exp[4] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif love_lv <= 0:
                messages.append(f'\u201c偶然之下\u201d{lover_name}帮了{char_name}一把……')
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
            elif love_lv < 30:
                messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 2
                love_exp[3] += 1

        elif lover == 2:
            # 威严的彪形大汉
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
                love_exp[4] += 1
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}为了和{lover_name}生孩子而努力准备着……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 2
            elif love_lv <= 0:
                messages.append(f"某次{char_name}陷入危机之时，被{lover_name}出手相救……")
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
            elif love_lv < 30:
                messages.append(f"{char_name}去{lover_name}的家里做客、被推倒了……")
                love_exp[4] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 2
                love_exp[3] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 2
                love_exp[3] += 2

        elif lover == 3:
            # 粗野的流氓
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚，{char_name}努力配合着{lover_name}各种花样的性要求……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}为了和{lover_name}生孩子而努力准备着……")
                love_exp[4] += 2
                love_exp[3] += 2
                love_exp[1] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 3
                love_exp[3] += 2
                love_exp[5] += 1
                love_exp[1] += 2
            elif love_lv <= 0:
                messages.append(f"某一天{char_name}在街头被{lover_name}搭讪了……")
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif love_lv < 30:
                messages.append(f"{char_name}去{lover_name}的家中相会、没多久，两人抽起了事后烟……")
                love_exp[4] += 2
                love_exp[3] += 1
                love_exp[1] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 2
                love_exp[3] += 2
                love_exp[1] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[5] += 1
                love_exp[3] += 2
                love_exp[1] += 2

        elif lover == 4:
            # 大腹便便的中年人
            if love_lv <= 0:
                messages.append(f"某天在酒吧里，{lover_name}请{char_name}喝酒并搭讪了……")
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif love_lv < 30:
                messages.append(f"{char_name}开始进出{lover_name}的家、并收到了昂贵的首饰作为礼物……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 2
                love_exp[3] += 2
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[5] += 1
                love_exp[3] += 2

        elif lover == 21:
            # 丑陋的兽人
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{lover_name}越来越熟悉对方的身体……")
                love_exp[4] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif love_lv <= 0:
                messages.append(f'\u201c偶然之下\u201d{lover_name}帮了{char_name}一把……')
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
            elif love_lv < 30:
                messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[3] += 1

        elif lover == 22:
            # 精灵美男子
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
                love_exp[4] += 1
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}为了和{lover_name}生孩子而努力准备着……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 2
            elif love_lv <= 0:
                messages.append(f'\u201c偶然之下\u201d{lover_name}帮了{char_name}一把……')
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
            elif love_lv < 30:
                messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
                love_exp[4] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 2
                love_exp[3] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[3] += 1

        elif lover == 23:
            # 暗黑精灵
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚，{char_name}努力配合着{lover_name}各种花样的性要求……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}为了和{lover_name}生孩子而努力准备着……")
                love_exp[4] += 2
                love_exp[3] += 2
                love_exp[1] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 3
                love_exp[3] += 2
                love_exp[5] += 1
                love_exp[1] += 2
            elif love_lv <= 0:
                messages.append(f"某一天{char_name}在街头被{lover_name}搭讪了……")
            elif love_lv < 10:
                messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}开始约会了……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif love_lv < 30:
                messages.append(f"{char_name}去{lover_name}的家中相会、没多久，两人抽起了事后烟……")
                love_exp[4] += 2
                love_exp[3] += 1
                love_exp[1] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 2
                love_exp[3] += 2
                love_exp[1] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[5] += 1
                love_exp[3] += 2
                love_exp[1] += 2
                love_exp[2] += 1

        elif lover == 24:
            # 奴隶
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{lover_name}越来越熟悉对方的身体……")
                love_exp[4] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 1
            elif love_lv <= 0:
                messages.append(f"某天，路过的{char_name}被{lover_name}工作的身影吸引了……")
            elif love_lv < 10:
                messages.append(f"{char_name}找上了奴隶主，表示想和{lover_name}说说话……")
            elif love_lv < 20:
                messages.append(f"{char_name}从奴隶主手中买下了{lover_name}，并开始和{lover_name}约会了……")
            elif love_lv < 30:
                messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 3
                love_exp[3] += 1

        elif lover in (41, 42, 43, 44):
            # 女性/扶她类型 (41=妓女, 42=女学生, 43=贵妇, 44=女骑士)
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{lover_name}越来越熟悉对方的身体……")
                love_exp[6] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[6] += 3 if lover in (41, 43, 44) else 2
            elif love_lv <= 0:
                if lover == 41:
                    messages.append(f'某天，{char_name}帮了\u201c身处困难\u201d的{lover_name}一把……')
                elif lover == 42:
                    messages.append(f'某天，{char_name}帮了\u201c身处困难\u201d的{lover_name}一把……')
                elif lover == 43:
                    messages.append(f"某一天，{char_name}被{lover_name}打招呼了……")
                else:  # 44
                    messages.append(f"某一天，{char_name}被{lover_name}打招呼了……")
            elif love_lv < 10:
                if lover in (43, 44):
                    messages.append(f"{char_name}和{lover_name}再次见面、说起了工作的事……")
                else:
                    messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                messages.append(f"{char_name}和{lover_name}约好、一起吃饭……")
            elif love_lv < 30:
                if lover == 43:
                    messages.append(f"{char_name}和{lover_name}去开房了……")
                else:
                    messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
                love_exp[6] += 1
            elif love_lv < 40:
                messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[6] += 2 if lover in (41, 43) else 1
            else:
                messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始亲热……")
                love_exp[6] += 3 if lover in (41, 43, 44) else 2

        elif lover in (61, 62, 63, 64):
            # 少年类型
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{lover_name}相处时，依旧有些笨拙……")
                love_exp[3] += 1
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{lover_name}越来越熟悉对方的身体……")
                love_exp[4] += 1
                love_exp[3] += 1
            elif marriage == 902:
                messages.append(f"{char_name}和{lover_name}过着和睦而又淫荡的新婚生活……")
                love_exp[4] += 2
                love_exp[3] += 2
            elif love_lv <= 0:
                if lover in (62, 64):
                    messages.append(f"{char_name}接受了家庭教师的委托，开始辅导{lover_name}的功课……")
                else:
                    messages.append(f'某天，{char_name}帮了\u201c身处困难\u201d的{lover_name}一把……')
            elif love_lv < 10:
                if lover in (62, 64):
                    messages.append(f"{lover_name}对{char_name}的辅导不是很上心、总是说一些其他的事……")
                else:
                    messages.append(f"{char_name}和{lover_name}再次相遇，说着毫无营养的话……")
            elif love_lv < 20:
                if lover in (62, 64):
                    messages.append(f"{lover_name}对{char_name}的辅导不是很上心、总爱说些私人话题……")
                else:
                    messages.append(f"{char_name}和{lover_name}一起出去玩、直到黄昏才回来……")
            elif love_lv < 30:
                if lover in (62, 64):
                    messages.append(f"{lover_name}根本不在意{char_name}教了什么、总是说一些让人心跳加速的情话……")
                else:
                    messages.append(f"{char_name}已经可以自由进出{lover_name}的家，还会为对方准备料理……")
                love_exp[3] += 1
            elif love_lv < 40:
                if lover in (62, 64):
                    messages.append(f"{char_name}和{lover_name}开始约会了……")
                else:
                    messages.append(f"{char_name}已经住进了{lover_name}的家……")
                love_exp[4] += 1
                love_exp[3] += 1
            else:
                if lover in (62, 64):
                    messages.append(f"{char_name}总是在辅导中被打断，然后和{lover_name}开始做其他的事情……")
                else:
                    messages.append(f"{char_name}一进家门，就被{lover_name}抱住开始激烈的性交……")
                love_exp[4] += 2
                love_exp[3] += 2 if lover != 64 else 3

        elif lover in (81, 82, 83, 84):
            # 犬/家畜类型
            animal_label = lover_name
            if marriage == 902 and love_lv < 10:
                messages.append(f"新婚的{char_name}和{animal_label}相处时，还是有些笨拙……")
            elif marriage == 902 and love_lv < 30:
                messages.append(f"新婚的{char_name}和{animal_label}终于开始交尾……")
                love_exp[3] += 1
                love_exp[7] += 1
            elif marriage == 902:
                mother_label = "母狗" if lover == 81 else ("母马" if lover == 82 else ("母猪" if lover == 83 else "母牛"))
                messages.append(f"{char_name}像{mother_label}一样被{animal_label}骑在身下没日没夜的猛艹……")
                love_exp[3] += 2
                love_exp[4] += 2
                love_exp[7] += 2
            elif love_lv <= 0:
                if lover == 81:
                    messages.append(f"有一天、{char_name}从宠物商店把光鲜亮丽的{animal_label}买回家了……")
                elif lover == 82:
                    messages.append(f"某一天，{char_name}将坐骑{animal_label}买回来了……")
                elif lover == 83:
                    messages.append(f"有一天、{char_name}在宠物商店看上了{animal_label}，并买回家了……")
                else:  # 84
                    messages.append(f"某一天，{char_name}发现身边似乎具有不可思议魅力的{animal_label}了……")
            elif love_lv < 10:
                if lover == 84:
                    messages.append(f"{char_name}为了接近照顾{animal_label}，特意去农家帮忙……")
                else:
                    messages.append(f"{char_name}带着{animal_label}举止过分亲昵的到处游玩、引来无数非议……")
            elif love_lv < 20:
                messages.append(f"{char_name}终于明白了自己对{animal_label}的心意……")
            elif love_lv < 30:
                messages.append(f"{char_name}开始故意挑逗{animal_label}……")
            elif love_lv < 40:
                messages.append(f"{char_name}成功的让{animal_label}性奋起来了……")
                love_exp[3] += 1
                love_exp[7] += 1
            else:
                messages.append(f"{char_name}开始被{animal_label}艹上瘾了……")
                love_exp[3] += 2
                love_exp[4] += 2
                love_exp[7] += 3 if lover in (83, 84) else 2

        elif lover == 200:
            # 角色间恋爱 - 简化实现
            love_id = char.cflag.get(610, -1)
            if love_id < 0 or love_id >= len(self.interpreter.vars.chars):
                return messages
            love_char = self.interpreter.vars.chars[love_id]
            love_char_name = love_char.name or "角色"
            lover_name = love_char_name

            char_state = char.cflag.get(1, 0)
            love_state = love_char.cflag.get(1, 0)
            char_fallen = char.cflag.get(0, 0) > 0
            love_fallen = love_char.cflag.get(0, 0) > 0

            if char_state == 2 and love_state == 2:
                messages.append(f"{char_name}吻了{lover_name}……")
                love_exp[0] += 1
            elif char_state == 0 and love_state == 0:
                if char_fallen and love_fallen:
                    messages.append(f"{char_name}和{lover_name}不顾场合地开始做爱……")
                elif char_fallen and not love_fallen:
                    messages.append(f"{char_name}向{lover_name}洗脑了魔族的美好……")
                elif not char_fallen and love_fallen:
                    messages.append(f"{char_name}从{lover_name}了解到了魔族的美好……")
                else:
                    messages.append(f"{char_name}和{lover_name}互相鼓励着不屈不挠的内心……")
            elif char_state == 7 and love_state == 7:
                if char_fallen and love_fallen:
                    messages.append(f"{char_name}和{lover_name}互相赞美着怀有身孕的肚子……")
                elif char_fallen and not love_fallen:
                    messages.append(f"{char_name}向{lover_name}讲述着孕育着魔族的美妙之处……")
                elif not char_fallen and love_fallen:
                    messages.append(f"{char_name}见到了孕育着魔族的{lover_name}后，内心崩溃了……")
                else:
                    messages.append(f"{char_name}与{lover_name}下了绝不因成为魔族的生育工具而屈服的决心……")
            elif char_state == 0 and love_state == 2:
                if char_fallen and not love_fallen:
                    messages.append(f"{char_name}期待着{lover_name}成为魔族的那一天……")
                else:
                    messages.append(f"{char_name}相信着{lover_name}一定会来救援……")
                return messages
            elif char_state == 2 and love_state == 0:
                if not char_fallen and love_fallen:
                    messages.append(f"{char_name}听说了{lover_name}堕为魔族的事，备受罪恶感的折磨……")
                else:
                    messages.append(f"{char_name}发誓一定要救{lover_name}出来……")
                return messages
            else:
                return messages

        # ---- 经验/珠结算 ----

        # 贞操带/处女封印检查：V性交→A性交
        if love_exp[4] > 0:
            has_chastity = (char.cflag.get(42, 0) == 79
                           and (char.cflag.get(40, 0) & 64)
                           and self.interpreter.vars.flag.get(37, 0))
            has_seal = char.talent.get(273, 0) == 1
            if has_chastity or has_seal:
                love_exp[5] += love_exp[4]
                love_exp[4] = 0

        # 接吻加成
        if love_lv >= 10:
            love_exp[0] += 1
        if love_lv >= 20:
            love_exp[0] += 1
        if love_lv >= 30:
            love_exp[0] += 2
        if love_lv >= 40:
            love_exp[0] += 3
        if love_lv >= 60:
            love_exp[0] += 5

        # 口交加成
        if love_exp[3] > 0:
            love_exp[3] += char.abl.get(12, 0)  # 技巧
            love_exp[3] += char.abl.get(13, 0)  # 侍奉技术
            love_exp[3] += char.abl.get(16, 0)  # 侍奉精神
            love_exp[3] += char.abl.get(32, 0)  # 精液中毒
            if char.talent.get(52, 0):
                love_exp[3] += 1  # 舌使い
            if char.talent.get(61, 0):
                love_exp[3] += 1  # 汚臭鈍感
            if char.talent.get(62, 0):
                love_exp[3] -= 1  # 汚臭敏感
            if char.talent.get(62, 0) and char.abl.get(32, 0) > 0:
                love_exp[3] += char.abl.get(32, 0) * 3

        # V性交加成
        if love_exp[4] > 0:
            love_exp[4] += char.abl.get(2, 0)  # V感覚
            if char.talent.get(103, 0):
                love_exp[4] -= 1  # V鈍感
            if char.talent.get(104, 0):
                love_exp[4] += 1  # V敏感
            if char.talent.get(75, 0):
                love_exp[4] += 1  # セックス狂
            if char.talent.get(232, 0):
                love_exp[4] += 1  # 淫壺

        # A性交加成
        if love_exp[5] > 0:
            love_exp[5] += char.abl.get(3, 0)  # A感覚
            if char.talent.get(105, 0):
                love_exp[5] -= 1  # A鈍感
            if char.talent.get(106, 0):
                love_exp[5] += 1  # A敏感
            if char.talent.get(77, 0):
                love_exp[5] += 1  # 尻穴狂
            if char.talent.get(233, 0):
                love_exp[5] += 1  # 淫肛

        # 百合加成
        if love_exp[6] > 0 and not char.talent.get(122, 0):
            love_exp[6] += char.abl.get(22, 0)  # レズっ気
            love_exp[6] += char.abl.get(33, 0)  # レズ中毒
            if char.talent.get(81, 0):
                love_exp[6] += 1  # 両刀
            if char.talent.get(82, 0):
                love_exp[6] += 1  # 男嫌い

        # 兽奸加成
        if love_exp[7] > 0:
            if char.talent.get(314, 0) == 2:  # 種族人狼
                love_exp[7] += 1
            if char.talent.get(317, 0) == 12:  # かわいい動物が好き
                love_exp[7] += 1
            love_exp[7] += char.abl.get(39, 0)  # 兽奸中毒
            if char.talent.get(136, 0):
                love_exp[7] += 3  # 牝犬
            if love_exp[4] > 0:
                love_exp[4] += love_exp[7]
            if love_exp[3] > 0:
                love_exp[3] += love_exp[7]

        # 被拍加成
        if char.talent.get(10, 0):
            love_exp[8] -= 1  # 臆病
        if char.talent.get(20, 0):
            love_exp[8] -= 1  # 自制心
        if char.talent.get(23, 0):
            love_exp[8] += 1  # 好奇心
        if char.talent.get(27, 0):
            love_exp[8] -= 1  # 一線越えない
        if char.talent.get(28, 0):
            love_exp[8] += 2  # 目立ちたがり
        if char.talent.get(89, 0):
            love_exp[8] += 3  # 露出狂
        love_exp[8] += char.abl.get(17, 0)  # 露出癖

        # 前戏加成
        love_exp[9] += love_exp[5] + love_exp[4] + love_exp[6]
        if love_exp[9] > 0:
            love_exp[9] += char.abl.get(0, 0)  # C感覚
            love_exp[9] += char.abl.get(1, 0)  # B感覚
            if char.talent.get(101, 0):
                love_exp[9] -= 1  # C鈍感
            if char.talent.get(102, 0):
                love_exp[9] += 1  # C敏感
            if char.talent.get(107, 0):
                love_exp[9] -= 1  # B鈍感
            if char.talent.get(108, 0):
                love_exp[9] += 1  # B敏感
            if char.talent.get(74, 0):
                love_exp[9] += 1  # 自慰狂
            if char.talent.get(78, 0):
                love_exp[9] += 1  # 乳狂
            if char.talent.get(230, 0):
                love_exp[9] += 1  # 淫核
            if char.talent.get(231, 0):
                love_exp[9] += 1  # 淫乳

        # 追加文
        if love_exp[0] > 0 and char.cflag.get(16, 0) == 0:
            messages.append("★初吻★")
            char.cflag[16] = 1
            char.cstr[4] = lover_name
        elif love_exp[3] > 0 and char.cflag.get(16, 0) == 0:
            messages.append("★初吻★")
            char.cflag[16] = 101
            char.cstr[4] = lover_name

        if char.talent.get(0, 0) == 1 and love_exp[4] > 0:
            messages.append("★处女丧失★")
            char.talent[0] = 0
            char.cflag[15] = 100
            char.cstr[3] = lover_name

        if love_exp[8] > 0:
            messages.append(f"{char_name}特意将水晶球保留了下来、向认识的人炫耀……")

        # 清算文本
        summary_parts: List[str] = []
        if love_exp[0] > 0:
            summary_parts.append(f"接吻：{love_exp[0]}次")
        if love_exp[1] > 0:
            summary_parts.append(f"吸烟：{love_exp[1]}根")
        if love_exp[2] > 0:
            summary_parts.append(f"药物经验＋{love_exp[2]}")
            char.exp[57] = char.exp.get(57, 0) + love_exp[2]
        if love_exp[3] > 0:
            summary_parts.append(f"口交经验＋{love_exp[3]}")
            char.exp[22] = char.exp.get(22, 0) + love_exp[3]
        if love_exp[9] > 0:
            summary_parts.append(f"阴核点数＋{love_exp[9] * 5}")
            char.juel[0] = char.juel.get(0, 0) + love_exp[9] * 5
            summary_parts.append(f"乳房点数＋{love_exp[9] * 5}")
            char.juel[14] = char.juel.get(14, 0) + love_exp[9] * 5
        if love_exp[4] > 0:
            summary_parts.append(f"私处经验＋{love_exp[4]}")
            char.exp[0] = char.exp.get(0, 0) + love_exp[4]
            summary_parts.append(f"私处点数＋{love_exp[4] * 5}")
            char.juel[1] = char.juel.get(1, 0) + love_exp[4] * 5
        if love_exp[5] > 0:
            summary_parts.append(f"肛门经验＋{love_exp[5]}")
            char.exp[1] = char.exp.get(1, 0) + love_exp[5]
            summary_parts.append(f"肛门点数＋{love_exp[5] * 5}")
            char.juel[2] = char.juel.get(2, 0) + love_exp[5] * 5
        if (love_exp[5] + love_exp[4]) > 0:
            total_sex = love_exp[5] + love_exp[4]
            summary_parts.append(f"性交经验＋{total_sex}")
            char.exp[5] = char.exp.get(5, 0) + total_sex
        semen_exp = (love_exp[5] + love_exp[4] + love_exp[3]) // 2
        if semen_exp > 0:
            summary_parts.append(f"精液经验＋{semen_exp}")
            char.exp[20] = char.exp.get(20, 0) + semen_exp
        if love_exp[7] > 0:
            summary_parts.append(f"兽奸经验＋{love_exp[7]}")
            char.exp[56] = char.exp.get(56, 0) + love_exp[7]
        if love_exp[8] > 0:
            summary_parts.append(f"拍摄经验＋{love_exp[8]}")
            char.exp[70] = char.exp.get(70, 0) + love_exp[8]

        if summary_parts:
            messages.append(" ".join(summary_parts))

        # 膣内射精处理
        if love_exp[4] // 2 > 0:
            if 1 <= lover <= 20:
                char.cflag[105] = love_exp[4]
            elif 21 <= lover <= 40:
                char.cflag[107] = love_exp[4]
            elif 41 <= lover <= 60:
                char.cflag[105] = love_exp[4]
            elif 61 <= lover <= 80:
                char.cflag[105] = love_exp[4]
            elif lover == 81:
                char.cflag[106] = love_exp[4]
            elif 82 <= lover <= 100:
                char.cflag[107] = love_exp[4]

        # 善恶值变化
        if marriage != 902:
            messages.append("(善恶值减少:-1)")
            self._add_character_karma(char, -1)

        # LOVE_LV递增
        char.cflag[607] = char.cflag.get(607, 0) + 1

        return messages

    # ========================================
    # MARRIAGE_DAY - 婚姻日系统
    # 对应 ERB/MARRIAGE_DAY.ERB
    # ========================================




    def _ensure_dungeon_town_lover(self, idx: int, char: Character) -> List[str]:
        if not self._can_start_dungeon_town_lover(idx, char):
            return []
        target_pair = self._find_dungeon_town_lover_target(idx, char)
        if target_pair is None:
            return []
        other_idx, other = target_pair
        char_entry = self._get_dungeon_town_lover_entry(idx)
        other_entry = self._get_dungeon_town_lover_entry(other_idx)
        char_entry["lover_flag"] = 200
        other_entry["lover_flag"] = 200
        char_entry["love_lv"] = 0
        other_entry["love_lv"] = 0
        char_entry["look_id"] = int(other.cflag.get(6, 0))
        other_entry["look_id"] = int(char.cflag.get(6, 0))
        char_entry["partner_token"] = self._get_character_identity_token(other_idx, other)
        other_entry["partner_token"] = self._get_character_identity_token(idx, char)
        return [f"{char.name} 被 {other.name} 吸引了，两人开始交往了。"]






    def _finalize_dungeon_bitch_work(self, char: Character, total_income: int, total_play: int, play_totals: Dict[str, int], customer_kinds: Dict[str, int]) -> List[str]:
        messages: List[str] = []
        public_share, tribute = self._route_dungeon_bitch_income(char, total_income)
        char.exp[80] = char.exp.get(80, 0) + max(1, total_play // 2)
        self._add_character_karma(char, -max(1, total_play))
        play_summary, customer_text = self._build_dungeon_bitch_work_summaries(play_totals, customer_kinds)
        messages.append(f"{char.name} 在地下城接待了 {customer_text}，公款 +{public_share}。")
        if tribute > 0:
            messages.append(f"{char.name} 将卖春收入的一半上交后，队伍资金 +{tribute}。")
        messages.append(f"{char.name} 本轮进行了 {play_summary}。")
        messages.append(f"{char.name} 的卖淫经验 +{total_play}。")
        return messages






    def _find_dungeon_town_lover_target(self, idx: int, char: Character) -> Optional[tuple[int, Character]]:
        current_state = int(char.cflag.get(1, 0))
        candidates: List[tuple[int, Character]] = []
        for other_idx, other in enumerate(self.interpreter.vars.chars):
            if other is char:
                continue
            if self._has_dungeon_town_lover(other_idx) or int(other.cflag.get(601, 0)) > 0:
                continue
            if int(other.cflag.get(1, 0)) != current_state:
                continue
            if current_state == 2 and int(char.cflag.get(533, 0)) != int(other.cflag.get(533, 0)):
                continue
            if char.talent.get(122, 0) and other.talent.get(122, 0):
                if int(char.abl.get(23, 0)) == 0 and int(other.abl.get(23, 0)) == 0:
                    continue
            elif not char.talent.get(122, 0) and not other.talent.get(122, 0):
                if int(char.abl.get(22, 0)) == 0 and int(other.abl.get(22, 0)) == 0:
                    continue
            candidates.append((other_idx, other))
        if not candidates:
            return None
        return random.choice(candidates)






    def _finish_dungeon_party_progress_summary(
        self,
        leader: Character,
        floor: int,
        walk: int,
        advanced: bool,
        pre_messages: List[str],
        tried_spy: bool,
        interception_messages: List[str],
        event_messages: List[str],
    ) -> str:
        if advanced:
            summary = f"{leader.name} 攻略完成并进入了第{floor}阶层。"
        else:
            summary = f"{leader.name} 在地下城推进了 {walk} 点，当前位于第{floor}阶层。"
        if tried_spy and interception_messages:
            event_messages = interception_messages + event_messages
        return self._compose_dungeon_party_progress_summary(summary, event_messages)






    def _get_active_dungeon_floor_traps(self, floor: int) -> List[int]:
        return [trap_id for trap_id in self._get_dungeon_floor_traps(floor) if trap_id > 0]






    def _get_available_dungeon_equip_reward_pool(self) -> List[int]:
        return [item_id for item_id in self._get_dungeon_equip_reward_pool() if self._get_item_count(item_id) > 0]






    def _get_campaign_dungeon_level(self) -> int:
        if self._get_active_campaign_id() != 1:
            return 0
        return 45




    def _get_character_dungeon_quest_tag(self, char: Character) -> str:
        if not self._is_dungeon_quest_board_enabled():
            return ""
        if int(char.cflag.get(1, 0)) != 2 or int(char.cflag.get(534, 0)) != 1:
            return ""
        return f"<任务:{self._build_dungeon_quest_name(char)}>"






    def _get_daily_dungeon_farm_seed_message(self) -> List[str]:
        seed_type = int(self.interpreter.vars.get_flag(613, 0))
        if seed_type == 1:
            return [
                "“播种的大叔们要好好努力让便器们怀孕啊。”",
                "监督的淫魔踹着俘虏中年的腰，中年将腥臭的精液大量注入了肉便器……",
            ]
        if seed_type == 2:
            return [
                "“小鸡鸡奴隶少年们，加把劲，把分配的播种任务完成就行了。”",
                "监督的淫魔温柔地催促着，俘虏少年将充满年轻气息的浓厚精液注入了肉便器……",
            ]
        if seed_type == 3:
            return [
                "“怀孕吧！怀上吧！啊哈哈哈，怀孕吧！”",
                "扶她淫魔的媚药精液不断地注入肉便器中……",
            ]
        return []






    def _get_daily_dungeon_shop_income(self, extra: int) -> int:
        player = self._get_player()
        level = int(player.cflag.get(9, 0)) if player is not None else 0
        income = level * (random.randint(0, 9) + 5)
        if extra & 1:
            income += level + 20
        if extra & 2:
            income += level + 20

        prestige = self._get_prestige_value()
        if 0 <= prestige <= 20:
            return 0
        if prestige <= 40:
            return income * 3 // 10
        if prestige <= 60:
            return income * 3 // 4
        if prestige <= 80:
            return income * 6 // 5
        return income * 2






    def _get_daily_dungeon_shop_prestige_text(self) -> str:
        prestige = self._get_prestige_value()
        if 0 <= prestige <= 20:
            return "威望值是【岌岌可危】"
        if prestige <= 40:
            return "威望值是【动荡不安】"
        if prestige <= 60:
            return "威望值是【略受质疑】"
        if prestige <= 80:
            return "威望值是【相安无事】"
        return "威望值是【广受爱戴】"






    def _get_dungeon_animal_relief_play_count(self, char: Character) -> int:
        play = self._build_dungeon_animal_relief_base_count(char)
        return self._apply_dungeon_animal_relief_bonus_count(char, play)






    def _get_dungeon_bitch_average_play_count(self, char: Character) -> int:
        base = 1
        base += int(char.abl.get(11, 0)) // 3
        base += int(char.abl.get(15, 0)) // 3
        base += int(char.abl.get(37, 0)) // 2
        if char.talent.get(76, 0):
            base += 1
        if char.talent.get(180, 0) or char.talent.get(181, 0):
            base += 1
        if char.cflag.get(500, 0) == 1:
            base += 1
        return max(1, base)






    def _get_dungeon_bitch_base_failure(self, char: Character) -> int:
        failure = 250 + int(char.cflag.get(151, 0))
        failure //= 1 + max(0, int(char.abl.get(37, 0)))
        if char.talent.get(76, 0):
            failure = failure * 7 // 10
        if char.talent.get(181, 0):
            failure //= 2
        elif char.talent.get(180, 0):
            failure = failure * 7 // 10
        return max(1, failure)






    def _get_dungeon_bitch_customer_count(self, char: Character) -> int:
        count = self._build_dungeon_bitch_customer_base_count(char)
        return self._apply_dungeon_bitch_customer_multipliers(char, count)






    def _get_dungeon_bitch_customer_kind(self, play_type: str) -> str:
        if play_type == "ANIMAL":
            return "animal"
        if play_type == "LES":
            return "girl"
        return "man"






    def _get_dungeon_bitch_pay_amount(self, char: Character, play_type: str, play_count: int) -> int:
        pay = 5 * (1 + int(char.cflag.get(501, 1)) + self._get_dungeon_bitch_pay_rate(char, play_type))
        if char.exp.get(74, 0) == 0:
            pay += 10
        if char.talent.get(0, 0):
            pay += 5
        return max(1, pay * max(1, play_count))






    def _get_dungeon_bitch_pay_rate(self, char: Character, play_type: str) -> int:
        karma_rate = max(1, (200 - max(-200, min(200, int(char.cflag.get(151, 0))))) // 10 + 5)
        type_rates = {
            "HAND": 4 + int(char.abl.get(13, 0)),
            "ORAL": 5 + int(char.abl.get(13, 0)) + int(char.abl.get(15, 0)) // 2,
            "LES": 7 + int(char.abl.get(22, 0)) + int(char.abl.get(33, 0)),
            "ANAL": 8 + int(char.abl.get(3, 0)) + int(char.abl.get(14, 0)) // 2,
            "SEX": 9 + int(char.abl.get(14, 0)) + int(char.exp.get(0, 0)) // 10,
            "ANIMAL": 6 + int(char.abl.get(39, 0)) * 2,
        }
        base = max(1, type_rates.get(play_type, 5))
        return max(1, karma_rate * base // 5)






    def _get_dungeon_bitch_play_effects_handler(self, play_type: str):
        return {
            "HAND": self._apply_dungeon_bitch_play_effects_hand,
            "ORAL": self._apply_dungeon_bitch_play_effects_oral,
            "LES": self._apply_dungeon_bitch_play_effects_les,
            "ANAL": self._apply_dungeon_bitch_play_effects_anal,
            "SEX": self._apply_dungeon_bitch_play_effects_sex,
            "ANIMAL": self._apply_dungeon_bitch_play_effects_animal,
        }.get(play_type)






    def _get_dungeon_bitch_play_label(self, play_type: str) -> str:
        return {
            "HAND": "手交",
            "ORAL": "口交",
            "LES": "百合接待",
            "ANAL": "肛交接待",
            "SEX": "性交接待",
            "ANIMAL": "兽交表演",
        }.get(play_type, play_type)






    def _get_dungeon_bitch_play_weights(self, char: Character) -> List[tuple[str, int]]:
        weights: List[tuple[str, int]] = [
            ("HAND", 25 + int(char.abl.get(13, 0)) * 8 + int(char.abl.get(15, 0)) * 4),
            ("ORAL", 22 + int(char.abl.get(13, 0)) * 6 + int(char.abl.get(15, 0)) * 5),
            ("LES", 10 + int(char.abl.get(22, 0)) * 10 + int(char.abl.get(33, 0)) * 8),
            ("ANAL", 12 + int(char.abl.get(3, 0)) * 8 + int(char.exp.get(5, 0)) // 5),
            ("SEX", 20 + int(char.abl.get(14, 0)) * 8 + int(char.exp.get(0, 0)) // 5),
            ("ANIMAL", 6 + int(char.abl.get(39, 0)) * 12),
        ]
        if char.cflag.get(500, 0) == 1:
            for idx, (play_type, weight) in enumerate(weights):
                if play_type in {"SEX", "ANAL", "LES"}:
                    weights[idx] = (play_type, weight + 10 + int(char.abl.get(10, 0)) * 2)
        return [(play_type, weight) for play_type, weight in weights if weight > 0 and self._can_do_dungeon_bitch_play(char, play_type)]






    def _get_dungeon_bitch_success_score(self, char: Character) -> int:
        score = 1500 // max(1, 25 - int(char.abl.get(11, 0)) - int(char.abl.get(37, 0)))
        if char.cflag.get(1, 0) == 3 and int(char.cflag.get(533, 0)) > 1:
            score = score * 3 // 4
        elif char.cflag.get(500, 0) == 1:
            score = score * (10 + int(char.abl.get(10, 0)) * 2) // 10
        else:
            score = score * 3 // 4
        level = int(char.cflag.get(120, 0))
        if level > 0:
            score += level * 5 - 5
        else:
            score = 1
        return max(1, score)






    def _get_dungeon_consumable_slot_ids(self) -> range:
        return range(560, 565)






    def _get_dungeon_equip_reward_pool(self) -> List[int]:
        pool = list(range(300, 321))
        return [item_id for item_id in pool if item_id in self.item_catalog]






    def _get_dungeon_floor_room(self, floor: int) -> int:
        if self._get_active_campaign_id() > 0:
            return self._get_campaign_room(floor)
        return self.interpreter.vars.get_flag(350 + floor - 1, 0)






    def _get_dungeon_floor_room_extra(self, floor: int) -> int:
        if self._get_active_campaign_id() > 0:
            return self._get_campaign_room_extra(floor)
        return self.interpreter.vars.get_flag(360 + floor - 1, 0)






    def _get_dungeon_floor_trap_flag_ids(self, floor: int) -> List[int]:
        if floor < 1 or floor > 9 or self._get_active_campaign_id() > 0:
            return []
        return [base + floor - 1 for base in (300, 310, 320)]






    def _get_dungeon_floor_traps(self, floor: int) -> List[int]:
        if self._get_active_campaign_id() > 0:
            return [
                self._get_campaign_trap_id(300 + floor),
                self._get_campaign_trap_id(310 + floor),
                self._get_campaign_trap_id(320 + floor),
            ]
        offsets = [300, 310, 320]
        return [self.interpreter.vars.get_flag(base + floor - 1, -1) for base in offsets]






    def _get_dungeon_floor_treasure(self, floor: int) -> int:
        if self._get_active_campaign_id() > 0:
            return self._get_campaign_equip_select(floor)
        return self.interpreter.vars.get_flag(340 + floor - 1, -1)






    def _get_dungeon_junk_loot_bonus(self, char: Character) -> int:
        bonus = 0
        if char.talent.get(164, 0):
            bonus += 10
        if int(char.talent.get(316, 0)) == 2:
            bonus += 20
        race_id = int(char.talent.get(317, 0))
        if race_id in (10, 11):
            bonus += 30
        if char.talent.get(203, 0):
            bonus += 30
        return bonus






    def _get_dungeon_master_level(self) -> int:
        player = self._get_player()
        if player is None:
            return 1
        return max(1, int(player.cflag.get(9, 0)))






    def _get_dungeon_party_candidates(self) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if char.base.get(0, 0) < 1:
                continue
            if char.cflag.get(1, 0) not in (2, 3, 12):
                continue
            candidates.append((idx, char))
        return candidates






    def _get_dungeon_party_walk_amount(self, leader: Character) -> int:
        walk = random.randint(10, 35)
        if leader.cflag.get(507, 0):
            walk *= -2
        if leader.cflag.get(509, 0):
            if random.randint(0, 2) == 0:
                leader.cflag[509] = 0
            else:
                walk = 0
        return walk






    def _get_dungeon_punishment_power(self, char: Character, abl_id: int) -> int:
        level = max(0, min(10, int(char.abl.get(abl_id, 0))))
        values = {
            0: 50,
            1: 100,
            2: 200,
            3: 400,
            4: 800,
            5: 1500,
            6: 3000,
            7: 6000,
            8: 12000,
            9: 25000,
            10: 50000,
        }
        return values.get(level, 50)






    def _get_dungeon_quest_battle_actor_stat_modifier(self, actor: Character) -> int:
        current_attack = int(actor.cflag.get(11, 0))
        current_defense = int(actor.cflag.get(12, 0))
        base_attack = int(actor.cflag.get(13, current_attack))
        base_defense = int(actor.cflag.get(14, current_defense))
        modifier = 0

        attack_delta = current_attack - base_attack
        defense_delta = current_defense - base_defense
        if attack_delta > 0:
            modifier += max(1, attack_delta // 10)
        elif attack_delta < 0:
            modifier -= max(1, (-attack_delta) // 10)
        if defense_delta > 0:
            modifier += max(1, defense_delta // 10)
        elif defense_delta < 0:
            modifier -= max(1, (-defense_delta) // 10)

        if current_attack <= 0:
            modifier -= 12
        if current_defense <= 0:
            modifier -= 12
        return modifier






    def _get_dungeon_quest_battle_defeat_reason(self, actor: Character) -> Optional[str]:
        current_hp = int(actor.base.get(0, 0))
        current_mp = int(actor.base.get(1, 0))
        if current_hp <= 0:
            return f"{actor.name} 最终在潮湿的地下城中用尽了最后的气力。"
        if current_hp <= 300:
            return f"{actor.name} 感觉到生命垂危，投降求饶了。"
        if current_mp <= 0:
            return f"{actor.name} 失去了战斗的意志，丢掉武器投降了。"
        return None






    def _get_dungeon_quest_battle_success_base(self, leader: Character, flags: int) -> int:
        success_base = 75
        if flags & (1 << 0):
            success_base -= 15
        if flags & (1 << 3):
            success_base -= 10
        success_base += max(0, self._get_character_level(leader) * 2)
        return success_base






    def _get_dungeon_quest_condition_names(self, char: Character) -> List[str]:
        flags = int(char.cflag.get(536, 0))
        names: List[str] = []
        for bit, label in DUNGEON_QUEST_CONDITION_LABELS.items():
            if flags & (1 << bit):
                names.append(label)
        return names






    def _get_dungeon_quest_label(self, char: Character) -> str:
        quest_type = int(char.cflag.get(537, 0))
        subject = self._get_dungeon_quest_subject_name(char)
        if quest_type == 1:
            return f"被掳走的{subject}"
        if quest_type == 2:
            return f"受魔诱惑的{subject}"
        if quest_type == 3:
            return f"因变异魔法而暴走的{subject}"
        return subject






    def _get_dungeon_quest_party(self, leader: Character) -> List[Character]:
        party: List[Character] = [leader]
        for member_idx in (531, 532):
            char_index = int(leader.cflag.get(member_idx, 0))
            if char_index <= 0 or char_index >= len(self.interpreter.vars.chars):
                continue
            member = self.interpreter.vars.chars[char_index]
            if member not in party:
                party.append(member)
        return party






    def _get_dungeon_quest_reward_name(self, reward_type: int) -> str:
        mapping = {
            1: "队伍资金",
            2: "善行值",
            3: "金钱报酬",
        }
        return mapping.get(int(reward_type), "报酬")






    def _get_dungeon_quest_subject_name(self, char: Character) -> str:
        quest_type = int(char.cflag.get(537, 0))
        variant = int(char.cflag.get(540, 0))
        default_name = {1: "村娘", 2: "人妻", 3: "魔女"}.get(quest_type, "目标")
        return DUNGEON_QUEST_SUBJECT_NAME_MAP.get(quest_type, {}).get(variant, default_name)






    def _get_dungeon_quest_target_floor(self, leader: Character) -> int:
        target_id = int(leader.cflag.get(538, 0))
        if target_id < 100:
            return 1
        return max(1, min(9, (target_id - 100) // 10 + 1))






    def _get_dungeon_room_name(self, room_id: int) -> str:
        room_names = {
            0: "通路",
            500: "商店街",
            501: "沼泽地",
            502: "牧场",
            503: "冰窟",
            504: "热窟",
            505: "魔性地带",
            506: "博物馆",
            507: "旅馆",
        }
        return room_names.get(room_id, f"设施{room_id}")






    def _get_dungeon_selection_flags(self) -> List[int]:
        flags = getattr(self, "_dungeon_selection_flags", None)
        if not isinstance(flags, list) or len(flags) != 3:
            flags = [0, 0, 0]
            self._dungeon_selection_flags = flags
        return flags






    def _get_dungeon_self_relief_mode(self, char: Character) -> str:
        if not char.talent.get(85, 0) and int(char.abl.get(22, 0)) > random.randint(0, 4):
            return "les"
        player = self._get_player()
        player_train = int(player.cflag.get(10, 0)) if player is not None else 0
        if not char.talent.get(85, 0) and int(char.abl.get(39, 0)) > random.randint(0, 4):
            return "animal"
        if random.randint(1, 40) < player_train:
            return "master"
        if random.randint(1, 5) < max(0, int(char.abl.get(31, 0))):
            return "obsessed"
        return "quiet"






    def _get_dungeon_setup_lines(self) -> List[str]:
        lines: List[str] = []
        if self._get_active_campaign_id() > 0:
            lines.append(f" 当前大型活动: {self._get_campaign_name(self._get_active_campaign_id())}")
            lines.append(f" 活动进度: {self._get_active_campaign_progress()} / {self._get_campaign_final_floor()}")
        for floor in range(1, 10):
            traps = self._get_dungeon_floor_traps(floor)
            trap_text = " / ".join(self._get_item_name(trap_id) if trap_id > 0 else "无" for trap_id in traps)
            treasure_id = self._get_dungeon_floor_treasure(floor)
            treasure_text = self._get_item_name(treasure_id) if treasure_id > 0 else "无"
            room_id = self._get_dungeon_floor_room(floor)
            room_text = self._get_dungeon_room_name(room_id)
            lines.append(f" 第{floor}阶层  陷阱:{trap_text}  设施:{room_text}  宝箱:{treasure_text}")
        return lines






    def _get_dungeon_status_grade(self, leader: Character) -> int:
        return self._calculate_dungeon_status_grade(leader)






    def _get_dungeon_status_name(self, char: Character) -> str:
        status_map = {
            2: "侵攻中",
            3: "迎击中",
            12: "迷宫探索",
        }
        if self._is_character_in_active_campaign(char):
            return "活动探索"
        return status_map.get(char.cflag.get(1, 0), "待机")






    def _get_dungeon_town_debt_repay_amount(self, money: int, debt: int, karma: int) -> int:
        divisor = self._get_dungeon_town_debt_repay_divisor(karma)
        repay = min(abs(debt), max(100, abs(debt) // divisor), money // 2)
        return repay // 100 * 100






    def _get_dungeon_town_debt_repay_divisor(self, karma: int) -> int:
        if karma > 180:
            return 2
        if karma > 130:
            return 3
        if karma > 80:
            return 4
        if karma > 30:
            return 5
        if karma > -20:
            return 6
        if karma > -70:
            return 7
        if karma > -120:
            return 8
        return 9






    def _get_dungeon_town_goal_debt_limits(self, karma: int) -> tuple[int, int, int]:
        if karma > 180:
            return -7000, -5500, -3000
        if karma > 130:
            return -8000, -6500, -4000
        if karma > 80:
            return -9000, -7500, -5000
        if karma > 30:
            return -10000, -8500, -6000
        if karma > -20:
            return -11000, -9500, -7000
        if karma > -70:
            return -12000, -10500, -8000
        if karma > -120:
            return -13000, -11500, -9000
        return -14000, -12500, -10000






    def _get_dungeon_town_lover_entry(self, idx: int) -> Dict[str, int]:
        store = self._get_dungeon_town_lover_store()
        entry = store.get(int(idx))
        if isinstance(entry, dict):
            return entry
        entry = {}
        store[int(idx)] = entry
        return entry






    def _get_dungeon_town_lover_store(self) -> Dict[int, Dict[str, int]]:
        store = self.interpreter.vars.items.get("dungeon_town_lovers")
        if isinstance(store, dict):
            return store
        store = {}
        self.interpreter.vars.items["dungeon_town_lovers"] = store
        return store






    def _get_dungeon_town_lover_visit_state(self, char: Character, partner: Character, love_lv: int, marriage_state: int) -> str:
        if int(char.cflag.get(1, 0)) == 2 and int(partner.cflag.get(1, 0)) == 2:
            if int(char.cflag.get(533, 0)) <= 0 or int(char.cflag.get(533, 0)) != int(partner.cflag.get(533, 0)):
                return "same_room_mismatch"
            return "same_room"
        if int(char.cflag.get(1, 0)) == 0 and int(partner.cflag.get(1, 0)) == 0:
            if marriage_state == 902 and love_lv >= 30:
                return "married"
            if love_lv >= 40:
                return "deep_love"
            if love_lv >= 20:
                return "dating"
            if love_lv >= 10:
                return "small_talk"
            return "warming_up"
        return "no_visit"






    def _get_dungeon_town_party(self, leader: Character) -> List[Character]:
        party: List[Character] = [leader]
        for member_flag in (531, 532):
            member_idx = int(leader.cflag.get(member_flag, 0))
            if member_idx <= 0 or member_idx >= len(self.interpreter.vars.chars):
                continue
            member = self.interpreter.vars.chars[member_idx]
            if member not in party:
                party.append(member)
        return party






    def _get_dungeon_trap_damage_profile(self, floor: int, trap_id: int) -> tuple[int, int, int]:
        hp_damage = max(5, floor * 4)
        mp_damage = max(0, floor * 2 - 1)
        progress_loss = 5
        if 70 <= trap_id < 80:
            hp_damage += 8
            progress_loss += 5
        elif 80 <= trap_id < 90:
            mp_damage += 10
            progress_loss += 8
        if trap_id % 3 == 2:
            progress_loss += 3
        return hp_damage, mp_damage, progress_loss






    def _get_dungeon_trap_hit_count(self, trap_ids: List[int]) -> int:
        if random.randint(0, 2) == 0:
            return min(2, len(trap_ids))
        return 1






    def _get_dungeon_treasure_reward(self, item_id: int) -> int:
        item_def = self._get_item_definition(item_id)
        if item_def is None:
            return 100
        cost = int(item_def.get("cost", 0))
        if cost > 0:
            return max(50, cost // 5)
        return 100






    def _get_dungeon_work_income(self, worker: Character) -> int:
        income = self._get_character_level(worker) * 20 + 100
        if int(worker.cflag.get(0, 0)) == 0:
            income //= 10
        return max(1, income)






    def _get_standard_dungeon_party_candidates(self) -> List[tuple[int, Character]]:
        return [
            (idx, char)
            for idx, char in self._get_dungeon_party_candidates()
            if int(char.cflag.get(1, 0)) in (2, 3)
        ]






    def _get_tax_dungeon_income(self) -> int:
        player = self._get_player()
        level = int(player.cflag.get(9, 0)) if player is not None else 0
        if level < 20:
            return level * 50 + 100
        if level < 40:
            return level * 40 + 300
        if level < 80:
            return level * 30 + 700
        if level < 150:
            return level * 20 + 1500
        if level < 300:
            return level * 10 + 3000
        return level * 5 + 4500






    def _grant_dungeon_room_shop_item(self, leader: Character, slots: range, item_base: int) -> bool:
        empty_slots = [slot for slot in slots if int(leader.cflag.get(slot, 0)) <= 0]
        if not empty_slots:
            return False
        slot = empty_slots[0]
        leader.cflag[slot] = item_base + random.randint(0, 13)
        return True






    def _handle_dungeon_menu_choice(self, choice: str) -> bool:
        if choice == "999":
            return True
        try:
            selected = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False

        if 900 <= selected <= 902:
            self._set_dungeon_display_mode(selected - 900)
            return False
        if selected == 100:
            self._toggle_monster_interception_block()
            return False
        if 10 <= selected <= 14:
            self._show_dungeon_personnel_group(selected)
            return False
        if self._handle_dungeon_setup_choice(selected):
            return False

        print("\nInvalid selection.")
        self._pause()
        return False






    def _handle_dungeon_room_setup_choice(self, selected: int) -> bool:
        flags = self._get_dungeon_selection_flags()
        if 100 < selected < 200:
            self._toggle_dungeon_floor_selection(selected, flags)
            return True
        if selected == 200:
            flags[0] = 0 if flags[0] == 511 else 511
            return True
        if selected == 0 or 500 <= selected < 508:
            if flags[0] == 0:
                self._show_dungeon_no_selection_message()
                return True
            self._confirm_and_apply_dungeon_room_setup(selected, flags)
            return True
        return False






    def _handle_dungeon_setup_choice(self, selected: int) -> bool:
        mode = getattr(self, "_dungeon_display_mode", 0)
        if mode == 0:
            return self._handle_dungeon_trap_setup_choice(selected)
        if mode == 1:
            return self._handle_dungeon_room_setup_choice(selected)
        return self._handle_dungeon_treasure_setup_choice(selected)






    def _handle_dungeon_trap_setup_choice(self, selected: int) -> bool:
        flags = self._get_dungeon_selection_flags()
        if 100 < selected < 204:
            self._toggle_dungeon_trap_selection(selected, flags)
            return True
        if selected == 0 or 60 <= selected < 89 and self._get_item_count(selected) > 0:
            if not any(flags):
                self._show_dungeon_no_selection_message()
                return True
            self._apply_dungeon_trap_setup(selected, flags)
            return True
        return False






    def _handle_dungeon_treasure_setup_choice(self, selected: int) -> bool:
        flags = self._get_dungeon_selection_flags()
        if 100 < selected < 200:
            self._toggle_dungeon_floor_selection(selected, flags)
            return True
        if selected == 200:
            flags[0] = 0 if flags[0] == 511 else 511
            return True
        if selected == 0 or 300 <= selected < 340 and self._get_item_count(selected) > 0:
            if flags[0] == 0:
                self._show_dungeon_no_selection_message()
                return True
            self._apply_dungeon_treasure_setup(selected, flags)
            return True
        return False






    def _has_dungeon_town_lover(self, idx: int) -> bool:
        entry = self._get_dungeon_town_lover_entry(idx)
        return int(entry.get("lover_flag", 0)) > 0






    def _is_dungeon_quest_board_enabled(self) -> bool:
        return self._get_flag_bit(8, 3)






    def _is_dungeon_quest_target_available(self, leader: Character) -> bool:
        target_id = int(leader.cflag.get(538, 0))
        if target_id <= 0:
            return False
        floor = max(1, min(9, int(leader.cflag.get(501, 1))))
        return target_id in self._get_floor_monster_ids(floor)






    def _iter_dungeon_treasure_candidates(self, leader: Character) -> List[Character]:
        return [member for member in self._get_dungeon_town_party(leader) if member.cflag.get(1, 0) == 2]






    def _mark_dungeon_return_event(self, char: Character, success: bool):
        char.cflag[590] = 1
        char.cflag[591] = 1 if success else 0






    def _plan_next_dungeon_town_goal(self, leader: Character) -> List[str]:
        if int(leader.cflag.get(1, 0)) not in (0,):
            return []
        current_goal = max(0, int(leader.cflag.get(520, 0)))
        debt = int(leader.cflag.get(582, 0))
        balance = int(leader.cflag.get(580, 0)) + debt
        karma = int(leader.cflag.get(151, 0))
        next_goal, start_floor, plan_text = self._choose_next_dungeon_town_goal(leader, current_goal, debt, balance, karma)
        cost = self._apply_dungeon_town_goal_plan(leader, next_goal, start_floor)
        return [plan_text, f"{leader.name} 为下次探索预支了 {cost} 点资金。"]






    def _process_dungeon_return_events(self) -> List[str]:
        messages: List[str] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if int(char.cflag.get(590, 0)) == 0:
                continue
            if int(char.cflag.get(591, 0)) > 0:
                messages.extend(self._apply_dungeon_reward_event(char))
            else:
                messages.extend(self._apply_dungeon_punishment_event(char))
            self._clear_dungeon_return_event(char)
        return messages






    def _prompt_dungeon_main_menu_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_dungeon_menu_choice(self) -> str:
        return self._prompt_dungeon_main_menu_choice()






    def _prompt_dungeon_menu_choice_with_render(self) -> str:
        self._render_dungeon_menu()
        return self._prompt_dungeon_menu_choice()






    def _prompt_dungeon_party_leader(self) -> Optional[Character]:
        parties = self._get_dungeon_party_candidates()
        if not parties:
            print("\n当前没有可操作的地下城队伍。")
            self._pause()
            return None
        print("\n请选择队伍：")
        for idx, char in parties:
            print(f" [{idx}] {char.name} - {self._summarize_dungeon_party(char)}")
        print(" [100] Back")
        selected = self._prompt_choice()
        if selected == "100":
            return None
        try:
            party_idx = int(selected)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        pair = next(((idx, char) for idx, char in parties if idx == party_idx), None)
        if pair is None:
            print("\nInvalid selection.")
            self._pause()
            return None
        return pair[1]






    def _refresh_dungeon_camp_state(self, leader: Character) -> None:
        for member in self._get_dungeon_town_party(leader):
            self._set_character_flag_bit(member, 503, DUNGEON_STATE_CAMP_BIT, False)
            if self._get_ring_effect_strength(member, 18) > 0:
                self._set_character_flag_bit(member, 503, DUNGEON_STATE_CAMP_BIT, True)
            if self._get_ring_effect_strength(member, 19) > 0:
                self._set_character_flag_bit(member, 503, DUNGEON_STATE_CAMP_BIT, False)






    def _render_dungeon_main_menu(self) -> None:
        mode = getattr(self, "_dungeon_display_mode", 0)
        selection_flags = getattr(self, "_dungeon_selection_flags", [0, 0, 0])
        print("\n【Dungeon Setup】")
        print("-" * 30)
        tabs = [("900", "陷阱"), ("901", "设施"), ("902", "戒指")]
        print(" ".join(f"[{code}] {'*' if idx == mode else ''}{label}" for idx, (code, label) in enumerate(tabs)))
        for floor in range(1, 10):
            print(self._build_dungeon_setup_floor_line(floor, mode, selection_flags))
        if mode == 0:
            print(" [200] 全部陷阱 [201] 陷阱A [202] 陷阱B [203] 陷阱C")
            self._render_dungeon_setup_inventory("trap")
        elif mode == 1:
            print(" [200] 全部阶层")
            self._render_dungeon_setup_inventory("room")
        else:
            print(" [200] 全部阶层")
            self._render_dungeon_setup_inventory("treasure")
        block_text = "ON" if self.interpreter.vars.get_flag(5, 0) & 16 else "OFF"
        print(" [10] 部下状态总览")
        print(" [11] 1～3层 [12] 4～6层 [13] 7～9层 [14] 近卫兵 显示部下")
        print(f" [100] 禁止怪物迎击 现在：{block_text}")
        print(" [999] Back")
        print("-" * 30)






    def _render_dungeon_menu(self) -> None:
        self._render_dungeon_main_menu()






    def _render_dungeon_setup_inventory(self, inventory_type: str) -> None:
        if inventory_type == "trap":
            entries = [(0, "解除陷阱")]
            entries.extend((item_id, self._get_item_name(item_id)) for item_id in range(60, 89) if self._get_item_count(item_id) > 0)
        elif inventory_type == "room":
            entries = [(0, "通路")]
            entries.extend((item_id, self._get_item_name(item_id)) for item_id in range(500, 508))
        else:
            entries = [(0, "取下宝物")]
            entries.extend((item_id, self._get_item_name(item_id)) for item_id in range(300, 340) if self._get_item_count(item_id) > 0)
        for start in range(0, len(entries), 3):
            print(" ".join(f"[{item_id:>3}] {name}" for item_id, name in entries[start:start + 3]))






    def _reset_dungeon_floor_progress(self, char: Character, floor: int = 1, return_flag: int = 0):
        char.cflag[501] = int(floor)
        char.cflag[502] = 0
        char.cflag[507] = int(return_flag)




    def _reset_dungeon_party_turn_state(self, leader: Character) -> None:
        for member in self._get_dungeon_town_party(leader):
            member.cflag[503] = 0






    def _resolve_dungeon_cursed_ring_reward(self, leader: Character, base_code: int, floor: int) -> int:
        failure_rate = 1 / 3 if leader.talent.get(202, 0) == 0 and leader.talent.get(207, 0) == 0 else 1 / 8
        if random.random() < failure_rate:
            return self._encode_equipment_code(base_code, floor, 0)
        clean_pool = [8, 7, 4, 5, 17, 16, 18, 3, 2, 9, 10, 1, 0]
        clean_base = clean_pool[min(len(clean_pool) - 1, int(random.random() * len(clean_pool)))]
        enhance = floor + 1 if floor < 10 else floor
        return self._encode_equipment_code(clean_base, enhance, 0)






    def _resolve_dungeon_floor_events(self, leader: Character, floor: int) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_dungeon_room_effect(leader, floor))
        messages.extend(self._apply_dungeon_traps(leader, floor))
        return messages






    def _resolve_dungeon_party_forward_action(
        self,
        leader: Character,
        floor_before: int,
        floor: int,
        walk: int,
        advanced: bool,
        pre_messages: List[str],
        tried_spy: bool,
        interception_messages: List[str],
    ) -> tuple[bool, str]:
        self._add_dungeon_party_funds(leader, random.randint(20, 120))
        intercepted, interception_messages = self._apply_interception_advance_result(leader, floor_before, advanced)
        if intercepted:
            return True, "\n".join(interception_messages)
        event_messages = self._resolve_dungeon_floor_events(leader, floor_before)
        event_messages.extend(self._resolve_dungeon_post_progress(leader))
        event_messages.extend(self._apply_campaign_monster_extra_effect(leader))
        event_messages.extend(self._resolve_campaign_completion(leader))
        if leader.cflag.get(1, 0) in (2, 3, 12):
            event_messages.extend(self._apply_dungeon_retreat_decision(leader, floor))
        return True, self._finish_dungeon_party_progress_summary(
            leader,
            floor,
            walk,
            advanced,
            pre_messages,
            tried_spy,
            interception_messages,
            event_messages,
        )






    def _resolve_dungeon_party_retreat_action(self, leader: Character, floor: int, walk: int, pre_messages: List[str]) -> tuple[bool, str]:
        if leader.cflag.get(507, 0) and floor <= 1:
            if self._is_character_in_active_campaign(leader):
                messages = self._apply_campaign_return(leader)
            else:
                messages = self._apply_dungeon_town_return(leader)
            if pre_messages:
                messages = pre_messages + messages
            return True, "\n".join(messages)
        summary = f"{leader.name} 在撤退途中后退了 {-walk} 点，当前位于第{floor}阶层。"
        if pre_messages:
            summary = "\n".join(pre_messages + [summary])
        return True, summary






    def _resolve_dungeon_post_progress(self, leader: Character) -> List[str]:
        messages: List[str] = []
        party = self._get_dungeon_town_party(leader)
        random_member = self._choose_random_dungeon_party_member(leader)
        quest_battle_messages, quest_battle_happened = self._resolve_dungeon_quest_battle(leader)
        messages.extend(quest_battle_messages)
        if not quest_battle_happened:
            messages.extend(self._apply_dungeon_post_battle_loot(leader))
            messages.extend(self._apply_dungeon_random_member_post_battle_effects(random_member))
            messages.extend(self._apply_dungeon_junk_loot(random_member))
        messages.extend(self._apply_dungeon_party_equip_rewards(leader))
        for member in party:
            messages.extend(self._apply_dungeon_auto_consumables(member, "战斗后"))
        messages.extend(self._apply_dungeon_party_night_rituals(leader))
        self._refresh_dungeon_camp_state(leader)
        messages.extend(self._apply_dungeon_rest_phase(leader))
        messages.extend(self._advance_dungeon_quest_state(leader))
        messages.extend(self._apply_interception_training_bonus(leader))
        messages.extend(self._apply_campaign_story_progress(leader))
        grade = self._get_dungeon_status_grade(leader)
        grade_text = {
            1: "元气满满",
            2: "轻伤",
            3: "重伤",
            4: "濒危",
        }.get(grade, "异常")
        messages.append(f"{leader.name} 当前状态评级: {grade_text}。")
        return messages






    def _resolve_dungeon_quest_battle(self, leader: Character) -> tuple[List[str], bool]:
        if not self._is_dungeon_quest_board_enabled():
            return [], False
        if int(leader.cflag.get(1, 0)) != 2 or int(leader.cflag.get(534, 0)) != 1:
            return [], False
        if random.randint(0, 3) > 0:
            return [], False
        if not self._is_dungeon_quest_target_available(leader):
            return [], False
        flags = int(leader.cflag.get(536, 0))
        quest_party = self._get_dungeon_quest_party(leader)
        messages = self._build_dungeon_quest_battle_messages(leader)
        self._apply_dungeon_quest_battle_prechecks(leader, flags, quest_party, messages)
        if self._resolve_dungeon_quest_battle_party_defeat(quest_party, messages):
            return messages, True
        state_bonus = self._apply_dungeon_quest_battle_party_state_bonus(quest_party, messages)
        success_bonus = self._apply_dungeon_quest_battle_slave_monster_attack(quest_party, messages)
        if self._apply_dungeon_quest_battle_sex_request(leader, flags, messages):
            self._apply_dungeon_quest_battle_party_recovery(quest_party, messages)
            return messages, True
        if self._resolve_dungeon_quest_battle_failure(
            leader,
            flags,
            quest_party,
            messages,
            success_bonus=success_bonus + state_bonus,
        ):
            self._apply_dungeon_quest_battle_party_recovery(quest_party, messages)
            return messages, True
        self._apply_dungeon_quest_battle_success_result(leader, flags, messages)
        self._apply_dungeon_quest_battle_party_recovery(quest_party, messages)
        self._apply_dungeon_quest_battle_party_loot(quest_party, messages)
        return messages, True






    def _resolve_dungeon_quest_battle_failure(
        self,
        leader: Character,
        flags: int,
        quest_party: List[Character],
        messages: List[str],
        *,
        success_bonus: int = 0,
    ) -> bool:
        success_base = self._get_dungeon_quest_battle_success_base(leader, flags)
        success_base += max(0, int(success_bonus))
        success_base = min(100, success_base)
        success_roll = random.randint(0, 100)
        if success_roll <= success_base:
            if flags & (1 << 5):
                leader.cflag[534] = int(leader.cflag.get(534, 0)) | (1 << 2)
                messages.append(f"{leader.name} 发现这场任务战背后其实是个假委托。")
            self._apply_dungeon_quest_battle_domination_capture(quest_party, leader, messages)
            return False
        failure_damage = max(8, self._get_character_level(leader) * 2)
        self._apply_dungeon_damage(leader, hp_damage=failure_damage, mp_damage=max(0, failure_damage // 2))
        messages.append(f"{leader.name} 没能在任务战中压制目标，HP-{failure_damage}。")
        if self._resolve_dungeon_quest_battle_party_defeat(quest_party, messages):
            return True
        return True






    def _resolve_dungeon_quest_battle_party_defeat(self, quest_party: List[Character], messages: List[str]) -> bool:
        for actor in quest_party:
            defeat_reason = self._get_dungeon_quest_battle_defeat_reason(actor)
            if defeat_reason is None:
                continue
            self._apply_dungeon_quest_battle_defeat_state(actor)
            messages.append(defeat_reason)
            return True
        return False






    def _resolve_dungeon_town_lover_partner(self, idx: int, char: Character) -> Optional[tuple[int, Character]]:
        entry = self._get_dungeon_town_lover_entry(idx)
        lover_flag = int(entry.get("lover_flag", 0))
        if lover_flag <= 0:
            return None
        if lover_flag == 200:
            token = int(entry.get("partner_token", 0))
            partner_idx = token // 1000
            if 0 <= partner_idx < len(self.interpreter.vars.chars):
                partner = self.interpreter.vars.chars[partner_idx]
                if partner is not char:
                    return partner_idx, partner
            return None
        return None






    def _roll_daily_dungeon_farm_talk_line(self, extra: int, meat_toilet_count: int) -> str:
        talk = random.randint(0, 5)
        if extra & 1 and random.randint(0, 5) == 0:
            talk += 10
        elif extra & 2 and random.randint(0, 4) == 0:
            talk += 20

        if meat_toilet_count > 100 and random.randint(0, 5) == 0:
            talk += 500
        elif meat_toilet_count > 80 and random.randint(0, 4) == 0:
            talk += 400
        elif meat_toilet_count > 60 and random.randint(0, 3) == 0:
            talk += 300
        elif meat_toilet_count > 40 and random.randint(0, 2) == 0:
            talk += 200
        elif meat_toilet_count > 20 and random.randint(0, 1) == 0:
            talk += 100

        talk_map = {
            0: "“嗯……嗯……”",
            1: "“已经……不想……再生了…………”",
            2: "“呜呜……啊！要泄了！！”",
            3: "“唔哦……噢噢～！哦哦哦！……”",
            4: "“唔……啊啊……… ”",
            5: "“已经怀孕了……请……饶了我吧…………”",
            10: "“奶水……要出来了…………”",
            20: "“扶她的鸡鸡…………”",
            100: "“不要……不要啊……”",
            101: "“啊啊…………”",
            102: "“肚子……在动……”",
            103: "“全是精液……好讨厌…………”",
            104: "“已经不行了…………”",
            105: "“这里是……哪里？”",
            110: "“放……放过胸部吧…………”",
            120: "“啊～鸡鸡……好舒服～！”",
            200: "“呜呜……明明……不会再反抗了……”",
            201: "“不要再插进来了！！……”",
            202: "“我……生了多少个了啊…………”",
            203: "“啊～精液……好美味～……”",
            204: "“好想回家…………”",
            205: "“现在……是何年何月了…………”",
            210: "“胸部……胸部……嘻嘻嘻嘻……哈哈哈哈哈…………”",
            220: "“啊，一直勃起着…………”",
            300: "“求求你们放过我吧……已经……不想再生……不想再生了！……”",
            301: "“里面……再狠狠地插进来…………”",
            302: "“啊～鸡鸡～……好美味啊～”",
            303: "“后面……也……来…………”",
            304: "“哈……哈…………”",
            305: "“你………新被抓来的？”",
            310: "“不行……乳头勃起来了…………”",
            320: "“精液……满满的…………”",
            400: "“又……又生了…………”",
            401: "“豆豆勃起着……收不回去了…………”",
            402: "“再来…………”",
            403: "（跪趴在地舔舐着零落的精液）",
            404: "“好大…………”",
            405: "“泄了！！又要泄了！！！！！……”",
            410: "“好舒服……再狠狠干榨我的乳汁啊！…………”",
            420: "“我是便器……我是便器…………”",
            500: "“啊哈哈……我的……孩子…………”",
            501: "“阴蒂……又肿……又痛……啊…………”",
            502: "“唔哦～！！…………”",
            503: "（央求着阴茎）",
            504: "（发疯似地扭动着腰）",
            505: "“……”",
            510: "“奶水好香……玩烂我的胸！玩坏它！哈哈哈……哈哈……”",
            520: "“哈哈……鸡鸡……鸡鸡……好棒好棒…………”",
        }
        return talk_map.get(talk, "“嗯……嗯……”")






    def _roll_dungeon_arousal_trap_check(self, leader: Character) -> int:
        roll = random.randint(0, 99)
        if self._get_character_flag_bit(leader, 503, DUNGEON_STATE_AROUSAL_BIT):
            roll = int(roll * 0.8)
        return roll






    def _roll_dungeon_bitch_play_type(self, char: Character) -> Optional[str]:
        weights = self._get_dungeon_bitch_play_weights(char)
        if not weights:
            return None
        total = sum(weight for _, weight in weights)
        roll = random.randint(1, total)
        for play_type, weight in weights:
            roll -= weight
            if roll <= 0:
                return play_type
        return weights[-1][0]






    def _roll_dungeon_town_borrow_funds(self, leader: Character) -> bool:
        return random.randint(0, max(0, 259 + int(leader.cflag.get(151, 0)))) < 50






    def _route_dungeon_bitch_income(self, char: Character, total_income: int) -> tuple[int, int]:
        if total_income <= 0:
            return 0, 0
        self._add_global_money(total_income)
        tribute = total_income // 2
        if tribute <= 0:
            return total_income, 0
        self._spend_global_money(tribute)
        self._add_dungeon_party_funds(char, tribute)
        return total_income - tribute, tribute






    def _run_dungeon_harvest_action(self, leader: Character) -> tuple[bool, str]:
        total_funds = int(leader.cflag.get(580, 0))
        funds = total_funds // 100
        if funds <= 0:
            return False, f"{leader.name} 还没有带回足够的资金。"
        self._add_global_money(funds)
        self._add_dungeon_party_funds(leader, -total_funds)
        return True, f"从 {leader.name} 的队伍处回收了 {funds} pts。"






    def _run_dungeon_party_action(self, leader: Character) -> tuple[bool, str]:
        if leader.cflag.get(1, 0) not in (2, 3, 12):
            return False, "该角色当前不在地下城活动中。"
        self._reset_dungeon_party_turn_state(leader)
        leader_idx = next((idx for idx, char in enumerate(self.interpreter.vars.chars) if char is leader), -1)
        floor_before = max(1, leader.cflag.get(501, 1))
        pre_messages = self._update_dungeon_depth_goal(leader, floor_before)
        tried_spy, intercepted, interception_messages = self._apply_interception_spy_action(leader_idx, leader, floor_before)
        if intercepted:
            return True, "\n".join(interception_messages)
        walk = self._get_dungeon_party_walk_amount(leader)
        _, floor, advanced = self._apply_dungeon_progress(leader, walk)
        floor = leader.cflag.get(501, 1)
        if walk >= 0:
            return self._resolve_dungeon_party_forward_action(
                leader,
                floor_before,
                floor,
                walk,
                advanced,
                pre_messages,
                tried_spy,
                interception_messages,
            )
        return self._resolve_dungeon_party_retreat_action(leader, floor, walk, pre_messages)






    def _run_dungeon_party_flow(self, action: str):
        leader = self._prompt_dungeon_party_leader()
        if leader is None:
            return
        self._advance_dungeon_party_flow(action, leader)






    def _run_dungeon_scout_action(self) -> tuple[bool, str]:
        stock = self._get_monster_stock()
        floor = random.randint(1, 9)
        trap_slot = random.choice([300, 310, 320])
        treasure_flag = 340 + floor - 1
        room_flag = 350 + floor - 1
        room_extra_flag = 360 + floor - 1
        available_traps = [item_id for item_id in stock if 60 <= item_id < 90 and stock[item_id] > 0]
        trap_id = random.choice(available_traps) if available_traps else -1
        treasure_candidates = self._get_available_dungeon_equip_reward_pool()
        treasure_id = random.choice(treasure_candidates) if treasure_candidates else -1
        room_id = random.choice([0, 500, 501, 502, 503, 504, 505, 506, 507])
        self.interpreter.vars.set_flag(trap_slot + floor - 1, trap_id)
        self.interpreter.vars.set_flag(treasure_flag, treasure_id)
        self.interpreter.vars.set_flag(room_flag, room_id)
        self.interpreter.vars.set_flag(room_extra_flag, random.randint(0, 3))
        return True, f"第{floor}阶层的配置被重新侦察了。"






    def _selected_dungeon_floor_count(self, flags: List[int]) -> int:
        return sum(1 for floor in range(1, 10) if flags[0] & (1 << (floor - 1)))






    def _set_character_dungeon_return_standby_state(
        self,
        char: Character,
        *,
        floor: int = 1,
        success: bool,
    ) -> None:
        char.cflag[1] = 0
        char.cflag[500] = 0
        self._reset_dungeon_floor_progress(char, floor=floor, return_flag=0)
        self._mark_dungeon_return_event(char, success=success)




    def _set_dungeon_assignment_state(
        self,
        char: Character,
        *,
        state: int,
        work_id: int,
        floor: int,
        progress: int = 0,
        fatigue: int = 0,
        return_flag: int = 0,
    ):
        char.cflag[1] = int(state)
        char.cflag[500] = int(work_id)
        char.cflag[501] = int(floor)
        char.cflag[502] = int(progress)
        char.cflag[505] = int(fatigue)
        char.cflag[507] = int(return_flag)




    def _set_dungeon_display_mode(self, mode: int) -> None:
        self._dungeon_display_mode = mode
        self._dungeon_selection_flags = [0, 0, 0]






    def _set_dungeon_floor_room_extra(self, floor: int, extra: int):
        if self._get_active_campaign_id() > 0:
            return
        if 1 <= floor <= 9:
            self.interpreter.vars.set_flag(360 + floor - 1, max(0, int(extra)))






    def _settle_dungeon_town_loot(self, leader: Character) -> List[str]:
        loot = max(0, int(leader.cflag.get(581, 0)))
        if loot <= 0:
            return []
        self._add_dungeon_party_funds(leader, loot)
        self._add_dungeon_party_loot(leader, -loot)
        return [f"{leader.name} 把这次探索的战利品换成了 {loot} 点队伍资金。"]






    def _should_dungeon_town_borrow_funds(self, leader: Character) -> bool:
        return leader.cflag.get(580, 0) < 10000 and leader.cflag.get(582, 0) > -50000






    def _should_start_dungeon_retreat(self, leader: Character, floor: int, grade: int) -> tuple[bool, int, Optional[str]]:
        party = self._get_dungeon_town_party(leader)
        critical_count = 0
        heavy_count = 0
        light_count = 0
        poor_condition_count = 0
        for member in party:
            member_grade = self._calculate_dungeon_status_grade(member)
            if member_grade >= 4:
                critical_count += 1
            elif member_grade >= 3:
                heavy_count += 1
            elif member_grade >= 2:
                light_count += 1
            if member.base.get(1, 0) * 100 < max(1, member.maxbase.get(1, 1)) * 30:
                poor_condition_count += 1

        retreat_floor = max(1, floor - 1)
        if len(party) >= 3:
            if critical_count >= 1:
                return True, max(1, floor - 2), f"有人濒危，{leader.name} 决定开始撤退。"
            if heavy_count >= 2:
                return True, max(1, floor - 2), f"大部分成员伤势过重，{leader.name} 决定开始撤退。"
            if light_count >= 3 or poor_condition_count >= 2:
                return True, retreat_floor, f"全队状态不佳，{leader.name} 决定开始撤退。"
            return False, retreat_floor, f"{leader.name} 决定继续在地下城内前进。"
        if len(party) == 2:
            if critical_count >= 1:
                return True, max(1, floor - 2), f"有人濒危，{leader.name} 决定开始撤退。"
            if heavy_count >= 1 and light_count >= 1:
                return True, max(1, floor - 2), f"队伍伤势混杂，{leader.name} 决定开始撤退。"
            if poor_condition_count >= 2:
                return True, retreat_floor, f"全队状态不佳，{leader.name} 决定开始撤退。"
            return False, retreat_floor, f"{leader.name} 决定继续在地下城内前进。"
        if grade >= 4 and (leader.talent.get(12, 0) or leader.talent.get(161, 0)):
            return True, retreat_floor, f"即使再顽强，{leader.name} 也已经濒危，只能开始撤退。"
        if grade >= 3:
            return True, retreat_floor, f"{leader.name} 伤势过重，决定开始撤退。"
        if grade >= 2 and leader.talent.get(10, 0):
            return True, retreat_floor, f"胆小的{leader.name} 受伤后决定开始撤退。"
        return False, retreat_floor, f"{leader.name} 决定继续在地下城内前进。"






    def _show_dungeon_info_panel(self):
        print("\n【Dungeon Info】")
        for line in self._get_dungeon_setup_lines():
            print(line)
        self._pause()






    def _show_dungeon_no_selection_message(self) -> None:
        print("\n* 还没有选择对象！！ *")
        self._pause()






    def _show_dungeon_parties_panel(self):
        parties = self._get_standard_dungeon_party_candidates()
        print("\n【Dungeon Parties】")
        if not parties:
            print(" 当前没有在地下城活动中的队伍。")
        else:
            for idx, char in parties:
                print(f" [{idx}] {char.name} - {self._summarize_dungeon_party(char)}")
        self._pause()






    def _show_dungeon_personnel_group(self, selected: int) -> None:
        if selected == 10:
            self._show_dungeon_personnel_range(1, 10)
        elif selected == 11:
            self._show_dungeon_personnel_range(1, 3)
        elif selected == 12:
            self._show_dungeon_personnel_range(4, 6)
        elif selected == 13:
            self._show_dungeon_personnel_range(7, 9)
        else:
            self._show_dungeon_personnel_range(10, 10)






    def _show_dungeon_personnel_range(self, start_floor: int, end_floor: int) -> None:
        print("\n******************")
        print("地下城内的部下")
        print("******************")
        stock = self._get_monster_stock()
        for floor in range(start_floor, end_floor + 1):
            print("-" * 30)
            print(f"第{floor}阶层" if floor != 10 else "近卫兵")
            for monster_id in self._get_floor_monster_ids(floor):
                count = int(stock.get(monster_id, 0))
                if count > 0:
                    print(f" [{monster_id}] {count}只{self._get_item_name(monster_id)}")
        self._pause()






    def _strip_dungeon_quest_label_prefix(self, label: str, quest_type: int) -> str:
        prefix = DUNGEON_QUEST_SUBJECT_PREFIXES.get(int(quest_type), "")
        return label.removeprefix(prefix) if prefix else label






    def _summarize_dungeon_party(self, char: Character) -> str:
        floor = char.cflag.get(501, 1)
        progress = char.cflag.get(502, 0)
        status = self._get_dungeon_status_name(char)
        retreating = " *逃走中*" if char.cflag.get(507, 0) else ""
        return f"{status} / 第{floor}阶层 / 侵攻度{progress}%{retreating}"






    def _toggle_dungeon_floor_selection(self, selected: int, flags: List[int]) -> None:
        floor = selected // 10 - 10
        if 1 <= floor <= 9:
            flags[0] ^= 1 << (floor - 1)






    def _toggle_dungeon_trap_selection(self, selected: int, flags: List[int]) -> None:
        if selected == 200:
            new_value = 0 if flags == [511, 511, 511] else 511
            flags[0] = flags[1] = flags[2] = new_value
            return
        if selected > 200:
            slot = selected - 201
            if 0 <= slot < 3:
                flags[slot] = 0 if flags[slot] == 511 else 511
            return
        floor = selected // 10 - 10
        slot_code = selected % 10
        if floor < 1 or floor > 9:
            return
        bit = 1 << (floor - 1)
        if slot_code == 0:
            all_selected = all(flag & bit for flag in flags)
            for idx in range(3):
                flags[idx] = flags[idx] & ~bit if all_selected else flags[idx] | bit
        elif 1 <= slot_code <= 3:
            slot = slot_code - 1
            flags[slot] ^= bit






    def _try_apply_dungeon_ring_reward(self, leader: Character, item_id: int) -> Optional[str]:
        if item_id < 300 or item_id >= 321:
            return None
        floor = max(1, int(leader.cflag.get(501, 1)))
        for slot_id in (551, 552):
            current_code = int(leader.cflag.get(slot_id, -1))
            if self._is_cursed_ring_code(current_code):
                return f"{leader.name} 发现了 {self._get_item_name(item_id)}，但诅咒中的装饰无法替换。"
        for slot_id in (551, 552):
            if not self._can_replace_dungeon_ring_slot(leader, slot_id, floor):
                continue
            leader.cflag[slot_id] = self._build_dungeon_ring_code(leader, item_id, floor)
            return f"{leader.name} 发现了 {self._get_item_name(item_id)}，并将其装备到了{self._get_equipment_slot_name(slot_id)}。"
        return f"{leader.name} 发现了 {self._get_item_name(item_id)}，但身上的装饰槽没有更换的必要。"






    def _update_dungeon_depth_goal(self, leader: Character, floor_before: int) -> List[str]:
        messages: List[str] = []
        if leader.cflag.get(1, 0) != 2 or self._get_active_campaign_id() > 0:
            return messages
        current_goal = max(1, int(leader.cflag.get(520, 0)))
        if current_goal >= floor_before:
            return messages
        if self._can_dungeon_party_press_deeper(leader):
            leader.cflag[520] = floor_before
            messages.append(f"{leader.name} 状态良好，决定把探索目标提高到第{floor_before + 1}阶层。")
        else:
            leader.cflag[507] = 1
            messages.append(f"{leader.name} 决定停止继续深入，开始撤退。")
        return messages






    def show_dungeon(self):
        """Dungeon menu aligned to the current dungeon setup / party flow."""
        self._dungeon_display_mode = 0
        self._dungeon_selection_flags = [0, 0, 0]
        while True:
            if self._advance_dungeon_menu():
                return

    def _dungeon_room(self):
        return self.call_erb_function('DUNGEON_ROOM')

    def _dungeon_town(self):
        return self.call_erb_function('DUNGEON_TOWN')

    def _dungeon_trap(self):
        return self.call_erb_function('DUNGEON_TRAP')

    def _dungeon_bitch(self):
        return self.call_erb_function('DUNGEON_BITCH')

    def _dungeon_info(self):
        return self.call_erb_function('DUNGEON_INFO')

    def _dungeon_farm(self):
        return self.call_erb_function('DUNGEON_FARM')

    def _dungeon_hotel(self):
        return self.call_erb_function('DUNGEON_HOTEL')

    def _dungeon_battle2_party(self):
        return self.call_erb_function('DUNGEON_BATTLE2_PARTY')





