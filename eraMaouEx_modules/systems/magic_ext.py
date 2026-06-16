from __future__ import annotations
"""Module for MagicExtMixin - 魔法系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class MagicExtMixin:
    """Mixin providing 魔法系统 methods for GameEngine"""

    def _check_magic_available(self, char, magic_id: int) -> bool:
        """检查魔法是否可用 - 对应 @MAGIC_CHECK
        检查角色是否拥有魔法天赋(TALENT:241)以及MP是否足够
        """
        if magic_id not in self._MAGIC_DEFINITIONS:
            return False

        magic_def = self._MAGIC_DEFINITIONS[magic_id]
        mp_cost = magic_def["mp_cost"]

        # 检查是否有魔法天赋 (TALENT:241 = 魔法適性)
        # TARGET_TYPE 1/4 检查 A 的 TALENT:241, TARGET_TYPE 3 检查 B 的 TALENT:241
        # 咒术 (7,8,9) 需要检查 TALENT:250 (呪術適性)
        if magic_id in (7, 8, 9):
            if not char.has_talent(250):
                return False
        else:
            if not char.has_talent(241):
                return False

        # 检查MP是否足够 (BASE:1 = MP)
        if char.base.get(1, 0) < mp_cost:
            return False

        return True






    def _get_magic_list(self, char) -> List[Dict[str, Any]]:
        """获取可用魔法列表"""
        available = []
        for magic_id, magic_def in self._MAGIC_DEFINITIONS.items():
            can_use = self._check_magic_available(char, magic_id)
            available.append({
                "id": magic_id,
                "name": magic_def["name"],
                "type": magic_def["type"],
                "mp_cost": magic_def["mp_cost"],
                "description": magic_def["description"],
                "available": can_use,
            })
        return available

    # ========================================
    # LOVERS - 恋人系统
    # 对应 ERB/LOVERS.ERB
    # ========================================

    # 恋人类型名称映射
    _LOVER_NAMES: Dict[int, str] = {
        1: "温柔的青年", 2: "威严的彪形大汉", 3: "粗野的流氓", 4: "大腹便便的中年人",
        21: "丑陋的兽人", 22: "精灵美男子", 23: "暗黑精灵", 24: "奴隶",
        41: "妓女", 42: "女学生", 43: "贵妇", 44: "女骑士",
        61: "懦弱少年", 62: "戴眼镜的男学生", 63: "活泼的少年", 64: "可爱的男学生",
        81: "大型宠物狗", 82: "爱马", 83: "宠物猪", 84: "农家的牛",
        200: "恋人",
    }






    def _get_magic_ring_inventory_ids(self, owner: Character) -> List[int]:
        return [item_id for item_id in range(300, 320) if self._get_item_count(owner, item_id) > 0]






    def _get_magic_weapon_inventory_ids(self, owner: Character) -> List[int]:
        weapon_ids = [340] + [item_id for item_id in range(341, 353) if item_id != 349]
        available = [item_id for item_id in weapon_ids if self._get_item_count(owner, item_id) > 0]
        if self._get_item_count(owner, 90) > 0 and 349 not in available:
            available.append(349)
        return available






    def _handle_magic_item_menu_choice(self, choice: str) -> Optional[int]:
        if choice == "999":
            return None
        if choice not in {"1", "2"}:
            self._show_invalid_selection()
            return -1
        return 551 if choice == "1" else 552






    def _handle_magic_item_slot_choice(self, target: Character, slot_flag: int, player: Character, sub_choice: str) -> Optional[bool]:
        current_code = int(target.cflag.get(slot_flag, -1))
        handled = self._handle_magic_item_slot_menu_command_choice(target, slot_flag, sub_choice, current_code)
        if handled is not None:
            return handled
        try:
            item_id = int(sub_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return True
        if not self._is_valid_magic_item_slot_choice(player, item_id):
            print("\nInvalid selection.")
            self._pause()
            return True
        ok, message = self._equip_ring_to_slot(target, slot_flag, item_id)
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_magic_item_slot_menu_command_choice(self, target: Character, slot_flag: int, choice: str, current_code: int) -> Optional[bool]:
        if choice == "999":
            return False
        if choice == "997":
            if self._get_character_level(self._get_player()) < 30 or current_code < 0:
                print("\n未开放（30级后才能装备强化）")
                self._pause()
                return True
            ok, message = self._apply_equipment_upgrade(target, slot_flag, False)
            print(f"\n{message}")
            self._pause()
            return True
        if choice == "998":
            if current_code < 0:
                print("\n当前没有可取下的装备。")
                self._pause()
                return True
            ok, message = self._remove_equipment_from_slot(target, slot_flag, False)
            print(f"\n{message}")
            self._pause()
            return True
        return None






    def _handle_magic_weapon_menu_choice(self, target: Character, player: Character, choice: str) -> Optional[bool]:
        current_code = int(target.cflag.get(550, -1))
        handled = self._handle_magic_weapon_menu_command_choice(target, choice, current_code)
        if handled is not None:
            return handled
        try:
            raw_id = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return True
        item_id = 349 if raw_id == 990 else raw_id
        if item_id < 340 or item_id >= 353 or not (self._is_item_owned(player, item_id) or (item_id == 349 and self._get_item_count(player, 90) > 0)):
            print("\nInvalid selection.")
            self._pause()
            return True
        if item_id == 349:
            ok, message = self._equip_weapon_to_slot(target, item_id, source_item_id=90)
            print(f"\n{message}")
            self._pause()
            return True
        ok, message = self._equip_weapon_to_slot(target, item_id)
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_magic_weapon_menu_command_choice(self, target: Character, choice: str, current_code: int) -> Optional[bool]:
        if choice == "999":
            return False
        if choice == "997":
            if current_code < 0:
                print("\n手无寸铁，强化啥子？")
                self._pause()
                return True
            if self._get_character_level(self._get_player()) < 30:
                print("\n未开放（30级后才能装备强化）")
                self._pause()
                return True
            ok, message = self._apply_equipment_upgrade(target, 550, True)
            print(f"\n{message}")
            self._pause()
            return True
        if choice == "998":
            if current_code < 0:
                print("\n当前没有可取下的武器。")
                self._pause()
                return True
            ok, message = self._remove_equipment_from_slot(target, 550, True)
            print(f"\n{message}")
            self._pause()
            return True
        return None






    def _render_magic_item_menu(self, target: Character):
        slot_a = int(target.cflag.get(551, -1))
        slot_b = int(target.cflag.get(552, -1))
        print("\n【魔法装备】")
        print("-" * 30)
        print(f" [1] 装饰A : {'无' if slot_a < 0 else self._get_equipment_ring_name(slot_a)}")
        print(f" [2] 装饰B : {'无' if slot_b < 0 else self._get_equipment_ring_name(slot_b)}")
        print(" [999] 返回")






    def _render_magic_item_slot_menu(self, target: Character, slot_flag: int, player: Character):
        current_code = int(target.cflag.get(slot_flag, -1))
        print(f"\n【{self._get_equipment_slot_name(slot_flag)}】")
        for item_id in self._get_magic_ring_inventory_ids(player):
            print(f" [{item_id}] {self._get_item_name(item_id)} ({self._get_item_count(player, item_id)})")
        if self._get_character_level(self._get_player()) >= 30 and current_code >= 0:
            print(" [997] 装备强化")
        if current_code >= 0:
            print(" [998] 取下")
        print(" [999] 返回")






    def _render_magic_weapon_menu(self, target: Character, player: Character):
        current_code = int(target.cflag.get(550, -1))
        print("\n【武器】")
        print("-" * 30)
        print(f" 当前武器 : {'空手' if current_code < 0 else self._get_equipment_weapon_name(current_code)}")
        for item_id in self._get_magic_weapon_inventory_ids(player):
            label = "武器化触手" if item_id == 349 else self._get_item_name(item_id)
            print(f" [{990 if item_id == 349 else item_id}] {label} ({self._get_item_count(player, 90 if item_id == 349 else item_id)})")
        if self._get_character_level(self._get_player()) >= 30 and current_code >= 0:
            print(" [997] 装备强化")
        if current_code >= 0:
            print(" [998] 取下")
        print(" [999] 返回")






    def _show_magic_item_menu(self, target: Character):
        player = self._get_player()
        if player is None:
            print("\n当前没有魔王角色。")
            self._pause()
            return
        while True:
            self._render_magic_item_menu(target)
            slot_flag = self._handle_magic_item_menu_choice(self._prompt_choice())
            if slot_flag is None:
                return
            if slot_flag == -1:
                continue
            while True:
                self._render_magic_item_slot_menu(target, slot_flag, player)
                sub_choice = self._prompt_choice()
                if not self._handle_magic_item_slot_choice(target, slot_flag, player, sub_choice):
                    break






    def _show_magic_weapon_menu(self, target: Character):
        player = self._get_player()
        if player is None:
            print("\n当前没有魔王角色。")
            self._pause()
            return
        while True:
            self._render_magic_weapon_menu(target, player)
            if not self._handle_magic_weapon_menu_choice(target, player, self._prompt_choice()):
                return






    def _use_magic(self, char, magic_id: int, target=None) -> Dict[str, Any]:
        """使用魔法 - 对应 @MAGIC_USE
        Args:
            char: 施法者
            magic_id: 魔法ID (1-9)
            target: 目标角色（可选，用于角色对角色场景）
        Returns:
            效果结果字典
        """
        if magic_id not in self._MAGIC_DEFINITIONS:
            return {"success": False, "message": "无效的魔法ID"}

        if not self._check_magic_available(char, magic_id):
            return {"success": False, "message": "无法使用该魔法"}

        magic_def = self._MAGIC_DEFINITIONS[magic_id]
        mp_cost = magic_def["mp_cost"]
        char_lv = char.cflag.get(9, 0)

        # 消耗MP
        char.base[1] = char.base.get(1, 0) - mp_cost

        result: Dict[str, Any] = {
            "success": True,
            "magic_id": magic_id,
            "magic_name": magic_def["name"],
            "mp_cost": mp_cost,
            "caster": char.name,
        }

        if magic_id == 1:
            result.update(self._use_teleport_magic(char, target))
        elif magic_id == 2:
            result.update(self._use_sleep_magic(char, target, char_lv))
        elif magic_id == 3:
            result.update(self._use_energy_bolt_magic(char, target, char_lv))
        elif magic_id == 4:
            result.update(self._use_energy_drain_magic(char, target, char_lv))
        elif magic_id == 5:
            result.update(self._use_fireball_magic(char, target, char_lv))
        elif magic_id == 6:
            result.update(self._use_heal_magic(char, target, char_lv))
        elif magic_id == 7:
            result.update(self._use_curse_magic(char, target, char_lv))
        elif magic_id == 8:
            result.update(self._use_mind_drain_magic(char, target, char_lv))
        elif magic_id == 9:
            result.update(self._use_lv_drain_magic(char, target, char_lv))

        return result





