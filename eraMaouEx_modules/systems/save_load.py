from __future__ import annotations
import os
"""Module for SaveLoadMixin - 存档/读档"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SaveLoadMixin:
    """Mixin providing 存档/读档 methods for GameEngine"""

    def _advance_load_game_menu(self) -> str:
        saves = self._collect_load_game_saves()
        if not saves:
            print("No saved games found.")
            return "TITLE"
        self._render_load_game_menu(saves)
        choice = self._prompt_load_game_choice()
        return self._handle_load_game_choice_result(choice)






    def _apply_departed_character_return_level(self, char: Character, set_level: int) -> None:
        if set_level <= 0:
            return
        current_level = max(1, int(char.cflag.get(9, 1) or 1))
        if current_level >= int(set_level):
            return
        for _ in range(int(set_level) - current_level):
            self._apply_single_level_up(-1, char)




    def _build_save_game_data(self) -> Dict[str, Any]:
        return {
            "vars": self.interpreter.vars,
            "text": self._format_day_text(),
            "date": datetime.now().isoformat(),
        }






    def _collect_load_game_saves(self) -> List[tuple[int, str, str]]:
        saves: List[tuple[int, str, str]] = []
        for i in self._iter_save_slot_indices():
            save_path = self.paths.save_slot_path(i)
            if os.path.exists(save_path):
                try:
                    data = self._load_pickle_file(save_path)
                    saves.append((i, data.get('text', ''), data.get('date', '')))
                except:
                    saves.append((i, "Unknown", ""))
        return saves






    def _handle_load_game_choice(self, choice: str) -> bool:
        return self._load_selected_game_slot(choice)






    def _handle_load_game_choice_result(self, choice: str) -> str:
        if choice == "100":
            return "TITLE"
        if self._handle_load_game_choice(choice):
            return "SHOP"
        return "TITLE"






    def _handle_save_game_choice(self, choice: str) -> None:
        if choice == "100":
            return
        if self._save_game_slot(choice):
            print("\nGame saved!")
        else:
            print("\nFailed to save!")
        self._pause()






    def _load_global_store(self) -> Dict[str, Any]:
        global_path = self.paths.global_path
        if not os.path.exists(global_path):
            return {}
        try:
            with open(global_path, "rb") as global_file:
                data = pickle.load(global_file)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}




    def _load_pickle_file(self, path: str) -> Dict[str, Any]:
        with open(path, 'rb') as f:
            return pickle.load(f)




    def _load_selected_game_slot(self, choice: str) -> bool:
        try:
            save_path = self._get_save_slot_path(choice)
            if os.path.exists(save_path):
                self._restore_loaded_game_state(save_path)
                print("Game loaded!")
                self._pause("Press enter...")
                return True
        except:
            pass
        return False




    def _prompt_load_game_choice(self) -> str:
        return self._prompt_choice_raw()






    def _render_load_game_menu(self, saves: List[tuple[int, str, str]]) -> None:
        print("\n【Load Game】")
        print("-" * 30)
        for slot, text, date in saves:
            print(f"[{slot:2}] {text} - {date}")
        print("\n[100] Back")






    def _render_save_game_menu(self) -> None:
        print("\n【Save Game】")
        print("-" * 30)
        print(f"Save directory: {self.paths.save_dir}")
        for i in self._iter_save_slot_indices():
            save_path = self.paths.save_slot_path(i)
            if os.path.exists(save_path):
                print(f"[{i:2}] Save exists")
            else:
                print(f"[{i:2}] Empty")
        print("\n[100] Back")






    def _restore_departed_character(self, slot: int, set_level: int = 0) -> Optional[Character]:
        data = self.interpreter.vars.departed_chars.get(int(slot))
        if not isinstance(data, dict):
            return None
        template_id = int(data.get("template_id", 0) or 0)
        restored = self._deserialize_maounet_character(dict(data))
        self._apply_departed_character_return_level(restored, set_level)
        # 原 ERB 的返场会回到模板默认名称，而不是保留离场前的可改名状态。
        if template_id > 0:
            template = self._load_character_template(template_id)
            if template is not None:
                restored.name = template.name
                restored.callname = template.callname
        restored.item = {}
        restored.cflag[190] = 0
        restored.cflag[501] = 0
        restored.cflag[502] = 0
        restored.cflag[1] = 0
        restored.base[0] = int(restored.maxbase.get(0, restored.base.get(0, 0)))
        restored.base[1] = int(restored.maxbase.get(1, restored.base.get(1, 0)))
        self._append_character(restored)
        self.interpreter.vars.departed_chars.pop(int(slot), None)
        return restored




    def _restore_loaded_game_state(self, save_path: str) -> None:
        data = self._load_pickle_file(save_path)
        self.interpreter.vars = data["vars"]
        self.interpreter.paths = self.paths
        if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
            self._ensure_race_age_defaults()
            self._ensure_all_character_body_profiles()
        # 存档数据修复 - 对应 @DATA_FIX
        self._apply_data_fix()




    def _save_game_slot(self, choice: str) -> bool:
        try:
            save_path = self._get_save_slot_path(choice)
            save_data = self._build_save_game_data()
            self._write_save_game_file(save_path, save_data)
            return True
        except:
            return False



    def _save_global_store(self, store: Dict[str, Any]):
        with open(self.paths.global_path, "wb") as global_file:
            pickle.dump(store, global_file)




    def _serialize_departed_character(self, char: Character) -> Dict[str, Any]:
        data = self._serialize_maounet_character(char)
        data.pop("item", None)
        data.pop("share_id", None)
        data["template_id"] = self._get_character_template_id(char) or int(data.get("template_id", 0) or 0)
        return data




    def _show_save_game_menu(self):
        self._render_save_game_menu()
        choice = self._prompt_choice_raw()
        self._handle_save_game_choice(choice)






    def _store_departed_character(self, slot: int, char: Character) -> None:
        if slot < 0:
            return
        self.interpreter.vars.departed_chars[int(slot)] = self._serialize_departed_character(char)




    def _write_save_game_file(self, save_path: str, save_data: Dict[str, Any]) -> None:
        with open(save_path, 'wb') as f:
            pickle.dump(save_data, f)






    def run_load_game(self):
        """Run load game screen"""
        return self._advance_load_game_menu()

    def do_save(self):
        """Save game"""
        self._show_save_game_menu()

    def _saveinfo(self):
        """存档信息 - 桥接ERB SAVEINFO"""
        return self.call_erb_function('SAVEINFO')

    def _system_savegame(self, slot=None):
        """保存游戏 - 桥接ERB SYSTEM_SAVEGAME"""
        return self.call_erb_function('SYSTEM_SAVEGAME')

    def _system_loadgame(self, slot=None):
        """读取游戏 - 桥接ERB SYSTEM_LOADGAME"""
        return self.call_erb_function('SYSTEM_LOADGAME')





