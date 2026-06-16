from __future__ import annotations
"""Module for SpecialExtMixin - 特殊检查"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SpecialExtMixin:
    """Mixin providing 特殊检查 methods for GameEngine"""

    def _check_special_skill(self, target: Character, seiin: int = 0) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars
        target_idx = self._find_char_index_for(target)
        if target_idx < 0:
            return messages

        char_name = getattr(target, 'savestr', target.name or target.callname or "")
        player = self._get_player()
        player_name = getattr(player, 'savestr', "主人") if player else "主人"

        if target.talent.get(9, 0):
            messages.extend(self._check_special_skill_bodyshift(target))
            return messages

        if target.mark.get(3, 0) == 0:
            if target.cflag.get(2, 0) >= 2000 and target.cflag.get(0, 0) < 2 and (target.talent.get(76, 0) or target.talent.get(85, 0)):
                messages.append(f"{char_name}带着崇敬的眼神看着你…")
                messages.append(f"{char_name}无论是灵魂还是肉体，都全心全意地献给{player_name}了…")
                if target.abl.get(10, 0) < 5:
                    target.abl[10] = 5
                    messages.append("顺从LV5了")
                if target.cflag.get(0, 0) < 1:
                    messages.append(f"{char_name}可以被卖掉了。")
                messages.append(f"{char_name}可以做助手了。")
                target.cflag[0] = 2

            elif target.cflag.get(2, 0) >= 1000:
                if (target.abl.get(10, 0) >= 3 and target.exp.get(21, 0) >= self.exp_level_thresholds[5]
                        and target.talent.get(76, 0) == 0 and target.talent.get(85, 0) == 0
                        and target.talent.get(184, 0) == 0 and target.mark.get(2, 0) == 3
                        and target.abl.get(16, 0) >= 3):
                    messages.append(f"{char_name}柔情似水地看着你…")
                    messages.append(f"{char_name}因{player_name}的行为而感到喜悦。想粘着你，想为你分忧，为你做些什么…渴望着你的宠爱。")
                    messages.append(f"{char_name}获得了【爱慕】。")
                    target.talent[85] = 1

                    if target.talent.get(76, 0) == 0:
                        v.flags[30] = int(v.flags.get(30, 0)) + 1

                    if target.talent.get(11, 0) and target.talent.get(18, 0):
                        messages.append(f"{char_name}失去了【傲娇】，获得了【顺从】。")
                        target.talent[11] = 0
                        target.talent[13] = 1

                    if target.talent.get(18, 0) == 0 and target.talent.get(11, 0):
                        messages.append(f"{char_name}失去了【傲娇】。")
                        target.talent[11] = 0

                    if target.talent.get(20, 0) or target.talent.get(21, 0):
                        lost = []
                        if target.talent.get(20, 0):
                            lost.append("【克制】")
                            target.talent[20] = 0
                        if target.talent.get(21, 0):
                            lost.append("【冷漠】")
                            target.talent[21] = 0
                        messages.append(f"{char_name}的{''.join(lost)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = target.juel.get(100, 0) // 2

                    if target.talent.get(27, 0):
                        messages.append(f"{char_name}失去了【一线越えない】。")
                        target.talent[27] = 0

                    if target.talent.get(151, 0):
                        messages.append(f"{char_name}失去了【绝不侍奉】。")
                        target.talent[151] = 0

                    if target.talent.get(84, 0):
                        messages.append(f"{char_name}失去了【嫉妒】。")
                        target.talent[84] = 0

                    if target.base.get(10, 0) and target.base.get(10, 0) > 0:
                        d = target.base.get(10, 0) // 2
                        messages.append(f"{char_name}时日无多，生命还剩下{d}天。")

                    if target.talent.get('魂缚', 0):
                        messages.append(f"{char_name}被束缚的灵魂，在向自己的爱与欲望屈服时被解放了。")
                        messages.append(f"{char_name}失去了【魂缚】。")
                        target.talent['魂缚'] = 0

                    if target.talent.get(273, 0):
                        messages.append(f"{char_name}的【贞操封印】的力量消失了……")

                    if int(getattr(target, 'no', -1)) == 17:
                        self._set_character_ex_talent(target, 3, 1)
                        messages.append(f"{char_name}一阵眩晕、似乎拥有了替身的素质……")

                if (target.abl.get(11, 0) >= 3
                        and target.abl.get(0, 0) + target.abl.get(1, 0) + target.abl.get(2, 0) + target.abl.get(3, 0) >= 10
                        and target.exp.get(50, 0) >= 3
                        and target.talent.get(85, 0) == 0 and target.talent.get(76, 0) == 0
                        and target.mark.get(1, 0) == 3 and target.mark.get(2, 0) == 3):
                    messages.append(f"{char_name}看你的眼神，好像忘记了你还有上半身…")
                    messages.append(f"{char_name}沉迷于{player_name}给予的快感之中了……")
                    messages.append(f"{char_name}获得了【淫乱】。")
                    target.talent[76] = 1

                    if target.talent.get(85, 0) == 0:
                        v.flags[30] = int(v.flags.get(30, 0)) + 1

                    if target.talent.get(20, 0) or target.talent.get(21, 0):
                        lost = []
                        if target.talent.get(20, 0):
                            lost.append("【克制】")
                            target.talent[20] = 0
                        if target.talent.get(21, 0):
                            lost.append("【冷漠】")
                            target.talent[21] = 0
                        messages.append(f"{char_name}的{''.join(lost)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = target.juel.get(100, 0) // 2

                    if target.talent.get(27, 0):
                        messages.append(f"{char_name}失去了【一线越えない】。")
                        target.talent[27] = 0

                    if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(84, 0):
                        lost = []
                        if target.talent.get(32, 0):
                            lost.append("【压抑】")
                            target.talent[32] = 0
                        if target.talent.get(34, 0):
                            lost.append("【抵抗】")
                            target.talent[34] = 0
                        if target.talent.get(84, 0):
                            lost.append("【嫉妒】")
                            target.talent[84] = 0
                        messages.append(f"{char_name}的{''.join(lost)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = target.juel.get(100, 0) // 2

                    if target.talent.get(71, 0):
                        messages.append(f"{char_name}失去了【否定快感】。")
                        target.talent[71] = 0

                    if target.talent.get(150, 0):
                        messages.append(f"{char_name}失去了【从不自慰】。")
                        target.talent[150] = 0

                    if not target.talent.get('魂缚', 0):
                        if target.talent.get(314, 0) == 1:
                            messages.append(f"{char_name}从高洁的精灵，堕落为卑微的肉壶了。")
                            target.talent[314] = 7
                            if target.talent.get(244, 0) == 0:
                                target.talent[253] = 1
                            target.talent[255] = 0
                        elif target.talent.get(314, 0) == 6:
                            messages.append(f"{char_name}纯洁的灵魂完全堕落了，成为了被淫靡欲望所支配的下等性奴隶。")
                            target.talent[314] = 8
                            if target.talent.get(244, 0) == 0:
                                target.talent[253] = 1
                            target.talent[255] = 0

                    if target.talent.get(273, 0):
                        messages.append(f"{char_name}的【贞操封印】的力量消失了……")

                    if int(getattr(target, 'no', -1)) == 17:
                        self._set_character_ex_talent(target, 3, 1)
                        messages.append(f"{char_name}一阵眩晕、似乎拥有了替身的素质……")

                if (target.cflag.get(2, 0) >= 5000
                        and target.abl.get(10, 0) >= 5
                        and target.mark.get(1, 0) == 3 and target.mark.get(2, 0) == 3):
                    if target.talent.get(150, 0):
                        messages.append(f"{char_name}失去了【从不自慰】。")
                        target.talent[150] = 0
                    if target.talent.get(151, 0):
                        messages.append(f"{char_name}失去了【绝不侍奉】。")
                        target.talent[151] = 0
                    if target.talent.get(152, 0):
                        messages.append(f"{char_name}失去了【不受洗脑】。")
                        target.talent[152] = 0

        if target.talent.get(47, 0) == 0:
            if (target.abl.get(12, 0) >= 7 and target.abl.get(13, 0) >= 7
                    and target.exp.get(22, 0) >= 2000 and target.talent.get(52, 0) == 0
                    and target.cflag.get(600, 0) >= 100):
                messages.append(f"{char_name}因为不断地强制精饮绝顶，终于完全适应了精液的味道……")
                messages.append("甚至还喜欢上了。")
                messages.append(f"{char_name}获得了【喜欢精液】。")
                target.talent[47] = 1
            elif (target.abl.get(12, 0) >= 5 and target.abl.get(13, 0) >= 5
                    and target.exp.get(22, 0) >= 1500 and target.talent.get(52, 0) == 0
                    and target.cflag.get(600, 0) >= 80):
                messages.append(f"{char_name}喜欢上了精液的味道……")
                messages.append(f"{char_name}获得了【喜欢精液】。")
                target.talent[47] = 1
            elif (target.abl.get(12, 0) >= 5 and target.abl.get(13, 0) >= 5
                    and target.exp.get(22, 0) >= 1000 and target.talent.get(52, 0)
                    and target.cflag.get(600, 0) >= 50):
                messages.append(f"{char_name}感到似乎离不开精液了……")
                messages.append(f"{char_name}获得了【喜欢精液】。")
                target.talent[47] = 1

        if target.talent.get(51, 0):
            if (target.abl.get(12, 0) >= 7 and target.abl.get(13, 0) >= 7
                    and target.exp.get(22, 0) >= 1500 and target.talent.get(52, 0) == 0):
                messages.append(f"{char_name}通过持续的侍奉，侍奉技术获得了飞跃的进步……")
                messages.append(f"{char_name}获得了【擅用舌头】。")
                target.talent[52] = 1
        else:
            if (target.abl.get(12, 0) >= 5 and target.abl.get(13, 0) >= 5
                    and target.exp.get(22, 0) >= 1000 and target.talent.get(52, 0) == 0):
                messages.append(f"{char_name}的侍奉技术精进了……")
                messages.append(f"{char_name}获得了【擅用舌头】。")
                target.talent[52] = 1

        if (target.abl.get(20, 0) >= 4 and target.abl.get(12, 0) >= 4
                and target.exp.get(33, 0) >= 300 and target.talent.get(83, 0) == 0):
            messages.append(f"{char_name}的眼神变得凌厉了…")
            messages.append(f"{char_name}学会了将快乐建立在他人的痛苦之上。")
            messages.append(f"{char_name}获得了【施虐狂】。")
            target.talent[83] = 1

        if (target.abl.get(21, 0) >= 4 and target.abl.get(17, 0) >= 2
                and target.exp.get(30, 0) >= 300 and target.talent.get(88, 0) == 0):
            messages.append(f"{char_name}的眼神变得卑微了…")
            messages.append(f"{char_name}将痛楚和快感视为一体，学会了享受被支配，被凌辱的喜悦。")
            messages.append(f"{char_name}获得了【受虐狂】。")
            target.talent[88] = 1

        if (target.abl.get(17, 0) >= 4 and target.abl.get(21, 0) >= 2
                and target.exp.get(11, 0) + target.exp.get(31, 0) + target.exp.get(54, 0) >= 200
                and target.talent.get(89, 0) == 0):
            messages.append(f"{char_name}的神情变得害羞…")
            messages.append("但是，却学会了将这份羞耻变成快感。将自己的被羞辱的姿态呈现他人，令她感到身心无比圆满。")
            messages.append(f"{char_name}获得了【露出狂】。")
            target.talent[89] = 1

        if (target.abl.get(11, 0) >= 5 and target.abl.get(39, 0) >= 3
                and target.exp.get(56, 0) >= 300 and target.talent.get(136, 0) == 0):
            messages.append(f"{char_name}的行为彻底变化了…")
            messages.append("整天喜欢四脚爬爬地在地上爬行，一边扭腰抬臀，一边仰视着你。")
            messages.append("完全像是一只发春的牝犬一样。")
            messages.append(f"{char_name}获得了【牝犬】。")
            target.talent[136] = 1

        if target.talent.get(74, 0) and target.talent.get(75, 0) and target.talent.get(77, 0) and target.talent.get(78, 0):
            pass
        else:
            sexskill_count = 0
            if target.talent.get(74, 0):
                sexskill_count += 1
            if target.talent.get(75, 0):
                sexskill_count += 1
            if target.talent.get(77, 0):
                sexskill_count += 1
            if target.talent.get(78, 0):
                sexskill_count += 1

            sexskill_exp_1 = 100 + 50 * sexskill_count
            sexskill_exp_2 = 100 + 10 * sexskill_count
            sexskill_exp_3 = 300 + 50 * sexskill_count

            if sexskill_count == 4:
                pass
            elif sexskill_count == 0:
                messages.extend(self._add_sexskill(target, sexskill_exp_1, sexskill_exp_2, sexskill_exp_3))
            else:
                can_add = False
                if (target.talent.get(74, 0) == 0 and target.abl.get(0, 0) >= 5
                        and target.exp.get(11, 0) >= sexskill_exp_1 and target.exp.get(2, 0) >= sexskill_exp_2):
                    can_add = True
                elif (target.talent.get(75, 0) == 0 and target.talent.get(122, 0)
                      and target.abl.get(0, 0) >= 5
                      and target.exp.get(5, 0) >= sexskill_exp_3 and target.exp.get(2, 0) >= sexskill_exp_1):
                    can_add = True
                elif (target.talent.get(75, 0) == 0 and target.abl.get(2, 0) >= 5
                      and target.exp.get(0, 0) >= sexskill_exp_3 and target.exp.get(2, 0) >= sexskill_exp_2):
                    can_add = True
                elif (target.talent.get(77, 0) == 0 and target.abl.get(3, 0) >= 5
                      and target.exp.get(32, 0) >= sexskill_exp_3 and target.exp.get(2, 0) >= sexskill_exp_2):
                    can_add = True
                elif (target.talent.get(78, 0) == 0 and target.talent.get(122, 0)
                      and target.abl.get(1, 0) >= 5
                      and target.juel.get(14, 0) >= sexskill_exp_1 and target.exp.get(2, 0) >= sexskill_exp_2):
                    can_add = True
                elif (target.talent.get(78, 0) == 0 and target.abl.get(1, 0) >= 5
                      and target.exp.get(54, 0) >= sexskill_exp_1 and target.exp.get(2, 0) >= sexskill_exp_2):
                    can_add = True

                if can_add:
                    messages.extend(self._add_sexskill(target, sexskill_exp_1, sexskill_exp_2, sexskill_exp_3))

        if int(v.flags.get(73, 0)) <= 0:
            if (target.abl.get(0, 0) >= 5 and target.exp.get(11, 0) >= 100
                    and target.exp.get(2, 0) >= 300 and target.talent.get(230, 0) == 0):
                if target.talent.get(122, 0):
                    messages.append(f"{char_name}获得了【绝伦】。")
                else:
                    messages.append(f"{char_name}获得了【淫核】。")
                target.talent[230] = 1

            if (target.abl.get(2, 0) >= 5 and target.exp.get(0, 0) >= 300
                    and target.exp.get(2, 0) >= 300 and target.talent.get(232, 0) == 0):
                messages.append(f"{char_name}获得了【淫壶】。")
                target.talent[232] = 1

            if (target.abl.get(3, 0) >= 5 and target.exp.get(32, 0) >= 300
                    and target.exp.get(2, 0) >= 300 and target.talent.get(233, 0) == 0):
                messages.append(f"{char_name}获得了【淫肛】。")
                target.talent[233] = 1

            if (target.abl.get(1, 0) >= 5 and target.exp.get(54, 0) >= 100
                    and target.exp.get(2, 0) >= 300 and target.talent.get(231, 0) == 0):
                messages.append(f"{char_name}获得了【淫乳】。")
                target.talent[231] = 1

            if (target.talent.get(230, 0) and target.talent.get(231, 0)
                    and target.talent.get(232, 0) and target.talent.get(233, 0)
                    and target.talent.get(272, 0) == 0):
                messages.append(f"{char_name}获得了【性豪】。")
                target.talent[272] = 1
                for dunsense_id in [101, 103, 105, 107]:
                    if target.talent.get(dunsense_id, 0):
                        dunsense_name = {101: "阴蒂钝感", 103: "私处钝感", 105: "肛门钝感", 107: "乳房钝感"}.get(dunsense_id, "")
                        messages.append(f"{char_name}失去了【{dunsense_name}】。")
                        target.talent[dunsense_id] = 0

        if int(v.flags.get(75, 0)) <= 0:
            if target.talent.get(271, 0) == 0:
                if target.cflag.get(81, 0) >= 700 and target.cflag.get(82, 0) >= 2250:
                    messages.append(f"{char_name}最近总是面带红霞…")
                    messages.append(f"{char_name}获得了【时常发情】。")
                    target.talent[271] = 1

                    if target.talent.get(43, 0) == 0 and target.talent.get(42, 0) == 0:
                        messages.append(f"{char_name}获得了【容易湿】。")
                        target.talent[42] = 1
                    elif target.talent.get(43, 0):
                        messages.append(f"{char_name}失去了【不易湿】。")
                        target.talent[43] = 0

                    if target.talent.get(32, 0) or target.talent.get(34, 0) or target.talent.get(84, 0):
                        lost = []
                        if target.talent.get(32, 0):
                            lost.append("【压抑】")
                            target.talent[32] = 0
                        if target.talent.get(34, 0):
                            lost.append("【抵抗】")
                            target.talent[34] = 0
                        if target.talent.get(84, 0):
                            lost.append("【嫉妒】")
                            target.talent[84] = 0
                        messages.append(f"{char_name}的{''.join(lost)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = target.juel.get(100, 0) // 2

                    if target.talent.get(71, 0):
                        messages.append(f"{char_name}失去了【否定快感】。")
                        target.talent[71] = 0

                    if target.talent.get(30, 0):
                        messages.append(f"{char_name}失去了【看重贞操】。")
                        target.talent[30] = 0

        if v.tflag.get(110, 0) and target.talent.get(47, 0) == 0 and seiin:
            messages.append(f"{char_name}最近一见到你，就感到舌干唇燥…")
            messages.append(f"{char_name}在没有任何性刺激的情况下，也渴望着饮精液了。")
            messages.append(f"{char_name}获得了【喜欢精液】。")
            target.talent[47] = 1

            if target.talent.get(62, 0):
                messages.append(f"{char_name}失去了【反感污臭】。")
                target.talent[62] = 0

            if target.abl.get(32, 0) < 3:
                messages.append(f"{char_name}的精液中毒LV3了。")
                target.abl[32] = 3

            v.tflag[110] = 0

        if target.abl.get(16, 0) >= 5 and target.talent.get(151, 0):
            messages.append(f"{char_name}失去了【绝不侍奉】。")
            target.talent[151] = 0

        if target.abl.get(31, 0) >= 5 and target.talent.get(150, 0):
            messages.append(f"{char_name}失去了【从不自慰】。")
            target.talent[150] = 0

        if int(v.flags.get(30, 0)) >= 5 and player is not None and player.talent.get(92, 0) == 0:
            messages.append(f"{getattr(player, 'savestr', player.name or '主人')}掌握了【谜之魅力】。")
            player.talent[92] = 1

        if (target.talent.get(315, 0) == 5 and target.exp.get(74, 0) >= 80
                and target.mark.get(3, 0) == 0 and target.abl.get(11, 0) >= 1
                and target.talent.get(180, 0) == 0):
            messages.append(f"{char_name}无法逃离作为妓女的生活方式……")
            messages.append(f"{char_name}获得了【妓女】。")
            target.talent[180] = 1
        elif (target.exp.get(74, 0) >= 100 and target.mark.get(3, 0) == 0
              and target.abl.get(11, 0) >= 2 and target.abl.get(12, 0) >= 1
              and target.talent.get(180, 0) == 0):
            messages.append(f"{char_name}以出卖肉体为主要的生活方式……")
            messages.append(f"{char_name}获得了【妓女】。")
            target.talent[180] = 1

        if (target.talent.get(315, 0) == 5 and target.exp.get(74, 0) >= 160
                and target.mark.get(3, 0) == 0 and target.talent.get(180, 0) == 1
                and target.talent.get(181, 0) == 0):
            messages.append(f"{char_name}热衷于从事分开双腿的工作……")
            messages.append(f"{char_name}获得了【倾城】。")
            target.talent[181] = 1
        elif (target.exp.get(74, 0) >= 200 and target.mark.get(3, 0) == 0
              and target.talent.get(180, 0) == 1 and target.talent.get(181, 0) == 0):
            messages.append(f"{char_name}热衷于从事分开双腿的工作……")
            messages.append(f"{char_name}获得了【倾城】。")
            target.talent[181] = 1

        if (target.talent.get(85, 0) and target.exp.get(81, 0) >= 5
                and target.mark.get(3, 0) == 0 and target.abl.get(10, 0) >= 4
                and target.talent.get(86, 0) == 0):
            messages.append("爱会使人盲目的吗？我们也许不得而知。")
            messages.append(f"但{char_name}对你，却一定是盲目的……")
            messages.append(f"{char_name}获得了【盲从】。")
            target.talent[86] = 1
        elif (target.talent.get(76, 0) and target.exp.get(81, 0) >= 10
              and target.mark.get(3, 0) == 0 and target.abl.get(10, 0) >= 5
              and target.talent.get(86, 0) == 0):
            messages.append("放荡的人，很难谈得上有什么纪律意识。")
            messages.append(f"但通过出色的调教，淫乱的{char_name}已经对你言听计从了……")
            messages.append(f"{char_name}获得了【盲从】。")
            target.talent[86] = 1

        if target.exp.get(76, 0) >= 60 and target.talent.get(188, 0) == 0:
            messages.append(f"{char_name}在死斗场获得了超绝的人气……")
            messages.append(f"{char_name}获得【闘姫】了")
            target.talent[188] = 1

        messages.extend(self._check_special_skill_bodyshift(target))
        return messages






    def _check_special_skill_bodyshift(self, target: Character) -> List[str]:
        messages: List[str] = []
        char_name = getattr(target, 'savestr', target.name or target.callname or "")

        if target.exp.get(62, 0) >= 20 and target.talent.get(158, 0) == 0:
            messages.append(f"{char_name}生育了太多异种的孩子，已经无法为同族生育了。")
            messages.append(f"{char_name}获得了【同族不育】")
            target.talent[158] = 1

        return messages






    def _check_special_talent(self, target, player, seiin: int = 0) -> List[str]:
        """特殊素质获取判定 - 对应 ERB/GET_SPECIALTALENT.ERB

        在调教后自动判定角色是否获得新素质。
        Args:
            target: 调教对象 (Character)
            player: 主人 (Character)
            seiin: 强制精饮参数 (默认0)
        Returns:
            获取提示消息列表
        """
        messages: List[str] = []

        # 崩壊している場合は肉体強制変化のみ
        if int(target.talent.get(9, 0)) != 0:
            messages.extend(self._check_special_talent_bodyshift(target))
            return messages

        # ---- 反抗刻印がない場合の判定 ----
        if int(target.mark.get(3, 0)) == 0:

            # 1. 売却・助手資格判定 (CFLAG:2 >= 2000 且 CFLAG:0 < 2 且 淫乱/愛慕)
            if (int(target.cflag.get(2, 0)) >= 2000
                    and int(target.cflag.get(0, 0)) < 2
                    and (int(target.talent.get(76, 0)) != 0 or int(target.talent.get(85, 0)) != 0)):
                messages.append(f"{target.name} 带着崇敬的眼神看着你……")
                messages.append(f"{target.name} 无论是灵魂还是肉体，都全心全意地献给你了……")
                if int(target.abl.get(10, 0)) < 5:
                    target.abl[10] = 5
                    messages.append("顺从LV5了")
                if int(target.cflag.get(0, 0)) < 1:
                    messages.append(f"{target.name} 可以被卖掉了。")
                messages.append(f"{target.name} 可以做助手了。")
                target.cflag[0] = 2

            # CFLAG:2 >= 1000 の判定群
            elif int(target.cflag.get(2, 0)) >= 1000:

                # 2. 愛慕取得
                if (int(target.abl.get(10, 0)) >= 3
                        and int(target.exp.get(21, 0)) >= 200
                        and int(target.talent.get(76, 0)) == 0
                        and int(target.talent.get(85, 0)) == 0
                        and int(target.talent.get(184, 0)) == 0
                        and int(target.mark.get(2, 0)) == 3
                        and int(target.abl.get(16, 0)) >= 3):
                    messages.append(f"{target.name} 柔情似水地看着你……")
                    messages.append(f"{target.name} 因你的行为而感到喜悦。想粘着你，想为你分忧，为你做些什么……渴望着你的宠爱。")
                    target.talent[85] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(85)}】。")
                    # 堕とし人数+1
                    if int(target.talent.get(76, 0)) == 0:
                        self.interpreter.vars.set_flag(30, int(self.interpreter.vars.get_flag(30, 0)) + 1)
                    # 傲嬌+反抗 → 坦率
                    if int(target.talent.get(11, 0)) != 0 and int(target.talent.get(18, 0)) != 0:
                        target.talent[11] = 0
                        target.talent[13] = 1
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(11)}】，获得了【{self._get_talent_name(13)}】。")
                    elif int(target.talent.get(11, 0)) != 0:
                        target.talent[11] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(11)}】。")
                    # 克制/冷漠 → 消失
                    if int(target.talent.get(20, 0)) != 0 or int(target.talent.get(21, 0)) != 0:
                        lost_names = []
                        if int(target.talent.get(20, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(20)}】")
                            target.talent[20] = 0
                        if int(target.talent.get(21, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(21)}】")
                            target.talent[21] = 0
                        messages.append(f"{target.name} 的{''.join(lost_names)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = int(target.juel.get(100, 0)) // 2
                    # 一線 → 消失
                    if int(target.talent.get(27, 0)) != 0:
                        target.talent[27] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(27)}】。")
                    # 絶不侍奉 → 消失
                    if int(target.talent.get(151, 0)) != 0:
                        target.talent[151] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(151)}】。")
                    # 嫉妬 → 消失
                    if int(target.talent.get(84, 0)) != 0:
                        target.talent[84] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(84)}】。")
                    # 寿命持ち
                    if int(target.base.get(10, 0)) > 0:
                        remaining_days = int(target.base.get(10, 0)) // 2
                        messages.append(f"{target.name} 时日无多，生命还剩下{remaining_days}天。")
                    # 魂縛 → 消失
                    if int(target.talent.get(274, 0)) != 0:
                        target.talent[274] = 0
                        messages.append(f"{target.name} 被束缚的灵魂，在向自己的爱与欲望屈服时被解放了。")
                        messages.append(f"{target.name} 失去了【魂缚】。")
                    # 貞操封印 → 選択
                    messages.extend(self._check_special_talent_shojo_seal_release(target))
                    # 瑪奥(NO:17) → EX_TALENT:3
                    messages.extend(self._check_special_talent_maou_ex_talent(target))

                # 3. 淫乱取得
                sensory_total = sum(int(target.abl.get(idx, 0)) for idx in range(4))
                if (int(target.abl.get(11, 0)) >= 3
                        and sensory_total >= 10
                        and int(target.exp.get(50, 0)) >= 3
                        and int(target.talent.get(85, 0)) == 0
                        and int(target.talent.get(76, 0)) == 0
                        and int(target.mark.get(1, 0)) == 3
                        and int(target.mark.get(2, 0)) == 3):
                    messages.append(f"{target.name} 看你的眼神，好像忘记了你还有上半身……")
                    messages.append(f"{target.name} 沉迷于你给予的快感之中了……")
                    target.talent[76] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(76)}】。")
                    # 堕とし人数+1
                    if int(target.talent.get(85, 0)) == 0:
                        self.interpreter.vars.set_flag(30, int(self.interpreter.vars.get_flag(30, 0)) + 1)
                    # 克制/冷漠 → 消失
                    if int(target.talent.get(20, 0)) != 0 or int(target.talent.get(21, 0)) != 0:
                        lost_names = []
                        if int(target.talent.get(20, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(20)}】")
                            target.talent[20] = 0
                        if int(target.talent.get(21, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(21)}】")
                            target.talent[21] = 0
                        messages.append(f"{target.name} 的{''.join(lost_names)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = int(target.juel.get(100, 0)) // 2
                    # 一線 → 消失
                    if int(target.talent.get(27, 0)) != 0:
                        target.talent[27] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(27)}】。")
                    # 压抑/抵抗/嫉妒 → 消失
                    if int(target.talent.get(32, 0)) != 0 or int(target.talent.get(34, 0)) != 0 or int(target.talent.get(84, 0)) != 0:
                        lost_names = []
                        if int(target.talent.get(32, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(32)}】")
                            target.talent[32] = 0
                        if int(target.talent.get(34, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(34)}】")
                            target.talent[34] = 0
                        if int(target.talent.get(84, 0)) != 0:
                            lost_names.append(f"【{self._get_talent_name(84)}】")
                            target.talent[84] = 0
                        messages.append(f"{target.name} 的{''.join(lost_names)}失去了。")
                        messages.append("否定点数减半。")
                        target.juel[100] = int(target.juel.get(100, 0)) // 2
                    # 否定快感 → 消失
                    if int(target.talent.get(71, 0)) != 0:
                        target.talent[71] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(71)}】。")
                    # 従不自慰 → 消失
                    if int(target.talent.get(150, 0)) != 0:
                        target.talent[150] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(150)}】。")
                    # 悪堕種族変化
                    if int(target.talent.get(274, 0)) == 0:
                        messages.extend(self._check_special_talent_corruption_race_fall(target))
                    # 貞操封印 → 選択
                    messages.extend(self._check_special_talent_shojo_seal_release(target))
                    # 瑪奥(NO:17) → EX_TALENT:3
                    messages.extend(self._check_special_talent_maou_ex_talent(target))

                # 4. 高順従消除 (CFLAG:2 >= 5000, 順従5, 快楽/屈服刻印3)
                if (int(target.cflag.get(2, 0)) >= 5000
                        and int(target.abl.get(10, 0)) >= 5
                        and int(target.mark.get(1, 0)) == 3
                        and int(target.mark.get(2, 0)) == 3):
                    for tid in (150, 151, 152):
                        if int(target.talent.get(tid, 0)) != 0:
                            target.talent[tid] = 0
                            messages.append(f"{target.name} 失去了【{self._get_talent_name(tid)}】。")

        # ---- 5. 喜歓精液取得 ----
        if int(target.talent.get(47, 0)) == 0:
            technique_abl = int(target.abl.get(12, 0))
            service_abl = int(target.abl.get(13, 0))
            oral_exp = int(target.exp.get(22, 0))
            cflag_600 = int(target.cflag.get(600, 0))
            if technique_abl >= 7 and service_abl >= 7 and oral_exp >= 2000 and int(target.talent.get(52, 0)) == 0 and cflag_600 >= 100:
                messages.append(f"{target.name} 因为不断地强制精饮绝顶，终于完全适应了精液的味道……")
                messages.append("甚至还喜欢上了。")
                target.talent[47] = 1
                messages.append(f"{target.name} 获得了【{self._get_talent_name(47)}】。")
            elif technique_abl >= 5 and service_abl >= 5 and oral_exp >= 1500 and int(target.talent.get(52, 0)) == 0 and cflag_600 >= 80:
                messages.append(f"{target.name} 喜欢上了精液的味道……")
                target.talent[47] = 1
                messages.append(f"{target.name} 获得了【{self._get_talent_name(47)}】。")
            elif technique_abl >= 5 and service_abl >= 5 and oral_exp >= 1000 and int(target.talent.get(52, 0)) != 0 and cflag_600 >= 50:
                messages.append(f"{target.name} 感到似乎离不开精液了……")
                target.talent[47] = 1
                messages.append(f"{target.name} 获得了【{self._get_talent_name(47)}】。")

        # ---- 6. 擅用舌頭取得 ----
        if int(target.talent.get(52, 0)) == 0:
            technique_abl = int(target.abl.get(12, 0))
            service_abl = int(target.abl.get(13, 0))
            oral_exp = int(target.exp.get(22, 0))
            if int(target.talent.get(51, 0)) != 0:
                # 学習緩慢あり
                if technique_abl >= 7 and service_abl >= 7 and oral_exp >= 1500:
                    messages.append(f"{target.name} 通过持续的侍奉，侍奉技术获得了飞跃的进步……")
                    target.talent[52] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(52)}】。")
            else:
                if technique_abl >= 5 and service_abl >= 5 and oral_exp >= 1000:
                    messages.append(f"{target.name} 的侍奉技术精进了……")
                    target.talent[52] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(52)}】。")

        # ---- 7. 施虐狂取得 ----
        if (int(target.abl.get(20, 0)) >= 4
                and int(target.abl.get(12, 0)) >= 4
                and int(target.exp.get(33, 0)) >= 300
                and int(target.talent.get(83, 0)) == 0):
            messages.append(f"{target.name} 的眼神变得凌厉了……")
            messages.append(f"{target.name} 学会了将快乐建立在他人的痛苦之上。")
            target.talent[83] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(83)}】。")

        # ---- 8. 受虐狂取得 ----
        if (int(target.abl.get(21, 0)) >= 4
                and int(target.abl.get(17, 0)) >= 2
                and int(target.exp.get(30, 0)) >= 300
                and int(target.talent.get(88, 0)) == 0):
            messages.append(f"{target.name} 的眼神变得卑微了……")
            messages.append(f"{target.name} 将痛楚和快感视为一体，学会了享受被支配，被凌辱的喜悦。")
            target.talent[88] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(88)}】。")

        # ---- 9. 露出狂取得 ----
        if (int(target.abl.get(17, 0)) >= 4
                and int(target.abl.get(21, 0)) >= 2
                and int(target.exp.get(11, 0)) + int(target.exp.get(31, 0)) + int(target.exp.get(54, 0)) >= 200
                and int(target.talent.get(89, 0)) == 0):
            messages.append(f"{target.name} 的神情变得害羞……")
            messages.append("但是，却学会了将这份羞耻变成快感。将自己的被羞辱的姿态呈现他人，令她感到身心无比圆满。")
            target.talent[89] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(89)}】。")

        # ---- 10. 牝犬取得 ----
        if (int(target.abl.get(11, 0)) >= 5
                and int(target.abl.get(39, 0)) >= 3
                and int(target.exp.get(56, 0)) >= 300
                and int(target.talent.get(136, 0)) == 0):
            messages.append(f"{target.name} 的行为彻底变化了……")
            messages.append("整天喜欢四脚爬爬地在地上爬行，一边扭腰抬臀，一边仰视着你。")
            messages.append("完全像是一只发春的牝犬一样。")
            target.talent[136] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(136)}】。")

        # ---- 11. 特殊性感素質 ----
        if not all(int(target.talent.get(t, 0)) != 0 for t in (74, 75, 77, 78)):
            sexskill_count = sum(1 for t in (74, 75, 77, 78) if int(target.talent.get(t, 0)) != 0)
            if sexskill_count < 4:
                can_gain = False
                if sexskill_count == 0:
                    can_gain = True
                else:
                    exp_req_masturbation = 100 + 50 * sexskill_count
                    exp_req_orgasm = 100 + 10 * sexskill_count
                    exp_req_penetration = 300 + 50 * sexskill_count
                    can_gain = (
                        (int(target.talent.get(74, 0)) == 0 and int(target.abl.get(0, 0)) >= 5 and int(target.exp.get(11, 0)) >= exp_req_masturbation and int(target.exp.get(2, 0)) >= exp_req_orgasm)
                        or (int(target.talent.get(75, 0)) == 0 and int(target.talent.get(122, 0)) != 0 and int(target.abl.get(0, 0)) >= 5 and int(target.exp.get(5, 0)) >= exp_req_penetration and int(target.exp.get(2, 0)) >= exp_req_masturbation)
                        or (int(target.talent.get(75, 0)) == 0 and int(target.abl.get(2, 0)) >= 5 and int(target.exp.get(0, 0)) >= exp_req_penetration and int(target.exp.get(2, 0)) >= exp_req_orgasm)
                        or (int(target.talent.get(77, 0)) == 0 and int(target.abl.get(3, 0)) >= 5 and int(target.exp.get(32, 0)) >= exp_req_penetration and int(target.exp.get(2, 0)) >= exp_req_orgasm)
                        or (int(target.talent.get(78, 0)) == 0 and int(target.talent.get(122, 0)) != 0 and int(target.abl.get(1, 0)) >= 5 and int(target.juel.get(14, 0)) >= exp_req_masturbation and int(target.exp.get(2, 0)) >= exp_req_orgasm)
                        or (int(target.talent.get(78, 0)) == 0 and int(target.abl.get(1, 0)) >= 5 and int(target.exp.get(54, 0)) >= exp_req_masturbation and int(target.exp.get(2, 0)) >= exp_req_orgasm)
                    )
                if can_gain:
                    messages.extend(self._check_special_talent_sex_skill(target))

        # ---- 12. 強化素質 (FLAG:73 <= 0) ----
        if int(self.interpreter.vars.get_flag(73, 0)) <= 0:
            # 淫核 (C感覚5+ 自慰経験100+ 絶頂経験300+)
            if (int(target.abl.get(0, 0)) >= 5
                    and int(target.exp.get(11, 0)) >= 100
                    and int(target.exp.get(2, 0)) >= 300
                    and int(target.talent.get(230, 0)) == 0):
                target.talent[230] = 1
                relieve = "他缓解" if int(target.talent.get(122, 0)) != 0 else "她解除"
                organ = "阴茎的肿涨。" if int(target.talent.get(121, 0)) != 0 or int(target.talent.get(122, 0)) != 0 else "阴蒂的肿痛。"
                reaction = "他便喘息了起来，" if int(target.talent.get(122, 0)) != 0 else "她便高声娇喘起来，"
                talent_name = "绝伦" if int(target.talent.get(122, 0)) != 0 else self._get_talent_name(230)
                messages.append(f"{target.name} 好像无法停止娇媚的呻吟，")
                messages.append(f"{target.name}在调教结束之后依然哀求着你为{relieve}{organ}")
                messages.append(f"但一摸下去，{reaction}越来越亢奋了……")
                messages.append(f"{target.name} 获得了【{talent_name}】。")

            # 淫壺 (V感覚5+ 私処経験300+ 絶頂経験300+)
            if (int(target.abl.get(2, 0)) >= 5
                    and int(target.exp.get(0, 0)) >= 300
                    and int(target.exp.get(2, 0)) >= 300
                    and int(target.talent.get(232, 0)) == 0):
                target.talent[232] = 1
                messages.append(f"{target.name} 不停地发出【唔～唔～唔……】的勾魂声音……")
                messages.append(f"{target.name}在调教结束之后依然哀求着你疼爱她的子宫。但一插进去，她便全身夸张地痉挛了起来，子宫口依依不舍地紧紧吸啜着龟头……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(232)}】。")

            # 淫肛 (A感覚5+ 肛門快楽経験300+ 絶頂経験300+)
            if (int(target.abl.get(3, 0)) >= 5
                    and int(target.exp.get(32, 0)) >= 300
                    and int(target.exp.get(2, 0)) >= 300
                    and int(target.talent.get(233, 0)) == 0):
                target.talent[233] = 1
                messages.append(f"{target.name} 用舌头轻轻地舔着嘴唇……")
                messages.append(f"{target.name}在调教结束之后依然哀求着你疼爱她的尻穴。但一插进去，她便全身夸张地痉挛了起来，直肠疯狂地蠕动，摩擦着阴茎……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(233)}】。")

            # 淫乳 (B感覚5+ 噴乳経験100+ 絶頂経験300+)
            if (int(target.abl.get(1, 0)) >= 5
                    and int(target.exp.get(54, 0)) >= 100
                    and int(target.exp.get(2, 0)) >= 300
                    and int(target.talent.get(231, 0)) == 0):
                target.talent[231] = 1
                messages.append(f"{target.name} 主动引导你的手推拿自己的胸部……")
                messages.append(f"{target.name}在调教结束之后依然哀求着你玩弄她的胸部。但一摸下去，她便昂首咬牙，爱液四射，高声娇喘起来了……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(231)}】。")

            # 13. 性豪 (四強化素質全部取得)
            if (int(target.talent.get(230, 0)) != 0
                    and int(target.talent.get(231, 0)) != 0
                    and int(target.talent.get(232, 0)) != 0
                    and int(target.talent.get(233, 0)) != 0
                    and int(target.talent.get(272, 0)) == 0):
                target.talent[272] = 1
                messages.append(f"{target.name} 获得了【{self._get_talent_name(272)}】。")
                for tid in (101, 103, 105, 107):
                    if int(target.talent.get(tid, 0)) != 0:
                        target.talent[tid] = 0
                        messages.append(f"{target.name} 失去了【{self._get_talent_name(tid)}】。")

        # ---- 14. 時常発情 (FLAG:75 <= 0) ----
        if int(self.interpreter.vars.get_flag(75, 0)) <= 0:
            if (int(target.talent.get(271, 0)) == 0
                    and int(target.cflag.get(81, 0)) >= 700
                    and int(target.cflag.get(82, 0)) >= 2250):
                target.talent[271] = 1
                messages.append(f"{target.name} 最近总是面带红霞……")
                # 体液描写
                parts: List[str] = []
                if int(target.talent.get(122, 0)) != 0 or int(target.talent.get(121, 0)) != 0:
                    parts.append("龟头")
                if int(target.talent.get(121, 0)) != 0:
                    parts.append("私处")
                elif int(target.talent.get(122, 0)) == 0:
                    parts.append("私处")
                messages.append(f"{target.name} 的{'和'.join(parts)}总是有透明的爱液滚滚涌出……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(271)}】。")
                # 容易湿追加 / 不易湿消失
                if int(target.talent.get(43, 0)) == 0 and int(target.talent.get(42, 0)) == 0:
                    target.talent[42] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(42)}】。")
                elif int(target.talent.get(43, 0)) != 0:
                    target.talent[43] = 0
                    messages.append(f"{target.name} 失去了【{self._get_talent_name(43)}】。")
                # 压抑/抵抗/嫉妒 → 消失
                if int(target.talent.get(32, 0)) != 0 or int(target.talent.get(34, 0)) != 0 or int(target.talent.get(84, 0)) != 0:
                    lost_names = []
                    if int(target.talent.get(32, 0)) != 0:
                        lost_names.append(f"【{self._get_talent_name(32)}】")
                        target.talent[32] = 0
                    if int(target.talent.get(34, 0)) != 0:
                        lost_names.append(f"【{self._get_talent_name(34)}】")
                        target.talent[34] = 0
                    if int(target.talent.get(84, 0)) != 0:
                        lost_names.append(f"【{self._get_talent_name(84)}】")
                        target.talent[84] = 0
                    messages.append(f"{target.name} 的{''.join(lost_names)}失去了。")
                    messages.append("否定点数减半。")
                    target.juel[100] = int(target.juel.get(100, 0)) // 2
                # 否定快感 → 消失
                if int(target.talent.get(71, 0)) != 0:
                    target.talent[71] = 0
                    messages.append(f"{target.name} 失去了【{self._get_talent_name(71)}】。")
                # 看重貞操 → 消失
                if int(target.talent.get(30, 0)) != 0:
                    target.talent[30] = 0
                    messages.append(f"{target.name} 失去了【{self._get_talent_name(30)}】。")

        # ---- 15. 強制精飲 → 喜歓精液 (TFLAG:110 且 SEIIN) ----
        if int(self.interpreter.vars.tflag.get(110, 0)) != 0 and int(target.talent.get(47, 0)) == 0 and seiin:
            messages.append(f"{target.name} 最近一见到你，就感到舌干唇燥……")
            messages.append(f"{target.name} 在没有任何性刺激的情况下，也渴望着饮精液了。")
            target.talent[47] = 1
            messages.append(f"{target.name} 获得了【{self._get_talent_name(47)}】。")
            # 反感汚臭 → 消失
            if int(target.talent.get(62, 0)) != 0:
                target.talent[62] = 0
                messages.append(f"{target.name} 失去了【{self._get_talent_name(62)}】。")
            # 精液中毒LV3
            if int(target.abl.get(32, 0)) < 3:
                target.abl[32] = 3
                messages.append(f"{target.name} 的精液中毒LV3了。")
            # 取得フラグリセット
            self.interpreter.vars.tflag[110] = 0

        # ---- 16. 負面素質消失 ----
        if int(target.abl.get(16, 0)) >= 5 and int(target.talent.get(151, 0)) != 0:
            target.talent[151] = 0
            messages.append(f"{target.name} 失去了【{self._get_talent_name(151)}】。")
        if int(target.abl.get(31, 0)) >= 5 and int(target.talent.get(150, 0)) != 0:
            target.talent[150] = 0
            messages.append(f"{target.name} 失去了【{self._get_talent_name(150)}】。")

        # ---- 17. 主人謎之魅力 (堕とし人数5+) ----
        if player is not None:
            if int(self.interpreter.vars.get_flag(30, 0)) >= 5 and int(player.talent.get(92, 0)) == 0:
                player.talent[92] = 1
                messages.append(f"{player.name} 掌握了【{self._get_talent_name(92)}】。")

        # ---- 18. 妓女/傾城取得 ----
        # 妓女
        if int(target.talent.get(180, 0)) == 0 and int(target.mark.get(3, 0)) == 0:
            prostitution_exp = int(target.exp.get(74, 0))
            if int(target.talent.get(315, 0)) == 5:
                if prostitution_exp >= 80 and int(target.abl.get(11, 0)) >= 1:
                    messages.append(f"{target.name} 无法逃离作为妓女的生活方式……")
                    target.talent[180] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(180)}】。")
            else:
                if prostitution_exp >= 100 and int(target.abl.get(11, 0)) >= 2 and int(target.abl.get(12, 0)) >= 1:
                    messages.append(f"{target.name} 以出卖肉体为主要的生活方式……")
                    target.talent[180] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(180)}】。")

        # 傾城
        if (int(target.talent.get(181, 0)) == 0
                and int(target.talent.get(180, 0)) != 0
                and int(target.mark.get(3, 0)) == 0):
            prostitution_exp = int(target.exp.get(74, 0))
            if int(target.talent.get(315, 0)) == 5:
                if prostitution_exp >= 160:
                    messages.append(f"{target.name} 热衷于从事分开双腿的工作……")
                    target.talent[181] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(181)}】。")
            else:
                if prostitution_exp >= 200:
                    messages.append(f"{target.name} 热衷于从事分开双腿的工作……")
                    target.talent[181] = 1
                    messages.append(f"{target.name} 获得了【{self._get_talent_name(181)}】。")

        # ---- 19. 妄信取得 ----
        if int(target.talent.get(86, 0)) == 0 and int(target.mark.get(3, 0)) == 0:
            medal_exp = int(target.exp.get(81, 0))
            obedience = int(target.abl.get(10, 0))
            if int(target.talent.get(85, 0)) != 0 and medal_exp >= 5 and obedience >= 4:
                target.talent[86] = 1
                messages.append("爱会使人盲目的吗？我们也许不得而知。")
                messages.append(f"但{target.name}对你，却一定是盲目的……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(86)}】。")
            elif int(target.talent.get(76, 0)) != 0 and medal_exp >= 10 and obedience >= 5:
                target.talent[86] = 1
                messages.append("放荡的人，很难谈得上有什么纪律意识。")
                messages.append(f"但通过出色的调教，淫乱的{target.name}已经对你言听计从了……")
                messages.append(f"{target.name} 获得了【{self._get_talent_name(86)}】。")

        # ---- 20. 肉体強制変化 ----
        messages.extend(self._check_special_talent_bodyshift(target))

        return messages






    def _check_special_talent_bodyshift(self, target) -> List[str]:
        """肉体強制変化 (異種妊娠経験20+ → 同族妊娠不可 TALENT:158)"""
        if int(target.exp.get(62, 0)) < 20:
            return []
        if int(target.talent.get(158, 0)) != 0:
            return []
        target.talent[158] = 1
        return [
            f"{target.name} 生育了太多异种的孩子，已经无法为同族生育了。",
            f"{target.name} 获得了【{self._get_talent_name(158)}】。",
        ]

    # ========================================
    # FULLMOON - 满月效果系统
    # 对应 ERB/FULLMOON.ERB
    # ========================================






    def _check_special_talent_corruption_race_fall(self, target) -> List[str]:
        """悪堕種族変化 (精霊314:1→7, 314:6→8)"""
        race_id = int(target.talent.get(314, 0))
        if race_id == 1:
            target.talent[314] = 7
            self._apply_turn_end_corruption_brown_skin(target)
            return [f"{target.name} 从高洁的精灵，堕落为卑微的肉壶了。"]
        if race_id == 6:
            target.talent[314] = 8
            self._apply_turn_end_corruption_brown_skin(target)
            return [f"{target.name} 纯洁的灵魂完全堕落了，成为了被淫靡欲望所支配的下等性奴隶。"]
        return []






    def _check_special_talent_maou_ex_talent(self, target) -> List[str]:
        """瑪奥替身判定 (NO:17 → EX_TALENT:3)"""
        if int(self._get_character_template_id(target) or 0) != 17:
            return []
        if int(self._get_character_ex_talent(target, 3)) != 0:
            return []
        self._set_character_ex_talent(target, 3, 1)
        return [f"{target.name} 一阵眩晕、似乎拥有了【替身】的素质……"]






    def _check_special_talent_sex_skill(self, target) -> List[str]:
        """特殊性感素質の取得判定（自慰狂/性愛狂/尻穴狂/弄乳狂）"""
        # 自慰狂 (C感覚4+ 調教自慰経験100+ 絶頂経験100+)
        if (int(target.abl.get(0, 0)) >= 4
                and int(target.exp.get(11, 0)) >= 100
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(74, 0)) == 0):
            target.talent[74] = 1
            organ_name = "阴茎" if int(target.talent.get(121, 0)) != 0 or int(target.talent.get(122, 0)) != 0 else "阴蒂"
            return [
                f"总觉得最近，{target.name}连呼吸都变得色情了起来……",
                f"调教结束之后，{target.name}当着你的面，肆无忌惮地继续玩弄着自己的{organ_name}。",
                f"{target.name} 获得了【{self._get_talent_name(74)}】。",
            ]
        # 性愛狂 (V感覚4+ 私処経験300+ 絶頂経験100+)
        if (int(target.abl.get(2, 0)) >= 4
                and int(target.exp.get(0, 0)) >= 300
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(75, 0)) == 0):
            target.talent[75] = 1
            return [
                f"{target.name} 最近对私处的运用，越来越炉火纯青……",
                f"调教结束之后，{target.name}依依不舍地抱着你，恳求着欢好。",
                f"{target.name} 获得了【{self._get_talent_name(75)}】。",
            ]
        # 性愛狂 (扶他: C感覚4+ 挿入経験300+ 絶頂経験100+)
        if (int(target.talent.get(122, 0)) != 0
                and int(target.abl.get(0, 0)) >= 4
                and int(target.exp.get(5, 0)) >= 300
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(75, 0)) == 0
                and int(target.talent.get(74, 0)) == 0):
            target.talent[75] = 1
            return [
                f"{target.name} 最近对性器的运用，越来越炉火纯青……",
                f"调教结束之后，{target.name}依依不舍地抱着你，恳求着欢好。",
                f"{target.name} 获得了【{self._get_talent_name(75)}】。",
            ]
        # 尻穴狂 (A感覚4+ 肛門快楽経験300+ 絶頂経験100+)
        if (int(target.abl.get(3, 0)) >= 4
                and int(target.exp.get(32, 0)) >= 300
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(77, 0)) == 0):
            target.talent[77] = 1
            return [
                f"{target.name} 最近好像学会了控制直肠的蠕动……",
                f"调教结束之后，{target.name}一边摆弄自己的肛门，一边用勾引的眼神目送你。",
                f"{target.name} 获得了【{self._get_talent_name(77)}】。",
            ]
        # 弄乳狂 (B感覚4+ 噴乳経験100+ 絶頂経験100+ 非扶他)
        if (int(target.abl.get(1, 0)) >= 4
                and int(target.exp.get(54, 0)) >= 100
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(78, 0)) == 0
                and int(target.talent.get(122, 0)) == 0):
            target.talent[78] = 1
            return [
                f"最近，总觉得{target.name}的胸部，好像有着神奇的引力一般……",
                f"调教结束之后，{target.name}用尖立的乳头直直地对着你，眼里充满了勾人的销魂神色。",
                f"{target.name} 获得了【{self._get_talent_name(78)}】。",
            ]
        # 弄乳狂 (扶他: B感覚4+ B珠100+ 絶頂経験100+)
        if (int(target.abl.get(1, 0)) >= 4
                and int(target.juel.get(14, 0)) >= 100
                and int(target.exp.get(2, 0)) >= 100
                and int(target.talent.get(78, 0)) == 0
                and int(target.talent.get(122, 0)) != 0):
            target.talent[78] = 1
            return [
                f"最近，{target.name}总觉得胸部越发敏感……",
                f"调教结束之后，{target.name}用尖立的乳头直直地对着你，眼里充满了渴望。",
                f"{target.name} 获得了【{self._get_talent_name(78)}】。",
            ]
        return []






    def _check_special_talent_shojo_seal_release(self, target) -> List[str]:
        """貞操封印の解除選択"""
        if int(target.talent.get(273, 0)) == 0:
            return []
        messages = [
            f"{target.name} 的【{self._get_talent_name(273)}】的力量消失了……",
            "如果是现在的话，可以解开封印。要解开封印吗？",
            " [0] - 保留封印",
            " [1] - 解开封印",
        ]
        while True:
            choice = self._prompt_choice()
            if choice == "0":
                return messages
            if choice == "1":
                target.talent[273] = 0
                messages.append(f"{target.name} 失去了【{self._get_talent_name(273)}】。")
                return messages





