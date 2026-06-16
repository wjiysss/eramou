from __future__ import annotations
"""Module for DataQueryMixin - 数据查询"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class DataQueryMixin:
    """Mixin providing 数据查询 methods for GameEngine"""

    def _get_active_campaign_character_entries(self) -> List[tuple[int, Character]]:
        entries: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if self._is_character_in_active_campaign(char):
                entries.append((idx, char))
        return entries

    def _get_active_campaign_characters(self) -> List[Character]:
        return [char for char in self.interpreter.vars.chars if self._is_character_in_active_campaign(char)]

    def _get_active_campaign_id(self) -> int:
        return int(self.interpreter.vars.get_flag(400, 0))

    def _get_active_campaign_progress(self) -> int:
        return int(self.interpreter.vars.get_flag(401, 0))

    def _get_aftertrain_masturbation_fantasy(self, target: Character, assistant: Optional[Character], lesbian_played: bool) -> tuple[str, int]:
        if int(target.talent.get(85, 0)) == 0 and lesbian_played == 1 and assistant is not None and int(target.abl.get(22, 0)) > random.randint(0, 4):
            return assistant.name, 1
        if int(target.talent.get(85, 0)) == 0 and int(target.abl.get(39, 0)) > random.randint(0, 4) and int(self.interpreter.vars.item[22]) > 0:
            return "兽交", 2
        player = self._get_player()
        return (player.name if player is not None else "主人"), 0

    def _get_assistant(self) -> Optional[Character]:
        """获取助手角色"""
        v = self.interpreter.vars
        assi_idx = v.assi if hasattr(v, 'assi') else -1
        if assi_idx >= 0 and assi_idx < len(v.chars):
            return v.chars[assi_idx]
        return None

    def _get_available_human_birth_template_ids(self) -> List[int]:
        return [
            template_id
            for template_id in list(range(1, 17)) + list(range(201, 211))
            if self._has_character_template(template_id)
        ]

    def _get_available_train_commands(self, target: Optional[Character]) -> List[int]:
        command_ids = [0, 1, 2, 3, 6, 30, 40, 50, 53, 56, 62, 64, 65, 128, 129, 130, 131, 132, 133, 134]
        return [command_id for command_id in command_ids if self._is_train_command_available(command_id, target)]

    def _get_birth_place_description(self, target: Character) -> str:
        if int(target.talent.get(341, 0)):
            return "从巨大的乳房中"
        if int(target.talent.get(342, 0)):
            return "从巨大的阴囊，通过阴茎"
        if int(target.talent.get(343, 0)):
            return "从巨大的腹部，通过肛门"
        return ""

    def _get_bit(self, val: int, bit: int) -> bool:
        """Get a specific bit from a value."""
        return bool(val & (1 << bit))

    def _get_body_desc(self, target) -> str:
        """Get body description.
        Corresponds to ERB LOOK_INFO body/nipple/pubic hair/penis section.
        """
        parts: List[str] = []
        body_type = int(target.talent.get(308, 0))
        nipple = int(target.talent.get(309, 0))
        pubic = int(target.talent.get(310, 0))
        if body_type and nipple and pubic:
            desc = f"[体型：{self._get_body_type_name(target)}]"
            desc += f"[乳头：{self._get_nipple_name(target)}]"
            desc += f"[阴毛：{self._get_pubic_hair_name(target)}]"
            # 阴茎 - 扶她或男人
            if int(target.talent.get(121, 0)) or int(target.talent.get(122, 0)):
                desc += f"[阴茎：{self._get_penis_state_name(target)}]"
            parts.append(desc)
        return "".join(parts)

    def _get_body_type_name(self, target) -> str:
        """获取体型名称 (TALENT:308)"""
        v = int(target.talent.get(308, 0))
        if 1 <= v <= 100:
            return "纤细"
        elif 101 <= v <= 200:
            return "标准"
        elif 201 <= v <= 300:
            return "丰满"
        return "ERROR"

    def _get_buy_plural_ids(self) -> List[int]:
        return [24, 25, 26, 27, 28, 34, 35, 53, 55] + [item_id for item_id in range(60, 90) if item_id in self.item_catalog and item_id != 90]

    def _get_calendar_month_length(self, month: int) -> int:
        if month == 2:
            return 28
        if month in {4, 6, 9, 11}:
            return 30
        return 31

    def _get_call_name(self, target: Character, other: Character) -> str:
        """Get how target calls other character.
        Uses CSTR:60 of the other character (their self-call) as a basis,
        falling back to the other character's callname/name.
        """
        other_self_call = str(other.cstr.get(60, "")).strip()
        if other_self_call:
            return other_self_call
        return other.callname or other.name or "我"

    def _get_chara_cost_value(self, target: Character) -> int:
        plus_150k = {0, 1, 10, 13, 14, 17, 23, 25, 28, 31, 37, 41, 42, 50, 52, 55, 57, 60, 61, 63, 64, 70, 72, 73, 74, 75, 76, 77, 78, 80, 81, 88, 89, 91, 92, 93, 99, 102, 104, 106, 108, 110, 111, 113, 114, 117, 118, 124, 125, 126, 130, 131, 132, 134, 136, 140, 141, 142, 143, 153, 154, 155, 157, 180, 181, 182, 183, 184, 185, 186, 187, 230, 231, 232, 233, 254, 271}
        plus_200k = set(range(240, 253)) | set(range(257, 264)) | {119}
        plus_600k = {85, 86}
        minus_50k = {11, 12, 15, 16, 84, 100, 133}
        minus_100k = {9, 20, 21, 22, 24, 27, 30, 32, 34, 43, 46, 51, 56, 62, 69, 71, 79, 82, 101, 103, 105, 107, 109, 112, 115, 116, 122, 123, 135, 150, 151, 152, 256, 273, 280}
        cost = 0
        for talent_id, value in target.talent.items():
            if int(value) != 1:
                continue
            if talent_id in plus_150k or 275 <= talent_id <= 279 or 471 <= talent_id <= 485:
                cost += 150000
            elif talent_id in plus_200k:
                cost += 200000
            elif talent_id in plus_600k:
                cost += 600000
            elif talent_id in minus_50k:
                cost -= 50000
            elif talent_id in minus_100k:
                cost -= 100000
            elif 200 <= talent_id <= 222:
                cost += 10000
        if target.talent.get(300, 0) == 11:
            cost += 100000
        return max(0, cost) + 500000

    def _get_charm_point_name(self, target) -> str:
        """获取魅力点名称 (TALENT:312)"""
        v = int(target.talent.get(312, 0))
        if v == 29:
            if int(target.talent.get(121, 0)) or int(target.talent.get(122, 0)):
                return "自己的鸡鸡"
            return "私处"
        return self._CHARM_POINT_NAMES.get(v, "ERROR")

    def _get_child_care_begin_kojo_lines(self, target: Character) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        if kojo_num == 100 and (int(target.talent.get(85, 0)) or int(target.talent.get(76, 0))):
            return [
                "「快看……爸爸来了哦？」",
                "「来打个招呼吧……？」",
                "她一边哄着孩子，一边露出了温柔的神情。",
            ]
        if kojo_num == 101 and (int(target.talent.get(85, 0)) or int(target.talent.get(76, 0))):
            return ["「呼呼，这孩子还真是好麻烦啊♪」"]
        if kojo_num == 103 and (int(target.talent.get(85, 0)) or int(target.talent.get(76, 0))):
            return ["「啊啊，我可爱的小宝宝！真不想放手呢！」"]
        if kojo_num == 105 and (int(target.talent.get(85, 0)) or int(target.talent.get(76, 0))):
            return ["「看啊，这么可爱的小宝宝哦……」"]
        if kojo_num == 119 and (int(target.talent.get(85, 0)) or int(target.talent.get(76, 0))):
            return ["「要健康地成长起来哦……」"]
        return []

    def _get_child_care_depart_kojo_lines(self, target: Character) -> List[str]:
        self.interpreter._set_self_kojo_context(target, 14)
        return self._run_self_kojo_lines(target)

    def _get_child_care_nurse_candidates(self, target: Character) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if int(char.talent.get(153, 0)) or int(char.talent.get(154, 0)):
                continue
            if int(char.talent.get(155, 0)) == 0:
                continue
            if int(char.talent.get(9, 0)):
                continue
            if int(char.cflag.get(0, 0)) != 2:
                continue
            if int(char.cflag.get(1, 0)) != 0:
                continue
            candidates.append((idx, char))
        return candidates

    def _get_child_care_visit_kojo_lines(self, target: Character) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        in_love = bool(int(target.talent.get(85, 0)) or int(target.talent.get(76, 0)))
        if not in_love:
            return []
        if int(target.talent.get(153, 0)):
            if kojo_num == 100:
                return [
                    "「嗯，马上就要生产了哦，请好好期待吧……」",
                    f"{target.name} 抚摸着即将临盆而鼓起的大肚子。",
                ]
            if kojo_num == 101:
                return [
                    "「另外，你真的有在担心我吗？」",
                    f"{target.name} 轻轻抚摸着快到产期的肚子。",
                ]
            if kojo_num == 103:
                return [
                    "「还有一会就要生出来了，敬请期待吧……♪」",
                    f"{target.name} 摸着迎接临盆而鼓起的肚子。",
                ]
            if kojo_num == 105:
                return [
                    "「在我的肚子里孕育着新生命……总觉得很不可思议呢。」",
                    f"{target.name} 抚摸着高高鼓起的肚子，安静地等待着生产。",
                ]
            if kojo_num == 119:
                return [f"{target.name} 安静地护着腹中的孩子。"]
            return []
        if int(target.talent.get(154, 0)):
            if kojo_num == 100:
                return [
                    "「快看……爸爸来了哦？」",
                    "「来打个招呼吧……？」",
                    f"{target.name} 和孩子亲密地依偎着。",
                ]
            if kojo_num == 101:
                return [
                    "「呼呼，这孩子还真是好麻烦啊♪」",
                    f"{target.name} 一边哄着孩子，一边露出得意的笑。",
                ]
            if kojo_num == 103:
                return [
                    "「啊啊，我可爱的小宝宝！真不想放手呢！」",
                    f"{target.name} 小心地抱着孩子。",
                ]
            if kojo_num == 105:
                return [
                    "「看啊，这么可爱的小宝宝哦……」",
                    f"{target.name} 一边哄着孩子，一边露出温柔的神情。",
                ]
            if kojo_num == 119:
                return ["「要健康地成长起来哦……」"]
        return []

    def _get_childbirth_kojo_lines(self, target: Character, source: int) -> List[str]:
        first_time = int(target.cflag.get(272, 0)) == 0
        kojo_num = self._get_kojo_num(target)
        if kojo_num == 100:
            if first_time:
                if int(target.talent.get(9, 0)):
                    return ["「呐呐……肚子里的厉害家伙，会从哪里出来呢？」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「哈啊……哈啊……和父亲真像……真是个可爱的小宝宝……♪」"]
                if source in (2, 3):
                    return ["「生下来了……生下来了………」"]
                if source == 4:
                    return ["「至少……要给这个孩子祝福………」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return [
                        "「平安出生了呢……我和狗狗大人的孩子……♪」",
                        f"{target.name} 温柔地亲吻着熟睡的小狗崽，脸上洋溢着母爱的光辉。",
                    ]
                if source == 5:
                    return ["「这样的小狗……才不是我的孩子……呜！」"]
                if source == 7:
                    return ["「啊啊……生、生下来了……啊啊啊啊………」"]
            else:
                if int(target.talent.get(9, 0)):
                    return ["「啊哈哈……又从肚子里出来了呢……♪」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return [
                        "「有了上次的经验，这次的生产更加顺利了♪」",
                        f"{target.name} 抱着刚出生的小狗崽，熟练地撩起衣服给它喂奶。",
                    ]
                if source == 5:
                    return ["「这样的小狗……才不是我的孩子……呜！」"]
                if source == 7:
                    return ["「啊啊……生、生下来了……啊啊啊啊………」"]
                return ["「啊啊啊……又、生下来了………」"]
        if kojo_num == 101:
            if first_time:
                if int(target.talent.get(9, 0)):
                    return ["「啊哇哈哈……你的角在生长～？非常可爱～？」"]
                if source == 6 and int(target.cflag.get(602, 0)) > 40:
                    return ["「生、生下来了……可爱的孩子……！」"]
                if source == 6:
                    return ["「生、生下来了……怪物的孩子……！」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「这个孩子出来了的话……真的是不能离开你了啊……」"]
            else:
                if int(target.talent.get(9, 0)):
                    return ["「啊哇哈哈……又生出来了吗……真可爱呀……？」"]
                if source == 6 and int(target.cflag.get(602, 0)) > 40:
                    return ["「生、生下来了……可爱的孩子……！」"]
                if source == 6:
                    return ["「生、生下来了……怪物的孩子……！」"]
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「这个孩子出来了的话……真的是不能离开你了啊……」"]
                if source == 5 and int(target.talent.get(136, 0)):
                    return ["「健康的狗的孩子生下来了吗？」"]
                if source == 7:
                    return ["「哈哈……生下狂王大人的孩子什么的………」"]
                return ["「哈……哈……哈……这样的孩子出生了什么的………」"]
        if kojo_num == 103 and first_time:
            if int(target.talent.get(9, 0)):
                return ["「嗯哈啊啊……有什么要出来了……要出来了……」"]
            if int(target.talent.get(85, 0)) and source == 1:
                return ["「哈啊……啊啊……果然，跟我想象中一样……跟大人你一模一样呢……」"]
            if source in (2, 3, 4):
                return ["「呜……呜呜……我的小宝宝要………」"]
            if source == 5 and int(target.talent.get(136, 0)):
                return ["「要、要生出来了，可爱的狗宝宝……♪」"]
            if source == 7:
                return ["「要、要生出来了，狂王大人的孩子……但是……」"]
            return ["「呜……呜呜……我的小宝宝要………」"]
        if kojo_num == 105 and first_time:
            if int(target.talent.get(9, 0)):
                return [
                    "「啊呀呀啊啊……精神的小宝宝出生了哦……看啊……姐姐……」",
                    f"精神已经完全混乱的{target.name} 嘴里说着莫名其妙的话。",
                ]
            if int(target.talent.get(85, 0)) and source == 1:
                return [
                    "「生出来啦……啊啊……我的小宝宝出生了哦………」",
                    f"{target.name} 流下喜悦的泪水，不停地喘息着。",
                ]
            return [
                f"{target.name} 刚怀孕时还十分抗拒，不过到了临月终于完全老实了下来。",
                "「像这样生孩子什么的……从来就没想过啊………」",
            ]
        if kojo_num == 119:
            if first_time:
                if int(target.talent.get(85, 0)) and source == 1:
                    return ["「……要健康地出生哦。」"]
                if source == 7:
                    return ["「这是狂王的孩子……」"]
        return []

    def _get_conquest_random_hair_colors(self) -> List[int]:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def _get_conquest_random_personality_ids(self) -> List[int]:
        return [160, 161, 162, 163, 164, 166, 172, 173]

    def _get_current_assistant(self) -> Optional[Character]:
        assi_idx = int(self.interpreter.vars.assi)
        if 0 <= assi_idx < len(self.interpreter.vars.chars):
            assistant = self.interpreter.vars.chars[assi_idx]
            if assi_idx > 0 and assistant.cflag.get(1, 0) == 0:
                return assistant
        return None

    def _get_default_callname(self, char) -> str:
        """获取默认自称"""
        if char.talent.get(122, 0):
            return "俺"
        elif char.talent.get(121, 0):
            return "僕"
        else:
            if char.talent.get(17, 0):
                return "わたくし"
            elif char.talent.get(13, 0):
                return "わたし"
            elif char.talent.get(12, 0):
                return "あたし"
            else:
                return "私"

    def _get_default_race_age_flags(self) -> tuple[int, int]:
        return 232015325431115011, 1001

    def _get_dog_walk_open_score(self, char: Character) -> int:
        open_score = int(char.abl.get(17, 0)) - 2
        if char.talent.get(89, 0):
            open_score += 1
        if char.talent.get(28, 0):
            open_score += 1
        return open_score

    def _get_dog_walk_play_score(self, char: Character) -> int:
        play = int(char.abl.get(39, 0))
        if char.talent.get(136, 0):
            play += 2
        if char.talent.get(124, 0) and play > 0:
            play += 1
        if char.talent.get(317, 0) == 12 and play > 0:
            play += 1
        return play

    def _get_dog_walk_target(self) -> int:
        if len(self.interpreter.vars.chars) <= 1:
            return 0
        selected_idx = random.randrange(len(self.interpreter.vars.chars) - 1)
        if selected_idx == 0:
            return 0
        selected = self.interpreter.vars.chars[selected_idx]
        if selected.cflag.get(1, 0) != 0:
            return 0
        if selected.cflag.get(0, 0) == 0:
            return 0
        return selected_idx

    def _get_elapsed_day_count(self) -> int:
        return self._get_total_day_count()

    def _get_endcheck_tracked_character_flags(self) -> Dict[int, int]:
        return {
            17: 2805,
            20: 2813,
            23: 2812,
            24: 2806,
            31: 2808,
            32: 2809,
            34: 2815,
        }

    def _get_ending_event_store(self) -> Dict[str, int]:
        store = self.interpreter.vars.items.get("ending_event_seen")
        if not isinstance(store, dict):
            store = {}
            self.interpreter.vars.items["ending_event_seen"] = store
        return store

    def _get_ending_list(self) -> List[Dict]:
        """Get list of available endings.
        Returns all defined endings with their current status.
        """
        result: List[Dict] = []
        v = self.interpreter.vars

        for ending_id, defn in self._ENDING_DEFINITIONS.items():
            flag_key = defn["flag_key"]
            check_value = defn["check_value"]

            # Determine current progress
            if flag_key == 2815:
                current = int(v.flags.get(flag_key, 0))
            else:
                current = int(v.globals.get(flag_key, 0))

            # Determine if ending is achievable
            achieved = False
            if ending_id == "N":
                achieved = current == 99 and self._get_total_day_count() >= 500
            elif ending_id == "1":
                achieved = current >= 10
            elif ending_id == "2":
                hero_idx = int(v.globals.get(2803, 0))
                achieved = hero_idx > 0
            elif ending_id in ("3", "4", "5"):
                achieved = int(v.flags.get(flag_key, 0)) >= 1
            elif ending_id == "7_princess":
                achieved = current >= 1200
            elif ending_id == "7_witch":
                achieved = current >= 2200
            elif ending_id == "11_tsundere":
                achieved = current >= 900
            elif ending_id == "14_ninja":
                achieved = 900 <= current < 1500
            elif ending_id == "14_dairy":
                achieved = current >= 2000
            elif ending_id == "10_godness":
                achieved = current >= 1900
            else:
                achieved = current >= check_value

            result.append({
                "id": ending_id,
                "name": defn["name"],
                "description": defn["description"],
                "achieved": achieved,
                "current_progress": current,
            })

        return result

    def _get_equip_name(self, equip_id: int) -> str:
        """Get equipment name by ID.
        equip_id is the base identification number (0-20 for rings, 40-52 for weapons).
        """
        if equip_id in self._EQUIP_WEAPON_NAMES:
            return self._EQUIP_WEAPON_NAMES[equip_id]
        if equip_id in self._EQUIP_RING_NAMES:
            return self._EQUIP_RING_NAMES[equip_id]
        return f"未知装备({equip_id})"

    def _get_equip_stats(self, target: Character) -> Dict[str, int]:
        """Get total equipment stats for a character.
        Corresponds to ERB @EQUIP_CHECK and @EQUIP_POWERUP.
        """
        total: Dict[str, Any] = {
            "damage": 0,
            "miss": 0,
            "spirit_recover": 0,
            "combo": 0,
            "def_dmg": 0,
            "spirit_dmg": 0,
            "cursed": False,
            "poison": False,
            "fire": False,
            "ice": False,
            "thunder": False,
            "effect_strength": {},
        }

        # Process all three equipment slots
        for slot_flag in (550, 551, 552):
            equip_code = int(target.cflag.get(slot_flag, -1))
            if equip_code < 0:
                continue

            is_weapon = (slot_flag == 550)
            stats = self._compute_equip_stats(equip_code, is_weapon, target)

            total["damage"] += stats.get("damage", 0)
            total["miss"] += stats.get("miss", 0)
            total["spirit_recover"] += stats.get("spirit_recover", 0)
            total["combo"] += stats.get("combo", 0)
            if stats.get("def_dmg", 100) != 100:
                total["def_dmg"] = max(total.get("def_dmg", 0), stats["def_dmg"]) if total.get("def_dmg") else stats["def_dmg"]
            if stats.get("spirit_dmg", 100) != 100:
                total["spirit_dmg"] = max(total.get("spirit_dmg", 0), stats["spirit_dmg"]) if total.get("spirit_dmg") else stats["spirit_dmg"]
            if stats.get("cursed", False):
                total["cursed"] = True
            if stats.get("poison", False):
                total["poison"] = True
            if stats.get("fire", False):
                total["fire"] = True
            if stats.get("ice", False):
                total["ice"] = True
            if stats.get("thunder", False):
                total["thunder"] = True

            # Track effect strengths for rings
            effect = stats.get("effect", 0)
            strength = stats.get("strength", 0)
            if effect > 0:
                total["effect_strength"][effect] = total["effect_strength"].get(effect, 0) + strength

        return total

    def _get_equipment_enhance_options(self, max_affordable: int) -> List[int]:
        options = [0, 1, 2, 4, 6, 8]
        if max_affordable not in options:
            options.append(max_affordable)
        return sorted(set(value for value in options if 0 <= value <= max_affordable))

    def _get_equipment_ring_name(self, equip_code: int) -> str:
        item_id = self._get_ring_item_id_from_code(equip_code)
        name = self._get_item_name(item_id)
        _, enhance, _ = self._decode_equipment_code(equip_code)
        return f"{name}+{enhance}" if enhance > 0 else name

    def _get_equipment_slot_name(self, slot_flag: int) -> str:
        return {
            550: "武器",
            551: "装饰A",
            552: "装饰B",
        }.get(slot_flag, f"装备槽{slot_flag}")

    def _get_equipment_weapon_name(self, equip_code: int) -> str:
        prefix_names = {
            1: "巨型",
            2: "剧毒",
            3: "致命",
            4: "强击",
            5: "烈火",
            6: "寒冰",
            7: "雷霆",
            8: "魔导",
            9: "暗黑",
        }
        item_id = self._get_weapon_item_id_from_code(equip_code)
        base_name = self._get_item_name(item_id)
        _, enhance, prefix = self._decode_equipment_code(equip_code)
        label = f"{prefix_names.get(prefix, '')}{base_name}"
        if enhance > 0:
            label += f"+{enhance}"
        return label

    def _get_ex_kojo_num(self, char_idx: int) -> int:
        """获取EX_TALENT口上编号"""
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return 0
        target = self.interpreter.vars.chars[char_idx]
        result = 0
        for idx in range(101, 201):
            if self._get_character_ex_talent(target, idx):
                result = idx + 900
        return result

    def _get_exhibition_pleasure_upgrade_costs(self, target: Character, level: int) -> Dict[int, int]:
        cost = {0: 100, 1: 1000, 2: 5000, 3: 15000, 4: 35000}.get(level, 0)
        cost = self._scale_perverse_cost(target, cost)
        cost = self._scale_exhibitionist_cost(target, cost)
        exp_key = 2 if level < 2 else 11
        return {8: cost, exp_key: 1}

    def _get_exp_level(self, value: int) -> int:
        return self._get_threshold_level(value, self.exp_level_thresholds)

    def _get_eye_color_name(self, target) -> str:
        """获取瞳色名称 (TALENT:306)"""
        v = int(target.talent.get(306, 0))
        return self._EYE_COLOR_NAMES.get(v, "ERROR")

    def _get_eye_shape_name(self, target) -> str:
        """获取眼形名称 (TALENT:305)"""
        v = int(target.talent.get(305, 0))
        return self._EYE_SHAPE_NAMES.get(v, "ERROR")

    def _get_flag_bit(self, flag_idx: int, bit: int) -> bool:
        value = self.interpreter.vars.get_flag(flag_idx, 0)
        return bool(value & (1 << bit))

    def _get_floor_monster_ids(self, floor: int) -> List[int]:
        if floor == 10:
            return list(range(190, 200))
        if floor < 1 or floor > 9:
            return []
        start = 100 + (floor - 1) * 10
        return list(range(start, start + 10))

    def _get_floor_monster_lines(self, floor: int) -> List[str]:
        stock = self._get_monster_stock()
        lines: List[str] = []
        for monster_id in self._get_floor_monster_ids(floor):
            count = max(0, int(stock.get(monster_id, 0)))
            if count <= 0:
                continue
            lines.append(f" {count:>3}只 {self._get_item_name(monster_id)}")
        if not lines:
            return [" 当前没有配置在这一阶层的怪物库存。"]
        return lines

    def _get_floor_party_counts(self, floor: int) -> tuple[int, int]:
        invasion = 0
        interception = 0
        for _, char in self._get_standard_dungeon_party_candidates():
            if int(char.cflag.get(501, 1)) != floor:
                continue
            if char.cflag.get(1, 0) == 2:
                invasion += 1
            elif char.cflag.get(1, 0) == 3:
                interception += 1
        return invasion, interception

    def _get_floor_status_lines(self, floor: int) -> List[str]:
        floor = max(1, min(9, floor))
        room_id = self._get_dungeon_floor_room(floor)
        invasion, interception = self._get_floor_party_counts(floor)
        lines: List[str] = [
            f"【第{floor}阶层】",
            f" 设施: {self._get_dungeon_room_name(room_id)}",
            f" 勇者队伍: {invasion} 人",
            f" 迎击队伍: {interception} 人",
            "",
            " 怪物配置:",
        ]
        lines.extend(self._get_floor_monster_lines(floor))
        return lines

    def _get_forced_semen_fetish_threshold(self, target: Character) -> int:
        threshold = 50
        if int(target.talent.get(13, 0)) != 0:
            threshold += 4
        if int(target.talent.get(24, 0)) != 0:
            threshold += 4
        if int(target.talent.get(25, 0)) != 0:
            threshold -= 2
        if int(target.talent.get(26, 0)) != 0:
            threshold += 2
        if int(target.talent.get(27, 0)) != 0:
            threshold += 5
        if int(target.talent.get(32, 0)) != 0:
            threshold += 4
        if int(target.talent.get(33, 0)) != 0:
            threshold -= 2
        if int(target.talent.get(61, 0)) != 0:
            threshold -= 2
        if int(target.talent.get(62, 0)) != 0:
            threshold += 2
        if int(target.talent.get(70, 0)) != 0:
            threshold -= 2
        if int(target.talent.get(71, 0)) != 0:
            threshold += 4
        if int(target.talent.get(72, 0)) != 0:
            threshold -= 5
        if int(target.talent.get(80, 0)) != 0:
            threshold -= 2
        if int(target.talent.get(76, 0)) != 0:
            threshold -= 20
        return threshold

    def _get_game_state_handler(self, state: str):
        handlers = {
            "TITLE": self.run_title,
            "SHOP": self.run_shop,
            "TRAIN": self.run_train,
            "LOAD": self.run_load_game,
            "EXIT": lambda: "EXIT",
        }
        return handlers.get(state)

    def _get_general_ending_branch_events(self) -> List[tuple[int, str, str, str, str, int, int]]:
        return [
            self._build_general_ending_branch_event(2805, "ending_maou_branch_love", "玛奥恋慕线", "解放我的女人哦！来吧！", "据说还有个姐姐？", 10, 3),
            self._build_general_ending_branch_event(2805, "ending_maou_branch_corruption", "玛奥淫乱线", "鬼畜村妹！我喜欢！", "我要等莉莉！", 20, 3),
            self._build_general_ending_branch_event(2806, "ending_lily_branch_love", "莉莉恋慕线", "巨乳我喜欢！来吧！", "土里土气，才不要！", 10, 3),
            self._build_general_ending_branch_event(2806, "ending_lily_branch_corruption", "莉莉淫乱线", "让村姑领教终极的快乐吧！", "不是我的菜！", 20, 3),
            self._build_general_ending_branch_event(2808, "ending_joan_branch_love", "琼恋慕线", "精灵妹子大好！", "才不要尖耳朵的！", 10, 0),
            self._build_general_ending_branch_event(2808, "ending_joan_branch_corruption", "琼淫乱线", "精灵妹子大好！", "才不要尖耳朵的！", 20, 0),
            self._build_general_ending_branch_event(2809, "ending_princess32_branch_love", "普林希斯恋慕线", "我就是驯龙高手！", "会喷火的妹子，怕怕！", 10, 0),
            self._build_general_ending_branch_event(2809, "ending_princess32_branch_corruption", "普林希斯淫乱线", "我就要当龙骑士！", "会喷火的妹子，怕怕！", 20, 0),
            self._build_general_ending_branch_event(2810, "ending_godness_branch_love", "嘉德恋慕线", "病娇大好！", "病娇怕怕！", 10, 0),
            self._build_general_ending_branch_event(2810, "ending_godness_branch_corruption", "嘉德淫乱线", "来一场天地间的爱恋！", "这么难调教，才不要！", 110, 0),
            self._build_general_ending_branch_event(2811, "ending_square_branch_love", "黑方片恋慕线", "肌肉女，实战利器！", "比我还壮，才不要！", 10, 0),
            self._build_general_ending_branch_event(2811, "ending_square_branch_corruption", "黑方片淫乱线", "肌肉女，实战利器！", "比我还壮，才不要！", 110, 0),
            self._build_general_ending_branch_event(2812, "ending_club_branch_love", "白梅花恋慕线", "扶你！扶我！扶她灵！", "无法忍受带把的！", 10, 0),
            self._build_general_ending_branch_event(2812, "ending_club_branch_corruption", "白梅花淫乱线", "扶你！扶我！扶她灵！", "无法忍受带把的！", 20, 0),
            self._build_general_ending_branch_event(2813, "ending_heart_branch_love", "金红桃恋慕线", "金发巨乳好！", "狂王二手货，才不要！", 10, 0),
            self._build_general_ending_branch_event(2813, "ending_heart_branch_corruption", "金红桃淫乱线", "金发巨乳好！", "狂王二手货，才不要！", 20, 0),
            self._build_general_ending_branch_event(2814, "ending_spade_branch_love", "银黑桃恋慕线", "女忍！爽！", "整天鬼鬼祟祟的妹子，才不要！", 10, 0),
            self._build_general_ending_branch_event(2814, "ending_spade_branch_corruption", "银黑桃淫乱线", "女忍！爽！", "整天鬼鬼祟祟的妹子，才不要！", 110, 0),
        ]

    def _get_global_level(self, key: int) -> int:
        return int(self.interpreter.vars.globals.get(key, 0))

    def _get_guard_status_lines(self) -> List[str]:
        guards = [
            (idx, char)
            for idx, char in enumerate(self.interpreter.vars.chars)
            if idx > 0 and char.base.get(0, 0) > 0 and char.cflag.get(1, 0) == 3
        ]
        lines = ["【近卫兵 / 迎击状态】"]
        if not guards:
            lines.append(" 当前没有处于迎击状态的角色。")
            return lines
        for idx, char in guards:
            lines.append(f" [{idx}] {char.name} - {self._summarize_dungeon_party(char)}")
        return lines

    def _get_habit_name(self, target) -> str:
        """获取癖好名称 (TALENT:313)"""
        v = int(target.talent.get(313, 0))
        return self._HABIT_NAMES.get(v, "ERROR")

    def _get_hand_service_dirty_score(self, player: Optional[Character], target: Character) -> int:
        if player is None:
            return 0

        score = 7 if target.equipt.get(89, 0) > 0 else 0
        if score == 0:
            penis_stain = player.stain.get(2, 0)
            if penis_stain & 1:
                score += 1
            if penis_stain & 4:
                score += 3
            if penis_stain & 8:
                score += 7
            if penis_stain & 16:
                score += 1
            if player.stain.get(4, 0) & 32:
                score += 3

        if target.talent.get(61, 0):
            score //= 3
        if target.talent.get(62, 0):
            score *= 2
        return score // 3

    def _get_hero_reason_name(self, target) -> str:
        """获取成为勇者的契机名称 (TALENT:316)"""
        v = int(target.talent.get(316, 0))
        return self._HERO_REASON_NAMES.get(v, "ERROR")

    def _get_job_name_for_char(self, char_idx: int) -> str:
        """获取角色职业名称的辅助方法

        Args:
            char_idx: 角色索引

        Returns:
            职业名称字符串
        """
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return "??????"
        char = self.interpreter.vars.chars[char_idx]
        # 职业相关素质 ID 200-229
        for talent_id in range(200, 230):
            if char.talent.get(talent_id, 0):
                return self._get_talent_name(talent_id)
        return "??????"

    def _get_juel(self, idx: int) -> int:
        return int(self.interpreter.vars.juel.get(idx, 0))

    def _get_knowledge_item_ids(self) -> List[int]:
        return [38, 39, 42, 52, 54, 56]

    def _get_last_training_target_index(self) -> int:
        return int(self.interpreter.vars.items.get("_last_training_target", 0))

    def _get_lesbian_pleasure_upgrade_paths(self, target: Character, level: int) -> List[Dict[str, Any]]:
        path_defs = {
            0: [
                {"label": "欲情+百合经验路线", "costs": {5: 200, 40: 50}},
                {"label": "快C+百合经验路线", "costs": {0: 1000, 40: 50}},
            ],
            1: [
                {"label": "欲情+百合经验路线", "costs": {5: 1000, 40: 200}},
                {"label": "快C+百合经验路线", "costs": {0: 5000, 40: 200}},
            ],
            2: [
                {"label": "欲情+屈服+百合经验路线", "costs": {5: 3000, 6: 1000, 40: 500}},
            ],
            3: [
                {"label": "欲情+屈服+百合经验路线", "costs": {5: 8000, 6: 2000, 40: 1000}},
            ],
            4: [
                {"label": "欲情+屈服+百合经验路线", "costs": {5: 20000, 6: 5000, 40: 2000}},
            ],
        }
        paths = []
        for path in path_defs.get(level, []):
            scaled_costs: Dict[int, int] = {}
            for resource_id, amount in path["costs"].items():
                scaled = amount
                if resource_id in {0, 5, 6, 40}:
                    scaled = self._scale_lesbian_cost(target, scaled)
                    scaled = self._scale_perverse_cost(target, scaled)
                    scaled = self._scale_line_crossing_cost(target, scaled, level)
                scaled_costs[resource_id] = scaled
            paths.append({"label": path["label"], "costs": scaled_costs})
        return paths

    def _get_level_up_required_exp(self, idx: int, char: Character) -> int:
        level = int(char.cflag.get(9, 0))
        base_requirement = level * 10 + 10
        if idx == 0:
            return base_requirement * 10
        if char.talent.get(220, 0):
            return (base_requirement - 10) * 2 + 10
        return base_requirement

    def _get_like_base_name(self, target) -> str:
        """获取喜欢的东西名称 (TALENT:317)"""
        v = int(target.talent.get(317, 0))
        return self._LIKE_BASE_NAMES.get(v, "")

    def _get_lip_name(self, target) -> str:
        """获取唇形名称 (TALENT:307)"""
        v = int(target.talent.get(307, 0))
        return self._LIP_NAMES.get(v, "ERROR")

    def _get_long_goodbye_bond_score(self, sold_identity: int, witness: Character) -> int:
        score = 0
        for flag_id in range(21, 26):
            relation_value = int(witness.cflag.get(flag_id, 0))
            if relation_value % 100 == sold_identity:
                score += 80
                if relation_value // 100 < 2:
                    score += 40
        return score

    def _get_love_corruption_swap_reset_rules(self) -> Dict[int, Dict[str, Any]]:
        return {
            22: {
                "global_flag": 2811,
                "love_reset_range": (100, 200),
                "love_reset_to": 10,
                "corruption_ranges": [(30, 100), (300, 310)],
                "corruption_reset_to": 110,
                "cflag_reset": 515,
            },
            21: {
                "global_flag": 2814,
                "love_reset_range": (110, 200),
                "love_reset_to": 30,
                "corruption_ranges": [(30, 100)],
                "corruption_reset_to": 110,
                "cflag_reset": 515,
            },
            33: {
                "global_flag": 2810,
                "love_reset_range": (110, 200),
                "love_reset_to": 10,
                "corruption_ranges": [(30, 100), (300, 310)],
                "corruption_reset_to": 110,
                "cflag_reset": 515,
            },
            35: {
                "global_flag": 2807,
                "love_reset_range": (130, 10**9),
                "love_reset_to": 30,
                "corruption_ranges": [(30, 130)],
                "corruption_reset_to": 130,
                "cflag_reset": 515,
            },
        }

    def _get_love_preferences(self, target) -> List[str]:
        """Calculate and return love preferences list.
        Corresponds to ERB @LOOK_INFO_LOVE.
        """
        main_love: Dict[int, int] = {i: 0 for i in range(100)}
        love_pool: Dict[int, int] = {i: 0 for i in range(100)}

        # 初始值
        main_love[0] = 15

        # 种族补正
        race = int(target.talent.get(314, 0))
        if race in (1, 6):  # 精灵・天使
            main_love[2] += 1
            main_love[21] -= 1
            main_love[22] -= 1
            main_love[40] += 1
            main_love[42] += 1
            main_love[61] -= 1
        elif race in (3, 4):  # 吸血鬼・无头骑士
            main_love[2] -= 1
            main_love[21] += 1
            main_love[22] += 1
            main_love[40] -= 1
            main_love[42] -= 1
        elif race == 2:  # 狼人
            main_love[2] -= 1
            main_love[40] += 1
            main_love[42] += 1
            main_love[41] += 1
            main_love[60] += 1
            main_love[61] += 1

        # 元の職業补正
        past = int(target.talent.get(315, 0))
        if past in (2, 12):  # 修女・圣女
            main_love[2] += 3
            main_love[20] -= 1
            main_love[21] -= 1
            main_love[22] -= 1
            main_love[30] += 1
        elif past == 5:  # 妓女
            main_love[21] += 2
            main_love[22] += 2
        elif past == 6:  # 小偷
            main_love[2] -= 2
            main_love[30] -= 1
        elif past in (7, 9):  # 乞丐・贫民
            main_love[2] += 1
        elif past == 8:  # 贵族
            main_love[21] -= 1
            main_love[22] -= 1
            main_love[50] += 1
        elif past == 11:  # 巫女
            main_love[21] -= 2
        elif past == 21:  # 主妇
            main_love[21] += 1
            main_love[22] -= 1
            main_love[40] += 2

        # 理由补正
        reason = int(target.talent.get(316, 0))
        if reason in (2, 11):
            main_love[2] -= 1
            main_love[22] += 1
        elif reason in (16, 17):
            main_love[2] += 3
            main_love[30] += 1

        # 喜欢的东西补正
        like = int(target.talent.get(317, 0))
        if like == 4:
            main_love[42] += 3
        elif like == 5:
            main_love[2] -= 1
            main_love[22] += 1
        elif like == 8 and int(target.talent.get(157, 0)):  # 家族+人妻
            main_love[40] += 3
        elif like == 8 and int(target.talent.get(140, 0)):  # 家族+恋母情结
            main_love[51] += 3
        elif like == 8 and int(target.talent.get(141, 0)):  # 家族+恋父情结
            main_love[52] += 3
        elif like in (9, 10):
            main_love[2] += 1
        elif like == 12:
            main_love[60] += 1
            main_love[61] += 1

        # 陷落度
        cflag0 = int(target.cflag.get(0, 0))
        if cflag0 == 1:  # 售出可
            main_love[1] += 1
            main_love[2] -= 1
            main_love[50] += 1
        elif cflag0 == 2:  # 助手可
            main_love[1] += 2
            main_love[2] -= 2
            main_love[50] += 2
        else:
            main_love[1] -= 1
            main_love[2] += 1
            main_love[50] -= 1

        # 素质补正
        if int(target.talent.get(85, 0)):  # 淫乱
            main_love[1] -= 1
            main_love[2] -= 5
            main_love[50] += 5
        if int(target.talent.get(86, 0)):  # 爱慕
            main_love[1] += 10
            main_love[2] -= 5
        if int(target.talent.get(0, 0)):  # 处女
            main_love[11] -= 60
        if int(target.talent.get(1, 0)):  # 童贞
            main_love[4] -= 1
            main_love[20] += 1
        if int(target.talent.get(9, 0)):  # 崩坏
            main_love[1] -= 3
            main_love[2] -= 60
            main_love[20] += 3
            main_love[21] += 3
            main_love[22] += 3
            main_love[31] += 3
            main_love[35] += 3
            main_love[40] += 3
            main_love[42] += 3
            main_love[41] += 3
            main_love[50] += 3
            main_love[60] += 1
            main_love[61] += 1
        if int(target.talent.get(23, 0)):  # 好奇心
            main_love[50] += 1
        if int(target.talent.get(24, 0)):  # 保守的
            main_love[22] -= 1
            main_love[50] -= 1
        if int(target.talent.get(30, 0)):  # 看重贞操
            main_love[21] -= 1
            main_love[22] -= 1
            main_love[50] -= 1
        if int(target.talent.get(31, 0)):  # 看轻贞操
            main_love[21] += 1
            main_love[22] += 1
            main_love[50] += 1
        if int(target.talent.get(35, 0)):  # 害羞
            main_love[35] += 1
        if int(target.talent.get(36, 0)):  # 不知羞耻
            main_love[35] -= 1
        if int(target.talent.get(40, 0)):  # 害怕疼痛
            main_love[33] += 1
        if int(target.talent.get(47, 0)):  # 喜欢精液
            main_love[31] += 10
        if int(target.talent.get(57, 0)):  # 漏尿癖
            main_love[35] += 1
        if int(target.talent.get(60, 0)):  # 容易自慰
            main_love[20] += 1
        if int(target.talent.get(74, 0)):  # 自慰狂
            main_love[10] += 3
            main_love[20] += 3
        if int(target.talent.get(75, 0)):  # 性爱狂
            main_love[11] += 3
            main_love[21] += 3
        if int(target.talent.get(77, 0)):  # 尻穴狂
            main_love[12] += 3
            main_love[20] += 1
            main_love[21] += 1
        if int(target.talent.get(78, 0)):  # 弄乳狂
            main_love[13] += 3
            main_love[20] += 3
        if int(target.talent.get(80, 0)):  # 倒错的
            main_love[32] += 1
            main_love[33] += 1
            main_love[34] += 1
            main_love[35] += 1
            main_love[50] += 1
            main_love[60] += 1
            main_love[61] += 1
        if int(target.talent.get(81, 0)):  # 双性恋
            main_love[32] += 1
        if int(target.talent.get(83, 0)):  # 施虐狂
            main_love[34] += 10
        if int(target.talent.get(88, 0)):  # 受虐狂
            main_love[33] += 10
        if int(target.talent.get(89, 0)):  # 露出狂
            main_love[35] += 10
        if int(target.talent.get(101, 0)):  # C钝感
            main_love[10] -= 1
        if int(target.talent.get(102, 0)):  # C敏感
            main_love[10] += 1
        if int(target.talent.get(103, 0)):  # V钝感
            main_love[11] -= 1
        if int(target.talent.get(104, 0)):  # V敏感
            main_love[11] += 1
        if int(target.talent.get(105, 0)):  # A钝感
            main_love[12] -= 1
        if int(target.talent.get(106, 0)):  # A敏感
            main_love[12] += 1
        if int(target.talent.get(107, 0)):  # B钝感
            main_love[13] -= 1
        if int(target.talent.get(108, 0)):  # B敏感
            main_love[13] += 1
        if int(target.talent.get(121, 0)) or int(target.talent.get(122, 0)):  # 扶她・男人
            main_love[4] += 1
        if int(target.talent.get(124, 0)):  # 动物耳朵
            main_love[60] += 3
            main_love[61] += 3
        if int(target.talent.get(130, 0)):  # 喷乳体质
            main_love[13] += 1
        if int(target.talent.get(133, 0)):  # 早泄
            main_love[4] -= 1
        if int(target.talent.get(140, 0)):  # 恋母情结
            main_love[51] += 10
        if int(target.talent.get(141, 0)):  # 恋父情结
            main_love[52] += 10
        if int(target.talent.get(142, 0)):  # 萝莉控
            main_love[53] += 10
        if int(target.talent.get(143, 0)):  # 正太控
            main_love[54] += 10
        if int(target.talent.get(150, 0)):  # 从不自慰
            main_love[20] -= 60
        if int(target.talent.get(151, 0)):  # 绝不侍奉
            main_love[30] -= 60
        if int(target.talent.get(157, 0)):  # 人妻
            main_love[40] += 3
        if int(target.talent.get(180, 0)):  # 妓女
            main_love[22] += 1
        if int(target.talent.get(181, 0)):  # 倾城
            main_love[22] += 2
        if int(target.talent.get(204, 0)):  # 肉便器
            main_love[2] -= 1
            main_love[21] += 1
            main_love[22] += 1
            main_love[40] -= 1
            main_love[42] -= 1
        if int(target.talent.get(230, 0)):  # 淫核
            main_love[10] += 3
        if int(target.talent.get(232, 0)):  # 淫壶
            main_love[11] += 3
        if int(target.talent.get(233, 0)):  # 淫肛
            main_love[12] += 3
        if int(target.talent.get(231, 0)):  # 淫乳
            main_love[13] += 3
        if int(target.talent.get(273, 0)):  # 私处封印
            main_love[11] -= 3

        # 能力补正
        main_love[10] += int(target.abl.get(0, 0))  # C感觉
        main_love[13] += int(target.abl.get(1, 0))  # B感觉
        main_love[11] += int(target.abl.get(2, 0))  # V感觉
        main_love[12] += int(target.abl.get(3, 0))  # A感觉

        if int(target.talent.get(86, 0)) and not int(target.talent.get(285, 0)):  # 爱慕+非狂王俘虏
            main_love[1] += int(target.abl.get(10, 0)) * 3  # 顺从
        if int(target.talent.get(85, 0)):  # 淫乱
            main_love[50] += int(target.abl.get(11, 0)) * 3  # 欲望

        if int(target.abl.get(13, 0)):  # 侍奉技术
            main_love[30] += int(target.abl.get(13, 0)) + int(target.abl.get(12, 0))
        if int(target.abl.get(14, 0)):  # 性交技术
            main_love[21] += int(target.abl.get(14, 0)) + int(target.abl.get(12, 0))

        main_love[30] += int(target.abl.get(16, 0))  # 侍奉精神
        main_love[35] += int(target.abl.get(17, 0))  # 露出癖
        main_love[34] += int(target.abl.get(20, 0))  # 抖S气质
        main_love[33] += int(target.abl.get(21, 0))  # 抖M气质
        main_love[32] += int(target.abl.get(22, 0))  # 百合气质
        main_love[32] += int(target.abl.get(23, 0))  # BL气质
        main_love[21] += int(target.abl.get(30, 0)) * 3  # 性交中毒
        main_love[20] += int(target.abl.get(31, 0)) * 3  # 自慰中毒
        main_love[31] += int(target.abl.get(32, 0)) * 3  # 精液中毒
        main_love[32] += int(target.abl.get(33, 0)) * 3  # 百合中毒
        main_love[22] += int(target.abl.get(37, 0)) * 3  # 卖淫中毒
        main_love[61] += int(target.abl.get(39, 0)) * 3  # 兽奸中毒

        # 经验补正
        exp_val = int(target.exp.get(78, 0))  # 精饮绝顶经验
        if exp_val > 100:
            main_love[31] += 3
        elif exp_val > 30:
            main_love[31] += 2
        elif exp_val > 0:
            main_love[31] += 1

        exp_val = int(target.exp.get(40, 0))  # 侍奉快乐经验
        if exp_val > 100:
            main_love[30] += 3
        elif exp_val > 30:
            main_love[30] += 2
        elif exp_val > 0:
            main_love[30] += 1

        exp_val = int(target.exp.get(50, 0))  # 爱情经验
        if exp_val > 100:
            main_love[1] += 3
        elif exp_val > 30:
            main_love[1] += 2
        elif exp_val > 0:
            main_love[1] += 1

        exp_val = int(target.exp.get(42, 0))  # 被虐快乐经验
        if exp_val > 100:
            main_love[33] += 3
        elif exp_val > 30:
            main_love[33] += 2
        elif exp_val > 0:
            main_love[33] += 1

        exp_val = int(target.exp.get(3, 0))  # 肛门快乐经验
        if exp_val > 200:
            main_love[12] += 3
        elif exp_val > 80:
            main_love[12] += 2
        elif exp_val > 0:
            main_love[12] += 1

        exp_val = int(target.exp.get(43, 0))  # 施虐快乐经验
        if exp_val > 100:
            main_love[34] += 3
        elif exp_val > 30:
            main_love[34] += 2
        elif exp_val > 0:
            main_love[34] += 1

        exp_val = int(target.exp.get(55, 0))  # 营业爱情经验
        if exp_val > 100:
            main_love[22] += 3
        elif exp_val > 30:
            main_love[22] += 2
        elif exp_val > 0:
            main_love[22] += 1

        # 新丈夫/恋人补正
        main_love[41] += int(target.cflag.get(602, 0)) // 3
        main_love[42] += int(target.cflag.get(607, 0)) // 3

        # 刻印补正
        main_love[50] += int(target.mark.get(0, 0)) * 3  # 快乐刻印
        main_love[1] -= int(target.mark.get(2, 0)) * 5  # 反抗刻印

        # 相互作用
        if main_love[51]:
            love_pool[51] += main_love[50]
        if main_love[52]:
            love_pool[52] += main_love[50]
        if main_love[53]:
            love_pool[53] += main_love[50]
        if main_love[54]:
            love_pool[54] += main_love[50]

        if int(target.talent.get(317, 0)) == 12:  # 可爱的动物
            love_pool[0] += main_love[60] // 3
            love_pool[0] += main_love[61] // 3
        love_pool[60] += main_love[61] // 2
        love_pool[40] -= main_love[41] // 3

        for lid in range(100):
            main_love[lid] += love_pool[lid]

        # 排序取前30
        love_sort: List[int] = []
        current_max = max(main_love.values()) if main_love else 0
        safety = 0
        while len(love_sort) < 30 and safety < 100:
            next_max = -9999
            for lid in range(100):
                if main_love[lid] == current_max:
                    love_sort.append(lid)
                elif main_love[lid] < current_max and main_love[lid] > next_max:
                    next_max = main_love[lid]
            current_max = next_max
            safety += 1

        # 生成显示列表
        _LOVE_NAMES = {
            1: "魔王大人", 2: "拯救万民", 3: "肉棒", 4: "勃起",
            10: "被弄阴蒂", 11: "被弄小穴", 12: "被弄菊穴", 13: "被弄乳房",
            20: "手淫", 21: "做爱", 22: "卖淫", 30: "侍奉", 31: "精液",
            33: "被人虐待", 34: "虐待别人", 35: "露出身体",
            40: "丈夫", 41: "现在的丈夫",
        }

        result: List[str] = []
        for lid in love_sort[:30]:
            if main_love[lid] <= 3:
                continue
            if lid == 0:
                like_name = self._get_like_base_name(target)
                if not like_name:
                    continue
                name = like_name
            elif lid == 32:
                name = "断背行为" if int(target.talent.get(122, 0)) else "百合行为"
            elif lid == 42:
                lover = int(target.cflag.get(606, 0))
                if lover == 0:
                    name = "将来的老公"
                elif lover == 200:
                    name = "恋人"
                else:
                    name = "恋人"
            elif lid == 50:
                continue  # 不显示
            elif lid == 51:
                name = "人妻" if main_love[50] > 6 else "妈妈"
            elif lid == 52:
                name = "中年大叔" if main_love[50] > 6 else "爸爸"
            elif lid == 53:
                name = "萝莉的小穴" if main_love[50] > 6 else "小女孩"
            elif lid == 54:
                name = "正太的阴茎" if main_love[50] > 6 else "美少年"
            elif lid == 60:
                name = "野狗大人" if main_love[50] > 6 else "狗"
            elif lid == 61:
                name = "和野兽交配" if main_love[50] > 6 else "可爱的东西"
            elif lid == 62:
                name = "狂王大人"
            elif lid in _LOVE_NAMES:
                name = _LOVE_NAMES[lid]
            else:
                continue

            # 金红桃
            hearts = (main_love[lid] // 5) - 1
            if hearts > 6:
                hearts = 6
            if hearts > 0:
                name += "♡" * hearts
            result.append(name)

        return result

    def _get_main_menu_panel_mode(self) -> int:
        mode = int(self.interpreter.vars.get_flag(36, 0))
        return mode if mode in (0, 1, 4, 5) else 0

    def _get_main_menu_panel_title(self) -> str:
        return {
            0: "物品/技能",
            1: "持有陷阱",
            4: "地城概况",
            5: "地城日常",
        }.get(self._get_main_menu_panel_mode(), "物品/技能")

    def _get_mark_name(self, mark_id: int) -> str:
        if int(mark_id) == 3:
            return "反抗刻印"
        return f"刻印{int(mark_id)}"

    def _get_masochism_pleasure_upgrade_paths(self, target: Character, level: int) -> List[Dict[str, Any]]:
        if level <= 2:
            path_defs = [
                {"label": "苦痛+欲情路线", "costs": {9: {0: 100, 1: 500, 2: 1200}[level], 5: {0: 100, 1: 500, 2: 1000}[level]}},
                {"label": "苦痛+屈服路线", "costs": {9: {0: 100, 1: 500, 2: 1500}[level], 6: {0: 100, 1: 300, 2: 1000}[level], 2: 1}},
            ]
        else:
            path_defs = [
                {"label": "苦痛+欲情路线", "costs": {30: {3: 10, 4: 50}[level]}},
                {"label": "苦痛+屈服路线", "costs": {9: {3: 3000, 4: 5000}[level], 6: {3: 6000, 4: 12000}[level], 30: {3: 10, 4: 50}[level], 2: 1}},
            ]
        paths = []
        for idx, path in enumerate(path_defs):
            scaled_costs: Dict[int, int] = {}
            for resource_id, amount in path["costs"].items():
                scaled = amount
                if resource_id in {5, 6, 9, 30}:
                    scaled = self._scale_release_cost(target, scaled)
                    scaled = self._scale_perverse_cost(target, scaled)
                    scaled = self._scale_line_crossing_cost(target, scaled, level)
                scaled_costs[resource_id] = scaled
            paths.append({"label": path["label"], "costs": scaled_costs})
        return paths

    def _get_masturbation_fantasy_target(self, target: Character, assistant: Optional[Character], lesbian_occurred: int) -> Tuple[str, int]:
        """获取自慰妄想对象 - 返回 (对象名, 类型: 0=主人 1=助手 2=兽)"""
        import random
        v = self.interpreter.vars
        player = self._get_player()

        if (int(target.talent.get(85, 0)) == 0 and lesbian_occurred == 1 and
                assistant is not None and int(target.abl.get(22, 0)) > random.randint(0, 4)):
            return getattr(assistant, 'savestr', "助手"), 1
        if (int(target.talent.get(85, 0)) == 0 and int(target.abl.get(39, 0)) > random.randint(0, 4) and
                int(v.get_item(22, 0)) > 0):
            return "兽交", 2
        return (getattr(player, 'callname', "主人") if player else "主人"), 0

    def _get_max_buyable_quantity(self, item_id: int, owner: Character, price: int) -> int:
        current_count = self._get_item_count(owner, item_id)
        stock_limit = self._get_item_stock_limit(item_id)
        max_affordable = self.interpreter.vars.money // max(1, price)
        max_buyable = min(stock_limit - current_count, max_affordable)
        if item_id == 55:
            player = self._get_player()
            max_trap_level = int(player.cflag.get(9, 0)) if player is not None else 0
            current_trap_level = int(self.interpreter.vars.get_flag(85, 0))
            max_buyable = min(max_buyable, max(0, max_trap_level - current_trap_level))
        return max(0, max_buyable)

    def _get_max_charanum(self) -> int:
        return 100

    def _get_meat_toilet_seed_name(self, seed_type: int) -> str:
        seed_names = {
            0: "怪物",
            1: "俘虏的中年",
            2: "俘虏的少年",
            3: "扶她淫魔",
        }
        return seed_names.get(seed_type, "怪物")

    def _get_medal_count(self) -> int:
        player = self._get_player()
        if player is None:
            return 0
        return max(0, int(player.exp.get(81, 0)))

    def _get_mod_switch_entries(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "label": "魔界银行"},
            {"id": 1, "label": "铁石心肠"},
            {"id": 2, "label": "打工系统"},
        ]

    def _get_mod_switch_status_text(self) -> str:
        parts = []
        for entry in self._get_mod_switch_entries():
            enabled = self._get_flag_bit(9000, int(entry["id"]))
            short_name = str(entry["label"]).replace("系统", "").replace("心肠", "心")
            parts.append(f"[{short_name}]{'ON' if enabled else 'OFF'}")
        return " ".join(parts)

    def _get_morning_fellatio_kojo_lines(self, char: Character) -> List[str]:
        kojo_num = self._get_kojo_num(char)
        lines = {
            100: ["「啊啊…早上就这么精神…额呵呵、早上好、主人～♪」"],
            101: ["「咕啾……嘞噜嘞噜…啊、变大了呢、早上好❤ 嘞噜…啾～啾噗～❤」"],
            105: ["「唔呣……早上好……唔呣❤ …魔王大人的肉棒……今天也是元气满满的呢❤」"],
            112: ["「早上好。啊啊、生理现象……就交给我吧♪」"],
            119: ["「嗯啾……呼……哈啊……主人的肉棒……诶嘿……一早上就……嗯……很精神呢……❤」"],
        }
        return lines.get(kojo_num, [])

    def _get_morning_fellatio_score(self, char: Character) -> int:
        score = int(char.abl.get(32, 0))
        if char.talent.get(61, 0):
            score += 1
        if char.talent.get(62, 0):
            score -= 1
        if char.talent.get(63, 0):
            score += 1
        if char.talent.get(76, 0):
            score += 1
        if char.talent.get(85, 0):
            score += 1
        return score

    def _get_night_stalking_score(self, char: Character) -> int:
        score = int(char.abl.get(30, 0))
        if char.talent.get(33, 0):
            score += 1
        if char.talent.get(20, 0):
            score -= 2
        if char.talent.get(70, 0):
            score += 1
        if char.talent.get(71, 0):
            score -= 1
        if char.talent.get(75, 0) and not char.talent.get(0, 0) and char.abl.get(2, 0) >= char.abl.get(3, 0):
            score += 1
        if char.talent.get(77, 0) and (char.talent.get(0, 0) or char.abl.get(3, 0) > char.abl.get(2, 0)):
            score += 1
        if char.talent.get(76, 0) and char.talent.get(0, 0):
            score += 1
        return score

    def _get_nipple_name(self, target) -> str:
        """获取乳头名称 (TALENT:309)"""
        v = int(target.talent.get(309, 0))
        return self._NIPPLE_NAMES.get(v, "ERROR")

    def _get_owned_catalog_item_ids(self, item_ids: List[int]) -> List[int]:
        player = self._get_player()
        if player is None:
            return []
        return [item_id for item_id in item_ids if self._get_item_count(player, item_id) > 0]

    def _get_palam_level(self, value: int) -> int:
        """获取PALAM等级"""
        PALAMLV = [0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000, 500000, 1000000, 5000000, 10000000]
        for i, threshold in enumerate(PALAMLV):
            if value < threshold:
                return max(0, i - 1)
        return len(PALAMLV) - 1

    def _get_part_time_job_name(self, flag_id: int) -> str:
        return {
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
        }.get(flag_id, "打工")

    def _get_past_life_name(self, target) -> str:
        """获取成为勇者前的生活名称 (TALENT:315)"""
        v = int(target.talent.get(315, 0))
        return self._PAST_LIFE_NAMES.get(v, "ERROR")

    def _get_pending_post_message_actions(self) -> List[Dict[str, Any]]:
        pending = self.interpreter.vars.items.get("pending_post_message_actions")
        if not isinstance(pending, list):
            pending = []
            self.interpreter.vars.items["pending_post_message_actions"] = pending
        return pending

    def _get_player(self) -> Optional[Character]:
        if self.interpreter.vars.chars:
            return self.interpreter.vars.chars[0]
        return None

    def _get_pleasure_a_upgrade_costs(self, target: Character, level: int) -> Dict[int, int]:
        juel_cost = {0: 1, 1: 50, 2: 600, 3: 7000, 4: 45000}.get(level, 0)
        exp_cost = {0: 2, 1: 10, 2: 30, 3: 150, 4: 300}.get(level, 0)
        if level == 1 and target.exp.get(1, 0) >= 3:
            juel_cost = 20
        elif level == 2 and target.exp.get(1, 0) >= 4:
            juel_cost = 100
        elif level == 3 and target.exp.get(1, 0) >= 5:
            juel_cost = 500
        elif level == 4 and target.exp.get(1, 0) >= 5:
            juel_cost = 8000
        juel_cost = self._scale_line_crossing_cost(target, juel_cost, level)
        exp_cost = self._scale_line_crossing_cost(target, exp_cost, level)
        return {2: juel_cost, 1: exp_cost}

    def _get_pleasure_f_upgrade_costs(self, target: Character, level: int) -> Dict[int, int]:
        costs = {
            0: {15: 1},
            1: {15: 50},
            2: {15: 600},
            3: {15: self._scale_line_crossing_cost(target, 7000, level)},
            4: {15: self._scale_line_crossing_cost(target, 45000, level)},
        }
        return dict(costs.get(level, {}))

    def _get_prestige_value(self) -> int:
        return max(0, min(100, int(self.interpreter.vars.get_flag(99, 0))))

    def _get_ptj_info(self, target: Character) -> Dict[str, Any]:
        """获取角色打工信息"""
        ptj_count = 0
        highest_pos = 0
        highest_level = 0
        ex_cflag = getattr(target, 'ex_cflag', {})
        for pos in range(400, 410):
            val = int(ex_cflag.get(pos, 0))
            if val % 10 > 0:
                ptj_count += 1
                if val % 10 > highest_level:
                    highest_level = val % 10
                    highest_pos = pos
        name = self._get_ptj_name(highest_pos) if highest_pos > 0 else ""
        return {
            "count": ptj_count,
            "highest_pos": highest_pos,
            "highest_level": highest_level,
            "name": name,
        }

    def _get_ptj_name(self, ptj_pos: int) -> str:
        """获取打工名称"""
        return self._PTJ_NAMES.get(ptj_pos, "")

    def _get_pubic_hair_name(self, target) -> str:
        """获取阴毛状态名称 (TALENT:310/311)"""
        v = int(target.talent.get(310, 0))
        if v == 1:
            return "白虎"
        elif 2 <= v <= 20:
            return "胎毛"
        elif 21 <= v <= 50:
            return "新长的"
        elif 51 <= v <= 100:
            return "稀薄"
        elif 101 <= v <= 150:
            return "标准"
        elif 151 <= v <= 200:
            return "浓密"
        elif 201 <= v <= 500:
            return "硬毛"
        return "ERROR"

    def _get_purchase_catalog_item_mode(self, item_id: int) -> str:
        if item_id in self._get_use_now_ids():
            return "use_now"
        if item_id in self._get_knowledge_item_ids():
            return "knowledge"
        return "plural"

    def _get_race2_name(self, target) -> str:
        """获取种族2名称 (TALENT:319)"""
        v = int(target.talent.get(319, 0))
        return self._RACE2_NAMES.get(v, f"种族2({v})")

    def _get_random_monster_id(self) -> int:
        stock = self._get_monster_stock()
        total_monsters = self._get_monster_count()
        while True:
            monster_id = 100 + random.randint(0, 8) * 10 + random.randint(0, 4)
            if stock.get(monster_id, 0) >= 999 and total_monsters < 44955:
                continue
            return monster_id

    def _get_reincarnation_block_reason(self, target: Character, candidate: Dict[str, Any]) -> Optional[str]:
        if not self._is_labo_target_controlled(target):
            return f"{target.name} 还不在你的统治之下。"
        level = self._get_character_level(target)
        required_level = int(candidate["required_level"])
        if level < required_level:
            return f"{target.name} 必须达到 Lv{required_level}（当前 Lv{level}）。"
        missing_names = [self._get_reincarnation_required_talent_names(int(candidate["group_id"]))[idx] for idx, talent_id in enumerate(candidate["required_talents"]) if talent_id in candidate["missing_talents"]]
        if missing_names:
            return f"{target.name} 还需要具备：" + "、".join(missing_names)
        if target.talent.get(322, 0) == int(candidate["monster_id"]):
            return f"{target.name} 已经是 {candidate['name']} 了。"
        return None

    def _get_reincarnation_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        return next((group for group in self._get_reincarnation_groups() if int(group["group_id"]) == group_id), None)

    def _get_reincarnation_groups(self) -> List[Dict[str, Any]]:
        return [
            {"group_id": 0, "monster_ids": [133, 143, 153, 163, 160, 170], "required_level": 0, "required_talents": []},
            {"group_id": 1, "monster_ids": [104, 113, 114, 172, 181], "required_level": 0, "required_talents": [244]},
            {"group_id": 2, "monster_ids": [110, 130, 121, 150], "required_level": 0, "required_talents": [99]},
            {"group_id": 3, "monster_ids": [101, 111, 123, 134, 164, 171], "required_level": 0, "required_talents": []},
            {"group_id": 4, "monster_ids": [100, 120], "required_level": 0, "required_talents": []},
            {"group_id": 5, "monster_ids": [102, 131, 142, 173, 184], "required_level": 0, "required_talents": []},
            {"group_id": 6, "monster_ids": [122, 141, 151, 162, 183], "required_level": 0, "required_talents": []},
            {"group_id": 7, "monster_ids": [103, 124, 174], "required_level": 0, "required_talents": []},
            {"group_id": 8, "monster_ids": [112, 144], "required_level": 0, "required_talents": []},
            {"group_id": 9, "monster_ids": [132, 140, 180], "required_level": 0, "required_talents": [244, 247, 245, 246]},
            {"group_id": 10, "monster_ids": [154, 152, 182], "required_level": 0, "required_talents": [244, 247, 245, 246, 76]},
        ]

    def _get_reincarnation_required_talent_names(self, group_id: int) -> List[str]:
        names = {
            76: "淫乱",
            99: "魁梧",
            244: "恶魔肌肤",
            245: "恶魔翅膀",
            246: "恶魔尾巴",
            247: "恶魔眼睛",
        }
        group = self._get_reincarnation_group(group_id)
        if group is None:
            return []
        return [names.get(talent_id, f"素质{talent_id}") for talent_id in group["required_talents"]]

    def _get_resistance_mark_reduction_cost(self, target: Character) -> int:
        resistance_level = int(target.mark.get(3, 0))
        cost = {1: 5000, 2: 10000, 3: 50000}.get(resistance_level, 0)
        if target.talent.get(12, 0):
            cost = cost * 3
        if target.talent.get(16, 0):
            cost = cost * 150 // 100
        if target.talent.get(13, 0):
            cost = cost * 50 // 100
        if target.talent.get(85, 0):
            cost = cost * 50 // 100
        return int(cost)

    def _get_resistance_mark_reduction_reasons(self, target: Character) -> List[str]:
        resistance_level = int(target.mark.get(3, 0))
        if resistance_level <= 0:
            return ["不存在反抗行为"]
        reasons: List[str] = []
        surrender_mark = int(target.mark.get(2, 0))
        required_submission = resistance_level + 2
        cost = self._get_resistance_mark_reduction_cost(target)
        if surrender_mark < resistance_level:
            reasons.append(f"屈服刻印不足({surrender_mark}/{resistance_level})")
        if int(target.abl.get(10, 0)) < required_submission:
            reasons.append(f"顺从不足({target.abl.get(10, 0)}/{required_submission})")
        if self._get_juel(6) < cost:
            reasons.append(f"屈服珠不足({self._get_juel(6)}/{cost})")
        return reasons

    def _get_ring_effect_strength(self, char: Character, effect_id: int) -> int:
        total = 0
        for slot_id in (551, 552):
            equip_code = int(char.cflag.get(slot_id, -1))
            if equip_code < 0:
                continue
            base_code, enhance, _ = self._decode_equipment_code(equip_code)
            if base_code == effect_id:
                total += enhance
        return total

    def _get_ring_item_id_from_code(self, equip_code: int) -> int:
        base_code, _, _ = self._decode_equipment_code(equip_code)
        return 300 + max(0, base_code)

    def _get_running_cost_amount(self) -> int:
        total_days = self._get_total_day_count()
        cost = self._get_running_cost_base_amount(total_days)
        cost += self._get_running_cost_flag_amount()

        player = self._get_player()
        if player is not None:
            cost = self._apply_running_cost_player_adjustments(cost, player)

        difficulty = int(self.interpreter.vars.get_flag(5, 0))
        char_count = len(self.interpreter.vars.chars)
        cost = self._apply_running_cost_difficulty_adjustments(cost, difficulty, total_days, char_count)
        return max(0, cost)

    def _get_running_cost_base_amount(self, total_days: int) -> int:
        cost = 500
        if total_days > 31:
            cost += 1000
        if total_days > 51:
            cost += 2000
        return cost

    def _get_running_cost_flag_amount(self) -> int:
        flag48 = int(self.interpreter.vars.get_flag(48, 0))
        amount = 0
        if flag48 & 1:
            amount += 500
        if flag48 & 2:
            amount += 100
        if flag48 & 4:
            amount += 1000
        if flag48 & 32:
            amount += 500
        if flag48 & 8:
            amount += 1800
        if flag48 & 16:
            amount += 100
        if flag48 & 64:
            amount += int(self.interpreter.vars.get_flag(40, 0)) * 500
        return amount

    def _get_save_slot_path(self, choice: str) -> str:
        slot = self._parse_choice_int(choice)
        if slot is None:
            raise ValueError(choice)
        return self.paths.save_slot_path(slot)

    def _get_self_call(self, target: Character) -> str:
        """Get character's self-reference (e.g. 私, 僕, 俺).
        Returns CSTR:60 if set, otherwise '我'.
        Corresponds to ERB @SELF_CALL.
        """
        return str(target.cstr.get(60, "")).strip() or "我"

    def _get_self_call_first(self, target: Character) -> str:
        """Get the first character of a character's self-reference.
        Corresponds to ERB @SELF_CALL_FIRST.
        """
        s = self._get_self_call(target)
        return s[0] if s else "我"

    def _get_service_pleasure_upgrade_paths(self, target: Character, level: int) -> List[Dict[str, Any]]:
        path_defs = {
            0: [
                {"label": "屈服珠路线", "costs": {6: 100, 2: 1, 20: 1}},
                {"label": "恭顺珠路线", "costs": {4: 20, 21: 1}},
                {"label": "习得珠路线", "costs": {7: 100, 2: 1}},
            ],
            1: [
                {"label": "屈服珠路线", "costs": {6: 1200, 2: 3, 20: 3}},
                {"label": "恭顺珠路线", "costs": {4: 100, 21: 1}},
            ],
            2: [
                {"label": "屈服珠路线", "costs": {6: 5000, 2: 6, 20: 6}},
                {"label": "恭顺珠路线", "costs": {4: 600, 21: 20}},
            ],
            3: [
                {"label": "屈服珠路线", "costs": {6: 10000, 2: 10, 20: 10}},
                {"label": "恭顺珠路线", "costs": {4: 2000, 21: 20}},
            ],
            4: [
                {"label": "屈服珠路线", "costs": {6: 30000, 2: 20, 20: 20}},
                {"label": "恭顺珠路线", "costs": {4: 8000, 21: 100}},
            ],
        }
        paths = []
        for path in path_defs.get(level, []):
            scaled_costs: Dict[int, int] = {}
            for resource_id, amount in path["costs"].items():
                scaled = amount
                if resource_id in {4, 6}:
                    scaled = self._scale_perverse_cost(target, scaled)
                    scaled = self._scale_line_crossing_cost(target, scaled, level)
                scaled_costs[resource_id] = scaled
            paths.append({"label": path["label"], "costs": scaled_costs})
        return paths

    def _get_shadow_servant_lifetime(self, char: Character) -> int:
        lifetime = int(char.cflag.get(820, 0))
        if lifetime > 0:
            return lifetime
        return 666666 if char.talent.get(292, 0) else 0

    def _get_single_equip_stats(self, equip_code: int, is_weapon: bool, target: Character) -> List[str]:
        """Get display lines for a single equipment's stats.
        Corresponds to ERB @EQUIP_ST_SHOW.
        """
        lines: List[str] = []
        stats = self._compute_equip_stats(equip_code, is_weapon, target)

        if not stats:
            return lines

        if stats.get("cursed", False):
            lines.append("*带有诅咒")
        if stats.get("poison", False):
            lines.append("*带有毒液")
        if stats.get("fire", False):
            lines.append("*带火")
        if stats.get("ice", False):
            lines.append("*带寒冰")
        if stats.get("thunder", False):
            lines.append("*带电")

        if is_weapon:
            if stats.get("damage", 0):
                lines.append(f"*{stats['damage']}的打击力")
            if stats.get("miss", 0):
                lines.append(f"*{stats['miss']}％概率打偏")
            if stats.get("spirit_recover", 0) > 0:
                lines.append(f"*恢复{stats['spirit_recover']}气力")
            if stats.get("spirit_recover", 0) < 0:
                lines.append(f"*消费{abs(stats['spirit_recover'])}气力")
            if stats.get("combo", 0):
                lines.append(f"*{stats['combo']}％概率二连击")
            if stats.get("def_dmg", 100) != 100:
                lines.append(f"*打击防御{stats['def_dmg']}％")
            if stats.get("spirit_dmg", 100) != 100:
                lines.append(f"*打击气力{stats['spirit_dmg']}％")
        else:
            effect = stats.get("effect", 0)
            if effect > 0:
                effect_name = self._EQUIP_EFFECT_NAMES.get(effect, "未知")
                strength = stats.get("strength", 0)
                lines.append(f"*效果：{effect_name}(强度{strength})")

        return lines

    def _get_skin_color_name(self, target: Character) -> str:
        if target.talent.get(255, 0):
            return "白皙"
        if target.talent.get(253, 0):
            return "褐色肌肤"
        if target.talent.get(244, 0):
            return "恶魔肌肤"
        return "普通肌肤"

    def _get_spawned_hero_role_label(self, hero: Character) -> str:
        if hero.talent.get(122, 0):
            return "冒险者"
        return "勇者"

    def _get_state_desc(self, target) -> str:
        """Get current state description.
        Covers race, past life, hero reason, pregnancy, money, and love preferences.
        """
        parts: List[str] = []

        # 种族
        race_name = self._get_race_name(target)
        if race_name and race_name != "ERROR":
            race_str = f"[种族：{race_name}"
            # 精英有种族2
            if int(target.talent.get(220, 0)):
                race2_name = self._get_race2_name(target)
                if race2_name:
                    race_str += f"·{race2_name}"
            # 魔族化
            if int(target.talent.get(314, 0)) == 9:
                cur_race = int(target.talent.get(320, 0))
                if 100 <= cur_race <= 220:
                    race_str += f"：{self._get_cloth_name(cur_race)}"
                orig_race = int(target.talent.get(321, 0))
                if orig_race == 9:
                    race_str += " [原种族：不明]"
                elif orig_race > 0:
                    orig_name = self._RACE_NAMES.get(orig_race, "")
                    if orig_name:
                        race_str += f" [原种族：{orig_name}]"
            race_str += "]"
            parts.append(race_str)

        # 发色与头发状态
        hair_color = int(target.talent.get(300, 0))
        hair_state = int(target.talent.get(301, 0))
        if hair_color and hair_state:
            parts.append(f"[发色：{self._get_hair_color_name(target)}]"
                         f"[头发状态：{self._get_hair_state_name(target)}]")

        # 头发长度・修剪・发型
        hair_length = int(target.talent.get(302, 0))
        hair_cut = int(target.talent.get(303, 0))
        hair_style = int(target.talent.get(304, 0))
        if hair_length and hair_cut and hair_style:
            parts.append(f"[头发长度：{self._get_hair_length_name(target)}]"
                         f"[修剪：{self._get_hair_cut_name(target)}]"
                         f"[发型：{self._get_hair_style_name(target)}]")

        # 眼形・瞳色・唇
        face_desc = self._get_face_desc(target)
        if face_desc:
            parts.append(face_desc)

        # 体型・乳头・阴毛
        body_desc = self._get_body_desc(target)
        if body_desc:
            parts.append(body_desc)

        # 魅力点・癖好
        charm = int(target.talent.get(312, 0))
        habit = int(target.talent.get(313, 0))
        if charm and habit:
            parts.append(f"[魅力点：{self._get_charm_point_name(target)}]"
                         f"[癖好：{self._get_habit_name(target)}]")

        # 成为勇者前的生活
        past_life = int(target.talent.get(315, 0))
        if past_life:
            no_target = int(target.cflag.get(0, 0))  # character number
            template_id = target.template_id
            if template_id is not None and template_id >= 200 and template_id != 222:
                parts.append(f"[来到据点之前：{self._get_past_life_name(target)}]")
            elif int(target.talent.get(220, 0)) == 1:
                parts.append(f"[出生是因为：{self._get_past_life_name(target)}]")
            elif target is not self._get_player() and not int(target.talent.get(122, 0)):
                parts.append(f"[成为勇者之前：{self._get_past_life_name(target)}]")
            elif target is not self._get_player():
                parts.append(f"[成为冒险者之前：{self._get_past_life_name(target)}]")
            else:
                parts.append(f"[成为魔王之前：{self._get_past_life_name(target)}]")

        # 成为勇者的契机
        hero_reason = int(target.talent.get(316, 0))
        if hero_reason:
            template_id = target.template_id
            if template_id is not None and template_id >= 200 and template_id != 222:
                parts.append(f"[回应召唤的理由：{self._get_hero_reason_name(target)}]")
            elif int(target.talent.get(220, 0)) == 1:
                parts.append(f"[选择留下的理由：{self._get_hero_reason_name(target)}]")
            elif target is not self._get_player() and not int(target.talent.get(122, 0)):
                parts.append(f"[成为勇者的契机：{self._get_hero_reason_name(target)}]")
            elif target is not self._get_player():
                parts.append(f"[成为冒险者的契机：{self._get_hero_reason_name(target)}]")
            else:
                parts.append(f"[成为魔王的契机：{self._get_hero_reason_name(target)}]")

        # 妊娠适性
        if int(target.talent.get(158, 0)):
            parts.append("[妊娠适性：只能异种族]")

        # 所持金
        money = int(target.cflag.get(580, 0))
        if money <= 0:
            parts.append("[所持金：身无分文]")
        else:
            parts.append(f"[所持金：{money}]")

        # 借金
        debt = int(target.cflag.get(582, 0))
        if debt < 0:
            parts.append(f"[借金：{0 - debt}]")

        # 信仰
        has_faith = (int(target.talent.get(242, 0)) or int(target.talent.get(250, 0))
                     or int(target.talent.get(315, 0)) == 11
                     or int(target.talent.get(315, 0)) == 12)
        faith_val = int(target.cflag.get(152, 0))
        if has_faith and faith_val >= 10 and target is not self._get_player():
            faith_name = ""
            if int(target.talent.get(85, 0)):
                faith_name = "魔王大人♡♡♡"
            elif int(target.cflag.get(0, 0)) != 0:
                faith_name = "无名的淫荡女神♡♡♡"
            elif int(target.talent.get(220, 0)):
                faith_name = "混沌的魔界女神"
            elif int(target.talent.get(250, 0)):
                faith_name = "潜藏地底的死亡女神"
            elif int(target.talent.get(242, 0)):
                faith_name = "纯洁的神圣女神"
            elif int(target.talent.get(315, 0)) == 11:
                faith_name = "丰饶的大地女神"
            elif int(target.talent.get(315, 0)) == 12:
                faith_name = "包容一切的大海女神"
            if faith_name:
                parts.append(f"[信仰：{faith_name}（信仰値：{faith_val}）]")

        return "\n".join(parts)

    def _get_submission_level(self, char: Optional[Character]) -> int:
        if char is None:
            return 0
        return char.abl.get(10, 0)

    def _get_talent_name(self, talent_id: int) -> str:
        return self.talent_catalog.get(talent_id, f"素质{talent_id}")

    def _get_target(self) -> Optional[Character]:
        target_idx = self.interpreter.vars.target
        if 0 <= target_idx < len(self.interpreter.vars.chars):
            return self.interpreter.vars.chars[target_idx]
        return None

    def _get_tattoo_slot_name(self, slot_id: int) -> str:
        return {
            10: "脸",
            11: "胸",
            12: "背",
            13: "下腹",
            14: "屁股",
            15: "性器",
            16: "肛门",
            17: "大腿",
        }.get(slot_id, f"部位{slot_id}")

    def _get_threshold_level(self, value: int, thresholds: List[int], max_level: int = 5) -> int:
        upper_bound = min(max_level, len(thresholds) - 1)
        for level in range(1, upper_bound + 1):
            if value < thresholds[level]:
                return level - 1
        return upper_bound

    def _get_total_day_count(self) -> int:
        year, month, day = self.interpreter.vars.day[:3]
        year = max(1, int(year))
        month = max(1, min(12, int(month)))
        day = max(1, int(day))
        elapsed_years = year - 1
        elapsed_month_days = sum(self._get_calendar_month_length(m) for m in range(1, month))
        return max(1, elapsed_years * 365 + elapsed_month_days + day)

    def _get_train_command_3_score(self, target: Character, player: Optional[Character]) -> int:
        score = self._get_common_order_score(target, player)
        score += target.abl.get(11, 0) * 3
        score += target.abl.get(17, 0) * 4
        score += target.abl.get(31, 0) * 3
        score += target.mark.get(1, 0) * 3
        score += self._get_palam_level(target.palam.get(5, 0)) * 3
        if target.talent.get(20, 0):
            score -= 5
        if target.talent.get(35, 0):
            score -= 5
        if target.talent.get(36, 0):
            score += 2
        if target.talent.get(60, 0):
            score += 5
        if target.talent.get(70, 0):
            score += 5
        if target.talent.get(71, 0):
            score -= 5
        if target.talent.get(89, 0):
            score += 10
        if target.equipt.get(21, 0):
            score += 8
        return score

    def _get_train_command_3_threshold(self, target: Character) -> int:
        threshold = 33
        if target.equipt.get(53, 0):
            threshold += 10
        if target.equipt.get(18, 0):
            threshold += 3
        if target.equipt.get(11, 0):
            threshold += 5
        if target.equipt.get(13, 0):
            threshold += 5
        return threshold

    def _get_train_command_name(self, command_id: int) -> str:
        return self.train_commands.get(command_id, f"Command {command_id}")

    def _get_train_command_penetrator_count(self, assistant: Character) -> int:
        penetrator_count = 0
        player = self._get_player()
        if player is not None and (player.talent.get(121, 0) or player.talent.get(122, 0)):
            penetrator_count += 1
        if assistant.talent.get(121, 0) or assistant.talent.get(122, 0):
            penetrator_count += 1
        return penetrator_count

    def _get_train_menu_target(self) -> Optional[Character]:
        if self.interpreter.vars.target >= 0 and self.interpreter.vars.chars:
            return self.interpreter.vars.chars[self.interpreter.vars.target]
        print("No target selected!")
        return None

    def _get_underwear_resale_income(self, target: Character) -> int:
        if int(target.cflag.get(43, -1)) < 0 or int(target.cflag.get(48, 0)) < 6:
            return 0
        amount = 50 * int(target.cflag.get(48, 0))
        if target.talent.get(74, 0):
            amount = int(amount * 1.5)
        if target.talent.get(92, 0):
            amount = int(amount * 2.0)
        if target.talent.get(126, 0):
            amount = int(amount * 1.5)
        return amount

    def _get_use_now_ids(self) -> List[int]:
        return [29, 30, 31, 33, 40, 41]

    def _get_weapon_item_id_from_code(self, equip_code: int) -> int:
        base_code, _, _ = self._decode_equipment_code(equip_code)
        return 300 + max(40, base_code)
