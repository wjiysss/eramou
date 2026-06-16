from __future__ import annotations
"""Module for AbilityExtMixin - 能力提升"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class AbilityExtMixin:
    """Mixin providing 能力提升 methods for GameEngine"""

    def _advance_ability_up_menu(self, target: Character, ability_ids: List[int]) -> bool:
        options = self._render_ability_up_panel(target, ability_ids)
        choice = self._prompt_ability_up_choice()
        return self._handle_ability_up_menu_choice(target, options, choice)






    def _advance_ability_up_target_from_roster(self, player_level: int, menu_code: str) -> bool:
        labels = self._get_ability_up_roster_mode_labels()
        candidates = self._list_ability_up_candidates(menu_code)
        self._render_ability_up_roster_screen(labels, menu_code, candidates)
        choice = self._prompt_ability_up_roster_choice()
        if choice == "100":
            return True
        if choice in ("997", "998"):
            if choice == "997" and player_level < 20:
                print("\n这个指令需要更高等级")
                self._pause()
                return False
            menu_code = choice
            return False
        return self._handle_ability_up_roster_selection(menu_code, candidates, choice)






    def _apply_ability_upgrade(self, target: Character, ability_id: int) -> tuple[bool, str]:
        option = self._build_ability_upgrade_option(target, ability_id)
        if not option["available"]:
            return False, "；".join(option["reasons"]) if option["reasons"] else "条件不足"

        selected_costs = dict(option["costs"])
        if option.get("paths"):
            selected_ok, selected_path = self._choose_ability_upgrade_path(option)
            if not selected_ok:
                return False, "已取消。"
            if selected_path is None:
                return False, "无效选择。"
            selected_costs = dict(selected_path["costs"])

        for resource_id, amount in selected_costs.items():
            resource_type = option["cost_types"].get(resource_id, "juel")
            if resource_type == "exp":
                target.exp[resource_id] = target.exp.get(resource_id, 0) - amount
            else:
                self._consume_juel(resource_id, amount)

        target.abl[ability_id] = target.abl.get(ability_id, 0) + 1
        if ability_id in (10, 11):
            self._update_sell_flags_for_target(target)
        return True, f"{option['name']} 变为 LV{target.abl[ability_id]}"






    def _build_ability_upgrade_abnormal_exp_10(self, target: Character) -> int:
        blocked_talents = [10, 13, 73, 76, 85, 86]
        if target.abl.get(10, 0) == 4 and not any(target.talent.get(idx, 0) for idx in blocked_talents):
            return 1
        if target.abl.get(10, 0) == 7 and not any(target.talent.get(idx, 0) for idx in blocked_talents):
            return 2
        return 0






    def _build_ability_upgrade_abnormal_exp_11(self, target: Character) -> int:
        blocked_talents = [33, 70, 73, 76, 123]
        if target.abl.get(11, 0) == 4 and not any(target.talent.get(idx, 0) for idx in blocked_talents):
            return 1
        if target.abl.get(11, 0) == 7 and not any(target.talent.get(idx, 0) for idx in blocked_talents):
            return 3
        return 0






    def _build_ability_upgrade_abnormal_exp_17(self, target: Character) -> int:
        blocked_talents = [28, 33, 76, 80, 88, 123]
        if target.abl.get(17, 0) >= 3 and not any(target.talent.get(idx, 0) for idx in blocked_talents):
            return max(0, target.abl.get(17, 0) - 2)
        return 0






    def _build_ability_upgrade_abnormal_exp_20(self, target: Character) -> int:
        if target.abl.get(20, 0) in (3, 4, 7) and not any(target.talent.get(idx, 0) for idx in [80, 83, 84, 87]):
            return target.abl.get(20, 0) - 2
        return 0






    def _build_ability_upgrade_abnormal_exp_23(self, target: Character) -> int:
        if target.abl.get(23, 0) >= 3 and not any(target.talent.get(idx, 0) for idx in [33, 80, 81, 123]):
            return target.abl.get(23, 0) - 2
        return 0






    def _build_ability_upgrade_abnormal_exp_31(self, target: Character) -> int:
        return self._build_ability_upgrade_abnormal_exp_by_talent_block(target, 31, [33, 60, 72, 76], offset=1)






    def _build_ability_upgrade_abnormal_exp_32(self, target: Character) -> int:
        return self._build_ability_upgrade_abnormal_exp_by_talent_block(target, 32, [47, 61, 72, 80, 123], offset=1)






    def _build_ability_upgrade_abnormal_exp_33(self, target: Character) -> int:
        return self._build_ability_upgrade_abnormal_exp_by_talent_block(target, 33, [72, 80, 81, 82, 123], offset=1)






    def _build_ability_upgrade_abnormal_exp_37(self, target: Character) -> int:
        if target.abl.get(37, 0) < 2 or target.talent.get(123, 0) or target.talent.get(9, 0):
            return 0
        penalty = self._build_ability_upgrade_abnormal_exp_37_base(target)
        return max(0, penalty)






    def _build_ability_upgrade_abnormal_exp_37_base(self, target: Character) -> int:
        penalty = target.abl.get(37, 0) - 1
        penalty -= 1 if target.talent.get(33, 0) else 0
        penalty -= 1 if target.talent.get(70, 0) else 0
        penalty -= 2 if target.talent.get(72, 0) else 0
        penalty -= 1 if target.talent.get(73, 0) else 0
        penalty -= 1 if target.talent.get(76, 0) else 0
        penalty -= 1 if target.talent.get(80, 0) else 0
        penalty -= 1 if target.talent.get(180, 0) else 0
        penalty -= 2 if target.talent.get(181, 0) else 0
        penalty += 1 if target.talent.get(11, 0) else 0
        penalty += 1 if target.talent.get(20, 0) else 0
        penalty += 1 if target.talent.get(32, 0) else 0
        penalty += 1 if target.talent.get(34, 0) else 0
        penalty += 1 if target.talent.get(71, 0) else 0
        penalty += 1 if target.talent.get(85, 0) else 0
        penalty += 2 if target.talent.get(184, 0) else 0
        return penalty






    def _build_ability_upgrade_abnormal_exp_39(self, target: Character) -> int:
        return self._build_ability_upgrade_abnormal_exp_by_talent_block(target, 39, [72, 76, 136], offset=-1)






    def _build_ability_upgrade_abnormal_exp_40(self, target: Character) -> int:
        return self._build_ability_upgrade_abnormal_exp_by_talent_block(target, 40, [72, 76], offset=-1)






    def _build_ability_upgrade_abnormal_exp_by_talent_block(self, target: Character, ability_id: int, blocked_talents: List[int], offset: int) -> int:
        level = target.abl.get(ability_id, 0)
        if level < 2 or any(target.talent.get(idx, 0) for idx in blocked_talents):
            return 0
        if offset >= 0:
            return max(0, level - offset)
        return max(0, level + abs(offset))






    def _build_ability_upgrade_cost_table(self, *rows: tuple[int, Dict[int, int]]) -> Dict[int, Dict[int, int]]:
        return {level: costs for level, costs in rows}






    def _build_ability_upgrade_option(self, target: Character, ability_id: int) -> Dict[str, Any]:
        rules = self._get_ability_upgrade_rules().get(ability_id)
        level = target.abl.get(ability_id, 0)
        option = self._create_ability_upgrade_option(ability_id, level)
        if rules is None:
            option["reasons"].append("未接入原作规则")
            return option

        soft_cap = rules["soft_cap"](target)
        max_level = rules["max_level"]
        prereq_result = self._check_ability_upgrade_limits(level, soft_cap, max_level)
        if prereq_result is not None:
            option["reasons"].append(prereq_result)
            return option

        self._populate_ability_upgrade_costs(option, rules, target, level)

        prereq = rules.get("prereq")
        prereq_message = prereq(self, target) if prereq is not None else None
        if prereq_message:
            option["reasons"].append(prereq_message)

        self._validate_ability_upgrade_option(option, target, rules)

        option["available"] = not option["reasons"]
        return option






    def _build_ability_upgrade_prereq_12_15_cap(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(12, 0) + target.abl.get(15, 0) < 15 else "技巧+话术上限为15"






    def _build_ability_upgrade_prereq_13(self, eng: Any, target: Character) -> Optional[str]:
        if (target.abl.get(13, 0) < 5 and target.abl.get(12, 0) >= target.abl.get(13, 0) + 1) or (target.abl.get(13, 0) >= 5 and target.abl.get(16, 0) >= target.abl.get(13, 0) + 1):
            return None
        return "前置能力不足"






    def _build_ability_upgrade_prereq_14(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(12, 0) >= min(5, target.abl.get(14, 0) + 1) else "技巧不足"






    def _build_ability_upgrade_prereq_16(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(10, 0) >= target.abl.get(16, 0) + 1 else "顺从不足"






    def _build_ability_upgrade_prereq_17(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(11, 0) >= target.abl.get(17, 0) + 1 or target.abl.get(10, 0) >= target.abl.get(17, 0) + 1 else "顺从/欲望不足"






    def _build_ability_upgrade_prereq_20(self, eng: Any, target: Character) -> Optional[str]:
        if target.abl.get(20, 0) + target.abl.get(21, 0) < 20 and target.abl.get(11, 0) >= target.abl.get(20, 0) + 1:
            return None
        if target.abl.get(20, 0) + target.abl.get(21, 0) >= 20:
            return "抖S+抖M上限为20"
        return "欲望不足"






    def _build_ability_upgrade_prereq_21(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(11, 0) >= target.abl.get(21, 0) + 1 else "欲望不足"






    def _build_ability_upgrade_prereq_22(self, eng: Any, target: Character) -> Optional[str]:
        if target.talent.get(122, 0):
            return "男人不能提升百合气质"
        return None if target.abl.get(11, 0) >= target.abl.get(22, 0) + 1 else "欲望不足"






    def _build_ability_upgrade_prereq_23(self, eng: Any, target: Character) -> Optional[str]:
        if not target.talent.get(122, 0):
            return "只有男性可提升断背气质"
        return None






    def _build_ability_upgrade_prereq_30(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(14, 0) >= target.abl.get(30, 0) + 1 else "性交技术不足"






    def _build_ability_upgrade_prereq_31(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(17, 0) >= target.abl.get(31, 0) + 1 and target.abl.get(0, 0) >= target.abl.get(31, 0) + 1 else "露出癖/阴蒂感觉不足"






    def _build_ability_upgrade_prereq_32(self, eng: Any, target: Character) -> Optional[str]:
        if (target.talent.get(76, 0) == 0 and target.abl.get(16, 0) >= target.abl.get(32, 0) + 1) or (target.talent.get(76, 0) == 1 and target.abl.get(11, 0) >= target.abl.get(32, 0) + 1):
            return None
        return "侍奉精神/欲望不足"






    def _build_ability_upgrade_prereq_33(self, eng: Any, target: Character) -> Optional[str]:
        if target.talent.get(122, 0):
            return "男人不能提升百合中毒"
        return None if target.abl.get(22, 0) >= target.abl.get(33, 0) + 1 else "百合气质不足"






    def _build_ability_upgrade_prereq_37(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(11, 0) >= target.abl.get(37, 0) + 1 else "欲望不足"






    def _build_ability_upgrade_prereq_39(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(11, 0) >= target.abl.get(39, 0) + 1 else "欲望不足"






    def _build_ability_upgrade_prereq_40(self, eng: Any, target: Character) -> Optional[str]:
        return None if target.abl.get(11, 0) >= target.abl.get(40, 0) + 1 else "欲望不足"






    def _build_ability_upgrade_prereq_sense_0(self, eng: Any, target: Character) -> Optional[str]:
        if target.abl.get(0, 0) >= 5 and not target.talent.get(74, 0):
            return "需要特殊素质才能继续提升"
        if target.talent.get(101, 0) & 2:
            return "阴蒂感觉已经被封锁"
        if target.abl.get(0, 0) >= min(25, eng._get_sense_lock_count(target, 0) * 5 + 10):
            return "已达最高级"
        return None






    def _build_ability_upgrade_prereq_sense_1(self, eng: Any, target: Character) -> Optional[str]:
        if target.abl.get(1, 0) >= 5 and not target.talent.get(78, 0):
            return "需要特殊素质才能继续提升"
        if target.talent.get(107, 0) & 2:
            return "乳房感觉已经被封锁"
        if target.abl.get(1, 0) >= min(25, eng._get_sense_lock_count(target, 1) * 5 + 10):
            return "已达最高级"
        return None






    def _build_ability_upgrade_prereq_sense_2(self, eng: Any, target: Character) -> Optional[str]:
        if target.talent.get(122, 0):
            return "男人不能提升私处感觉"
        if target.abl.get(2, 0) >= 5 and not target.talent.get(75, 0):
            return "需要特殊素质才能继续提升"
        if target.talent.get(103, 0) & 2:
            return "私处感觉已经被封锁"
        if target.abl.get(2, 0) >= min(25, eng._get_sense_lock_count(target, 2) * 5 + 10):
            return "已达最高级"
        return None






    def _build_ability_upgrade_prereq_sense_3(self, eng: Any, target: Character) -> Optional[str]:
        if target.abl.get(3, 0) >= 5 and not target.talent.get(77, 0):
            return "需要特殊素质才能继续提升"
        if target.talent.get(105, 0) & 2:
            return "肛门感觉已经被封锁"
        if target.abl.get(3, 0) >= min(25, eng._get_sense_lock_count(target, 3) * 5 + 10):
            return "已达最高级"
        return None






    def _build_ability_upgrade_rule_entries_from_specs(self, specs: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        return {ability_id: self._build_ability_upgrade_rule_entry_from_spec(spec) for ability_id, spec in specs.items()}






    def _build_ability_upgrade_rule_entry(self, max_level: int, soft_cap, cost_types: Dict[int, str], costs, prereq=None, abnormal_exp=None, paths=None) -> Dict[str, Any]:
        entry: Dict[str, Any] = {
            "max_level": max_level,
            "soft_cap": soft_cap,
            "cost_types": cost_types,
        }
        if costs is not None:
            entry["costs"] = costs
        if prereq is not None:
            entry["prereq"] = prereq
        if abnormal_exp is not None:
            entry["abnormal_exp"] = abnormal_exp
        if paths is not None:
            entry["paths"] = paths
        return entry






    def _build_ability_upgrade_rule_entry_from_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        soft_cap = spec["soft_cap"]
        if isinstance(soft_cap, str):
            soft_cap = getattr(self, soft_cap)
        abnormal_exp = spec.get("abnormal_exp")
        if isinstance(abnormal_exp, str):
            abnormal_exp = getattr(self, abnormal_exp)
        prereq = spec.get("prereq")
        if isinstance(prereq, str):
            prereq = getattr(self, prereq)
        paths = spec.get("paths")
        if isinstance(paths, str):
            paths = getattr(self, paths)
        return self._build_ability_upgrade_rule_entry(
            spec["max_level"],
            soft_cap,
            spec["cost_types"],
            spec.get("costs"),
            prereq=prereq,
            abnormal_exp=abnormal_exp,
            paths=paths,
        )






    def _build_ability_upgrade_rules_core(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rules_core_block()






    def _build_ability_upgrade_rules_core_block(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rule_groups(
            self._build_ability_upgrade_rules_core_group_10_13(),
            self._build_ability_upgrade_rules_core_group_14_17(),
        )






    def _build_ability_upgrade_rules_core_group_10_13(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs(self._build_ability_upgrade_rules_core_group_10_13_specs())






    def _build_ability_upgrade_rules_core_group_10_13_specs(self) -> Dict[int, Dict[str, Any]]:
        return ABILITY_UPGRADE_COST_TABLE_10_13






    def _build_ability_upgrade_rules_core_group_14_17(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs(self._build_ability_upgrade_rules_core_group_14_17_specs())






    def _build_ability_upgrade_rules_core_group_14_17_specs(self) -> Dict[int, Dict[str, Any]]:
        return ABILITY_UPGRADE_COST_TABLE_14_17






    def _build_ability_upgrade_rules_senses(self) -> Dict[int, Dict[str, Any]]:
        return {
            0: {
                "max_level": 25,
                "soft_cap": self._build_ability_upgrade_soft_cap_25,
                "cost_types": {0: "juel"},
                "costs": lambda eng, t, level: eng._get_sense_upgrade_costs(t, 0, level),
                "prereq": self._build_ability_upgrade_prereq_sense_0,
            },
            1: {
                "max_level": 25,
                "soft_cap": self._build_ability_upgrade_soft_cap_25,
                "cost_types": {14: "juel"},
                "costs": lambda eng, t, level: eng._get_sense_upgrade_costs(t, 1, level),
                "prereq": self._build_ability_upgrade_prereq_sense_1,
            },
            2: {
                "max_level": 25,
                "soft_cap": self._build_ability_upgrade_soft_cap_25,
                "cost_types": {1: "juel", 0: "exp"},
                "costs": lambda eng, t, level: eng._get_sense_upgrade_costs(t, 2, level),
                "prereq": self._build_ability_upgrade_prereq_sense_2,
            },
            3: {
                "max_level": 25,
                "soft_cap": self._build_ability_upgrade_soft_cap_25,
                "cost_types": {2: "juel", 1: "exp"},
                "costs": lambda eng, t, level: eng._get_sense_upgrade_costs(t, 3, level),
                "prereq": self._build_ability_upgrade_prereq_sense_3,
            },
        }






    def _build_ability_upgrade_rules_services(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rule_groups(
            self._build_ability_upgrade_rules_services_4(),
            self._build_ability_upgrade_rules_services_5(),
            self._build_ability_upgrade_rules_services_6(),
            self._build_ability_upgrade_rules_services_7(),
            self._build_ability_upgrade_rules_services_8(),
            self._build_ability_upgrade_rules_services_9(),
        )






    def _build_ability_upgrade_rules_services_4(self) -> Dict[int, Dict[str, Any]]:
        return {
            4: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_5,
                "cost_types": {15: "juel"},
                "costs": lambda eng, t, level: eng._get_pleasure_f_upgrade_costs(t, level),
            }
        }






    def _build_ability_upgrade_rules_services_5(self) -> Dict[int, Dict[str, Any]]:
        return {
            5: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_5,
                "cost_types": {2: "juel", 1: "exp"},
                "costs": lambda eng, t, level: eng._get_pleasure_a_upgrade_costs(t, level),
            }
        }






    def _build_ability_upgrade_rules_services_6(self) -> Dict[int, Dict[str, Any]]:
        return {
            6: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_5,
                "paths": lambda eng, t, level: eng._get_ability_upgrade_path_options(t, 6, level),
                "cost_types": {2: "exp", 4: "juel", 6: "juel", 7: "juel", 20: "exp", 21: "exp"},
                "prereq": lambda eng, t: eng._get_ability_upgrade_path_prereq(t, 6),
                "abnormal_exp": lambda t: 1 if t.abl.get(6, 0) == 3 and not t.talent.get(86, 0) else 2 if t.abl.get(6, 0) == 4 and not t.talent.get(86, 0) else 0,
            }
        }






    def _build_ability_upgrade_rules_services_7(self) -> Dict[int, Dict[str, Any]]:
        return {
            7: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_5,
                "cost_types": {8: "juel", 2: "exp", 11: "exp"},
                "costs": lambda eng, t, level: eng._get_exhibition_pleasure_upgrade_costs(t, level),
                "prereq": lambda eng, t: eng._get_ability_upgrade_path_prereq(t, 7),
                "abnormal_exp": lambda t: 1 if t.abl.get(7, 0) == 3 and not t.talent.get(28, 0) else 2 if t.abl.get(7, 0) == 4 and not t.talent.get(28, 0) else 0,
            }
        }






    def _build_ability_upgrade_rules_services_8(self) -> Dict[int, Dict[str, Any]]:
        return {
            8: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_5,
                "paths": lambda eng, t, level: eng._get_ability_upgrade_path_options(t, 8, level),
                "cost_types": {2: "exp", 5: "juel", 6: "juel", 9: "juel", 30: "exp"},
                "prereq": lambda eng, t: eng._get_ability_upgrade_path_prereq(t, 8),
                "abnormal_exp": lambda t: 1 if t.abl.get(8, 0) == 3 and not t.talent.get(33, 0) else 2 if t.abl.get(8, 0) == 4 and not t.talent.get(33, 0) else 0,
            }
        }






    def _build_ability_upgrade_rules_services_9(self) -> Dict[int, Dict[str, Any]]:
        return {
            9: {
                "max_level": 5,
                "soft_cap": self._build_ability_upgrade_soft_cap_9,
                "paths": lambda eng, t, level: eng._get_ability_upgrade_path_options(t, 9, level),
                "cost_types": {0: "juel", 5: "juel", 6: "juel", 40: "exp"},
                "prereq": self._build_ability_upgrade_prereq_9,
                "abnormal_exp": lambda t: 1 if t.abl.get(9, 0) == 3 and not t.talent.get(81, 0) else 2 if t.abl.get(9, 0) == 4 and not t.talent.get(81, 0) else 0,
            }
        }






    def _build_ability_upgrade_rules_special(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rule_groups(
            self._build_ability_upgrade_rules_special_group_30_33(),
            self._build_ability_upgrade_rules_special_group_37_40(),
        )






    def _build_ability_upgrade_rules_special_group_30(self) -> Dict[int, Dict[str, Any]]:
        return {
            30: self._build_ability_upgrade_rule_entry(
                10,
                self._build_ability_upgrade_soft_cap_30,
                {5: "juel", 2: "juel", 14: "exp"},
                {
                    0: {5: 800, 2: 10, 14: 1},
                    1: {5: 2000, 2: 25, 14: 3},
                    2: {5: 3500, 2: 40, 14: 6},
                    3: {5: 8000, 2: 80, 14: 10},
                    4: {5: 15000, 2: 200, 14: 15},
                    5: {5: 25000, 2: 500, 14: 20},
                    6: {5: 35000, 2: 800, 14: 30},
                    7: {5: 50000, 2: 1200, 14: 40},
                    8: {5: 80000, 2: 1500, 14: 50},
                    9: {5: 150000, 2: 2000, 14: 80},
                },
                prereq=self._build_ability_upgrade_prereq_30,
            ),
        }






    def _build_ability_upgrade_rules_special_group_30_33(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rule_groups(
            self._build_ability_upgrade_rules_special_group_30(),
            self._build_ability_upgrade_rules_special_group_31(),
            self._build_ability_upgrade_rules_special_group_32(),
            self._build_ability_upgrade_rules_special_group_33(),
        )






    def _build_ability_upgrade_rules_special_group_31(self) -> Dict[int, Dict[str, Any]]:
        return {
            31: self._build_ability_upgrade_rule_entry(
                10,
                self._build_ability_upgrade_soft_cap_31,
                {5: "juel", 0: "juel", 8: "juel", 10: "exp"},
                {
                    0: {5: 3000, 0: 10000, 8: 1000, 10: 100},
                    1: {5: 6000, 0: 25000, 8: 3000, 10: 250},
                    2: {5: 12000, 0: 50000, 8: 6000, 10: 500},
                    3: {5: 20000, 0: 100000, 8: 15000, 10: 1000},
                    4: {5: 32000, 0: 200000, 8: 30000, 10: 1500},
                    5: {5: 50000, 0: 300000, 8: 50000, 10: 2500},
                    6: {5: 80000, 0: 500000, 8: 80000, 10: 3500},
                    7: {5: 120000, 0: 800000, 8: 120000, 10: 5000},
                    8: {5: 180000, 0: 1200000, 8: 180000, 10: 8000},
                    9: {5: 250000, 0: 1800000, 8: 250000, 10: 12000},
                },
                abnormal_exp=self._build_ability_upgrade_abnormal_exp_31,
                prereq=self._build_ability_upgrade_prereq_31,
            ),
        }






    def _build_ability_upgrade_rules_special_group_32(self) -> Dict[int, Dict[str, Any]]:
        return {
            32: self._build_ability_upgrade_rule_entry(
                10,
                self._build_ability_upgrade_soft_cap_32,
                {5: "juel", 6: "juel", 20: "exp"},
                {
                    0: {5: 3000, 6: 10000, 20: 10},
                    1: {5: 8000, 6: 20000, 20: 25},
                    2: {5: 15000, 6: 35000, 20: 40},
                    3: {5: 30000, 6: 60000, 20: 80},
                    4: {5: 50000, 6: 130000, 20: 200},
                    5: {5: 65000, 6: 190000, 20: 500},
                    6: {5: 90000, 6: 300000, 20: 800},
                    7: {5: 120000, 6: 500000, 20: 1200},
                    8: {5: 200000, 6: 800000, 20: 1500},
                    9: {5: 500000, 6: 1500000, 20: 2000},
                },
                abnormal_exp=self._build_ability_upgrade_abnormal_exp_32,
                prereq=self._build_ability_upgrade_prereq_32,
            ),
        }






    def _build_ability_upgrade_rules_special_group_33(self) -> Dict[int, Dict[str, Any]]:
        return {
            33: self._build_ability_upgrade_rule_entry(
                10,
                self._build_ability_upgrade_soft_cap_33,
                {5: "juel", 6: "juel", 0: "juel", 40: "exp"},
                {
                    0: {5: 1200, 6: 1200, 0: 5000, 40: 300},
                    1: {5: 3900, 6: 3900, 0: 15000, 40: 600},
                    2: {5: 6000, 6: 6000, 0: 23000, 40: 1000},
                    3: {5: 18000, 6: 18000, 0: 50000, 40: 1400},
                    4: {5: 30000, 6: 30000, 0: 70000, 40: 2100},
                    5: {5: 55000, 6: 55000, 0: 120000, 40: 3000},
                    6: {5: 70000, 6: 70000, 0: 200000, 40: 4000},
                    7: {5: 100000, 6: 100000, 0: 350000, 40: 5200},
                    8: {5: 150000, 6: 150000, 0: 500000, 40: 6500},
                    9: {5: 300000, 6: 300000, 0: 800000, 40: 8000},
                },
                abnormal_exp=self._build_ability_upgrade_abnormal_exp_33,
                prereq=self._build_ability_upgrade_prereq_33,
            ),
        }






    def _build_ability_upgrade_rules_special_group_37_40(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs(self._build_ability_upgrade_rules_special_group_37_40_specs())






    def _build_ability_upgrade_rules_special_group_37_40_specs(self) -> Dict[int, Dict[str, Any]]:
        return ABILITY_UPGRADE_COST_TABLE_37_40






    def _build_ability_upgrade_rules_traits(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rule_groups(
            self._build_ability_upgrade_rules_traits_20(),
            self._build_ability_upgrade_rules_traits_21(),
            self._build_ability_upgrade_rules_traits_22(),
            self._build_ability_upgrade_rules_traits_23(),
        )






    def _build_ability_upgrade_rules_traits_20(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs({
            20: {
                "max_level": 10,
                "soft_cap": self._build_ability_upgrade_soft_cap_20,
                "cost_types": {5: "juel", 33: "exp"},
                "costs": {
                    0: {5: 100, 33: 5},
                    1: {5: 500, 33: 20},
                    2: {5: 1500, 33: 50},
                    3: {5: 3000, 33: 120},
                    4: {5: 5000, 33: 300},
                    5: {5: 8000, 33: 600},
                    6: {5: 12000, 33: 1500},
                    7: {5: 15000, 33: 3000},
                    8: {5: 25000, 33: 5000},
                    9: {5: 30000, 33: 8000},
                },
                "abnormal_exp": self._build_ability_upgrade_abnormal_exp_20,
                "prereq": self._build_ability_upgrade_prereq_20,
            },
        })






    def _build_ability_upgrade_rules_traits_21(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs({
            21: {
                "max_level": 10,
                "soft_cap": self._build_ability_upgrade_soft_cap_10,
                "cost_types": {30: "exp", 50: "exp", 2: "exp"},
                "costs": {
                    0: {30: 10, 50: 1},
                    1: {30: 50, 50: 2},
                    2: {30: 150, 50: 3, 2: 1},
                    3: {30: 400, 50: 5, 2: 4},
                    4: {30: 1000, 50: 8, 2: 10},
                    5: {30: 2500, 50: 12, 2: 20},
                    6: {30: 5000, 50: 20, 2: 40},
                    7: {30: 12000, 50: 35, 2: 80},
                    8: {30: 20000, 50: 50, 2: 120},
                    9: {30: 35000, 50: 80, 2: 200},
                },
                "prereq": self._build_ability_upgrade_prereq_21,
            },
        })






    def _build_ability_upgrade_rules_traits_22(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs({
            22: {
                "max_level": 10,
                "soft_cap": self._build_ability_upgrade_soft_cap_22,
                "cost_types": {40: "exp"},
                "costs": {
                    0: {40: 1},
                    1: {40: 5},
                    2: {40: 15},
                    3: {40: 40},
                    4: {40: 80},
                    5: {40: 150},
                    6: {40: 250},
                    7: {40: 400},
                    8: {40: 650},
                    9: {40: 1000},
                },
                "prereq": self._build_ability_upgrade_prereq_22,
            },
        })






    def _build_ability_upgrade_rules_traits_23(self) -> Dict[int, Dict[str, Any]]:
        return self._build_ability_upgrade_rule_entries_from_specs({
            23: {
                "max_level": 10,
                "soft_cap": self._build_ability_upgrade_soft_cap_23,
                "cost_types": {5: "juel", 41: "exp", 6: "juel"},
                "costs": {
                    0: {5: 200, 41: 50},
                    1: {5: 1000, 41: 150},
                    2: {5: 3000, 41: 300, 6: 1000},
                    3: {5: 8000, 41: 500, 6: 2000},
                    4: {5: 20000, 41: 800, 6: 5000},
                    5: {5: 40000, 41: 1200, 6: 10000},
                    6: {5: 80000, 41: 1800, 6: 13000},
                    7: {5: 150000, 41: 2600, 6: 18000},
                    8: {5: 200000, 41: 3600, 6: 30000},
                    9: {5: 300000, 41: 5000, 6: 50000},
                },
                "abnormal_exp": self._build_ability_upgrade_abnormal_exp_23,
                "prereq": self._build_ability_upgrade_prereq_23,
            },
        })






    def _build_ability_upgrade_soft_cap_10(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_10_without_love(self, target: Character) -> int:
        return 5 if not (target.talent.get(85, 0) or target.talent.get(86, 0)) else 10






    def _build_ability_upgrade_soft_cap_11_without_support(self, target: Character) -> int:
        return 5 if not (target.talent.get(73, 0) or target.talent.get(76, 0)) else 10






    def _build_ability_upgrade_soft_cap_13(self, target: Character) -> int:
        return 10 if target.abl.get(16, 0) >= 5 else 5






    def _build_ability_upgrade_soft_cap_14(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_15(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_16(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_17(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_20(self, target: Character) -> int:
        return 10 if (target.talent.get(80, 0) or target.talent.get(83, 0) or target.talent.get(127, 0) or target.abl.get(20, 0) < 5) else 5






    def _build_ability_upgrade_soft_cap_22(self, target: Character) -> int:
        return 10 if not target.talent.get(122, 0) else 0






    def _build_ability_upgrade_soft_cap_23(self, target: Character) -> int:
        if target.talent.get(122, 0) and (target.talent.get(33, 0) or target.talent.get(80, 0) or target.talent.get(81, 0) or target.talent.get(123, 0) or target.abl.get(23, 0) < 5):
            return 10
        return 5 if target.talent.get(122, 0) else 0






    def _build_ability_upgrade_soft_cap_25(self, target: Character) -> int:
        return 25






    def _build_ability_upgrade_soft_cap_30(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_31(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_32(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_33(self, target: Character) -> int:
        if target.talent.get(122, 0):
            return 0
        if target.talent.get(76, 0) or target.talent.get(80, 0) or target.talent.get(81, 0) or target.talent.get(82, 0) or target.abl.get(33, 0) < 5:
            return 10
        return 5






    def _build_ability_upgrade_soft_cap_37(self, target: Character) -> int:
        return 10 if (target.talent.get(76, 0) or target.talent.get(31, 0) or target.talent.get(180, 0) or target.abl.get(37, 0) < 5) else 5






    def _build_ability_upgrade_soft_cap_39(self, target: Character) -> int:
        return 10 if (target.talent.get(76, 0) or target.talent.get(124, 0) or target.talent.get(136, 0) or target.abl.get(39, 0) < 5) else 5






    def _build_ability_upgrade_soft_cap_40(self, target: Character) -> int:
        return 10






    def _build_ability_upgrade_soft_cap_5(self, target: Character) -> int:
        return 5






    def _build_ability_upgrade_soft_cap_9(self, target: Character) -> int:
        return 0 if target.talent.get(122, 0) else 5






    def _check_ability_upgrade_limits(self, level: int, soft_cap: int, max_level: int) -> Optional[str]:
        if soft_cap <= 0:
            return "该角色无法提升此能力"
        if level >= max_level:
            return "已达最高级"
        if level >= soft_cap:
            return "需要特殊素质才能继续提升"
        return None






    def _choose_ability_upgrade_path(self, option: Dict[str, Any]) -> tuple[bool, Optional[Dict[str, Any]]]:
        available_paths = [path for path in option["paths"] if path.get("available")]
        if len(available_paths) > 1:
            print(f"\n【{option['name']} 升级路线】")
            for path in available_paths:
                path_cost_text = self._format_ability_upgrade_costs(path["costs"], option["cost_types"])
                print(f" [{path['menu_id']}] {path['label']} - {path_cost_text}")
            print(" [100] 放弃")
            raw_choice = self._prompt_choice()
            if raw_choice == "100":
                return False, None
            try:
                menu_id = int(raw_choice)
            except ValueError:
                return False, None
            selected_path = next((path for path in available_paths if int(path["menu_id"]) == menu_id), None)
            return True, selected_path
        if available_paths:
            return True, available_paths[0]
        return True, None






    def _collect_ability_upgrade_resource_shortfalls(self, target: Character, costs: Dict[int, int], cost_types: Dict[int, str]) -> List[str]:
        shortfalls: List[str] = []
        for resource_id, amount in costs.items():
            resource_type = cost_types.get(resource_id, "juel")
            current = self._get_ability_upgrade_resource_current(target, resource_id, resource_type)
            if current < amount:
                shortfalls.append(f"{resource_id}:{current}/{amount}")
        return shortfalls






    def _find_ability_up_roster_candidate(
        self,
        candidates: List[tuple[int, Character, Optional[str]]],
        selected: int,
    ) -> Optional[tuple[int, Character]]:
        return next(((idx, char) for idx, char, _ in candidates if idx == selected), None)






    def _get_ability_up_roster_blocked_reason(self, menu_code: str, idx: int, char: Character) -> Optional[str]:
        if menu_code == "997":
            return self._can_open_ability_up_hero_target(idx, char)
        return self._can_open_ability_up_slave_target(idx, char)






    def _get_ability_up_roster_mode_labels(self) -> Dict[str, str]:
        player = self._get_player()
        player_level = int(player.cflag.get(9, 0)) if player is not None else 0
        hero_locked = player_level < 20
        return {
            "998": "奴隶一览",
            "997": "勇者一览" + (" (需要迷宫Lv20)" if hero_locked else ""),
        }






    def _get_ability_upgrade_abnormal_exp_requirement_for_desire(self, target: Character) -> int:
        level = int(target.abl.get(11, 0))
        if level == 4 and all(int(target.talent.get(tid, 0)) == 0 for tid in (33, 70, 73, 76, 123)):
            return 1
        if level == 7 and all(int(target.talent.get(tid, 0)) == 0 for tid in (33, 70, 73, 76, 123)):
            return 3
        return 0






    def _get_ability_upgrade_cost_for_desire(self, target: Character) -> int:
        level = int(target.abl.get(11, 0))
        value = {
            0: 5,
            1: 50,
            2: 1000,
            3: 5000,
            4: 12000,
            5: 20000,
            6: 30000,
            7: 50000,
            8: 80000,
            9: 150000,
        }.get(level, 150000)
        if int(target.talent.get(27, 0)):
            if level == 3:
                value = value * 150 // 100
            elif level == 4:
                value *= 2
            elif level == 5:
                value = value * 250 // 100
            elif level >= 6:
                value *= 3
        if int(target.talent.get(20, 0)):
            value = value * 120 // 100
        if int(target.talent.get(24, 0)):
            value = value * 110 // 100
        if int(target.talent.get(30, 0)):
            value = value * 150 // 100
        elif int(target.talent.get(31, 0)):
            value = value * 95 // 100
        if int(target.talent.get(32, 0)):
            value = value * 150 // 100
        elif int(target.talent.get(33, 0)):
            value = value * 90 // 100
        if int(target.talent.get(34, 0)):
            value = value * 150 // 100
        if int(target.talent.get(35, 0)):
            value = value * 110 // 100
        elif int(target.talent.get(36, 0)):
            value = value * 95 // 100
        if int(target.talent.get(70, 0)):
            value = value * 80 // 100
        elif int(target.talent.get(71, 0)):
            value = value * 150 // 100
        if int(target.talent.get(72, 0)):
            value = value * 95 // 100
        if int(target.talent.get(73, 0)):
            value = value * 50 // 100
        if int(target.talent.get(76, 0)):
            value = value * 70 // 100
        if int(target.talent.get(180, 0)):
            value = value * 90 // 100
        if int(target.talent.get(181, 0)):
            value = value * 80 // 100
        if int(target.talent.get(157, 0)):
            value = value * 80 // 100
        return max(1, value)






    def _get_ability_upgrade_cost_for_sense(self, target: Character, ability_id: int) -> int:
        level = int(target.abl.get(ability_id, 0))
        return {
            0: 1,
            1: 20,
            2: 400,
            3: 8000,
            4: 20000,
            5: 40000,
            6: 60000,
            7: 90000,
            8: 120000,
            9: 180000,
        }.get(level, 180000)






    def _get_ability_upgrade_exp_requirement_for_sense(self, target: Character, ability_id: int) -> int:
        level = int(target.abl.get(ability_id, 0))
        if ability_id not in (2, 3):
            return 0
        if level == 0:
            return 2 if ability_id == 2 else 10
        if level == 1:
            return 10
        if level == 2:
            return 30
        if level == 3:
            return 75
        if level == 4:
            return 150
        if level == 5:
            return 180
        if level == 6:
            return 250
        if level == 7:
            return 350
        if level == 8:
            return 500
        return 600






    def _get_ability_upgrade_name(self, ability_id: int) -> str:
        names = {
            0: "阴蒂感觉",
            1: "乳房感觉",
            2: "私处感觉",
            3: "肛门感觉",
            4: "快F",
            5: "快A",
            6: "奉仕快感",
            7: "露出快感",
            8: "被虐快感",
            9: "百合快感",
            10: "顺从",
            11: "欲望",
            12: "技巧",
            13: "侍奉技术",
            14: "性交技术",
            15: "话术",
            16: "侍奉精神",
            17: "露出癖",
            20: "抖S气质",
            21: "抖M气质",
            22: "百合气质",
            23: "断背气质",
            30: "性交中毒",
            31: "自慰中毒",
            32: "精液中毒",
            33: "百合中毒",
            37: "卖淫中毒",
            39: "兽奸中毒",
            40: "自由中毒",
            99: "反抗刻印",
        }
        return names.get(ability_id, f"Ability {ability_id}")






    def _get_ability_upgrade_path_options(self, target: Character, ability_id: int, level: int) -> List[Dict[str, Any]]:
        if ability_id == 6:
            return self._get_service_pleasure_upgrade_paths(target, level)
        if ability_id == 8:
            return self._get_masochism_pleasure_upgrade_paths(target, level)
        if ability_id == 9:
            return self._get_lesbian_pleasure_upgrade_paths(target, level)
        return []






    def _get_ability_upgrade_path_prereq(self, target: Character, ability_id: int) -> Optional[str]:
        if ability_id == 6 and target.abl.get(10, 0) < target.abl.get(6, 0) + 1:
            return "顺从不足"
        if ability_id == 7 and target.abl.get(11, 0) < target.abl.get(7, 0) + 1:
            return "欲望不足"
        if ability_id == 8 and target.abl.get(11, 0) < target.abl.get(8, 0) + 1:
            return "欲望不足"
        return None






    def _get_ability_upgrade_resource_current(self, target: Character, resource_id: int, resource_type: str) -> int:
        if resource_type == "exp":
            return target.exp.get(resource_id, 0)
        return self._get_juel(resource_id)






    def _get_ability_upgrade_rules(self) -> Dict[int, Dict[str, Any]]:
        return self._merge_ability_upgrade_rules(
            self._build_ability_upgrade_rules_senses(),
            self._build_ability_upgrade_rules_services(),
            self._build_ability_upgrade_rules_core(),
            self._build_ability_upgrade_rules_traits(),
            self._build_ability_upgrade_rules_special(),
        )






    def _handle_ability_up_choice(self, target: Character, options: List[Dict[str, Any]], choice: str) -> Optional[bool]:
        if choice in ("100", "999"):
            return False
        if choice == "99":
            ok, message = self._apply_resistance_mark_reduction(target)
            print(f"\n{message}")
            self._pause()
            return True
        if not choice.isdigit():
            print("\nInvalid selection.")
            self._pause()
            return None

        ability_id = int(choice)
        selected_option = next((option for option in options if option["id"] == ability_id), None)
        if selected_option is None:
            print("\nInvalid selection.")
            self._pause()
            return None

        ok, message = self._apply_ability_upgrade(target, ability_id)
        print(f"\n{message}")
        self._pause()
        return True






    def _handle_ability_up_menu_choice(self, target: Character, options: List[Dict[str, Any]], choice: str) -> bool:
        handled = self._handle_ability_up_choice(target, options, choice)
        if handled is False:
            return True
        if handled is None:
            return False
        return False






    def _handle_ability_up_roster_selection(
        self,
        menu_code: str,
        candidates: List[tuple[int, Character, Optional[str]]],
        choice: str,
    ) -> bool:
        selected = self._parse_ability_up_roster_choice(choice)
        if selected is None:
            return False

        selected_pair = self._find_ability_up_roster_candidate(candidates, selected)
        if selected_pair is None:
            print("\nInvalid selection.")
            self._pause()
            return False

        idx, char = selected_pair
        blocked_reason = self._get_ability_up_roster_blocked_reason(menu_code, idx, char)
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            self._pause()
            return False
        self.interpreter.vars.target = idx
        return True






    def _prompt_ability_up_choice(self) -> str:
        return self._prompt_choice()






    def _prompt_ability_up_roster_choice(self) -> str:
        return self._prompt_choice()






    def _render_ability_up_panel(self, target: Character, ability_ids: List[int]) -> List[Dict[str, Any]]:
        print("\n【Ability Up】")
        print("-" * 30)
        print(f" Target: {target.name}")
        print(f" Submission: {self._get_submission_level(target)}")
        print(f" Desire: {target.abl.get(11, 0)}")
        print(f" Abnormal EXP: {target.exp.get(50, 0)}")
        print("-" * 30)

        options = [self._build_ability_upgrade_option(target, ability_id) for ability_id in ability_ids]
        for option in options:
            marker = "*" if option["available"] else "-"
            cost_text = self._format_ability_upgrade_costs(option["costs"], option["cost_types"]) if option["costs"] else "无"
            print(f" [{option['id']}] {marker} {option['name']} LV{option['level']} -> LV{option['level'] + 1}")
            print(f"      Cost: {cost_text}")
            if option["reasons"]:
                print(f"      Block: {'；'.join(option['reasons'])}")
        self._render_resistance_mark_reduction_option(target)
        print(" [999] Back")
        return options






    def _render_ability_up_roster_screen(
        self,
        labels: Dict[str, str],
        menu_code: str,
        candidates: List[tuple[int, Character, Optional[str]]],
    ) -> None:
        print("\n【Ability Up】")
        print("-" * 30)
        print(f" [998] {labels['998']}")
        print(f" [997] {labels['997']}")
        print(" 要提高谁的能力值？")
        print("-" * 30)
        if not candidates:
            print(" 当前没有符合条件的对象。")
        else:
            for idx, char, _ in candidates:
                level = self._get_character_level(char)
                status = "侵攻中" if menu_code == "997" else "待机"
                print(f" [{idx}] {char.name}  LV{level}  {status}")
        print(" [100] Back")






    def _select_ability_up_target_from_roster(self) -> bool:
        player = self._get_player()
        player_level = int(player.cflag.get(9, 0)) if player is not None else 0
        menu_code = "998"

        while True:
            if self._advance_ability_up_target_from_roster(player_level, menu_code):
                return False






    def show_ability_up(self):
        """Show ability up menu"""
        while True:
            target, ability_ids = self._prepare_ability_up_menu()
            if target is None:
                return
            if self._advance_ability_up_menu(target, ability_ids):
                return





