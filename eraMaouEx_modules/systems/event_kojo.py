from __future__ import annotations
"""Module for EventKojoMixin - Event kojo (character personality event) dispatch methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class EventKojoMixin:
    """Mixin providing Event kojo (character personality event) dispatch methods"""
    def _get_kojo_num(self, target: Optional[Character]) -> int:
        if target is None:
            return 0
        if int(self._get_character_ex_talent(target, 103)) == 1:
            return 1003
        if int(self._get_character_ex_talent(target, 104)) == 1:
            return 1004
        for talent_id in range(160, 180):
            if int(target.talent.get(talent_id, 0)) == 1:
                return talent_id - 60
        return 0


    def _get_kojo_num(self, target: Character) -> int:
        """Determine the kojo (dialogue personality) number for a character.
        Mirrors @GET_KOJO_NUM in EVENT_K.ERB – checks TALENT:160-179 range
        and EX_TALENT:101+ range.
        """
        for tid in range(160, 180):
            if target.talent.get(tid, 0):
                return tid - 60
        # EX kojo check (CFLAG:6 based personality)
        cflag6 = target.cflag.get(6, 0)
        if cflag6 == 10031:
            return 101
        elif cflag6 == 10032:
            return 102
        elif cflag6 == 10033:
            return 103
        elif cflag6 == 10035:
            return 104
        return -1


    def _event_k_dispatch(self, target: Character, event_type: str) -> List[str]:
        """Dispatch to the character-specific event handler based on kojo number.

        event_type: "daily", "train_before", "train_after", "shop",
                    "execution", "sell", "com", "palam", "mark",
                    "dungeon_ryouzyoku", "dungeon_victory", "ntr",
                    "museum", "banishment", "benki", "colosseum"
        
        Priority: Try ERB function first (direct ERB execution),
                  fallback to Python stub.
        """
        kojo_num = self._get_kojo_num(target)
        
        # Map event_type to ERB function name patterns
        # ERB uses patterns like: KOJO_MESSAGE_COM_{num}, SELF_KOJO_K{num},
        # K{num}_KOJO2, DUNGEON_RYOUZYOKU_K{num}, etc.
        erb_func_candidates = []
        
        event_erb_map = {
            "train_before": ["EVENTTRAIN"],
            "train_after": ["EVENTEND"],
            "shop": ["EVENTSHOP"],
            "com": [f"KOJO_MESSAGE_COM_{kojo_num}", "KOJO_MESSAGE_COM"],
            "palam": [f"KOJO_MESSAGE_PALAMCNG_{kojo_num}", "KOJO_MESSAGE_PALAMCNG"],
            "mark": [f"KOJO_MESSAGE_MARKCNG_{kojo_num}", "KOJO_MESSAGE_MARKCNG"],
            "daily": [f"K{kojo_num}_KOJO2", f"SELF_KOJO_K{kojo_num}", "SELF_KOJO"],
            "dungeon_ryouzyoku": [f"DUNGEON_RYOUZYOKU_K{kojo_num}", "DUNGEON_RYOUZYOKU"],
            "dungeon_ryouzyoku_after": [f"DUNGEON_RYOUZYOKU_AFTER_K{kojo_num}", "DUNGEON_RYOUZYOKU_AFTER"],
            "dungeon_victory": [f"DUNGEON_VICTORY_K{kojo_num}", "VICTORY_KOUJO"],
            "dungeon_attack": [f"DUNGEON_ATTACK_K{kojo_num}", "ATTACK_KOUJO"],
            "ntr": [f"NTR_KOUJO_K{kojo_num}", "NTR_KOUJO"],
            "execution": [f"EXUCUTION_KOUJO_K{kojo_num}", "EXUCUTION_KOUJO"],
            "public_execution": [f"PUBLIC_EXUCUTION_KOUJO_K{kojo_num}", "PUBLIC_EXUCUTION_KOUJO"],
            "museum": [f"MUSEUM_KOUJO_K{kojo_num}", "MUSEUM_KOUJO"],
            "banishment": [f"BANISHMENT_KOUJO_K{kojo_num}", "BANISHMENT_KOUJO"],
            "benki": [f"BENKI_KOUJO_K{kojo_num}", "BENKI_KOUJO"],
            "colosseum": [f"COLOSSEUM_KOJO_{kojo_num}"],
            "dog": [f"DOG_KOJO_{kojo_num}"],
            "gohoubi_request": [f"GOHOUBI_REQUEST_KOUJO_K{kojo_num}", "GOHOUBI_REQUEST_KOUJO"],
            "gohoubi_after": [f"GOHOUBI_AFTER_KOUJO_K{kojo_num}", "GOHOUBI_AFTER_KOUJO"],
            "grotesque": [f"GROTESQUE_KOUJO_K{kojo_num}", "GROTESQUE_KOUJO"],
            "oshioki": [f"OSIOKI_KOUJO_K{kojo_num}", "OSIOKI_KOUJO"],
            "enter_enemy": [f"ENTERENEMY_KOUJO_K{kojo_num}", "ENTERENEMY_KOUJO"],
            "gobi": [f"GOBI_KOUJO_K{kojo_num}", "GOBI_KOUJO"],
            "aegi": [f"AEGI_K{kojo_num}"],
            "fuku": [f"K{kojo_num}_FUKU"],
        }
        
        erb_func_candidates = event_erb_map.get(event_type, [])
        
        # Try each ERB function candidate
        for func_name in erb_func_candidates:
            if func_name in self.interpreter.functions:
                return self.interpreter.call_erb_function(func_name)
        
        # Fallback: try Python handler
        handler_map: Dict[int, str] = {
            0: "_event_k0", 1: "_event_k1", 2: "_event_k2", 3: "_event_k3",
            4: "_event_k4", 5: "_event_k5", 6: "_event_k6", 7: "_event_k7",
            8: "_event_k8", 9: "_event_k9", 10: "_event_k10", 11: "_event_k11",
            12: "_event_k12", 13: "_event_k13", 14: "_event_k14",
            15: "_event_k15", 19: "_event_k19", 903: "_event_k903",
        }
        handler_name = handler_map.get(kojo_num)
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            return handler(target, event_type)
        return []

    # --- Individual personality stubs ---


    def _event_k0(self, target: Character, event_type: str) -> List[str]:
        """慈愛 – 圣女般的勇者"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「今天也请多关照了。」"]
        elif event_type == "train_before":
            return [f"{name}：「请温柔地对待我……」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):  # 淫乱
                return [f"{name}：「啊……身体变得好奇怪……」"]
            return [f"{name}：「已经结束了吗……」"]
        elif event_type == "shop":
            return [f"{name}：「需要我帮忙吗？」"]
        elif event_type == "execution":
            return [f"{name}：「请不要太过分……」"]
        elif event_type == "sell":
            return [f"{name}：「……请善待我。」"]
        return []


    def _event_k1(self, target: Character, event_type: str) -> List[str]:
        """自信家 – 高傲的勇者"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「哼，我可是最强的！」"]
        elif event_type == "train_before":
            return [f"{name}：「这种程度，我才不会输！」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):  # 淫乱
                return [f"{name}：「呜……才不是感觉好呢！」"]
            return [f"{name}：「哼，不过如此而已。」"]
        elif event_type == "shop":
            return [f"{name}：「让我看看有什么好东西。」"]
        elif event_type == "execution":
            return [f"{name}：「你敢对我做这种事？！」"]
        elif event_type == "sell":
            return [f"{name}：「别以为我会屈服……」"]
        return []


    def _event_k2(self, target: Character, event_type: str) -> List[str]:
        """気弱 – 胆小的勇者"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「那个……今天也请多关照……」"]
        elif event_type == "train_before":
            return [f"{name}：「不、不要……请别那样……」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「呜呜……身体好奇怪……」"]
            return [f"{name}：「呜……终于结束了……」"]
        elif event_type == "shop":
            return [f"{name}：「我、我可以看看吗……」"]
        elif event_type == "execution":
            return [f"{name}：「不要啊……求求你……」"]
        elif event_type == "sell":
            return [f"{name}：「好可怕……」"]
        return []


    def _event_k3(self, target: Character, event_type: str) -> List[str]:
        """高貴 – 高贵的勇者"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「身为勇者，我绝不会屈服。」"]
        elif event_type == "train_before":
            return [f"{name}：「无礼之徒，竟敢对我出手。」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「这种事……绝不允许再有下次……」"]
            return [f"{name}：「哼，这等屈辱我记下了。」"]
        elif event_type == "shop":
            return [f"{name}：「让我看看有什么。」"]
        elif event_type == "execution":
            return [f"{name}：「你终将为此付出代价。」"]
        elif event_type == "sell":
            return [f"{name}：「我的尊严不容践踏。」"]
        return []


    def _event_k4(self, target: Character, event_type: str) -> List[str]:
        """冷徹 – 冷静沉着的勇者"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「……今天有什么安排？」"]
        elif event_type == "train_before":
            return [f"{name}：「……随你便。」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「……身体已经不受理智控制了。」"]
            return [f"{name}：「……结束了？」"]
        elif event_type == "shop":
            return [f"{name}：「……有什么有用的东西吗？」"]
        elif event_type == "execution":
            return [f"{name}：「……这就是你的手段？」"]
        elif event_type == "sell":
            return [f"{name}：「……随你处置。」"]
        return []


    def _event_k5(self, target: Character, event_type: str) -> List[str]:
        """マオ – 嚣张的萝莉村娘"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「本小姐今天也要加油！」"]
        elif event_type == "train_before":
            return [f"{name}：「哼！本小姐才不怕你！」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「呜……本小姐的身体才没有觉得舒服！」"]
            return [f"{name}：「哼，这种程度不算什么！」"]
        elif event_type == "shop":
            return [f"{name}：「有什么好东西给本小姐看看！」"]
        elif event_type == "execution":
            return [f"{name}：「你、你对本小姐做了什么？！」"]
        elif event_type == "sell":
            return [f"{name}：「本小姐才不会认输……」"]
        return []


    def _event_k6(self, target: Character, event_type: str) -> List[str]:
        """悪女 – 坏女人"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「呵，今天想玩什么呢？」"]
        elif event_type == "train_before":
            return [f"{name}：「来吧，让我看看你的本事。」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「啊……还不够呢……」"]
            return [f"{name}：「就这点程度？」"]
        elif event_type == "shop":
            return [f"{name}：「有没有什么有趣的东西？」"]
        elif event_type == "execution":
            return [f"{name}：「呵，这种事我也做得出来。」"]
        elif event_type == "sell":
            return [f"{name}：「把我卖掉？你确定？」"]
        return []


    def _event_k7(self, target: Character, event_type: str) -> List[str]:
        """ハート – 爱心"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「今天也要在一起哦♥」"]
        elif event_type == "train_before":
            return [f"{name}：「请对我温柔一点哦♥」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「好舒服……还要♥」"]
            return [f"{name}：「嘿嘿，很有趣呢♥」"]
        elif event_type == "shop":
            return [f"{name}：「一起逛街好开心♥」"]
        elif event_type == "execution":
            return [f"{name}：「好过分……但是♥」"]
        elif event_type == "sell":
            return [f"{name}：「不要丢下我……♥」"]
        return []


    def _event_k8(self, target: Character, event_type: str) -> List[str]:
        """スペード – 黑桃"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「……今天有什么作战计划？」"]
        elif event_type == "train_before":
            return [f"{name}：「……开始吧。」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「……身体已经无法回头了。」"]
            return [f"{name}：「……结束了。」"]
        elif event_type == "shop":
            return [f"{name}：「……需要补给。」"]
        elif event_type == "execution":
            return [f"{name}：「……这就是你的做法吗。」"]
        elif event_type == "sell":
            return [f"{name}：「……无所谓。」"]
        return []


    def _event_k9(self, target: Character, event_type: str) -> List[str]:
        """ダイヤ – 方块"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「今天也是闪耀的一天呢！」"]
        elif event_type == "train_before":
            return [f"{name}：「请让我见识更多！」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「啊……这种感觉……！」"]
            return [f"{name}：「学到了新的东西呢。」"]
        elif event_type == "shop":
            return [f"{name}：「有没有什么珍贵的东西？」"]
        elif event_type == "execution":
            return [f"{name}：「这也算是一种体验吧……」"]
        elif event_type == "sell":
            return [f"{name}：「即使如此我也不会放弃的。」"]
        return []


    def _event_k10(self, target: Character, event_type: str) -> List[str]:
        """クラブ – 梅花"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「今天也要好好休息呢。」"]
        elif event_type == "train_before":
            return [f"{name}：「请不要太勉强……」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「呜……身体变得好奇怪……」"]
            return [f"{name}：「辛苦了……」"]
        elif event_type == "shop":
            return [f"{name}：「需要什么日常用品吗？」"]
        elif event_type == "execution":
            return [f"{name}：「太过分了……」"]
        elif event_type == "sell":
            return [f"{name}：「……请保重。」"]
        return []


    def _event_k11(self, target: Character, event_type: str) -> List[str]:
        """リリィ – 百合"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「今天也要优雅地度过。」"]
        elif event_type == "train_before":
            return [f"{name}：「请不要粗鲁……」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「啊……这种事不应该的……」"]
            return [f"{name}：「请不要再做了……」"]
        elif event_type == "shop":
            return [f"{name}：「有什么漂亮的衣服吗？」"]
        elif event_type == "execution":
            return [f"{name}：「你太过分了……」"]
        elif event_type == "sell":
            return [f"{name}：「至少请让我保持尊严……」"]
        return []


    def _event_k19(self, target: Character, event_type: str) -> List[str]:
        """菲娅"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「……今天也请多指教。」"]
        elif event_type == "train_before":
            return [f"{name}：「……要开始了吗？」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):
                return [f"{name}：「……已经无法抗拒了。」"]
            return [f"{name}：「……结束了吗。」"]
        elif event_type == "shop":
            return [f"{name}：「……有什么需要的东西吗？」"]
        elif event_type == "execution":
            return [f"{name}：「……这是必须的吗？」"]
        elif event_type == "sell":
            return [f"{name}：「……我明白了。」"]
        return []


    def _event_k903(self, target: Character, event_type: str) -> List[str]:
        """嘉德 – 傲娇的超级腹黑，下任主神候补"""
        name = target.name or "她"
        if event_type == "daily":
            return [f"{name}：「哼，别以为我会对你客气。」"]
        elif event_type == "train_before":
            if target.talent.get(27, 0):  # 戒备森严
                return [f"{name}：「别靠近我！你这个卑鄙的魔族！」"]
            return [f"{name}：「哼，这种程度我才不怕呢！」"]
        elif event_type == "train_after":
            if target.talent.get(70, 0):  # 淫乱
                return [f"{name}：「呜……才、才不是觉得舒服呢！只是身体自己的反应！」"]
            if target.talent.get(80, 0):  # 爱慕
                return [f"{name}：「哼……下次再这样我可不会原谅你……大概。」"]
            return [f"{name}：「哼，这种事情对我无效！」"]
        elif event_type == "shop":
            return [f"{name}：「这种低级的东西我才不稀罕。」"]
        elif event_type == "execution":
            return [f"{name}：「你竟敢对我做这种事！我可是下任主神候补！」"]
        elif event_type == "sell":
            return [f"{name}：「卖掉我？你一定会后悔的！」"]
        return []

    # ------------------------------------------------------------------
    # LOOK (角色外观查看)
    # ------------------------------------------------------------------

    _HAIR_COLOR_MAP: Dict[int, str] = {
        1: "金色", 2: "栗色", 3: "黑色", 4: "红色", 5: "银色",
        6: "青色", 7: "绿色", 8: "紫色", 9: "白色", 10: "暗金色", 11: "粉色",
    }
    _HAIR_STYLE_MAP: Dict[int, str] = {
        1: "直发", 2: "卷发", 3: "内卷", 4: "外卷", 5: "乱发", 6: "波浪",
    }
    _EYE_TYPE_MAP: Dict[int, str] = {
        1: "细长", 2: "大眼", 3: "神秘", 4: "吊眼", 5: "湿润",
        6: "普通", 7: "三白眼", 8: "下垂眼",
    }
    _EYE_COLOR_MAP: Dict[int, str] = {
        1: "碧色", 2: "棕色", 3: "灰色", 4: "金色", 5: "深红", 6: "黑色",
    }
    _LIP_MAP: Dict[int, str] = {
        1: "肉感的", 2: "薄的", 3: "水润的", 4: "普通的", 5: "丰厚的",
    }


