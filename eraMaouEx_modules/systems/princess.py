from __future__ import annotations
"""Module for PrincessMixin - 公主/结局系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class PrincessMixin:
    """Mixin providing 公主/结局系统 methods for GameEngine"""

    def _advance_princess_black_route(self, char: Character, current: int, favor: int):
        self._route_princess_black_stage(char, current, favor)






    def _advance_princess_prompt_stage(self, stage: int) -> None:
        current_stage = int(self.interpreter.vars.globals.get(2807, 0))
        if current_stage == stage:
            self.interpreter.vars.globals[2807] = stage + 1






    def _advance_princess_story_after_ending_prompt(self) -> None:
        current_stage = int(self.interpreter.vars.globals.get(2807, 0))
        if current_stage in (120, 220):
            self.interpreter.vars.globals[2807] = current_stage + 1






    def _advance_princess_white_route(self, char: Character, current: int, favor: int):
        if 10 <= current < 20:
            self._advance_princess_white_route_10_to_20(char)
        elif 20 <= current < 30:
            self._advance_princess_white_route_20_to_30(char)
        elif 30 <= current < 60:
            self._advance_princess_white_route_30_to_60(char, current, favor)
        elif 60 <= current < 70:
            self._advance_princess_white_route_60_to_70(char)
        elif 70 <= current < 120:
            self._advance_princess_white_route_waiting(char, current)






    def _advance_princess_white_route_10_to_20(self, char: Character) -> None:
        obedience_mark = int(char.mark.get(1, 0))
        pain_mark = int(char.mark.get(2, 0))
        if obedience_mark == 3 and char.talent.get(0, 0):
            self.interpreter.vars.globals[2807] = 20
        elif (obedience_mark == 3 or pain_mark == 3) and char.talent.get(0, 0) == 0:
            self.interpreter.vars.globals[2807] = -10






    def _advance_princess_white_route_20_to_30(self, char: Character) -> None:
        if char.talent.get(85, 0) == 1:
            self.interpreter.vars.globals[2807] = 30
        elif char.talent.get(76, 0) == 1:
            self.interpreter.vars.globals[2807] = 130






    def _advance_princess_white_route_30_to_60(self, char: Character, current: int, favor: int) -> None:
        if current < 40 and favor >= 2000:
            self.interpreter.vars.globals[2807] = 40
        elif current < 50 and favor >= 5000:
            self.interpreter.vars.globals[2807] = 50
        elif current < 60 and favor >= 10000:
            self.interpreter.vars.globals[2807] = 60






    def _advance_princess_white_route_60_to_70(self, char: Character) -> None:
        if int(char.cflag.get(601, 0)) == 901:
            self.interpreter.vars.globals[2807] = 70
            char.cflag[515] = 0






    def _advance_princess_white_route_waiting(self, char: Character, current: int) -> None:
        wait_targets = {
            70: (10, 80),
            80: (30, 90),
            90: (60, 100),
            100: (100, 110),
            110: (150, 120),
        }
        for start, (wait, next_stage) in wait_targets.items():
            if start <= current < start + 10 and self._advance_story_wait_counter(char, wait, next_stage):
                self.interpreter.vars.globals[2807] = next_stage
                return






    def _apply_princess_endcheck(self, char: Character):
        current = int(self.interpreter.vars.globals.get(2807, 0))
        favor = int(char.cflag.get(2, 0))
        current = self._sync_princess_endcheck_route(char, current)
        self._advance_princess_white_route(char, current, favor)
        self._advance_princess_black_route(char, current, favor)






    def _apply_princess_ending_stage_effects(self, stage: int) -> None:
        char = self._find_character_by_template_id(35)
        if char is None:
            return
        if stage == 70:
            char.talent[1254] = 1
        elif stage == 170:
            char.talent[1253] = 1
            char.cflag[11] = int(char.cflag.get(11, 0)) + 200
            char.cflag[12] = int(char.cflag.get(12, 0)) + 200






    def _apply_princess_ending_stage_output(self, messages: List[str], stage: int, event_key: str) -> None:
        for line in self._build_princess_event_lines(stage):
            messages.append(line)
        self._apply_princess_ending_stage_effects(stage)
        self._mark_ending_event_seen(event_key)
        if stage == -10:
            self.interpreter.vars.globals[2807] = -11






    def _build_princess_event_lines(self, stage: int) -> List[str]:
        return self._build_stage_lines(stage, self._build_princess_event_stage_lines())






    def _build_princess_event_stage_lines(self) -> Dict[int, List[str]]:
        return {
            **self._build_princess_event_stage_lines_early(),
            **self._build_princess_event_stage_lines_middle(),
            **self._build_princess_event_stage_lines_late(),
        }






    def _build_princess_event_stage_lines_early(self) -> Dict[int, List[str]]:
        return {
            **self._build_princess_event_stage_lines_early_intro(),
            **self._build_princess_event_stage_lines_early_affection(),
        }






    def _build_princess_event_stage_lines_early_affection(self) -> Dict[int, List[str]]:
        return {
            40: [
                "「魔王大人，今天也是个好天气呢～」",
                "菲娅看着窗外，轻轻朝你打招呼，晨风吹起了她的发梢与衣角。",
                "她红着脸小声说昨晚又梦到了你，至于梦的内容则神秘地表示要保密。",
                "那副调皮模样里，已经能清楚看出她对你的依恋。",
            ],
            50: [
                "「魔王大人……那个……菲娅……试着做了点心……」",
                "她有些扭捏地端着盘子，里面放着心形的小甜饼。",
                "虽然做得有些简陋，但对她来说大概已经是鼓足勇气后的成果了。",
                "「怎，怎么样……味道……？」",
            ],
            60: [
                "「魔王大人～❤」",
                "菲娅扑过来紧紧抱住你，深深吸了一口气，像是在贪恋你身上的味道。",
                "看着那双装满幸福的眼睛，你很清楚她已经完全离不开你了。",
                "银色戒指在她纤细的手指上闪闪发亮，而她也终于走到了想和你继续更远的地方。",
            ],
        }






    def _build_princess_event_stage_lines_early_intro(self) -> Dict[int, List[str]]:
        return {
            10: [
                "菲娅在床上迷糊地看着四周，似乎还没搞清楚自己如今的处境。",
                "一下子被丢进这样陌生的环境里，会迷茫也是理所当然的。",
                "而已经将她人生彻底握在手里的你，只是透过水晶球静静俯视着她。",
                "接下来……该怎么处置她好呢？",
            ],
            20: [
                "「啊，魔王大人～♪」",
                "看见你出现，菲娅啪嗒啪嗒地迎了过来。",
                "「呐呐，今天也要一起玩吗？」",
            ],
        }






    def _build_princess_event_stage_lines_late(self) -> Dict[int, List[str]]:
        return {
            140: [
                "「啊，魔王大人～」",
                "满脸绯红的菲娅在路上拦住了你，直白地说自己从早上开始就一直想和你做H的事情。",
                "看那个样子，她大概已经湿得一塌糊涂了吧。",
                "今天就好好玩弄她一下，似乎也不错。",
            ],
            150: [
                "「嗯……啾……呼哈……」",
                "只是早餐时想坐在你怀里，回过神来就已经变成了唇舌交缠的气氛。",
                "双手在她幼小而柔软的身体上游走时，那股奇妙诱惑力反而越来越强。",
                "你们度过了一段彻底染上粉红色的早餐时间。",
            ],
            160: [
                "「诶嘿嘿……肚子里面……还是黏糊糊的呢，感觉好舒服～」",
                "菲娅依偎在你怀里，泛着粉色的小脸上流露出与年龄不符的色欲。",
                "对如今的她来说，只要能和你做H的事情，就已经是最大的满足。",
                "因为对菲娅来说，你早已是一切。",
            ],
            170: [
                "「啊啊，魔王大人～」",
                "菲娅兴冲冲地跑来告诉你，她已经开始学习魔法了。",
                "她想为你做些什么，也想在努力之后得到你用H来发放的奖励。",
                "菲娅获得了素质【魔女】。",
                "攻击力和防御力增加了！",
            ],
            180: [
                "「魔王大人……❤」",
                "菲娅趴在你身上，任由你玩弄，一边索要属于努力后的奖赏。",
                "她主动脱下已经黏糊糊的胖次，满心期待着接下来的奖励。",
                "你顺势将她压在身下，开始了新的欢爱。",
            ],
            190: [
                "走廊上，你看见菲娅从一旁轻快地飞了过去。",
                "她已经能很熟练地运用魔法，甚至还特意在你面前展示飞行姿势。",
                "看得出来，她在这方面确实相当有天赋。",
                "今后也许能成为很有用的家伙吧。",
            ],
            200: [
                "「啊，魔王大人，那个……菲娅稍微出去一下哦～」",
                "最近她似乎总在背着你收集素材，不找她的时候常常一整天不见踪影。",
                "屋子里也堆起了各种奇怪材料，多半是在折腾魔药一类的东西。",
                "虽说如此……似乎还是有些太频繁了，下次得好好说教一下才行。",
            ],
            210: [
                "「诶？菲娅在做什么吗？」",
                "你好不容易在她正要出门的时候把人逮了个正着。",
                "她撒着娇说现在还不能告诉你，但绝对不是坏东西。",
                "说完又亲了你一下，强调那是为了最喜欢的魔王大人而准备的。",
            ],
            220: [
                "「呐呐，魔王大人❤」",
                "菲娅轻轻飘到你床边，拿着装满粉色液体、不断冒泡的小瓶子。",
                "她说那是被称作爱的魔药，能让喜欢的人永远都不分开。",
                "在一番激烈运动之后，她依偎在你身边，幸福地说能够遇见你就是一生中最幸运的事。",
                "后来，这位曾经的公主也以大魔女的身份飞舞在天空，守护着你亲手建立的秩序。",
                "～菲娅 魔女 Ending～",
            ],
        }






    def _build_princess_event_stage_lines_middle(self) -> Dict[int, List[str]]:
        return {
            **self._build_princess_event_stage_lines_middle_growth(),
            **self._build_princess_event_stage_lines_middle_endings(),
        }






    def _build_princess_event_stage_lines_middle_endings(self) -> Dict[int, List[str]]:
        return {
            110: [
                "路过菲娅房间的时候，你听见了悦耳的琴声。",
                "出于好奇朝里面看去，只见她闭着眼在钢琴上努力练习着。",
                "中途虽然偶尔弹错，但她很快又鼓起劲继续演奏起来。",
                "……暂时还是不要打搅她了吧。",
            ],
            120: [
                "走进菲娅房间的时候，感觉气氛有些不一样。",
                "她坐在钢琴前，为你一个人弹奏起准备了很久的曲子，然后靠进你怀里坦率诉说一路走来的不安与依恋。",
                "在废墟上逐渐重建的新秩序里，这位曾经的公主最终也成了属于你的新纪元象征之一。",
                "而现在的你，大概正和菲娅一起享受着只属于彼此的快乐时光吧。",
                "～菲娅 魔界公主 Ending～",
            ],
        }






    def _build_princess_event_stage_lines_middle_growth(self) -> Dict[int, List[str]]:
        return {
            70: [
                "「魔王大人。」",
                "菲娅难得穿得十分正式，认真告诉你她终于也想为你做些真正有用的事情。",
                "在已被你支配的国家里，原本身为公主的她很自然地被重新接纳，开始以新的身份协助你的统治。",
                "菲娅获得了素质【魔界公主】。",
                "从地上掠夺的资金增加了，而且可以获得兵员了。",
            ],
            80: [
                "「啊，魔王大人～～」",
                "正式成为魔界公主后已经过了一些日子，可菲娅一见到你还是会像从前那样扑过来撒娇。",
                "她嘴上抱怨着最近忙起来后少了很多和你玩乐的时间。",
                "不过看那副黏人的样子，果然终究还是个小孩子。",
            ],
            90: [
                "「呼……呼……」",
                "菲娅轻轻吹着还在冒热气的奶茶，旁边的女仆静静服侍着。",
                "刚显出一点优雅气质，她转眼又因为见到你而慌乱起来。",
                "和她一起度过这样一段温温软软的休息时间，似乎也很不错。",
            ],
            100: [
                "最近菲娅似乎在偷偷摸摸准备着什么。",
                "被问起来时，她只会红着脸说是为了你准备的秘密。",
                "亲了你一下后，她就啪嗒啪嗒地跑开了。",
                "总之先这样放着不管吧。",
            ],
        }






    def _build_princess_stage_20_choice_lines(self, choice: int) -> List[str]:
        if choice == 1:
            return [
                "「哇～魔王大人最好了～那，菲娅先去房间里了哦～♪」",
                "菲娅蹦蹦跳跳地走掉了，看起来很开心的样子。",
                "看起来她已经完全适应这里的生活了。",
            ]
        return [
            "「啊唔唔……魔王大人今天很忙吗……这样啊……」",
            "「那，菲娅会乖乖地等着的哦……」",
            "看起来她也已经慢慢适应了这里的生活。",
        ]






    def _build_princess_stage_50_choice_lines(self, choice: int) -> List[str]:
        if choice == 3:
            return [
                "「……啊～那样的话太好了」",
                "菲娅看起来很开心的样子。",
            ]
        return [
            "「这，这样啊……虽然努力练习过了……果然还是不行吗……」",
            "菲娅看起来相当沮丧。",
        ]






    def _build_princess_witch_potion_choice_lines(self, choice: str) -> Optional[List[str]]:
        if choice == "5":
            return [
                "药水并不多，只一小口就全部喝干净了。",
                "并没有什么不适，只是总觉得身体慢慢热了起来。",
                "大概是做成了媚药一类的东西吧，不过，也没什么不好的。",
                "你顺势把菲娅按倒在床上，扯开了她的衣服……",
            ]
        if choice == "6":
            return [
                "「不，不要喝吗……？」",
                "「诶？即使不用这种东西，菲娅也是魔王大人的……怎，怎么这样……这种事……太犯规了啦……」",
                "听见话语的菲娅愣了一下，豆大的泪珠涌出了眼眶，顺着白皙的脸颊滑了下来。",
                "小小的身体扑在你身上大声哭了起来，而你也只好轻轻抚摸着她的头安慰她。",
                "虽然有点不像自己的风格，不过偶尔这样也不坏呢……",
            ]
        if choice == "7":
            return [
                "打开瓶子以后，趁着菲娅不注意，你把药统统喂进了她嘴里。",
                "「咕咳咳……？！魔，魔王大人……突然就这么粗暴的……」",
                "「呼啊啊……身体……怎么……好热呢……❤」",
                "看着皮肤泛起粉色的菲娅，只是把她揽进怀里，就已经让她娇喘连连。",
                "大概是做成了媚药一类的东西吧，你顺势让她趴在自己身上，扯开了衣服……",
            ]
        return None






    def _get_princess_black_next_stage(self, char: Character, current: int, favor: int) -> Optional[int]:
        return self._resolve_princess_black_next_stage(char, current, favor)






    def _get_princess_ending_event_key(self, stage: int) -> Optional[str]:
        stage_to_key = {
            -10: "ending_princess_bad_end",
            10: "ending_princess_intro_10",
            20: "ending_princess_intro_20",
            30: "ending_princess_branch_love",
            40: "ending_princess_scene_40",
            50: "ending_princess_scene_50",
            60: "ending_princess_scene_60",
            70: "ending_princess_scene_70",
            80: "ending_princess_scene_80",
            90: "ending_princess_scene_90",
            100: "ending_princess_scene_100",
            110: "ending_princess_scene_110",
            120: "ending_princess_scene_120",
            130: "ending_princess_branch_corruption",
            140: "ending_princess_scene_140",
            150: "ending_princess_scene_150",
            160: "ending_princess_scene_160",
            170: "ending_princess_scene_170",
            180: "ending_princess_scene_180",
            190: "ending_princess_scene_190",
            200: "ending_princess_scene_200",
            210: "ending_princess_scene_210",
            220: "ending_princess_scene_220",
        }
        return stage_to_key.get(stage)






    def _process_princess_ending_events(self, messages: List[str]):
        stage = int(self.interpreter.vars.globals.get(2807, 0))
        event_key = self._get_princess_ending_event_key(stage)
        if not event_key or self._has_seen_ending_event(event_key):
            return
        if self._queue_princess_ending_prompt(stage, event_key):
            return
        self._apply_princess_ending_stage_output(messages, stage, event_key)






    def _prompt_princess_ending_choice(self, event_key: str):
        print("可以达成菲娅的魔界公主结局，想要进入这个结局吗？")
        print(" [1] 好的")
        print(" [2] 还是算了")
        print(" [3] 明天再问我")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                for line in self._build_princess_event_lines(120):
                    print(line)
                self._advance_princess_story_after_ending_prompt()
                self._apply_story_ending_main_completion()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("好吧，菲娅尊重你的选择哦。")
                self._advance_princess_story_after_ending_prompt()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("可以哦，明天会继续问你的。")
                self._pause()
                return






    def _prompt_princess_stage_20_choice(self, event_key: str) -> None:
        for line in self._build_princess_event_lines(20):
            print(line)
        print(" [1] 点头")
        print(" [2] 摇头")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                for line in self._build_princess_stage_20_choice_lines(1):
                    print(line)
                self._mark_ending_event_seen(event_key)
                self._advance_princess_prompt_stage(20)
                self._pause()
                return
            if choice == "2":
                for line in self._build_princess_stage_20_choice_lines(2):
                    print(line)
                self._mark_ending_event_seen(event_key)
                self._advance_princess_prompt_stage(20)
                self._pause()
                return






    def _prompt_princess_stage_50_choice(self, event_key: str) -> None:
        for line in self._build_princess_event_lines(50):
            print(line)
        print(" [3] 好吃！")
        print(" [4] 不怎么好吃")
        while True:
            choice = self._prompt_choice()
            if choice == "3":
                for line in self._build_princess_stage_50_choice_lines(3):
                    print(line)
                self._mark_ending_event_seen(event_key)
                self._advance_princess_prompt_stage(50)
                self._pause()
                return
            if choice == "4":
                for line in self._build_princess_stage_50_choice_lines(4):
                    print(line)
                self._mark_ending_event_seen(event_key)
                self._advance_princess_prompt_stage(50)
                self._pause()
                return






    def _prompt_princess_witch_ending_choice(self, event_key: str):
        print("可以达成菲娅的魔女结局，想要进入这个结局吗？")
        print(" [1] 好的")
        print(" [2] 还是算了")
        print(" [3] 明天再问我")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                self._prompt_princess_witch_potion_choice()
                for line in self._build_princess_event_lines(220):
                    print(line)
                self._advance_princess_story_after_ending_prompt()
                self._apply_story_ending_main_completion()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("好吧，菲娅尊重你的选择哦。")
                self._advance_princess_story_after_ending_prompt()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("可以哦，明天会继续问你的。")
                self._pause()
                return






    def _prompt_princess_witch_potion_choice(self) -> None:
        print("菲娅拿出了自己完成的爱的魔药，你要怎么做？")
        print(" [5] 喝掉")
        print(" [6] 不喝")
        print(" [7] 喂菲娅喝")
        while True:
            choice = self._prompt_choice()
            prelude = self._build_princess_witch_potion_choice_lines(choice)
            if prelude is None:
                continue
            for line in prelude:
                print(line)
            return






    def _queue_princess_ending_prompt(self, stage: int, event_key: str) -> bool:
        if stage == 20:
            self._queue_post_message_action({"kind": "princess_stage_20_prompt", "event_key": event_key})
            return True
        if stage in (30, 130):
            branch_name = "菲娅恋慕线" if stage == 30 else "菲娅淫乱线"
            self._queue_post_message_action(
                {
                    "kind": "story_branch_prompt",
                    "event_key": event_key,
                    "global_flag": 2807,
                    "main_flag_delta": 2,
                    "lines": self._build_story_branch_prompt(branch_name, "菲娅！！菲娅！！", "不好萝莉这口！"),
                }
            )
            return True
        if stage == 50:
            self._queue_post_message_action({"kind": "princess_stage_50_prompt", "event_key": event_key})
            return True
        if stage == 120:
            self._queue_post_message_action({"kind": "princess_ending_prompt", "event_key": event_key})
            return True
        if stage == 220:
            self._queue_post_message_action({"kind": "princess_witch_ending_prompt", "event_key": event_key})
            return True
        return False






    def _resolve_princess_black_next_stage(self, char: Character, current: int, favor: int) -> Optional[int]:
        if 130 <= current < 140 and favor >= 2000:
            return 140
        if 140 <= current < 150 and favor >= 5000:
            return 150
        if 150 <= current < 160 and favor >= 10000:
            return 160
        if 170 <= current < 180 and self._advance_story_wait_counter(char, 10, 180):
            return 180
        if 180 <= current < 190 and self._advance_story_wait_counter(char, 30, 190):
            return 190
        if 190 <= current < 200 and self._advance_story_wait_counter(char, 60, 200):
            return 200
        if 200 <= current < 210 and self._advance_story_wait_counter(char, 100, 210):
            return 210
        if 210 <= current < 220 and self._advance_story_wait_counter(char, 150, 220):
            return 220
        return None






    def _route_princess_black_stage(self, char: Character, current: int, favor: int):
        next_stage = self._get_princess_black_next_stage(char, current, favor)
        if next_stage is not None:
            self.interpreter.vars.globals[2807] = next_stage






    def _sync_princess_endcheck_route(self, char: Character, current: int) -> int:
        if current == 0:
            self.interpreter.vars.globals[2807] = 10
            return 10
        if char.talent.get(85, 0) == 1 and current >= 130:
            self.interpreter.vars.globals[2807] = 30
            char.cflag[515] = 0
            return 30
        if char.talent.get(76, 0) == 1 and 30 <= current <= 130:
            self.interpreter.vars.globals[2807] = 130
            char.cflag[515] = 0
            return 130
        return current





