"""
eraMaouEx 模块化重构包 - Mixin架构

将原单文件的 eraMaouEx.py 拆分为独立Mixin模块：
- core: 核心常量和基础类
- systems: 游戏系统Mixin（调教、商店、地城等）
"""

from .core import constants

__version__ = '0.2.0'

__all__ = ['constants']
