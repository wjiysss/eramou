from __future__ import annotations
"""Module for EquipMixin - EQUIP (equipment) methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EquipMixin:
    """Mixin providing EQUIP (equipment) methods"""
    def _equip_com11(self, target: Character) -> Dict[str, int]:
        source = {}
        abl1 = int(target.abl.get(1, 0))
        source["快V"] = 200 + abl1 * 100
        if int(target.talent.get(76, 0)):
            source["快V"] = int(source.get("快V", 0) * 1.5)
        if int(target.talent.get(85, 0)):
            source["情爱"] = 50
        source["不洁"] = 20
        source["露出"] = 30
        return source


    def _equip_com13(self, target: Character) -> Dict[str, int]:
        source = {}
        abl2 = int(target.abl.get(2, 0))
        source["快A"] = 200 + abl2 * 100
        if int(target.talent.get(76, 0)):
            source["快A"] = int(source.get("快A", 0) * 1.5)
        source["不洁"] = 30
        source["屈辱"] = 30
        return source


    def _equip_com14(self, target: Character) -> Dict[str, int]:
        source = {}
        abl0 = int(target.abl.get(0, 0))
        source["快C"] = 100 + abl0 * 80
        source["露出"] = 20
        return source


    def _equip_com15(self, target: Character) -> Dict[str, int]:
        source = {}
        abl3 = int(target.abl.get(3, 0))
        source["快B"] = 100 + abl3 * 80
        source["露出"] = 20
        source["痛苦"] = 10
        return source


    def _equip_com16(self, target: Character) -> Dict[str, int]:
        source = {}
        abl3 = int(target.abl.get(3, 0))
        source["快B"] = 150 + abl3 * 100
        source["露出"] = 30
        if int(target.talent.get(158, 0)):
            source["快B"] = int(source.get("快B", 0) * 2)
        return source


    def _equip_com43(self, target: Character) -> Dict[str, int]:
        source = {}
        source["恐怖"] = 50
        source["露出"] = 50
        if int(target.talent.get(85, 0)):
            source["恭顺"] = 50
        return source


    def _equip_com44(self, target: Character) -> Dict[str, int]:
        source = {}
        source["恐怖"] = 100
        source["露出"] = 80
        source["痛苦"] = 50
        return source


    def _equip_com45(self, target: Character) -> Dict[str, int]:
        source = {}
        source["恐怖"] = 50
        source["屈辱"] = 50
        source["露出"] = 30
        return source


    def _equip_com53(self, target: Character) -> Dict[str, int]:
        source = {}
        source["露出"] = 200
        source["屈辱"] = 100
        return source


    def _equip_com54(self, target: Character) -> Dict[str, int]:
        source = {}
        source["露出"] = 300
        source["屈辱"] = 200
        source["恐怖"] = 100
        return source


    def _equip_com57(self, target: Character) -> Dict[str, int]:
        source = {}
        source["露出"] = 500
        source["屈辱"] = 300
        source["恐怖"] = 50
        return source


    def _equip_com89(self, target: Character) -> Dict[str, int]:
        source = {}
        source["不洁"] = 500
        source["屈辱"] = 500
        source["恐怖"] = 200
        return source


    def _equip_com100(self, target: Character) -> Dict[str, int]:
        source = {}
        source["快C"] = 200
        source["快V"] = 200
        source["恐怖"] = 100
        source["不洁"] = 100
        return source

    # =====================================================================
    # SOURCE SUB 计算 (辅助函数)
    # =====================================================================

    def _equip_check(self, target=None):
        """装备检查 - 桥接ERB EQUIP_CHECK"""
        return self.call_erb_function('EQUIP_CHECK')


