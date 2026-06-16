from __future__ import annotations
"""Module for NtrExtMixin - NTR系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class NtrExtMixin:
    """Mixin providing NTR系统 methods for GameEngine"""

    def _apply_ntr_child_birth(self, target: Character) -> List[str]:
        source = int(target.cflag.get(102, 0))
        messages = ["从狂王处收到了水晶球。"]
        messages.extend(self._build_ntr_child_birth_lines(target, source))
        messages.extend(self._run_ntr_kojo_lines(target))
        messages.extend(self._reset_pregnancy_state(target))
        return messages






    def _apply_ntr_growth_checks(self, target: Character) -> List[str]:
        messages: List[str] = []
        result, juel_cost = self._decide_ablup2(target)
        if result:
            target.abl[2] = int(target.abl.get(2, 0)) + 1
            self._consume_juel(1, juel_cost)
            messages.append(f"{self._get_ability_name(2)}变为LV{target.abl[2]}")
        result, juel_cost = self._decide_ablup3(target)
        if result:
            target.abl[3] = int(target.abl.get(3, 0)) + 1
            self._consume_juel(2, juel_cost)
            messages.append(f"{self._get_ability_name(3)}变为LV{target.abl[3]}")
        result, juel_cost = self._decide_ablup11(target)
        if result:
            target.abl[11] = int(target.abl.get(11, 0)) + 1
            self._consume_juel(5, juel_cost)
            messages.append(f"{self._get_ability_name(11)}变为LV{target.abl[11]}")
        return messages






    def _apply_ntr_video_play(self, target: Character) -> List[str]:
        if target is None:
            return []
        if (
            (int(target.talent.get(0, 0)) == 1 and random.randint(0, 1) == 0)
            or (int(target.cflag.get(42, 0)) == 79 and (int(target.cflag.get(40, 0)) & 64) and int(self.interpreter.vars.globals.get(37, 0)))
            or int(target.talent.get(273, 0))
        ):
            messages = []
            if int(self.interpreter.vars.globals.get(500, 0)) == 1:
                target.exp[1] = int(target.exp.get(1, 0)) + 10
                target.exp[40] = int(target.exp.get(40, 0)) + 5
            else:
                target.exp[1] = int(target.exp.get(1, 0)) + 10
                target.exp[20] = int(target.exp.get(20, 0)) + 10
            target.palam[2] = target.palam.get(2, 0) + 2000
            target.palam[5] = target.palam.get(5, 0) + 2500
            messages.append(f"{target.name} 的处女肛交影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages
        if int(target.talent.get(0, 0)) == 1:
            messages = []
            target.exp[0] = int(target.exp.get(0, 0)) + 3
            target.palam[1] = target.palam.get(1, 0) + 600
            title = f"失贞的{target.name}"
            target.cstr[6] = title
            self._maturo_video_title(target, title)
            target.talent[0] = 0
            target.talent[280] = 1
            target.cflag[15] = 105
            target.cstr[random.randint(10, 17)] = "狂王的纹章"
            messages.append(f"{target.name} 失去了处女。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages

        if int(target.abl.get(39, 0)) > 0 and random.randint(0, 9) == 0:
            messages = []
            target.exp[0] = int(target.exp.get(0, 0)) + 20
            target.exp[20] = int(target.exp.get(20, 0)) + 20
            target.exp[56] = int(target.exp.get(56, 0)) + 20
            target.palam[1] = target.palam.get(1, 0) + 4000
            target.palam[5] = target.palam.get(5, 0) + 5000
            target.cstr[6] = f"兽奸秀{target.name}"
            self._maturo_video_title(target, target.cstr[6])
            if int(self.interpreter.vars.globals.get(5, 0)) & 4:
                target.cflag[106] = 10
            messages.append(f"{target.name} 的兽奸影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages

        play_type = random.randint(0, 3) + 4

        if play_type == 4:
            messages = []
            if int(self.interpreter.vars.globals.get(500, 0)) == 1:
                target.exp[0] = int(target.exp.get(0, 0)) + 5
                target.exp[40] = int(target.exp.get(40, 0)) + 5
            else:
                target.exp[0] = int(target.exp.get(0, 0)) + 5
                target.exp[20] = int(target.exp.get(20, 0)) + 5
            target.palam[1] = target.palam.get(1, 0) + 1000
            target.palam[5] = target.palam.get(5, 0) + 1250
            target.cstr[6] = f"狂王的NTR视频{target.name}"
            self._maturo_video_title(target, target.cstr[6])
            if int(self.interpreter.vars.globals.get(500, 0)) != 1 and int(self.interpreter.vars.globals.get(5, 0)) & 4:
                target.cflag[108] = 10
            if int(target.cflag.get(16, -1)) == -1:
                target.cflag[16] = 993
            messages.append(f"{target.name} 的 NTR 影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages
        if play_type == 5:
            messages = []
            target.exp[0] = int(target.exp.get(0, 0)) + 10
            target.exp[1] = int(target.exp.get(1, 0)) + 10
            if int(self.interpreter.vars.globals.get(500, 0)) == 1:
                target.exp[40] = int(target.exp.get(40, 0)) + 5
            else:
                target.exp[20] = int(target.exp.get(20, 0)) + 10
            target.palam[1] = target.palam.get(1, 0) + 2000
            target.palam[2] = target.palam.get(2, 0) + 2000
            target.palam[5] = target.palam.get(5, 0) + 2500
            target.cstr[6] = f"狂王的NTR视频{target.name}"
            self._maturo_video_title(target, target.cstr[6])
            if int(self.interpreter.vars.globals.get(500, 0)) != 1 and int(self.interpreter.vars.globals.get(5, 0)) & 4:
                target.cflag[105] = 10
            messages.append(f"{target.name} 的 NTR 影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages
        if play_type == 6:
            messages = []
            target.exp[0] = int(target.exp.get(0, 0)) + 20
            target.exp[1] = int(target.exp.get(1, 0)) + 20
            target.exp[20] = int(target.exp.get(20, 0)) + 20
            target.palam[1] = target.palam.get(1, 0) + 4000
            target.palam[2] = target.palam.get(2, 0) + 4000
            target.palam[5] = target.palam.get(5, 0) + 5000
            target.cstr[6] = f"魔族公厕{target.name}"
            self._maturo_video_title(target, target.cstr[6])
            if int(self.interpreter.vars.globals.get(5, 0)) & 4:
                target.cflag[105] = 10
            messages.append(f"{target.name} 的公厕影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages
        if play_type == 7:
            messages = []
            if int(self.interpreter.vars.globals.get(500, 0)) != 1:
                target.exp[22] = int(target.exp.get(22, 0)) + 3
                target.exp[20] = int(target.exp.get(20, 0)) + 3
            target.palam[5] = target.palam.get(5, 0) + 1250
            target.cstr[6] = f"侍奉狂王的{target.name}"
            self._maturo_video_title(target, target.cstr[6])
            if int(self.interpreter.vars.globals.get(500, 0)) != 1 and int(target.cflag.get(16, -1)) == -1:
                target.cflag[16] = 993
            messages.append(f"{target.name} 的侍奉影像被记录了。")
            messages.extend(self._run_ntr_kojo_lines(target))
            return messages
        return []






    def _build_ntr_child_birth_lines(self, target: Character, source: int) -> List[str]:
        lines = [f"水晶球里播放着{target.name}在狂王和观众前公开生孩子的视频。"]
        if source == 7:
            lines.append("被魔法药物促进发育的胎儿，全身肌肤和毛发都是雪白的婴儿呱呱坠地了。")
            lines.append("『都不知道生了几个这样的，从十人之后就没数了。』狂王笑着说，周围的观众也都笑了。")
            return lines
        if source == 4:
            lines.append("被魔法药物促进发育的胎儿，全身肌肤和毛发都是雪白的婴儿呱呱坠地了。")
            lines.append("『连父亲都不知道是谁的孩子，就当成是你的啦！』狂王笑着说，周围的观众也都笑了。")
            return lines
        if source in (2, 3):
            lines.append("被魔法药物促进发育的胎儿，全身肌肤和毛发都是雪白的婴儿呱呱坠地了。")
            lines.append("『在勇者之间配对，是个不错的爱好，不止魔王才这样哦！』狂王笑着说，周围的观众也都笑了。")
            return lines
        roll = random.randint(0, 2)
        if roll == 0:
            lines.append("『污秽的肚子里，只能生出怪物了吗？』周围的观众嘲笑着。")
            lines.append("刚出生的怪物，当场被肢解杀掉了………")
        elif roll == 1:
            lines.append("『污秽的肚子里，只能生出怪物了吗？』周围的观众嘲笑着。")
            lines.append("刚出生的怪物，企图攻击狂王，被随手杀掉了………")
        else:
            lines.append("『污秽的肚子里，只能生出怪物了吗？』周围的观众嘲笑着。")
            lines.append("刚出生的怪物，被举高丢地板上，举高丢地板上，好几次，被摔死了………")
        return lines






    def _build_ntr_kojo_fallback_lines(self, target: Character) -> List[str]:
        source = int(target.cflag.get(102, 0))
        kojo_num = self._get_kojo_num(target)
        if kojo_num == 100:
            if int(target.talent.get(76, 0)) or int(target.talent.get(85, 0)):
                if source == 1:
                    return ["「呜咕～咿咕～…魔王大人和我的小宝宝…啊啊啊～对不起～对不起～～！」"]
                return ["「啊呜～呜呜～…对不起、对不起…我的可爱宝宝………」"]
            return ["「哈啊哈啊…是、我的子宮是狂王大人的専用孕袋…啊啊啊…」"]
        return []






    def _can_pay_ntr_growth_cost(self, target: Character, juel_idx: int, required: int) -> bool:
        return self._get_juel(juel_idx) >= required






    def _decide_ntr_anal_sense_upgrade(self, target: Character) -> tuple[bool, int]:
        level = int(target.abl.get(3, 0))
        lock_count = sum(1 for talent_id in (101, 103, 107) if int(target.talent.get(talent_id, 0)) & 2)
        if level >= 5 and int(target.talent.get(77, 0)) == 0:
            return False, 0
        if level >= lock_count * 5 + 10:
            return False, 0
        if int(target.talent.get(105, 0)) & 2:
            return False, 0
        cost = self._get_ntr_sense_upgrade_cost(3, level, target)
        exp_cost = self._get_ntr_sense_upgrade_exp_cost(3, level, target)
        if not self._can_pay_ntr_growth_cost(target, 2, cost):
            return False, cost
        if int(target.exp.get(1, 0)) < exp_cost:
            return False, cost
        return True, cost






    def _decide_ntr_desire_upgrade(self, target: Character) -> tuple[bool, int]:
        level = int(target.abl.get(11, 0))
        if level >= 5 and int(target.talent.get(73, 0)) == 0 and int(target.talent.get(76, 0)) == 0:
            return False, 0
        if level >= 10:
            return False, 0
        cost = self._get_ability_upgrade_cost_for_desire(target)
        if not self._can_pay_ntr_growth_cost(target, 5, cost):
            return False, cost
        if int(target.exp.get(50, 0)) < self._get_ability_upgrade_abnormal_exp_requirement_for_desire(target):
            return False, cost
        return True, cost






    def _decide_ntr_private_sense_upgrade(self, target: Character) -> tuple[bool, int]:
        if int(target.talent.get(122, 0)):
            return False, 0
        level = int(target.abl.get(2, 0))
        lock_count = sum(1 for talent_id in (101, 105, 107) if int(target.talent.get(talent_id, 0)) & 2)
        if level >= 5 and int(target.talent.get(75, 0)) == 0:
            return False, 0
        if level >= lock_count * 5 + 10:
            return False, 0
        if int(target.talent.get(103, 0)) & 2:
            return False, 0
        cost = self._get_ntr_sense_upgrade_cost(2, level, target)
        exp_cost = self._get_ntr_sense_upgrade_exp_cost(2, level, target)
        if not self._can_pay_ntr_growth_cost(target, 1, cost):
            return False, cost
        if int(target.exp.get(0, 0)) < exp_cost:
            return False, cost
        return True, cost






    def _get_ntr_sense_upgrade_cost(self, ability_id: int, level: int, target: Optional[Character] = None) -> int:
        cost_table = {
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
        }
        if level in cost_table:
            value = cost_table[level]
        elif level < 15:
            value = 180000
            for _ in range(level - 8):
                value = value * 125 // 100
        elif level < 20:
            value = 362000
            for _ in range(level - 13):
                value = value * 120 // 100
        elif level < 25:
            value = 583000
            for _ in range(level - 18):
                value = value * 115 // 100
        else:
            value = 583000
        if target is None:
            return max(1, value)
        if int(target.talent.get(27, 0)):
            if level == 4:
                value *= 2
            elif level == 5:
                value = value * 250 // 100
            elif level >= 6:
                value *= 3
        if ability_id == 2 and int(target.talent.get(103, 0)):
            value = value * 120 // 100
        if ability_id == 3 and int(target.talent.get(105, 0)):
            value = value * 120 // 100
        lock_ids = (101, 105, 107) if ability_id == 2 else (101, 103, 107)
        lock_count = sum(1 for talent_id in lock_ids if int(target.talent.get(talent_id, 0)) & 2)
        if level > 5 and level <= 10 and lock_count > 0:
            value = value * (15 - lock_count) // 15
        elif level <= 15 and lock_count > 1:
            value = value * (16 - lock_count) // 15
        elif level <= 20 and lock_count > 2:
            value = value * (17 - lock_count) // 15
        if int(target.talent.get(76, 0)):
            value = value * 80 // 100
        if ability_id == 2 and int(target.talent.get(75, 0)):
            value = value * 80 // 100
        if ability_id == 3 and int(target.talent.get(77, 0)):
            value = value * 80 // 100
        if int(target.talent.get(104 if ability_id == 2 else 106, 0)):
            value = value * 80 // 100
        return max(1, value)






    def _get_ntr_sense_upgrade_exp_cost(self, ability_id: int, level: int, target: Optional[Character] = None) -> int:
        exp_table = {
            0: 2,
            1: 10,
            2: 30,
            3: 75,
            4: 150,
            5: 180,
            6: 250,
            7: 350,
            8: 500,
            9: 600,
        }
        if level in exp_table:
            value = exp_table[level]
        elif level < 15:
            value = 600
            for _ in range(level - 8):
                value = value * 115 // 100
        elif level < 20:
            value = 966
            for _ in range(level - 13):
                value = value * 120 // 100
        elif level < 25:
            value = 1942
            for _ in range(level - 18):
                value = value * 125 // 100
        else:
            value = 1942
        if target is None:
            return max(1, value)
        if int(target.talent.get(27, 0)):
            if level == 4:
                value *= 2
            elif level == 5:
                value = value * 250 // 100
            elif level >= 6:
                value *= 3
        if ability_id == 2 and int(target.talent.get(103, 0)):
            value = value * 110 // 100
        if ability_id == 3 and int(target.talent.get(105, 0)):
            value = value * 110 // 100
        lock_ids = (101, 105, 107) if ability_id == 2 else (101, 103, 107)
        lock_count = sum(1 for talent_id in lock_ids if int(target.talent.get(talent_id, 0)) & 2)
        if level > 5 and level <= 10 and lock_count > 0:
            value = value * (20 - lock_count) // 20
        elif level <= 15 and lock_count > 1:
            value = value * (21 - lock_count) // 20
        elif level <= 20 and lock_count > 2:
            value = value * (22 - lock_count) // 20
        if int(target.talent.get(76, 0)):
            value = value * 80 // 100
        if ability_id == 2 and int(target.talent.get(75, 0)):
            value = value * 80 // 100
        if ability_id == 3 and int(target.talent.get(77, 0)):
            value = value * 80 // 100
        if int(target.talent.get(104 if ability_id == 2 else 106, 0)):
            value = value * 80 // 100
        return max(1, value)






    def _load_ntr_kojo_source_text(self, target: Character) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        if kojo_num <= 0:
            return []
        lines: List[str] = []
        for suffix, block_kojo_num in self._get_self_kojo_source_variants(kojo_num):
            path = self._resolve_kojo_file_path(suffix)
            if path is None:
                continue
            content = self._read_kojo_file_content(path)
            lines.extend(self._extract_kojo_block_lines(content, f"@NTR_KOUJO_K{block_kojo_num}"))
        return lines




    def _restore_character_as_invading_hero_from_ntr_video(self, hero: Character) -> None:
        hero.cflag[1] = 2
        hero.cflag[501] = 1
        hero.cflag[502] = 0
        hero.cflag[508] = 3
        if int(hero.cflag.get(151, 0)) < -50:
            hero.cflag[151] = -50
        hero.cflag[2] = 20




    def _run_ntr_kojo_lines(self, target: Character) -> List[str]:
        source_lines = self._load_ntr_kojo_source_text(target)
        if not source_lines:
            return self._build_ntr_kojo_fallback_lines(target)
        return self._parse_self_kojo_block(source_lines, target)

    def _ntr_play(self):
        return self.call_erb_function('NTR_PLAY')

    def _ntr_child_birth(self):
        return self.call_erb_function('NTR_CHILD_BIRTH')





