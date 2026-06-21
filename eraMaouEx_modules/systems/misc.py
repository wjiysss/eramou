from __future__ import annotations
"""Module for MiscMixin - Remaining miscellaneous GameEngine methods"""
import random
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character

VERSION = "0.92 Ex 2.1"
VERSION_NAME = "Python Edition"


class MiscMixin:
    """Mixin providing remaining miscellaneous GameEngine methods"""
    def __init__(self, erb_dir: str):
        self.erb_dir = erb_dir
        self.paths = GamePaths(erb_dir)
        self.paths.ensure_dirs()
        self.interpreter = ERBInterpreter()
        self.interpreter.paths = self.paths
        self.palam_level_thresholds, self.exp_level_thresholds = self._load_level_thresholds()
        self.train_commands = self._load_train_commands()
        self.item_catalog = self._load_item_catalog()
        self.talent_catalog = self._load_talent_catalog()
        self.character_template_catalog = self._build_character_template_catalog()
        self.running = True


    def __init__(self, erb_dir: str):
        self.erb_dir = erb_dir
        self.paths = GamePaths(erb_dir)
        self.paths.ensure_dirs()
        self.interpreter = ERBInterpreter()
        self.interpreter.paths = self.paths
        self.palam_level_thresholds, self.exp_level_thresholds = self._load_level_thresholds()
        self.train_commands = self._load_train_commands()
        self.item_catalog = self._load_item_catalog()
        self.talent_catalog = self._load_talent_catalog()
        self.character_template_catalog = self._build_character_template_catalog()
        self.running = True


    def _adjust_long_goodbye_witness_stress(self, witness: Character, stress: int) -> int:
        if witness.talent.get(85, 0):
            stress -= 120
        if witness.talent.get(76, 0):
            stress -= 60
        if witness.talent.get(12, 0):
            stress -= 20
        if witness.talent.get(22, 0):
            stress -= 20
        if witness.talent.get(134, 0):
            stress += 20

        stress -= int(witness.abl.get(10, 0)) * 10
        stress += int(witness.mark.get(3, 0)) * 30
        return stress


    def _after_autotrain(self, target: Character) -> List[str]:
        """自动调教後処理 - 对应 @AFTER_AUTOTRAIN
        カルマ増減、潤滑/欲情蓄積、珠チェック、自動能力UP等
        """
        messages: List[str] = []
        v = self.interpreter.vars

        ex_1 = int(target.exp.get(1, 0)) if isinstance(target.exp.get(1, 0), int) else 0
        if ex_1:
            messages.append("(私处绝顶导致善良值下降:-1)")
            messages.extend(self._karma(target, -1))

        ex_2 = int(target.exp.get(2, 0)) if isinstance(target.exp.get(2, 0), int) else 0
        if ex_2:
            messages.append("(肛门绝顶导致善良值下降:-2)")
            messages.extend(self._karma(target, -2))

        if int(v.get_flag(75, 0)) == 0 and int(target.talent.get(271, 0)) == 0:
            palam_3 = int(target.palam.get(3, 0))
            if palam_3 >= 10000:
                target.cflag[81] = int(target.cflag.get(81, 0)) + palam_3 // 10000
            else:
                target.cflag[81] = 0

            palam_5 = int(target.palam.get(5, 0))
            if palam_5 >= 10000:
                target.cflag[82] = int(target.cflag.get(82, 0)) + palam_5 // 10000
            else:
                target.cflag[82] = 0

        target.juel[100] = 0

        target.cflag[667] = int(target.cflag.get(667, 0)) + int(target.cflag.get(666, 0))

        messages.extend(self._juel_check_main(target))

        if self._get_flag_bit(5, 35):
            self._auto_ablup(target)

        if int(target.cflag.get(667, 0)) > 50:
            target.cflag[667] = 50

        return messages


    def _aftertrain_assistant_lesbian_count_by_toxicity(self, level: int) -> int:
        return {1: 1, 2: 2, 3: 5, 4: 8, 5: 13}.get(level, 18 if level >= 6 else 0)


    def _aftertrain_lesbian_count_by_toxicity(self, level: int) -> int:
        return {1: 1, 2: 2, 3: 3, 4: 5, 5: 7}.get(level, 9 if level >= 6 else 0)


    def _append_character(self, char: Optional[Character]) -> Optional[Character]:
        if char is None:
            return None
        self.interpreter.vars.chars.append(char)
        if len(self.interpreter.vars.chars) > 1 and (self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15)):
            self._ensure_character_body_profile(char)
        return char


    def _append_conquest_candidate(self, target: Character) -> tuple[bool, str]:
        if len(self.interpreter.vars.chars) >= self._get_max_charanum():
            return False, "奴隶太多了！"
        self._append_character(target)
        return True, f"{target.name} 加入了队伍。"


    def _append_train_video_to_shelf(self, title: str) -> None:
        next_id = 0
        if self.interpreter.vars.suisei_str:
            next_id = max(int(key) for key in self.interpreter.vars.suisei_str.keys()) + 1
        self.interpreter.vars.suisei_str[next_id] = title


    # ========================================
    # MAGIC - 魔法系统
    # 对应 ERB/MAGIC.ERB
    # ========================================

    # 魔法定义表
    # ID: { name, type, mp_cost, description }
    _MAGIC_DEFINITIONS = {
        1: {"name": "传送术", "type": "escape", "mp_cost": 10,
            "description": "危机关头传送脱离"},
        2: {"name": "睡眠咒语", "type": "debuff", "mp_cost": 30,
            "description": "使目标陷入睡眠"},
        3: {"name": "魔法箭", "type": "attack", "mp_cost": 15,
            "description": "魔法箭攻击"},
        4: {"name": "魔法吸取", "type": "drain_hp", "mp_cost": 30,
            "description": "吸取HP恢复自身"},
        5: {"name": "火球术", "type": "attack_aoe", "mp_cost": 40,
            "description": "范围火焰攻击"},
        6: {"name": "治疗术", "type": "heal", "mp_cost": 5,
            "description": "恢复HP"},
        7: {"name": "诅咒术", "type": "debuff", "mp_cost": 30,
            "description": "降低目标防御"},
        8: {"name": "精神吸收", "type": "drain_mp", "mp_cost": 30,
            "description": "吸取气力恢复自身"},
        9: {"name": "经验吸取", "type": "drain_exp", "mp_cost": 50,
            "description": "吸取经验值"},
    }


    # ========================================
    # 角色创建系统 (对应 ERB CHARA_MAKE.ERB)
    # ========================================


    def _assign_invading_hero_spawn_position(self, hero: Character):
        x = random.randint(0, 31)
        y = random.randint(0, 31)
        roll = random.randint(0, 3)
        if roll == 0:
            x = 0
        elif roll == 1:
            y = 0
        elif roll == 2:
            x = 31
        else:
            y = 31
        hero.cflag[510] = x
        hero.cflag[511] = y


    def _auto_ablup(self, target: Character) -> List[str]:
        """自動能力UP - 对应 @AUTO_ABLUP
        珠が足りている場合に自動的に能力を上げる
        """
        messages: List[str] = []
        abl_cost_map = {
            0: {0: 10},
            1: {0: 20},
            2: {0: 30},
            3: {0: 40},
            4: {0: 50},
            5: {0: 60},
            6: {0: 70},
            7: {0: 80},
            8: {0: 90},
            9: {0: 100},
        }
        for abl_id, costs in abl_cost_map.items():
            current_abl = int(target.abl.get(abl_id, 0))
            required_level = current_abl + 1
            cost = costs.get(0, required_level * 10)
            juel_available = int(target.juel.get(0, 0))
            if juel_available >= cost:
                target.abl[abl_id] = required_level
                target.juel[0] = juel_available - cost
                char_name = getattr(target, 'savestr', target.name or "")
                messages.append(f"{char_name}的ABL:{abl_id}自动提升到{required_level}")
        return messages


    def _auto_buying(self) -> List[str]:
        """アイテムの自動購入処理 - 对应 @AUTO_BUYING"""
        messages: List[str] = []
        v = self.interpreter.vars

        if (v.flags.get(34, 0) & 1) and v.money >= 200 and v.items.get(25, 0) == 0:
            v.items[25] = v.items.get(25, 0) + 1
            v.money -= 200
            if hasattr(v, 'ex_flag'):
                v.ex_flag[4444] = v.ex_flag.get(4444, 0) - 200

        if (v.flags.get(34, 0) & 2) and v.money >= 500 and v.items.get(6, 0) and v.items.get(28, 0) == 0:
            v.items[28] = v.items.get(28, 0) + 1
            v.money -= 500
            if hasattr(v, 'ex_flag'):
                v.ex_flag[4444] = v.ex_flag.get(4444, 0) - 500

        if v.flags.get(34, 0) & 8:
            for _ in range(10):
                if v.money >= 100 and v.items.get(24, 0) < 10:
                    v.items[24] = v.items.get(24, 0) + 1
                    v.money -= 100
                    if hasattr(v, 'ex_flag'):
                        v.ex_flag[4444] = v.ex_flag.get(4444, 0) - 100

        return messages


    def _before_autotrain(self, target: Character) -> None:
        """自动调教前ソースリセット - 对应 @BEFORE_AUTOTRAIN"""
        for i in range(17):
            target.source[i] = 0


    def _beforetrain_noclothes(self, target: Character) -> List[str]:
        """初次调教时·着衣设定OFF - 对应 @PRITRAIN_MESSAGE_NOCLOTHES"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()
        target_name = getattr(target, 'savestr', target.name or "")
        player_name = getattr(player, 'callname', "主人") if player else "主人"

        if int(target.talent.get(22, 0)):
            messages.append(f"{target_name}依{player_name}的命令脱掉了衣服，")
            messages.append("没有展露出任何情绪，或是很好地掩饰住了情绪。然后就这样呆立不动。")
        elif int(target.talent.get(132, 0)) and int(target.talent.get(135, 0)):
            messages.append(f"{target_name}没有等{player_name}把命令说完就开始了脱衣服，一下子脱得精光。")
        elif int(target.talent.get(12, 0)):
            messages.append(f"赤裸的{target_name}把双手遮在胸前，")
            messages.append("露出绝不屈服的坚决态度。")
        elif int(target.talent.get(11, 0)):
            messages.append(f"{player_name}伸手粗暴地将{target_name}剥光。")
            messages.append(f"{target_name}一边拼命抓住衣服，一边用手遮住裸露出来的皮肤，")
            messages.append(f"同时用可怕的眼神狠狠地盯着{player_name}。")
        elif int(target.talent.get(21, 0)):
            messages.append(f"听到{player_name}的命令，{target_name}耸了耸肩，把衣服脱了。")
            messages.append("无论怎样都无所谓，只是请稍微迅速一点。")
            messages.append("就是这种态度。")
        elif int(target.talent.get(132, 0)):
            messages.append(f"被剥光的{target_name}非常地害怕。")
            messages.append("再怎么伪装也还是个孩子罢了。")
        elif int(target.talent.get(20, 0)):
            messages.append(f"被剥光的{target_name}用手遮住自己的身体，")
            messages.append("表面上仍装作很平静。")
        elif int(target.talent.get(10, 0)):
            messages.append(f"被剥光的{target_name}肩膀颤抖着。")
            messages.append("想象到了自己今后的命运，不禁牙齿打颤。")
        elif int(target.talent.get(15, 0)):
            messages.append(f"{target_name}想到全裸的耻辱和今后作为奴隶的屈辱，")
            messages.append("拼命地克制住自己颤抖着的牙齿和肩膀。")
        elif int(target.talent.get(17, 0)):
            messages.append(f"被剥光的{target_name}提心吊胆地观察着{player_name}的表情。")
            messages.append("心里想着言听计从的话也许可以减少痛苦。")
        elif int(target.talent.get(13, 0)):
            messages.append(f"被剥光的{target_name}对自己现在的处境难以接受。")
            messages.append("人不能对他人做这么过分的事，难道不是这样的吗？")
        elif int(target.talent.get(14, 0)):
            messages.append(f"意识到抵抗是无用的，{target_name}乖乖地把自己的衣服脱光了。")
            messages.append("至少，躲过了被强行剥光的屈辱不是吗？")
        elif int(target.talent.get(16, 0)):
            messages.append(f"{target_name}在害怕的同时对{player_name}投以挑衅的目光。")
            messages.append("这种事是不会让我屈服的，好像有这种自信的样子。")
        else:
            messages.append(f"{target_name}被剥光了。")

        return messages


    def _begin_child_care_state(self, target: Character) -> List[str]:
        messages: List[str] = []
        target.talent[153] = 0
        target.talent[154] = 1
        target.cflag[1] = 10
        self._clear_current_character_selection(target)
        if target.talent.get(85, 0) and int(target.cflag.get(111, 0)) == 0 and int(target.talent.get(155, 0)) == 0:
            messages.append(f"{target.name} 温柔地哄着为你生下的孩子………")
            messages.append(f"看来{target.name} 的【{self._get_talent_name(155)}】觉醒了。")
            target.talent[155] = 1
        target.talent[341] = 0
        target.talent[342] = 0
        target.talent[343] = 0
        messages.append(f"{target.name} 开始在育儿室照顾孩子。")
        messages.extend(self._get_child_care_begin_kojo_lines(target))
        return messages


    def _bootstrap_game_runtime(self) -> None:
        print(f"Loading eraMaouEx v{VERSION} ({VERSION_NAME})...")
        try:
            self.load_erb_files()
            self._report_loaded_erb_function_count()
        except Exception as e:
            self._report_erb_load_failure(e)


    def _break_character_lover(self, idx: int, char: Character) -> tuple[bool, str]:
        if not self._has_dungeon_town_lover(idx):
            return False, f"{char.name} 当前没有恋人。"
        self._clear_character_lover_relation(idx, char)
        return True, f"{char.name} 与恋人分手了。"


    def _calculate_aftertrain_beastsex_count(self, target: Character) -> int:
        count = 0
        level = int(target.abl.get(39, 0))
        if level == 0:
            count -= 2
        elif level == 1:
            count -= 1
        elif level == 2:
            count += 0
        elif level == 3:
            count += 1
        elif level == 4:
            count += 2
        elif level == 5:
            count += 3
        elif level >= 6:
            count += 4
        if int(target.talent.get(124, 0)) and int(target.abl.get(11, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.talent.get(136, 0)):
            count += 2
        if int(target.talent.get(17, 0)):
            count += 1
        if int(target.talent.get(33, 0)):
            count += 1
        if int(target.talent.get(124, 0)):
            count += 1
        if int(target.talent.get(15, 0)):
            count -= 1
        if int(target.talent.get(20, 0)):
            count -= 1
        if int(target.talent.get(32, 0)):
            count -= 1
        if int(target.talent.get(62, 0)) and int(target.talent.get(64, 0)) == 0:
            count -= 2
        if int(target.talent.get(70, 0)):
            count += 1
        elif int(target.talent.get(71, 0)):
            count -= 2
        if int(target.talent.get(76, 0)):
            count += 1
        if int(target.talent.get(136, 0)):
            count = int(count * 1.5)
        return max(count, 0)


    def _calculate_aftertrain_lesbian_play_count(self, target: Character, assistant: Character) -> int:
        plays = 0
        plays += self._aftertrain_lesbian_count_by_toxicity(int(target.abl.get(33, 0)))
        plays += self._aftertrain_assistant_lesbian_count_by_toxicity(int(assistant.abl.get(33, 0)))
        if plays <= 0:
            return 0
        if int(target.abl.get(22, 0)) >= 5 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            plays += 1
        if int(assistant.abl.get(22, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            plays += 1
        if int(target.abl.get(11, 0)) >= 7 and int(target.abl.get(5, 0)) >= 6 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            plays += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(2, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            plays += 1
        relation = self._get_character_relation(assistant)
        if relation > 0:
            plays = plays * relation // 100
        if int(target.talent.get(24, 0)):
            plays -= 1
        if int(assistant.talent.get(24, 0)):
            plays -= 1
        if int(target.talent.get(27, 0)):
            plays -= 1
        if int(assistant.talent.get(27, 0)):
            plays -= 1
        if int(target.talent.get(81, 0)):
            plays += 2
        if int(assistant.talent.get(81, 0)):
            plays += 2
        if int(target.talent.get(76, 0)):
            plays += 1
        if int(assistant.talent.get(76, 0)):
            plays += 1
        if int(target.talent.get(70, 0)):
            plays += 1
        elif int(target.talent.get(71, 0)):
            plays -= 2
        if int(assistant.talent.get(70, 0)):
            plays += 1
        elif int(assistant.talent.get(71, 0)):
            plays -= 2
        return max(plays, 0)


    def _calculate_aftertrain_masturbation_count(self, target: Character, assistant: Optional[Character]) -> int:
        count = 0
        level = int(target.abl.get(31, 0))
        if level == 1:
            count += 1
        elif level == 2:
            count += 2
        elif level == 3:
            count += 4
        elif level == 4:
            count += 6
        elif level == 5:
            count += 9
        elif level >= 6:
            count += 14
        if int(target.talent.get(60, 0)) and int(target.abl.get(11, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if assistant is not None and int(assistant.talent.get(118, 0)) and int(target.abl.get(11, 0)) >= 4 and self._get_palam_level(target.palam.get(5, 0)) >= 3:
            count += 1
        if int(target.abl.get(11, 0)) >= 5 and int(target.abl.get(17, 0)) >= 4 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.abl.get(11, 0)) >= 4 and int(target.abl.get(17, 0)) >= 3 and self._get_palam_level(target.palam.get(5, 0)) >= 4:
            count += 1
        if int(target.talent.get(74, 0)):
            count = int(count * 1.5)
        if assistant is not None and int(assistant.talent.get(118, 0)):
            count = int(count * 1.2)
        if int(target.talent.get(17, 0)):
            count += 1
        if int(target.talent.get(33, 0)):
            count += 1
        if int(target.talent.get(15, 0)):
            count -= 1
        if int(target.talent.get(20, 0)):
            count -= 1
        if int(target.talent.get(32, 0)):
            count -= 1
        if int(target.talent.get(70, 0)):
            count += 1
        elif int(target.talent.get(71, 0)):
            count -= 2
        if int(target.talent.get(76, 0)):
            count += 1
        return max(count, 0)


    def _calculate_com_order_base(self, target: Character) -> int:
        """计算执行判定基础分数"""
        score = 0
        
        # 顺从 (ABL:10)
        abl_10 = target.abl.get(10, 0)
        score += abl_10 * 10
        
        # 快乐刻印 (MARK:1)
        mark_1 = target.mark.get(1, 0)
        score += mark_1 * 5
        
        # 屈从刻印 (MARK:2)
        mark_2 = target.mark.get(2, 0)
        score += mark_2 * 10
        
        return score


    def _capture_train_video_after_command(self, target: Character, command_id: int, player: Optional[Character]) -> None:
        if not self._is_train_video_recording(target):
            return
        video_max = 10 + 4 * int(target.cflag.get(499, 0))
        frame_count = int(target.cflag.get(491, 0))
        if frame_count <= 0:
            target.cflag[491] = 1
            return
        if frame_count > video_max:
            self._stop_train_video_recording(target, player)
            return
        self._store_train_video_frame(target, frame_count - 1, command_id)
        target.cflag[491] = frame_count + 1
        if int(target.abl.get(17, 0)) >= 2 and frame_count > 1:
            target.exp[70] = int(target.exp.get(70, 0)) + 1
            print("拍摄经验＋１")


    def _char_body_generate(self, char: Character) -> None:
        """身体数据生成"""
        # 年龄
        char.cflag[600] = random.randint(18, 35)
        # 身高 (cm)
        if char.talent.get(100, 0):  # 娇小
            char.cflag[601] = random.randint(140, 155)
        elif char.talent.get(99, 0):  # 魁梧
            char.cflag[601] = random.randint(170, 190)
        else:
            char.cflag[601] = random.randint(155, 175)
        # 体重 (kg)
        char.cflag[602] = int(char.cflag[601] * 0.4 + random.randint(-5, 5))


    def _chara_make_full(self, char_idx: int, personality: int = 0, race: int = 0) -> None:
        """完整的角色创建流程 (对应 @CHARA_MAKE)"""
        char = self.interpreter.vars.chars[char_idx]
        
        # 性别设定 (CM_GENDER)
        self._cm_gender(char)
        
        # Level 和经验值设定
        char.cflag[9] = 1   # 等级
        char.exp[80] = 0    # 经验值
        
        # 家族初始化
        char.cflag[605] = 0
        
        # 卖春积极性
        char.cflag[120] = 1
        
        # 检查是否精英或后代
        is_elite = char.talent.get(220, 0) == 1
        is_descendant = char.talent.get(2, 0) == 1  # EX_TALENT:2
        
        if not is_elite and not is_descendant:
            # 侵攻楼层设定 (CM_STP)
            self._cm_stp(char)
            # 职业基础设定 (CM_BASE)
            self._cm_base(char)
            # 勇者初始等级 (CM_ST)
            self._cm_st(char)
        elif not is_descendant:
            # 精英部下
            char.cflag[1] = 0
            self._cm_base(char)
            self._cm_st_ace(char)
        else:
            # 后代
            char.cflag[1] = 0
            self._cm_base(char)
        
        # 口上性格 (CM_KJ)
        char_no = char.no
        if 1 <= char_no <= 16 or 200 <= char_no <= 211:
            self._cm_kj(char, personality)
        
        # 初心者的烙印
        day = self.interpreter.vars.day[0]
        if day <= 60:
            char.talent[291] = 1
        
        # 处女设定 (CM_VIRGIN)
        self._cm_virgin(char, is_descendant)
        
        # 素质设定 (CM_TALENT)
        self._cm_talent(char)
        
        # 战术技能 (CM_SKILL)
        self._cm_skill(char)
        
        # 外貌设定 (CM_LOOK)
        self._cm_look(char, race)
        
        # 善恶值 (CM_KIND)
        self._cm_kind(char, is_elite)
        
        # 家族设定
        if random.randint(0, 3) == 0 and not is_descendant:
            self._family_register(char_idx)
        
        # 家族素质继承 (CM_FAMILY_TALENT)
        self._cm_family_talent(char, char_idx)
        
        # 服装设定 (CM_CLOTH)
        self._cm_cloth(char)
        
        # 身体数据设定
        if self._get_flag_bit(5, 12) or self._get_flag_bit(5, 15):
            self._char_body_generate(char)


    # =========================================================================
    # SELF_CALL (称呼系统)
    # =========================================================================


    # ========================================
    # NAMING - 命名系统
    # 对应 ERB/NAMING.ERB → CHARA_NAME_EDIT.ERB
    # ========================================


    def _childbirth(self, target) -> List[str]:
        """出産处理 - 对应 @CHILDBIRTH"""
        messages: List[str] = []
        messages.append(f"{target.savestr}生下了孩子。")
        target.cflag[110] = 0
        target.cflag[111] = 1
        return messages


    def _cleanup_invalid_marriage_links(self) -> List[str]:
        messages: List[str] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            marriage_state = int(char.cflag.get(601, 0))
            if marriage_state <= 902:
                continue
            partner_pair = self._resolve_character_marriage_partner(idx, char)
            if partner_pair is None:
                char.cflag[601] = 0
                char.cflag[602] = 0
                char.cflag[609] = 0
                messages.append(f"{char.name} 的婚姻关系因为对象消失而结束了。")
                continue
            partner_idx, partner = partner_pair
            expected = int(self._get_character_identity_token(idx, char) + 9)
            if int(partner.cflag.get(601, 0)) != expected:
                char.cflag[601] = 0
                char.cflag[602] = 0
                char.cflag[609] = 0
                messages.append(f"{char.name} 的婚姻关系已经失效，记录被整理掉了。")
                continue
            char.cflag[609] = int(partner.cflag.get(6, 0))
        return messages


    def _collect_night_stalking_candidates(self) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if self._can_trigger_night_stalking(idx, char):
                candidates.append((idx, char))
        return candidates


    def _collect_selectable_item_targets(self, allow_master: bool = True) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if self._can_select_item_target(idx, char, allow_master=allow_master) is not None:
                continue
            candidates.append((idx, char))
        return candidates


    def _collect_turn_end_early_messages(self, new_day: bool) -> List[str]:
        messages: List[str] = []
        messages.extend(self._apply_turn_end_special_skill_checks())
        return messages


    def _compute_equip_stats(self, equip_code: int, is_weapon: bool, target: Character) -> Dict[str, Any]:
        """Compute stats for a single equipment item.
        Corresponds to ERB @EQUIP_DATABASE + @EQUIP_POWERUP.
        """
        base_code, enhance, prefix = self._decode_equipment_code(equip_code)
        result: Dict[str, Any] = {}

        if is_weapon:
            db = self._EQUIP_WEAPON_DATABASE.get(base_code, {})
            if not db:
                return result
            result["damage"] = db.get("damage", 100)
            result["miss"] = db.get("miss", 0)
            result["spirit_recover"] = db.get("spirit_recover", 0)
            result["combo"] = db.get("combo", 0)
            result["def_dmg"] = db.get("def_dmg", 100)
            result["spirit_dmg"] = db.get("spirit_dmg", 100)
            result["cursed"] = False
            result["special"] = 0

            # Prefix enchantments
            self._apply_prefix_effects(result, prefix)

            # Enhancement bonus
            result["damage"] += enhance * 5

            # Talent-based powerups
            self._apply_equip_powerup(result, target)
        else:
            db = self._EQUIP_RING_DATABASE.get(base_code, {})
            if not db:
                return result
            result["effect"] = db.get("effect", 0)
            result["strength"] = enhance
            result["cursed"] = db.get("cursed", False)
            result["special"] = db.get("special", 0)
            result["damage"] = 0
            result["miss"] = 0
            result["spirit_recover"] = 0
            result["combo"] = 0
            result["def_dmg"] = 100
            result["spirit_dmg"] = 100

            # Ring effects that affect combat
            effect = result["effect"]
            if effect == 1:  # 伤害增加
                result["damage"] = enhance * 10
            elif effect == 7:  # 攻击变动
                result["damage"] = enhance * 5
            elif effect == 8:  # 防御变动
                result["def_dmg"] = 100 + enhance * 5
            elif effect == 3:  # 速度UP
                result["combo"] = enhance * 5
            elif effect == 5:  # 气力回复
                result["spirit_recover"] = enhance * 5
            elif effect == 11:  # 装备劣化
                result["cursed"] = True
            elif effect == 13:  # HP·气力减少
                result["spirit_recover"] = -enhance * 5
            elif effect == 14:  # 攻击·防御减少
                result["damage"] = -enhance * 5
                result["def_dmg"] = max(0, 100 - enhance * 5)

            # Special flags from special field
            special = result["special"]
            result["poison"] = bool(special & 1)
            result["fire"] = bool(special & 2)
            result["ice"] = bool(special & 4)
            result["thunder"] = bool(special & 8)

        return result


    def _comseq_register(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars

        messages.append("调教菜单登录")
        messages.append("-" * 40)

        menu_len = int(v.flags.get(550, 0))
        registered = []
        for i in range(menu_len):
            com_id = int(v.flags.get(551 + i, 0))
            com_name = self.train_commands.get(com_id, f"指令{com_id}")
            registered.append(com_name)

        if registered:
            messages.append(f"已登录指令：{' → '.join(registered)}")
        else:
            messages.append("已登录指令：（无）")

        messages.append("-" * 40)
        messages.append("选择指令编号进行注册")
        messages.append("[998] 重置菜单")
        messages.append("[999] 重复指令")
        messages.append("[1000] 保存并返回")
        return messages


    def _comseq_show(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars

        menu_len = int(v.flags.get(550, 0))
        registered = []
        for i in range(menu_len):
            com_id = int(v.flags.get(551 + i, 0))
            com_name = self.train_commands.get(com_id, f"指令{com_id}")
            registered.append(com_name)

        if registered:
            messages.append(f"已登录指令：{' → '.join(registered)}")
        else:
            messages.append("已登录指令：（无）")

        return messages


    def _comseq_train(self) -> List[str]:
        messages: List[str] = []
        v = self.interpreter.vars

        messages.append("-" * 40)
        messages.extend(self._comseq_show())
        messages.append("-" * 40)
        messages.append("开始自动执行调教指令")

        menu_len = int(v.flags.get(550, 0))
        v.tflag[224] = 555

        can_execute = True
        for i in range(menu_len):
            com_id = int(v.flags.get(551 + i, 0))
            if not self._multi_comable(com_id):
                can_execute = False
                break

        if can_execute and menu_len > 0:
            for i in range(menu_len):
                com_id = int(v.flags.get(551 + i, 0))
                messages.append(f"执行指令：{self.train_commands.get(com_id, f'指令{com_id}')}")
        else:
            v.tflag[224] = 0
            messages.append("所登录的指令目前无法实行")

        v.tflag[224] = 0
        return messages


    def _confirm_catalog_item_purchase(self, item_name: str) -> bool:
        print(f"\n确定购买{item_name}？")
        print(" [0] 好的")
        print(" [1] 不要")
        while True:
            choice = self._prompt_choice()
            if choice == "0":
                return True
            if choice == "1":
                return False
            self._show_invalid_selection()


    def _confirm_reincarnation_choice(self, target: Character, candidate: Dict[str, Any]) -> bool:
        print(f"\n确定要将 {target.name} 转生为 {candidate['name']} 吗？")
        print(" [0] 确定")
        print(" [1] 取消")
        confirm = self._prompt_choice()
        return confirm == "0"


    def _consume_juel(self, idx: int, value: int) -> bool:
        current = self._get_juel(idx)
        if value > current:
            return False
        self.interpreter.vars.juel[idx] = current - int(value)
        return True


    def _consume_medals(self, amount: int) -> bool:
        if amount <= 0:
            return True
        player = self._get_player()
        if player is None:
            return False
        current = max(0, int(player.exp.get(81, 0)))
        if current < amount:
            return False
        player.exp[81] = current - amount
        return True


    def _count_standby_withdrawal_supporters(self) -> int:
        supporters = 0
        for char in self.interpreter.vars.chars[1:]:
            if int(char.cflag.get(1, 0)) != 0:
                continue
            if int(char.talent.get(117, 0)) or int(char.talent.get(63, 0)):
                supporters += 1
        return supporters


    def _count_training_orgasm_channels(self, source: Dict[int, int]) -> int:
        count = 0
        for source_id in (0, 1, 2, 14, 15):
            if int(source.get(source_id, 0)) >= 10000:
                count += 1
        return count


    # ========================================
    # COM0: 爱抚 (对应 ERB COMF0_愛撫.ERB)
    # ========================================


    def _curse_equip_ring(self) -> List[str]:
        """指輪と召喚 - 对应 @CURSE_EQUIP_RING"""
        messages: List[str] = []
        return messages


    def _customize_life_cradle_first_history(self, target: Character) -> tuple[bool, str]:
        self._clear_life_cradle_first_history(target)
        ok, _ = self._select_life_cradle_first_kiss(target)
        if not ok:
            return False, "已取消。"
        ok, _ = self._select_life_cradle_first_experience(target)
        if not ok:
            return False, "已取消。"
        print("\n" + self._summarize_life_cradle_first_kiss(target))
        print(self._summarize_life_cradle_first_experience(target))
        print("这样就可以了吗？")
        print(" [0] 好的")
        print(" [1] 还是改一下吧")
        confirm = self._prompt_choice()
        if confirm == "1":
            return self._customize_life_cradle_first_history(target)
        if confirm != "0":
            return False, "已取消。"
        return True, "初始经历设定完成。"


    def _customize_life_cradle_looks(self, target: Character) -> tuple[bool, str]:
        pages = self._get_life_cradle_look_pages()
        page_index = 0
        while True:
            price = self._get_chara_cost_value(target)
            for line in self._build_life_cradle_look_page_lines(target, page_index, price):
                print(line)
            choice = self._prompt_choice()
            if choice == "998":
                page_index = min(page_index + 1, len(pages) - 1)
                continue
            if choice == "997":
                page_index = max(page_index - 1, 0)
                continue
            if choice == "996":
                return False, "已取消。"
            if choice == "999":
                return True, "外观设定完成。"
            try:
                field_id = int(choice)
            except ValueError:
                print("\n无效值")
                self._pause()
                continue
            ok, message = self._apply_life_cradle_look_field(target, field_id)
            print(f"\n{message}")
            self._pause()


    def _customize_life_cradle_talents(self, target: Character) -> tuple[bool, str]:
        pages = self._get_life_cradle_talent_pages()
        page_index = 0
        while True:
            price = self._get_chara_cost_value(target)
            for line in self._build_life_cradle_page_lines(target, page_index, price):
                print(line)
            outcome = self._handle_life_cradle_talent_choice(target, page_index)
            if outcome is None:
                continue
            if outcome == -1:
                page_index = min(page_index + 1, len(pages) - 1)
                continue
            if outcome == -2:
                page_index = max(page_index - 1, 0)
                continue
            if outcome == -3:
                return False, "已取消。"
            if outcome == -4:
                valid, messages = self._validate_life_cradle_talents(target)
                if not valid:
                    print()
                    for message in messages:
                        print(message)
                    self._pause()
                    continue
                return True, "人物设定完成。"
            _, message = self._apply_life_cradle_talent_toggle(target, outcome)
            print(f"\n{message}")
            self._pause()


    def _data_fix(self) -> None:
        self._apply_data_fix()

    # =====================================================================
    # ENDINGDATA (结局数据系统)
    # Corresponds to ERB ENDINGDATA.ERB, ENDINGDATA_ADDON1.ERB
    # =====================================================================


    def _death_check(self, target: Character) -> Tuple[bool, List[str]]:
        """死亡检查 - 对应 @CHARADEAD_CHECK"""
        messages: List[str] = []
        v = self.interpreter.vars
        player = self._get_player()

        if target is None:
            return False, messages

        if int(target.base.get(0, 0)) > 0:
            return False, messages

        if int(v.get_flag(35, 0)):
            if int(target.base.get(0, 0)) < 1:
                target.base[0] = 1
            return False, messages

        target_idx = -1
        for i, c in enumerate(v.chars):
            if c is target:
                target_idx = i
                break

        target_name = getattr(target, 'savestr', str(target_idx))
        player_name = getattr(player, 'savestr', "主人") if player else "主人"

        if target_idx == 0:
            ex_flag_3 = 0
            if hasattr(v, 'ex_flag'):
                ex_flag_3 = int(v.ex_flag.get(3, 0))
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
                    replacement_name = getattr(v.chars[ex_flag_3], 'savestr', "")
                assistant = self._get_assistant()
                mao_idx = -1
                for i, c in enumerate(v.chars):
                    if hasattr(c, 'no') and int(c.no) == 17:
                        mao_idx = i
                        break
                is_mao = (ex_flag_3 == mao_idx)
                is_player = (ex_flag_3 == 0)
                is_assi = (assistant is not None and ex_flag_3 == self._find_char_index_for(assistant))

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

        tflag = getattr(v, 'tflag', {})
        tflag[13] = 999

        messages.append("")
        messages.append("─" * 50)
        messages.append("")
        if target_idx == 0:
            messages.append(f"{target_name}死掉了……")
        else:
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


    def _decide_ablup11(self, target: Character) -> tuple[bool, int]:
        return self._decide_ntr_desire_upgrade(target)


    def _decide_ablup2(self, target: Character) -> tuple[bool, int]:
        return self._decide_ntr_private_sense_upgrade(target)


    def _decide_ablup3(self, target: Character) -> tuple[bool, int]:
        return self._decide_ntr_anal_sense_upgrade(target)


    def _decode_equipment_code(self, equip_code: int) -> tuple[int, int, int]:
        base_code = equip_code % 1000
        enhance = (equip_code % 100000) // 1000
        prefix = equip_code // 100000
        return base_code, enhance, prefix


    def _discard_chastity_key(self, target: Character) -> tuple[bool, str]:
        if not self._can_discard_chastity_key(target):
            return False, "当前不能丢弃这名角色贞操带的钥匙。"
        print(f"\n{target.name} 贞操带的钥匙一旦丢掉，就再也无法打开了。")
        print(" [0] 丢掉钥匙")
        print(" [1] 取消")
        choice = self._prompt_choice()
        if choice != "0":
            return False, "取消了丢弃钥匙。"
        target.cflag[49] = 1
        return True, f"{target.name} 的贞操带钥匙被彻底丢弃了。"


    def _divorce_character(self, idx: int, char: Character) -> tuple[bool, str]:
        if int(char.cflag.get(601, 0)) == 0:
            return False, f"{char.name} 当前并没有结婚。"
        marriage_state = int(char.cflag.get(601, 0))
        if marriage_state == 902:
            partner_pair = self._resolve_dungeon_town_lover_partner(idx, char)
            if partner_pair is not None:
                partner = partner_pair[1]
                partner.cflag[601] = 0
                partner.cflag[602] = 0
            self._clear_character_lover_relation(idx, char)
        elif marriage_state > 902:
            partner_pair = self._resolve_character_marriage_partner(idx, char)
            if partner_pair is not None:
                partner = partner_pair[1]
                partner.cflag[601] = 0
                partner.cflag[602] = 0
                partner.cflag[609] = 0
        char.cflag[601] = 0
        char.cflag[602] = 0
        char.cflag[609] = 0
        return True, f"{char.name} 离婚了。"


    def _drain_post_message_actions(self):
        pending = self._get_pending_post_message_actions()
        while pending:
            action = pending.pop(0)
            kind = str(action.get("kind", ""))
            handler_name = POST_MESSAGE_ACTION_KIND_METHODS.get(kind)
            if handler_name is None:
                continue
            handler = getattr(self, handler_name, None)
            if handler is not None:
                handler(action)


    def _edit_character_name(self, char_idx: int, new_name: str, name_type: str = "name") -> Dict[str, Any]:
        """角色命名 - 对应 @CHARA_NAME_EDIT
        name_type: "name"=名称, "callname"=呼称, "nickname"=绰号
        """
        v = self.interpreter.vars
        if char_idx < 0 or char_idx >= len(v.chars):
            return {'success': False, 'message': "无效角色"}

        char = v.chars[char_idx]
        old_name = ""

        if name_type == "name":
            old_name = char.savestr
            char.savestr = new_name
            char.name = new_name
        elif name_type == "callname":
            old_name = char.callname or ""
            char.callname = new_name
        elif name_type == "nickname":
            old_name = char.nickname or ""
            char.nickname = new_name
        else:
            return {'success': False, 'message': "无效命名类型"}

        return {
            'success': True,
            'message': f"名称变更：{old_name} → {new_name}",
            'old_name': old_name,
            'new_name': new_name,
        }


    def _emit_aftertrain_separator(self) -> None:
        print("-" * 50)


    def _encode_equipment_code(self, base_code: int, enhance: int = 0, prefix: int = 0) -> int:
        return base_code + enhance * 1000 + prefix * 100000


    def _enter_lover(self, char_idx: int, lover_type: int) -> List[str]:
        """恋人派遣 - 对应 @ENTER_LOVER

        为指定勇者派遣恋人，设置恋人类型并重置爱情度。

        Args:
            char_idx: 角色索引
            lover_type: 恋人类型ID (1-84为NPC恋人, 200为角色间恋爱, 0为不派遣)

        Returns:
            事件消息列表
        """
        messages: List[str] = []
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"

        # 获取当前恋人
        old_lover = char.cflag.get(606, 0)

        # 设置新恋人
        char.cflag[606] = lover_type

        # 爱情度重置（恋人变更时）
        if lover_type != old_lover:
            char.cflag[607] = 0

        if lover_type > 0:
            lover_name = self._name_lover(lover_type)
            messages.append(f"{char_name}为目标{lover_name}开始接触邂逅了")
        else:
            messages.append(f"引诱{char_name}的行动正在进行中")

        return messages


    def _equip_ring_to_slot(self, target: Character, slot_flag: int, item_id: int) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "当前没有魔王角色。"
        if not self._is_item_owned(player, item_id):
            return False, "没有这件装备。"
        enhance = self._choose_equipment_enhancement()
        if enhance is None:
            return False, "已取消。"
        cost = enhance * 10000
        if self.interpreter.vars.money < cost:
            return False, "钱不够！！"
        current_code = int(target.cflag.get(slot_flag, -1))
        if current_code >= 0:
            self._return_equipment_item(player, self._get_ring_item_id_from_code(current_code))
        self._use_item(player, self._get_item_name(item_id), 1)
        self._spend_global_money(cost)
        target.cflag[slot_flag] = self._encode_equipment_code(item_id - 300, enhance, 0)
        return True, f"{target.name} 装备了{self._get_equipment_ring_name(target.cflag[slot_flag])}。"


    def _equip_weapon_to_slot(self, target: Character, item_id: int, source_item_id: Optional[int] = None) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "当前没有魔王角色。"
        inventory_item_id = item_id if source_item_id is None else source_item_id
        if not self._is_item_owned(player, inventory_item_id):
            return False, "没有这件武器。"
        enhance = self._choose_equipment_enhancement()
        if enhance is None:
            return False, "已取消。"
        cost = enhance * 10000
        if self.interpreter.vars.money < cost:
            return False, "钱不够！！"
        prefix = self._choose_weapon_prefix()
        if prefix is None:
            return False, "已取消。"
        current_code = int(target.cflag.get(550, -1))
        if current_code >= 0:
            self._return_equipment_item(player, self._get_weapon_item_id_from_code(current_code))
        self._use_item(player, self._get_item_name(inventory_item_id), 1)
        self._spend_global_money(cost)
        target.cflag[550] = self._encode_equipment_code(item_id - 300, enhance, prefix)
        return True, f"{target.name} 装备了{self._get_equipment_weapon_name(target.cflag[550])}。"


    def _event1(self) -> List[str]:
        """一般事件处理 - EVENT1.ERB"""
        output = []
        target = self.characters.get(self.vars.flag.get(1, -1))
        if target is None:
            return output
        if int(target.cflag.get(100, 0)):
            return output
        exp0 = int(target.exp.get(0, 0))
        exp1 = int(target.exp.get(1, 0))
        if exp0 == 0 and exp1 > 0 and int(target.talent.get(30, 0)):
            target.cflag[100] = 1
            output.append("（能守住贞操的话，稍微被进攻一下后面，也不是不能接受）")
        return output

    # ------------------------------------------------------------------
    # EXCOM_PROCESS - 扩展指令处理
    # ------------------------------------------------------------------


    def _execute_character(self, target: Character, method: int) -> List[str]:
        """Execute a character with the selected method.
        method: 0=流放, 1=公开处刑, 2=博物馆, 3=猎奇, 4=肉便器, 5=士兵化, 6=固定示众, 7=消除记忆释放
        """
        messages: List[str] = []
        master_name = self._get_player().name if self._get_player() else "魔王"
        target_name = target.name
        is_favorite = int(target.cflag.get(700, 0)) != 0

        # Methods 0-4: favorites cannot be executed
        if method in (0, 1, 2, 3, 4) and is_favorite:
            messages.append(f"{target_name}在收藏列表之中，不能被处刑。")
            return messages

        # Method 5: check for 不受洗脑 (talent 17-40 range check via NO)
        if method == 5:
            template_id = target.template_id
            if template_id is not None and 17 <= template_id <= 40:
                messages.append(f"{target_name}拥有【不受洗脑】，无法进行士兵化洗脑。")
                return messages

        if method == 0:
            # 流放出地下城
            messages.append(f"{master_name}把{target_name}从地下城里永久驱逐了。")
            # Remove character
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 1:
            # 公开处刑
            messages.append(f"{master_name}把{target_name}公开处刑了。")
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 2:
            # 博物馆展品
            messages.append(f"{target_name}被带到了工作室……")
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 3:
            # 施行猎奇向处刑 -> calls grotesque
            messages.append(f"{master_name}决定让{target_name}品尝真正的痛苦…")
            messages.append("　　　　　　　　　　< ※ 注 意 ！ ※ >")
            messages.append("（之后将发生非常黄暴的事！！）")
            # The grotesque sub-menu should be called separately by the caller

        elif method == 4:
            # 做成肉便器
            flag_83 = int(self.interpreter.vars.get_flag(83, 0))
            self.interpreter.vars.set_flag(83, flag_83 + 1)

            # Prestige adjustment
            if target.talent.get(220, 0) != 1 and self._get_character_ex_talent(target, 1) != 1:
                self._add_prestige_value(2)
                messages.append("威望值增加")
            else:
                self._add_prestige_value(-10)
                messages.append("威望值减少")

            # 爱慕 (talent 85)
            if target.talent.get(85, 0):
                messages.append(f"深爱着你的{target_name}不知道自己为什么要被做成肉便器，不停地高叫着你的名字，请求饶恕。")
            messages.append(f"但{master_name}依然给{target_name}烙上了封锁所有力量的封印，")
            messages.append("被吸收了全部力量的她，身体变成淫靡的肉块了。")
            messages.append("作为地下城里怪物的慰问品被使用着，")
            messages.append("今后别说重新当勇者，就连看一眼阳光也不可能了吧。")

            # 精灵族 (原种族 talent)
            if int(target.talent.get(0, 0)) == 1:
                messages.append(f"精灵族的{target_name}在丑陋的兽人中广受好评。")
            # 精液中毒 (ABL:32) or 擅用舌头 (talent)
            if int(target.abl.get(32, 0)) > 0 or target.talent.get(0, 0):
                messages.append(f"{target_name}作为精液便器，每天都心怀欢喜地把精液喝光了。")
            # 百合中毒 (ABL:33) or 百合气质 (ABL:22)
            if int(target.abl.get(33, 0)) > 0 or int(target.abl.get(22, 0)) > 2:
                messages.append(f"作为女子便器的{target_name}获得了很高的评价。阴部、肛门有污垢也毫不在意，老老实实地把她们舔高潮了。")
            # 抖M气质 (ABL:21)
            if int(target.abl.get(21, 0)) > 0:
                messages.append(f"沐浴在骂声中的{target_name}腿间开始湿润，脸上浮现起恍惚的笑容。")
            # 露出癖 (ABL:17)
            if int(target.abl.get(17, 0)) > 0:
                messages.append(f"{target_name}在地下城的大街上展露痴态。不管是不是怪物，对所有路过的客人，均热情献媚。")
            # 侍奉精神 (ABL:16)
            if int(target.abl.get(16, 0)) > 0:
                messages.append(f"完全崩坏了的{target_name}连自我都失去了，只有在侍奉肉棒时能感觉到喜悦。")
            # V感覚 (ABL:2)
            if int(target.abl.get(2, 0)) > 3:
                messages.append(f"被数之不尽的阴茎抽插，{target_name}的私处完全扩张，失去弹性了。最近的对象，全是巨魔和马这样有巨根的。")
            # A感覚 (ABL:3)
            if int(target.abl.get(3, 0)) > 3:
                messages.append(f"已经算不上是性器官，{target_name}的肛门，被极限扩张，关都关不上了。可是哪怕这样，只要有肉棒在直肠射精，她还是兴奋得快疯了似得。")
            # 爱慕 (talent 85)
            if target.talent.get(85, 0):
                messages.append(f"{target_name}把所有的阴茎都幻想成深爱的你的阴茎的模样。")
            # V敏感(talent 104)・淫壺(talent 232)
            if target.talent.get(104, 0) or target.talent.get(232, 0):
                messages.append(f"{target_name}对被什么东西插入并不在意，用卑微的话语哀求着打种。")
            # A敏感(talent 106)・淫肛(talent 233)
            if target.talent.get(106, 0) or target.talent.get(233, 0):
                messages.append(f"{target_name}的肛门特别有感觉，恶魔们特意把她的肛门改造成能怀孕的样子。")
            # C敏感(talent 102)・淫核(talent 230)
            if target.talent.get(102, 0) or target.talent.get(230, 0):
                messages.append(f"{target_name}的阴蒂又大又肿，一鞭子下去，她就爱液四射，口水横流地绝顶了。")
            # B敏感(talent 108)・淫乳(talent 231)
            if target.talent.get(108, 0) or target.talent.get(231, 0):
                messages.append(f"{target_name}的乳头被恶魔们改造过，现在可以插入乳头里性交了。")
            # 魔术(talent 241)・咒术(talent 250)
            if target.talent.get(241, 0) or target.talent.get(250, 0):
                messages.append(f"有魔力的{target_name}，头部完全被头罩包裹，强制地被削弱了魔力。")
            # 法术(talent 242)
            if target.talent.get(242, 0):
                messages.append(f"有神圣之力的{target_name}，被恶魔们强制肛交了无数次，完全堕落为恶魔的力量了。")

            # 扶她(talent 121) & 2+肉便器
            if target.talent.get(121, 0) and int(self.interpreter.vars.get_flag(83, 0)) >= 2:
                penis_type = int(target.talent.get(318, 0))
                if penis_type == 1:
                    # 巨根
                    messages.append(f"扶她巨根的{target_name}被改造成更大的阴茎，")
                    messages.append("奉命去侵犯其它的肉便器了。")
                elif penis_type == 2:
                    # 短小包茎
                    messages.append(f"扶她短小包茎的{target_name}为了发泄性欲压在其它肉便器身上。")
                    messages.append("但即使激烈地摆动腰身，也无法令对方满足。")
                elif penis_type == 3:
                    # 包茎
                    messages.append(f"扶她包茎的{target_name}哪怕洗澡，也不剥开包皮清洗里面的污垢。")
                    messages.append("而是让其它肉便器用口服侍清洁。")
                else:
                    # 普通
                    messages.append(f"扶她的{target_name}积极地侵犯着其它肉便器，")
                    messages.append("巨大的阴囊生产了大量的精液，射到周围都是。")

            # 魅力点(talent 312)
            charm_point = int(target.talent.get(312, 0))
            if charm_point == 12:
                messages.append("作为魅力点的美乳，现在变成一堆丑陋膨胀的肉块了。")
            elif charm_point == 14:
                messages.append("作为魅力点的臀部曲线，现在变成一团下流膨胀的肉块了。")
            elif charm_point == 21:
                messages.append("作为魅力点的性器，现在正变成奇怪的肉块。")
            elif charm_point == 22:
                messages.append("作为魅力点的光泽的头发，现在完全褪色了。")
            elif charm_point == 23:
                messages.append("作为魅力点的大屁股，现在变成了充满下流气息的成熟桃子。")

            # 故乡的恋人(talent 317==4)・憧憬的人(talent 317==11)
            if int(target.talent.get(317, 0)) == 4 or int(target.talent.get(317, 0)) == 11:
                messages.append(f"{target_name}双眼空虚，在重复着谁的名字。也许正在妄想和爱人拥抱吧。")

            messages.append(f"现在的肉便器数量：{self.interpreter.vars.get_flag(83, 0)}")

            # Remove character
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 5:
            # 士兵化
            target.talent[254] = 1
            messages.append(f"在{target_name}的身体上刻上了服从的刻印，")
            messages.append("只残留一点点的意识和记忆，")
            messages.append("命令其现在就去把勇者杀光。")
            target.cflag[13] = int(target.cflag.get(13, 0)) // 2
            target.cflag[14] = int(target.cflag.get(14, 0)) // 2
            messages.append("*法术的副作用导致其战斗力下降了*")
            # Remove character
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 6:
            # 固定示众
            target.cflag[1] = 8
            messages.append(f"把{target_name}的屁股抬高，扣在固定的枷锁上，")
            messages.append("任由怪物们发泄性欲，")
            if int(target.talent.get(9, 0)) == 1:
                messages.append("被玩坏了的奴隶，什么都意识不到，在痴笑着。")
            elif int(target.talent.get(76, 0)) == 1:
                messages.append("淫乱的奴隶，不如说，正在享受现在的样子。")
            else:
                messages.append("悲哀的奴隶，对今后将发生的制裁害怕极了。")
            # Remove character
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        elif method == 7:
            # 消除记忆后释放
            messages.append(f"{target_name}被清除了关于地下城的所有记忆，被丢到地下城外了。")
            messages.append(f"{target_name}再次开始了冒险……")
            # Reset invasion state
            target.cflag[501] = 1
            target.cflag[502] = 0
            target.cflag[1] = 2
            target.cflag[508] = 3
            # Restore karma partially
            if int(target.cflag.get(151, 0)) < -50:
                target.cflag[151] = -50
            # Lower favorability
            target.cflag[2] = 20
            # Remove character
            idx = self.interpreter.vars.chars.index(target)
            self._clear_execution_equipment(target)
            self._remove_character_at(idx)
            self._award_execution_absorption(target)
            level = int(target.cflag.get(9, 0))
            gain = (level + 1) * 50
            messages.append(f"《封印吸收了力量，使你获得了{gain}的经验值！》")

        return messages

    # =========================================================================
    # GROTESQUE (残酷处刑系统)
    # =========================================================================


    def _expire_shadow_servant(self, idx: int, char: Character) -> List[str]:
        messages = [f"{char.name} 消失在了光芒之中……"]
        char.cflag[9] = 1
        messages.extend(self._execute_character_mini_execution(idx, char, with_log=False))
        return messages


    def _extract_kojo_block_lines(self, content: str, marker: str) -> List[str]:
        start = content.find(marker)
        if start < 0:
            return []
        block_start = content.find("\n", start) + 1
        if block_start == 0:
            block_start = start + len(marker)
        end = len(content)
        next_label = content.find("\n@", block_start)
        if next_label > block_start:
            end = next_label
        block = content[block_start:end]
        lines: List[str] = []
        for raw_line in block.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(";") or stripped.startswith("@"):
                continue
            lines.append(stripped)
        return lines


    def _find_birth_father_character(self, mother: Character, father_source: int) -> Optional[Character]:
        father_name = str(mother.cstr.get(2, "")).strip()
        if father_source not in (2, 3) or not father_name:
            return None
        for char in self.interpreter.vars.chars[1:]:
            if char is mother:
                continue
            if char.name == father_name or char.callname == father_name:
                return char
        return None


    def _find_char_index_for(self, char: Character) -> int:
        """查找角色在列表中的索引"""
        v = self.interpreter.vars
        for i, c in enumerate(v.chars):
            if c is char:
                return i
        return -1


    def _finish_life_cradle_first_kiss(
        self,
        target: Character,
        site_code: int,
        partner_name: Optional[str] = None,
    ) -> tuple[bool, str]:
        self._apply_life_cradle_first_kiss(target, site_code, partner_name)
        return True, self._summarize_life_cradle_first_kiss(target)


    def _gain_next_special_sex_talent(self, target: Character) -> List[str]:
        if int(target.talent.get(74, 0)) == 0 and int(target.abl.get(0, 0)) >= 4 and int(target.exp.get(11, 0)) >= 100 and int(target.exp.get(2, 0)) >= 100:
            target.talent[74] = 1
            organ_name = "阴茎" if int(target.talent.get(121, 0)) != 0 or int(target.talent.get(122, 0)) != 0 else "阴蒂"
            return [
                f"总觉得最近，{target.name}连呼吸都变得色情了起来……",
                f"调教结束之后，{target.name}当着你的面，肆无忌惮地继续玩弄着自己的{organ_name}。",
                f"{target.name} 获得了【{self._get_talent_name(74)}】。",
            ]
        if int(target.talent.get(75, 0)) == 0 and int(target.abl.get(2, 0)) >= 4 and int(target.exp.get(0, 0)) >= 300 and int(target.exp.get(2, 0)) >= 100:
            target.talent[75] = 1
            return [
                f"{target.name} 最近对私处的运用，越来越炉火纯青……",
                f"调教结束之后，{target.name}依依不舍地抱着你，恳求着欢好。",
                f"{target.name} 获得了【{self._get_talent_name(75)}】。",
            ]
        if int(target.talent.get(122, 0)) != 0 and int(target.abl.get(0, 0)) >= 4 and int(target.exp.get(5, 0)) >= 300 and int(target.exp.get(2, 0)) >= 100 and int(target.talent.get(75, 0)) == 0 and int(target.talent.get(74, 0)) == 0:
            target.talent[75] = 1
            return [
                f"{target.name} 最近对性器的运用，越来越炉火纯青……",
                f"调教结束之后，{target.name}依依不舍地抱着你，恳求着欢好。",
                f"{target.name} 获得了【{self._get_talent_name(75)}】。",
            ]
        if int(target.talent.get(77, 0)) == 0 and int(target.abl.get(3, 0)) >= 4 and int(target.exp.get(32, 0)) >= 300 and int(target.exp.get(2, 0)) >= 100:
            target.talent[77] = 1
            return [
                f"{target.name} 最近好像学会了控制直肠的蠕动……",
                f"调教结束之后，{target.name}一边摆弄自己的肛门，一边用勾引的眼神目送你。",
                f"{target.name} 获得了【{self._get_talent_name(77)}】。",
            ]
        if int(target.talent.get(78, 0)) == 0 and int(target.talent.get(122, 0)) == 0 and int(target.abl.get(1, 0)) >= 4 and int(target.exp.get(54, 0)) >= 100 and int(target.exp.get(2, 0)) >= 100:
            target.talent[78] = 1
            return [
                f"最近，总觉得{target.name}的胸部，好像有着神奇的引力一般……",
                f"调教结束之后，{target.name}用尖立的乳头直直地对着你，眼里充满了勾人的销魂神色。",
                f"{target.name} 获得了【{self._get_talent_name(78)}】。",
            ]
        if int(target.talent.get(78, 0)) == 0 and int(target.talent.get(122, 0)) != 0 and int(target.abl.get(1, 0)) >= 4 and int(target.juel.get(14, 0)) >= 100 and int(target.exp.get(2, 0)) >= 100:
            target.talent[78] = 1
            return [
                f"最近，{target.name}总觉得胸部越发敏感……",
                f"调教结束之后，{target.name}用尖立的乳头直直地对着你，眼里充满了渴望。",
                f"{target.name} 获得了【{self._get_talent_name(78)}】。",
            ]
        return []


    # ========================================
    # FUNC_CLOTH - 服装函数系统
    # 对应 ERB/FUNC_CLOTH.ERB
    # ========================================

    _CLOTH_NAMES = {
        0: "全裸",
        1: "内衣",
        2: "女仆装",
        3: "护士服",
        4: "水手服",
        5: "旗袍",
        6: "兔女郎装",
        7: "修女服",
        8: "巫女服",
        9: "女骑士铠甲",
        10: "魔女服",
        11: "舞娘装",
        12: "泳装",
        13: "浴衣",
        14: "晚礼服",
        15: "女学生制服",
        16: "SM拘束服",
        17: "触手服",
        18: "宠物装",
        19: "女王装",
        20: "魔界军服",
        21: "神官服",
        22: "盗贼服",
        23: "魔法师袍",
        24: "战士铠甲",
        25: "弓手服",
        26: "忍者服",
        27: "吟游诗人服",
        28: "商人服",
        29: "厨师服",
        30: "奴隶项圈",
        31: "贞操带",
        32: "眼罩",
        33: "口球",
        34: "绳索",
        35: "拘束衣",
        36: "项圈+锁链",
        37: "乳头夹",
        38: "阴蒂夹",
        39: "振动棒",
        40: "肛门塞",
        41: "拉链拘束",
        42: "木马",
        43: "十字架",
        44: "铁笼",
        45: "公开处刑台",
        46: "宠物犬装",
        47: "家畜装",
        48: "便器装",
        49: "展示台",
    }


    # ========================================
    # MAOUNET - 魔王网通信系统
    # 对应 ERB/MAOUNET.ERB
    # ========================================


    # =========================================================================
    # System 1: EXCOM (EX素质系统)
    # Based on ERB/EXCOM.ERB
    # =========================================================================

    _EX_TALENT_NAMES = {
        0: "灵魂错位",
        1: "近卫",
        2: "后代",
        3: "魔王替身",
        4: "狂王替身",
        101: "琼",
        102: "普林希斯",
        103: "嘉德",
        104: "菲娅",
        200: "魔王",
        801: "无双",
        901: "一人军团",
        902: "魔女",
        903: "魔界公主",
        904: "天神",
    }


    def _has_assistable_candidates(self, exclude_idx: Optional[int] = None) -> bool:
        for idx, char in enumerate(self.interpreter.vars.chars):
            if exclude_idx is not None and idx == exclude_idx:
                continue
            if self._can_select_standby_slave(idx, char) is None:
                return True
        return False


    def _has_character_template(self, template_id: int) -> bool:
        return self._get_character_template_baseline(int(template_id)) is not None


    def _has_onesho_catheter_setup(self, char: Character, clothes_enabled: bool) -> bool:
        accessory_id = int(char.cflag.get(42, 0))
        cloth_state = int(char.cflag.get(40, 0))
        return accessory_id in (98, 99) and bool(cloth_state & 64) and clothes_enabled


    def _has_seen_ending_event(self, key: str) -> bool:
        return int(self._get_ending_event_store().get(key, 0)) != 0


    def _human_age_generate(self, age_days: int, target) -> int:
        """年龄生成 - 对应 @HUMAN_AGE_GENERATE
        根据出生日数计算外表年龄
        """
        base_race = target.talent.get(314, 0)
        if base_race in (1, 2, 5, 6, 7, 8):
            return age_days // 365
        elif base_race in (3, 4):
            return min(age_days // 365, 30)
        else:
            return age_days // 365


    def _ikai_bonus(self) -> List[str]:
        """异界综合征相关奖励处理 - IKAI_BONUS.ERB"""
        output = []
        # IKAI_SOURCE_CHECK: 根据异界综合征等级给予debuff
        # 0-2: BUFF, 3-5: DEBUFF
        # 目前为框架，具体逻辑待实现
        return output

    # ------------------------------------------------------------------
    # LVUP_CHECK - 等级提升检查
    # ------------------------------------------------------------------


    def _in_vagina_all(self, target) -> List[str]:
        """妊娠判定(全キャラ) - 对应 @IN_VAGINA_ALL"""
        messages: List[str] = []
        return messages


    def _in_vagina_extra(self, target) -> List[str]:
        """売春による妊娠判定 - 对应 @IN_VAGINA_EXTRA"""
        messages: List[str] = []
        return messages


    def _in_vagina_kyouou_to_t(self, target) -> List[str]:
        """狂王と獣姦による妊娠判定 - 对应 @IN_VAGINA_KYOUOU_TO_T"""
        messages: List[str] = []
        return messages


    def _in_vagina_ntrd_to_t(self, target) -> List[str]:
        """NTRD妊娠判定 - 对应 @IN_VAGINA_NTRD_TO_T"""
        messages: List[str] = []
        return messages


    def _inherit_birth_child_talents(self, child: Character, mother: Character, father: Optional[Character] = None):
        for talent_id in self._iter_birth_inheritable_talent_ids():
            if father is None:
                if random.randint(0, 3) != 0:
                    child.talent[talent_id] = int(mother.talent.get(talent_id, 0))
                continue
            if random.randint(0, 15) != 0:
                source = mother if random.randint(0, 1) == 0 else father
                child.talent[talent_id] = int(source.talent.get(talent_id, 0))
        for talent_id in list(range(470, 490)):
            if mother.talent.get(220, 0) and mother.talent.get(talent_id, 0):
                child.talent[talent_id] = int(mother.talent.get(talent_id, 0))
            if father is not None and father.talent.get(220, 0) and father.talent.get(talent_id, 0):
                child.talent[talent_id] = int(father.talent.get(talent_id, 0))
        for talent_id, value in list(child.talent.items()):
            if int(value):
                self._apply_life_cradle_conflict_rules(child, talent_id)


    def _init_ex_talent_names(self) -> None:
        """初始化EX_TALENT名称（如果尚未初始化）"""
        # Names are already defined in _EX_TALENT_NAMES class variable
        pass

    # =========================================================================
    # System 2: MAKAI_BANK (魔界银行系统)
    # Based on ERB/MOD/MAKAIGINKOU v2.03v1/MAKAI_BANK.ERB
    # =========================================================================


    def _iter_birth_inheritable_talent_ids(self) -> List[int]:
        ids: List[int] = []
        for talent_id in range(10, 154):
            if 74 <= talent_id <= 78 or 121 <= talent_id <= 123 or 130 <= talent_id <= 143 or talent_id == 85:
                continue
            ids.append(talent_id)
        for talent_id in range(240, 265):
            if 244 <= talent_id <= 247 or talent_id == 254:
                continue
            ids.append(talent_id)
        ids.extend(range(275, 281))
        ids.extend(range(300, 315))
        return ids


    def _iter_life_cradle_page_ids(self, page_index: int) -> List[int]:
        pages = self._get_life_cradle_talent_pages()
        if page_index < 0 or page_index >= len(pages):
            return []
        ids: List[int] = []
        for section in pages[page_index]["sections"]:
            ids.extend(section["ids"])
        return ids


    def _iter_save_slot_indices(self):
        return range(20)


    def _juel_check_main(self, target: Character) -> List[str]:
        """珠チェック - 对应 @JUEL_CHECK_MAIN
        調教で得られた珠をキャラに反映
        """
        messages: List[str] = []
        for palam_id in range(17):
            juel_val = int(target.juel.get(palam_id, 0))
            if juel_val > 0:
                gotjuel_key = palam_id
                current = int(target.juel.get(gotjuel_key, 0))
                target.juel[gotjuel_key] = current + juel_val
        return messages


    def _level_up_character(self, idx: int, char: Character) -> tuple[bool, str]:
        needed_exp = self._get_character_level_up_exp_gap(idx, char)
        cost = needed_exp * 100
        if cost <= 0:
            return False, f"{char.name} 当前已经满足升级所需经验。"
        if self.interpreter.vars.money < cost:
            return False, f"需要金钱{cost}G，金钱不够"

        print(f"\n要使用金钱提升{char.name}的等级吗？")
        print(f"到下一级经验还要{needed_exp}点，需花费金钱{cost}G")
        print(" [0] 提升等级")
        print(" [1] 还是算了")
        choice = self._prompt_choice()
        if choice != "0":
            return False, "已取消提升等级。"

        self._spend_global_money(cost)
        char.exp[80] = int(char.exp.get(80, 0)) + needed_exp
        self._apply_level_up(idx)
        return True, f"花费了{cost}G，为{char.name}购买了经验{needed_exp}点"


    def _level_value(self, level: int, values: List[int]) -> int:
        index = max(0, min(level, len(values) - 1))
        return values[index]


    def _life_list(self, page: int = 0, mode: int = 1, num_per_page: int = 20) -> List[str]:
        """角色列表显示 - 对应 @LIFE_LIST

        显示所有存在角色的列表，包含编号、名称、职业、等级、沦陷状态等。

        Args:
            page: 页码（从0开始）
            mode: 显示模式（0=含主人, 1=标准, 2=简化）
            num_per_page: 每页显示数量

        Returns:
            显示文本行列表
        """
        lines: List[str] = []
        chars = self.interpreter.vars.chars
        char_num = len(chars)
        if char_num == 0:
            return lines

        master_idx = 0

        # 计算各列最大宽度
        max_num_len = len(str((page + 1) * num_per_page))
        max_name_len = max((len(c.name or "") for c in chars), default=4)
        max_name_len = max(max_name_len, 4)

        # 显示主人行
        if mode == 0 and master_idx < char_num:
            master = chars[master_idx]
            master_name = master.name or "你"
            master_lv = master.cflag.get(9, 0)
            lines.append(f"[{0:>{max_num_len}}]  {master_name:<{max_name_len}}（可强化地下城） LV{master_lv}")
        elif mode != 2 and master_idx < char_num:
            master = chars[master_idx]
            master_name = master.name or "你"
            master_lv = master.cflag.get(9, 0)
            lines.append(f"[{0:>{max_num_len}}]  {master_name:<{max_name_len}}        LV{master_lv}")

        # 显示角色列表
        start = page * num_per_page + 1
        end = min((page + 1) * num_per_page + 1, char_num)
        for count in range(start, end):
            if count >= char_num:
                lines.append("")
                continue
            if count == master_idx:
                continue

            char = chars[count]
            char_name = char.name or "???"
            char_lv = char.cflag.get(9, 0)
            job_name = self._get_job_name_for_char(count)

            # 沦陷状态
            if char.talent.get(85, 0):
                fall_status = "<爱  慕>"
            elif char.talent.get(76, 0):
                fall_status = "<淫  乱>"
            else:
                fall_status = "<未沦陷>"

            # 收藏标记
            favorite = "[☆]" if char.cflag.get(700, 0) else "     "

            # 可被卖/可作为助手
            sell_mark = ""
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) > 0
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可被卖]"
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) == 2
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可作为助手]"

            # 虫寄生
            parasite_mark = ""
            if (char.talent.get(190, 0) or char.talent.get(191, 0)
                    or char.talent.get(192, 0) or char.talent.get(193, 0)):
                parasite_mark = "[虫寄生]"

            # 妊娠标记
            pregnancy_mark = ""
            if char.talent.get(153, 0) or char.talent.get(341, 0) or char.talent.get(342, 0):
                pregnancy_mark = "[妊娠]"
            elif char.talent.get(341, 0):
                pregnancy_mark = "[乳内妊娠]"
            elif char.talent.get(342, 0):
                pregnancy_mark = "[精巣妊娠]"

            # 派遣标记
            dispatch_mark = "[派遣]" if char.cflag.get(1, 0) == 12 else ""

            line = (f"[{count:>{max_num_len}}]  {char_name:<{max_name_len}} "
                    f"{job_name:<6} LV{char_lv} {fall_status} {favorite}"
                    f"{sell_mark}{parasite_mark}{pregnancy_mark}{dispatch_mark}")
            lines.append(line)

        lines.append("-" * 60)
        return lines


    def _life_list_enemy(self, page: int = 0, num_per_page: int = 20) -> List[str]:
        """勇者列表显示 - 对应 @LIFE_LIST_ENEMY

        只显示侵攻中的勇者(CFLAG:1==2)。

        Args:
            page: 页码（从0开始）
            num_per_page: 每页显示数量

        Returns:
            显示文本行列表
        """
        lines: List[str] = []
        chars = self.interpreter.vars.chars
        char_num = len(chars)

        # 收集所有勇者
        enemies = []
        for count in range(char_num):
            char = chars[count]
            if (char.cflag.get(1, 0) == 2 and count != 0
                    and char.base.get(0, 0) > 0):
                enemies.append(count)

        # 分页
        start = page * num_per_page
        end = min((page + 1) * num_per_page, len(enemies))

        for i in range(start, end):
            count = enemies[i]
            char = chars[count]
            char_name = char.name or "???"
            char_lv = char.cflag.get(9, 0)
            train_count = char.cflag.get(10, 0)
            job_name = self._get_job_name_for_char(count)

            # 沦陷状态
            if char.talent.get(85, 0):
                fall_status = "<爱  慕>"
            elif char.talent.get(76, 0):
                fall_status = "<淫  乱>"
            else:
                fall_status = "<未沦陷>"

            # 性别
            if char.talent.get(122, 0):
                gender = "<男>"
            elif char.talent.get(121, 0):
                gender = "<扶她>"
            else:
                gender = "<女>"

            # 收藏
            favorite = "[☆]" if char.cflag.get(700, 0) else ""

            # 可被卖/可作为助手
            sell_mark = ""
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) > 0
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可被卖]"
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) == 2
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可作为助手]"

            # 虫寄生
            parasite_mark = ""
            if (char.talent.get(190, 0) or char.talent.get(191, 0)
                    or char.talent.get(192, 0) or char.talent.get(193, 0)):
                parasite_mark = "[虫寄生]"

            # 妊娠标记
            pregnancy_mark = ""
            if char.talent.get(153, 0) or char.talent.get(341, 0) or char.talent.get(342, 0):
                pregnancy_mark = "[妊娠]"

            # 派遣标记
            dispatch_mark = "[派遣]" if char.cflag.get(1, 0) == 12 else ""

            line = (f"[{count:>2}] {char_name:<12} {job_name:<6} LV{char_lv:>4}  "
                    f"调教回数:{train_count:<3} {fall_status} {gender} "
                    f"{favorite}{sell_mark}{parasite_mark}{pregnancy_mark}{dispatch_mark}")
            lines.append(line)

        return lines


    def _life_list_slave(self, page: int = 0, num_per_page: int = 20) -> List[str]:
        """奴隶列表显示 - 对应 @LIFE_LIST_SALAVE

        只显示奴隶状态的角色(CFLAG:1为0,3,5,6,7,10)。

        Args:
            page: 页码（从0开始）
            num_per_page: 每页显示数量

        Returns:
            显示文本行列表
        """
        lines: List[str] = []
        chars = self.interpreter.vars.chars
        char_num = len(chars)
        master_idx = 0

        # 收集所有奴隶
        slave_states = {0, 3, 5, 6, 7, 10}
        slaves = []
        for count in range(char_num):
            if count == master_idx:
                continue
            char = chars[count]
            if (char.cflag.get(1, 0) in slave_states
                    and count != 0 and char.base.get(0, 0) > 0):
                slaves.append(count)

        # 分页
        start = page * num_per_page
        end = min((page + 1) * num_per_page, len(slaves))

        for i in range(start, end):
            count = slaves[i]
            char = chars[count]
            char_name = char.name or "???"
            char_lv = char.cflag.get(9, 0)
            train_count = char.cflag.get(10, 0)
            job_name = self._get_job_name_for_char(count)

            # 沦陷状态
            if char.talent.get(85, 0):
                fall_status = "<爱  慕>"
            elif char.talent.get(76, 0):
                fall_status = "<淫  乱>"
            else:
                fall_status = "<未沦陷>"

            # 性别
            if char.talent.get(122, 0):
                gender = "<男>"
            elif char.talent.get(121, 0):
                gender = "<扶她>"
            else:
                gender = "<女>"

            # 收藏
            favorite = "[☆]" if char.cflag.get(700, 0) else ""

            # 可被卖/可作为助手
            sell_mark = ""
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) > 0
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可被卖]"
            if (char.cflag.get(1, 0) == 0 and char.cflag.get(0, 0) == 2
                    and count != 0 and char.base.get(0, 0) > 0):
                sell_mark = "[可作为助手]"

            # 虫寄生
            parasite_mark = ""
            if (char.talent.get(190, 0) or char.talent.get(191, 0)
                    or char.talent.get(192, 0) or char.talent.get(193, 0)):
                parasite_mark = "[虫寄生]"

            # 妊娠标记
            pregnancy_mark = ""
            if char.talent.get(153, 0) or char.talent.get(341, 0) or char.talent.get(342, 0):
                pregnancy_mark = "[妊娠]"

            # 派遣标记
            dispatch_mark = "[派遣]" if char.cflag.get(1, 0) == 12 else ""

            line = (f"[{count:>2}] {char_name:<12} {job_name:<6} LV{char_lv:>4}  "
                    f"调教回数:{train_count:<3} {fall_status} {gender} "
                    f"{favorite}{sell_mark}{parasite_mark}{pregnancy_mark}{dispatch_mark}")
            lines.append(line)

        return lines


    def _list_ability_up_candidates(self, menu_code: str) -> List[tuple[int, Character, Optional[str]]]:
        candidates: List[tuple[int, Character, Optional[str]]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx < 0:
                continue
            if menu_code == "997":
                blocked_reason = self._can_open_ability_up_hero_target(idx, char)
            else:
                blocked_reason = self._can_open_ability_up_slave_target(idx, char)
            if blocked_reason is None:
                candidates.append((idx, char, None))
        return candidates


    def _list_inventory(self, owner: Character) -> List[str]:
        if not owner.item:
            return ["  (empty)"]
        return [f"  - {name} x{count}" for name, count in sorted(owner.item.items())]


    def _list_morning_fellatio_candidates(self) -> List[tuple[int, Character, int]]:
        candidates: List[tuple[int, Character, int]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if not self._can_join_bedroom_daily_service(idx, char):
                continue
            if char.abl.get(11, 0) < 4 or char.abl.get(16, 0) < 4 or char.abl.get(32, 0) < 1:
                continue
            score = self._get_morning_fellatio_score(char)
            if score > 0:
                candidates.append((idx, char, score))
        return candidates


    def _magic_bonus_c_to_c(self, attacker, damage: int, defender=None) -> int:
        """角色对角色的魔法效果补正 - 对应 @MAGIC_BONUS_C_TO_C"""
        # 精灵特性 (TALENT:314 == 1 or 7) 1.5倍
        if attacker.talent.get(314, 0) in (1, 7):
            damage += damage // 2
        # 青肌特性 (TALENT:244) 1.33倍
        if attacker.has_talent(244):
            damage += damage // 3
        # 额之目特性 (TALENT:260) 1.2倍
        if attacker.has_talent(260):
            damage += damage // 5

        if defender is not None:
            # 魔法耐性 (TALENT:257) 0.77倍
            if defender.has_talent(257):
                damage -= damage // 3
            # 褐色肌 (TALENT:253) 0.8倍
            if defender.has_talent(253):
                damage -= damage // 5
            # 魔法debuff (CFLAG:682)
            magic_debuff = defender.cflag.get(682, 0)
            if magic_debuff > 50:
                damage += damage // 2
                defender.cflag[682] = magic_debuff - (magic_debuff // 10) - 1
            elif magic_debuff > 0:
                damage = damage * (100 + magic_debuff) // 100
                defender.cflag[682] = magic_debuff - (magic_debuff // 10) - 1
        return damage


    def _magic_bonus_c_to_m(self, char, damage: int) -> int:
        """角色对怪物的魔法效果补正 - 对应 @MAGIC_BONUS_C_TO_M"""
        # 精灵特性 (TALENT:314 == 1 or 7) 1.5倍
        if char.talent.get(314, 0) in (1, 7):
            damage += damage // 2
        # 青肌特性 (TALENT:244) 1.33倍
        if char.has_talent(244):
            damage += damage // 3
        # 额之目特性 (TALENT:260) 1.2倍
        if char.has_talent(260):
            damage += damage // 5
        return damage


    def _magic_bonus_m_to_c(self, char, damage: int) -> int:
        """怪物对角色的魔法效果补正 - 对应 @MAGIC_BONUS_M_TO_C"""
        if char is None:
            return damage
        # 魔法耐性 (TALENT:257) 0.77倍
        if char.has_talent(257):
            damage -= damage // 3
        # 褐色肌 (TALENT:253) 0.8倍
        if char.has_talent(253):
            damage -= damage // 5
        # 魔法debuff (CFLAG:682)
        magic_debuff = char.cflag.get(682, 0)
        if magic_debuff > 50:
            damage += damage // 2
            char.cflag[682] = magic_debuff - (magic_debuff // 10) - 1
        elif magic_debuff > 0:
            damage = damage * (100 + magic_debuff) // 100
            char.cflag[682] = magic_debuff - (magic_debuff // 10) - 1
        return damage


    def _magic_cast(self, caster_idx: int, spell_id: int, target_idx: int) -> Dict[str, int]:
        """Cast a spell. Returns a dict of effects (damage, heal, etc.).

        Mirrors @MAGIC_USE in MAGIC.ERB.
        """
        result: Dict[str, int] = {"spell_id": spell_id}
        if spell_id <= 0 or spell_id > 9:
            return result

        spell_name = self._SPELL_NAMES.get(spell_id, "未知魔法")
        result["spell_name_hash"] = hash(spell_name) & 0xFFFF

        chars = self.interpreter.vars.chars
        if caster_idx < 0 or caster_idx >= len(chars):
            return result

        caster = chars[caster_idx]
        magic_lv = caster.cflag.get(9, 0)  # CFLAG:9 = magic level

        # Base power scales with magic level
        base_power = magic_lv * 10 + 20

        if spell_id == 1:  # 瞬间移动
            result["evasion"] = 1
        elif spell_id == 2:  # 催眠术
            result["sleep_chance"] = min(base_power, 100)
        elif spell_id == 3:  # 能量弹
            result["damage"] = base_power * 2
        elif spell_id == 4:  # 能量吸收
            drain = base_power
            result["damage"] = drain
            result["heal_hp"] = drain // 2
        elif spell_id == 5:  # 火球术
            result["damage"] = base_power * 3
        elif spell_id == 6:  # 治愈术
            result["heal_hp"] = base_power * 2
        elif spell_id == 7:  # 诅咒术
            result["curse_power"] = base_power
        elif spell_id == 8:  # 精神吸取
            result["mp_damage"] = base_power
            result["heal_mp"] = base_power // 2
        elif spell_id == 9:  # 等级吸取
            result["level_drain"] = max(1, magic_lv // 3)

        # Anti-magic diffusion check (CFLAG:503 & 2)
        if caster.cflag.get(503, 0) & 2:
            anti_dmg = magic_lv * 10 + 200
            if anti_dmg > 600:
                anti_dmg = 600
            result["self_damage"] = anti_dmg

        return result

    # ------------------------------------------------------------------
    # INFRASTRUCTURE (基础设施)
    # ------------------------------------------------------------------

    _INFRA_NAMES: Dict[int, str] = {
        600: "石像", 601: "标本", 602: "蜡像", 603: "人体模型人偶",
        604: "球型关节人偶", 605: "金属雕像", 606: "冰雕", 607: "宝石像",
        608: "家具", 609: "画像", 611: "石制喷水像", 612: "金属喷水像",
    }

    _INFRA_DESC: Dict[int, str] = {
        600: "被石化了的原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。",
        601: "被制成标本的原勇者的美丽肢体，空洞的眼神注视着对面墙壁上的装饰。",
        602: "被制成蜡像的原勇者的美丽肢体，一个个都有独一无二的姿势和装饰。",
        603: "被制成人体模型人偶的原勇者的美丽肢体，四肢和头部都可以自由拆卸。",
        604: "被制成球型关节人偶的原勇者的美丽肢体，能做出许多匪夷所思的动作。",
        605: "被制成金属雕像的原勇者的美丽肢体，发出美丽的光泽展示于人前。",
        606: "被制成冰雕的原勇者的美丽肢体，保持着永恒的冰冷姿态。",
        607: "被制成宝石像的原勇者的美丽肢体，闪耀着耀眼的光辉。",
        608: "原本是活生生的勇者们，现在被再造成无机的家具展出。",
        609: "原本是活生生的勇者们，现在被弄成一幅画在展出着。",
        611: "被石化的原勇者的美丽肢体，从各处喷出漂亮的涌泉。",
        612: "被制成金属喷水像的原勇者的美丽肢体，喷出壮丽的水柱。",
    }


    def _magic_damage_cap(self, char_lv: int, enemy_lv: int, damage: int, dmg_cap: int) -> int:
        """伤害上限计算 - 对应 @MAGIC_DAMAGE_CAP"""
        cap_bonus = char_lv - enemy_lv
        if cap_bonus <= -100:
            cap_bonus = -99
        dmg_cap = dmg_cap * (100 + cap_bonus) // 100
        if damage > dmg_cap:
            damage = dmg_cap
        if damage <= 0:
            damage = 1
        return damage


    def _maou_kouho(self) -> List[str]:
        """确定魔王候补 - 对应 @MAOU_KOUHO"""
        messages: List[str] = []
        return messages


    def _mark_ending_event_seen(self, key: str):
        self._get_ending_event_store()[key] = 1


    def _mark_pending_morning_events(self) -> None:
        self.interpreter.vars.items["_pending_morning_event_day"] = tuple(int(part) for part in self.interpreter.vars.day)


    def _marriage_day(self, char_idx: int) -> List[str]:
        """结婚生活 - 对应 @MARRIAGE_DAY

        根据婚姻类型(CFLAG:601)执行不同的结婚生活事件。

        Args:
            char_idx: 角色索引

        Returns:
            事件消息列表
        """
        messages: List[str] = []
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"

        # 非调教可状态检查
        if char.cflag.get(1, 0) != 0:
            # 不是奴隶状态时，尝试恋人事件
            if char.cflag.get(606, 0) == 200:
                return self._dungeon_town_lover(char_idx)
            return messages

        marry_type = char.cflag.get(601, 0)
        if marry_type == 0:
            # 没有配偶，尝试恋人事件
            if char.cflag.get(606, 0) == 200:
                return self._dungeon_town_lover(char_idx)
            return messages

        # 增加结婚日数
        char.cflag[602] = char.cflag.get(602, 0) + 1

        # 妊娠/育児检查
        if char.talent.get(153, 0):
            messages.append("夫妇俩人期待着孩子的出生。")
            return messages
        elif char.talent.get(154, 0):
            messages.append("夫妇俩人期待着孩子的长大。")
            return messages

        # 确定配偶名称
        spouse_name = ""
        if marry_type == 902:
            # 恋人结婚
            lover_id = char.cflag.get(606, 0)
            spouse_name = self._name_lover(lover_id)
        elif marry_type == 900:
            spouse_name = "野狗"
        elif marry_type == 901:
            spouse_name = "你"
        elif marry_type < 900:
            # 怪物配偶
            spouse_name = f"怪物{marry_type}"
        else:
            spouse_name = "奴隶"

        messages.append(f"*{char_name}和{spouse_name}的结婚生活*")

        # 根据婚姻类型分派
        if marry_type == 900:
            messages.extend(self._marriage_day_dog(char_idx))
        elif marry_type == 901:
            messages.extend(self._marriage_day_you(char_idx))
        elif marry_type == 902:
            messages.extend(self._marriage_day_lovers(char_idx))
        else:
            # 怪物配偶 - 简化实现
            messages.append(f"{char_name}和{spouse_name}一同生活着。")

        # 处女丧失检查
        if char.talent.get(0, 0) == 1 and char.exp.get(0, 0) > 0:
            if not char.talent.get(273, 0) and char.cflag.get(42, 0) != 79:
                messages.append("【处女丧失】")
                char.talent[0] = 0

        # 母乳贩卖
        if char.talent.get(130, 0) == 1:
            y_val = 1
            milk_income = y_val * 100
            messages.append(f"{char_name}多余的奶水被卖出了获得{milk_income}pts")
            self.interpreter.vars.money = getattr(self.interpreter.vars, 'money', 10000) + milk_income

        return messages


    def _marriage_day_dog(self, char_idx: int) -> List[str]:
        """野狗结婚生活 - 对应 @MARRIAGE_DAY_DOG"""
        messages: List[str] = []
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"
        marry_days = char.cflag.get(602, 0)
        y_val = 1

        messages.append(f"{char_name}和野狗在狗屋生活着。")

        is_anal = (char.talent.get(273, 0) == 1
                   or char.talent.get(122, 0) == 1
                   or (char.cflag.get(42, 0) == 79
                       and (char.cflag.get(40, 0) & 64)
                       and self.interpreter.vars.flag.get(37, 0)))

        if char.talent.get(136, 0) == 1:
            # 牝犬
            tail_action = "摇着尾巴" if char.talent.get(314, 0) == 2 else "摇着屁股"
            location = "在公众场所" if char.abl.get(17, 0) >= 3 else ""
            hole = "用肛门" if is_anal else ""
            action = random.choice(["发情交尾着。", "交配着。", "爱爱着。"])
            messages.append(f"{char_name}{tail_action}{location}{hole}和野狗{action}")
            if is_anal:
                messages.append(f"肛门经验＋{y_val}")
                char.exp[1] = char.exp.get(1, 0) + y_val
            else:
                messages.append(f"私处经验＋{y_val}")
                char.exp[0] = char.exp.get(0, 0) + y_val
                char.cflag[106] = char.cflag.get(106, 0) + y_val
            messages.append(f"兽奸经验＋{y_val}")
            char.exp[56] = char.exp.get(56, 0) + y_val
        elif char.abl.get(39, 0) >= 1 or marry_days > 40:
            # 兽奸中毒Lv1以上 或 结婚爱情40超
            if is_anal:
                messages.append(f"{char_name}时常主动与狗交缠舌头，仿佛热恋中的情侣一般。")
                messages.append(f"在被狗抽插肛门的时候，{char_name}热切地摇摆着腰肢配合着。")
                messages.append(f"滚烫的野兽精液灌入直肠，令{char_name}感觉到了爱意。")
                messages.append(f"肛门经验＋{y_val}")
                char.exp[1] = char.exp.get(1, 0) + y_val
            else:
                messages.append(f"{char_name}时常主动与狗交缠舌头，仿佛热恋中的情侣一般。")
                messages.append(f"在被狗抽插小穴的时候，{char_name}热切地摇摆着腰肢配合着。")
                messages.append(f"滚烫的野兽精液灌入小穴，令{char_name}感觉到了爱意。")
                messages.append(f"私处经验＋{y_val}")
                char.exp[0] = char.exp.get(0, 0) + y_val
                char.cflag[106] = char.cflag.get(106, 0) + y_val
            messages.append(f"兽奸经验＋{y_val}")
            char.exp[56] = char.exp.get(56, 0) + y_val
        elif marry_days > 20:
            # 结婚爱情20超
            if char.talent.get(11, 0) == 1:
                messages.append(f"{char_name}终于理解自己的状况了……")
            elif char.talent.get(12, 0) == 1:
                messages.append(f"{char_name}和野狗一起玩耍，关系加深了……")
            elif char.talent.get(13, 0) == 1 or char.talent.get(317, 0) == 12:
                messages.append(f"{char_name}与野狗热情接吻的样子被目击了。")
            else:
                messages.append(f"{char_name}用刷子为野狗刷毛……")
        else:
            if char.talent.get(11, 0) == 1:
                messages.append(f"{char_name}用手推开靠过来的野狗。")
            elif char.talent.get(12, 0) == 1:
                messages.append(f"{char_name}有空就去照看野狗。")
            elif char.talent.get(13, 0) == 1 or char.talent.get(317, 0) == 12:
                messages.append(f"{char_name}有空就去和野狗玩耍。")
            else:
                messages.append(f"从不正眼看野狗，{char_name}陷入了深深的绝望中……")

        return messages


    def _marriage_day_lovers(self, char_idx: int) -> List[str]:
        """恋人结婚生活 - 对应 @MARRIAGE_DAY_LOVERS"""
        messages: List[str] = []
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"
        lover_id = char.cflag.get(606, 0)
        lover_name = self._name_lover(lover_id) if lover_id > 0 else "恋人"

        messages.append(f"{char_name}和{lover_name}一起生活着。")

        # 调用城镇恋人事件
        lover_messages = self._dungeon_town_lover(char_idx)
        messages.extend(lover_messages)

        return messages

    # ========================================
    # LIFE_LIST - 生命列表系统
    # 对应 ERB/LIFE_LIST.ERB
    # ========================================


    def _marriage_day_you(self, char_idx: int) -> List[str]:
        """与主人结婚生活 - 对应 @MARRIAGE_DAY_YOU"""
        messages: List[str] = []
        if char_idx < 0 or char_idx >= len(self.interpreter.vars.chars):
            return messages

        char = self.interpreter.vars.chars[char_idx]
        char_name = char.name or "角色"

        messages.append(f"{char_name}与你一起生活着。")

        if char.talent.get(85, 0) == 1:
            # 爱慕
            messages.append(f"{char_name}常常一言不发，柔情似水地凝望着你。一副自豪的样子在你身旁侍奉着。")
            messages.append("为成为一个好妃子努力修行着。自动接受着各种羞耻的调教。")
        elif char.talent.get(76, 0) == 1:
            # 淫乱
            body_part = "阴茎" if (char.talent.get(121, 0) or char.talent.get(122, 0)) else "身体"
            messages.append(f"{char_name}经常在身边露出淫媚的笑容，在你的{body_part}上不停摩挲着。")
            messages.append("心里却盘算着如何偷偷引诱你某几个部下...")
        elif char.abl.get(10, 0) >= 3:
            # 顺从3以上
            messages.append(f"{char_name}作为勇者陷落的象征，勉为其难地陪侍着你身边。")
            messages.append("偶尔象征性的表示期望你的调教...")
        elif char.mark.get(3, 0) >= 1:
            # 反抗刻印
            messages.append(f"{char_name}被链子锁着，用充满杀意的目光望着你。")
            messages.append("但已经被调教过的身体是诚实的...")
        else:
            messages.append(f"{char_name}被链子锁着，放弃了似得自暴自弃。")
            messages.append("被恐惧、羞耻与绝望侵蚀着...")

        return messages


    def _merge_ability_upgrade_rule_groups(self, *groups: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        merged: Dict[int, Dict[str, Any]] = {}
        for group in groups:
            merged.update(group)
        return merged


    def _merge_ability_upgrade_rules(self, *groups: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        merged: Dict[int, Dict[str, Any]] = {}
        for group in groups:
            merged.update(group)
        return merged


    def _name_lover(self, lover_id: int) -> str:
        """获取恋人名称 - 对应 @NAME_LOVER

        Args:
            lover_id: 恋人类型ID

        Returns:
            恋人名称字符串，无效ID返回空字符串
        """
        return self._LOVER_NAMES.get(lover_id, "")


    def _night_stalking_check(self) -> List[str]:
        """性交中毒による夜這いチェック - 对应 @NIGHT_STALKING_CHECK"""
        messages: List[str] = []
        return messages


    def _normal_point_pickup(self, center: int) -> int:
        roll = random.randint(1, 17)
        if roll == 1:
            return int(center) - 2
        if roll <= 4:
            return int(center) - 1
        if roll <= 13:
            return int(center)
        if roll <= 16:
            return int(center) + 1
        return int(center) + 2


    def _normalize_ability_upgrade_paths(self, path_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized_paths = []
        for idx, path in enumerate(path_entries):
            normalized_paths.append({
                "menu_id": idx,
                "label": str(path["label"]),
                "costs": dict(path["costs"]),
            })
        return normalized_paths


    def _normalize_birth_template_id(self, template_id: Optional[int], elite_preferred: bool = False) -> Optional[int]:
        if template_id is None:
            return None
        available = set(self._get_available_human_birth_template_ids())
        if elite_preferred:
            if 201 <= int(template_id) <= 210 and int(template_id) in available:
                return int(template_id)
            if 1 <= int(template_id) <= 16:
                elite_guess = int(template_id) + 200
                if elite_guess in available:
                    return elite_guess
        if int(template_id) in available:
            return int(template_id)
        return None


    def _normalize_spawned_hero_identity(self, hero: Character):
        if not hero.name:
            hero.name = hero.callname or "勇者"
        if not hero.callname:
            hero.callname = hero.name
        if not hero.cstr.get(1, ""):
            hero.cstr[1] = hero.name


    def _parse_ability_up_roster_choice(self, choice: str) -> Optional[int]:
        try:
            return int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return None


    def _parse_choice_int(self, choice: str, offset: int = 0) -> Optional[int]:
        try:
            return int(choice) + offset
        except ValueError:
            return None


    def _pause(self, prompt: str = "\nPress enter to continue..."):
        self._read_input(prompt)


    def _player_has_service_target(self, player: Character) -> bool:
        if player.talent.get(121, 0) or player.talent.get(122, 0):
            return True
        return player.maxbase.get(2, 0) > 0 or player.base.get(2, 0) > 0


    def _populate_ability_upgrade_costs(self, option: Dict[str, Any], rules: Dict[str, Any], target: Character, level: int) -> None:
        option["cost_types"] = dict(rules.get("cost_types", {}))
        raw_paths = rules.get("paths")
        if raw_paths is not None:
            path_entries = list(raw_paths(self, target, level))
            option["paths"] = self._normalize_ability_upgrade_paths(path_entries)
            if option["paths"]:
                option["costs"] = dict(option["paths"][0]["costs"])
            return

        raw_costs = rules.get("costs", {})
        if callable(raw_costs):
            option["costs"] = dict(raw_costs(self, target, level))
        else:
            option["costs"] = dict(raw_costs.get(level, {}))


    def _precipitate_withdrawal(self, target) -> List[str]:
        """禁断症状 - 对应 @PRECIPITATE_WITHDRAWAL"""
        import random
        messages = []
        v = self.interpreter.vars

        messages.append(f"{target.savestr}在诉说着自己的身体不适应症状。")
        messages.append("看来，春药中毒的禁断症状出现了……")

        # 计算治疗/献身人数
        U = 0
        for char in v.chars:
            if (char.talent.get(117, 0) or char.talent.get(63, 0)) and char.cflag.get(1, 0) == 0:
                U += 1

        # 禁断症状酷度
        V = (target.cflag.get(31, 0) // 10) + 1 - U
        V = max(1, min(V, 10))

        # 检查是否恶化
        W = 0
        for _ in range(V):
            if random.randint(0, 99) < 40:
                W = random.randint(0, 49) - V + (U * 2)
                break

        if W < 5 and W != 0:
            # 严重恶化
            if not target.talent.get(9, 0):
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，完全变成一个废人了。")
                messages.append(f"{target.savestr}的精神【崩坏】了……")
                target.talent[19] = 1
            elif not target.talent.get(123, 0):
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，充满攻击性了。")
                messages.append(f"{target.savestr}获得了【疯狂】。")
                target.talent[123] = 1
            elif target.relation.get(0, 0) == 0 or target.relation.get(0, 0) > 50:
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，被主人嫌弃了。")
                if target.relation.get(0, 0) == 0:
                    target.relation[0] = 50
                else:
                    target.relation[0] = max(30, target.relation.get(0, 0) - 50)
                target.cflag[2] = target.cflag.get(2, 0) - 200
            elif not target.talent.get(34, 0):
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，变得不和善了。")
                messages.append(f"{target.savestr}获得了【抵抗】。")
                target.talent[34] = 1
            elif not target.talent.get(26, 0):
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，对人生看法灰暗。")
                messages.append(f"{target.savestr}获得了【悲观的】。")
                target.talent[26] = 1
            elif not target.talent.get(22, 0):
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，连感情都失去了。")
                messages.append(f"{target.savestr}获得了【感情淡薄】。")
                target.talent[22] = 1
            else:
                messages.append(f"{target.savestr}的样子明显不对头……")
                messages.append(f"{target.savestr}饱受禁断症状的痛苦，被主人嫌弃了。")
                target.cflag[2] = target.cflag.get(2, 0) - 200

            # 体力/气力下降
            target.maxbase[0] = max(600, target.maxbase.get(0, 1000) - 50)
            target.maxbase[1] = max(100, target.maxbase.get(1, 500) - 50)
            target.base[0] = min(target.base.get(0, 0), target.maxbase[0])
            target.base[1] = min(target.base.get(1, 0), target.maxbase[1])
            target.base[0] = max(1, target.base.get(0, 0) - 500)

            # 看护者体力下降
            for char in v.chars:
                if char.cflag.get(1, 0) == 0:
                    if char.talent.get(117, 0) or char.talent.get(63, 0):
                        char.base[0] = max(1, char.base.get(0, 100) - 200)
                    elif random.randint(0, 2) == 0:
                        char.base[0] = max(1, char.base.get(0, 100) - 200)

            messages.append(f"被禁断症状折磨着的{target.savestr}痛苦地在地上打滚，")
            messages.append("持续数小时的癫狂的行为也终于让她感到累了，症状被平息，终于老实了下来。")
            messages.append(f"{target.savestr}的体力和气力衰退了。")
        else:
            messages.append(f"数小时后，{target.savestr}身体的颤抖终于停止了，")
            messages.append("护理人员也辛苦了，这次总算平安度过了……")
            target.base[0] = max(1, target.base.get(0, 100) - 300)

            for char in v.chars:
                if char.cflag.get(1, 0) == 0:
                    if char.talent.get(117, 0) or char.talent.get(63, 0):
                        char.base[0] = max(1, char.base.get(0, 100) - 100)
                    elif random.randint(0, 2) == 0:
                        char.base[0] = max(1, char.base.get(0, 100) - 100)

        return messages

    # ========================================
    # EVENT_SABBATH - 安息日系统
    # 对应 ERB/EVENT_SABBATH.ERB
    # ========================================


    def _print_delta_summary(self, label: str, delta_map: Dict[int, int]):
        if not delta_map:
            return
        parts = [f"{key}:+{value}" for key, value in sorted(delta_map.items()) if value]
        if parts:
            print(f"{label} " + ", ".join(parts))


    def _print_turn_end_early_messages(self, early_messages: List[str]) -> None:
        for message in early_messages:
            print(message)


    def _print_turn_end_new_day_messages(self) -> None:
        for message in self._process_new_day():
            print(message)


    def _purchase_catalog_item(self, item_id: int):
        purchase_context = self._prepare_purchase_catalog_item(item_id)
        if purchase_context is None:
            return

        mode = purchase_context["mode"]
        if mode == "use_now":
            self._handle_purchase_catalog_item_use_now(item_id, purchase_context["price"], purchase_context["item_name"])
            return

        if mode == "knowledge":
            self._handle_purchase_catalog_item_knowledge(item_id, purchase_context["price"], purchase_context["item_name"])
            return

        self._handle_purchase_catalog_item_plural_purchase(
            item_id,
            purchase_context["player"],
            purchase_context["price"],
            purchase_context["item_name"],
        )


    def _queue_post_message_action(self, action: Dict[str, Any]):
        self._get_pending_post_message_actions().append(action)


    def _queue_square_ending_prompt(self, stage: int, event_key: str) -> bool:
        if stage == 40:
            self._queue_post_message_action({"kind": "square_departure_prompt", "event_key": event_key})
            return True
        if stage == 90:
            self._queue_post_message_action({"kind": "square_love_ending_prompt", "event_key": event_key})
            return True
        return False


    def _random_self_call(self, target: Character, mode: int = 0) -> int:
        """Determine a character's self-call (first person pronoun).
        Corresponds to ERB @RANDOM_SELF_CALL.
        mode=0: random, mode=1: custom input
        Returns the CFLAG:450 value set.
        """
        local = int(target.cflag.get(450, 0))

        if mode == 1:
            # Custom input mode - handled by _set_self_call
            return local

        # RANDOM path
        if local >= 200:
            local = -1

        if local < 0:
            # Try CSV template CSTR:60
            template = self._get_character_template_baseline_for_target(target)
            if template is not None:
                template_self_call = str(template.cstr.get(60, "")).strip()
                if template_self_call:
                    target.cstr[60] = template_self_call
                    target.cflag[450] = 0
                    return 0

        if local < 9:
            target.cstr[60] = "我"
            target.cflag[450] = 9
            return 9

        if local < 100:
            local -= 10
            result = self._set_suit_selfcall(target, local)
            if result >= 0:
                target.cflag[450] = result + 10
                return result + 10
            local = 99

        if local < 200:
            local -= 100
            result = self._set_nick_selfcall(target, local)
            if result >= 0:
                target.cflag[450] = result + 100
                return result

        target.cflag[450] = -1
        return self._random_self_call(target, mode=0)


    def _recalculate_all_character_race_ages(self) -> int:
        updated = 0
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx == 0:
                continue
            human_age = int(char.cflag.get(451, 0))
            if human_age <= 0:
                continue
            char.cflag[452] = self._generate_race_age(human_age, int(char.talent.get(314, 0)))
            updated += 1
        return updated


    def _record_public_video(self, target: Character, title: str, count_campaign_total: bool = False) -> None:
        if not title:
            return
        if count_campaign_total:
            self._maturo_video_title_with_campaign(target, title)
            return
        self._maturo_video_title(target, title)


    def _recover_character(self, char: Character) -> tuple[bool, str]:
        cost = self._get_character_recover_cost(char)
        if cost <= 0:
            return False, f"{char.name} 当前不需要恢复。"
        if self.interpreter.vars.money < cost:
            return False, f"需要金钱{cost}G，金钱不够"

        print(f"\n要使用金钱恢复{char.name}的体力和气力吗？")
        print(
            f"恢复{max(0, int(char.maxbase.get(0, 0)) - int(char.base.get(0, 0)))}点体力和"
            f"{max(0, int(char.maxbase.get(1, 0)) - int(char.base.get(1, 0)))}点气力，需花费金钱{cost}G"
        )
        print(" [0] 立即恢复")
        print(" [1] 还是算了")
        choice = self._prompt_choice()
        if choice != "0":
            return False, "已取消恢复。"

        self._spend_global_money(cost)
        char.base[0] = char.maxbase.get(0, char.base.get(0, 0))
        char.base[1] = char.maxbase.get(1, char.base.get(1, 0))
        return True, f"花费{cost}G，恢复了{char.name}的体力与气力"


    def _refresh_story_presence_flags(self):
        tracked_templates = {
            17: 2805,
            20: 2813,
            21: 2814,
            22: 2811,
            23: 2812,
            24: 2806,
            31: 2808,
            32: 2809,
            33: 2810,
            34: 2815,
            35: 2807,
        }
        for template_id, flag_id in tracked_templates.items():
            char = self._find_character_by_template_id(template_id)
            if char is not None:
                continue
            current = int(self.interpreter.vars.get_flag(flag_id, 0)) if flag_id == 2815 else int(self.interpreter.vars.globals.get(flag_id, 0))
            if flag_id == 2814 and current >= 300:
                continue
            if flag_id == 2810 and int(self.interpreter.vars.globals.get(2814, 0)) >= 500:
                continue
            if flag_id == 2815:
                self.interpreter.vars.set_flag(flag_id, 0)
            else:
                self.interpreter.vars.globals[flag_id] = 0


    def _remove_equipment_from_slot(self, target: Character, slot_flag: int, is_weapon: bool) -> tuple[bool, str]:
        player = self._get_player()
        if player is None:
            return False, "当前没有魔王角色。"
        current_code = int(target.cflag.get(slot_flag, -1))
        if current_code < 0:
            return False, "当前没有可取下的装备。"
        item_id = self._get_weapon_item_id_from_code(current_code) if is_weapon else self._get_ring_item_id_from_code(current_code)
        self._return_equipment_item(player, item_id)
        target.cflag[slot_flag] = -1
        return True, f"{target.name} 取下了{self._get_equipment_slot_name(slot_flag)}。"


    def _remove_last_character_if_matches(self, char: Optional[Character]):
        if char is None or not self.interpreter.vars.chars:
            return
        if self.interpreter.vars.chars[-1] is char:
            self._remove_character_at(len(self.interpreter.vars.chars) - 1)


    def _rename_character(self, idx: int, target: Character, reset: bool = False) -> tuple[bool, str]:
        blocked_reason = self._can_edit_character_name(idx, target)
        if blocked_reason is not None and not (idx == 0 and reset):
            return False, blocked_reason
        if reset:
            return self._reset_character_name(target)

        print(f"\n{target.callname}的新名字是？")
        new_name = self._prompt_choice("Name >> ")
        if len(new_name) > 16:
            return False, "名字太长，请使用全角八字以下的名字。"
        if not new_name:
            return True, f"{target.callname}的名字没有变更。"
        target.callname = new_name
        target.name = new_name
        if int(target.cflag.get(450, 0)) >= 99:
            self._reset_character_self_call(target)
        return True, f"{target.callname}今后被称呼为{new_name}。"


    def _report_erb_load_failure(self, error: Exception) -> None:
        print(f"Note: Could not load ERB files: {error}")


    def _report_loaded_erb_function_count(self) -> None:
        print(f"Loaded {len(self.interpreter.functions)} functions from ERB files")


    def _reset_daily_shop_flags(self):
        self.interpreter.vars.set_flag(61, 0)


    def _reset_invading_hero_runtime_state(
        self,
        hero: Character,
        assign_spawn_position: bool = True,
    ):
        hero.cflag[1] = 2
        hero.cflag[500] = 0
        hero.cflag[505] = 0
        hero.cflag[506] = 0
        self._reset_dungeon_floor_progress(hero, floor=1, return_flag=0)
        hero.cflag[520] = max(1, int(hero.cflag.get(520, 0)))
        hero.cflag[999] = 0
        if assign_spawn_position:
            self._assign_invading_hero_spawn_position(hero)


    def _restore_character_as_invading_hero(
        self,
        hero: Character,
        karma_floor: int = -50,
        assign_spawn_position: bool = True,
    ) -> None:
        self._reset_invading_hero_runtime_state(hero, assign_spawn_position=assign_spawn_position)
        hero.base[0] = int(hero.maxbase.get(0, hero.base.get(0, 0)))
        hero.base[1] = int(hero.maxbase.get(1, hero.base.get(1, 0)))
        hero.cflag[508] = 3
        if int(hero.cflag.get(151, 0)) < karma_floor:
            hero.cflag[151] = karma_floor
        hero.cflag[2] = 20


    def _return_equipment_item(self, owner: Character, item_id: int):
        self._add_item(owner, self._get_item_name(item_id), 1)


    def _roll_daily_cursed_ring_base_code(self) -> int:
        roll = random.randint(0, 99)
        if roll < 20:
            return 13
        if roll < 40:
            return 14
        if roll < 60:
            return 19
        if roll < 80:
            return 20
        if roll < 90:
            return 12
        if roll < 95:
            return 11
        if roll < 98:
            return 6
        if roll < 100:
            return 15
        return 13


    def _run_conquest_random_candidate_picker(
        self,
        random_title: str,
        retry_text: str,
    ) -> tuple[bool, str]:
        personality_id: Optional[int] = None
        hair_color: Optional[int] = None
        while True:
            candidate = self._spawn_conquest_random_candidate(hair_color=hair_color, personality_id=personality_id)
            if candidate is None:
                return False, "缺少可用的贡品模板。"
            sub_choice = self._prompt_conquest_random_candidate_choice(candidate, random_title, retry_text)
            handled, result = self._handle_conquest_random_candidate_choice(sub_choice, candidate, personality_id, hair_color)
            if not handled:
                continue
            if result is None:
                continue
            return result


    def _run_game_state_loop(self) -> None:
        state = "TITLE"
        while self.running:
            state = self._advance_game_state_safely(state)
            if state == "EXIT":
                break


    def _run_life_cradle_customization_stage(self, new_char: Character) -> Optional[tuple[bool, str]]:
        ok, message = self._customize_life_cradle_talents(new_char)
        if not ok:
            return False, message
        ok, message = self._customize_life_cradle_looks(new_char)
        if not ok:
            return False, message
        ok, message = self._customize_life_cradle_first_history(new_char)
        if not ok:
            return False, message
        ok, message = self._apply_life_cradle_custom_name(new_char)
        if not ok:
            return False, message
        return None


    def _run_pending_morning_events_if_needed(self) -> None:
        if self.interpreter.vars.time != 0:
            return
        pending_day = self.interpreter.vars.items.get("_pending_morning_event_day")
        if pending_day != tuple(int(part) for part in self.interpreter.vars.day):
            return
        for message in self._process_event_newday():
            print(message)
        self.interpreter.vars.items.pop("_pending_morning_event_day", None)


    def _run_turn_end_post_message_actions(self) -> None:
        for message in self._apply_turn_end_anomaly_events():
            print(message)
        self._drain_post_message_actions()


    def _search_family(self, target: Character) -> int:
        """Search for target in the character list's family (CFLAG:605).
        Returns the character index if found, or -1 if not found.
        """
        target_family = int(target.cflag.get(605, 0))
        if target_family == 0:
            return -1
        family_unit = target_family % 10
        chars = self.interpreter.vars.chars
        for i, ch in enumerate(chars):
            if ch is target:
                continue
            ch_family = int(ch.cflag.get(605, 0))
            if ch_family > 0 and ch_family % 10 == family_unit:
                return i
        return -1


    def _select_assistant_from_roster(self) -> Optional[int]:
        candidates = [
            (idx, char)
            for idx, char in enumerate(self.interpreter.vars.chars)
            if self._can_select_standby_slave(idx, char) is None
        ]
        if not candidates:
            return None

        return self._advance_assistant_selection(candidates)


    def _select_life_cradle_first_experience(self, target: Character) -> tuple[bool, str]:
        if target.talent.get(0, 0):
            return True, "处女角色不设定初体验对象。"

        while True:
            result = self._advance_life_cradle_first_experience(target)
            if result is not None:
                return result


    def _select_life_cradle_first_kiss(self, target: Character) -> tuple[bool, str]:
        while True:
            result = self._advance_life_cradle_first_kiss(target)
            if result is not None:
                return result


    def _select_maou_candidate(self) -> Optional[int]:
        best_idx: Optional[int] = None
        best_score = -1
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            if int(self._get_character_ex_talent(char, 3)) != 1:
                continue
            score = int(char.cflag.get(2, 0))
            if score > best_score:
                best_idx = idx
                best_score = score
        return best_idx


    def _select_target_from_roster(self) -> bool:
        captives = [
            (idx, char)
            for idx, char in enumerate(self.interpreter.vars.chars)
            if idx > 0
        ]
        if not captives:
            print("No captives are available.")
            return False

        self._render_target_roster(captives)
        return self._handle_target_roster_choice(captives)


    # =====================================================================
    # ENDING (结局系统)
    # Corresponds to ERB ENDING.ERB, ENDINGDATA.ERB, ENDINGDATA_ADDON1.ERB
    # =====================================================================

    _ENDING_DEFINITIONS = {
        "1": {
            "id": "1",
            "name": "Good End - 魔王征服世界",
            "description": "魔王终于再次掌握了世界",
            "flag_key": 2801,
            "check_value": 1,
        },
        "2": {
            "id": "2",
            "name": "Bad End - 魔王城陷落",
            "description": "新的女勇者攻陷了魔王的地下城",
            "flag_key": 2803,
            "check_value": -1,
        },
        "3": {
            "id": "3",
            "name": "精灵领域制霸",
            "description": "魔王征服了精灵族的领域",
            "flag_key": 87,
            "check_value": 1,
        },
        "4": {
            "id": "4",
            "name": "龙族山脉制霸",
            "description": "魔王征服了龙族的山脉",
            "flag_key": 89,
            "check_value": 1,
        },
        "5": {
            "id": "5",
            "name": "天界领域制霸",
            "description": "魔王征服了天界",
            "flag_key": 91,
            "check_value": 1,
        },
        "N": {
            "id": "N",
            "name": "Normal End - 500日",
            "description": "自从魔王被解开封印已经过了整整500天",
            "flag_key": 2801,
            "check_value": 99,
        },
        "7_princess": {
            "id": "7_princess",
            "name": "菲娅 魔界公主Ending",
            "description": "菲娅成为了魔界的公主",
            "flag_key": 2807,
            "check_value": 1200,
        },
        "7_witch": {
            "id": "7_witch",
            "name": "菲娅 魔女Ending",
            "description": "菲娅成为了大魔女",
            "flag_key": 2807,
            "check_value": 2200,
        },
        "11_tsundere": {
            "id": "11_tsundere",
            "name": "黑方片 傲娇的商贾后裔Ending",
            "description": "黑方片建立了地下组织",
            "flag_key": 2811,
            "check_value": 900,
        },
        "14_ninja": {
            "id": "14_ninja",
            "name": "银黑桃 忍者组织头领Ending",
            "description": "银黑桃建立了忍者组织",
            "flag_key": 2814,
            "check_value": 900,
        },
        "14_dairy": {
            "id": "14_dairy",
            "name": "银黑桃 魔王专属乳牛Ending",
            "description": "银黑桃成为了魔王乳业的招牌",
            "flag_key": 2814,
            "check_value": 2000,
        },
        "10_godness": {
            "id": "10_godness",
            "name": "嘉德 淫乱天神Ending",
            "description": "嘉德成为了天界之主",
            "flag_key": 2810,
            "check_value": 1900,
        },
    }

    _ENDING_TEXTS = {
        "1": [
            "┌─────────────────────────────┐",
            "｜　　　　　　　　魔王终于再次掌握了世界　　　　　　　　　　｜",
            "｜　魔物们冲入皇宫，将还在熟睡中的年幼公主拖下床，抓了起来　｜",
            "｜　　　　　　而且，魔王还对人类提出了这样的要求　　　　　　｜",
            "｜　　　　　命令人类继续派出勇者到地下城来讨伐自己　　　　　｜",
            "｜　　　　　因为这样很有趣，哈哈哈哈。魔王这么说着　　　　　｜",
            "｜　　　　这些女孩实际上已经不是勇者，而是魔王的祭品　　　　｜",
            "└─────────────────────────────┘",
            "",
            "",
            "人间界已经陷落了，不过世上还有很多其它地方，要继续游戏吗？",
            "[0] - 世界这么大，我想再去看看！",
            "[1] - 我已经……不想做魔王了……",
        ],
        "2": [
            "┌─────────────────────────────┐",
            "｜　　　　　　新的女勇者，终于攻陷了魔王的地下城　　　　　　｜",
            "｜　　　　　　魔王将打倒自己的勇者的模样铭记于心　　　　　　｜",
            "｜　　　带着一丝不易察觉的微笑，再次陷入了封印的沉睡之中　　｜",
            "└─────────────────────────────┘",
            "",
            "-------------------------------GAMEOVER---------------------------------",
        ],
        "3": [
            "┌─────────────────────────────┐",
            "｜　　　　　　　　魔王终于征服了精灵族的领域　　　　　　　　｜",
            "｜　　　　于是，魔王向精灵族的长老提出了这样的要求　　　　　｜",
            "｜　　　　　　　　要求献上秘藏的精灵族圣女　　　　　　　　　｜",
            "└─────────────────────────────┘",
        ],
        "4": [
            "┌─────────────────────────────┐",
            "｜　　　　　　　　　魔王终于征服了龙族的山脉　　　　　　　　｜",
            "｜　　　　　于是，魔王向龙族的长老提出了这样的要求　　　　　｜",
            "｜　　　　　　　要求献上有着最悠久血统的龙族公主　　　　　　｜",
            "└─────────────────────────────┘",
        ],
        "5": [
            "┌─────────────────────────────┐",
            "｜　　　　　　　　　　魔王终于征服了天界　　　　　　　　　　｜",
            "｜　　　　　　　　于是，魔王向天界提出了要求　　　　　　　　｜",
            "｜　　　　　　　命令献上被选为下一代主神的天使　　　　　　　｜",
            "└─────────────────────────────┘",
        ],
        "N": [
            "自从魔王被解开封印已经过了整整500天。",
            "尽管各界源源不断地派遣勇者讨伐魔王，",
            "但都要么成为了魔王的收藏品，",
            "要么被倒卖到大陆各个龌龊的角落，",
            "要么成为了魔王力量的一部分，帮助魔王为祸人间。",
            "",
            "这块大陆的人们渐渐也习惯于魔王地下城的存在，想要寻找财富或者冒险...",
            "或者...期待着女性最本能的渴望．．．",
            "...各种心思的女孩子们，依然在源源不断地走进这个魔窟。",
            "...",
            "...",
            "大概，已经不会有尽头了吧。",
            "达成了【Normal End】。",
        ],
        "7_princess": [
            "走进菲娅房间的时候，感觉气氛有些不一样，",
            "和平时可爱的感觉不同，显得看起来正式很多，",
            "菲娅坐在钢琴面前，指尖流露出悦耳的音符来，",
            "看来是经过相当的练习了吧，弹奏的非常熟练，看来，最近几个月似乎一直都在准备的就是这个了。",
            "虽然平时怎么看都是小孩子，但是正式起来的话，果然还是看得出一点贵族的感觉。",
            "该怎么说呢……不愧是公主吗？",
            "「魔王大人……那个……怎么样……？」",
            "「这个呢……是只弹给喜欢的人听的曲子哦」",
            "「拼命，拼命练习了很久，才终于能流利的弹奏出来了呢……」",
            "「这个是……只为魔王大人……只有魔王大人才可以听的哦」",
            "菲娅靠在魔王的怀里，闭着眼睛轻轻摩蹭着",
            "「一开始来到这里的时候，觉得很可怕……不知道怎么办才好……」",
            "「但是……能遇上魔王大人……菲娅……真的很开心呢……」",
            "「不管是碰上可怕的事情也好……碰见过分的人也好……只要心里想着魔王大人……就觉得没有什么事情好怕的……」",
            "「今后……要一直，一直～和魔王大人在一起～」",
            "「因为魔王大人，是菲娅最最喜欢的人了呐～」",
            "…………",
            "……",
            "自从地上世界被完全征服已经过去了相当一段时间了，",
            "渐渐安定下来的世界，开始收拾起战争的残骸，开始重新建设起文明来。",
            "在那之中，引领着人们的，正是小小的菲娅。",
            "虽然年龄尚小，但借着菲娅的人望，原本混乱的王国渐渐聚拢起来，开始建设起新的秩序，",
            "骑士们拥立着原来的公主，在魔王的统治下开始了新的纪元。",
            "在废墟上展开的花朵，比原先开放的更加灿烂，",
            "而在史书上由历史学家们所记录的，也大多是赞颂着魔王的话语，",
            "当然，那都是后话了，",
            "现在的魔王，大概正在和菲娅享受着快乐的时光吧？",
            "～菲娅 魔界公主Ending～",
        ],
        "7_witch": [
            "「呐呐，魔王大人❤」",
            "菲娅轻轻飘了过来坐到了魔王的床边，小手里拿着透明的小瓶子，",
            "瓶子里面装着粉红色的液体，还在时不时的冒着泡泡，",
            "一眼就能看出是某种魔药吧。",
            "虽然乍一看觉得有点危险，但是直觉却令人觉得是一种很色气的药水……",
            "刚想问的时候，菲娅就已经先开口了。",
            "「这个呢……是被称作爱的魔药的东西呢。」",
            "「诶嘿嘿，据说可以让喜欢的人永远都不会分开来的魔力呢❤」",
            "「虽然花了很多功夫，不过终于还是完成了～」",
            "「所以……那个……」",
            "菲娅期待的看着这边……",
            "一番激烈的运动以后，菲娅依偎在魔王身旁，",
            "小小的身体上还残留着魔王施暴的痕迹，时不时因为高潮的余韵而微微颤抖一下。",
            "「诶嘿嘿……这样子……魔王大人和菲娅……就永远都不分开了呢❤」",
            "「菲娅……好幸福……能够遇到魔王大人，是菲娅一生最幸运的事情哟……」",
            "「因为魔王大人，是菲娅最最喜欢的人了呐～」",
            "「所以……再来一次吧……？❤」",
            "…………",
            "……",
            "自从地上世界被完全征服已经过去了相当一段时间了，",
            "动乱已经渐渐安定下来，人们开始重新建设起新的秩序来，",
            "但是仍然有些企图反抗魔王统治的愚蠢的家伙们，",
            "既然有反抗的人，自然也会有镇压的人，",
            "在那之中，有一个在天空中飞舞着的小小的身影，",
            "在自己出生的这片大地上自由的飞翔着，维护着自己心爱的人的统治，",
            "那是曾经是王国的公主的，菲娅，不过她现在的身份，是魔王手下的大魔女，",
            "在她和许多人的努力下，魔王建立起了稳固的统治，",
            "时代翻开了新的一轮篇章，",
            "当然，那都是后话了，",
            "现在的魔王，大概正在和菲娅享受着快乐的时光吧？",
            "～菲娅 魔女Ending～",
        ],
        "11_tsundere": [
            "传说有一个只效忠于魔王的地下组织",
            "传说这个组织的成员必须是中年以下的美女",
            "传说要加入这个组织需要经过地狱一般的调教考验，以及长时间的辛苦学习",
            "传说这个组织的首领是魔王的后妃",
            "传说这个组织间接的控制着世界上一半的国家",
            "但是这个被通称为『魔王的金手指』的组织，只被当做街头巷尾的笑谈而已",
            "只有极少一部分人才知道，这个组织虽然并不叫这个名字，但真的存在",
            "而民间流传的这个流言，却巧妙的让大部分人以为这个组织只是一个玩笑而已",
            "这些流言，自然是由那个组织刻意传出去的，而『魔王的金手指』这个虚假的名字，则是来源于组织的创立者和魔王交往中自己领会到的，超越了魔王的手指技巧",
            "～黑方片 傲娇的商贾后裔 Ending～",
        ],
        "14_ninja": [
            "传说有一个只效忠于魔王的地下组织",
            "传说这个组织的成员不论性别，年龄，种族，都是以一当十的精英",
            "传说要加入这个组织需要经过地狱一般的选拔与训练",
            "传说这个组织的首领是魔王的后妃",
            "传说这个组织间接的灭掉了好几个国家",
            "但是这个被通称为「魔王的无名指」，只被当做街头巷尾的笑谈而已",
            "只有极少一部分人才知道，这个组织虽然并不叫这个名字，但真的存在",
            "而民间流传的这个流言，却巧妙的让大部分人以为这个组织只是一个玩笑而已",
            "这些流言，自然是由那个组织刻意传出去的，而「魔王的无名指」这个虚伪的名字，则是来源于组织的创立者不能将戒指带在左手无名指上的小小遗憾",
            "～银黑桃 忍者组织头领 Ending～",
        ],
        "14_dairy": [
            "现在魔王乳业已经完全不用魔王费心了",
            "就连广告，银黑桃也偶尔为了满足自己的露出癖而主动去拍",
            "作为魔王军稳定的资金来源之一，魔王乳业正源源不绝的充实着你的国库",
            "后来在魔族之间的，人乳从流行慢慢变成了日常",
            "甚至出现了因为「抓一只人类自己养来产奶」这样的理由而参军的魔族",
            "不过这一切对于银黑桃来说都无关紧要",
            "对她来说，只有享受被魔王榨乳的快感才是最重要的",
            "～银黑桃 魔王专属乳牛 Ending～",
        ],
        "10_godness": [
            "---------------------嘉德淫乱Ending---------------------",
            "～嘉德 淫乱天神 Ending～",
        ],
    }


    # ------------------------------------------------------------------
    # SELL_MATURO (卖出末路口上) system
    # Based on ERB/SELL_MATURO.ERB
    # ------------------------------------------------------------------


    def _sort_character_indices(self, sort_mode: int, status_cycle: int = 0) -> List[int]:
        indices = [idx for idx in range(1, len(self.interpreter.vars.chars))]
        if sort_mode == 1400:
            return sorted(indices, key=lambda idx: (-self._get_character_money_value(self.interpreter.vars.chars[idx]), idx))
        if sort_mode == 1500:
            return sorted(indices, key=lambda idx: (-self._get_character_debt_value(self.interpreter.vars.chars[idx]), idx))
        if sort_mode == 1300:
            if status_cycle % 2 == 0:
                return sorted(indices, key=lambda idx: (self.interpreter.vars.chars[idx].cflag.get(1, 0), -self._get_character_level(self.interpreter.vars.chars[idx]), idx))
            return sorted(indices, key=lambda idx: (-self._get_character_level(self.interpreter.vars.chars[idx]), self.interpreter.vars.chars[idx].cflag.get(1, 0), idx))
        return indices


    def _spend_character_temptation_cost(self, player: Character) -> None:
        player.base[1] = int(player.base.get(1, 0)) - 2000


    def _spend_global_money(self, amount: int):
        self._add_global_money(-int(amount))


    def _split_character_from_party(self, char: Character) -> bool:
        idx = self._find_character_index(char)
        if idx <= 0:
            return False
        if int(char.cflag.get(533, 0)) <= 0:
            return False
        self._remove_character_from_party(idx)
        return True


    def _start_new_game_from_title(self) -> str:
        self._initialize_new_game_state()
        print("\n新的猎物出现了！")
        print("你作为魔王苏醒了...")
        self._pause("\n按回车继续...")
        return "SHOP"


    def _stop_train_video_recording(self, target: Character, player: Optional[Character]) -> None:
        if not self._is_train_video_recording(target):
            return
        target.cflag[498] = 0
        if player is not None:
            self._use_item(player, "水晶球魔力源")
        print("录像拍摄已结束。")


    def _summarize_life_cradle_first_experience(self, target: Character) -> str:
        code = int(target.cflag.get(15, 0))
        if code < 0:
            return "初体验对象：未设定"
        if code == 0:
            return "初体验对象：未设定"
        if code == 998:
            return "初体验对象：无"
        labels = {
            1: "魔王",
            101: "蠕虫",
            102: "触手生物",
            103: "野狗",
            104: "怪物",
            105: "狂王",
        }
        if code in labels:
            return f"初体验对象：{labels[code]}"
        template = self._get_character_template_baseline(code - 1) if code > 1 else None
        if template is not None:
            partner_name = template.name or template.callname or target.cstr.get(3, "")
            if partner_name:
                return f"初体验对象：{partner_name}"
        if code == 997 and target.cstr.get(3, ""):
            return f"初体验对象：{target.cstr[3]}"
        if code > 1 and target.cstr.get(3, ""):
            return f"初体验对象：{target.cstr[3]}"
        return "初体验对象：未设定"


    def _summarize_life_cradle_first_kiss(self, target: Character) -> str:
        code = int(target.cflag.get(16, 0))
        if code == -2:
            return "初吻对象：无"
        if code < 0:
            return "初吻对象：未设定"
        if code == 0:
            return "初吻对象：不明"
        if code == 993:
            return "初吻对象：狂王"
        if code == 994:
            return "初吻对象：怪物"
        if code == 995:
            return "初吻对象：怪物的阴茎"
        if code == 996:
            return "初吻对象：野狗的肛门"
        if code == 997:
            return "初吻对象：野狗的阴茎"
        if code == 998:
            return "初吻对象：野狗的嘴"
        if code == 999:
            return "初吻对象：触手"
        partner = target.cstr.get(4, "") or "某人"
        if code < 100:
            site = "唇"
        elif code < 300:
            site = "阴茎"
        elif code < 400:
            site = "私处"
        else:
            site = "肛门"
        return f"初吻对象：{partner}的{site}"


    def _sync_square_endcheck_route(self, char: Character, current: int) -> int:
        if char.talent.get(85, 0) == 1 and 100 <= current <= 200:
            self.interpreter.vars.globals[2811] = 10
            char.cflag[515] = 0
            return 10
        if char.talent.get(76, 0) == 1 and ((30 <= current <= 100) or (300 <= current <= 310)):
            self.interpreter.vars.globals[2811] = 110
            char.cflag[515] = 0
            return 110
        return current


    def _system_debug_out(self) -> List[str]:
        """调试输出 - SYSTEM_DEBUG_OUT.ERB"""
        output = []
        day = int(self.vars.flag.get(0, 0))
        time = int(self.vars.flag.get(1, 0))
        money = int(self.vars.flag.get(2, 0))
        output.append(f"【系统状态】Day={day}, Time={time}, MONEY={money}")
        return output

    # ------------------------------------------------------------------
    # SYSTEM_MODEINT - 模式初始化
    # ------------------------------------------------------------------


    def _system_modeint(self) -> List[str]:
        """模式初始化 - SYSTEM_MODEINT.ERB"""
        output = []
        # QUE2MK - currently returns 0
        return output

    # ------------------------------------------------------------------
    # GET_MONSTER_DATA_FULL - 完整怪物数据
    # ------------------------------------------------------------------


    def _target_has_blocking_modes(self, target: Character) -> bool:
        return bool(target.talent.get(122, 0) or target.talent.get(135, 0))


    def _toggle_bit(self, val: int, bit: int) -> int:
        """Toggle a specific bit in a value."""
        return val ^ (1 << bit)


    def _toggle_flag_bit(self, flag_idx: int, bit: int) -> bool:
        value = self.interpreter.vars.get_flag(flag_idx, 0)
        updated = value ^ (1 << bit)
        self.interpreter.vars.set_flag(flag_idx, updated)
        return bool(updated & (1 << bit))


    def _toggle_mod_switch(self, mod_bit: int) -> None:
        """Toggle a MOD bit in EX_FLAG:9000 with special handling."""
        g = self.interpreter.vars.globals
        ex_flag_9000 = int(g.get(9000, 0))

        # Toggle the bit
        ex_flag_9000 = self._toggle_bit(ex_flag_9000, mod_bit)
        g[9000] = ex_flag_9000

        # Special handling for bit 0 (银行)
        if mod_bit == 0:
            debt = int(g.get(9003, 0))
            if debt > 0:
                if self._get_bit(ex_flag_9000, 0):
                    # Bank turned ON with debt: add debt to MONEY
                    self.interpreter.vars.money += debt
                    g[4444] = int(g.get(4444, 0)) + debt
                else:
                    # Bank turned OFF with debt: subtract debt from MONEY
                    self.interpreter.vars.money -= debt
                    g[4444] = int(g.get(4444, 0)) - debt

        # Special handling for bit 2 (打工)
        if mod_bit == 2:
            chars = self.interpreter.vars.chars
            if self._get_bit(ex_flag_9000, 2):
                # 打工 ON: sync CFLAG:120 -> EX_CFLAG:400
                for ch in chars:
                    ex_cflag = getattr(ch, 'ex_cflag', None)
                    if ex_cflag is None:
                        ex_cflag = {}
                        setattr(ch, 'ex_cflag', ex_cflag)
                    ex_cflag[400] = int(ch.cflag.get(120, 0))
            else:
                # 打工 OFF: sync EX_CFLAG:400 -> CFLAG:120
                for ch in chars:
                    ex_cflag = getattr(ch, 'ex_cflag', {})
                    ch.cflag[120] = int(ex_cflag.get(400, 0))


    def _update_training_heat_counter(self, target: Character, palam_id: int, cflag_id: int) -> None:
        current = int(target.palam.get(palam_id, 0))
        if current >= 10000:
            target.cflag[cflag_id] = int(target.cflag.get(cflag_id, 0)) + current // 10000
        else:
            target.cflag[cflag_id] = 0


    def _video_backup(self, title: str) -> None:
        self._append_video_to_shelf(title)


    def do_rest(self):
        """Rest by ending the turn with the special tax bonus."""
        self._apply_rest_turn_end()


    def do_save(self):
        """Save game"""
        self._show_save_game_menu()


    def run(self):
        """Main game loop"""
        self._bootstrap_game_runtime()
        self._run_game_state_loop()
        print("\nThanks for playing eraMaouEx Python!")


    def run_title(self):
        """Run title screen"""
        self._render_title_screen()
        choice = self._prompt_title_choice()
        return self._handle_title_choice(choice)


    def show_communication(self):
        """MAOUNET communication menu based on the original ERB flow."""
        while True:
            if self._advance_communication_menu():
                return


    def show_summon(self):
        """Monster summon shop aligned to SHOP_MONSTER.ERB."""
        while True:
            if self._advance_summon_menu():
                return

