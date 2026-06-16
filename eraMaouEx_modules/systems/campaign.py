from __future__ import annotations
"""Module for CampaignMixin - 战役系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CampaignMixin:
    """Mixin providing 战役系统 methods for GameEngine"""

    def _advance_campaign_menu(self) -> bool:
        active_id = self._get_active_campaign_id()
        self._render_campaign_menu(active_id)
        choice = self._prompt_campaign_choice()
        return self._handle_campaign_menu_choice(choice, active_id)






    def _apply_campaign_daily_upkeep(self) -> List[str]:
        campaign_id = self._get_active_campaign_id()
        if campaign_id < 1:
            return []
        player = self._get_player()
        if player is None:
            return []
        messages = [f"大型活动【{self._get_campaign_name(campaign_id)}】持续进行中。"]
        player.base[1] = max(0, player.base.get(1, 0) - 100)
        messages.append("魔王气力因持续指挥活动而减少了100。")
        if player.base.get(1, 0) > 0:
            return messages
        messages.append(f"***{player.name}的气力耗尽了***")
        messages.append("战役结束了。")
        campaign_chars = self._get_active_campaign_characters()
        self._clear_active_campaign()
        player.base[1] = 1
        for char in campaign_chars:
            self._set_character_campaign_standby_state(char)
        return messages






    def _apply_campaign_monster_extra_effect(self, leader: Character) -> List[str]:
        extra = self._get_campaign_active_monster_extra(leader)
        if extra <= 0:
            return []
        messages: List[str] = []
        if extra == 2:
            leader.cflag[502] = min(100, leader.cflag.get(502, 0) + 10)
            messages.append(f"{leader.name} 利用地形适应快速穿过了险地，侵攻度额外 +10。")
        elif extra == 400:
            defense_gain = max(1, self._get_character_level(leader) // 3)
            leader.cflag[12] = leader.cflag.get(12, 0) + defense_gain
            messages.append(f"{leader.name} 遇到了肉铠兵支援，防御临时 +{defense_gain}。")
        return messages






    def _apply_campaign_recruit(self) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "没有可用的魔王角色。"
        if player.base.get(1, 0) < 100:
            return False, "气力不足。"
        available, message = self._can_use_life_cradle()
        if not available:
            return False, message
        selected = self._choose_life_cradle_template()
        if selected is None:
            return False, "已取消。"
        new_char = self._instantiate_life_cradle_character(int(selected["id"]))
        if new_char is None:
            return False, "角色模板不存在。"
        self._grant_campaign_mark_to_character(new_char)
        self._append_character(new_char)
        player.base[1] = max(0, player.base.get(1, 0) - 100)
        return True, f"{new_char.name} 获得了大型活动刻印并加入待派遣名单。"






    def _apply_campaign_return(self, leader: Character) -> List[str]:
        messages: List[str] = [f"{leader.name} 从大型活动现场撤回来了。"]
        for member in self._get_dungeon_town_party(leader):
            self._set_character_campaign_standby_state(member)
        return messages






    def _apply_campaign_story_progress(self, leader: Character) -> List[str]:
        campaign_id = self._get_active_campaign_id()
        if campaign_id < 1 or not self._is_character_in_active_campaign(leader):
            return []
        floor = int(leader.cflag.get(501, 1))
        progress = self._get_active_campaign_progress()
        if floor <= progress:
            return []
        lines = self._get_campaign_story_lines(progress)
        self.interpreter.vars.set_flag(401, progress + 1)
        if not lines:
            return []
        return ["-- STORY --"] + lines






    def _dispatch_campaign_character(self, idx: int, char: Character) -> tuple[bool, str]:
        talent_id = self._get_campaign_mark_talent_id()
        if talent_id <= 0 or char.talent.get(talent_id, 0) == 0:
            return False, "该角色没有对应的大型活动刻印。"
        if self._is_maou_shadow(char):
            return False, "魔王之影无法被派遣。"
        if self._is_character_in_active_campaign(char):
            return False, "该角色已经被派遣。"
        if char.cflag.get(1, 0) != 0:
            return False, "该角色当前无法被派遣。"
        self._set_dungeon_assignment_state(
            char,
            state=12,
            work_id=int(char.cflag.get(500, 0)),
            floor=1,
            progress=0,
            fatigue=int(char.cflag.get(505, 0)),
            return_flag=0,
        )
        char.cflag[520] = 0
        char.cflag[521] = 1
        return True, f"已派遣 {char.name} 前往 {self._get_campaign_name(self._get_active_campaign_id())}。"






    def _get_campaign_active_monster_extra(self, leader: Character) -> int:
        campaign_id = self._get_active_campaign_id()
        if campaign_id < 1 or leader.cflag.get(1, 0) != 12:
            return 0
        floor = int(leader.cflag.get(501, 1))
        monster_id = self._get_campaign_monster_list(floor)
        return self._get_campaign_monster_extra(monster_id)




    def _get_campaign_available_entries(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "name": self._get_campaign_name(1),
                "intro": [
                    "极东之地、赤蛮咒森。魔王的支配无法触及的诅咒之地。",
                    "咒森深处有一尊能令女人淫乱至狂的神奇雕像。",
                    "迷惑能够出入咒森的巫女，纳为侵略咒森的棋子吧。",
                ],
            }
        ]




    def _get_campaign_ending_lines(self, campaign_id: int) -> List[str]:
        if int(campaign_id) != 1:
            return []
        return [
            "为何、为何这个女人……不受诱惑！？ 神像之力竟不奏效……",
            "女王对于猥神雕像无法控制感到了恐慌。",
            "神像的力量越来越强，神殿中的人们彻底被性欲所支配。",
            "这次远征或许以失败告终了，但世界仍有尚未发掘之物。",
            "赤森谜路 - ROAD to CRIMSON FOREST -（终）",
        ]




    def _get_campaign_equip_select(self, floor: int) -> int:
        if self._get_active_campaign_id() != 1:
            return -1
        equip_map = {
            3: 313,
            4: 314,
            5: 319,
        }
        return equip_map.get(int(floor), -1)




    def _get_campaign_final_floor(self, campaign_id: Optional[int] = None) -> int:
        active_id = self._get_active_campaign_id() if campaign_id is None else int(campaign_id)
        if active_id == 1:
            return 6
        return 0



    def _get_campaign_mark_talent_id(self, campaign_id: Optional[int] = None) -> int:
        active_id = self._get_active_campaign_id() if campaign_id is None else int(campaign_id)
        return active_id + 360 if active_id > 0 else 0




    def _get_campaign_monster_extra(self, monster_id: int) -> int:
        if self._get_active_campaign_id() != 1:
            return 190
        extra_map = {
            607: 2,
            608: 400,
        }
        return extra_map.get(int(monster_id), 0)




    def _get_campaign_monster_list(self, floor: int) -> int:
        if self._get_active_campaign_id() != 1:
            return 190
        tables = {
            1: [600, 601, 602],
            2: [601, 602, 603],
            3: [603, 604, 605],
            4: [604, 605, 606],
            5: [606, 607, 608],
            6: [607, 608, 609],
        }
        options = tables.get(int(floor), [190])
        return random.choice(options)




    def _get_campaign_name(self, campaign_id: int) -> str:
        if int(campaign_id) == 1:
            return "赤森谜路 - ROAD to CRIMSON FOREST"
        return "无"




    def _get_campaign_room(self, floor: int) -> int:
        if self._get_active_campaign_id() != 1:
            return self.interpreter.vars.get_flag(350 + floor - 1, 0)
        return 502 if floor > 3 else 0




    def _get_campaign_room_extra(self, floor: int) -> int:
        if self._get_active_campaign_id() != 1:
            return self.interpreter.vars.get_flag(360 + floor - 1, 0)
        extra = 0
        if floor > 4:
            extra += 1
        if floor > 5:
            extra += 2
        return extra




    def _get_campaign_story_lines(self, progress: int) -> List[str]:
        if self._get_active_campaign_id() != 1:
            return []
        story_map = {
            0: [
                "真是奇妙的森林。奇形怪状的植物，与其共生进化而来的动物和昆虫四处蔓延。",
                "半裸的原住民见到魔王的奴隶便四下逃开，森林深处的神殿似乎藏着关键。",
            ],
            1: [
                "越往深处前进，空气中的甜腻气味越发浓重。",
                "原住民的踪迹越来越少，取而代之的是更加鲜艳妖异的植物群。",
            ],
            2: [
                "赤蛮咒森的防卫开始加强，敌方也意识到了入侵者正在逼近。",
            ],
            3: [
                "森林深处的神殿残影已经若隐若现，派遣队伍离目标越来越近。",
            ],
            4: [
                "派遣队伍接近最深处，空气里弥漫着不祥而淫靡的气息。",
            ],
            5: [
                "最后的障碍已经被跨越，终焉近在眼前。",
            ],
        }
        return story_map.get(int(progress), [])




    def _get_campaign_trap_id(self, trap_num: int) -> int:
        if self._get_active_campaign_id() != 1:
            return 0
        trap_map = {
            301: 60,
            302: 60,
            303: 82,
            304: 82,
            305: 78,
            312: 72,
            313: 72,
            314: 84,
            315: 84,
            323: 76,
            324: 65,
            325: 65,
        }
        return trap_map.get(int(trap_num), 0)




    def _grant_campaign_mark_to_character(self, char: Character):
        talent_id = self._get_campaign_mark_talent_id()
        if talent_id > 0:
            char.talent[talent_id] = 1






    def _handle_campaign_action_menu_choice(self, sub: str) -> bool:
        if sub == "999":
            return True
        try:
            campaign_id = int(sub)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        ok, messages = self._start_campaign(campaign_id)
        print()
        for line in messages:
            print(line)
        if not ok:
            self._pause()
            return False
        self._pause()
        return True






    def _handle_campaign_dispatch_menu_choice(self, candidates: List[tuple[int, Character]], sub: str) -> bool:
        try:
            char_idx = int(sub)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False
        selected = next(((idx, char) for idx, char in candidates if idx == char_idx), None)
        if selected is None:
            print("\nInvalid selection.")
            self._pause()
            return False
        ok, message = self._dispatch_campaign_character(*selected)
        print(f"\n{message}")
        self._pause()
        return ok






    def _handle_campaign_menu_choice(self, choice: str, active_id: int) -> bool:
        if choice == "999":
            return True
        if choice == "0":
            self._show_campaign_action_selection(active_id)
            return False
        if active_id == 0:
            print("\n请先选择行动。")
            self._pause()
            return False
        if choice == "1":
            ok, message = self._apply_campaign_recruit()
            print(f"\n{message}")
            self._pause()
            return False
        if choice == "2":
            self._show_campaign_dispatch_menu()
            return False
        if choice == "3":
            self._show_campaign_status_menu(active_id)
            return False
        print("\nInvalid selection.")
        self._pause()
        return False






    def _list_campaign_dispatch_candidates(self) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        talent_id = self._get_campaign_mark_talent_id()
        if talent_id <= 0:
            return candidates
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0 or char.base.get(0, 0) < 1:
                continue
            if char.talent.get(talent_id, 0) == 0:
                continue
            if self._is_maou_shadow(char):
                continue
            if char.cflag.get(1, 0) != 0:
                continue
            candidates.append((idx, char))
        return candidates






    def _prompt_campaign_action_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_campaign_choice(self):
        return self._prompt_choice()






    def _prompt_campaign_dispatch_choice(self) -> str:
        return self._prompt_choice()






    def _render_campaign_action_selection(self, entries: List[Dict[str, Any]]) -> None:
        print("\n【选择大型活动】")
        print("-" * 30)
        for entry in entries:
            print(f" [{entry['id']}] {entry['name']}")
        print(" [999] Back")






    def _render_campaign_dispatch_menu(self, candidates: List[tuple[int, Character]]) -> None:
        print("\n请选择要派遣的奴隶")
        for idx, char in candidates:
            status = "已派遣" if self._is_character_in_active_campaign(char) else "待命"
            print(f" [{idx}] {char.name} LV{self._get_character_level(char)} {status}")
        print(" [999] Back")






    def _render_campaign_menu(self, active_id: int):
        print("\n【Campaign】")
        print("-" * 30)
        print(f" 当前行动: {self._get_campaign_name(active_id)}")
        if active_id == 0:
            print(" [0] 行动选择")
        else:
            print(" [1] 奴隶选召（气力-100）")
            print(" [2] 派遣奴隶")
            print(" [3] 查看活动状态")
        print(" [999] Back")






    def _resolve_campaign_completion(self, leader: Character) -> List[str]:
        campaign_id = self._get_active_campaign_id()
        if campaign_id < 1 or leader.cflag.get(1, 0) != 12 or leader.cflag.get(521, 0) != 1:
            return []
        final_floor = self._get_campaign_final_floor(campaign_id)
        if final_floor <= 0 or int(leader.cflag.get(501, 1)) < final_floor:
            return []
        messages = [
            f"{leader.name} 到达了 {self._get_campaign_name(campaign_id)} 的最深处。",
            "-- ENDING --",
        ]
        messages.extend(self._get_campaign_ending_lines(campaign_id))
        campaign_chars = self._get_active_campaign_characters()
        for char in campaign_chars:
            self._set_character_campaign_standby_state(char)
        self._clear_active_campaign()
        return messages






    def _show_campaign_action_selection(self, active_id: int):
        if active_id != 0:
            print("\n当前无法变更行动。")
            self._pause()
            return
        entries = self._get_campaign_available_entries()
        self._render_campaign_action_selection(entries)
        sub = self._prompt_campaign_action_choice()
        self._handle_campaign_action_menu_choice(sub)






    def _show_campaign_dispatch_menu(self):
        candidates = self._list_campaign_dispatch_candidates()
        if not candidates:
            print("\n当前没有可派遣的对象。")
            self._pause()
            return
        self._render_campaign_dispatch_menu(candidates)
        sub = self._prompt_campaign_dispatch_choice()
        self._handle_campaign_dispatch_menu_choice(candidates, sub)






    def _show_campaign_menu(self):
        while True:
            if self._advance_campaign_menu():
                return






    def _show_campaign_status_menu(self, active_id: int):
        print("\n【Campaign Status】")
        print(f" 名称: {self._get_campaign_name(active_id)}")
        print(f" 进度: {self._get_active_campaign_progress()}")
        print(f" 地城等级: {self._get_campaign_dungeon_level()}")
        parties = self._get_active_campaign_character_entries()
        if parties:
            for idx, char in parties:
                print(f" [{idx}] {char.name} - {self._summarize_dungeon_party(char)}")
        else:
            print(" 当前没有活动中的队伍。")
        self._pause()






    def _start_campaign(self, campaign_id: int) -> tuple[bool, List[str]]:
        entry = next((item for item in self._get_campaign_available_entries() if int(item["id"]) == int(campaign_id)), None)
        if entry is None:
            return False, ["未找到对应的大型活动。"]
        self._set_active_campaign(int(campaign_id))
        return True, list(entry["intro"])





