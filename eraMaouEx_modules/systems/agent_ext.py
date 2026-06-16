from __future__ import annotations
"""Module for AgentExtMixin - 特工系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class AgentExtMixin:
    """Mixin providing 特工系统 methods for GameEngine"""

    def _agent_event(self, agent_idx: int) -> List[str]:
        """间谍事件处理 - 对应 AGENT_EVENT.ERB / CAMPAIGN_QUEST

        处理派遣间谍在敌方地城中的事件、故事推进和结局。
        """
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars
        campaign_id = int(v.flag.get(400, 0))

        if campaign_id < 1:
            return lines

        if agent_idx < 0 or agent_idx >= len(chars):
            return lines

        char = chars[agent_idx]
        name = char.name or f"角色{agent_idx}"

        # 检查是否处于派遣状态
        if int(char.cflag.get(1, 0)) != 12:
            return lines

        # 战役进度检查 - 阶层超过进度时推进故事
        current_floor = int(char.cflag.get(501, 1))
        story_progress = int(v.flag.get(401, 0))

        if current_floor > story_progress:
            lines.append("―STORY―")
            # 尝试调用ERB战役故事函数
            story_func = f"CAMPAIGN_STORY_{campaign_id}"
            if story_func in self.interpreter.functions:
                try:
                    story_output = self.interpreter.call_erb_function(story_func)
                    lines.extend(story_output)
                except Exception:
                    lines.append(f"{name}在敌方地城继续前进着……")
            else:
                lines.append(f"{name}在敌方地城继续前进着……")

            # 推进故事进度
            v.flag[401] = story_progress + 1

        # 战役关卡检查
        quest_func = f"CAMPAIGN_QUEST_{campaign_id}"
        if quest_func in self.interpreter.functions:
            try:
                self.interpreter.call_erb_function(quest_func, agent_idx)
            except Exception:
                pass

        # 游戏结束判定 - 主角气力耗尽
        master = chars[0] if len(chars) > 0 else None
        if master is not None and int(master.base.get(1, 0)) <= 0:
            lines.append(f"***{master.name or '魔王'}的体力耗尽了***")
            lines.append("战役结束了")
            v.flag[400] = 0
            master.base[1] = 1
            # 取消所有派遣状态
            for c in chars:
                if int(c.cflag.get(1, 0)) == 12:
                    c.cflag[1] = 0

        return lines

    # ==================================================================
    # Character Template Data - 角色模板数据 (CHARA0-35.ERB)
    # ==================================================================



    def _agent_main(self) -> List[str]:
        """间谍系统主菜单 - 对应 @AGENT_MENU

        管理战役选择、奴隶选择与派遣。
        FLAG:400 = 当前战役编号 (0=无)
        FLAG:401 = 战役进度(深度)
        """
        lines: List[str] = []
        v = self.interpreter.vars
        campaign_id = int(v.flag.get(400, 0))

        lines.append("=" * 40)
        if campaign_id > 0:
            # 尝试获取战役名称
            campaign_name = ""
            name_func = f"CAMPAIGN_NAME_{campaign_id}"
            if name_func in self.interpreter.functions:
                try:
                    name_output = self.interpreter.call_erb_function(name_func)
                    campaign_name = "".join(name_output).strip()
                except Exception:
                    campaign_name = f"战役{campaign_id}"
            else:
                campaign_name = f"战役{campaign_id}"
            lines.append(f"当前选择的目标: {campaign_name}")
        else:
            lines.append("当前选择的目标: 无")
        lines.append("=" * 40)

        if campaign_id == 0:
            lines.append("[0] 行动选择")
        else:
            lines.append("[1] 奴隶选择（气力-100）")
            lines.append("[2] 派遣奴隶")
        lines.append("=" * 40)
        lines.append("[999] 返回")

        return lines




    def _agent_send(self, agent_idx: int, target_area: int) -> List[str]:
        """派遣间谍到指定区域 - 对应 AGENT.ERB 中的派遣逻辑

        agent_idx: 被派遣角色的索引
        target_area: 目标区域(=战役编号)
        """
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars

        if agent_idx < 0 or agent_idx >= len(chars):
            lines.append("*无效的角色*")
            return lines

        char = chars[agent_idx]
        campaign_id = int(v.flag.get(400, 0))

        if campaign_id == 0:
            lines.append("*请先选择行动*")
            return lines

        # 检查角色状态
        name = char.name or f"角色{agent_idx}"
        if int(char.base.get(0, 0)) < 1:
            lines.append(f"*{name}濒死中，无法派遣*")
            return lines

        # 检查事件素质 (FLAG:400 + 360)
        talent_id = campaign_id + 360
        if int(char.talent.get(talent_id, 0)) == 0:
            talent_name = v.talent_name.get(talent_id, f"素质{talent_id}")
            lines.append(f"无法派遣没有【{talent_name}】的奴隶")
            return lines

        # 检查魔王之影
        if int(char.talent.get(292, 0)):
            lines.append(f"由于{name}是魔王之影而无法派遣")
            return lines

        # 检查是否已被派遣
        if int(char.cflag.get(1, 0)) == 12:
            lines.append(f"{name}已经被派遣了")
            return lines

        # 检查是否可派遣
        if int(char.cflag.get(1, 0)) != 0:
            lines.append(f"{name}当前无法被派遣")
            return lines

        # 执行派遣
        char.cflag[1] = 12  # 派遣状态
        char.cflag[501] = 1  # 当前阶层
        char.cflag[507] = 0  # 归还标志
        char.cflag[520] = 0  # 目标阶层
        char.cflag[521] = 1  # 到达阶层记忆
        lines.append(f"派遣了{name}")

        return lines

    def _agent_menu(self):
        return self.call_erb_function('AGENT_MENU')

    def _agent_dungeon_lv_1(self):
        return self.call_erb_function('AGENT_DUNGEON_LV_1')

    def _agent_ending_1(self):
        return self.call_erb_function('AGENT_ENDING_1')

    def _agent_equip_select_1(self):
        return self.call_erb_function('AGENT_EQUIP_SELECT_1')

    def _agent_exist_1(self):
        return self.call_erb_function('AGENT_EXIST_1')

    def _agent_monster_extra_1(self):
        return self.call_erb_function('AGENT_MONSTER_EXTRA_1')

    def _agent_monster_list_1(self):
        return self.call_erb_function('AGENT_MONSTER_LIST_1')

    def _agent_name_1(self):
        return self.call_erb_function('AGENT_NAME_1')

    def _agent_quest_1(self):
        return self.call_erb_function('AGENT_QUEST_1')

    def _agent_room_1(self):
        return self.call_erb_function('AGENT_ROOM_1')

    def _agent_room_extra_1(self):
        return self.call_erb_function('AGENT_ROOM_EXTRA_1')

    def _agent_set_1(self):
        return self.call_erb_function('AGENT_SET_1')

    def _agent_story_1(self):
        return self.call_erb_function('AGENT_STORY_1')

    def _agent_trap_1(self):
        return self.call_erb_function('AGENT_TRAP_1')



