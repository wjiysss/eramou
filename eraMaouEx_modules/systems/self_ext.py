from __future__ import annotations
"""Module for SelfExtMixin - 自身检查"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SelfExtMixin:
    """Mixin providing 自身检查 methods for GameEngine"""

    def _get_self_kojo_lines(self, target: Character, tflag_13: int) -> List[str]:
        self.interpreter._set_self_kojo_context(target, tflag_13)
        kojo_num = self._get_kojo_num(target)
        if kojo_num <= 0:
            return []
        source_lines = self.interpreter._get_self_kojo_source_text(kojo_num)
        if not source_lines:
            return []
        return self.interpreter._parse_self_kojo_block(source_lines, target)






    def _run_self_kojo(self, target: Character, tflag_13: int) -> None:
        lines = self._get_self_kojo_lines(target, tflag_13)
        for line in lines:
            print(line)






    def _run_self_kojo_lines(self, target: Character) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        if kojo_num <= 0:
            return []
        source_lines = self.interpreter._get_self_kojo_source_text(kojo_num)
        if not source_lines:
            return []
        return self.interpreter._parse_self_kojo_block(source_lines, target)






    def _self_check(self, target: Character) -> List[str]:
        """调教后行为检查 - 对应 @SELF_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()
        assistant = self._get_assistant()

        if player is not None and int(player.cflag.get(61, 0)):
            player.cflag[61] = 0

        if target is None:
            return messages

        tflag = getattr(v, 'tflag', {})
        if int(tflag.get(899, 0)) >= 1:
            return messages

        if (int(target.talent.get(122, 0)) or
            (int(target.talent.get(122, 0)) == 0 and int(target.abl.get(2, 0)) < int(target.abl.get(3, 0))) or
            (int(target.talent.get(0, 0)) and int(target.abl.get(3, 0)) >= 3)):
            s, sex_msgs = self._self_check_analsex(target)
        else:
            s, sex_msgs = self._self_check_sex(target)
        messages.extend(sex_msgs)

        n, lesbian_msgs = self._self_check_lesbian(target, s)
        messages.extend(lesbian_msgs)

        a, masturbation_msgs = self._self_check_masturbation(target, s, n)
        messages.extend(masturbation_msgs)

        b, beast_msgs = self._self_check_beast(target)
        messages.extend(beast_msgs)

        return messages






    def _self_check_analsex(self, target: Character) -> Tuple[int, List[str]]:
        """调教后肛交自检 - 对应 @AFTERTRAIN_ANALSEX_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()

        if target is None:
            return 0, messages
        if int(target.talent.get(85, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            return 0, messages
        if int(target.exp.get(5, 0)) < 30:
            return 0, messages
        if player is None or (int(player.talent.get(122, 0)) == 0 and int(player.talent.get(121, 0)) == 0):
            return 0, messages
        if int(target.base.get(0, 0)) < 500:
            return 0, messages

        s = 0
        abl_a = int(target.abl.get(3, 0))
        if abl_a == 4:
            s += 1
        elif abl_a == 5:
            s += 2
        elif abl_a >= 6:
            s += 3

        abl_sex_addict = int(target.abl.get(30, 0))
        if abl_sex_addict:
            s += abl_sex_addict // 2 + 1

        if s <= 0:
            return 0, messages

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = self._get_palam_level(palam_lust)
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and lust_lv >= 4:
            s += 2
        if int(target.abl.get(11, 0)) == 4 and int(target.abl.get(16, 0)) >= 4 and lust_lv >= 4:
            s += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and lust_lv >= 3:
            s += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and lust_lv >= 3:
            s += 1

        if int(target.talent.get(85, 0)):
            s += 1
        if int(target.talent.get(76, 0)):
            s += 1
        if int(target.talent.get(75, 0)):
            s += 2

        if int(target.talent.get(70, 0)):
            s += 1
        elif int(target.talent.get(71, 0)):
            s -= 2

        if s <= 0:
            return 0, messages

        player_name = getattr(player, 'callname', "主人") if player else "主人"
        target_name = getattr(target, 'savestr', target.name or "")

        messages.append("─" * 50)
        messages.append(f"{player_name}和{target_name}抑制不住无法冷却的兴奋，")
        messages.append(f"回到床上做了{s}次…")

        target.exp[1] = int(target.exp.get(1, 0)) + s
        target.exp[5] = int(target.exp.get(5, 0)) + s
        if hasattr(target, 'juel'):
            target.juel[2] = int(target.juel.get(2, 0)) + s * 200
            target.juel[4] = int(target.juel.get(4, 0)) + s * 100
            target.juel[5] = int(target.juel.get(5, 0)) + s * 250

        if int(target.abl.get(10, 0)) + int(target.abl.get(3, 0)) + int(target.abl.get(16, 0)) >= 13:
            messages.append(f"{target_name}在依依不舍地拉着{player_name}的袖子，")
            messages.append(f"但{player_name}抖开了那只手，离开房间…")

        return 1, messages






    def _self_check_beast(self, target: Character) -> Tuple[int, List[str]]:
        """调教后兽奸自检 - 对应 @AFTERTRAIN_BEASTSEX_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars

        if target is None:
            return 0, messages
        if int(target.talent.get(135, 0)):
            return 0, messages
        if int(target.exp.get(56, 0)) < 50:
            return 0, messages
        if int(target.talent.get(0, 0)) or int(target.talent.get(122, 0)) == 1:
            return 0, messages
        if int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64):
            return 0, messages
        if int(target.cflag.get(273, 0)):
            return 0, messages
        if int(v.get_item(22, 0)) == 0:
            return 0, messages
        if int(target.base.get(0, 0)) < 500:
            return 0, messages

        b = self._calc_beastsex_count(target)
        if b <= 0:
            return 0, messages

        target_name = getattr(target, 'savestr', target.name or "")

        messages.append("─" * 50)
        messages.append(f"之后，{target_name}悄悄地去了饲养狗的狗舍，")
        messages.append(f"进行了{b}次交配。")

        target.exp[56] = int(target.exp.get(56, 0)) + b
        target.exp[0] = int(target.exp.get(0, 0)) + b
        target.exp[5] = int(target.exp.get(5, 0)) + b

        if hasattr(target, 'juel'):
            target.juel[1] = int(target.juel.get(1, 0)) + b * 200
            target.juel[6] = int(target.juel.get(6, 0)) + b * 300
            target.juel[8] = int(target.juel.get(8, 0)) + b * 200

        if (int(target.abl.get(10, 0)) + int(target.abl.get(17, 0)) + int(target.abl.get(21, 0)) >= 12 and
                int(getattr(v, 'time', 0)) == 0):
            if int(target.talent.get(124, 0)):
                messages.append(f"在那之后{target_name}摇着尾巴，来报告了。")
            else:
                messages.append(f"在那之后{target_name}来报告了。")
            if hasattr(target, 'juel'):
                target.juel[8] = int(target.juel.get(8, 0)) + b * 200

        return 1, messages






    def _self_check_lesbian(self, target: Character, intercourse_occurred: int = 0) -> Tuple[int, List[str]]:
        """调教后百合自检 - 对应 @AFTERTRAIN_LESBIANSEX_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()
        assistant = self._get_assistant()

        if target is None or assistant is None:
            return 0, messages

        if int(target.talent.get(122, 0)) or int(assistant.talent.get(122, 0)):
            return 0, messages
        if int(target.abl.get(22, 0)) < 2 or int(target.abl.get(0, 0)) < 3 or int(target.abl.get(10, 0)) < 2 or int(target.abl.get(11, 0)) < 2:
            return 0, messages
        if int(target.abl.get(33, 0)) == 0 and int(assistant.abl.get(33, 0)) == 0:
            return 0, messages
        if int(target.base.get(0, 0)) < 500:
            return 0, messages

        n = self._calc_lesbian_play_count(target, assistant)
        if n <= 0:
            return 0, messages

        target_name = getattr(target, 'savestr', target.name or "")
        assistant_name = getattr(assistant, 'savestr', "助手")
        player_name = getattr(player, 'callname', "主人") if player else "主人"

        if intercourse_occurred == 1:
            messages.append("─" * 50)
            messages.append(f"{player_name}出去之后，")
        else:
            messages.append("调教结束之后，")
        messages.append(f"{target_name}和{assistant_name}好像又百合PLAY了{n}回。")

        target.exp[40] = int(target.exp.get(40, 0)) + n * 20
        exp_2_add = n * 100 * int(target.abl.get(10, 0)) // 500
        if exp_2_add > 0:
            target.exp[2] = int(target.exp.get(2, 0)) + exp_2_add

        if hasattr(target, 'juel'):
            target.juel[0] = int(target.juel.get(0, 0)) + n * 100 * int(target.abl.get(10, 0))
            target.juel[5] = int(target.juel.get(5, 0)) + n * 200

        if int(assistant.talent.get(121, 0)):
            target.exp[20] = int(target.exp.get(20, 0)) + n
            if hasattr(target, 'juel'):
                target.juel[6] = int(target.juel.get(6, 0)) + n * 100 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0)))
                target.juel[7] = int(target.juel.get(7, 0)) + n * 100 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0)))
        else:
            if hasattr(target, 'juel'):
                target.juel[6] = int(target.juel.get(6, 0)) + n * 50 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0)))
                target.juel[7] = int(target.juel.get(7, 0)) + n * 50 * (int(target.abl.get(12, 0)) + int(target.abl.get(16, 0)))

        if int(assistant.talent.get(83, 0)):
            target.exp[30] = int(target.exp.get(30, 0)) + n
            if hasattr(target, 'juel'):
                target.juel[9] = int(target.juel.get(9, 0)) + n * 100 * int(target.abl.get(21, 0))

        if int(target.talent.get(121, 0)):
            target.exp[3] = int(target.exp.get(3, 0)) + n
            if hasattr(target, 'juel'):
                target.juel[8] = int(target.juel.get(8, 0)) + n * 100

        if (int(target.talent.get(121, 0)) and int(assistant.talent.get(121, 0)) and
                int(target.abl.get(16, 0)) >= 3 and int(target.abl.get(32, 0)) >= 3):
            target.exp[3] = int(target.exp.get(3, 0)) + n
            target.exp[20] = int(target.exp.get(20, 0)) + n
            target.exp[21] = int(target.exp.get(21, 0)) + n
            target.exp[22] = int(target.exp.get(22, 0)) + n
            if hasattr(target, 'juel'):
                target.juel[5] = int(target.juel.get(5, 0)) + n * 100
                target.juel[6] = int(target.juel.get(6, 0)) + n * 100
                target.juel[8] = int(target.juel.get(8, 0)) + n * 100

        return 1, messages






    def _self_check_masturbation(self, target: Character, intercourse_occurred: int = 0, lesbian_occurred: int = 0) -> Tuple[int, List[str]]:
        """调教后自慰自检 - 对应 @AFTERTRAIN_MASTURBATION_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()
        assistant = self._get_assistant()

        if target is None:
            return 0, messages
        if int(target.abl.get(0, 0)) < 3 or int(target.abl.get(11, 0)) < 2:
            return 0, messages
        if int(target.talent.get(150, 0)):
            return 0, messages
        if int(target.base.get(0, 0)) < 500:
            return 0, messages

        a = self._calc_masturbation_count(target, assistant)
        if a <= 0:
            return 0, messages

        target_name = getattr(target, 'savestr', target.name or "")
        player_name = getattr(player, 'callname', "主人") if player else "主人"
        assistant_name = getattr(assistant, 'savestr', "助手") if assistant else "助手"

        messages.append("─" * 50)

        prefix = ""
        if lesbian_occurred == 1 and assistant is not None:
            prefix = f"{target_name}在{assistant_name}出去之后，"
        elif intercourse_occurred == 1:
            prefix = f"{target_name}在{player_name}出去之后，"
        else:
            prefix = f"{target_name}在调教结束之后，"

        fantasy, fantasy_kind = self._get_masturbation_fantasy_target(target, assistant, lesbian_occurred)
        messages.append(f"{prefix}好像一边想着{fantasy}，一边自慰了{a}次。")

        target.exp[10] = int(target.exp.get(10, 0)) + a
        if hasattr(target, 'juel'):
            target.juel[0] = int(target.juel.get(0, 0)) + a * 500
            target.juel[4] = int(target.juel.get(4, 0)) + a * 100
            target.juel[5] = int(target.juel.get(5, 0)) + a * 250

        if (int(target.abl.get(10, 0)) + int(target.abl.get(17, 0)) + int(target.abl.get(21, 0)) >= 10 and
                int(getattr(v, 'time', 0)) == 0):
            messages.append(f"在那之后{target_name}来报告了。")
            if hasattr(target, 'juel'):
                target.juel[8] = int(target.juel.get(8, 0)) + a * 200

        if (int(target.abl.get(10, 0)) >= 5 or int(target.abl.get(11, 0)) >= 5) and fantasy_kind == 0:
            messages.append(f"无论自慰了多少次，也无法填满对{player_name}的欲望。")
        elif (int(target.abl.get(11, 0)) >= 5 or int(target.abl.get(33, 0)) >= 3) and fantasy_kind == 1 and assistant is not None:
            messages.append(f"无论自慰了多少次，也无法填满对{assistant_name}的欲望。")
        elif (int(target.abl.get(11, 0)) >= 5 or int(target.abl.get(39, 0)) >= 3) and fantasy_kind == 2:
            messages.append("无论自慰了多少次，也无法填满对兽交的欲望。")

        return 1, messages






    def _self_check_sex(self, target: Character) -> Tuple[int, List[str]]:
        """调教后阴道性交自检 - 对应 @AFTERTRAIN_SEX_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()

        if target is None:
            return 0, messages
        if int(target.talent.get(135, 0)):
            return 0, messages
        if int(target.talent.get(85, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            return 0, messages
        if int(target.exp.get(5, 0)) < 30:
            return 0, messages
        if int(target.talent.get(0, 0)) or int(target.talent.get(122, 0)) == 1:
            return 0, messages
        if int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64):
            return 0, messages
        if int(target.cflag.get(273, 0)):
            return 0, messages
        if player is None or (int(player.talent.get(122, 0)) == 0 and int(player.talent.get(121, 0)) == 0):
            return 0, messages
        if int(target.base.get(0, 0)) < 500:
            return 0, messages

        s = 0
        abl_v = int(target.abl.get(2, 0))
        if abl_v == 4:
            s += 1
        elif abl_v == 5:
            s += 2
        elif abl_v >= 6:
            s += 3

        abl_sex_addict = int(target.abl.get(30, 0))
        if abl_sex_addict:
            s += abl_sex_addict // 2 + 1

        if s <= 0:
            return 0, messages

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = self._get_palam_level(palam_lust)
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(16, 0)) >= 5 and lust_lv >= 4:
            s += 2
        if int(target.abl.get(11, 0)) == 4 and int(target.abl.get(16, 0)) >= 4 and lust_lv >= 4:
            s += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and lust_lv >= 3:
            s += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and lust_lv >= 3:
            s += 1

        if int(target.talent.get(85, 0)):
            s += 1
        if int(target.talent.get(76, 0)):
            s += 1
        if int(target.talent.get(75, 0)):
            s += 2

        if int(target.talent.get(70, 0)):
            s += 1
        elif int(target.talent.get(71, 0)):
            s -= 2

        if s <= 0:
            return 0, messages

        player_name = getattr(player, 'callname', "主人") if player else "主人"
        target_name = getattr(target, 'savestr', target.name or "")

        messages.append("─" * 50)
        messages.append(f"{player_name}和{target_name}抑制不住无法冷却的兴奋，")
        messages.append(f"回到床上做了{s}次…")

        target.exp[0] = int(target.exp.get(0, 0)) + s
        target.exp[5] = int(target.exp.get(5, 0)) + s
        if hasattr(target, 'juel'):
            target.juel[1] = int(target.juel.get(1, 0)) + s * 200
            target.juel[4] = int(target.juel.get(4, 0)) + s * 100
            target.juel[5] = int(target.juel.get(5, 0)) + s * 250

        if int(target.abl.get(10, 0)) + int(target.abl.get(2, 0)) + int(target.abl.get(16, 0)) >= 13:
            messages.append(f"{target_name}在依依不舍地拉着{player_name}的袖子，")
            messages.append(f"但{player_name}抖开了那只手，离开房间。")

        return 1, messages





