from __future__ import annotations
import os
"""Module for CommunicationMixin - MAOUNET通信"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CommunicationMixin:
    """Mixin providing MAOUNET通信 methods for GameEngine"""

    def _append_maounet_team_members(self, selected: Dict[str, Any]) -> int:
        pool = self._get_maounet_pool()
        existing_ids = {str(entry.get("share_id", "")) for entry in pool}
        added = 0
        level_cap = self.interpreter.vars.get_flag(76, 0)
        force_level_one = self.interpreter.vars.get_flag(77, 0) != 0

        for member in selected.get("members", []):
            share_id = str(member.get("share_id", ""))
            if share_id in existing_ids:
                continue
            imported = dict(member)
            level = int(imported.get("level", 1) or 1)
            if force_level_one:
                level = 1
            elif level_cap >= 0:
                level = min(level, max(1, level_cap))
            imported["level"] = max(1, level)
            pool.append(imported)
            existing_ids.add(share_id)
            added += 1

        self._set_maounet_pool(pool)
        return added






    def _build_maounet_share_data(self, team_name: str, slot: int, selected_chars: List[Character]) -> Dict[str, Any]:
        timestamp = int(datetime.now().timestamp() * 1000)
        members = []
        for offset, char in enumerate(selected_chars):
            char.cflag[190] = timestamp + offset
            payload = self._serialize_maounet_character(char)
            payload["share_id"] = str(char.cflag[190])
            members.append(payload)
        return {
            "kind": "maounet_share",
            "team_name": team_name,
            "members": members,
            "text": f"{team_name} ({len(members)} heroes)",
            "date": datetime.now().isoformat(),
        }






    def _clear_maounet_pool(self) -> tuple[bool, str]:
        self._set_maounet_pool([])
        return True, "已清除登录的通信勇者信息。"






    def _deserialize_maounet_character(self, data: Dict[str, Any]) -> Character:
        char = Character()
        char.name = str(data.get("name", "通信勇者"))
        char.callname = str(data.get("callname", char.name))
        char.nick_name = str(data.get("nick_name", ""))
        for field in ["base", "maxbase", "abl", "exp", "juel", "talent", "mark", "palam", "equipt", "stain", "cflag", "cstr", "item"]:
            source = data.get(field, {})
            setattr(char, field, dict(source) if isinstance(source, dict) else {})
        template_id = int(data.get("template_id", 0) or 0)
        if template_id > 0:
            char.template_id = template_id
        char.cflag[190] = char.cflag.get(190, 0) or int(datetime.now().timestamp() * 1000)
        char.cflag[9] = int(data.get("level", char.cflag.get(9, 1) or 1))
        char.cflag[10] = int(data.get("training_count", char.cflag.get(10, 0)))
        return char




    def _export_maounet_team(self) -> tuple[bool, str]:
        candidates = self._list_maounet_export_candidates()
        if not candidates:
            return False, "没有可共享的奴隶。"

        print("\n【MAOUNET Export】")
        self._print_maounet_export_candidates(candidates)
        raw_choice = self._prompt_choice()
        if raw_choice == "100":
            return False, "已取消共享。"

        selected_indices = self._parse_maounet_selection(raw_choice)
        if selected_indices is None:
            return False, "输入格式无效。"
        if not selected_indices or len(selected_indices) > 5:
            return False, "请选择 1 到 5 名角色。"

        selected_chars, error = self._resolve_maounet_selected_characters(candidates, selected_indices)
        if error:
            return False, error

        slot, error = self._prompt_maounet_share_slot()
        if error:
            return False, error

        team_name = self._prompt_maounet_team_name(slot)
        save_data = self._build_maounet_share_data(team_name, slot, selected_chars)

        save_path = self.paths.save_slot_path(1000 + slot)
        with open(save_path, "wb") as save_file:
            pickle.dump(save_data, save_file)
        return True, f"已将 {len(selected_chars)} 名角色共享到槽位 {slot}。"






    def _get_maounet_pool(self) -> List[Dict[str, Any]]:
        store = self._load_global_store()
        pool = store.get("maounet_pool", [])
        return pool if isinstance(pool, list) else []






    def _handle_maounet_choice(self, choice: str) -> bool:
        if choice == "0":
            ok, message = self._export_maounet_team()
            print(f"\n{message}")
            self._pause()
            return True
        if choice == "1":
            ok, message = self._import_maounet_team()
            print(f"\n{message}")
            self._pause()
            return True
        if choice == "2":
            ok, message = self._clear_maounet_pool()
            print(f"\n{message}")
            self._pause()
            return True
        if choice == "3":
            self._show_maounet_level_cap_menu()
            return True
        if choice == "4":
            self._toggle_maounet_level_reset()
            return True
        if choice == "5" and self._is_makai_bank_enabled():
            self._show_maounet_bank_menu()
            return True
        return False






    def _handle_maounet_direct_choice(self, choice: str) -> bool:
        if choice in ("0", "1", "2"):
            return self._handle_maounet_pool_transfer_choice(choice)
        if choice in ("3", "4", "5"):
            return self._handle_maounet_settings_choice(choice)
        return False






    def _handle_maounet_level_cap_input(self, new_cap: str) -> None:
        try:
            self.interpreter.vars.set_flag(76, int(new_cap))
            print("\n通信勇者等级上限已更新。")
        except ValueError:
            print("\n输入无效。")






    def _handle_maounet_pool_transfer_choice(self, choice: str) -> bool:
        action_map = {
            "0": self._export_maounet_team,
            "1": self._import_maounet_team,
            "2": self._clear_maounet_pool,
        }
        action = action_map[choice]
        ok, message = action()
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_maounet_settings_choice(self, choice: str) -> bool:
        if choice == "3":
            self._show_maounet_level_cap_menu()
            return True
        if choice == "4":
            self._toggle_maounet_level_reset()
            return True
        if choice == "5" and self._is_makai_bank_enabled():
            self._show_maounet_bank_menu()
            return True
        return False






    def _import_maounet_team(self) -> tuple[bool, str]:
        shares = self._list_maounet_share_slots()
        if not shares:
            return False, "没有找到可导入的通信队伍。"

        print("\n【MAOUNET Import】")
        self._print_maounet_share_slots(shares)
        raw_choice = self._prompt_choice()
        if raw_choice == "99":
            return False, "已取消导入。"

        slot, error = self._parse_maounet_share_slot_choice(raw_choice)
        if error:
            return False, "输入无效。"

        selected = next((data for share_slot, data in shares if share_slot == slot), None)
        if selected is None:
            return False, "未找到对应的通信队伍。"

        added = self._append_maounet_team_members(selected)
        return True, f"{selected.get('team_name', '通信队伍')} 导入完成，新增 {added} 名通信勇者。"






    def _is_maounet_pool_entry_spawnable(self, entry: Dict[str, Any]) -> bool:
        template_id = int(entry.get("template_id", 0) or 0)
        if template_id <= 0:
            return True
        return self._find_character_by_template_id(template_id) is None






    def _list_maounet_export_candidates(self) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx == self.interpreter.vars.master:
                continue
            if char.cflag.get(1, 0):
                continue
            candidates.append((idx, char))
        return candidates






    def _list_maounet_share_slots(self) -> List[tuple[int, Dict[str, Any]]]:
        shares: List[tuple[int, Dict[str, Any]]] = []
        for slot in range(20):
            save_path = self.paths.save_slot_path(1000 + slot)
            if not os.path.exists(save_path):
                continue
            try:
                with open(save_path, "rb") as save_file:
                    data = pickle.load(save_file)
            except Exception:
                continue
            if isinstance(data, dict) and data.get("kind") == "maounet_share":
                shares.append((slot, data))
        return shares






    def _maounet_clear_imports(self) -> List[str]:
        """清除已导入的通信勇者 - 对应 @MAOUNET 清除"""
        v = self.interpreter.vars
        if hasattr(v, 'globals'):
            for key in list(v.globals.keys()):
                if key.startswith('maounet_'):
                    del v.globals[key]
        return ["已清除登录的通信勇者信息"]




    def _maounet_export(self, char_indices: List[int], team_name: str) -> Dict[str, Any]:
        """魔王网导出 - 对应 @EXPORT
        将指定角色导出到共享存档
        """
        v = self.interpreter.vars
        result = {'success': False, 'messages': [], 'team_name': team_name}

        if len(char_indices) > 5:
            result['messages'].append("一次最多送出5人！")
            return result

        # 验证角色
        valid_indices = []
        for idx in char_indices:
            if idx < 0 or idx >= len(v.chars):
                continue
            char = v.chars[idx]
            # 主人不可导出
            if idx == 0:
                result['messages'].append(f"{char.savestr}是主人，无法导出")
                continue
            # 敌方不可导出
            if char.cflag.get(1, 0):
                result['messages'].append(f"{char.savestr}是敌方角色，无法导出")
                continue
            valid_indices.append(idx)

        if not valid_indices:
            result['messages'].append("没有可导出的角色")
            return result

        # 保存导出数据
        import time
        export_data = {
            'team_name': team_name,
            'timestamp': int(time.time() * 1000),
            'characters': [],
        }

        for idx in valid_indices:
            char = v.chars[idx]
            char_data = {
                'name': char.savestr,
                'level': char.cflag.get(9, 0),
                'hp': char.base.get(0, 0),
                'maxhp': char.maxbase.get(0, 0),
                'job': self._get_job_name_for_char(idx),
                'train_count': char.cflag.get(10, 0),
                'cflag_190': int(time.time() * 1000) + idx,
            }
            export_data['characters'].append(char_data)

        # 保存到全局存档区
        if not hasattr(v, 'globals'):
            v.globals = {}
        save_slot = len([k for k in v.globals.keys() if k.startswith('maounet_')])
        v.globals[f'maounet_{save_slot}'] = export_data

        result['success'] = True
        char_names = [v.chars[idx].savestr for idx in valid_indices]
        result['messages'].append(f"已将 {', '.join(char_names)} 以「{team_name}」的名义保存")
        result['messages'].append("在其他存档中可以召来这些勇者！")
        return result




    def _maounet_import(self, slot: int) -> Dict[str, Any]:
        """魔王网导入 - 对应 @INPORT_A
        从共享存档导入勇者
        """
        v = self.interpreter.vars
        result = {'success': False, 'messages': [], 'characters': []}

        key = f'maounet_{slot}'
        if not hasattr(v, 'globals') or key not in v.globals:
            result['messages'].append("该存档位没有数据")
            return result

        export_data = v.globals[key]
        level_cap = v.flag.get(76, 999)

        for char_data in export_data.get('characters', []):
            # 等级上限检查
            if v.flag.get(77, 0):
                char_data['level'] = 1
            elif char_data['level'] > level_cap:
                char_data['level'] = level_cap

            result['characters'].append(char_data)

        result['success'] = True
        result['team_name'] = export_data.get('team_name', '')
        result['messages'].append(f"从「{export_data.get('team_name', '')}」导入了 {len(result['characters'])} 名勇者")
        return result




    def _maounet_list_saves(self) -> List[str]:
        """列出可用的通信存档"""
        v = self.interpreter.vars
        lines = []
        if not hasattr(v, 'globals'):
            lines.append("没有可用的通信数据")
            return lines

        for i in range(20):
            key = f'maounet_{i}'
            if key in v.globals:
                data = v.globals[key]
                team_name = data.get('team_name', '----')
                char_count = len(data.get('characters', []))
                lines.append(f"[{i:>3}] {team_name} ({char_count}人)")
            else:
                lines.append(f"[{i:>3}] ----")

        return lines

    # ========================================
    # INFRASTRUCTURE - 设施展示系统
    # 对应 ERB/INFRASTRUCTURE.ERB
    # ========================================

    _INFRASTRUCTURE_TYPES = {
        0: ('石像', 'FLAG:600', '被石化了的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。苦闷、惊愕、恍惚、悲壮，石像上浮现着各种各样的表情，好像在对欣赏的人诉说着什么。那些话语和传说，已经不会被传达到了吧……'),
        1: ('标本', 'FLAG:601', '被制成标本的是原勇者的美丽肢体，空洞的眼神注视着对面墙壁上的装饰。苦闷、恍惚、悲壮、达观，标本上浮现着各种各样的表情，好像在对欣赏的人诉说着什么。不过她们被冻结的心，已经不会再产生任何感情了吧……'),
        2: ('蜡像', 'FLAG:602', '被制成蜡像的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。苦闷、惊愕、恍惚、悲壮，蜡像上浮现着各种各样的表情，看上去好像马上就能活动。不过她们现在的身体，已经不会再做出什么动作了吧…'),
        3: ('人体模型人偶', 'FLAG:603', '被制成人体模型人偶的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。她们的四肢和头部、上下半身，都可以自由地拆卸，完全没有保留作为人的部分了。拆下来的零件，乱七八糟地散落一地，经常找不到哪个对应哪个，最后只有使用暴力硬装上去。在她们身上穿戴着不同仪式用的新服装作为展览，随着信仰堕落神的信徒越来越多，这种展览也变得热闹了。穿着不知廉耻的暴露乳房及其它身体局部的服装，在大众面前展示身段的她们，神色不动，静静伫立……'),
        4: ('球型关节人偶', 'FLAG:604', '被制成球型关节人偶的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。她们的四肢和头部、半身都可以自由活动，能做出许多活人做不出的匪夷所思的动作。虽然不能和她们做爱，但为了看她们诱惑的姿势慕名而来的游客，也是大有人在。无论是弄成什么样的猥琐动作，她们都不为所动，被随意摆布着……'),
        5: ('金属雕像', 'FLAG:605', '被制成金属雕像的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。每天，全部的金属雕像都在规定的时间里进行全身打磨，确保她们能发出美丽的光泽展示于人前。过分的美丽使得经常都忍不住要玩弄她们的全身，一不小心被玩坏了的，也有这么一部分。曾经美丽的残缺肢体，无论再怎么过分地玩弄，也不会引起反感，她们只是这么静静伫立着……'),
        6: ('冰雕', 'FLAG:606', '被制成冰雕的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。为了保持她们作为冰雕的身形，这里比其它区域的气温低了不少。冷得大家尿意都出来了，忍不住把尿撒到冰雕上的人相当不少，不过隔日，这些就会成为冰雕上的新的冰柱，迎宾一样地对着客人。无论对她们做出多么过分的事，都不会破坏她们的表情，继续把曾经美丽的肢体暴露在大众的眼前……'),
        7: ('宝石像', 'FLAG:607', '被制成宝石像的是原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。每天，全部的宝石像都在规定的时间里进行全身打磨，确保她们能发出耀眼的光辉展示于人前。经常有大量的精液沾在宝石像的身上，不过从来没有肇事者特意会回来擦掉。宝石像带着如泣如诉的生动表情，大概是被这份美丽所感动了吧……'),
        8: ('家具', 'FLAG:608', '原本是活生生的勇者们，现在被再造成无机的家具展出。烛台里点亮着蓝色火焰的蜡烛，花瓶中插着魔界特有的花朵。各式各样的工具和杂物都被放在柜子里，还有一些有用的小玩意。在这种场合，在桌子和椅子上休息的人也络绎不绝。以打倒魔王为己任的勇者们，现在作为家具在侍奉着魔界的魔物，可喜可贺，可喜可贺……'),
        9: ('画像', 'FLAG:609', '原本是活生生的勇者们，现在被弄成一幅画在展出着。通过画布前设置的水晶球，游客们能看到画里面的活动。在画的世界里，人们能欣赏到她们永远被持续凌辱着的样子。她们不断地求助着，不过这是无法传达到给看客的。于是凌辱天天持续着……'),
        11: ('石制喷水像', 'FLAG:611', '被石化了的是原勇者的美丽肢体，一个个都有独一无二的羞耻姿势和装饰。乳房、性器、尿道等地方被换成喷水装置的她们，正从各自的位置喷出有气势的漂亮涌泉。她们已经没有人类的基本羞耻了，今后也会保持着下流的动作，毫不扭捏地持续喷水吧……'),
        12: ('金属喷水像', 'FLAG:612', '被制成金属喷水像的是原勇者的美丽肢体，一个个都有独一无二的羞耻姿势和装饰。从乳房和性器等部位喷出的水柱，在阳光下闪耀着美丽的光辉。她们已经不再是人类了，今后也会保持着下流的姿势，作为喷水装置持续运转吧……'),
    }




    def _maounet_mod_print(self) -> List[str]:
        """Show MOD-specific buttons for MaouNet (bank button if enabled)."""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))
        lines: List[str] = []

        # 魔界银行按钮
        if self._get_bit(ex_flag_9000, 0):
            savings = int(g.get(9001, 0))
            lines.append(f"[5] 连接到魔界银行(目前存款{savings})")

        return lines




    def _maounet_mod_script(self, result: int) -> None:
        """Handle MOD-specific MaouNet commands (bank access if result == 5)."""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))

        # 魔界银行执行
        if result == 5 and self._get_bit(ex_flag_9000, 0):
            # Call the bank display
            self._show_makai_bank()

    # =========================================================================
    # EXECUTION (处刑系统)
    # =========================================================================



    def _maounet_set_level_cap(self, cap: int) -> None:
        """设置通信勇者等级上限 - 对应 @MAOUNET 设定"""
        v = self.interpreter.vars
        v.flag[76] = cap




    def _maounet_toggle_level1(self) -> bool:
        """切换通信勇者登场等级1 - 对应 @MAOUNET 切换"""
        v = self.interpreter.vars
        current = v.flag.get(77, 0)
        v.flag[77] = 0 if current else 1
        return v.flag[77] == 1




    def _parse_maounet_selection(self, raw_choice: str) -> Optional[List[int]]:
        selected_indices: List[int] = []
        try:
            for token in raw_choice.split(","):
                token = token.strip()
                if not token:
                    continue
                value = int(token)
                if value not in selected_indices:
                    selected_indices.append(value)
        except ValueError:
            return None
        return selected_indices






    def _parse_maounet_share_slot_choice(self, raw_choice: str) -> tuple[int, Optional[str]]:
        try:
            return int(raw_choice), None
        except ValueError:
            return 0, "输入无效。"






    def _pop_next_spawnable_maounet_entry(self, pool: List[Dict[str, Any]]) -> tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
        remaining = list(pool)
        for idx, entry in enumerate(remaining):
            if not self._is_maounet_pool_entry_spawnable(entry):
                continue
            selected = dict(remaining.pop(idx))
            return selected, remaining
        return None, remaining






    def _print_maounet_export_candidates(self, candidates: List[tuple[int, Character]]) -> None:
        print("-" * 30)
        for idx, char in candidates:
            level = self._get_character_level(char)
            print(f" [{idx}] {char.name}  LV{level}  HP {char.base.get(0, 0)}/{char.maxbase.get(0, 0)}  调教次数 {char.cflag.get(10, 0)}")
        print(" 一次最多选择 5 人，使用半角逗号分隔，例如: 1,3,4")
        print(" [100] Back")






    def _print_maounet_share_slots(self, shares: List[tuple[int, Dict[str, Any]]]) -> None:
        print("-" * 30)
        for slot, data in shares:
            team_name = data.get("team_name", f"Shared Team {slot}")
            member_count = len(data.get("members", []))
            date_text = data.get("date", "")
            print(f" [{slot}] {team_name}  ({member_count}人)  {date_text}")
        print(" [99] Back")






    def _prompt_maounet_share_slot(self) -> tuple[int, Optional[str]]:
        slot_text = self._prompt_choice("共享存档槽(0-19) >> ")
        try:
            slot = int(slot_text)
        except ValueError:
            return 0, "共享槽位无效。"
        if slot < 0 or slot > 19:
            return 0, "共享槽位必须在 0 到 19 之间。"
        return slot, None






    def _prompt_maounet_team_name(self, slot: int) -> str:
        team_name = self._prompt_choice("队伍名 >> ")
        if not team_name:
            team_name = f"Shared Team {slot}"
        return team_name






    def _render_maounet_level_cap_menu(self) -> None:
        print("\n请输入允许从其他存档来袭的勇者等级上限。")
        print("如果输入小于 0，则不会从其他存档共享勇者。")






    def _resolve_maounet_selected_characters(
        self,
        candidates: List[tuple[int, Character]],
        selected_indices: List[int],
    ) -> tuple[List[Character], Optional[str]]:
        selected_chars: List[Character] = []
        candidate_map = {idx: char for idx, char in candidates}
        for idx in selected_indices:
            char = candidate_map.get(idx)
            if char is None:
                return [], f"角色编号 {idx} 无法共享。"
            selected_chars.append(char)
        return selected_chars, None




    def _serialize_maounet_character(self, char: Character) -> Dict[str, Any]:
        return {
            "name": char.name,
            "callname": char.callname,
            "nick_name": char.nick_name,
            "base": dict(char.base),
            "maxbase": dict(char.maxbase),
            "abl": dict(char.abl),
            "exp": dict(char.exp),
            "juel": dict(char.juel),
            "talent": dict(char.talent),
            "mark": dict(char.mark),
            "palam": dict(char.palam),
            "equipt": dict(char.equipt),
            "stain": dict(char.stain),
            "cflag": dict(char.cflag),
            "cstr": dict(char.cstr),
            "item": dict(char.item),
            "level": self._get_character_level(char),
            "training_count": int(char.cflag.get(10, 0)),
            "template_id": self._get_character_template_id(char) or 0,
            "share_id": f"{int(char.cflag.get(190, 0))}:{char.name or char.callname or 'hero'}",
        }




    def _set_maounet_pool(self, pool: List[Dict[str, Any]]):
        store = self._load_global_store()
        store["maounet_pool"] = pool
        self._save_global_store(store)






    def _show_maounet_bank_menu(self):
        self._show_makai_bank_menu()






    def _show_maounet_clear_menu(self):
        self._show_result_message(self._clear_maounet_pool())






    def _show_maounet_export_menu(self):
        self._show_result_message(self._export_maounet_team())






    def _show_maounet_import_menu(self):
        self._show_result_message(self._import_maounet_team())






    def _show_maounet_level_cap_menu(self):
        self._render_maounet_level_cap_menu()
        new_cap = self._prompt_choice("Level cap >> ")
        self._handle_maounet_level_cap_input(new_cap)
        self._pause()






    def _spawn_maounet_pool_hero(self) -> Optional[str]:
        if not self._can_spawn_daily_enemy():
            return None
        pool = self._get_maounet_pool()
        if not pool:
            return None

        imported, remaining_pool = self._pop_next_spawnable_maounet_entry(pool)
        if imported is None:
            return None
        hero = self._deserialize_maounet_character(imported)
        self._prepare_spawned_invading_hero(
            hero,
            reset_import_level=bool(self.interpreter.vars.get_flag(77, 0)),
            apply_base_level_bonus=bool(self.interpreter.vars.get_flag(77, 0)),
        )
        self._append_character(hero)
        self._set_maounet_pool(remaining_pool)
        self._apply_spawned_hero_level_progression()
        return self._format_spawned_hero_entry_message(hero, origin="maounet")






    def _summarize_maounet_pool(self) -> str:
        pool = self._get_maounet_pool()
        if not pool:
            return "当前没有已登记的通信勇者。"
        preview = ", ".join(f"{entry.get('name', '通信勇者')} LV{entry.get('level', 1)}" for entry in pool[:5])
        if len(pool) > 5:
            preview += f" ... 共 {len(pool)} 人"
        return preview






    def _toggle_maounet_level_reset(self):
        self.interpreter.vars.set_flag(77, 0 if self.interpreter.vars.get_flag(77) else 1)
        print("\n通信勇者初始等级设定已切换。")
        self._pause()

    def show_communication(self):
        """MAOUNET communication menu based on the original ERB flow."""
        while True:
            if self._advance_communication_menu():
                return

    def _maounet(self):
        return self.call_erb_function('MAOUNET')





