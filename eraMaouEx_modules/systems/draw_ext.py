from __future__ import annotations
"""Module for DrawExtMixin - 绘制系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class DrawExtMixin:
    """Mixin providing 绘制系统 methods for GameEngine"""

    def _render_main_menu_character_detail(self, idx: int, char: Character) -> None:
        print("\n【Character Detail】")
        print("-" * 30)
        for line in self._build_character_detail_lines(idx, char):
            print(line)
        print("-" * 30)
        action_lines = self._build_character_detail_action_lines(idx, char)
        if action_lines:
            for line in action_lines:
                print(line)
        print(" [100] 返回")




    def _render_main_menu_header(self):
        year, month, day = self.interpreter.vars.day[:3]
        time_str = "Morning" if self.interpreter.vars.time == 0 else "Afternoon"
        print(f"\n{'='*50}")
        print(f" Year {year} Month {month} Day {day} ({time_str})")
        print(f" Money: {self.interpreter.vars.money} pts")
        print(f"{'='*50}")




    def _render_main_menu_sections(self):
        print("\n" + "-" * 50)
        for line in self._build_main_menu_target_assistant_lines():
            print(line)
        print("\n" + "-" * 50)
        print(f" Info Panel: {self._get_main_menu_panel_title()}")
        for line in self._build_main_menu_panel_lines():
            print(line)
        print(" [500] 物品/技能")
        print(" [501] 持有陷阱")
        print(" [504] 地城概况")
        print(" [505] 地城日常")
        print("\n" + "-" * 50)
        for line in self._build_shop_command_lines():
            print(line)
        print(" [999] Exit")
        print("-" * 50)



    def _render_main_menu_target_panel(self):
        if self.interpreter.vars.target >= 0 and self.interpreter.vars.target < len(self.interpreter.vars.chars):
            target = self.interpreter.vars.chars[self.interpreter.vars.target]
            print(f"\nTraining Target: {target.name}")
            print(f"  HP: {target.base.get(0, 0)}/{target.maxbase.get(0, 0)}")
            print(f"  MP: {target.base.get(1, 0)}/{target.maxbase.get(1, 0)}")




    def _render_title_screen(self) -> None:
        print("=" * 50)
        print("  eraMaouEx Python Implementation")
        print(f"  Ver {VERSION}")
        print(f"  Saves: {self.paths.save_dir}")
        print("=" * 50)
        print()
        print("[0] Load Game")
        print("[1] New Game")
        print()



