from __future__ import annotations
"""Module for ExecutionMixin - 处决/流放系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ExecutionMixin:
    """Mixin providing 处决/流放系统 methods for GameEngine"""

    def _adjust_execution_prestige(self, target: Character):
        self._add_prestige_value(-10 if target.talent.get(220, 0) else 2)




    def _advance_execution_candidate_menu(self) -> bool:
        candidates = self._list_execution_candidates()
        self._render_execution_candidate_menu(candidates)
        if not candidates:
            self._pause()
            return False

        choice = self._prompt_execution_candidate_choice()
        return self._handle_execution_candidate_choice(candidates, choice)




    def _advance_execution_target_menu(self, idx: int, target: Character) -> bool:
        self._render_execution_target_menu(target)
        action_choice = self._prompt_execution_target_choice()
        return self._handle_execution_target_choice(idx, target, action_choice)




    def _apply_animal_banishment(self, idx: int, target: Character) -> tuple[bool, str]:
        self._emit_execution_reaction("banishment", target, 3)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        self._finalize_banishment_removal(idx, target)
        return True, f"{target.name} 被封印力量后化作小动物，并被放逐到了地下城外。"






    def _apply_banishment_option(self, idx: int, target: Character, option_id: int) -> tuple[bool, str]:
        blocked_reason = self._can_apply_banishment_option(target, option_id)
        if blocked_reason:
            return False, blocked_reason
        if option_id == 0:
            return self._apply_standard_banishment(idx, target)
        if option_id == 1:
            return self._apply_masculinization_banishment(idx, target)
        if option_id == 2:
            return self._apply_memory_wipe_banishment(idx, target)
        if option_id == 3:
            return self._apply_animal_banishment(idx, target)
        if option_id == 4:
            return self._apply_former_life_banishment(idx, target)
        return False, "未实现的放逐方式。"






    def _apply_campaign_exp_pillory(self, source_char: Optional[Character] = None) -> List[str]:
        campaign_id = self._get_active_campaign_id()
        if campaign_id < 1:
            return []
        source = source_char or self._get_target()
        if source is None:
            return []
        pillory_total = sum(int(source.cflag.get(flag_id, 0)) for flag_id in (661, 662, 663, 664, 665))
        support_exp = pillory_total // 5 + 1
        campaign_chars = self._get_active_campaign_characters()
        if not campaign_chars:
            return []
        for char in campaign_chars:
            char.exp[80] = char.exp.get(80, 0) + support_exp
        return [f"通过榨取攻略中的奴隶能量，活动队伍获得了 {support_exp} 点经验值支援。"]






    def _apply_character_daily_pillory_event(self, char: Character) -> List[str]:
        if int(char.cflag.get(1, 0)) != 8:
            return []
        return self._apply_daily_pillory_event_for_character(char)






    def _apply_character_release_from_pillory(self, char: Character) -> tuple[bool, str]:
        char.cflag[1] = 0
        self._reset_pillory_counts(char)
        return True, f"{char.name} 已从固定示众状态中解除。"






    def _apply_daily_auto_execution(self) -> List[str]:
        if not self._get_flag_bit(5, 3):
            return []

        messages: List[str] = []
        idx = 0
        while idx < len(self.interpreter.vars.chars):
            if idx <= 0:
                idx += 1
                continue
            target = self.interpreter.vars.chars[idx]
            if int(target.cflag.get(506, 0)) == 1 and int(target.abl.get(10, 0)) < 2 and int(target.cflag.get(700, 0)) == 0:
                messages.extend(self._execute_character_mini_execution(idx, target))
                idx = 0
                continue
            if int(target.cflag.get(506, 0)) == 1:
                messages.append(f"{target.name} 拼命地求饶，向魔王宣誓效忠。")
            idx += 1
        return messages




    def _apply_daily_pillory_event_for_character(self, char: Character) -> List[str]:
        messages = self._build_pillory_intro_lines(char)
        messages.extend(self._build_pillory_slogan_lines(char))
        counts = self._get_pillory_daily_counts(char)
        messages.extend(self._apply_pillory_daily_effects(char, counts))
        messages.extend(self._apply_campaign_exp_pillory(char))
        return messages






    def _apply_daily_pillory_events(self) -> List[str]:
        messages: List[str] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if not self._should_apply_daily_pillory_event(idx, char):
                continue
            messages.extend(self._apply_character_daily_pillory_event(char))
        return messages






    def _apply_execution_action(self, idx: int, target: Character, action_id: int) -> tuple[bool, str]:
        blocked_reason = self._can_execute_action(target, action_id)
        if blocked_reason:
            return False, blocked_reason

        handler = self._get_execution_action_handler(action_id)
        if handler is None:
            return False, "未实现的处刑方式。"
        return handler(idx, target)






    def _apply_execution_action_captive_furniture(self, idx: int, target: Character) -> tuple[bool, str]:
        self.interpreter.vars.set_flag(83, self.interpreter.vars.get_flag(83, 0) + 1)
        self._adjust_execution_prestige(target)
        self._set_execution_related_title(target, "肉便器")
        self._set_execution_alias(target, f"肉便器{target.name}")
        self._record_execution_public_video(f"肉便器{target.name}", target)
        return self._finalize_execution_removal(idx, target)






    def _apply_execution_action_pillory(self, idx: int, target: Character) -> tuple[bool, str]:
        target.cflag[1] = 8
        self._clear_execution_equipment(target)
        self._set_execution_related_title(target, "魔族公厕")
        self._set_execution_alias(target, f"魔族公厕{target.name}")
        self._record_execution_video_title_only(f"魔族公厕{target.name}", target)
        return True, f"{target.name} 被固定示众，状态变更为晒し台。"






    def _apply_execution_action_puppet(self, idx: int, target: Character) -> tuple[bool, str]:
        target.talent[254] = 1
        if 13 in target.cflag:
            target.cflag[13] //= 2
        if 14 in target.cflag:
            target.cflag[14] //= 2
        self._clear_execution_equipment(target)
        self._set_execution_related_title(target, "魔王傀儡")
        self._set_execution_alias(target, f"魔王傀儡{target.name}")
        self._record_execution_video_title_only(f"魔王傀儡{target.name}", target)
        return True, f"{target.name} 被刻上服从刻印，转化为魔王傀儡。"






    def _apply_execution_action_release_hero(self, idx: int, target: Character) -> tuple[bool, str]:
        return self._release_execution_target_as_invading_hero(target)






    def _apply_execution_batch_action(self, candidate_map: Dict[int, Character], selected_indices: set[int], action_id: int) -> None:
        blocked = self._get_execution_batch_blocked_targets(candidate_map, selected_indices, action_id)
        if blocked:
            print("\n批量处刑对象中包含无法执行该方式的目标，请检查名单。")
            for name, reason in blocked:
                print(f" - {name}: {reason}")
            self._pause()
            return
        for idx in sorted(selected_indices, reverse=True):
            target = candidate_map.get(idx)
            if target is None:
                continue
            ok, message = self._apply_execution_action(idx, target, action_id)
            print(f"\n{message}")
        selected_indices.clear()
        self._pause()




    def _apply_former_life_banishment(self, idx: int, target: Character) -> tuple[bool, str]:
        self._emit_execution_reaction("banishment", target, 4)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        lines, maturo = self._build_former_life_banishment_result(target)
        for line in lines:
            print(line)
        print(f"——下场：{maturo}")
        self._finalize_banishment_removal(idx, target)
        return True, f"{target.name} 的力量被封印后，被放逐回了成为勇者前的生活。"






    def _apply_grotesque_execution(self, idx: int, target: Character) -> tuple[bool, str]:
        print("\n【猎奇向处刑】")
        for option in self._get_grotesque_execution_options():
            print(f" [{option['id']}] {option['name']}")
        print(" [100] 退出")
        choice = self._prompt_choice()
        if choice == "100":
            return False, "已取消。"
        try:
            option_id = int(choice)
        except ValueError:
            return False, "Invalid selection."
        option = next((item for item in self._get_grotesque_execution_options() if int(item["id"]) == option_id), None)
        if option is None:
            return False, "Invalid selection."

        self._emit_execution_reaction("grotesque_execution", target, option_id)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        mature_title = self._build_grotesque_execution_mature_title(target, option_id)
        self._set_execution_result_identity(target, mature_title)
        self._print_grotesque_execution_outcome(target, option_id)
        video_title = f"{mature_title}{target.name}"
        self._record_execution_public_video(video_title, target)
        self._finalize_execution_removal(idx, target)
        return True, f"{target.name} 被施以{option['name']}，留下了《{video_title}》的记录。"






    def _apply_masculinization_banishment(self, idx: int, target: Character) -> tuple[bool, str]:
        self._emit_execution_reaction("banishment", target, 1)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        target.talent[122] = 1
        print(f"{target.name} 所有的力量都在烙印被打上的那一瞬间被封印了。")
        print(f"{target.name} 的身体被咒语改变成为男性，不可逆转。")
        print("放逐的过程中，他也渐渐忘记了自己曾是女性的事实，决定今后将作为男性继续活下去……")
        self._finalize_banishment_removal(idx, target)
        return True, f"{target.name} 被施予男性化的诅咒后放逐。"






    def _apply_memory_wipe_banishment(self, idx: int, target: Character) -> tuple[bool, str]:
        self._emit_execution_reaction("banishment", target, 2)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        self._finalize_banishment_removal(idx, target)
        return True, f"{target.name} 的记忆与力量被封印后，被茫然地放逐到了地下城外。"






    def _apply_museum_execution(self, idx: int, target: Character) -> tuple[bool, str]:
        print("\n【博物馆展品】")
        print(" 要制作成什么样的展品呢？")
        for option in self._get_museum_exhibit_options():
            print(f" [{option['id']}] {option['name']}")
        print(" [100] 返回")
        choice = self._prompt_choice()
        if choice == "100":
            return False, "已取消。"
        try:
            option_id = int(choice)
        except ValueError:
            return False, "Invalid selection."
        option = next((item for item in self._get_museum_exhibit_options() if int(item["id"]) == option_id), None)
        if option is None:
            return False, "Invalid selection."

        self._adjust_execution_prestige(target)
        self.interpreter.vars.set_flag(84, self.interpreter.vars.get_flag(84, 0) + 1)
        flag_id = self._get_museum_exhibit_flag_id(target, option)
        self.interpreter.vars.set_flag(flag_id, self.interpreter.vars.get_flag(flag_id, 0) + 1)
        exhibit_title = self._get_museum_exhibit_title(target, option)
        mature_title = self._build_museum_mature_title(target, option)
        self._set_execution_result_identity(target, mature_title)
        video_title = f"{mature_title}{target.name}"
        self._record_execution_public_video(video_title, target)
        self._finalize_execution_removal(idx, target)
        achievement_lines = self._apply_museum_collection_achievement_if_needed()
        message = f"{target.name} 被制成了博物馆展品《{video_title}》。"
        if achievement_lines:
            message = "\n".join([message, *achievement_lines])
        return True, message






    def _apply_pillory_daily_counter_exp(self, char: Character, name: str, count: int) -> None:
        if name == "vaginal":
            char.exp[0] = char.exp.get(0, 0) + max(1, count // 3)
            char.exp[5] = char.exp.get(5, 0) + max(1, count // 4)
        elif name == "anal":
            char.exp[1] = char.exp.get(1, 0) + max(1, count // 3)
        elif name == "oral":
            char.exp[22] = char.exp.get(22, 0) + max(1, count // 3)
        elif name == "breast":
            char.exp[3] = char.exp.get(3, 0) + max(1, count // 2)






    def _apply_pillory_daily_counter_palam(self, char: Character, name: str, count: int) -> None:
        if name == "vaginal":
            char.palam[1] = char.palam.get(1, 0) + count * 120
        elif name == "anal":
            char.palam[2] = char.palam.get(2, 0) + count * 120






    def _apply_pillory_daily_counter_updates(self, char: Character, vaginal: int, anal: int, oral: int, breast: int, other: int) -> None:
        for name, count in {
            "vaginal": vaginal,
            "anal": anal,
            "oral": oral,
            "breast": breast,
            "other": other,
        }.items():
            cflag_id, exp_id, palam_id, palam_scale = PILLORY_DAILY_COUNTER_FIELDS[name]
            char.cflag[cflag_id] = int(char.cflag.get(cflag_id, 0)) + count
            if count <= 0 or exp_id is None:
                continue
            self._apply_pillory_daily_counter_exp(char, name, count)
            self._apply_pillory_daily_counter_palam(char, name, count)






    def _apply_pillory_daily_effects(self, char: Character, counts: Dict[str, int]) -> List[str]:
        vaginal, anal, oral, breast, other, semen, beast = self._normalize_pillory_counts(counts)
        total = vaginal + anal + oral + breast + other

        self._apply_pillory_daily_stat_changes(char, vaginal, anal, oral, breast, other, semen, beast, total)
        messages = [
            f"{char.name} 被整天固定在示众台上，累计遭受了 {total} 次凌辱。",
            f"其中前穴 {vaginal} 次、后穴 {anal} 次、口部 {oral} 次、胸部 {breast} 次。",
        ]
        messages.extend(self._build_pillory_pregnancy_lines(char))
        messages.extend(self._build_pillory_count_mark_lines(char))
        messages.append(f"{char.name}被各种侮辱的涂鸦写在身上了……")
        messages.extend(self._build_pillory_daily_actor_lines(char, vaginal, anal, oral, breast, semen, beast))
        return messages






    def _apply_pillory_daily_special_updates(self, char: Character, semen: int, beast: int, total: int) -> None:
        if semen > 0:
            char.exp[20] = char.exp.get(20, 0) + max(1, semen // 4)
            char.palam[5] = char.palam.get(5, 0) + semen * 100
        if beast > 0:
            char.exp[56] = char.exp.get(56, 0) + max(1, beast // 6)
        if total > 0:
            char.palam[8] = char.palam.get(8, 0) + total * 60
            char.palam[6] = char.palam.get(6, 0) + total * 30






    def _apply_pillory_daily_stat_changes(
        self,
        char: Character,
        vaginal: int,
        anal: int,
        oral: int,
        breast: int,
        other: int,
        semen: int,
        beast: int,
        total: int,
    ):
        self._apply_pillory_daily_counter_updates(char, vaginal, anal, oral, breast, other)
        self._apply_pillory_daily_special_updates(char, semen, beast, total)






    def _apply_public_execution(self, idx: int, target: Character) -> tuple[bool, str]:
        print("\n【公开处刑】")
        for option in self._get_public_execution_options():
            print(f" [{option['id']}] {option['name']}")
        print(" [100] 算了")
        choice = self._prompt_choice()
        if choice == "100":
            return False, "已取消。"
        try:
            option_id = int(choice)
        except ValueError:
            return False, "Invalid selection."
        option = next((item for item in self._get_public_execution_options() if int(item["id"]) == option_id), None)
        if option is None:
            return False, "Invalid selection."

        self._emit_execution_reaction("public_execution", target, option_id)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        mature_title = self._build_public_execution_mature_title(target, option_id)
        self._set_execution_result_identity(target, mature_title)
        self._print_public_execution_outcome(target, option_id, mature_title)
        video_title = f"{mature_title}{target.name}"
        self._record_execution_public_video(video_title, target)
        self._finalize_execution_removal(idx, target)
        return True, f"{target.name} 被公开处刑了，留下了《{video_title}》的记录。"






    def _apply_standard_banishment(self, idx: int, target: Character) -> tuple[bool, str]:
        self._emit_execution_reaction("banishment", target, 0)
        self._adjust_execution_prestige(target)
        self._award_execution_medal(1)
        self._finalize_banishment_removal(idx, target)
        return True, f"{target.name} 的力量被封印后，被放逐到了地下城外。"






    def _award_execution_absorption(self, target: Character):
        level = int(target.cflag.get(9, 0))
        gain = (level + 1) * 50
        player = self._get_player()
        if player is not None:
            player.exp[80] = player.exp.get(80, 0) + gain
        self.interpreter.vars.set_flag(80, self.interpreter.vars.get_flag(80, 0) + 1)




    def _award_execution_medal(self, amount: int = 1):
        player = self._get_player()
        if player is not None:
            player.exp[81] = player.exp.get(81, 0) + amount




    def _build_former_life_banishment_result(self, target: Character) -> tuple[List[str], str]:
        former_life = int(target.talent.get(315, 0))
        builder = {
            1: self._build_former_life_banishment_result_student,
            2: self._build_former_life_banishment_result_nun,
            3: self._build_former_life_banishment_result_farmer,
            4: self._build_former_life_banishment_result_fisherwoman,
            5: self._build_former_life_banishment_result_prostitute,
            6: self._build_former_life_banishment_result_thief,
            7: self._build_former_life_banishment_result_beggar_prostitute,
            8: self._build_former_life_banishment_result_noble_lady,
            9: self._build_former_life_banishment_result_poor,
            10: self._build_former_life_banishment_result_gravekeeper,
            11: self._build_former_life_banishment_result_shrine_maiden,
            12: self._build_former_life_banishment_result_saint,
            13: self._build_former_life_banishment_result_prophet,
            14: self._build_former_life_banishment_result_fortune_teller,
            15: self._build_former_life_banishment_result_shopkeeper,
            16: self._build_former_life_banishment_result_village_girl,
            17: self._build_former_life_banishment_result_hermit,
            18: self._build_former_life_banishment_result_bakery_shopkeeper,
            19: self._build_former_life_banishment_result_female_officer,
            20: self._build_former_life_banishment_result_slave,
            21: self._build_former_life_banishment_result_housewife,
        }.get(former_life)
        if builder is not None:
            return builder(target)
        if former_life > 0:
            return [f"{target.name} 被放逐回了曾经的人生轨道之中。"], "下落不明"
        return [f"在此之后，{target.name} 的下落不明了……"], "下落不明"




    def _build_former_life_banishment_result_bakery_shopkeeper(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = ["面包店的"]
        lines: List[str] = []
        if target.talent.get(204, 0):
            lines.append(f"身为肉便器的 {target.name} 回乡继续经营面包店后，店里似乎多了些吸引男性顾客的可疑“副业”。")
            prefix_parts.append("沦为肉便器的")
        lines.append(f"“太可疑了，为什么客人都往 {target.name} 的店里跑？”竞争对手们私下里总是这么议论。")
        return lines, self._build_former_life_prefix(*prefix_parts, "看板娘")




    def _build_former_life_banishment_result_beggar_prostitute(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(180, 0):
            lines.append(f"不久后传来消息，{target.name} 已经沦为最底层的站街女，给多给少都会张腿。")
            prefix_parts.append("低贱的")
        lines.append(f"{target.name} 再次成为社会底层的廉价娼妇。")
        return lines, self._build_former_life_prefix(*prefix_parts, "乞丐妓女")




    def _build_former_life_banishment_result_farmer(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(13, 0):
            lines.append(f"{target.name} 坦然面对自己的过去，嫁给农夫后每日都在田里辛勤劳作。")
            prefix_parts.append("种田的")
        if int(target.exp.get(56, 0)) >= 5:
            lines.append(f"{target.name} 似乎忘不掉与家畜交尾的经验，她家里的牲畜近来都显得异常活跃。")
            prefix_parts.append("兽奸的")
        lines.append(f"总之，{target.name} 成为了一名农妇，过着平凡的生活。")
        return lines, self._build_former_life_prefix(*prefix_parts, "农妇")




    def _build_former_life_banishment_result_female_officer(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.exp.get(70, 0)) >= 5:
            lines.append(f"然而在军队内部，{target.name} 的水晶球影像早已流传甚广，军营里满是古怪的流言。")
            prefix_parts.append("恥辱的")
        lines.append(f"归队后的 {target.name}，从军之路看来并不会很顺利。")
        return lines, self._build_former_life_prefix(*prefix_parts, "女将校")




    def _build_former_life_banishment_result_fisherwoman(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(13, 0):
            lines.append(f"{target.name} 坦然面对自己的过去，努力工作，修补渔网的手艺也越来越熟练。")
            prefix_parts.append("工作上手的")
        if int(target.exp.get(74, 0)) >= 5:
            lines.append(f"偶尔有商船停靠时，{target.name} 仍会张开双腿，悄悄赚些外快。")
            prefix_parts.append("卖淫的")
        lines.append(f"总之，{target.name} 成为了一名渔妇，过着平凡的生活。")
        return lines, self._build_former_life_prefix(*prefix_parts, "渔妇")




    def _build_former_life_banishment_result_fortune_teller(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(11, 0)) > 0 or target.talent.get(36, 0):
            lines.append(f"回到故地后的 {target.name} 继续经营占卜事业，只是常把性骚扰般的戏弄掺进服务里。")
            prefix_parts.append("性骚扰")
        lines.append(f"于是，街头巷尾都流传着“变态色情占卜师”{target.name} 的故事。")
        return lines, self._build_former_life_prefix(*prefix_parts, "占卜师")




    def _build_former_life_banishment_result_gravekeeper(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(17, 0)) > 0 or target.talent.get(28, 0):
            lines.append(f"{target.name} 十分享受那些藏在暗处偷窥的淫秽目光，毕竟“全裸守墓人”本就充满刺激。")
            prefix_parts.append("露出狂")
        lines.append(f"总之，{target.name} 继续着她守墓人的生涯。")
        return lines, self._build_former_life_prefix(*prefix_parts, "守墓人")




    def _build_former_life_banishment_result_hermit(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(17, 0)) > 0 or target.talent.get(28, 0):
            lines.append(f"虽然 {target.name} 依旧不常露面，但她主演的水晶球影像却仍在市面上偷偷流传。")
            prefix_parts.append("神秘的")
        lines.append(f"总之，{target.name} 又回到了之前的隐居生活。")
        return lines, self._build_former_life_prefix(*prefix_parts, "隐居者")




    def _build_former_life_banishment_result_housewife(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.exp.get(56, 0)) >= 5:
            lines.append(f"{target.name} 最近新买了一只宠物犬，只是她看向那只狗的眼神里总带着情欲。")
            prefix_parts.append("爱好兽奸的")
        lines.append(f"面对对她过往毫不知情的丈夫，{target.name} 又回到了平静的主妇生活。")
        return lines, self._build_former_life_prefix(*prefix_parts, "主妇")




    def _build_former_life_banishment_result_noble_lady(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = ["贵族的"]
        lines: List[str] = [f"身为原贵族的 {target.name} 回到家族，重新过上与过去近似的生活。"]
        if int(target.abl.get(11, 0)) > 0 or target.talent.get(102, 0) or target.talent.get(60, 0):
            lines.append(f"只是 {target.name} 已无法压抑甜美的欲望，常常独自躲在房间里疯狂手淫。")
            prefix_parts.append("手淫中毒的")
        lines.append(f"总之，{target.name} 又回到了贵族社交圈之中。")
        return lines, self._build_former_life_prefix(*prefix_parts, "千金小姐")




    def _build_former_life_banishment_result_nun(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(13, 0)) > 0 or target.talent.get(52, 0):
            lines.append(f"{target.name} 仍十分享受替少年神官口淫时，那种愉悦与苦闷并存的表情。")
            prefix_parts.append("沦为口交母猪的")
        if int(target.abl.get(3, 0)) > 0 or target.talent.get(106, 0):
            lines.append(f"{target.name} 无法抗拒尻穴性交的背德感，暗地里继续着肮脏的买春交易。")
            prefix_parts.append("尻穴买春的")
        lines.append(f"总之，{target.name} 仍在主持着神殿的日常工作。")
        return lines, self._build_former_life_prefix(*prefix_parts, "修女")




    def _build_former_life_banishment_result_poor(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.exp.get(70, 0)) >= 5:
            lines.append(f"由于曾拍摄过的水晶球影像流出，回到贫民区后的 {target.name} 身边很快围上了不少男人。")
            prefix_parts.append("前女优")
        lines.append(f"总之，{target.name} 回到了贫民的生活中。")
        return lines, self._build_former_life_prefix(*prefix_parts, "贫民")




    def _build_former_life_banishment_result_prophet(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(13, 0)) > 0 or target.talent.get(52, 0):
            lines.append(f"回到神殿后的 {target.name} 仍享受替少年神官口淫时，那种愉悦与苦闷混杂的表情。")
            prefix_parts.append("沦为口交母猪的")
        lines.append(f"总之，{target.name} 开始继续着神殿的日常工作。")
        return lines, self._build_former_life_prefix(*prefix_parts, "预言者")




    def _build_former_life_banishment_result_prostitute(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(21, 0)) > 0:
            lines.append(f"身为抖M的 {target.name} 手活不错，在店里相当受欢迎。")
            prefix_parts.append("手交猪猡")
        if int(target.abl.get(17, 0)) > 0 or target.talent.get(28, 0):
            lines.append(f"{target.name} 喜欢在公开场合卖淫做爱取乐，甚至还向围观的人群收起了票钱。")
            prefix_parts.append("露出狂")
        lines.append(f"总之，{target.name} 又回到了之前的妓女生涯。")
        return lines, self._build_former_life_prefix(*prefix_parts, "妓女")




    def _build_former_life_banishment_result_saint(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(13, 0)) > 0 or target.talent.get(52, 0):
            lines.append(f"回到神殿后的 {target.name} 仍享受替少年神官口淫时，那种愉悦与苦闷混杂的表情。")
            prefix_parts.append("沦为口交母猪的")
        lines.append(f"总之，{target.name} 开始继续着神殿的日常工作。")
        return lines, self._build_former_life_prefix(*prefix_parts, "圣女")




    def _build_former_life_banishment_result_shopkeeper(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(204, 0):
            lines.append(f"身为肉便器的 {target.name} 回乡继续经营商店后，店里似乎多了些吸引男客的可疑“副业”。")
            prefix_parts.append("沦为肉便器的")
        lines.append(f"“今天，你进去了么？”路过 {target.name} 商店的男客们，总会露出心照不宣的笑容。")
        return lines, self._build_former_life_prefix(*prefix_parts, "看板娘")




    def _build_former_life_banishment_result_shrine_maiden(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(3, 0)) > 0 or target.talent.get(106, 0):
            lines.append(f"回到神殿后的 {target.name} 难以抵抗欲望，偷偷继续着肛交卖淫的背德交易。")
            prefix_parts.append("肛交卖淫的")
        lines.append(f"总之，{target.name} 开始继续着神殿的日常工作。")
        return lines, self._build_former_life_prefix(*prefix_parts, "巫女")




    def _build_former_life_banishment_result_slave(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(143, 0) or target.talent.get(13, 0):
            lines.append(f"几经倒卖后，{target.name} 像商品一样被转手给某位性格温柔的少年主人，对方似乎很重视她。")
            prefix_parts.append("少年专用的")
        lines.append(f"被放逐后的 {target.name}，又回到了之前的奴隶生涯。")
        return lines, self._build_former_life_prefix(*prefix_parts, "奴隶")




    def _build_former_life_banishment_result_student(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if target.talent.get(204, 0):
            lines.append(f"已经沦为肉便器的 {target.name} 成了学校里有名的荡妇。")
            prefix_parts.append("淫娃")
        if target.talent.get(48, 0):
            lines.append(f"{target.name} 朴素的眼镜装扮，看上去仍有几分学霸般的认真气质。")
            prefix_parts.append("眼镜娘")
        if target.talent.get(180, 0):
            lines.append(f"放学后，{target.name} 依旧会靠援交赚取维生的钱财。")
            prefix_parts.append("卖淫")
        lines.append(f"总之，{target.name} 以学生的身份，继续“享受”着生活。")
        return lines, self._build_former_life_prefix(*prefix_parts, "学生")




    def _build_former_life_banishment_result_thief(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(22, 0)) > 0 or target.talent.get(81, 0) or target.talent.get(82, 0):
            lines.append(f"{target.name} 热衷于诱拐女性再将其卖去卖淫，每个受害者往往还会先被她亲自染指。")
            prefix_parts.append("诱拐人口的")
        lines.append(f"于是，{target.name} 再次沦为社会底层的犯罪份子。")
        return lines, self._build_former_life_prefix(*prefix_parts, "盗贼")




    def _build_former_life_banishment_result_village_girl(self, target: Character) -> tuple[List[str], str]:
        prefix_parts: List[str] = []
        lines: List[str] = []
        if int(target.abl.get(17, 0)) > 0 or target.talent.get(28, 0):
            lines.append(f"回到村庄后的 {target.name} 喜欢独自脱光衣服，在森林中享受那种奇妙的刺激。")
            prefix_parts.append("裸体")
        lines.append(f"看来 {target.name} 打算在那个寂静的村庄中度过余生。")
        return lines, self._build_former_life_prefix(*prefix_parts, "村娘")




    def _build_grotesque_execution_mature_title(self, target: Character, option_id: int) -> str:
        option = next((item for item in self._get_grotesque_execution_options() if int(item["id"]) == option_id), None)
        return str(option["title"]) if option is not None else "猎奇处刑"






    def _build_pillory_beast_lines(self, char: Character) -> List[str]:
        lines = [
            "『谁的鸡鸡都OK！』",
            "『最爱兽奸！』",
            "『兽奸死忠』",
        ]
        return [random.choice(lines)]






    def _build_pillory_count_mark_lines(self, char: Character) -> List[str]:
        messages: List[str] = []
        messages.extend(self._build_pillory_count_mark_lines_for_group(char, 661, ["肉穴使用次数", "中出次数", "性经验急速上升中", "小穴", "被播种"], ["一", "丅", "下", "㠪"]))
        messages.extend(self._build_pillory_count_mark_lines_for_group(char, 662, ["肛门使用次数", "菊穴使用次数", "菊穴", "屁股"], ["一", "丅", "下", "㠪"]))
        messages.extend(self._build_pillory_count_mark_lines_for_group(char, 663, ["嘴巴", "污垢处理", "口爆"], ["一", "丅", "下", "㠪"]))
        messages.extend(self._build_pillory_count_mark_lines_for_group(char, 664, ["胸部", "乳房"], ["一", "丅", "下", "㠪"]))
        messages.extend(self._build_pillory_count_mark_lines_for_group(char, 665, ["其他使用次数"], ["一", "丅", "下", "㠪"], include_prefix=False))
        return messages






    def _build_pillory_count_mark_lines_for_group(
        self,
        char: Character,
        flag_id: int,
        labels: List[str],
        units: List[str],
        include_prefix: bool = True,
    ) -> List[str]:
        count = int(char.cflag.get(flag_id, 0))
        if count <= 0:
            return []
        messages: List[str] = []
        if count > 99 and flag_id == 661:
            messages.append("『正字写太多了，有点恶心』")
        if count > 49 and flag_id == 661:
            messages.append("『祝贺！达成了五十！！！』")
        if count > 29 and flag_id == 661:
            messages.append("『突破三十！！』")
        if count > 9 and flag_id == 661:
            messages.append("『真的一个打十个！』")
        label = random.choice(labels)
        prefix = f"『{label}：" if include_prefix else "『"
        body = "正" * (count // 5)
        remainder = units[count % 5 - 1] if count % 5 in {1, 2, 3, 4} else ""
        if include_prefix:
            messages.append(f"{prefix}{body}{remainder}』")
        else:
            messages.append(f"『{body}{remainder}』")
        return messages






    def _build_pillory_count_payload(
        self,
        vaginal: int,
        anal: int,
        oral: int,
        breast: int,
        sealed_front: bool,
        beast: bool,
    ) -> Dict[str, int]:
        semen = vaginal + anal + oral + random.randint(1, 10)
        if beast:
            semen += random.randint(1, 10)
        other = max(0, semen - vaginal - anal - oral - breast)
        return {
            "vaginal": 0 if sealed_front else vaginal,
            "anal": anal,
            "oral": oral,
            "breast": breast,
            "other": other,
            "semen": semen,
            "beast": semen if beast else 0,
        }






    def _build_pillory_daily_actor_lines(
        self,
        char: Character,
        vaginal: int,
        anal: int,
        oral: int,
        breast: int,
        semen: int,
        beast: int,
    ) -> List[str]:
        messages: List[str] = []
        pillory_user = random.randint(0, 4)
        if beast > 0:
            actor_name = self._get_pillory_beast_actor_name(pillory_user)
            messages.append(f"被拘束着的{char.name}，抬起了屁股，被{actor_name}侵犯着。")
            messages.append(random.choice([
                f"『这个大变态！　{actor_name}的小鸡鸡就这么舒服么』",
                "『讨厌，像野兽一样……』",
                "『感觉如何！？大声说交配很舒服！』",
            ]))
            return messages
        if anal > 0 and vaginal > 0:
            resolved_user = 2 if int(char.talent.get(143, 0)) else pillory_user
            actor_name = self._get_pillory_av_actor_name(resolved_user)
            messages.append(f"被拘束着的{char.name}，抬起了屁股，被{actor_name}侵犯着。")
            if resolved_user == 1:
                messages.append(random.choice([
                    "『做吧！真正的免费小穴！』",
                    "魔族男人舒畅地射精了。",
                    "『要…流出来了！』『喂！太快了吧！我再给你塞上……』",
                ]))
            elif resolved_user == 2:
                messages.append(random.choice([
                    "『大姐姐……我已经忍不住了！』",
                    "『啊啊啊……全部出来了！』",
                    "少年拼命地挺动着腰",
                ]))
            elif resolved_user == 3:
                messages.append(random.choice([
                    "『这个下等便器！』",
                    "『听说是免费的…又臭又脏呢』",
                    "『好好来侍奉！』",
                ]))
            else:
                messages.append(random.choice([
                    "『啊哈！！肛门也很舒服！来，怀上我的孩子吧！』",
                    "『呵呵～魔王大人！太感谢您了……』",
                    "『哇哈哈！这个程度还不足以谢罪啊！』",
            ]))
            return messages
        if anal > 0:
            resolved_user = 2 if int(char.talent.get(143, 0)) else pillory_user
            actor_name = self._get_pillory_anal_actor_name(resolved_user)
            messages.append(f"被拘束着的{char.name}，抬起了屁股，被{actor_name}侵犯着。")
            if resolved_user == 1:
                messages.append(random.choice([
                    "『走后门的时候，前面的穴居然在潮吹哦！』",
                    "『真是淫乱的肛门啊……』",
                    "『后庭已经变得这么柔软了啊？』",
                ]))
            elif resolved_user == 2:
                messages.append(random.choice([
                    "『大姐姐的肛穴……好舒服啊…………』",
                    "『啊啊啊……肛穴发出啪啪啪的声音！』",
                    "少年拼命地挺动着腰",
                ]))
            elif resolved_user == 3:
                messages.append(random.choice([
                    "『这个下等便器！』",
                    "『听说是免费的…又臭又脏呢』",
                    "『好好来侍奉！』",
                ]))
            else:
                messages.append(random.choice([
                    "『哈哈！！　后庭最棒啦！　用我的精液来给你灌肠！』",
                    "『呵呵～魔王大人！太感谢您了……』",
                    "『哇哈哈！这个程度还不足以谢罪啊！』",
                ]))
            return messages
        if vaginal > 0:
            actor_name = self._get_pillory_av_actor_name(pillory_user)
            messages.append(f"被拘束着的{char.name}，下体被{actor_name}侵犯着。")
            if pillory_user == 1:
                messages.append("『做吧！真正的免费小穴！』")
            elif pillory_user == 2:
                messages.append("『大姐姐……我已经忍不住了！』")
            elif pillory_user == 3:
                messages.append("『这个下等便器！』")
            else:
                messages.append("『啊哈！！　来，怀上我的孩子吧！』")
        return messages






    def _build_pillory_general_lines(self, char: Character) -> List[str]:
        lines = [
            "『什么都可以放进去』",
            "『精液的垃圾箱』",
            "『淫乱』",
            "『中出记录更新中』",
        ]
        return [random.choice(lines)]






    def _build_pillory_identity_lines(self, char: Character) -> List[str]:
        messages: List[str] = []
        if int(char.talent.get(15, 0)):
            race_name = self._get_pillory_race_name(int(char.talent.get(314, 0)))
            messages.append(random.choice([
                "『自尊心很高的便器哦！』",
                f"『{race_name}之耻』",
                "『死脑筋』",
            ]))
        if int(char.talent.get(248, 0)):
            messages.append("『大猩猩』")
        if int(char.talent.get(21, 0)) or int(char.talent.get(22, 0)):
            messages.append("『性冷淡』")
        if int(char.talent.get(24, 0)) or int(char.talent.get(30, 0)) or int(char.talent.get(163, 0)):
            if int(char.talent.get(0, 0)) or int(char.talent.get(273, 0)):
                messages.append("『享受名门世家的肛门吧』")
            else:
                messages.append(random.choice([
                    "『某家的大小姐』",
                    "『享受名门世家的小穴吧』",
                    "『我很幼稚，请大家用肉棒来教育我吧！』",
                    "『大小姐』",
                ]))
        if int(char.talent.get(42, 0)):
            messages.append("『马上就湿的荡妇』")
        if int(char.talent.get(61, 0)):
            messages.append(random.choice([
                "『喜欢脏东西』",
                "『请让我舔大家的屁股』",
                "『肮脏的小鸡鸡优先』",
                "『热烈欢迎脏东西』",
                "『做完之后记得尿我身上哦！』",
            ]))
        if int(char.talent.get(70, 0)) or int(char.talent.get(73, 0)):
            messages.append("『BITCH』")
        if int(char.talent.get(82, 0)):
            messages.append(random.choice([
                "『变态百合女』",
                "『我想跟女孩子做爱』",
                "『谢绝男人的小鸡鸡』",
            ]))
        if int(char.talent.get(100, 0)):
            messages.append(random.choice([
                f"『{char.name}，八岁』",
                "『←死小孩』",
                "『小孩肉穴』",
            ]))
        if int(char.talent.get(109, 0)) or int(char.talent.get(116, 0)):
            messages.append(random.choice([
                "『砧板一样的，真对不起！』",
                "『大家来帮我揉大吧！』",
                "『前后一致的女人』",
            ]))
        if int(char.talent.get(110, 0)) or int(char.talent.get(114, 0)) or int(char.talent.get(119, 0)):
            messages.append(random.choice([
                "『大胸部』",
                "『笨蛋乳』",
                "『胸大无脑』",
            ]))
        if int(char.talent.get(153, 0)):
            messages.append(random.choice([
                "『恭喜怀孕！』",
                "『十分感谢大家让我怀孕』",
                "『长枪体内过，腹中婴儿来』",
            ]))
        if int(char.talent.get(121, 0)):
            messages.append(self._get_pillory_penis_status_text(char))
        elif int(char.talent.get(122, 0)):
            messages.append("『人妖小子』")
        if int(char.talent.get(140, 0)):
            messages.append(random.choice([
                "『妈妈快来看～』",
                "『妈妈救救我～』",
                "『比妈妈更淫乱』",
            ]))
        if int(char.talent.get(141, 0)):
            messages.append(random.choice([
                "『爸爸快来看～』",
                "『想要爸爸的小鸡鸡～』",
                "『爸爸的鸡鸡最棒！』",
            ]))
        if int(char.talent.get(142, 0)):
            messages.append(random.choice([
                "『萝莉猪』",
                "『因为萝莉的小穴而兴奋』",
                "『淫乱萝莉控』",
            ]))
        if int(char.talent.get(143, 0)):
            messages.append(random.choice([
                "『正太专用便器』",
                "『正太小鸡鸡爱好者』",
                "『对不起，我是痴女』",
            ]))
        messages.extend(self._build_pillory_job_lines(char))
        messages.append(random.choice([
            "『浑身的精液臭味真对不起！』",
            "『勇者之耻』",
            "『热烈欢迎不负责任的中出』",
            f"『记住{char.name}这个名字哦！』",
            "『喜欢一边被殴打，一边被侵犯』",
            "『弱小的』",
            "『我们的目标是——黑木耳』",
            "『里面请用精液来好好关爱』",
            "『ＷＣ』",
            "『请侵犯来自遥远农村的私处』",
            "『请卜滋卜滋干个爽吧』",
            "『想要你的阴茎』",
        ]))
        return messages






    def _build_pillory_intro_lines(self, char: Character) -> List[str]:
        messages = [f"示众刑：{char.name}"]
        current_day = self._get_total_day_count()
        if int(char.cflag.get(110, 0)) == current_day:
            messages.append("（出产）")
        elif int(char.cflag.get(110, 0)) - 2 <= current_day and int(char.talent.get(153, 0)):
            messages.append("（临月）")
        elif int(char.talent.get(153, 0)):
            messages.append("（怀孕中）")
        elif int(char.talent.get(0, 0)):
            messages.append("（处女）")
        elif int(char.talent.get(273, 0)):
            messages.append("（前穴封印）")
        messages.extend(
            [
                "被固定在示众台上。",
                "姿态的她被大群男性围观着。",
            ]
        )
        return messages






    def _build_pillory_job_lines(self, char: Character) -> List[str]:
        messages: List[str] = []
        for talent_id in range(200, 210):
            if int(char.talent.get(talent_id, 0)) == 0:
                continue
            job_name = self._get_talent_name(talent_id)
            if int(char.talent.get(0, 0)) or int(char.talent.get(273, 0)):
                messages.append(random.choice([
                    f"『{job_name}勇者{char.name}，是各位专用的变态肛交妻』",
                    "『前穴是魔王大人的专用通道！』",
                    f"『{char.name}是肛门特别有感觉的变态{job_name}』",
                ]))
            else:
                messages.append(random.choice([
                    "『用肉穴向大家道歉』",
                    f"『{job_name}勇者{char.name}，除了中出，做什么都可以』",
                    "『免清洗的阴茎入口』",
                ]))
        return messages






    def _build_pillory_pregnancy_lines(self, char: Character) -> List[str]:
        if int(char.talent.get(153, 0)) == 0:
            return []
        current_day = self._get_total_day_count()
        if int(char.cflag.get(110, 0)) == current_day:
            return [random.choice([
                "『淫乱的大肚便器，小家伙～』",
                "『快临盘了，但是还是不能忘掉鸡鸡的味道～』",
                "『咦……这样淫乱的妈妈好讨厌～』",
            ])]
        if int(char.cflag.get(110, 0)) - 2 <= current_day:
            return [random.choice([
                "『祝贺怀孕！』",
                "『随便怀孕不知廉耻的小家伙～』",
                "『怀着不知道父亲是谁的孩子！』",
            ])]
        return [random.choice([
            "『现在肉穴松弛了』",
            "『被干怀孕了谢谢大家』",
            "『不管什么都好，想要怀孕啊～』",
        ])]






    def _build_pillory_slogan_lines(self, char: Character) -> List[str]:
        messages: List[str] = []
        if int(char.talent.get(0, 0)):
            messages.append("『处女』")
        elif int(char.talent.get(273, 0)):
            messages.append("『菊花专用』")
        elif int(char.abl.get(39, 0)) >= 1 and random.randint(0, 1) == 0:
            messages.extend(self._build_pillory_beast_lines(char))
        elif int(char.cflag.get(42, 0)) == 79 and (int(char.cflag.get(40, 0)) & 64) and self.interpreter.vars.get_flag(37, 0):
            messages.append("『私处禁入！』")
        else:
            messages.extend(self._build_pillory_general_lines(char))
        messages.extend(self._build_pillory_identity_lines(char))
        return messages






    def _build_public_execution_mature_title(self, target: Character, option_id: int) -> str:
        if option_id == 0:
            return "凌辱致死"
        if option_id == 1:
            return "淫行悬挂"
        if option_id == 2:
            return random.choice(
                [
                    "武具的素材",
                    "实验人形",
                    "人肉充气娃娃",
                    "淫魔的使魔",
                    "魔法师的肉体",
                    "食材",
                    "人体实验的素材",
                    "降神的傀儡",
                    "怪兽口粮",
                ]
            )
        option = next((item for item in self._get_public_execution_options() if int(item["id"]) == option_id), None)
        return str(option["title"]) if option is not None else "公开处刑"






    def _can_apply_banishment_option(self, target: Character, option_id: int) -> Optional[str]:
        if option_id == 1 and target.talent.get(122, 0):
            return f"{target.name} 已经是男性了。换个手段吧。"
        return None






    def _check_execution_available(self, target: Character) -> bool:
        """Check if execution is available for target.
        Target must have cflag:1 == 0 or 7, not be index 0, and not be
        protected by EX_TALENT:1 unless EX_TALENT:2 with EX_FLAG:9000 bit 1.
        """
        status = int(target.cflag.get(1, 0))
        if status not in (0, 7):
            return False
        # Check if character is the player (index 0)
        chars = self.interpreter.vars.chars
        if chars.index(target) == 0:
            return False
        # Check EX_TALENT protection
        ex_talent_1 = self._get_character_ex_talent(target, 1)
        if ex_talent_1 == 1:
            ex_talent_2 = self._get_character_ex_talent(target, 2)
            ex_flag_9000 = int(self.interpreter.vars.globals.get(9000, 0))
            if not (ex_talent_2 and self._get_bit(ex_flag_9000, 1)):
                return False
        return True




    def _clear_execution_equipment(self, target: Character):
        for flag_id in (550, 551, 552):
            target.cflag[flag_id] = -1




    def _emit_execution_reaction(self, event_kind: str, target: Character, option_id: int):
        line: Optional[str] = None
        if event_kind == "banishment":
            line = self._get_banishment_kojo_line(target, option_id)
        elif event_kind == "public_execution":
            line = self._get_public_execution_kojo_line(target, option_id)
        elif event_kind == "grotesque_execution":
            line = self._get_grotesque_execution_kojo_line(target, option_id)
        if line:
            print(line)






    def _execute_character_mini_execution(self, idx: int, target: Character, *, with_log: bool = True) -> List[str]:
        messages: List[str] = []
        level = int(target.cflag.get(9, 0))
        self._clear_execution_equipment(target)
        self._remove_character_at(idx)

        if with_log:
            messages.extend(
                [
                    f"给 {target.name} 刻下了封印所有力量的烙印。",
                    "继续处刑。",
                ]
            )
            previous_prestige = self._get_prestige_value()
            self._adjust_execution_prestige(target)
            current_prestige = self._get_prestige_value()
            if current_prestige != previous_prestige:
                messages.append("威望值增加。" if current_prestige > previous_prestige else "威望值减少。")

        self._award_execution_absorption(target)
        self._award_execution_medal(1)

        if with_log:
            gain = (level + 1) * 50
            messages.extend(
                [
                    "得到了用勇者力量形成的勋章。",
                    "勋章经验+1。",
                    f"《封印把勇者的力量吸收了，你获得了 {gain} 点经验值！》",
                ]
            )
        return messages




    def _execute_grotesque(self, target: Character, method: int) -> List[str]:
        """Execute grotesque method on target.
        method: 0=四肢切断, 1=内脏陵辱, 2=斩首, 3=火烧, 4=食肉, 5=死灵化, 6=僵尸化
        """
        messages: List[str] = []
        master_name = self._get_player().name if self._get_player() else "魔王"
        target_name = target.name
        has_love = target.talent.get(85, 0)  # 爱慕

        # Prestige adjustment
        if target.talent.get(220, 0) != 1 and self._get_character_ex_talent(target, 1) != 1:
            self._add_prestige_value(2)
            messages.append("威望值增加")
        else:
            self._add_prestige_value(-10)
            messages.append("威望值减少")

        if method == 0:
            # 四肢切断刑
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"四肢被固定住的{target_name}被怪物们狠狠地凌虐之后")
            messages.append("四肢被一根一根地切下，喂给了下级怪物们了")
            messages.append(f"{target_name}就这样被放置直到失血死为止了。")
            messages.append(f"{target_name}之后被漂亮地剥製后，摆在了魔王的大宫殿里当装饰了………")
            if has_love:
                messages.append(f"你十分疼爱地抚摸着被剥製后的{target_name}的脸颊………")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 1:
            # 内脏陵辱刑
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"四肢被固定住的{target_name}被怪物们活生生地刨开了腹部")
            messages.append("肝脏还有肾脏都被怪物们互相争夺吃掉了、只留下维持生命的脏器而已")
            messages.append(f"{target_name}虽然暂时还活着………不过在短暂地挣扎中力竭了………")
            if has_love:
                messages.append(f"你将{target_name}的尸体漂亮地剥製后、挂在了你的房间里当装饰了………")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 2:
            # 斩首刑
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"被固定在斩首台上的{target_name}被怪物们狠狠地侵犯的途中………")
            messages.append("斩首台的刀刃落下来了………")
            if has_love:
                messages.append(f"{target_name}被干净利落切下来的脑袋被泡在了充满福尔马林液体的罐子里保管起来了………")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 3:
            # 火烧刑
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"被实行火烧刑的{target_name}被火焰抱住了………")
            if has_love:
                messages.append(f"在火焰中的听到了{target_name}不停地哭着求救的叫声………")
            messages.append(f"变成黑炭的{target_name}的尸体被挂在了地下城入口处了")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 4:
            # 食肉刑
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印后、被执行了食肉刑………")
            messages.append(f"用魔法将其身体的痛感变成快感后、怪物们将{target_name}的身体大卸八块了………")
            if has_love:
                messages.append("「明明…明明…胸部被怪物们吃着…但是好舒服啊…啊呜…呃…嗯哼呜呜」")
                messages.append(f"{target_name}好像已经坏掉了的样子………")
            messages.append(f"最后{target_name}的脑袋被怪物们分食之后，{target_name}才咽下了最后一口气………")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 5:
            # 死灵化
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"{target_name}被施加了死灵化的诅咒………")
            messages.append(f"因为诅咒而变成低级死灵的{target_name}发出了怪异的叫声………")
            if has_love:
                messages.append(f"「啊啊啊…这样就能…一直跟{master_name}、一直一直在一起了~…好、好、好高高高高兴兴兴兴兴兴…………」")
                messages.append(f"{target_name}好像对你的身体十分地眷恋而四处徘徊着………")
            messages.append(f"{target_name}再也不能转生了，成为了地下城里的又一只游魂野鬼………")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        elif method == 6:
            # 僵尸化
            if has_love:
                messages.append(f"{target_name}就这样不知道为什么会被处刑的情况下、怜爱地叫着你的名字请求着原谅。然而{master_name}却")
            messages.append(f"在{target_name}的身上刻下了封印所有力量的烙印")
            messages.append(f"{target_name}被施加了僵尸化的诅咒………")
            messages.append(f"变成僵尸后的{target_name}进行着扩张地下城的工作………")
            if has_love:
                messages.append("「啊呜…呜…胸部…腐烂掉了…要被…要被那位大人讨厌了…嫌要被讨厌了…」")
                messages.append(f"{target_name}的嘴边不停地掉落着扭动着的蠕虫的同时喃喃自语着………")
            messages.append(f"变成永远的奴隶的{target_name}将会成为你的力量的基石吧。")
            messages.append("")
            messages.append("到手的勇者之力以勋章的形式保留下来了")
            messages.append("勋章经验+1")
            self._award_execution_medal(1)

        # Common: remove character and award XP
        idx = self.interpreter.vars.chars.index(target)
        self._clear_execution_equipment(target)
        self._remove_character_at(idx)
        self._award_execution_absorption(target)
        level = int(target.cflag.get(9, 0))
        gain = (level + 1) * 50
        messages.append(f"《吸收了被封印的勇者之力后你获得了{gain}的经验值！》")

        return messages

    # =========================================================================
    # FULLMOON (满月事件)
    # =========================================================================






    def _finalize_banishment_removal(self, idx: int, target: Character):
        self._clear_execution_equipment(target)
        self._remove_character_at(idx)






    def _finalize_execution_removal(self, idx: int, target: Character) -> tuple[bool, str]:
        self._clear_execution_equipment(target)
        self._award_execution_absorption(target)
        self._remove_character_at(idx)
        return True, f"{target.name} 已从地下城中移除。"






    def _get_banishment_kojo_line(self, target: Character, option_id: int) -> Optional[str]:
        kojo_num = self._get_kojo_num(target)
        if kojo_num == 119 and option_id == 0:
            if target.talent.get(85, 0):
                return "「求求你……不要……赶我走……」"
            return "「终于……可以回家了吗……啊啊……」"
        lines = {
            100: {
                0: "「即使失去力量…我也还有能做的事…！」",
            },
            101: {
                0: "「骗、骗人的吧…我的力量该不会被封印了吧………」",
            },
            110: {
                0: "「我的魔法连让小石头动一下都不行了…啊啊………」",
            },
            112: {
                0: "「我的研究、就到此为止了吗……」",
            },
        }
        return lines.get(kojo_num, {}).get(option_id)






    def _get_banishment_option_ids(self) -> List[int]:
        return [0, 1, 2, 3, 4]






    def _get_banishment_option_name(self, option_id: int) -> str:
        names = {
            0: "就这样流放掉",
            1: "施予男性化的诅咒",
            2: "消去之前的记忆",
            3: "变成小动物后放生",
            4: "让她回到成为勇者前的生活",
        }
        return names.get(option_id, f"Banishment {option_id}")






    def _get_execution_action_handler(self, action_id: int):
        return {
            0: self._prompt_banishment_action,
            1: self._apply_public_execution,
            2: self._apply_museum_execution,
            3: self._apply_grotesque_execution,
            4: self._apply_execution_action_captive_furniture,
            5: self._apply_execution_action_puppet,
            6: self._apply_execution_action_pillory,
            7: self._apply_execution_action_release_hero,
        }.get(action_id)






    def _get_execution_action_ids(self) -> List[int]:
        return [0, 1, 2, 3, 4, 5, 6, 7]






    def _get_execution_action_name(self, action_id: int) -> str:
        names = {
            0: "流放出地下城",
            1: "公开处刑",
            2: "博物馆展品",
            3: "施行猎奇向处刑",
            4: "做成肉便器",
            5: "士兵化",
            6: "固定示众",
            7: "消除记忆后释放",
        }
        return names.get(action_id, f"Execution {action_id}")






    def _get_execution_batch_blocked_targets(self, candidate_map: Dict[int, Character], selected_indices: set[int], action_id: int) -> List[tuple[str, str]]:
        blocked: List[tuple[str, str]] = []
        for idx in sorted(selected_indices):
            target = candidate_map.get(idx)
            if target is None:
                continue
            reason = self._can_execute_action(target, action_id)
            if reason:
                blocked.append((target.name, reason))
        return blocked






    def _get_grotesque_execution_kojo_line(self, target: Character, option_id: int) -> Optional[str]:
        kojo_num = self._get_kojo_num(target)
        lines: Dict[int, Dict[int, str]] = {
            100: {
                5: "「啊啊啊……这样就能……一直和你在一起了……」",
                6: "「呜……胸部腐烂掉了……会被你讨厌的……」",
            },
            101: {
                5: "「咿……不要变成那种东西……」",
                6: "「讨厌……身体都坏掉了……」",
            },
            110: {
                5: "「啊……永远都逃不掉了吗……」",
                6: "「变成尸体还要继续服从什么的……」",
            },
            112: {
                5: "「研究……到这里也结束了吗……」",
                6: "「就连死后也还要被利用吗……」",
            },
        }
        return lines.get(kojo_num, {}).get(option_id)






    def _get_grotesque_execution_options(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "name": "四肢切断刑", "title": "人棍"},
            {"id": 1, "name": "内脏陵辱刑", "title": "活体饲料"},
            {"id": 2, "name": "斩首刑", "title": "身首异处"},
            {"id": 3, "name": "火烧刑", "title": "红烧肉"},
            {"id": 4, "name": "食肉刑", "title": "肉类"},
            {"id": 5, "name": "死灵化", "title": "低级幽灵"},
            {"id": 6, "name": "僵尸化", "title": "丧尸奴隶"},
        ]






    def _get_pillory_anal_actor_name(self, pillory_user: int) -> str:
        return {
            1: "魔族男人",
            2: "黑暗精灵少年",
            3: "下级恶魔",
            4: "兽人",
        }.get(int(pillory_user), "兽人")






    def _get_pillory_av_actor_name(self, pillory_user: int) -> str:
        return {
            1: "魔族男人",
            2: "暗精灵的少年",
            3: "下等恶魔",
            4: "兽人",
        }.get(int(pillory_user), "兽人")






    def _get_pillory_beast_actor_name(self, pillory_user: int) -> str:
        return {
            1: "魔兽",
            2: "猪",
            3: "小马",
            4: "狗",
        }.get(int(pillory_user), "狗")






    def _get_pillory_daily_counts(self, char: Character) -> Dict[str, int]:
        sealed_front = int(char.cflag.get(42, 0)) == 79 and bool(int(char.cflag.get(40, 0)) & 64) and self.interpreter.vars.get_flag(37, 0) != 0
        if int(char.talent.get(0, 0)):
            vaginal = random.randint(1, 20)
            oral = random.randint(1, 10)
            return self._build_pillory_count_payload(vaginal, 0, oral, 0, sealed_front, beast=False)
        if int(char.talent.get(273, 0)):
            anal = random.randint(1, 20)
            oral = random.randint(1, 10)
            return self._build_pillory_count_payload(0, anal, oral, 0, sealed_front, beast=False)
        if int(char.abl.get(39, 0)) >= 1 and random.randint(0, 1) == 0:
            vaginal = 0 if sealed_front else random.randint(1, 10)
            anal = random.randint(1, 10)
            oral = random.randint(1, 10)
            breast = 0 if int(char.abl.get(1, 0)) < 3 and not (char.talent.get(110, 0) or char.talent.get(114, 0) or char.talent.get(119, 0)) else random.randint(1, 4)
            return self._build_pillory_count_payload(vaginal, anal, oral, breast, sealed_front, beast=True)
        if sealed_front:
            anal = random.randint(1, 20)
            oral = random.randint(1, 10)
            return self._build_pillory_count_payload(0, anal, oral, 0, True, beast=False)
        vaginal = random.randint(1, 10)
        anal = random.randint(1, 10)
        oral = random.randint(1, 10)
        breast = random.randint(0, 4) if int(char.abl.get(1, 0)) >= 3 or char.talent.get(110, 0) or char.talent.get(114, 0) or char.talent.get(119, 0) else 0
        return self._build_pillory_count_payload(vaginal, anal, oral, breast, False, beast=False)






    def _get_pillory_penis_status_text(self, char: Character) -> str:
        status = int(char.talent.get(318, 0))
        labels = {
            0: "普通阴茎",
            1: "巨根",
            2: "短小包茎",
            3: "包茎",
            4: "马阴茎",
        }
        return labels.get(status, "普通阴茎")






    def _get_pillory_race_name(self, race_id: int) -> str:
        race_names = {
            0: "人类",
            1: "精灵",
            2: "狼人",
            3: "吸血鬼",
            4: "无头骑士",
            5: "龙族",
            6: "天使",
            7: "暗精灵",
            8: "堕天使",
            9: "魔族",
            10: "霍比特人",
            11: "矮人",
        }
        return race_names.get(int(race_id), "种族")






    def _get_public_execution_kojo_line(self, target: Character, option_id: int) -> Optional[str]:
        kojo_num = self._get_kojo_num(target)
        lines = {
            100: {
                0: "「啊啊…啊啊…为什么要…这样对待我…咿…咿呀啊啊啊啊啊啊啊啊！」",
                1: "「绞刑…我要被…像罪人一样地被绞死吗………」",
            },
            101: {
                0: "「讨厌啊…咿…呀咿咿！再也不会被弄坏了！」",
            },
            110: {
                0: "「呐..开玩笑的吧？那样的…我可不觉得好笑…啊～…啊啊～！」",
                1: "「咿…绞刑不要…饶了我！…求求你了！请住手吧！请住..手..呃..！」",
            },
            112: {
                0: "「咿呀啊～！　救命啊～！」",
            },
        }
        return lines.get(kojo_num, {}).get(option_id)






    def _get_public_execution_options(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "name": "凌辱刑", "title": "凌辱致死"},
            {"id": 1, "name": "绞刑", "title": "淫行悬挂"},
            {"id": 2, "name": "魂粉砕", "title": "魂之粉碎"},
        ]






    def _handle_execution_batch_command_choice(self, choice: str) -> Optional[str]:
        if choice == "100":
            return "back"
        if choice == "101":
            enabled = self._toggle_flag_bit(9000, 2)
            print(f"\n水晶球记录已切换为 {'ON' if enabled else 'OFF'}。")
            self._pause()
            return "continue"
        return None




    def _handle_execution_batch_selection_choice(self, choice: str, candidate_map: Dict[int, Character], selected_indices: set[int]) -> str:
        if choice == "100":
            return "back"
        if choice == "121":
            if selected_indices:
                return "execute"
            print("\n尚未选择处刑对象。")
            self._pause()
            return "continue"
        try:
            selected_idx = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return "continue"
        if selected_idx not in candidate_map:
            print("\nInvalid selection.")
            self._pause()
            return "continue"
        if selected_idx in selected_indices:
            selected_indices.remove(selected_idx)
        else:
            selected_indices.add(selected_idx)
        return "continue"




    def _handle_execution_candidate_choice(self, candidates: List[tuple[int, Character]], choice: str) -> bool:
        if choice == "100":
            return True
        if choice == "121":
            self._show_execution_batch_selection_menu(candidates)
            return False

        try:
            selected_idx = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False

        selected_pair = next(((idx, char) for idx, char in candidates if idx == selected_idx), None)
        if selected_pair is None:
            print("\nInvalid selection.")
            self._pause()
            return False

        idx, target = selected_pair
        self._show_execution_target_menu(idx, target)
        return False




    def _handle_execution_target_choice(self, idx: int, target: Character, action_choice: str) -> bool:
        handled, exit_menu = self._handle_execution_target_command_choice(idx, target, action_choice)
        if handled:
            return exit_menu

        try:
            action_id = int(action_choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False

        if action_id not in self._get_execution_action_ids():
            print("\nInvalid selection.")
            self._pause()
            return False

        ok, message = self._apply_execution_action(idx, target, action_id)
        print(f"\n{message}")
        self._pause()
        return bool(ok and action_id in (0, 1, 2, 3, 4))




    def _handle_execution_target_command_choice(self, idx: int, target: Character, action_choice: str) -> tuple[bool, bool]:
        if action_choice == "100":
            return True, True
        if action_choice == "101":
            enabled = self._toggle_flag_bit(9000, 2)
            print(f"\n水晶球记录已切换为 {'ON' if enabled else 'OFF'}。")
            self._pause()
            return True, False
        return False, False




    def _is_execution_candidate(self, idx: int, target: Character) -> bool:
        if idx <= 0:
            return False
        return target.cflag.get(1, 0) in (0, 7)






    def _is_execution_video_recording_enabled(self) -> bool:
        return self._get_flag_bit(9000, 2)






    def _list_execution_candidates(self) -> List[tuple[int, Character]]:
        return [(idx, char) for idx, char in enumerate(self.interpreter.vars.chars) if self._is_execution_candidate(idx, char)]






    def _normalize_pillory_counts(self, counts: Dict[str, int]) -> Tuple[int, int, int, int, int, int, int]:
        vaginal = max(0, int(counts.get("vaginal", 0)))
        anal = max(0, int(counts.get("anal", 0)))
        oral = max(0, int(counts.get("oral", 0)))
        breast = max(0, int(counts.get("breast", 0)))
        other = max(0, int(counts.get("other", 0)))
        semen = max(0, int(counts.get("semen", 0)))
        beast = max(0, int(counts.get("beast", 0)))
        return vaginal, anal, oral, breast, other, semen, beast






    def _parse_execution_batch_action_choice(self, choice: str) -> Optional[int]:
        try:
            action_id = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None
        if action_id not in self._get_execution_action_ids():
            print("\nInvalid selection.")
            self._pause()
            return None
        return action_id




    def _pillory(self, target) -> List[str]:
        """桎梏 - 对应 @PILLORY"""
        messages: List[str] = []
        return messages






    def _print_grotesque_execution_outcome(self, target: Character, option_id: int) -> None:
        if int(target.talent.get(85, 0)):
            print(f"深爱着你的{target.name}不明白自己为何会被处刑，只能不断呼喊你的名字求饶。")
        print(f"你在{target.name}身上刻下了封锁全部力量的烙印。")
        if option_id == 0:
            print(f"四肢被固定后的{target.name}先遭到怪物们的凌虐，随后四肢被一根根切下喂给了下级怪物。")
            print(f"{target.name} 就这样被丢在原地，直到失血而死。")
            print(f"之后她被制成了漂亮的剥制装饰。")
            if int(target.talent.get(85, 0)):
                print(f"你甚至还怜爱地抚摸了被剥制后的{target.name}。")
            return
        if option_id == 1:
            print(f"{target.name} 被活生生剖开腹部，肝脏与肾脏都被怪物们争抢着吞食。")
            print("只剩维持生命的脏器后，她也只在短暂挣扎中耗尽了力气。")
            if int(target.talent.get(85, 0)):
                print(f"你把{target.name}的尸体也做成了房间里的装饰。")
            return
        if option_id == 2:
            print(f"{target.name} 被固定在斩首台上，凌辱还未结束，斩首台的刀刃就已经落下。")
            if int(target.talent.get(85, 0)):
                print(f"{target.name} 被利落切下的头颅后来还被浸泡在标本液里保存。")
            return
        if option_id == 3:
            print(f"{target.name} 在火烧刑中被火焰整个吞没。")
            if int(target.talent.get(85, 0)):
                print(f"火焰中还不断传来{target.name}哭着求救的声音。")
            print(f"最后变成焦炭的尸体被挂在了地下城入口。")
            return
        if option_id == 4:
            print(f"{target.name} 在被封印力量后遭到了食肉刑。")
            print("魔法把痛觉扭曲成快感，怪物们将她的身体一点点分食。")
            if int(target.talent.get(85, 0)):
                print("她甚至在身体被啃食时也只能发出已经坏掉般的呻吟。")
            print(f"直到头颅也被吃掉后，{target.name} 才终于断气。")
            return
        if option_id == 5:
            print(f"{target.name} 被施加了死灵化诅咒，最终变成了低级幽灵。")
            if int(target.talent.get(85, 0)):
                print(f"{target.name} 似乎因为对你过度眷恋，而像游魂般在地下城四处徘徊。")
            print(f"{target.name} 再也无法转生，只能作为地下城中的游魂继续存在。")
            return
        if option_id == 6:
            print(f"{target.name} 被施加了僵尸化诅咒，变成僵尸后继续从事扩张地下城的劳役。")
            if int(target.talent.get(85, 0)):
                print(f"{target.name} 一边让腐烂的身体往下掉着虫子，一边还在喃喃自语害怕被你厌弃。")
            print(f"{target.name} 作为永远的奴隶，将继续成为地下城力量的基石。")






    def _print_public_execution_outcome(self, target: Character, option_id: int, mature_title: str) -> None:
        if option_id == 0:
            if int(target.talent.get(85, 0)):
                print(f"深爱着你的{target.name}不明白自己为何会落到这种下场，只能不断呼喊着你的名字求饶。")
            print(f"但你依然在{target.name}身上刻下了封锁全部力量的烙印。")
            print("直到被彻底玩坏为止，她被地下城里的怪物们随意凌辱。")
            print(f"{target.name} 最终作为一时取乐的公开处刑祭品死去了。")
            if int(target.talent.get(85, 0)):
                print(f"{target.name} 的尸体后来还被怪物们郑重地当作献给你的祭品。")
            return
        if option_id == 1:
            if int(target.talent.get(85, 0)):
                print(f"深爱着你的{target.name}不明白自己为何会落到这种下场，只能不断呼喊着你的名字求饶。")
            print(f"你在{target.name}身上刻下了封锁全部力量的烙印。")
            print("她被全裸吊在地下城的大街上，脖子上挂着羞辱性的牌子。")
            print("私处与肛门都被粗大的假阳具贯穿，只能在众目睽睽之下死去。")
            if int(target.talent.get(85, 0)):
                print(f"{target.name} 的尸体被悬挂示众数日后，最终由你亲手火化。")
            return
        if option_id == 2:
            print(f"封印了{target.name}的力量后，她的四肢被拘束了起来。")
            print("在咒术师的咏唱下，白色球状的灵魂从挣扎的身体里被硬生生抽离。")
            print("你随手捏碎了那团灵魂，这场景也以“违逆魔王的勇者”为题在地下城中直播。")
            outcome_map = {
                "武具的素材": f"{target.name} 的肉体被魔界锻造工坊回收，作为武具材料再利用了。",
                "实验人形": f"{target.name} 的肉体被魔界魔法公会回收，成了实验用人偶。",
                "人肉充气娃娃": f"{target.name} 被某个军官领走，当成了人肉充气娃娃。",
                "淫魔的使魔": f"{target.name} 被偏爱百合的淫魔回收，作为使魔使用。",
                "魔法师的肉体": f"{target.name} 被隐居老魔法师夺走，当成了自己的新身体。",
                "食材": f"{target.name} 被魔界厨师回收，做成了特别菜色的食材。",
                "人体实验的素材": f"{target.name} 被魔术学院回收，成了人体实验的素材。",
                "降神的傀儡": f"{target.name} 被奇妙组织领走，成了可疑信仰的降神傀儡。",
                "怪兽口粮": f"{target.name} 最后被下级怪物们直接分食了。",
            }
            print(outcome_map.get(mature_title, f"{target.name} 最终被处理成了《{mature_title}》的下场。"))






    def _prompt_banishment_action(self, idx: int, target: Character) -> tuple[bool, str]:
        while True:
            print(f"\n【Banishment: {target.name}】")
            print("-" * 30)
            print(" 要来点有意思的放逐吗？")
            for option_id in self._get_banishment_option_ids():
                option_name = self._get_banishment_option_name(option_id)
                blocked_reason = self._can_apply_banishment_option(target, option_id)
                line = f" [{option_id}] {option_name}"
                if blocked_reason:
                    line += f"  - {blocked_reason}"
                print(line)
            print(" [100] 返回")

            choice = self._prompt_choice()
            if choice == "100":
                return False, "已取消。"
            try:
                option_id = int(choice)
            except ValueError:
                print("\nInvalid selection.")
                self._pause()
                continue
            if option_id not in self._get_banishment_option_ids():
                print("\nInvalid selection.")
                self._pause()
                continue
            return self._apply_banishment_option(idx, target, option_id)






    def _prompt_execution_candidate_choice(self) -> str:
        return self._prompt_choice()




    def _prompt_execution_target_choice(self) -> str:
        return self._prompt_choice()




    def _record_execution_public_video(self, title: str, target: Optional[Character] = None):
        if not title or not self._is_execution_video_recording_enabled():
            return
        record_target = target if target is not None else self._get_target()
        if record_target is None:
            self._maturo_video_title_only_with_campaign(title)
            return
        record_target.cstr[6] = title
        self._maturo_video_title_with_campaign(record_target, title)




    def _record_execution_video_title_only(self, title: str, target: Optional[Character] = None):
        if not title or not self._is_execution_video_recording_enabled():
            return
        record_target = target if target is not None else self._get_target()
        if record_target is not None:
            record_target.cstr[6] = title
        self._maturo_video_title_only_with_campaign(title)




    def _release_execution_target_as_invading_hero(self, target: Character) -> tuple[bool, str]:
        self._clear_execution_equipment(target)
        self._restore_character_as_invading_hero(target, karma_floor=-50, assign_spawn_position=True)
        return True, f"{target.name} 被清除了关于地下城的记忆，并重新作为侵攻者放出。"




    def _render_execution_batch_action_menu(self) -> None:
        print("\n【Execution: Batch Action】")
        print("-" * 30)
        for action_id in self._get_execution_action_ids():
            print(f" [{action_id}] {self._get_execution_action_name(action_id)}")
        print(f" [101] 水晶球记录 : {'ON' if self._is_execution_video_recording_enabled() else 'OFF'}")
        print(" [100] 停止")




    def _render_execution_batch_selection_menu(self, candidates: List[tuple[int, Character]], selected_indices: set[int]) -> None:
        print("\n【Execution: Batch Selection】")
        print("-" * 30)
        print(" 请进行处刑对象的批量选择")
        for idx, char in candidates:
            status_parts = [f"LV{self._get_character_level(char)}"]
            if char.cflag.get(700, 0):
                status_parts.append("☆收藏")
            if char.cflag.get(0, 0) > 0:
                status_parts.append("可卖掉")
            if idx in selected_indices:
                status_parts.append("处刑认可")
            print(f" [{idx}] {char.name}  {' '.join(status_parts)}")
        print(" [121] 选择处刑方式")
        print(" [100] 返回")




    def _render_execution_candidate_menu(self, candidates: List[tuple[int, Character]]) -> None:
        print("\n【Execution】")
        print("-" * 30)
        print(" 请选择处刑对象")
        for idx, char in candidates:
            status_parts = [f"LV{self._get_character_level(char)}"]
            if char.cflag.get(700, 0):
                status_parts.append("☆收藏")
            if char.cflag.get(0, 0) > 0:
                status_parts.append("可卖掉")
            status_text = " ".join(status_parts)
            print(f" [{idx}] {char.name}  {status_text}")
        print(" [121] 批量选择")
        print(" [100] Back")
        if not candidates:
            print(" 当前没有可处刑的对象。")




    def _render_execution_target_menu(self, target: Character) -> None:
        print(f"\n【Execution: {target.name}】")
        print("-" * 30)
        for action_id in self._get_execution_action_ids():
            action_name = self._get_execution_action_name(action_id)
            blocked_reason = self._can_execute_action(target, action_id)
            line = f" [{action_id}] {action_name}"
            if blocked_reason:
                line += f"  - {blocked_reason}"
            print(line)
        print(f" [101] 水晶球记录 : {'ON' if self._is_execution_video_recording_enabled() else 'OFF'}")
        print(" [100] Back")




    def _reset_pillory_counts(self, char: Character):
        for flag_id in (661, 662, 663, 664, 665):
            char.cflag[flag_id] = 0






    def _set_execution_alias(self, target: Character, alias: str):
        target.cstr[30] = alias




    def _set_execution_related_title(self, target: Character, prefix: str):
        target.cstr[5] = f"{prefix}{target.name}"




    def _set_execution_result_identity(self, target: Character, mature_title: str) -> None:
        if not mature_title:
            return
        target.cstr[5] = mature_title
        target.cstr[30] = f"{mature_title}{target.name}"




    def _should_apply_daily_pillory_event(self, idx: int, char: Character) -> bool:
        return idx > 0 and int(char.cflag.get(1, 0)) == 8






    def _show_execution_batch_action_menu(self, candidate_map: Dict[int, Character], selected_indices: set[int]) -> None:
        while True:
            self._render_execution_batch_action_menu()
            choice = self._prompt_execution_candidate_choice()
            handled = self._handle_execution_batch_command_choice(choice)
            if handled == "back":
                return
            if handled == "continue":
                continue
            action_id = self._parse_execution_batch_action_choice(choice)
            if action_id is None:
                continue
            self._apply_execution_batch_action(candidate_map, selected_indices, action_id)
            return




    def _show_execution_batch_selection_menu(self, candidates: List[tuple[int, Character]]) -> None:
        selected_indices: set[int] = set()
        candidate_map = {idx: char for idx, char in candidates}
        while True:
            self._render_execution_batch_selection_menu(candidates, selected_indices)
            choice = self._prompt_execution_candidate_choice()
            result = self._handle_execution_batch_selection_choice(choice, candidate_map, selected_indices)
            if result == "back":
                return
            if result == "execute":
                self._show_execution_batch_action_menu(candidate_map, selected_indices)




    def _show_execution_candidate_menu(self):
        while True:
            if self._advance_execution_candidate_menu():
                return




    def _show_execution_menu(self, target: Character) -> List[str]:
        """Show execution method selection menu."""
        lines: List[str] = []
        is_favorite = int(target.cflag.get(700, 0)) != 0
        can_sell = int(target.cflag.get(0, 0)) > 0

        lines.append("[0] 流放出地下城")
        lines.append("[1] 公开处刑")
        lines.append("[2] 博物馆展品")
        lines.append("[3] 施行猎奇向处刑")
        if is_favorite:
            lines.append("[4] 做成肉便器")
        else:
            lines.append("[4] 做成肉便器")
        lines.append("[5] 士兵化")
        lines.append("[6] 固定示众")
        lines.append("[7] 消除记忆后释放")
        lines.append("")
        lines.append("[100] 停止")
        ex_flag_9000 = int(self.interpreter.vars.globals.get(9000, 0))
        if self._get_bit(ex_flag_9000, 2):
            lines.append("[101] 水晶球记录 (ON)")
        else:
            lines.append("[101] 水晶球记录 (OFF)")
        return lines



    def _show_execution_target_menu(self, idx: int, target: Character):
        while True:
            if self._advance_execution_target_menu(idx, target):
                return




    def _show_grotesque_menu(self, target: Character) -> List[str]:
        """Show grotesque execution menu."""
        lines: List[str] = []
        lines.append("[0] 四肢切断刑")
        lines.append("[1] 内脏陵辱刑")
        lines.append("[2] 斩首刑")
        lines.append("[3] 火烧刑")
        lines.append("[4] 食肉刑")
        lines.append("[5] 死灵化")
        lines.append("[6] 僵尸化")
        lines.append("")
        lines.append("[100] 退出")
        return lines






    def show_execution(self):
        """Execution menu aligned to EXECUTION.ERB structure."""
        self._show_execution_candidate_menu()

    def _execution(self):
        return self.call_erb_function('EXECUTION')

    def _execution_mini(self):
        return self.call_erb_function('EXECUTION_MINI')





