from __future__ import annotations
"""Module for SummonExtMixin - 召唤怪物"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SummonExtMixin:
    """Mixin providing 召唤怪物 methods for GameEngine"""

    def _advance_otherworld_hero_summon_menu(self) -> bool:
        self._render_otherworld_hero_summon_menu()
        sex_choice = self._handle_otherworld_hero_summon_sex_choice(self._prompt_otherworld_hero_summon_choice())
        if sex_choice == -1:
            return True
        if sex_choice is None:
            return False

        preview_result = self._prepare_otherworld_hero_summon_preview(sex_choice)
        if preview_result is None:
            return False
        preview_char = preview_result
        return self._handle_otherworld_hero_summon_preview_confirmation(preview_char)






    def _advance_summon_menu(self) -> bool:
        ok, message = self._can_open_monster_shop()
        self._render_summon_main_menu(ok, message)
        choice = self._prompt_summon_choice()
        if self._handle_summon_main_menu_command_choice(choice):
            return choice == "100"
        print("\nInvalid selection.")
        self._pause()
        return False




    def _apply_shadow_summon_state(self, target: Character):
        target.talent[292] = 1
        target.cflag[1] = 11
        target.cflag[420] = 1
        target.cflag[820] = 666666
        self._reset_shadow_summon_progress_flags(target)






    def _apply_story_monster_summon_bonus(self, monster_id: int, count: int) -> int:
        adjusted = max(1, int(count))
        princess = self._find_character_by_template_id(35)
        if princess is not None and int(princess.talent.get(1254, 0)) == 1:
            adjusted = adjusted * 150 // 100

        square = self._find_character_by_template_id(21)
        if square is not None and int(square.talent.get(474, 0)) == 1 and int(monster_id) in (160, 170):
            adjusted = adjusted * 150 // 100
        return adjusted






    def _finalize_otherworld_hero_summon_preview(self, preview_char: Character) -> bool:
        ok, message = self._finalize_otherworld_hero_preview(preview_char)
        if not ok:
            self._remove_last_character_if_matches(preview_char)
            print(f"\n{message}")
            self._pause()
            return False
        print(f"\n{message}")
        self._pause()
        return True






    def _get_shadow_summon_candidate_range(self) -> range:
        return range(150, 200)






    def _get_summon_attempt_count(self, weak_mode: bool = False) -> int:
        player = self._get_player()
        level = int(player.cflag.get(9, 0)) if player is not None else 0
        attempts = 5
        for threshold in [10, 30, 50, 70, 100]:
            if level >= threshold:
                attempts += 1
        if player is not None and player.talent.get(325, 0):
            attempts += 1
        if weak_mode:
            attempts //= 2
        return max(1, attempts)






    def _get_summon_stack_size(self, monster_id: int) -> int:
        player = self._get_player()
        level = int(player.cflag.get(9, 0)) if player is not None else 0
        summon_pow = max(0, (monster_id - 100) // 10)
        base_roll_max = max(1, 25 - (summon_pow * 3))
        count = random.randint(0, base_roll_max - 1) + 1
        for threshold in [20, 40, 60, 80, 100]:
            if level >= threshold:
                count += 1
        if player is not None and player.talent.get(327, 0):
            count += 1
        count = self._apply_story_monster_summon_bonus(monster_id, count)
        return max(1, count)






    def _handle_otherworld_hero_summon_confirm_choice(self, preview_char: Character, confirm_choice: str) -> Optional[bool]:
        if confirm_choice == "100":
            self._remove_last_character_if_matches(preview_char)
            return False
        if confirm_choice == "1":
            if self.interpreter.vars.money <= 1500:
                print("\n金钱不够！")
                self._remove_last_character_if_matches(preview_char)
                self._pause()
                return False
            self._spend_global_money(1500)
            self._remove_last_character_if_matches(preview_char)
            print("\n你重新连接了次元大门，准备换一个对象。")
            self._pause()
            return False
        if confirm_choice != "0":
            print("\nInvalid selection.")
            self._remove_last_character_if_matches(preview_char)
            self._pause()
            return False
        return None






    def _handle_otherworld_hero_summon_preview_confirmation(self, preview_char: Character) -> bool:
        print(" 确定要召唤这名异界勇者么？")
        print(" [0] 就是她/他了")
        print(" [1] 再换一个（花费1500）")
        print(" [100] 返回")
        confirm_result = self._handle_otherworld_hero_summon_confirm_choice(preview_char, self._prompt_otherworld_hero_summon_choice())
        if confirm_result is not None:
            return False
        if self._finalize_otherworld_hero_summon_preview(preview_char):
            return True
        return False






    def _handle_otherworld_hero_summon_sex_choice(self, choice_raw: str) -> Optional[int]:
        if choice_raw == "100":
            return -1
        try:
            sex_choice = int(choice_raw)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        if sex_choice not in (1, 2, 3):
            print("\nInvalid selection.")
            self._pause()
            return None
        return sex_choice






    def _handle_summon_main_menu_command_choice(self, choice: str) -> bool:
        if choice == "100":
            return True
        if choice == "1":
            self._show_monster_follower_summon_menu()
            return True
        return False






    def _prepare_otherworld_hero_summon_preview(self, sex_choice: int) -> Optional[Character]:
        preview_ok, preview_message = self._apply_otherworld_hero_template(sex_choice, finalize=False)
        print(f"\n{preview_message}")
        if not preview_ok:
            self._pause()
            return None
        preview_char = self.interpreter.vars.chars[-1] if self.interpreter.vars.chars else None
        if preview_char is None:
            print("\n召唤失败。")
            self._pause()
            return None
        return preview_char






    def _prompt_otherworld_hero_summon_choice(self):
        return self._prompt_choice()






    def _prompt_summon_choice(self):
        return self._prompt_choice()






    def _render_otherworld_hero_summon_menu(self):
        print("\n【召唤异界勇者】")
        print("-" * 30)
        print("《需要勋章经验来激活次元大门，并支付一定金钱来召唤异界勇者》")
        print(f" 所持金: {self.interpreter.vars.money} 点")
        print(f" 勋章: {self._get_medal_count()} 点")
        print(" 请选择要召唤的勇者的性别")
        print(" [1] 男性")
        print(" [2] 女性")
        print(" [3] 扶她")
        print(" [100] 返回")






    def _render_summon_main_menu(self, ok, message):
        print("\n【召唤】")
        print("-" * 30)
        print("《需要献祭同类的怪物，并支付一定金钱来召唤精英魔物从者》")
        print(f" 所持金: {self.interpreter.vars.money}点")
        print(f" 当前角色数: {len(self.interpreter.vars.chars)}/{self._get_max_charanum()}")
        print(f" 魔物从者数: {self._count_monster_followers()}/30")
        if ok:
            print(" [1] 召唤魔物从者")
        else:
            print(f" 召唤魔物从者: {message}")
        print(" [100] Back")






    def _reset_shadow_summon_progress_flags(self, target: Character):
        for flag_id in range(800, 811):
            target.cflag[flag_id] = 0






    def _show_otherworld_hero_summon_menu(self):
        while True:
            if self._advance_otherworld_hero_summon_menu():
                return

    def show_summon(self):
        """Monster summon shop aligned to SHOP_MONSTER.ERB."""
        while True:
            if self._advance_summon_menu():
                return

    def _summon_monster_master(self):
        return self.call_erb_function('SUMMON_MONSTER_MASTER')

    def _summon_slave(self):
        return self.call_erb_function('SUMMON_SLAVE')

    def _summon_trap(self):
        return self.call_erb_function('SUMMON_TRAP')





