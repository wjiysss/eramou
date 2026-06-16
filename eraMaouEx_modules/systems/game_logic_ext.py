from __future__ import annotations
"""Module for GameLogicMixin - 游戏逻辑"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class GameLogicMixin:
    """Mixin providing 游戏逻辑 methods for GameEngine"""

    def _calc_beastsex_count(self, target: Character) -> int:
        """计算兽奸回数"""
        b = 0
        abl_beast = int(target.abl.get(39, 0))
        if abl_beast == 0:
            b -= 2
        elif abl_beast == 1:
            b -= 1
        elif abl_beast == 2:
            b += 0
        elif abl_beast == 3:
            b += 1
        elif abl_beast == 4:
            b += 2
        elif abl_beast == 5:
            b += 3
        elif abl_beast >= 6:
            b += 4

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = self._get_palam_level(palam_lust)

        if int(target.talent.get(124, 0)) and int(target.abl.get(11, 0)) >= 3 and lust_lv >= 3:
            b += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and lust_lv >= 4:
            b += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and lust_lv >= 4:
            b += 1

        if int(target.talent.get(136, 0)):
            b += 2

        if b <= 0:
            return 0

        if int(target.talent.get(17, 0)):
            b += 1
        if int(target.talent.get(33, 0)):
            b += 1
        if int(target.talent.get(124, 0)):
            b += 1
        if int(target.talent.get(15, 0)):
            b -= 1
        if int(target.talent.get(20, 0)):
            b -= 1
        if int(target.talent.get(32, 0)):
            b -= 1
        if int(target.talent.get(62, 0)) and int(target.talent.get(64, 0)) == 0:
            b -= 2

        if int(target.talent.get(70, 0)):
            b += 1
        elif int(target.talent.get(71, 0)):
            b -= 2

        if int(target.talent.get(76, 0)):
            b += 1

        if int(target.talent.get(136, 0)):
            b = int(b * 1.50)

        return max(b, 0)

    def _calc_interest(self) -> None:
        """计算存款利息和欠款滞纳金"""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))
        # EX_FLAG:9000 bit 0 未设置则不计算利息
        if not (ex_flag_9000 & 1):
            return

        current_day = self._get_total_day_count()
        last_op_day = int(g.get(9002, 0))
        savings = int(g.get(9001, 0))
        debt = int(g.get(9003, 0))

        if last_op_day > 0 and current_day - last_op_day >= 30:
            days_passed = current_day - last_op_day
            # 利息 = 存款 * 天数 * (20+随机0-4) / 1000
            interest = savings * days_passed * (20 + random.randint(0, 4)) // 1000
            g[9001] = savings + interest

            # 欠款滞纳金
            if debt > 0:
                first_loan_day = int(g.get(9006, 0))
                if first_loan_day > 0 and current_day - first_loan_day >= 30:
                    penalty = debt * 5 // 10  # 50%滞纳金
                    g[9003] = debt + penalty

            g[9002] = current_day

    def _calc_lesbian_play_count(self, target: Character, assistant: Character) -> int:
        """计算百合PLAY回数"""
        n = 0

        target_les_lv = int(target.abl.get(33, 0))
        n += {1: 1, 2: 2, 3: 3, 4: 5, 5: 7}.get(target_les_lv, 9 if target_les_lv >= 6 else 0)

        assi_les_lv = int(assistant.abl.get(33, 0))
        n += {1: 1, 2: 2, 3: 5, 4: 8, 5: 13}.get(assi_les_lv, 18 if assi_les_lv >= 6 else 0)

        if n <= 0:
            return 0

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = self._get_palam_level(palam_lust)

        if int(target.abl.get(22, 0)) >= 5 and lust_lv >= 3:
            n += 1
        if int(assistant.abl.get(22, 0)) >= 3 and lust_lv >= 3:
            n += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and lust_lv >= 3:
            n += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and lust_lv >= 3:
            n += 1

        relation = self._get_relation_value(assistant)
        if relation > 0:
            n = n * relation // 100

        if int(target.talent.get(24, 0)):
            n -= 1
        if int(assistant.talent.get(24, 0)):
            n -= 1
        if int(target.talent.get(27, 0)):
            n -= 1
        if int(assistant.talent.get(27, 0)):
            n -= 1

        if int(target.talent.get(81, 0)):
            n += 2
        if int(assistant.talent.get(81, 0)):
            n += 2
        if int(target.talent.get(76, 0)):
            n += 1
        if int(assistant.talent.get(76, 0)):
            n += 1

        if int(target.talent.get(70, 0)):
            n += 1
        elif int(target.talent.get(71, 0)):
            n -= 2
        if int(assistant.talent.get(70, 0)):
            n += 1
        elif int(assistant.talent.get(71, 0)):
            n -= 2

        return max(n, 0)

    def _calc_loan_limit(self) -> int:
        """计算贷款额度"""
        player = self._get_player()
        if player is None:
            return 0
        level = int(player.cflag.get(9, 0))
        if level < 10:
            return 100000 + level * 10000
        elif level < 51:
            return 200000 + (level - 10) * 100000
        elif level < 101:
            return 4200000 + (level - 50) * 1000000
        else:
            return 54200000 + (level - 100) * 10000000

    def _calc_masturbation_count(self, target: Character, assistant: Optional[Character] = None) -> int:
        """计算自慰回数"""
        import random
        a = 0
        abl_mast = int(target.abl.get(31, 0))
        if abl_mast == 1:
            a += 1
        elif abl_mast == 2:
            a += 2
        elif abl_mast == 3:
            a += 4
        elif abl_mast == 4:
            a += 6
        elif abl_mast == 5:
            a += 9
        elif abl_mast >= 6:
            a += 14

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = self._get_palam_level(palam_lust)

        if int(target.talent.get(60, 0)) and int(target.abl.get(11, 0)) >= 3 and lust_lv >= 3:
            a += 1
        if assistant is not None and int(assistant.talent.get(118, 0)) and int(target.abl.get(11, 0)) >= 4 and lust_lv >= 3:
            a += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and lust_lv >= 4:
            a += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and lust_lv >= 4:
            a += 1

        if int(target.talent.get(74, 0)):
            a = int(a * 1.50)
        if assistant is not None and int(assistant.talent.get(118, 0)):
            a = int(a * 1.20)

        if int(target.talent.get(17, 0)):
            a += 1
        if int(target.talent.get(33, 0)):
            a += 1
        if int(target.talent.get(15, 0)):
            a -= 1
        if int(target.talent.get(20, 0)):
            a -= 1
        if int(target.talent.get(32, 0)):
            a -= 1

        if int(target.talent.get(70, 0)):
            a += 1
        elif int(target.talent.get(71, 0)):
            a -= 2

        if int(target.talent.get(76, 0)):
            a += 1

        return max(a, 0)

    def _calc_selfcall_factor(self, target: Character) -> tuple:
        """Calculate self-call factors: education, posture, openness.
        Corresponds to ERB @CALC_SELFCALL_FACTOR.
        Returns (L_教育, L_姿态, L_开放).
        """
        import random
        l_education = 0
        l_posture = 0
        l_openness = 0

        # Race factor
        race = self._get_character_race_name(target)
        if race in ("精灵", "暗精灵"):
            l_education += 2
            l_posture += 2
            l_openness += 2
        elif race in ("天使", "堕天使"):
            l_openness += 2
        elif race == "吸血鬼":
            l_education += 2
            l_posture += 1
        elif race == "龙族":
            l_education += 2
            l_posture += 1
            l_openness -= 2
        elif race == "魔族":
            # Race2 sub-factor
            race2 = self._get_character_race2_name(target)
            if race2 == "植物":
                l_posture -= 1
            elif race2 in ("妖精", "史莱姆"):
                l_education += 1
            elif race2 in ("魔兽",):
                l_education -= 2
        elif race == "矮人":
            l_education -= 2
            l_posture += 1
            l_openness -= 1

        # Pre-hero life factor
        life = self._get_character_pre_hero_life(target)
        if life == "学生":
            l_education += 1
        elif life == "修女":
            l_education += 1
            l_posture -= 1
        elif life in ("巫女", "预言家", "占卜师", "隐士"):
            l_education += 1
            l_openness -= 2
        elif life in ("小偷", "乞丐", "贫民"):
            l_education -= 2
        elif life == "商人":
            l_education += 1
            l_posture -= 2
        elif life == "军人":
            l_posture -= 2
        elif life == "贵族":
            l_posture += 2

        # Talent factors
        # 高贵 (163)
        if target.talent.get(163, 0):
            l_education += 2
            l_posture += 2
        # 智慧 (172)
        if target.talent.get(172, 0):
            l_education += 2
            l_posture -= 1
        # 懦弱 (162)
        if target.talent.get(162, 0):
            l_posture -= 2
        # 恶女 (166)
        if target.talent.get(166, 0):
            l_education += 1
            l_posture += 2
            if random.randint(0, 3) == 0:
                l_posture += 1
        # 贵公子 (174)
        if target.talent.get(174, 0):
            l_education += 2
            l_posture += 1
            if random.randint(0, 3) == 0:
                l_posture += 2
            if random.randint(0, 2) == 0:
                l_education += 1
        # 好奇的 (23)
        if target.talent.get(23, 0):
            l_openness += 5
        # 保守的 (24)
        if target.talent.get(24, 0):
            l_openness = -10
        # 嚣张(16)、傲娇(18)
        if target.talent.get(16, 0) or target.talent.get(18, 0):
            l_posture += 5
        # 高姿态 (15)
        if target.talent.get(15, 0):
            l_posture = 10
        # 低姿态 (17)
        if target.talent.get(17, 0):
            l_posture = -10

        return (l_education, l_posture, l_openness)

    def _is_aphrodisiac_weekly_decay_day(self) -> bool:
        return (int(self.interpreter.vars.day[2]) + 1) % 7 == 0

    def _is_birth_elite_template_id(self, template_id: Optional[int]) -> bool:
        return template_id is not None and 201 <= int(template_id) <= 210

    def _is_calendar_month_overflow(self) -> bool:
        month = int(self.interpreter.vars.day[1])
        day = int(self.interpreter.vars.day[2])
        return day > self._get_calendar_month_length(month)

    def _is_cursed_ring_code(self, equip_code: int) -> bool:
        if equip_code < 0:
            return False
        base_code, _, _ = self._decode_equipment_code(equip_code)
        return 6 <= base_code <= 20

    def _is_dog_walk_no_sex(self, char: Character) -> bool:
        if char.talent.get(0, 0) or char.talent.get(273, 0):
            return True
        accessory_id = int(char.cflag.get(42, 0))
        return accessory_id == 79 and bool(char.cflag.get(40, 0) & 64) and self.interpreter.vars.get_flag(37, 0) != 0

    def _is_duplicate_hero_entry_allowed(self) -> bool:
        return bool(int(self.interpreter.vars.get_flag(5, 0)) & (1 << 32))

    def _is_hero_level_scaling_enabled(self) -> bool:
        return bool(int(self.interpreter.vars.get_flag(5, 0)) & (1 << 1))

    def _is_maou_shadow(self, target: Optional[Character]) -> bool:
        return bool(target is not None and target.talent.get(292, 0))

    def _is_part_time_job_system_enabled(self) -> bool:
        return self._get_flag_bit(9000, 2)

    def _is_player_character(self, target: Character) -> bool:
        return bool(self.interpreter.vars.chars) and self.interpreter.vars.chars[0] is target

    def _is_same_sex_pair(self, player: Optional[Character], target: Character) -> bool:
        if player is None:
            return False
        return player.talent.get(122, 0) == target.talent.get(122, 0)

    def _is_training_master_affection_blocked(self, target: Character) -> bool:
        if self._get_current_assistant() is not None:
            return True
        if int(target.equipt.get(90, 0)) != 0:
            return True
        return False

    def _is_valid_magic_item_slot_choice(self, player: Character, item_id: int) -> bool:
        return 300 <= item_id < 320 and self._is_item_owned(player, item_id)

    def _is_weapon_usable_by_character(self, target: Character, base_code: int) -> bool:
        if 0 <= base_code <= 20:
            return True
        weapon_groups = (
            (200, {40, 42, 43, 47, 48, 50, 51, 52}),
            (201, {41, 46}),
            (202, {41, 46}),
            (203, {42, 43, 44, 50, 52}),
            (205, {40, 42, 43, 47, 48, 50}),
            (206, {40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51}),
            (207, {43, 44, 50, 52}),
            (208, {43, 45}),
        )
        for talent_id, allowed in weapon_groups:
            if int(target.talent.get(talent_id, 0)):
                return base_code in allowed
        return False

    def _scale_exhibitionist_cost(self, target: Character, amount: int) -> int:
        if target.talent.get(28, 0):
            return amount * 50 // 100
        return amount

    def _scale_lesbian_cost(self, target: Character, amount: int) -> int:
        if target.talent.get(81, 0):
            return amount * 25 // 100
        return amount

    def _scale_line_crossing_cost(self, target: Character, amount: int, level: int) -> int:
        if target.talent.get(27, 0):
            if level == 3:
                return amount * 2
            if level == 4:
                return amount * 3
        return amount

    def _scale_perverse_cost(self, target: Character, amount: int) -> int:
        if target.talent.get(80, 0):
            return amount * 75 // 100
        return amount

    def _scale_release_cost(self, target: Character, amount: int) -> int:
        if target.talent.get(33, 0):
            return amount * 50 // 100
        return amount

    def _scale_training_source_if_present(self, source: Dict[int, int], idx: int, scale: float) -> None:
        if int(source.get(idx, 0)) == 0:
            return
        source[idx] = self._scale_value(int(source.get(idx, 0)), scale)

    def _scale_value(self, value: int, factor: float) -> int:
        return int(value * factor)

    def _should_apply_daily_dematurity_check(self, target: Character) -> bool:
        return int(target.mark.get(3, 0)) == 3

    def _should_apply_daily_due_birth_event(self, target: Character, today: int) -> bool:
        if not target.talent.get(153, 0):
            return False
        due_day = int(target.cflag.get(110, 0))
        return due_day > 0 and due_day == today

    def _should_apply_onesho_event(self, idx: int, char: Character) -> bool:
        return idx > 0 and self._can_trigger_onesho(char)

    def _should_character_loot_after_quest_battle(self, actor: Character) -> bool:
        score = 0
        karma = int(actor.cflag.get(151, 0))
        if karma > 150:
            score += random.randint(0, 124)
        elif karma > 100:
            score += random.randint(0, 74)
        elif karma > 50:
            score += random.randint(0, 34)
        elif karma > 0:
            score += random.randint(0, 24)
        else:
            score += random.randint(0, 14)

        if int(actor.talent.get(17, 0)):
            score -= 1
        if int(actor.talent.get(23, 0)):
            score -= 1
        if int(actor.talent.get(17, 0)):
            score -= 1
        if int(actor.talent.get(36, 0)):
            score -= 1
        if int(actor.talent.get(203, 0)):
            score -= 1

        if int(actor.talent.get(15, 0)):
            score += 1
        if int(actor.talent.get(20, 0)):
            score += 1
        if int(actor.talent.get(27, 0)):
            score += 1
        if int(actor.talent.get(35, 0)):
            score += 1
        return score <= 5

    def _should_process_pregnancy_room_transfer(self, target: Character) -> bool:
        return bool(target.talent.get(153, 0) or target.talent.get(154, 0))
