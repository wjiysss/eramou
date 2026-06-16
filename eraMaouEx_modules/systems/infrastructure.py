from __future__ import annotations
"""Module for InfrastructureMixin - 基础设施"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class InfrastructureMixin:
    """Mixin providing 基础设施 methods for GameEngine"""

    def _advance_facility_exhibit_menu(self):
        self._render_facility_exhibit_menu()
        choice = self._prompt_choice()
        return self._handle_facility_exhibit_choice(choice)




    def _advance_facility_menu(self, facilities: List[Dict[str, Any]]) -> bool:
        self._render_facility_menu()
        choice = self._prompt_facility_choice()
        if choice == "100":
            return True
        if self._handle_facility_menu_choice(facilities, choice):
            return False
        print("\nInvalid selection.")
        self._pause()
        return False




    def _build_facility_exhibit_detail_lines(self, menu_id: int) -> List[str]:
        entry = self._get_facility_exhibit_entry(menu_id)
        if entry is None:
            return ["无效的展品分类。"]
        count = self.interpreter.vars.get_flag(int(entry["flag_id"]), 0)
        if count <= 0:
            return [str(entry["empty"])]
        return [
            f"博物馆内现在有 {count} 个{entry['name']}。",
            str(entry["summary"]),
        ]






    def _build_facility_exhibit_overview_lines(self) -> List[str]:
        total = self.interpreter.vars.get_flag(84, 0)
        if total <= 0:
            return ["还没制作过展品。"]
        lines = [
            f"博物馆内现在有 {total} 个展品。",
            "原勇者的身体被改造成了各式标本、雕像与陈列品。",
        ]
        fountain_counts: List[str] = []
        stone_fountain = int(self.interpreter.vars.get_flag(611, 0))
        metal_fountain = int(self.interpreter.vars.get_flag(612, 0))
        if stone_fountain > 0:
            fountain_counts.append(f"石制喷水像 x{stone_fountain}")
        if metal_fountain > 0:
            fountain_counts.append(f"金属喷水像 x{metal_fountain}")
        if fountain_counts:
            lines.append("特殊展区：" + " / ".join(fountain_counts))
        categories = []
        for entry in self._get_facility_exhibit_definitions():
            count = self.interpreter.vars.get_flag(int(entry["flag_id"]), 0)
            if count > 0:
                categories.append(f"{entry['name']} x{count}")
        if categories:
            lines.append("当前展区：" + " / ".join(categories))
        return lines






    def _can_open_infrastructure(self) -> tuple[bool, str]:
        if self.interpreter.vars.assi < 0:
            return False, "没有待机中的奴隶，没有人能保护你，并挡住可能出现的勇者。"
        if self.interpreter.vars.assi >= len(self.interpreter.vars.chars):
            return False, "没有待机中的奴隶，没有人能保护你，并挡住可能出现的勇者。"
        guard = self.interpreter.vars.chars[self.interpreter.vars.assi]
        if guard.base.get(0, 0) < 1:
            return False, "没有待机中的奴隶，没有人能保护你，并挡住可能出现的勇者。"
        return True, ""




    def _get_facility_definitions(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 1, "global_id": 10, "name": "拷问设施", "base_cost": 1200, "desc": "提升调教辅助效率"},
            {"menu_id": 2, "global_id": 11, "name": "休养设施", "base_cost": 900, "desc": "提升休息恢复量"},
            {"menu_id": 3, "global_id": 12, "name": "研究设施", "base_cost": 1500, "desc": "提升研究所层级"},
        ]




    def _get_facility_exhibit_definitions(self) -> List[Dict[str, Any]]:
        return [
            {"menu_id": 0, "flag_id": 600, "name": "石像", "empty": "还没制作过石像。", "summary": "被石化的原勇者以各异的姿势与表情陈列着。"},
            {"menu_id": 1, "flag_id": 601, "name": "标本", "empty": "还没制作过标本。", "summary": "被制成标本的原勇者保持着冻结的神态。"},
            {"menu_id": 2, "flag_id": 602, "name": "蜡像", "empty": "还没制作过蜡像。", "summary": "蜡像看上去几乎像下一刻就会重新活动。"},
            {"menu_id": 3, "flag_id": 603, "name": "人体模型人偶", "empty": "还没制作过人体模型人偶。", "summary": "可拆卸的人偶被换上仪式用服装公开展示。"},
            {"menu_id": 4, "flag_id": 604, "name": "球型关节人偶", "empty": "还没制作过球型关节人偶。", "summary": "四肢与半身可自由摆弄，展示出活人做不到的姿态。"},
            {"menu_id": 5, "flag_id": 605, "name": "金属雕像", "empty": "还没制作过金属雕像。", "summary": "每日被打磨得光亮夺目，残缺也成了展览的一部分。"},
            {"menu_id": 6, "flag_id": 606, "name": "冰雕", "empty": "还没制作过冰雕。", "summary": "低温区域里的冰雕持续暴露着曾经美丽的肢体。"},
            {"menu_id": 7, "flag_id": 607, "name": "宝石像", "empty": "还没制作过宝石像。", "summary": "宝石般的光辉衬托出仍旧生动的表情。"},
            {"menu_id": 8, "flag_id": 608, "name": "家具", "empty": "还没制作过家具。", "summary": "原本的勇者被改造成无机家具供魔界使用。"},
            {"menu_id": 9, "flag_id": 609, "name": "画像", "empty": "还没制作过画像。", "summary": "被定格在画中的原勇者成为可随意观赏的装饰。"},
            {"menu_id": 11, "flag_id": 611, "name": "石制喷水像", "empty": "还没制作过石制喷水像。", "summary": "石制喷水像被摆成迎宾般的姿态。"},
            {"menu_id": 12, "flag_id": 612, "name": "金属喷水像", "empty": "还没制作过金属喷水像。", "summary": "金属喷水像在展区里持续反射着夺目的光泽。"},
        ]




    def _get_facility_exhibit_entry(self, menu_id: int) -> Optional[Dict[str, Any]]:
        return next((entry for entry in self._get_facility_exhibit_definitions() if entry["menu_id"] == menu_id), None)




    def _get_facility_upgrade_cost(self, facility: Dict[str, Any]) -> int:
        level = self._get_global_level(int(facility["global_id"]))
        return int(facility["base_cost"]) * (level + 1)




    def _handle_facility_common_submenu_choice(self, choice: str) -> bool:
        if choice == "50":
            self._show_facility_overview_menu()
            return True
        if choice == "51":
            self._show_meat_toilet_menu()
            return True
        if choice == "99":
            self._show_video_shelf_menu()
            return True
        return False






    def _handle_facility_exhibit_choice(self, choice: str) -> bool:
        if choice == "100":
            return True
        if choice == "99":
            self._show_video_shelf_menu()
            return False
        if choice == "50":
            for line in self._build_facility_exhibit_overview_lines():
                print(line)
            self._pause()
            return False
        if choice == "51":
            self._show_meat_toilet_menu()
            return False
        try:
            menu_id = int(choice)
        except ValueError:
            self._show_invalid_selection()
            return False
        if self._get_facility_exhibit_entry(menu_id) is None:
            self._show_invalid_selection()
            return False
        for line in self._build_facility_exhibit_detail_lines(menu_id):
            print(line)
        self._pause()
        return False






    def _handle_facility_menu_choice(self, facilities: List[Dict[str, Any]], choice: str) -> bool:
        return self._show_facility_submenu(facilities, choice)






    def _handle_facility_numeric_submenu_choice(self, facilities: List[Dict[str, Any]], choice: str) -> bool:
        try:
            menu_id = int(choice)
        except ValueError:
            return False

        return self._show_facility_exhibit_detail_menu(menu_id)






    def _infrastructure_main(self) -> List[str]:
        """Infrastructure management – show museum/facility status.
        Mirrors @INFRASTRUCTURE in INFRASTRUCTURE.ERB.
        """
        lines: List[str] = []
        flag = self.interpreter.vars.flag

        lines.append("【设施一览】")

        # Meat toilet count (FLAG:83)
        meat_toilet = flag.get(83, 0)
        if meat_toilet > 0:
            lines.append(f"肉便器数量：{meat_toilet}")

        # Total furnishings (FLAG:84)
        total_furn = flag.get(84, 0)
        lines.append(f"调度品合计：{total_furn}")

        # Museum items
        lines.append("")
        lines.append("── 博物馆 ──")
        has_any = False
        for flag_id in sorted(self._INFRA_NAMES.keys()):
            count = flag.get(flag_id, 0)
            if count > 0:
                has_any = True
                name = self._INFRA_NAMES[flag_id]
                lines.append(f"  {name}：{count}个")
        if not has_any:
            lines.append("  博物馆内还没有任何展品。")

        # Video crystal (FLAG:99)
        video = flag.get(99, 0)
        if video > 0:
            lines.append(f"影像水晶球：{video}个")

        return lines

    # ------------------------------------------------------------------
    # MONSTER_DATA (怪物数据)
    # ------------------------------------------------------------------

    _MONSTER_RACE_NAMES: Dict[int, str] = {
        0: "无", 1: "亚人", 2: "史莱姆", 3: "昆虫", 4: "植物",
        5: "触手", 6: "妖精", 7: "巨人", 8: "男魔族", 9: "女魔族",
        10: "兽", 11: "脑奸", 12: "马",
    }

    _MONSTER_SPECIAL_NAMES: Dict[int, str] = {
        0: "无", 1: "粘液捕获", 2: "落穴捕获", 3: "藤蔓捕获",
        4: "铠破坏", 5: "透明", 6: "再生", 7: "拟态",
        8: "迷惑", 9: "吐息", 10: "麻痹", 11: "诱惑",
        12: "混乱", 13: "经验值吸取", 14: "破铠吐息",
        15: "魔力吸取", 16: "射击", 17: "地形能力",
    }



    def _prompt_facility_choice(self):
        return self._prompt_choice()






    def _render_facility_exhibit_menu(self):
        print("\n【设施展览】")
        print("-" * 30)
        print(" [50] 查看全部展品")
        print(" [51] 查看肉便器")
        for entry in self._get_facility_exhibit_definitions():
            count = self.interpreter.vars.get_flag(int(entry["flag_id"]), 0)
            print(f" [{entry['menu_id']}] {entry['name']} ({count})")
        print(" [99] 查看已拍的影像水晶球")
        print(" [100] Back")






    def _render_facility_menu(self):
        print("\n【设施·设备】")
        print("-" * 30)
        print(" [50] 查看全部展品")
        print(" [51] 看看肉便器的样子")
        for entry in self._get_facility_exhibit_definitions():
            print(f" [{entry['menu_id']}] 看看{entry['name']}的状态")
        print(" [99] 看看已拍的影像水晶球")
        print("-" * 30)
        print(" [100] Back")






    def _show_facility_exhibit_detail_menu(self, menu_id: int) -> bool:
        exhibit_entry = self._get_facility_exhibit_entry(menu_id)
        if exhibit_entry is None:
            print("\nInvalid selection.")
            self._pause()
            return False
        for line in self._build_facility_exhibit_detail_lines(menu_id):
            print(line)
        self._pause()
        return True




    def _show_facility_exhibit_menu(self):
        while True:
            if self._advance_facility_exhibit_menu():
                return




    def _show_facility_overview_menu(self):
        for line in self._build_facility_exhibit_overview_lines():
            print(line)
        self._pause()




    def _show_facility_submenu(self, facilities: List[Dict[str, Any]], choice: str) -> bool:
        if self._handle_facility_common_submenu_choice(choice):
            return True
        return self._handle_facility_numeric_submenu_choice(facilities, choice)




    def _show_facility_upgrade_menu(self, facilities: List[Dict[str, Any]], menu_id: int) -> bool:
        facility = next((entry for entry in facilities if entry["menu_id"] == menu_id - 200), None)
        if facility is None:
            print("\nInvalid selection.")
            self._pause()
            return False
        ok, message = self._upgrade_facility(facility)
        print(f"\n{message}")
        self._pause()
        return True




    def _show_infrastructure(self, facility_type: int) -> List[str]:
        """设施展示 - 对应 @INFRASTRUCTURE
        展示博物馆中各种设施的状态
        """
        v = self.interpreter.vars

        if facility_type == 50:
            # 全部展品一览
            return self._show_all_exhibits()

        if facility_type == 51:
            # 肉便器
            return self._show_benki()

        if facility_type == 99:
            # 影像水晶球
            return self._show_video_crystal()

        if facility_type not in self._INFRASTRUCTURE_TYPES:
            return ["无效的设施类型"]

        name, flag_key, description = self._INFRASTRUCTURE_TYPES[facility_type]
        # 解析 FLAG 编号
        flag_num = int(flag_key.split(':')[1])
        count = v.flag.get(flag_num, 0)

        if count == 0:
            return [f"还没制作过{name}。"]

        messages = [f"博物馆内现在有 {count}个{name}。"]
        messages.append(description)
        return messages






    def _upgrade_facility(self, facility: Dict[str, Any]) -> tuple[bool, str]:
        cost = self._get_facility_upgrade_cost(facility)
        if self.interpreter.vars.money < cost:
            return False, "金钱不足。"
        global_id = int(facility["global_id"])
        self._spend_global_money(cost)
        self.interpreter.vars.globals[global_id] = self._get_global_level(global_id) + 1
        return True, f"{facility['name']} 升级到了 Lv{self._get_global_level(global_id)}。"






    def show_facility(self):
        """Infrastructure showcase menu aligned to INFRASTRUCTURE.ERB visible entries."""
        ok, message = self._can_open_infrastructure()
        if not ok:
            print(f"\n{message}")
            self._pause()
            return

        facilities = self._get_facility_definitions()
        while True:
            if self._advance_facility_menu(facilities):
                return





