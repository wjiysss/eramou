from __future__ import annotations
"""Module for MuseumExtMixin - 博物馆"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class MuseumExtMixin:
    """Mixin providing 博物馆 methods for GameEngine"""

    def _apply_museum_collection_achievement_if_needed(self) -> List[str]:
        player = self._get_player()
        if player is None:
            return []
        if int(self.interpreter.vars.get_flag(84, 0)) < 20:
            return []
        total_days = self._get_total_day_count()
        if total_days >= 60 or int(player.talent.get(329, 0)):
            return []
        player.talent[329] = 1
        return [
            "派遣讨伐魔王的勇者，似乎让城市渐渐过上了安宁的日子……",
            "某天，传出了地下城附近建起一座以魔王的“友好之证”为名的博物馆的传闻。",
            "你获得了素质【友好之证】。",
        ]






    def _build_museum_mature_title(self, target: Character, option: Dict[str, Any]) -> str:
        option_id = int(option["id"])
        flag_id = self._get_museum_exhibit_flag_id(target, option)
        exhibit_title = self._get_museum_exhibit_title(target, option)
        prefix = self._get_museum_exhibit_mature_prefix(target, option_id, flag_id)
        if option_id == 9:
            return f"{prefix}像" if prefix else "画像"
        return f"{prefix}{exhibit_title}"






    def _get_museum_exhibit_flag_id(self, target: Character, option: Dict[str, Any]) -> int:
        option_id = int(option["id"])
        if option_id == 0 and (target.talent.get(57, 0) or target.talent.get(121, 0) or target.talent.get(122, 0) or target.talent.get(130, 0)):
            return 611
        if option_id == 5 and (target.talent.get(57, 0) or target.talent.get(121, 0) or target.talent.get(122, 0) or target.talent.get(130, 0)):
            return 612
        return int(option["flag_id"])






    def _get_museum_exhibit_mature_prefix(self, target: Character, option_id: int, flag_id: int) -> str:
        if option_id in (0, 5):
            if flag_id == 611:
                prefix = ""
                if int(target.talent.get(121, 0)) or int(target.talent.get(122, 0)):
                    prefix += "射精"
                if int(target.talent.get(130, 0)):
                    prefix += "喷乳"
                if int(target.talent.get(153, 0)):
                    prefix += "妊娠"
                if int(target.talent.get(136, 0)):
                    prefix += "牝犬"
                if int(target.talent.get(113, 0)):
                    prefix += "魅惑"
                return prefix
            prefix = ""
            if int(target.talent.get(153, 0)):
                prefix += "妊娠"
            if int(target.talent.get(136, 0)):
                prefix += "牝犬"
            if int(target.talent.get(113, 0)):
                prefix += "魅惑"
            return prefix
        if option_id in (1, 2, 6, 7):
            if int(target.talent.get(153, 0)):
                return "妊娠"
            if int(target.talent.get(113, 0)):
                return "魅惑"
            if int(target.talent.get(136, 0)) and option_id == 7:
                return "牝犬"
            return ""
        if option_id == 3:
            prefix = ""
            body_type = int(target.talent.get(308, 0))
            if body_type <= 201:
                prefix += "肉感"
            elif body_type >= 100:
                prefix += "纤细"
            charm = int(target.talent.get(312, 0))
            charm_map = {
                12: "美乳",
                13: "细腰",
                14: "翘臀",
                15: "美腿",
                23: "巨尻",
            }
            prefix += charm_map.get(charm, "")
            if int(target.talent.get(153, 0)):
                prefix = "妊娠" + prefix
            if int(target.talent.get(113, 0)):
                prefix = "魅惑" + prefix
            return prefix
        if option_id == 4:
            if int(target.talent.get(153, 0)):
                return "妊娠的"
            if int(target.talent.get(113, 0)):
                return "魅惑的"
            return ""
        if option_id == 8:
            return ""
        if option_id == 9:
            if int(target.talent.get(85, 0)):
                return "魔王侧室"
            former_life = int(target.talent.get(315, 0))
            if int(target.talent.get(317, 0)) == 4 or former_life == 21:
                return "人妻"
            if former_life == 1:
                return "学生"
            if former_life in (2, 12):
                return "升天"
            return random.choice(["森女", "裸妇", "娼妇", "群交", "贵族", "人鱼", "狂王性奴"])
        return ""






    def _get_museum_exhibit_options(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "name": "石像", "title": "石像", "flag_id": 600},
            {"id": 1, "name": "标本", "title": "标本", "flag_id": 601},
            {"id": 2, "name": "蜡像", "title": "蜡像", "flag_id": 602},
            {"id": 3, "name": "人体模型人偶", "title": "人体模型人偶", "flag_id": 603},
            {"id": 4, "name": "球型关节人偶", "title": "球型关节人偶", "flag_id": 604},
            {"id": 5, "name": "金属雕像", "title": "金属雕像", "flag_id": 605},
            {"id": 6, "name": "冰雕", "title": "冰雕", "flag_id": 606},
            {"id": 7, "name": "宝石像", "title": "宝石像", "flag_id": 607},
            {"id": 8, "name": "屋内家具", "title": "人形家具", "flag_id": 608},
            {"id": 9, "name": "画像", "title": "画像", "flag_id": 609},
        ]






    def _get_museum_exhibit_title(self, target: Character, option: Dict[str, Any]) -> str:
        option_id = int(option["id"])
        if option_id == 0 and self._get_museum_exhibit_flag_id(target, option) == 611:
            return "石制喷水像"
        if option_id == 5 and self._get_museum_exhibit_flag_id(target, option) == 612:
            return "金属喷水像"
        return str(option["title"])


    def _museum(self):
        return self.call_erb_function('MUSEUM')

    def _museum_koujo(self, kojo_num):
        self.interpreter.set_var('ARG', kojo_num)
        return self.call_erb_function('MUSEUM_KOUJO')





