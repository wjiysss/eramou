from __future__ import annotations
"""Module for SquareExtMixin - 广场系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SquareExtMixin:
    """Mixin providing 广场系统 methods for GameEngine"""

    def _advance_square_black_route(self, char: Character, current: int, favor: int):
        if char.talent.get(76, 0) != 1:
            return
        next_stage = self._resolve_square_black_next_stage(char, current, favor)
        if next_stage is not None:
            self.interpreter.vars.globals[2811] = next_stage






    def _advance_square_female_route(self, char: Character, current: int, favor: int):
        if char.talent.get(85, 0) != 1:
            return
        if favor >= 2000 and current < 10:
            self.interpreter.vars.globals[2811] = 10
        elif 10 <= current < 20 and favor >= 5000:
            self.interpreter.vars.globals[2811] = 20
        elif 20 <= current < 30 and favor >= 10000:
            self.interpreter.vars.globals[2811] = 30
        elif 30 <= current < 40 and int(char.abl.get(10, 0)) + int(char.abl.get(16, 0)) >= 14:
            self.interpreter.vars.globals[2811] = 40
            char.cflag[515] = 0
        elif 40 <= current < 50 and self._advance_story_wait_counter(char, 10, 50):
            self.interpreter.vars.globals[2811] = 50
        elif 50 <= current < 60 and self._advance_story_wait_counter(char, 30, 60):
            self.interpreter.vars.globals[2811] = 60
        elif 60 <= current < 70 and self._advance_story_wait_counter(char, 60, 70):
            self.interpreter.vars.globals[2811] = 70
        elif 70 <= current < 80 and self._advance_story_wait_counter(char, 100, 80):
            self.interpreter.vars.globals[2811] = 80
        elif 80 <= current < 90 and self._advance_story_wait_counter(char, 150, 90):
            self.interpreter.vars.globals[2811] = 90
        elif current == 300 and random.randint(0, 4) == 0:
            self.interpreter.vars.globals[2811] = 310






    def _apply_square_departure_corrupt(self, event_key: str):
        for line in [
            "「要坏掉了……」",
            "「我才不……喜欢……不喜……喜欢……我……喜欢……好喜欢啊！」",
            "黑方片脸上的困惑很快就被欢愉所取代。",
            "她的反抗心与抗拒在更粗暴的快感中迅速瓦解，只剩下彻底被你占有后的淫乱与渴求。",
            "你也借此将她重新拽回到了继续为魔王效劳的轨道上。",
        ]:
            print(line)
        square = self._find_character_by_template_id(22)
        if square is not None:
            square.talent[11] = 0
            square.talent[69] = 0
            square.talent[477] = 1
            square.talent[478] = 1
            square.talent[480] = 1
            square.talent[481] = 1
            square.talent[482] = 1
            square.cflag[11] = int(square.cflag.get(11, 0)) + 200
            square.cflag[12] = int(square.cflag.get(12, 0)) + 200
            square.base[0] = int(square.base.get(0, 0)) + 1000
            square.base[1] = int(square.base.get(1, 0)) + 1000
        self.interpreter.vars.globals[2811] = 51
        self._mark_ending_event_seen(event_key)
        self._pause()






    def _apply_square_departure_leave(self, event_key: str):
        print("「感谢您的信任……」")
        print("然而你并不知道，被放走的已经是一头失去理智的凶兽……")
        self.interpreter.vars.globals[2811] = 300
        self._mark_ending_event_seen(event_key)
        self._pause()






    def _apply_square_endcheck(self, char: Character):
        current = int(self.interpreter.vars.globals.get(2811, 0))
        favor = int(char.cflag.get(2, 0))
        current = self._sync_square_endcheck_route(char, current)

        self._advance_square_female_route(char, current, favor)
        self._advance_square_black_route(char, current, favor)






    def _apply_square_ending_stage_effects(self, stage: int) -> None:
        char = self._find_character_by_template_id(22)
        if char is None:
            return
        if stage == 20:
            self._apply_square_stage_20_exp(char)
        elif stage == 50:
            self._apply_square_stage_50_exp(char)






    def _apply_square_stage_20_exp(self, char: Character) -> None:
        char.exp[10] = int(char.exp.get(10, 0)) + 10
        char.exp[11] = int(char.exp.get(11, 0)) + 10
        char.exp[35] = int(char.exp.get(35, 0)) + 10
        char.exp[1] = int(char.exp.get(1, 0)) + 10
        char.exp[30] = int(char.exp.get(30, 0)) + 10
        if int(char.talent.get(0, 0)) == 0:
            char.exp[0] = int(char.exp.get(0, 0)) + 10






    def _apply_square_stage_50_exp(self, char: Character) -> None:
        char.exp[20] = int(char.exp.get(20, 0)) + 10
        char.exp[21] = int(char.exp.get(21, 0)) + 10
        if int(char.talent.get(0, 0)) == 0:
            char.exp[0] = int(char.exp.get(0, 0)) + 10






    def _build_square_event_lines(self, stage: int) -> List[str]:
        return self._build_stage_lines(stage, self._build_square_event_stage_lines())






    def _build_square_event_stage_lines(self) -> Dict[int, List[str]]:
        return {
            **self._build_square_event_stage_lines_early(),
            **self._build_square_event_stage_lines_middle(),
            **self._build_square_event_stage_lines_late(),
        }






    def _build_square_event_stage_lines_early(self) -> Dict[int, List[str]]:
        return {
            10: [
                "「大人，今晚也请早些休息。」",
                "黑方片努力维持严肃威严的样子，但反而显得格外滑稽又诱人。",
                "被你日常调戏之后，她嘴硬地否认着自己的动摇，最后还是满脸通红。",
                "这是有趣，要强迫这家伙侍寝吗？不，这对她来说反而像奖励吧。",
            ],
            20: [
                "黑方片被你当场揭穿偷听墙角后，气得挥舞大剑冲了上来。",
                "可这本就是你自导自演的戏码，她的抵抗很快就被拆得七零八落。",
                "最后你把她丢到床边，只留下一句想要的话随时可以来找你。",
                "她拼命维持着最后的尊严，却已经彻底乱了阵脚。",
            ],
            30: [
                "沐浴之后，欲言又止的黑方片终于主动凑到了你面前。",
                "她结结巴巴地试探着，最后干脆整个人抱了上来。",
                "那线条优美的身体滚烫得惊人，而她口中否认的话也早就失去了说服力。",
                "这一次，房间里只有你和她两个人。",
            ],
            40: [
                "黑方片第一次认真提出想回家一趟。",
                "她承认自己过去建立的一切价值观都在崩坏，也坦率说出想回去做个了断。",
                "泪水和扭曲的光一起出现在她眼中，她已经到了某种临界点。",
                "这一步之后，她的人生会彻底走向不同的方向。",
            ],
        }






    def _build_square_event_stage_lines_late(self) -> Dict[int, List[str]]:
        return {
            90: [
                "神殿里，黑方片跟在你身后做着工作汇报。",
                "她靠商贾团队与城管体系逐步切断狂王的经济来源，也让更多地方落入你的掌控。",
                "在被你抱住、侵犯、宣告占有之后，她眼中原本混杂的恐惧终于慢慢消失了。",
                "传说中那个只效忠于魔王、暗中控制世界半数国家的地下组织，也正是在这样的关系里诞生。",
                "～黑方片 傲娇的商贾后裔 Ending～",
            ],
            310: [
                "黑方片离开后不久，外面传来她烧毁庄园、屠杀富贾家族的消息。",
                "数日后你收到包裹与水晶球，狂王在影像里用恶心的笑意讲述着她如何彻底坏掉并最终被杀。",
                "包裹里那团再也辨不清原样的残肢，仍让你一眼认出了那曾经属于黑方片的身体。",
                "而你已经什么都听不进去了。",
            ],
        }






    def _build_square_event_stage_lines_middle(self) -> Dict[int, List[str]]:
        return {
            50: [
                "黑方片带着一群惶恐的同族女孩出现在你面前，声称她们会为魔王城繁荣效命到死。",
                "原来她偷偷溜回了家，把家族里的商人和资源统统绑了回来。",
                "你干脆顺势把一些产业和相关女孩交给她去打理调教。",
                "黑方片也因此开始真正参与魔族特色商业链的构建。",
            ],
            60: [
                "魔王的房间里横七竖八地倒着女孩们，而作为金库打理者的她们身心都只属于魔王。",
                "黑方片虽然气喘吁吁，却还是撑着身体凑上来讨要惯例的奖励。",
                "嘴上依旧说着并没有期待什么，身体却早已经诚实得不能再诚实。",
                "最后她在极度快感中被女孩们抬了出去。",
            ],
            70: [
                "商业的运作已经走上了轨道，黑方片和她挑选的人都相当能干。",
                "她提出下一步要把那些人训练成魔王的护卫。",
                "虽然嘴上还是一如既往地傲娇，但和几个月前相比，她明显已经恢复了很多。",
                "不过继续把她当成只会交尾的母狗也未免太可惜了。",
            ],
            80: [
                "大约一百天过去后，整个魔王城的气氛都变了。",
                "在黑方片主导下，商业、治安与城卫训练都逐渐成了规模。",
                "她嘴里念叨的仍旧离不开魔王大人和做爱，但也确实在认真发挥自己的才华。",
                "看着她睡着后下体还不安分地紧吸着你，你又开始思考还能把她开发到什么地步。",
            ],
        }






    def _get_square_ending_event_key(self, stage: int) -> Optional[str]:
        stage_to_key = {
            10: "ending_square_scene_10",
            20: "ending_square_scene_20",
            30: "ending_square_scene_30",
            40: "ending_square_scene_40",
            50: "ending_square_scene_50",
            60: "ending_square_scene_60",
            70: "ending_square_scene_70",
            80: "ending_square_scene_80",
            90: "ending_square_scene_90",
            310: "ending_square_scene_310",
        }
        return stage_to_key.get(stage)






    def _prompt_square_departure_choice(self, event_key: str):
        for line in self._build_square_event_lines(40):
            print(line)
        print("黑方片请求回家做个了断，你要怎么处理？")
        print(" [1] 放她离开")
        print(" [2] 直接把她丢到床上")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                self._apply_square_departure_leave(event_key)
                return
            if choice == "2":
                self._apply_square_departure_corrupt(event_key)
                return






    def _prompt_square_love_ending_choice(self, event_key: str):
        print("可以达成黑方片的纯爱结局，想要进入这个结局吗？")
        print(" [1] 好的")
        print(" [2] 还是算了")
        print(" [3] 明天再问我")
        while True:
            choice = self._prompt_choice()
            if choice == "1":
                for line in self._build_square_event_lines(90):
                    print(line)
                self._advance_story_flag_if_matches(2811, 90)
                self._apply_story_ending_main_completion()
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "2":
                print("好吧，黑方片尊重你的选择哦。")
                self._advance_story_flag_if_matches(2811, 90)
                self._mark_ending_event_seen(event_key)
                self._pause()
                return
            if choice == "3":
                print("可以哦，明天会继续问你的。")
                self._pause()
                return





