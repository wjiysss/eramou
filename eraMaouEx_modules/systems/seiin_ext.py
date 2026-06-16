from __future__ import annotations
"""Module for SeiinExtMixin - 精印系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SeiinExtMixin:
    """Mixin providing 精印系统 methods for GameEngine"""

    def _seiin_check(self):
        return self.call_erb_function('SEIIN_CHECK')

    def _seiin_orgasm(self):
        return self.call_erb_function('SEIIN_ORGASM')

    def _seiin_start(self):
        return self.call_erb_function('SEIIN_START')

    def _seiin_compulsion_orgasm(self):
        return self.call_erb_function('SEIIN_COMPULSION_ORGASM')
