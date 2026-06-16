from __future__ import annotations
"""Module for ShopExtMixin - Shop extension methods (ability up, shop display, sell, train checks)"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ShopExtMixin:
    """Mixin providing Shop extension methods (ability up, shop display, sell, train checks)"""
    def _estimate_sell_price(self, target: Character) -> Dict[str, Any]:
        return self._build_sell_price_detail(target)


    def _show_shop_group_menu(self, title: str, groups: List[Dict[str, Union[str, List[int]]]], switch_label: Optional[str] = None, switch_code: Optional[str] = None) -> Optional[str]:
        while True:
            result = self._advance_shop_group_menu(title, groups, switch_label=switch_label, switch_code=switch_code)
            if result is None:
                return None
            if result == "RETRY":
                continue
            if result == "SWITCH":
                return switch_code
            return None


    def _show_shop_main_menu(self):
        self._render_shop_main_menu()


    def _ability_up(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars
        chars = v.chars

        messages.append("=" * 40)
        messages.append("能力值升级")
        messages.append("=" * 40)
        messages.append("[998] 奴隶一览")
        messages.append("[997] 勇者一览")
        messages.append("")
        messages.append("要提高谁的能力值？")
        messages.append("-" * 40)

        master = chars[0] if chars else None
        if master is not None:
            master_name = getattr(master, 'savestr', master.name or "")
            master_lv = master.cflag.get(9, 0)
            messages.append(f"[ 0] {master_name:<12} LV{master_lv:>4}")

        for idx, char in enumerate(chars[1:], 1):
            if char.cflag.get(1, 0) != 0:
                continue
            char_name = getattr(char, 'savestr', char.name or "")
            char_lv = char.cflag.get(9, 0)
            messages.append(f"[{idx:>2}] {char_name:<12} LV{char_lv:>4}")

        messages.append("-" * 40)
        messages.append("[999] 返  回")
        return messages


    def _shop_function(self, func_id: int) -> List[str]:
        if func_id == 0:
            return self._show_list_trainable()
        elif func_id == 1:
            return self._show_list_assistable()
        elif func_id == 2:
            return self._check_trainable()
        elif func_id == 3:
            return self._check_assistable()
        elif func_id == 4:
            return self._show_job_names()
        return []


    def _is_trainable_check(self, char_idx: int) -> int:
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        if char_idx < 1 or char_idx >= len(chars) or char_idx == v.master:
            return 1
        char = chars[char_idx]
        if char.cflag.get(1, 0) != 0:
            return 2
        return 0


    def _is_assistable_check(self, char_idx: int) -> int:
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        if char_idx < 1 or char_idx >= len(chars):
            return 1
        char = chars[char_idx]
        if char.cflag.get(0, 0) != 2:
            return 2
        if char.cflag.get(1, 0) != 0:
            return 3
        if v.target == char_idx:
            return 4
        return 0


    def _bar_str(self, current: int, maximum: int, width: int) -> str:
        if maximum <= 0:
            return "[" + "." * width + "]"
        filled = int(width * min(current, maximum) / maximum)
        filled = max(0, min(filled, width))
        return "[" + "*" * filled + "." * (width - filled) + "]"


    def _estimate_sell_price(self, target: Character) -> int:
        detail = self._build_sell_price_detail(target)
        return detail.get("price", 0)


    def _show_shop(self) -> List[str]:
        """商店主显示

        查找优先级: ERB函数 SHOW_SHOP → Python回退
        """
        # 1. 尝试ERB函数 SHOW_SHOP
        if "SHOW_SHOP" in self.interpreter.functions:
            return self.interpreter.call_erb_function("SHOW_SHOP")

        # 2. Python回退: 生成商店显示
        v = self.interpreter.vars
        day = v.day
        day_repr = f"{day[0]}:{day[1]}:{day[2]}" if isinstance(day, (list, tuple)) and len(day) >= 3 else str(day)
        lines = []
        lines.append("=" * 50)
        lines.append(f"  eraMaouEx  Day:{day_repr}  金钱:{v.money}")
        lines.append("=" * 50)
        lines.append("")
        lines.append("[100] 选择调教对象")
        lines.append("[101] 角色信息")
        lines.append("[102] 地下城")
        lines.append("[107] 商店")
        lines.append("[199] 休息")
        lines.append("[200] 保存")
        lines.append("[300] 读取")
        lines.append("[777] 设置")
        lines.append("")
        return lines

    # ------------------------------------------------------------------
    # EVENT_K 角色口上事件框架
    # ------------------------------------------------------------------

    _EVENT_K_PERSONALITY_MAP: Dict[int, str] = {
        0: "慈愛", 1: "自信家", 2: "気弱", 3: "高貴", 4: "冷徹",
        5: "マオ", 6: "悪女", 7: "ハート", 8: "スペード", 9: "ダイヤ",
        10: "クラブ", 11: "リリィ", 19: "菲娅", 903: "嘉德",
    }


