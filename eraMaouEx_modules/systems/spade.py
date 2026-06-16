from __future__ import annotations
"""Module for SpadeMixin - 黑桃系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SpadeMixin:
    """Mixin providing 黑桃系统 methods for GameEngine"""

    def _advance_spade_endcheck_godness_early_route(self, char: Character, current: int, favor: int) -> None:
        if favor >= 2000 and current < 10:
            self.interpreter.vars.globals[2814] = 110
            char.cflag[515] = 0
        elif 110 <= current < 120 and favor >= 5000:
            self.interpreter.vars.globals[2814] = 120






    def _advance_spade_endcheck_godness_late_route(self, char: Character, current: int) -> None:
        if 150 <= current < 160 and self._advance_story_wait_counter(char, 10, 160):
            self.interpreter.vars.globals[2814] = 160
        elif 160 <= current < 170 and self._advance_story_wait_counter(char, 30, 170):
            self.interpreter.vars.globals[2814] = 170
        elif 170 <= current < 180 and self._advance_story_wait_counter(char, 60, 180):
            self.interpreter.vars.globals[2814] = 180
        elif 180 <= current < 190 and self._advance_story_wait_counter(char, 100, 190):
            self.interpreter.vars.globals[2814] = 190
        elif 190 <= current < 200 and self._advance_story_wait_counter(char, 150, 200):
            self.interpreter.vars.globals[2814] = 200






    def _advance_spade_endcheck_godness_middle_route(self, char: Character, current: int, favor: int) -> None:
        if 120 <= current < 130:
            if self._advance_story_wait_counter(char, 2, 130):
                self.interpreter.vars.globals[2814] = 130
        elif 130 <= current < 140 and favor >= 10000:
            self.interpreter.vars.globals[2814] = 140
        elif 140 <= current < 150:
            if (
                int(char.abl.get(1, 0)) == 10
                and int(char.abl.get(17, 0)) == 5
                and char.talent.get(78, 0) == 1
                and char.talent.get(0, 0) == 0
            ):
                self.interpreter.vars.globals[2814] = 150
                char.cflag[515] = 0






    def _apply_spade_departure_leave(self, event_key: str):
        print("「是，我会提着狂王的头回来的。」")
        print("然而你并不知道，这会是银黑桃留给你的最后一句话。")
        self.interpreter.vars.globals[2814] = 300
        self._remove_character_by_template_id(21)
        self._mark_ending_event_seen(event_key)
        self._pause()






    def _apply_spade_departure_stay(self, event_key: str):
        for line in [
            "「我很高兴您会担心我的安全，但是只要能……不管我怎么说，您都不会改变主意吧。」",
            "银黑桃叹了口气。",
            "「既然如此，在我获得能确实除掉狂王的力量之前，这个计划就暂时停止吧。」",
            "「在此期间，请您允许我继续守护在您的身边，同时允许我收集关于狂王的情报。」",
            "她告退离开前，似乎还低声念叨起了把旧部重新挖回来的事情。",
        ]:
            print(line)
        spade = self._find_character_by_template_id(21)
        if spade is not None:
            spade.talent[82] = 0
            spade.talent[474] = 1
            spade.talent[472] = 1
            spade.cflag[11] = int(spade.cflag.get(11, 0)) + 200
            spade.cflag[12] = int(spade.cflag.get(12, 0)) + 200
            spade.base[0] = int(spade.base.get(0, 0)) + 1000
            spade.base[1] = int(spade.base.get(1, 0)) + 1000
        self.interpreter.vars.globals[2814] = 51
        self._mark_ending_event_seen(event_key)
        self._pause()






    def _apply_spade_endcheck(self, char: Character, messages: List[str]):
        current = int(self.interpreter.vars.globals.get(2814, 0))
        favor = int(char.cflag.get(2, 0))
        self._apply_spade_endcheck_income(current, messages)
        current = self._apply_spade_endcheck_route_sync(char, current)
        self._apply_spade_endcheck_fia_route(char, current, favor)
        self._apply_spade_endcheck_godness_route(char, current, favor)






    def _apply_spade_endcheck_fia_route(self, char: Character, current: int, favor: int):
        if char.talent.get(85, 0) != 1:
            return
        if favor >= 2000 and current < 10:
            self.interpreter.vars.globals[2814] = 10
        elif 10 <= current < 20 and favor >= 5000:
            self.interpreter.vars.globals[2814] = 20
        elif 20 <= current < 30 and favor >= 10000:
            self.interpreter.vars.globals[2814] = 30
        elif 30 <= current < 40 and int(char.abl.get(10, 0)) + int(char.abl.get(16, 0)) >= 14:
            self.interpreter.vars.globals[2814] = 40
            char.cflag[515] = 0
        elif 40 <= current < 50 and self._advance_story_wait_counter(char, 10, 50):
            self.interpreter.vars.globals[2814] = 50
        elif 50 <= current < 60 and self._advance_story_wait_counter(char, 30, 60):
            self.interpreter.vars.globals[2814] = 60
        elif 60 <= current < 70 and self._advance_story_wait_counter(char, 60, 70):
            self.interpreter.vars.globals[2814] = 70
        elif 70 <= current < 80 and self._advance_story_wait_counter(char, 100, 80):
            self.interpreter.vars.globals[2814] = 80
        elif 80 <= current < 90 and self._advance_story_wait_counter(char, 150, 90):
            self.interpreter.vars.globals[2814] = 90
        elif current == 300 and self._advance_story_wait_counter(char, 10, 310):
            self.interpreter.vars.globals[2814] = 310






    def _apply_spade_endcheck_godness_route(self, char: Character, current: int, favor: int):
        if char.talent.get(76, 0) != 1:
            return
        if current < 120:
            self._advance_spade_endcheck_godness_early_route(char, current, favor)
        elif 120 <= current < 150:
            self._advance_spade_endcheck_godness_middle_route(char, current, favor)
        elif 150 <= current < 200:
            self._advance_spade_endcheck_godness_late_route(char, current)






    def _apply_spade_endcheck_income(self, current: int, messages: List[str]):
        if current < 151:
            return
        income = max(0, (current - 140) // 10) * random.randint(200, 399)
        if income > 0:
            self._add_global_money(income)
            messages.append(f"银黑桃乳业带来了 {income} 金收入。")






    def _apply_spade_endcheck_route_sync(self, char: Character, current: int) -> int:
        if char.talent.get(85, 0) == 1 and 110 <= current <= 200:
            self.interpreter.vars.globals[2814] = 30
            char.cflag[515] = 0
            return 30
        if char.talent.get(76, 0) == 1 and 30 <= current <= 100:
            self.interpreter.vars.globals[2814] = 110
            char.cflag[515] = 0
            return 110
        return current






    def _apply_spade_ending_stage_150_effect(self) -> None:
        char = self._find_character_by_template_id(21)
        if char is None:
            return
        char.talent[82] = 0
        char.talent[108] = 1
        char.talent[114] = 1
        char.talent[89] = 1






    def _apply_spade_ending_stage_effects(self, stage: int) -> None:
        char = self._find_character_by_template_id(21)
        if char is None:
            if stage == 310:
                self.interpreter.vars.globals[2814] = 0
            return
        if stage in (20, 50, 110):
            self._apply_spade_shared_bed_exp(char)
        elif stage == 150:
            self._apply_spade_ending_stage_150_effect()






    def _apply_spade_ending_stage_output(self, messages: List[str], stage: int, event_key: str) -> None:
        for line in self._build_spade_event_lines(stage):
            messages.append(line)
        self._apply_spade_ending_stage_effects(stage)
        if stage == 310:
            self.interpreter.vars.globals[2814] = 0
        self._mark_ending_event_seen(event_key)






    def _apply_spade_shared_bed_exp(self, char: Character) -> None:
        char.exp[35] = int(char.exp.get(35, 0)) + 10
        char.exp[34] = int(char.exp.get(34, 0)) + 15
        char.exp[20] = int(char.exp.get(20, 0)) + 10
        if int(char.talent.get(0, 0)) == 0:
            char.exp[0] = int(char.exp.get(0, 0)) + 10






    def _build_spade_event_lines(self, stage: int) -> List[str]:
        return self._build_stage_lines(stage, self._build_spade_event_stage_lines())






    def _build_spade_event_stage_lines(self) -> Dict[int, List[str]]:
        return {
            **self._build_spade_event_stage_lines_early(),
            **self._build_spade_event_stage_lines_middle(),
            **self._build_spade_event_stage_lines_late(),
        }






    def _build_spade_event_stage_lines_early(self) -> Dict[int, List[str]]:
        return {
            **self._build_spade_event_stage_lines_early_trust(),
            **self._build_spade_event_stage_lines_early_recruitment(),
        }






    def _build_spade_event_stage_lines_early_recruitment(self) -> Dict[int, List[str]]:
        return {
            50: [
                "银黑桃带来了一排同族忍者，说他们愿意一同投奔魔王麾下。",
                "你顺势和她谈起组建魔族忍者部队的构想。",
                "而她在被你公主抱起时，比起惊讶反而更快意识到你真正想去的地方。",
                "训练与奖励，从这时起都变得更加名正言顺了。",
            ],
            60: [
                "训练场里，各种被推荐来的『精英』正在等待最后测试。",
                "银黑桃嘴角带笑，眼神里却看不见一丝笑意。",
                "她保证那些不能用的人会自己放弃，不会给你添麻烦。",
                "当天晚些时候，不时有连哀嚎都发不出来的落榜者被担架抬出训练场。",
            ],
            70: [
                "偶然问起忍者部队的近况时，银黑桃说已经有几个人快能正式派上用场了。",
                "她顺口又提起要不要去取狂王首级，但语气里早已没了最初那份执拗。",
                "你知道这更多只是撒娇的一种方式。",
                "可惜这天之后你已经另有安排，不然调教时间大概又会提前开始。",
            ],
            80: [
                "仅仅三个月，忍者部队就已经开始发挥作用。",
                "曾参与暗杀你的魔族贵族身首异处，支持狂王的人类国王情报也被陆续送来。",
                "而最大功臣的银黑桃，此时正缠在你怀里露出幸福的睡脸。",
                "她手上那只不妨碍行动的手镯，像极了替代戒指的小小执念。",
            ],
        }






    def _build_spade_event_stage_lines_early_trust(self) -> Dict[int, List[str]]:
        return {
            10: [
                "「明天见，魔王大人。」",
                "银黑桃依旧恭敬地行礼离开，而你也承认自己还没有完全信任这个前近卫。",
                "然而窗外忽然传来的动静让你看见她正拖着刺客的尸体离开。",
                "看来真正信任她的日子，并没有你想象中那么遥远。",
            ],
            20: [
                "早上醒来时，银黑桃不知从哪里冒出来，为你拿来了更换的衣物。",
                "不知不觉间，你已经开始习惯把这种贴身服侍交给她。",
                "这大概就是完全信任她的证明吧。",
                "而这种信任，很快也自然地转化成了更私密的占有。",
            ],
            30: [
                "路过训练场时，正好遇见了刚结束训练的银黑桃。",
                "你只是摸了摸她的头，她就从惊讶慢慢变成了像被顺毛的小猫一样放松。",
                "她匆匆告退时脸上残留的那抹红晕，已经把许多心事都暴露了出来。",
                "下次该怎么疼爱她，你已经忍不住开始思考了。",
            ],
            40: [
                "银黑桃认真地请求你允许她去暗杀狂王。",
                "她说自己愿意冒任何风险，只要能替你除去这个心头之患。",
                "这也是她最近疯狂锻炼自己的理由。",
                "恐怕这就是她长时间独自训练的理由，而接下来要怎么回应她，全看你的决定。",
            ],
        }






    def _build_spade_event_stage_lines_late(self) -> Dict[int, List[str]]:
        return {
            **self._build_spade_event_stage_lines_late_milk(),
            **self._build_spade_event_stage_lines_late_farm(),
        }






    def _build_spade_event_stage_lines_late_farm(self) -> Dict[int, List[str]]:
        return {
            190: [
                "如今银黑桃已经彻底成了『魔王乳业』的招牌。",
                "随着生产走上正轨，她反而有了更多空闲，于是又开始监视你。",
                "不过和几个月前不同，只要你一个暗示，她就会立刻现身并主动奉上胸部解渴。",
                "唯一的问题是，她原本的忍者技术大概已经再也无法像最初那样派上用场了。",
            ],
            200: [
                "今天你一时兴起去视察人乳农场，银黑桃则乖乖跟在身边。",
                "看着成排被固定榨乳的女性，她露出了毫不掩饰的羡慕神色。",
                "而作为魔王乳业的招牌与专属乳牛，她当然不会被你和那些『劣等乳牛』混为一谈。",
                "后来，人乳在魔族之间从流行慢慢变成了日常，而对银黑桃来说，最重要的始终只是被你榨乳时的快感。",
                "～银黑桃 魔王专属乳牛 Ending～",
            ],
            310: [
                "失去银黑桃的消息数日后，你收到了一个包裹和水晶球。",
                "狂王在影像里用恶心的笑容说，那个曾经的部下无论如何都不肯回头，最后甚至干脆自尽了。",
                "你匆忙拆开包裹，里面那块残留的身体碎片仍让你认出它曾属于银黑桃。",
                "而之后水晶球里还在说什么，你已经完全听不进去了。",
            ],
        }






    def _build_spade_event_stage_lines_late_milk(self) -> Dict[int, List[str]]:
        return {
            150: [
                "银黑桃一边揉搓自己的乳房，一边在床上失控地自慰着。",
                "你只是轻轻一压，她的乳汁就喷在了你脸上。",
                "那股越来越合你口味的香甜，让你第一次认真考虑起把这份快感和收益一起固定下来。",
                "一个围绕『魔王乳业』的计划，也开始在你心里成形。",
            ],
            160: [
                "你牵着脖子上戴着项圈、胸部几乎完全暴露的银黑桃在走廊上行走。",
                "她不但不害羞，反而因为长期露出和禁止自慰而发情到几乎发抖。",
                "你最近总把她带在身边，一来防止跟踪，二来也能随时喝到最新鲜的奶水。",
                "很快，『魔王大人喜欢喝人奶』的传闻开始在外面发酵。",
            ],
            170: [
                "你品味着鲜榨乳汁，旁边的银黑桃因刚结束调教而沉沉睡去。",
                "喝完一杯后，你还想再抓起她的乳房继续，却最终克制住了。",
                "为了保证乳汁质量，现在还不是玩坏她的时候。",
                "窗外那座世界上第一间专门生产人乳的农场，让你露出了满意的笑容。",
            ],
            180: [
                "被固定在木架上的银黑桃，乳汁正顺着透明软管一点点流进桶里。",
                "你一边挑逗着她，一边从桶里舀起新鲜乳汁送入口中。",
                "这副景象被水晶球拍下后，很快就会成为『魔王乳业』最好的宣传材料。",
                "与其一波波打压那些私开人乳农场的家伙，不如干脆把整个产业彻底垄断。",
            ],
        }






    def _build_spade_event_stage_lines_middle(self) -> Dict[int, List[str]]:
        return {
            **self._build_spade_event_stage_lines_middle_org(),
            **self._build_spade_event_stage_lines_middle_tracking(),
        }






    def _build_spade_event_stage_lines_middle_org(self) -> Dict[int, List[str]]:
        return {
            90: [
                "走廊上，银黑桃跟在你身后，为迟迟没找到狂王所在地而低声道歉。",
                "可你很清楚，交给忍者部队的其他任务都做得极其漂亮，唯独狂王这一件事没有进展，只能说明他藏得太深。",
                "在你带着她走向新的目标、甚至将某个曾资助狂王的国王逼入绝境后，那个只效忠于魔王的地下组织传说也开始悄然成形。",
                "世人将它称作『魔王的无名指』，而真正知道内幕的人却寥寥无几。",
                "～银黑桃 忍者组织头领 Ending～",
            ],
            110: [
                "「你终于又来了。」",
                "银黑桃一上来就用妩媚到和往日判若两人的姿态缠住了你。",
                "她埋怨你明明最近调教次数不少，却还是让她寂寞得难耐。",
                "还没等你回过神来，她就已经把你扑倒在了床上。",
            ],
            120: [
                "最近几天，你总觉得有谁在暗中观察自己。",
                "虽然找不到恶意，但那种被视线黏着的感觉仍旧让人极不舒服。",
                "不管怎么查都找不到来源，也没有任何魔法痕迹。",
                "可你始终确信，这绝不只是神经过敏。",
            ],
        }






    def _build_spade_event_stage_lines_middle_tracking(self) -> Dict[int, List[str]]:
        return {
            130: [
                "被监视数日之后，你终于察觉到那股视线的规律。",
                "它几乎只在你移动、尤其是决定调教谁的时候出现。",
                "顺着这个直觉闯进银黑桃的房间后，你果然抓到了她和那本记满你行程的笔记本。",
                "所谓跟踪你的理由，居然只是为了在你不来时自己解决欲望。",
            ],
            140: [
                "虽然没有任何证据，但你今天大概又被银黑桃跟踪了。",
                "这一次那股视线格外热情，几乎把空气都染成了粉色。",
                "看来她的欲求已经彻底写在了目光里。",
                "下次调教，也许该再激烈一点了。",
            ],
        }






    def _get_spade_ending_event_key(self, stage: int) -> Optional[str]:
        stage_to_key = {
            10: "ending_spade_scene_10",
            20: "ending_spade_scene_20",
            30: "ending_spade_scene_30",
            40: "ending_spade_scene_40",
            50: "ending_spade_scene_50",
            60: "ending_spade_scene_60",
            70: "ending_spade_scene_70",
            80: "ending_spade_scene_80",
            90: "ending_spade_scene_90",
            110: "ending_spade_scene_110",
            120: "ending_spade_scene_120",
            130: "ending_spade_scene_130",
            140: "ending_spade_scene_140",
            150: "ending_spade_scene_150",
            160: "ending_spade_scene_160",
            170: "ending_spade_scene_170",
            180: "ending_spade_scene_180",
            190: "ending_spade_scene_190",
            200: "ending_spade_scene_200",
            310: "ending_spade_scene_310",
        }
        return stage_to_key.get(stage)






    def _process_spade_ending_events(self, messages: List[str]):
        stage = int(self.interpreter.vars.globals.get(2814, 0))
        event_key = self._get_spade_ending_event_key(stage)
        if not event_key or self._has_seen_ending_event(event_key):
            return
        if self._queue_spade_ending_prompt(stage, event_key):
            return
        self._apply_spade_ending_stage_output(messages, stage, event_key)






    def _prompt_spade_departure_choice(self, event_key: str):
        for line in self._build_spade_event_lines(40):
            print(line)
        print("银黑桃请求独自去刺杀狂王，你要怎么处理？")
        print(" [1] 许可")
        print(" [2] 阻止")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                self._apply_spade_departure_leave(event_key)
                return
            if choice == "2":
                self._apply_spade_departure_stay(event_key)
                return






    def _prompt_spade_love_ending_choice(self, event_key: str):
        print("可以达成银黑桃的纯爱结局，想要进入这个结局吗？")
        print(" [1] 好的")
        print(" [2] 还是算了")
        print(" [3] 明天再问我")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                for line in self._build_spade_event_lines(90):
                    print(line)
                self._advance_story_flag_if_matches(2814, 90)
                self._apply_story_ending_main_completion()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("好吧，银黑桃尊重你的选择哦。")
                self._advance_story_flag_if_matches(2814, 90)
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("可以哦，明天会继续问你的。")
                self._pause()
                return






    def _prompt_spade_milk_ending_choice(self, event_key: str):
        print("可以达成银黑桃的乳牛结局，想要进入这个结局吗？")
        print(" [1] 好的")
        print(" [2] 还是算了")
        print(" [3] 明天再问我")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                for line in self._build_spade_event_lines(200):
                    print(line)
                self._advance_story_flag_if_matches(2814, 200)
                self._apply_story_ending_main_completion()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("好吧，银黑桃尊重你的选择哦。")
                self._advance_story_flag_if_matches(2814, 200)
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("可以哦，明天会继续问你的。")
                self._pause()
                return






    def _queue_spade_ending_prompt(self, stage: int, event_key: str) -> bool:
        if stage == 40:
            self._queue_post_message_action({"kind": "spade_departure_prompt", "event_key": event_key})
            return True
        if stage == 90:
            self._queue_post_message_action({"kind": "spade_love_ending_prompt", "event_key": event_key})
            return True
        if stage == 200:
            self._queue_post_message_action({"kind": "spade_milk_ending_prompt", "event_key": event_key})
            return True
        return False





