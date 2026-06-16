from __future__ import annotations
"""Module for CmExtMixin - 自定义菜单"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class CmExtMixin:
    """Mixin providing 自定义菜单 methods for GameEngine"""

    def _cm_base(self, char: Character) -> None:
        """职业基础参数设定 (对应 @CM_BASE)"""
        # 战士或骑士
        if char.talent.get(200, 0) or char.talent.get(205, 0):
            char.cflag[11] = 20  # STR
            char.cflag[12] = 20  # VIT
            char.cflag[13] = 20  # INT
            char.cflag[14] = 20  # AGI
        # 魔法师或巫女
        elif char.talent.get(201, 0) or char.talent.get(206, 0):
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15
        # 神官或忍者
        elif char.talent.get(202, 0) or char.talent.get(207, 0):
            char.cflag[11] = 15
            char.cflag[12] = 20
            char.cflag[13] = 15
            char.cflag[14] = 20
        # 盗贼或弓手
        elif char.talent.get(203, 0) or char.talent.get(208, 0):
            char.cflag[11] = 20
            char.cflag[12] = 15
            char.cflag[13] = 20
            char.cflag[14] = 15
        # 精英
        elif char.talent.get(220, 0):
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15
        else:
            char.cflag[11] = 15
            char.cflag[12] = 15
            char.cflag[13] = 15
            char.cflag[14] = 15
        
        # 神官和巫女有治癒技能
        if char.talent.get(202, 0) or char.talent.get(206, 0):
            char.talent[117] = 1
            char.cflag[152] = 20  # 信仰值
        # 战士和骑士有鼓舞技能
        elif char.talent.get(200, 0) or char.talent.get(205, 0):
            char.talent[118] = 1
        
        # 种族加成
        race2 = char.talent.get(314, 0)  # 种族2
        if race2 == 2:  # 史莱姆
            char.cflag[12] += 5
            char.cflag[14] += 5
        elif race2 == 5:  # 触手
            char.cflag[11] += 5
            char.cflag[13] += 5
        elif race2 == 6:  # 妖精
            char.cflag[11] -= 4
            char.cflag[12] -= 4
            char.cflag[13] -= 4
            char.cflag[14] -= 4
        elif race2 == 7:  # 巨人
            char.cflag[11] += 5
            char.cflag[12] += 5
            char.cflag[13] += 5
            char.cflag[14] += 5
        
        # 精英有魔的刻印
        if char.talent.get(220, 0):
            char.talent[254] = 1






    def _cm_gender(self, char: Character) -> None:
        """性别设定 (对应 @CM_GENDER)"""
        # 扶她 (TALENT:121)
        if random.randint(0, 59) == 0:
            char.talent[121] = 1
        # 男人 (TALENT:122)
        elif random.randint(0, 5) == 0 and self._get_flag_bit(8, 0):
            char.talent[122] = 1






    def _cm_kind(self, char: Character, is_elite: bool = False) -> None:
        """善恶值设定 (对应 @CM_KIND)"""
        if not is_elite:
            char.cflag[151] = random.randint(0, 199)
        else:
            char.cflag[151] = random.randint(0, 99)






    def _cm_kj(self, char: Character, personality: int = 0) -> None:
        """口上性格设定 (对应 @CM_KJ)"""
        # 清除现有性格 (160-179)
        for i in range(160, 180):
            char.talent[i] = 0
        
        if 160 <= personality <= 180:
            char.talent[personality] = 1
        else:
            # 随机性格
            while True:
                x = random.randint(160, 168)
                # 排除 UNIQUE 性格
                if x == 165:  # 村娘A (MAO专用)
                    continue
                # 男人不能是恶女
                if char.talent.get(122, 0) and x == 166:
                    continue
                # 高贵的男人是贵公子
                if char.talent.get(122, 0) and x == 163:
                    x = 174
                # 167 -> 175
                if x == 167:
                    x = 175
                # 168-169 调整
                if 168 <= x <= 169:
                    x += 5
                    # 女性贵公子改为高贵
                    if char.talent.get(122, 0) == 0 and x == 174:
                        x = 163
                char.talent[x] = 1
                break






    def _cm_look(self, char: Character, race: int = 0) -> None:
        """外貌设定 (对应 @CM_LOOK)"""
        # 种族设定
        if race > 0:
            char.talent[314] = race
        else:
            char.talent[314] = random.randint(1, 12)
        
        # 阴毛状态 (后代默认为 2)
        if char.talent.get(2, 0):  # 后代
            char.talent[300] = 2






    def _cm_skill(self, char: Character) -> None:
        """战术技能设定 (对应 @CM_SKILL)"""
        race2 = char.talent.get(314, 0)
        
        # 战术 (240)
        if random.randint(0, 39) == 0:
            char.talent[240] = 1
        
        # 魔术 (241) - 妖精更容易获得
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[241] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[241] = 1
        
        # 法术 (242) - 妖精更容易获得
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[242] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[242] = 1
        
        # 奇袭 (243)
        if random.randint(0, 39) == 0:
            char.talent[243] = 1
        
        # 肌肉型/虚弱 (248/256) - 巨人更容易肌肉型
        if race2 == 7:
            if random.randint(0, 9) == 0:
                char.talent[248] = 1
        else:
            if random.randint(0, 29) == 0:
                char.talent[248] = 1
            elif random.randint(0, 28) == 0:
                char.talent[256] = 1
        
        # 铁壁 (249)
        if random.randint(0, 39) == 0:
            char.talent[249] = 1
        
        # 咒术 (250) - 妖精更容易获得
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[250] = 1
        else:
            if random.randint(0, 19) == 0:
                char.talent[250] = 1
        
        # 忍术 (251) - 妖精也容易获得
        if race2 != 6:
            if random.randint(0, 39) == 0:
                char.talent[251] = 1
        else:
            if random.randint(0, 29) == 0:
                char.talent[251] = 1
        
        # 先制 (252)
        if random.randint(0, 39) == 0:
            char.talent[252] = 1
        
        # 褐色/白皙 (253/255)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[253] = 1
        elif x == 1:
            char.talent[255] = 1
        elif race2 == 8 or race2 == 9:  # 堕天使/魔族
            if random.randint(0, 9) == 0:
                char.talent[244] = 1
        
        # 魔法耐性 (257)
        if random.randint(0, 39) == 0:
            char.talent[257] = 1
        
        # 妖精如果没有任何术则获得魔法耐性
        if race2 == 6 and not char.talent.get(241, 0) and not char.talent.get(242, 0) and \
           not char.talent.get(250, 0) and not char.talent.get(251, 0):
            char.talent[257] = 1
        
        # 俊足 (258)
        if random.randint(0, 39) == 0:
            char.talent[258] = 1
        
        # 独眼/额头天眼 (259/260)
        x = random.randint(0, 59)
        if x == 0:
            char.talent[259] = 1
        elif x == 1:
            char.talent[260] = 1






    def _cm_st(self, char: Character) -> None:
        """勇者初始等级设定"""
        # 基础等级为 1
        pass






    def _cm_st_ace(self, char: Character) -> None:
        """精英部下初始等级设定"""
        # 精英等级较高
        char.cflag[9] = 5






    def _cm_stp(self, char: Character) -> None:
        """侵攻楼层设定 (对应 @CM_STP)"""
        char.cflag[501] = 1   # 侵攻楼层
        char.cflag[502] = 0   # 侵攻度
        char.cflag[1] = 2     # 侵攻中
        char.cflag[508] = 3   # 再起点






    def _cm_talent(self, char: Character) -> None:
        """素质随机生成 (对应 @CM_TALENT)"""
        # 胆怯/刚强/文静 (10/12/14)
        x = random.randint(0, 2)
        if x == 0 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[10] = 1
        elif x == 1 and (char.talent.get(161, 0) or char.talent.get(163, 0) or 
                         char.talent.get(164, 0) or char.talent.get(166, 0) or 
                         char.talent.get(174, 0) or char.talent.get(175, 0)):
            char.talent[12] = 1
        elif x == 2 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[14] = 1
        
        # 反抗心/坦率/嚣张 (11/13/16)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[11] = 1
            if random.randint(0, 7) == 0:
                char.talent[18] = 1  # 傲娇
        elif x == 1:
            char.talent[13] = 1
        elif x == 2 and (char.talent.get(161, 0) or char.talent.get(163, 0) or 
                         char.talent.get(164, 0) or char.talent.get(166, 0) or 
                         char.talent.get(174, 0) or char.talent.get(175, 0)):
            char.talent[16] = 1
        
        # 高姿态/低姿态/傲娇 (15/17/18)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[15] = 1
        elif x == 1 and not char.talent.get(18, 0):
            char.talent[17] = 1
        elif x == 2 and not char.talent.get(18, 0):
            char.talent[18] = 1
        
        # 克制/冷漠/感情淡薄/好奇心/献身的 (20/21/22/23/63)
        x = random.randint(0, 15)
        if x == 0:
            char.talent[21] = 1
        elif x == 1:
            char.talent[23] = 1
        elif x == 2:
            char.talent[22] = 1
        elif x == 3:
            char.talent[20] = 1
        elif x == 4:
            char.talent[63] = 1
        
        # 保守的/乐观的/悲观的 (24/25/26)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[24] = 1
        elif x == 1:
            char.talent[25] = 1
        elif x == 2:
            char.talent[26] = 1
        
        # 戒备森严/爱表现 (27/28)
        x = random.randint(0, 7)
        if x == 0:
            char.talent[27] = 1
        elif x == 1:
            char.talent[28] = 1
        
        # 看重贞操/看轻贞操 (30/31)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[30] = 1
        elif x == 1:
            char.talent[31] = 1
        
        # 压抑/开放 (32/33)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[32] = 1
        elif x == 1:
            char.talent[33] = 1
        
        # 抵抗 (34)
        if random.randint(0, 11) == 0:
            char.talent[34] = 1
        
        # 害羞/不知羞耻 (35/36)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[35] = 1
        elif x == 1:
            char.talent[36] = 1
        
        # 把柄 (37)
        if random.randint(0, 7) == 0:
            char.talent[37] = 1
        
        # 害怕疼痛/不惧疼痛 (40/41)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[40] = 1
        elif x == 1:
            char.talent[41] = 1
        
        # 容易湿/不易湿 (42/43)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[42] = 1
        elif x == 1:
            char.talent[43] = 1
        
        # 眼镜 (48)
        if random.randint(0, 11) == 0:
            char.talent[48] = 1
        
        # 快速学习/学习缓慢 (50/51)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[50] = 1
        elif x == 1:
            char.talent[51] = 1
        
        # 擅用舌头 (52)
        if random.randint(0, 7) == 0:
            char.talent[52] = 1
        
        # 漏尿癖 (57)
        if random.randint(0, 49) == 0:
            char.talent[57] = 1
        
        # 容易自慰 (60)
        if random.randint(0, 7) == 0:
            char.talent[60] = 1
        
        # 不怕污臭/反感污臭 (61/62)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[61] = 1
        elif x == 1:
            char.talent[62] = 1
        
        # 接受快感/否定快感 (70/71)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[70] = 1
        elif x == 1:
            char.talent[71] = 1
        
        # 容易上瘾 (72)
        if random.randint(0, 7) == 0:
            char.talent[72] = 1
        
        # 容易陷落 (73)
        if random.randint(0, 29) == 0:
            char.talent[73] = 1
        
        # 抵抗诱惑 (69)
        if random.randint(0, 29) == 0:
            char.talent[69] = 1
        
        # 倒错的 (80)
        if random.randint(0, 7) == 0:
            char.talent[80] = 1
        
        # 双性恋/讨厌男人 (81/82)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[81] = 1
        elif x == 1:
            char.talent[82] = 1
        
        # 抖S/抖M气质 (ABL:20/21)
        x = random.randint(0, 7)
        if x == 0:
            char.abl[20] = 3
        elif x == 1:
            char.abl[21] = 3
        
        # 嫉妒 (84)
        if random.randint(0, 9) == 0:
            char.talent[84] = 1
        
        # 小恶魔 (87)
        if random.randint(0, 7) == 0:
            char.talent[87] = 1
        
        # 露出癖 (ABL:17)
        if random.randint(0, 39) == 0:
            char.abl[17] = 3
        
        # 魅惑 (91)
        if random.randint(0, 19) == 0:
            char.talent[91] = 1
        
        # 魁梧/娇小 (99/100)
        x = random.randint(0, 11)
        race2 = char.talent.get(314, 0)
        if race2 == 7:  # 巨人
            if x <= 8:
                char.talent[99] = 1
            elif x == 11:
                char.talent[100] = 1
        else:
            if x == 0:
                char.talent[99] = 1
            elif x == 1:
                char.talent[100] = 1
        
        # 阴蒂钝感/敏感 (101/102)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[101] = 1
        elif x == 1:
            char.talent[102] = 1
        
        # 私处钝感/敏感 (103/104) - 仅女性
        x = random.randint(0, 11)
        if char.talent.get(122, 0) == 0:
            if x == 0:
                char.talent[103] = 1
            elif x == 1:
                char.talent[104] = 1
        
        # 肛门钝感/敏感 (105/106)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[105] = 1
        elif x == 1:
            char.talent[106] = 1
        
        # 乳房钝感/敏感 (107/108)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[107] = 1
        elif x == 1:
            char.talent[108] = 1
        
        # 超乳/爆乳/绝壁/贫乳/巨乳 (119/114/116/109/110) - 仅女性
        if char.talent.get(122, 0) == 0:
            if random.randint(0, 49) == 0:
                char.talent[119] = 1
            elif random.randint(0, 24) == 0:
                char.talent[114] = 1
            elif random.randint(0, 23) == 0:
                char.talent[116] = 1
            elif random.randint(0, 7) == 0:
                char.talent[109] = 1
            elif random.randint(0, 6) == 0:
                char.talent[110] = 1
        
        # 快速回复/回复缓慢 (111/112)
        x = random.randint(0, 11)
        if x == 0:
            char.talent[111] = 1
        elif x == 1:
            char.talent[112] = 1
        
        # 魅力 (113)
        if random.randint(0, 7) == 0:
            char.talent[113] = 1
        
        # 早泄 (133) - 男性/扶她
        if random.randint(0, 24) == 0 and (char.talent.get(122, 0) or char.talent.get(121, 0)):
            char.talent[133] = 1
        
        # 软弱 (134) - 慈爱/懦弱
        if random.randint(0, 5) == 0 and (char.talent.get(160, 0) or char.talent.get(162, 0)):
            char.talent[134] = 1
        
        # 未熟 (135)
        if random.randint(0, 11) == 0:
            char.talent[135] = 1
            if random.randint(0, 7) == 0:
                char.talent[132] = 1  # 幼稚
            if random.randint(0, 7) == 0 and (char.talent.get(122, 0) or char.talent.get(121, 0)):
                char.talent[133] = 1  # 早泄
        
        # 各种情结 (140-143)
        x = random.randint(0, 100)
        if char.talent.get(122, 0):  # 男性
            if x < 4:
                char.talent[140] = 1  # 恋母情结
            elif x < 8:
                char.talent[142] = 1  # 萝莉控
            elif x < 10:
                char.talent[141] = 1  # 恋父情结
            elif x < 12:
                char.talent[143] = 1  # 正太控
        elif char.talent.get(121, 0):  # 扶她
            if x < 3:
                char.talent[140] = 1
            elif x < 6:
                char.talent[142] = 1
            elif x < 9:
                char.talent[141] = 1
            elif x < 12:
                char.talent[143] = 1
        else:  # 女性
            if x < 4:
                char.talent[141] = 1
            elif x < 8:
                char.talent[143] = 1
            elif x < 10:
                char.talent[140] = 1
            elif x < 12:
                char.talent[142] = 1
        
        # 不受洗脑 (152)
        if random.randint(0, 29) == 0:
            char.talent[152] = 1
        
        # 担保人 (290)
        if char.talent.get(37, 0) and random.randint(0, 3) == 0:
            char.talent[290] = 1
        elif random.randint(0, 11) == 0:
            char.talent[290] = 1





