from __future__ import annotations
"""Module for EventApplyMixin - event and ending effect apply methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EventApplyMixin:
    """Mixin providing event and ending effect apply methods"""
    def _apply_dog_walk_event(self) -> List[str]:
        if self.interpreter.vars.items.get(22, 0) == 0:
            return []

        walker_idx = self._get_dog_walk_target()
        if walker_idx == 0:
            return ["你带着野狗去散步了。"]

        walker = self.interpreter.vars.chars[walker_idx]
        play = self._get_dog_walk_play_score(walker)
        open_score = self._get_dog_walk_open_score(walker)
        no_sex = self._is_dog_walk_no_sex(walker)
        messages = [f"{walker.name} 和野狗一起去散步了。"]

        if play <= 0:
            return messages

        walker.exp[56] = walker.exp.get(56, 0) + 1
        line = self._build_dog_walk_event_line(walker, play, no_sex)
        if open_score > 0:
            messages.extend(self._apply_dog_walk_open_score_effect(walker, play, line))
            return messages
        messages.append(line)
        return messages

    def _apply_dog_walk_open_score_effect(self, walker: Character, play: int, line: str) -> List[str]:
        walker.juel[8] = walker.juel.get(8, 0) + 5 * play
        return [
            f"{line} 路人面前的露出感也让她更兴奋。",
            f"{walker.name} 因为当众暴露而积累了更多羞耻。",
        ]

    def _apply_ending_event_triggers(self, messages: List[str]):
        total_days = self._get_total_day_count()
        self._apply_normal_ending_event(messages, total_days)

        self._process_princess_ending_events(messages)
        self._process_square_ending_events(messages)
        self._process_spade_ending_events(messages)
        self._process_godness_ending_events(messages)
        self._apply_general_ending_branch_events(messages)

    def _apply_fullmoon_effect(self, char) -> None:
        """满月效果 - 对应 @FULLMOON_EFFECT
        满月时根据角色种族调整基础数值
        """
        # 种族2优先
        if char.talent.get(220, 0):
            race2 = char.talent.get(318, 0)  # 种族2
            if race2 == 4:
                # 植物
                char.cflag[11] = char.cflag.get(11, 0) * 2
                char.base[0] = char.maxbase.get(0, 1000)
                char.base[1] = char.maxbase.get(1, 500)
            elif race2 in (5, 11):
                # 触手
                char.cflag[11] = char.cflag.get(11, 0) * 5
                char.base[0] = char.maxbase.get(0, 1000)
                char.base[1] = char.maxbase.get(1, 500)
            elif race2 == 6:
                # 妖精
                char.cflag[11] = char.cflag.get(11, 0) * 2
                char.base[0] = char.maxbase.get(0, 1000) * 2
                char.base[1] = char.maxbase.get(1, 500) * 2
            else:
                char.cflag[11] = char.cflag.get(11, 0) * 2
                char.base[1] = char.maxbase.get(1, 500)
            return

        # 种族1
        race = char.talent.get(317, 0)  # 种族
        if race == 2:
            # 狼人
            char.cflag[11] = char.cflag.get(11, 0) * 10
            char.cflag[12] = char.cflag.get(12, 0) * 10
            char.base[0] = char.maxbase.get(0, 1000)
            char.base[1] = char.maxbase.get(1, 500)
        elif race == 3:
            # 吸血鬼
            char.cflag[11] = max(char.cflag.get(11, 0), char.cflag.get(13, 0))
            char.cflag[12] = max(char.cflag.get(12, 0), char.cflag.get(14, 0))
            char.base[0] = char.maxbase.get(0, 1000) * 10
            char.base[1] = char.maxbase.get(1, 500) * 10
        elif race == 6:
            # 天使
            char.base[1] = char.maxbase.get(1, 500) // 2
        elif race == 7:
            # 暗精灵
            char.cflag[11] = char.cflag.get(11, 0) * 2
            char.base[0] = char.maxbase.get(0, 1000)
            char.base[1] = char.maxbase.get(1, 500)
        elif race == 8:
            # 堕天使
            char.cflag[11] = char.cflag.get(11, 0) * 2
        elif race == 9:
            # 魔族
            char.cflag[11] = char.cflag.get(11, 0) * 2
        self.interpreter.vars.set_flag(0, 0)

    # ========================================
    # IKAI_BONUS - 异界奖励系统
    # 对应 ERB/IKAI_BONUS.ERB
    # ========================================

    def _apply_general_ending_branch_event(
        self,
        messages: List[str],
        branch: tuple[int, str, str, str, str, int, int],
    ) -> None:
        flag_id, event_key, label, rise_text, fall_text, threshold, main_flag_delta = branch
        self._process_general_story_branch_event(
            messages,
            flag_id,
            event_key,
            label,
            rise_text,
            fall_text,
            threshold,
            main_flag_delta=main_flag_delta,
        )

    def _apply_general_ending_branch_events(self, messages: List[str]):
        for branch in self._build_general_ending_branch_events():
            self._apply_general_ending_branch_event(messages, branch)

    def _apply_morning_fellatio_event(self) -> List[str]:
        player = self._get_player()
        if player is None or not (player.talent.get(121, 0) or player.talent.get(122, 0)):
            return []

        candidates = self._list_morning_fellatio_candidates()
        if not candidates:
            return []

        _, char, score = random.choice(candidates)
        exp_gain = max(1, score)
        semen_gain = score // 2
        char.exp[22] = char.exp.get(22, 0) + exp_gain
        char.exp[20] = char.exp.get(20, 0) + semen_gain
        char.juel[4] = char.juel.get(4, 0) + exp_gain * 100
        char.juel[6] = char.juel.get(6, 0) + exp_gain * 30
        char.juel[7] = char.juel.get(7, 0) + exp_gain * 40
        char.stain[0] = char.stain.get(0, 0) | 4
        messages = [
            f"早上，你是在 {char.name} 的口交中醒来的。",
            f"{char.name} 带着淫媚的笑容抬起沾满精液的脸，完成了早晨的问候。",
        ]
        messages.extend(self._get_morning_fellatio_kojo_lines(char))
        return messages

    def _apply_night_stalking_anal_path(self, char: Character, play: int) -> List[str]:
        if char.abl.get(3, 0) <= 4:
            play += 1
        elif char.abl.get(3, 0) == 5:
            play += 2
        else:
            play += 4
        char.exp[1] = char.exp.get(1, 0) + play
        char.exp[5] = char.exp.get(5, 0) + play
        char.juel[2] = char.juel.get(2, 0) + play * 400
        char.juel[4] = char.juel.get(4, 0) + play * 250
        char.juel[5] = char.juel.get(5, 0) + play * 250
        return [
            f"入睡前，{char.name} 突然跑进了你的房间。",
            f"{char.name} 渴求着你的拥抱，用后穴索求了 {play} 次欢爱后才依偎着睡去。",
        ]

    def _apply_night_stalking_event(self) -> List[str]:
        player = self._get_player()
        if player is None or not (player.talent.get(121, 0) or player.talent.get(122, 0)):
            return []

        candidates = self._collect_night_stalking_candidates()
        if not candidates:
            return []

        _, char = random.choice(candidates)
        return self._apply_night_stalking_for_character(char)

    def _apply_night_stalking_for_character(self, char: Character) -> List[str]:
        use_v = self._can_night_stalking_use_v(char)
        play = int(char.abl.get(30, 0))
        if use_v:
            return self._apply_night_stalking_v_path(char, play)
        return self._apply_night_stalking_anal_path(char, play)

    def _apply_night_stalking_messages(self) -> List[str]:
        return self._apply_night_stalking_event()

    def _apply_night_stalking_v_path(self, char: Character, play: int) -> List[str]:
        if char.abl.get(2, 0) <= 4:
            play += 1
        elif char.abl.get(2, 0) == 5:
            play += 2
        else:
            play += 4
        char.exp[0] = char.exp.get(0, 0) + play
        char.exp[5] = char.exp.get(5, 0) + play
        char.juel[1] = char.juel.get(1, 0) + play * 400
        char.juel[4] = char.juel.get(4, 0) + play * 250
        char.juel[5] = char.juel.get(5, 0) + play * 250
        return [
            f"入睡前，{char.name} 突然跑进了你的房间。",
            f"{char.name} 渴求着你的拥抱，在 {play} 次交合后才心满意足地沉沉睡去。",
        ]

    def _apply_normal_ending_event(self, messages: List[str], total_days: int):
        if int(self.interpreter.vars.globals.get(2801, 0)) != 99 or total_days != 500:
            return
        event_key = "ending_normal_end"
        if self._has_seen_ending_event(event_key):
            return
        messages.extend(self._build_normal_end_lines())
        self._mark_ending_event_seen(event_key)
        self._queue_post_message_action({"kind": "normal_end_followup"})

    def _apply_post_calendar_day_enemy_entries(self) -> List[str]:
        return self._apply_daily_enemy_reinforcement()

    def _apply_special_daily_enemy_entries(self) -> List[str]:
        messages: List[str] = []
        for spawn_func in [self._spawn_lily_special_enemy, self._spawn_crazylord_special_enemy]:
            message = spawn_func()
            if message is not None:
                messages.append(message)
        return messages

    def _apply_story_ending_main_completion(self) -> None:
        current_main = int(self.interpreter.vars.globals.get(2801, 0))
        if current_main >= 99:
            return
        if current_main <= 90:
            current_main = 90
        self.interpreter.vars.globals[2801] = current_main + 1

