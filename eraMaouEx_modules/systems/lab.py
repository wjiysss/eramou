from __future__ import annotations
"""Module for LabMixin - 实验室"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class LabMixin:
    """Mixin providing 实验室 methods for GameEngine"""

    def _advance_labo_menu(self, pages: List[Dict[str, Any]], page_index: int) -> tuple[bool, int]:
        self._render_labo_page(page_index, pages)
        choice = self._prompt_choice()
        exit_menu, next_page_index = self._handle_labo_choice(choice, page_index, pages)
        if exit_menu:
            return True, page_index
        return False, next_page_index




    def _apply_labo_amnesia(self, idx: int, target: Character) -> tuple[bool, str]:
        if idx == 0:
            return False, "不能对魔王执行记忆消去。"
        if self.interpreter.vars.assi == idx:
            self.interpreter.vars.assi = -1
        self._clear_labo_amnesia_combat_state(target)
        self._clear_labo_amnesia_talent_state(target)
        self._clear_labo_amnesia_character_state(target)
        self._restore_labo_amnesia_talent_flags(target)
        return True, f"{target.name} 失去了调教开始后的一切记忆。"






    def _apply_labo_animal(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(124, 0):
            return False, f"{target.name} 已经有动物耳朵了。"
        target.talent[124] = 1
        return True, f"{target.name} 长出了动物耳朵。"






    def _apply_labo_animal_erase(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(124, 0):
            return False, "没有动物耳朵可以消去。"
        target.talent[124] = 0
        return True, f"{target.name} 的动物耳朵被消去了。"






    def _apply_labo_battle_stat_upgrade(self, target: Character, project: Dict[str, Any]) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        stat_id = int(project["stat"])
        stat_name = self._get_labo_stat_name(stat_id)
        max_steps = self._get_labo_stat_remaining_steps(target, stat_id)
        if max_steps <= 0:
            return False, f"{stat_name}值的成长到极限了，请先提升等级。"

        affordable = self.interpreter.vars.money // int(project["cost"])
        max_count = min(max_steps, affordable)
        if max_count <= 0:
            return False, "金钱不足。"

        print(f"\n强化 {target.name} 的{stat_name}多少次呢？(1-{max_count})")
        choice = self._prompt_choice()
        try:
            count = int(choice)
        except ValueError:
            return False, "已取消。"
        if count <= 0:
            return False, "已取消。"
        if count > max_count:
            return False, "数值太大了。"

        extra_cost = int(project["cost"]) * (count - 1)
        if extra_cost > 0:
            self._charge_labo_cost(extra_cost)
        target.cflag[stat_id] = target.cflag.get(stat_id, 0) + count
        return True, f"{target.name} 的{stat_name}强化了。"






    def _apply_labo_block_feeling(self, target: Character) -> tuple[bool, str]:
        while True:
            part_id = self._choose_block_feeling_part(target)
            if part_id is None:
                return False, "已取消。"
            if part_id == -1:
                return False, "重新选择角色。"

            part_def = self._get_labo_block_feeling_part_definition(part_id)
            if part_def is None:
                return False, "输入无效。"

            blocked_reason = self._get_labo_block_feeling_blocked_reason(target, part_def)
            if blocked_reason is not None:
                print(f"\n{blocked_reason}")
                continue

            if not self._confirm_labo_block_feeling_change():
                return False, "已取消。"

            part_name, talent_id, _ = part_def
            target.talent[talent_id] = target.talent.get(talent_id, 0) | 2
            return True, f"{target.name} 的{part_name}感觉被封锁了。"






    def _apply_labo_bonyu(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(122, 0):
            return False, "【男人】不能改造母乳体质。"
        if target.talent.get(109, 0) or target.talent.get(116, 0):
            return False, "胸部过小，无法改造成母乳体质。"
        if target.talent.get(130, 0):
            return False, f"{target.name} 已经是母乳体质了。"
        target.talent[130] = 1
        if not target.talent.get(110, 0) and not target.talent.get(114, 0) and not target.talent.get(119, 0):
            target.talent[110] = 1
        return True, f"{target.name} 现在可以分泌母乳了。"






    def _apply_labo_bonyu_erase(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(130, 0):
            return False, "没有母乳体质可消去。"
        if target.talent.get(153, 0):
            return False, "孕妇无法消去母乳体质。"
        if target.talent.get(154, 0):
            return False, "育儿中的角色无法消去母乳体质。"
        target.talent[130] = 0
        return True, f"{target.name} 不再分泌母乳了。"






    def _apply_labo_brainwash_talent(self, target: Character, talent_id: int) -> tuple[bool, str]:
        if target.talent.get(talent_id, 0):
            return False, f"{target.name} 已经有【{self._get_talent_name(talent_id)}】了。"
        if target.cflag.get(0, 0) < 2:
            return False, "不能洗脑不可做助手的角色。"
        if talent_id == 133 and not (target.talent.get(121, 0) or target.talent.get(122, 0)):
            return False, "不是【扶她】和【男人】不能附加该素质，没有相应设备。"
        if target.talent.get(152, 0):
            return False, f"【{self._get_talent_name(152)}】的人不能被洗脑。"

        print(f"\n为 {target.name} 附加【{self._get_talent_name(talent_id)}】吗？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"
        target.talent[talent_id] = 1
        return True, f"{target.name} 获得【{self._get_talent_name(talent_id)}】了。"






    def _apply_labo_bustdown(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(122, 0):
            return False, "【男人】不能贫乳化。"
        if target.talent.get(116, 0):
            return False, f"{target.name} 已经平如镜子。"
        if target.talent.get(119, 0):
            target.talent[119] = 0
            target.talent[114] = 1
            return True, f"{target.name} 的胸部缩回到了爆乳阶段。"
        if target.talent.get(114, 0):
            target.talent[114] = 0
            target.talent[110] = 1
            return True, f"{target.name} 的胸部缩回到了巨乳阶段。"
        if target.talent.get(110, 0):
            target.talent[110] = 0
            return True, f"{target.name} 的胸部回到了标准大小。"
        if target.talent.get(109, 0):
            target.talent[109] = 0
            target.talent[116] = 1
            return True, f"{target.name} 的胸部线条完全消失了。"
        target.talent[109] = 1
        return True, f"{target.name} 获得了贫乳。"






    def _apply_labo_bustup(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(122, 0):
            return False, "【男人】不能巨乳化。"
        if target.talent.get(119, 0):
            return False, f"{target.name} 的胸已经是奇尺大乳了。"
        if target.talent.get(116, 0):
            target.talent[116] = 0
            target.talent[109] = 1
            return True, f"{target.name} 的胸部恢复到了贫乳阶段。"
        if target.talent.get(109, 0):
            target.talent[109] = 0
            return True, f"{target.name} 的胸部恢复到了标准大小。"
        if target.talent.get(110, 0):
            target.talent[110] = 0
            target.talent[114] = 1
            return True, f"{target.name} 获得了爆乳。"
        if target.talent.get(114, 0):
            target.talent[114] = 0
            target.talent[119] = 1
            return True, f"{target.name} 获得了奇尺大乳。"
        target.talent[110] = 1
        return True, f"{target.name} 获得了巨乳。"






    def _apply_labo_cure_insane(self, target: Character) -> tuple[bool, str]:
        if self._get_labo_medal_count() < 30:
            return False, "勋章不足，至少需要 30 个。"
        if not target.talent.get(9, 0) and not target.talent.get(123, 0):
            return False, f"{target.name} 的精神没有崩坏。"

        print(f"\n恢复 {target.name} 的理智么？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        changed = []
        clear_insane = bool(target.talent.get(9, 0))
        clear_nightmare = bool(target.talent.get(123, 0))
        if not self._consume_labo_medals(30):
            return False, "勋章不足，至少需要 30 个。"
        if clear_insane:
            changed.append("瞳孔再度射出理性的光辉")
        if clear_nightmare:
            changed.append("从无尽的噩梦中苏醒")
        if clear_insane:
            target.talent[9] = 0
        if clear_nightmare:
            target.talent[123] = 0
        return True, f"{target.name} 已恢复理智。{'；'.join(changed)}。"






    def _apply_labo_dematurity(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(135, 0):
            return False, f"{target.name} 不是未熟的人。"
        target.talent[135] = 0
        if target.talent.get(121, 0) or target.talent.get(122, 0):
            if int(target.talent.get(318, 0)) > 1:
                target.talent[318] = max(0, int(target.talent.get(318, 0)) - random.randint(0, 1))
        return True, f"{target.name} 的身体发育了，未熟特性被消去了。"






    def _apply_labo_demon_trait(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"

        selected = self._choose_labo_demon_trait()
        if selected is None:
            return False, "已取消。"
        _, label, talent_id = selected
        if target.talent.get(talent_id, 0):
            return False, f"{target.name} 已经拥有【{label}】了。"

        print(f"\n赋予 {target.name} {label}吗？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        return True, self._apply_labo_demon_trait_grant(target, talent_id)






    def _apply_labo_demon_trait_grant(self, target: Character, talent_id: int) -> str:
        target.talent[talent_id] = 1
        if talent_id == 244:
            previous_skin = None
            if target.talent.get(253, 0):
                previous_skin = "褐色肌肤"
            elif target.talent.get(255, 0):
                previous_skin = "白皙"
            target.talent[253] = 0
            target.talent[255] = 0
            if previous_skin is not None:
                return f"{target.name} 的{previous_skin}变成恶魔肌肤了。"
            return f"{target.name} 获得恶魔般的肌肤了。"
        if talent_id == 245:
            return f"{target.name} 长出了恶魔的翅膀。"
        if talent_id == 246:
            return f"{target.name} 长出了恶魔的尾巴。"
        if talent_id == 247:
            return f"{target.name} 获得了恶魔的眼睛。"
        return f"{target.name} 获得了恶魔体征。"






    def _apply_labo_erase_encharmed(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        if not target.talent.get(280, 0):
            return False, f"你确定 {target.name} 曾被狂王俘虏过？"

        print(f"\n将 {target.name} 被狂王俘虏的印记消去？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        target.talent[280] = 0
        return True, f"《{target.name} 的【{self._get_talent_name(280)}】被消去了》"






    def _apply_labo_extra_preg_erase(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(340, 0):
            return False, f"{target.name} 并不是异常妊娠体质。"
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        target.talent[340] = 0
        return True, f"{target.name} 的异常妊娠体质消除了。"






    def _apply_labo_extra_preg_mark(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(340, 0):
            return False, f"{target.name} 已经拥有了异常妊娠体质。"
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        target.talent[340] = 1
        return True, f"{target.name} 获得了异常妊娠体质。"






    def _apply_labo_free_train(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        current = str(target.cstr.get(7, "")).strip()
        if current:
            print(f"\n设定新的内容的话{current}调教成果将被重置。")
        print(f"\n要对{target.name}进行自由局部调教设定吗？")
        print(" [0] 是")
        print(" [1] 放弃")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"
        print("\n请输入新的自由局部调教项目。")
        print("发送空白将会重置。")
        custom_text = self._prompt_choice_raw("Free Train >> ")
        self._reset_labo_free_train_progress(target)
        target.cstr[7] = custom_text
        if not custom_text:
            return True, "自由局部调教重置完毕。"
        return True, f"{custom_text} 调教设定完毕。"






    def _apply_labo_futanari(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(121, 0) or target.talent.get(122, 0):
            return False, f"{target.name} 已经有兵器了。"
        print("\n要赋予什么样的阳具？")
        print(" [0] 普通")
        print(" [1] 巨根")
        print(" [2] 短小包茎")
        print(" [3] 包茎")
        print(" [4] 马阴茎")
        print(" [999] Back")
        choice = self._prompt_choice()
        if choice == "999":
            return False, "已取消。"
        try:
            style = int(choice)
        except ValueError:
            return False, "输入无效。"
        if style not in (0, 1, 2, 3, 4):
            return False, "输入无效。"
        target.talent[121] = 1
        target.talent[326] = 0
        target.talent[318] = style
        target.talent[1] = 1
        return True, f"{target.name} 获得了扶她化改造。"






    def _apply_labo_futanari_erase(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(122, 0):
            return False, "本作暂不提供阉割功能。"
        if not target.talent.get(121, 0):
            return False, "没有可消去的阴茎。"
        target.talent[121] = 0
        return True, f"{target.name} 的扶她特征被消去了。"






    def _apply_labo_grant_human_life(self, target: Character) -> tuple[bool, str]:
        if self._get_labo_medal_count() <= 0:
            return False, "没有可供交换的勋章。"
        if target.talent.get(85, 0) == 0:
            return False, f"{target.name} 已经没有继续留在人间的理由了。"
        if target.base.get(10, 0) == 0 and target.talent.get(124, 0) == 0:
            return False, f"{target.name} 已经拥有超长的寿命了。"

        if not self._confirm_labo_grant_human_life(target):
            return False, "已取消。"

        new_talent_124, new_base_10, messages = self._build_labo_grant_human_life_state(target)
        if not messages:
            return False, f"{target.name} 已经拥有超长的寿命了。"
        if not self._spend_all_labo_medals():
            return False, "没有可供交换的勋章。"
        target.talent[124] = new_talent_124
        target.base[10] = new_base_10
        return True, "；".join(messages) + "。"






    def _apply_labo_hair_color(self, target: Character) -> tuple[bool, str]:
        current = self._get_hair_color_name(int(target.talent.get(300, 0)))
        print(f"\n变成什么颜色？（现在：{current}）")
        for color_id in range(7):
            print(f" [{color_id}] {self._get_hair_color_name(color_id + 1)}")
        print(" [999] 取消")
        choice = self._prompt_choice_int()
        if choice == 999:
            return False, "已取消。"
        if choice is None:
            return False, "输入无效。"
        if choice not in range(7):
            return False, "输入无效。"
        new_color = choice + 1
        print(f"\n要将{target.name}的头发变成{self._get_hair_color_name(new_color)}吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"
        target.talent[300] = new_color
        return True, f"{target.name} 的发色变成【{self._get_hair_color_name(new_color)}】了。"






    def _apply_labo_horn(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        if target.talent.get(264, 0):
            return False, f"{target.name} 已经长着犄角了。"
        target.talent[264] = 1
        return True, f"{target.name} 长出了犄角。"






    def _apply_labo_life_cradle(self) -> tuple[bool, str]:
        available, message = self._can_use_life_cradle()
        if not available:
            return False, message

        selected = self._choose_life_cradle_template()
        if selected is None:
            return False, "已取消。"

        new_char = self._prepare_life_cradle_character(selected)
        if new_char is None:
            return False, "已取消。"

        stage_result = self._run_life_cradle_customization_stage(new_char)
        if stage_result is not None:
            return stage_result

        price = self._get_chara_cost_value(new_char)
        final_result = self._finalize_life_cradle_character(new_char, price)
        if not final_result[0]:
            return final_result

        self._apply_life_cradle_post_creation(new_char)
        return True, f"花费金钱 {price} 点，{new_char.name} 现已加入地下城。"






    def _apply_labo_love_corruption_swap(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"

        if self._can_swap_love_to_corruption(target):
            target.talent[85] = 0
            target.talent[76] = 1
            self._apply_love_corruption_swap_story_reset(target, 76)
            return True, (
                f"《{target.name}的【{self._get_talent_name(85)}】被消去了》\n"
                f"{target.name}看你的眼神，好像忘记了你还有上半身……\n"
                f"{target.name}沉迷于魔王给予的快感之中了……\n"
                f"{target.name}获得了【{self._get_talent_name(76)}】。"
            )

        if self._can_swap_corruption_to_love(target):
            target.talent[76] = 0
            target.talent[85] = 1
            self._apply_love_corruption_swap_story_reset(target, 85)
            return True, (
                f"《{target.name}的【{self._get_talent_name(76)}】被消去了》\n"
                f"{target.name}柔情似水地看着你……\n"
                f"{target.name}因你的行为而感到喜悦。想粘着你，想为你分忧，为你做些什么……渴望着你的宠爱。\n"
                f"{target.name}获得了【{self._get_talent_name(85)}】。"
            )

        return False, f"{target.name}改变失败了"






    def _apply_labo_magic_resistance(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        if target.talent.get(257, 0):
            return False, f"{target.name} 已经拥有魔法耐性了。"
        print(f"\n赋予 {target.name} 魔法耐性吗？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"
        target.talent[257] = 1
        return True, f"《{target.name} 获得了魔法耐性》"






    def _apply_labo_omorashi_erase(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(57, 0):
            return False, "没有漏尿癖"
        target.talent[57] = 0
        target.exp[31] = 0
        return True, f"{target.name} 的漏尿癖被治好了。"






    def _apply_labo_project(self, project: Dict[str, Any]) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "没有可用的魔王角色。"

        cost = int(project["cost"])
        if self.interpreter.vars.money < cost:
            return False, "金钱不足。"

        kind = project.get("kind")
        target_pair: Optional[tuple[int, Character]] = None
        target_mode = self._get_labo_project_target_mode(kind)
        if target_mode is not None:
            target_pair = self._choose_labo_target(mode=target_mode)
            if target_pair is None:
                return False, "已取消。"

        if kind == "life_cradle":
            return self._apply_labo_life_cradle()

        self._ensure_labo_cost_accounting()
        self._charge_labo_cost(cost)
        if kind in {"item", "summon", "resurrection"}:
            return self._apply_labo_project_without_target(kind, player, cost)

        return self._apply_labo_project_with_target(kind, project, target_pair, cost)






    def _apply_labo_project_body_group(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        result = self._apply_labo_project_body_group_impl(kind, target, target_idx)
        if result is None:
            return None
        return self._finalize_labo_project_result(cost, result)






    def _apply_labo_project_body_group_impl(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
    ) -> Optional[tuple[bool, str]]:
        handlers = {
            "bustup": self._apply_labo_bustup,
            "bustdown": self._apply_labo_bustdown,
            "bonyu": self._apply_labo_bonyu,
            "bonyu_erase": self._apply_labo_bonyu_erase,
            "futanari": self._apply_labo_futanari,
            "futanari_erase": self._apply_labo_futanari_erase,
            "animal": self._apply_labo_animal,
            "animal_erase": self._apply_labo_animal_erase,
            "remove_hair": self._apply_labo_remove_hair,
            "dematurity": self._apply_labo_dematurity,
            "omorashi_erase": self._apply_labo_omorashi_erase,
            "shojo_saisei": self._apply_labo_shojo_saisei,
            "shojo_seal": self._apply_labo_shojo_seal,
            "shojo_seal_off": self._apply_labo_shojo_seal_off,
            "tattoo": self._apply_labo_tattoo,
            "hair_color": self._apply_labo_hair_color,
            "skin_color": self._apply_labo_skin_color,
        }
        handler = handlers.get(kind)
        if handler is None:
            return None
        return handler(target)






    def _apply_labo_project_stat_group(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        result = self._apply_labo_project_stat_group_impl(kind, target, target_idx, project, cost)
        if result is None:
            return None
        return self._finalize_labo_project_result(cost, result)






    def _apply_labo_project_stat_group_impl(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        handlers = {
            "stat": lambda: self._apply_labo_vital_stat_upgrade(target, int(project["stat"]), int(project["amount"])),
            "battle_stat": lambda: self._apply_labo_battle_stat_upgrade(target, project),
            "talent": lambda: self._apply_labo_talent_upgrade(target, project, cost),
            "brainwash": lambda: self._apply_labo_brainwash_talent(target, int(project["talent"])),
            "grant_human_life": lambda: self._apply_labo_grant_human_life(target),
            "cure_insane": lambda: self._apply_labo_cure_insane(target),
            "recover_chastity_key": lambda: self._apply_labo_recover_chastity_key(target),
        }
        handler = handlers.get(kind)
        if handler is None:
            return None
        return handler()






    def _apply_labo_project_status_group(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        result = self._apply_labo_project_status_group_impl(kind, target, target_idx, project)
        if result is None:
            return None
        return self._finalize_labo_project_result(cost, result)






    def _apply_labo_project_status_group_impl(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
    ) -> Optional[tuple[bool, str]]:
        handlers = {
            "amnesia": lambda: self._apply_labo_amnesia(target_idx, target),
            "block_feeling": lambda: self._apply_labo_block_feeling(target),
            "extra_preg_mark": lambda: self._apply_labo_extra_preg_mark(target),
            "extra_preg_erase": lambda: self._apply_labo_extra_preg_erase(target),
            "trans_sex": lambda: self._apply_labo_trans_sex(target),
            "free_train": lambda: self._apply_labo_free_train(target),
            "horn": lambda: self._apply_labo_horn(target),
            "demon_trait": lambda: self._apply_labo_demon_trait(target),
            "soulbound": lambda: self._apply_labo_soulbound(target),
            "soulbound_erase": lambda: self._apply_labo_soulbound_erase(target),
            "erase_encharmed": lambda: self._apply_labo_erase_encharmed(target),
            "reincarnate": lambda: self._apply_labo_reincarnation(target),
            "love_corruption_swap": lambda: self._apply_labo_love_corruption_swap(target),
        }
        handler = handlers.get(kind)
        if handler is None:
            return None
        return handler()






    def _apply_labo_project_with_target(
        self,
        kind: Optional[str],
        project: Dict[str, Any],
        target_pair: Optional[tuple[int, Character]],
        cost: int,
    ) -> tuple[bool, str]:
        if target_pair is None:
            self._refund_labo_cost(cost)
            return False, "目标无效。"

        target_idx, target = target_pair
        result = self._execute_labo_project_target_flow(kind, target, target_idx, project, cost)
        if result is not None:
            return result

        self._refund_labo_cost(cost)
        return False, f"{project['name']} 还未完全接入原作改造流程。"






    def _apply_labo_project_without_target(self, kind: Optional[str], player: Character, cost: int) -> tuple[bool, str]:
        if kind == "item":
            return self._finalize_labo_project_result(cost, self._apply_labo_tentacle_purchase(player))
        if kind == "summon":
            return self._finalize_labo_project_result(cost, self._apply_labo_shadow_summon())
        if kind == "resurrection":
            return self._finalize_labo_project_result(cost, self._apply_labo_resurrection())
        self._refund_labo_cost(cost)
        return False, "未接入该改造项目。"






    def _apply_labo_recover_chastity_key(self, target: Character) -> tuple[bool, str]:
        if self._get_labo_medal_count() <= 0:
            return False, "没有可供交换的勋章。"
        if target.cflag.get(49, 0) == 0:
            return False, f"没有为 {target.name} 找回贞操带钥匙的必要。"

        print(f"\n确认寻找 {target.name} 的贞操带钥匙吗？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        if not self._spend_all_labo_medals():
            return False, "没有可供交换的勋章。"
        target.cflag[49] = 0
        return True, f"《{target.name} 的贞操带钥匙找到了》"






    def _apply_labo_reincarnation(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"

        candidate = self._choose_reincarnation_candidate(target)
        if candidate is None:
            return False, "已取消。"

        blocked_reason = self._get_reincarnation_block_reason(target, candidate)
        if blocked_reason:
            return False, blocked_reason

        if not self._confirm_reincarnation_choice(target, candidate):
            return False, "已取消。"

        if target.talent.get(314, 0) != 9:
            target.talent[321] = target.talent.get(314, 0)
        target.talent[314] = 9
        target.talent[322] = int(candidate["monster_id"])

        bonus_messages = self._apply_reincarnation_bonus(target, str(candidate["name"]))
        hair_message = self._apply_random_reincarnation_hair_color(target)
        message = f"{target.name} 的转生仪式成功了，已经转生为【魔族中的{candidate['name']}】。"
        if bonus_messages:
            message += " " + " ".join(bonus_messages)
        if hair_message:
            message += " " + hair_message
        return True, message






    def _apply_labo_remove_hair(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(125, 0):
            return False, f"{target.name} 本来就是白虎。"
        target.talent[125] = 1
        target.talent[310] = 1
        target.talent[311] = 1
        return True, f"{target.name} 完成了永久脱毛。"






    def _apply_labo_resurrection(self) -> tuple[bool, str]:
        can_apply, message = self._can_apply_labo_resurrection()
        if not can_apply:
            return False, message

        if not self._confirm_labo_resurrection():
            return False, "已取消。"

        candidate = self._choose_labo_resurrection_candidate()
        if candidate is None:
            return False, "已取消。"

        template_id = int(candidate["template_id"])
        new_char = self._instantiate_character_from_template(template_id)
        if new_char is None:
            return False, "角色模板不存在。"

        if not self._spend_all_labo_medals():
            return False, "没有可供交换的勋章。"

        self._append_character(new_char)
        new_idx = len(self.interpreter.vars.chars) - 1
        self.interpreter.vars.set_flag(int(candidate["flag_id"]), -1)
        self.interpreter.vars.target = new_idx
        return True, f"《{new_char.name} 被从彼岸召唤回来了》"






    def _apply_labo_shadow_summon(self) -> tuple[bool, str]:
        player = self._get_player()
        can_apply, message = self._check_labo_shadow_summon_requirements(player)
        if not can_apply:
            return False, message

        template_id = self._prompt_labo_shadow_summon_template_id()
        if template_id is None:
            return False, "已取消。"

        summon = self._instantiate_character_from_template(template_id)
        if summon is None:
            return False, "所选奴隶并不存在。"

        summon.cstr[1] = summon.name
        self._apply_shadow_summon_state(summon)
        self._append_character(summon)
        player.cflag[9] = max(0, player.cflag.get(9, 0) - 30)
        self.interpreter.vars.set_flag(83, max(0, self.interpreter.vars.get_flag(83, 0) - 30))
        return True, (
            f"从魔王的影子中将 {summon.name} 召唤了出来。"
            f" 作为代价等级和肉便器减少了30，{summon.name} 处于召唤醉状态。"
        )






    def _apply_labo_shojo_saisei(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(122, 0):
            return False, "男人无法再生处女膜。"
        if target.talent.get(0, 0):
            return False, f"{target.name} 本来就是处女。"
        target.talent[0] = 1
        target.cflag[71] = target.cflag.get(71, 0) + 1
        return True, f"{target.name} 的处女膜被再生了。"






    def _apply_labo_shojo_seal(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(273, 0):
            return False, f"{target.name} 的性器已经被封印了。"
        target.talent[273] = 1
        return True, f"{target.name} 的性器被封印了。"






    def _apply_labo_shojo_seal_off(self, target: Character) -> tuple[bool, str]:
        if not target.talent.get(273, 0):
            return False, f"{target.name} 本来就没有被封印。"
        target.talent[273] = 0
        return True, f"{target.name} 的性器封印被解除了。"






    def _apply_labo_skin_color(self, target: Character) -> tuple[bool, str]:
        current = self._get_skin_color_name(target)
        selected = self._prompt_labo_skin_color_selection(target, current)
        if selected is None:
            return False, "已取消。"
        if selected < 0:
            return False, "输入无效。"
        if not self._confirm_labo_skin_color_change(target, selected):
            return False, "已取消。"
        self._apply_labo_skin_color_selection(target, selected)
        options = self._get_labo_skin_color_options()
        return True, f"{target.name} 的{current}变成{options[selected]}了。"






    def _apply_labo_skin_color_selection(self, target: Character, selected: int) -> None:
        target.talent[244] = 0
        target.talent[253] = 0
        target.talent[255] = 0
        if selected == 1:
            target.talent[255] = 1
        elif selected == 2:
            target.talent[253] = 1






    def _apply_labo_soulbound(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        if target.talent.get(274, 0):
            return False, f"{target.name} 的灵魂已经被束缚过了。"

        print(f"\n要对 {target.name} 施展魂缚吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        target.talent[274] = 1
        return True, f"《{target.name} 的灵魂被束缚了》"






    def _apply_labo_soulbound_erase(self, target: Character) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        if not target.talent.get(274, 0):
            return False, f"{target.name} 的灵魂没有被束缚。"

        print(f"\n解除 {target.name} 的魂缚状态吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        if confirm != "0":
            return False, "已取消。"

        target.talent[274] = 0
        return True, f"《{target.name} 的魂缚状态解除了》"






    def _apply_labo_talent_upgrade(self, target: Character, project: Dict[str, Any], cost: int) -> tuple[bool, str]:
        talent_id = int(project["talent"])
        if talent_id == 257:
            return self._apply_labo_magic_resistance(target)
        if target.talent.get(talent_id, 0):
            return False, f"{target.name} 已经拥有该特性。"
        target.talent[talent_id] = 1
        return True, f"{target.name} 获得了新的特性。"






    def _apply_labo_tattoo(self, target: Character) -> tuple[bool, str]:
        slot_id = self._prompt_labo_tattoo_slot(target)
        if slot_id is None:
            return False, "已取消。"
        if slot_id < 0:
            return False, "输入无效。"
        tattoo_text = self._prompt_labo_tattoo_text(target, slot_id)
        if not self._confirm_labo_tattoo_action(slot_id, tattoo_text):
            return False, "已取消。"
        self._apply_labo_tattoo_text(target, slot_id, tattoo_text)
        if tattoo_text:
            return True, f"{self._get_tattoo_slot_name(slot_id)}上雕刻了『{tattoo_text}』的刺青。"
        return True, f"{self._get_tattoo_slot_name(slot_id)}的刺青消去了。"






    def _apply_labo_tattoo_text(self, target: Character, slot_id: int, tattoo_text: str) -> None:
        target.cstr[slot_id] = tattoo_text






    def _apply_labo_tentacle_purchase(self, player: Character) -> tuple[bool, str]:
        if player.item.get("触手生物", 0) > 0:
            return False, "已经拥有触手生物。"
        self._add_item(player, "触手生物")
        return True, "已购买触手生物。"






    def _apply_labo_trans_sex(self, target: Character) -> tuple[bool, str]:
        if target.cflag.get(70, 0) and self.interpreter.vars.chars.index(target) != 0:
            return False, f"{target.name} 已经被转性过了。"
        if target.talent.get(122, 0):
            target.talent[122] = 0
            target.talent[0] = 1
            target.talent[1] = 0
        else:
            if target.talent.get(121, 0):
                target.talent[121] = 0
            target.talent[122] = 1
            target.talent[0] = 0
            target.talent[1] = 1
        target.exp[50] = target.exp.get(50, 0) + 1
        target.cflag[70] = 1
        return True, f"{target.name} 的性别被更改了。"






    def _apply_labo_vital_stat_upgrade(self, target: Character, stat_id: int, amount: int) -> tuple[bool, str]:
        if not self._is_labo_target_controlled(target):
            return False, f"{target.name} 还不在你的统治之下。"
        limit = self._get_labo_stat_limit(target, stat_id)
        current = self._get_labo_stat_current(target, stat_id)
        if current >= limit:
            return False, f"{self._get_labo_stat_name(stat_id)}的成长到极限了，请先提升等级。"
        target.maxbase[stat_id] = min(limit, target.maxbase.get(stat_id, 0) + amount)
        target.base[stat_id] = min(target.maxbase.get(stat_id, 0), target.base.get(stat_id, 0) + amount)
        return True, f"{target.name} 的{self._get_labo_stat_name(stat_id)}强化了。"






    def _build_labo_grant_human_life_state(self, target: Character) -> tuple[int, int, List[str]]:
        new_talent_124 = int(target.talent.get(124, 0))
        new_base_10 = int(target.base.get(10, 0))
        messages: List[str] = []
        if target.talent.get(124, 0):
            new_talent_124 = 0
            messages.append(f"{target.name} 的寿命被延长了")
        if target.base.get(10, 0) > 0:
            new_base_10 = 0
            messages.append(f"{target.name} 不再受当前寿命限制")
        return new_talent_124, new_base_10, messages






    def _build_labo_project_target_group_handlers(self):
        return (
            self._apply_labo_project_body_group,
            self._apply_labo_project_status_group,
            self._apply_labo_project_stat_group,
        )






    def _can_apply_labo_resurrection(self) -> tuple[bool, str]:
        if self._get_labo_medal_count() <= 0:
            return False, "人的生命可是无法购买的……"
        capacity_limit = self._get_labo_resurrection_capacity_limit()
        if len(self.interpreter.vars.chars) > capacity_limit:
            return False, "这个世界好像已经没有亡者容身之所了"
        if not self._list_labo_resurrection_candidates():
            return False, "没有可供苏生的人。"
        return True, ""






    def _can_select_labo_target(self, idx: int, target: Optional[Character], mode: str = "default") -> Optional[str]:
        if target is None:
            return "对象不存在。"
        if idx < 0 or idx >= len(self.interpreter.vars.chars):
            return "对象不存在。"
        if target.base.get(0, 0) < 1:
            return f"{target.name} 处于濒死状态，无法选择。"

        if mode == "brainwash":
            if idx == 0:
                return "不能对魔王进行洗脑。"
            if target.cflag.get(0, 0) < 2:
                return "不能洗脑不可做助手的角色。"
            return None

        if mode == "amnesia":
            if idx == 0:
                return "不能对魔王执行记忆消去。"
            state = int(target.cflag.get(1, 0))
            if state not in (0, 10):
                return "只有待机中的对象才能进行这项改造。"
            return None

        return None



    def _charge_labo_cost(self, cost: int):
        self._add_global_money(-cost)






    def _check_labo_shadow_summon_requirements(self, player: Optional[Character]) -> tuple[bool, str]:
        if player is None:
            return False, "没有可用的魔王角色。"
        if self._get_character_level(player) < 30:
            return False, "等级不足。"
        if self.interpreter.vars.get_flag(83, 0) < 30:
            return False, "肉便器数量不足。"
        return True, ""






    def _choose_labo_demon_trait(self) -> Optional[tuple[int, str, int]]:
        options = [
            (1, "恶魔的蓝色肌肤", 244),
            (2, "恶魔的翅膀", 245),
            (3, "恶魔的尾巴", 246),
            (4, "恶魔的眼睛", 247),
        ]
        print("\n要进行什么样的恶魔改造呢？")
        for menu_id, label, _ in options:
            print(f" [{menu_id}] {label}")
        print(" [999] 返回")
        choice = self._prompt_choice_int()
        if choice == 999:
            return None
        if choice is None:
            return None
        return next(((item_id, label, talent_id) for item_id, label, talent_id in options if item_id == choice), None)






    def _choose_labo_resurrection_candidate(self) -> Optional[Dict[str, Any]]:
        candidates = self._list_labo_resurrection_candidates()
        if not candidates:
            return None
        selection = self._prompt_labo_resurrection_candidate_selection(candidates)
        if selection is None:
            return None
        return next((entry for entry in candidates if int(entry["template_id"]) == selection), None)






    def _choose_labo_target(self, mode: str = "default") -> Optional[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if self._can_select_labo_target(idx, char, mode=mode) is not None:
                continue
            candidates.append((idx, char))

        if not candidates:
            return None

        print("\n请选择对象：")
        for idx, char in candidates:
            tags = []
            if char.cflag.get(0, 0) >= 2:
                tags.append("助手候选")
            if char.cflag.get(1, 0) == 10:
                tags.append("特殊待机")
            print(f" [{idx}] {char.name}" + (f" ({', '.join(tags)})" if tags else ""))
        print(" [999] Back")
        choice = self._prompt_choice()
        if choice == "999":
            return None
        try:
            selected = int(choice)
        except ValueError:
            return None
        return next(((idx, char) for idx, char in candidates if idx == selected), None)






    def _clear_labo_amnesia_character_state(self, target: Character) -> None:
        target.cflag[0] = 0
        target.cflag[2] = 0
        target.cflag[10] = 0
        target.cflag[15] = 0
        target.cflag[16] = -1
        target.cstr[3] = ""
        target.cstr[4] = ""
        self._reset_labo_free_train_progress(target)






    def _clear_labo_amnesia_combat_state(self, target: Character) -> None:
        target.abl.clear()
        target.mark.clear()
        target.palam.clear()
        target.source.clear()
        target.juel.clear()






    def _clear_labo_amnesia_talent_state(self, target: Character) -> None:
        for talent_id in range(74, 79):
            target.talent[talent_id] = 0
        for talent_id in range(230, 234):
            target.talent[talent_id] = 0
        target.talent[271] = 0
        target.talent[272] = 0
        target.talent[85] = 0
        target.talent[86] = 0






    def _confirm_labo_block_feeling_change(self) -> bool:
        print("\n此项改造属于小白鼠专用，一旦实行就无法逆转。")
        print(" [0] 确认")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        return confirm == "0"






    def _confirm_labo_grant_human_life(self, target: Character) -> bool:
        print(f"\n为 {target.name} 延长寿命？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        return confirm == "0"






    def _confirm_labo_resurrection(self) -> bool:
        print("\n过去从这个世界上消失和逝去的人，")
        print("所有的记忆都将被忘记，")
        print("好似重获新生一般出现在你面前。")
        print("……这样的结果，是你想要的吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        return confirm == "0"






    def _confirm_labo_skin_color_change(self, target: Character, selected: int) -> bool:
        options = self._get_labo_skin_color_options()
        print(f"\n将{target.name}变为{options[selected]}吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        return confirm == "0"






    def _confirm_labo_tattoo_action(self, slot_id: int, tattoo_text: str) -> bool:
        action = f"在{self._get_tattoo_slot_name(slot_id)}雕刻『{tattoo_text}』刺青" if tattoo_text else f"消去{self._get_tattoo_slot_name(slot_id)}的刺青"
        print(f"\n{action}吗？")
        print(" [0] 好的")
        print(" [1] 不要")
        confirm = self._prompt_choice()
        return confirm == "0"






    def _consume_labo_medals(self, amount: int) -> bool:
        player = self._get_player()
        if player is None:
            return False
        current = int(player.exp.get(81, 0))
        if current < amount:
            return False
        player.exp[81] = current - amount
        return True






    def _ensure_labo_cost_accounting(self):
        self.interpreter.vars.globals[4444] = self.interpreter.vars.globals.get(4444, 0)






    def _execute_labo_project_target_flow(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        target_groups = self._build_labo_project_target_group_handlers()
        return self._route_labo_project_group(target_groups, kind, target, target_idx, project, cost)






    def _finalize_labo_project_result(self, cost: int, result: tuple[bool, str]) -> tuple[bool, str]:
        ok, message = result
        if not ok:
            self._refund_labo_cost(cost)
        return ok, message






    def _get_labo_block_feeling_blocked_reason(self, target: Character, part_def: tuple[str, int, int]) -> Optional[str]:
        _, talent_id, abl_id = part_def
        if target.abl.get(abl_id, 0) > 0:
            return "已经超过LV1以上的部位无法封锁。"
        if target.talent.get(talent_id, 0) & 2:
            return "已经封锁过了。"
        return None






    def _get_labo_block_feeling_part_definition(self, part_id: int) -> Optional[tuple[str, int, int]]:
        part_map = {
            0: ("阴核", 101, 0),
            1: ("私处", 103, 2),
            2: ("肛门", 105, 3),
            3: ("乳房", 107, 1),
        }
        return part_map.get(part_id)






    def _get_labo_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        for page in self._get_labo_pages():
            for item in self._iter_visible_labo_items(page):
                if item["id"] == item_id:
                    return item
        return None






    def _get_labo_medal_count(self) -> int:
        player = self._get_player()
        if player is None:
            return 0
        return int(player.exp.get(81, 0))






    def _get_labo_pages(self) -> List[Dict[str, Any]]:
        return LABO_PAGES






    def _get_labo_project_body_modes(self) -> set[str]:
        return {
            "bustup",
            "bustdown",
            "bonyu",
            "bonyu_erase",
            "futanari",
            "futanari_erase",
            "animal",
            "animal_erase",
            "remove_hair",
            "dematurity",
            "omorashi_erase",
            "tattoo",
            "hair_color",
            "skin_color",
        }






    def _get_labo_project_default_target_mode(self, kind: Optional[str]) -> Optional[str]:
        if kind in self._get_labo_project_target_modes():
            return "default"
        return None






    def _get_labo_project_special_modes(self) -> set[str]:
        return {
            "demon_trait",
            "grant_human_life",
            "soulbound",
            "soulbound_erase",
            "erase_encharmed",
        }






    def _get_labo_project_special_target_mode(self, kind: Optional[str]) -> Optional[str]:
        if kind == "brainwash":
            return "brainwash"
        if kind == "amnesia":
            return "amnesia"
        return None






    def _get_labo_project_stat_modes(self) -> set[str]:
        return {
            "stat",
            "battle_stat",
            "talent",
            "brainwash",
            "love_corruption_swap",
            "horn",
            "reincarnate",
        }






    def _get_labo_project_status_modes(self) -> set[str]:
        return {
            "shojo_saisei",
            "shojo_seal",
            "shojo_seal_off",
            "amnesia",
            "block_feeling",
            "extra_preg_mark",
            "extra_preg_erase",
            "trans_sex",
            "free_train",
            "cure_insane",
            "recover_chastity_key",
        }






    def _get_labo_project_target_mode(self, kind: Optional[str]) -> Optional[str]:
        return self._resolve_labo_project_target_mode(kind)






    def _get_labo_project_target_modes(self) -> set[str]:
        return set().union(
            self._get_labo_project_stat_modes(),
            self._get_labo_project_body_modes(),
            self._get_labo_project_status_modes(),
            self._get_labo_project_special_modes(),
        )






    def _get_labo_resurrection_capacity_limit(self) -> int:
        return 30 if self.interpreter.vars.get_flag(5, 0) == 9 else 10






    def _get_labo_skin_color_options(self) -> Dict[int, str]:
        return {
            0: "普通肌肤",
            1: "白皙",
            2: "褐色肌肤",
        }






    def _get_labo_stat_current(self, target: Character, stat_id: int) -> int:
        if stat_id in (0, 1):
            return target.maxbase.get(stat_id, 0)
        return target.cflag.get(stat_id, 0)






    def _get_labo_stat_gain_per_step(self, stat_id: int) -> int:
        return 10 if stat_id in (0, 1) else 1






    def _get_labo_stat_limit(self, target: Character, stat_id: int) -> int:
        level = max(0, self._get_character_level(target))
        if stat_id in (0, 1):
            return 2000 + level * 50
        return level * 5






    def _get_labo_stat_name(self, stat_id: int) -> str:
        stat_names = {
            0: "HP",
            1: "气力",
            13: "攻击",
            14: "防御",
        }
        return stat_names.get(stat_id, f"能力{stat_id}")






    def _get_labo_stat_remaining_steps(self, target: Character, stat_id: int) -> int:
        limit = self._get_labo_stat_limit(target, stat_id)
        current = self._get_labo_stat_current(target, stat_id)
        gain = self._get_labo_stat_gain_per_step(stat_id)
        if current >= limit:
            return 0
        return max(0, (limit - current) // gain)






    def _grant_labo_talent_once(self, target: Character, talent_id: int) -> bool:
        if target.talent.get(talent_id, 0):
            return False
        target.talent[talent_id] = 1
        return True






    def _handle_labo_choice(self, choice: str, page_index: int, pages: List[Dict[str, Any]]) -> tuple[bool, int]:
        if choice == "999":
            return True, page_index
        if choice == "997":
            return False, (page_index - 1) % len(pages)
        if choice == "998":
            return False, (page_index + 1) % len(pages)
        try:
            project_id = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False, page_index
        project = self._get_labo_item(project_id)
        if project is None:
            print("\nInvalid selection.")
            self._pause()
            return False, page_index
        ok, message = self._apply_labo_project(project)
        print(f"\n{message}")
        self._pause()
        return False, page_index






    def _is_labo_item_visible(self, item: Dict[str, Any]) -> bool:
        kind = item.get("kind")
        if kind == "item":
            player = self._get_player()
            return player is not None and player.item.get("触手生物", 0) == 0
        if kind in {"resurrection", "grant_human_life", "cure_insane", "recover_chastity_key"}:
            return self._get_labo_medal_count() > 0
        return True






    def _is_labo_target_controlled(self, target: Character) -> bool:
        return target.cflag.get(1, 0) != 2






    def _iter_visible_labo_items(self, page: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [item for item in page["items"] if self._is_labo_item_visible(item)]






    def _labo_c_out(self, value: int) -> str:
        """Color character output.
        Corresponds to ERB @C_OUT.
        """
        color_map = {
            7: (0xE1, 0x67, 0x45),
            6: (0xF7, 0xB3, 0x57),
            5: (0xB8, 0xD2, 0x6B),
            4: (0x8C, 0xC0, 0x6C),
            3: (0x5A, 0xAD, 0x6D),
            2: (0x4C, 0xB5, 0xE8),
            1: (0x59, 0x84, 0xBD),
            0: (0x5C, 0x6A, 0xA6),
        }
        digit_map = {0: "０", 1: "１", 2: "２", 3: "３", 4: "４", 5: "５", 6: "６", 7: "７"}
        if value in color_map:
            r, g, b = color_map[value]
            return f"\033[38;2;{r};{g};{b}m{digit_map.get(value, '?')},\033[0m"
        return ","




    def _labo_color_output_test(self) -> List[str]:
        """Color output test.
        Corresponds to ERB @COLOR_OUTPUT_TEST.
        """
        lines: List[str] = []
        color_map = {
            0: (0x5C, 0x6A, 0xA6),
            1: (0x59, 0x84, 0xBD),
            2: (0x4C, 0xB5, 0xE8),
            3: (0x5A, 0xAD, 0x6D),
            4: (0x8C, 0xC0, 0x6C),
            5: (0xB8, 0xD2, 0x6B),
            6: (0xF7, 0xB3, 0x57),
            7: (0xE1, 0x67, 0x45),
        }
        digit_map = {0: "０", 1: "１", 2: "２", 3: "３", 4: "４", 5: "５", 6: "６", 7: "７"}
        for i in range(8):
            r, g, b = color_map[i]
            lines.append(f"  \033[38;2;{r};{g};{b}m{digit_map[i]},\033[0m")
        lines.append("")
        return lines




    def _labo_da_clear(self) -> None:
        """Clear the DA (map) array.
        Corresponds to ERB @DA_CLEAR.
        """
        self._labo_da = [[0] * 50 for _ in range(50)]




    def _labo_execute(self, choice: int) -> List[str]:
        """Execute a laboratory command.
        Corresponds to ERB @LABO input handling.
        """
        if choice == 100:
            return []
        elif choice == 1:
            return self._labo_color_output_test()
        elif choice == 4:
            return self._labo_geo_test()
        elif choice == 5:
            return self._labo_geo_output()
        elif choice == 6:
            self._labo_da_clear()
            return ["地图数据已清除"]
        elif choice == 7:
            return ["[HEART_R] ❤"]
        elif choice == 8:
            return self._labo_face_test()
        else:
            return []




    def _labo_face_test(self) -> List[str]:
        """Face/avatar test.
        Corresponds to ERB @U_FACE.
        """
        lines: List[str] = []
        if self.interpreter.vars.chars:
            for idx, char in enumerate(self.interpreter.vars.chars[:5]):
                lines.append(f"[{idx}] {char.name or '???'}")
        else:
            lines.append("没有可显示的角色")
        return lines

    # ------------------------------------------------------------------
    # LOOK (角色外观显示) system
    # Corresponds to ERB @LOOK_INFO / @GET_LOOK_INFO / @LOOK_INFO_LOVE
    # ------------------------------------------------------------------

    _HAIR_COLOR_NAMES = {
        1: "金发", 2: "栗发", 3: "黑发", 4: "红发", 5: "银发",
        6: "蓝发", 7: "绿发", 8: "紫发", 9: "白发", 10: "暗金发", 11: "粉发",
    }
    _HAIR_COLOR_RAW = {
        1: "金色", 2: "栗色", 3: "黑色", 4: "红色", 5: "银色",
        6: "蓝色", 7: "绿色", 8: "紫色", 9: "白色", 10: "暗金色", 11: "粉色",
    }
    _HAIR_STATE_NAMES = {
        1: "直发", 2: "卷发", 3: "内卷发", 4: "外卷发", 5: "天然卷", 6: "大波浪",
    }
    _HAIR_CUT_NAMES = {
        1: "基本剪法", 2: "齐剪", 3: "层剪", 4: "碎发",
    }
    _HAIR_STYLE_NAMES = {
        1: "自然", 2: "中分", 3: "不均分", 4: "长束发", 5: "马尾",
        6: "侧马尾", 7: "垂发辫", 8: "双马尾", 9: "顶束发", 10: "侧束发",
        11: "鱼骨辫", 12: "卷发",
    }
    _EYE_SHAPE_NAMES = {
        1: "细长眼", 2: "大眼", 3: "深邃眼", 4: "吊眼", 5: "水汪汪眼",
        6: "标准眼", 7: "三白眼", 8: "下垂眼",
    }
    _EYE_COLOR_NAMES = {
        1: "蓝色", 2: "棕色", 3: "灰色", 4: "金色", 5: "红色", 6: "黑色",
    }
    _LIP_NAMES = {
        1: "肉感的", 2: "薄的", 3: "丰润的", 4: "标准",
    }
    _BODY_TYPE_NAMES = "纤细"  # range-based
    _NIPPLE_NAMES = {
        1: "粉红色", 2: "褐色", 3: "标准", 4: "凹陷",
    }
    _PUBIC_HAIR_NAMES = "range"  # range-based
    _PENIS_STATE_NAMES = {
        1: "巨根", 2: "短小包茎", 3: "包茎", 4: "马阴茎",
    }
    _CHARM_POINT_NAMES = {
        1: "皮肤", 2: "眼角", 3: "鼻梁", 4: "嘴角", 5: "泪痣",
        6: "锁骨", 7: "小臂", 8: "手腕", 9: "手", 10: "手指",
        11: "肚脐", 12: "美乳", 13: "腰线", 14: "臀部线条", 15: "腿部线条",
        16: "膝盖", 17: "脚踝", 18: "脚跟", 19: "背脊", 20: "耳朵",
        21: "性器", 22: "头发的光泽", 23: "丰满的屁股", 24: "长睫毛", 25: "虎牙",
        26: "眉毛", 27: "指甲", 28: "寝癖",
    }
    _HABIT_NAMES = {
        1: "舔嘴唇", 2: "往后看", 3: "摸头发", 4: "用腿夹住手", 5: "抱手臂",
        6: "手指交握", 7: "抖腿", 8: "打拍子", 9: "仰视对方", 10: "歪脖子",
        11: "叹气", 12: "动作夸张", 13: "频繁眨眼", 14: "鼓腮", 15: "咬紧牙关",
        16: "遮住嘴", 17: "摸耳朵", 18: "懒散", 19: "咂嘴", 20: "咬指甲",
        21: "挠鼻子", 22: "扶额", 23: "握拳", 24: "用手指人", 25: "说口头禅",
        26: "扭腰", 27: "闭上一只眼", 28: "眯眼", 29: "歪嘴", 30: "碎碎念",
        31: "总往角落躲", 32: "估算物体长度", 33: "说话越说越近", 34: "舔手背",
    }
    _RACE_NAMES = {
        0: "人类", 1: "精灵", 2: "狼人", 3: "吸血鬼", 4: "无头骑士",
        5: "龙族", 6: "天使", 7: "暗精灵", 8: "堕天使", 9: "魔族",
        10: "霍比特人", 11: "矮人",
    }
    _RACE2_NAMES = {
        1: "兽人", 2: "史莱姆", 3: "昆虫", 4: "植物", 5: "触手", 6: "妖精",
        7: "巨人", 8: "魔族", 9: "魔族", 10: "魔兽", 11: "触手", 12: "魔兽",
    }
    _PAST_LIFE_NAMES = {
        0: "不明", 1: "学生", 2: "修女", 3: "农民", 4: "渔民", 5: "妓女",
        6: "小偷", 7: "乞丐", 8: "贵族", 9: "贫民", 10: "守墓人", 11: "巫女",
        12: "圣女", 13: "预言家", 14: "占卜师", 15: "商人", 16: "采药人",
        17: "隐士", 18: "面包师", 19: "军人", 20: "奴隶", 21: "主妇",
        90: "淫乱的产物", 91: "堕落的结果", 92: "爱的结晶",
        93: "交欢的副产品", 94: "魔族的孽种",
    }
    _HERO_REASON_NAMES = {
        0: "不明", 1: "命运的引导", 2: "为了钱", 3: "受到了上天启示",
        4: "因使命感而热血沸腾", 5: "对日常感到厌倦", 6: "经历无尽悲伤后",
        7: "拯救故乡", 8: "复仇", 9: "国王的任命", 10: "赎罪",
        11: "自暴自弃", 12: "纯属意外", 13: "被命令了", 14: "无可奈何",
        15: "测试自己的力量", 16: "为了和平", 17: "为了正义",
        18: "梦见自己有所作为", 19: "获得了力量", 20: "旅行的结果",
        90: "父母的嘱咐", 91: "憧憬魔王", 92: "为了出人头地",
        93: "为了报恩", 94: "被恶魔诱惑",
    }
    _LIKE_BASE_NAMES = {
        1: "甜食", 2: "辣条", 3: "唱歌", 4: "故乡的恋人", 5: "钱",
        6: "跳舞", 7: "绘画", 8: "家族", 9: "使命", 10: "故乡",
        11: "憧憬的那个人", 12: "可爱的动物", 13: "美丽的饰品", 14: "宝石",
        15: "点心", 16: "喝茶", 17: "睡觉", 18: "小说", 19: "开怀大笑",
        20: "游泳",
    }



    def _labo_geo_calc_interp(self, ul: int, ur: int, dl: int, dr: int,
                               dx: int, dy: int, x: int, y: int) -> None:
        """Interpolation calculation for geography.
        Corresponds to ERB @GEO_CALC_INTERP.
        """
        # Coefficient table
        coeff = {1: 4, 2: 15, 3: 31, 4: 50, 5: 69, 6: 85, 7: 96}
        px = coeff.get(dx, 0)
        py = coeff.get(dy, 0)

        result = (ul - ur - dl + dr) * px * py // 10000 + (ur - ul) * px // 100 + (dl - ul) * py // 100 + ul
        if 0 <= y < 50 and 0 <= x < 50:
            self._labo_da[y][x] = result




    def _labo_geo_output(self) -> List[str]:
        """Output the map.
        Corresponds to ERB @GEO_OUTPUT.
        """
        lines: List[str] = []
        if not hasattr(self, '_labo_da'):
            self._labo_da_clear()

        for y in range(32):
            row = ""
            for x in range(32):
                val = self._labo_da[y][x] // 32
                row += self._labo_c_out(val)
            lines.append(row)
        return lines




    def _labo_geo_test(self) -> List[str]:
        """Geography test with interpolation.
        Corresponds to ERB @GEO_TEST.
        """
        import random
        lines: List[str] = []
        points = 5
        world_size = (points - 1) * 8

        # Initialize DA if needed
        if not hasattr(self, '_labo_da'):
            self._labo_da_clear()

        # Point random generation
        for y in range(points):
            target_y = y * 8
            for x in range(points):
                target_x = x * 8
                self._labo_da[target_y][target_x] = random.randint(0, 255)

        # X-direction interpolation
        for y_idx in range(points):
            for x_idx in range(points - 1):
                x0 = x_idx * 8
                y0 = y_idx * 8
                for x in range(x0 + 1, x0 + 8):
                    self._labo_da[y0][x] = self._labo_linear_interp_cos_x(x0, x0 + 8, x, y0)

        # Y-direction interpolation
        for x_idx in range(points):
            for y_idx in range(points - 1):
                x0 = x_idx * 8
                y0 = y_idx * 8
                for y in range(y0 + 1, y0 + 8):
                    self._labo_da[y][x0] = self._labo_linear_interp_cos_y(y0, y0 + 8, y, x0)

        # Inner interpolation
        for x_idx in range(points - 1):
            for y_idx in range(points - 1):
                x0 = x_idx * 8
                y0 = y_idx * 8
                ul = self._labo_da[y0][x0]
                ur = self._labo_da[y0][x0 + 8]
                dl = self._labo_da[y0 + 8][x0]
                dr = self._labo_da[y0 + 8][x0 + 8]
                for y in range(y0 + 1, y0 + 8):
                    for x in range(x0 + 1, x0 + 8):
                        self._labo_geo_calc_interp(ul, ur, dl, dr, x - x0, y - y0, x, y)

        lines.append(f"地形生成完成 (点数={points}, 世界大小={world_size})")
        return lines




    def _labo_linear_interp_cos_x(self, x0: int, x1: int, x: int, y: int) -> int:
        """Linear interpolation on X axis.
        Corresponds to ERB @LINEAR_INTERP_COS_X.
        """
        if not hasattr(self, '_labo_da'):
            self._labo_da_clear()
        z0 = self._labo_da[y][x0] if 0 <= y < 50 and 0 <= x0 < 50 else 0
        z1 = self._labo_da[y][x1] if 0 <= y < 50 and 0 <= x1 < 50 else 0
        coeff = {1: 4, 2: 15, 3: 31, 4: 50, 5: 69, 6: 85, 7: 96}
        c = coeff.get(x - x0, 0)
        return z0 + (z1 - z0) * c // 100




    def _labo_linear_interp_cos_y(self, y0: int, y1: int, y: int, x: int) -> int:
        """Linear interpolation on Y axis.
        Corresponds to ERB @LINEAR_INTERP_COS_Y.
        """
        if not hasattr(self, '_labo_da'):
            self._labo_da_clear()
        z0 = self._labo_da[y0][x] if 0 <= y0 < 50 and 0 <= x < 50 else 0
        z1 = self._labo_da[y1][x] if 0 <= y1 < 50 and 0 <= x < 50 else 0
        coeff = {1: 4, 2: 15, 3: 31, 4: 50, 5: 69, 6: 85, 7: 96}
        c = coeff.get(y - y0, 0)
        return z0 + (z1 - z0) * c // 100




    def _list_labo_resurrection_candidates(self) -> List[Dict[str, Any]]:
        templates = self.character_template_catalog.get("templates", {})
        candidates: List[Dict[str, Any]] = []
        for template_id in sorted(templates.keys()):
            flag_id = self._get_character_vanish_flag_id(int(template_id))
            if int(self.interpreter.vars.get_flag(flag_id, 0)) <= -2:
                template = templates[template_id]
                candidates.append(
                    {
                        "template_id": int(template_id),
                        "flag_id": flag_id,
                        "name": template.name or template.callname or f"Character{template_id}",
                    }
                )
        return candidates






    def _prompt_labo_resurrection_candidate_selection(self, candidates: List[Dict[str, Any]]) -> Optional[int]:
        print("\n想要苏醒谁？")
        print("-" * 30)
        for entry in candidates:
            print(f" [{entry['template_id'] + 100}] {entry['name']}")
        print(" [999] 取消")

        choice = self._prompt_choice_int()
        if choice == 999:
            return None
        if choice is None:
            return None
        return choice - 100






    def _prompt_labo_shadow_summon_template_id(self) -> Optional[int]:
        print("\n【召唤影之仆从】")
        print(" 读取CSV来生成奴隶")
        print(" 还需要消耗30的等级和30个肉便器")
        print(" 条件达成。要生成奴隶吗？")
        print(" 若要生成，请输入要奴隶的编号")
        print(" [0] 不生成")
        choice = self._prompt_choice_int()
        if choice == 0:
            return None
        if choice is None:
            return -1
        if choice not in self._get_shadow_summon_candidate_range():
            return -1
        return choice






    def _prompt_labo_skin_color_selection(self, target: Character, current: str) -> Optional[int]:
        options = self._get_labo_skin_color_options()
        print(f"\n想要变成什么肤色？（现在：{current}）")
        for option_id, label in options.items():
            print(f" [{option_id}] {label}")
        print(" [999] 取消")
        choice = self._prompt_choice_int()
        if choice == 999:
            return None
        if choice is None:
            return -1
        if choice not in options:
            return -1
        return choice






    def _prompt_labo_tattoo_slot(self, target: Character) -> Optional[int]:
        print(f"\n{target.name} 的刺青")
        for slot_id in range(10, 18):
            current = str(target.cstr.get(slot_id, "")).strip() or "没有"
            print(f" [{slot_id}] {self._get_tattoo_slot_name(slot_id)} - 『{current}』")
        print(" [999] 停止")
        choice = self._prompt_choice_int()
        if choice == 999:
            return None
        if choice is None:
            return -1
        if choice not in range(10, 18):
            return -1
        return choice






    def _prompt_labo_tattoo_text(self, target: Character, slot_id: int) -> str:
        print("请输入想雕刻的刺青，留空代表消去。")
        current = str(target.cstr.get(slot_id, "")).strip() or "没有"
        print(f"现在雕刻的刺青是：『{current}』")
        return self._prompt_choice_raw("Tattoo >> ")






    def _refund_labo_cost(self, cost: int):
        self._add_global_money(cost)






    def _render_labo_page(self, page_index: int, pages: List[Dict[str, Any]]) -> None:
        page = pages[page_index]
        print("\n【Secret Labo】")
        print("-" * 30)
        print(f" Page {page_index + 1}/{len(pages)} - {page['title']}")
        print(f" Money: {self.interpreter.vars.money} pts")
        for item in self._iter_visible_labo_items(page):
            print(f" [{item['id']}] {item['name']} ({item['cost']}点)")
        print(" [997] Prev Page")
        print(" [998] Next Page")
        print(" [999] Back")






    def _reset_labo_free_train_progress(self, target: Character):
        target.cstr[7] = ""
        target.abl[4] = 0
        target.abl[40] = 0
        target.juel[15] = 0






    def _resolve_labo_project_target_mode(self, kind: Optional[str]) -> Optional[str]:
        special_mode = self._get_labo_project_special_target_mode(kind)
        if special_mode is not None:
            return special_mode
        return self._get_labo_project_default_target_mode(kind)






    def _restore_labo_amnesia_talent_flags(self, target: Character) -> None:
        if target.talent.get(153, 0) and not target.talent.get(155, 0) and not target.talent.get(12, 0):
            target.talent[9] = 1






    def _route_labo_project_group(self, handlers, kind: Optional[str], target: Character, target_idx: int, project: Dict[str, Any], cost: int) -> Optional[tuple[bool, str]]:
        for handler in handlers:
            result = handler(kind, target, target_idx, project, cost)
            if result is not None:
                return result
        return None






    def _route_labo_project_target(
        self,
        kind: Optional[str],
        target: Character,
        target_idx: int,
        project: Dict[str, Any],
        cost: int,
    ) -> Optional[tuple[bool, str]]:
        return self._route_labo_project_group(
            self._build_labo_project_target_group_handlers(),
            kind,
            target,
            target_idx,
            project,
            cost,
        )






    def _show_labo(self) -> List[str]:
        """Show laboratory menu.
        Corresponds to ERB @LABO.
        """
        lines: List[str] = []
        lines.append("----------")
        lines.append("[LABORATORY]")
        lines.append("[001] 文字色彩测试")
        lines.append("[004] GEO_MAKE")
        lines.append("[005] GEO_OUTPUT")
        lines.append("[006] GEO清除")
        lines.append("[007] 图片测试")
        lines.append("[008] 头像测试")
        lines.append("[100] 返回")
        return lines




    def _spend_all_labo_medals(self) -> bool:
        player = self._get_player()
        if player is None:
            return False
        if int(player.exp.get(81, 0)) <= 0:
            return False
        player.exp[81] = 0
        return True






    def show_lab(self):
        """Laboratory menu aligned to the original SHOP_LABO page structure."""
        ok, message = self._can_open_secret_labo()
        if not ok:
            print(f"\n{message}")
            self._pause()
            return

        pages = self._get_labo_pages()
        page_index = 0
        while True:
            exit_menu, page_index = self._advance_labo_menu(pages, page_index)
            if exit_menu:
                return

    def _labo_page1(self):
        return self.call_erb_function('LABO_PAGE1')

    def _labo_page2(self):
        return self.call_erb_function('LABO_PAGE2')

    def _labo_page3(self):
        return self.call_erb_function('LABO_PAGE3')

    def _labo_page4(self):
        return self.call_erb_function('LABO_PAGE4')

    def _labo_dr_change_hair_color(self):
        return self.call_erb_function('LABO_DR_CHANGE_HAIR_COLOR')

    def _labo_dr_get_talent(self):
        return self.call_erb_function('LABO_DR_GET_TALENT')

    def _labo_map_set(self):
        return self.call_erb_function('LABO_MAP_SET')





