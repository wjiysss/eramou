from __future__ import annotations
"""Module for VideoExtMixin - 视频系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class VideoExtMixin:
    """Mixin providing 视频系统 methods for GameEngine"""

    def _advance_video_campaign_choice(self, choice: str, stock: int, sent: int, active: int, days_left: int) -> bool:
        if choice in {"1", "2"} and stock <= 0:
            return True
        if choice == "1":
            self._apply_video_campaign_direct_delivery(stock, sent, active, days_left)
            return True
        if choice == "2":
            self._apply_video_campaign_merchant_delivery(stock, sent, active, days_left)
            return True
        if choice == "3":
            self._apply_video_campaign_enhance_popularity(active, days_left)
            return True
        if choice == "4":
            self._apply_video_campaign_extend_popularity(active, days_left)
            return True
        return False






    def _append_video_to_shelf(self, title: str) -> None:
        next_id = 0
        if self.interpreter.vars.suisei_str:
            next_id = max(int(key) for key in self.interpreter.vars.suisei_str.keys()) + 1
        self.interpreter.vars.suisei_str[next_id] = title






    def _apply_video_campaign_direct_delivery(self, stock: int, sent: int, active: int, days_left: int):
        print("\n通过投放拍摄的影像，激起反抗魔王的决心。")
        amount = self._prompt_video_campaign_amount()
        if amount is None:
            return
        if amount > stock:
            print("\n超出数量，请重新输入。")
            self._pause()
            return
        applied, bonus_messages = self._get_video_campaign_bonus_count(amount, merchant_mode=False)
        self._finalize_video_campaign_delivery(sent, amount, applied, bonus_messages, active, days_left)






    def _apply_video_campaign_enhance_popularity(self, active: int, days_left: int):
        if active <= 0 or days_left <= 0:
            return
        print("\n通过奸商代理投放拍摄的影像，增强投放的效果。")
        print("将收取 50000G 或 5 枚勋章。")
        pay_choice = self._prompt_video_campaign_payment_choice(include_exit=True)
        if pay_choice == "999":
            return
        if pay_choice == "1":
            if self.interpreter.vars.money <= 50000:
                print("\n金钱不足。")
                self._pause()
                return
            self._spend_global_money(50000)
        elif pay_choice == "2":
            if not self._consume_labo_medals(5):
                print("\n勋章不足。")
                self._pause()
                return
        else:
            return
        updated_active = self._calculate_video_campaign_boost(active, active * 2)
        self._set_video_campaign_active(updated_active, days_left)
        print("\n因为剪辑出了更多的版本，投放效果增强了。")
        self._pause()






    def _apply_video_campaign_extend_popularity(self, active: int, days_left: int):
        if active <= 0 or days_left <= 0:
            return
        print("\n通过增加投放量延长流行时间。")
        print("将收取 50000G。")
        print(" [1] 支付")
        print(" [999] 算了")
        pay_choice = self._prompt_choice()
        if pay_choice == "999":
            return
        if pay_choice != "1" or self.interpreter.vars.money <= 50000:
            print("\n金钱不足。")
            self._pause()
            return
        self._spend_global_money(50000)
        updated_days = self._calculate_video_campaign_boost(days_left, days_left + 5)
        if updated_days - days_left < 1:
            updated_days = days_left + 1
        self._set_video_campaign_active(active, updated_days)
        print("\n流行时间延长了。")
        self._pause()






    def _apply_video_campaign_merchant_delivery(self, stock: int, sent: int, active: int, days_left: int):
        print("\n通过奸商代理投放拍摄的影像，或许更能激起反抗魔王的决心。")
        print("每部需要支付 5000G 或 1 枚勋章。")
        amount = self._prompt_video_campaign_amount()
        if amount is None:
            return
        if not self._validate_video_campaign_merchant_amount(amount, stock):
            return
        pay_choice = self._prompt_video_campaign_payment_choice()
        if not self._apply_video_campaign_merchant_payment(amount, pay_choice):
            return
        applied, bonus_messages = self._get_video_campaign_bonus_count(amount, merchant_mode=True)
        self._finalize_video_campaign_delivery(sent, amount, applied, bonus_messages, active, days_left)






    def _apply_video_campaign_merchant_payment(self, amount: int, pay_choice: str) -> bool:
        if pay_choice == "1":
            cost = amount * 5000
            if self.interpreter.vars.money < cost:
                print("\n金钱不足。")
                self._pause()
                return False
            self._spend_global_money(cost)
            return True
        if pay_choice == "2":
            if not self._consume_labo_medals(amount):
                print("\n勋章不足。")
                self._pause()
                return False
            return True
        return False






    def _build_video_shelf_page_lines(self, page_index: int, row_count: int = 7) -> List[str]:
        return self._get_video_shelf_page_lines_from_slots(page_index, row_count=row_count)






    def _calculate_video_campaign_boost(self, current_value: int, limit_value: int) -> int:
        updated_value = current_value * 120 // 100
        if random.randint(0, 4) == 0:
            updated_value = updated_value * 160 // 100
        if random.randint(0, 1) == 0:
            updated_value = updated_value * 120 // 100
        return min(updated_value, limit_value)






    def _check_video_shelf(self) -> int:
        return self._get_video_shelf_content_count()






    def _decay_video_campaign(self):
        days_left = self._get_video_campaign_days_left() - 1
        active = self._get_video_campaign_active_count()
        if random.randint(0, 2) != 0:
            active -= 1
        if days_left <= 0 or active <= 0:
            self._set_video_campaign_active(0, 0)
            return
        self._set_video_campaign_active(active, days_left)






    def _finalize_video_campaign_delivery(self, sent: int, amount: int, applied: int, bonus_messages: List[str], active: int, days_left: int):
        self.interpreter.vars.globals[9011] = sent + amount
        self._set_video_campaign_active(active + applied, days_left + applied)
        message = f"成功投放 {amount} 部水晶球。"
        if bonus_messages:
            message += " " + " ".join(bonus_messages)
        print(f"\n{message}")
        self._pause()






    def _get_video_campaign_active_count(self) -> int:
        return int(self.interpreter.vars.globals.get(9012, 0))






    def _get_video_campaign_bonus_count(self, amount: int, merchant_mode: bool = False) -> tuple[int, List[str]]:
        current = max(0, int(amount))
        base = current
        messages: List[str] = []
        if merchant_mode:
            current = current * 110 // 100
            if random.randint(0, 1) == 0:
                current = current * 120 // 100
            if random.randint(0, 2) == 0:
                current = current * 120 // 100
            if random.randint(0, 3) == 0:
                current = current * 120 // 100
        if random.randint(0, 1) == 0:
            current = current * 120 // 100
        if random.randint(0, 2) == 0:
            current = current * 80 // 100
        if merchant_mode and current > base:
            messages.append("奸商们制作更多的版本提升了投放效果。")
        elif not merchant_mode and current > base:
            messages.append("在投放过程中似乎传出了不同的版本，投放效果提升了。")
        elif current < base:
            messages.append("似乎有些水晶球投放不是太成功。")
        if merchant_mode and current <= base:
            current = base
        return max(0, current), messages






    def _get_video_campaign_days_left(self) -> int:
        return int(self.interpreter.vars.globals.get(9013, 0))






    def _get_video_campaign_sent(self) -> int:
        return int(self.interpreter.vars.globals.get(9011, 0))






    def _get_video_campaign_stock(self) -> int:
        return max(0, self._get_video_campaign_total() - self._get_video_campaign_sent())






    def _get_video_campaign_total(self) -> int:
        return int(self.interpreter.vars.globals.get(9010, 0))






    def _get_video_shelf_content_count(self) -> int:
        return len([title for title in self.interpreter.vars.suisei_str.values() if str(title).strip()])






    def _get_video_shelf_count(self) -> int:
        return len(self._get_video_shelf_slots())






    def _get_video_shelf_max_page(self, row_count: int = 7) -> int:
        slots = self._get_video_shelf_slots()
        if not slots:
            return 0
        max_slot_id = max(slot_id for slot_id, _ in slots)
        return max(0, max_slot_id // max(1, row_count * 3))






    def _get_video_shelf_page_lines_from_slots(self, page_index: int, row_count: int = 7) -> List[str]:
        slots = self._get_video_shelf_slots()
        total = len(slots)
        if total <= 0:
            return ["还没拍摄过任何影像。"]

        slot_start, slot_end = self._get_video_shelf_page_range(page_index, row_count=row_count)
        lines = [f"总共拍摄了{total}部水晶球。", "-" * 30]
        current_row: List[str] = []
        shown = 0
        for slot_id, title in slots:
            if slot_id < slot_start or slot_id >= slot_end:
                continue
            current_row.append(f"《{title}》")
            shown += 1
            if shown % 3 == 0:
                lines.append("  ".join(current_row))
                current_row = []
        if current_row:
            lines.append("  ".join(current_row))

        while len(lines) < row_count + 2:
            lines.append("")

        max_page = self._get_video_shelf_max_page(row_count=row_count)
        lines.append("-" * 30)
        lines.append(f"[1000] 上一页   [999] 离开   [1001] 下一页   <{page_index + 1}/{max_page + 1}>")
        return lines






    def _get_video_shelf_page_range(self, page_index: int, row_count: int = 7) -> tuple[int, int]:
        max_page = self._get_video_shelf_max_page(row_count=row_count)
        page_index = max(0, min(page_index, max_page))
        slot_start = page_index * row_count * 3
        slot_end = slot_start + self._get_video_shelf_page_span(row_count=row_count)
        return slot_start, slot_end






    def _get_video_shelf_page_span(self, row_count: int = 7) -> int:
        return row_count * 3 + 1






    def _get_video_shelf_slots(self) -> List[tuple[int, str]]:
        slots: List[tuple[int, str]] = []
        for raw_key, raw_title in sorted(self.interpreter.vars.suisei_str.items(), key=lambda item: int(item[0])):
            cleaned = str(raw_title).strip()
            if cleaned:
                slots.append((int(raw_key), cleaned))
        return slots






    def _get_video_shelf_title_count(self) -> int:
        return len([title for title in self.interpreter.vars.suisei_str.values() if str(title).strip()])






    def _handle_video_campaign_choice(self, choice: str, stock: int, sent: int, active: int, days_left: int) -> bool:
        return self._advance_video_campaign_choice(choice, stock, sent, active, days_left)






    def _ntr_video(self, target) -> List[str]:
        """NTR動画 - 对应 @NTR_VIDEO"""
        messages: List[str] = []
        return messages



    def _prompt_video_campaign_amount(self) -> Optional[int]:
        raw_amount = self._prompt_choice("请输入要投放的数量 >> ")
        try:
            amount = int(raw_amount)
        except ValueError:
            return None
        if amount <= 0:
            return None
        return amount






    def _prompt_video_campaign_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_video_campaign_payment_choice(self, include_exit: bool = False) -> str:
        print(" [1] 支付金币")
        print(" [2] 支付勋章")
        if include_exit:
            print(" [999] 离开")
        return self._prompt_choice()






    def _render_video_campaign_menu(self, stock: int, sent: int, active: int, days_left: int) -> None:
        print("\n【向城里投放水晶球】")
        print("-" * 30)
        print(f" 可用于投放的水晶球 {stock} 部    已投放 {sent} 部")
        if active > 0 and days_left > 0:
            print(f" 正流行的有 {active} 部    {days_left} 天后将过时")
        else:
            print(" 目前没有投放中的水晶球")
        print("-" * 30)
        if stock > 0:
            print(" [1] 投放水晶球")
            print(" [2] 派奸商投放水晶球")
        else:
            print(" 当前没有可以用于投放的水晶球")
        if active > 0 and days_left > 0:
            print(" [3] 增强流行效果")
            print(" [4] 延长流行时间")
        print(" [999] 离开")






    def _sengen_video_de(self) -> List[str]:
        """水晶球投放结算 - 对应 @SENGEN_VIDEO_DE"""
        messages: List[str] = []
        return messages






    def _set_video_campaign_active(self, count: int, days_left: int):
        self.interpreter.vars.globals[9012] = max(0, int(count))
        self.interpreter.vars.globals[9013] = max(0, int(days_left))






    def _show_video_campaign_menu(self):
        while True:
            stock = self._get_video_campaign_stock()
            sent = self._get_video_campaign_sent()
            active = self._get_video_campaign_active_count()
            days_left = self._get_video_campaign_days_left()
            self._render_video_campaign_menu(stock, sent, active, days_left)
            choice = self._prompt_video_campaign_choice()
            if choice == "999":
                return
            if self._advance_video_campaign_choice(choice, stock, sent, active, days_left):
                continue






    def _show_video_crystal(self) -> List[str]:
        """影像水晶球展示"""
        v = self.interpreter.vars
        count = v.flag.get(620, 0)
        if count == 0:
            return ["还没有拍摄过影像。"]
        return [f"现在有 {count} 个影像水晶球。"]

    # ========================================
    # EVENT_ADDICT - 媚药中毒系统
    # 对应 ERB/EVENT_ADDICT.ERB
    # ========================================






    def _show_video_shelf_menu(self):
        if self._get_video_shelf_content_count() <= 0:
            print("\n还没拍摄过任何影像。")
            self._pause()
            return

        page_index = 0
        while True:
            print("\n【影像水晶球书架】")
            for line in self._build_video_shelf_page_lines(page_index):
                print(line)
            choice = self._prompt_choice()
            if choice == "999":
                return
            if choice == "1000":
                page_index = max(0, page_index - 1)
                continue
            if choice == "1001":
                max_page = self._get_video_shelf_max_page(row_count=7)
                page_index = min(max_page, page_index + 1)
                continue
            print("\n无效值")
            self._pause()






    def _validate_video_campaign_merchant_amount(self, amount: int, stock: int) -> bool:
        if amount > stock:
            print("\n超出可投放数量，请重新输入。")
            self._pause()
            return False
        medals = self._get_labo_medal_count()
        if amount > medals and amount * 5000 > self.interpreter.vars.money:
            print("\n没有足够的奖赏来打动奸商。")
            self._pause()
            return False
        return True





