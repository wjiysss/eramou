from __future__ import annotations
"""Module for CharaExtMixin - Character extension methods (body, custom, make, hair, look)"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CharaExtMixin:
    """Mixin providing Character extension methods (body, custom, make, hair, look)"""
    def _func_chara_and_hair(self, target: Character) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        ID_OF_GENERAL_CHARASTERISTICS = [160, 161, 162, 163, 164, 166, 172, 173, 174, 175]
        personality_names = {
            160: "慈爱", 161: "自信家", 162: "懦弱", 163: "高贵",
            164: "冷静", 166: "恶女", 172: "智慧", 173: "庇护者",
            174: "贵公子", 175: "伶俐"
        }

        current_personality = None
        for tid in ID_OF_GENERAL_CHARASTERISTICS:
            if target.talent.get(tid, 0):
                current_personality = tid
                break
        result["personality_id"] = current_personality
        result["personality_name"] = personality_names.get(current_personality, "") if current_personality else ""

        new_personality = self._set_random_characteristic(target, ID_OF_GENERAL_CHARASTERISTICS)
        result["new_personality_id"] = new_personality
        result["new_personality_name"] = personality_names.get(new_personality, "") if new_personality is not None else ""

        hair_color = self._generate_hair_color(target)
        result["hair_color"] = hair_color

        hair_style = self._generate_hair_style(target)
        result["hair_style"] = hair_style

        return result


    def _generate_hair_style(self, target: Character) -> str:
        ARR_HAIR_STYLE = [
            "", "自然", "中分", "不均分", "长束发", "马尾",
            "侧马尾", "垂发辫", "双马尾", "顶束发", "侧束发",
            "鱼骨辫", "卷发"
        ]
        style_idx = random.randint(1, len(ARR_HAIR_STYLE) - 1)
        return ARR_HAIR_STYLE[style_idx]


    def _generate_hair_color(self, target: Character) -> str:
        ARR_HAIRCOLOR = [
            "", "金发", "栗发", "黑发", "红发", "银发",
            "蓝发", "绿发", "紫发", "白发", "暗金发", "粉发"
        ]

        roll = random.randint(0, 99)
        if roll == 0:
            color_id = 11
        elif 1 <= roll <= 20:
            color_id = 1
        elif 21 <= roll <= 30:
            color_id = 6
        elif 31 <= roll <= 40:
            color_id = 7
        elif 41 <= roll <= 60:
            color_id = 2
        elif 61 <= roll <= 80:
            color_id = 3
        elif 81 <= roll <= 97:
            color_id = 4
        else:
            color_id = 5

        target.talent[300] = color_id
        return ARR_HAIRCOLOR[color_id]


    def _look_character(self, target: Character) -> List[str]:
        """Display character appearance based on LOOK.ERB logic."""
        lines: List[str] = []
        name = target.name or "角色"

        # Hair color
        hair_color_id = target.talent.get(300, 0)
        hair_color = self._HAIR_COLOR_MAP.get(hair_color_id, "未知")

        # Hair style
        hair_style_id = target.talent.get(301, 0)
        hair_style = self._HAIR_STYLE_MAP.get(hair_style_id, "未知")

        # Hair length
        hair_length_val = target.talent.get(302, 0)
        if hair_length_val >= 1 and hair_length_val <= 100:
            hair_length = "短发"
        elif hair_length_val >= 101 and hair_length_val <= 200:
            hair_length = "中长发"
        elif hair_length_val > 200:
            hair_length = "长发"
        else:
            hair_length = "未设定"

        # Eye type
        eye_type_id = target.talent.get(305, 0)
        eye_type = self._EYE_TYPE_MAP.get(eye_type_id, "普通")

        # Eye color
        eye_color_id = target.talent.get(306, 0)
        eye_color = self._EYE_COLOR_MAP.get(eye_color_id, "未知")

        # Lip
        lip_id = target.talent.get(307, 0)
        lip = self._LIP_MAP.get(lip_id, "普通的")

        lines.append(f"【{name}的外观】")
        lines.append(f"发色：{hair_color}　发型：{hair_style}　长度：{hair_length}")
        lines.append(f"眼型：{eye_type}　瞳色：{eye_color}　嘴唇：{lip}")

        # Clothing state (CFLAG:40 based)
        cloth_state = target.cflag.get(40, 0)
        cloth_type = target.cflag.get(41, 0)
        if cloth_type == 0 and target.cflag.get(42, 0) == 0:
            lines.append("着衣：全裸")
        else:
            parts: List[str] = []
            if cloth_state & 1:
                parts.append("内裤")
            if cloth_state & 2:
                parts.append("胸罩")
            if cloth_state & 4:
                parts.append("上衣")
            if cloth_state & 8:
                parts.append("裙子")
            if cloth_state & 16:
                parts.append("裤子")
            if cloth_state & 64:
                parts.append("特别服装")
            if parts:
                lines.append(f"着衣：{'、'.join(parts)}")
            else:
                lines.append("着衣：全裸")

        # Body features
        if target.talent.get(0, 0):
            lines.append("特征：处女")
        if target.talent.get(109, 0):
            lines.append("特征：巨乳")
        elif target.talent.get(116, 0):
            lines.append("特征：绝壁")
        elif target.talent.get(132, 0):
            lines.append("特征：贫乳")
        if target.talent.get(135, 0):
            lines.append("特征：男孩子气")
        if target.talent.get(122, 0):
            lines.append("特征：男性")

        return lines

    # ------------------------------------------------------------------
    # LOVERS (恋人系统)
    # ------------------------------------------------------------------

    _LOVER_NAME_MAP: Dict[int, str] = {
        1: "温柔的青年", 2: "威严的彪形大汉", 3: "粗野的流氓",
        4: "大腹便便的中年人", 21: "丑陋的兽人", 22: "精灵美男子",
        23: "暗黑精灵", 24: "奴隶", 41: "妓女", 42: "女学生",
        43: "贵妇", 44: "女骑士", 61: "懦弱少年", 62: "戴眼镜的男学生",
        63: "活泼的少年", 64: "可爱的男学生", 81: "大型宠物狗",
        82: "爱马", 83: "宠物猪", 84: "农家的牛", 200: "恋人",
    }


    def _chara_first_exp(self, target: Character, exp_type: int) -> List[str]:
        """First experience processing based on CHARA_FIRST_EXP.ERB.

        exp_type: 0=first_kiss, 1=first_sex
        """
        lines: List[str] = []
        name = target.name or "她"

        # CFLAG:16 = first kiss partner, CFLAG:15 = first sex partner
        # CSTR:4 = first kiss description, CSTR:3 = first sex description

        if exp_type == 0:  # First kiss
            first_kiss = target.cflag.get(16, -1)
            if first_kiss == -1:
                # Not yet set - determine based on experience
                kiss_exp = target.exp.get(5, 0)  # 性交经验
                if kiss_exp > 0:
                    lines.append(f"{name}的初吻对象尚未设定。")
                    # Check family settings (TALENT:320)
                    family = target.talent.get(320, 0)
                    family_flag = family % 10
                    if family_flag == 1 and random.randint(0, 19) == 0:
                        lines.append(f"也许是和亲人……")
                    target.cflag[16] = 0
                else:
                    lines.append(f"{name}还没有经历过初吻。")
            elif first_kiss == 0:
                lines.append(f"{name}的初吻对象不明。")
            else:
                desc = target.cstr.get(4, "")
                if desc:
                    lines.append(f"{name}的初吻是和{desc}。")
                else:
                    lines.append(f"{name}的初吻对象编号：{first_kiss}")

        elif exp_type == 1:  # First sex
            first_sex = target.cflag.get(15, -1)
            is_virgin = target.talent.get(0, 0)  # TALENT:0 = 处女
            is_male = target.talent.get(122, 0)  # TALENT:122 = 男性

            if is_virgin and not is_male:
                lines.append(f"{name}还是处女。")
            elif first_sex == -1:
                if not is_virgin and not is_male:
                    # Non-virgin but no record
                    lines.append(f"{name}的初次经验对象不明。")
                    target.cflag[15] = 0
                else:
                    lines.append(f"{name}还没有性经验。")
            elif first_sex == 0:
                lines.append(f"{name}的初次经验对象不明。")
            else:
                desc = target.cstr.get(3, "")
                if desc:
                    lines.append(f"{name}的初次是和{desc}。")
                else:
                    lines.append(f"{name}的初次经验对象编号：{first_sex}")

        return lines

    # ------------------------------------------------------------------
    # EXCOM (扩展指令)
    # ------------------------------------------------------------------

    _EX_TALENT_NAMES: Dict[int, str] = {
        0: "灵魂错位", 1: "近卫", 2: "后代", 3: "魔王替身", 4: "狂王替身",
        101: "琼", 102: "普林希斯", 103: "嘉德", 104: "菲娅",
        200: "魔王", 801: "无双", 901: "一人军团", 902: "魔女",
        903: "魔界公主", 904: "天神",
    }


    def _chara_body2(self, target: Character) -> List[str]:
        """Extended body description based on CHARA_BODY2.ERB.

        Generates height, weight, and bust measurements using
        statistical data and talent modifiers.
        """
        lines: List[str] = []
        name = target.name or "她"

        # Age from CFLAG or talent
        age = int(target.cflag.get(451, 0))
        if age <= 0:
            age = 18

        is_male = int(target.talent.get(122, 0))
        is_futa = int(target.talent.get(121, 0))
        is_petite = int(target.talent.get(100, 0))  # 娇小
        is_tall = int(target.talent.get(99, 0))  # 魁梧

        # Base height/weight from statistics
        base_height = 109000  # 109.0cm * 1000
        base_weight = 17000   # 17.0kg * 1000

        # Simplified height/weight generation
        if is_male:
            height = 170000 + random.randint(-8000, 8000)
            weight = 62000 + random.randint(-8000, 8000)
        else:
            height = 158000 + random.randint(-7000, 7000)
            weight = 50000 + random.randint(-7000, 7000)

        # Talent modifiers
        if is_petite:
            height = int(height * 0.92)
            weight = int(weight * 0.88)
        elif is_tall:
            height = int(height * 1.08)
            weight = int(weight * 1.10)

        # Race modifiers (TALENT:314)
        race = int(target.talent.get(314, 0))
        if race == 1 or race == 7:  # 精灵
            height += int((height - base_height) * 3 // 20)
            weight += int((weight - base_weight) * 3 // 20)
        elif race == 5:  # 龙族
            height += int((height - base_height) // 4)
            weight += int((weight - base_weight) * 4 // 5)
        elif race == 10:  # 霍比特
            height -= int((height - base_height) * 15 // 20)
            weight -= int((weight - base_weight) * 12 // 20)
        elif race == 11:  # 矮人
            height -= int((height - base_height) * 9 // 20)
            weight -= int((weight - base_weight) * 7 // 20)

        # Body type modifiers
        if int(target.talent.get(248, 0)):  # 肌肉型
            weight = int(weight * 108 // 100)
            if is_male:
                weight = int(weight * 108 // 100)
        if int(target.talent.get(256, 0)):  # 虚弱
            weight = int(weight * 92 // 100)
        if int(target.talent.get(115, 0)):  # 肥胖
            weight = int(weight * 115 // 100)

        h_display = height / 1000
        w_display = weight / 1000
        lines.append(f"{name}的身高：{h_display:.1f}cm")
        lines.append(f"{name}的体重：{w_display:.1f}kg")

        # Bust generation (simplified)
        if not is_male:
            bust_diff = 12500  # Default B cup area
            if int(target.talent.get(116, 0)):  # 绝壁
                bust_diff = 5000 + random.randint(0, 25) * 100
            elif int(target.talent.get(109, 0)):  # 贫乳
                bust_diff = 10000 + random.randint(0, 25) * 100
            elif int(target.talent.get(110, 0)):  # 巨乳
                bust_diff = 20000 + random.randint(0, 30) * 100
            elif int(target.talent.get(114, 0)):  # 爆乳
                bust_diff = 25000 + random.randint(0, 30) * 100
            elif int(target.talent.get(119, 0)):  # 超乳
                bust_diff = 35000 + random.randint(0, 30) * 100

            # Under bust estimate
            under_bust = int(h_display * 0.43 * 100)
            bust = under_bust + bust_diff // 100

            cup_names = {0: "AAA", 2500: "AA", 5000: "A", 7500: "A+",
                         10000: "B", 12500: "C", 15000: "D", 17500: "E",
                         20000: "F", 22500: "G", 25000: "H", 27500: "I",
                         30000: "J", 32500: "K", 35000: "L", 37500: "M",
                         40000: "N"}
            cup = "B"
            for threshold, cup_name in sorted(cup_names.items()):
                if bust_diff >= threshold:
                    cup = cup_name

            lines.append(f"{name}的胸围：{bust} 下胸围：{under_bust} 罩杯：{cup}")
        else:
            lines.append(f"{name}的胸围：男性体型")

        return lines

    # ------------------------------------------------------------------
    # CHARA_CUSTOM2 (扩展角色自定义)
    # ------------------------------------------------------------------


    def _chara_custom2(self, target: Character) -> List[str]:
        """Extended character customization based on CHARA_CUSTOM2.ERB.

        Handles talent page display, talent deal processing,
        conflict checking, and character cost calculation.
        """
        lines: List[str] = []
        name = target.name or "她"

        # Calculate character cost
        cost = 500000  # Base price
        cost_modifiers = {
            10: 150000, 13: 150000, 14: 150000, 17: 150000,
            37: 150000, 41: 150000, 99: 150000, 125: 150000,
            131: 150000, 132: 150000, 134: 150000, 140: 150000,
            141: 150000, 142: 150000, 143: 150000,
            11: -50000, 12: -50000, 15: -50000, 16: -50000,
            84: -50000, 100: -50000, 133: -50000,
            20: -100000, 21: -100000, 22: -100000, 24: -100000,
            27: -100000, 32: -100000, 34: -100000, 43: -100000,
            51: -100000, 79: -100000, 82: -100000,
            23: 150000, 25: 150000, 28: 150000, 33: 150000,
            42: 150000, 50: 150000, 57: 150000,
            85: 600000, 86: 600000,
            119: 200000,
        }
        for tid, modifier in cost_modifiers.items():
            if int(target.talent.get(tid, 0)):
                cost += modifier

        # Combat talents cost
        for tid in range(240, 253):
            if int(target.talent.get(tid, 0)):
                cost += 200000

        # Pink hair bonus
        if int(target.talent.get(300, 0)) == 11:
            cost += 100000

        cost = max(cost, 0)
        lines.append(f"{name}的角色价值：{cost}")

        # Talent emptiness check
        has_kojo = False
        has_job = False
        for tid in range(160, 175):
            if int(target.talent.get(tid, 0)):
                has_kojo = True
                break
        for tid in range(200, 221):
            if int(target.talent.get(tid, 0)):
                has_job = True
                break

        missing = []
        if not has_kojo:
            missing.append("需要设定性格（口上）")
        if not has_job:
            missing.append("需要有职业设定")
        if not int(target.talent.get(300, 0)):
            missing.append("需要设定发色")
        if not int(target.talent.get(304, 0)):
            missing.append("需要设定发型")
        if not int(target.talent.get(306, 0)):
            missing.append("需要设定瞳色")

        if missing:
            for m in missing:
                lines.append(m)
            lines.append("请返回继续设定")
        else:
            lines.append("人物设定完成")

        return lines

    # ------------------------------------------------------------------
    # CHARA_CUSTOM3 (追加自定义)
    # ------------------------------------------------------------------


    def _chara_custom3(self, target: Character) -> List[str]:
        """Additional customization based on CHARA_CUSTOM3.ERB.

        Handles look pages (appearance details) and look deal processing.
        """
        lines: List[str] = []
        name = target.name or "她"

        # Hair color
        hair_color = int(target.talent.get(300, 0))
        hair_colors = {0: "未设定", 1: "黑", 2: "茶", 3: "金", 4: "赤",
                       5: "青", 6: "紫", 7: "银", 8: "桃", 9: "白",
                       10: "绿", 11: "粉"}
        lines.append(f"发色：{hair_colors.get(hair_color, '其他')}")

        # Hair style
        hair_style = int(target.talent.get(304, 0))
        lines.append(f"发型：#{hair_style}")

        # Hair length
        hair_length = int(target.talent.get(301, 0))
        if hair_length <= 100:
            length_str = "短"
        elif hair_length <= 200:
            length_str = "半长"
        else:
            length_str = "长"
        lines.append(f"头发长度：{length_str}")

        # Eye type
        eye_type = int(target.talent.get(305, 0))
        lines.append(f"眼型：#{eye_type}")

        # Pupil color
        pupil_color = int(target.talent.get(306, 0))
        lines.append(f"瞳色：#{pupil_color}")

        # Lip type
        lip_type = int(target.talent.get(307, 0))
        lines.append(f"唇型：#{lip_type}")

        # Body type
        body_type = int(target.talent.get(308, 0))
        if body_type <= 100:
            bt_str = "纤细"
        elif body_type <= 200:
            bt_str = "标准"
        else:
            bt_str = "丰满"
        lines.append(f"体型：{bt_str}")

        # Nipple type
        nipple = int(target.talent.get(309, 0))
        lines.append(f"乳头：#{nipple}")

        # Pubic hair
        pubic = int(target.talent.get(310, 0))
        if pubic <= 1:
            ph_str = "白虎"
        elif pubic <= 20:
            ph_str = "胎毛"
        elif pubic <= 50:
            ph_str = "稀薄"
        elif pubic <= 100:
            ph_str = "标准"
        elif pubic <= 150:
            ph_str = "浓密"
        else:
            ph_str = "硬毛"
        lines.append(f"阴毛状态：{ph_str}")

        # Charm point
        charm = int(target.talent.get(312, 0))
        lines.append(f"魅力点：#{charm}")

        # Habit
        habit = int(target.talent.get(313, 0))
        lines.append(f"癖好：#{habit}")

        # Previous life
        prev_life = int(target.talent.get(315, 0))
        lines.append(f"成为勇者前的生活：#{prev_life}")

        # Motivation
        motivation = int(target.talent.get(316, 0))
        lines.append(f"成为勇者的契机：#{motivation}")

        # Race
        race = int(target.talent.get(314, 0))
        race_names = {0: "未设定", 1: "精灵", 5: "龙族", 7: "高等精灵",
                      9: "魔族", 10: "霍比特", 11: "矮人"}
        lines.append(f"种族：{race_names.get(race, f'#{race}')}")

        return lines

    # ------------------------------------------------------------------
    # CHARA_MAKE_INHERIT (角色继承)
    # ------------------------------------------------------------------


    def _chara_make_inherit(self, target: Character) -> List[str]:
        """Character inheritance from previous save based on CHARA_MAKE_INHERIT.ERB.

        Child character inherits talents from parent(s) with probability.
        Does not inherit: breakdown, kojo, training talents, race, job, experience.
        """
        lines: List[str] = []
        name = target.name or "她"

        # Personality, sexual interest, maiden heart, constitution, technique
        # Range 10-152, excluding special talents
        skip_ranges = [(74, 79), (121, 124), (130, 144)]
        skip_single = [85]

        for tid in range(10, 153):
            # Skip special talent ranges
            should_skip = False
            for sr in skip_ranges:
                if sr[0] <= tid < sr[1]:
                    should_skip = True
                    break
            if tid in skip_single:
                should_skip = True
            if should_skip:
                continue

        # Private seal check
        is_futa = int(target.talent.get(121, 0))
        is_male = int(target.talent.get(122, 0))
        is_virgin = int(target.talent.get(0, 0))
        if is_futa or is_male or not is_virgin:
            target.talent[8] = 0  # 私处封印解除

        # Conflict check
        conflict_pairs = [
            (10, 12), (11, 13), (14, 16), (15, 17), (17, 18),
            (20, 23), (21, 23), (22, 23), (23, 24), (25, 26),
            (27, 28), (30, 31), (32, 33), (35, 36), (40, 41),
            (42, 43), (44, 45), (50, 51), (61, 62), (62, 64),
            (70, 71), (79, 80), (79, 81), (79, 82), (79, 122),
            (80, 81), (80, 82), (81, 82), (99, 100), (101, 102),
            (103, 104), (105, 106), (107, 108), (111, 112),
            (109, 110), (109, 114), (109, 116), (121, 122),
            (153, 154), (99, 263), (153, 122), (154, 122),
            (130, 122), (155, 122), (157, 122),
            (60, 150), (82, 143),
        ]
        resolved = []
        for a, b in conflict_pairs:
            if int(target.talent.get(a, 0)) and int(target.talent.get(b, 0)):
                # Randomly remove one
                if random.randint(0, 1):
                    target.talent[a] = 0
                    resolved.append(f"冲突解决：移除素质#{a}")
                else:
                    target.talent[b] = 0
                    resolved.append(f"冲突解决：移除素质#{b}")

        if resolved:
            lines.extend(resolved)
        else:
            lines.append(f"{name}的继承处理完成，无冲突。")

        return lines

    # ------------------------------------------------------------------
    # CHARA_MAKE_INPORT (角色导入)
    # ------------------------------------------------------------------


    def _chara_make_inport(self, target: Character) -> List[str]:
        """Character import based on CHARA_MAKE_INPORT.ERB.

        Imports a hero character from global data (GLOBALS),
        setting up ABL, BASE, MAXBASE, CFLAG, EXP, EQUIP, JUEL, TALENT, MARK, CSTR.
        """
        lines: List[str] = []
        v = self.interpreter.vars
        name = target.name or "她"

        # Check if import is enabled (FLAG:76)
        flag76 = int(v.get_array("FLAG", 76, 0))
        if flag76 <= 0:
            lines.append("角色导入功能未启用。")
            return lines

        # Set initial position and status
        target.cflag[501] = 1   # Floor 1
        target.cflag[502] = 0   # Progress 0
        target.cflag[1] = 2     # Invading status

        # Level setup
        flag77 = int(v.get_array("FLAG", 77, 0))
        if flag77:
            target.cflag[9] = 1  # Level 1
            target.exp[80] = 0   # Reset exp

            # Level up based on FLAG:60
            flag60 = int(v.get_array("FLAG", 60, 0))
            if flag60 > 0:
                current_level = 1
                for _ in range(flag60):
                    current_level += 1
                target.cflag[9] = min(current_level, 99)

        # Full HP/MP recovery
        target.base[0] = int(target.maxbase.get(0, 100))
        target.base[1] = int(target.maxbase.get(1, 100))

        # Generate body data if not present
        if int(target.cflag.get(451, 0)) == 0:
            lines.append(f"{name}的身体数据已生成。")

        lines.append(f"{name}已导入，等级：{int(target.cflag.get(9, 1))}")

        return lines

    # ------------------------------------------------------------------
    # CHARA_NAME_INIT (角色名初始化)
    # ------------------------------------------------------------------


    def _chara_name_init(self, target: Character) -> List[str]:
        """Initialize character name lists based on CHARA_NAME_INIT.ERB.

        Populates LIST_CHARA_NAME with western, Japanese, male, and Chinese names.
        Only initializes if the list is empty.
        """
        lines: List[str] = []
        v = self.interpreter.vars

        # Check if already initialized
        existing = ""
        try:
            existing = str(v.get_array("LIST_CHARA_NAME", 0, ""))
        except Exception:
            pass

        if len(existing) > 1:
            return lines  # Already initialized

        # Western female names (indices 0-199, 1200-1584)
        west_female = [
            "玛丽", "索菲亚", "安娜", "西尔维亚", "卡蒂亚", "艾莉",
            "米歇尔", "艾伦", "艾提卡", "爱丽丝", "弗朗索瓦斯",
            "厄勒克特拉", "格雷丝", "杰西卡", "莱亚", "丽贝卡",
            "薇儿薇特", "雅儿贝德", "叶卡捷琳娜", "阿加莎", "阿梅利亚",
            "安杰丽卡", "布丽奇特", "克里斯蒂娜", "科洛蒂亚", "雪莉露",
            "雪莉", "塞西莉亚", "贝拉", "贝基", "艾薇儿", "多萝西",
            "艾蜜莉", "费利西亚", "弗兰西斯卡", "格洛丽亚", "詹妮弗",
            "玛格丽特", "奥莉维亚", "维罗妮卡", "塞拉菲娜", "弗洛拉",
            "塔巴莎", "艾达", "卡罗尔", "夏洛特", "考狄利亚",
        ]

        # Japanese female names (indices 200-649)
        jp_female = [
            "樱", "遥", "霞", "雏", "葵", "瑞穂", "绫", "巴",
            "皐月", "弥生", "抚子", "佳奈美", "菖蒲", "唯", "凛",
            "日向", "朝雾", "雪风", "兰", "姫", "明日香", "狭雾",
            "瑞希", "焔", "沙耶香", "爱理", "百合子", "步美",
            "成实", "雏田", "枫", "纲手", "和美", "红叶", "绘里奈",
        ]

        # Western male names (indices 2000-2451)
        west_male = [
            "艾伦", "艾布特", "亚伯", "艾布纳", "亚伯拉罕", "亚岱尔",
            "亚当", "艾狄生", "阿道夫", "亚度尼斯", "亚德里恩",
            "亚恒", "艾伯特", "奥德里奇", "亚历山大", "阿历克斯",
            "亚尔弗列得", "阿尔杰", "阿尔杰农", "奥斯顿", "阿尔瓦",
            "阿尔文", "亚尔维斯", "亚摩斯", "安得烈", "安德鲁",
            "安迪", "安其罗", "安格斯", "安斯艾尔", "安东尼",
        ]

        # Japanese male names (indices 3000-4057)
        jp_male = [
            "翔太", "蓮", "陸", "颯太", "翼", "隼人", "大和", "拓海",
            "健太", "大輔", "翔", "悠太", "悠斗", "陽斗", "奏太",
            "大地", "響", "誠", "海斗", "諒", "太一", "亮太", "一郎",
            "駿", "優斗", "樹", "匠", "直樹", "悠", "太郎", "空",
        ]

        # Chinese names (indices 4500-5288)
        cn_names = [
            "宝清", "小波", "硕白", "阿靓", "泽瑞", "璐儿", "雅玉",
            "思雨", "一丁", "筱雨", "一男", "阿午", "筱枚", "首君",
            "小琳", "泽文", "泽雯", "俊达", "雅竹", "奕男", "伊丽",
            "文华", "书于", "勤勤", "知冀", "小凤", "天玺", "欣然",
        ]

        # Store name counts
        v.set_array("WEST_NAME_COUNT", 0, 585)
        v.set_array("JAPEN_NAME_COUNT", 0, 450)
        v.set_array("WEST_MALE_NAME_COUNT", 0, 453)
        v.set_array("JAPEN_MALE_NAME_COUNT", 0, 1059)
        v.set_array("CHINA_NAME_COUNT", 0, 789)

        # Store names into LIST_CHARA_NAME
        for i, n in enumerate(west_female):
            v.set_array("LIST_CHARA_NAME", i, n)
        for i, n in enumerate(jp_female):
            v.set_array("LIST_CHARA_NAME", 200 + i, n)
        for i, n in enumerate(west_male):
            v.set_array("LIST_CHARA_NAME", 2000 + i, n)
        for i, n in enumerate(jp_male):
            v.set_array("LIST_CHARA_NAME", 3000 + i, n)
        for i, n in enumerate(cn_names):
            v.set_array("LIST_CHARA_NAME", 4500 + i, n)

        lines.append("角色名列表已初始化。")
        return lines

    # ------------------------------------------------------------------
    # CHARA_FIRST_EXP (初次经验处理 - 完整版)
    # ------------------------------------------------------------------


    def _chara_first_exp_full(self, target: Character, exp_type: int) -> List[str]:
        """Full first experience processing based on CHARA_FIRST_EXP.ERB.

        exp_type: 0=first_kiss, 1=first_sex
        Determines first kiss/sex partner based on family settings,
        previous life, and random events.
        """
        lines: List[str] = []
        name = target.name or "她"

        first_kiss = int(target.cflag.get(16, -1))
        kiss_desc = str(target.cstr.get(4, ""))
        first_sex = int(target.cflag.get(15, -1))
        sex_desc = str(target.cstr.get(3, ""))

        is_male = int(target.talent.get(122, 0))
        is_futa = int(target.talent.get(121, 0))
        is_virgin = int(target.talent.get(0, 0))

        # If non-virgin female with no sex record, set to 0
        if not is_male and not is_virgin and first_sex == -1:
            first_sex = 0

        # If has sex experience, kiss is possible
        sex_exp = int(target.exp.get(5, 0))
        prostitution_exp = int(target.exp.get(74, 0))
        if (sex_exp > 0 or prostitution_exp > 0) and first_kiss == -1:
            first_kiss = 0

        # Bestiality experience checks
        bestiality_exp = int(target.exp.get(56, 0))
        if kiss_desc == "" and first_kiss == 0 and bestiality_exp > 0:
            if random.randint(0, 19) == 0:
                first_kiss = 996  # Wild dog anus
            elif random.randint(0, 9) == 0:
                first_kiss = 997  # Wild dog penis
            elif random.randint(0, 4) == 0:
                first_kiss = 998  # Wild dog mouth

        # Family settings check (TALENT:320)
        family = int(target.talent.get(320, 0))
        family_flag = family % 10
        partner_desc = ""
        men_or_girl = 0  # 1=male, 2=female, 3=futa, 4=random

        if family_flag == 1:
            # Has family settings
            marriage_type = (family % 100000) // 10000
            spouse_gender = (family % 10000000000) // 1000000000

            if marriage_type == 1:  # Married
                if spouse_gender in (0, 4, 8):
                    partner_desc = "丈夫"
                    men_or_girl = 1
                elif spouse_gender in (1, 5, 7):
                    partner_desc = "扶她妻子"
                    men_or_girl = 3
                else:
                    partner_desc = "妻子"
                    men_or_girl = 2
            elif marriage_type == 2:  # Divorced
                if spouse_gender in (0, 4, 8):
                    partner_desc = "前夫"
                    men_or_girl = 1
                elif spouse_gender in (1, 5, 7):
                    partner_desc = "前扶她妻子"
                    men_or_girl = 3
                else:
                    partner_desc = "前妻"
                    men_or_girl = 2
            elif marriage_type == 5:  # Widowed
                if spouse_gender in (0, 4, 8):
                    partner_desc = "亡夫"
                    men_or_girl = 1
                elif spouse_gender in (1, 5, 7):
                    partner_desc = "亡妻（扶她）"
                    men_or_girl = 3
                else:
                    partner_desc = "亡妻"
                    men_or_girl = 2

            # Sibling checks
            older_bro = (family % 10000000) // 1000000
            younger_bro = (family % 1000000000) // 100000000
            older_sis = (family % 1000000) // 100000
            younger_sis = (family % 100000000) // 10000000

            if not partner_desc:
                if older_bro > 0 and random.randint(0, 19) == 0:
                    partner_desc = "亲哥哥"
                    men_or_girl = 1
                elif younger_bro > 0 and random.randint(0, 19) == 0:
                    partner_desc = "亲弟弟"
                    men_or_girl = 1
                elif younger_bro > 0 and int(target.talent.get(143, 0)) and random.randint(0, 4) == 0:
                    partner_desc = "亲弟弟"
                    men_or_girl = 1
                elif older_sis > 0 and random.randint(0, 19) == 0:
                    partner_desc = "亲姐姐"
                    men_or_girl = 2
                elif younger_sis > 0 and random.randint(0, 19) == 0:
                    partner_desc = "亲妹妹"
                    men_or_girl = 2
                elif younger_sis > 0 and int(target.talent.get(142, 0)) and random.randint(0, 4) == 0:
                    partner_desc = "亲妹妹"
                    men_or_girl = 2

            # Parent checks
            if not partner_desc:
                if random.randint(0, 19) == 0:
                    partner_desc = "亲爹"
                    men_or_girl = 1
                elif int(target.talent.get(141, 0)) and random.randint(0, 9) == 0:
                    partner_desc = "亲爹"
                    men_or_girl = 1
                elif random.randint(0, 19) == 0:
                    partner_desc = "亲妈"
                    men_or_girl = 2
                elif int(target.talent.get(140, 0)) and random.randint(0, 9) == 0:
                    partner_desc = "亲妈"
                    men_or_girl = 2

        # Hometown lover
        if int(target.talent.get(317, 0)) == 4:
            partner_desc = "故乡的恋人"
            men_or_girl = 4

        # Assign kiss partner
        if kiss_desc == "" and first_kiss == 0:
            if partner_desc and random.randint(0, 1) == 0:
                kiss_desc = partner_desc

        # Assign sex partner
        if not is_virgin and sex_desc == "" and first_sex == 0:
            if partner_desc and random.randint(0, 1) == 0:
                sex_desc = partner_desc

        # Previous life based partner
        prev_life = int(target.talent.get(315, 0))
        life_partners_male = {
            1: ["学校的後輩", "学校的先輩", "女教师", "同級生"],
            3: "农妇", 4: "港口的娼妇", 6: "街边的娼妇",
            8: ["家庭教师", "小女仆"],
            15: ["女上司", "客户", "熟客"],
            18: "熟客",
            19: ["战地的少女", "战友", "长官", "部下", "部下的女儿", "长官的女儿"],
            5: "女客人", 20: "女奴隶主",
        }
        life_partners_female = {
            1: ["学校的後輩", "学校的先輩", "教师", "同級生"],
            3: "农夫", 4: "渔民", 6: "流氓",
            8: ["家庭教师", "佣人"],
            15: ["上司", "客户", "熟客"],
            18: "熟客",
            19: ["战地的少年", "战友", "长官", "部下", "部下的儿子", "长官的儿子", "少年士兵"],
            5: "中年客人", 20: "奴隶主",
        }

        if not partner_desc:
            if is_male or is_futa:
                partners = life_partners_male.get(prev_life, [])
            else:
                partners = life_partners_female.get(prev_life, [])

            if isinstance(partners, list) and partners:
                partner_desc = random.choice(partners)
                if is_male or is_futa:
                    men_or_girl = 2
                else:
                    men_or_girl = 1
            elif isinstance(partners, str):
                partner_desc = partners
                if is_male or is_futa:
                    men_or_girl = 2
                else:
                    men_or_girl = 1

        # Final assignment
        if kiss_desc == "" and first_kiss == 0 and partner_desc:
            kiss_desc = partner_desc

        if not is_virgin and sex_desc == "" and first_sex == 0 and partner_desc:
            sex_desc = partner_desc

        # Default kiss point
        if kiss_desc and first_kiss == 0:
            if random.randint(0, 29) > 0:
                first_kiss = 1  # Lips
            elif random.randint(0, 2) == 0:
                first_kiss = 401  # Anus
            elif men_or_girl == 1:
                first_kiss = 101  # Penis
            elif men_or_girl == 2:
                first_kiss = 301  # Vagina
            elif men_or_girl == 3:
                first_kiss = 101 if random.randint(0, 1) == 0 else 301

        if sex_desc and first_sex == 0:
            first_sex = 100

        # Store results
        target.cflag[16] = first_kiss
        target.cstr[4] = kiss_desc
        target.cflag[15] = first_sex
        target.cstr[3] = sex_desc

        # Display
        if exp_type == 0 and kiss_desc:
            location = {1: "唇", 101: "阴茎", 301: "私处", 401: "肛门"}.get(first_kiss, "不明")
            lines.append(f"{name}的初吻是和{kiss_desc}的{location}。")
        elif exp_type == 1 and sex_desc:
            lines.append(f"{name}的初次是和{sex_desc}。")

        return lines

    # ==================================================================
    # AGENT System - 间谍/密探系统 (AGENT.ERB / AGENT_1.ERB / AGENT_EVENT.ERB)
    # ==================================================================

    def _show_status(self, target=None):
        """状态显示 - 桥接ERB SHOW_STATUS"""
        return self.call_erb_function('SHOW_STATUS')


