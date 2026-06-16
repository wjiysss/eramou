from __future__ import annotations
"""Module for TrainExtMixin - 训练系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class TrainExtMixin:
    """Mixin providing 训练系统 methods for GameEngine"""

    def _advance_train_menu(self) -> Optional[str]:
        player = self._get_player()
        if player is not None:
            self._ensure_player_ejaculation_gauge(player)

        target = self._get_train_menu_target()
        if target is None:
            return "SHOP"

        available_commands = self._get_available_train_commands(target)
        choice = self._prompt_train_choice(target, available_commands)
        return self._handle_train_menu_choice(choice, target, available_commands)




    def _apply_train_command_128_134_common_sequence(
        self,
        target: Character,
        player: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
        love_exp: int = 0,
        stain_transfer: Optional[str] = None,
    ):
        self._apply_sex_virgin_break(target, player, exp_delta, submission_floor=2)
        self._apply_vaginal_sex_shared_effects(player, target)
        if stain_transfer == "mouth":
            self._apply_mouth_stain_transfer(target, player)
        elif stain_transfer == "rear":
            self._apply_standing_rear_stain_transfer(target, player)
        self._apply_sex_ejaculation_to_receiver(player, target, exp_delta, source, target, 1)
        self._add_love_exp(exp_delta, target, love_exp)






    def _apply_train_command_2_anal_exp_adjustments(self, target: Character, source: Dict[int, int]) -> None:
        anal_exp_level = self._get_exp_level(target.exp.get(1, 0))
        if anal_exp_level == 0:
            source[2] = self._scale_value(source[2], 0.2)
            source[13] = self._scale_value(source[13], 0.2)
            source[6] = 500
            source[14] += 200
        elif anal_exp_level == 1:
            source[2] = self._scale_value(source[2], 0.5)
            source[13] = self._scale_value(source[13], 0.5)
            source[6] = 400
            source[14] += 100
        elif anal_exp_level == 2:
            source[6] = 300
            source[14] += 50
        elif anal_exp_level == 3:
            source[2] = self._scale_value(source[2], 1.2)
            source[13] = self._scale_value(source[13], 1.2)
            source[6] = 200
        elif anal_exp_level == 4:
            source[2] = self._scale_value(source[2], 1.6)
            source[13] = self._scale_value(source[13], 1.6)
            source[6] = 100
        else:
            source[2] = self._scale_value(source[2], 1.8)
            source[13] = self._scale_value(source[13], 1.8)
            source[6] = 50






    def _apply_train_command_2_lubrication_adjustments(self, target: Character, source: Dict[int, int]) -> None:
        lubrication_level = self._get_palam_level(target.palam.get(3, 0))
        if lubrication_level == 0:
            source[2] = self._scale_value(source[2], 0.1)
            source[13] = self._scale_value(source[13], 0.1)
            source[6] = self._scale_value(source[6], 3.0)
        elif lubrication_level == 1:
            source[2] = self._scale_value(source[2], 0.2)
            source[13] = self._scale_value(source[13], 0.2)
            source[6] = self._scale_value(source[6], 2.0)
        elif lubrication_level == 2:
            source[2] = self._scale_value(source[2], 0.6)
            source[13] = self._scale_value(source[13], 0.6)
        elif lubrication_level == 3:
            source[6] = self._scale_value(source[6], 0.5)
        else:
            source[2] = self._scale_value(source[2], 2.0)
            source[13] = self._scale_value(source[13], 2.0)
            source[6] = self._scale_value(source[6], 0.1)

        lust_level = self._get_palam_level(target.palam.get(5, 0))
        source[2] = self._scale_value(source[2], self._level_value(lust_level, [30, 60, 100, 130, 160, 160]) / 100.0)
        source[13] = self._scale_value(source[13], self._level_value(lust_level, [30, 60, 100, 130, 160, 160]) / 100.0)






    def _apply_train_command_2_stain_effects(self, target: Character, player: Optional[Character]) -> None:
        if target.equipt.get(90, 0) > 0:
            target.stain[4] = target.stain.get(4, 0) | 2 | 4
            self._add_pregnancy_source_amount(target, 6, 1)
        else:
            self._apply_finger_stain_transfer(target, player, 4)






    def _apply_train_command_2_talent_adjustments(self, target: Character, source: Dict[int, int]) -> None:
        if target.talent.get(263, 0):
            source[2] = self._scale_value(source[2], 1.5)
        if target.talent.get(105, 0):
            source[6] = self._scale_value(source[6], 1.5)
            source[13] = self._scale_value(source[13], 1.5)
            source[14] = self._scale_value(source[14], 1.5)
        elif target.talent.get(106, 0):
            source[6] = self._scale_value(source[6], 0.6)
            source[13] = self._scale_value(source[13], 0.6)
            source[14] = self._scale_value(source[14], 0.6)
        if target.talent.get(0, 0) and target.talent.get(30, 0):
            source[13] = self._scale_value(source[13], 0.8)
            source[14] = self._scale_value(source[14], 0.5)
        if target.talent.get(135, 0):
            source[6] = self._scale_value(source[6], 2.0)






    def _apply_train_command_3_addiction_scaling(self, target: Character, source: Dict[int, int], addiction_level: int) -> None:
        source[7] = self._level_value(addiction_level, [0, 100, 300, 800, 1500, 2500])
        high_addiction_scale = self._level_value(addiction_level, [100, 110, 120, 130, 150, 170]) / 100.0
        low_addiction_scale = self._level_value(addiction_level, [100, 110, 120, 130, 150, 150]) / 100.0
        for key in [0, 17]:
            source[key] = self._scale_value(source.get(key, 0), high_addiction_scale)
        for key in [1, 2]:
            source[key] = self._scale_value(source.get(key, 0), low_addiction_scale)






    def _apply_train_command_3_anal_effects(self, target: Character, source: Dict[int, int], losebase: Dict[int, int], anal_gain: int, pain_gain: int, pleasure_penalty: int) -> tuple[int, int, int]:
        if target.equipt.get(13, 0):
            return self._apply_train_command_3_anal_effects_with_plug(target, source, losebase, anal_gain, pain_gain, pleasure_penalty)
        elif target.equipt.get(18, 0):
            return self._apply_train_command_3_anal_effects_with_anal_gear(target, source, anal_gain, pleasure_penalty)
        return self._apply_train_command_3_anal_effects_without_anal_gear(source, anal_gain, pain_gain, pleasure_penalty)






    def _apply_train_command_3_anal_effects_with_anal_gear(self, target: Character, source: Dict[int, int], anal_gain: int, pleasure_penalty: int) -> tuple[int, int, int]:
        source[0] = self._level_value(target.abl.get(0, 0), [150, 400, 800, 1200, 1500, 1800])
        source[12] = self._level_value(target.abl.get(0, 0), [1000, 1300, 1600, 1900, 2200, 2500])
        source[13] = self._level_value(target.abl.get(0, 0), [50, 80, 120, 190, 250, 300])
        source[1] = self._level_value(target.abl.get(2, 0), [0, 100, 200, 300, 400, 500])
        pleasure_penalty = self._level_value(target.abl.get(2, 0), [0, 300, 400, 500, 600, 700])
        anal_gain = self._level_value(target.abl.get(3, 0), [40, 120, 300, 500, 650, 850])
        pleasure_penalty += self._level_value(target.abl.get(3, 0), [150, 400, 700, 900, 1000, 1200])
        if target.talent.get(103, 0) or target.talent.get(105, 0):
            pleasure_penalty = self._scale_value(pleasure_penalty, 1.5)
        elif target.talent.get(104, 0) or target.talent.get(106, 0):
            pleasure_penalty = self._scale_value(pleasure_penalty, 0.6)
        source[13] += pleasure_penalty
        return anal_gain, 0, pleasure_penalty






    def _apply_train_command_3_anal_effects_with_plug(self, target: Character, source: Dict[int, int], losebase: Dict[int, int], anal_gain: int, pain_gain: int, pleasure_penalty: int) -> tuple[int, int, int]:
        losebase[0] += 30
        losebase[1] += 80
        anal_gain = self._level_value(target.abl.get(3, 0), [40, 120, 300, 500, 650, 850])
        pleasure_penalty += self._level_value(target.abl.get(3, 0), [150, 400, 700, 900, 1000, 1200])
        anal_exp_level = self._get_exp_level(target.exp.get(1, 0))
        anal_gain = self._scale_value(anal_gain, self._level_value(anal_exp_level, [50, 100, 110, 120, 140, 160]) / 100.0)
        pain_gain += self._level_value(anal_exp_level, [1000, 150, 20, 0, 0, 0])
        if target.talent.get(105, 0):
            pain_gain = self._scale_value(pain_gain, 1.5)
            pleasure_penalty = self._scale_value(pleasure_penalty, 1.5)
        elif target.talent.get(106, 0):
            pain_gain = self._scale_value(pain_gain, 0.6)
            pleasure_penalty = self._scale_value(pleasure_penalty, 0.6)
        source[13] += pleasure_penalty
        return anal_gain, pain_gain, pleasure_penalty






    def _apply_train_command_3_anal_effects_without_anal_gear(self, source: Dict[int, int], anal_gain: int, pain_gain: int, pleasure_penalty: int) -> tuple[int, int, int]:
        source[1] = 0
        source[2] = 0
        return anal_gain, pain_gain, pleasure_penalty






    def _apply_train_command_3_bathing_effects(self, target: Character) -> None:
        if not target.equipt.get(18, 0):
            return
        target.stain[1] = 0
        target.stain[2] = 2
        target.stain[3] = 1
        target.stain[4] = 8
        target.palam[3] = target.palam.get(3, 0) // 2






    def _apply_train_command_3_exhibition_effects(self, target: Character, source: Dict[int, int]) -> None:
        if not target.equipt.get(18, 0):
            return
        lubrication_level = self._get_palam_level(target.palam.get(3, 0))
        source[1] = source.get(1, 0) + self._scale_value(source.get(1, 0), self._level_value(lubrication_level, [40, 80, 100, 140, 180, 180]) / 100.0)
        source[2] = source.get(2, 0) + self._scale_value(source.get(2, 0), self._level_value(lubrication_level, [40, 80, 100, 140, 180, 180]) / 100.0)
        lust_level = self._get_palam_level(target.palam.get(5, 0))
        source[1] = self._scale_value(source.get(1, 0), self._level_value(lust_level, [80, 90, 100, 110, 120, 120]) / 100.0)
        source[2] = self._scale_value(source.get(2, 0), self._level_value(lust_level, [80, 90, 100, 110, 120, 120]) / 100.0)
        submission_level = target.abl.get(10, 0)
        source[1] = self._scale_value(source.get(1, 0), self._level_value(submission_level, [80, 90, 100, 110, 120, 130]) / 100.0)
        source[2] = self._scale_value(source.get(2, 0), self._level_value(submission_level, [80, 90, 100, 110, 120, 130]) / 100.0)






    def _apply_train_command_3_exhibition_scaling(self, target: Character, source: Dict[int, int]) -> None:
        exhibition_level = target.abl.get(17, 0)
        source[7] += self._level_value(exhibition_level, [0, 100, 300, 800, 1500, 2500])
        exhibition_scale = self._level_value(exhibition_level, [100, 110, 120, 130, 150, 170]) / 100.0
        exposure_scale = self._level_value(exhibition_level, [100, 120, 140, 160, 200, 300]) / 100.0
        for key in [0, 17, 1, 2]:
            source[key] = self._scale_value(source.get(key, 0), exhibition_scale)
        source[12] = self._scale_value(source.get(12, 0), exposure_scale)
        if target.talent.get(89, 0):
            source[7] += 500
            for key in [0, 17, 1, 2]:
                source[key] = self._scale_value(source.get(key, 0), 1.2)
            source[12] = self._scale_value(source.get(12, 0), 1.5)






    def _apply_train_command_3_post_effects(self, target: Character) -> None:
        self._apply_self_stain_transfer(target)
        if target.equipt.get(18, 0):
            target.stain[1] = 0
            target.stain[2] = 2
            target.stain[3] = 1
            target.stain[4] = 8
            target.palam[3] = target.palam.get(3, 0) // 2






    def _apply_train_command_3_progression_cap(self, target: Character, source: Dict[int, int]) -> None:
        if target.talent.get(125, 0) == 0 and target.talent.get(310, 0) <= 20:
            source[12] = self._scale_value(source.get(12, 0), 2.0)






    def _apply_train_command_3_progression_scaling(self, target: Character, source: Dict[int, int]) -> None:
        technique_level = target.abl.get(12, 0)
        self._apply_train_command_3_technique_scaling(target, source, technique_level)

        addiction_level = target.abl.get(31, 0)
        self._apply_train_command_3_addiction_scaling(target, source, addiction_level)

        if target.equipt.get(53, 0) or target.equipt.get(54, 0):
            self._apply_train_command_3_exhibition_scaling(target, source)

        self._apply_train_command_3_progression_cap(target, source)






    def _apply_train_command_3_scene_effects(self, target: Character, source: Dict[int, int], losebase: Dict[int, int]) -> tuple[int, int, int, int]:
        vaginal_gain = 0
        anal_gain = 0
        pain_gain = 0
        pleasure_penalty = 0

        vaginal_gain, pain_gain, pleasure_penalty = self._apply_train_command_3_vaginal_effects(target, source, vaginal_gain, pain_gain, pleasure_penalty)
        anal_gain, pain_gain, pleasure_penalty = self._apply_train_command_3_anal_effects(target, source, losebase, anal_gain, pain_gain, pleasure_penalty)
        vaginal_gain, anal_gain, pain_gain = self._apply_train_command_3_shared_sense_effects(target, source, vaginal_gain, anal_gain, pain_gain)
        self._apply_train_command_3_exhibition_effects(target, source)

        return vaginal_gain, anal_gain, pain_gain, pleasure_penalty

    # ========================================
    # COM4: 口交(主) (对应 ERB COMF4_フェラする.ERB)
    # ========================================






    def _apply_train_command_3_shared_sense_effects(self, target: Character, source: Dict[int, int], vaginal_gain: int, anal_gain: int, pain_gain: int) -> tuple[int, int, int]:
        if target.equipt.get(11, 0) or target.equipt.get(13, 0):
            combined_sense = target.abl.get(2, 0) + target.abl.get(3, 0)
            source[0] = self._scale_value(source[0], self._level_value(combined_sense, [100, 100, 90, 80, 70, 60, 50]) / 100.0)
            source[17] = self._scale_value(source[17], self._level_value(combined_sense, [100, 100, 90, 80, 70, 60, 50]) / 100.0)

            lubrication_level = self._get_palam_level(target.palam.get(3, 0))
            vaginal_gain = self._scale_value(vaginal_gain, self._level_value(lubrication_level, [40, 80, 100, 140, 180, 180]) / 100.0)
            anal_gain = self._scale_value(anal_gain, self._level_value(lubrication_level, [40, 80, 100, 140, 180, 180]) / 100.0)
            pain_gain += self._level_value(lubrication_level, [800, 500, 300, 120, 100, 100])

            lust_level = self._get_palam_level(target.palam.get(5, 0))
            vaginal_gain = self._scale_value(vaginal_gain, self._level_value(lust_level, [80, 90, 100, 110, 120, 120]) / 100.0)
            anal_gain = self._scale_value(anal_gain, self._level_value(lust_level, [80, 90, 100, 110, 120, 120]) / 100.0)

            submission_level = target.abl.get(10, 0)
            vaginal_gain = self._scale_value(vaginal_gain, self._level_value(submission_level, [80, 90, 100, 110, 120, 130]) / 100.0)
            anal_gain = self._scale_value(anal_gain, self._level_value(submission_level, [80, 90, 100, 110, 120, 130]) / 100.0)

            if target.talent.get(99, 0):
                pain_gain = self._scale_value(pain_gain, 0.8)
            if target.talent.get(100, 0):
                pain_gain = self._scale_value(pain_gain, 2.0)
            if target.talent.get(30, 0):
                pain_gain = self._scale_value(pain_gain, 3.0)

            source[1] = vaginal_gain
            source[2] = anal_gain
            source[6] = pain_gain
        return vaginal_gain, anal_gain, pain_gain






    def _apply_train_command_3_technique_scaling(self, target: Character, source: Dict[int, int], technique_level: int) -> None:
        source[4] = self._level_value(technique_level, [100, 160, 220, 280, 340, 400])
        technique_scale = self._level_value(technique_level, [30, 70, 100, 120, 140, 160]) / 100.0
        for key in [0, 17, 1, 2]:
            source[key] = self._scale_value(source.get(key, 0), technique_scale)






    def _apply_train_command_3_vaginal_effects(self, target: Character, source: Dict[int, int], vaginal_gain: int, pain_gain: int, pleasure_penalty: int) -> tuple[int, int, int]:
        if not target.equipt.get(11, 0):
            return vaginal_gain, pain_gain, pleasure_penalty

        vaginal_gain = self._level_value(target.abl.get(2, 0), [40, 120, 300, 500, 650, 850])
        pleasure_penalty += self._level_value(target.abl.get(2, 0), [150, 400, 700, 900, 1000, 1200])
        vaginal_exp_level = max(1, self._get_exp_level(target.exp.get(0, 0)))
        vaginal_gain = self._scale_value(vaginal_gain, self._level_value(vaginal_exp_level, [60, 60, 100, 120, 140, 160]) / 100.0)
        pain_gain += self._level_value(vaginal_exp_level, [0, 150, 20, 0, 0, 0])
        if target.talent.get(103, 0):
            pain_gain = self._scale_value(pain_gain, 1.5)
            pleasure_penalty = self._scale_value(pleasure_penalty, 1.5)
        elif target.talent.get(104, 0):
            pain_gain = self._scale_value(pain_gain, 0.6)
            pleasure_penalty = self._scale_value(pleasure_penalty, 0.6)
        source[13] += pleasure_penalty
        return vaginal_gain, pain_gain, pleasure_penalty






    def _apply_train_command_64_mode_effects(
        self,
        target: Character,
        player: Character,
        assistant: Character,
        mode_pair: tuple[int, int],
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> None:
        self._apply_threesome_penetration_effects(target, mode_pair, source, exp_delta)
        if 1 in mode_pair:
            self._apply_sex_virgin_break(target, player, exp_delta, submission_floor=2)
        self._apply_threesome_ejaculation(player, assistant, target, mode_pair, source, exp_delta)
        self._add_same_sex_exp(exp_delta, player, target, female_value=3, male_value=3)
        self._add_same_sex_exp(exp_delta, assistant, target, female_value=3, male_value=3)






    def _apply_train_command_6_first_kiss_mark(self, target: Character, player: Optional[Character]) -> int:
        love_exp = 1
        if target.talent.get(85, 0):
            love_exp += 2
        if target.cflag.get(16, -1) == -1:
            target.cflag[16] = 1
            if player is not None:
                target.cstr[4] = player.name
            love_exp += 20
            print("初吻标记已按 COM6 更新。")
        if player is not None and player.cflag.get(16, -1) == -1:
            player.cflag[16] = 1
            player.cstr[4] = target.name
        return love_exp

    # ========================================
    # COM8: 插入手指 (对应 ERB COMF8_指挿入れ.ERB)
    # ========================================






    def _apply_train_command_6_partner_branch(self, target: Character, player: Optional[Character], source: Dict[int, int]) -> None:
        if target.equipt.get(89, 0) > 0:
            beast_level = target.abl.get(39, 0)
            source[3] = self._level_value(beast_level, [0, 0, 0, 100, 300, 800])
            source[10] = self._level_value(beast_level, [0, 0, 0, 0, 100, 200])
            source[8] = self._scale_value(source[8], self._level_value(beast_level, [200, 100, 80, 50, 30, 10]) / 100.0)
            if target.cflag.get(16, -1) == -1:
                target.cflag[16] = 998
            return
        player_tech = player.abl.get(12, 0) if player is not None else 0
        source[3] = self._level_value(player_tech, [100, 150, 200, 300, 500, 800])
        source[10] = self._level_value(player_tech, [0, 0, 0, 50, 100, 200])
        if target.talent.get(85, 0):
            source[3] *= 2
        self._apply_mouth_stain_transfer(target, player)






    def _apply_train_command_6_service_scaling(self, target: Character, source: Dict[int, int]) -> None:
        service_level = target.abl.get(16, 0)
        source[4] = self._level_value(service_level, [50, 150, 200, 250, 300, 350])
        source[5] = self._level_value(service_level, [10, 50, 100, 180, 300, 500])
        source[8] = self._scale_value(source[8], self._level_value(service_level, [400, 250, 150, 100, 50, 10]) / 100.0)

        kiss_tech_level = target.abl.get(12, 0)
        source[4] = self._scale_value(source[4], self._level_value(kiss_tech_level, [50, 80, 100, 150, 250, 400]) / 100.0)
        source[5] = self._scale_value(source[5], self._level_value(kiss_tech_level, [50, 80, 100, 150, 250, 400]) / 100.0)






    def _apply_training_achieve_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(5, 0))
        if source_value == 0:
            return
        obedience_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.50, 0.80, 1.00, 1.20, 1.40, 1.60, 1.80, 2.00]))
        obedience_value = self._scale_value(obedience_value, self._level_value(int(target.abl.get(16, 0)), [0.00, 0.40, 0.80, 1.20, 1.60, 2.00, 2.40]))
        obedience_value = self._scale_value(obedience_value, self._level_value(int(target.abl.get(13, 0)), [0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30]))
        self._add_training_palam_gain(palam_delta, 4, obedience_value)






    def _apply_training_anal_pleasure_experience(
        self,
        target: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> None:
        base_value = int(source.get(2, 0))
        if base_value < 300:
            return
        scaled = base_value
        if base_value < 1000:
            scaled *= 1
        elif base_value < 5000:
            scaled *= 2
        elif base_value < 10000:
            scaled *= 3
        else:
            scaled *= 4
        gain = self._get_training_derived_exp_gain(scaled)
        if gain <= 0:
            return
        exp_delta[32] = exp_delta.get(32, 0) + gain
        self._scale_training_source_if_present(source, 11, self._get_training_derived_scale(scaled, (0.95, 0.90, 0.85, 0.85, 0.80, 0.80)))
        self._scale_training_source_if_present(source, 12, self._get_training_derived_scale(scaled, (1.00, 1.00, 0.95, 0.95, 0.90, 0.90)))
        self._scale_training_source_if_present(source, 6, self._get_training_derived_scale(scaled, (1.00, 1.00, 1.05, 1.10, 1.15, 1.20)))






    def _apply_training_autotrain_progress(self, target: Character) -> None:
        progress = int(target.cflag.get(666, 0))
        if progress <= 0:
            return
        target.cflag[667] = min(50, int(target.cflag.get(667, 0)) + progress)






    def _apply_training_derived_palam_effects(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        derived: Dict[int, int] = {}
        self._apply_training_love_palam_effects(target, source, derived)
        self._apply_training_impulsive_palam_effects(target, source, derived)
        self._apply_training_achieve_palam_effects(target, source, derived)
        self._apply_training_pain_palam_effects(target, source, derived)
        self._apply_training_poison_palam_effects(target, source, derived)
        self._apply_training_dirty_palam_effects(target, source, derived)
        self._add_training_palam_gain(derived, 3, int(source.get(10, 0)))
        self._add_training_palam_gain(derived, 5, int(source.get(11, 0)))
        self._apply_training_flasher_palam_effects(target, source, derived)
        self._apply_training_submit_palam_effects(target, source, derived)
        self._apply_training_deviate_palam_effects(target, source, derived)
        self._add_training_palam_gain(derived, 11, int(source.get(15, 0)))
        self._add_training_palam_gain(derived, 4, int(source.get(16, 0)))
        return derived






    def _apply_training_deviate_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(14, 0))
        if int(target.talent.get(23, 0)) != 0:
            source_value = self._scale_value(source_value, 0.30)
        if int(target.talent.get(24, 0)) != 0:
            source_value = self._scale_value(source_value, 3.00)
        source[14] = source_value
        if source_value == 0:
            return
        hatred_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [1.00, 0.80, 0.70, 0.40, 0.20, 0.00]))
        hatred_value = self._scale_value(hatred_value, self._level_value(int(target.abl.get(11, 0)), [0.90, 0.70, 0.50, 0.30, 0.10, 0.00]))
        self._add_training_palam_gain(palam_delta, 11, hatred_value)






    def _apply_training_dirty_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(8, 0))
        if source_value == 0:
            return
        hatred_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.60, 0.40, 0.25, 0.10, 0.00, 0.00]))
        discomfort_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [1.00, 0.80, 0.60, 0.30, 0.10, 0.00]))
        self._add_training_palam_gain(palam_delta, 11, hatred_value)
        self._add_training_palam_gain(palam_delta, 12, discomfort_value)






    def _apply_training_easy_fall_checks(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(73, 0)) == 0:
            return
        self._apply_training_easy_fall_source_ability(target, source, 0, 0, dull_talent_id=101)
        self._apply_training_easy_fall_source_ability(target, source, 1, 2, dull_talent_id=103)
        self._apply_training_easy_fall_source_ability(target, source, 2, 3, dull_talent_id=105)
        self._apply_training_easy_fall_source_ability(target, source, 14, 1, dull_talent_id=107)
        self._apply_training_easy_fall_simple_ability(target, source, 4, 10)
        self._apply_training_easy_fall_simple_ability(target, source, 5, 11)
        self._apply_training_easy_fall_simple_ability(target, source, 7, 12)
        self._apply_training_easy_fall_gated_ability(target, source, 6, 16, gate_ability_id=0)
        self._apply_training_easy_fall_gated_ability(target, source, 8, 17, gate_ability_id=1)
        self._apply_training_easy_fall_gated_ability(target, source, 9, 21, gate_ability_id=11)
        self._apply_training_easy_fall_exp_ability(target, 40, 22, gate_ability_id=11)
        self._apply_training_easy_fall_exp_ability(target, 41, 23, gate_ability_id=11)






    def _apply_training_easy_fall_exp_ability(
        self,
        target: Character,
        exp_id: int,
        ability_id: int,
        *,
        gate_ability_id: int,
    ) -> None:
        value = int(target.exp.get(exp_id, 0))
        gate_level = int(target.abl.get(gate_ability_id, 0))
        thresholds = (1, 5, 20, 40, 100)
        self._apply_training_easy_fall_thresholds(target, ability_id, value, thresholds, gate_level=gate_level)






    def _apply_training_easy_fall_gated_ability(
        self,
        target: Character,
        source: Dict[int, int],
        source_id: int,
        ability_id: int,
        *,
        gate_ability_id: int,
    ) -> None:
        value = int(source.get(source_id, 0))
        gate_level = int(target.abl.get(gate_ability_id, 0))
        thresholds = (1, 30, 60, 200, 1000)
        self._apply_training_easy_fall_thresholds(target, ability_id, value, thresholds, gate_level=gate_level)






    def _apply_training_easy_fall_simple_ability(
        self,
        target: Character,
        source: Dict[int, int],
        source_id: int,
        ability_id: int,
    ) -> None:
        thresholds = (1, 30, 60, 200, 1000)
        self._apply_training_easy_fall_thresholds(target, ability_id, int(source.get(source_id, 0)), thresholds)






    def _apply_training_easy_fall_source_ability(
        self,
        target: Character,
        source: Dict[int, int],
        source_id: int,
        ability_id: int,
        *,
        dull_talent_id: int,
    ) -> None:
        if int(target.talent.get(dull_talent_id, 0)) & 2:
            return
        self._apply_training_easy_fall_simple_ability(target, source, source_id, ability_id)






    def _apply_training_easy_fall_thresholds(
        self,
        target: Character,
        ability_id: int,
        value: int,
        thresholds: tuple[int, int, int, int, int],
        *,
        gate_level: Optional[int] = None,
    ) -> None:
        current = int(target.abl.get(ability_id, 0))
        for level, threshold in enumerate(thresholds, start=1):
            if value > threshold and current < level and (gate_level is None or gate_level >= level):
                target.abl[ability_id] = level
                current = level






    def _apply_training_flasher_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        base_source = int(source.get(12, 0))
        if int(target.talent.get(35, 0)) != 0:
            base_source = self._scale_value(base_source, 2.0)
        elif int(target.talent.get(36, 0)) != 0:
            base_source = self._scale_value(base_source, 0.5)
        base_source += max(0, int(source.get(3, 0))) // 2
        source[12] = base_source
        if base_source == 0:
            return
        lust_value = self._scale_value(base_source, self._level_value(int(target.abl.get(17, 0)), [0.00, 0.10, 0.20, 0.40, 0.60, 0.80, 1.00]))
        shame_value = self._scale_value(base_source, self._get_training_flasher_shame_scale(target))
        hatred_value = self._scale_value(base_source, self._level_value(int(target.abl.get(17, 0)), [1.00, 0.90, 0.70, 0.50, 0.30, 0.10, 0.00]))
        hatred_value = self._scale_value(hatred_value, self._level_value(int(target.abl.get(10, 0)), [0.50, 0.30, 0.15, 0.05, 0.00, 0.00]))
        self._add_training_palam_gain(palam_delta, 5, lust_value)
        self._add_training_palam_gain(palam_delta, 8, shame_value)
        self._add_training_palam_gain(palam_delta, 11, hatred_value)






    def _apply_training_heat_accumulation(self, target: Character) -> None:
        if int(self.interpreter.vars.get_flag(75, 0)) != 0:
            return
        if int(target.talent.get(271, 0)) != 0:
            return
        self._update_training_heat_counter(target, 3, 81)
        self._update_training_heat_counter(target, 5, 82)






    def _apply_training_impulsive_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(4, 0))
        if source_value == 0:
            return
        learn_value = self._scale_value(source_value, self._level_value(int(target.abl.get(16, 0)), [0.60, 0.80, 1.00, 1.20, 1.40, 1.70, 2.00]))
        learn_value = self._scale_value(learn_value, self._level_value(int(target.abl.get(13, 0)), [0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30]))
        depression_value = 0
        if int(target.talent.get(32, 0)) != 0 or int(target.talent.get(34, 0)) != 0:
            depression_value = source_value // 5
            depression_value = self._scale_value(depression_value, self._level_value(int(target.abl.get(16, 0)), [1.80, 1.30, 0.90, 0.70, 0.50, 0.30, 0.10]))
        self._add_training_palam_gain(palam_delta, 7, learn_value)
        self._add_training_palam_gain(palam_delta, 13, depression_value)






    def _apply_training_love_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(3, 0))
        if source_value == 0:
            return
        obedience_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.10, 0.25, 0.40, 0.60, 0.80, 1.00, 1.20]))
        obedience_value = self._scale_value(obedience_value, self._level_value(int(target.abl.get(16, 0)), [0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30]))
        lust_value = self._scale_value(source_value, self._level_value(int(target.abl.get(11, 0)), [0.00, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]))
        self._add_training_palam_gain(palam_delta, 4, obedience_value)
        self._add_training_palam_gain(palam_delta, 5, lust_value)






    def _apply_training_masochism_experience(
        self,
        target: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> None:
        pleasure_total = sum(int(source.get(idx, 0)) for idx in (0, 1, 2, 14))
        if pleasure_total == 0:
            pleasure_total = int(source.get(5, 0))
        pain_value = int(source.get(9, 0))
        gain = self._get_training_pain_pleasure_exp_gain(pleasure_total, pain_value)
        if gain <= 0:
            return
        exp_delta[30] = exp_delta.get(30, 0) + gain
        self._scale_training_source_if_present(source, 11, self._get_training_pain_pleasure_hatred_scale(pleasure_total, pain_value))






    def _apply_training_master_affection_gain(self, target: Character, player: Character, master_bonus: int) -> None:
        gain = self._get_training_master_affection_gain(target, player, master_bonus)
        if gain <= 0:
            return
        target.cflag[2] = int(target.cflag.get(2, 0)) + gain






    def _apply_training_master_followup(self, target: Character, source: Dict[int, int]) -> None:
        player = self._get_player()
        if player is None:
            return
        orgasm_count = self._count_training_orgasm_channels(source)
        ejaculation_count = self._get_training_master_ejaculation_count(player, source)
        self._apply_training_master_orgasm_experience(player, orgasm_count)
        if self._is_training_master_affection_blocked(target):
            return
        master_bonus = self._get_training_master_bonus_score(target, player, source, orgasm_count, ejaculation_count)
        self._apply_training_master_affection_gain(target, player, master_bonus)






    def _apply_training_master_orgasm_experience(self, player: Character, orgasm_count: int) -> None:
        if orgasm_count <= 0:
            return
        player.exp[3] = int(player.exp.get(3, 0)) + orgasm_count






    def _apply_training_milk_followup(
        self,
        target: Character,
        losebase: Dict[int, int],
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> tuple[Dict[int, int], Dict[int, int]]:
        if int(target.talent.get(130, 0)) == 0:
            return losebase, source
        milk_gain = self._get_training_milk_gain(target, source)
        target.base[3] = int(target.base.get(3, 0)) + milk_gain
        current = int(target.base.get(3, 0))
        gauge_max = max(1, int(target.maxbase.get(3, 0)))
        if current <= gauge_max:
            return losebase, source
        adjusted_losebase = dict(losebase)
        adjusted_source = dict(source)
        milk_exp = int(target.exp.get(54, 0))
        if current > gauge_max * 2:
            adjusted_losebase[0] = int(adjusted_losebase.get(0, 0)) + 20
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 100
            source12, source13 = self._get_training_milk_heavy_source_bonus(milk_exp)
            exp_delta[54] = exp_delta.get(54, 0) + 2
            if milk_exp == 0:
                exp_delta[50] = exp_delta.get(50, 0) + 1
            target.base[3] = max(0, current - gauge_max * 2)
        else:
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 40
            source12, source13 = self._get_training_milk_light_source_bonus(milk_exp)
            exp_delta[54] = exp_delta.get(54, 0) + 1
            if milk_exp == 0:
                exp_delta[50] = exp_delta.get(50, 0) + 1
            target.base[3] = max(0, current - gauge_max)
        if target.base[3] >= gauge_max:
            target.base[3] = gauge_max - 1
        adjusted_source[12] = int(adjusted_source.get(12, 0)) + source12
        adjusted_source[13] = int(adjusted_source.get(13, 0)) + source13
        target.stain[5] = int(target.stain.get(5, 0)) | 16
        return adjusted_losebase, adjusted_source






    def _apply_training_omorashi_followup(self, target: Character, source: Dict[int, int]) -> None:
        orgasm_score = self._get_training_omorashi_orgasm_score(source)
        if orgasm_score <= 0:
            return
        gain = self._get_training_omorashi_exp_gain(target, orgasm_score)
        if gain <= 0:
            return
        target.exp[31] = int(target.exp.get(31, 0)) + gain
        if int(target.equipt.get(22, 0)) != 0 and int(target.talent.get(57, 0)) == 0:
            target.equipt[22] = 0
        target.stain[2] = int(target.stain.get(2, 0)) | 32
        target.stain[3] = int(target.stain.get(3, 0)) | 32
        self._apply_onesho_cloth_soiling(target)






    def _apply_training_pain_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(6, 0))
        if source_value == 0:
            return
        fear_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.80, 0.70, 0.55, 0.45, 0.35, 0.25, 0.15]))
        hatred_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.80, 0.60, 0.50, 0.40, 0.20, 0.05, 0.00]))
        lust_value = self._scale_value(hatred_value, self._level_value(int(target.abl.get(21, 0)), [0.00, 0.10, 0.20, 0.30, 0.45, 0.60, 0.75]))
        player = self._get_player()
        if player is not None:
            lust_value = self._scale_value(lust_value, self._level_value(int(player.abl.get(20, 0)), [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60]))
            if int(player.talent.get(83, 0)) != 0:
                lust_value = self._scale_value(lust_value, 2.0)
        if int(target.talent.get(88, 0)) != 0:
            lust_value = self._scale_value(lust_value, 2.0)
        pain_value = source_value
        if int(target.talent.get(40, 0)) != 0:
            pain_value = self._scale_value(pain_value, 1.5)
            lust_value = self._scale_value(lust_value, 4.0)
        elif int(target.talent.get(41, 0)) != 0:
            pain_value = self._scale_value(pain_value, 0.8)
            lust_value = self._scale_value(lust_value, 0.8)
        self._add_training_palam_gain(palam_delta, 9, pain_value)
        self._add_training_palam_gain(palam_delta, 10, fear_value)
        self._add_training_palam_gain(palam_delta, 11, hatred_value)
        self._add_training_palam_gain(palam_delta, 5, lust_value)






    def _apply_training_poison_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(7, 0))
        if source_value == 0:
            return
        obedience_value = self._scale_value(source_value, self._level_value(int(target.abl.get(11, 0)), [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]))
        lust_value = self._scale_value(source_value, self._level_value(int(target.abl.get(11, 0)), [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]))
        self._add_training_palam_gain(palam_delta, 4, obedience_value)
        self._add_training_palam_gain(palam_delta, 5, lust_value)






    def _apply_training_service_pleasure_experience(
        self,
        target: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> None:
        service_value = int(source.get(7, 0))
        if service_value < 100:
            return
        pleasure_total = sum(int(source.get(idx, 0)) for idx in (0, 1, 2, 14))
        if pleasure_total <= 0:
            return
        scaled = pleasure_total
        if service_value < 300:
            scaled *= 1
        elif service_value < 700:
            scaled *= 2
        elif service_value < 1500:
            scaled *= 3
        else:
            scaled *= 4
        gain = self._get_training_derived_exp_gain(scaled)
        if gain <= 0:
            return
        exp_delta[21] = exp_delta.get(21, 0) + gain
        self._scale_training_source_if_present(source, 11, self._get_training_derived_scale(scaled, (0.65, 0.70, 0.75, 0.80, 0.85, 0.90)))
        self._scale_training_source_if_present(source, 12, self._get_training_derived_scale(scaled, (0.30, 0.40, 0.50, 0.60, 0.70, 0.80)))






    def _apply_training_source_anal_mania_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(77, 0)) != 0:
            self._scale_training_source_if_present(source, 2, 1.5)
            self._scale_training_source_if_present(source, 5, 1.2)
            self._scale_training_source_if_present(source, 6, 1.2)
            self._scale_training_source_if_present(source, 13, 0.5)
        if int(target.talent.get(233, 0)) != 0:
            self._scale_training_source_if_present(source, 2, 2.0)






    def _apply_training_source_autotrain_count_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        count = int(target.cflag.get(667, 0))
        scale = self._get_training_source_autotrain_count_scale(count)
        if scale == 1.0:
            return
        for idx in range(18):
            if idx >= 11 and idx != 14:
                continue
            self._scale_training_source_if_present(source, idx, scale)






    def _apply_training_source_blind_faith_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(86, 0)) == 0:
            return
        if int(source.get(6, 0)) != 0:
            source[6] = self._scale_value(int(source.get(6, 0)), 4.0)
        if int(source.get(11, 0)) != 0:
            source[11] = self._scale_value(int(source.get(11, 0)), 0.5)






    def _apply_training_source_breast_mania_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(78, 0)) != 0:
            self._scale_training_source_if_present(source, 14, 1.5)
            self._scale_training_source_if_present(source, 5, 1.2)
            self._scale_training_source_if_present(source, 13, 0.5)
        if int(target.talent.get(231, 0)) != 0:
            self._scale_training_source_if_present(source, 14, 2.0)






    def _apply_training_source_clit_mania_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(74, 0)) != 0:
            self._scale_training_source_if_present(source, 0, 1.5)
            self._scale_training_source_if_present(source, 5, 1.2)
            self._scale_training_source_if_present(source, 13, 0.5)
        if int(target.talent.get(230, 0)) != 0:
            self._scale_training_source_if_present(source, 0, 2.0)






    def _apply_training_source_devotion_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(63, 0)) != 0:
            self._scale_training_source_if_present(source, 6, 2.0)






    def _apply_training_source_followup_effects(
        self,
        target: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> None:
        self._apply_training_service_pleasure_experience(target, source, exp_delta)
        self._apply_training_anal_pleasure_experience(target, source, exp_delta)
        self._apply_training_masochism_experience(target, source, exp_delta)






    def _apply_training_source_heat_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(271, 0)) == 0:
            return
        for idx in (5, 3):
            if int(source.get(idx, 0)) != 0:
                source[idx] = self._scale_value(int(source.get(idx, 0)), 1.2)






    def _apply_training_source_learning_speed_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(50, 0)) != 0:
            self._scale_training_source_if_present(source, 7, 2.0)
        if int(target.talent.get(51, 0)) != 0:
            self._scale_training_source_if_present(source, 7, 0.5)






    def _apply_training_source_love_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(85, 0)) == 0:
            return
        self._scale_training_source_if_present(source, 4, 1.2)
        self._scale_training_source_if_present(source, 6, 2.0)
        self._scale_training_source_if_present(source, 11, 0.5)
        self._scale_training_source_if_present(source, 12, 0.5)






    def _apply_training_source_player_intimidation_modifiers(self, source: Dict[int, int]) -> None:
        player = self._get_player()
        if player is None or int(player.talent.get(93, 0)) == 0:
            return
        self._scale_training_source_if_present(source, 10, 2.0)
        self._scale_training_source_if_present(source, 11, 0.5)






    def _apply_training_source_pleasure_acceptance_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(70, 0)) != 0:
            self._scale_training_source_if_present(source, 5, 2.0)
        if int(target.talent.get(71, 0)) != 0:
            self._scale_training_source_if_present(source, 5, 0.5)






    def _apply_training_source_rebellion_mark_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        rebellion_level = int(target.mark.get(3, 0))
        if rebellion_level == 3:
            self._scale_training_source_if_present(source, 4, 0.1)
        elif rebellion_level == 2:
            self._scale_training_source_if_present(source, 4, 0.4)
        elif rebellion_level == 1:
            self._scale_training_source_if_present(source, 4, 0.7)






    def _apply_training_source_sex_hero_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(272, 0)) == 0:
            return
        for idx in (0, 1, 2, 14, 5):
            if int(source.get(idx, 0)) != 0:
                source[idx] = self._scale_value(int(source.get(idx, 0)), 1.2)






    def _apply_training_source_special_sex_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        self._apply_training_source_clit_mania_modifiers(target, source)
        self._apply_training_source_vagina_mania_modifiers(target, source)
        self._apply_training_source_anal_mania_modifiers(target, source)
        self._apply_training_source_breast_mania_modifiers(target, source)






    def _apply_training_source_talent_modifiers(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        adjusted = dict(source)
        self._apply_training_source_special_sex_modifiers(target, adjusted)
        self._apply_training_source_sex_hero_modifiers(target, adjusted)
        self._apply_training_source_learning_speed_modifiers(target, adjusted)
        self._apply_training_source_devotion_modifiers(target, adjusted)
        self._apply_training_source_pleasure_acceptance_modifiers(target, adjusted)
        self._apply_training_source_love_modifiers(target, adjusted)
        self._apply_training_source_blind_faith_modifiers(target, adjusted)
        self._apply_training_source_player_intimidation_modifiers(adjusted)
        self._apply_training_source_heat_modifiers(target, adjusted)
        self._apply_training_source_rebellion_mark_modifiers(target, adjusted)
        self._apply_training_source_autotrain_count_modifiers(target, adjusted)
        return adjusted






    def _apply_training_source_vagina_mania_modifiers(self, target: Character, source: Dict[int, int]) -> None:
        if int(target.talent.get(75, 0)) != 0:
            self._scale_training_source_if_present(source, 1, 1.5)
            self._scale_training_source_if_present(source, 4, 1.2)
            self._scale_training_source_if_present(source, 5, 1.2)
            self._scale_training_source_if_present(source, 13, 0.5)
        if int(target.talent.get(232, 0)) != 0:
            self._scale_training_source_if_present(source, 1, 1.5)






    def _apply_training_submit_palam_effects(self, target: Character, source: Dict[int, int], palam_delta: Dict[int, int]) -> None:
        source_value = int(source.get(13, 0))
        if source_value == 0:
            return
        depression_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.12, 0.10, 0.05, 0.02, 0.00, 0.00, 0.00, 0.00]))
        submission_value = self._scale_value(source_value, self._level_value(int(target.abl.get(10, 0)), [0.50, 0.80, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50]))
        submission_value = self._scale_value(submission_value, self._level_value(int(target.abl.get(39, 0)), [1.00, 1.10, 1.20, 1.50, 2.00, 3.00, 4.00]))
        self._add_training_palam_gain(palam_delta, 13, depression_value)
        self._add_training_palam_gain(palam_delta, 6, submission_value)






    def _apply_training_target_ejaculation_followup(
        self,
        target: Character,
        losebase: Dict[int, int],
        source: Dict[int, int],
        exp_delta: Dict[int, int],
    ) -> tuple[Dict[int, int], Dict[int, int]]:
        if int(target.talent.get(121, 0)) == 0 and int(target.talent.get(122, 0)) == 0:
            return losebase, source
        adjusted_stimulation = self._get_training_target_ejaculation_gain(target, source)
        current = int(target.base.get(2, 0)) + adjusted_stimulation
        target.base[2] = current
        gauge_max = max(1, int(target.maxbase.get(2, 0)))
        if current <= gauge_max:
            if int(target.talent.get(135, 0)) != 0 and int(target.base.get(2, 0)) > 2000:
                target.base[2] = 2000
            return losebase, source
        adjusted_losebase = dict(losebase)
        adjusted_source = dict(source)
        ejac_exp = int(target.exp.get(3, 0))
        if current > gauge_max * 2:
            adjusted_losebase[0] = int(adjusted_losebase.get(0, 0)) + 20
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 100
            source12, source13 = self._get_training_target_ejac_heavy_source_bonus(ejac_exp)
            exp_delta[20] = exp_delta.get(20, 0) + 1
            exp_delta[3] = exp_delta.get(3, 0) + 2
            if ejac_exp == 0 and int(target.talent.get(122, 0)) == 0:
                exp_delta[50] = exp_delta.get(50, 0) + 1
            self._apply_training_target_immature_ejaculation_penalty(target, adjusted_losebase, heavy=True)
            target.base[2] = max(0, current - gauge_max * 2)
        else:
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 40
            source12, source13 = self._get_training_target_ejac_light_source_bonus(ejac_exp)
            exp_delta[3] = exp_delta.get(3, 0) + 1
            if ejac_exp == 0 and int(target.talent.get(122, 0)) == 0:
                exp_delta[50] = exp_delta.get(50, 0) + 1
            self._apply_training_target_immature_ejaculation_penalty(target, adjusted_losebase, heavy=False)
            target.base[2] = max(0, current - gauge_max)
        if target.base[2] >= gauge_max:
            target.base[2] = gauge_max - 1
        adjusted_source[12] = int(adjusted_source.get(12, 0)) + source12
        adjusted_source[13] = int(adjusted_source.get(13, 0)) + source13
        target.stain[2] = int(target.stain.get(2, 0)) | 4
        return adjusted_losebase, adjusted_source






    def _apply_training_target_immature_ejaculation_penalty(
        self,
        target: Character,
        losebase: Dict[int, int],
        *,
        heavy: bool,
    ) -> None:
        if int(target.talent.get(135, 0)) == 0:
            return
        target.maxbase[0] = max(600, int(target.maxbase.get(0, 0)) - 10)
        mp_loss = 30 if heavy else 10
        target.maxbase[1] = max(100, int(target.maxbase.get(1, 0)) - mp_loss)
        losebase[0] = int(losebase.get(0, 0)) + (50 if heavy else 10)
        losebase[1] = int(losebase.get(1, 0)) + (100 if heavy else 40)






    def _apply_training_wormbirth_followup(
        self,
        target: Character,
        losebase: Dict[int, int],
        source: Dict[int, int],
    ) -> tuple[Dict[int, int], Dict[int, int]]:
        if int(target.talent.get(190, 0)) == 0 and int(target.talent.get(191, 0)) == 0:
            return losebase, source
        pleasure_total = sum(int(source.get(idx, 0)) for idx in (0, 1, 2, 14))
        if pleasure_total <= 0:
            return losebase, source
        adjusted = pleasure_total
        if int(target.talent.get(20, 0)) != 0:
            adjusted //= 2
        if int(target.talent.get(70, 0)) != 0:
            adjusted = self._scale_value(adjusted, 1.2)
        if int(target.talent.get(76, 0)) != 0:
            adjusted = self._scale_value(adjusted, 1.1)
        if int(target.talent.get(71, 0)) != 0:
            adjusted = self._scale_value(adjusted, 0.8)
        if int(target.equipt.get(21, 0)) != 0:
            adjusted *= 2
        if adjusted <= 10000:
            return losebase, source
        adjusted_losebase = dict(losebase)
        adjusted_source = dict(source)
        birth_exp = int(target.exp.get(60, 0))
        if adjusted > 25000:
            adjusted_losebase[0] = int(adjusted_losebase.get(0, 0)) + 20
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 100
            source12, source13 = self._get_training_wormbirth_heavy_source_bonus(birth_exp)
            target.exp[60] = birth_exp + 2
        else:
            adjusted_losebase[1] = int(adjusted_losebase.get(1, 0)) + 40
            source12, source13 = self._get_training_wormbirth_light_source_bonus(birth_exp)
            target.exp[60] = birth_exp + 1
        adjusted_source[12] = int(adjusted_source.get(12, 0)) + source12
        adjusted_source[13] = int(adjusted_source.get(13, 0)) + source13
        return adjusted_losebase, adjusted_source






    def _apply_training_zero_energy_modifiers(
        self,
        target: Character,
        losebase: Dict[int, int],
        source: Dict[int, int],
    ) -> tuple[Dict[int, int], Dict[int, int]]:
        if int(target.base.get(1, 0)) > 0:
            return losebase, source
        adjusted_losebase = dict(losebase)
        adjusted_source = dict(source)
        for idx in (3, 4, 5, 7, 9, 13):
            if int(adjusted_source.get(idx, 0)) != 0:
                adjusted_source[idx] = int(adjusted_source.get(idx, 0)) // 2
        adjusted_losebase[0] = int(adjusted_losebase.get(0, 0)) * 2 + 80
        return adjusted_losebase, adjusted_source






    def _build_train_command_2_base_source(self, target: Character) -> tuple[Dict[str, int], Dict[int, int]]:
        losebase = {0: 20, 1: 100}
        source = {12: 850, 14: 200}
        source[2] = self._level_value(target.abl.get(3, 0), [20, 75, 300, 700, 1100, 1500])
        source[13] = self._level_value(target.abl.get(3, 0), [300, 350, 400, 650, 1000, 1500])
        return losebase, source






    def _build_train_command_3_base_source(self, target: Character) -> tuple[Dict[int, int], Dict[int, int]]:
        losebase = {0: 5, 1: 50}
        source = {14: 400}
        if target.equipt.get(53, 0):
            source[10] = 50
            source[11] = 100
        source[0] = self._level_value(target.abl.get(0, 0), [15, 50, 300, 700, 1100, 1600])
        source[12] = self._level_value(target.abl.get(0, 0), [2000, 2300, 2600, 2900, 3200, 3500])
        source[13] = self._level_value(target.abl.get(0, 0), [500, 800, 1200, 1900, 2500, 3000])
        source[17] = self._level_value(target.abl.get(1, 0), [15, 50, 300, 700, 1100, 1600])
        return losebase, source






    def _build_train_command_3_exp_delta(self, target: Character, player: Optional[Character]) -> Dict[int, int]:
        exp_delta = {10: 2 if target.equipt.get(53, 0) or target.equipt.get(54, 0) else 1, 11: 2 if target.equipt.get(53, 0) or target.equipt.get(54, 0) else 1}
        if (target.equipt.get(53, 0) or target.equipt.get(54, 0)) and target.cflag.get(3, 0) == 0:
            exp_delta[50] = 1
            target.cflag[3] = 1
        return exp_delta






    def _build_train_command_3_label(self, target: Character) -> str:
        label_parts: List[str] = []
        if target.equipt.get(53, 0):
            label_parts.append("公开")
        if target.equipt.get(54, 0):
            label_parts.append("野外")
        if target.equipt.get(18, 0):
            label_parts.append("沐浴")
        if target.equipt.get(11, 0) and target.equipt.get(13, 0):
            label_parts.append("二穴振动")
        elif target.equipt.get(11, 0):
            label_parts.append("振动")
        elif target.equipt.get(13, 0):
            label_parts.append("后庭振动")
        label_parts.append("手淫" if any(target.equipt.get(flag, 0) for flag in [11, 13, 18, 53, 54]) else "自慰")
        return "".join(label_parts)






    def _build_train_command_56_base_values(self, target: Character) -> tuple[Dict[int, int], Dict[int, int], int, bool]:
        submission_level = target.abl.get(10, 0)
        has_love = target.talent.get(85, 0) == 1
        if has_love and submission_level >= 5:
            losebase = {0: 0, 1: 10}
        elif has_love:
            losebase = {0: 10, 1: 10}
        elif submission_level >= 3:
            losebase = {0: 10, 1: 30}
        else:
            losebase = {0: 20, 1: 50}

        source: Dict[int, int] = {}
        if has_love:
            source[16] = 60
        elif submission_level >= 5:
            source[15] = 10
            source[16] = 50
        elif submission_level >= 4:
            source[15] = 20
            source[16] = 40
        elif submission_level >= 3:
            source[15] = 30
            source[16] = 30
        elif submission_level >= 2:
            source[15] = 40
            source[16] = 20
        else:
            source[15] = 50
            source[16] = 10

        return losebase, source, submission_level, has_love






    def _build_train_command_56_exp_delta(self, target: Character, player: Optional[Character], palam_level: int, has_love: bool) -> Dict[int, int]:
        exp_delta: Dict[int, int] = {}
        talk_exp = self._level_value(palam_level, [1, 1, 2, 2, 3])
        if has_love:
            talk_exp *= 2
        if player is not None:
            talk_exp += self._level_value(player.abl.get(15, 0), [0, 1, 1, 2, 2, 3])
        exp_delta[73] = talk_exp
        if target.abl.get(71, 0) > 1 and talk_exp > 2:
            exp_delta[71] = talk_exp + target.abl.get(71, 0) - 3
        if target.abl.get(72, 0) > 1 and target.equipt.get(54, 0) > 0 and talk_exp > 2:
            exp_delta[72] = talk_exp + target.abl.get(72, 0) - 3
        return exp_delta






    def _build_train_command_56_source_values(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        palam_level = self._get_palam_level(target.palam.get(4, 0))
        source[16] += self._level_value(palam_level, [10, 30, 60, 100, 150])
        source[16] += self._level_value(target.abl.get(16, 0), [0, 20, 40, 70, 110, 150])
        source[16] = self._scale_value(source[16], self._level_value(target.abl.get(15, 0), [90, 100, 110, 120, 130, 140]) / 100.0)

        if target.equipt.get(53, 0):
            source[12] = 1000
            source[4] = self._level_value(target.abl.get(17, 0), [0, 10, 50, 100, 200, 400])
            if target.abl.get(17, 0) >= 4:
                source[10] = source.get(10, 0) + 50
            if target.abl.get(17, 0) >= 5:
                source[10] = source.get(10, 0) + 50
            if target.talent.get(28, 0):
                source[4] = self._scale_value(source[4], 1.2)
                source[12] = self._scale_value(source[12], 1.2)
            if target.talent.get(89, 0):
                source[4] = self._scale_value(source[4], 1.6)
                source[12] = self._scale_value(source[12], 1.6)
                source[10] = self._scale_value(source.get(10, 0), 1.6)
        return source






    def _build_train_command_62_base_values(self, target: Character) -> tuple[Dict[int, int], Dict[int, int]]:
        losebase = {0: 40, 1: 220}
        source = {
            3: 1500,
            10: self._level_value(target.abl.get(11, 0), [200, 400, 750, 1200, 1700, 2500]),
            13: self._level_value(target.abl.get(11, 0), [1600, 1900, 2300, 2700, 3100, 3500]),
            14: 800,
        }
        source[3] = self._scale_value(source[3], self._level_value(target.abl.get(16, 0), [10, 40, 70, 100, 160, 200]) / 100.0)
        source[10] = self._scale_value(source[10], self._level_value(target.abl.get(16, 0), [50, 80, 100, 150, 200, 250]) / 100.0)
        return losebase, source






    def _build_train_command_62_exp_delta(
        self,
        target: Character,
        player: Character,
        assistant: Character,
        source: Dict[int, int],
    ) -> Dict[int, int]:
        exp_delta: Dict[int, int] = {}
        self._apply_assistant_sex_witness_effects(target, assistant, exp_delta, source)
        self._apply_sex_virgin_break(assistant, player, exp_delta, submission_floor=2)
        self._apply_vaginal_sex_shared_effects(player, assistant)
        self._apply_sex_ejaculation_to_receiver(player, assistant, exp_delta, source, assistant, 1)
        self._add_same_sex_exp(exp_delta, player, assistant, female_value=10, male_value=10)
        self._add_love_exp(exp_delta, assistant, 2)
        return exp_delta






    def _build_train_command_62_score(self, target: Character, player: Character, assistant: Character) -> int:
        score = self._get_common_order_score(target, player)
        score += target.abl.get(11, 0) * 2
        score += target.abl.get(16, 0) * 4
        score += target.mark.get(1, 0) * 2
        score += self._get_palam_level(target.palam.get(5, 0)) * 2
        if target.talent.get(35, 0):
            score -= 1
        if target.talent.get(63, 0):
            score += 6
        if target.talent.get(85, 0):
            score += 5
        if assistant.exp.get(0, 0) == 0:
            score -= 15
        return score






    def _build_train_command_65_score(self, target: Character, player: Optional[Character], assistant: Character) -> int:
        score = self._get_common_order_score(target, player)
        score += target.abl.get(11, 0) * 2
        score += target.abl.get(16, 0) * 4
        score += target.mark.get(1, 0) * 2
        score += self._get_palam_level(target.palam.get(5, 0)) * 2
        if target.talent.get(35, 0):
            score -= 1
        if target.talent.get(63, 0):
            score += 6
        if target.talent.get(70, 0):
            score += 2
        if target.talent.get(71, 0):
            score -= 2
        if target.talent.get(79, 0) and assistant.talent.get(122, 0) == 0:
            score -= 5
        if target.talent.get(85, 0):
            score += 5
        return score






    def _build_train_command_65_source(self, target: Character) -> Dict[int, int]:
        source = {
            0: self._level_value(target.abl.get(16, 0), [800, 1400, 2000, 2500, 2900, 3200]),
            4: self._level_value(target.abl.get(16, 0), [1600, 1900, 2300, 2700, 3100, 3500]),
            5: self._level_value(target.abl.get(16, 0), [200, 400, 750, 1150, 1750, 2500]),
            13: 1500,
            14: 800,
        }
        source[0] = self._scale_value(source[0], 0.5)
        technique_scale = self._level_value(target.abl.get(12, 0), [50, 80, 100, 150, 200, 250]) / 100.0
        source[4] = self._scale_value(source[4], technique_scale)
        source[5] = self._scale_value(source[5], technique_scale)
        return source






    def _build_train_command_6_dirty_score(self, target: Character, player: Optional[Character]) -> int:
        dirty_score = 7 if target.equipt.get(89, 0) > 0 else self._mouth_stain_score(player)
        if target.talent.get(61, 0):
            dirty_score //= 3
        if target.talent.get(62, 0):
            dirty_score *= 2
        return dirty_score // 2






    def _build_train_video_equip_mask(self, target: Character) -> int:
        equip_mask = 0
        if target.equipt.get(54, 0):
            equip_mask |= 1
        if target.equipt.get(58, 0):
            equip_mask |= 2
        if target.equipt.get(59, 0):
            equip_mask |= 4
        if target.equipt.get(44, 0):
            equip_mask |= 8
        if target.equipt.get(11, 0):
            equip_mask |= 16
        if target.equipt.get(13, 0):
            equip_mask |= 32
        if target.equipt.get(46, 0):
            equip_mask |= 64
        if target.equipt.get(89, 0):
            equip_mask |= 128
        if target.equipt.get(90, 0):
            equip_mask |= 256
        if target.equipt.get(18, 0):
            equip_mask |= 512
        return equip_mask






    def _build_train_video_title(self, target: Character) -> str:
        parts: List[str] = []
        for offset in range(10):
            command_id = int(target.cflag.get(460 + offset, 0))
            if command_id > 0:
                parts.append(self._get_train_command_name(command_id))
        if not parts:
            return f"{target.name} 的录像"
        preview = " / ".join(parts[:3])
        if len(parts) > 3:
            preview += " ..."
        return f"{target.name} 的录像：{preview}"






    def _calculate_train_video_score(self, target: Character, player: Optional[Character]) -> int:
        weights = {
            0: 80,
            1: 80,
            2: 120,
            3: 500,
            6: 100,
            30: 150,
            40: 100,
            50: 60,
            56: 10,
            62: 800,
            64: 3000,
            65: 1200,
            128: 800,
            129: 900,
            130: 1000,
            131: 1300,
            132: 1400,
            133: 1500,
            134: 1500,
        }
        frame_count = min(int(target.cflag.get(491, 0)), 10)
        if frame_count <= 0:
            return 0

        command_ids: List[int] = []
        for offset in range(frame_count):
            command_id = int(target.cflag.get(460 + offset, 0))
            if command_id > 0:
                command_ids.append(command_id)
        if not command_ids:
            return 0

        score = 0
        for command_id in command_ids:
            score += weights.get(command_id, 100)

        score += len(set(command_ids)) * 50
        score += max(0, int(target.abl.get(17, 0))) * 20

        assistant = self._get_current_assistant()
        if assistant is not None:
            edit_level = int(assistant.abl.get(15, 0))
            if edit_level > 0:
                score += score * edit_level * 5 // 100

        return max(score, 1)






    def _check_train_order(self, score: int, threshold: int, command_name: str) -> bool:
        print(f"执行值 {score} / {threshold}")
        if score >= threshold:
            return True
        print(f"{command_name} 的原作 COM_ORDER 判定未通过。")
        return False






    def _clear_train_video_frames(self, target: Character) -> None:
        for offset in range(10):
            target.cflag[460 + offset] = 0






    def _dispatch_train_command(self, command: str, target: Character, player: Optional[Character]) -> bool:
        handlers = {
            "0": self._execute_train_command_0,
            "1": self._execute_train_command_1,
            "2": self._execute_train_command_2,
            "3": self._execute_train_command_3,
            "4": self._execute_train_command_4,
            "5": self._execute_train_command_5,
            "6": self._execute_train_command_6,
            "7": self._execute_train_command_7,
            "8": self._execute_train_command_8,
            "9": self._execute_train_command_9,
            "10": self._execute_train_command_10,
            "11": self._execute_train_command_11,
            "12": self._execute_train_command_12,
            "13": self._execute_train_command_13,
            "14": self._execute_train_command_14,
            "15": self._execute_train_command_15,
            "16": self._execute_train_command_16,
            "17": self._execute_train_command_17,
            "18": self._execute_train_command_18,
            "19": self._execute_train_command_19,
            "20": self._execute_train_command_20,
            "21": self._execute_train_command_21,
            "22": self._execute_train_command_22,
            "23": self._execute_train_command_23,
            "24": self._execute_train_command_24,
            "25": self._execute_train_command_25,
            "30": self._execute_train_command_30,
            "31": self._execute_train_command_31,
            "32": self._execute_train_command_32,
            "33": self._execute_train_command_33,
            "34": self._execute_train_command_34,
            "35": self._execute_train_command_35,
            "36": self._execute_train_command_36,
            "37": self._execute_train_command_37,
            "38": self._execute_train_command_38,
            "40": self._execute_train_command_40,
            "41": self._execute_train_command_41,
            "42": self._execute_train_command_42,
            "43": self._execute_train_command_43,
            "44": self._execute_train_command_44,
            "45": self._execute_train_command_45,
            "46": self._execute_train_command_46,
            "47": self._execute_train_command_47,
            "48": self._execute_train_command_48,
            "49": self._execute_train_command_49,
            "50": self._execute_train_command_50,
            "51": self._execute_train_command_51,
            "52": self._execute_train_command_52,
            "53": self._execute_train_command_53,
            "54": self._execute_train_command_54,
            "55": self._execute_train_command_55,
            "56": self._execute_train_command_56,
            "57": self._execute_train_command_57,
            "58": self._execute_train_command_58,
            "59": self._execute_train_command_59,
            "60": self._execute_train_command_60,
            "61": self._execute_train_command_61,
            "62": self._execute_train_command_62,
            "63": self._execute_train_command_63,
            "64": self._execute_train_command_64,
            "65": self._execute_train_command_65,
            "66": self._execute_train_command_66,
            "67": self._execute_train_command_67,
            "68": self._execute_train_command_68,
            "69": self._execute_train_command_69,
            "70": self._execute_train_command_70,
            "71": self._execute_train_command_71,
            "72": self._execute_train_command_72,
            "73": self._execute_train_command_73,
            "128": self._execute_train_command_128,
            "129": self._execute_train_command_129,
            "130": self._execute_train_command_130,
            "131": self._execute_train_command_131,
            "132": self._execute_train_command_132,
            "133": self._execute_train_command_133,
            "134": self._execute_train_command_134,
        }

        handler = handlers.get(command)
        if handler is not None:
            handler(target, player)
            return True
        return False



    def _execute_train_command_0(self, target: Character, player: Optional[Character]):
        """爱抚 - 调教者用手和口刺激调教对象的乳房和阴蒂"""
        print("爱抚")
        
        # 基础消耗
        losebase = {0: 5, 1: 50}
        
        # 基础 SOURCE
        source = {
            0: 0,    # 快C (阴蒂感觉)
            17: 0,   # 快B (乳房感觉)
            3: 0,    # 情爱
            4: 60,   # 性行动
            8: 30,   # 不洁
            12: 100, # 露出
        }
        
        # ABL:阴蒂感觉 (ABL:0)
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 20
            source[3] = 25
        elif abl_c == 1:
            source[0] = 100
            source[3] = 50
        elif abl_c == 2:
            source[0] = 500
            source[3] = 80
        elif abl_c == 3:
            source[0] = 1200
            source[3] = 100
        elif abl_c == 4:
            source[0] = 2000
            source[3] = 115
        else:
            source[0] = 2800
            source[3] = 125
        
        # ABL:乳房感觉 (ABL:1)
        abl_b = target.abl.get(1, 0)
        if abl_b == 0:
            source[17] = 15
            source[3] += 25
        elif abl_b == 1:
            source[17] = 50
            source[3] += 50
        elif abl_b == 2:
            source[17] = 300
            source[3] += 80
        elif abl_b == 3:
            source[17] = 700
            source[3] += 100
        elif abl_b == 4:
            source[17] = 1100
            source[3] += 115
        else:
            source[17] = 1600
            source[3] += 125
        
        # 污臭处理
        stain_0 = target.stain.get(0, 0)
        is_assi_play = player is not None and player.cflag.get(1, 0) == 1  # ASSIPLAY
        
        # 检查口的污秽 (爱液、精液、肛门、尿)
        if (stain_0 & 1 or stain_0 & 4 or stain_0 & 8 or stain_0 & 32) and is_assi_play:
            if player is not None:
                abl_assi_10 = player.abl.get(10, 0)
                talent_assi_62 = player.talent.get(62, 0)  # 反感污臭
                talent_assi_64 = player.talent.get(64, 0)  # 不怕脏
                if abl_assi_10 <= 3 and talent_assi_62 and not talent_assi_64:
                    source[8] = 0
                    source[0] //= 2
                    source[3] //= 4
        # 口塞使用中
        elif target.equipt.get(45, 0):
            source[8] = 0
            source[0] //= 2
            source[3] //= 4
        # 初吻未体验
        elif target.cflag.get(16, -1) == -1:
            source[8] = 0
            source[0] //= 2
            source[3] //= 4
        else:
            # 不怕污臭 (TALENT:61)
            if target.talent.get(61, 0):
                source[8] //= 4
            # 反感污臭 (TALENT:62)
            if target.talent.get(62, 0):
                source[8] *= 3
            # 自尊心 (TALENT:15)
            if target.talent.get(15, 0):
                source[8] *= 2
            # 爱慕 (TALENT:85) 且非助手
            if target.talent.get(85, 0) and not is_assi_play:
                source[3] *= 2
                source[8] //= 10
            
            # 主人的口有污秽
            if player is not None and player.stain.get(0, 0):
                source[8] *= 3
                source[8] //= 2
            
            # 污秽移动
            if player is not None:
                target.stain[0] = target.stain.get(0, 0) | player.stain.get(0, 0)
                player.stain[0] = player.stain.get(0, 0) | target.stain.get(0, 0)
        
        # 兽奸情况下提前结束
        if target.equipt.get(89, 0):
            self._finalize_train_effects(target, losebase, source, {}, "COM0 兽奸分支，提前结束")
            return
        
        # 污秽处理 (触手或手指)
        if target.equipt.get(90, 0):  # 触手
            target.stain[1] = target.stain.get(1, 0) | 2 | 4  # V 污秽
            target.stain[5] = target.stain.get(5, 0) | 2 | 4  # B 污秽
        elif player is not None:
            # V 和手指污秽移动
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(1, 0)
            player.stain[1] = player.stain.get(1, 0) | target.stain.get(3, 0)
            # B 和手指污秽移动
            target.stain[5] = target.stain.get(5, 0) | player.stain.get(1, 0)
            player.stain[1] = player.stain.get(1, 0) | target.stain.get(5, 0)
        
        # 经验上升
        exp_delta: Dict[int, int] = {}
        
        # 百合经验 / ホモ经验
        if player is not None:
            target_female = target.talent.get(122, 0) == 0  # 女性
            player_female = player.talent.get(122, 0) == 0
            if target_female and player_female:
                exp_delta[40] = 5  # 百合经验
            elif not target_female and not player_female:
                exp_delta[41] = 5  # ホモ经验
        
        # 爱情经验
        if target.cflag.get(2, 0) >= 1000 and not is_assi_play:
            exp_delta[23] = 2  # 爱情经验
        
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM0 爱抚完成")






    def _execute_train_command_1(self, target: Character, player: Optional[Character]):
        print("舔阴")
        losebase = {0: 5, 1: 50}
        source = {10: 100, 12: 220, 14: 50}
        source[0] = self._level_value(target.abl.get(0, 0), [40, 160, 700, 1500, 2400, 3300])

        if player is not None and (player.talent.get(52, 0) or target.equipt.get(89, 0) > 0):
            source[0] *= 2
            source[16] = source.get(16, 0) + source[0] // 20

        if target.equipt.get(89, 0) > 0:
            self._add_pregnancy_source_amount(target, 5, 1)
            self._finalize_train_effects(target, losebase, source, {}, "按原作 COM1 进入兽奸分支，本次提前结束后续结算。")
            return

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(0, 0)
            player.stain[0] = player.stain.get(0, 0) | target.stain.get(3, 0)

        exp_delta: Dict[int, int] = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=3, male_value=0)
        if player is not None and player.cflag.get(16, -1) == -1:
            player.cflag[16] = 301
            player.cstr[4] = target.name
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM1 的阴蒂感觉表与舌技加成结算当前效果。")






    def _execute_train_command_10(self, target: Character, player: Optional[Character]):
        """振动杖 - 用振动杖刺激阴蒂"""
        print("振动杖")
        losebase = {0: 30, 1: 150}
        source = {12: 120, 14: 400}
        
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 2000
        elif abl_c == 1:
            source[0] = 2500
        elif abl_c == 2:
            source[0] = 3000
        elif abl_c == 3:
            source[0] = 3300
        elif abl_c == 4:
            source[0] = 3600
        else:
            source[0] = 3800
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM10 振动杖完成")

    # ========================================
    # COM11: 蠕虫 (バイブ)
    # ========================================






    def _execute_train_command_11(self, target: Character, player: Optional[Character]):
        """蠕虫 - 用蠕虫刺激阴道"""
        print("蠕虫")
        losebase = {0: 30, 1: 100}
        source = {}
        
        # ABL:私处感觉
        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 80
        elif abl_v == 1:
            source[1] = 250
        elif abl_v == 2:
            source[1] = 600
        elif abl_v == 3:
            source[1] = 1000
        elif abl_v == 4:
            source[1] = 1300
        else:
            source[1] = 1700
        
        # 私处经验调整
        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.4)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.6)
            source[6] = 0
        
        # 润滑调整
        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 400
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM11 蠕虫完成")

    # ========================================
    # COM12: 肛门蠕虫 (アナルワーム)
    # ========================================






    def _execute_train_command_12(self, target: Character, player: Optional[Character]):
        """肛门蠕虫 - 用蠕虫刺激肛门"""
        print("肛门蠕虫")
        losebase = {0: 30, 1: 100}
        source = {}
        
        # ABL:肛门感觉
        abl_a = target.abl.get(3, 0)
        if abl_a == 0:
            source[2] = 80
        elif abl_a == 1:
            source[2] = 250
        elif abl_a == 2:
            source[2] = 600
        elif abl_a == 3:
            source[2] = 1000
        elif abl_a == 4:
            source[2] = 1300
        else:
            source[2] = 1700
        
        # 肛门经验调整
        a_exp_level = self._get_exp_level(target.exp.get(1, 0))
        if a_exp_level == 0:
            source[2] = self._scale_value(source[2], 0.2)
            source[6] = 5500
        elif a_exp_level == 1:
            source[2] = self._scale_value(source[2], 0.6)
            source[6] = 300
        elif a_exp_level == 2:
            source[6] = 50
        elif a_exp_level == 3:
            source[2] = self._scale_value(source[2], 1.2)
            source[6] = 10
        elif a_exp_level == 4:
            source[2] = self._scale_value(source[2], 1.4)
            source[6] = 0
        else:
            source[2] = self._scale_value(source[2], 1.6)
            source[6] = 0
        
        # 润滑调整
        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[2] = self._scale_value(source[2], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[2] = self._scale_value(source[2], 0.4)
            source[6] = source.get(6, 0) + 400
        elif lub_level == 2:
            source[2] = self._scale_value(source[2], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[2] = self._scale_value(source[2], 1.2)
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM12 肛门蠕虫完成")

    # ========================================
    # COM13: 阴蒂夹 (クリキャップ)
    # ========================================






    def _execute_train_command_128(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("正常位・接吻")
        losebase = {0: 60, 1: 120}
        source = self._build_face_sex_base_source(target)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta, love_exp=2, stain_transfer="mouth")
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM128 的简化正常位接吻主干结算当前效果，并记录主角内射来源。")






    def _execute_train_command_129(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("正常位・胸爱抚")
        losebase = {0: 60, 1: 120}
        source = self._build_face_sex_base_source(target)
        self._apply_breast_stimulation_bonus(target, source, rear_mode=False)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM129 的简化正常位胸爱抚变体结算当前效果，并记录主角内射来源。")






    def _execute_train_command_13(self, target: Character, player: Optional[Character]):
        """阴蒂夹 - 用夹子夹住阴蒂"""
        print("阴蒂夹")
        losebase = {0: 20, 1: 80}
        source = {12: 120, 14: 100}
        
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 300
        elif abl_c == 1:
            source[0] = 600
        elif abl_c == 2:
            source[0] = 1200
        elif abl_c == 3:
            source[0] = 1800
        elif abl_c == 4:
            source[0] = 2400
        else:
            source[0] = 3000
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM13 阴蒂夹完成")

    # ========================================
    # COM14: 乳头夹 (ニプルキャップ)
    # ========================================






    def _execute_train_command_130(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("正常位ＳＰ")
        losebase = {0: 70, 1: 130}
        source = self._build_face_sex_base_source(target)
        self._apply_sp_sex_bonus(target, source, rear_mode=False)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta, love_exp=2, stain_transfer="mouth")
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM130 的简化正常位 SP 主干结算当前效果，复用正常位接吻并叠加阴蒂/乳房强化与主角内射来源。")






    def _execute_train_command_131(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("背后位・胸爱抚")
        losebase = {0: 60, 1: 120}
        source = self._build_face_sex_base_source(target)
        self._apply_rear_sex_adjustment(target, source)
        self._apply_breast_stimulation_bonus(target, source, rear_mode=True)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM131 的简化背后位胸爱抚变体结算当前效果，并记录主角内射来源。")






    def _execute_train_command_132(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("背后位・打屁股")
        losebase = {0: 100, 1: 120}
        source = self._build_face_sex_base_source(target)
        self._apply_rear_sex_adjustment(target, source)
        self._apply_spanking_sex_bonus(target, source)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM132 的简化背后位打屁股变体结算当前效果，并记录主角内射来源。")






    def _execute_train_command_133(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("站立背后位")
        losebase = {0: 60, 1: 120}
        source = self._build_face_sex_base_source(target)
        self._apply_rear_sex_adjustment(target, source)
        self._apply_breast_stimulation_bonus(target, source, rear_mode=False)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta, love_exp=1, stain_transfer="rear")
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM133 的简化站立背后位主干结算当前效果，复用背后位并补入口部/前后污秽传递与主角内射来源。")






    def _execute_train_command_134(self, target: Character, player: Optional[Character]):
        if player is None:
            print("没有可用的调教者。")
            return
        print("背后位ＳＰ")
        losebase = {0: 60, 1: 120}
        source = self._build_face_sex_base_source(target)
        self._apply_rear_sex_adjustment(target, source)
        self._apply_sp_sex_bonus(target, source, rear_mode=True)
        self._apply_rear_spanking_followup_bonus(target, source)
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_128_134_common_sequence(target, player, source, exp_delta, love_exp=1, stain_transfer="rear")
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM134 的简化背后位 SP 主干结算当前效果，复用站立背后位并叠加子宫责め侧强化与主角内射来源。")






    def _execute_train_command_14(self, target: Character, player: Optional[Character]):
        """乳头夹 - 用夹子夹住乳头"""
        print("乳头夹")
        losebase = {0: 20, 1: 80}
        source = {12: 120, 14: 100}
        
        abl_b = target.abl.get(1, 0)
        if abl_b == 0:
            source[17] = 300
        elif abl_b == 1:
            source[17] = 600
        elif abl_b == 2:
            source[17] = 1200
        elif abl_b == 3:
            source[17] = 1800
        elif abl_b == 4:
            source[17] = 2400
        else:
            source[17] = 3000
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM14 乳头夹完成")

    # ========================================
    # COM15: 搾乳器
    # ========================================






    def _execute_train_command_15(self, target: Character, player: Optional[Character]):
        """搾乳器 - 用机器榨取母乳"""
        print("搾乳器")
        losebase = {0: 20, 1: 80}
        source = {12: 150, 14: 200}
        
        abl_b = target.abl.get(1, 0)
        if abl_b == 0:
            source[17] = 200
        elif abl_b == 1:
            source[17] = 400
        elif abl_b == 2:
            source[17] = 800
        elif abl_b == 3:
            source[17] = 1200
        elif abl_b == 4:
            source[17] = 1600
        else:
            source[17] = 2000
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM15 搾乳器完成")

    # ========================================
    # COM16: 飞机杯 (オナホール)
    # ========================================






    def _execute_train_command_16(self, target: Character, player: Optional[Character]):
        """飞机杯 - 用飞机杯刺激阴茎"""
        print("飞机杯")
        losebase = {0: 10, 1: 50}
        source = {12: 100, 14: 50}
        
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 200
        elif abl_c == 1:
            source[0] = 400
        elif abl_c == 2:
            source[0] = 900
        elif abl_c == 3:
            source[0] = 1600
        elif abl_c == 4:
            source[0] = 2400
        else:
            source[0] = 3000
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM16 飞机杯完成")

    # ========================================
    # COM17: 淋浴 (シャワー)
    # ========================================






    def _execute_train_command_17(self, target: Character, player: Optional[Character]):
        """淋浴 - 用淋浴清洗身体"""
        print("淋浴")
        losebase = {0: 0, 1: 30}
        source = {12: 50, 14: 30}
        
        # 清洗污秽
        for key in target.stain:
            target.stain[key] = 0
        
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM17 淋浴完成")

    # ========================================
    # COM18: 肛门珠 (アナルビーズ)
    # ========================================






    def _execute_train_command_18(self, target: Character, player: Optional[Character]):
        """肛门珠 - 将珠子插入肛门"""
        print("肛门珠")
        losebase = {0: 30, 1: 100}
        source = {12: 200, 14: 150}
        
        abl_a = target.abl.get(3, 0)
        if abl_a == 0:
            source[2] = 100
        elif abl_a == 1:
            source[2] = 300
        elif abl_a == 2:
            source[2] = 700
        elif abl_a == 3:
            source[2] = 1200
        elif abl_a == 4:
            source[2] = 1600
        else:
            source[2] = 2000
        
        # 肛门经验调整
        a_exp_level = self._get_exp_level(target.exp.get(1, 0))
        if a_exp_level == 0:
            source[2] = self._scale_value(source[2], 0.2)
            source[6] = 3000
        elif a_exp_level == 1:
            source[2] = self._scale_value(source[2], 0.5)
            source[6] = 200
        elif a_exp_level == 2:
            source[6] = 50
        elif a_exp_level == 3:
            source[2] = self._scale_value(source[2], 1.2)
            source[6] = 10
        else:
            source[2] = self._scale_value(source[2], 1.5)
            source[6] = 0
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM18 肛门珠完成")

    # ========================================
    # COM19: 拍摄 (水晶球)
    # ========================================






    def _execute_train_command_19(self, target: Character, player: Optional[Character]):
        """拍摄 - 用水晶球记录调教过程"""
        print("水晶球拍摄")
        losebase = {0: 0, 1: 50}
        source = {12: 300, 14: 100}
        
        exp_delta = {50: 2}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM19 水晶球拍摄完成")

    # ========================================
    # COM20: 正常位
    # ========================================






    def _execute_train_command_2(self, target: Character, player: Optional[Character]):
        print("肛门爱抚")
        losebase, source = self._build_train_command_2_base_source(target)
        self._apply_train_command_2_anal_exp_adjustments(target, source)
        self._apply_train_command_2_lubrication_adjustments(target, source)
        self._apply_train_command_2_talent_adjustments(target, source)
        self._apply_train_command_2_stain_effects(target, player)

        anal_abl = target.abl.get(3, 0)
        anal_exp_gain = 1 if anal_abl <= 1 else 2 if anal_abl <= 4 else 3 if anal_abl <= 7 else 4
        exp_delta = {1: anal_exp_gain}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM2 的肛感、经验、润滑和欲情倍率结算当前效果。")






    def _execute_train_command_20(self, target: Character, player: Optional[Character]):
        """正常位 - 阴茎插入阴道"""
        print("正常位")
        losebase = {0: 50, 1: 100}
        source = {12: 400}
        
        # ABL:私处感觉
        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 150
        elif abl_v == 1:
            source[1] = 150
            source[3] = 250
        elif abl_v == 2:
            source[1] = 400
            source[3] = 350
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 500
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 700
        else:
            source[1] = 2200
            source[3] = 1000
        
        # 私处经验调整
        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0
        
        # 润滑调整
        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)
        
        # 污秽移动
        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)
        
        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM20 正常位完成")

    # ========================================
    # COM21: 后入位
    # ========================================






    def _execute_train_command_21(self, target: Character, player: Optional[Character]):
        """后入位 - 从背后插入阴道"""
        print("后入位")
        losebase = {0: 50, 1: 100}
        source = {12: 800}

        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 50
        elif abl_v == 1:
            source[1] = 150
            source[3] = 150
        elif abl_v == 2:
            source[1] = 400
            source[3] = 250
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 350
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 600
        else:
            source[1] = 2200
            source[3] = 850

        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5000
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 220
        elif v_exp_level == 2:
            source[6] = 30
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 5
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 900
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 250
        elif lub_level == 2:
            pass
        elif lub_level == 3:
            source[1] = self._scale_value(source[1], 1.4)
            source[6] = int(source.get(6, 0) * 0.2)
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = int(source.get(6, 0) * 0.1)

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)

        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM21 后入位完成")

    # ========================================
    # COM22: 对面座位
    # ========================================






    def _execute_train_command_22(self, target: Character, player: Optional[Character]):
        """对面座位 - 面对面坐着插入"""
        print("对面座位")
        losebase = {0: 50, 1: 100}
        source = {12: 500}

        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 200
        elif abl_v == 1:
            source[1] = 150
            source[3] = 300
        elif abl_v == 2:
            source[1] = 400
            source[3] = 450
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 600
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 850
        else:
            source[1] = 2200
            source[3] = 1200

        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)

        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 3)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM22 对面座位完成")

    # ========================================
    # COM23: 背面座位
    # ========================================






    def _execute_train_command_23(self, target: Character, player: Optional[Character]):
        """背面座位 - 背对背坐着插入"""
        print("背面座位")
        losebase = {0: 50, 1: 100}
        source = {12: 700}

        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 100
        elif abl_v == 1:
            source[1] = 150
            source[3] = 200
        elif abl_v == 2:
            source[1] = 400
            source[3] = 300
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 400
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 550
        else:
            source[1] = 2200
            source[3] = 750

        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)

        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM23 背面座位完成")

    # ========================================
    # COM24: 逆强奸
    # ========================================






    def _execute_train_command_24(self, target: Character, player: Optional[Character]):
        """逆强奸 - 调教对象主动骑乘"""
        print("逆强奸")
        losebase = {0: 30, 1: 80}
        source = {12: 600}

        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 100
        elif abl_v == 1:
            source[1] = 150
            source[3] = 200
        elif abl_v == 2:
            source[1] = 400
            source[3] = 300
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 450
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 600
        else:
            source[1] = 2200
            source[3] = 800

        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)

        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM24 逆强奸完成")

    # ========================================
    # COM25: 逆肛交
    # ========================================






    def _execute_train_command_25(self, target: Character, player: Optional[Character]):
        """逆肛交 - 调教对象主动肛交"""
        print("逆肛交")
        losebase = {0: 50, 1: 100}
        source = {12: 800}

        abl_a = target.abl.get(3, 0)
        if abl_a == 0:
            source[2] = 40
            source[3] = 50
        elif abl_a == 1:
            source[2] = 150
            source[3] = 150
        elif abl_a == 2:
            source[2] = 400
            source[3] = 250
        elif abl_a == 3:
            source[2] = 1000
            source[3] = 350
        elif abl_a == 4:
            source[2] = 1700
            source[3] = 600
        else:
            source[2] = 2200
            source[3] = 850

        a_exp_level = self._get_exp_level(target.exp.get(1, 0))
        if a_exp_level == 0:
            source[2] = self._scale_value(source[2], 0.2)
            source[6] = 5000
        elif a_exp_level == 1:
            source[2] = self._scale_value(source[2], 0.6)
            source[6] = 220
        elif a_exp_level == 2:
            source[6] = 30
        elif a_exp_level == 3:
            source[2] = self._scale_value(source[2], 1.2)
            source[6] = 5
        elif a_exp_level == 4:
            source[2] = self._scale_value(source[2], 1.3)
            source[6] = 0
        else:
            source[2] = self._scale_value(source[2], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[2] = self._scale_value(source[2], 0.1)
            source[6] = source.get(6, 0) + 900
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[2] = self._scale_value(source[2], 0.4)
            source[6] = source.get(6, 0) + 250
        elif lub_level == 2:
            pass
        elif lub_level == 3:
            source[2] = self._scale_value(source[2], 1.4)
            source[6] = int(source.get(6, 0) * 0.2)
        else:
            source[2] = self._scale_value(source[2], 1.8)
            source[6] = int(source.get(6, 0) * 0.1)

        if player is not None:
            target.stain[4] = target.stain.get(4, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(4, 0)

        exp_delta = {1: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM25 逆肛交完成")

    # ========================================
    # COM30: 手淫
    # ========================================






    def _execute_train_command_3(self, target: Character, player: Optional[Character]):
        print(self._build_train_command_3_label(target))

        score = self._get_train_command_3_score(target, player)
        threshold = self._get_train_command_3_threshold(target)
        if not self._check_train_order(score, threshold, "自慰"):
            return

        losebase, source = self._build_train_command_3_base_source(target)
        self._apply_train_command_3_scene_effects(target, source, losebase)
        self._apply_train_command_3_progression_scaling(target, source)
        self._apply_self_stain_transfer(target)
        self._apply_train_command_3_bathing_effects(target)
        exp_delta = self._build_train_command_3_exp_delta(target, player)
        self._add_same_sex_exp(exp_delta, player, target, female_value=3, male_value=3)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM3 的执行值判定、自慰中毒和场景分支结算当前效果。")






    def _execute_train_command_30(self, target: Character, player: Optional[Character]):
        """手淫 - 用手刺激"""
        print("手淫")
        losebase = {0: 10, 1: 50}
        source = {12: 200, 14: 300}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 100
        elif abl_tech == 1:
            source[4] = 150
        elif abl_tech == 2:
            source[4] = 250
        elif abl_tech == 3:
            source[4] = 400
        elif abl_tech == 4:
            source[4] = 600
        else:
            source[4] = 800

        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM30 手淫完成")

    # ========================================
    # COM31: 口交
    # ========================================






    def _execute_train_command_31(self, target: Character, player: Optional[Character]):
        """口交 - 用口刺激"""
        print("口交")
        losebase = {0: 20, 1: 80}
        source = {12: 300, 14: 400}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 150
        elif abl_tech == 1:
            source[4] = 250
        elif abl_tech == 2:
            source[4] = 400
        elif abl_tech == 3:
            source[4] = 600
        elif abl_tech == 4:
            source[4] = 900
        else:
            source[4] = 1200

        exp_delta = {22: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM31 口交完成")

    # ========================================
    # COM32: 乳交
    # ========================================






    def _execute_train_command_32(self, target: Character, player: Optional[Character]):
        """乳交 - 用胸部刺激"""
        print("乳交")
        losebase = {0: 20, 1: 80}
        source = {12: 400, 14: 500}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 100
        elif abl_tech == 1:
            source[4] = 200
        elif abl_tech == 2:
            source[4] = 350
        elif abl_tech == 3:
            source[4] = 550
        elif abl_tech == 4:
            source[4] = 800
        else:
            source[4] = 1100

        exp_delta = {23: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM32 乳交完成")

    # ========================================
    # COM33: 素股
    # ========================================






    def _execute_train_command_33(self, target: Character, player: Optional[Character]):
        """素股 - 大腿摩擦"""
        print("素股")
        losebase = {0: 30, 1: 80}
        source = {12: 300, 14: 400}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 100
        elif abl_tech == 1:
            source[4] = 200
        elif abl_tech == 2:
            source[4] = 350
        elif abl_tech == 3:
            source[4] = 500
        elif abl_tech == 4:
            source[4] = 700
        else:
            source[4] = 950

        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM33 素股完成")

    # ========================================
    # COM34: 骑乘位
    # ========================================






    def _execute_train_command_34(self, target: Character, player: Optional[Character]):
        """骑乘位 - 调教对象骑乘"""
        print("骑乘位")
        losebase = {0: 50, 1: 100}
        source = {12: 600}

        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 40
            source[3] = 150
        elif abl_v == 1:
            source[1] = 150
            source[3] = 250
        elif abl_v == 2:
            source[1] = 400
            source[3] = 350
        elif abl_v == 3:
            source[1] = 1000
            source[3] = 500
        elif abl_v == 4:
            source[1] = 1700
            source[3] = 700
        else:
            source[1] = 2200
            source[3] = 1000

        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = 5500
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = 300
        elif v_exp_level == 2:
            source[6] = 50
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[6] = 10
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.3)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[1] = self._scale_value(source[1], 1.2)

        if player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(3, 0)

        exp_delta = {0: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM34 骑乘位完成")

    # ========================================
    # COM35: 泡泡浴
    # ========================================






    def _execute_train_command_35(self, target: Character, player: Optional[Character]):
        """泡泡浴 - 用身体清洗"""
        print("泡泡浴")
        losebase = {0: 20, 1: 60}
        source = {12: 200, 14: 300}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 150
        elif abl_tech == 1:
            source[4] = 250
        elif abl_tech == 2:
            source[4] = 400
        elif abl_tech == 3:
            source[4] = 600
        elif abl_tech == 4:
            source[4] = 850
        else:
            source[4] = 1100

        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM35 泡泡浴完成")

    # ========================================
    # COM36: 骑乘位肛交
    # ========================================






    def _execute_train_command_36(self, target: Character, player: Optional[Character]):
        """骑乘位肛交 - 调教对象主动肛交"""
        print("骑乘位肛交")
        losebase = {0: 50, 1: 100}
        source = {12: 700}

        abl_a = target.abl.get(3, 0)
        if abl_a == 0:
            source[2] = 40
            source[3] = 100
        elif abl_a == 1:
            source[2] = 150
            source[3] = 200
        elif abl_a == 2:
            source[2] = 400
            source[3] = 300
        elif abl_a == 3:
            source[2] = 1000
            source[3] = 400
        elif abl_a == 4:
            source[2] = 1700
            source[3] = 550
        else:
            source[2] = 2200
            source[3] = 750

        a_exp_level = self._get_exp_level(target.exp.get(1, 0))
        if a_exp_level == 0:
            source[2] = self._scale_value(source[2], 0.2)
            source[6] = 5500
        elif a_exp_level == 1:
            source[2] = self._scale_value(source[2], 0.6)
            source[6] = 300
        elif a_exp_level == 2:
            source[6] = 50
        elif a_exp_level == 3:
            source[2] = self._scale_value(source[2], 1.2)
            source[6] = 10
        elif a_exp_level == 4:
            source[2] = self._scale_value(source[2], 1.3)
            source[6] = 0
        else:
            source[2] = self._scale_value(source[2], 1.8)
            source[6] = 0

        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[2] = self._scale_value(source[2], 0.1)
            source[6] = source.get(6, 0) + 1000
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[2] = self._scale_value(source[2], 0.4)
            source[6] = source.get(6, 0) + 300
        elif lub_level == 2:
            source[2] = self._scale_value(source[2], 0.8)
            source[6] = source.get(6, 0) + 100
        elif lub_level == 3:
            pass
        else:
            source[2] = self._scale_value(source[2], 1.2)

        if player is not None:
            target.stain[4] = target.stain.get(4, 0) | player.stain.get(2, 0)
            player.stain[2] = player.stain.get(2, 0) | target.stain.get(4, 0)

        exp_delta = {1: 1, 7: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM36 骑乘位肛交完成")

    # ========================================
    # COM37: 肛门侍奉
    # ========================================






    def _execute_train_command_37(self, target: Character, player: Optional[Character]):
        """肛门侍奉 - 舔舐肛门"""
        print("肛门侍奉")
        losebase = {0: 30, 1: 80}
        source = {12: 300, 14: 400}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 100
        elif abl_tech == 1:
            source[4] = 200
        elif abl_tech == 2:
            source[4] = 350
        elif abl_tech == 3:
            source[4] = 500
        elif abl_tech == 4:
            source[4] = 700
        else:
            source[4] = 950

        exp_delta = {22: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM37 肛门侍奉完成")

    # ========================================
    # COM38: 足交
    # ========================================






    def _execute_train_command_38(self, target: Character, player: Optional[Character]):
        """足交 - 用脚刺激"""
        print("足交")
        losebase = {0: 10, 1: 50}
        source = {12: 200, 14: 300}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 80
        elif abl_tech == 1:
            source[4] = 150
        elif abl_tech == 2:
            source[4] = 250
        elif abl_tech == 3:
            source[4] = 400
        elif abl_tech == 4:
            source[4] = 600
        else:
            source[4] = 800

        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM38 足交完成")

    # ========================================
    # COM40: 打屁股
    # ========================================






    def _execute_train_command_4(self, target: Character, player: Optional[Character]):
        """口交(主) - 调教者用口刺激调教对象的阴茎"""
        print("口交(主)")
        
        # 基础消耗
        losebase = {0: 5, 1: 50}
        
        # 基础 SOURCE
        source = {
            12: 220,  # 露出
            14: 50,   # 达成
        }
        
        # ABL:阴蒂感觉 (ABL:0)
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 50
        elif abl_c == 1:
            source[0] = 200
        elif abl_c == 2:
            source[0] = 800
        elif abl_c == 3:
            source[0] = 1600
        elif abl_c == 4:
            source[0] = 2400
        else:
            source[0] = 3200
        
        # 调教者的 TALENT:擅用舌头 (TALENT:52)
        if player is not None and player.talent.get(52, 0):
            source[0] *= 2
            source[16] = source.get(16, 0) + source[0] // 20
        
        # 兽奸情况下提前结束
        if target.equipt.get(89, 0):
            self._finalize_train_effects(target, losebase, source, {}, "COM4 兽奸分支")
            return
        
        # 污秽移动
        if player is not None:
            # 奴隶的 P 和调教者的口的污秽移动
            target.stain[2] = target.stain.get(2, 0) | player.stain.get(0, 0)
            player.stain[0] = player.stain.get(0, 0) | target.stain.get(2, 0)
        
        # 经验上升
        exp_delta: Dict[int, int] = {}
        
        # 百合经验 / ホモ经验
        if player is not None:
            target_female = target.talent.get(122, 0) == 0
            player_female = player.talent.get(122, 0) == 0
            if target_female and player_female:
                exp_delta[40] = 3  # 百合经验
            elif not target_female and not player_female:
                exp_delta[41] = 3  # ホモ经验
        
        # 调教者的初吻
        if player is not None and player.cflag.get(16, -1) == -1:
            player.cflag[16] = 201
            player.cstr[4] = target.name
        
        # 调教者的经验
        if player is not None:
            player.cflag[22] = player.cflag.get(22, 0) + 1
        
        # 爱情经验
        love_exp = 2 if target.talent.get(122, 0) == 1 else 1
        if target.cflag.get(2, 0) >= 1000:
            exp_delta[23] = love_exp
        
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM4 口交(主)完成")

    # ========================================
    # COM5: 胸爱抚 (对应 ERB COMF5_胸愛撫.ERB)
    # ========================================






    def _execute_train_command_40(self, target: Character, player: Optional[Character]):
        """打屁股 - SM系指令"""
        print("打屁股")
        losebase = {0: 80, 1: 40}
        source = {12: 200, 14: 500}

        pain_level = self._get_palam_level(target.palam.get(9, 0))
        if pain_level == 0:
            source[6] = 300
        elif pain_level == 1:
            source[6] = 500
        elif pain_level == 2:
            source[6] = 800
        elif pain_level == 3:
            source[6] = 1200
        else:
            source[6] = 1800

        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=0)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM40 打屁股完成")

    # ========================================
    # COM41: 鞭子
    # ========================================






    def _execute_train_command_41(self, target: Character, player: Optional[Character]):
        """鞭子 - SM系指令"""
        print("鞭子")
        losebase = {0: 100, 1: 50}
        source = {12: 300, 14: 600}

        pain_level = self._get_palam_level(target.palam.get(9, 0))
        if pain_level == 0:
            source[6] = 500
        elif pain_level == 1:
            source[6] = 800
        elif pain_level == 2:
            source[6] = 1200
        elif pain_level == 3:
            source[6] = 1800
        else:
            source[6] = 2500

        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=0)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM41 鞭子完成")

    # ========================================
    # COM42: 针
    # ========================================






    def _execute_train_command_42(self, target: Character, player: Optional[Character]):
        """针 - SM系指令"""
        print("针")
        losebase = {0: 120, 1: 80}
        source = {12: 400, 14: 800}

        pain_level = self._get_palam_level(target.palam.get(9, 0))
        if pain_level == 0:
            source[6] = 800
        elif pain_level == 1:
            source[6] = 1200
        elif pain_level == 2:
            source[6] = 1800
        elif pain_level == 3:
            source[6] = 2500
        else:
            source[6] = 3500

        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=0)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM42 针完成")

    # ========================================
    # COM43: 眼罩
    # ========================================






    def _execute_train_command_43(self, target: Character, player: Optional[Character]):
        """眼罩 - 装备系指令"""
        print("眼罩")
        if target.equipt.get(43, 0):
            target.equipt[43] = 0
            print("解除了眼罩")
        else:
            target.equipt[43] = 1
            print("戴上了眼罩")
        losebase = {0: 0, 1: 10}
        source = {12: 100, 14: 50}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM43 眼罩完成")

    # ========================================
    # COM44: 绳子
    # ========================================






    def _execute_train_command_44(self, target: Character, player: Optional[Character]):
        """绳子 - 装备系指令"""
        print("绳子")
        if target.equipt.get(44, 0):
            target.equipt[44] = 0
            print("解开了绳子")
        else:
            target.equipt[44] = 1
            print("绑上了绳子")
        losebase = {0: 0, 1: 10}
        source = {12: 100, 14: 50}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM44 绳子完成")

    # ========================================
    # COM45: 口球
    # ========================================






    def _execute_train_command_45(self, target: Character, player: Optional[Character]):
        """口球 - 装备系指令"""
        print("口球")
        if target.equipt.get(45, 0):
            target.equipt[45] = 0
            print("取下了口球")
        else:
            target.equipt[45] = 1
            print("戴上了口球")
        losebase = {0: 0, 1: 10}
        source = {12: 100, 14: 50}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM45 口球完成")

    # ========================================
    # COM46: 灌肠器+塞子
    # ========================================






    def _execute_train_command_46(self, target: Character, player: Optional[Character]):
        """灌肠器+塞子 - 特殊指令"""
        print("灌肠器+塞子")
        losebase = {0: 50, 1: 100}
        source = {12: 500, 14: 800, 6: 2000}
        exp_delta = {1: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=0)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM46 灌肠器+塞子完成")

    # ========================================
    # COM47: 拘束衣
    # ========================================






    def _execute_train_command_47(self, target: Character, player: Optional[Character]):
        """拘束衣 - 装备系指令"""
        print("拘束衣")
        if target.equipt.get(47, 0):
            target.equipt[47] = 0
            print("脱下了拘束衣")
        else:
            target.equipt[47] = 1
            print("穿上了拘束衣")
        losebase = {0: 0, 1: 10}
        source = {12: 100, 14: 50}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM47 拘束衣完成")

    # ========================================
    # COM48: 足交给予
    # ========================================






    def _execute_train_command_48(self, target: Character, player: Optional[Character]):
        """足交给予 - 侍奉系指令"""
        print("足交给予")
        losebase = {0: 10, 1: 50}
        source = {12: 200, 14: 300}
        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM48 足交给予完成")

    # ========================================
    # COM49: 肛门电极
    # ========================================






    def _execute_train_command_49(self, target: Character, player: Optional[Character]):
        """肛门电极 - 特殊指令"""
        print("肛门电极")
        losebase = {0: 80, 1: 100}
        source = {12: 600, 14: 500, 6: 3000}
        exp_delta = {1: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=0)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM49 肛门电极完成")

    # ========================================
    # COM51: 媚药
    # ========================================






    def _execute_train_command_5(self, target: Character, player: Optional[Character]):
        """胸爱抚 - 调教者用手和口刺激调教对象的乳房"""
        print("胸爱抚")
        
        # 基础消耗
        losebase = {0: 5, 1: 50}
        
        # 基础 SOURCE
        source = {
            4: 60,    # 性行动
            8: 20,    # 不洁
            12: 100,  # 露出
        }
        
        # ABL:乳房感觉 (ABL:1)
        abl_b = target.abl.get(1, 0)
        if abl_b == 0:
            source[17] = 20
            source[3] = 50
        elif abl_b == 1:
            source[17] = 100
            source[3] = 100
        elif abl_b == 2:
            source[17] = 500
            source[3] = 160
        elif abl_b == 3:
            source[17] = 1200
            source[3] = 200
        elif abl_b == 4:
            source[17] = 2000
            source[3] = 230
        else:
            source[17] = 2800
            source[3] = 250
        
        # 死斗场或兽奸情况下提前结束
        if target.equipt.get(89, 0) or target.equipt.get(55, 0):
            self._finalize_train_effects(target, losebase, source, {}, "COM5 死斗场/兽奸分支")
            return
        
        # 教者 [幼儿退行] (TALENT:131)
        if player is not None and player.talent.get(131, 0) and not target.equipt.get(89, 0):
            source[17] = int(source[17] * 1.2)
            source[3] = int(source[3] * 1.2)
        
        # 调教者 [幼稚] (TALENT:132)
        if player is not None and player.talent.get(132, 0) and not target.equipt.get(89, 0):
            source[17] = int(source[17] * 1.2)
            source[3] = int(source[3] * 1.2)
        
        # 污秽处理
        if target.equipt.get(90, 0):  # 触手
            target.stain[5] = target.stain.get(5, 0) | 2 | 4
        elif player is not None:
            # 乳房污秽较少时用口
            stain_5 = target.stain.get(5, 0)
            is_assi_play = player.cflag.get(1, 0) == 1
            master_no_fear = self.interpreter.vars.get_flag(64, 0) == 1
            
            if stain_5 < 2 or stain_5 == 16 or stain_5 == 17 or is_assi_play or master_no_fear:
                # 调教者擅用舌头
                if player.talent.get(52, 0):
                    source[17] = int(source[17] * 1.4)
                    source[16] = source.get(16, 0) + source[17] // 20
                
                # 口污秽移动
                target.stain[5] = target.stain.get(5, 0) | player.stain.get(0, 0)
                player.stain[0] = player.stain.get(0, 0) | target.stain.get(5, 0)
            
            # 手指污秽移动
            target.stain[5] = target.stain.get(5, 0) | player.stain.get(1, 0)
            player.stain[1] = player.stain.get(1, 0) | target.stain.get(5, 0)
        
        # 经验上升
        exp_delta: Dict[int, int] = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=5, male_value=5)
        self._add_love_exp(exp_delta, target, 1)
        
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM5 胸爱抚完成")

    # ========================================
    # COM6: 接吻 (对应 ERB COMF6_キス.ERB)
    # ========================================






    def _execute_train_command_50(self, target: Character, player: Optional[Character]):
        if player is not None and self._use_item(player, "润滑液"):
            losebase: Dict[int, int] = {}
            source = {10: 10000, 12: 300}
            exp_delta: Dict[int, int] = {}
            self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
            print("润滑液")
            self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM50 直接消耗 ITEM:25，并结算固定 SOURCE。")
        else:
            print("没有可用的润滑液。")






    def _execute_train_command_51(self, target: Character, player: Optional[Character]):
        """媚药 - 道具系指令"""
        print("媚药")
        if player is not None and self._use_item(player, "媚药"):
            losebase = {0: 0, 1: 10}
            source = {5: 5000, 10: 2000}
            exp_delta = {}
            self._finalize_train_effects(target, losebase, source, exp_delta, "COM51 媚药完成")
            target.equipt[21] = 1
            target.cflag[31] = int(target.cflag.get(31, 0)) + 1
            if target.talent.get(46, 0):
                target.cflag[32] = 1
        else:
            print("没有可用的媚药。")

    # ========================================
    # COM52: 利尿剂
    # ========================================






    def _execute_train_command_52(self, target: Character, player: Optional[Character]):
        """利尿剂 - 道具系指令"""
        print("利尿剂")
        if player is not None and self._use_item(player, "利尿剂"):
            losebase = {0: 0, 1: 10}
            source = {8: 2000, 10: 1000}
            exp_delta = {}
            self._finalize_train_effects(target, losebase, source, exp_delta, "COM52 利尿剂完成")
        else:
            print("没有可用的利尿剂。")

    # ========================================
    # COM54: 野外PLAY
    # ========================================






    def _execute_train_command_53(self, target: Character, player: Optional[Character]):
        if self._is_train_video_recording(target):
            self._stop_train_video_recording(target, player)
            return

        if player is None or self._get_item_count(player, 28) <= 0:
            print("没有可用的水晶球魔力源。")
            return
        self._start_train_video_recording(target)
        print("水晶球已开始录像。")






    def _execute_train_command_54(self, target: Character, player: Optional[Character]):
        """野外PLAY - 场景系指令"""
        print("野外PLAY")
        if target.equipt.get(54, 0):
            target.equipt[54] = 0
            print("回到了室内")
        else:
            target.equipt[54] = 1
            print("来到了野外")
        losebase = {0: 10, 1: 30}
        source = {12: 500, 14: 200}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM54 野外PLAY完成")

    # ========================================
    # COM55: 什么都不做
    # ========================================






    def _execute_train_command_55(self, target: Character, player: Optional[Character]):
        """什么都不做 - 放置PLAY"""
        print("什么都不做")
        losebase = {0: 0, 1: 10}
        source = {14: 50}

        lust_level = self._get_palam_level(target.palam.get(5, 0))
        if lust_level == 0:
            source[12] = 10
        elif lust_level == 1:
            source[12] = 30
        elif lust_level == 2:
            source[12] = 60
        elif lust_level == 3:
            source[12] = 100
        else:
            source[12] = 150

        abl_service = target.abl.get(16, 0)
        if abl_service == 0:
            source[3] = 0
        elif abl_service == 1:
            source[3] = 20
        elif abl_service == 2:
            source[3] = 40
        elif abl_service == 3:
            source[3] = 70
        elif abl_service == 4:
            source[3] = 110
        else:
            source[3] = 150

        abl_maso = target.abl.get(21, 0)
        if abl_maso == 0:
            source[3] = self._scale_value(source[3], 0.8)
            source[12] = self._scale_value(source[12], 0.8)
            source[10] = 0
        elif abl_maso == 1:
            source[10] = 20
        elif abl_maso == 2:
            source[3] = self._scale_value(source[3], 1.3)
            source[12] = self._scale_value(source[12], 1.2)
            source[10] = 40
        elif abl_maso == 3:
            source[3] = self._scale_value(source[3], 1.4)
            source[12] = self._scale_value(source[12], 1.4)
            source[10] = 70
        elif abl_maso == 4:
            source[3] = self._scale_value(source[3], 1.7)
            source[12] = self._scale_value(source[12], 1.5)
            source[10] = 110
        else:
            source[3] = self._scale_value(source[3], 2.0)
            source[12] = self._scale_value(source[12], 1.7)
            source[10] = 150

        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM55 什么都不做完成")

    # ========================================
    # COM57: 羞耻PLAY
    # ========================================






    def _execute_train_command_56(self, target: Character, player: Optional[Character]):
        print("介绍自己" if target.equipt.get(53, 0) else "交谈")
        losebase, source, submission_level, has_love = self._build_train_command_56_base_values(target)
        source = self._build_train_command_56_source_values(target, source)
        palam_level = self._get_palam_level(target.palam.get(4, 0))
        exp_delta = self._build_train_command_56_exp_delta(target, player, palam_level, has_love)
        talk_exp = exp_delta[73]
        self._add_love_exp(exp_delta, target, talk_exp)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM56 的爱慕、顺从、侍奉精神与话术倍率结算当前效果。")






    def _execute_train_command_57(self, target: Character, player: Optional[Character]):
        """羞耻PLAY - 场景系指令"""
        print("羞耻PLAY")
        if target.equipt.get(57, 0):
            target.equipt[57] = 0
            print("结束了羞耻PLAY")
        else:
            target.equipt[57] = 1
            print("开始了羞耻PLAY")
        losebase = {0: 10, 1: 30}
        source = {12: 600, 14: 300}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM57 羞耻PLAY完成")

    # ========================================
    # COM58: 浴室PLAY
    # ========================================






    def _execute_train_command_58(self, target: Character, player: Optional[Character]):
        """浴室PLAY - 场景系指令"""
        print("浴室PLAY")
        if target.equipt.get(58, 0):
            target.equipt[58] = 0
            print("结束了浴室PLAY")
        else:
            target.equipt[58] = 1
            print("开始了浴室PLAY")
        losebase = {0: 10, 1: 20}
        source = {12: 300, 14: 100}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM58 浴室PLAY完成")

    # ========================================
    # COM59: 新妻PLAY
    # ========================================






    def _execute_train_command_59(self, target: Character, player: Optional[Character]):
        """新妻PLAY - 场景系指令"""
        print("新妻PLAY")
        if target.equipt.get(59, 0):
            target.equipt[59] = 0
            print("结束了新妻PLAY")
        else:
            target.equipt[59] = 1
            print("开始了新妻PLAY")
        losebase = {0: 10, 1: 20}
        source = {12: 400, 14: 200, 3: 200}
        exp_delta = {}
        self._add_love_exp(exp_delta, target, 1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM59 新妻PLAY完成")

    # ========================================
    # COM60: 助手接吻
    # ========================================






    def _execute_train_command_6(self, target: Character, player: Optional[Character]):
        print("接吻")
        dirty_score = self._build_train_command_6_dirty_score(target, player)
        losebase = {0: 5, 1: 50}
        source = {8: dirty_score * 20 + 10}
        self._apply_train_command_6_service_scaling(target, source)
        self._apply_train_command_6_partner_branch(target, player, source)
        exp_delta: Dict[int, int] = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=3, male_value=3)
        love_exp = self._apply_train_command_6_first_kiss_mark(target, player)
        self._add_love_exp(exp_delta, target, love_exp)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM6 的污秽值、侍奉精神与技巧倍率结算当前效果。")






    def _execute_train_command_60(self, target: Character, player: Optional[Character]):
        """助手接吻 - 助手系指令"""
        print("助手接吻")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 10, 1: 30}
        source = {12: 100, 3: 100}
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM60 助手接吻完成")

    # ========================================
    # COM61: 强制舔阴
    # ========================================






    def _execute_train_command_61(self, target: Character, player: Optional[Character]):
        """强制舔阴 - 助手系指令"""
        print("强制舔阴")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 20, 1: 60}
        source = {12: 300, 14: 400}
        exp_delta = {1: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM61 强制舔阴完成")

    # ========================================
    # COM63: 贝合
    # ========================================






    def _execute_train_command_62(self, target: Character, player: Optional[Character]):
        assistant = self._get_current_assistant()
        if player is None or assistant is None:
            print("没有可用的助手。")
            return
        print("侵犯助手")
        score = self._build_train_command_62_score(target, player, assistant)
        if not self._check_train_order(score, 40, "侵犯助手"):
            return
        losebase, source = self._build_train_command_62_base_values(target)
        exp_delta = self._build_train_command_62_exp_delta(target, player, assistant, source)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM62 的基础执行值、助手性交经验与主角射精来源结算当前效果。")






    def _execute_train_command_63(self, target: Character, player: Optional[Character]):
        """贝合 - 助手系指令"""
        print("贝合")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 30, 1: 80}
        source = {12: 400, 14: 300}
        exp_delta = {0: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=3, male_value=3)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM63 贝合完成")

    # ========================================
    # COM66: 二人口交
    # ========================================






    def _execute_train_command_64(self, target: Character, player: Optional[Character]):
        assistant = self._get_current_assistant()
        if player is None or assistant is None:
            print("没有可用的助手。")
            return
        mode_pair = self._choose_threesome_mode()
        if mode_pair is None:
            return
        print("３Ｐ")
        losebase = {0: 160, 1: 350}
        source: Dict[int, int] = {11: 1500, 12: 2500, 14: 1500, 13: 0}
        exp_delta: Dict[int, int] = {}
        self._apply_train_command_64_mode_effects(target, player, assistant, mode_pair, source, exp_delta)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM64 的简化三人性交模式结算当前效果，并记录主角/助手的受孕来源。")






    def _execute_train_command_65(self, target: Character, player: Optional[Character]):
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        print("逆侵犯助手")
        score = self._build_train_command_65_score(target, player, assistant)
        if assistant.exp.get(0, 0) == 0:
            score -= 15
        if not self._check_train_order(score, 40, "逆侵犯助手"):
            return

        losebase = {0: 40, 1: 220}
        source = self._build_train_command_65_source(target)

        exp_delta: Dict[int, int] = {}
        self._resolve_train_command_65_sequence(target, assistant, source, exp_delta)
        self._finalize_train_effects(target, losebase, source, exp_delta, "按原作 COM65 的基础执行值、助手性交经验与调教对象射精来源结算当前效果。")






    def _execute_train_command_66(self, target: Character, player: Optional[Character]):
        """二人口交 - 多人系指令"""
        print("二人口交")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 30, 1: 100}
        source = {12: 500, 14: 600}
        exp_delta = {22: 2}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM66 二人口交完成")

    # ========================================
    # COM67: 足交给予2
    # ========================================






    def _execute_train_command_67(self, target: Character, player: Optional[Character]):
        """足交给予2 - 侍奉系指令"""
        print("足交给予2")
        losebase = {0: 10, 1: 50}
        source = {12: 200, 14: 300}
        exp_delta = {20: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM67 足交给予2完成")

    # ========================================
    # COM68: 双重口交
    # ========================================






    def _execute_train_command_68(self, target: Character, player: Optional[Character]):
        """双重口交 - 多人系指令"""
        print("双重口交")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 30, 1: 100}
        source = {12: 500, 14: 600}
        exp_delta = {22: 2}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM68 双重口交完成")

    # ========================================
    # COM69: 六九式
    # ========================================






    def _execute_train_command_69(self, target: Character, player: Optional[Character]):
        """六九式 - 互相侍奉"""
        print("六九式")
        losebase = {0: 30, 1: 80}
        source = {12: 400, 14: 400}

        abl_tech = target.abl.get(13, 0)
        if abl_tech == 0:
            source[4] = 100
        elif abl_tech == 1:
            source[4] = 200
        elif abl_tech == 2:
            source[4] = 350
        elif abl_tech == 3:
            source[4] = 500
        elif abl_tech == 4:
            source[4] = 700
        else:
            source[4] = 950

        exp_delta = {22: 1}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM69 六九式完成")

    # ========================================
    # COM70: 双重素股
    # ========================================






    def _execute_train_command_7(self, target: Character, player: Optional[Character]):
        """自己扒开 - 调教对象自己用手打开阴道展示"""
        label = "公开" if target.equipt.get(53, 0) else ""
        print(f"{label}自己扒开")
        
        # 基础消耗
        losebase = {0: 5, 1: 30}
        
        # 基础 SOURCE
        source = {
            12: 500,  # 露出
            14: 100,  # 达成
        }
        
        # ABL:私处感觉 (ABL:2)
        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 50
        elif abl_v == 1:
            source[1] = 200
        elif abl_v == 2:
            source[1] = 500
        elif abl_v == 3:
            source[1] = 1000
        elif abl_v == 4:
            source[1] = 1800
        else:
            source[1] = 2500
        
        # 执行判定
        score = self._calculate_com_order_base(target)
        score += target.abl.get(11, 0) * 3   # 欲望
        score += abl_v * 2                   # 私处感觉
        score += target.abl.get(16, 0) * 4   # 侍奉精神
        score += target.abl.get(17, 0) * 3   # 露出癖
        score += target.abl.get(31, 0) * 3   # 自慰中毒
        
        # 欲情等级
        lust_level = self._get_palam_level(target.palam.get(5, 0))
        score += lust_level * 3
        
        # 润滑不足减分
        lubrication_level = self._get_palam_level(target.palam.get(3, 0))
        if lubrication_level < 3:
            score -= 5
        
        if score < 0:
            self.output_buffer.append("自己扒开执行失败")
            return
        
        # 露出癖加成
        exposure_level = target.abl.get(17, 0)
        if exposure_level >= 3:
            source[12] *= 2
        
        # 公开拍摄加成
        if target.equipt.get(53, 0):
            source[12] *= 2
            source[14] *= 2
        
        # 经验上升
        exp_delta: Dict[int, int] = {}
        exp_delta[50] = 1  # 露出经验
        
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM7 自己扒开完成")






    def _execute_train_command_70(self, target: Character, player: Optional[Character]):
        """双重素股 - 多人系指令"""
        print("双重素股")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 30, 1: 100}
        source = {12: 500, 14: 500}
        exp_delta = {20: 2}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM70 双重素股完成")

    # ========================================
    # COM71: 双重乳交
    # ========================================






    def _execute_train_command_71(self, target: Character, player: Optional[Character]):
        """双重乳交 - 多人系指令"""
        print("双重乳交")
        assistant = self._get_current_assistant()
        if assistant is None:
            print("没有可用的助手。")
            return
        losebase = {0: 30, 1: 100}
        source = {12: 600, 14: 600}
        exp_delta = {23: 2}
        self._add_same_sex_exp(exp_delta, player, target, female_value=2, male_value=2)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM71 双重乳交完成")

    # ========================================
    # COM72: 剃阴毛
    # ========================================






    def _execute_train_command_72(self, target: Character, player: Optional[Character]):
        """剃阴毛 - 特殊指令"""
        print("剃阴毛")
        losebase = {0: 0, 1: 20}
        source = {12: 200, 14: 100}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM72 剃阴毛完成")

    # ========================================
    # COM73: 弄发型
    # ========================================






    def _execute_train_command_73(self, target: Character, player: Optional[Character]):
        """弄发型 - 特殊指令"""
        print("弄发型")
        losebase = {0: 0, 1: 10}
        source = {12: 100, 14: 50}
        exp_delta = {}
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM73 弄发型完成")






    def _execute_train_command_8(self, target: Character, player: Optional[Character]):
        """插入手指 - 调教者用手指刺激调教对象的阴道"""
        print("插入手指")
        losebase = {0: 30, 1: 80}
        source = {12: 300, 14: 200}
        
        # ABL:私处感觉
        abl_v = target.abl.get(2, 0)
        if abl_v == 0:
            source[1] = 10
            source[13] = 150
        elif abl_v == 1:
            source[1] = 50
            source[13] = 250
        elif abl_v == 2:
            source[1] = 250
            source[13] = 400
        elif abl_v == 3:
            source[1] = 600
            source[13] = 700
        elif abl_v == 4:
            source[1] = 1200
            source[13] = 1300
        else:
            source[1] = 1800
            source[13] = 2000
        
        # 私处经验调整
        v_exp_level = self._get_exp_level(target.exp.get(0, 0))
        if v_exp_level == 0:
            source[1] = self._scale_value(source[1], 0.2)
            source[13] = self._scale_value(source[13], 0.2)
            source[6] = 300
        elif v_exp_level == 1:
            source[1] = self._scale_value(source[1], 0.5)
            source[13] = self._scale_value(source[13], 0.5)
            source[6] = 180
        elif v_exp_level == 2:
            source[6] = 80
        elif v_exp_level == 3:
            source[1] = self._scale_value(source[1], 1.2)
            source[13] = self._scale_value(source[13], 1.0)
            source[6] = 30
        elif v_exp_level == 4:
            source[1] = self._scale_value(source[1], 1.6)
            source[13] = self._scale_value(source[13], 1.2)
            source[6] = 0
        else:
            source[1] = self._scale_value(source[1], 1.8)
            source[13] = self._scale_value(source[13], 1.5)
            source[6] = 0
        
        # 小人体型效果提升
        if target.talent.get(263, 0):
            source[1] = self._scale_value(source[1], 1.5)
        
        # 润滑调整
        lub_level = self._get_palam_level(target.palam.get(3, 0))
        if lub_level == 0:
            source[1] = self._scale_value(source[1], 0.1)
            source[6] = source.get(6, 0) + 700
            source[6] = int(source[6] * 3.0)
        elif lub_level == 1:
            source[1] = self._scale_value(source[1], 0.2)
            source[6] = source.get(6, 0) + 200
        elif lub_level == 2:
            source[1] = self._scale_value(source[1], 0.6)
            source[6] = int(source.get(6, 0) * 0.8)
        elif lub_level == 3:
            source[6] = int(source.get(6, 0) * 0.5)
        else:
            source[1] = self._scale_value(source[1], 2.0)
            source[6] = int(source.get(6, 0) * 0.1)
        
        # 欲情调整
        lust_level = self._get_palam_level(target.palam.get(5, 0))
        if lust_level == 0:
            source[1] = self._scale_value(source[1], 0.5)
        elif lust_level == 1:
            source[1] = self._scale_value(source[1], 0.8)
        elif lust_level == 2:
            source[1] = self._scale_value(source[1], 1.2)
        elif lust_level == 3:
            source[1] = self._scale_value(source[1], 1.5)
        else:
            source[1] = self._scale_value(source[1], 1.8)
        
        # 私处敏感/钝感
        if target.talent.get(103, 0):  # 钝感
            source[6] = int(source.get(6, 0) * 1.5)
            source[13] = int(source[13] * 1.5)
            source[14] = int(source[14] * 1.5)
        elif target.talent.get(104, 0):  # 敏感
            source[6] = int(source.get(6, 0) * 0.6)
            source[13] = int(source[13] * 0.6)
            source[14] = int(source[14] * 0.6)
        
        # 处女且看重贞操
        if target.exp.get(0, 0) == 0 and target.talent.get(30, 0):
            source[13] = int(source[13] * 2.0)
        
        # 未熟
        if target.talent.get(135, 0):
            source[6] = int(source.get(6, 0) * 2.0)
        
        # 污秽处理
        if target.equipt.get(90, 0):  # 触手
            target.stain[3] = target.stain.get(3, 0) | 2 | 4
        elif player is not None:
            target.stain[3] = target.stain.get(3, 0) | player.stain.get(1, 0)
            player.stain[1] = player.stain.get(1, 0) | target.stain.get(3, 0)
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM8 插入手指完成")

    # ========================================
    # COM9: 振动宝石 (ローター)
    # ========================================






    def _execute_train_command_9(self, target: Character, player: Optional[Character]):
        """振动宝石 - 用振动宝石刺激阴蒂"""
        print("振动宝石")
        losebase = {0: 10, 1: 80}
        source = {12: 120, 14: 70}
        
        abl_c = target.abl.get(0, 0)
        if abl_c == 0:
            source[0] = 200
        elif abl_c == 1:
            source[0] = 400
        elif abl_c == 2:
            source[0] = 900
        elif abl_c == 3:
            source[0] = 1600
        elif abl_c == 4:
            source[0] = 2400
        else:
            source[0] = 3000
        
        exp_delta = {}
        self._add_same_sex_exp(exp_delta, player, target, female_value=1, male_value=1)
        self._finalize_train_effects(target, losebase, source, exp_delta, "COM9 振动宝石完成")

    # ========================================
    # COM10: 振动杖 (Eマッサージャ)
    # ========================================






    def _get_training_derived_exp_gain(self, scaled_value: int) -> int:
        if scaled_value >= 12000:
            return 16
        if scaled_value >= 8000:
            return 12
        if scaled_value >= 5000:
            return 8
        if scaled_value >= 3000:
            return 4
        if scaled_value >= 2000:
            return 2
        if scaled_value >= 1000:
            return 1
        return 0






    def _get_training_derived_scale(self, scaled_value: int, scales: tuple[float, float, float, float, float, float]) -> float:
        if scaled_value >= 12000:
            return scales[0]
        if scaled_value >= 8000:
            return scales[1]
        if scaled_value >= 5000:
            return scales[2]
        if scaled_value >= 3000:
            return scales[3]
        if scaled_value >= 2000:
            return scales[4]
        if scaled_value >= 1000:
            return scales[5]
        return 1.0






    def _get_training_flasher_shame_scale(self, target: Character) -> float:
        current_shame = int(target.palam.get(8, 0))
        if current_shame < self.palam_level_thresholds[1]:
            return 1.00
        if current_shame < self.palam_level_thresholds[2]:
            return 0.90
        if current_shame < self.palam_level_thresholds[3]:
            return 0.70
        if current_shame < self.palam_level_thresholds[4]:
            return 0.50
        return 0.30






    def _get_training_master_affection_gain(self, target: Character, player: Character, master_bonus: int) -> int:
        base_gain = int(target.abl.get(10, 0))
        base_gain += self._get_training_master_affection_talent_adjustment(target, player)
        base_gain = max(1, base_gain)
        return max(0, base_gain + master_bonus)






    def _get_training_master_affection_talent_adjustment(self, target: Character, player: Character) -> int:
        adjustment = 0
        if int(target.talent.get(11, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(13, 0)) != 0:
            adjustment += 1
        if int(target.talent.get(20, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(21, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(22, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(34, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(63, 0)) != 0:
            adjustment += 1
        if int(target.talent.get(70, 0)) != 0:
            adjustment += 1
        if int(target.talent.get(71, 0)) != 0:
            adjustment -= 1
        if int(target.talent.get(79, 0)) != 0 and int(player.talent.get(122, 0)) == 0:
            adjustment -= 1
        if int(target.talent.get(82, 0)) != 0 and int(player.talent.get(122, 0)) != 0:
            adjustment -= 1
        if int(player.talent.get(91, 0)) != 0:
            adjustment += 1
        if int(player.talent.get(92, 0)) != 0:
            adjustment += 1
        if int(player.talent.get(113, 0)) != 0:
            adjustment += 1
        if int(player.talent.get(126, 0)) != 0:
            adjustment += 1
        return adjustment






    def _get_training_master_bonus_score(
        self,
        target: Character,
        player: Character,
        source: Dict[int, int],
        orgasm_count: int,
        ejaculation_count: int,
    ) -> int:
        orgasm_bonus = self._get_training_master_orgasm_bonus(source, orgasm_count)
        ejaculation_bonus = self._get_training_master_ejaculation_bonus(target, ejaculation_count)
        return orgasm_bonus + ejaculation_bonus






    def _get_training_master_ejaculation_bonus(self, target: Character, ejaculation_count: int) -> int:
        if ejaculation_count <= 0:
            return 0
        if int(target.exp.get(20, 0)) < self.exp_level_thresholds[3]:
            return 0
        return ejaculation_count






    def _get_training_master_ejaculation_count(self, player: Character, source: Dict[int, int]) -> int:
        count = 0
        if int(source.get(4, 0)) > 0:
            count += 1
        penis_stain = int(player.stain.get(2, 0))
        if penis_stain & 4:
            count += 1
        return count






    def _get_training_master_orgasm_bonus(self, source: Dict[int, int], orgasm_count: int) -> int:
        if orgasm_count <= 0:
            return 0
        total = 0
        for source_id in (0, 1, 2, 14):
            value = int(source.get(source_id, 0))
            if value >= 10000:
                total += max(1, value // 10000)
        if int(source.get(15, 0)) >= 10000:
            total += max(1, int(source.get(15, 0)) // 10000)
        return total * max(1, orgasm_count)






    def _get_training_milk_gain(self, target: Character, source: Dict[int, int]) -> int:
        value = int(source.get(0, 0)) // 5 + int(source.get(1, 0)) // 5 + int(source.get(2, 0)) // 5 + int(source.get(14, 0)) * 3
        if int(target.talent.get(20, 0)) != 0:
            value //= 2
        if int(target.talent.get(70, 0)) != 0:
            value = self._scale_value(value, 1.2)
        if int(target.talent.get(76, 0)) != 0:
            value = self._scale_value(value, 1.1)
        if int(target.talent.get(71, 0)) != 0:
            value = self._scale_value(value, 0.8)
        if int(target.talent.get(108, 0)) != 0:
            value = self._scale_value(value, 1.5)
        if int(target.equipt.get(21, 0)) != 0:
            value *= 2
        if int(target.equipt.get(22, 0)) != 0:
            value //= 2
        player = self._get_player()
        if player is not None and (int(player.talent.get(131, 0)) != 0 or int(player.talent.get(132, 0)) != 0):
            value *= 2
        if int(target.talent.get(109, 0)) != 0:
            value = self._scale_value(value, 0.5)
        if int(target.talent.get(116, 0)) != 0:
            value = self._scale_value(value, 0.2)
        return max(0, 1000 + (value - 1000) // 2)






    def _get_training_milk_heavy_source_bonus(self, milk_exp: int) -> tuple[int, int]:
        if milk_exp < 1:
            return 20000, 10000
        if milk_exp < 10:
            return 10000, 8000
        if milk_exp < 50:
            return 7000, 6000
        if milk_exp < 100:
            return 5000, 4000
        if milk_exp < 150:
            return 3000, 2000
        return 1800, 1200






    def _get_training_milk_light_source_bonus(self, milk_exp: int) -> tuple[int, int]:
        if milk_exp < 1:
            return 10000, 5000
        if milk_exp < 10:
            return 5000, 4000
        if milk_exp < 50:
            return 2500, 2000
        if milk_exp < 100:
            return 1600, 1400
        if milk_exp < 150:
            return 800, 500
        return 200, 250






    def _get_training_omorashi_exp_gain(self, target: Character, orgasm_score: int) -> int:
        has_catheter = int(target.equipt.get(22, 0)) != 0
        has_omorashi_talent = int(target.talent.get(57, 0)) != 0
        if orgasm_score >= 7 and has_catheter and has_omorashi_talent:
            return 5
        if (orgasm_score >= 7 and has_catheter) or (orgasm_score >= 5 and has_catheter and has_omorashi_talent):
            return 4
        if (orgasm_score >= 7 and has_omorashi_talent) or (orgasm_score >= 5 and has_catheter) or (orgasm_score >= 3 and has_catheter and has_omorashi_talent):
            return 3
        if (orgasm_score >= 5 and has_omorashi_talent) or (orgasm_score >= 3 and has_catheter) or (orgasm_score >= 1 and has_catheter and has_omorashi_talent):
            return 2
        if (orgasm_score >= 3 and has_omorashi_talent) or (orgasm_score >= 1 and has_catheter):
            return 1
        return 0






    def _get_training_omorashi_orgasm_score(self, source: Dict[int, int]) -> int:
        score = 0
        for source_id in (0, 1, 2, 14, 15):
            value = int(source.get(source_id, 0))
            if value >= 10000:
                score += max(1, value // 10000)
        return score






    def _get_training_pain_pleasure_exp_gain(self, pleasure_total: int, pain_value: int) -> int:
        if pleasure_total >= 3000 and pain_value >= 2000:
            return 16
        if pleasure_total >= 2500 and pain_value >= 1500:
            return 12
        if pleasure_total >= 1500 and pain_value >= 1000:
            return 8
        if pleasure_total >= 1000 and pain_value >= 500:
            return 4
        if pleasure_total >= 600 and pain_value >= 300:
            return 2
        if pleasure_total >= 300 and pain_value >= 100:
            return 1
        return 0






    def _get_training_pain_pleasure_hatred_scale(self, pleasure_total: int, pain_value: int) -> float:
        gain = self._get_training_pain_pleasure_exp_gain(pleasure_total, pain_value)
        if gain >= 16:
            return 0.65
        if gain >= 12:
            return 0.70
        if gain >= 8:
            return 0.75
        if gain >= 4:
            return 0.80
        if gain >= 2:
            return 0.85
        if gain >= 1:
            return 0.90
        return 1.0






    def _get_training_source_autotrain_count_scale(self, count: int) -> float:
        if count <= 0:
            return 1.0
        if count < 5:
            return 1.25
        if count < 10:
            return 1.50
        if count < 15:
            return 2.10
        if count < 20:
            return 2.85
        if count < 25:
            return 3.90
        if count < 30:
            return 5.30
        if count < 40:
            return 7.25
        return 9.90






    def _get_training_target_ejac_heavy_source_bonus(self, ejac_exp: int) -> tuple[int, int]:
        if ejac_exp < 1:
            return 20000, 10000
        if ejac_exp < 10:
            return 10000, 8000
        if ejac_exp < 50:
            return 7000, 6000
        if ejac_exp < 100:
            return 5000, 4000
        if ejac_exp < 150:
            return 3000, 2000
        return 1800, 1200






    def _get_training_target_ejac_light_source_bonus(self, ejac_exp: int) -> tuple[int, int]:
        if ejac_exp < 1:
            return 10000, 5000
        if ejac_exp < 10:
            return 5000, 4000
        if ejac_exp < 50:
            return 2500, 2000
        if ejac_exp < 100:
            return 1600, 1400
        if ejac_exp < 150:
            return 800, 500
        return 200, 250






    def _get_training_target_ejaculation_gain(self, target: Character, source: Dict[int, int]) -> int:
        value = sum(int(source.get(idx, 0)) for idx in (0, 1, 2, 14))
        if int(target.talent.get(20, 0)) != 0:
            value //= 2
        if int(target.talent.get(70, 0)) != 0:
            value = self._scale_value(value, 1.2)
        if int(target.talent.get(76, 0)) != 0:
            value = self._scale_value(value, 1.1)
        if int(target.talent.get(71, 0)) != 0:
            value = self._scale_value(value, 0.8)
        if int(target.equipt.get(21, 0)) != 0:
            value *= 2
        if int(target.equipt.get(22, 0)) != 0:
            value //= 2
        if int(target.equipt.get(37, 0)) != 0:
            value //= 2
        if int(target.talent.get(135, 0)) != 0:
            immature_penalty = random.randint(0, 699) - random.randint(0, 799) + 400
            value -= immature_penalty
        return max(0, 1000 + (value - 1000) // 2)






    def _get_training_wormbirth_heavy_source_bonus(self, birth_exp: int) -> tuple[int, int]:
        if birth_exp < 1:
            return 20000, 10000
        if birth_exp < 10:
            return 10000, 8000
        if birth_exp < 50:
            return 7000, 6000
        if birth_exp < 100:
            return 5000, 4000
        if birth_exp < 150:
            return 3000, 2000
        return 1800, 1200






    def _get_training_wormbirth_light_source_bonus(self, birth_exp: int) -> tuple[int, int]:
        if birth_exp < 1:
            return 10000, 5000
        if birth_exp < 10:
            return 5000, 4000
        if birth_exp < 50:
            return 2500, 2000
        if birth_exp < 100:
            return 1600, 1400
        if birth_exp < 150:
            return 800, 500
        return 200, 250






    def _handle_train_menu_choice(self, choice: str, target: Character, available_commands: List[int]) -> Optional[str]:
        if choice == "100":
            player = self._get_player()
            for message in self._finalize_train_video_sale(target, player):
                print(message)
            self.advance_time()
            return "SHOP"
        if choice == "10":
            player = self._get_player()
            for message in self._finalize_train_video_sale(target, player):
                print(message)
            self.do_rest()
            return None
        command_id = self._parse_choice_int(choice)
        if command_id is not None and command_id in available_commands:
            self.execute_train_command(choice, target)
            return None
        print("Invalid selection.")
        return None






    def _is_train_command_available(self, command_id: int, target: Optional[Character]) -> bool:
        if target is None:
            return False

        clothing_enabled = self.interpreter.vars.get_flag(37) != 0
        clothing_state = target.cflag.get(40, 0)
        target_is_male = target.talent.get(122, 0) == 1
        duel_mode = target.equipt.get(55, 0) > 0
        tentacle_mode = target.equipt.get(90, 0) > 0
        beast_mode = target.equipt.get(89, 0) > 0
        mouth_gagged = target.equipt.get(45, 0) > 0

        basic = self._is_train_command_available_basic(command_id, target, clothing_enabled, clothing_state, target_is_male, duel_mode, tentacle_mode, beast_mode, mouth_gagged)
        if basic is not None:
            return basic
        partnership = self._is_train_command_available_partnership(command_id, target)
        if partnership is not None:
            return partnership
        assisted = self._is_train_command_available_assisted(command_id, target)
        if assisted is not None:
            return assisted
        special = self._is_train_command_available_special(command_id, target, clothing_enabled, clothing_state, tentacle_mode, beast_mode)
        if special is not None:
            return special
        return False




    def _is_train_command_available_assisted(self, command_id: int, target: Character) -> Optional[bool]:
        if command_id not in (62, 64, 65):
            return None
        assistant = self._get_current_assistant()
        if assistant is None:
            return False
        if command_id in (62, 65):
            if target.talent.get(122, 0):
                return False
            return True
        if target.talent.get(122, 0) or target.talent.get(135, 0):
            return False
        if self._target_has_blocking_modes(target):
            return False
        if self._target_has_clothing_block(target):
            return False
        penetrator_count = self._get_train_command_penetrator_count(assistant)
        return penetrator_count >= 2 and int(target.exp.get(1, 0)) >= 10




    def _is_train_command_available_basic(self, command_id: int, target: Character, clothing_enabled: bool, clothing_state: int, target_is_male: bool, duel_mode: bool, tentacle_mode: bool, beast_mode: bool, mouth_gagged: bool) -> Optional[bool]:
        if duel_mode:
            return False
        if command_id == 0:
            return True
        if command_id == 1:
            if target_is_male or tentacle_mode:
                return False
            if clothing_enabled and clothing_state & 17:
                return False
            return True
        if command_id == 2:
            if beast_mode:
                return False
            if clothing_enabled and clothing_state & 17:
                return False
            return True
        if command_id == 3:
            if target.talent.get(150, 0) == 1 or target.equipt.get(44, 0) > 0:
                return False
            if tentacle_mode or beast_mode:
                return False
            if clothing_enabled and clothing_state & 17:
                return False
            return True
        if command_id == 6:
            if target.talent.get(151, 0) == 1 or mouth_gagged or tentacle_mode:
                return False
            return True
        return None




    def _is_train_command_available_partnership(self, command_id: int, target: Character) -> Optional[bool]:
        if command_id == 30:
            return not target.talent.get(122, 0)
        if command_id == 40:
            return True
        if command_id == 50:
            player = self._get_player()
            return player is not None and player.item.get("润滑液", 0) > 0
        if command_id == 53:
            return True
        if command_id == 56:
            return True
        return None




    def _is_train_command_available_special(self, command_id: int, target: Character, clothing_enabled: bool, clothing_state: int, tentacle_mode: bool, beast_mode: bool) -> Optional[bool]:
        if command_id == 128:
            if target.talent.get(122, 0):
                return False
            if target.talent.get(135, 0):
                player = self._get_player()
                if player is None or not player.talent.get(83, 0):
                    return False
            if tentacle_mode or beast_mode:
                return False
            if clothing_enabled and (clothing_state & 17):
                return False
            player = self._get_player()
            if player is None:
                return False
            return bool(player.talent.get(121, 0) or player.talent.get(122, 0))
        if command_id in (129, 130, 131, 132, 133, 134):
            if target.talent.get(122, 0):
                return False
            if target.talent.get(135, 0):
                player = self._get_player()
                if player is None or not player.talent.get(83, 0):
                    return False
            if tentacle_mode:
                return False
            if clothing_enabled and (clothing_state & 17):
                return False
            player = self._get_player()
            if player is None:
                return False
            return bool(player.talent.get(121, 0) or player.talent.get(122, 0))
        return None




    def _is_train_video_recording(self, target: Character) -> bool:
        return int(target.cflag.get(498, 0)) == 1






    def _prompt_train_choice(self, target: Character, available_commands: List[int]) -> str:
        self._render_train_screen(target, available_commands)
        return self._prompt_choice()






    def _render_train_screen(self, target: Character, available_commands: List[int]) -> None:
        print(f"\n{'='*50}")
        print(f" Training: {target.name}")
        print(f" HP: {target.base.get(0, 0)}/{target.maxbase.get(0, 0)}")
        print(f" MP: {target.base.get(1, 0)}/{target.maxbase.get(1, 0)}")
        print(f" Submission: {self._get_submission_level(target)}")
        print(f"{'='*50}")

        print()
        for command_id in available_commands:
            print(f" [{command_id}] {self._get_train_command_name(command_id)}")
        print(" [10] Rest")
        print(" [100] Back to Menu")






    def _resolve_train_command_65_sequence(self, target: Character, assistant: Character, source: Dict[int, int], exp_delta: Dict[int, int]):
        self._apply_sex_virgin_break(assistant, target, exp_delta, submission_floor=3)
        self._apply_vaginal_sex_shared_effects(target, assistant)
        self._apply_sex_ejaculation_to_receiver(target, assistant, exp_delta, source, assistant, 3)
        self._add_same_sex_exp(exp_delta, target, assistant, female_value=10, male_value=10)






    def _start_train_video_recording(self, target: Character) -> None:
        target.cflag[498] = 1
        target.cflag[491] = 0
        for offset in range(10):
            target.cflag[480 + offset] = 0
        target.cflag[22] = self._build_train_video_equip_mask(target)
        self._clear_train_video_frames(target)






    def _store_train_snapshot(self, target: Character, losebase: Dict[int, int], source: Dict[int, int]):
        # Keep only the current command's calculated SOURCE/LOSEBASE values.
        target.losebase = {key: value for key, value in losebase.items() if value}
        target.source = {key: value for key, value in source.items() if value}






    def _store_train_video_frame(self, target: Character, frame_index: int, command_id: int) -> None:
        if 0 <= frame_index < 10:
            target.cflag[460 + frame_index] = command_id






    def execute_train_command(self, command: str, target: Character):
        """Execute a training command"""
        print()
        player = self._get_player()
        target_idx = self._find_character_index(target)

        dispatched = self._dispatch_train_command(command, target, player)
        if dispatched and command != "53":
            self._capture_train_video_after_command(target, int(command), player)
        if dispatched and target_idx > 0:
            self._set_last_training_target_index(target_idx)
        if dispatched:
            self._apply_aftertrain_event(target)
            self._apply_aftertrain_followup_checks(target)
        if not dispatched:
            print(f"{self._get_train_command_name(int(command))}")
            print("这个指令还没有接入。")

        self._pause()




    def run_train(self):
        """Run training mode"""
        while True:
            next_state = self._advance_train_menu()
            if next_state is not None:
                return next_state





