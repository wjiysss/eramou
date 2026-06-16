from __future__ import annotations
"""Module for RelationExtMixin - 关系系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class RelationExtMixin:
    """Mixin providing 关系系统 methods for GameEngine"""

    def _get_relation_value(self, char: Character) -> int:
        """获取相性值"""
        v = self.interpreter.vars
        idx = self._find_char_index_for(char)
        if idx < 0:
            return 0
        relation = v.relation if hasattr(v, 'relation') else []
        if idx < len(relation):
            return int(relation[idx])
        return 0

    def _relation_get(self, chara_idx1, chara_idx2):
        self.interpreter.set_var('ARG', chara_idx1)
        self.interpreter.set_var('ARG:1', chara_idx2)
        return self.call_erb_function('RELATION_GET')

    def _relation_set(self, chara_idx1, chara_idx2, value):
        self.interpreter.set_var('ARG', chara_idx1)
        self.interpreter.set_var('ARG:1', chara_idx2)
        self.interpreter.set_var('ARG:2', value)
        return self.call_erb_function('RELATION_SET')

    def _relation_rebuild(self):
        return self.call_erb_function('RELATION_REBUILD')

    def _relation_check_rebuild(self):
        return self.call_erb_function('RELATION_CHECK_REBUILD')





