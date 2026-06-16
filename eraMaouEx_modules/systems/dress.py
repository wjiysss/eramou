from __future__ import annotations
"""Module for DressMixin - 衣装/裁缝"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class DressMixin:
    """Mixin providing 衣装/裁缝 methods for GameEngine"""

    def _advance_dress_menu(self, target: Character, categories: Dict[str, str], category_labels: Dict[str, str]) -> bool:
        self._render_dress_main_menu(target, category_labels)
        choice = self._prompt_choice()
        if choice == "100":
            return True
        if self._handle_dress_common_action(target, choice):
            return False
        if choice not in categories:
            print("\nInvalid selection.")
            self._pause()
            return False

        category_key = categories[choice]
        self._show_dress_category_menu(target, category_key)
        return False






    def _apply_dress_accessory_option(self, target: Character, cloth_id: int) -> tuple[bool, str]:
        target.cflag[42] = cloth_id
        target.cflag[47] = 0
        return True, f"{target.name} 穿戴了{self._get_dress_accessory_name(cloth_id)}。"






    def _apply_dress_diaper_option(self, target: Character) -> tuple[bool, str]:
        target.cflag[42] = 69
        target.cflag[47] = 0
        return True, f"为 {target.name} 更换了新的尿布。"






    def _apply_dress_main_option(self, target: Character, cloth_id: int, tear_flag: int = 0, tear_message: str = "") -> tuple[bool, str]:
        target.cflag[41] = cloth_id
        target.cflag[45] = 0
        target.cflag[46] = 0
        dress_name = self._get_dress_main_cloth_name(cloth_id)
        if tear_flag == 1:
            target.cflag[44] = -3
            target.cflag[45] = -3
            return True, f"{target.name} 换上了{dress_name}。\n{tear_message}"
        if tear_flag == 2:
            target.cflag[46] = -3
            return True, f"{target.name} 换上了{dress_name}。\n{tear_message}"
        return True, f"{target.name} 换上了{dress_name}。"






    def _apply_dress_option(self, target: Character, option: Dict[str, Any]) -> tuple[bool, str]:
        blocked = self._can_apply_dress_option(target, option)
        if blocked:
            return False, blocked

        cost = int(option["cost"])
        cloth_id = int(option["cloth_id"])
        slot = str(option["slot"])
        if slot not in {"main", "underwear", "diaper", "accessory"}:
            return False, "未接入该服装类别。"
        tear_flag = 0
        tear_message = ""
        if slot == "main":
            confirmed, tear_flag, tear_message = self._confirm_child_cloth_force(target, cloth_id)
            if not confirmed:
                return False, tear_message
        self._spend_global_money(cost)

        if slot == "main":
            return self._apply_dress_main_option(target, cloth_id, tear_flag, tear_message)
        if slot == "underwear":
            return self._apply_dress_underwear_option(target)
        if slot == "diaper":
            return self._apply_dress_diaper_option(target)
        if slot == "accessory":
            return self._apply_dress_accessory_option(target, cloth_id)
        return False, "未接入该服装类别。"






    def _apply_dress_underwear_option(self, target: Character) -> tuple[bool, str]:
        resale_income = self._get_underwear_resale_income(target)
        target.cflag[40] = 3
        target.cflag[43] = 0
        target.cflag[44] = 0
        target.cflag[48] = 0
        if target.cflag.get(41, 0) == 0:
            target.cflag[41] = 1
            target.cflag[45] = -3
            target.cflag[46] = -3
        message = f"为 {target.name} 更换了新的内衣。"
        if resale_income > 0:
            self._add_global_money(resale_income)
            message += f"\n穿过的内裤被卖掉挣了{resale_income}点钱。"
        return True, message






    def _beforetrain_clothed(self, target: Character) -> List[str]:
        """初次调教时·上着着用时 - 对应 @PRITRAIN_MESSAGE_CLOTHED"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()
        target_name = getattr(target, 'savestr', target.name or "")
        player_name = getattr(player, 'callname', "主人") if player else "主人"

        if int(target.talent.get(22, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}毫无表情地呆立不动。")
        elif int(target.talent.get(132, 0)) and int(target.talent.get(135, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}不理解要发生什么了。")
        elif int(target.talent.get(12, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}展示出了坚决的态度。")
            messages.append("不会被抓到把柄，有这样的觉悟。")
        elif int(target.talent.get(11, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}用可怕的眼神狠狠地盯着{player_name}。")
        elif int(target.talent.get(21, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}耸耸肩。")
            messages.append("无论怎样都无所谓，只是请稍微迅速一点。")
            messages.append("就是这种态度。")
        elif int(target.talent.get(132, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}非常地害怕。")
            messages.append("再怎么伪装也还是个孩子罢了。")
        elif int(target.talent.get(20, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}表面上仍装作很平静。")
        elif int(target.talent.get(10, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}肩膀在颤抖着。")
            messages.append("想象到了自己今后的命运，不禁牙齿打颤。")
        elif int(target.talent.get(15, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}想到今后作为奴隶的屈辱，")
            messages.append("拼命地克制住自己颤抖着的牙齿和肩膀。")
        elif int(target.talent.get(17, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}提心吊胆地观察着{player_name}的神色。")
            messages.append("心里想着言听计从的话也许可以减少痛苦。")
        elif int(target.talent.get(13, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}对自己现在的处境难以接受。")
            messages.append("人不能对他人做这么过分的事，难道不是这样的吗？")
        elif int(target.talent.get(14, 0)):
            messages.append(f"意识到抵抗是无用的，{self._print_clothtype(target)}的{target_name}老老实实的。")
        elif int(target.talent.get(16, 0)):
            messages.append(f"{self._print_clothtype(target)}的{target_name}害怕的同时对{player_name}投以挑衅的目光。")
            messages.append("这种事是不会让我屈服的，好像有这种自信的样子。")
        else:
            messages.append(f"{self._print_clothtype(target)}的{target_name}被带到调教室了。")

        return messages






    def _build_dress_accessory_options(self, target: Optional[Character] = None) -> List[Dict[str, Any]]:
        options: List[Dict[str, Any]] = []
        for entry in self._get_dress_accessory_definitions():
            cloth_id = int(entry["cloth_id"])
            option = dict(entry)
            option["slot"] = "accessory"
            option["req"] = self._get_dress_accessory_requirement(target, cloth_id)
            options.append(option)
        return options






    def _clear_dress_slot(self, target: Character, slot: str) -> tuple[bool, str]:
        if slot == "main":
            target.cflag[41] = 0
            return True, f"{target.name} 脱下了外衣。"
        if slot == "accessory":
            target.cflag[42] = 0
            target.cflag[47] = 0
            target.cflag[49] = 0
            return True, f"{target.name} 解除了一般饰品。"
        return False, "无法解除该部位。"






    def _cm_cloth(self, char: Character) -> None:
        """服装设定 (对应 @CM_CLOTH)"""
        # 默认服装
        char.equipt[0] = 1  # 基础服装






    def _confirm_child_cloth_force(self, target: Character, cloth_id: int) -> tuple[bool, int, str]:
        if cloth_id != 22:
            return True, 0, ""
        if target.talent.get(99, 0):
            print(f"\n{target.name} 应该穿不下这件衣服。")
            print(" [0] 强行套上")
            print(" [1] 作罢")
            choice = self._prompt_choice()
            if choice != "0":
                return False, 0, "取消了更换童装。"
            return True, 2, "强行套上的时候，把衣服的下半身撑破了。"
        if target.talent.get(100, 0) == 0 and (
            target.talent.get(114, 0) or target.talent.get(110, 0) or target.talent.get(119, 0)
        ):
            print(f"\n{target.name} 应该穿不下这件衣服。")
            print(" [0] 强行套上")
            print(" [1] 作罢")
            choice = self._prompt_choice()
            if choice != "0":
                return False, 0, "取消了更换童装。"
            return True, 1, "强行套上的时候，把衣服的上半身撑破了。"
        return True, 0, ""






    def _func_cloth(self, target: Character, action: str) -> List[str]:
        """Clothing management based on FUNC_CLOTH.ERB.

        action: "wear", "remove", "status", "init"
        """
        lines: List[str] = []
        name = target.name or "她"
        cloth_state = target.cflag.get(40, 0)
        cloth_type = target.cflag.get(41, 0)
        special_type = target.cflag.get(42, 0)

        if action == "status":
            # Display current clothing state
            if cloth_type == 0 and special_type == 0:
                lines.append(f"{name}：全裸")
            else:
                parts: List[str] = []
                if cloth_state & 1:
                    parts.append("内裤")
                if cloth_state & 2:
                    parts.append("胸罩")
                if cloth_state & 4:
                    parts.append("上衣(上)")
                if cloth_state & 8:
                    parts.append("上衣(下)-裙子")
                if cloth_state & 16:
                    parts.append("上衣(下)-裤子")
                if cloth_state & 64:
                    parts.append("特别服装")
                if parts:
                    lines.append(f"{name}穿着：{'、'.join(parts)}")
                else:
                    lines.append(f"{name}：全裸")

        elif action == "wear":
            # Wear all standard clothing
            new_state = 0
            if cloth_type != 0:
                new_state |= 1  # 内裤
                # 胸罩 (unless flat/immature)
                if not target.talent.get(116, 0) and not target.talent.get(135, 0):
                    if target.talent.get(132, 0) == 0 or target.talent.get(109, 0) == 0:
                        new_state |= 2
                # Skirt type (1-100)
                if 1 <= cloth_type <= 100:
                    new_state |= 4 | 8
                # Pants type (101-200)
                elif 101 <= cloth_type <= 200:
                    new_state |= 4 | 16
                # Full body type (201-300)
                elif 201 <= cloth_type <= 300:
                    new_state |= 4 | 8 | 16
            target.cflag[40] = new_state
            lines.append(f"{name}穿上了衣服。")

        elif action == "remove":
            # Remove all clothing
            target.cflag[40] = 0
            lines.append(f"{name}脱掉了所有衣服。")

        elif action == "init":
            # Initialize clothing based on character template
            if cloth_type == 0 and special_type == 0:
                lines.append(f"{name}没有设定服装。")
            else:
                target.cflag[40] = 0
                # Re-wear
                new_state = 0
                if cloth_type != 0:
                    new_state |= 1
                    if not target.talent.get(116, 0) and not target.talent.get(135, 0):
                        if target.talent.get(132, 0) == 0 or target.talent.get(109, 0) == 0:
                            new_state |= 2
                    if 1 <= cloth_type <= 100:
                        new_state |= 4 | 8
                    elif 101 <= cloth_type <= 200:
                        new_state |= 4 | 16
                    elif 201 <= cloth_type <= 300:
                        new_state |= 4 | 8 | 16
                target.cflag[40] = new_state
                lines.append(f"{name}的服装已初始化。")

        return lines

    # ------------------------------------------------------------------
    # EVENT_PREGNANCY (妊娠事件)
    # ------------------------------------------------------------------



    def _get_cloth_desc(self, target) -> str:
        """Get clothing description.
        Uses existing _get_wearing_cloths helper.
        """
        parts: List[str] = []
        cloths = self._get_wearing_cloths(target)
        if cloths:
            for c in cloths:
                parts.append(c.get('name', ''))
        else:
            main_cloth = int(target.cflag.get(40, 0))
            if main_cloth == 0:
                parts.append("全裸")
            else:
                parts.append(self._get_cloth_name(main_cloth))
        return " ".join(parts)






    def _get_cloth_name(self, cloth_id: int) -> str:
        """获取服装名称"""
        return self._CLOTH_NAMES.get(cloth_id, f"服装{cloth_id}")






    def _get_dress_accessory_definitions(self) -> List[Dict[str, Any]]:
        return DRESS_ACCESSORY_DEFINITIONS




    def _get_dress_accessory_name(self, accessory_id: int) -> str:
        return DRESS_ACCESSORY_NAMES.get(accessory_id, f"饰品{accessory_id}")




    def _get_dress_accessory_requirement(self, target: Optional[Character], cloth_id: int) -> int:
        if target is None:
            return 0
        rule = DRESS_ACCESSORY_REQUIREMENT_RULES.get(cloth_id)
        if rule is None:
            return 0
        kind = rule[0]
        if kind == "fixed":
            return int(rule[1])
        if kind == "talent":
            _, talent_id, base_req, special_talent_id, special_req = rule
            req = base_req - int(target.talent.get(talent_id, 0))
            if target.talent.get(special_talent_id, 0) and req < special_req:
                req = special_req
            return max(0, req)
        if kind == "group":
            _, cloth_ids, abl_id, base_req, cap_talent_id, cap_req, floor_talent_id, floor_req = rule
            if cloth_id not in cloth_ids:
                return 0
            req = base_req - int(target.abl.get(abl_id, 0))
            if target.talent.get(cap_talent_id, 0) and req > cap_req:
                req = cap_req
            if target.talent.get(floor_talent_id, 0) or req < floor_req:
                req = floor_req
            return max(0, req)
        if kind == "special":
            _, base_req, talent_a, talent_b, talent_c = rule
            req = base_req
            if (target.talent.get(talent_a, 0) or target.talent.get(talent_b, 0)) and target.talent.get(talent_c, 0):
                req = 3
            return req
        if kind == "binary":
            _, talent_id, yes_req, no_req = rule
            return yes_req if target.talent.get(talent_id, 0) else no_req
        return 0




    def _get_dress_casual_options(self, target: Optional[Character]) -> List[Dict[str, Any]]:
        skirt_req = 0
        if target is not None and target.talent.get(122, 0):
            skirt_req = 3
        return [
            {"menu_id": 1, "slot": "main", "name": "日常着装·裙子", "cloth_id": 1, "cost": 100, "req": skirt_req},
            {"menu_id": 2, "slot": "main", "name": "日常着装·裤子", "cloth_id": 101, "cost": 100, "req": 0},
        ]




    def _get_dress_category_options(self, category: str, target: Optional[Character] = None) -> List[Dict[str, Any]]:
        if category == "casual":
            return self._get_dress_casual_options(target)
        if category == "normal":
            return self._get_dress_normal_options()
        if category == "normal_special":
            return self._get_dress_normal_special_options()
        if category == "underwear":
            return self._get_dress_underwear_options()
        if category == "diaper":
            return self._get_dress_diaper_options()
        if category == "accessory":
            return self._build_dress_accessory_options(target)
        return []




    def _get_dress_diaper_options(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 1, "slot": "diaper", "name": "替换尿布", "cloth_id": 69, "cost": 50, "req": 0},
        ]




    def _get_dress_main_cloth_name(self, cloth_id: int) -> str:
        return self._get_dress_main_cloth_names().get(cloth_id, f"服装{cloth_id}")




    def _get_dress_main_cloth_names(self) -> Dict[int, str]:
        return DRESS_MAIN_CLOTH_NAMES




    def _get_dress_menu_categories(self) -> Dict[str, str]:
        return {
            "0": "casual",
            "1": "normal",
            "2": "accessory",
            "3": "underwear",
        }




    def _get_dress_menu_choice_labels(self) -> Dict[str, str]:
        return {
            "0": "日常服饰",
            "1": "普通装备",
            "2": "其它",
            "3": "替换内衣",
        }




    def _get_dress_menu_page_count(self, category: str, options: List[Dict[str, Any]]) -> int:
        page_size = self._get_dress_menu_page_size(category)
        if page_size <= 0:
            return 1
        return max(1, (len(options) + page_size - 1) // page_size)




    def _get_dress_menu_page_options(self, category: str, options: List[Dict[str, Any]], page: int) -> List[Dict[str, Any]]:
        page_size = self._get_dress_menu_page_size(category)
        if page_size <= 0:
            return options
        page_count = self._get_dress_menu_page_count(category, options)
        page = page % page_count
        start = page * page_size
        end = start + page_size
        return options[start:end]




    def _get_dress_menu_page_size(self, category: str) -> int:
        return {
            "normal": 10,
            "normal_special": 10,
            "accessory": 10,
        }.get(category, 0)




    def _get_dress_menu_title(self, category: str) -> str:
        return {
            "casual": "日常服饰",
            "normal": "普通装备",
            "normal_special": "服装黑市",
            "accessory": "其它",
            "underwear": "替换内衣",
        }.get(category, "Dress")




    def _get_dress_normal_options(self) -> List[Dict[str, Any]]:
        return DRESS_NORMAL_OPTIONS




    def _get_dress_normal_special_options(self) -> List[Dict[str, Any]]:
        return DRESS_NORMAL_SPECIAL_OPTIONS




    def _get_dress_summary_lines(self, target: Character) -> List[str]:
        return [
            f" 外衣: {self._get_dress_main_cloth_name(target.cflag.get(41, 0))}",
            f" 饰品: {self._get_dress_accessory_name(target.cflag.get(42, 0))}",
            f" 衣装状态: {target.cflag.get(40, 0)}",
            f" 贞操带: {'ON' if target.cflag.get(49, 0) else 'OFF'}",
        ]




    def _get_dress_underwear_options(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 1, "slot": "underwear", "name": "替换内衣", "cloth_id": 3, "cost": 5, "req": 0},
        ]




    def _get_wearing_cloths(self, target) -> List[Dict[str, Any]]:
        """获取角色穿着的服装列表"""
        cloths = []
        # CFLAG:40 = 服装ID, CFLAG:41 = 内衣ID, CFLAG:42 = 鞋子ID
        # CFLAG:45 = 服装颜色, CFLAG:46 = 服装材质
        main_cloth = target.cflag.get(40, 0)
        if main_cloth > 0:
            cloths.append({
                'id': main_cloth,
                'name': self._get_cloth_name(main_cloth),
                'slot': 'main',
                'color': target.cflag.get(45, 0),
                'material': target.cflag.get(46, 0),
            })

        # TEQUIP 装备
        for equip_id in [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:
            if target.tequip.get(equip_id, 0):
                cloths.append({
                    'id': equip_id,
                    'name': self._get_cloth_name(equip_id),
                    'slot': 'equip',
                })

        return cloths






    def _handle_dress_category_choice(
        self,
        target: Character,
        category_key: str,
        category_name: str,
        options: List[Dict[str, Any]],
        page: int,
        page_count: int,
        page_options: List[Dict[str, Any]],
        sub_choice: str,
    ) -> tuple[bool, str, str, List[Dict[str, Any]], int]:
        handled, new_category_key, new_category_name, new_options, new_page = self._handle_dress_category_navigation(
            target,
            category_key,
            category_name,
            options,
            page,
            page_count,
            sub_choice,
        )
        if handled:
            return True, new_category_key, new_category_name, new_options, new_page
        selected_option = self._select_dress_category_option(page_options, sub_choice)
        if selected_option is None:
            print("\nInvalid selection.")
            self._pause()
            return False, category_key, category_name, options, page
        self._apply_selected_dress_option(target, selected_option)
        return False, category_key, category_name, options, page






    def _handle_dress_category_navigation(
        self,
        target: Character,
        category_key: str,
        category_name: str,
        options: List[Dict[str, Any]],
        page: int,
        page_count: int,
        sub_choice: str,
    ) -> tuple[bool, str, str, List[Dict[str, Any]], int]:
        if sub_choice == "997" and page_count > 1:
            return True, category_key, category_name, options, (page + 1) % page_count
        if sub_choice == "998" and page_count > 1:
            return True, category_key, category_name, options, (page - 1) % page_count
        if sub_choice == "996" and category_key == "normal":
            new_category_key = "normal_special"
            new_category_name = self._get_dress_menu_title(new_category_key)
            new_options = self._get_dress_category_options(new_category_key, target)
            return True, new_category_key, new_category_name, new_options, 0
        return False, category_key, category_name, options, page






    def _handle_dress_chastity_key_action(self, target: Character) -> bool:
        ok, message = self._discard_chastity_key(target)
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_dress_common_action(self, target: Character, choice: str) -> bool:
        if self._handle_dress_immediate_action(target, choice):
            return True
        return self._handle_dress_submenu_action(target, choice)






    def _handle_dress_diaper_replace_action(self, target: Character) -> bool:
        if not self._can_replace_diaper(target):
            print("\n现在不能替换尿布。")
            self._pause()
            return True
        options = self._get_dress_category_options("diaper")
        selected_option = options[0]
        ok, message = self._apply_dress_option(target, selected_option)
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_dress_immediate_action(self, target: Character, choice: str) -> bool:
        if choice == "4":
            return self._handle_dress_diaper_replace_action(target)
        if choice == "5":
            return self._handle_dress_chastity_key_action(target)
        return False






    def _handle_dress_submenu_action(self, target: Character, choice: str) -> bool:
        if choice == "7":
            self._show_magic_item_menu(target)
            return True
        if choice == "8":
            self._show_magic_weapon_menu(target)
            return True
        return False






    def _is_cloth_exposing(self, target) -> bool:
        """检查服装是否暴露"""
        cloth_id = target.cflag.get(40, 0)
        if cloth_id == 0:
            return True  # 全裸
        if cloth_id in (1, 6, 11, 12, 16, 17, 18, 30, 46, 47, 48):
            return True  # 暴露服装
        return False






    def _prepare_dress_menu_target(self) -> Optional[Character]:
        target = self._get_target()
        blocked_reason = self._can_select_standby_slave(self.interpreter.vars.target, target)
        if blocked_reason is None:
            return target
        print("\n【Dress/Equipment】")
        print("No captive is currently selected." if blocked_reason == "无效对象" else blocked_reason)
        self._pause()
        return None




    def _print_clothtype(self, target: Character) -> str:
        """衣着类型描述 - 对应 @PRINT_CLOTHTYPE"""
        cloth_state = int(target.cflag.get(40, 0))
        cloth_names = []
        if cloth_state & 1:
            cloth_names.append("内裤")
        if cloth_state & 2:
            cloth_names.append("胸罩")
        if cloth_state & 4:
            cloth_names.append("上着")
        if cloth_state & 8:
            cloth_names.append("裙子")
        if cloth_state & 16:
            cloth_names.append("裤子")
        if cloth_state & 32:
            cloth_names.append("手套")
        if cloth_state & 64:
            cloth_names.append("套装")
        if not cloth_names:
            return "全裸"
        return "穿着" + "、".join(cloth_names)






    def _prompt_dress_category_choice(self) -> str:
        return self._prompt_choice()






    def _render_dress_category_menu(
        self,
        category_name: str,
        category_key: str,
        page: int,
        page_count: int,
        page_options: List[Dict[str, Any]],
    ) -> None:
        print(f"\n【{category_name}】")
        print("-" * 30)
        if page_count > 1:
            print(f" 第{page + 1}/{page_count}页")
        for option in page_options:
            req = int(option["req"])
            req_text = f" / 顺从{req}" if req > 0 else ""
            print(f" [{option['menu_id']}] {option['name']} ({option['cost']} pts{req_text})")
        if category_key == "normal":
            print(" [996] 服装黑市")
        if page_count > 1:
            print(" [997] 下一页")
            print(" [998] 上一页")
        print(" [100] Back")






    def _render_dress_main_menu(self, target: Character, category_labels: Dict[str, str]) -> None:
        print("\n【Dress/Equipment】")
        print("-" * 30)
        print(f" Target: {target.name}")
        print(f" Money: {self.interpreter.vars.money} pts")
        for line in self._get_dress_summary_lines(target):
            print(line)
        print("-" * 30)
        for choice_id in ("0", "1", "2", "3"):
            print(f" [{choice_id}] {category_labels[choice_id]}")
        if self._can_replace_diaper(target):
            print(" [4] 替换尿布")
        if self._can_discard_chastity_key(target):
            print(" [5] 扔掉贞操带的钥匙")
        print(" [7] 魔法装备")
        print(" [8] 武器")
        print(" [100] Back")






    def _run_dress_menu_loop(self, target: Character, categories: Dict[str, str], category_labels: Dict[str, str]) -> None:
        while True:
            if self._advance_dress_menu(target, categories, category_labels):
                return




    def _select_dress_category_option(self, page_options: List[Dict[str, Any]], sub_choice: str) -> Optional[Dict[str, Any]]:
        try:
            menu_id = int(sub_choice)
        except ValueError:
            return None
        return next((entry for entry in page_options if int(entry["menu_id"]) == menu_id), None)






    def _show_dress_category_menu(self, target: Character, category_key: str):
        category_name = self._get_dress_menu_title(category_key)
        options = self._get_dress_category_options(category_key, target)
        page = 0
        while True:
            page_options = self._get_dress_menu_page_options(category_key, options, page)
            page_count = self._get_dress_menu_page_count(category_key, options)
            self._render_dress_category_menu(category_name, category_key, page, page_count, page_options)
            sub_choice = self._prompt_dress_category_choice()
            if sub_choice == "100":
                return
            handled, category_key, category_name, options, page = self._handle_dress_category_choice(
                target,
                category_key,
                category_name,
                options,
                page,
                page_count,
                page_options,
                sub_choice,
            )
            if handled:
                continue




    def _target_has_clothing_block(self, target: Character) -> bool:
        clothing_enabled = self.interpreter.vars.get_flag(37) != 0
        clothing_state = target.cflag.get(40, 0)
        return bool(clothing_enabled and (clothing_state & 17))






    def _wearing_cloth_all(self, target: Character) -> int:
        """计算穿着全部衣物的状态 - 对应 @WEARING_CLOTH_ALL"""
        cloth_state = int(target.cflag.get(40, 0))
        return cloth_state






    def show_dress(self):
        """Dress / tailor menu aligned to the current TAILOR core reimplementation scope."""
        target = self._prepare_dress_menu_target()
        if target is None:
            return
        categories = self._get_dress_menu_categories()
        category_labels = self._get_dress_menu_choice_labels()
        self._run_dress_menu_loop(target, categories, category_labels)





