from __future__ import annotations
"""Module for EventDailyMixin - Daily event methods (nextday, nextmonth, turnend, beforetrain, aftertrain, autotrain, chara_leave, chara_return)"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EventDailyMixin:
    """Mixin providing Daily event methods (nextday, nextmonth, turnend, beforetrain, aftertrain, autotrain, chara_leave, chara_return)"""
    def _event_nextday(self) -> List[str]:
        """每日事件处理 - 对应 @EVENT_NEXTDAY
        日付変更時に起きるイベント：素質変更チェック、媚药中毒、妊娠関連、キャライベント等
        """
        import random
        messages: List[str] = []
        v = self.interpreter.vars

        for target in v.chars[1:]:
            if target.talent.get(121, 0) == 0 and target.talent.get(122, 0) == 0:
                if target.talent.get(326, 0) == 1 and target.exp.get(20, 0) >= 150:
                    target.talent[326] = 0
                    target.talent[121] = 1
                    target.talent[1] = 1
                    messages.append(f"（呃…这是什么？）")
                    messages.append(f"{target.savestr}获得了【扶她】。")

            if target.talent.get(57, 0) == 0:
                if target.talent.get(132, 0) and target.exp.get(31, 0) >= 15:
                    target.talent[57] = 1
                    messages.append(f"当晚，{target.savestr}尿床了…")
                    messages.append(f"{target.savestr}获得了【漏尿癖】。")
                elif not target.talent.get(132, 0) and target.exp.get(31, 0) >= 40:
                    target.talent[57] = 1
                    messages.append(f"当晚，{target.savestr}尿床了…")
                    messages.append(f"{target.savestr}获得了【漏尿癖】。")

            if target.mark.get(3, 0) == 3:
                if (target.talent.get(132, 0) or target.talent.get(134, 0)) and \
                   target.abl.get(11, 0) >= 5 and target.abl.get(10, 0) >= 5 and \
                   target.abl.get(21, 0) >= 5 and target.exp.get(50, 0) >= 5:
                    target.talent[131] = 1
                    messages.append(f"（呃……这是什么？）")
                    messages.append(f"{target.savestr}的样子有点奇怪……")
                    messages.append(f"{target.savestr}再也无法接受严厉的调教，获得了【幼儿退行】…")
                    for t_idx in (20, 21, 22, 24, 26, 27):
                        if target.talent.get(t_idx, 0):
                            target.talent[t_idx] = 0
                elif target.abl.get(11, 0) >= 5 and target.abl.get(10, 0) >= 5 and \
                     target.abl.get(21, 0) >= 5 and target.abl.get(17, 0) >= 5 and \
                     target.exp.get(50, 0) >= 7 and target.talent.get(57, 0) == 1:
                    target.talent[131] = 1
                    messages.append(f"（呃……这是什么？）")
                    messages.append(f"{target.savestr}的样子有点奇怪……")
                    messages.append(f"{target.savestr}再也无法接受严厉的调教，获得了【幼儿退行】…")
                    for t_idx in (20, 21, 22, 24, 26, 27):
                        if target.talent.get(t_idx, 0):
                            target.talent[t_idx] = 0

            if target.talent.get(314, 0) != 9:
                if target.talent.get(244, 0) == 1 and target.talent.get(245, 0) == 1 and \
                   target.talent.get(246, 0) == 1 and target.talent.get(247, 0) == 1:
                    target.talent[314] = 9
                    messages.append(f"{target.savestr}的种族变成了【魔族】。")

            messages.extend(self._check_aphrodisiac_addict(target))

            if target.talent.get(315, 0):
                if target.cflag.get(821, 0) > 0:
                    target.cflag[821] = target.cflag.get(821, 0) - 1
                    if target.cflag[821] <= 0:
                        target.cflag[821] = 0
                        target.talent[315] = 0
                        messages.append(f"{target.savestr}的灵魂归位了。")

        for target in v.chars:
            if target.cflag.get(109, 0):
                messages.append(f"{target.savestr}的排卵诱发剂的效果消失了。")
                messages.append("————————————")
                target.cflag[109] = 0

        v.flags[61] = 0

        messages.extend(self._ninsin_main())

        for target in v.chars[1:]:
            if target.talent.get(0, 0):
                messages.extend(self._offer_virgin_check(target))

        messages.extend(self._night_stalking_check())

        messages.extend(self._curse_equip_ring())
        messages.extend(self._summon_monster(0))
        messages.extend(self._dungeon_room_day())

        for target in v.chars[1:]:
            messages.extend(self._pillory(target))
            messages.extend(self._check_sabbath_day(target))
            messages.extend(self._ntr_video(target))
            messages.extend(self._event_video_day(target))

            if target.talent.get(0, 0) == 0 and random.randint(0, 2) == 0:
                messages.extend(self._karma(target, 1))
            if target.talent.get(85, 0) == 1 and random.randint(0, 2) == 0:
                messages.extend(self._karma(target, 1))
            if target.cflag.get(1, 0) == 2 and random.randint(0, 2) == 0:
                messages.extend(self._karma(target, 1))
            if random.randint(0, 1) == 0:
                messages.extend(self._karma(target, 1))
            else:
                messages.extend(self._karma(target, -1))

            if target.talent.get(202, 0) or target.talent.get(206, 0):
                messages.extend(self._faith(target, 1))
            elif target.cflag.get(152, 0) < 30:
                messages.extend(self._faith(target, -1))
            elif random.randint(0, 3) == 0:
                messages.extend(self._faith(target, 1))
            elif random.randint(0, 2) == 0:
                messages.extend(self._faith(target, -1))

        messages.extend(self._tax_get())
        messages.extend(self._sengen_video_de())
        messages.extend(self._maou_kouho())

        return messages


    def _event_video_day(self, target) -> List[str]:
        """動画イベント(日次) - 对应 @EVENT_VIDEO_DAY"""
        messages: List[str] = []
        return messages


    def _event_nextmonth(self) -> List[str]:
        """每月事件处理 - 对应 @EVENT_NEXTMONTH
        各月末日で月替わり処理、12月末は年越し＋全キャラ加齢
        DAY:1=月, DAY:2=日
        """
        messages: List[str] = []
        v = self.interpreter.vars
        month = v.day[1] if len(v.day) > 1 else 1
        day = v.day[2] if len(v.day) > 2 else 1

        if month == 2:
            v.day[1] = month + 1
            v.day[2] = 1
            messages.append(f"明天就是{v.day[1]}月了，是个适合调教的月份呢……")
        elif day > 30 and month in (4, 6, 9, 11):
            v.day[1] = month + 1
            v.day[2] = 1
            messages.append(f"明天就是{v.day[1]}月了，是个适合调教的月份呢……")
        elif day > 31 and month in (1, 3, 5, 7, 8, 10):
            v.day[1] = month + 1
            v.day[2] = 1
            messages.append(f"明天就是{v.day[1]}月了，是个适合调教的月份呢……")
        elif day > 31 and month == 12:
            v.day[1] = 1
            v.day[2] = 1
            messages.append("明天就是新一年的开始了，再努力地把邪恶传播到各处吧！")
            for char in v.chars[1:]:
                age_days = char.cflag.get(452, 0)
                age_days += 1
                char.cflag[452] = age_days
                char.cflag[451] = self._human_age_generate(age_days, char)

        return messages


    def _event_turnend(self) -> List[str]:
        """回合结束处理 - 对应 @EVENTTURNEND
        BEGIN TURNEND後最初に呼び出される：売却/助手判定、特殊素質、妊娠判定、
        日付変更、敵生成、アイテム自動購入等
        """
        import random
        messages: List[str] = []
        v = self.interpreter.vars

        messages.append(f"【DEBUG】回合结束 - Day:{v.day[0]}, Time:{v.time}, MONEY:{v.money}, 角色数:{len(v.chars)}")

        for target in v.chars:
            messages.extend(self._check_sell_assiable(target))

        for target in v.chars[1:]:
            messages.extend(self._check_special_talent(target, self._get_player()))

        for target in v.chars:
            messages.extend(self._in_vagina_all(target))
            messages.extend(self._conception_check_all(target))

        v.flags[0] = 0

        if v.time == 1:
            for target in v.chars:
                messages.extend(self._in_vagina_extra(target))
                messages.extend(self._conception_check_extra(target))
                messages.extend(self._in_vagina_kyouou_to_t(target))
                messages.extend(self._conception_check_kyouou_to_t(target))
                messages.extend(self._in_vagina_ntrd_to_t(target))
                messages.extend(self._conception_check_ntrd_to_t(target))

            messages.extend(self._event_nextday())

            v.day[0] += 1
            v.day[2] = v.day[2] + 1

            if v.day[2] > 28:
                messages.extend(self._event_nextmonth())

            v.day[3] = v.day[3] + 1
            if v.day[3] > 6:
                v.day[3] = 0

            v.time = 0

            messages.extend(self._apply_daily_enter_enemy())
        else:
            v.time = 1

        messages.extend(self._auto_buying())

        v.target = -1
        v.assi = -1

        return messages


    def _event_beforetrain(self, target: Character) -> List[str]:
        """调教前事件 - 对应 @PRITRAIN_MESSAGE / EVENT_BEFORETRAIN.ERB
        调教开始时的消息显示：衣着状态、初次调教反应、素质判定、助手反应等
        """
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()

        target.cflag[10] = int(target.cflag.get(10, 0)) + 1
        train_count = int(target.cflag.get(10, 0))

        if int(v.get_flag(6, 0)) & 1:
            target_name = getattr(target, 'savestr', target.name or "")
            messages.append(f"{target_name}的第{train_count}次调教开始了。")
            return messages

        messages.append("─" * 50)

        if int(v.get_flag(37, 0)) == 0:
            target.cflag[40] = 0

        target_name = getattr(target, 'savestr', target.name or "")
        player_name = getattr(player, 'callname', "主人") if player else "主人"
        assistant = self._get_assistant()
        assistant_name = getattr(assistant, 'savestr', "助手") if assistant else ""
        cloth_state = int(target.cflag.get(40, 0))

        if train_count == 1:
            messages.append(f"{target_name}的第一次调教开始了，把她变成棒棒哒性奴隶吧！")
            messages.append("")

            if int(v.get_flag(37, 0)):
                messages.extend(self._beforetrain_clothed(target))
            else:
                messages.extend(self._beforetrain_noclothes(target))

            if int(target.talent.get(23, 0)):
                messages.append("")
                messages.append(f"然而在{target_name}的眼神最深处却好像流淌着期待的光芒。")

            if assistant is not None:
                if int(assistant.talent.get(83, 0)):
                    messages.append("")
                    messages.append(f"助手{assistant_name}心想着如何才能尽情享受凌辱{target_name}的乐趣。")
                    messages.append("那猎人看向猎物的眼神已经将她的心思完全暴露了出来。")
                elif int(assistant.talent.get(13, 0)):
                    messages.append("")
                    messages.append(f"助手{assistant_name}看到{target_name}的这个样子，")
                    messages.append(f"在得到{player_name}的许可后，轻轻把手放到了{target_name}的肩上。")
                    if int(target.talent.get(11, 0)):
                        messages.append(f"而{target_name}却无情地把手甩开了。")

            return messages

        messages.append(f"{target_name}的第{train_count}次调教开始了。")

        s = 0

        if int(target.talent.get(9, 0)):
            messages.append(f"{target_name}{self._print_clothtype(target)}，面露痴笑，精神恍惚。")
            messages.append(f"仔细观察就会发觉{target_name}的眼神已经完全失去了生气………")
        elif ((int(target.talent.get(13, 0)) or int(target.talent.get(14, 0)) or int(target.talent.get(88, 0))) and
              int(target.abl.get(10, 0)) >= 4 and int(target.abl.get(16, 0)) >= 3 and int(target.mark.get(3, 0)) == 0):
            messages.append(f"{target_name}{self._print_clothtype(target)}，土下座地跪在地上，恭敬地为{player_name}带来调教前的问候。")
            if player is not None and int(player.talent.get(83, 0)):
                messages.append(f"{player_name}把脚踩在{target_name}的后脑上，将其动人的脸在地板上摩擦。")
                if int(target.abl.get(21, 0)) >= 3:
                    messages.append(f"被这样卑贱地对待{target_name}的胯间似乎开始潮湿了……")
            s = 1
        elif ((int(target.talent.get(13, 0)) or int(target.talent.get(14, 0))) and
              int(target.abl.get(10, 0)) >= 3 and int(target.mark.get(3, 0)) <= 1):
            messages.append(f"{target_name}{self._print_clothtype(target)}，悄悄地看了{player_name}一眼，然后低下了头，带来调教前的问候。")
            s = 1
        else:
            messages.append(f"{self._print_clothtype(target)}的{target_name}被带来了。")
            s = 1

        if int(target.cflag.get(42, 0)) == 11 and (cloth_state & 64):
            if cloth_state == 64:
                messages.append("貌似，里面是真空的……")
            return messages

        if int(target.talent.get(153, 0)):
            day_val = int(getattr(v, 'day', [0, 0, 0])[0]) if hasattr(v, 'day') and isinstance(v.day, list) else 0
            cflag_110 = int(target.cflag.get(110, 0))
            if cflag_110 <= day_val + 10:
                if s == 0:
                    messages.append(self._print_clothtype(target) + "的")
                messages.append(f"{target_name}")
                if int(target.talent.get(100, 0)):
                    messages.append("现在正挺着与娇小的身材不相称的大肚子。")
                else:
                    messages.append("现在正挺着个大肚子。")
                messages.append("（请避免过激的调教）")
            elif cflag_110 <= day_val + 20:
                messages.append(f"{target_name}腹中的胎儿已进入了稳定期，展露出孕妇特有的圆润曲线。")
            elif cflag_110 <= day_val + 30:
                messages.append(f"{target_name}的肚子非常引人注目。")

        a_cloth = int(target.cflag.get(40, 0))
        b_cloth = self._wearing_cloth_all(target)
        target.cflag[40] = a_cloth

        if (a_cloth & 4):
            if (a_cloth & 2) == 0 and (b_cloth & 2) and int(target.talent.get(109, 0)) == 0 and int(target.talent.get(116, 0)) == 0:
                msg = "没有束缚的乳房在衣服内"
                if int(target.talent.get(110, 0)) or int(target.talent.get(114, 0)):
                    msg += "明显地"
                else:
                    msg += "稍稍地"
                msg += f"摇曳着。{player_name}的眼睛正愉快地吃着雪糕。"
                messages.append(msg)

        if (int(target.cflag.get(7, 0)) & 1) and (a_cloth & 2) == 0:
            if (a_cloth & 4) == 1:
                messages.append(f"隔着衣服，{target_name}乳头及上面的乳环浮现了出来。")
            else:
                messages.append(f"随着{target_name}身体的运动，两个乳环也随之起舞。")

        if (a_cloth & 1) == 0 and ((a_cloth & 8) or (a_cloth & 16)):
            if (b_cloth & 1) and int(target.talent.get(135, 0)) == 0 and int(target.abl.get(17, 0)) < 3:
                messages.append(f"{target_name}对没有穿裤子的下体非常在意，频繁地注意着自己的胯股间……")

        if (a_cloth & 1) == 0 and (a_cloth & 8):
            if (b_cloth & 1) and int(target.abl.get(17, 0)) >= 3:
                messages.append(f"{target_name}卷起裙子的下摆，把没穿内裤的私处呈现了出来。")

        if (int(target.cflag.get(7, 0)) & 4) or ((int(target.cflag.get(7, 0)) & 8) and (a_cloth & 1) == 0 and (a_cloth & 16) == 0):
            if (a_cloth & 8) == 1:
                body_prefix = "从裙子里看到的"
            else:
                body_prefix = "裸露着的"
            if int(target.talent.get(122, 0)) or int(target.talent.get(121, 0)):
                body_part = "阴茎"
            else:
                body_part = "阴唇"
                if int(target.cflag.get(7, 0)) & 4:
                    body_part += "两边"
                if (int(target.cflag.get(7, 0)) & 4) and (int(target.cflag.get(7, 0)) & 8):
                    body_part += "和"
                if int(target.cflag.get(7, 0)) & 8:
                    body_part += "阴蒂"
            messages.append(f"{body_prefix}{body_part}穿了环，映射出金属的光芒……")

        if assistant is not None:
            messages.append("")
            if int(assistant.talent.get(76, 0)) and int(assistant.abl.get(20, 0)) >= 3:
                player_name_savestr = getattr(player, 'savestr', "主人") if player else "主人"
                messages.append(f"{player_name_savestr}的助手{assistant_name}用舌头轻舔嘴唇，津津有味地看着{target_name}，")
                messages.append(f"好像在考虑如何凌辱{target_name}。")
            elif int(assistant.talent.get(85, 0)) and int(assistant.abl.get(20, 0)) >= 3:
                player_name_savestr = getattr(player, 'savestr', "主人") if player else "主人"
                messages.append(f"助手{assistant_name}抱着{player_name_savestr}的手臂，微笑地看着即将被调教的{target_name}。")
                messages.append(f"一边在{player_name_savestr}耳边轻轻地说着什么，一边指着{target_name}呵呵地笑着。")
            else:
                player_name_savestr = getattr(player, 'savestr', "主人") if player else "主人"
                messages.append(f"{player_name_savestr}的身边站着助手{assistant_name}。")

        return messages


    def _event_aftertrain(self, target: Character) -> List[str]:
        """调教后事件 - 对应 @EVENT_AFTERTRAIN / EVENT_AFTERTRAIN.ERB
        先执行死亡检查，再执行SELF_CHECK
        """
        messages: List[str] = []

        dead, dead_msgs = self._death_check(target)
        messages.extend(dead_msgs)
        if dead:
            return messages

        messages.extend(self._self_check(target))

        return messages


    def _event_autotrain(self) -> List[str]:
        """自动调教系统 - 对应 @AUTOTRAIN
        罠や呪われた装備、イベントなどで勇者が調教されていく
        CFLAG:666 が非0のキャラに対して自動調教を実行
        """
        messages: List[str] = []
        v = self.interpreter.vars

        for target in v.chars[1:]:
            if int(target.cflag.get(666, 0)) == 0:
                continue

            self._format_autotrain(target)

            cloth_type = target.equipt.get(0, 0)
            char_name = getattr(target, 'savestr', target.name or target.callname or "")
            messages.append(f"【{cloth_type}】{char_name}的调教结果")

            messages.extend(self._after_autotrain(target))

        return messages


    def _chara_leave(self, char_idx: int) -> List[str]:
        """角色离场事件 - 对应 @EVENT_CHARA_LEAVE
        キャラのデータをシリアライズして保存し、キャラを削除
        """
        messages: List[str] = []
        v = self.interpreter.vars

        if char_idx < 0 or char_idx >= len(v.chars):
            return messages

        char = v.chars[char_idx]
        char_name = getattr(char, 'savestr', char.name or char.callname or "")

        slot = int(char.cflag.get(190, 0))
        if slot == 0:
            slot = char_idx

        self._store_departed_character(slot, char)

        if int(v.get_flag(1, 0)) == char_idx:
            v.set_flag(1, -1)
        if int(v.get_flag(2, 0)) == char_idx:
            v.set_flag(2, -1)

        if int(v.get_flag(1, 0)) == char_idx:
            v.set_flag(1, 0)
        if int(v.get_flag(2, 0)) > char_idx:
            v.set_flag(2, 0)

        for i in range(len(v.chars)):
            if i == char_idx:
                continue
            other = v.chars[i]
            party_idx = int(other.cflag.get(500, -1))
            if party_idx == char_idx:
                other.cflag[500] = -1

        del v.chars[char_idx]

        messages.append(f"{char_name}离去了……")

        return messages


    def _chara_return(self, slot: int, set_level: int = 0) -> List[str]:
        """角色返场事件 - 对应 @EVENT_CHARA_RETURN
        保存されたキャラデータをデシリアライズして復元
        """
        messages: List[str] = []
        restored = self._restore_departed_character(slot, set_level)

        if restored is None:
            return messages

        char_name = getattr(restored, 'savestr', restored.name or restored.callname or "")

        restored.cflag[501] = 0
        restored.cflag[502] = 0
        restored.cflag[1] = 0

        restored.base[0] = int(restored.maxbase.get(0, restored.base.get(0, 0)))
        restored.base[1] = int(restored.maxbase.get(1, restored.base.get(1, 0)))

        if int(restored.cflag.get(451, 0)) == 0:
            self._ensure_character_body_profile(restored)

        messages.append(f"{char_name}回来了！")

        return messages


    def _event_pregnancy(self, target: Character) -> List[str]:
        """Pregnancy events based on EVENT_PREGNANCY.ERB logic."""
        lines: List[str] = []
        name = target.name or "她"

        # TALENT:153 = 妊娠, TALENT:158 = 同族妊娠不可
        is_pregnant = target.talent.get(153, 0)
        no_pregnancy = target.talent.get(158, 0)

        if no_pregnancy:
            return lines  # Cannot get pregnant

        # CFLAG:101 = master vaginal ejaculation count
        # CFLAG:110 = birth day, CFLAG:102 = who impregnated
        master_count = target.cflag.get(101, 0)
        birth_day = target.cflag.get(110, 0)
        father_type = target.cflag.get(102, 0)

        _FATHER_NAMES: Dict[int, str] = {
            1: "主人", 2: "助手", 3: "奴隶", 4: "客人",
            5: "犬", 6: "怪物/触手", 7: "狂王",
        }

        if is_pregnant:
            father_name = _FATHER_NAMES.get(father_type, "不明")
            lines.append(f"{name}已经怀孕了。")
            lines.append(f"父亲：{father_name}")
            if birth_day > 0:
                lines.append(f"预产期：第{birth_day}日")
            # Weight/bust changes (CFLAG:121-124)
            weight_add = target.cflag.get(121, 0)
            bust_add = target.cflag.get(122, 0)
            if weight_add > 0:
                lines.append(f"体重增加：+{weight_add}")
            if bust_add > 0:
                lines.append(f"胸围增加：+{bust_add}")
        else:
            # Check for conception possibility
            if master_count > 0 and not no_pregnancy:
                # Simple conception check
                conception_chance = min(master_count * 5, 50)
                if random.randint(0, 99) < conception_chance:
                    lines.append(f"{name}怀孕了！")
                    target.talent[153] = 1
                    target.cflag[102] = 1  # Master
                    # Set birth day (roughly 30 days later)
                    current_day = self.interpreter.vars.flag.get(0, 0)
                    target.cflag[110] = current_day + 30
                else:
                    lines.append(f"{name}没有怀孕。")

        return lines

    # ------------------------------------------------------------------
    # CHARA_FIRST_EXP (初次经验)
    # ------------------------------------------------------------------

    def _eventfirst(self):
        """初次事件 - 桥接ERB EVENTFIRST"""
        return self.call_erb_function('EVENTFIRST')

    def _eventload(self):
        """读取事件 - 桥接ERB EVENTLOAD"""
        return self.call_erb_function('EVENTLOAD')


