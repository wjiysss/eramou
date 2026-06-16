from __future__ import annotations
"""Module for GodnessMixin - 女神事件"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class GodnessMixin:
    """Mixin providing 女神事件 methods for GameEngine"""

    def _advance_godness_black_route(self, char: Character, current: int, favor: int, total_days: int):
        if char.talent.get(76, 0) != 1:
            return
        self._route_godness_black_stage(char, current, favor, total_days)






    def _advance_godness_story_stage_after_scene(self, stage: int) -> None:
        current = int(self.interpreter.vars.globals.get(2810, 0))
        scene_stage_advances = {
            110: 111,
            130: 131,
            140: 141,
            160: 161,
            170: 171,
            180: 181,
            190: 191,
            200: 201,
            540: 541,
        }
        target = scene_stage_advances.get(stage)
        if target is not None and current == stage:
            self.interpreter.vars.globals[2810] = target






    def _apply_godness_endcheck(self, char: Character):
        current = int(self.interpreter.vars.globals.get(2810, 0))
        favor = int(char.cflag.get(2, 0))
        total_days = self._get_total_day_count()
        current = self._sync_godness_endcheck_route(char, current)
        self._advance_godness_black_route(char, current, favor, total_days)






    def _apply_godness_ending_stage_effects(self, stage: int) -> None:
        if stage == 150:
            self._apply_godness_escape_losses()
            self.interpreter.vars.globals[2810] = 540
        elif stage == 200:
            self.interpreter.vars.globals[2801] = 99






    def _apply_godness_ending_stage_output(self, messages: List[str], stage: int, event_key: str) -> None:
        for line in self._build_godness_event_lines(stage):
            messages.append(line)
        self._apply_godness_ending_stage_effects(stage)
        self._mark_ending_event_seen(event_key)
        self._advance_godness_story_stage_after_scene(stage)






    def _apply_godness_escape_losses(self):
        self.interpreter.vars.globals[99] = max(0, int(self.interpreter.vars.globals.get(99, 0)) - 50)
        self._halve_godness_escape_monster_stock()
        self._apply_godness_escape_party_damage()
        current_money = max(0, int(self.interpreter.vars.money))
        new_money = int(current_money * 0.8)
        lost_money = current_money - new_money
        self.interpreter.vars.money = new_money
        self.interpreter.vars.globals[4444] = int(self.interpreter.vars.globals.get(4444, 0)) - lost_money
        self._remove_character_by_template_id(33, departure_slot=85)






    def _apply_godness_escape_party_damage(self):
        for char in self.interpreter.vars.chars[1:]:
            char.base[0] = max(1, int(char.base.get(0, 0)) - 800)
            char.base[1] = max(0, int(char.base.get(1, 0)) - 1000)






    def _apply_godness_stage_120_choice_join(self, event_key: str) -> None:
        godness = self._find_character_by_template_id(33)
        favor = int(godness.cflag.get(2, 0)) if godness is not None else 0
        advanced = False
        if 3000 <= favor < 5000:
            self.interpreter.vars.globals[2810] = 122
            advanced = True
        elif 2500 <= favor < 4000:
            self.interpreter.vars.globals[2810] = 121
            advanced = True
        if advanced:
            self._mark_ending_event_seen(event_key)
        self._pause()






    def _apply_godness_stage_120_choice_watch(self, event_key: str) -> None:
        self.interpreter.vars.globals[2810] = 121
        self._mark_ending_event_seen(event_key)
        self._pause()






    def _build_godness_event_lines(self, stage: int) -> List[str]:
        return self._build_stage_lines(stage, GODNESS_EVENT_LINES)






    def _get_godness_ending_event_key(self, stage: int) -> Optional[str]:
        stage_to_key = {
            110: "ending_godness_scene_110",
            120: "ending_godness_scene_120",
            130: "ending_godness_scene_130",
            140: "ending_godness_scene_140",
            150: "ending_godness_scene_150",
            540: "ending_godness_scene_540",
            160: "ending_godness_scene_160",
            170: "ending_godness_scene_170",
            180: "ending_godness_scene_180",
            190: "ending_godness_scene_190",
            200: "ending_godness_scene_200",
        }
        return stage_to_key.get(stage)






    def _halve_godness_escape_monster_stock(self):
        stock = self._get_monster_stock()
        for monster_id in range(100, 201):
            current = int(stock.get(monster_id, 0))
            if current <= 0:
                continue
            reduced = current // 2
            if monster_id < 190 and reduced <= 30:
                reduced = 30
            stock[monster_id] = max(0, reduced)






    def _process_godness_ending_events(self, messages: List[str]):
        stage = int(self.interpreter.vars.globals.get(2810, 0))
        event_key = self._get_godness_ending_event_key(stage)
        if not event_key or self._has_seen_ending_event(event_key):
            return
        if stage == 120:
            self._queue_post_message_action({"kind": "godness_stage_120_prompt", "event_key": event_key})
            return
        self._apply_godness_ending_stage_output(messages, stage, event_key)






    def _prompt_godness_stage_120_choice(self, event_key: str):
        for line in self._build_godness_event_lines(120):
            print(line)
        print(" [1] 「想要肉棒是吗」")
        print(" [2] 呵呵，有趣")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                self._apply_godness_stage_120_choice_join(event_key)
                return
            if choice == "2":
                self._apply_godness_stage_120_choice_watch(event_key)
                return






    def _route_godness_black_stage(self, char: Character, current: int, favor: int, total_days: int):
        if favor >= 2000 and current < 10:
            self._route_godness_black_stage_to_110(char)
        elif 110 <= current < 120:
            self._route_godness_black_stage_110_119(char, favor)
        elif 110 <= current < 130:
            self._route_godness_black_stage_120_129(char, favor)
        elif 130 <= current < 140:
            self._route_godness_black_stage_130_139(char)
        elif 140 <= current < 150:
            self._route_godness_black_stage_140_149(char, total_days)
        elif current == 560:
            self._route_godness_black_stage_560(char, total_days)
        elif 160 <= current < 170:
            self._route_godness_black_stage_160_169(char, total_days)
        elif 170 <= current < 180:
            self._route_godness_black_stage_170_179(char, total_days)
        elif 180 <= current < 190:
            self._route_godness_black_stage_180_189(char, total_days)
        elif current == 300 and self._advance_story_wait_counter(char, 300, 310):
            self.interpreter.vars.globals[2810] = 310






    def _route_godness_black_stage_110_119(self, char: Character, favor: int) -> None:
        if favor <= 5000 and int(char.cflag.get(515, 0)) >= 70:
            self.interpreter.vars.globals[2810] = 120
        char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_120_129(self, char: Character, favor: int) -> None:
        char.cflag[515] = int(char.cflag.get(515, 0)) + 1
        if favor >= 8000:
            self.interpreter.vars.globals[2810] = 130






    def _route_godness_black_stage_130_139(self, char: Character) -> None:
        char.cflag[515] = int(char.cflag.get(515, 0)) + 1
        if int(char.abl.get(10, 0)) + int(char.abl.get(16, 0)) >= 14:
            self.interpreter.vars.globals[2810] = 140






    def _route_godness_black_stage_140_149(self, char: Character, total_days: int) -> None:
        if int(char.cflag.get(515, 0)) >= 150 and total_days >= 350 and self._find_character_by_template_id(34) is not None:
            self.interpreter.vars.globals[2810] = 150
        else:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_160_169(self, char: Character, total_days: int) -> None:
        if int(char.cflag.get(515, 0)) >= 200 and total_days >= 350 and self._find_character_by_template_id(33) is not None:
            self.interpreter.vars.globals[2810] = 170
        else:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_170_179(self, char: Character, total_days: int) -> None:
        if int(char.cflag.get(515, 0)) >= 220 and total_days >= 350 and self._find_character_by_template_id(33) is not None:
            self.interpreter.vars.globals[2810] = 180
        else:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_180_189(self, char: Character, total_days: int) -> None:
        if int(char.cflag.get(515, 0)) >= 250 and total_days >= 350 and self._find_character_by_template_id(33) is not None:
            self.interpreter.vars.globals[2810] = 190
        else:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_560(self, char: Character, total_days: int) -> None:
        if int(char.cflag.get(515, 0)) >= 180 and total_days >= 350:
            self.interpreter.vars.globals[2810] = 160
        else:
            char.cflag[515] = int(char.cflag.get(515, 0)) + 1






    def _route_godness_black_stage_to_110(self, char: Character) -> None:
        self.interpreter.vars.globals[2810] = 110
        char.cflag[515] = 0






    def _sync_godness_endcheck_route(self, char: Character, current: int) -> int:
        if char.talent.get(85, 0) == 1 and 110 <= current <= 200:
            self.interpreter.vars.globals[2810] = 10
            char.cflag[515] = 0
            return 10
        if char.talent.get(76, 0) == 1 and ((30 <= current <= 100) or (300 <= current <= 310)):
            self.interpreter.vars.globals[2810] = 110
            char.cflag[515] = 0
            return 110
        return current






    def _sync_godness_post_escape_progress(self) -> None:
        current = int(self.interpreter.vars.globals.get(2810, 0))
        if not (540 <= current < 550):
            return
        if int(self.interpreter.vars.get_flag(93, 0)) != 3:
            return
        self.interpreter.vars.globals[2810] = 560





