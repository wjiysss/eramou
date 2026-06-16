from __future__ import annotations
"""Module for ConditionMixin - 条件判断"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class ConditionMixin:
    """Mixin providing 条件判断 methods for GameEngine"""

    def _can_apply_dress_option(self, target: Character, option: Dict[str, Any]) -> Optional[str]:
        if self.interpreter.vars.money < int(option["cost"]):
            return "钱不够"
        if target.abl.get(10, 0) < int(option["req"]):
            return "拒绝穿戴"
        if option["slot"] == "accessory" and target.cflag.get(49, 0) and int(option["cloth_id"]) != 79:
            return "不解开贞操带的话，无法穿戴其他装备"
        if int(option["cloth_id"]) == 79 and target.talent.get(122, 0):
            return "男性角色无法穿戴贞操带"
        return None

    def _can_apply_marriage_daily(self, idx: int, char: Character) -> bool:
        if idx <= 0:
            return False
        if int(char.cflag.get(1, 0)) != 0:
            return False
        return int(char.cflag.get(601, 0)) > 0

    def _can_apply_pregnancy_flow(self, target: Optional[Character], target_index: int) -> bool:
        if target is None:
            return False
        return self._can_open_trainable_target(target_index, target) is None

    def _can_apply_turn_end_anomaly_events(self) -> bool:
        return int(self.interpreter.vars.globals.get(2801, 0)) % 100 < 10

    def _can_capture_challenge_target(self, area: Optional[Dict[str, Any]] = None) -> bool:
        return self._can_capture_invasion_enemy(area)

    def _can_change_character_job(self, idx: int, target: Optional[Character]) -> Optional[str]:
        if target is None or idx < 0 or idx >= len(self.interpreter.vars.chars):
            return "无效对象"
        if idx == 0:
            return "你的职业无法改变"
        state = int(target.cflag.get(1, 0))
        if state == 2:
            return "侵攻中的勇者不能转职。"
        if int(target.cflag.get(9, 0)) < 50:
            return "必须积累更多经验！"
        if state not in (0, 7):
            return "该角色处于不可转职的状态"
        return None

    def _can_daily_dematurity_regress(self, target: Character) -> bool:
        return (
            ((target.talent.get(132, 0) or target.talent.get(134, 0))
             and int(target.abl.get(11, 0)) >= 5
             and int(target.abl.get(10, 0)) >= 5
             and int(target.abl.get(21, 0)) >= 5
             and int(target.exp.get(50, 0)) >= 5)
            or (
                int(target.abl.get(11, 0)) >= 5
                and int(target.abl.get(10, 0)) >= 5
                and int(target.abl.get(21, 0)) >= 5
                and int(target.abl.get(17, 0)) >= 5
                and int(target.exp.get(50, 0)) >= 7
                and target.talent.get(57, 0)
            )
        )

    def _can_discard_chastity_key(self, target: Character) -> bool:
        return (
            target.cflag.get(42, 0) == 79
            and bool(target.cflag.get(40, 0) & 64)
            and target.cflag.get(49, 0) == 0
            and bool(target.talent.get(0, 0))
            and target.cflag.get(71, 0) == 0
        )

    def _can_edit_character_name(self, idx: int, target: Optional[Character]) -> Optional[str]:
        if target is None or idx < 0 or idx >= len(self.interpreter.vars.chars):
            return "无效对象"
        if idx == 0:
            return "魔王的名字无法在这里更改。"
        state = int(target.cflag.get(1, 0))
        if state == 2:
            return "侵攻中的勇者不能改名。"
        if state == 7:
            return "苗床不可改变名字"
        if state not in (0, 3):
            return "角色处于不能变更名字的状态"
        return None

    def _can_execute_action(self, target: Character, action_id: int) -> Optional[str]:
        if self._is_maou_shadow(target):
            return f"{target.name} 只是魔王之影，一旦离开便会消散，无法对其执行该操作。"
        if action_id in (0, 1, 2, 3, 4) and target.cflag.get(700, 0):
            return f"{target.name} 在收藏列表之中，不能被处刑。"
        if action_id == 5 and target.talent.get(254, 0):
            return f"{target.name} 拥有【不受洗脑】，无法进行士兵化洗脑。"
        return None

    def _can_gain_additional_special_sex_talent(self, target: Character, sexskill_count: int) -> bool:
        masturbation_exp_req = 100 + 50 * sexskill_count
        orgasm_exp_req = 100 + 10 * sexskill_count
        penetration_exp_req = 300 + 50 * sexskill_count
        return (
            (int(target.talent.get(74, 0)) == 0 and int(target.abl.get(0, 0)) >= 5 and int(target.exp.get(11, 0)) >= masturbation_exp_req and int(target.exp.get(2, 0)) >= orgasm_exp_req)
            or (int(target.talent.get(75, 0)) == 0 and int(target.talent.get(122, 0)) != 0 and int(target.abl.get(0, 0)) >= 5 and int(target.exp.get(5, 0)) >= penetration_exp_req and int(target.exp.get(2, 0)) >= masturbation_exp_req)
            or (int(target.talent.get(75, 0)) == 0 and int(target.abl.get(2, 0)) >= 5 and int(target.exp.get(0, 0)) >= penetration_exp_req and int(target.exp.get(2, 0)) >= orgasm_exp_req)
            or (int(target.talent.get(77, 0)) == 0 and int(target.abl.get(3, 0)) >= 5 and int(target.exp.get(32, 0)) >= penetration_exp_req and int(target.exp.get(2, 0)) >= orgasm_exp_req)
            or (int(target.talent.get(78, 0)) == 0 and int(target.talent.get(122, 0)) != 0 and int(target.abl.get(1, 0)) >= 5 and int(target.juel.get(14, 0)) >= masturbation_exp_req and int(target.exp.get(2, 0)) >= orgasm_exp_req)
            or (int(target.talent.get(78, 0)) == 0 and int(target.abl.get(1, 0)) >= 5 and int(target.exp.get(54, 0)) >= masturbation_exp_req and int(target.exp.get(2, 0)) >= orgasm_exp_req)
        )

    def _can_gain_turn_end_corruption_talent(self, target: Character) -> bool:
        sensory_total = sum(int(target.abl.get(idx, 0)) for idx in range(4))
        return (
            int(target.cflag.get(2, 0)) >= 1000
            and int(target.abl.get(11, 0)) >= 3
            and sensory_total >= 10
            and int(target.exp.get(50, 0)) >= 3
            and int(target.talent.get(85, 0)) == 0
            and int(target.talent.get(76, 0)) == 0
            and int(target.mark.get(1, 0)) == 3
            and int(target.mark.get(2, 0)) == 3
        )

    def _can_gain_turn_end_love_talent(self, target: Character) -> bool:
        return (
            int(target.cflag.get(2, 0)) >= 1000
            and int(target.abl.get(10, 0)) >= 3
            and int(target.exp.get(21, 0)) >= 200
            and int(target.talent.get(76, 0)) == 0
            and int(target.talent.get(85, 0)) == 0
            and int(target.talent.get(184, 0)) == 0
            and int(target.mark.get(2, 0)) == 3
            and int(target.abl.get(16, 0)) >= 3
        )

    def _can_join_bedroom_daily_service(self, idx: int, char: Character) -> bool:
        if idx <= 0:
            return False
        if char.base.get(0, 0) <= 500:
            return False
        due_day = int(char.cflag.get(110, 0))
        current_day = self._get_total_day_count()
        if char.talent.get(154, 0) or (due_day - 2 <= current_day and char.talent.get(153, 0)):
            return False
        if char.cflag.get(1, 0) != 0:
            return False
        marriage_state = int(char.cflag.get(601, 0))
        if marriage_state not in (0, 901):
            return False
        if char.talent.get(151, 0):
            return False
        if char.mark.get(3, 0) > 0:
            return False
        return True

    def _can_night_stalking_use_v(self, char: Character) -> bool:
        if char.talent.get(122, 0):
            return False
        if char.talent.get(0, 0) or char.talent.get(273, 0):
            return False
        if int(char.cflag.get(42, 0)) == 79 and bool(char.cflag.get(40, 0) & 64):
            return False
        return char.abl.get(2, 0) >= char.abl.get(3, 0)

    def _can_open_ability_up_for_target(self, idx: int, target: Optional[Character]) -> Optional[str]:
        blocked_reason = self._can_open_trainable_target(idx, target)
        if blocked_reason is not None:
            return "No captive is currently selected." if blocked_reason == "无效对象" else blocked_reason
        return None

    def _can_open_ability_up_hero_target(self, idx: int, target: Optional[Character]) -> Optional[str]:
        if idx <= 0 or target is None:
            return "无效对象"
        if target.base.get(0, 0) < 1:
            return "濒死中，无法选择"
        if target.cflag.get(1, 0) != 2:
            return "不能选择非侵攻状态的勇者"
        return None

    def _can_open_ability_up_slave_target(self, idx: int, target: Optional[Character]) -> Optional[str]:
        return self._can_open_trainable_target(idx, target)

    def _can_open_character_standby_service(self, idx: int, target: Optional[Character]) -> Optional[str]:
        return self._can_open_trainable_target(idx, target)

    def _can_open_monster_shop(self) -> tuple[bool, str]:
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            return False, "奴隶太多了！"
        return True, ""

    def _can_open_secret_labo(self) -> tuple[bool, str]:
        player = self._get_player()
        if player is None or not player.talent.get(325, 0):
            return False, "尚未掌握进入秘密实验室所需的魔界知识。"
        return True, ""

    def _can_open_trainable_target(self, idx: int, target: Optional[Character]) -> Optional[str]:
        if idx <= 0 or target is None:
            return "无效对象"
        if target.base.get(0, 0) < 1:
            return "濒死中，无法选择"
        if target.cflag.get(1, 0) != 0:
            return "不能选择非待命状态的奴隶"
        return None

    def _can_prepare_monster_follower_sacrifice_plan(self, family_values: List[int], required_level: int) -> bool:
        auto_plan = self._build_monster_sacrifice_plan(family_values, required_level)
        return auto_plan is not None

    def _can_purchase_catalog_item(self, item_id: int, player: Character) -> Optional[str]:
        if item_id == 38 and player.talent.get(91, 0):
            return "已经掌握了【爱慕体系】相关知识。"
        if item_id == 39 and player.talent.get(325, 0):
            return "已经掌握了【魔界知识】。"
        if item_id == 42 and player.talent.get(55, 0):
            return "已经掌握了【调合知识】。"
        if item_id == 52 and (player.abl.get(12, 0) >= 10 or player.abl.get(12, 0) > self.interpreter.vars.get_flag(30, 0) + 1):
            return "技巧等级暂时无法继续提升。"
        if item_id == 54 and player.talent.get(327, 0):
            return "已经掌握了【淫魔知识】。"
        if item_id == 56 and player.talent.get(328, 0):
            return "已经掌握了【魔虫知识】。"
        return None

    def _can_purchase_knowledge_item(self, item_id: int, player: Character) -> Optional[str]:
        if item_id == 38 and player.talent.get(91, 0):
            return "已经掌握了【爱慕体系】相关知识。"
        if item_id == 39 and player.talent.get(325, 0):
            return "已经掌握了【魔界知识】。"
        if item_id == 42 and player.talent.get(55, 0):
            return "已经掌握了【调合知识】。"
        if item_id == 52 and (player.abl.get(12, 0) >= 10 or player.abl.get(12, 0) > self.interpreter.vars.get_flag(30, 0) + 1):
            return "技巧等级暂时无法继续提升。"
        if item_id == 54 and player.talent.get(327, 0):
            return "已经掌握了【淫魔知识】。"
        if item_id == 56 and player.talent.get(328, 0):
            return "已经掌握了【魔虫知识】。"
        return None

    def _can_reduce_resistance_mark(self, target: Character) -> bool:
        return not self._get_resistance_mark_reduction_reasons(target)

    def _can_replace_diaper(self, target: Character) -> bool:
        return target.cflag.get(42, 0) == 69 and ((target.cflag.get(40, 0) & 64) == 0 or target.cflag.get(47, 0) > 0)

    def _can_reset_character_self_call(self, idx: int, target: Optional[Character]) -> bool:
        return target is not None and idx >= 0 and idx < len(self.interpreter.vars.chars)

    def _can_select_item_target(self, idx: int, target: Optional[Character], allow_master: bool = True) -> Optional[str]:
        if target is None:
            return "无效对象"
        if idx == 0 and not allow_master:
            return "无效对象"
        if target.base.get(0, 0) < 1:
            return "濒死中，无法选择"
        if idx > 0 and target.cflag.get(1, 0) != 0:
            return "此人物尚不可选择"
        return None

    def _can_select_standby_slave(self, idx: int, target: Optional[Character]) -> Optional[str]:
        blocked_reason = self._can_open_trainable_target(idx, target)
        if blocked_reason is not None:
            return blocked_reason
        if target.cflag.get(0, 0) != 2:
            return "不能选择不可做助手的角色"
        if self.interpreter.vars.target == idx:
            return "调教对象不能同时担任助手"
        return None

    def _can_show_character_bitch_level(self, idx: int, target: Optional[Character]) -> bool:
        return idx > 0 and target is not None

    def _can_show_character_equipment(self, idx: int, target: Optional[Character]) -> bool:
        if idx <= 0 or target is None:
            return False
        self._update_sell_flags_for_target(target)
        return (
            int(target.cflag.get(0, 0)) > 0
            or int(target.cflag.get(2, 0)) >= 20
            or int(target.abl.get(10, 0)) > 0
            or bool(target.talent.get(28, 0))
            or int(target.cflag.get(151, 0)) <= 0
        )

    def _can_show_character_marriage_action(self, idx: int, char: Character) -> bool:
        if idx <= 0:
            return False
        state = int(char.cflag.get(1, 0))
        return state in (0, 2, 3, 7)

    def _can_show_character_temptation(self, idx: int, target: Optional[Character]) -> bool:
        return self._check_able_to_temptation(idx, target) == 0

    def _can_show_shop_item(self, item_id: int, player: Optional[Character]) -> bool:
        if item_id not in self.item_catalog:
            return False
        if player is None:
            return True
        difficulty = int(self.interpreter.vars.get_flag(5, 0))
        if item_id in {24, 25, 26, 27, 28, 34, 35} and self._get_item_count(player, item_id) >= 99:
            return False
        if item_id in {37, 38, 39, 42, 52, 54, 56} and self._get_item_count(player, item_id) > 0:
            return False
        if item_id == 38 and difficulty in (3, 4):
            return False
        return True

    def _can_spawn_crazylord_special_enemy(self) -> bool:
        if not self._can_spawn_daily_enemy():
            return False
        if self.interpreter.vars.get_flag(224, 0) == 1:
            return False
        if self._get_total_day_count() < 350:
            return False
        heart = self._get_character_by_template_id(20)
        if heart is None or self._get_character_by_template_id(34) is not None:
            return False
        if heart.cflag.get(1, 0) != 0:
            return False
        if self.interpreter.vars.get_flag(92, 0) != 15:
            return False
        return bool(heart.talent.get(85, 0) or heart.talent.get(76, 0))

    def _can_spawn_daily_enemy(self) -> bool:
        char_count = len(self.interpreter.vars.chars)
        if self.interpreter.vars.get_flag(82, 0) == 0 and char_count > 60:
            return False
        if self.interpreter.vars.get_flag(87, 0) == 0 and self.interpreter.vars.get_flag(89, 0) == 0 and self.interpreter.vars.get_flag(91, 0) == 0 and char_count > 65:
            return False
        if (
            self.interpreter.vars.get_flag(87, 0) * self.interpreter.vars.get_flag(89, 0) == 0
            and self.interpreter.vars.get_flag(89, 0) * self.interpreter.vars.get_flag(91, 0) == 0
            and self.interpreter.vars.get_flag(91, 0) * self.interpreter.vars.get_flag(87, 0) == 0
            and char_count > 70
        ):
            return False
        if (
            self.interpreter.vars.get_flag(87, 0) == 0
            or self.interpreter.vars.get_flag(89, 0) == 0
            or self.interpreter.vars.get_flag(91, 0) == 0
        ) and char_count > 75:
            return False
        if self.interpreter.vars.get_flag(92, 0) < 15 and char_count > 80:
            return False
        return char_count < self._get_max_charanum()

    def _can_spawn_lily_special_enemy(self) -> bool:
        if not self._can_spawn_daily_enemy():
            return False
        if self.interpreter.vars.get_flag(223, 0) == 1:
            return False
        if self._get_total_day_count() < 200:
            return False
        maou = self._get_character_by_template_id(17)
        if maou is None or self._get_character_by_template_id(24) is not None:
            return False
        if maou.cflag.get(1, 0) != 0:
            return False
        return bool(maou.talent.get(85, 0) or maou.talent.get(76, 0))

    def _can_start_training_from_shop(self) -> Optional[str]:
        player = self._get_player()
        if player is not None and player.cflag.get(1, 0) == 10:
            return "育儿室中的你不能进行调教……"
        return None

    def _can_swap_corruption_to_love(self, target: Character) -> bool:
        return (
            target.talent.get(76, 0) == 1
            and int(target.abl.get(10, 0)) >= 3
            and int(target.exp.get(21, 0)) >= 200
            and target.talent.get(85, 0) == 0
            and int(target.mark.get(2, 0)) == 3
            and int(target.abl.get(16, 0)) >= 3
        )

    def _can_swap_love_to_corruption(self, target: Character) -> bool:
        sensory_total = sum(int(target.abl.get(idx, 0)) for idx in range(4))
        return (
            target.talent.get(85, 0) == 1
            and int(target.abl.get(11, 0)) >= 3
            and sensory_total >= 10
            and int(target.exp.get(50, 0)) >= 3
            and int(target.mark.get(1, 0)) == 3
            and int(target.mark.get(2, 0)) == 3
        )

    def _can_trigger_night_stalking(self, idx: int, char: Character) -> bool:
        if not self._can_join_bedroom_daily_service(idx, char):
            return False
        if char.abl.get(11, 0) < 4 or char.abl.get(30, 0) < 1:
            return False
        obedience = int(char.abl.get(10, 0))
        lust = int(char.abl.get(11, 0))
        anal_sense = int(char.abl.get(3, 0))
        vaginal_sense = int(char.abl.get(2, 0))
        if char.talent.get(0, 0) and obedience + lust + anal_sense <= 14:
            return False
        if char.talent.get(122, 0):
            if obedience + lust + anal_sense <= 12:
                return False
        elif obedience + lust + vaginal_sense <= 12 and obedience + lust + anal_sense <= 14:
            return False
        if int(char.cflag.get(42, 0)) == 79 and bool(char.cflag.get(40, 0) & 64) and obedience + lust + anal_sense <= 14:
            return False
        return self._get_night_stalking_score(char) > 0

    def _can_trigger_onesho(self, char: Character) -> bool:
        if char.base.get(0, 0) <= 0:
            return False
        if char.talent.get(57, 0) != 1:
            return False
        threshold = max(0, char.exp.get(31, 0) // 10 + char.talent.get(132, 0) * 2)
        return random.randint(0, 11) <= threshold

    def _can_use_item_on_target(self, item_id: int, target: Character) -> Optional[str]:
        item_name = self._get_item_name(item_id)
        if item_id == 30 and target.base.get(0, 0) >= target.maxbase.get(0, 0):
            return f"{target.name}的体力已经达到了最大值"
        if item_id == 31 and target.palam.get(100, 0) < 1:
            return f"{target.name}的否定点数已经不能再减少了"
        if item_id == 33 and (target.base.get(10, 0) == 0 or target.talent.get(85, 0) == 0):
            return f"{target.name}已经不受寿命限制了"
        if item_id == 40 and target.talent.get(153, 0):
            return f"怀孕中的{target.name}不能使用{item_name}"
        if item_id == 40 and target.talent.get(154, 0):
            return f"育儿中的{target.name}不能使用{item_name}"
        return None

    def _can_use_life_cradle(self) -> tuple[bool, str]:
        char_count = len(self.interpreter.vars.chars)
        capacity = self._get_life_cradle_capacity_limit()
        if char_count > capacity:
            return False, "勇者数量过多。"
        if char_count >= 999:
            return False, "勇者数量过多。"
        return True, ""

    def _check_able_to_temptation(self, idx: int, target: Optional[Character]) -> int:
        if idx <= 0 or target is None:
            return 1
        if int(target.cflag.get(1, 0)) != 2:
            return 1
        if int(target.cflag.get(800, 0)) == 4:
            return 2
        return 0

    def _check_aphrodisiac_addict(self, target) -> List[str]:
        """媚药中毒检查 - 对应 @APHRODISIAC_ADDICT
        每7天减少体内残留度，检查中毒/疯狂/崩坏获取
        """
        messages = []
        v = self.interpreter.vars
        current_day = v.day[0] if hasattr(v, 'day') else 0

        # 每7天减少残留度
        if (current_day + 1) % 7 == 0:
            if target.cflag.get(31, 0) > 0:
                target.cflag[31] = target.cflag.get(31, 0) - 1
                if target.cflag[31] < 0:
                    target.cflag[31] = 0

            # 媚药中毒时检查禁断症状
            if target.talent.get(46, 0):
                if target.cflag.get(1, 0) != 9:
                    if target.cflag.get(32, 0):
                        target.cflag[32] = 0
                    else:
                        messages.extend(self._precipitate_withdrawal(target))

        # 媚药中毒消失判定
        if target.cflag.get(31, 0) == 0 and target.talent.get(46, 0):
            messages.append(f"{target.savestr}的样子变了……")
            messages.append(f"体内的媚药效果被根除，{target.savestr}的药瘾消失了。")
            messages.append(f"{target.savestr}的【媚药中毒】消除了。")
            target.talent[46] = 0

        # 媚药中毒获取判定
        threshold_normal = 12
        threshold_easy = 9
        if (not target.talent.get(86, 0) and target.cflag.get(31, 0) >= threshold_normal) or \
           (target.talent.get(72, 0) and target.cflag.get(31, 0) >= threshold_easy):
            if not target.talent.get(46, 0):
                messages.append(f"{target.savestr}的样子有点奇怪……")
                messages.append(f"媚药的过量使用，令{target.savestr}沾上药瘾了。")
                messages.append(f"{target.savestr}获得了【媚药中毒】。")
                target.talent[46] = 1
                if target.cflag.get(31, 0) < 15:
                    target.cflag[31] = 15

        # 疯狂获取判定
        crazy_threshold = 40 if not target.talent.get(72, 0) else 30
        if target.cflag.get(31, 0) >= crazy_threshold and not target.talent.get(123, 0):
            messages.append(f"{target.savestr}的样子有点奇怪……")
            messages.append(f"{target.savestr}随着媚药的过量使用，人也变得暴躁了。")
            messages.append(f"{target.savestr}获得了【疯狂】。")
            target.talent[123] = 1

        # 崩坏获取判定
        wreck_threshold = 100 if not target.talent.get(72, 0) else 75
        if target.cflag.get(31, 0) >= wreck_threshold and not target.talent.get(9, 0):
            messages.append(f"{target.savestr}的样子有点奇怪……")
            messages.append(f"{target.savestr}随着媚药的过量使用，完全变成了废人。")
            messages.append(f"{target.savestr}的精神【崩坏】了……")
            target.talent[9] = 1

        return messages

    def _check_assistable(self) -> List[str]:
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        for idx in range(1, len(chars)):
            result = self._is_assistable_check(idx)
            char = chars[idx]
            name = getattr(char, 'savestr', char.name or "???")
            if result == 0:
                lines.append(f"[{idx:2d}] {name} - 可助手")
            else:
                lines.append(f"[{idx:2d}] {name} - 不可助手(原因:{result})")
        return lines

    def _check_fullmoon(self) -> List[str]:
        """Check and process full moon events.
        During full moon nights, certain races get stat boosts.
        """
        messages: List[str] = []
        for target in self.interpreter.vars.chars:
            # Skip if no valid character
            if target is None:
                continue
            # Check if character is a primary race (talent:220 == 0) or secondary race
            is_secondary = int(target.talent.get(220, 0)) != 0
            race = int(target.talent.get(0, 0))  # 种族

            if not is_secondary:
                # LABEL_种族: primary race
                if race == 0:
                    # 人类 - no effect
                    pass
                elif race == 1:
                    # 精灵 - no effect
                    pass
                elif race == 2:
                    # 狼人
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 10
                    target.cflag[12] = int(target.cflag.get(12, 0)) * 10
                    target.base[0] = int(target.maxbase.get(0, 0))
                    target.base[1] = int(target.maxbase.get(1, 0))
                    messages.append(f"满月之夜，{target.name}的野性觉醒了！")
                elif race == 3:
                    # 吸血鬼
                    target.cflag[11] = max(int(target.cflag.get(11, 0)), int(target.cflag.get(13, 0)))
                    target.cflag[12] = max(int(target.cflag.get(12, 0)), int(target.cflag.get(14, 0)))
                    target.base[0] = int(target.maxbase.get(0, 0)) * 10
                    target.base[1] = int(target.maxbase.get(1, 0)) * 10
                    messages.append(f"满月之夜，{target.name}的吸血鬼之力增强了！")
                elif race == 4:
                    # 无头骑士 - no effect
                    pass
                elif race == 5:
                    # 龙族 - no effect
                    pass
                elif race == 6:
                    # 天使
                    target.base[1] = int(target.base.get(1, 0)) // 2
                    messages.append(f"满月之夜，{target.name}的魔力被削弱了。")
                elif race == 7:
                    # 暗精灵
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    target.base[0] = int(target.maxbase.get(0, 0))
                    target.base[1] = int(target.maxbase.get(1, 0))
                    messages.append(f"满月之夜，{target.name}的暗之力增强了！")
                elif race == 8:
                    # 堕天使
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    messages.append(f"满月之夜，{target.name}的堕天使之力增强了！")
                elif race == 9:
                    # 魔族
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    messages.append(f"满月之夜，{target.name}的魔力增强了！")
                elif race == 10:
                    # 霍比特人 - no effect
                    pass
                elif race == 11:
                    # 矮人 - no effect
                    pass
            else:
                # LABEL_种族2: secondary race
                if race == 4:
                    # 植物
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    target.base[0] = int(target.maxbase.get(0, 0))
                    target.base[1] = int(target.maxbase.get(1, 0))
                    messages.append(f"满月之夜，{target.name}的植物之力增强了！")
                elif race in (5, 11):
                    # 触手
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 5
                    target.base[0] = int(target.maxbase.get(0, 0))
                    target.base[1] = int(target.maxbase.get(1, 0))
                    messages.append(f"满月之夜，{target.name}的触手之力大幅增强了！")
                elif race == 6:
                    # 妖精
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    target.base[0] = int(target.maxbase.get(0, 0)) * 2
                    target.base[1] = int(target.maxbase.get(1, 0)) * 2
                    messages.append(f"满月之夜，{target.name}的妖精之力增强了！")
                else:
                    # CASEELSE
                    target.cflag[11] = int(target.cflag.get(11, 0)) * 2
                    target.base[1] = int(target.maxbase.get(1, 0))
                    messages.append(f"满月之夜，{target.name}的力量增强了！")

        return messages

    def _check_otherworld_hero_template_finalize_costs(self, finalize: bool) -> Optional[tuple[bool, str]]:
        if not finalize:
            return None
        if self.interpreter.vars.money <= 1500:
            return False, "金钱不够！"
        if self._get_medal_count() < 1:
            return False, "勋章不够！"
        if not self._consume_medals(1):
            return False, "勋章不够！"
        return None

    def _check_sabbath(self, target) -> List[str]:
        """安息日检查 - 对应 @SABBATH
        满月时淫乱角色参与性仪式
        """
        import random
        messages = []
        v = self.interpreter.vars

        # 非调教状态排除
        if target.cflag.get(1, 0) != 0:
            return messages

        # 非满月排除
        moon_phase = v.day[2] if hasattr(v, 'day') and len(v.day) > 2 else 0
        if moon_phase <= 14 or moon_phase >= 16:
            return messages

        # 需要法术或咒术
        if not target.talent.get(242, 0) and not target.talent.get(250, 0):
            return messages

        # 需要淫乱
        if not target.talent.get(76, 0):
            return messages

        COUNT_F = 0
        COUNT_A = 0
        COUNT_B = 0
        COUNT_V = 0
        COUNT_S = 0
        COUNT_Z = 0

        messages.append(f"{target.savestr}参与了献给无名的淫荡女神的仪式，")

        if target.talent.get(122, 0):
            # 男性
            messages.append("全裸的魔族女性和女奴隶在陪侍着，")
        elif target.talent.get(121, 0):
            # 扶她
            messages.append("暴露乳房的装束让阴茎勃起了，")
        else:
            messages.append("穿着乳房、性器、屁股全部暴露的邪恶服装，")

        messages.append("对地下城里的怪物们，进行了性施舍。")

        # 按状态分派
        if target.talent.get(122, 0):
            # 男性
            messages.append(f"{target.savestr}抱着魔族女人，将精液施舍给了她。")
        elif target.talent.get(121, 0):
            # 扶她
            messages.append(f"{target.savestr}抱着魔族女人，将精液施舍给了她。")
            if target.talent.get(0, 0) or target.talent.get(273, 0):
                messages.append(f"{target.savestr}因为性器被封印着，所以使用肛门不停地侍奉着阴茎。")
                if target.talent.get(77, 0):
                    messages.append(f"{target.savestr}陶醉在从后穴传递向前穴的快感中。")
                    COUNT_A += 1
                COUNT_A += random.randint(1, 10)
                COUNT_S += COUNT_A + random.randint(1, 10)
            else:
                messages.append("将自己能用上的穴，全部拿来侍奉阴茎。")
                COUNT_V += random.randint(1, 10)
                COUNT_A += random.randint(1, 10)
                COUNT_S += COUNT_A + COUNT_V + random.randint(1, 10)
        elif target.talent.get(0, 0):
            # 处女
            messages.append(f"{target.savestr}纯洁的性器上被贴上了封条。所以使用肛门不停地侍奉着阴茎。")
            if target.talent.get(77, 0):
                messages.append(f"{target.savestr}因肛门的快感而愉悦着。")
                COUNT_A += 1
            COUNT_A += random.randint(1, 10)
            COUNT_S += COUNT_A + random.randint(1, 10)
        elif target.talent.get(273, 0):
            # 私处封印
            messages.append(f"{target.savestr}因为性器被封印着，所以使用肛门不停地侍奉着阴茎。")
            if target.talent.get(77, 0):
                messages.append(f"{target.savestr}陶醉在从后穴传递向前穴的快感中。")
                COUNT_A += 1
            COUNT_A += random.randint(1, 10)
            COUNT_S += COUNT_A + random.randint(1, 10)
        elif target.abl.get(39, 0) >= 1 and random.randint(0, 1) == 0:
            # 兽奸中毒
            if target.abl.get(17, 0) >= 1:
                messages.append(f"{target.savestr}有着喜欢与野兽交配的传闻，聚集了很多从地下城里慕名而来的人。")
                COUNT_V += target.abl.get(17, 0)
                COUNT_A += target.abl.get(17, 0)
            messages.append(f"{target.savestr}满心欢喜地用性器迎接了猪的阴茎。")
            messages.append("为路人呈现了一场献给邪神的兽奸秀。")
            if target.talent.get(75, 0):
                COUNT_V += 1
            if target.talent.get(77, 0):
                COUNT_A += 1
            COUNT_V += random.randint(1, 10) + target.abl.get(39, 0)
            COUNT_A += random.randint(1, 10) + target.abl.get(39, 0)
            COUNT_S += COUNT_A + COUNT_V + random.randint(1, 10)
            COUNT_Z += COUNT_S
        else:
            # 普通
            if target.abl.get(17, 0) >= 1:
                messages.append(f"{target.savestr}在观众的欢呼声中，开始了乱交派对。")
                COUNT_V += target.abl.get(17, 0)
                COUNT_A += target.abl.get(17, 0)
            if target.abl.get(16, 0) >= 1:
                messages.append(f"无论是多么丑陋的怪物和魔族，{target.savestr}都一视同仁地给予了性施舍。")
                COUNT_V += target.abl.get(16, 0)
                COUNT_A += target.abl.get(16, 0)
            messages.append("有空的怪物们不停地排着队，将她所有能用的穴都侵犯了一遍。")
            messages.append("浑身里里外外都沾满了精液，整个广场被异样的臭味笼罩着。")
            if target.talent.get(75, 0):
                COUNT_V += 1
            if target.talent.get(77, 0):
                COUNT_A += 1
            COUNT_V += random.randint(1, 10) + 1
            COUNT_A += random.randint(1, 10) + 1
            COUNT_S += COUNT_A + COUNT_V + random.randint(1, 10)

        # 经验加算
        if COUNT_A > 0:
            target.exp[1] = target.exp.get(1, 0) + COUNT_A
            messages.append(f"肛门经验+{COUNT_A}")
        if COUNT_V > 0:
            target.exp[0] = target.exp.get(0, 0) + COUNT_V
            messages.append(f"私处经验+{COUNT_V}")
        sex_count = COUNT_A + COUNT_V
        if sex_count > 0:
            target.exp[5] = target.exp.get(5, 0) + sex_count
            messages.append(f"性交经验+{sex_count}")
        if COUNT_S > 0:
            target.exp[20] = target.exp.get(20, 0) + COUNT_S
            messages.append(f"精液经验+{COUNT_S}")
        if COUNT_Z > 0:
            target.exp[56] = target.exp.get(56, 0) + COUNT_Z
            messages.append(f"兽奸经验+{COUNT_Z}")

        # 珠加算
        if COUNT_A > 0:
            target.juel[2] = target.juel.get(2, 0) + COUNT_A
            messages.append(f"快A点数+{COUNT_A}")
        if COUNT_V > 0:
            target.juel[1] = target.juel.get(1, 0) + COUNT_V
            messages.append(f"快V点数+{COUNT_V}")
        lust_shame = (COUNT_A + COUNT_V + COUNT_S + COUNT_Z) * 10
        if lust_shame > 0:
            target.juel[5] = target.juel.get(5, 0) + lust_shame
            target.juel[8] = target.juel.get(8, 0) + lust_shame
            messages.append(f"欲情点数+{lust_shame}")
            messages.append(f"耻情点数+{lust_shame}")

        # 童贞丧失
        if target.talent.get(1, 0):
            messages.append("【童贞丧失】")
            target.talent[1] = 0

        return messages

    def _check_sabbath_day(self, target) -> List[str]:
        """安息日（每日版）- 对应 @SABBATH_DAY
        每3天一次的信徒仪式
        """
        import random
        messages = []
        v = self.interpreter.vars

        # 每3天一次
        local = v.day[2] if hasattr(v, 'day') and len(v.day) > 2 else 0
        if local % 3 != 0:
            return messages

        # 需要法术或咒术
        if not target.talent.get(242, 0) and not target.talent.get(250, 0):
            return messages

        # 需要已沦陷
        if target.cflag.get(0, 0) == 0:
            return messages

        # 信仰值40以上
        if target.cflag.get(152, 0) < 40:
            return messages

        sabbath_user = random.randint(0, 3)
        messages.append(f"{target.savestr}参与了献给无名的淫荡女神的仪式，")

        if sabbath_user == 0 and v.items.get(22, 0):
            # 兽奸仪式
            options = [
                "祭坛前，信徒的少女和山羊交配了起来……",
                "为了收集狗的精液的女信徒用嘴巴不停收集着……",
                "祭坛前，信徒的人妻和狗交配着……",
            ]
            messages.append(random.choice(options))
        elif sabbath_user == 1 and target.cflag.get(152, 0) > 80:
            # 乱交仪式
            options = [
                "祭坛前，信众们开始做起了爱……",
                "新婚的信众夫妇们玩起了交换Play……",
                "祭坛前年轻的信众们乱交了起来……",
            ]
            messages.append(random.choice(options))
        elif sabbath_user == 2 and target.cflag.get(152, 0) > 60:
            # 亵渎仪式
            if target.talent.get(250, 0) and (target.talent.get(17, 0) or target.talent.get(282, 0)):
                options = [
                    "向潜藏地底的死亡女神献上了她被侵犯着的淫荡画像……",
                    "向潜藏地底的死亡女神的圣器里自慰发泄着……",
                ]
                messages.append(random.choice(options))
            elif target.talent.get(242, 0) and (target.talent.get(17, 0) or target.talent.get(282, 0)):
                options = [
                    "向纯洁的神圣女神唱起了她被人侵犯着的歌词……",
                    "向纯洁的神圣女神展示着她的信徒在野外被玷污的画面……",
                ]
                messages.append(random.choice(options))
            else:
                options = [
                    "祭坛前，信徒的女孩自慰了起来……",
                    "献上了淫荡的雕像，信徒的少年在那上面喷上了精液……",
                    "献上了信徒的女精灵和兽人做爱的模样……",
                ]
                messages.append(random.choice(options))
        else:
            options = [
                "祭坛前，信徒的女孩自慰了起来……",
                "献上了淫荡的雕像，信徒的少年在那上面喷上了精液……",
                "献上了信徒的女精灵和兽人做爱的模样……",
            ]
            messages.append(random.choice(options))

        return messages

    def _check_trainable(self) -> List[str]:
        lines: List[str] = []
        v = self.interpreter.vars
        chars = v.chars if hasattr(v, 'chars') else []
        for idx in range(1, len(chars)):
            result = self._is_trainable_check(idx)
            char = chars[idx]
            name = getattr(char, 'savestr', char.name or "???")
            if result == 0:
                lines.append(f"[{idx:2d}] {name} - 可调教")
            else:
                lines.append(f"[{idx:2d}] {name} - 不可调教(原因:{result})")
        return lines
