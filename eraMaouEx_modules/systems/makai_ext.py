from __future__ import annotations
"""Module for MakaiExtMixin - 魔界系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class MakaiExtMixin:
    """Mixin providing 魔界系统 methods for GameEngine"""

    def _advance_makai_bank_menu(self) -> bool:
        self._render_makai_bank_menu()
        choice = self._prompt_makai_bank_choice()
        return self._handle_makai_bank_choice(choice)






    def _apply_makai_bank_borrow(self):
        current_debt = self._get_makai_bank_debt()
        current_limit = self._get_makai_bank_credit_limit()
        print(f"\n请输入贷款金额,返回上层请输入0。(目前欠款为{current_debt}贷款额度为{current_limit})")
        print("贷款利息为百分之二十，本息超过额度将无法借贷或追加借贷。")
        amount = self._read_makai_bank_amount("Amount >> ")
        if amount is None:
            print("\n输入无效。")
            self._pause()
            return
        if amount == 0:
            return
        if amount <= 0 or amount > (current_limit - current_debt):
            print("\n您的额度不足，请重新输入。")
            self._pause()
            return
        self._borrow_makai_bank_cash(amount)
        print(f"\n已贷款{amount}资金。")
        self._pause()






    def _apply_makai_bank_deposit(self):
        current_deposit = self._get_makai_bank_deposit()
        current_money = self.interpreter.vars.money
        print(f"\n请输入需要存入的资金数量,返回上层请输入0。(目前的存款为{current_deposit}现金为{current_money})")
        amount = self._read_makai_bank_amount("Amount >> ")
        if amount is None:
            print("\n输入无效。")
            self._pause()
            return
        if amount == 0:
            return
        if amount <= 0 or current_money < amount:
            print("\n您的操作有误，请重新输入。")
            self._pause()
            return
        self._deposit_makai_bank_cash(amount)
        print(f"\n已转移{amount}资金至银行。")
        self._pause()






    def _apply_makai_bank_repay(self):
        current_debt = self._get_makai_bank_debt()
        current_money = self.interpreter.vars.money
        print(f"\n请输入还款金额,返回上层请输入0。(目前欠款为{current_debt})")
        amount = self._read_makai_bank_amount("Amount >> ")
        if amount is None:
            print("\n输入无效。")
            self._pause()
            return
        if amount == 0:
            return
        if amount <= 0 or current_money - amount < 0:
            print("\n您没有足够的资金，请重新输入。")
            self._pause()
            return
        if amount > current_debt:
            self._repay_makai_bank_cash(amount)
            print("\n您的输入金额超出欠款额，多余金额将自动转入银行。")
            self._pause()
            return
        self._repay_makai_bank_cash(amount)
        print(f"\n已偿还{amount}资金。")
        self._pause()






    def _apply_makai_bank_withdraw(self):
        current_deposit = self._get_makai_bank_deposit()
        current_money = self.interpreter.vars.money
        print(f"\n请输入需要取出的资金数量,返回上层请输入0。(目前的存款为{current_deposit}现金为{current_money})")
        amount = self._read_makai_bank_amount("Amount >> ")
        if amount is None:
            print("\n输入无效。")
            self._pause()
            return
        if amount == 0:
            return
        if amount <= 0 or current_deposit < amount:
            print("\n您的操作有误，请重新输入。")
            self._pause()
            return
        self._withdraw_makai_bank_cash(amount)
        print(f"\n已提取{amount}资金。")
        self._pause()






    def _borrow_makai_bank_cash(self, amount: int):
        self._set_makai_bank_debt(self._get_makai_bank_debt() + amount * 12 // 10)
        self._add_global_money(amount)






    def _deposit_makai_bank_cash(self, amount: int):
        self._set_makai_bank_deposit(self._get_makai_bank_deposit() + amount)
        self._spend_global_money(amount)






    def _get_makai_bank_credit_limit(self) -> int:
        player = self._get_player()
        level = int(player.cflag.get(9, 0)) if player is not None else 1
        if level < 10:
            return 100000 + level * 10000
        if level < 51:
            return 200000 + (level - 10) * 100000
        if level < 101:
            return 4200000 + (level - 50) * 1000000
        return 54200000 + (level - 100) * 10000000






    def _get_makai_bank_debt(self) -> int:
        return int(self.interpreter.vars.get_flag(9003, 0))






    def _get_makai_bank_deposit(self) -> int:
        return int(self.interpreter.vars.get_flag(9001, 0))






    def _handle_makai_bank_choice(self, choice: str) -> bool:
        if choice == "9":
            return True
        if choice == "1":
            self._apply_makai_bank_deposit()
            return False
        if choice == "2":
            self._apply_makai_bank_withdraw()
            return False
        if choice == "3":
            self._apply_makai_bank_borrow()
            return False
        if choice == "4":
            self._apply_makai_bank_repay()
            return False
        print("\nInvalid selection.")
        self._pause()
        return False






    def _is_makai_bank_enabled(self) -> bool:
        return self._get_flag_bit(9000, 0)






    def _makai_bank_deposit(self, amount: int) -> List[str]:
        """存款"""
        g = self.interpreter.vars.globals
        if amount > 0 and self.interpreter.vars.money >= amount:
            savings = int(g.get(9001, 0))
            g[9001] = savings + amount
            self.interpreter.vars.money -= amount
            g[4444] = int(g.get(4444, 0)) - amount
            return [f"已转移{amount}资金至银行。"]
        return ["您的操作有误，请重新输入。"]






    def _makai_bank_loan(self, amount: int) -> List[str]:
        """贷款"""
        g = self.interpreter.vars.globals
        loan_limit = self._calc_loan_limit()
        debt = int(g.get(9003, 0))
        if amount > 0 and amount <= (loan_limit - debt):
            g[9003] = debt + amount * 12 // 10  # 20%利息
            self.interpreter.vars.money += amount
            g[4444] = int(g.get(4444, 0)) + amount
            # 记录首次贷款日
            if debt == 0:
                g[9006] = self._get_total_day_count()
            return [f"已贷款{amount}资金。"]
        return ["您的额度不足，请重新输入。"]






    def _makai_bank_repay(self, amount: int) -> List[str]:
        """还款"""
        g = self.interpreter.vars.globals
        debt = int(g.get(9003, 0))
        if amount <= 0:
            return ["正在返回上层"]
        if self.interpreter.vars.money - amount < 0:
            return ["您没有足够的资金，请重新输入。"]
        if amount > debt:
            excess = amount - debt
            savings = int(g.get(9001, 0))
            g[9001] = savings + excess
            self.interpreter.vars.money -= amount
            g[4444] = int(g.get(4444, 0)) - amount
            g[9003] = 0
            return ["您输入的金额超出欠款额，多余金额将自动转入银行。"]
        # 正常还款
        g[9003] = debt - amount
        self.interpreter.vars.money -= amount
        g[4444] = int(g.get(4444, 0)) - amount
        return [f"已偿还{amount}资金。"]






    def _makai_bank_withdraw(self, amount: int) -> List[str]:
        """取款"""
        g = self.interpreter.vars.globals
        savings = int(g.get(9001, 0))
        if amount > 0 and savings >= amount:
            g[9001] = savings - amount
            self.interpreter.vars.money += amount
            g[4444] = int(g.get(4444, 0)) + amount
            return [f"已提取{amount}资金。"]
        return ["您的操作有误，请重新输入。"]






    def _prompt_makai_bank_choice(self) -> str:
        return self._prompt_choice()






    def _read_makai_bank_amount(self, prompt: str) -> Optional[int]:
        amount_raw = self._read_input_stripped(prompt)
        try:
            return int(amount_raw)
        except ValueError:
            return None






    def _render_makai_bank_menu(self) -> None:
        print("\n【魔界银行】")
        print("-" * 30)
        print(f" 欢迎进入魔界银行远程客户端，您目前的存款为{self._get_makai_bank_deposit()}，现金为{self.interpreter.vars.money}。")
        print(f" 当前欠款: {self._get_makai_bank_debt()} / 额度: {self._get_makai_bank_credit_limit()}")
        print(" [1] 存款")
        print(" [2] 取款")
        print(" [3] 贷款")
        print(" [4] 还款")
        print(" [9] 返回")






    def _repay_makai_bank_cash(self, amount: int):
        debt = self._get_makai_bank_debt()
        if amount > debt:
            self._set_makai_bank_deposit(self._get_makai_bank_deposit() + amount - debt)
            self._set_makai_bank_debt(0)
        else:
            self._set_makai_bank_debt(debt - amount)
        self._spend_global_money(amount)






    def _set_makai_bank_debt(self, amount: int):
        self.interpreter.vars.set_flag(9003, max(0, int(amount)))






    def _set_makai_bank_deposit(self, amount: int):
        self.interpreter.vars.set_flag(9001, max(0, int(amount)))






    def _show_makai_bank(self) -> List[str]:
        """显示魔界银行界面"""
        self._calc_interest()
        g = self.interpreter.vars.globals
        savings = int(g.get(9001, 0))
        lines = [
            f"欢迎进入魔界银行远程客户端，您目前的存款为{savings}，现金为{self.interpreter.vars.money}。",
            "[1] 存款",
            "[2] 取款",
            "[3] 贷款",
            "[4] 还款",
            "[9] 返回",
        ]
        return lines

    # =========================================================================
    # System 3: PTJ (打工系统)
    # Based on ERB/MOD/PartTimeJob/PTJ.ERB
    # =========================================================================

    _PTJ_NAMES = {
        400: "风俗",
        401: "斗姬",
        402: "演艺",
        403: "女仆",
        404: "教师",
        405: "驯兽师",
        406: "狱卒",
        407: "图书管理员",
        408: "宗教",
        409: "研究",
    }






    def _show_makai_bank_menu(self):
        while True:
            if self._advance_makai_bank_menu():
                return






    def _withdraw_makai_bank_cash(self, amount: int):
        self._set_makai_bank_deposit(self._get_makai_bank_deposit() - amount)
        self._add_global_money(amount)





