from __future__ import annotations
"""Module for AftertrainMixin - after-training and sexual effect apply methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class AftertrainMixin:
    """Mixin providing after-training and sexual effect apply methods"""
    def _apply_aftertrain_analsex_check(self, target: Character) -> int:
        if int(target.talent.get(85, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            return 0
        if int(target.exp.get(5, 0)) < 30:
            return 0
        player = self._get_player()
        if player is None or (int(player.talent.get(122, 0)) == 0 and int(player.talent.get(121, 0)) == 0):
            return 0
        if int(target.base.get(0, 0)) < 500:
            return 0
        count = 0
        if int(target.abl.get(3, 0)) == 4:
            count += 1
        elif int(target.abl.get(3, 0)) == 5:
            count += 2
        elif int(target.abl.get(3, 0)) >= 6:
            count += 3
        if int(target.abl.get(30, 0)):
            count += int(target.abl.get(30, 0)) // 2 + 1
        if count <= 0:
            return
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 2
        if int(target.abl.get(11, 0)) == 4 and int(target.abl.get(16, 0)) >= 4 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.talent.get(85, 0)):
            count += 1
        if int(target.talent.get(76, 0)):
            count += 1
        if int(target.talent.get(75, 0)):
            count += 2
        if int(target.talent.get(70, 0)):
            count += 1
        elif int(target.talent.get(71, 0)):
            count -= 2
        if count <= 0:
            return 0
        self._emit_aftertrain_separator()
        print(f"{player.name if player is not None else '主人'}和{target.name}抑制不住无法冷却的兴奋，")
        print(f"回到床上做了{count}次…")
        self._run_self_kojo(target, 4)
        self._add_exp_delta(target, {1: count, 5: count})
        self._add_juel(2, count * 200)
        self._add_juel(4, count * 100)
        self._add_juel(5, count * 250)
        return 1

    def _apply_aftertrain_beastsex_check(self, target: Character, masturbation_count: int) -> int:
        if int(target.abl.get(39, 0)) <= 0:
            return 0
        if int(target.talent.get(135, 0)):
            return 0
        if int(target.exp.get(56, 0)) < 50:
            return 0
        if int(target.talent.get(0, 0)) or int(target.talent.get(122, 0)) == 1:
            return 0
        if int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64):
            return 0
        if int(target.cflag.get(273, 0)):
            return 0
        if int(self.interpreter.vars.item[22]) == 0:
            return 0
        if int(target.base.get(0, 0)) < 500:
            return 0
        count = self._calculate_aftertrain_beastsex_count(target)
        if count <= 0:
            return 0
        self._emit_aftertrain_separator()
        print(f"之后，{target.name}悄悄地去了饲养狗的狗舍，", end="")
        print(f"进行了{count}次交配。")
        self._add_exp_delta(target, {56: count, 0: count, 5: count})
        self._add_juel(1, count * 200)
        self._add_juel(6, count * 300)
        self._add_juel(8, count * 200)
        if int(target.abl.get(10, 0)) + int(target.abl.get(17, 0)) + int(target.abl.get(21, 0)) >= 12 and int(self.interpreter.vars.time) == 0:
            print(f"在那之后{target.name}", end="")
            if int(target.talent.get(124, 0)):
                print("摇着尾巴，", end="")
            print("来报告了。")
            self._add_juel(8, count * 200)
        return 1

    def _apply_aftertrain_event(self, target: Character) -> None:
        if int(target.template_id) != 35:
            return
        current = int(self.interpreter.vars.globals.get(2807, 0))
        if 160 <= current < 170 and self._get_train_menu_target() is target:
            self.interpreter.vars.globals[2807] = 170

    def _apply_aftertrain_followup_checks(self, target: Character) -> None:
        # 对应 SELF_CHECK 开头：SIF CFLAG:MASTER:61 → CFLAG:MASTER:61 = 0
        # （逆强奸标记在调教结束时统一清零，避免影响下轮）
        player = self._get_player()
        if player is not None and int(player.cflag.get(61, 0)):
            player.cflag[61] = 0
        if target is None:
            return
        if int(self.interpreter.vars.tflag[899]) >= 1:
            return
        assistant = self._get_current_assistant()
        intercourse_occurred = self._apply_aftertrain_intercourse_check(target)
        lesbian_count = self._apply_aftertrain_lesbiansex_check(target, intercourse_occurred)
        masturbation_count = self._apply_aftertrain_masturbation_check(target, assistant, intercourse_occurred, lesbian_count)
        self._apply_aftertrain_beastsex_check(target, masturbation_count)

    def _apply_aftertrain_intercourse_check(self, target: Character) -> int:
        if int(target.talent.get(122, 0)) or (int(target.talent.get(122, 0)) == 0 and int(target.abl.get(2, 0)) < int(target.abl.get(3, 0))) or (int(target.talent.get(0, 0)) and int(target.abl.get(3, 0)) >= 3):
            return self._apply_aftertrain_analsex_check(target)
        return self._apply_aftertrain_sex_check(target)

    def _apply_aftertrain_lesbiansex_check(self, target: Character, intercourse_occurred: int) -> int:
        assistant = self._get_current_assistant()
        if assistant is None:
            return 0
        if int(target.abl.get(22, 0)) < 2 or int(target.abl.get(0, 0)) < 3 or int(target.abl.get(10, 0)) < 2 or int(target.abl.get(11, 0)) < 2:
            return 0
        if int(target.talent.get(122, 0)) or int(assistant.talent.get(122, 0)):
            return 0
        if int(target.base.get(0, 0)) < 500:
            return 0
        if int(target.abl.get(33, 0)) == 0 and int(assistant.abl.get(33, 0)) == 0:
            return 0
        plays = self._calculate_aftertrain_lesbian_play_count(target, assistant)
        if plays <= 0:
            return 0
        if intercourse_occurred == 1:
            self._emit_aftertrain_separator()
            player = self._get_player()
            print(f"{player.name if player is not None else '主人'}出去之后，", end="")
        else:
            print("调教结束之后，", end="")
        print(f"{target.name}和{assistant.name}好像又百合PLAY了{plays}回。")
        self._run_self_kojo(target, 2)
        self._add_exp_delta(target, {40: plays * 20, 2: plays * 100 * int(target.abl.get(10, 0)) // 500})
        self._add_juel(0, plays * 100 * int(target.abl.get(10, 0)))
        self._add_juel(5, plays * 200)
        if int(assistant.talent.get(121, 0)):
            self._add_exp_delta(target, {20: plays})
            self._add_juel(6, plays * 100 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0))))
            self._add_juel(7, plays * 100 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0))))
        else:
            self._add_juel(6, plays * 50 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0))))
            self._add_juel(7, plays * 50 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0))))
        if int(assistant.talent.get(83, 0)):
            self._add_exp_delta(target, {30: plays})
            self._add_juel(9, plays * 100 * int(target.abl.get(21, 0)))
        if int(target.talent.get(121, 0)):
            self._add_exp_delta(target, {3: plays})
            self._add_juel(8, plays * 100)
        if int(target.talent.get(121, 0)) and int(assistant.talent.get(121, 0)) and int(target.abl.get(16, 0)) >= 3 and int(target.abl.get(32, 0)) >= 3:
            self._add_exp_delta(target, {21: plays, 22: plays})
            self._add_juel(5, plays * 100)
            self._add_juel(6, plays * 100)
            self._add_juel(8, plays * 100)
        return 1

    def _apply_aftertrain_masturbation_check(self, target: Character, assistant: Optional[Character], intercourse_count: int, lesbian_count: int) -> int:
        if int(target.abl.get(0, 0)) < 3 or int(target.abl.get(11, 0)) < 2:
            return 0
        if int(target.talent.get(150, 0)):
            return 0
        if int(target.base.get(0, 0)) < 500:
            return 0
        if int(target.abl.get(31, 0)) <= 0:
            return 0
        count = self._calculate_aftertrain_masturbation_count(target, assistant)
        if count <= 0:
            return 0
        self._emit_aftertrain_separator()
        print(f"{target.name}在", end="")
        if lesbian_count == 1 and assistant is not None:
            print(f"{assistant.name}出去之后，", end="")
        elif intercourse_count == 1:
            player = self._get_player()
            print(f"{player.name if player is not None else '主人'}出去之后，", end="")
        else:
            print("调教结束之后，", end="")
        fantasy, fantasy_kind = self._get_aftertrain_masturbation_fantasy(target, assistant, lesbian_count)
        print(f"好像一边想着{fantasy},一边自慰了{count}次。")
        self._run_self_kojo(target, 1)
        self._add_exp_delta(target, {10: count})
        self._add_juel(0, count * 500)
        self._add_juel(4, count * 100)
        self._add_juel(5, count * 250)
        if int(target.abl.get(10, 0)) + int(target.abl.get(17, 0)) + int(target.abl.get(21, 0)) >= 10 and int(self.interpreter.vars.time) == 0:
            print(f"在那之后{target.name}来报告了。")
            self._add_juel(8, count * 200)
        if (int(target.abl.get(10, 0)) >= 5 or int(target.abl.get(11, 0)) >= 5) and fantasy_kind == 0:
            print(f"无论自慰了多少次，也无法填满对{self._get_player().name if self._get_player() is not None else '主人'}的欲望。")
        elif (int(target.abl.get(11, 0)) >= 5 or int(target.abl.get(33, 0)) >= 3) and fantasy_kind == 1 and assistant is not None:
            print(f"无论自慰了多少次，也无法填满对{assistant.name}的欲望。")
        elif (int(target.abl.get(11, 0)) >= 5 or int(target.abl.get(39, 0)) >= 3) and fantasy_kind == 2:
            print("无论自慰了多少次，也无法填满对兽交的欲望。")
        return 1

    def _apply_aftertrain_sex_check(self, target: Character) -> int:
        if int(target.talent.get(135, 0)):
            return 0
        if int(target.talent.get(85, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            return 0
        if int(target.exp.get(5, 0)) < 30:
            return 0
        if int(target.talent.get(0, 0)) or int(target.talent.get(122, 0)) == 1:
            return 0
        if int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64):
            return 0
        if int(target.cflag.get(273, 0)):
            return 0
        player = self._get_player()
        if player is None or (int(player.talent.get(122, 0)) == 0 and int(player.talent.get(121, 0)) == 0):
            return 0
        if int(target.base.get(0, 0)) < 500:
            return 0
        count = 0
        if int(target.abl.get(2, 0)) == 4:
            count += 1
        elif int(target.abl.get(2, 0)) == 5:
            count += 2
        elif int(target.abl.get(2, 0)) >= 6:
            count += 3
        if int(target.abl.get(30, 0)):
            count += int(target.abl.get(30, 0)) // 2 + 1
        if count <= 0:
            return 0
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 2
        if int(target.abl.get(11, 0)) == 4 and int(target.abl.get(16, 0)) >= 4 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.talent.get(85, 0)):
            count += 1
        if int(target.talent.get(76, 0)):
            count += 1
        if int(target.talent.get(75, 0)):
            count += 2
        if int(target.talent.get(70, 0)):
            count += 1
        elif int(target.talent.get(71, 0)):
            count -= 2
        if count <= 0:
            return 0
        self._emit_aftertrain_separator()
        print(f"{player.name if player is not None else '主人'}和{target.name}抑制不住无法冷却的兴奋，")
        print(f"回到床上做了{count}次…")
        self._run_self_kojo(target, 4)
        self._add_exp_delta(target, {0: count, 5: count})
        self._add_juel(1, count * 200)
        self._add_juel(4, count * 100)
        self._add_juel(5, count * 250)
        return 1

    def _apply_assistant_sex_witness_effects(self, witness: Character, assistant: Character, exp_delta: Dict[int, int], source: Dict[int, int]):
        assistant.exp[0] = assistant.exp.get(0, 0) + 1
        assistant.exp[5] = assistant.exp.get(5, 0) + 1
        if witness.cflag.get(2, 0) >= 1000:
            exp_delta[23] = exp_delta.get(23, 0) + 2
        if witness.talent.get(85, 0):
            source[13] = self._scale_value(source.get(13, 0), 1.2)

    def _apply_breast_stimulation_bonus(self, target: Character, source: Dict[int, int], rear_mode: bool = False):
        breast_values = [50, 200, 500, 800, 1300, 1800] if not rear_mode else [20, 100, 500, 1200, 2000, 2800]
        source[17] = self._level_value(target.abl.get(1, 0), breast_values)
        source[3] = source.get(3, 0) + (50 if not rear_mode else 30)

    def _apply_hand_service_double_overflow(
        self,
        target: Character,
        player: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
        current_gauge: int,
        gauge_max: int,
    ) -> None:
        source[7] = self._scale_value(source.get(7, 0), 2.0)
        source[5] = self._scale_value(source.get(5, 0), 1.5)
        player.exp[3] = player.exp.get(3, 0) + 2
        exp_delta[20] = exp_delta.get(20, 0) + 3
        player.stain[2] = player.stain.get(2, 0) | 4
        self._add_pregnancy_source_amount(target, 1, 2)
        player.base[2] = max(0, current_gauge - gauge_max * 2)
        if player.base[2] >= gauge_max:
            player.base[2] = gauge_max - 1

    def _apply_hand_service_ejaculation(self, target: Character, player: Character, source: Dict[int, int], exp_delta: Dict[int, int]):
        if not self._player_has_service_target(player):
            return

        self._ensure_player_ejaculation_gauge(player)
        player.base[2] = player.base.get(2, 0) + self._build_hand_service_stimulation(target, player)
        current_gauge = player.base.get(2, 0)
        gauge_max = max(1, player.maxbase.get(2, 10000))
        if current_gauge <= gauge_max:
            return

        self._apply_hand_service_stimulation_overflow(target, player, source, exp_delta, current_gauge, gauge_max)

    def _apply_hand_service_single_overflow(
        self,
        target: Character,
        player: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
        current_gauge: int,
        gauge_max: int,
    ) -> None:
        player.exp[3] = player.exp.get(3, 0) + 1
        exp_delta[20] = exp_delta.get(20, 0) + 1
        player.stain[2] = player.stain.get(2, 0) | 4
        self._add_pregnancy_source_amount(target, 1, 1)
        player.base[2] = max(0, current_gauge - gauge_max)
        if player.base[2] >= gauge_max:
            player.base[2] = gauge_max - 1

    def _apply_hand_service_stimulation_overflow(
        self,
        target: Character,
        player: Character,
        source: Dict[int, int],
        exp_delta: Dict[int, int],
        current_gauge: int,
        gauge_max: int,
    ) -> None:
        source[4] = self._scale_value(source.get(4, 0), 3.0)
        semen_addiction = target.abl.get(32, 0)
        source[7] = self._level_value(semen_addiction, [0, 200, 600, 1500, 3000, 6000])
        source[5] = self._scale_value(source.get(5, 0), self._level_value(semen_addiction, [200, 250, 300, 400, 500, 600]) / 100.0)
        source[13] = self._scale_value(source.get(13, 0), self._level_value(semen_addiction, [200, 160, 100, 70, 40, 10]) / 100.0)
        if current_gauge > gauge_max * 2:
            self._apply_hand_service_double_overflow(target, player, source, exp_delta, current_gauge, gauge_max)
            return
        self._apply_hand_service_single_overflow(target, player, source, exp_delta, current_gauge, gauge_max)

    def _apply_rear_sex_adjustment(self, target: Character, source: Dict[int, int]):
        source[12] = 800
        source[3] = max(0, source.get(3, 0) - 100)
        exp_level = self._get_exp_level(target.exp.get(0, 0))
        if exp_level == 0:
            source[6] = 5000
        elif exp_level == 1:
            source[6] = 220
        elif exp_level == 2:
            source[6] = 30
        elif exp_level == 3:
            source[6] = 5

    def _apply_rear_spanking_followup_bonus(self, target: Character, source: Dict[int, int]):
        source[10] = max(source.get(10, 0), 300)
        source[13] = max(source.get(13, 0), 500)
        maso_level = target.abl.get(21, 0)
        source[10] = self._scale_value(source.get(10, 0), self._level_value(maso_level, [80, 100, 120, 140, 180, 250]) / 100.0)
        source[13] = self._scale_value(source.get(13, 0), self._level_value(maso_level, [80, 100, 130, 180, 260, 400]) / 100.0)

    def _apply_sex_ejaculation_to_receiver(self, actor: Character, receiver: Character, exp_delta: Dict[int, int], source: Dict[int, int], pregnancy_target: Optional[Character], pregnancy_source: int):
        if not self._player_has_service_target(actor):
            return
        self._ensure_player_ejaculation_gauge(actor)
        actor.base[2] = actor.base.get(2, 0) + self._build_sex_stimulation_gain(actor, receiver)
        current_gauge = actor.base.get(2, 0)
        gauge_max = max(1, actor.maxbase.get(2, 10000))
        if current_gauge <= gauge_max:
            return

        source[4] = self._scale_value(source.get(4, 0), 3.0)
        if current_gauge > gauge_max * 2:
            actor.exp[3] = actor.exp.get(3, 0) + 2
            exp_delta[20] = exp_delta.get(20, 0) + 1
            actor.stain[2] = actor.stain.get(2, 0) | 4
            self._add_pregnancy_source_amount(pregnancy_target, pregnancy_source, 2)
            actor.base[2] = max(0, current_gauge - gauge_max * 2)
        else:
            actor.exp[3] = actor.exp.get(3, 0) + 1
            actor.stain[2] = actor.stain.get(2, 0) | 4
            self._add_pregnancy_source_amount(pregnancy_target, pregnancy_source, 1)
            actor.base[2] = max(0, current_gauge - gauge_max)
        if actor.base[2] >= gauge_max:
            actor.base[2] = gauge_max - 1

    def _apply_sp_sex_bonus(self, target: Character, source: Dict[int, int], rear_mode: bool = False):
        if rear_mode:
            source[0] = self._level_value(target.abl.get(0, 0), [20, 100, 500, 1200, 2000, 2800])
            source[17] = self._level_value(target.abl.get(1, 0), [20, 100, 600, 1400, 2200, 3200])
            source[3] = source.get(3, 0) + self._level_value(target.abl.get(1, 0), [50, 100, 200, 300, 600, 1000])
        else:
            source[0] = self._level_value(target.abl.get(0, 0), [20, 100, 500, 1200, 2000, 2800])
            source[17] = self._level_value(target.abl.get(1, 0), [20, 100, 500, 1200, 2000, 2800])
            source[3] = self._level_value(target.abl.get(1, 0), [50, 100, 160, 200, 230, 250])
        source[12] = max(source.get(12, 0), 400 if not rear_mode else 800)

    def _apply_spanking_sex_bonus(self, target: Character, source: Dict[int, int]):
        source[10] = 800
        source[12] = 800
        source[13] = max(800, source.get(13, 0))
        source[14] = 500
        pain_level = self._get_palam_level(target.palam.get(9, 0))
        source[6] = self._level_value(pain_level, [300, 500, 800, 1200, 1800, 1800])
        maso_level = target.abl.get(21, 0)
        source[10] = self._scale_value(source.get(10, 0), self._level_value(maso_level, [80, 100, 120, 140, 200, 300]) / 100.0)
        source[13] = self._scale_value(source.get(13, 0), self._level_value(maso_level, [80, 100, 150, 300, 500, 800]) / 100.0)

    def _apply_threesome_ejaculation(self, player: Character, assistant: Character, target: Character, mode_pair: tuple[int, int], source: Dict[int, int], exp_delta: Dict[int, int]):
        player_mode, assistant_mode = mode_pair
        if player_mode == 1:
            self._apply_sex_ejaculation_to_receiver(player, target, exp_delta, source, target, 1)
        else:
            self._apply_sex_ejaculation_to_receiver(player, target, exp_delta, source, None, 1)
        if assistant_mode == 1:
            self._apply_sex_ejaculation_to_receiver(assistant, target, exp_delta, source, target, 2)
        else:
            self._apply_sex_ejaculation_to_receiver(assistant, target, exp_delta, source, None, 2)

    def _apply_threesome_penetration_effects(self, target: Character, mode_pair: tuple[int, int], source: Dict[int, int], exp_delta: Dict[int, int]):
        if 1 in mode_pair:
            source[1] = self._level_value(target.abl.get(2, 0), [40, 150, 400, 1000, 1700, 2200])
            target.exp[0] = target.exp.get(0, 0) + 1
            target.exp[5] = target.exp.get(5, 0) + 1
            exp_delta[0] = exp_delta.get(0, 0) + 1
            exp_delta[5] = exp_delta.get(5, 0) + 1
        if 2 in mode_pair:
            source[2] = self._level_value(target.abl.get(3, 0), [10, 30, 500, 1000, 1700, 2200])
            source[13] = max(source.get(13, 0), self._level_value(target.abl.get(3, 0), [100, 700, 1500, 3000, 5000, 8000]))
            target.exp[1] = target.exp.get(1, 0) + 5
            target.exp[5] = target.exp.get(5, 0) + 1
            exp_delta[1] = exp_delta.get(1, 0) + 5
            exp_delta[5] = exp_delta.get(5, 0) + 1
        if 3 in mode_pair:
            source[4] = self._level_value(target.abl.get(16, 0), [420, 500, 580, 660, 740, 820])
            source[5] = self._level_value(target.abl.get(16, 0), [150, 300, 600, 900, 1500, 2200])

    def _apply_vaginal_sex_shared_effects(self, actor: Character, receiver: Character):
        receiver.exp[0] = receiver.exp.get(0, 0) + 1
        receiver.exp[5] = receiver.exp.get(5, 0) + 1
        if actor.talent.get(119, 0) or actor.talent.get(121, 0) or actor.talent.get(122, 0):
            actor.stain[2] = actor.stain.get(2, 0) | receiver.stain.get(3, 0)
            receiver.stain[3] = receiver.stain.get(3, 0) | actor.stain.get(2, 0)

