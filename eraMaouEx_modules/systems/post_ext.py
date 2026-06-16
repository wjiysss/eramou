from __future__ import annotations
"""Module for PostExtMixin - 后续处理"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class PostExtMixin:
    """Mixin providing 后续处理 methods for GameEngine"""

    def _handle_post_message_godness_stage_120_prompt(self, action: Dict[str, Any]):
        self._prompt_godness_stage_120_choice(str(action.get("event_key", "")))






    def _handle_post_message_human_conquest_followup(self, action: Dict[str, Any]):
        self._prompt_human_conquest_followup()






    def _handle_post_message_normal_end_followup(self, action: Dict[str, Any]):
        self._prompt_normal_end_followup()






    def _handle_post_message_princess_ending_prompt(self, action: Dict[str, Any]):
        self._prompt_princess_ending_choice(str(action.get("event_key", "")))






    def _handle_post_message_princess_stage_20_prompt(self, action: Dict[str, Any]):
        self._prompt_princess_stage_20_choice(str(action.get("event_key", "")))






    def _handle_post_message_princess_stage_50_prompt(self, action: Dict[str, Any]):
        self._prompt_princess_stage_50_choice(str(action.get("event_key", "")))






    def _handle_post_message_princess_witch_ending_prompt(self, action: Dict[str, Any]):
        self._prompt_princess_witch_ending_choice(str(action.get("event_key", "")))






    def _handle_post_message_spade_departure_prompt(self, action: Dict[str, Any]):
        self._prompt_spade_departure_choice(str(action.get("event_key", "")))






    def _handle_post_message_spade_love_ending_prompt(self, action: Dict[str, Any]):
        self._prompt_spade_love_ending_choice(str(action.get("event_key", "")))






    def _handle_post_message_spade_milk_ending_prompt(self, action: Dict[str, Any]):
        self._prompt_spade_milk_ending_choice(str(action.get("event_key", "")))






    def _handle_post_message_square_departure_prompt(self, action: Dict[str, Any]):
        self._prompt_square_departure_choice(str(action.get("event_key", "")))






    def _handle_post_message_square_love_ending_prompt(self, action: Dict[str, Any]):
        self._prompt_square_love_ending_choice(str(action.get("event_key", "")))






    def _handle_post_message_story_branch_prompt(self, action: Dict[str, Any]):
        for line in action.get("lines", []):
            print(line)
        self._prompt_story_branch_selection(
            str(action.get("event_key", "")),
            int(action.get("global_flag", 0)),
            main_flag_delta=int(action.get("main_flag_delta", 2)),
        )





