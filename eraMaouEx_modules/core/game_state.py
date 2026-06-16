"""GameState门面类 - 统一封装游戏状态访问，解耦Mixin与ERB解释器内部结构"""
from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import ERBVariable


class GameState:
    """游戏状态门面类 - 提供语义化的状态访问接口

    封装ERBVariable的内部结构，使Mixin方法无需直接访问interpreter.vars。
    所有属性通过property提供，保持与ERB变量的同步。
    """

    def __init__(self, vars: "ERBVariable"):
        self._vars = vars

    # ---- 原始访问（向后兼容） ----
    @property
    def raw(self) -> "ERBVariable":
        """直接访问原始ERB变量（仅用于过渡期）"""
        return self._vars

    # ---- 助手操作 ----
    @property
    def assiplay(self) -> int:
        """是否助手操作 (TFLAG:50)"""
        return int(self._vars.tflag.get(50, 0))

    # ---- 日期/时间 ----
    @property
    def day(self) -> list:
        """当前日期 [年,月,日,星期] (DAY)"""
        return self._vars.day if hasattr(self._vars, 'day') else [1, 1, 1, 0]

    @property
    def time(self) -> int:
        """当前时间 (TIME: 0=上午, 1=下午)"""
        return int(self._vars.time) if hasattr(self._vars, 'time') else 0

    # ---- 金钱 ----
    @property
    def money(self) -> int:
        """当前金钱 (MONEY)"""
        return int(self._vars.money) if hasattr(self._vars, 'money') else 0

    @money.setter
    def money(self, value: int) -> None:
        self._vars.money = value

    # ---- 调教指令 ----
    @property
    def prevcom(self) -> int:
        """上一个调教指令 (TFLAG:59)"""
        return int(self._vars.tflag.get(59, -1))

    @property
    def nextcom(self) -> int:
        """下一个调教指令 (TFLAG:60)"""
        return int(self._vars.tflag.get(60, -1))

    # ---- 目标/助手索引 ----
    @property
    def target_no(self) -> int:
        """当前调教目标编号 (TARGET)"""
        return int(self._vars.target) if hasattr(self._vars, 'target') else -1

    @property
    def assi_no(self) -> int:
        """当前助手编号 (ASSI)"""
        return int(self._vars.assi) if hasattr(self._vars, 'assi') else -1

    # ---- TFLAG常用访问 ----
    def tflag(self, key: int, default: Any = 0) -> Any:
        """通用TFLAG访问"""
        return self._vars.tflag.get(key, default)

    def set_tflag(self, key: int, value: Any) -> None:
        """设置TFLAG"""
        self._vars.tflag[key] = value

    # ---- 特殊标志 ----
    @property
    def is_first_training(self) -> bool:
        """是否初次调教 (TFLAG:201 == 1)"""
        return int(self._vars.tflag.get(201, 0)) == 1

    @property
    def ejaculation_type(self) -> int:
        """射精类型 (TFLAG:3)"""
        return int(self._vars.tflag.get(3, 0))

    # ---- 调教计数 ----
    @property
    def train_count(self) -> int:
        """调教次数 (TFLAG:200)"""
        return int(self._vars.tflag.get(200, 0))

    # ---- 常用tflag key常量 ----
    # (方便后续重构时查找)
    TFLAG_ASSIPLAY = 50
    TFLAG_PREVCOM = 59
    TFLAG_NEXTCOM = 60
    TFLAG_FIRST_TRAINING = 201
    TFLAG_TRAIN_COUNT = 200
    TFLAG_EJAC_TYPE = 3
