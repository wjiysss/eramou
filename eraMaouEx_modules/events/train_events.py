"""
eraMaouEx 调教事件系统模块
对应 ERB EVENT_AFTERTRAIN.ERB / EVENT_BEFORETRAIN.ERB / EVENT_AUTOTRAIN.ERB / EVENT_CHARA_LEAVE.ERB
管理调教前/后事件、死亡检查、SELF_CHECK、角色离脱/归还
"""

import random
from typing import Dict, List, Optional, Any, Tuple


PALAMLV = [0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000, 500000, 1000000, 5000000, 10000000]


def _get_palam_level(value: int) -> int:
    for i, threshold in enumerate(PALAMLV):
        if value < threshold:
            return max(0, i - 1)
    return len(PALAMLV) - 1


class TrainEventManager:
    """调教事件管理器 - 统一管理调教前/后事件、死亡检查、SELF_CHECK、角色离脱/归还"""

    def __init__(self, game_engine):
        self.engine = game_engine

    def _vars(self):
        return self.engine.interpreter.vars

    def _get_player(self):
        v = self._vars()
        if v.chars and len(v.chars) > 0:
            return v.chars[0]
        return None

    def _get_assistant(self):
        v = self._vars()
        assi_idx = v.assi if hasattr(v, 'assi') else -1
        if assi_idx >= 0 and assi_idx < len(v.chars):
            return v.chars[assi_idx]
        return None

    def _get_target(self):
        v = self._vars()
        target_idx = v.target if hasattr(v, 'target') else -1
        if target_idx >= 0 and target_idx < len(v.chars):
            return v.chars[target_idx]
        return None

    # ========================================
    # EVENT_AFTERTRAIN - 调教后事件
    # 对应 ERB EVENT_AFTERTRAIN.ERB
    # ========================================

    def after_train(self, target, player=None, assistant=None) -> Dict[str, Any]:
        """调教后事件总入口 - 对应 @EVENT_AFTERTRAIN
        依次执行: 死亡检查 → SELF_CHECK
        """
        result = {
            'dead': False,
            'self_check': {},
            'messages': [],
        }

        dead, dead_msgs = self.chara_dead_check(target, player)
        result['messages'].extend(dead_msgs)
        if dead:
            result['dead'] = True
            return result

        self_check_result = self.self_check(target, player, assistant)
        result['self_check'] = self_check_result
        result['messages'].extend(self_check_result.get('messages', []))

        return result

    # ========================================
    # CHARADEAD_CHECK - 死亡检查
    # 对应 ERB @CHARADEAD_CHECK
    # ========================================

    def chara_dead_check(self, target, player=None) -> Tuple[bool, List[str]]:
        """角色死亡检查 - 对应 @CHARADEAD_CHECK
        返回 (是否死亡, 消息列表)
        """
        messages = []
        v = self._vars()

        if target is None:
            return False, messages

        if int(target.base.get(0, 0)) > 0:
            return False, messages

        if int(v.get_flag(35, 0)):
            if int(target.base.get(0, 0)) < 1:
                target.base[0] = 1
            return False, messages

        target_idx = self._find_char_index(target)
        if target_idx == 0:
            ex_flag_3 = v.get_ex_flag(3, 0)
            if not ex_flag_3:
                messages.append("-------------------------------GAMEOVER---------------------------------")
                return True, messages
            else:
                messages.append("-------------------------------GAMEOVER---------------------------------")
                messages.append("------------------------------------------------------------------------")
                messages.append("------------------------------------------------------------------------")
                messages.append("------------------------------------------------------------------------")
                messages.append("-------------------------------@@@@@@@@---------------------------------")
                replacement_name = ""
                if ex_flag_3 < len(v.chars):
                    replacement_name = v.chars[ex_flag_3].savestr if hasattr(v.chars[ex_flag_3], 'savestr') else ""
                player_name = player.savestr if player else "主人"
                assistant = self._get_assistant()
                assistant_name = assistant.savestr if assistant else ""

                mao_idx = self._find_char_by_no(17)
                is_mao = (ex_flag_3 == mao_idx)
                is_player = (ex_flag_3 == 0)
                is_assi = (assistant is not None and ex_flag_3 == self._find_char_index(assistant))

                if not is_mao and (is_player or is_assi):
                    messages.append("你猛的醒了过来、看见了倒在了自己身旁的原本属于自己的身体")
                    messages.append("你似乎明白了什么……")
                    messages.append(f"从一旁的巨大镜子中映出的是{replacement_name}的身影……")
                elif not is_mao and not is_player and not is_assi:
                    messages.append("你猛的醒了过来、看着这似曾相识的房间……")
                    messages.append("你似乎明白了什么……")
                    messages.append(f"从一旁的镜子中映出的是{replacement_name}的身影……")
                elif is_mao and (is_player or is_assi):
                    messages.append(f"{replacement_name}看着倒在眼前的东西……")
                    messages.append("心中有些怅然若失……")
                    messages.append(f"但很快、{replacement_name}似乎感受到了什么似的、眼中闪过了一丝光芒")
                    messages.append(f"=============={replacement_name}成为魔王了==============")
                elif is_mao and not is_player and not is_assi:
                    messages.append(f"{replacement_name}突然像丢了魂似的瘫坐在地上……")
                    messages.append(f"但很快、{replacement_name}似乎感受到了什么似的、眼中闪过了一丝光芒")
                    messages.append(f"=============={replacement_name}成为魔王了==============")

        target_name = target.savestr if hasattr(target, 'savestr') else str(target_idx)
        player_name = player.savestr if player else "主人"

        messages.append(f"{target_name}死掉了……")

        target.base[0] = -1

        char_no = int(target.no) if hasattr(target, 'no') else target_idx
        flag_idx = char_no + 999
        v.set_flag(flag_idx, -2)

        kill_count = int(v.get_flag(31, 0)) + 1
        v.set_flag(31, kill_count)

        if kill_count >= 3 and player is not None and int(player.talent.get(93, 0)) == 0:
            messages.append(f"{player_name}掌握了【威圧感】。")
            player.talent[93] = 1

        return True, messages

    # ========================================
    # SELF_CHECK - 调教后行为检查
    # 对应 ERB @SELF_CHECK
    # ========================================

    def self_check(self, target, player=None, assistant=None) -> Dict[str, Any]:
        """调教后行为检查 - 对应 @SELF_CHECK
        依次检查: 性交/肛交 → 百合 → 自慰 → 兽奸
        """
        result = {
            'sex_count': 0,
            'lesbian_count': 0,
            'masturbation_count': 0,
            'beast_count': 0,
            'messages': [],
        }

        if target is None:
            return result

        if player is not None and int(player.cflag.get(61, 0)):
            player.cflag[61] = 0

        v = self._vars()
        target_idx = self._find_char_index(target)
        if target_idx < 0:
            return result

        if int(v.tflag.get(899, 0)) >= 1:
            return result

        if (int(target.talent.get(122, 0)) or
            (int(target.talent.get(122, 0)) == 0 and int(target.abl.get(2, 0)) < int(target.abl.get(3, 0))) or
            (int(target.talent.get(0, 0)) and int(target.abl.get(3, 0)) >= 3)):
            sex_count, sex_msgs = self._aftertrain_analsex_check(target, player)
        else:
            sex_count, sex_msgs = self._aftertrain_sex_check(target, player)
        result['sex_count'] = sex_count
        result['messages'].extend(sex_msgs)

        lesbian_count, lesbian_msgs = self._aftertrain_lesbiansex_check(target, player, assistant, sex_count)
        result['lesbian_count'] = lesbian_count
        result['messages'].extend(lesbian_msgs)

        masturbation_count, masturbation_msgs = self._aftertrain_masturbation_check(
            target, player, assistant, sex_count, lesbian_count
        )
        result['masturbation_count'] = masturbation_count
        result['messages'].extend(masturbation_msgs)

        beast_count, beast_msgs = self._aftertrain_beastsex_check(target, masturbation_count)
        result['beast_count'] = beast_count
        result['messages'].extend(beast_msgs)

        return result

    # ---- AFTERTRAIN_SEX_CHECK ----

    def _aftertrain_sex_check(self, target, player=None) -> Tuple[int, List[str]]:
        """调教后性交检查 - 对应 @AFTERTRAIN_SEX_CHECK"""
        messages = []
        v = self._vars()
        target_idx = self._find_char_index(target)
        if target_idx < 0:
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
        lust_lv = _get_palam_level(palam_lust)
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

        player_name = player.savestr if player else "主人"
        target_name = target.savestr if hasattr(target, 'savestr') else "对方"

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

    # ---- AFTERTRAIN_ANALSEX_CHECK ----

    def _aftertrain_analsex_check(self, target, player=None) -> Tuple[int, List[str]]:
        """调教后肛交检查 - 对应 @AFTERTRAIN_ANALSEX_CHECK"""
        messages = []
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
        lust_lv = _get_palam_level(palam_lust)
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

        player_name = player.savestr if player else "主人"
        target_name = target.savestr if hasattr(target, 'savestr') else "对方"

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

    # ---- AFTERTRAIN_LESBIANSEX_CHECK ----

    def _aftertrain_lesbiansex_check(self, target, player=None, assistant=None,
                                      intercourse_occurred: int = 0) -> Tuple[int, List[str]]:
        """调教后百合检查 - 对应 @AFTERTRAIN_LESBIANSEX_CHECK"""
        messages = []
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

        target_name = target.savestr if hasattr(target, 'savestr') else "对方"
        assistant_name = assistant.savestr if hasattr(assistant, 'savestr') else "助手"
        player_name = player.savestr if player else "主人"

        if intercourse_occurred == 1:
            messages.append("─" * 50)
            messages.append(f"{player_name}出去之后，", end="")
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

    def _calc_lesbian_play_count(self, target, assistant) -> int:
        """计算百合PLAY回数"""
        n = 0

        target_les_lv = int(target.abl.get(33, 0))
        n += {1: 1, 2: 2, 3: 3, 4: 5, 5: 7}.get(target_les_lv, 9 if target_les_lv >= 6 else 0)

        assi_les_lv = int(assistant.abl.get(33, 0))
        n += {1: 1, 2: 2, 3: 5, 4: 8, 5: 13}.get(assi_les_lv, 18 if assi_les_lv >= 6 else 0)

        if n <= 0:
            return 0

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = _get_palam_level(palam_lust)

        if int(target.abl.get(22, 0)) >= 5 and lust_lv >= 3:
            n += 1
        if int(assistant.abl.get(22, 0)) >= 3 and lust_lv >= 3:
            n += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and lust_lv >= 3:
            n += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and lust_lv >= 3:
            n += 1

        relation = self._get_relation(assistant)
        if relation > 0:
            n = n * relation // 100

        if int(target.talent.get(24, 0)):
            n -= 1
        if int(assistant.talent.get(24, 0)):
            n -= 1
        if int(target.talent.get(27, 0)):
            n -= 1
        if int(assistant.talent.get(27, 0)):
            n -= 1

        if int(target.talent.get(81, 0)):
            n += 2
        if int(assistant.talent.get(81, 0)):
            n += 2
        if int(target.talent.get(76, 0)):
            n += 1
        if int(assistant.talent.get(76, 0)):
            n += 1

        if int(target.talent.get(70, 0)):
            n += 1
        elif int(target.talent.get(71, 0)):
            n -= 2
        if int(assistant.talent.get(70, 0)):
            n += 1
        elif int(assistant.talent.get(71, 0)):
            n -= 2

        return max(n, 0)

    # ---- AFTERTRAIN_MASTURBATION_CHECK ----

    def _aftertrain_masturbation_check(self, target, player=None, assistant=None,
                                        intercourse_occurred: int = 0,
                                        lesbian_occurred: int = 0) -> Tuple[int, List[str]]:
        """调教后自慰检查 - 对应 @AFTERTRAIN_MASTURBATION_CHECK"""
        messages = []
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

        target_name = target.savestr if hasattr(target, 'savestr') else "对方"
        player_name = player.savestr if player else "主人"
        assistant_name = assistant.savestr if assistant else "助手"

        messages.append("─" * 50)

        if lesbian_occurred == 1 and assistant is not None:
            messages.append(f"{target_name}在{assistant_name}出去之后，", end="")
        elif intercourse_occurred == 1:
            messages.append(f"{target_name}在{player_name}出去之后，", end="")
        else:
            messages.append(f"{target_name}在调教结束之后，", end="")

        fantasy, fantasy_kind = self._get_masturbation_fantasy(target, assistant, lesbian_occurred)
        messages.append(f"好像一边想着{fantasy}，一边自慰了{a}次。")

        target.exp[10] = int(target.exp.get(10, 0)) + a
        if hasattr(target, 'juel'):
            target.juel[0] = int(target.juel.get(0, 0)) + a * 500
            target.juel[4] = int(target.juel.get(4, 0)) + a * 100
            target.juel[5] = int(target.juel.get(5, 0)) + a * 250

        v = self._vars()
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

    def _calc_masturbation_count(self, target, assistant=None) -> int:
        """计算自慰回数"""
        a = 0
        abl_mast = int(target.abl.get(31, 0))
        if abl_mast == 1:
            a += 1
        elif abl_mast == 2:
            a += 2
        elif abl_mast == 3:
            a += 4
        elif abl_mast == 4:
            a += 6
        elif abl_mast == 5:
            a += 9
        elif abl_mast >= 6:
            a += 14

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = _get_palam_level(palam_lust)

        if int(target.talent.get(60, 0)) and int(target.abl.get(11, 0)) >= 3 and lust_lv >= 3:
            a += 1
        if assistant is not None and int(assistant.talent.get(118, 0)) and int(target.abl.get(11, 0)) >= 4 and lust_lv >= 3:
            a += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and lust_lv >= 4:
            a += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and lust_lv >= 4:
            a += 1

        if int(target.talent.get(74, 0)):
            a = int(a * 1.50)
        if assistant is not None and int(assistant.talent.get(118, 0)):
            a = int(a * 1.20)

        if int(target.talent.get(17, 0)):
            a += 1
        if int(target.talent.get(33, 0)):
            a += 1
        if int(target.talent.get(15, 0)):
            a -= 1
        if int(target.talent.get(20, 0)):
            a -= 1
        if int(target.talent.get(32, 0)):
            a -= 1

        if int(target.talent.get(70, 0)):
            a += 1
        elif int(target.talent.get(71, 0)):
            a -= 2

        if int(target.talent.get(76, 0)):
            a += 1

        return max(a, 0)

    def _get_masturbation_fantasy(self, target, assistant, lesbian_occurred: int) -> Tuple[str, int]:
        """获取自慰妄想对象 - 返回 (对象名, 类型: 0=主人 1=助手 2=兽)"""
        v = self._vars()
        if (int(target.talent.get(85, 0)) == 0 and lesbian_occurred == 1 and
                assistant is not None and int(target.abl.get(22, 0)) > random.randint(0, 4)):
            return assistant.savestr if hasattr(assistant, 'savestr') else "助手", 1
        if (int(target.talent.get(85, 0)) == 0 and int(target.abl.get(39, 0)) > random.randint(0, 4) and
                int(v.get_item(22, 0)) > 0):
            return "兽交", 2
        player = self._get_player()
        return (player.savestr if player else "主人"), 0

    # ---- AFTERTRAIN_BEASTSEX_CHECK ----

    def _aftertrain_beastsex_check(self, target, masturbation_occurred: int = 0) -> Tuple[int, List[str]]:
        """调教后兽奸检查 - 对应 @AFTERTRAIN_BEASTSEX_CHECK"""
        messages = []
        v = self._vars()
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

        target_name = target.savestr if hasattr(target, 'savestr') else "对方"

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

    def _calc_beastsex_count(self, target) -> int:
        """计算兽奸回数"""
        b = 0
        abl_beast = int(target.abl.get(39, 0))
        if abl_beast == 0:
            b -= 2
        elif abl_beast == 1:
            b -= 1
        elif abl_beast == 2:
            b += 0
        elif abl_beast == 3:
            b += 1
        elif abl_beast == 4:
            b += 2
        elif abl_beast == 5:
            b += 3
        elif abl_beast >= 6:
            b += 4

        palam_lust = int(target.palam.get(5, 0))
        lust_lv = _get_palam_level(palam_lust)

        if int(target.talent.get(124, 0)) and int(target.abl.get(11, 0)) >= 3 and lust_lv >= 3:
            b += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and lust_lv >= 4:
            b += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and lust_lv >= 4:
            b += 1

        if int(target.talent.get(136, 0)):
            b += 2

        if b <= 0:
            return 0

        if int(target.talent.get(17, 0)):
            b += 1
        if int(target.talent.get(33, 0)):
            b += 1
        if int(target.talent.get(124, 0)):
            b += 1
        if int(target.talent.get(15, 0)):
            b -= 1
        if int(target.talent.get(20, 0)):
            b -= 1
        if int(target.talent.get(32, 0)):
            b -= 1
        if int(target.talent.get(62, 0)) and int(target.talent.get(64, 0)) == 0:
            b -= 2

        if int(target.talent.get(70, 0)):
            b += 1
        elif int(target.talent.get(71, 0)):
            b -= 2

        if int(target.talent.get(76, 0)):
            b += 1

        if int(target.talent.get(136, 0)):
            b = int(b * 1.50)

        return max(b, 0)

    # ========================================
    # EVENT_BEFORETRAIN - 调教前事件
    # 对应 ERB EVENT_BEFORETRAIN.ERB
    # ========================================

    def before_train(self, target, player=None, assistant=None) -> Dict[str, Any]:
        """调教前事件 - 整合 TrainMainSystem.before_train_message 的逻辑
        返回 {'messages': [...], 'cflag_10': 调教回数}
        """
        from ..systems.train_main import TrainMainSystem
        tms = TrainMainSystem(self.engine)
        messages = tms.before_train_message(target, player, assistant)
        return {
            'messages': messages,
            'cflag_10': int(target.cflag.get(10, 0)),
        }

    # ========================================
    # EVENT_AUTOTRAIN - 自动调教事件
    # 对应 ERB EVENT_AUTOTRAIN.ERB
    # ========================================

    def autotrain(self) -> List[Dict[str, Any]]:
        """自动调教 - 整合 TrainMainSystem.run_autotrain 的逻辑"""
        from ..systems.train_main import TrainMainSystem
        tms = TrainMainSystem(self.engine)
        return tms.run_autotrain()

    # ========================================
    # EVENT_CHARA_LEAVE - 角色离脱/归还
    # 对应 ERB EVENT_CHARA_LEAVE.ERB
    # ========================================

    def chara_leave(self, char_idx: int, str_idx: int = 0) -> Dict[str, Any]:
        """角色离脱序列化 - 对应 @EVENT_CHARA_LEAVE(ARG, CHARA)
        将角色的所有数据序列化到 STR:str_idx 中，然后从角色列表中移除
        """
        v = self._vars()
        if char_idx < 0 or char_idx >= len(v.chars):
            return {'success': False, 'message': "无效角色索引"}

        char = v.chars[char_idx]

        parts = []
        parts.append(str(int(char.no) if hasattr(char, 'no') else char_idx))
        parts.append(str(int(char.cflag.get(9, 0))))

        nickname = getattr(char, 'nickname', '') or ''
        parts.append(nickname)

        abl_str = self._serialize_dict(char.abl)
        parts.append(abl_str)

        base_str = self._serialize_dict(char.base)
        parts.append(base_str)

        maxbase_str = self._serialize_dict(char.maxbase)
        parts.append(maxbase_str)

        cflag_str = self._serialize_dict(char.cflag)
        parts.append(cflag_str)

        exp_str = self._serialize_dict(char.exp)
        parts.append(exp_str)

        equip_str = self._serialize_dict(char.equip if hasattr(char, 'equip') else {})
        parts.append(equip_str)

        juel_str = self._serialize_dict(char.juel if hasattr(char, 'juel') else {})
        parts.append(juel_str)

        talent_str = self._serialize_dict(char.talent)
        parts.append(talent_str)

        mark_str = self._serialize_dict(char.mark if hasattr(char, 'mark') else {})
        parts.append(mark_str)

        cstr_str = self._serialize_cstr(char.cstr if hasattr(char, 'cstr') else {})
        parts.append(cstr_str)

        serialized = "_".join(parts)

        if not hasattr(v, 'str'):
            v.str = {}
        v.str[str_idx] = serialized

        if int(v.get_flag(1, 0)) == char_idx:
            v.set_flag(1, -1)
        if int(v.get_flag(2, 0)) == char_idx:
            v.set_flag(2, -1)
        if int(v.get_flag(1, 0)) == char_idx:
            v.set_flag(1, 0)
        if int(v.get_flag(2, 0)) > char_idx:
            v.set_flag(2, 0)

        v.chars.pop(char_idx)

        return {
            'success': True,
            'message': f"角色{char.savestr if hasattr(char, 'savestr') else char_idx}已离脱",
            'serialized': serialized,
        }

    def chara_return(self, str_idx: int = 0, set_lv: int = 0) -> Dict[str, Any]:
        """角色归还反序列化 - 对应 @EVENT_CHARA_RETURN(ARG, SETLV)
        从 STR:str_idx 中反序列化角色数据，创建新角色
        """
        v = self._vars()
        serialized = v.str.get(str_idx, '') if hasattr(v, 'str') else ''
        if not serialized:
            return {'success': False, 'message': "无序列化数据"}

        parts = serialized.split("_")
        if len(parts) < 13:
            return {'success': False, 'message': "序列化数据格式错误"}

        char_no = int(parts[0])
        cflag_9 = int(parts[1])
        nickname = parts[2]

        new_char = self._create_void_character()
        if new_char is None:
            return {'success': False, 'message': "无法创建空角色"}

        new_char.no = char_no
        new_char.cflag[9] = cflag_9

        if nickname:
            new_char.savestr = nickname

        self._deserialize_dict(new_char.abl, parts[3])
        self._deserialize_dict(new_char.base, parts[4])
        self._deserialize_dict(new_char.maxbase, parts[5])
        self._deserialize_dict(new_char.cflag, parts[6])
        self._deserialize_dict(new_char.exp, parts[7])
        self._deserialize_dict(new_char.equip if hasattr(new_char, 'equip') else {}, parts[8])
        self._deserialize_dict(new_char.juel if hasattr(new_char, 'juel') else {}, parts[9])
        self._deserialize_dict(new_char.talent, parts[10])
        self._deserialize_dict(new_char.mark if hasattr(new_char, 'mark') else {}, parts[11])
        self._deserialize_cstr(new_char, parts[12])

        new_char.cflag[501] = 0
        new_char.cflag[502] = 0
        new_char.cflag[1] = 0

        lv = int(new_char.cflag.get(9, 0))
        if lv < set_lv:
            lv = set_lv - lv
        for _ in range(lv):
            self._st_up(new_char)

        new_char.base[0] = int(new_char.maxbase.get(0, 1000))
        new_char.base[1] = int(new_char.maxbase.get(1, 500))

        v.chars.append(new_char)

        v.str[str_idx] = ''

        return {
            'success': True,
            'message': f"角色{new_char.savestr if hasattr(new_char, 'savestr') else char_no}已归还",
            'char_idx': len(v.chars) - 1,
        }

    # ========================================
    # 序列化/反序列化辅助方法
    # ========================================

    def _serialize_dict(self, data: Dict) -> str:
        """将字典序列化为 "key,value/key,value/" 格式"""
        parts = []
        if data is None:
            return ""
        for k, val in data.items():
            if val:
                parts.append(f"{k},{val}")
        return "/".join(parts)

    def _deserialize_dict(self, target_dict: Dict, data: str) -> None:
        """从 "key,value/key,value/" 格式反序列化到字典"""
        if not data:
            return
        entries = data.split("/")
        for entry in entries:
            if not entry:
                continue
            kv = entry.split(",")
            if len(kv) >= 2:
                try:
                    key = int(kv[0])
                    val = int(kv[1])
                    target_dict[key] = val
                except (ValueError, TypeError):
                    pass

    def _serialize_cstr(self, data: Dict) -> str:
        """将CSTR字典序列化为 "key,value/key,value/" 格式（值为字符串）"""
        parts = []
        if data is None:
            return ""
        for k, val in data.items():
            if val:
                parts.append(f"{k},{val}")
        return "/".join(parts)

    def _deserialize_cstr(self, char, data: str) -> None:
        """从 "key,value/key,value/" 格式反序列化CSTR"""
        if not data:
            return
        if not hasattr(char, 'cstr'):
            char.cstr = {}
        entries = data.split("/")
        for entry in entries:
            if not entry:
                continue
            kv = entry.split(",")
            if len(kv) >= 2:
                try:
                    key = int(kv[0])
                    val = kv[1]
                    char.cstr[key] = val
                except (ValueError, TypeError):
                    pass

    def _create_void_character(self):
        """创建空角色 - 对应 ADDVOIDCHARA"""
        v = self._vars()
        try:
            from ..core.constants import Character
            new_char = Character()
            return new_char
        except ImportError:
            class VoidChar:
                def __init__(self):
                    self.no = 0
                    self.savestr = ""
                    self.name = ""
                    self.abl = {}
                    self.base = {}
                    self.maxbase = {}
                    self.cflag = {}
                    self.exp = {}
                    self.equip = {}
                    self.juel = {}
                    self.talent = {}
                    self.mark = {}
                    self.cstr = {}
                    self.palam = {}
                    self.source = {}
                    self.stain = {}
                    self.nowex = {}
            return VoidChar()

    def _st_up(self, char):
        """角色属性提升 - 对应 @ST_UP"""
        pass

    def _find_char_index(self, char) -> int:
        """查找角色在列表中的索引"""
        v = self._vars()
        for i, c in enumerate(v.chars):
            if c is char:
                return i
        return -1

    def _find_char_by_no(self, char_no: int) -> int:
        """根据角色编号查找索引 - 对应 GETCHARA"""
        v = self._vars()
        for i, c in enumerate(v.chars):
            if hasattr(c, 'no') and int(c.no) == char_no:
                return i
        return -1

    def _get_relation(self, char) -> int:
        """获取相性值"""
        v = self._vars()
        idx = self._find_char_index(char)
        if idx < 0:
            return 0
        relation = v.relation if hasattr(v, 'relation') else []
        if idx < len(relation):
            return int(relation[idx])
        return 0
