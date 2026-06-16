from __future__ import annotations
"""Module for TaxExtMixin - 税收系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class TaxExtMixin:
    """Mixin providing 税收系统 methods for GameEngine"""

    def _append_tax_section(self, messages: List[str], title: str, section_messages: List[str], income: int) -> None:
        messages.extend(["", title])
        messages.extend(section_messages)
        messages.append(f"合计 {income}")






    def _apply_tax_collection(self) -> List[str]:
        today = int(self.interpreter.vars.day[2])
        if today not in (10, 20, 30):
            return []

        support_income, prestige_text = self._get_tax_support_income()
        messages = self._build_tax_collection_headlines(support_income, prestige_text)

        land_income, land_messages = self._get_tax_land_income()
        self._append_tax_section(messages, "*土地税*", land_messages, land_income)

        brothel_income, brothel_messages = self._get_tax_brothel_income()
        self._append_tax_section(messages, "*肉便器税*", brothel_messages, brothel_income)

        subtotal = support_income + land_income + brothel_income
        special_tax = self._apply_tax_special_tax(subtotal)
        messages.extend(["", "*魔王特別税*", f"合計 {special_tax}"])

        total_tax = subtotal + special_tax
        black_diamond = int(self.interpreter.vars.globals.get(2811, 0))
        if 51 <= black_diamond < 100:
            bonus_level = black_diamond // 10
            messages.append(f"黑方片的商业运营有方，收入乘以1.{bonus_level}")
            total_tax = total_tax * (10 + bonus_level) // 10

        messages.extend(["", f"合计税收 {total_tax}"])
        self._add_global_money(total_tax)
        return messages






    def _apply_tax_special_tax(self, subtotal: int) -> int:
        special_tax = subtotal * (int(self.interpreter.vars.get_flag(9, 0)) + 100) // 100 - subtotal
        self.interpreter.vars.set_flag(9, 0)
        return special_tax






    def _apply_turn_end_blind_faith_talent_check(self, target: Character) -> List[str]:
        if int(target.talent.get(86, 0)) != 0:
            return []
        if int(target.mark.get(3, 0)) != 0:
            return []
        medal_exp = int(target.exp.get(81, 0))
        obedience = int(target.abl.get(10, 0))
        if int(target.talent.get(85, 0)) != 0 and medal_exp >= 5 and obedience >= 4:
            target.talent[86] = 1
            return [
                "爱会使人盲目的吗？我们也许不得而知。",
                f"但{target.name}对你，却一定是盲目的……",
                f"{target.name} 获得了【{self._get_talent_name(86)}】。",
            ]
        if int(target.talent.get(76, 0)) != 0 and medal_exp >= 10 and obedience >= 5:
            target.talent[86] = 1
            return [
                "放荡的人，很难谈得上有什么纪律意识。",
                f"但通过出色的调教，淫乱的{target.name}已经对你言听计从了……",
                f"{target.name} 获得了【{self._get_talent_name(86)}】。",
            ]
        return []




    def _build_tax_collection_headlines(self, support_income: int, prestige_text: Optional[str]) -> List[str]:
        messages = ["", "- - - 收税 - - -", ""]
        if prestige_text:
            messages.append(prestige_text)
        messages.append(f"来自魔界的支援 {support_income}")
        return messages






    def _faith(self, target, amount: int) -> List[str]:
        """信仰値増減 - 对应 @FAITH"""
        messages: List[str] = []
        current = target.cflag.get(152, 0)
        target.cflag[152] = current + amount
        return messages




    def _get_tax_brothel_income(self) -> tuple[int, List[str]]:
        total = 0
        messages: List[str] = []
        exhibit_tax = int(self.interpreter.vars.get_flag(84, 0)) * 10
        if exhibit_tax > 0:
            total += exhibit_tax
            messages.append(f"├ 展品观赏税 {exhibit_tax}")
        toilet_tax = int(self.interpreter.vars.get_flag(83, 0)) * 10
        if toilet_tax > 0:
            total += toilet_tax
            messages.append(f"├ 肉便器使用税 {toilet_tax}")

        prostitution_tax = (
            self._get_item_count(143) * 2
            + self._get_item_count(152) * 2
            + self._get_item_count(182) * 2
            + 20
        )
        total += prostitution_tax
        messages.append(f"└ 淫魔卖春税 {prostitution_tax}")

        for local in range(1, 11):
            if int(self.interpreter.vars.get_flag(local + 349, 0)) == 507:
                total = total * 11 // 10
        return total, messages






    def _get_tax_land_income(self) -> tuple[int, List[str]]:
        total = 0
        messages: List[str] = []
        area_rules = [
            (81, 82, "地上的魔界领土", "人间界殖民地", 1),
            (86, 87, "黑暗精灵的领土", "精灵族领域殖民地", 2),
            (88, 89, "混沌龙之山", "龙之山脉殖民地", 2),
            (90, 91, "堕天使的淫界", "天界的殖民地", 2),
        ]
        for progress_flag, conquer_flag, conquered_name, colony_name, conquered_threshold in area_rules:
            conquer_state = int(self.interpreter.vars.get_flag(conquer_flag, 0))
            progress = int(self.interpreter.vars.get_flag(progress_flag, 0))
            if conquer_state >= conquered_threshold:
                total += 1200
                messages.append(f"├ {conquered_name} 1200")
            elif progress > 10:
                income = progress // 10
                total += income
                messages.append(f"├ {colony_name} {income}")
        if int(self.interpreter.vars.get_flag(92, 0)) == 15:
            total += 1500
            messages.append("├ 圣灵骑士的卖春堡垒 1500")
        dungeon_income = self._get_tax_dungeon_income()
        total += dungeon_income
        messages.append(f"└ 地下城 {dungeon_income}")
        return total, messages






    def _get_tax_support_income(self) -> tuple[int, Optional[str]]:
        prestige = self._get_prestige_value()
        years_elapsed = max(1, int(self.interpreter.vars.day[0]))
        if 0 <= prestige <= 20:
            return 0, "威望值是【岌岌可危】"
        if 20 < prestige <= 40:
            value = years_elapsed * 30 * prestige // 100
            return min(5000, value), "威望值是【动荡不安】"
        if 40 < prestige <= 60:
            value = years_elapsed * 50 * prestige // 100
            return min(10000, value), "威望值是【略受质疑】"
        if 60 < prestige <= 80:
            value = years_elapsed * 50 * prestige // 100
            return min(30000, value), "威望值是【相安无事】"
        value = years_elapsed * 100 * prestige // 100
        return min(50000, value), "威望值是【广受爱戴】"






    def _karma(self, target, amount: int) -> List[str]:
        """善恶値増減 - 对应 @KARMA"""
        messages: List[str] = []
        current = target.cflag.get(9, 0)
        target.cflag[9] = current + amount
        return messages




    def _tax_get(self) -> List[str]:
        """税収 - 对应 @TAX_GET"""
        messages: List[str] = []
        return messages


