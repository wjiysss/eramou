from __future__ import annotations
import os
"""Module for MonsterExtMixin - 怪物系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class MonsterExtMixin:
    """Mixin providing 怪物系统 methods for GameEngine"""

    def _add_monster_stock(self, monster_id: int, count: int) -> int:
        stock = self._get_monster_stock()
        current = max(0, int(stock.get(monster_id, 0)))
        updated = min(999, current + max(0, count))
        stock[monster_id] = updated
        return updated - current






    def _advance_monster_follower_summon_family_menu(self, family_choice: int, sex_choice: int) -> bool:
        candidates = self._get_monster_shop_template_candidates(family_choice)
        if not candidates:
            print("\n没有能召唤的魔物从者。")
            self._pause()
            return False

        while True:
            template_id = self._handle_monster_follower_template_choice(candidates)
            if template_id is None:
                return False

            selected = self._find_monster_shop_template_candidate(candidates, template_id)
            if selected is None:
                print("\nInvalid selection.")
                self._pause()
                continue

            if self._advance_monster_follower_summon_template_menu(template_id, sex_choice, selected):
                return True
        return False






    def _advance_monster_follower_summon_menu(self, family_entries: List[Dict[str, Any]]) -> bool:
        sex_choice = self._handle_monster_follower_sex_choice()
        if sex_choice is None:
            return False
        while True:
            family_choice = self._handle_monster_follower_family_choice(family_entries)
            if family_choice is None:
                return False
            if self._advance_monster_follower_summon_family_menu(family_choice, sex_choice):
                return True
        return False






    def _advance_monster_follower_summon_template_menu(self, template_id: int, sex_choice: int, selected: Dict[str, Any]) -> bool:
        required_level = int(selected["min_level"])
        family_values = self._get_monster_sacrifice_family_values(template_id, selected.get("template"))
        if self._handle_monster_follower_template_confirm(template_id, sex_choice, selected, family_values, required_level):
            return True
        return False






    def _advance_monster_follower_template_confirm_menu(
        self,
        template_id: int,
        sex_choice: int,
        family_values: List[int],
        required_level: int,
    ) -> bool:
        return self._handle_monster_follower_template_confirm_choice(template_id, sex_choice, family_values, required_level)






    def _apply_monster_birth_result(self, mother: Character) -> List[str]:
        messages: List[str] = []
        father_source = int(mother.cflag.get(102, 0))
        status = int(mother.cflag.get(1, 0))
        monster_id, birth_count = self._resolve_monster_birth_result(mother)

        if status == 9:
            messages.append(f"{mother.name} 生下的 {birth_count} 只{self._get_item_name(monster_id)} 全部被处理掉了。")
            return messages
        if father_source in (2, 3, 4, 7):
            messages.append(f"{mother.name} 生下的孩子启程了。")
            return messages

        gained = self._add_monster_stock(monster_id, birth_count)
        messages.append(f"{mother.name} 生下的 {gained} 只{self._get_item_name(monster_id)} 增加到了战斗力里。")
        if int(mother.cflag.get(111, 0)) != -2 and int(mother.talent.get(314, 0)) in (3, 4) and birth_count == 1 and random.randint(0, 1) == 0:
            twin_id = 172 if int(mother.talent.get(314, 0)) == 3 else 171
            extra = self._add_monster_stock(twin_id, 1)
            if extra > 0:
                messages.append(f"哦呀？！生了双胞胎呢！额外增加了 1 只{self._get_item_name(twin_id)}。")
        return messages






    def _apply_monster_birth_status_reset(self, target: Character) -> None:
        target.cflag[1] = 0






    def _apply_monster_follower_template(self, template_id: int, sex_choice: int, sacrifice_plan: Optional[Dict[int, int]] = None) -> tuple[bool, str]:
        if self._count_monster_followers() >= 30:
            return False, "召唤的魔物从者数量太多，魔界已经没有志愿者了……"

        candidate, required_level, cost, family_values, plan, candidate_error = self._prepare_monster_follower_template(
            template_id, sacrifice_plan
        )
        if candidate_error is not None:
            return False, candidate_error
        cost_error = self._validate_monster_follower_template_cost(cost)
        if cost_error is not None:
            return False, cost_error
        plan_error = self._validate_monster_follower_template_plan(plan, required_level)
        if plan_error is not None:
            return False, plan_error
        entry_error = self._validate_monster_follower_template_entry_map(plan, family_values)
        if entry_error is not None:
            return False, entry_error
        return self._apply_monster_follower_template_result(candidate, sex_choice, cost, plan)






    def _apply_monster_follower_template_result(self, candidate: Character, sex_choice: int, cost: int, plan: Dict[int, int]) -> tuple[bool, str]:
        new_char = candidate
        self._append_character(new_char)
        new_char.cflag[1] = 0
        new_char.talent[220] = 1
        new_char.talent[121] = 1 if sex_choice == 3 else 0
        new_char.talent[122] = 1 if sex_choice == 1 else 0
        self._spend_global_money(cost)
        self._consume_monster_stock(plan)

        summary = "，".join(self._summarize_monster_sacrifice_plan(plan))
        sex_label = {1: "男性", 2: "女性", 3: "扶她"}.get(sex_choice, "女性")
        return True, f"{new_char.name} 回应了你的召唤。性别: {sex_label}，消耗 {cost} 点金钱。祭品: {summary}"






    def _apply_monster_summon(self, weak_mode: bool = False) -> tuple[bool, str]:
        attempts = self._get_summon_attempt_count(weak_mode=weak_mode)
        added: Dict[int, int] = {}
        for _ in range(attempts + 1):
            monster_id = self._get_random_monster_id()
            summon_count = self._get_summon_stack_size(monster_id)
            gained = self._add_monster_stock(monster_id, summon_count)
            if gained > 0:
                added[monster_id] = added.get(monster_id, 0) + gained

        if not added:
            return False, "召唤完成，但库存已满，没有新的怪物加入。"

        summary = "，".join(f"{self._get_item_name(monster_id)} +{count}" for monster_id, count in sorted(added.items()))
        mode_name = "弱召唤" if weak_mode else "通常召唤"
        return True, f"{mode_name}完成，共新增 {sum(added.values())} 只怪物：{summary}"






    def _apply_monster_summon_entry(self, weak_mode: bool):
        ok, message = self._apply_monster_summon(weak_mode=weak_mode)
        print(f"\n{message}")
        self._pause()






    def _build_monster_sacrifice_entry_map(self, family_values: set[int]) -> Dict[int, Dict[str, int]]:
        return {int(entry["monster_id"]): entry for entry in self._get_monster_sacrifice_candidates(family_values)}






    def _build_monster_sacrifice_plan(self, family_values: set[int], required_level: int) -> Optional[Dict[int, int]]:
        candidates = self._get_monster_sacrifice_candidates(family_values)
        if not candidates:
            return None

        total_available = sum(entry["level"] * entry["count"] for entry in candidates)
        if total_available < required_level:
            return None

        plan: Dict[int, int] = {}
        remaining = required_level
        for entry in sorted(candidates, key=lambda value: value["level"], reverse=True):
            if remaining <= 0:
                break
            use_count = min(entry["count"], (remaining + entry["level"] - 1) // entry["level"])
            if use_count <= 0:
                continue
            plan[int(entry["monster_id"])] = int(use_count)
            remaining -= int(entry["level"]) * int(use_count)

        if remaining > 0:
            return None
        return plan






    def _consume_monster_stock(self, plan: Dict[int, int]):
        stock = self._get_monster_stock()
        for monster_id, count in plan.items():
            current = max(0, int(stock.get(monster_id, 0)))
            updated = max(0, current - max(0, int(count)))
            if updated <= 0:
                stock.pop(monster_id, None)
            else:
                stock[monster_id] = updated






    def _count_monster_followers(self) -> int:
        return sum(1 for char in self.interpreter.vars.chars[1:] if char.talent.get(220, 0))






    def _finalize_monster_follower_template_confirm_choice(
        self,
        template_id: int,
        sex_choice: int,
        family_values: List[int],
        required_level: int,
    ) -> bool:
        selected_plan = self._select_monster_sacrifice_plan(template_id, required_level, family_values)
        if selected_plan is None:
            return False

        ok, result_message = self._apply_monster_follower_template(template_id, sex_choice, sacrifice_plan=selected_plan)
        print(f"\n{result_message}")
        self._pause()
        return ok






    def _find_monster_shop_template_candidate(self, candidates: List[Dict[str, Any]], template_id: int) -> Optional[Dict[str, Any]]:
        return next((entry for entry in candidates if int(entry["template_id"]) == template_id), None)






    def _get_monster_count(self) -> int:
        return sum(max(0, int(count)) for count in self._get_monster_stock().values())






    def _get_monster_data(self, monster_id: int) -> Dict[str, int]:
        """Get monster stats based on MONSTER_DATA.ERB logic.

        Returns a dict with keys: id, race, level, attack, defense,
        speed, special, magic, resistance, count.
        """
        result: Dict[str, int] = {"id": monster_id}
        flag = self.interpreter.vars.flag
        chars = self.interpreter.vars.chars

        # Level calculation based on CFLAG:0:9 (dungeon level)
        dungeon_lv = 0
        if chars and len(chars) > 0:
            dungeon_lv = chars[0].cflag.get(9, 0)
        base_lv = dungeon_lv // 12 + 2
        if random.randint(0, 9) < (dungeon_lv % 10):
            base_lv += 1
        result["level"] = base_lv

        # Monster count from ITEM array
        item_count = self.interpreter.vars.item.get(monster_id, 0)
        if item_count <= 0:
            # All dead -> skeleton soldier
            result["id"] = 190
            result["race"] = 1  # 亚人
            result["count"] = random.randint(1, 10)
        elif item_count > 10:
            result["count"] = random.randint(1, 10)
        else:
            result["count"] = item_count

        # Base stats scale with level
        result["attack"] = base_lv * 8 + 10
        result["defense"] = base_lv * 5 + 5
        result["speed"] = base_lv * 3 + 5
        result["special"] = 0
        result["magic"] = 0
        result["resistance"] = 0

        # Race assignment based on monster_id ranges
        if 100 <= monster_id < 200:
            result["race"] = 1  # 亚人
        elif 200 <= monster_id < 300:
            result["race"] = 2  # 史莱姆
        elif 300 <= monster_id < 400:
            result["race"] = 5  # 触手
        elif 400 <= monster_id < 500:
            result["race"] = 10  # 兽
        elif 500 <= monster_id < 600:
            result["race"] = 9  # 女魔族
        elif monster_id >= 600:
            result["race"] = 8  # 男魔族 (event)
        else:
            result["race"] = 0

        # Boss flag for single monsters
        if result["count"] <= 1 and monster_id != 190:
            result["boss"] = 1
        else:
            result["boss"] = 0

        return result

    # ------------------------------------------------------------------
    # FUNC_CLOTH (服装功能)
    # ------------------------------------------------------------------





    def _get_monster_data_baseline(self, monster_id: int) -> Optional[Dict[int, int]]:
        cache = getattr(self, "_monster_data_baseline_cache", None)
        if cache is None:
            cache = self._load_monster_data_baseline_cache()
            self._monster_data_baseline_cache = cache
        return cache.get(monster_id)






    def _get_monster_data_full(self, monster_id: int) -> Dict[str, Any]:
        """获取完整怪物数据 - MONSTER_DATA.ERB"""
        _MONSTER_DATA = {
            100: {"name": "狗头人", "level": 1, "atk": 1, "def": 2, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 0},
            101: {"name": "哥布林", "level": 1, "atk": 2, "def": 1, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 0},
            102: {"name": "黏液怪", "level": 1, "atk": 1, "def": 2, "spd": -1, "special": 1, "magic": 0, "type": 2, "resist": 0},
            103: {"name": "龙头苍蝇", "level": 1, "atk": 1, "def": 1, "spd": 1, "special": 0, "magic": 0, "type": 3, "resist": 1},
            104: {"name": "丧尸", "level": 1, "atk": 2, "def": 2, "spd": -1, "special": 0, "magic": 0, "type": 0, "resist": 2},
            110: {"name": "兽人", "level": 2, "atk": 3, "def": 2, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 0},
            111: {"name": "熊地精", "level": 2, "atk": 2, "def": 3, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 0},
            112: {"name": "藤蔓怪", "level": 2, "atk": 2, "def": 2, "spd": 0, "special": 3, "magic": 0, "type": 4, "resist": 0},
            113: {"name": "丧尸虫", "level": 2, "atk": 3, "def": 3, "spd": -3, "special": 0, "magic": 0, "type": 5, "resist": 2},
            114: {"name": "丧尸猎犬", "level": 2, "atk": 4, "def": 1, "spd": 0, "special": 0, "magic": 0, "type": 10, "resist": 2},
            120: {"name": "蜥蜴人", "level": 3, "atk": 4, "def": 3, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 1},
            121: {"name": "食人魔", "level": 3, "atk": 3, "def": 4, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 0},
            122: {"name": "食铠者", "level": 3, "atk": 2, "def": 4, "spd": 0, "special": 4, "magic": 0, "type": 5, "resist": 4},
            123: {"name": "小仙子", "level": 3, "atk": 2, "def": 2, "spd": 2, "special": 5, "magic": 1, "type": 6, "resist": 0},
            124: {"name": "毒蜈蚣", "level": 3, "atk": 4, "def": 4, "spd": -1, "special": 0, "magic": 0, "type": 3, "resist": 0},
            130: {"name": "巨魔", "level": 4, "atk": 5, "def": 4, "spd": 0, "special": 6, "magic": 0, "type": 7, "resist": 6},
            131: {"name": "石像鬼", "level": 4, "atk": 4, "def": 5, "spd": 0, "special": 7, "magic": 0, "type": 8, "resist": 4},
            132: {"name": "小恶魔", "level": 4, "atk": 3, "def": 3, "spd": 2, "special": 0, "magic": 2, "type": 6, "resist": 0},
            133: {"name": "男巫", "level": 4, "atk": 0, "def": 4, "spd": 0, "special": 0, "magic": 3, "type": 8, "resist": 0},
            134: {"name": "报丧女妖", "level": 4, "atk": 4, "def": 3, "spd": 2, "special": 8, "magic": 0, "type": 9, "resist": 4},
            140: {"name": "下等恶魔", "level": 5, "atk": 6, "def": 5, "spd": 0, "special": 4, "magic": 4, "type": 8, "resist": 1},
            141: {"name": "地狱猎犬", "level": 5, "atk": 5, "def": 6, "spd": 0, "special": 9, "magic": 0, "type": 10, "resist": 1},
            142: {"name": "史莱姆", "level": 5, "atk": 2, "def": 8, "spd": 0, "special": 1, "magic": 0, "type": 2, "resist": 2},
            143: {"name": "女巫", "level": 5, "atk": 0, "def": 5, "spd": 0, "special": 0, "magic": 5, "type": 9, "resist": 0},
            144: {"name": "吸血树", "level": 5, "atk": 7, "def": 5, "spd": 0, "special": 3, "magic": 0, "type": 4, "resist": 0},
            150: {"name": "巨人", "level": 6, "atk": 8, "def": 6, "spd": 0, "special": 0, "magic": 0, "type": 7, "resist": 0},
            151: {"name": "奇美拉", "level": 6, "atk": 6, "def": 7, "spd": 0, "special": 9, "magic": 0, "type": 10, "resist": 1},
            152: {"name": "魅魔", "level": 6, "atk": 5, "def": 6, "spd": 0, "special": 11, "magic": 4, "type": 9, "resist": 0},
            153: {"name": "男祭司", "level": 6, "atk": 6, "def": 6, "spd": 0, "special": 0, "magic": 6, "type": 8, "resist": 4},
            154: {"name": "夜少女", "level": 6, "atk": 6, "def": 8, "spd": 0, "special": 15, "magic": 0, "type": 9, "resist": 0},
            160: {"name": "女忍", "level": 7, "atk": 8, "def": 7, "spd": 0, "special": 11, "magic": 0, "type": 9, "resist": 0},
            161: {"name": "黑暗骑士", "level": 7, "atk": 8, "def": 9, "spd": -1, "special": 15, "magic": 0, "type": 8, "resist": 4},
            162: {"name": "食脑魔", "level": 7, "atk": 10, "def": 5, "spd": 0, "special": 12, "magic": 0, "type": 11, "resist": 7},
            163: {"name": "女祭司", "level": 7, "atk": 7, "def": 7, "spd": 0, "special": 0, "magic": 6, "type": 9, "resist": 4},
            164: {"name": "小精灵", "level": 7, "atk": 6, "def": 6, "spd": 0, "special": 8, "magic": 2, "type": 6, "resist": 2},
            170: {"name": "忍者", "level": 8, "atk": 9, "def": 8, "spd": 0, "special": 8, "magic": 0, "type": 8, "resist": 3},
            171: {"name": "无头骑士", "level": 8, "atk": 9, "def": 9, "spd": 0, "special": 15, "magic": 0, "type": 8, "resist": 2},
            172: {"name": "吸血鬼", "level": 8, "atk": 8, "def": 8, "spd": 0, "special": 11, "magic": 4, "type": 8, "resist": 2},
            173: {"name": "幽灵", "level": 8, "atk": 0, "def": 9, "spd": 0, "special": 8, "magic": 4, "type": 0, "resist": 4},
            174: {"name": "死亡蝎", "level": 8, "atk": 11, "def": 4, "spd": 2, "special": 4, "magic": 0, "type": 3, "resist": 1},
            180: {"name": "大恶魔", "level": 9, "atk": 12, "def": 10, "spd": 0, "special": 12, "magic": 5, "type": 8, "resist": 3},
            181: {"name": "死亡领主", "level": 9, "atk": 10, "def": 12, "spd": 2, "special": 13, "magic": 6, "type": 8, "resist": 4},
            182: {"name": "莉莉丝", "level": 9, "atk": 10, "def": 10, "spd": 0, "special": 11, "magic": 4, "type": 9, "resist": 1},
            183: {"name": "梦魇", "level": 9, "atk": 11, "def": 11, "spd": 2, "special": 10, "magic": 2, "type": 12, "resist": 2},
            184: {"name": "眼魔", "level": 9, "atk": 11, "def": 11, "spd": 0, "special": 12, "magic": 0, "type": 5, "resist": 6},
            190: {"name": "骷髅兵", "level": 1, "atk": 1, "def": 1, "spd": 0, "special": 0, "magic": 0, "type": 0, "resist": 0},
            191: {"name": "黑暗救世主", "level": 30, "atk": 35, "def": 30, "spd": 1, "special": 13, "magic": 5, "type": 8, "resist": 6},
            192: {"name": "九尾", "level": 30, "atk": 30, "def": 40, "spd": 1, "special": 15, "magic": 9, "type": 9, "resist": 5},
            193: {"name": "混沌龙", "level": 30, "atk": 50, "def": 40, "spd": 0, "special": 14, "magic": 0, "type": 10, "resist": 3},
            600: {"name": "野蛮人", "level": 1, "atk": 2, "def": 1, "spd": 0, "special": 0, "magic": 0, "type": 8, "resist": 0},
            601: {"name": "巨型蚂蚁", "level": 1, "atk": 3, "def": 2, "spd": -1, "special": 0, "magic": 0, "type": 3, "resist": 1},
            602: {"name": "红兽人", "level": 2, "atk": 2, "def": 3, "spd": 0, "special": 0, "magic": 0, "type": 1, "resist": 1},
            603: {"name": "食人花", "level": 2, "atk": 4, "def": 2, "spd": -1, "special": 3, "magic": 0, "type": 4, "resist": 0},
            604: {"name": "大猩猩", "level": 3, "atk": 4, "def": 4, "spd": -1, "special": 0, "magic": 0, "type": 10, "resist": 0},
            605: {"name": "纹身女孩", "level": 4, "atk": 3, "def": 3, "spd": 1, "special": 16, "magic": 6, "type": 9, "resist": 1},
            606: {"name": "大象", "level": 5, "atk": 6, "def": 6, "spd": -1, "special": 4, "magic": 0, "type": 10, "resist": 0},
            607: {"name": "红萨满", "level": 5, "atk": 4, "def": 4, "spd": 1, "special": 12, "magic": 5, "type": 8, "resist": 1},
            608: {"name": "巨魔法师", "level": 6, "atk": 6, "def": 7, "spd": 0, "special": 6, "magic": 4, "type": 7, "resist": 6},
            609: {"name": "森林龙", "level": 6, "atk": 8, "def": 8, "spd": 0, "special": 9, "magic": 2, "type": 10, "resist": 6},
        }
        return _MONSTER_DATA.get(monster_id, {"name": "未知", "level": 0, "atk": 0, "def": 0, "spd": 0, "special": 0, "magic": 0, "type": 0, "resist": 0})

    # ------------------------------------------------------------------
    # TRAIN_MESSAGE 调教消息集成
    # ------------------------------------------------------------------






    def _get_monster_sacrifice_candidates(self, family_values: set[int]) -> List[Dict[str, int]]:
        stock = self._get_monster_stock()
        candidates: List[Dict[str, int]] = []
        for monster_id in range(100, 200):
            count = max(0, int(stock.get(monster_id, 0)))
            if count <= 0:
                continue
            monster_level = max(0, (monster_id - 100) // 10 + 1)
            monster_family = (monster_id - 100) % 10 + 1
            if monster_family not in family_values:
                continue
            candidates.append({
                "monster_id": monster_id,
                "level": monster_level,
                "count": count,
            })
        return candidates






    def _get_monster_sacrifice_family_values(self, template_id: int, candidate: Optional[Character] = None) -> set[int]:
        if candidate is None:
            candidate = self._get_character_template_baseline(template_id)
        if candidate is None:
            return set()
        family_values = {int(candidate.talent.get(319, 0))}
        if template_id == 205:
            return {5, 11}
        if template_id in (208, 209):
            return {8, 9}
        if template_id == 210:
            return {10, 12}
        return family_values






    def _get_monster_sacrifice_plan_level(self, plan: Dict[int, int]) -> int:
        total_level = 0
        for monster_id, count in plan.items():
            level = max(0, (monster_id - 100) // 10 + 1)
            total_level += level * max(0, int(count))
        return total_level






    def _get_monster_shop_family_map(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 1, "name": "兽人类", "family_values": {1}},
            {"menu_id": 2, "name": "史莱姆类", "family_values": {2}},
            {"menu_id": 3, "name": "昆虫类", "family_values": {3}},
            {"menu_id": 4, "name": "植物类", "family_values": {4}},
            {"menu_id": 5, "name": "触手类", "family_values": {5, 11}},
            {"menu_id": 6, "name": "妖精类", "family_values": {6}},
            {"menu_id": 7, "name": "巨人类", "family_values": {7}},
            {"menu_id": 8, "name": "魔人类", "family_values": {8, 9}},
            {"menu_id": 9, "name": "魔兽类", "family_values": {10, 12}},
        ]






    def _get_monster_shop_template_candidates(self, family_menu_id: int) -> List[Dict[str, Any]]:
        family_entry = next((entry for entry in self._get_monster_shop_family_map() if entry["menu_id"] == family_menu_id), None)
        if family_entry is None:
            return []

        candidates: List[Dict[str, Any]] = []
        for item_id in range(201, 281):
            item_def = self._get_item_definition(item_id)
            if item_def is None:
                continue
            template = self._get_character_template_baseline(item_id)
            if template is None:
                continue
            family_value = int(template.talent.get(319, 0))
            if family_value not in family_entry["family_values"]:
                continue
            candidates.append({
                "item_id": item_id,
                "template_id": item_id,
                "name": str(item_def["name"]),
                "min_level": int(item_def["price"]),
                "family_value": family_value,
                "template": template,
            })
        return candidates






    def _get_monster_stock(self) -> Dict[int, int]:
        stock = self.interpreter.vars.items.get("monster_stock")
        if isinstance(stock, dict):
            return stock
        stock = {}
        self.interpreter.vars.items["monster_stock"] = stock
        return stock






    def _handle_monster_follower_family_choice(self, family_entries: List[Dict[str, Any]]) -> Optional[str]:
        return self._prompt_monster_follower_family(family_entries)






    def _handle_monster_follower_sex_choice(self) -> Optional[int]:
        return self._prompt_monster_follower_sex()






    def _handle_monster_follower_template_choice(self, candidates: List[Dict[str, Any]]) -> Optional[int]:
        return self._prompt_monster_follower_template(candidates)






    def _handle_monster_follower_template_confirm(self, template_id: int, sex_choice: int, selected: Dict[str, Any], family_values: List[int], required_level: int) -> bool:
        print("\n【召唤确认】")
        print("-" * 30)
        print(f" 目标: {selected['name']}")
        print(f" 需要金钱: {required_level * 135}")
        print(f" 需要祭品等级合计: {required_level}")
        if not self._can_prepare_monster_follower_sacrifice_plan(family_values, required_level):
            print(" 目前没有足够的同系怪物祭品。")
            self._pause()
            return False
        print(" 可用祭品充足，进入手动选择祭品。")
        print(" [0] 确认召唤")
        print(" [100] 返回")
        return self._advance_monster_follower_template_confirm_menu(template_id, sex_choice, family_values, required_level)






    def _handle_monster_follower_template_confirm_choice(
        self,
        template_id: int,
        sex_choice: int,
        family_values: List[int],
        required_level: int,
    ) -> bool:
        confirm_result = self._prompt_monster_follower_template_confirm_choice()
        return self._resolve_monster_follower_template_confirm_choice(template_id, sex_choice, family_values, required_level, confirm_result)






    def _handle_monster_follower_template_confirm_command_choice(self, confirm_choice: str) -> Optional[str]:
        if confirm_choice == "100":
            return "cancel"
        if confirm_choice == "0":
            return "confirm"
        return None






    def _handle_monster_sacrifice_plan_confirmation(self, plan: Dict[int, int], choice_raw: str, required_level: int) -> Optional[Dict[int, int]]:
        if choice_raw == "0" and self._get_monster_sacrifice_plan_level(plan) >= required_level:
            return dict(plan)
        if choice_raw == "100":
            return None
        print("\nInvalid selection.")
        self._pause()
        return {}






    def _handle_monster_sacrifice_plan_entry_choice(
        self,
        entry_map: Dict[int, Dict[str, int]],
        plan: Dict[int, int],
        choice_raw: str,
    ) -> bool:
        try:
            monster_id = int(choice_raw)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        entry = entry_map.get(monster_id)
        if entry is None:
            print("\nInvalid selection.")
            self._pause()
            return False
        selected = plan.get(monster_id, 0)
        if selected >= int(entry["count"]):
            print("\n已经没有更多可选数量了。")
            self._pause()
            return False
        plan[monster_id] = selected + 1
        return True






    def _load_monster_data_baseline_cache(self) -> Dict[int, Dict[int, int]]:
        erb_path = os.path.join(self.paths.root_dir, "ERB", "MONSTER_DATA.ERB")
        try:
            with open(erb_path, "r", encoding="utf-8-sig") as file:
                text = file.read()
        except OSError:
            return {}
        function_to_monster = self._parse_monster_data_dispatch_map(text)
        function_data = self._parse_monster_data_function_baselines(text)
        return {
            monster_id: function_data[function_name]
            for monster_id, function_name in function_to_monster.items()
            if function_name in function_data
        }




    def _parse_monster_data_dispatch_map(self, text: str) -> Dict[int, str]:
        dispatch: Dict[int, str] = {}
        current_id: Optional[int] = None
        for raw_line in text.splitlines():
            line = raw_line.split(";", 1)[0].strip()
            match_id = re.match(r"(?:IF|ELSEIF)\s+INUM\s*==\s*(\d+)", line)
            if match_id:
                current_id = int(match_id.group(1))
                continue
            if current_id is None:
                continue
            match_call = re.match(r"CALL\s+([A-Z0-9_]+)\s*,\s*TOP\b", line)
            if match_call:
                dispatch[current_id] = match_call.group(1)
                current_id = None
        return dispatch






    def _parse_monster_data_function_baselines(self, text: str) -> Dict[str, Dict[int, int]]:
        baselines: Dict[str, Dict[int, int]] = {}
        current_function: Optional[str] = None
        current_data: Dict[int, int] = {}
        for raw_line in text.splitlines():
            line = raw_line.split(";", 1)[0].strip()
            match_func = re.match(r"@([A-Z0-9_]+)\s*,", line)
            if match_func:
                current_function = match_func.group(1)
                current_data = {}
                continue
            if current_function is None:
                continue
            match_value = re.match(r"E:\(ARG:0(?:\+(\d+))?\)\s*=\s*(-?\d+)", line)
            if match_value:
                offset = int(match_value.group(1) or 0)
                current_data[offset] = int(match_value.group(2))
                continue
            if line.startswith("RETURN"):
                if current_data:
                    baselines[current_function] = current_data
                current_function = None
                current_data = {}
        return baselines






    def _prepare_monster_follower_template(self, template_id: int, sacrifice_plan: Optional[Dict[int, int]] = None) -> tuple[Optional[Character], int, int, set[int], Optional[Dict[int, int]], Optional[str]]:
        candidate = self._instantiate_character_from_template(template_id)
        if candidate is None:
            return None, 0, 0, set(), None, "缺少对应的魔物从者模板。"

        required_level = int(self._get_item_definition(template_id)["price"]) if self._get_item_definition(template_id) else 0
        cost = required_level * 135
        family_values = self._get_monster_sacrifice_family_values(template_id, candidate)
        plan = dict(sacrifice_plan) if sacrifice_plan is not None else self._build_monster_sacrifice_plan(family_values, required_level)
        return candidate, required_level, cost, family_values, plan, None






    def _prompt_monster_follower_family(self, family_entries: List[Dict[str, Any]]) -> Optional[int]:
        print("\n【召唤魔物从者】")
        print("-" * 30)
        print(" 请选择魔物从者的种类")
        for entry in family_entries:
            candidates = self._get_monster_shop_template_candidates(int(entry["menu_id"]))
            if not candidates:
                continue
            print(f" [{entry['menu_id']}] {entry['name']}")
        print(" [100] 返回")
        family_choice_raw = self._prompt_choice()
        if family_choice_raw == "100":
            return None
        try:
            family_choice = int(family_choice_raw)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        return family_choice






    def _prompt_monster_follower_sex(self) -> Optional[int]:
        print("\n【召唤魔物从者】")
        print("-" * 30)
        print(" 请选择要召唤的魔物从者的性别")
        print(" [1] 男性")
        print(" [2] 女性")
        print(" [3] 扶她")
        print(" [100] 返回")
        sex_choice_raw = self._prompt_choice()
        if sex_choice_raw == "100":
            return None
        try:
            sex_choice = int(sex_choice_raw)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        if sex_choice not in (1, 2, 3):
            print("\nInvalid selection.")
            self._pause()
            return None
        return sex_choice






    def _prompt_monster_follower_template(self, candidates: List[Dict[str, Any]]) -> Optional[int]:
        print("\n【可召唤的精英魔物从者】")
        print("-" * 30)
        for entry in candidates:
            cost = int(entry["min_level"]) * 135
            print(f" [{entry['template_id']}] {entry['name']} 最低等级:{entry['min_level']} 金钱:{cost}")
        print(" [100] 返回")
        template_choice_raw = self._prompt_choice()
        if template_choice_raw == "100":
            return None
        try:
            template_id = int(template_choice_raw)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        return template_id






    def _prompt_monster_follower_template_confirm_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_monster_sacrifice_confirmation(self) -> None:
        print(" [0] 确认这些祭品")
        print(" [100] 返回")






    def _render_monster_sacrifice_plan_entries(self, entry_map: Dict[int, Dict[str, int]], plan: Dict[int, int]) -> None:
        for monster_id in sorted(entry_map):
            entry = entry_map[monster_id]
            selected = plan.get(monster_id, 0)
            print(
                f" [{monster_id}] {self._get_item_name(monster_id)} "
                f"LV{entry['level']} 持有:{entry['count']} 已选:{selected}"
            )
        print(" [100] 返回")






    def _render_monster_sacrifice_plan_menu(self, template_id: int, required_level: int, plan: Dict[int, int], entry_map: Dict[int, Dict[str, int]]):
        current_level = self._get_monster_sacrifice_plan_level(plan)
        remaining_level = max(0, required_level - current_level)
        print("\n【选择祭品】")
        print("-" * 30)
        print(f" 目标: {self._get_item_name(template_id)}")
        print(f" 剩余等级需求: {remaining_level}")
        print(" 当前已选择的怪物:")
        for line in self._summarize_monster_sacrifice_plan(plan):
            print(line)
        print("-" * 30)
        return current_level






    def _resolve_monster_birth_result(self, mother: Character) -> tuple[int, int]:
        father_id = int(mother.cflag.get(111, 0))
        base_count = random.randint(1, 3)
        monster_id = random.choice([191, 192, 193])

        if father_id == -2 and int(mother.talent.get(314, 0)) == 5:
            if random.randint(0, 1) == 0:
                monster_id = 141
                base_count += random.randint(0, 2)
            else:
                monster_id = 151
            return monster_id, base_count

        if father_id == -2:
            monster_id = 114 if random.randint(0, 1) == 0 else 141
            base_count += random.randint(0, 2)
            return monster_id, base_count

        if int(mother.cflag.get(112, 0)) > 0 and father_id == -3:
            return int(mother.cflag.get(112, 0)), base_count

        return monster_id, base_count






    def _resolve_monster_follower_template_confirm_choice(
        self,
        template_id: int,
        sex_choice: int,
        family_values: List[int],
        required_level: int,
        confirm_choice: str,
    ) -> bool:
        confirm_state = self._handle_monster_follower_template_confirm_command_choice(confirm_choice)
        if confirm_state is None:
            print("\nInvalid selection.")
            self._pause()
            return False
        if confirm_state in {"cancel", "retry"}:
            return False

        return self._finalize_monster_follower_template_confirm_choice(template_id, sex_choice, family_values, required_level)






    def _select_monster_sacrifice_plan(self, template_id: int, required_level: int, family_values: set[int]) -> Optional[Dict[int, int]]:
        entry_map = self._build_monster_sacrifice_entry_map(family_values)
        if not entry_map:
            print("\n没有能作为祭品的同系怪物。")
            self._pause()
            return None

        total_available = sum(int(entry["level"]) * int(entry["count"]) for entry in entry_map.values())
        if total_available < required_level:
            print("\n＊作为祭品的怪物等级不足＊")
            self._pause()
            return None

        plan: Dict[int, int] = {}
        while True:
            current_level = self._render_monster_sacrifice_plan_menu(template_id, required_level, plan, entry_map)
            if current_level >= required_level:
                self._prompt_monster_sacrifice_confirmation()
            else:
                self._render_monster_sacrifice_plan_entries(entry_map, plan)

            choice_raw = self._prompt_choice()
            if current_level >= required_level:
                confirmed = self._handle_monster_sacrifice_plan_confirmation(plan, choice_raw, required_level)
                if confirmed is not None:
                    return confirmed
                continue

            if choice_raw == "100":
                return None
            self._handle_monster_sacrifice_plan_entry_choice(entry_map, plan, choice_raw)






    def _show_monster_follower_summon_menu(self):
        ok, message = self._can_open_monster_shop()
        if not ok:
            print(f"\n{message}")
            self._pause()
            return
        if self._count_monster_followers() >= 30:
            print("\n召唤的魔物从者数量太多，魔界已经没有志愿者了……")
            self._pause()
            return

        family_entries = self._get_monster_shop_family_map()
        while True:
            if self._advance_monster_follower_summon_menu(family_entries):
                return






    def _show_monster_stock_menu(self):
        print("\n【Monster Stock】")
        for line in self._summarize_monster_stock_lines():
            print(line)
        self._pause()






    def _summarize_monster_sacrifice_plan(self, plan: Dict[int, int]) -> List[str]:
        lines: List[str] = []
        for monster_id, count in sorted(plan.items()):
            level = max(0, (monster_id - 100) // 10 + 1)
            lines.append(f" {self._get_item_name(monster_id)} Lv{level} x{count}")
        lines.append(f" 合计等级: {self._get_monster_sacrifice_plan_level(plan)}")
        return lines






    def _summarize_monster_stock_lines(self, limit: int = 12) -> List[str]:
        stock = self._get_monster_stock()
        populated = [(monster_id, count) for monster_id, count in sorted(stock.items()) if count > 0]
        if not populated:
            return [" 当前没有任何怪物库存。"]
        lines: List[str] = []
        for monster_id, count in populated[:limit]:
            lines.append(f" [{monster_id}] {self._get_item_name(monster_id)} x{count}")
        if len(populated) > limit:
            lines.append(f" ... 还有 {len(populated) - limit} 种")
        return lines






    def _summon_monster(self, mode: int = 0) -> List[str]:
        """召喚 - 对应 @SUMMON_MONSTER"""
        messages: List[str] = []
        return messages



    def _toggle_monster_interception_block(self) -> None:
        self.interpreter.vars.set_flag(5, int(self.interpreter.vars.get_flag(5, 0)) ^ 16)






    def _validate_monster_follower_template_cost(self, cost: int) -> Optional[str]:
        if self.interpreter.vars.money < cost:
            return "虽然魔物从者都不是物质的女孩，但必要的金钱总是要准备的吧。"
        return None






    def _validate_monster_follower_template_entry_map(self, plan: Dict[int, int], family_values: set[int]) -> Optional[str]:
        entry_map = self._build_monster_sacrifice_entry_map(family_values)
        for monster_id, count in plan.items():
            entry = entry_map.get(monster_id)
            if entry is None:
                return "祭品中包含了不符合条件的怪物。"
            if int(count) > int(entry["count"]):
                return "选择的祭品数量超过了库存。"
        return None






    def _validate_monster_follower_template_plan(self, plan: Optional[Dict[int, int]], required_level: int) -> Optional[str]:
        if plan is None:
            return "没有足够的同系怪物作为祭品，或祭品合计等级不足。"
        if self._get_monster_sacrifice_plan_level(plan) < required_level:
            return "祭品合计等级不足。"
        return None





