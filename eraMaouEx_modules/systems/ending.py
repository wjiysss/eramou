from __future__ import annotations
"""Module for EndingMixin - Ending condition check and data loading methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EndingMixin:
    """Mixin providing Ending condition check and data loading methods"""
    def _check_ending(self) -> Optional[str]:
        """Check if any ending condition is met, return ending ID.
        Corresponds to ERB @ENDCHECK, @ENDCHECKMAIN, @ENDCHECKCHARA.
        """
        v = self.interpreter.vars

        # Apply endcheck main flags first
        self._apply_endcheck_main_flags()

        # Reset story flags for missing characters
        self._refresh_story_presence_flags()

        # Check character-specific endings
        self._apply_endcheck_characters()

        # Check main storyline flag
        main_flag = int(v.globals.get(2801, 0))

        # Normal End: 500 days and main flag is 99
        total_days = self._get_total_day_count()
        if main_flag == 99 and total_days >= 500:
            return "N"

        # Good End: main flag reached 10 (character endings completed)
        if main_flag >= 10:
            return "1"

        # Check area conquest endings
        if int(v.flags.get(87, 0)) == 1:
            return "3"
        if int(v.flags.get(89, 0)) == 1:
            return "4"
        if int(v.flags.get(91, 0)) == 1:
            return "5"

        # Check character-specific ending flags
        fia_flag = int(v.globals.get(2807, 0))
        if fia_flag >= 1200:
            return "7_princess"
        if fia_flag >= 2200:
            return "7_witch"

        square_flag = int(v.globals.get(2811, 0))
        if square_flag >= 900:
            return "11_tsundere"

        spade_flag = int(v.globals.get(2814, 0))
        if spade_flag >= 900 and spade_flag < 1500:
            return "14_ninja"
        if spade_flag >= 2000:
            return "14_dairy"

        godness_flag = int(v.globals.get(2810, 0))
        if godness_flag >= 1900:
            return "10_godness"

        # Castle fall ending - if a hero has very high combat power
        hero_idx = int(v.globals.get(2803, 0))
        if hero_idx > 0 and hero_idx < len(v.chars):
            hero = v.chars[hero_idx]
            if int(hero.cflag.get(9, 0)) >= 5000 and int(hero.cflag.get(1, 0)) == 0:
                return "2"

        return None


    def _load_ending_data(self) -> None:
        v = self.interpreter.vars
        if not hasattr(v, '_ending_data_loaded'):
            v._ending_data_loaded = True
        self._refresh_story_presence_flags()
        self._apply_endcheck_main_flags()
        self._apply_endcheck_characters()
        for template_id, flag_id in [
            (17, 2805), (20, 2813), (21, 2814), (22, 2811),
            (23, 2812), (24, 2806), (31, 2808), (32, 2809),
            (33, 2810), (35, 2807),
        ]:
            char = self._find_character_by_template_id(template_id)
            if char is None:
                if flag_id == 2815:
                    v.set_flag(flag_id, 0)
                else:
                    current = int(v.globals.get(flag_id, 0))
                    if flag_id == 2814 and current >= 300:
                        pass
                    elif flag_id == 2810 and int(v.globals.get(2810, 0)) >= 500:
                        pass
                    else:
                        v.globals[flag_id] = 0


    def _check_ending_conditions(self) -> Optional[str]:
        v = self.interpreter.vars
        self._load_ending_data()
        total_days = self._get_total_day_count()
        main_flag = int(v.globals.get(2801, 0))
        if main_flag == 99 and total_days >= 500:
            return "N"
        if int(v.flags.get(82, 0)) == 1 and int(v.flags.get(81, 0)) >= 1000:
            return "1"
        if int(v.flags.get(87, 0)) == 1:
            return "3"
        if int(v.flags.get(89, 0)) == 1:
            return "4"
        if int(v.flags.get(91, 0)) == 1:
            return "5"
        fia_flag = int(v.globals.get(2807, 0))
        if fia_flag >= 2200:
            return "7_witch"
        if fia_flag >= 1200:
            return "7_princess"
        square_flag = int(v.globals.get(2811, 0))
        if square_flag >= 900:
            return "11_tsundere"
        spade_flag = int(v.globals.get(2814, 0))
        if spade_flag >= 2000:
            return "14_dairy"
        if spade_flag >= 900:
            return "14_ninja"
        godness_flag = int(v.globals.get(2810, 0))
        if godness_flag >= 1900:
            return "10_godness"
        rebellion_flag = int(v.flags.get(2816, 0))
        if rebellion_flag >= 10:
            return "rebellion"
        hero_idx = int(v.globals.get(2803, 0))
        if 0 < hero_idx < len(v.chars):
            hero = v.chars[hero_idx]
            if int(hero.cflag.get(9, 0)) >= 5000 and int(hero.cflag.get(1, 0)) == 0:
                return "2"
        if main_flag >= 10:
            return "1"
        return None

    # =====================================================================
    # SYSTEM (系统初始化)
    # Corresponds to ERB SYSTEM.ERB
    # =====================================================================


