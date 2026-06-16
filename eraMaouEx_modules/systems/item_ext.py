from __future__ import annotations
import os
import csv
"""Module for ItemExtMixin - 道具系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ItemExtMixin:
    """Mixin providing 道具系统 methods for GameEngine"""

    def _add_item(self, owner: Character, item_name: str, count: int = 1):
        owner.item[item_name] = owner.item.get(item_name, 0) + count






    def _craft_item(self, recipe_id: int) -> List[str]:
        """Craft an item using a recipe.
        Placeholder for item crafting system.
        """
        messages: List[str] = []
        messages.append(f"尝试合成配方 #{recipe_id}...")
        # Recipe validation would go here
        messages.append("合成功能尚未实现")
        return messages






    def _decompose_item(self, item_id: int) -> List[str]:
        """Decompose an item into materials.
        Placeholder for item decomposition system.
        """
        messages: List[str] = []
        messages.append(f"尝试分解物品 #{item_id}...")
        # Decomposition logic would go here
        messages.append("分解功能尚未实现")
        return messages






    def _equip_item(self, target: Character, slot: int, item_id: int) -> bool:
        """Equip an item to a character's slot.
        Corresponds to ERB @EQUIP_SELECT logic.
        slot: 0=weapon(CFLAG:550), 1=ringA(CFLAG:551), 2=ringB(CFLAG:552)
        """
        player = self._get_player()
        if player is None:
            return False

        slot_flag = {0: 550, 1: 551, 2: 552}.get(slot)
        if slot_flag is None:
            return False

        is_weapon = (slot == 0)

        # Check if item is owned
        if not self._is_item_owned(player, item_id):
            return False

        # Check if already equipped with cursed item
        current_code = int(target.cflag.get(slot_flag, -1))
        if current_code >= 0:
            if is_weapon:
                _, _, prefix = self._decode_equipment_code(current_code)
                base_code = current_code % 1000
                db = self._EQUIP_WEAPON_DATABASE.get(base_code, {})
            else:
                base_code = current_code % 1000
                db = self._EQUIP_RING_DATABASE.get(base_code, {})

            if db.get("cursed", False):
                return False  # Cannot replace cursed equipment

            # Return current equipment to inventory
            if is_weapon:
                self._return_equipment_item(player, self._get_weapon_item_id_from_code(current_code))
            else:
                self._return_equipment_item(player, self._get_ring_item_id_from_code(current_code))

        # Remove item from inventory
        self._use_item(player, self._get_item_name(item_id), 1)

        # Set equipment code
        if is_weapon:
            base_code = item_id - 300
            if base_code < 40:
                base_code = 40
            target.cflag[slot_flag] = self._encode_equipment_code(base_code, 0, 0)
        else:
            base_code = item_id - 300
            if base_code < 0:
                base_code = 0
            target.cflag[slot_flag] = self._encode_equipment_code(base_code, 0, 0)

        return True






    def _get_item_count(self, owner: Character, item_id: int) -> int:
        return owner.item.get(self._get_item_name(item_id), 0)






    def _get_item_definition(self, item_id: int) -> Optional[Dict[str, Union[str, int]]]:
        return self.item_catalog.get(item_id)






    def _get_item_name(self, item_id: int) -> str:
        item_def = self._get_item_definition(item_id)
        if item_def is None:
            return f"Item {item_id}"
        return str(item_def["name"])






    def _get_item_purchase_quantity(self, item_id: int, item_name: str, max_buyable: int) -> Optional[int]:
        if item_id not in self._get_buy_plural_ids():
            return 1
        print(f"\n要买多少{item_name}？（1-{max_buyable}，0返回）")
        choice = self._prompt_choice("Quantity >> ")
        if choice == "0":
            return None
        try:
            quantity = int(choice)
        except ValueError:
            print("\nInvalid quantity.")
            return None
        if quantity < 1 or quantity > max_buyable:
            print("\nInvalid quantity.")
            return None
        return quantity






    def _get_item_stock_limit(self, item_id: int) -> int:
        if item_id in self._get_buy_plural_ids() or item_id in self._get_use_now_ids():
            return 99
        return 1






    def _is_item_owned(self, owner: Character, item_id: int) -> bool:
        return owner.item.get(self._get_item_name(item_id), 0) > 0






    def _load_item_catalog(self) -> Dict[int, Dict[str, Union[str, int]]]:
        catalog: Dict[int, Dict[str, Union[str, int]]] = {}
        csv_candidates = [
            os.path.join(self.erb_dir, "CSV", "Item.csv"),
            os.path.join(os.path.dirname(self.erb_dir), "CSV", "Item.csv"),
        ]
        csv_path = next((path for path in csv_candidates if os.path.exists(path)), "")
        if not csv_path:
            return catalog

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            for row in csv.reader(csv_file):
                if not row or not row[0] or row[0].startswith(";"):
                    continue
                try:
                    item_id = int(row[0])
                except ValueError:
                    continue
                name = row[1].strip() if len(row) > 1 else ""
                try:
                    price = int(row[2]) if len(row) > 2 and row[2].strip() else 0
                except ValueError:
                    price = 0
                catalog[item_id] = {"name": name, "price": price}
        return catalog




    def _select_item_target(self, allow_master: bool = True) -> Optional[Character]:
        candidates = self._collect_selectable_item_targets(allow_master=allow_master)
        if not candidates:
            print("\nNo valid target is available.")
            return None

        self._render_select_item_target_menu(candidates)
        choice = self._prompt_choice_raw()
        return self._choose_select_item_target(candidates, choice, allow_master=allow_master)






    def _unequip_item(self, target: Character, slot: int) -> bool:
        """Unequip an item from a character's slot.
        slot: 0=weapon(CFLAG:550), 1=ringA(CFLAG:551), 2=ringB(CFLAG:552)
        """
        player = self._get_player()
        if player is None:
            return False

        slot_flag = {0: 550, 1: 551, 2: 552}.get(slot)
        if slot_flag is None:
            return False

        is_weapon = (slot == 0)
        current_code = int(target.cflag.get(slot_flag, -1))
        if current_code < 0:
            return False

        # Check if cursed
        base_code = current_code % 1000
        if is_weapon:
            db = self._EQUIP_WEAPON_DATABASE.get(base_code, {})
        else:
            db = self._EQUIP_RING_DATABASE.get(base_code, {})

        if db.get("cursed", False):
            return False  # Cannot unequip cursed items

        # Return to inventory
        if is_weapon:
            self._return_equipment_item(player, self._get_weapon_item_id_from_code(current_code))
        else:
            self._return_equipment_item(player, self._get_ring_item_id_from_code(current_code))

        target.cflag[slot_flag] = -1
        return True






    def _use_item(self, owner: Character, item_name: str, count: int = 1) -> bool:
        current = owner.item.get(item_name, 0)
        if current < count:
            return False
        remaining = current - count
        if remaining > 0:
            owner.item[item_name] = remaining
        else:
            owner.item.pop(item_name, None)
        return True





