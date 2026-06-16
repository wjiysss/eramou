from __future__ import annotations
"""Module for SellExtMixin - 销售系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SellExtMixin:
    """Mixin providing 销售系统 methods for GameEngine"""

    def _advance_sell_candidate_menu(self) -> bool:
        candidates = self._list_sellable_targets()
        return self._show_sell_candidate_selection_menu(candidates)






    def _append_sell_multiplier(self, multipliers: List[tuple[str, int]], label: str, value: int) -> None:
        multipliers.append((label, value))






    def _append_sell_multiplier_if(self, multipliers: List[tuple[str, int]], condition: bool, label: str, value: int) -> None:
        if condition:
            multipliers.append((label, value))






    def _apply_sell_experience_multipliers(self, target: Character, detail: Dict[str, Any], score: int) -> int:
        prostitution_exp = target.exp.get(74, 0)
        if prostitution_exp == 0:
            score = self._apply_sell_multiplier(detail, score, "卖淫经验", 100)
        elif prostitution_exp < 5:
            score = self._apply_sell_multiplier(detail, score, "卖淫经验", 80)
        elif prostitution_exp < 30 or target.talent.get(180, 0) or target.talent.get(181, 0):
            score = self._apply_sell_multiplier(detail, score, "卖淫经验", 50)
        elif prostitution_exp < 100:
            score = self._apply_sell_multiplier(detail, score, "卖淫经验", 30)
        else:
            score = self._apply_sell_multiplier(detail, score, "卖淫经验", 10)

        birth_exp = target.exp.get(60, 0)
        if birth_exp == 0:
            score = self._apply_sell_multiplier(detail, score, "生育经验", 100)
        elif birth_exp == 1:
            score = self._apply_sell_multiplier(detail, score, "生育经验", 50)
        elif birth_exp == 2:
            score = self._apply_sell_multiplier(detail, score, "生育经验", 20)
        else:
            score = self._apply_sell_multiplier(detail, score, "生育经验", 10)
        return score




    def _apply_sell_locked_trait_penalties(self, target: Character, detail: Dict[str, Any], score: int) -> int:
        for talent_id, (label, value) in {
            101: ("阴核感觉封锁", 150),
            103: ("私处感觉封锁", 150),
            105: ("肛门感觉封锁", 150),
            107: ("乳房感觉封锁", 150),
        }.items():
            if target.talent.get(talent_id, 0) & 2:
                score -= value
                detail["base_penalties"].append((label, 0, value))
        return score




    def _apply_sell_multiplier(self, detail: Dict[str, Any], score: int, label: str, value: int) -> int:
        detail["multipliers"].append((label, value))
        return score * value // 100




    def _apply_sell_multipliers(self, target: Character, detail: Dict[str, Any], score: int) -> int:
        for label, value in [
            ("阴蒂感觉", self._get_sell_multiplier(target.abl.get(0, 0), {0: 100, 1: 100, 2: 100, 3: 100, 4: 110, 5: 120, 6: 130, 7: 140, 8: 150, 9: 170, 10: 200}, [(15, 10, 100), (20, 25, -125), (25, 40, -425)])),
            ("乳房感觉", self._get_sell_multiplier(target.abl.get(1, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 120, 5: 130, 6: 140, 7: 150, 8: 160, 9: 180, 10: 200}, [(15, 10, 100), (20, 25, -125), (25, 32, -265)])),
            ("私处感觉", self._get_sell_multiplier(target.abl.get(2, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 120, 5: 140, 6: 150, 7: 160, 8: 170, 9: 190, 10: 200}, [(15, 10, 100), (20, 18, -20), (25, 30, -260)])),
            ("肛门感觉", self._get_sell_multiplier(target.abl.get(3, 0), {0: 100, 1: 100, 2: 110, 3: 120, 4: 140, 5: 160, 6: 180, 7: 190, 8: 200, 9: 230, 10: 250}, [(15, 10, 150), (20, 19, 15), (25, 28, -165)])),
            ("侍奉精神", self._get_sell_multiplier(target.abl.get(16, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 130, 5: 150, 6: 150, 7: 150}, default=180)),
            ("露出癖", self._get_sell_multiplier(target.abl.get(17, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 130, 5: 150, 6: 150, 7: 150}, default=180)),
            ("抖S气质", self._get_sell_multiplier(target.abl.get(20, 0), {0: 100, 1: 100, 2: 100, 3: 130, 4: 140, 5: 150, 6: 200, 7: 200, 8: 250, 9: 250}, default=300)),
            ("抖M气质", self._get_sell_multiplier(target.abl.get(21, 0), {0: 100, 1: 100, 2: 100, 3: 130, 4: 140, 5: 150, 6: 200, 7: 200, 8: 250, 9: 250}, default=300)),
            ("百合气质", self._get_sell_multiplier(target.abl.get(22, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 130, 5: 150, 6: 150, 7: 150}, default=180)),
            ("男色气质", self._get_sell_multiplier(target.abl.get(23, 0), {0: 100, 1: 100, 2: 100, 3: 110, 4: 130, 5: 150, 6: 150, 7: 150}, default=180)),
        ]:
            score = self._apply_sell_multiplier(detail, score, label, value)
        return score




    def _apply_sell_party_multipliers(self, target: Character, detail: Dict[str, Any], score: int) -> int:
        assistant_multiplier = 50 if self.interpreter.vars.assi == self.interpreter.vars.chars.index(target) else 100
        detail["assistant_multiplier"] = assistant_multiplier
        score = self._apply_sell_multiplier(detail, score, "助手出售", assistant_multiplier)

        best_merchant_skill = 0
        target_index = self.interpreter.vars.chars.index(target)
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx == target_index:
                continue
            if idx == 0 or self.interpreter.vars.assi == idx:
                best_merchant_skill = max(best_merchant_skill, char.abl.get(15, 0))
        merchant_multiplier = 100 + best_merchant_skill * 2 if best_merchant_skill else 100
        detail["merchant_multiplier"] = merchant_multiplier
        score = self._apply_sell_multiplier(detail, score, "商卖人交涉", merchant_multiplier)
        return score




    def _apply_sell_prestige_change(self, target: Character) -> tuple[int, str]:
        prestige_delta = 5
        message = "威望值增加"
        if target.talent.get(220, 0) and not target.talent.get(292, 0):
            prestige_delta = -10
            message = "威望值减少"
        self._add_prestige_value(prestige_delta)
        return prestige_delta, message




    def _apply_sell_score_tables(self, target: Character, detail: Dict[str, Any]) -> int:
        additive_tables, penalty_tables, additive_labels = self._build_sell_price_tables()
        score = 0
        for idx, table in additive_tables.items():
            value = self._get_sell_additive_score(target.abl.get(idx, 0), table)
            if value:
                score += value
                detail["base_additions"].append((additive_labels[idx], target.abl.get(idx, 0), value))
        for idx, table in penalty_tables.items():
            value = self._get_sell_additive_score(target.abl.get(idx, 0), table)
            if value:
                score -= value
                detail["base_penalties"].append((additive_labels[idx], target.abl.get(idx, 0), value))
        return score




    def _apply_sell_trait_multipliers(self, target: Character, detail: Dict[str, Any], score: int) -> int:
        for label, value in self._collect_sell_trait_multipliers(target):
            score = self._apply_sell_multiplier(detail, score, label, value)
        return score




    def _build_exotic_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        return self._build_exotic_market_sell_followup_lines_core(target, price)






    def _build_exotic_market_sell_followup_lines_core(self, target: Character, price: int) -> Optional[List[str]]:
        tier = self._get_sell_price_tier(price)
        race_id = int(target.talent.get(314, 0))
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        busty = self._is_sell_busty_target(target)
        level = int(target.cflag.get(9, 0))
        rebellious = int(target.mark.get(3, 0)) == 3

        if rebellious:
            return self._build_exotic_market_sell_followup_lines_rebellious(
                target, tier, race_id, warrior_like, priest_like, busty, level
            )
        if price >= 1_000_000:
            return self._build_exotic_market_sell_followup_lines_high_value(target, warrior_like, priest_like, busty)
        if price >= 500_000:
            return self._build_exotic_market_sell_followup_lines_mid_high(target, warrior_like, priest_like, busty)
        if price >= 100_000:
            return self._build_exotic_market_sell_followup_lines_mid(target, warrior_like, priest_like, busty)
        return self._build_exotic_market_sell_followup_lines_low(target, tier)






    def _build_exotic_market_sell_followup_lines_high_value(
        self,
        target: Character,
        warrior_like: bool,
        priest_like: bool,
        busty: bool,
    ) -> Optional[List[str]]:
        if warrior_like:
            if int(target.talent.get(75, 0)):
                return [
                    f"{target.name} 作为珍稀异族被送进了专门的研究设施。",
                    "那里的研究员将她当成活体样本反复观察、采样与展示，她的身体也逐渐被改造成更适合被观看与繁殖的模样。",
                    f"从那之后，你再也没有见过 {target.name}。",
                ]
            return [
                f"{target.name} 作为珍稀异族被送进了专门的研究设施。",
                "她被安置在极其昂贵的隔离区里，日夜接受各种繁殖与顺从性测试，最后几乎只剩下被展示的价值。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if priest_like:
            if busty:
                return [
                    f"{target.name} 被当成高价祭品供进了异族神殿。",
                    "神殿里的人对她的身体极为满意，甚至把她当作最上等的仪式素材反复供奉。",
                    f"从那之后，你再也没有见过 {target.name}。",
                ]
            return [
                f"{target.name} 被当成高价祭品供进了异族神殿。",
                "她很快被洗成了顺从的神殿收藏品，只能在无数次仪式和展示中度过余生。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被高价转卖后，似乎作为某位强大魔族的专属玩物活了下去。",
            "她的身体在展示与调教中变得越来越适合被占有，最后成了彻头彻尾的珍贵藏品。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_low(self, target: Character, tier: int) -> Optional[List[str]]:
        if int(target.talent.get(75, 0)):
            return self._build_sell_followup_lines_tiered(
                target,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[75]),
                tier,
            )
        if int(target.talent.get(76, 0)):
            return self._build_sell_followup_lines_tiered(
                target,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[76]),
                tier,
            )
        if int(target.talent.get(85, 0)):
            return self._build_sell_followup_lines_tiered(
                target,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[85]),
                tier,
            )
        return None






    def _build_exotic_market_sell_followup_lines_mid(
        self,
        target: Character,
        warrior_like: bool,
        priest_like: bool,
        busty: bool,
    ) -> Optional[List[str]]:
        if warrior_like:
            return self._build_exotic_market_sell_followup_lines_mid_warrior(target, int(target.talent.get(75, 0)))
        if priest_like:
            return self._build_exotic_market_sell_followup_lines_mid_priest(target, int(target.talent.get(77, 0)))
        if busty:
            return self._build_exotic_market_sell_followup_lines_mid_busty(target)
        return self._build_exotic_market_sell_followup_lines_mid_default(target)






    def _build_exotic_market_sell_followup_lines_mid_busty(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了黑暗精灵学校的讲师。",
            "她那呼之欲出的胸部让少年学生们充满憧憬；可最近与黑暗精灵少年的淫行败露后，她已经被刺上了“淫行老师”的耻辱纹样。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_mid_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了黑暗精灵学校的讲师。",
            "经验丰富的她几乎和全班男生都维持着性关系，甚至还把手伸向了几名女学生；据说保健课上，整班人都会和她一起进行性实习。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_mid_high(
        self,
        target: Character,
        warrior_like: bool,
        priest_like: bool,
        busty: bool,
    ) -> Optional[List[str]]:
        if warrior_like:
            return [
                f"{target.name} 被卖给了兽人的佣兵团，慢慢适应了那种拳头解决问题的生活。",
                "她开始学着兽人的嚣张语气说话，用木剑狠狠干训练对象，辛劳过后还会和兽人们一起裸体洗澡，最后几乎成了佣兵团不可或缺的一员。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if priest_like:
            return [
                f"{target.name} 被吸血鬼洗礼后，成了暗黑之神的信徒。",
                "邪恶仪式与药物让她被洗脑得忠诚又得心应手，只是经常会在失禁之后顺势绝顶，样子可悲又滑稽。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if busty:
            return [
                f"{target.name} 被当成奶罐饲养在畜舍里。",
                "她和一排同样被极限丰乳化的裸体女人并列着，流着口水戴着鼻环，一副高潮脸地被当成牲畜持续榨取。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成繁殖用家畜奴隶关进畜舍。",
            "不知从哪买来的男奴就那么拽着锁链在她身上挺腰，她的自由和人权一起被剥夺，只剩下贪图交配快感的本能。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_mid_priest(self, target: Character, anal_crazed: bool) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 在魔像的大农场里负责生产肥料。",
                "大量饲料与残羹被灌进她像孕妇般胀起的肚子，在被改造过的内脏里发酵，最后随着淫靡娇喘化成高品质肥料排出。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了魔像体内的生物零件。",
            "她全身都被封进魔像里，大脑一片空白，只剩下操纵巨躯行动与永恒感受胯间、乳头慰安装置快感这两件事。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_mid_warrior(self, target: Character, sex_crazed: bool) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 成了六头海蛇联防队的外籍战士。",
                "她原本在共同训练与战斗中表现得十分活跃，却因为性欲旺盛，老是在训练间隙偷偷和别的海蛇交合，最后甚至被强行装上贞操带。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了六头海蛇联防队的外籍战士。",
            "在共同磨砺与战斗中，她逐渐与那些海蛇建立起信赖，最近甚至传出了要和队里某位年轻海蛇成婚的消息。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_rebellious(
        self,
        target: Character,
        tier: int,
        race_id: int,
        warrior_like: bool,
        priest_like: bool,
        busty: bool,
        level: int,
    ) -> List[str]:
        if tier >= 1:
            return self._build_exotic_market_sell_followup_lines_rebellious_tier_one(
                target, race_id, warrior_like, priest_like, level
            )
        if busty:
            return self._build_exotic_market_sell_followup_lines_rebellious_tier_zero_busty(target)
        return self._build_exotic_market_sell_followup_lines_rebellious_tier_zero_default(target)






    def _build_exotic_market_sell_followup_lines_rebellious_tier_one(
        self,
        target: Character,
        race_id: int,
        warrior_like: bool,
        priest_like: bool,
        level: int,
    ) -> List[str]:
        tier_lines = SELL_FOLLOWUP_REBELLIOUS_TIER_ONE_LINES.get(race_id)
        if tier_lines is None:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 最终成了吸血鬼的饮料机。",
                "全身被紧紧拘束的她只能通过管子吃喝与排泄，唯一还能称作乐趣的，只剩睡前那一次被爱抚到绝顶。",
            )
        if race_id == 5:
            return self._build_sell_followup_lines_with_ending(
                target,
                *self._format_sell_followup_body_lines(target, tier_lines["default"]),
            )
        if warrior_like:
            key = "warrior_high" if level >= 100 else "warrior_low"
            return self._build_sell_followup_lines_with_ending(
                target,
                *self._format_sell_followup_body_lines(target, tier_lines[key]),
            )
        if priest_like:
            return self._build_sell_followup_lines_with_ending(
                target,
                *self._format_sell_followup_body_lines(target, tier_lines["priest"]),
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            *self._format_sell_followup_body_lines(target, tier_lines["fallback"]),
        )






    def _build_exotic_market_sell_followup_lines_rebellious_tier_zero_busty(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被当成奶罐饲养在畜舍里。",
            "她和一排同样被极限丰乳化的裸体女人并列着，流着口水戴着鼻环，一副高潮脸地被当成牲畜持续榨取。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_exotic_market_sell_followup_lines_rebellious_tier_zero_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被当成繁殖用家畜奴隶关进畜舍。",
            "不知从哪买来的男奴就那么拽着锁链在她身上挺腰，她的自由和人权一起被剥夺，只剩下贪图交配快感的本能。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_generic_sell_followup_lines(self, target: Character, price: int, market_kind: str) -> List[str]:
        market_label = self._get_sell_market_label(market_kind)
        lines = [f"就这样，{target.name} 被卖到了{market_label}。"]
        tier = self._get_sell_price_tier(price)
        if target.mark.get(3, 0) == 3:
            return self._build_sell_followup_rebellious_lines(target, price, market_kind, lines)
        if market_kind in {"default", "quick"}:
            special_lines = self._build_sell_followup_black_market_special_lines(target, price)
            if special_lines:
                return special_lines
        if market_kind == "pet":
            return self._build_sell_followup_pet_market_lines(target, price, lines)
        if market_kind == "exotic":
            return self._build_sell_followup_exotic_market_lines(target, price, tier, lines)
        return self._build_sell_followup_default_lines(target, price, tier, lines)






    def _build_lewd_demon_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        profile = self._get_sell_followup_profile(target)

        if profile["race_id"] != 9:
            return None
        if price >= 1_000_000:
            return self._build_lewd_demon_black_market_sell_followup_lines_high_value(target, profile)
        if price >= 500_000:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_high(target, profile)
        if price >= 100_000:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid(target, profile)
        return self._build_lewd_demon_black_market_sell_followup_lines_low(target, profile)






    def _build_lewd_demon_black_market_sell_followup_lines_high_value(self, target: Character, profile: Optional[Dict[str, Any]] = None) -> List[str]:
        profile = profile or self._get_sell_followup_profile(target)

        if profile["race_id"] != 9:
            return []
        if profile["warrior_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_high_value_warrior(target, profile["level"])
        if profile["knight_ninja_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_high_value_knight_ninja(target, profile["busty"])
        if profile["priest_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_high_value_priest(target, profile["busty"])
        if profile["meat_toilet"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_high_value_meat_toilet(target)
        return self._build_lewd_demon_black_market_sell_followup_lines_high_value_default(target)






    def _build_lewd_demon_black_market_sell_followup_lines_high_value_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被推上了大富豪的舞台，作为扩张奴隶被公开炫耀。",
            "她的股间被巨大的假阳具撑到极限，兴奋的客人们催促着主人亲手把玩这件昂贵的肉奴隶。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_high_value_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 在高级妓院彻底成了传说级的乳交娼妇。",
                "据说她只靠乳房就榨干过整整一支小队的精液，曾经身为勇者挥剑的模样已无人能够想象。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 在高级妓院成了预约爆满的高级娼妇。",
            "她日夜都渴求阴茎，甚至曾把初次接待的客人直接榨死，结果反而让想预约她的人越来越多。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_high_value_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 在掌声中被推上了大富豪的舞台，作为妊娠便器公开展示。",
            "排卵与阵痛诱发剂让她挺着夸张隆起的腹部参加所谓的“出产秀”，所有观众都在等着看她会生下什么。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_high_value_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 成了堕落神最上等的祭品之一。",
                "神官长以秘术完成了活祭仪式，而她也像是脱离现世一般，被带去了堕落神身边享受永恒快感。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被带进神殿深处，成了堕落神秘术仪式的一环。",
            "“堕落神即将降临”之类的流言后来四处流传，不过对你来说已经没什么意义了。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_high_value_warrior(
        self,
        target: Character,
        level: int,
    ) -> List[str]:
        if level >= 100:
            return [
                f"{target.name} 最终被谍报机关利用，甚至传出与山间小国君主结婚、借机煽动政局的消息。",
                "那场以稀有魔石之国为中心的骚动，对你来说已经只是无关紧要的远方传闻。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被谍报机关当成提审官使用。",
            "她那淫魔般的极品身体让讯问对象无论男女都被吸干精气而死，而这种生活对她来说似乎也算一种幸福。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_low(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        meat_toilet = bool(target.talent.get(204, 0))

        if warrior_like:
            return [
                f"{target.name} 成了酒吧周末活动里的特别赠品。",
                "她会作为飞镖比赛的靶子在魔法作用下把痛楚转成快感，而优胜者往往能当场侵犯已然发情的她。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if knight_ninja_like:
            return [
                f"{target.name} 夜里在主人的巢穴里被疼爱，白天则被租给乞丐朋友换酒钱。",
                "不论是丰满乳房被尽情玩弄，还是单纯沦为主人们共享的宠物，她似乎都对这种身份感到愉悦。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if priest_like:
            return [
                f"{target.name} 被安排进了量产触手的触手小屋。",
                "她不知道替那里培育了多少触手，最后彻底习惯了作为触手母体的生活，要一直持续到生命尽头。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if meat_toilet:
            return [
                f"{target.name} 被锁进公厕，成了无休止侍奉众人的公众便所。",
                "直到锁链解开的那天前，她大概都会在不断被侵犯的日常中替几百人生下孩子。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成公众肉便器昼夜不停地使用着。",
            "被你彻底调教过的淫乱身体不断吸收着市民的欲望，连呻吟都像成了最普通的日常。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_mid(self, target: Character) -> List[str]:
        context = self._build_lewd_black_market_context(target)
        if context["warrior_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_warrior(target, context["level"])
        if context["knight_ninja_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_knight_ninja(target)
        if context["priest_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_priest(target, context["busty"])
        if context["meat_toilet"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_meat_toilet(target)
        return self._build_lewd_demon_black_market_sell_followup_lines_mid_default(target)






    def _build_lewd_demon_black_market_sell_followup_lines_mid_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了赌场随奖附送的赠品。",
            "她被一再送给中奖者，又很快因为借债抵押而回到赌场手里，久而久之甚至传出了她会吸走财运的流言。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high(self, target: Character) -> List[str]:
        context = self._build_lewd_black_market_context(target)
        if context["warrior_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_high_warrior(target, context["level"])
        if context["knight_ninja_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_high_knight_ninja(target, context["busty"])
        if context["priest_like"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_high_priest(target, context["busty"])
        if context["meat_toilet"]:
            return self._build_lewd_demon_black_market_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_lewd_demon_black_market_sell_followup_lines_mid_high_default(target)






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被削成人棍，成了好事之徒的抱枕。",
            "手脚被砍断后还专门配上装饰，而她似乎无论被侵犯多少次都仍旧觉得不够。",
        )






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 在高级酒吧里与其说是女服务员，不如说更像主动勾引客人的妓女。",
                "她用高耸乳房去诱人把小费塞进乳沟，再立刻把客人拖进别的房间共度春宵。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了高级酒吧的表演者。",
            "从钢管舞到轮奸、从兽奸到分娩秀，她什么都演过，甚至连孩子长大后也还在这妖艳肉体旁继续荒唐地繁衍。",
        )






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被放置在屋中厕所里，成了任何人都能使用的肉便器。",
            "主人甚至专门请人负责清洁与保养她，每次使用后都细心维护，像是在照顾一件贵重器具。",
        )






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 从神殿开门到关门都被信徒侵犯着。",
                "在堕落神庇护下，她丰满乳房里即使未怀孕也会滴出母乳，最终彻底沉溺于无穷快感之中。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了堕落神的性奴。",
            "她在信徒中拥有极高人气，每次都会同时被数人狠狠玩弄，而她看起来竟也对此感到幸福。",
        )






    def _build_lewd_demon_black_market_sell_followup_lines_mid_high_warrior(
        self,
        target: Character,
        level: int,
    ) -> List[str]:
        if level >= 50:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了高级将校的保镖兼情人。",
                "即便已经堕落，原勇者的战斗力依旧不可小觑，而那发情生疼的肉体也夜夜被主人尽情疼爱。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了高级将校的情人。",
            "她那淫媚的身体总算遇上了能承受主人日夜征讨的强韧肉体，于是被当作长期性奴般豢养起来。",
        )






    def _build_lewd_demon_black_market_sell_followup_lines_mid_knight_ninja(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被摆进妓院橱窗里招揽客人。",
            "不论是乳房上的下流图案与乳环，还是脸侧刺上的淫纹，都让她成了熟客眼里离不开男人的刺青娼妇。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_mid_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被塞进赌场的侍奉房间，成了专门安抚输家们的肉便器。",
            "赌场特制筹码会被塞进她的私处与肛门，而她往后大概都只能作为这种泄愤玩具活下去了。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_mid_priest(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 成了黑酒吧里的乳奴隶。",
                "特制母乳果实让她分泌带有强烈催情成分的母乳，受优待的客人甚至能直接趴在她胸前饮用。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了黑酒吧的女侍应。",
            "嗑药或喝高的客人时常会把她按倒侵犯，而她甚至开始享受这种充满偶发性的混乱。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_demon_black_market_sell_followup_lines_mid_warrior(
        self,
        target: Character,
        level: int,
    ) -> List[str]:
        if level >= 30:
            return [
                f"{target.name} 在黑帮里被委以重任，成了真正的成员。",
                "她每晚都用淫秽肉体和部下交欢来维系团队团结，往后会在这种黑暗世界里活成什么样已无人能料。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了黑社会成员们轮流侍奉的情妇。",
            "对一天都离不开性爱的她来说，这样的环境甚至称得上相当合适。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_non_demon_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        context = self._build_lewd_black_market_party_context(target)
        if context["is_demon"]:
            return None

        if price >= 1_000_000:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value(target, context)

        if price >= 500_000:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_mid_high(target, context)

        if price >= 100_000:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_mid(target, context)

        return self._build_lewd_non_demon_black_market_sell_followup_lines_low(target, context)






    def _build_lewd_non_demon_black_market_sell_followup_lines_high_value(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value_warrior(target, context["level"])
        if context["knight_ninja_like"]:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value_knight_ninja(target)
        if context["priest_like"]:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value_priest(target, context["busty"])
        if context["meat_toilet"]:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value_meat_toilet(target)
        return self._build_lewd_non_demon_black_market_sell_followup_lines_high_value_default(target)






    def _build_lewd_non_demon_black_market_sell_followup_lines_low(
        self,
        target: Character,
        busty: bool,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        meat_toilet: bool,
        vagina_sense: int,
    ) -> List[str]:
        if warrior_like:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_low_warrior(target, vagina_sense)
        if knight_ninja_like:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_low_knight_ninja(target)
        if priest_like:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_low_priest(target, busty)
        if meat_toilet:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_low_meat_toilet(target, True)
        return self._build_lewd_non_demon_black_market_sell_followup_lines_low_meat_toilet(target, False)






    def _build_lewd_non_demon_black_market_sell_followup_lines_low_knight_ninja(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了酒吧周末飞镖比赛里的玩具。",
            "无论是被射得鲜血淋漓的高耸乳房，还是千疮百孔的身体，她都只能作为优胜奖金的一部分被人围观。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_non_demon_black_market_sell_followup_lines_low_meat_toilet(self, target: Character, dirty: bool) -> List[str]:
        if dirty:
            return [
                f"{target.name} 继续以现役肉便器的身份侍奉公众。",
                "在漫长岁月里，她像公共设施一样被市民反复疼爱，据说最后甚至生下了不下一百个孩子。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了昼夜不停被使用的公众肉便器。",
            "那种过于残酷的生活让她不到半年便精神崩溃，而身体却仍会继续被开放给所有路过的人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_non_demon_black_market_sell_followup_lines_low_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被安排进触手小屋，成了量产触手的豪乳苗床。",
                "她那膨胀到原本两倍大小的乳房所培育出的触手格外值钱，于是这辈子大概都只能这样被榨干价值。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被安排进触手小屋，成了量产触手的母体。",
            "她不知道已培育出多少触手，整个人也已完全适应了这种身份，直到死去恐怕都无法离开。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_non_demon_black_market_sell_followup_lines_low_warrior(
        self,
        target: Character,
        vagina_sense: int,
    ) -> List[str]:
        if vagina_sense >= 5:
            return [
                f"{target.name} 被当成矿工们的慰问品饲养着。",
                "即便连续被侵犯数次也不肯屈服，那份倔强只会让矿工们抱怨她一点都不可爱。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成矿工们的慰问品饲养着。",
            "她几次被侵犯时都嚎啕大哭，而矿工们偏偏就觉得这很有趣，于是她反倒变得格外受欢迎。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_lewd_non_demon_black_market_sell_followup_lines_mid(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        return self._build_lewd_non_demon_black_market_sell_followup_lines_mid_route(target, context)






    def _build_lewd_non_demon_black_market_sell_followup_lines_mid_high(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_lewd_non_demon_black_market_sell_followup_lines_mid_high_warrior(target, context["vagina_sense"])
        if context["knight_ninja_like"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了隔着橱窗招揽客人的橱窗娼妇。",
                "从裸露衣着下被刺上淫纹的胸部，到总被同一个男人包夜侵犯到失禁的身体，她最终还是拒绝了任何赎身的可能。",
            )
        if context["priest_like"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了黑酒馆里的瘾君子。",
                "无论是必须定期被榨取的致幻母乳，还是毒品带来的甘甜喘息与吞精快感，都已经让她离不开这种沉沦。",
            )
        if context["meat_toilet"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被塞进赌场侍奉房间，成了专门安抚输家们的肉便器。",
                "特制筹码不断被塞进她的私处与肛门，而这辈子大概也只能在赌徒间充当这样的玩具了。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了赌场的赠品。",
            "她刚被送给中了大奖的客人，转眼又会在把奴隶当赌注的牌局中被重新押上桌面，最后在数十名赌徒之间不停转手。",
        )






    def _build_lewd_non_demon_black_market_sell_followup_lines_mid_high_warrior(self, target: Character, vagina_sense: int) -> List[str]:
        if vagina_sense >= 5:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了黑帮干部的情妇。",
                "在卓越调教下彻底堕落的她被放进别墅，每晚都用自己的身体去操纵和笼络不同的男人。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了虐待狂干部的情妇。",
            "最初她也为这种生活感到困惑，可夜夜上演的过激玩法最终还是让她彻底沉迷于其中。",
        )






    def _build_lewd_non_demon_black_market_sell_followup_lines_mid_priest(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被拴进触手小屋，成了培育量产触手的苗床。",
                "尤其是那膨胀到原本两倍大小的惊人豪乳，所培育出的触手格外价值连城。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被安排在量产触手的触手小屋里，成了彻底适应一切的母体。",
            "她不知道已经培育出多少触手，而这样的日子恐怕会持续到她死去的那一天。",
        )






    def _build_lewd_non_demon_black_market_sell_followup_lines_mid_route(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了酒吧周末特别竞赛里的赠品。",
                "她作为飞镖靶子在魔法作用下把痛楚化成电击般快感，谁能逼她叫得最大声，谁就能成为那场竞赛的优胜者。",
            )
        if context["knight_ninja_like"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 夜里在主人的巢穴里被疼爱，白天则被租给乞丐朋友换酒钱。",
                "无论是丰满乳房被毫不客气地玩弄，还是刚生下的孩子立刻又被卖掉，她都只能更频繁地被转租出去。",
            )
        if context["priest_like"]:
            if context["busty"]:
                return self._build_sell_followup_lines_pair_and_ending(
                    target,
                    f"{target.name} 被拴进触手小屋，成了培育量产触手的苗床。",
                    "尤其是那膨胀到原本两倍大小的惊人豪乳，所培育出的触手格外价值连城。",
                )
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被安排在量产触手的触手小屋里，成了彻底适应一切的母体。",
                "她不知道已经培育出多少触手，而这样的日子恐怕会持续到她死去的那一天。",
            )
        if context["meat_toilet"]:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 继续以现役肉便器的身份被公众使用着。",
                "漫长岁月里，她像公共设施一样侍奉着市民，甚至已经为几百人生下过孩子。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了不分昼夜都被使用的公众肉便器。",
            "她每次被男人侵犯时都会甜腻呻吟，被你彻底调教过的淫乱身体就这样不断吸收着整座城市的欲望。",
        )






    def _build_loving_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        profile = self._get_sell_followup_profile(target)

        if profile["race_id"] != 9:
            return None

        if price >= 1_000_000:
            return self._build_loving_black_market_sell_followup_lines_high_value(target, profile)
        if price >= 500_000:
            return self._build_loving_black_market_sell_followup_lines_mid_high(target, profile)
        if price >= 100_000:
            return self._build_loving_black_market_sell_followup_lines_mid(target, profile)
        return self._build_loving_black_market_sell_followup_lines_low(target, profile)






    def _build_loving_black_market_sell_followup_lines_high_value(self, target: Character, profile: Optional[Dict[str, Any]] = None) -> List[str]:
        profile = profile or self._get_sell_followup_profile(target)

        if profile["race_id"] != 9:
            return []
        if profile["warrior_like"]:
            return self._build_loving_black_market_sell_followup_lines_high_value_warrior(target, profile["sex_crazed"])
        if profile["knight_ninja_like"]:
            return self._build_loving_black_market_sell_followup_lines_high_value_knight(target, profile["busty"])
        if profile["priest_like"]:
            return self._build_loving_black_market_sell_followup_lines_high_value_priest(target, profile["anal_crazed"])
        if profile["negotiation_skill"] >= 5:
            return self._build_loving_black_market_sell_followup_lines_high_value_negotiated(target)
        return self._build_loving_black_market_sell_followup_lines_high_value_default(target)






    def _build_loving_black_market_sell_followup_lines_high_value_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被魔界土豪买下后，作为第八个情妇如影随形地侍奉主人。",
            "她温柔得不太像魔族喜爱的类型，却很受那一大家子的孩子欢迎，最后也在宠爱中被长期占有。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_high_value_knight(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 被魔界贵族买下后，成了备受宠爱的宠物兼情人。",
                "每晚都被细致地玩弄乳房，在床榻间不断喘息，日子反而显得有些安逸。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被魔界贵族买下后，在屋里兼做女仆与情人。",
            "只要主人高兴就会被叫去陪寝，甚至连怀孕与堕胎都像是迟早会发生的命运。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_high_value_negotiated(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被魔界土豪买下后，很快因为枕边妙语与交涉本领而被当成了秘书。",
            "机智的应对与性感的身体一起为主人牟利，每晚客厅里都回荡着她被疼爱的呻吟。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_high_value_priest(self, target: Character, anal_crazed: bool) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 被堕落神的神官长买下后，作为近侍留在神殿中工作。",
                "为了更好地供奉堕落神，她的肛门被深度调教，最终成了连巨魔都能轻易进入的菊奴女神官。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被堕落神的神官长买下后，成了对方众多情妇中的一人。",
            "曾经的神职者如今夜夜歌颂堕落神，在亵渎与快感中不断堕落下去。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_high_value_warrior(self, target: Character, sex_crazed: bool) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被魔王军将军买走后，作为性奴留在了对方身边。",
                "她那无论被怎样粗暴对待都只会愉悦起来的肉体，很快让这段关系从占有变得近似宠爱。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被魔王军将军买走后，夜夜都以性奴隶的身份被粗暴侵犯。",
            "只靠原勇者级别的耐久勉强支撑着身体，仿佛随时都会被彻底玩坏。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_low(self, target: Character, profile: Optional[Dict[str, Any]] = None) -> List[str]:
        profile = profile or self._get_sell_followup_profile(target)

        if profile["warrior_like"]:
            return self._build_loving_black_market_sell_followup_lines_low_warrior(target, profile["sex_crazed"])
        if profile["knight_ninja_like"]:
            return self._build_loving_black_market_sell_followup_lines_low_knight(target, profile["busty"])
        if profile["priest_like"]:
            return self._build_loving_black_market_sell_followup_lines_low_priest(target, profile["busty"])
        if profile["meat_toilet"]:
            return self._build_loving_black_market_sell_followup_lines_low_meat_toilet(target)
        return self._build_loving_black_market_sell_followup_lines_low_default(target)






    def _build_loving_black_market_sell_followup_lines_low_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被当成公众肉便器不分昼夜地使用着。",
            "过于残酷的生活最终让她一边呼喊着你曾经的名字，一边彻底坏掉。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_low_knight(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 被卖进酒吧后，因傲人的胸部被要求赤裸上身接客。",
                "客人们毫不客气地把玩着她的乳房，而她也开始在意小费，甚至会主动挺胸去讨好他们。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被卖进酒吧后，店主总会特意向客人强调她可以出台。",
            "身为异族少女的她仍旧相当有人气，只是大多数皮肉钱都会被主人直接拿走。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_low_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 继续以现役肉便器的身份侍奉着公众。",
            "在漫长岁月里，她像公共设施一样被无数市民使用着，甚至生下了不下一百个孩子。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_low_priest(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 因丰满乳房被拴进厩舍，当成牛奴隶饲养。",
                "怀上牛系魔兽的孩子后，她的乳房又被注射肥大药剂，往后只能像乳牛般被日复一日地榨取。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被迫与各种家畜交配，以便制造新品种的家畜。",
            "虽然暂时还没有成果，但只要实验继续下去，总有一天会在她身上见效。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_low_warrior(self, target: Character, sex_crazed: bool) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被当成矿工们的慰问品饲养着。",
                "即便被连续侵犯多次也不肯屈服，于是等待她的只会是越来越粗暴的对待。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成矿工们的慰问品饲养着。",
            "她几次被侵犯时都嚎啕大哭，这份反应反倒让矿工们觉得有趣，于是变得格外受欢迎。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_mid(self, target: Character, profile: Optional[Dict[str, Any]] = None) -> List[str]:
        profile = profile or self._get_sell_followup_profile(target)

        if profile["warrior_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_warrior(target, profile["sex_crazed"])
        if profile["knight_mage_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_knight_mage(target, profile["busty"])
        if profile["priest_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_priest(target, profile["anal_crazed"])
        if profile["meat_toilet"]:
            return [
                f"{target.name} 被魔界商人买下后，作为店里的肉便器被锁进了厕所。",
                "不论客人还是店员都能随意使用她，甚至连怀孕都被当成了展示“出产秀”的噱头。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被妖术师当成素材买走了。",
            "她的身体被依照客户需求改造出新的附加价值，随后又被转卖给了别人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_black_market_sell_followup_lines_mid_high(self, target: Character, profile: Optional[Dict[str, Any]] = None) -> List[str]:
        profile = profile or self._get_sell_followup_profile(target)

        if profile["warrior_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_high_warrior(target, profile["thief_like"])
        if profile["knight_ninja_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_high_knight(target, profile["busty"])
        if profile["priest_like"]:
            return self._build_loving_black_market_sell_followup_lines_mid_high_priest(target, profile["anal_crazed"])
        if profile["meat_toilet"]:
            return self._build_loving_black_market_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_loving_black_market_sell_followup_lines_mid_high_default(target)






    def _build_loving_black_market_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被魔界大商人买走后，老老实实地侍奉着主人。",
            "每晚她都与正室一同服侍商人，据说怀上的孩子也被当成宠物一样抚养起来了。",
        )






    def _build_loving_black_market_sell_followup_lines_mid_high_knight(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被地方领主买下后，穿着低胸女仆装在宅邸里侍奉。",
                "白天遭受下流目光与揩油，夜里则被领主彻底占有，最后成了领主的女仆。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被地方领主买下后，像玩具一样被留在年幼主人的身边。",
            "她过上了如同布娃娃般任人摆弄的生活，而这种日子看起来还会持续很久。",
        )






    def _build_loving_black_market_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被魔界大商人买走后，作为员工们的肉便器被长期放置在公司里。",
            "十几年间她生下许多连父亲是谁都不明的孩子，而那些孩子很快也会被转卖出去。",
        )






    def _build_loving_black_market_sell_followup_lines_mid_high_priest(self, target: Character, anal_crazed: bool) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送进了堕落神神殿，成了为神殿献身的贡品。",
                "在络绎不绝的信徒侵犯下，她越来越淫靡的呻吟像是在不断讨好堕落神。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被送进了堕落神神殿，成了所有信徒都可无偿侵犯的贡品。",
            "就连被侵犯后生下的孩子也在神殿中抚养，她自己也逐渐全心信奉起了堕落神。",
        )






    def _build_loving_black_market_sell_followup_lines_mid_high_warrior(self, target: Character, thief_like: bool) -> List[str]:
        if thief_like:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被黑帮首领买走后，很快凭借旧日盗贼经验融入了黑社会生活。",
                "她后来成了首领的情人，在繁华都市中习惯了被每天疼爱的日子。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被黑帮首领买走后，以原本战士的本领做起了保镖般的工作。",
            "与此同时，她也作为首领的情人被日复一日地占有着。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        race_id = int(target.talent.get(314, 0))
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        knight_mage_like = self._has_sell_job_talent(target, 205, 201)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        meat_toilet = bool(target.talent.get(204, 0))
        negotiation_skill = int(target.abl.get(15, 0))
        thief_like = bool(target.talent.get(203, 0))

        if race_id == 9:
            return None
        if price >= 1_000_000:
            return self._build_loving_non_demon_black_market_sell_followup_lines_high_value(target)
        if price >= 500_000:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high(target)
        if price >= 100_000:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid(target)
        return self._build_loving_non_demon_black_market_sell_followup_lines_low(target)






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        negotiation_skill = int(target.abl.get(15, 0))

        if warrior_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_high_value_warrior(target, sex_crazed)
        if knight_ninja_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_high_value_knight(target, busty)
        if priest_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_high_value_priest(target, anal_crazed)
        if negotiation_skill >= 5:
            return self._build_loving_non_demon_black_market_sell_followup_lines_high_value_negotiated(target)
        return self._build_loving_non_demon_black_market_sell_followup_lines_high_value_default(target)






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被当成土豪的宠物买下后，对主人表现得异常顺从。",
            "主人的孩子们也很喜欢她，这份被多次弄怀孕与分娩的生活，反倒像成了她作为宠物的最高幸福。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value_knight(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 因傲人的双峰被魔界贵族买下，最终成了摆放宝石的人体家具。",
                "拘束衣托起丰满乳房，乳环与针刺伤痕被当作装饰，她的身体本身就成了主人的陈设。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被魔界贵族当成专用宠物饲养起来。",
            "她被刻意避免弄伤地用拘束具锁着，四肢着地像狗一样爬行，只要主人命令就会像牝犬般交配。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value_negotiated(self, target: Character) -> List[str]:
        return [
            f"{target.name} 原本只是被当作性奴买回来的，却因能说会道而成了土豪的宴客工具。",
            "为了让商谈占优，主人常命她陪侍其他男人，而她也在这样的夜晚里反复怀孕分娩。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value_priest(self, target: Character, anal_crazed: bool) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 被堕落神的神官长买下后，成了劝人改信堕落神的菊奴女神官。",
                "她一边被粗硬阴茎侵犯着肛门，一边听着布教的话语，仿佛迟早也会彻底改宗。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了神官长的奴隶后，每晚都参加妖邪的仪式。",
            "对于正神信徒肮脏不堪的祭礼，如今的她却像被魅惑般主动沉溺其中。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_high_value_warrior(self, target: Character, sex_crazed: bool) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被魔王军将军买走后，作为异族性奴得到了近乎罕见的优待。",
                "她那无论如何粗暴对待都只会愉悦起来的身体，让将军几乎宠她到亲手喂饭的地步。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被魔王军将军买走后，夜夜都作为性奴被粗暴侵犯。",
            "若真有一天被彻底玩坏，主人的房间里大概只会再多出一具标本。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_low(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        meat_toilet = bool(target.talent.get(204, 0))

        if warrior_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_low_warrior(target, sex_crazed)
        if knight_ninja_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_low_knight(target, busty)
        if priest_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_low_priest(target, busty)
        if meat_toilet:
            return self._build_loving_non_demon_black_market_sell_followup_lines_low_meat_toilet(target, True)
        return self._build_loving_non_demon_black_market_sell_followup_lines_low_meat_toilet(target, False)






    def _build_loving_non_demon_black_market_sell_followup_lines_low_knight(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被卖进酒吧后，因傲人的胸部被要求赤裸上身接客。",
                "客人们毫不客气地把玩着她的乳房，而她也开始在意小费，甚至会主动挺胸去讨好他们。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被卖进酒吧后，店主总会特意向客人强调她可以出台。",
            "身为异族少女的她仍旧相当有人气，只是大多数皮肉钱都会被主人直接拿走。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_low_meat_toilet(self, target: Character, dirty: bool) -> List[str]:
        if dirty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 继续以现役肉便器的身份侍奉着公众。",
                "在漫长岁月里，她像公共设施一样被无数市民使用着，甚至生下了不下一百个孩子。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被当成公众肉便器不分昼夜地使用着。",
            "过于残酷的生活最终让她一边呼喊着你曾经的名字，一边彻底坏掉。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_low_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 因丰满乳房被拴进厩舍，当成牛奴隶饲养。",
                "怀上牛系魔兽的孩子后，她的乳房又被注射肥大药剂，往后只能像乳牛般被日复一日地榨取。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被迫与各种家畜交配，以便制造新品种的家畜。",
            "虽然暂时还没有成果，但只要实验继续下去，总有一天会在她身上见效。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_low_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被当成矿工们的慰问品饲养着。",
                "即便被连续侵犯多次也不肯屈服，于是等待她的只会是越来越粗暴的对待。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被当成矿工们的慰问品饲养着。",
            "她几次被侵犯时都嚎啕大哭，这份反应反倒让矿工们觉得有趣，于是变得格外受欢迎。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        knight_mage_like = self._has_sell_job_talent(target, 205, 201)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        meat_toilet = bool(target.talent.get(204, 0))

        if warrior_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_warrior(target, sex_crazed)
        if knight_mage_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_knight_mage(target, busty)
        if priest_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_meat_toilet(target, True)
        return self._build_loving_non_demon_black_market_sell_followup_lines_mid_meat_toilet(target, False)






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        meat_toilet = bool(target.talent.get(204, 0))
        thief_like = bool(target.talent.get(203, 0))
        anal_crazed = bool(target.talent.get(77, 0))

        if warrior_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high_warrior(target, thief_like)
        if knight_ninja_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high_knight_ninja(target, busty)
        if priest_like:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_loving_non_demon_black_market_sell_followup_lines_mid_high_default(target)






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被大商人当成宠物买下，彻底失去了原勇者的自尊。",
            "她被从头到尾按宠物方式教育，甚至得到了“若再多学点技艺就能参加品评会”的评价。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 成了负责提供母乳的人形奶牛。",
                "她和挤奶工一起住在小屋里，茶会时还要亲手挤出鲜奶献给主人与客人。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 成了供客人使用的宴客肉被子。",
            "她接待了各种种族的来客，甚至得到了不错评价，生下的几个孩子也被宅邸里的仆人们一同抚养。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被当成员工们的肉便器长期放置在公司里。",
            "十几年间生下许多连父亲都不明的孩子，那些孩子也会很快被再度卖掉。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送进堕落神神殿后，成了广受信徒欢迎的贡品。",
                "因为被异族与异教徒侵犯也被当成功德，她那淫乱的肛门几乎接受了所有人的阴茎。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被送进堕落神神殿后，成了排着长队也要被侵犯的贡品。",
            "昔日信奉其他神明的她，早晚会从心底彻底变成堕落神的信徒。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_high_warrior(
        self,
        target: Character,
        thief_like: bool,
    ) -> List[str]:
        if thief_like:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被黑帮首领当成顺从宠物买下，慢慢也学会和主人一起“努力”活下去。",
                "过去试过多次逃跑的她，在意识到项圈和手铐根本解不开后终于老实下来，还得到了相对宽松的自由。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被黑帮首领买下后，作为顺从宠物陪伴主人。",
            "堕落的身体让她几乎忘了自己曾是勇者，甚至连被主人践踏都开始感到快感。",
        )






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_knight_mage(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被魔界学院买下后，乳房成了淫虫培养实验的苗床。",
                "蠢蠢欲动的淫虫分泌奇妙体液，让她持续浸在甜美快感中，而这实验若成功还会带来新的媚药。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了学院学生们每天都会使用的玩具。",
            "哪怕上课途中被侵犯也是常态，老师甚至会以“妨碍上课”为由当众鞭打她来进一步煽动欲望。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_meat_toilet(self, target: Character, dirty: bool) -> List[str]:
        if dirty:
            return [
                f"{target.name} 作为坏掉旧肉便器后的替代品，被重新锁进了厕所里。",
                "不论客人还是员工都能随意使用她，连什么时候生出什么孩子都被拿来开赌局。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被妖术师当作素材买下了。",
            "对方正烦恼该如何使用“原勇者”这种稀有素材，最后大概还是会按客人的偏好继续改造她。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 被大农场主顺手买下后，过上了谁都可以玩弄她的奴隶生活。",
                "巨大的阴茎一再蹂躏之后，她如今只能瘫在床上，身上还带着脱肛的痕迹。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成大农场主送给儿子们的礼物。",
            "在彻底被玩弄并怀孕后，她如今像所有人的生育奴隶一样被“疼爱”着。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_non_demon_black_market_sell_followup_lines_mid_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被年轻士官用第一次军功的奖金买下。",
                "对那位士官而言，她更像可爱的恋人而非单纯的性奴，而她也夜夜以身体侍奉着对方。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被年轻士官用第一次军功的奖金买下。",
            "她并未完全屈服，却每天都在半推半就中被对方品尝着身体，关系更像畸形的恋人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines(
        self, target: Character, price: int
    ) -> Optional[List[str]]:
        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_core(target, price)






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_core(
        self, target: Character, price: int
    ) -> Optional[List[str]]:
        race_id = int(target.talent.get(314, 0))
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        knight_mage_like = self._has_sell_job_talent(target, 205, 201)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        busty = self._is_sell_busty_target(target)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        negotiation_skill = int(target.abl.get(15, 0))
        thief_like = bool(target.talent.get(203, 0))
        meat_toilet = bool(target.talent.get(204, 0))

        if race_id != 9 or not (target.talent.get(85, 0) or target.talent.get(76, 0)):
            return None

        if price >= 1_000_000:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value(
                target, warrior_like, knight_ninja_like, priest_like, busty, anal_crazed, negotiation_skill
            )

        if price >= 500_000:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high(
                target, warrior_like, knight_ninja_like, priest_like, busty, anal_crazed, thief_like, meat_toilet
            )

        if price >= 100_000:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid(
                target, warrior_like, knight_mage_like, priest_like, busty, sex_crazed, anal_crazed, meat_toilet
            )

        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low(
            target, warrior_like, knight_ninja_like, knight_mage_like, priest_like, busty, sex_crazed, meat_toilet
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value(
        self,
        target: Character,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        busty: bool,
        anal_crazed: bool,
        negotiation_skill: int,
    ) -> List[str]:
        if warrior_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_warrior(target)
        if knight_ninja_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_knight_ninja(target, busty)
        if priest_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_priest(target, anal_crazed)
        if negotiation_skill >= 5:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_negotiation(target, True)
        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_negotiation(target, False)






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了上级恶魔的女仆。",
                "露出乳头的女仆装下，她那对豪乳与长期勃起的乳头总会暴露无遗；每次被主人发现，就得接受更加淫秽的惩罚。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了上级恶魔的女仆。",
            "只要犯下一点小错，主人就会立刻发动让她当场自慰的诅咒；可最近的她，甚至已经学会故意犯错来换取公开自渎的机会。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_negotiation(
        self,
        target: Character,
        high_skill: bool,
    ) -> List[str]:
        if high_skill:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 用巧言说服了魔兽研究设施的研究员。",
                "她逐渐主导起试验品的采购与使用，每天都在听着那些被她买回来的交配奴隶悲鸣时自慰取乐。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了魔兽交配实验用的奴隶。",
            "如今的她被强制与怪物交合，甚至开始在交配时忘情呼喊实验魔兽的名字，像恋人一样扭腰亲吻那些怪物。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 在异形之神的神殿里照顾着变异信徒。",
                "那些连行走和进食都需要照料的怪物，只要那可怕的阴茎一勃起，还得由她用后庭亲自去安抚平复。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 在异形之神的神殿里照顾着变异信徒。",
            "作为神明的新娘，她的子宫被视作所有信徒的公共财产，如今甚至已经怀上了异形的孩子。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_high_value_warrior(
        self,
        target: Character,
    ) -> List[str]:
        if target.talent.get(75, 0):
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了暗黑龙的新娘。",
                "在龙之洞窟里，她一边接受那条暗黑龙的蹂躏与播种，一边为濒危的龙族反复怀孕产子；最近甚至已经开始为那过度频繁的播种而叫苦不迭。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了暗黑龙的新娘。",
            "她那魔族的身体在龙的挞伐与种子中孕育出了几只幼龙，连肉体本身也按暗黑龙的喜好持续被改造下去。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_low(
        self,
        target: Character,
        warrior_like: bool,
        knight_ninja_like: bool,
        knight_mage_like: bool,
        priest_like: bool,
        busty: bool,
        sex_crazed: bool,
        meat_toilet: bool,
    ) -> List[str]:
        if warrior_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low_warrior(target, sex_crazed)
        if knight_ninja_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low_knight_ninja(target, busty)
        if priest_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low_meat_toilet(target, True)
        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_low_meat_toilet(target, False)






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_low_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了巨魔苦力们共用的飞机杯。",
                "那些巨魔完全不懂怜香惜玉，只会把她粗暴地套在阴茎上疯狂抽插，就连从丰乳里挤出的奶水也被直接拿来解渴。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了巨魔苦力们共用的飞机杯。",
            "她被改造成只能依赖巨魔精液生存，日子久了，脸上甚至会自己浮现出既淫荡又扭曲的满足神情。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_low_meat_toilet(
        self,
        target: Character,
        dirty: bool,
    ) -> List[str]:
        if dirty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 被全裸摆进街角的杂耍小屋里招揽客人。",
                "她那被淫秽改造成怪诞形状的性器与夸张膨胀的乳房，引得路人纷纷驻足；最近甚至已经开始和丑陋扶她奴隶公开交欢表演。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 被全裸摆进街角的杂耍小屋里招揽客人。",
            "她被改造出畸形的阴茎，在街头公开自慰到射得阳痿；听说后来甚至学会把那软塌塌的器官塞进自己体内取乐。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_low_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了黑暗精灵学者的新发明实验体。",
                "特殊假阳具昼夜不停蹂躏着她的肛门，学者们想借此开发出比阴道快感更极端、更无法忍耐的新式性拷问。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了黑暗精灵学者的新型媚药实验体。",
            "新药注射与发狂绝顶一遍遍重复后，如今哪怕只是微风吹过，她都会立刻抽搐着高潮，甚至连“忍耐快感”的反向实验都开始在她身上展开。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_low_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 作为佣兵团一员被招募了。",
                "性欲旺盛的她常常在训练途中偷偷替兽人同伴口交，渐渐把整支佣兵团都拖进了更混乱淫靡的风气里。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 作为佣兵团一员被招募了。",
            "她被团长看上，坚持要和她生下孩子，于是每个夜晚都只能在团长一遍遍播种里慢慢习惯这份粗暴占有。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid(
        self,
        target: Character,
        warrior_like: bool,
        knight_mage_like: bool,
        priest_like: bool,
        busty: bool,
        sex_crazed: bool,
        anal_crazed: bool,
        meat_toilet: bool,
    ) -> List[str]:
        if warrior_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_warrior(target, sex_crazed)
        if knight_mage_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_knight_mage(target, busty)
        if priest_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_meat_toilet(target, True)
        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_meat_toilet(target, False)






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high(
        self,
        target: Character,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        busty: bool,
        anal_crazed: bool,
        thief_like: bool,
        meat_toilet: bool,
    ) -> List[str]:
        if warrior_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_warrior(target, thief_like)
        if knight_ninja_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_knight_ninja(target, busty)
        if priest_like:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_meat_toilet(target, True)
        return self._build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_meat_toilet(target, False)






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 过上了抚养半人马孩子的生活。",
                "丰满乳房持续供给着母乳，她看着那些拥有惊人尺寸阴茎的幼驹渐渐长大，甚至开始盘算着进行“禁断的性教育”。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了半人马骑士团的侍从。",
            "她要负责一切杂役，甚至不被允许在下半身穿任何衣物；性欲旺盛的半人马们常常会突然把她推倒，当场尽情侵犯。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_meat_toilet(
        self,
        target: Character,
        dirty: bool,
    ) -> List[str]:
        if dirty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 作为宴客用肉便器，在兽人富商宅邸里占据了特殊地位。",
                "“把勇者当肉便器”这件事极大满足了主人的虚荣心，于是她被摆在书房角落，在主人与宾客的视线下毫无顾忌地疯狂自慰。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 作为爱人被买回了兽人富商家中。",
            "那位富商完全倾心于她，每天都用珠宝与华服精心打扮她；久而久之，她整个人连气质都变得像真正的贵妇一样。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 作为优秀的祭典演员，受到了牛头人祭司们的赞赏。",
                "每次仪式，她都要一边用肛门自慰，一边跳出淫乱舞蹈；那枚被扩张到极限的后穴，已经以扭曲又妖艳的方式盛开了。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了牛头人神殿的圣母。",
            "为了生下混血而强大的牛头人后代，她正不断经历神殿仪式，如今甚至已在分娩那位牛面之神的孩子。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_high_warrior(
        self,
        target: Character,
        thief_like: bool,
    ) -> List[str]:
        if thief_like:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了食人魔佣兵团的后勤与支援成员。",
                "她专心负责资产、装备与物资采购，肚子则夸张地鼓了起来，正孕育着团长亲手播下的下一任继承者。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了食人魔佣兵团的战士。",
            "比起奴隶时代，她的肌肉与筋骨都被锻炼得更强壮了，而食人魔们也越来越沉迷于这份强大战力本身带来的性魅力。",
        )






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_knight_mage(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 成了黑暗精灵学校的讲师。",
                "她那呼之欲出的胸部让少年学生们充满憧憬；可最近与黑暗精灵少年的淫行败露后，她已经被刺上了“淫行老师”的耻辱纹样。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了黑暗精灵学校的讲师。",
            "经验丰富的她几乎和全班男生都维持着性关系，甚至还把手伸向了几名女学生；据说保健课上，整班人都会和她一起进行性实习。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_meat_toilet(
        self,
        target: Character,
        dirty: bool,
    ) -> List[str]:
        if dirty:
            return [
                f"{target.name} 在狼人的赌场里成了供人下注观赏的肉便器。",
                "被改造成能怀上犬种的身体后，她不断表演着遭狼人侵犯的戏码，观众们则围着“第几次会怀孕”这种赌局兴奋下注。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 在狼人的赌场里成了扶她玩具。",
            "她被改造成不能在让母狼高潮前射精的异形肉具，赌客们则围着“到底能狠狠干多少个女狼人”这种问题热烈下注。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 在魔像的大农场里负责生产肥料。",
                "大量饲料与残羹被灌进她像孕妇般胀起的肚子，在被改造过的内脏里发酵，最后随着淫靡娇喘化成高品质肥料排出。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了魔像体内的生物零件。",
            "她全身都被封进魔像里，大脑一片空白，只剩下操纵巨躯行动与永恒感受胯间、乳头慰安装置快感这两件事。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_demon_exotic_sell_followup_lines_mid_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 成了六头海蛇联防队的外籍战士。",
                "她原本在共同训练与战斗中表现得十分活跃，却因为性欲旺盛，老是在训练间隙偷偷和别的海蛇交合，最后甚至被强行装上贞操带。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了六头海蛇联防队的外籍战士。",
            "在共同磨砺与战斗中，她逐渐与那些海蛇建立起信赖，最近甚至传出了要和队里某位年轻海蛇成婚的消息。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_exotic_sell_context(self, target: Character) -> Dict[str, Any]:
        return {
            "race_id": int(target.talent.get(314, 0)),
            "warrior_like": self._has_sell_job_talent(target, 200, 203),
            "knight_ninja_like": self._has_sell_job_talent(target, 205, 207),
            "knight_mage_like": self._has_sell_job_talent(target, 205, 201),
            "priest_like": self._has_sell_job_talent(target, 202, 206),
            "busty": self._is_sell_busty_target(target),
            "sex_crazed": bool(target.talent.get(75, 0)),
            "anal_crazed": bool(target.talent.get(77, 0)),
            "negotiation_skill": int(target.abl.get(15, 0)),
            "thief_like": bool(target.talent.get(203, 0)),
            "meat_toilet": bool(target.talent.get(204, 0)),
            "is_demon": int(target.talent.get(314, 0)) == 9,
            "is_exotic": bool(target.talent.get(85, 0) or target.talent.get(76, 0)),
        }






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines(
        self, target: Character, price: int
    ) -> Optional[List[str]]:
        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_core(target, price)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_core(
        self, target: Character, price: int
    ) -> Optional[List[str]]:
        context = self._build_loving_or_lewd_exotic_sell_context(target)
        if context["is_demon"] or not context["is_exotic"]:
            return None

        if price >= 1_000_000:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value(target, context)

        if price >= 500_000:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high(target, context)

        if price >= 100_000:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid(target, context)

        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low(target, context)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_warrior(target, context["sex_crazed"])
        if context["knight_ninja_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_knight_ninja(target, context["busty"])
        if context["priest_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_priest(target, context["anal_crazed"])
        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_negotiation(target, context["negotiation_skill"] >= 5)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了狮鹫快递的看板骑手。",
                "表面上她骑着狮鹫四处送件，实际上却靠上门侍奉赚取更多指名费；那对惹眼的豪乳让她很快成了最出名的招牌。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了狮鹫快递的骑手。",
            "白天她像信使一样穿梭各地，夜里则以上门服务的妓女身份继续被使用，甚至因口技出名而越来越受欢迎。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_negotiation(
        self,
        target: Character,
        high_skill: bool,
    ) -> List[str]:
        if high_skill:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了哥布林大剧场的偶像。",
                "她穿着欲盖弥彰的下流布条，在台上唱着黄色小调、扭动着身体，剧场总是被哥布林观众挤得水泄不通。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了哥布林大剧场的偶像。",
            "哪怕只是披着几块勉强称得上衣服的布条，她那淫靡舞姿也足以让越来越多的哥布林为她疯狂。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了蛇妖高级妓院里专卖后庭的头牌。",
                "异种名流们把她当成少见的珍品排队等候，就连平常会被别家拒之门外的异形客人，也都挤在门前想一亲芳泽。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 在蛇妖的高级妓院里工作着。",
            "哪怕怀上异形的孩子，她也仍要为偏爱孕妇的客人张开双腿，渐渐成了异种名流间颇有名气的娼妇。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_high_value_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 成了堕天使贵族少年们的性教育教师。",
                "那些愈是堕落就愈强大的少爷们，把实习课程几乎都压在了她的床上；而她也常常把一群欲望旺盛的少年榨得连声求饶。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 成了堕天使贵族少年们的性教育教师。",
            "她总是温柔抱住那些欲火高涨的少年，在一遍遍实习里把他们教成懂得如何玩弄奴隶与女人的合格贵族。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_warrior(target, context["sex_crazed"])
        if context["knight_ninja_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_knight_ninja(target, context["busty"])
        if context["priest_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_priest(target, context["busty"])
        if context["meat_toilet"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_meat_toilet(target, True)
        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_meat_toilet(target, False)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 最终和蜥蜴人骑士结婚了。",
                "哪怕丈夫有着陌生的鳞片肌肤，也没能阻止她沉浸在这段关系里；而那对傲人的巨乳，更成了丈夫最引以为傲、天天夸耀的对象。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 最终和蜥蜴人骑士结婚了。",
            "那层陌生鳞甲并没妨碍两人的爱意，随着共同生活的日子一天天增加，她也越来越被丈夫溺爱，几乎每天都会听见一大串赞美。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_meat_toilet(
        self,
        target: Character,
        dirty: bool,
    ) -> List[str]:
        if dirty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 被锁进异种街区的公厕里，成了公众肉便器。",
                "她必须接受所有种族的阴茎，哪怕怀孕也不被允许休息；而生下来的孩子则会被送进孤儿院，作为街区未来的新劳动力继续培养。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 被锁进异种街区的公厕里，成了公众肉便器。",
            "她的身体迟早会孕育出各式各样混杂血统的孩子，而街上的人们则把这种一视同仁承接所有欲望的存在，当成理所当然的公共设施。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 在黑暗精灵女神官的引导下修行着。",
                "她和对方交换了姐妹契约，日复一日把自己奉献给暗黑之神；那对傲人的双峰如今总是半露在外，乳环上还闪烁着契约魔法的光。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 在黑暗精灵女神官的引导下修行着。",
            "她和对方交换了姐妹契约，把余生都献给暗黑之神；而她的性器也已被契约之环封闭，看起来今后都不会再接受任何阴茎了。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_low_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return self._build_sell_followup_lines_with_ending(
                target,
                f"{target.name} 最终和一位兽人高级战士结婚了。",
                "她迷上了那副健壮肉体，与丈夫爱得难舍难分；可最近，连那位兽人丈夫都开始在性欲上渐渐跟不上她了。",
            )
        return self._build_sell_followup_lines_with_ending(
            target,
            f"{target.name} 最终和一位兽人高级战士结婚了。",
            "陌生而健壮的异族肉体并没妨碍她坠入爱河，听说两人已经深深相爱，而她大概很快就要生下第五个孩子。",
        )






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["warrior_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_warrior(target, context["sex_crazed"])
        if context["knight_mage_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_knight_mage(target, context["busty"])
        if context["priest_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_priest(target, context["anal_crazed"])
        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_negotiation(target, context["negotiation_skill"] >= 5)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high(
        self,
        target: Character,
        context: Dict[str, Any],
    ) -> List[str]:
        if context["thief_like"] or (context["knight_ninja_like"] and target.talent.get(207, 0)):
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_thief(target, context["thief_like"])
        if context["warrior_like"] or context["knight_ninja_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_pirate(target, context["busty"])
        if context["priest_like"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_priest(target, context["anal_crazed"])
        if context["meat_toilet"]:
            return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_default(target)






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被刻满奇异咒纹，生活在未开化的蛮族部落里。",
            "她早已不像从前的自己，乳头与私处挂满饰环，甚至会带着满足笑容主动扑进蛮族那宽厚粗暴的怀抱。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被刻满奇异咒纹后，成了蛮族部落公开拥有的玩物。",
            "乳头、私处、鼻尖与耳朵都被穿上圆环，背上还刻着主人的名字；而这种被彻底占有的感觉，似乎让她反而越来越愉快。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_pirate(self, target: Character, busty: bool) -> List[str]:
        if busty:
            return [
                f"{target.name} 成了六头海蛇海贼团的女船长。",
                "海蛇们似乎格外迷恋她那对漂亮乳房，甚至把她推上船长室的高座；而她也开始习惯在亲信按摩下发号施令。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了六头海蛇海贼团的船员。",
            "船上的水手多半都是被掠来的奴隶，她则负责用自己的身体安抚那些污浊又危险的家伙，慢慢成了船上默许的发泄口。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_priest(self, target: Character, anal_crazed: bool) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 夜夜都被喜好百合与后庭玩法的蛇妖富豪玩弄着。",
                "那条灵活长舌总在她肛门里来回搅弄，逼得她每次都只能痛苦又甜腻地喘息到腿软。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 夜夜都被喜好百合的蛇妖富豪缠在怀里。",
            "修长的蛇尾与柔软身躯把她越勒越紧，她也在那种几乎无法呼吸的亲昵里，一次次发出苦闷又淫靡的喘息。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_high_thief(self, target: Character, thief_like: bool) -> List[str]:
        if thief_like:
            return [
                f"{target.name} 成了黑暗精灵暗杀公会的情报员。",
                "过去的一切都被抹成谜团后，她不断从炮友与床伴身上窃取情报；而每到没有任务的夜晚，她反倒会焦躁地等待下一场性拷问。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了黑暗精灵暗杀公会的刺客。",
            "和她睡过的男人，往往第二天就会变成尸体；没有任务的日子里，她甚至会因等不到性拷问而感到难耐。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_knight_mage(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被兽人骑士团拿去抚育与训练兽人的孩子。",
                "随着双峰被进一步改造，她承担了所有幼崽的喂养工作，还得一边授乳一边教那些小兽人战斗。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了兽人骑士团的一员。",
            "她跟着骑士团袭击人类村庄、掠夺财物与女人，最后总会带着新的战利品回到那位深爱她的兽人丈夫身边。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_negotiation(
        self,
        target: Character,
        high_skill: bool,
    ) -> List[str]:
        if high_skill:
            return [
                f"{target.name} 成了花妖炼金术师的重要助手。",
                "靠着能说会道与擅长取悦他人的本事，她被留下来负责和顾客谈妥各种淫药与活体素材的生意。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被花妖炼金术师买走了。",
            "她的身体不断被拿来测试新药、催淫香与奇怪药剂，渐渐连自己究竟被改造成了什么模样都分不清了。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 被鹰身女妖富豪买去做照料生活的奴隶。",
                "她全身赤裸，只戴着项圈，专门侍奉富豪家的女儿；而那位出了名的施虐狂大小姐，经常塞着肛塞对她进行严苛的排泄管理。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被鹰身女妖富豪买去做照料生活的奴隶。",
            "她全身赤裸，只戴着项圈，照料着鹰身女妖一家起居；而在工作的空档，她还得和男奴交配，为这个家生出更多新的奴隶。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_loving_or_lewd_non_demon_exotic_sell_followup_lines_mid_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 成了魔界植物园培育魔界植物的苗床。",
                "那些植物的根深深扎进她的阴道，直接吸取体内养分；而她偏偏又无法抗拒那份插入感，只能把身体一点点献给植株。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 成了魔界植物园培育植物的苗床。",
            "粗壮根须从她直肠深处汲取养分，而由她培育出的作物却长势惊人，甚至替主人在品评会上赢得了奖项。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        race_id = int(target.talent.get(314, 0))
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        anal_crazed = bool(target.talent.get(77, 0))
        meat_toilet = bool(target.talent.get(204, 0))
        vagina_sense = int(target.abl.get(2, 0))

        if race_id != 9:
            return None

        if price >= 500_000:
            return self._build_normal_demon_black_market_sell_followup_lines_high_value(
                target, busty, warrior_like, knight_ninja_like, priest_like, meat_toilet, sex_crazed
            )

        if price >= 100_000:
            return self._build_normal_demon_black_market_sell_followup_lines_mid_high(
                target, busty, warrior_like, knight_ninja_like, priest_like, meat_toilet, anal_crazed
            )

        return self._build_normal_demon_black_market_sell_followup_lines_low(
            target, busty, warrior_like, knight_ninja_like, priest_like, meat_toilet, vagina_sense
        )






    def _build_normal_demon_black_market_sell_followup_lines_high_value(
        self,
        target: Character,
        busty: bool,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        meat_toilet: bool,
        sex_crazed: bool,
    ) -> List[str]:
        if warrior_like:
            return self._build_normal_demon_black_market_sell_followup_lines_high_value_warrior(target, sex_crazed)
        if knight_ninja_like:
            return self._build_normal_demon_black_market_sell_followup_lines_high_value_knight_ninja(target, busty)
        if priest_like:
            return self._build_normal_demon_black_market_sell_followup_lines_high_value_priest(target, busty)
        if meat_toilet:
            return self._build_normal_demon_black_market_sell_followup_lines_high_value_meat_toilet(target)
        return self._build_normal_demon_black_market_sell_followup_lines_high_value_default(target)






    def _build_normal_demon_black_market_sell_followup_lines_high_value_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 作为主人的第五个性奴，住进了宅邸地下室。",
            "多亏你留下的调教痕迹，她很快就适应了新环境，对夜夜被叫去侍奉主人这件事也驾轻就熟。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_high_value_knight_ninja(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被放在领主宅邸里，当成一台会产奶的人形奶牛。",
                "特殊药物让原本就丰满的乳房愈发膨胀，主人总会对她源源不断的母乳赞不绝口。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被地方领主送给儿子当新玩具。",
            "那个孩子有着禁忌血统，据说一旦巨魔化就会把奴隶活活捏碎，而她恐怕很难有好下场。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_high_value_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被装进专用箱子里，成了大商人随身携带的肉便器。",
            "每逢出差她都会像行李一样被搬来搬去，甚至被搬运工指着称作“那位大商人的肉箱子”。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_high_value_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被丢在堕落神神殿的角落，成了仪式里最受欢迎的女奴。",
                "一整天不停轮奸的新奴隶当中，她那对诱人的双峰尤其让信徒们趋之若鹜。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 因信奉其他神明而立刻被带进地下室。",
            "神官们一边嘲弄她的信仰，一边持续侵犯直到她的理性彻底粉碎，最终被迫发誓皈依堕落神。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_high_value_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被改造成魔族后，成了高级将校十分满意的性奴。",
                "主人每晚都温柔对待她，而她也像在新主人身上找到了从你这里得不到的东西。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被高级将校当成宠物饲养。",
            "每逢宾客来访，她都要讲述自己如何从勇者沦落为奴隶的故事，而主人正是为这种展示感到无比满足。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_low(
        self,
        target: Character,
        busty: bool,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        meat_toilet: bool,
        vagina_sense: int,
    ) -> List[str]:
        if warrior_like:
            return self._build_normal_demon_black_market_sell_followup_lines_low_warrior(target, vagina_sense)
        if knight_ninja_like:
            return self._build_normal_demon_black_market_sell_followup_lines_low_knight_ninja(target)
        if priest_like:
            return self._build_normal_demon_black_market_sell_followup_lines_low_priest(target, busty)
        if meat_toilet:
            return self._build_normal_demon_black_market_sell_followup_lines_low_meat_toilet(target, True)
        return self._build_normal_demon_black_market_sell_followup_lines_low_meat_toilet(target, False)






    def _build_normal_demon_black_market_sell_followup_lines_low_knight_ninja(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了酒吧周末飞镖比赛里的玩具。",
            "无论是被射得鲜血淋漓的高耸乳房，还是千疮百孔的身体，她都只能作为优胜奖金的一部分被人围观。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_low_meat_toilet(self, target: Character, dirty: bool) -> List[str]:
        if dirty:
            return [
                f"{target.name} 被锁进公厕后，继续以现役肉便器的身份侍奉公众。",
                "后来甚至通过了专门的“肉便器放置法案”，在那一天到来之前，她大概已经替几百人生下了孩子。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被锁进公厕，成了被各族男人昼夜使用的公众肉便器。",
            "那种残酷生活最终让她在半年内就精神崩溃，而她的身体却依然还要继续被开放给所有人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_low_priest(
        self,
        target: Character,
        busty: bool,
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被安排进触手小屋，成了量产触手的豪乳苗床。",
                "她那膨胀到原本两倍大小的乳房培育出的触手尤其值钱，最终彻底变成了触手温床。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被安排进触手小屋，成了量产触手的母体。",
            "她不知道已经被多少触手侵犯到头脑失常，连直肠与私处也一起化成了触手的温床。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_low_warrior(
        self,
        target: Character,
        vagina_sense: int,
    ) -> List[str]:
        if vagina_sense >= 5:
            return [
                f"{target.name} 被当成矿工们的慰问品饲养着。",
                "即便连续被侵犯数次也不肯屈服，那份倔强只会让矿工们抱怨她一点都不可爱。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成矿工们的慰问品饲养着。",
            "她几次被侵犯时都嚎啕大哭，而矿工们偏偏就觉得这很有趣，于是她反倒变得格外受欢迎。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_mid_high(
        self,
        target: Character,
        busty: bool,
        warrior_like: bool,
        knight_ninja_like: bool,
        priest_like: bool,
        meat_toilet: bool,
        anal_crazed: bool,
    ) -> List[str]:
        if warrior_like:
            return self._build_normal_demon_black_market_sell_followup_lines_mid_high_warrior(target, bool(target.talent.get(75, 0)))
        if knight_ninja_like:
            return self._build_normal_demon_black_market_sell_followup_lines_mid_high_knight_ninja(target)
        if priest_like:
            return self._build_normal_demon_black_market_sell_followup_lines_mid_high_priest(target, anal_crazed)
        if meat_toilet:
            return self._build_normal_demon_black_market_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_normal_demon_black_market_sell_followup_lines_mid_high_default(target)






    def _build_normal_demon_black_market_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了赌场赠品。",
            "她作为包装精致的美丽魔族奴隶，被摆在灯光下等待下一位能把自己带走的新主人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_mid_high_knight_ninja(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被摆进了妓院橱窗里吸引客人。",
            "不论是乳房上的淫靡图案与乳环，还是脸侧被刻上的下流纹样，最初的哭喊最终都被夜夜娇媚呻吟所取代。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被塞进赌场的侍奉房间，成了专门安抚输家们的赌场肉便器。",
            "特制筹码不断被塞进她的私处与肛门，她往后大概都只能作为这种玩具被永远使用下去。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_mid_high_priest(
        self,
        target: Character,
        anal_crazed: bool,
    ) -> List[str]:
        if anal_crazed:
            return [
                f"{target.name} 被大农场主顺手买下，当成礼物送给了自己的儿子们。",
                "那群邪恶的孩子最喜欢折腾她敏感的肛门，而此刻的她也仍在作为肛门玩具被反复侵犯。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被大农场主买下后送给儿子们取乐。",
            "那群邪恶的孩子夜夜都要狠狠干她，而她很快就怀孕得连孩子父亲是谁都能被拿来下注。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_demon_black_market_sell_followup_lines_mid_high_warrior(
        self,
        target: Character,
        sex_crazed: bool,
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被当成奖赏送给了立下战功的年轻士官。",
                "那位士官还不太习惯把如此年轻漂亮的魔族姑娘叫作奴隶，于是近乎把她当恋人般疼爱。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成奖赏送给了立下战功的年轻士官。",
            "刚从战场回来的士官总是格外粗暴，于是她每晚都在那份蛮横蹂躏里度日。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        race_id = int(target.talent.get(314, 0))
        if race_id == 9:
            return None

        if price >= 500_000:
            return self._build_normal_non_demon_black_market_sell_followup_lines_high_value(target)
        if price >= 100_000:
            return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high(target)
        return self._build_normal_non_demon_black_market_sell_followup_lines_low(target)






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        meat_toilet = bool(target.talent.get(204, 0))

        if warrior_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_high_value_warrior(target, sex_crazed)
        if knight_ninja_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_high_value_knight(target, busty)
        if priest_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_high_value_priest(target, busty)
        if meat_toilet:
            return self._build_normal_non_demon_black_market_sell_followup_lines_high_value_meat_toilet(target)
        return self._build_normal_non_demon_black_market_sell_followup_lines_high_value_default(target)






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 作为主人的宠物生活在屋里。",
            "她已经在主人的脚边撒娇到几乎忘了自己曾经是勇者，余生看起来也只会这样过去。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value_knight(
        self, target: Character, busty: bool
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被当成一台人形奶牛安置在屋内。",
                "特殊药物让她本就有规模的乳房继续膨胀滴乳，主人甚至还专门雇了女仆来照料她与加热母乳。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被领主送给了儿子当玩具。",
            "那个孩子偶尔会巨魔化，把她抓起来当飞机杯使唤，而原勇者的体质也只是让她多撑一阵罢了。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 起初只是被当成肉便器买回来的，后来被直接放进主人房间。",
            "作为主人专用的便器，她总是珍惜着每次与主人相处的时间，而主人也对这份驯服感到十分满意。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value_priest(
        self, target: Character, busty: bool
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 作为侍奉神殿的女奴，终日都被信徒们侵犯着。",
                "原本信奉别神的她，如今已彻底改信堕落神，而那对被绳索勒出的诱人双峰更让信徒们欲望高涨。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 因信奉其他神明而被直接拖进了地下室。",
            "神官们一边嘲弄她的信仰，一边持续侵犯到全身被精液染白，最终逼得她只能发誓皈依堕落神。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_high_value_warrior(
        self, target: Character, sex_crazed: bool
    ) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被主人当成重要的性奴对待。",
                "她也尽力侍奉着新主人，在那份不属于你的温柔里，似乎真的过得相当幸福。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成宠物饲养在高级将校的宅邸里。",
            "每当宾客来访，她都要讲述自己如何从勇者沦落为奴隶，而主人则享受着旁人轻蔑注视她的时刻。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_low(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        meat_toilet = bool(target.talent.get(204, 0))
        vagina_sense = int(target.abl.get(2, 0))

        if warrior_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_low_warrior(target, vagina_sense)
        if knight_ninja_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_low_knight(target)
        if priest_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_low_priest(target, busty)
        if meat_toilet:
            return self._build_normal_non_demon_black_market_sell_followup_lines_low_meat_toilet(target)
        return self._build_normal_non_demon_black_market_sell_followup_lines_low_default(target)






    def _build_normal_non_demon_black_market_sell_followup_lines_low_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了昼夜不停被使用的公众肉便器。",
            "那种过于残酷的生活让她不到半年便精神崩溃，而身体却仍会继续被开放给所有路过的人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_low_knight(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了酒吧周末飞镖比赛里的玩具。",
            "无论是早已鲜血横流的宏伟乳房，还是千疮百孔的身体，她都只能在围观中等着优胜者出现。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_low_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 继续以现役肉便器的身份侍奉公众。",
            "在漫长岁月里，她像公共设施一样被市民反复疼爱，据说最后甚至生下了不下一百个孩子。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_low_priest(
        self, target: Character, busty: bool
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 被安排进触手小屋，成了量产触手的豪乳苗床。",
                "她那膨胀到原本两倍大小的乳房所培育出的触手格外值钱，于是这辈子大概都只能这样被榨干价值。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被安排进触手小屋，成了量产触手的母体。",
            "她不知道已培育出多少触手，整个人也已完全适应了这种身份，直到死去恐怕都无法离开。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_low_warrior(
        self, target: Character, vagina_sense: int
    ) -> List[str]:
        if vagina_sense >= 5:
            return [
                f"{target.name} 被当成矿工们的慰问品饲养着。",
                "即便连续被侵犯几次也不肯屈服，那份倔强反而让人嫌她一点都不可爱。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被当成矿工们的慰问品饲养着。",
            "她几次在被侵犯时都嚎啕大哭，而矿工们偏偏就喜欢这份反应，于是她变得格外受欢迎。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high(self, target: Character) -> List[str]:
        busty = self._is_sell_busty_target(target)
        warrior_like = self._has_sell_job_talent(target, 200, 203)
        knight_ninja_like = self._has_sell_job_talent(target, 205, 207)
        priest_like = self._has_sell_job_talent(target, 202, 206)
        sex_crazed = bool(target.talent.get(75, 0))
        meat_toilet = bool(target.talent.get(204, 0))
        vagina_sense = int(target.abl.get(2, 0))

        if warrior_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high_warrior(target, vagina_sense)
        if knight_ninja_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high_knight(target)
        if priest_like:
            return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high_priest(target, busty)
        if meat_toilet:
            return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high_meat_toilet(target)
        return self._build_normal_non_demon_black_market_sell_followup_lines_mid_high_default(target)






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了赌场里的赛狗。",
            "被彻底调教得只会四脚爬行的她，因为跑得够快，又被拿去和其他赛狗配种，人们只盼着她生出更优良的后代。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high_knight(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被收进专门搜罗异族美女的妓院，成了异种专用娼妇。",
            "不论烙印被烙在丰满乳房还是肩膀上，原勇者这个噱头都让这家店从此再也不愁客人。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high_meat_toilet(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被塞进赌场侍奉房间，成了专门抚慰输家们的赌场肉便器。",
            "筹码不断被塞进她的私处与肛门，她往后大概只能永远以这种肉便器玩具的方式活下去。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high_priest(
        self, target: Character, busty: bool
    ) -> List[str]:
        if busty:
            return [
                f"{target.name} 因丰满乳房被挑中，作为牛奴隶被拴进厩舍。",
                "怀上牛系魔兽的孩子后，她还被注射肥大药剂，每天像乳牛一样被榨乳，脸上总会露出销魂表情。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被拿去和所有家畜交配，成了家畜奴隶。",
            "实验还在继续，旁人甚至已经开始认真讨论她和魔界猪杂交后会不会产出更松软的肉。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_normal_non_demon_black_market_sell_followup_lines_mid_high_warrior(
        self, target: Character, vagina_sense: int
    ) -> List[str]:
        if vagina_sense >= 5:
            return [
                f"{target.name} 被年轻士官用奖金买下后，当成温驯的异族美女奴隶夜夜疼爱。",
                "面对新主人的所有欲望，她都表现得近乎热情顺从。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被年轻士官用奖金买下后，当成温驯的异族美女奴隶夜夜疼爱。",
            "只是她回应新主人的方式仍是夹杂悲鸣的喘息，而那也似乎足够让对方满足。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        tier = self._get_sell_price_tier(price)
        dog_like = bool(target.talent.get(136, 0))
        sex_crazed = bool(target.talent.get(75, 0))
        negotiation_skill = int(target.abl.get(15, 0))
        lewd = bool(target.talent.get(76, 0))

        if dog_like:
            return self._build_pet_market_sell_followup_lines_dog(target, tier, sex_crazed, negotiation_skill)

        if lewd:
            return self._build_pet_market_sell_followup_lines_lewd(target, tier)

        return None






    def _build_pet_market_sell_followup_lines_dog(
        self, target: Character, tier: int, sex_crazed: bool, negotiation_skill: int
    ) -> List[str]:
        if tier == 3:
            return self._build_pet_market_sell_followup_lines_dog_tier_3(target, sex_crazed, negotiation_skill)
        if tier == 2:
            return self._build_pet_market_sell_followup_lines_dog_tier_2(target, sex_crazed, negotiation_skill)
        if tier == 1:
            return self._build_pet_market_sell_followup_lines_dog_tier_1(target, sex_crazed, negotiation_skill)
        if sex_crazed:
            return self._build_pet_market_sell_followup_lines_dog_tier_0_sex_crazed(target)
        if negotiation_skill >= 5:
            return self._build_pet_market_sell_followup_lines_dog_tier_0_negotiated(target)
        return self._build_pet_market_sell_followup_lines_dog_tier_0_default(target)






    def _build_pet_market_sell_followup_lines_dog_tier_0_default(self, target: Character) -> List[str]:
        return [
            f"{target.name} 被当成真正的牝犬宠物牵走了。",
            "那个变态主人似乎只有在看她和大型犬交尾时才会兴奋，而她就在那种复杂难言的心情中迎来了高潮。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_dog_tier_0_negotiated(self, target: Character) -> List[str]:
        return [
            f"{target.name} 成了在小剧场里表演兽奸秀的牝犬女优。",
            "为了让门票卖得更好，她后来甚至开始和更加丑陋怪异的珍兽进行交尾表演。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_dog_tier_0_sex_crazed(self, target: Character) -> List[str]:
        return [
            f"{target.name} 最终成了所谓“魔犬新娘”。",
            "那只拥有知性的魔犬渴求最优秀的母体，而她淫乱的身体似乎正好足以满足这份期待。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_dog_tier_1(self, target: Character, sex_crazed: bool, negotiation_skill: int) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被牝犬饲养员买下后，和同伴们一起致力于让牝犬奴隶孕育幼犬。",
                "她既喜欢看交尾，也喜欢亲身参与，每个月都和同伴及奴隶们愉快地进行着乱交兽奸。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if negotiation_skill >= 5:
            return [
                f"{target.name} 被个体经营的训练员买下，成了继续增加兽奸狂与牝犬奴隶的工具。",
                "她买下女奴隶，深入教授兽爱，再把成果公开，甚至还梦想着创办一本兽奸杂志。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 作为女兽奸狂朋友买下的宠物，过上了愉快的牝犬生活。",
            "她很快就和有着共同兴趣的主人同居，还会亲密地和大型犬并排发情。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_dog_tier_2(self, target: Character, sex_crazed: bool, negotiation_skill: int) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 被当成高级母种犬饲养。",
                "异种族交配而生的幼犬被视作比普通魔犬更聪明的成果，而她自己却只剩下一张不断高潮受孕的脸。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if negotiation_skill >= 5:
            return [
                f"{target.name} 成了在圆形剧场表演兽奸秀的高级牝犬女优。",
                "她把被围观、被驱使、被当作舞台上的母犬这一切都演得驾轻就熟。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被女富豪买下后，过上了淫行牝犬的生活。",
            "那位有施虐癖的女富豪越来越喜欢看她在路边被呵斥着开始交尾的堕落样子。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_dog_tier_3(self, target: Character, sex_crazed: bool, negotiation_skill: int) -> List[str]:
        if sex_crazed:
            return [
                f"{target.name} 成了最高级牝犬饲养员身边的重要母犬。",
                "她不仅把怀上幼犬当成至高喜悦，甚至还会亲自买来女奴隶，让她们也去孕育新的幼犬。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        if negotiation_skill >= 5:
            return [
                f"{target.name} 被训练员买下后，成了把别的女人也调教成牝犬兽奸奴隶的样板。",
                "那个女人甚至妄想着把世界变成谁在路边牝犬交配都不奇怪的地方。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被土豪买下后，优雅地作为宠物牝犬生活着。",
            "后来她还多次在牝犬品评会上获奖，成了让其他牝犬奴隶羡慕的榜样。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_pet_market_sell_followup_lines_lewd(self, target: Character, tier: int) -> List[str]:
        tier_lines = {
            3: f"{target.name} 被当成高级牝犬饲养，过上了被当作名犬与发情母狗反复展示的生活。",
            2: f"{target.name} 被卖给了牝犬饲养员，成了专门繁殖用的母种犬。",
            1: f"{target.name} 被卖去做淫乱母犬，从此把发情与配种当成了日常。",
            0: f"{target.name} 被低价当成淫乱母犬牵走，往后的生活只剩下反复发情与被配种。",
        }
        return [tier_lines[tier], f"从那之后，你再也没有见过 {target.name}。"]






    def _build_rebellious_black_market_sell_followup_lines(self, target: Character, price: int) -> Optional[List[str]]:
        profile = self._get_sell_followup_profile(target)
        if profile["race_id"] == 9:
            return self._build_rebellious_black_market_sell_followup_lines_demon(target, price)
        return self._build_rebellious_black_market_sell_followup_lines_non_demon(target, price)






    def _build_rebellious_black_market_sell_followup_lines_demon(self, target: Character, price: int) -> Optional[List[str]]:
        profile = self._get_sell_followup_profile(target)

        if price >= 100_000:
            if profile["priest_like"]:
                return [
                    f"{target.name} 被送去了魔界中央奴隶市场，随后被选为新落成神殿的祭品。",
                    f"听说 {target.name} 过去是高明的圣职者，这一点让那群神官十分满意。",
                    f"从那之后，你再也没有见过 {target.name}。",
                ]
            if profile["level"] >= 50:
                return [
                    f"{target.name} 被送去了魔界中央奴隶市场，作为死斗场的角斗士挣扎求生。",
                    "她似乎熬过了许多严苛的死斗，但那种日子随时都可能突然结束。",
                    f"从那之后，你再也没有见过 {target.name}。",
                ]
            return [
                f"{target.name} 被送去了魔界中央奴隶市场。",
                "她在奴隶船上煽动叛乱，却很快被其它奴隶背叛并镇压，最后被丢进海里喂鱼了。",
                    f"从那之后，你再也没有见过 {target.name}。",
                ]
        if profile["busty"]:
            return [
                f"{target.name} 被送去了魔界地方奴隶市场。",
                "她在市场上掀起暴动后，被以恶毒闻名的地方领主买下，最后沦为了被切碎贩卖的肉品。",
                f"从那之后，你再也没有见过 {target.name}。",
            ]
        return [
            f"{target.name} 被送去了魔界地方奴隶市场。",
            "逃跑失败后，她被绑上手术台，四肢被截去并改造成了供猎奇收藏家把玩的生物标本。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]






    def _build_rebellious_black_market_sell_followup_lines_non_demon(self, target: Character, price: int) -> Optional[List[str]]:
        profile = self._get_sell_followup_profile(target)

        if price >= 100_000:
            return self._build_rebellious_black_market_sell_followup_lines_non_demon_high_value(
                target,
                profile["race_id"],
                profile["warrior_like"],
                profile["priest_like"],
            )
        return self._build_rebellious_black_market_sell_followup_lines_non_demon_low_value(target, profile["busty"])






    def _build_rebellious_black_market_sell_followup_lines_non_demon_high_value(
        self,
        target: Character,
        race_id: int,
        warrior_like: bool,
        priest_like: bool,
    ) -> Optional[List[str]]:
        if race_id == 5:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送去了魔界中央奴隶市场。",
                "她最终以标本的形式被展示给熟客，据说是在不愿成为奴隶后咬舌自尽了。",
            )
        if warrior_like:
            return self._build_rebellious_black_market_sell_followup_lines_non_demon_high_value_warrior(target)
        if priest_like:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送去了魔界中央奴隶市场，随后被选作神殿的祭品。",
                f"听说 {target.name} 曾是高明的圣职者，这让那座神殿显得格外满意。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被送去了魔界中央奴隶市场。",
            "最后她被锁在船底充当划桨奴隶，直到风浪吞没了整条船。",
        )






    def _build_rebellious_black_market_sell_followup_lines_non_demon_high_value_warrior(self, target: Character) -> List[str]:
        if int(target.cflag.get(9, 0)) >= 100:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送去了魔界中央奴隶市场，作为角斗士与同伴发动过一次叛乱。",
                "叛乱最后仍被镇压，但作为主谋的她此后行踪不明。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被送去了魔界中央奴隶市场，作为角斗士被迫战斗。",
            "她与其它角斗士发动叛乱后遭到镇压，最终成了冠军猛兽的食物。",
        )






    def _build_rebellious_black_market_sell_followup_lines_non_demon_low_value(self, target: Character, busty: bool) -> Optional[List[str]]:
        if busty:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"{target.name} 被送去了魔界地方奴隶市场。",
                "在那里，她最终被当成肉品般拆卖处理，只剩下供人议论的残酷传闻。",
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            f"{target.name} 被送去了魔界地方奴隶市场。",
            "手术刀最终夺走了她的四肢与声音，余生被做成了供人摆设的活体家具。",
        )






    def _build_sell_followup_black_market_special_lines(self, target: Character, price: int) -> Optional[List[str]]:
        if target.talent.get(85, 0):
            loving_lines = self._build_loving_black_market_sell_followup_lines(target, price)
            if loving_lines:
                return loving_lines
            loving_non_demon_lines = self._build_loving_non_demon_black_market_sell_followup_lines(target, price)
            if loving_non_demon_lines:
                return loving_non_demon_lines
        if target.talent.get(76, 0):
            lewd_demon_lines = self._build_lewd_demon_black_market_sell_followup_lines(target, price)
            if lewd_demon_lines:
                return lewd_demon_lines
            lewd_non_demon_lines = self._build_lewd_non_demon_black_market_sell_followup_lines(target, price)
            if lewd_non_demon_lines:
                return lewd_non_demon_lines
        normal_demon_lines = self._build_normal_demon_black_market_sell_followup_lines(target, price)
        if normal_demon_lines:
            return normal_demon_lines
        normal_non_demon_lines = self._build_normal_non_demon_black_market_sell_followup_lines(target, price)
        if normal_non_demon_lines:
            return normal_non_demon_lines
        return None




    def _build_sell_followup_default_lines(self, target: Character, price: int, tier: int, lines: List[str]) -> List[str]:
        return self._build_sell_followup_lines_by_talent_tier(
            target,
            tier,
            lines,
            {
                76: self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_DEFAULT_TIER_LINES[76]),
                85: self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_DEFAULT_TIER_LINES[85]),
            },
            [
                f"{target.name} 被当做普通奴隶卖掉，就这样慢慢消失在黑暗的世界之中。",
                self._build_sell_followup_ending(target),
            ],
        )




    def _build_sell_followup_ending(self, target: Character) -> str:
        return f"从那之后，你再也没有见过 {target.name}。"




    def _build_sell_followup_exotic_market_lines(self, target: Character, price: int, tier: int, lines: List[str]) -> List[str]:
        exotic_lines = self._build_exotic_market_sell_followup_lines(target, price)
        if exotic_lines:
            return exotic_lines
        if target.talent.get(75, 0):
            return self._build_sell_followup_lines_by_tier_map(
                target,
                tier,
                lines,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[75]),
            )
        if target.talent.get(76, 0):
            return self._build_sell_followup_lines_by_tier_map(
                target,
                tier,
                lines,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[76]),
            )
        if target.talent.get(85, 0):
            return self._build_sell_followup_lines_by_tier_map(
                target,
                tier,
                lines,
                self._format_sell_followup_tier_lines(target, SELL_FOLLOWUP_EXOTIC_MARKET_TIER_LINES[85]),
            )
        return lines + [
            f"{target.name} 被当做普通奴隶卖掉，就这样慢慢消失在黑暗的世界之中。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]




    def _build_sell_followup_lines(self, *lines: str) -> List[str]:
        return list(lines)




    def _build_sell_followup_lines_body_and_ending(self, target: Character, body_line: str) -> List[str]:
        return self._build_sell_followup_lines_with_ending(target, body_line)




    def _build_sell_followup_lines_by_talent_tier(
        self,
        target: Character,
        tier: int,
        lines: List[str],
        tier_lines_by_talent: Dict[int, Dict[int, str]],
        default_lines: List[str],
    ) -> List[str]:
        for talent_id, tier_lines in tier_lines_by_talent.items():
            if target.talent.get(talent_id, 0):
                return lines + [tier_lines[tier], self._build_sell_followup_ending(target)]
        return lines + default_lines




    def _build_sell_followup_lines_by_tier_map(
        self,
        target: Character,
        tier: int,
        lines: List[str],
        tier_lines: Dict[int, str],
    ) -> List[str]:
        return lines + [tier_lines[tier], self._build_sell_followup_ending(target)]




    def _build_sell_followup_lines_kojo_119(self, target: Character, tier: int, market_kind: str) -> Optional[List[str]]:
        if market_kind not in {"default", "quick"}:
            return None
        if target.mark.get(3, 0) == 3:
            return self._build_sell_followup_lines_pair_and_ending(
                target,
                f"被卖掉的 {target.name} 含着眼泪，用怨恨的目光看着你。",
                "「像你这样子的坏人，一，一定会有报应的！」",
            )
        if target.talent.get(76, 0):
            return self._build_sell_followup_lines(
                f"{target.name} 被带走时，还有些不舍地回头看着你。",
                SELL_FOLLOWUP_KOJO_119_TIER_LINES[76][tier],
                self._build_sell_followup_ending(target),
            )
        if target.talent.get(85, 0):
            return self._build_sell_followup_lines(
                f"{target.name} 被带走时，一言不发地含着眼泪回头看着你。",
                SELL_FOLLOWUP_KOJO_119_TIER_LINES[85][tier],
                self._build_sell_followup_ending(target),
            )
        return self._build_sell_followup_lines_pair_and_ending(
            target,
            "「呜呜……好想……好想回家……」",
            f"被装在囚车里拉走的 {target.name} 一路上都在抽泣。",
        )




    def _build_sell_followup_lines_pair_and_ending(self, target: Character, first_line: str, second_line: str) -> List[str]:
        return self._build_sell_followup_lines_with_ending(target, first_line, second_line)




    def _build_sell_followup_lines_tiered(self, target: Character, tier_lines: Dict[int, str], tier: int) -> List[str]:
        return self._build_sell_followup_lines_with_ending(target, tier_lines[tier])




    def _build_sell_followup_lines_with_ending(self, target: Character, *body_lines: str) -> List[str]:
        return self._build_sell_followup_lines(*body_lines, self._build_sell_followup_ending(target))




    def _build_sell_followup_pet_market_lines(self, target: Character, price: int, lines: List[str]) -> List[str]:
        pet_lines = self._build_pet_market_sell_followup_lines(target, price)
        if pet_lines:
            return pet_lines
        return lines + [
            f"{target.name} 被当成宠物调教对象带走，往后的人生大概会越来越不像“人”。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]




    def _build_sell_followup_rebellious_lines(self, target: Character, price: int, market_kind: str, lines: List[str]) -> List[str]:
        if market_kind in {"default", "quick"}:
            rebellious_lines = self._build_rebellious_black_market_sell_followup_lines(target, price)
            if rebellious_lines:
                return rebellious_lines
        return [
            f"被带走的 {target.name} 含着眼泪，怨恨地回头看了你最后一眼。",
            f"从那之后，你再也没有见过 {target.name}。",
        ]




    def _build_sell_market_label(self, market_kind: str) -> str:
        return {
            "default": "魔界的黑市",
            "exotic": "魔界的异族交易市场",
            "pet": "魔界的宠物市场",
            "quick": "某个不知名的奴隶贩子手里",
        }.get(market_kind, "某个市场")




    def _build_sell_price_detail(self, target: Character) -> Dict[str, Any]:
        detail = self._create_sell_price_detail()
        if self._is_maou_shadow(target):
            detail["price"] = 0
            return detail

        score = self._apply_sell_score_tables(target, detail)
        score = self._apply_sell_locked_trait_penalties(target, detail, score)
        if score <= 0:
            detail["price"] = 0
            return detail
        score = self._apply_sell_multipliers(target, detail, score)
        score = self._apply_sell_experience_multipliers(target, detail, score)
        score = self._apply_sell_trait_multipliers(target, detail, score)
        score = self._apply_sell_party_multipliers(target, detail, score)

        detail["price"] = min(max(score, 0), 25000000)
        return detail




    def _build_sell_price_tables(self) -> tuple[Dict[int, List[int]], Dict[int, List[int]], Dict[int, str]]:
        additive_tables = {
            10: [0, 200, 500, 850, 1500, 2000, 2300, 2600, 3000, 3200, 3500],
            11: [10, 100, 300, 700, 1200, 2000, 2300, 2600, 3000, 3200, 3500],
            12: [0, 100, 200, 400, 700, 1200, 1500, 1800, 2200, 2600, 3000],
            13: [0, 100, 150, 300, 500, 800, 2000, 2500, 3000, 3800, 5000],
            14: [0, 100, 150, 300, 500, 800, 2000, 2500, 3000, 3800, 5000],
            15: [0, 50, 120, 200, 300, 450, 1000, 1400, 2100, 2800, 3500],
            30: [0, 250, 500, 750, 1000, 1300],
            31: [0, 250, 500, 750, 1000, 1300],
            32: [0, 300, 600, 900, 1300, 1700],
            33: [0, 250, 500, 750, 1000, 1300],
            39: [0, 100, 300, 500, 1000, 1700, 3000],
            71: [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5200, 6500],
            73: [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5200, 6500],
        }
        penalty_tables = {
            37: [0, 500, 1000, 2000, 4000, 10000],
        }
        additive_labels = {
            10: "顺从",
            11: "欲望",
            12: "技巧",
            13: "侍奉技术",
            14: "性交技术",
            15: "话术",
            30: "性交中毒",
            31: "自慰中毒",
            32: "精液中毒",
            33: "百合中毒",
            37: "卖淫中毒",
            39: "兽奸中毒",
            71: "歌唱技能",
            73: "料理技能",
        }
        return additive_tables, penalty_tables, additive_labels




    def _can_sell_target(self, idx: int, target: Character) -> bool:
        self._update_sell_flags_for_target(target)
        if idx <= 0:
            return False
        if target.cflag.get(0, 0) < 1:
            return False
        if target.base.get(0, 0) < 1:
            return False
        if self._is_maou_shadow(target):
            return False
        if target.cflag.get(1, 0) != 0:
            return False
        if target.cflag.get(700, 0):
            return False
        if target.cflag.get(12, 0) and self.interpreter.vars.time == 1:
            return False
        return True




    def _check_sell_assiable(self, target) -> List[str]:
        """売却可・助手可判定 - 对应 @CHECK_SELLASSIABLE"""
        messages: List[str] = []
        return messages






    def _collect_sell_trait_multipliers(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        multipliers.extend(self._collect_sell_trait_multipliers_personality(target))
        multipliers.extend(self._collect_sell_trait_multipliers_sensory(target))
        multipliers.extend(self._collect_sell_trait_multipliers_body(target))
        multipliers.extend(self._collect_sell_trait_multipliers_social(target))
        multipliers.extend(self._collect_sell_trait_multipliers_appearance(target))
        multipliers.extend(self._collect_sell_trait_multipliers_species(target))
        multipliers.extend(self._collect_sell_trait_multipliers_status(target))
        return multipliers






    def _collect_sell_trait_multipliers_appearance(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        if target.talent.get(248, 0):
            multipliers.append(("肌肉型", 60))
        if target.talent.get(253, 0):
            multipliers.append(("褐色肌肤", 80))
        if target.talent.get(255, 0):
            multipliers.append(("白皙", 120))
        if any(target.talent.get(idx, 0) for idx in [165, 167, 168, 169, 170, 171, 174, 175, 176, 177, 178]):
            multipliers.append(("稀有人物", 400))
        return multipliers






    def _collect_sell_trait_multipliers_body(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        self._collect_sell_trait_multipliers_body_shape(multipliers, target)
        self._collect_sell_trait_multipliers_body_gender(multipliers, target)
        self._collect_sell_trait_multipliers_body_species(multipliers, target)
        return multipliers






    def _collect_sell_trait_multipliers_body_gender(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        if not (target.talent.get(122, 0) and not target.talent.get(113, 0) and not target.talent.get(132, 0) and not target.talent.get(135, 0)):
            return
        if target.abl.get(10, 0) <= 3 or target.abl.get(11, 0) <= 3 or target.abl.get(23, 0) <= 2:
            self._append_sell_multiplier(multipliers, "男人", 20)
        elif target.abl.get(10, 0) <= 4 or target.abl.get(11, 0) <= 4 or target.abl.get(23, 0) <= 3:
            self._append_sell_multiplier(multipliers, "男人", 40)
        elif target.abl.get(10, 0) <= 5 or target.abl.get(11, 0) <= 5 or target.abl.get(23, 0) <= 4:
            self._append_sell_multiplier(multipliers, "男人", 70)






    def _collect_sell_trait_multipliers_body_shape(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(109, 0) and not target.talent.get(100, 0) and not target.talent.get(132, 0) and not target.talent.get(135, 0)), "贫乳", 75)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(110, 0)), "巨乳", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(111, 0)), "快速回复", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(113, 0)), "魅力", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(114, 0)), "爆乳", 160)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(119, 0)), "超乳", 170)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(116, 0) and not target.talent.get(132, 0) and not target.talent.get(135, 0)), "绝壁", 50)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(121, 0)), "扶她", 80)






    def _collect_sell_trait_multipliers_body_species(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(124, 0)), "动物耳朵", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(125, 0)), "白虎", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(126, 0)), "高人气", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(130, 0)), "母乳体质", 140)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(135, 0)), "未熟", 50)






    def _collect_sell_trait_multipliers_personality(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        self._collect_sell_trait_multipliers_personality_append(multipliers, target)
        return multipliers






    def _collect_sell_trait_multipliers_personality_append(self, multipliers: List[tuple[str, int]], target: Character):
        self._collect_sell_trait_multipliers_personality_identity(multipliers, target)
        self._collect_sell_trait_multipliers_personality_desire(multipliers, target)
        self._collect_sell_trait_multipliers_personality_social(multipliers, target)






    def _collect_sell_trait_multipliers_personality_desire(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(74, 0)), "自慰狂", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(75, 0)), "性爱狂", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(76, 0)), "淫乱", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(77, 0)), "尻穴狂", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(78, 0)), "淫乳", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(80, 0)), "倒错的", 150)






    def _collect_sell_trait_multipliers_personality_identity(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(0, 0)), "处女", 200 if target.cflag.get(71, 0) == 0 else 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(12, 0) and target.abl.get(10, 0) >= 3), "刚强", 110)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(15, 0) and target.abl.get(10, 0) >= 3), "自尊心", 110)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(20, 0) and target.abl.get(11, 0) <= 3), "克制", 80)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(21, 0) and target.abl.get(11, 0) <= 3), "冷漠", 80)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(22, 0) and target.abl.get(11, 0) <= 3), "感情淡薄", 80)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(24, 0) and target.abl.get(11, 0) <= 3), "保守的", 80)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(27, 0) and target.abl.get(10, 0) <= 3), "戒备森严", 80)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(33, 0)), "开放", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(42, 0)), "容易湿", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(46, 0)), "幸福草中毒", 20)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(63, 0)), "献身的", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(70, 0) and target.abl.get(11, 0) >= 3), "接受快感", 120)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(71, 0) and target.abl.get(11, 0) <= 3), "否定快感", 60)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(73, 0)), "容易陷落", 20)






    def _collect_sell_trait_multipliers_personality_social(self, multipliers: List[tuple[str, int]], target: Character) -> None:
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(91, 0)), "魅惑", 150)
        self._append_sell_multiplier_if(multipliers, bool(target.talent.get(92, 0)), "谜之魅力", 400)






    def _collect_sell_trait_multipliers_sensory(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        if target.talent.get(101, 0):
            multipliers.append(("阴蒂钝感", 80))
        if target.talent.get(102, 0):
            multipliers.append(("阴蒂敏感", 120))
        if target.talent.get(103, 0):
            multipliers.append(("私处钝感", 80))
        if target.talent.get(104, 0):
            multipliers.append(("私处敏感", 120))
        if target.talent.get(105, 0):
            multipliers.append(("肛门钝感", 80))
        if target.talent.get(106, 0):
            multipliers.append(("肛门敏感", 120))
        if target.talent.get(107, 0):
            multipliers.append(("乳房钝感", 80))
        if target.talent.get(108, 0):
            multipliers.append(("乳房敏感", 120))
        return multipliers






    def _collect_sell_trait_multipliers_social(self, target: Character) -> List[tuple[str, int]]:
        multipliers: List[tuple[str, int]] = []
        if target.talent.get(180, 0) and not target.talent.get(181, 0):
            multipliers.append(("妓女", 80))
        if target.talent.get(181, 0):
            multipliers.append(("倾城", 150))
        if target.talent.get(182, 0):
            multipliers.append(("巧言", 150))
        if target.talent.get(185, 0):
            multipliers.append(("歌姬", 180))
        if target.talent.get(186, 0):
            multipliers.append(("舞姬", 180))
        if target.talent.get(187, 0):
            multipliers.append(("美姬", 180))
        return multipliers






    def _collect_sell_trait_multipliers_species(self, target: Character) -> List[tuple[str, int]]:
        race_multiplier = {
            0: 90,
            1: 120,
            2: 110,
            3: 120,
            4: 110,
            5: 180,
            6: 200,
            7: 120,
            8: 200,
            9: 120,
            10: 80,
            11: 80,
        }.get(target.talent.get(314, 0), 100)
        return [("种族", race_multiplier)]






    def _collect_sell_trait_multipliers_status(self, target: Character) -> List[tuple[str, int]]:
        if target.talent.get(9, 0):
            return [("崩坏", target.abl.get(10, 0) * 5)]
        if target.talent.get(123, 0):
            return [("疯狂", target.abl.get(10, 0) * 5)]
        if target.talent.get(153, 0):
            return [("妊娠", target.abl.get(10, 0) * 5)]
        return []






    def _create_sell_price_detail(self) -> Dict[str, Any]:
        return {
            "base_additions": [],
            "base_penalties": [],
            "multipliers": [],
            "assistant_multiplier": 100,
            "merchant_multiplier": 100,
        }






    def _emit_sell_reaction(self, target: Character):
        for line in self._get_sell_kojo_lines(target):
            print(line)




    def _format_sell_followup_body_lines(self, target: Character, body_lines: List[str]) -> List[str]:
        return [line.format(name=target.name) for line in body_lines]




    def _format_sell_followup_tier_lines(self, target: Character, tier_lines: Dict[int, str]) -> Dict[int, str]:
        return {tier: line.format(name=target.name) for tier, line in tier_lines.items()}




    def _format_sell_price(self, price: int) -> str:
        return f"{price:,}"




    def _get_sell_additive_score(self, level: int, values: List[int]) -> int:
        if level <= 0:
            return values[0]
        index = min(level, len(values) - 1)
        return values[index]




    def _get_sell_blocked_reason(self, idx: int, target: Optional[Character]) -> Optional[str]:
        if idx <= 0 or target is None:
            return "无效对象"
        self._update_sell_flags_for_target(target)
        if target.cflag.get(0, 0) < 1:
            return "此对象还不满足出售条件。"
        if target.base.get(0, 0) < 1:
            return "濒死中，无法出售。"
        if self._is_maou_shadow(target):
            return "近卫不能被卖掉。"
        if target.cflag.get(1, 0) != 0:
            return "不能出售非待机状态的角色。"
        if target.cflag.get(700, 0):
            return "收藏中的角色不能卖掉。"
        if target.cflag.get(12, 0) and self.interpreter.vars.time == 1:
            return "该角色当前时段不能出售。"
        return None




    def _get_sell_followup_market_options(self) -> List[Dict[str, Any]]:
        return [
            {"id": 0, "name": "魔界的黑市", "kind": "default"},
            {"id": 1, "name": "魔界的异族交易市场", "kind": "exotic"},
            {"id": 2, "name": "魔界的宠物市场", "kind": "pet"},
            {"id": 999, "name": "随手卖掉吧", "kind": "quick"},
        ]




    def _get_sell_followup_profile(self, target: Character) -> Dict[str, Any]:
        return {
            "race_id": int(target.talent.get(314, 0)),
            "busty": self._is_sell_busty_target(target),
            "warrior_like": self._has_sell_job_talent(target, 200, 203),
            "knight_ninja_like": self._has_sell_job_talent(target, 205, 207),
            "knight_mage_like": self._has_sell_job_talent(target, 205, 201),
            "priest_like": self._has_sell_job_talent(target, 202, 206),
            "sex_crazed": bool(target.talent.get(75, 0)),
            "anal_crazed": bool(target.talent.get(77, 0)),
            "meat_toilet": bool(target.talent.get(204, 0)),
            "negotiation_skill": int(target.abl.get(15, 0)),
            "thief_like": bool(target.talent.get(203, 0)),
            "level": int(target.cflag.get(9, 0)),
        }




    def _get_sell_kojo_lines(self, target: Character) -> List[str]:
        kojo_num = self._get_kojo_num(target)
        if kojo_num == 110:
            if target.talent.get(85, 0) and int(target.mark.get(3, 0)) < 3:
                return [
                    "「小孩子的时候…有个占卜师曾经说过呢，总有一天你的面前会出现两个王。」",
                    "「算上狂王那时候的话…果然你是地狱的门呢………」",
                    "「………最后的最后赌输了呢」",
                ]
            if int(target.mark.get(3, 0)) == 3:
                return [
                    "「果然、不曾和你见面更好呢………」",
                ]
            if target.talent.get(76, 0):
                return [
                    "「诶、骗、骗人的吧…把人家卖掉什么是玩笑吧？啊哈哈…」",
                    "「比人家好的扶她肉棒不可能有的吧！不、不要…放开我…不要啊…人家才不会被卖掉！」",
                ]
            return [
                "「这样啊…被卖掉了呢………」",
                "「果然…还是不行……呢」",
            ]
        if kojo_num == 101:
            if int(target.mark.get(3, 0)) == 3:
                return [
                    "明明马上就要被卖掉了，她却还对自己的胜利沾沾自喜。",
                    "就这样，一只牝犬被卖掉了。",
                ]
            if target.talent.get(76, 0):
                return [
                    "「哈…这次对方会是什么样的主人呢…」",
                    "「啊啊啊身体好疼哇………」",
                ]
            return [
                "「…求…求求你…不要…把我卖掉…」",
            ]
        return []




    def _get_sell_multiplier(
        self,
        level: int,
        base_table: Dict[int, int],
        ranges: Optional[List[tuple[int, int, int]]] = None,
        default: int = 100,
    ) -> int:
        if level in base_table:
            return base_table[level]
        if ranges is not None:
            for upper, factor, offset in ranges:
                if level <= upper:
                    return level * factor + offset
        return default




    def _get_sell_price_tier(self, price: int) -> int:
        if price >= 1_000_000:
            return 3
        if price >= 500_000:
            return 2
        if price >= 100_000:
            return 1
        return 0




    def _handle_sell_candidate_menu_choice(self, candidates: List[tuple[int, Character]], choice: str) -> bool:
        try:
            selected = int(choice)
        except ValueError:
            print("\nInvalid selection.")
            self._pause()
            return False

        selected_char = self.interpreter.vars.chars[selected] if 0 <= selected < len(self.interpreter.vars.chars) else None
        blocked_reason = self._get_sell_blocked_reason(selected, selected_char)
        if blocked_reason is not None:
            print(f"\n{blocked_reason}")
            self._pause()
            return False

        selected_pair = next(((idx, char) for idx, char in candidates if idx == selected), None)
        if selected_pair is None:
            print("\nInvalid selection.")
            self._pause()
            return False

        idx, target = selected_pair
        estimate = self._build_sell_price_detail(target)
        return self._show_sell_confirmation_menu(idx, target, estimate)






    def _has_sell_job_talent(self, target: Character, *talent_ids: int) -> bool:
        return any(target.talent.get(talent_id, 0) for talent_id in talent_ids)






    def _is_sell_busty_target(self, target: Character) -> bool:
        return any(target.talent.get(talent_id, 0) for talent_id in (110, 114, 119))






    def _list_sellable_targets(self) -> List[tuple[int, Character]]:
        candidates: List[tuple[int, Character]] = []
        for idx, char in enumerate(self.interpreter.vars.chars):
            if self._can_sell_target(idx, char):
                candidates.append((idx, char))
        return candidates




    def _maturo_video_title(self, target: Character, title: str) -> None:
        self._mark_character_public_video(target, title)
        self._video_backup(title)






    def _maturo_video_title_only(self, title: str) -> None:
        self._video_backup(title)






    def _maturo_video_title_only_with_campaign(self, title: str) -> None:
        self._video_backup(title)
        self.interpreter.vars.globals[9010] = int(self.interpreter.vars.globals.get(9010, 0)) + 1






    def _maturo_video_title_with_campaign(self, target: Character, title: str) -> None:
        self._maturo_video_title(target, title)
        self.interpreter.vars.globals[9010] = int(self.interpreter.vars.globals.get(9010, 0)) + 1






    def _print_sell_estimate_detail(self, target: Character, estimate: Dict[str, Any]):
        print(f"\n{target.name} 的评价明细")
        print("-" * 30)
        for label, level, value in estimate["base_additions"]:
            print(f" {label} LV{level}  +{value}")
        for label, level, value in estimate["base_penalties"]:
            level_text = f" LV{level}" if level else ""
            print(f" {label}{level_text}  -{value}")
        for label, value in estimate["multipliers"]:
            if value != 100:
                print(f" {label} x{value / 100:.2f}")
        if estimate.get("assistant_multiplier", 100) != 100:
            print(f" 助手出售修正 x{estimate['assistant_multiplier'] / 100:.2f}")
        if estimate.get("merchant_multiplier", 100) != 100:
            print(f" 商卖人交涉修正 x{estimate['merchant_multiplier'] / 100:.2f}")
        print(f" 预计售价: {self._format_sell_price(estimate['price'])} pts")




    def _prompt_sell_candidate_choice(self) -> str:
        return self._prompt_choice()






    def _refresh_sell_assistant_flags(self):
        for idx, char in enumerate(self.interpreter.vars.chars):
            if idx <= 0:
                continue
            self._update_sell_flags_for_target(char)




    def _render_sell_candidate_menu(self, candidates: List[tuple[int, Character]]) -> None:
        print("\n【Sell】")
        print("-" * 30)
        print(f" Money: {self.interpreter.vars.money} pts")
        if not candidates:
            print(" No captive currently satisfies the original sale conditions.")
            return
        for idx, char in candidates:
            estimate = self._build_sell_price_detail(char)
            status = []
            if self.interpreter.vars.assi == idx:
                status.append("原助手")
            elif char.cflag.get(0, 0) >= 2:
                status.append("可做助手")
            if char.cflag.get(700, 0):
                status.append("收藏")
            status_text = f" ({', '.join(status)})" if status else ""
            print(f" [{idx}] {char.name}  评价额:{self._format_sell_price(estimate['price'])} pts{status_text}")
        print(" [100] Back")






    def _sell_maturo(self, target: Character, sell_price: int) -> Tuple[List[str], str]:
        """Determine a sold character's fate (末路) based on attributes and price.
        Returns (messages, maturo_title) where messages is a list of display strings
        and maturo_title is the fate label.
        """
        msgs: List[str] = []
        tn = target.name
        player = self._get_player()
        master_name = player.name if player else ""

        def has_talent(tid: int) -> bool:
            return int(target.talent.get(tid, 0)) == 1

        def get_abl(aid: int) -> int:
            return int(target.abl.get(aid, 0))

        def get_cflag(cid: int) -> int:
            return int(target.cflag.get(cid, 0))

        def get_mark(mid: int) -> int:
            return int(target.mark.get(mid, 0))

        is_mazoku = int(target.talent.get(314, 0)) == 9
        is_dragon = int(target.talent.get(314, 0)) == 5

        maturo = ""

        # ==================================================================
        # 反抗刻印Lv3
        # ==================================================================
        if get_mark(3) == 3:
            if is_mazoku:
                if sell_price >= 100000:
                    if random.randint(0, 1) == 0:
                        locals_name = "魔界中央奴隶市场"; local = 1
                    else:
                        locals_name = "魔界中央奴隶市场"; local = 0
                    msgs.append(f"{tn}被送到{locals_name}………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if get_cflag(9) >= 50:
                            msgs.append(f"{tn}作为死斗场的角斗士在战斗着。")
                            msgs.append("貌似经历了许多相当严苛的死斗，依然活下来了。")
                            msgs.append("如果让主办者不尽兴的话，也许很快就会不明不白地死掉吧。")
                            maturo = "角斗士"
                        else:
                            msgs.append(f"{tn}在奴隶船上叫醒了其它奴隶，发动了叛乱。")
                            msgs.append("但是起义却被其它的奴隶背叛，被轻易地镇压了。")
                            msgs.append("作为惩罚，貌似被丢海里喂鱼了……")
                            maturo = "鲨鱼的食物"
                    else:
                        if has_talent(202) or has_talent(206):
                            msgs.append("被选为新落成的神殿的祭品。")
                            msgs.append(f"{tn}被带来了。听说{tn}以前是高明的圣职者，神官们都因此非常满意。")
                            msgs.append(f"拿{tn}做祭品的神殿，一定是了不起的神殿吧……")
                            maturo = "神殿的人柱"
                        else:
                            msgs.append(f"作为原勇者的{tn}，现在双手双脚都被锁链锁着，在港口做苦力。")
                            msgs.append("时而展現出的反抗态度，告诉了人们背上伤痕累累的原因。")
                            msgs.append("这种悲惨而痛苦的生活，应该一生都无法摆脱了……")
                            maturo = "苦力奴隶"
                else:
                    if random.randint(0, 1) == 0:
                        locals_name = "魔界地方奴隶市场"; local = 1
                    else:
                        locals_name = "魔界地方奴隶市场"; local = 0
                    msgs.append(f"{tn}被送到{locals_name}………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if random.randint(0, 1) == 0:
                            msgs.append(f"{tn}在奴隶小屋准备转运奴隸的时候試圖逃走。")
                            msgs.append(f"当然，最后还是被抓回来了，{tn}要因此被重罚。")
                            msgs.append("双眼都被小刀挖掉了。")
                            msgs.append("「那位客人……来看看这个吧？双目失明不可能逃走哦！」")
                            maturo = "瞎子奴隶"
                        else:
                            msgs.append("「知道逃脱的奴隶会怎么样吗？哎呀，即使不知道也马上会知道了哦！」")
                            msgs.append(f"{tn}在奴隶小屋准备转运奴隸的时候試圖逃走。")
                            msgs.append(f"当然，最后还是被抓回来了，{tn}要因此接受惩罚。")
                            msgs.append("右脚的脚跟被挑断了，其它奴隶看得心惊胆颤。")
                            msgs.append("「这样，以后都别想逃跑了…」")
                            maturo = "瘸子奴隶"
                    else:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"尚擁有反抗心的{tn}在市场上引起暴动，把前来视察的地方领主的脸刮伤了。")
                            msgs.append("本来只需要普通的鞭刑。但是，那位大人有另外的打算。")
                            msgs.append("以恶毒性虐者而闻名的地方领主，将她买下带到肉联厂去了。")
                            msgs.append("")
                            msgs.append("「你看，上等的肉哦？！看看这胸～」")
                            msgs.append(f"就这样，{tn}的肉以一斤500点的价格在市面上出售了。")
                            maturo = "肉品"
                        else:
                            msgs.append("「知道逃脱的奴隶会怎么样吗？哎呀，即使不知道也马上会知道了哦！」")
                            msgs.append(f"逃走失败的{tn}被绑在手术台上，看来马上要进行什么变态的改造。")
                            msgs.append("数小时后，她的手脚都被截肢，弄成人棍了。")
                            msgs.append("猎奇收藏家觉得不错，马上把她买走了……")
                            maturo = "生物标本"
            else:
                if sell_price >= 100000:
                    if is_dragon:
                        locals_name = "魔界中央奴隶市场"; local = 2
                    elif has_talent(200) or has_talent(203):
                        locals_name = "魔界中央奴隶市场"; local = 1
                    else:
                        locals_name = "魔界中央奴隶市场"; local = 0
                    msgs.append(f"{tn}被送到{locals_name}………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 2:
                        msgs.append("「客人客人！过来看过来挑啊！这里可是有好东西哦！？」")
                        msgs.append("被叫住的客人是和贩子相熟的商人，被引入帐篷里了。")
                        msgs.append("一进去，就看到了张牙舞爪，振翅挺胸随时可以高飞似得龙族女孩。")
                        msgs.append(f"不过{tn}的眼神里，却没有生命的灵光，因为已经是个标本了。")
                        msgs.append("「我和你熟才告诉你啊～这孩子咬舌自尽了！就这么讨厌当奴隶么……」")
                        maturo = "标本"
                    elif local == 1:
                        msgs.append(f"{tn}作为死斗场的角斗士在战斗着。")
                        if get_cflag(9) >= 100:
                            msgs.append("和其它角斗士一起发动了叛乱，最后被镇压了。")
                            msgs.append(f"作为主谋的{tn}一直行踪不明，无法处置。")
                            msgs.append("而其它在叛乱中被生擒的角斗士，全部拿去喂猛兽了。")
                        else:
                            msgs.append("和其它角斗士一起发动了叛乱，最后被镇压了。")
                            msgs.append(f"作为主谋的{tn}要因此接受惩罚。")
                            msgs.append("成为了死斗场中冠军猛兽的食物。")
                        maturo = "角斗士"
                    else:
                        if has_talent(202) or has_talent(206):
                            msgs.append("被选为新落成的神殿的祭品。")
                            msgs.append(f"{tn}被带来了。听说{tn}以前是高明的圣职者，神官们都非常满意。")
                            msgs.append(f"拿{tn}做祭品的神殿，一定是了不起的神殿了吧……")
                            maturo = "神殿的人柱"
                        else:
                            msgs.append("作为船底仓的划桨奴隶，被锁在桨上。")
                            msgs.append("一天，船遇到了风浪，沉没了。")
                            msgs.append(f"在那之后，就再也没有听到{tn}的消息。")
                            maturo = "划桨奴隶"
                else:
                    if random.randint(0, 1) == 0:
                        locals_name = "魔界地方奴隶市场"; local = 1
                    else:
                        locals_name = "魔界地方奴隶市场"; local = 0
                    msgs.append(f"{tn}被送到{locals_name}………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if random.randint(0, 1) == 0:
                            msgs.append("「哈哈～像你这种沉默不语的最可爱了！」")
                            msgs.append(f"即将對{tn}进行手术的男人笑着说。")
                            msgs.append("她的手肘及膝盖以下都被切除，换成金属的替代品。")
                            msgs.append("完全没有听到任何的抗议，因为舌头已经被拔掉了。")
                            msgs.append("「呃呃，这张桌子，应该能卖个好价钱………」")
                            maturo = "活着的桌子"
                        else:
                            msgs.append("「哈哈～像你这种沉默不语的最可爱了！」")
                            msgs.append(f"即将为{tn}进行手术的男人笑着说。")
                            msgs.append("她的四肢被齐根切除，以人棍的模样被做成了人肉椅子。")
                            msgs.append("舌头也被拔掉了，手脚則作为椅子的装饰被粘合在椅子上。")
                            msgs.append("「呃呃，这张椅子，应该能卖个好价钱………」")
                            maturo = "活着的椅子"
                    else:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"尚擁有反抗心的{tn}在市场上引起暴动，把前来视察的地方领主的脸刮伤了。")
                            msgs.append("本来只需要普通的鞭刑，但是，那位大人有另外的打算。")
                            msgs.append("以恶毒性虐者而闻名的地方领主，将她买下带到肉联厂去了。")
                            msgs.append("")
                            msgs.append("「你看，上等的肉哦？！看看这胸～」")
                            msgs.append(f"就这样{tn}的肉以一斤500点的价格在市面上出售了。")
                            maturo = "肉品"
                        else:
                            msgs.append("「知道逃脱的奴隶会怎么样吗？哎呀，即使不知道也马上会知道了哦」")
                            msgs.append(f"逃走失败的{tn}被绑在手术台上，看来马上要进行什么变态的改造。")
                            msgs.append("数小时后，她的手脚都被截肢，弄成人棍了。")
                            msgs.append("猎奇收藏家觉得不错，马上把她买走了……")
                            maturo = "生物标本"

        # ==================================================================
        # 爱慕 (TALENT:85)
        # ==================================================================
        elif int(target.talent.get(85, 0)):
            if is_mazoku:
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军将军"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界贵族"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神官长"; local = 1
                    else:
                        locals_name = "魔界土豪"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}的蜜壶，不管被怎么粗暴对待都只会产生快感。私处紧紧地按摩着将军的阴茎，让他也快感连连。")
                            msgs.append("迷人的肉体以及作为原勇者的经历，也是将军非常中意的地方。")
                            msgs.append("原来只是打算买个性奴隶，现在渐渐变得像是爱人了。")
                        else:
                            msgs.append(f"将军对{tn}的肉穴相当粗暴。")
                            msgs.append("作为性奴隶，每晚都被狠狠侵犯，像是要玩坏一般。")
                            msgs.append("只靠作为原勇者的耐久力，恐怕被玩坏也只是时间问题了吧。")
                        maturo = "性奴隶"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"被主人买下的{tn}每天晚上都被仔细地玩弄乳房，在床上不断娇喘着。")
                            msgs.append("不过，她在你身边的时候已经充分学会如何应对这种情况了。")
                            msgs.append(f"作为被主人宠爱的宠物，{tn}的生活还是过得比较幸福的。")
                        else:
                            msgs.append(f"{tn}在屋里做着女仆和情人的工作。")
                            msgs.append("每天都过着只要主人高兴就会被叫到房里做爱的生活。")
                            msgs.append("恐怕没几天就会被主人干到怀孕，不过应该也会被勒令堕胎吧。")
                        maturo = "魔界贵族的情人"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}作为堕落神和神官长的近侍在神殿里工作着。")
                            msgs.append("为了更好地供奉堕落神，神官长对她的肛门进行了深度的调教。")
                            msgs.append("现在，敏感的菊穴已经被扩张，巨魔的阴茎也能轻易插入了。")
                            maturo = "菊奴女神官"
                        else:
                            msgs.append(f"{tn}作为神官长的第五个情妇每晚都被侵犯。")
                            msgs.append(f"曾经也是神职人员的{tn}，现在歌颂堕落神。")
                            msgs.append("因为堕落神赐予的愉悦，而不断娇喘着。")
                            maturo = "性奴女神官"
                    else:
                        if get_abl(15) >= 5:
                            msgs.append(f"{tn}在枕边经常妙语连珠，让土豪决定把她当成秘书。")
                            msgs.append("机智的交涉及性感的身体，为主人带来了不少好处。")
                            msgs.append("每晚，从客厅里都不断传出被主人和客人疼爱的呻吟。")
                            maturo = "生意助手"
                        else:
                            msgs.append(f"{tn}作为土豪的第八个情妇被买下了，总是如影随形地跟着。")
                            msgs.append("过于温柔的性格不为魔族所喜，不过土豪的众多孩子却相当喜欢。")
                            msgs.append("被土豪已经成年的儿子求爱了，在房间里每晚都被疼爱着。")
                            maturo = "土豪的情人"
                elif sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "黑帮首领"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界地方领主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的大商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(203):
                            msgs.append(f"在魔界也是首屈一指的繁荣城市里，{tn}成为了黑社会的一员。")
                            msgs.append("因为原来的盗贼经历，马上融入到了黑社会的生活之中了。")
                            msgs.append("作为首领的爱人，也习惯了被每天疼爱着。")
                        else:
                            msgs.append(f"在魔界也是首屈一指的繁荣城市里，{tn}成为了黑社会的一员。")
                            msgs.append("原来作为战士的本领得以发挥，过着保镖一样的生活。")
                            msgs.append("作为首领的爱人，也习惯了被每天疼爱着。")
                        maturo = "黑老大的情人"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在女仆长的指示下在屋子里帮忙收拾。")
                            msgs.append("因为低胸的女仆装，总是被男人们用下流的眼光看着，有时还被揩油。")
                            msgs.append("到了晚上，就彻底地被领主所占有了，过着这样的生活。")
                            maturo = "领主的女仆"
                        else:
                            msgs.append(f"{tn}因为年轻，被作为年幼的领主的玩具一样被放置在他的身边。")
                            msgs.append("每天过着像布娃娃一样的生活。")
                            msgs.append("在主人玩够之前，这种生活还要不停地持续着。")
                            maturo = "领主的玩物"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"神殿新设置了堕落神的贡品，{tn}作为奴隶要为神殿献出身心。")
                            msgs.append(f"被络绎不绝的信徒们侵犯肛门多次，{tn}淫媚的呻吟越来越大声了。")
                            msgs.append("好像这样子就能让堕落神高兴似得，不断奉献着。")
                            maturo = "邪神殿的菊奴"
                        else:
                            msgs.append("神殿新设置了堕落神的贡品，所有信徒都可以无偿侵犯。")
                            msgs.append("然后，被信徒侵犯所生下的孩子，也在神殿中被抚养着。")
                            msgs.append(f"原来信仰其它神的{tn}，现在全心全意地信奉着堕落神了。")
                            maturo = "邪神殿的性奴"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为员工们的肉便器被放置在公司。")
                            msgs.append("十几年间，生下了许多不知父亲是谁的孩子。")
                            msgs.append(f"生下的孩子也马上作为肉便器被卖掉了，那些钱拿来做了{tn}的生活费。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"作为情妇被买下的{tn}老老实实地侍奉着自己的主人。")
                            msgs.append("每晚都和商人的正室一起侍奉着商人，应该说是作为商人夫妇的共同宠物被宠爱着。")
                            msgs.append("据说在怀孕之后，孩子也作为宠物被抚养了。")
                            maturo = "商人的情人"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的士官"; local = 3
                    elif has_talent(205) or has_talent(201):
                        locals_name = "魔界学院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界大农场"; local = 1
                    else:
                        locals_name = "魔界商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"士官在战场上立功了，用奖金买下了{tn}。")
                            msgs.append(f"被年轻士官推倒的时候，{tn}终于有被卖了的自觉。")
                            msgs.append(f"士官沉迷于{tn}舒服的私处感触里了。")
                        else:
                            msgs.append(f"士官在战场上立功了，用奖金买下了{tn}。")
                            msgs.append(f"被年轻士官推倒的时候，{tn}终于有被卖了的自觉。")
                            msgs.append("在因被侵犯而泪流满面的奴隶身上，年轻的士官终于成为了大人了。")
                        maturo = "士官的性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}那双有魅力的乳房，被注射了学院还在开发中的药剂。")
                            msgs.append("乳房变为以前的两倍大，还不停地分泌着母乳，作为食堂的人形取奶器而受到欢迎。")
                            msgs.append(f"巨大的胸部让学生们爱不释手，{tn}每天都因此被玩得死去活来。")
                            maturo = "人形奶牛"
                        else:
                            msgs.append(f"作为学生的性处理便器而购买的{tn}，作用还不止于此，")
                            msgs.append("经常作为交配用的实验动物，被实验室所征用。")
                            msgs.append("如果能产生什么新物种的话，整个实验小组会被你传召嘉獎也说不定。")
                            maturo = "异种交配实验体"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"大农场主在买农奴的时候顺便买下了{tn}。")
                            msgs.append("最初品尝过她的肛门之后，被预想以外的快感所震惊，因而每晚都要侵犯她。")
                            msgs.append("被巨大阴茎连续侵犯的结果，就是她现在只能摊在床上，还略带有脱肛。")
                        else:
                            msgs.append(f"大农场主在买农奴的时候顺便买下了{tn}。")
                            msgs.append("也说不出到底喜欢她哪里，但是依然像对妻子一样温柔地对待她。")
                            msgs.append(f"接受了主人精液的{tn}怀孕了，临盘也快了。")
                        maturo = "大农场主的性奴隶"
                    else:
                        if has_talent(204):
                            msgs.append("作为店里的肉便器被放在厕所里。")
                            msgs.append(f"无论客人还是店员都可以使用的肉便器，{tn}的身上还标明了哪些时段是客人专用。")
                            msgs.append("终于怀孕了的时候还被挂上了【肉便器出产秀】的牌子，看来到极限为止都会被锁在厕所里。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"{tn}作为素材被妖术师买下了。")
                            msgs.append(f"按照顾客的需求进行了改造，给{tn}赋予了一些附加价值。")
                            msgs.append("好像又转卖给其它人了。")
                            maturo = "魔改肉块"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的矿山主"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界的农场"; local = 1
                    else:
                        locals_name = "街角的公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("连续被侵犯几次都不屈服。「再这么下去真是一点都不可爱」")
                        else:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("好几次都因被侵犯而嚎啕大哭。")
                        maturo = "矿山性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"对{tn}宏伟的胸部来说，女服务员的制服胸口处实在是太小了。")
                            msgs.append("「适合你的制服呢～」店长这么说着，最后的结果是要她一直赤裸上身迎客。")
                            msgs.append("每晚都收到很多小费，再这么下去，看来帮自己赎身也只是时间问题而已。")
                            maturo = "酒馆女侍应"
                        else:
                            msgs.append(f"在店主和客人之间周旋，{tn}像个娼妇一样地活着。")
                            msgs.append("原勇者，现在也彻底堕落了。")
                            maturo = "酒馆女侍应"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}和其它几个奴隶作为农奴被买下了。")
                            msgs.append("不过，农场主在试过她舒服的肛门之后上瘾了。")
                            msgs.append("现在作为专用性奴隶而存在着。")
                            maturo = "农场主的性奴"
                        else:
                            msgs.append(f"{tn}和其它几个奴隶作为农奴被买下了。")
                            msgs.append("为了不让其它农奴逃跑，强制让她做了农奴们的共同妻子，每晚都被好几个男人侵犯着。")
                            maturo = "农奴的共妻"
                    else:
                        if has_talent(204):
                            msgs.append("作为现役肉便器继续侍奉着。")
                            msgs.append(f"{tn}在相当长的时间内作为公众肉便器被广大市民所疼爱。")
                            msgs.append("在被精液淹死之前，好像生下了不下一百个的孩子。")
                        else:
                            msgs.append(f"{tn}作为公众肉便器不分昼夜地被使用着。")
                            msgs.append("过于残酷的生活让她精神崩溃了。")
                            msgs.append("到最后，从灵魂到身體，都彻底坏掉了。")
                        maturo = "肉便器"
            else:
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的将军"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界贵族"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神官长"; local = 1
                    else:
                        locals_name = "魔界土豪"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}的蜜壶，不管被怎么粗暴对待都只会产生快感。私处紧紧地按摩着将军的阴茎，让他也快感连连。")
                            msgs.append("迷人的肉体以及作为原勇者的经历，也是将军非常中意的地方。")
                            msgs.append("将军疼爱得就差亲手喂饭给她吃了，对于异族性奴隶来说，是难得得好待遇。")
                        else:
                            msgs.append(f"将军对{tn}的肉穴相当粗暴。")
                            msgs.append("作为性奴隶，每晚都被狠狠侵犯，像是要玩坏一般。")
                            msgs.append("如果真被玩坏了的话，将军的屋里可能又要多一具标本了吧。")
                        maturo = "魔界将军的性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}因为傲人的双峰被看上了。")
                            msgs.append("用皮质的拘束衣托起丰满的乳房，上面用乳环及针刺的伤痕漂亮地点缀着。")
                            msgs.append("成为了主人放置宝石的上等人体家具。")
                            maturo = "人体家具"
                        else:
                            msgs.append(f"作为主人专用宠物的{tn}，在主人有意不弄伤的情况下用拘束具锁着。")
                            msgs.append("经常四肢着地，像狗一样地爬行着。")
                            msgs.append("完全萌生了作为宠物的自觉，只要主人命令，便马上作为牝犬和其它宠物交配。")
                            maturo = "贵族的宠物"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append("让信仰其它神的人改信堕落神，也是神官长的一项重要工作。")
                            msgs.append(f"{tn}被神官长粗硬的阴茎侵犯着肛门，听他说了一天的教。")
                            msgs.append(f"曾经被你攻陷的{tn}，看来改信堕落神也只是时间问题了吧。")
                            maturo = "菊奴女神官"
                        else:
                            msgs.append(f"成为神官长奴隶的{tn}，每晚都参加妖邪的仪式。")
                            msgs.append("对于信奉正神的人来说，是肮脏不堪的仪式。")
                            msgs.append(f"但曾经被你攻陷的{tn}，现在則認为这是相当有魅力的仪式，积极地参加着。")
                            maturo = "性奴女神官"
                    else:
                        if get_abl(15) >= 5:
                            msgs.append(f"{tn}本来只是作为性奴隶被买回来，土豪却意外地发现她相当能说会道。")
                            msgs.append("为了让商谈取得优势，经常把她当做夜晚的宴客工具，")
                            msgs.append(f"{tn}在主人的指示下与其它男人发生关系，多次怀孕并分娩了。")
                            maturo = "宴客性奴"
                        else:
                            msgs.append(f"作为土豪宠物的{tn}，对主人相当顺从。")
                            msgs.append("土豪的众多孩子们也很喜欢可爱的她，作为宠物被多次弄怀孕并分娩了。")
                            msgs.append("她已经得到了作为宠物的最高幸福了吧。")
                            maturo = "土豪的宠物"
                elif sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "黑帮首领"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界地方领主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的大商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(203):
                            msgs.append(f"{tn}作为顺从的宠物与主人一起努力着。")
                            msgs.append("以前也试过多次逃走，但是发现奴隶项圈和奴隶手铐根本无法靠自己取下来之后变得老实了。")
                            msgs.append(f"主人对这样的{tn}非常疼爱，给予了她比较宽松的自由。")
                        else:
                            msgs.append(f"{tn}作为顺从的宠物与主人一起努力着。")
                            msgs.append(f"因為身体已經堕落了，{tn}完全记不起自己曾经身为勇者。")
                            msgs.append("被主人践踏也會产生快感。")
                        maturo = "驯化的宠物"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"负责提供母乳的{tn}，")
                            msgs.append("和挤奶工一起住小屋里。")
                            msgs.append("茶会的时候，則自己用手把母乳挤出来，為主人提供鮮榨乳汁。")
                            maturo = "人形奶牛"
                        else:
                            msgs.append(f"{tn}成为了供客人使用的肉被子，")
                            msgs.append("接待了不同种族的不少客人，甚至取得了广泛的好评。")
                            msgs.append("生下了几个孩子。在宅邸里被男仆和女仆们共同抚养着。")
                            maturo = "宴客肉被子"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"神殿新设置了堕落神的贡品，{tn}作为奴隶要因此为神殿献出身心。")
                            msgs.append(f"因為被异族和异教徒侵犯也算是一种功德，{tn}在信徒中得到了很高的人气。")
                            msgs.append("所有的阴茎都被那淫乱的肛门接受了，好像这样子就能让堕落神高兴似的，不断奉献着。")
                            maturo = "神殿的菊奴"
                        else:
                            msgs.append(f"神殿新设置了堕落神的贡品，{tn}作为贡品，被堕落信徒没完没了地侵犯着。")
                            msgs.append("侵犯异族和异教徒的女人也算是一种功德，信徒们每天都为侵犯她而排起了长队。")
                            msgs.append(f"以前信仰其它神的{tn}早晚也会从心底变成堕落神的信徒了吧。")
                            maturo = "神殿的性奴"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为员工们的肉便器被放置在公司。")
                            msgs.append("十几年间，生下了许多不知父亲是谁的孩子。")
                            msgs.append(f"生下的孩子也马上作为肉便器被卖掉了，那些钱拿来做了{tn}的生活费。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"作为宠物被买下的{tn}老实的顺从着自己的主人。")
                            msgs.append("原勇者的自尊心已经彻底粉碎了，完全作为宠物被教育，甚至受到了好评。")
                            msgs.append("「如果再懂得一些技艺，就能参加宠物品评会了吧！」主人这么说道。")
                            maturo = "大商人的宠物"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的士官"; local = 3
                    elif has_talent(205) or has_talent(201):
                        locals_name = "魔界学院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界大农场"; local = 1
                    else:
                        locals_name = "魔界商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"士官将第一次军功的奖金，交给了{tn}，")
                            msgs.append("对年轻的士官来说，与其说是性奴隶，不如说是可爱的恋人更为贴切。")
                            msgs.append(f"看着每晚都服侍自己阴茎的她，士官对{tn}越来越爱怜了。")
                        else:
                            msgs.append(f"士官将第一次军功的奖金，交给了{tn}，")
                            msgs.append("对年轻的士官来说，与其说是性奴隶，不如说是可爱的恋人更为贴切。")
                            msgs.append(f"並未完全屈服的{tn}，每天都半推半就地被士官品尝着身体。")
                        maturo = "士官的性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}那双有魅力的乳房，被注射了学院还在开发中的药剂。")
                            msgs.append("作为乳房淫虫的培养基，乳房中蠢蠢欲动的淫虫分泌着奇妙的体液，给予她持续的甜美快感。")
                            msgs.append("如果这个实验成功的话，市面上应该就会多出一种新的媚药了吧。")
                            maturo = "淫虫的苗床"
                        else:
                            msgs.append(f"作为学生的性处理便器而购买的{tn}每天都被学生们侵犯。")
                            msgs.append("哪怕在上课途中，被学生侵犯也是常态。")
                            msgs.append(f"这種时候，老师就会以「妨碍学生上课」为由鞭打{tn}。")
                            msgs.append(f"听着被鞭打的{tn}的惨叫响彻教室，学生们的欲望更加高涨了。")
                            maturo = "学生的玩具"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"大农场主在买农奴的时候顺便买下了{tn}。")
                            msgs.append("过着谁都可以將其玩弄的奴隶生活。")
                            msgs.append("被巨大阴茎连续侵犯的结果，就是她现在只能摊在床上，还略带有脱肛。")
                            maturo = "农场主的菊奴"
                        else:
                            msgs.append(f"大农场主在买农奴的时候顺便买下了{tn}。")
                            msgs.append(f"作为給大农场主儿子们的礼物，{tn}被彻底地玩弄着，怀孕了。")
                            msgs.append("据说现在作为所有人的生育奴隶被疼爱着。")
                            maturo = "农场主的性奴"
                    else:
                        if has_talent(204):
                            msgs.append("之前的肉便器崩溃了，作为新的肉便器被放置在厕所里。")
                            msgs.append("无论是客人还是员工都可以使用。")
                            msgs.append("终于到了出产秀的时候，会生出什么样的孩子还被设立了赌局。")
                        else:
                            msgs.append(f"{tn}作为素材被妖术师买下了。")
                            msgs.append("妖术师为如何使用原勇者这种素材而烦恼着。")
                            msgs.append("「反正听听客人怎么说，按顾客的喜欢来改造总不会错吧。」")
                        maturo = "肉便器"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的矿山主"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界的农场"; local = 1
                    else:
                        locals_name = "街角的公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("连续被侵犯几次都未屈服。于是侵犯变得越来越粗暴了。")
                        else:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("好几次被侵犯時都嚎啕大哭，矿工们觉得很有意思，令她相当受欢迎。")
                        maturo = "矿山性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"看中了{tn}傲人胸部的魅力，于是让她赤裸上身接待客人。")
                            msgs.append("客人们毫不客气地把玩她的乳房，作为奴隶的她只能忍耐。")
                            msgs.append("为了帮自己赎身，每晚都很在意客人的小费，有时会故意挺胸让客人们玩。")
                        else:
                            msgs.append("店主对客人介绍她的时候，会特意提醒她可以出台。")
                            msgs.append(f"作为异族女孩{tn}还是相当有人气的，不过皮肉钱绝大部分都被主人拿走，没留下多少给她。")
                        maturo = "酒馆女侍应"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"看中了{tn}丰满的乳房，被作为牛奴隶栓到厩舍里。")
                            msgs.append("怀上了牛系魔兽的孩子，乳房还被注射了肥大化的药剂，作为乳牛每天被榨乳。")
                            maturo = "乳牛奴隷"
                        else:
                            msgs.append(f"为了做出新品种的家畜让{tn}和一切的家畜交配。")
                            msgs.append("还没有什么实验成果，不过持续下去，应该不久就见效了吧。")
                            maturo = "异种交配家畜"
                    else:
                        if has_talent(204):
                            msgs.append("作为现役肉便器继续侍奉着。")
                            msgs.append(f"{tn}在相当长的时间内作为公众肉便器被广大市民所疼爱。")
                            msgs.append("好像生下了不下一百个的孩子。")
                        else:
                            msgs.append(f"{tn}作为公众肉便器不分昼夜地被使用着。")
                            msgs.append("过于残酷的生活让她精神崩溃了。")
                            msgs.append("多次呐喊着曾经作为主人的你的名字，最后终于完全坏掉了。")
                        maturo = "肉便器"

        # ==================================================================
        # 淫乱 (TALENT:76)
        # ==================================================================
        elif int(target.talent.get(76, 0)):
            if is_mazoku:
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的谍报机关"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的高级妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神官长"; local = 1
                    else:
                        locals_name = "魔界大富豪"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 100:
                            msgs.append(f"{tn}据闻和一个山间小国的君主结婚了。")
                            msgs.append("那国王在和她相处了一晚之后就马上发布了结婚的决定。")
                            msgs.append("你突然想起，那小国是生产魔界中为数不多的珍稀魔石的地方。")
                            msgs.append("近来，那国家好像发生了什么政变，不过这对你来说已经是无关重要的话题了吧。")
                            maturo = "魔界的谍报员"
                        else:
                            msgs.append(f"作为淫魔且擁有极品身体的{tn}对讯问官手舞足蹈着，")
                            msgs.append("无论男女都被她吸干精气而死，面对这样的身姿，其他讯问官都胆怯地跑掉了。")
                            msgs.append(f"这样的生活，对于{tn}来说，也算是一种幸福了吧。")
                            maturo = "谍报组织的提审官"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}彻底堕落的身体让所有客人都很尽兴。从现在这个在男人身上淫乱不堪的样子，根本无法想象她曾经作为勇者挥剑战斗。")
                            msgs.append("面对整晚都在渴求阴茎的她，有熟客说不如让他手下的一个小队来玩轮奸秀吧！")
                            msgs.append("结果留下了光靠乳交就榨干了一个小队的精液这样的轶事。")
                            maturo = "乳交娼妇"
                        else:
                            msgs.append(f"{tn}彻底堕落的身体让所有客人都很尽兴。从现在这个在男人身上淫乱不堪的样子，根本无法想象她曾经作为勇者挥剑战斗。")
                            msgs.append("一天到晚都在渴求阴茎，还曾发生把初次接待的客人榨干致死的事。")
                            msgs.append("没有三个人一起上是搞不定她的，传出这样的传闻，让预约她的客人反而大大增加了。")
                            maturo = "高级娼妇"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("成熟了的淫乱魔族的肉体，是堕落神最好的祭品之一。")
                            msgs.append(f"神官长使用秘术，活祭{tn}的仪式取得了成功。")
                            msgs.append(f"現在{tn}已脱离了现世，去堕落神身边体验永恒的快乐了。")
                            maturo = "堕落神的祭品"
                        else:
                            msgs.append(f"{tn}被带到神殿的深处。")
                            msgs.append(f"以神官长为首的神官们，对{tn}使用了秘术。")
                            msgs.append("「堕落神即将降临」「神殿新的祭品」「默示录即将开始」等等稀奇古怪的传言，对你来说是无关重要的事了吧……")
                            maturo = "堕落神的巫女"
                    else:
                        if has_talent(204):
                            msgs.append(f"「知道主人为她花费了多少吗？」正当客人这样窃窃私语的时候，{tn}在掌声中入场了。")
                            msgs.append(f"被带上台的{tn}腹部夸张地隆起，能看出快要临盘了。")
                            msgs.append("排卵诱发剂让她同时多重怀孕了，也进一步注射了阵痛诱发剂。")
                            msgs.append("今晚的出产秀，到底会生出个什么呢？大家都拭目以待。")
                            maturo = "妊娠便器"
                        else:
                            msgs.append(f"「知道她的主人为她花费了多少吗？」正当客人这样窃窃私语的时候，{tn}在掌声中入场了。")
                            msgs.append(f"被车子推上台的{tn}的股间被两根巨大的假阳具撑开到极限。")
                            msgs.append(f"因肉奴隶出色的状态而兴奋非常的客人们，催促着主人把手伸向{tn}……")
                            maturo = "扩张奴隶"
                elif sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的高级将校"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的高级酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的好事之徒"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 50:
                            msgs.append(f"{tn}现在作为主人的保镖兼情人生活着。")
                            msgs.append("即使已经堕落了，原勇者的战斗力也是不容小视的。")
                            msgs.append("发情生疼的淫靡肉体，也每晚都被主人疼爱着。")
                            maturo = "高级将校的保镖"
                        else:
                            msgs.append(f"{tn}现在作为主人的情人生活着。")
                            msgs.append("淫媚的肉体，每晚都接受着主人过剩性欲的糟蹋。")
                            msgs.append("至今为止已经玩坏了许多奴隶的主人，貌似终于找到一个可以承受他日夜征讨的性奴隶了。")
                            maturo = "高级将校的情人"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}与其说是女服务员，不如说是恳求客人交欢的妓女。")
                            msgs.append("用高耸挺拔的乳房引诱着客人往乳沟里塞小费，事成后马上把客人拖去另一个房间。")
                            msgs.append("似乎只要给够钱，不管什么人都可以同度春宵的样子。")
                            maturo = "高级酒馆的女侍应"
                        else:
                            msgs.append(f"{tn}每晚都参加舞台上各式各样的表演。")
                            msgs.append("从钢管舞到轮奸，从兽奸到分娩秀，什么玩法都表演过了。")
                            msgs.append("现在，孩子都长大，还被轮奸出孙子了，但依然保持着妖艳的肉体。")
                            maturo = "高级酒馆的表演者"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}每天从神殿开门到神殿关门，都被信徒们侵犯着。")
                            msgs.append("在堕落神的保佑下，即使没怀孕，也会从丰满的乳房滴出母乳来。")
                            msgs.append("现在已经彻底沉迷在无穷的快感之中，完全变成堕落神的信徒了。")
                            maturo = "堕落神的信徒"
                        else:
                            msgs.append(f"{tn}每天从神殿开门到神殿关门，都被信徒们侵犯着。")
                            msgs.append("在信徒中有着高人气，每次都同时被好几人狠狠玩弄。")
                            msgs.append("不过，看起来貌似对这样的生活感到很幸福的样子。")
                            maturo = "堕落神的性奴"
                    else:
                        if has_talent(204):
                            msgs.append("作为肉便器被放置在屋子的厕所里，无论主人、客人还是佣人，男女老少都可以使用。")
                            msgs.append(f"特意请人来负责肉便器{tn}的清洁及维护工作。")
                            msgs.append("每使用一次都进行一遍保养，主人就是想得这么周到。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"{tn}的手脚都被砍断了，作为主人的抱枕而存在着。")
                            msgs.append("为了照顾这样的抱枕，特意雇佣了一个女仆来负责。")
                            msgs.append("作为抱枕，好像有着无论被侵犯多少次都不够的样子。")
                            maturo = "好事者的抱枕"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的黑帮"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界的黑酒吧"; local = 1
                    else:
                        locals_name = "魔界的赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 30:
                            msgs.append(f"{tn}成为黑社会的一员了。因为原来的勇者经历，被委以重任了。")
                            msgs.append("每晚都用淫秽的肉体和部下交欢着，团队内部因此非常团结。")
                            msgs.append(f"{tn}在黑社会中如何生存下去真的难以预料，愿她长寿吧……")
                            maturo = "黑帮成员"
                        else:
                            msgs.append(f"{tn}成为黑社会的一員了。作为成员情妇的{tn}每晚都要侍奉不同的男人。")
                            msgs.append("对于一天都不能没有性爱的她来说，也算是一个可喜的环境吧。")
                            msgs.append(f"{tn}在黑社会中如何生存下去真的难以预料，愿她长寿吧……")
                            maturo = "黑社会的情妇"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被放在橱窗里吸引客人。不知是否是妓院主人的爱好，她的丰满的乳房被画上了下流的图案，乳头也穿了几个乳环。")
                            msgs.append(f"因为这个原因，总有很多熟客找上门来。对于{tn}这一直渴求男人的淫靡肉体来说，能每晚交欢，应该是比能挣钱还重要吧。")
                            msgs.append("她已经无法想象没有性的生活了。")
                            maturo = "刺青娼妇"
                        else:
                            msgs.append(f"{tn}被放在橱窗里吸引客人。不知是否是妓院主人的爱好，她的脸的右側被画上了下流的图案。")
                            msgs.append("貌似因为这个原因吸引了不少有着奇妙癖好的熟客，每晚她的房间里都传出不间断的悲鸣。")
                            msgs.append(f"对于不能没有男人的{tn}来说，这样的生活也许也是一种幸福吧。")
                            maturo = "刺青娼妇"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("贩毒的黑帮在自己经营的黑酒吧里，也流通着毒品。")
                            msgs.append(f"{tn}被喂食了特制的母乳果实，双峰分泌出特殊的母乳了。")
                            msgs.append("一般都是把母乳挤到杯子里，不过一些优待的客人可以直接从乳房上喝。")
                            msgs.append(f"母乳里有强烈的催情成分，一般{tn}当场就被这些客人侵犯了。")
                            maturo = "黑酒吧的乳奴隶"
                        else:
                            msgs.append("贩毒的黑帮在自己经营的黑酒吧里，也流通着毒品。")
                            msgs.append(f"{tn}平常只是做一般的服务员，有时也会被一些嗑药嗑高了，或者喝多了的客人侵犯。")
                            msgs.append("不过她也挺享受这种偶发事件的。")
                            maturo = "黑酒吧的女侍应"
                    else:
                        if has_talent(204):
                            msgs.append("赌场为了安抚那些输了很多的客人，就会把他们带到一个侍奉房间里。")
                            msgs.append(f"在里面，客人可以彻底地玩弄作为肉便器的{tn}，")
                            msgs.append("私处和肛门，被塞了很多赌场特制的筹码，")
                            msgs.append("每天在赌场里输掉的人络绎不绝，看来今后她都要作为肉便器玩具永远这样生活下去了。")
                            maturo = "赌场的肉便器"
                        else:
                            msgs.append(f"{tn}成为了赌场的赠品。")
                            msgs.append("在被买回来的当天，就被作为附加礼品送给了中了大乐透的客人。")
                            msgs.append("不过不久之后，就作为借款的抵押，又被赌场当成赠品了。这样的事连续发生了好多次。")
                            msgs.append("在赌徒中，开始有流言说她是会吸取财运的魔女。")
                            maturo = "赌场的赠品"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的酒吧"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "乞丐"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "触手小屋"; local = 1
                    else:
                        locals_name = "公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 20:
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。特别的魔法，让她被射中的痛楚都会转变为快感。")
                            msgs.append(f"赢了的人，就可以当场侵犯已经发情的{tn}，不过她做爱如此疯狂，常常会把优胜者给榨干。")
                            maturo = "酒吧的赠品"
                        else:
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。特别的魔法，让她被射中的痛楚都会转变为快感。")
                            msgs.append(f"赢了的人，就可以当场侵犯已经发情的{tn}，其它的参赛者，往往也会在之后对她进行轮奸。")
                            maturo = "酒吧的赠品"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("晚上在主人的巢穴里被疼爱着，白天则被租给主人的乞丐朋友，为主人换取喝酒钱。")
                            msgs.append("丰满的乳房被毫不客气地玩弄着，但淫靡的肉体却无法反抗这种醉人的痛楚。")
                            msgs.append(f"不过，{tn}貌似对成为主人朋友们的宠物感到挺愉悦的。")
                            maturo = "乞丐的妻子"
                        else:
                            msgs.append("晚上在主人的巢穴里被疼爱着，白天则被租给主人的乞丐朋友，为主人换取喝酒钱。")
                            msgs.append(f"不过，{tn}貌似对成为主人朋友们的宠物感到挺愉悦的。")
                            maturo = "乞丐的妻子"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append("特别是膨胀到原来两倍大小的惊人豪乳所培养出来的触手更是价值连城。")
                            maturo = "触手的苗床"
                        else:
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append("完全适应了作为触手的母体，看来这样的生活会持续到她死去的那一天。")
                            maturo = "触手的苗床"
                    else:
                        if has_talent(204):
                            msgs.append(f"被锁在公厕里的{tn}，作为公众肉便器开始了无休止的侍奉。")
                            msgs.append("被无尽的男人們侵犯，只是最普通的日常罢了。")
                            msgs.append(f"直到{tn}身上的鎖鏈被解開的那天，好像为几百人生了孩子。")
                            maturo = "公众便所"
                        else:
                            msgs.append(f"{tn}作为市民的公众肉便器，不分昼夜地被使用着。")
                            msgs.append("每次被男人侵犯的时候，她都不停地娇声呻吟着。")
                            msgs.append("被你彻底调教的淫乱身体起了充分的反应，不断吸收着市民们的欲望。")
                            maturo = "公众肉便器"
            else:
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的间谍培训机构"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的高级妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神官长"; local = 1
                    else:
                        locals_name = "魔界大富豪"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 100:
                            msgs.append(f"{tn}在人间界被保护了的消息，你是知道的。")
                            msgs.append("到底怎么逃出去的还不清楚，不过的确是回到了原来的王国。")
                            msgs.append("受到了很好的治疗，不断康复，同时积极地进言向魔界进军。")
                            msgs.append("据说引导了主流舆论，组成了相当规模的大军。")
                            msgs.append("可是你知道，他们进军的地区是魔界中也相当有名的激战区，人类军团在那种地狱应该没有胜算吧。")
                            msgs.append("而且，因为这样，那个王国现在守备空虚，")
                            msgs.append("你开始盘算着如何侵略它了……")
                            maturo = "魔界的间谍"
                        else:
                            msgs.append("将所有知道的地面情报都供出了之后，被当作活教材被收容在设施里。")
                            msgs.append(f"以原勇者的名头与新人对战训练，是{tn}无聊的牢狱生活中唯一的娱乐。")
                            msgs.append("训练生们也知道这一点，所以在对战胜利之后，也会相当彻底地凌辱她一番。")
                            maturo = "间谍教材"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"作为完全调教的奴隶而被买入的{tn}，马上就被客人指名了。")
                            msgs.append("最初的客人为了留念，在她的乳房上留下了刺青，从那时起，老鸨就为她推出了刺青服务。")
                            msgs.append(f"各种各样的刺青，现在充斥在{tn}高耸迷人的乳房上。")
                            maturo = "高级娼妇"
                        else:
                            msgs.append(f"作为完全调教的奴隶而被买入的{tn}，马上就被客人指名了。")
                            msgs.append("像淫魔一样变换着花式来榨取着客人的精气，她的身姿连老鸨都看呆了。")
                            msgs.append(f"实际上，{tn}没用多久，就成为了头牌。")
                            maturo = "高级娼妇"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("彻底被调教開發的淫乱肉体，是堕落神最好的祭品之一。")
                            msgs.append("更何况是信仰其它神灵的人。")
                            msgs.append(f"神官长，花了相当长的时间来传教，将{tn}的信仰扭转，发誓完全皈依堕落神。")
                            msgs.append("作为堕落神的教徒，会享受到一生的无尽快感吧。")
                            maturo = "堕落神的信徒"
                        else:
                            msgs.append(f"{tn}被带到了神殿深处。")
                            msgs.append("以神官长为首的神官们，为她施下了淫乱的秘术。")
                            msgs.append("准备着数百年一次的仪式，貌似打算把她当作最后一天的祭品。")
                            maturo = "堕落神的巫女"
                    else:
                        if has_talent(204):
                            msgs.append(f"被做了手术，{tn}作为肉便器被放在屋里。")
                            msgs.append("手脚都被切掉了，身子和一根铁管连在一起一动也不能动。")
                            msgs.append("一般来说这么弄要顺便洗脑的，不过主人说要保持她的智力和意识，所以未实施。")
                            msgs.append("通常女孩被这么弄早就发疯了，但被你彻底调教的她却坚持了下来。")
                            msgs.append(f"被主人和客人的尿淋满一身，{tn}居然愉悦地绝顶了。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"{tn}被装上台座，被放到屋里。")
                            msgs.append("台座伸出两根巨大的假阳具，深深地插入了她的私处及肛门，不停抽插着。")
                            msgs.append(f"在同一房间内，不知有多少个与{tn}一样处境的原勇者，被作为展品似的放置着。")
                            msgs.append("那位大富豪貌似有这样的收藏癖，用重金把所有战败勇者都收集起来。")
                            maturo = "大富豪的收藏品"
                elif sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的高级将校"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的高级酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的好事之徒"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_cflag(9) >= 50:
                            msgs.append(f"{tn}被主人卓越的调教弄得彻底堕落了，然后被编入了魔界军。")
                            msgs.append("原勇者的实力，让她得心应手地指挥着部队。")
                            msgs.append("她的部队据说有着非常凶悍的炮友亲卫队，用疯狂的战斗热情让其它部队都感到颤抖。")
                            maturo = "魔界的士官"
                        else:
                            msgs.append("作为主人的其中一个新奴隶住在屋子里。")
                            msgs.append("在宅邸里，还有几个其它种族的奴隶的照料着主人。")
                            msgs.append(f"{tn}发挥领导人的才智，把大家团结起来，互助互爱，因而得到了主人的认可，成为了奴隶长。")
                            maturo = "高级将校的奴隶"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}的乳头被打入了好几根乳钉，穿着露乳服装接待着客人。")
                            msgs.append("客人們可以拔下她乳头上的细钉，來代替叉子来食用料理。")
                            msgs.append("这种服务，受到了客人们的广泛好评。")
                            maturo = "高级酒馆的女侍应"
                        else:
                            msgs.append(f"{tn}被指派专门接待脾气不好的客人。但被客人责骂，{tn}也感到相当愉悦。")
                            msgs.append("应对性骚扰也显得游刃有余，对于淫乱的她来说，这根本不是問題。")
                            msgs.append("当然，为了接待怎么也不满足的客人，她为他们留下了一间特别的侍奉房间。")
                            maturo = "高级酒馆的女侍应"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}每天从神殿开门到神殿关门，都被信徒们侵犯着。")
                            msgs.append("在堕落神的保佑下，即使没怀孕，也会从丰满的乳房滴出母乳来。")
                            msgs.append("而且，生出的孩子也被神殿所重视，重点培养了。")
                            maturo = "神殿的性奴"
                        else:
                            msgs.append(f"{tn}每天从神殿开门到神殿关门，都被信徒们侵犯着。")
                            msgs.append("作为异族以及信奉其它神的人，在信徒中有着高人气，每次都同时被數人狠狠玩弄。")
                            msgs.append(f"现在，{tn}已经成为了信仰堕落神的性巫女，将在神殿中度过余生。")
                            maturo = "堕落神的巫女"
                    else:
                        if has_talent(204):
                            msgs.append("作为男仆們和女仆們的肉便器被绑在马厩里。")
                            msgs.append(f"当然，马到了发情期的时候，会狠狠地侵犯{tn}。")
                            msgs.append("主人有时也会身穿便服来马厩侵犯她。脏脏的小屋里，气氛非常和谐。")
                            maturo = "马厩的肉便器"
                        else:
                            msgs.append("作为好事者的抱枕被使用着。")
                            msgs.append("手脚都被切断了，被削成人棍，还被装上了一些可爱的装饰。")
                            msgs.append("不过，也许是主人的睡相不好吧～总是在早上发现她掉到床下正在挣扎。")
                            maturo = "好事者的抱枕"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的黑帮"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界的黑酒吧"; local = 1
                    else:
                        locals_name = "魔界的赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}作为干部的情妇生活着。")
                            msgs.append(f"{tn}在干部的卓越调教下堕落了，利用她来操纵着部下。")
                            msgs.append("被放到别墅里，每晚都侍奉着不同的男人。")
                            maturo = "黑社会的情妇"
                        else:
                            msgs.append(f"{tn}作为虐待狂干部的情妇生活着。")
                            msgs.append("她最开始也为此困惑过，不过夜晚的生活比想象中的更充实、更令她满足。")
                            msgs.append(f"每晚的过激玩法，让{tn}彻底沉迷于这种快乐。")
                            maturo = "黑社会的情妇"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}隔着橱窗招揽客人。")
                            msgs.append("在橱窗待了一段时间之后，她出名了。因为袒胸露乳的衣着下，她丰满的乳房被画上了下流的刺青，乳头也被穿上乳环。")
                            msgs.append("虽然以后也很难把胸部藏起来了，但在熟客们的照顾下，还是过得不错。")
                            maturo = "橱窗娼妇"
                        else:
                            msgs.append(f"{tn}隔着橱窗招揽客人，看上去已经习惯自己的妆容了。")
                            msgs.append("身为异族女人好像特别受欢迎，最近每个月底都会有个魔族男人总是指名她。")
                            msgs.append("直接包夜，结结实实地侵犯着她的全身，把她弄丢几十次。")
                            msgs.append(f"那人有意无意地传递着想帮她赎身的想法，但{tn}婉拒了。")
                            maturo = "橱窗娼妇"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("贩毒的黑帮在自己经营的黑酒吧里，也流通着毒品。")
                            msgs.append(f"{tn}被喂食了特制的母乳果实，双峰分泌出特殊的母乳了。")
                            msgs.append("有着强力陶醉效果的母乳，如果不定期榨取，母体本身都会因此疯掉。")
                            msgs.append("现在一直恳求被侵犯的同时，也恳求着客人来挤奶。")
                            maturo = "黑酒馆的瘾君子"
                        else:
                            msgs.append("贩毒的黑帮在自己经营的黑酒吧里，也流通着毒品。")
                            msgs.append(f"{tn}完全沉迷在毒品带来的快乐中，彻底上瘾了。整天发出甘甜、妖艳的喘息。")
                            msgs.append("今晚，也在客人胯间努力地用嘴巴吸啜着，一但射出精液，也会满足地一饮而尽。")
                            maturo = "黑酒馆的瘾君子"
                    else:
                        if has_talent(204):
                            msgs.append("赌场为了安抚那些输了很多的客人，就会把他们带到一个侍奉房间里。")
                            msgs.append(f"在里面，客人可以彻底地玩弄作为肉便器的{tn}．")
                            msgs.append("私处和肛门，被塞了很多赌场特制的筹码，")
                            msgs.append("每天在赌场里输掉的人络绎不绝，看来今后她都要作为肉便器玩具永远这样生活下去了。")
                            maturo = "赌场的肉便器"
                        else:
                            msgs.append(f"{tn}成为了赌场的赠品。")
                            msgs.append("在被买回来的当天，就被作为附加礼品送给了中了大乐透的客人。")
                            msgs.append("不过，在那个赌场里，奴隶是可以当作赌注的。")
                            msgs.append(f"{tn}因此被作为赌注，在数十个赌徒之间被不停转手着。")
                            maturo = "赌场的赠品"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的酒吧"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "乞丐"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "触手小屋"; local = 1
                    else:
                        locals_name = "公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append("周末，这种酒吧都会搞一些特别的竞赛。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。特别的魔法，让她被射中都不会留下伤口，而是转变为一种电击似的痛楚。")
                            msgs.append("谁让她惨叫得最大声，谁就会成为优胜者。竞赛在热烈的气氛中持续着。")
                        else:
                            msgs.append("周末，这种酒吧都会搞一些特别的表演。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。特别的魔法，让她被射中都不会留下伤口，而是转变为一种电击似的痛楚。")
                            msgs.append("酒吧老板很有技巧地投掷着飞镖，让她连晕过去都做不到，持续地惨叫着……")
                        maturo = "酒吧的赠品"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}晚上在主人的巢穴里被疼爱着，白天则被租给主人的乞丐朋友，为主人换取喝酒钱。")
                            msgs.append("丰满的乳房被毫不客气地玩弄着，但淫靡的肉体却无法反抗这种醉人的痛楚。")
                            msgs.append("怀孕生下的孩子马上又被卖掉了，因此更加频繁地出租给别人。")
                        else:
                            msgs.append(f"{tn}晚上在主人的巢穴里被疼爱着，白天则被租给主人的乞丐朋友，为主人换取喝酒钱。")
                            msgs.append("怀孕生下的孩子马上又被卖掉了，因此更加频繁地出租给别人。")
                        maturo = "乞丐的妻子"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("被不知道几万的触手侵犯过，头脑都变得不正常了。")
                            msgs.append("曾经漂亮的丰满乳房现在已经彻底变成触手的温床了。")
                        else:
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("被不知道几万的触手侵犯过，头脑都变得不正常了。")
                            msgs.append("不止是私处，连直肠都无可避免地成为了触手的温床。")
                        maturo = "触手的苗床"
                    else:
                        if has_talent(204):
                            msgs.append(f"被锁在公厕里的{tn}，作为公众肉便器开始了无休止的侍奉。")
                            msgs.append(f"被地下城里各个种族的无尽的男人侵犯，对她来说，还没有住在公厕里辛苦。")
                            msgs.append(f"后来，通过了肉便器放置的法案，{tn}被开放了。直到那天为止，好像为几百人生了孩子。")
                        else:
                            msgs.append(f"被锁在公厕里的{tn}，作为公众肉便器开始了无休止的侍奉。")
                            msgs.append("各个种族的男人都使用她的身体来处理性欲。")
                            msgs.append(f"后来，通过了肉便器放置的法案，{tn}被开放了。直到那天为止，好像为几百人生了孩子。")
                        maturo = "公众肉便器"

        # ==================================================================
        # 普通 (その他)
        # ==================================================================
        else:
            if is_mazoku:
                if sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的高级将校"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界地方领主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的大商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"被改造成魔族的{tn}，每晚都被主人温柔地对待着。")
                            msgs.append("她好像在主人身上感受到了在你身上感受不到的东西。")
                            msgs.append("主人也觉得自己买了个好奴隶，非常满意。")
                            maturo = "高级将校的性奴"
                        else:
                            msgs.append(f"主人把{tn}当作宠物来饲养。")
                            msgs.append("主人整天在客人来访的时候让她讲述自己如何作为勇者战败，最后沦落为奴隶的故事。每讲一次，都能宾主尽欢。")
                            msgs.append("主人对此非常满意，认为自己买了个好奴隶。")
                            maturo = "高级将校的宠物"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}作为母乳机被放在屋内。")
                            msgs.append("被灌下了特殊的药物，以前就很有规模的乳房，现在更加膨胀了，总是滴出母乳。")
                            msgs.append(f"然后，{tn}的母乳，总是受到主人的称赞。")
                            maturo = "人形奶牛"
                        else:
                            msgs.append(f"{tn}被领主送给儿子当新玩具。")
                            msgs.append("那个孩子，有着禁忌的血统的力量，传闻有时候会巨魔化然后捏碎自己的奴隶。")
                            msgs.append("她的下场，想必不会很好吧。")
                            maturo = "领主孩子的玩具"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被放在神殿的角落，身边围满了呱噪的信徒们。")
                            msgs.append("在新奴隶即将作为神殿侍奉而举行的仪式上，一整天都被信徒们持续轮奸着。")
                            msgs.append(f"这一期的女孩，素质大多都差不多。但其中有着诱人双峰的{tn}是最受欢迎的。")
                            maturo = "神殿的奴隶"
                        else:
                            msgs.append(f"{tn}因为被发现信奉着其它的神，立刻被带到了地下室。")
                            msgs.append("神官们嘲弄着她的信仰，不停地狠狠侵犯着她，直到蓝色肌肤完全被精液染成白色。")
                            msgs.append("她的理性终于被粉碎，屈服了，发誓自己将皈依堕落神。")
                            maturo = "堕落神的信徒"
                    else:
                        if has_talent(204):
                            msgs.append(f"作为肉便器被买回来的{tn}，被装到一个专用的箱子里。")
                            msgs.append("主人商务出差的时候，就被当做行李搬走，作为主人专用的肉便器随着出差。")
                            msgs.append(f"「这是大商人的肉箱子！」，搬行李的人指着{tn}对其它人这么说到。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"{tn}作为主人的第五个性奴隶在宅邸的地下室生活着。")
                            msgs.append("多亏了你的调教，她早就习惯了地下的生活，很快就习惯了新环境。")
                            msgs.append("每晚被叫去侍奉主人也是轻车熟路，对她来说就是单纯换了个主人而已。")
                            maturo = "性奴隶"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的士官"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界大农场"; local = 1
                    else:
                        locals_name = "魔界的赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为奖赏，赏给立了战功的士官。")
                            msgs.append("「这么年轻漂亮的魔族姑娘是我的奴隶」，年轻的士官还不是很适应状况，因而像恋人一样地对待她。")
                            msgs.append(f"{tn}积极地回应着主人的疼爱，展露出与年轻的脸不相称的性交上的成熟。")
                        else:
                            msgs.append(f"{tn}作为奖赏，赏给立了战功的士官。")
                            msgs.append("士官对年轻漂亮的魔族姑娘尽情地蹂躏着。")
                            msgs.append("要说为什么的话，刚从战场回来的士官，总是特别粗暴的。")
                        maturo = "士官的性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被放在橱窗里吸引客人。不知是否是妓院主人的爱好，她的丰满的乳房被画上了下流的图案，乳头也穿了几个乳环。")
                            msgs.append(f"据说在被弄上淫靡装饰的时候，{tn}不停地在哭喊。")
                            msgs.append("不过现在似乎已经忘记了那件事，每晚都在客人的拥抱中发出娇媚的呻吟。")
                        else:
                            msgs.append(f"{tn}被放在橱窗里吸引客人。不知是否是妓院主人的爱好，她的脸的右侧被画上了下流的图案。")
                            msgs.append(f"据说在被弄上淫靡装饰的时候，{tn}不停地在哭喊。")
                            msgs.append("不过现在似乎已经忘记了那件事，总是跨坐在客人的身上发出娇媚的呻吟。")
                        maturo = "橱窗娼妇"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"大农场的主人在买其它农奴的时候顺便买下了{tn}，作为礼物送给自己的儿子们。")
                            msgs.append(f"邪恶的孩子们，特别喜欢欺负{tn}敏感的肛门。")
                            msgs.append(f"此时此刻，{tn}也正作为肛门玩具，被他们狠狠地侵犯着。")
                        else:
                            msgs.append(f"大农场的主人在买其它农奴的时候顺便买下了{tn}，作为礼物送给自己的儿子们。")
                            msgs.append(f"邪恶的孩子们，每晚都要狠狠地侵犯{tn}。")
                            msgs.append("没多长时间，她怀孕了，孩子们对父亲是谁开了一个赌局。")
                        maturo = "大农场里的玩具"
                    else:
                        if has_talent(204):
                            msgs.append("赌场为了安抚那些输了很多的客人，就会把他们带到一个侍奉房间里。")
                            msgs.append(f"在里面，客人可以彻底地玩弄作为肉便器的{tn}。")
                            msgs.append("私处和肛门，被塞了很多赌场特制的筹码，")
                            msgs.append("每天在赌场里输掉的人络绎不绝，看来今后她都要作为肉便器玩具永远这样生活下去了。")
                            maturo = "赌场肉便器"
                        else:
                            msgs.append(f"{tn}成为了赌场的赠品。")
                            msgs.append("作为美丽的魔族奴隶的她，被漂亮地包装着，")
                            msgs.append("等待着什么时候，会有新主人来把自己带走……")
                            maturo = "赌场赠品"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的矿山主"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "触手小屋"; local = 1
                    else:
                        locals_name = "公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("连续被侵犯几次都不屈服。「再这么下去真是一点都不可爱」")
                        else:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("好几次在被侵犯都嚎啕大哭。矿工们觉得这很有意思，令她相当受欢迎。")
                        maturo = "矿山性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。优胜者可以拿到可观的奖金。")
                            msgs.append("在决出优胜者的时候，她那宏伟挺拔的乳房，早已鲜血横流了。")
                        else:
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。优胜者可以拿到可观的奖金。")
                            msgs.append("在决出优胜者的时候，她的身体已经千疮百孔，血流满地了。")
                        maturo = "酒吧的玩具"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append("特别是膨胀到原来两倍大小的惊人豪乳所培养出来的触手更是价值连城。")
                        else:
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append("完全适应了作为触手的母体，看来这样的生活会持续到她死去的那一天。")
                        maturo = "触手的苗床"
                    else:
                        if has_talent(204):
                            msgs.append("作为现役肉便器继续侍奉着。")
                            msgs.append(f"{tn}在相当长的时间内作为公众肉便器被广大市民所疼爱。")
                            msgs.append("好像生下了不下一百个的孩子。")
                        else:
                            msgs.append(f"{tn}作为公众肉便器不分昼夜地被使用着。")
                            msgs.append("过于残酷的生活让她不到半年便精神崩溃了。")
                        maturo = "公众肉便器"
            else:
                if sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的高级将校"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界地方领主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "堕落神的神殿"; local = 1
                    else:
                        locals_name = "魔界的大商人"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append("主人把她当成重要的性奴隶来看待。")
                            msgs.append(f"然后，{tn}也尽力地侍奉着主人，在主人身上感受到了在你身上感受不到的温柔。")
                            msgs.append("虽然没有自由，但每晚都被主人充分地疼爱着，似乎过得很幸福。")
                            maturo = "高级将校的性奴"
                        else:
                            msgs.append(f"主人把{tn}当作宠物来饲养。")
                            msgs.append("主人整天在客人来访的时候让她讲述自己如何作为勇者战败，最后沦落为奴隶的故事。每讲一次，都能宾主尽欢。")
                            msgs.append(f"然后，客人总会轻蔑地看着{tn}。主人每次都很享受这种时光。")
                            maturo = "高级将校的宠物"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}作为母乳机被放在屋内。")
                            msgs.append("被灌下了特殊的药物，以前就很有规模的乳房，现在更加膨胀了，总是滴出母乳。")
                            msgs.append("主人还特意雇佣了一个女仆来照顾她以及加热她的母乳。")
                            maturo = "人形奶牛"
                        else:
                            msgs.append(f"{tn}被领主送给儿子当新玩具。")
                            msgs.append(f"那个孩子，有着禁忌的血统的力量，有时候会巨魔化，然后抓起{tn}当飞机杯使。")
                            msgs.append(f"用原勇者的体质顽强地坚持着，但{tn}看来也熬不了多久了。")
                            maturo = "领主孩子的玩具"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}作为侍奉神殿的女奴，整天都被信徒们侵犯着。")
                            msgs.append("本来信奉其它神灵的她，现在已经彻底转为信奉堕落神了。")
                            msgs.append("那对诱人的双峰被绳子勒着，更是极大地激发起信徒们的情欲。")
                            maturo = "堕落神的性奴"
                        else:
                            msgs.append(f"{tn}因为被发现信奉着其它的神，立刻被带到了地下室。")
                            msgs.append("神官们嘲弄着她的信仰，不停地狠狠侵犯着她，直到全身肌肤完全被精液染成白色。")
                            msgs.append("她的理性终于被粉碎，屈服了，发誓自己将皈依堕落神。")
                            maturo = "堕落神的信徒"
                    else:
                        if has_talent(204):
                            msgs.append(f"最初只是作为肉便器被买回来的{tn}，被放在主人的房间里。")
                            msgs.append("作为主人专用的便器，在主人使用的时候，总是目不转睛地珍惜着与主人一起相处的时间。")
                            msgs.append(f"被当成肉便器的{tn}被调教的这么好，主人也很满意。")
                            maturo = "肉便器"
                        else:
                            msgs.append(f"{tn}作为主人的宠物生活在屋里。")
                            msgs.append("在主人的脚下撒娇着，她已经忘记了自己曾经身为勇者了吧。")
                            msgs.append("看来她的一生也就是这样了。")
                            maturo = "大商人的宠物"
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔王军的士官"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的妓院"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔界大农场"; local = 1
                    else:
                        locals_name = "魔界的赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"年轻的士官用奖金买下了{tn}。")
                            msgs.append("作为异族的温驯的美女奴隶，每晚都在疼爱着。")
                            msgs.append(f"{tn}热情地接受着新主人的所有欲望。")
                        else:
                            msgs.append(f"年轻的士官用奖金买下了{tn}。")
                            msgs.append("作为异族的温驯美女奴隶，每晚都在疼爱着。")
                            msgs.append(f"{tn}用悲鸣回应着新主人的欲望。")
                        maturo = "士官的性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}成为了专门收集异族美女的妓院里的奴隶。")
                            msgs.append("为了让她逃跑也跑不远，在丰满的乳房上烙下了烙印，因为过度的疼痛而晕倒了。")
                            msgs.append("托了原勇者这个绰头的福，现在这里完全不愁客人了。")
                        else:
                            msgs.append(f"{tn}成为了专门收集异族美女的妓院里的奴隶。")
                            msgs.append("为了让她逃跑也跑不远，在肩膀上烙下了烙印，因为过度的疼痛而晕倒了。")
                            msgs.append("托了原勇者这个绰头的福，现在这里完全不愁客人了。")
                        maturo = "异种专用娼妇"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}因为丰满的乳房而被看中了。作为牛奴隶被栓在厩舍里。")
                            msgs.append("怀上了牛系魔兽的孩子，乳房还被注射了肥大化的药剂，作为乳牛每天被榨乳。")
                            msgs.append(f"被榨乳的时候，{tn}的脸上总会露出销魂的表情。")
                            maturo = "乳牛奴隶"
                        else:
                            msgs.append(f"为了做出新品种的家畜而让{tn}和所有的家畜交配。")
                            msgs.append("实验还在继续，应该能培养出意想不到的新物种吧。")
                            msgs.append("「和魔界猪杂交出来的品种，肉应该会变得更加松软吧。」")
                            maturo = "家畜奴隶"
                    else:
                        if has_talent(204):
                            msgs.append("赌场为了安抚那些输了很多的客人，就会把他们带到一个侍奉房间里。")
                            msgs.append(f"在里面，客人可以彻底地玩弄作为肉便器的{tn}。")
                            msgs.append("私处和肛门，被塞了很多赌场特制的筹码，")
                            msgs.append(f"每天在赌场里输掉的人络绎不绝，看来今后{tn}都要作为肉便器玩具永远这样生活下去了。")
                            maturo = "赌场的肉便器"
                        else:
                            msgs.append(f"{tn}成为了赌场里的赛狗。")
                            msgs.append("被彻底调教的她，现在只会四脚爬爬地行走了。")
                            msgs.append(f"赛跑成绩不错的{tn}，被拿去和其它赛狗配种，人们希望她能生出更优良的赛狗。")
                            maturo = "赌场的狗"
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的矿山主"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "魔界的酒吧"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "触手小屋"; local = 1
                    else:
                        locals_name = "公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append("连续被侵犯几次都不屈服。「再这么下去真是一点都不可爱」")
                        else:
                            msgs.append(f"{tn}作为开矿奴隶的慰问品被饲养着。")
                            msgs.append(f"{tn}好几次在被侵犯时都会嚎啕大哭，矿工们觉得很有意思。这令她相当受欢迎。")
                        maturo = "矿山性奴"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。优胜者可以拿到可观的奖金。")
                            msgs.append("在决出优胜者的时候，她那宏伟挺拔的乳房，早已鲜血横流了。")
                        else:
                            msgs.append("周末，这种酒吧都会搞一些特别的活动。")
                            msgs.append(f"{tn}作为飞镖的靶子，参加了特别的飞镖比赛。优胜者可以拿到可观的奖金。")
                            msgs.append("在决出优胜者的时候，她的身体已经千疮百孔，血流满地了。")
                        maturo = "酒吧的玩具"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append("特别是膨胀到原来两倍大小的惊人豪乳所培养出来的触手更是价值连城。")
                        else:
                            msgs.append(f"{tn}被安排在量产触手的触手小屋里，")
                            msgs.append("不知培养了多少触手，也许成百上千了。")
                            msgs.append(f"{tn}已经完全适应了作为触手的母体，看来这样的生活会持续到她死去的那一天。")
                        maturo = "触手的苗床"
                    else:
                        if has_talent(204):
                            msgs.append("作为现役肉便器继续侍奉着。")
                            msgs.append(f"{tn}在相当长的时间内，作为公众肉便器而被广大市民所疼爱。")
                            msgs.append("好像生下了不下一百个的孩子。")
                        else:
                            msgs.append(f"{tn}作为公众肉便器，不分昼夜地被使用着。")
                            msgs.append("过于残酷的生活让她不到半年便精神崩溃了。")
                        maturo = "公众肉便器"

        # ------------------------------------------------------------------
        # Final output: set family CSTR, TSTR, closing text
        # ------------------------------------------------------------------
        family_idx = self._search_family(target)
        if family_idx >= 0:
            self.interpreter.vars.chars[family_idx].cstr[5] = f"{maturo}{tn}"

        if not hasattr(self.interpreter.vars, 'tstr'):
            self.interpreter.vars.tstr = {}
        self.interpreter.vars.tstr[30] = f"{maturo}{tn}"

        msgs.append("")
        msgs.append(f"就这样，{master_name}和{tn}再也没有见面……")
        msgs.append("")

        return (msgs, maturo)


    # ======================================================================
    # SELL_MATURO_K1 (异种族末路口上)
    # ======================================================================




    def _sell_maturo_k1(self, target: Character, sell_price: int) -> Tuple[List[str], str]:
        """异种族末路口上 - sold to non-demon buyers.
        Returns (messages, maturo_title).
        """
        msgs: List[str] = []
        tn = target.name
        player = self._get_player()
        master_name = player.name if player else ""

        def has_talent(tid: int) -> bool:
            return int(target.talent.get(tid, 0)) == 1

        def get_abl(aid: int) -> int:
            return int(target.abl.get(aid, 0))

        def get_cflag(cid: int) -> int:
            return int(target.cflag.get(cid, 0))

        def get_mark(mid: int) -> int:
            return int(target.mark.get(mid, 0))

        is_mazoku = int(target.talent.get(314, 0)) == 9
        is_dragon = int(target.talent.get(314, 0)) == 5
        maturo = ""

        # ==================================================================
        # 反抗刻印Lv3
        # ==================================================================
        if get_mark(3) == 3:
            if is_mazoku:
                if sell_price >= 100000:
                    if random.randint(0, 1) == 0:
                        locals_name = "食脑魔的诸侯"; local = 1
                    else:
                        locals_name = "食脑魔的大神官"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if get_cflag(9) >= 50:
                            msgs.append(f"反抗心很强的{tn}受到了好事之徒的喜爱。")
                            msgs.append("脑子被改造，成为了唯命是从的奴隶。")
                            msgs.append(f"{tn}，现在作为优秀的指挥官，不断地流着爱液和口水履行着自己的职务。")
                            maturo = "脑改造指挥官"
                        else:
                            msgs.append(f"反抗心很强的{tn}被好事之徒改造了脑子。")
                            msgs.append("但是手术失败了，完全成为了废人，行为退行到婴幼儿一样。")
                            msgs.append("每天屎尿横流地，无忧无虑在玩耍……")
                            maturo = "白痴"
                    else:
                        if has_talent(202) or has_talent(206):
                            msgs.append(f"反抗心很强的{tn}成为了奇怪的教团的干部。")
                            msgs.append("现在，已经被洗脑成了顺从的神圣娼妓了。")
                            msgs.append(f"{tn}向信徒们大开双腿，述说着堕落神的慈爱。")
                            maturo = "堕落神的神圣娼妇"
                        else:
                            msgs.append(f"反抗心很强的{tn}被奇怪的教团选为祭品了。")
                            msgs.append("脑子的一部分被献给了堕落神，现在已经成为了完全顺从的神圣娼妓。")
                            msgs.append("口水和爱液不断地流出来，但是她却感到幸福……")
                            maturo = "堕落神的神圣娼妇"
                else:
                    if random.randint(0, 1) == 0:
                        locals_name = "恶魔的诸侯"; local = 1
                    else:
                        locals_name = "恶魔的大富豪"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if random.randint(0, 1) == 0:
                            msgs.append(f"反抗心很强的{tn}成为了恶魔的玩具。")
                            msgs.append("性器被改造得乱七八糟，还弄出了阴茎，")
                            msgs.append("被恶魔们当成杂耍奴隶而存在着。")
                            maturo = "恶魔的玩具"
                        else:
                            msgs.append(f"反抗心很强的{tn}成为了肥料制造装置。")
                            msgs.append("嘴巴被强灌家畜用的饲料，不到一个小时就产生了优质的肥料。")
                            msgs.append(f"因为脱粪时的叫声很像叫床声，{tn}被")
                            msgs.append("设置在开阔的农田中，作为展示物而被展示着。")
                            maturo = "脱粪肥料装置"
                    else:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"反抗心很强的{tn}被当作奶罐被饲养着畜舍里。")
                            msgs.append("原来就很有规模的乳房，被魔法和药物弄得更加夸张了，犹如史莱姆一般。")
                            msgs.append(f"每天都被强制地榨乳和播种，{tn}口水和爱液持续不断地滴落下来。")
                            maturo = "奶罐"
                        else:
                            msgs.append(f"反抗心很强的{tn}被魔法夺取了作为人类的思考和语言能力。")
                            msgs.append("现在，无论有没有来客，她都被颈圈和锁链扣着，作为一只用四肢爬行的狗而存在。")
                            msgs.append("今晚，也在进行着与狗交配的表演。")
                            msgs.append(f"{tn}带着幸福的表情，积极地扭动着自己的腰肢。")
                            maturo = "无脑的牝犬"
            else:
                if sell_price >= 100000:
                    if is_dragon:
                        locals_name = "高阶魔法研究所"; local = 2
                    elif has_talent(200) or has_talent(203):
                        locals_name = "兽人的佣兵团"; local = 1
                    else:
                        locals_name = "吸血鬼的暗黑神殿"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 2:
                        msgs.append(f"反抗心很强的{tn}被当作珍贵的异族关入了笼子里。")
                        msgs.append(f"{tn}被饲养在充满法师和魔女的魔法研究设施中。")
                        msgs.append("每天都有人定时采集她的血液及排泄物。")
                        msgs.append(f"被充分灌肠，在桶里排泄着的{tn}，满眼泪光……")
                        maturo = "排泄实验素材"
                    elif local == 1:
                        msgs.append(f"{tn}作为护卫剑士被雇佣了。")
                        if get_cflag(9) >= 100:
                            msgs.append(f"靠着武艺高强和牙尖嘴利，{tn}成为了兽人们大姐一样的角色。")
                            msgs.append("有时在训练的时候，还会直接用脚踢飞它们。")
                            msgs.append("「到底谁才是奴隶啊……」兽人们苦笑着……")
                        else:
                            msgs.append(f"{tn}没怎么反抗了，似乎适应了在佣兵团的生活。")
                            msgs.append("使用着和兽人一样的嚣张语气，不管问题都用拳头解决，训练的时候用木剑相互搏击……")
                            msgs.append("一天的辛劳过后，还会和兽人们一起裸体洗澡……")
                            msgs.append(f"看来很快{tn}就会成为佣兵团里不可或缺的一员了吧。")
                        maturo = "护卫剑士"
                    else:
                        if has_talent(202) or has_talent(206):
                            msgs.append(f"反抗心很强的{tn}，被吸血鬼所洗礼，成了暗黑之神的信徒。")
                            msgs.append("由于已经被邪恶的仪式洗脑了几次，现在的她忠诚而得心应手地履行着职务。")
                            msgs.append("不过，由于使用了强烈的药物，她经常无意识地失禁，接着因此绝顶……")
                            maturo = "暗黑神的信徒"
                        else:
                            msgs.append(f"反抗心很强的{tn}，现在作为饮料机为吸血鬼提供着血液。")
                            msgs.append("全身被紧紧地拘束着，抽血的管子从胳膊处延伸出来。进食和排泄也都通过管子来处理。")
                            msgs.append("她唯一的乐趣，就是临睡前被爱抚至绝顶，每天有且仅有一次……")
                            maturo = "吸血鬼的饮料"
                else:
                    if random.randint(0, 1) == 0:
                        locals_name = "巨魔佣兵团"; local = 1
                    else:
                        locals_name = "恶魔的人间牧场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 1:
                        if random.randint(0, 1) == 0:
                            msgs.append(f"反抗心很强的{tn}被改造成适应巨魔佣兵团团长的阴茎的飞机杯。")
                            msgs.append("手脚都被切掉，私处被扩张至极限，用锁链绑在了巨魔的身上。")
                            msgs.append("子宫也完全的肉穴化了，变得无论怎么被弄都不会怀孕的样子……")
                            maturo = "巨魔的飞机杯"
                        else:
                            msgs.append(f"反抗心很强的{tn}被当成巨魔们的繁殖用便器。")
                            msgs.append(f"{tn}的子宫，像气球一样地夸张膨胀着，孕育着健康的巨魔婴儿。")
                            msgs.append(f"孩子到底是谁的，{tn}自己也分不清楚了……")
                            maturo = "巨魔的繁殖便器"
                    else:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"反抗心很强的{tn}作为奶罐而被饲养着畜舍里。")
                            msgs.append("旁边排列着不知多少和她相似的裸体女人，全员的乳房都被逼近极限地肥大化了。")
                            msgs.append(f"淌着口水，一副高潮脸的{tn}，和鼻子上的鼻环真相称呢～")
                            maturo = "奶罐"
                        else:
                            msgs.append(f"反抗心很强的{tn}作为繁殖用牲畜而被饲养在畜舍里。")
                            msgs.append("也不知道哪里买回来的男奴，在她身上拼命地挺动着腰，锁链撞得啦啦作响。")
                            msgs.append(f"{tn}的自由和人权都被剥夺了，只能贪图着性交的快乐……")
                            maturo = "繁殖用家畜奴隶"

        # ==================================================================
        # 爱慕或淫乱
        # ==================================================================
        elif has_talent(85) or has_talent(76):
            if is_mazoku:
                # 魔族 100万+
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "暗黑龙"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "上级恶魔"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "异形之神的神殿"; local = 1
                    else:
                        locals_name = "魔兽的研究设施"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}成为了暗黑龙的新娘，在龙的洞穴里生活着。")
                            msgs.append("接受着龙的挞伐和种子，帮助濒临绝种的龙延续后代而多次怀孕产子。")
                            msgs.append("最近，好像因为暗黑龙的播种过度而叫苦不迭。")
                        else:
                            msgs.append(f"{tn}成为了暗黑龙的新娘，在龙的洞穴里生活着。")
                            msgs.append("魔族的肉体接受着龙的挞伐和种子，孕育了几只龙的幼崽。")
                            msgs.append(f"{tn}的肉体，按照龙的想法在持续地被改造着。")
                        maturo = "暗黑龙的新娘"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"有着伟岸胸部的{tn}成为了上级恶魔的女仆。")
                            msgs.append("穿着露出乳头的衣服，乳头常年兴奋地勃起着。")
                            msgs.append("一但被主人发现乳头勃起，就要接受淫秽的惩罚，")
                            msgs.append(f"但是，即使是主人邪恶的催淫咒语，{tn}也愉悦地享受着……")
                        else:
                            msgs.append(f"{tn}成为了上级恶魔的女仆。")
                            msgs.append("只要犯错，就会触发主人的自慰诅咒，当场自慰起来。")
                            msgs.append("一直带着常人难以理解的紧张感在工作着。")
                            msgs.append(f"不过最近，{tn}似乎故意犯错而主动地在公开自慰，主人为此十分苦恼。")
                        maturo = "上级恶魔的女仆"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}在异形之神的神殿，照顾着变异的信徒。")
                            msgs.append("那些信徒，无论吃饭还是行走，都需要她的帮助。")
                            msgs.append(f"而且，如果那可怕的阴茎勃起的话，也是需要{tn}用肛门去平复的。")
                        else:
                            msgs.append(f"{tn}在异形之神的神殿，照顾着变异的信徒。")
                            msgs.append(f"作为神的新娘，{tn}的子宫是信徒们的公共财产。")
                            msgs.append("现在，也接受了异形的种子，怀上了异形宝宝。")
                        maturo = "异形之神的干事"
                    else:
                        if get_abl(15) >= 5:
                            msgs.append(f"{tn}用巧妙的话语说服了魔兽研究所的研究人员，")
                            msgs.append("让她主导了实验室里试验品的购买和使用。")
                            msgs.append("和魔兽、异形杂交用的奴隶，从各地被她购买回来，明天都在听着她们的悲鸣而手淫着。")
                            maturo = "实验室的采购"
                        else:
                            msgs.append(f"{tn}作为与魔兽交配用的奴隶被买回来了，现在也被强制与怪物交配着。")
                            msgs.append("最近，好像对魔兽们起了爱意，交配时会忘情地叫着实验魔兽的名字。")
                            msgs.append("扭动着腰，与魔兽相互亲吻着……")
                            maturo = "魔兽交配奴隶"

                # 魔族 50万+
                elif sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "食人魔佣兵团"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "半人马的骑士团"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "牛头人祭司"; local = 1
                    else:
                        locals_name = "兽人富商"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(203):
                            msgs.append(f"{tn}成为了食人魔佣兵团的一员，起到支援和后勤的作用。")
                            msgs.append("专心致志地，负责着资产管理、装备与物资的购买等工作。")
                            msgs.append("因为怀上了团长的孩子，肚子夸张地膨胀了起来，孕育着下一任的团长。")
                        else:
                            msgs.append(f"{tn}作为佣兵团的战士而活跃着。")
                            msgs.append("比起奴隶时代，肌肉也好，筋骨也好，都更加强壮了。")
                            msgs.append(f"佣兵团的食人魔们看着这样的{tn}，个个都情难自禁。")
                            msgs.append("强大的战斗力，对于它们来说才是最富吸引力的性魅力。")
                        maturo = "食人魔佣兵团员"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}过着抚养半人马孩子的生活。")
                            msgs.append("丰满的乳房，不断地供给着母乳，尽显慈母姿态。")
                            msgs.append("半人马的孩子，和马一样，阴茎拥有令人咋舌的尺寸。")
                            msgs.append(f"看着青涩的果实逐渐成长，{tn}忍不住舔了舔嘴唇。")
                            msgs.append("「今晚，也进行禁断的性教育吧……」")
                            maturo = "半人马的奶妈"
                        else:
                            msgs.append(f"{tn}作为骑士团的侍从，在打杂着。")
                            msgs.append("半人马的性欲很强，不允许她的下半身穿任何东西。")
                            msgs.append(f"{tn}经常因此突然间就被推倒、侵犯…………")
                            maturo = "半人马骑士侍从"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}作为优秀的祭典活动人，受到牛头人祭司们的肯定。")
                            msgs.append("作为暗黑神的使徒，在仪式的时候要一边用肛门自慰着，一边跳着淫乱的舞蹈。")
                            msgs.append("那个肛门，被扩张到了极限，通过奇妙的方式盛开着……")
                            maturo = "牛头人圣女"
                        else:
                            msgs.append(f"作为牛头人神殿的圣母，{tn}怀上了牛头人的幼崽。")
                            msgs.append("为了产下混血又强大的牛头人，进行着仪式，")
                            msgs.append("现在，这位圣母正分娩着牛面之神的孩子……")
                            maturo = "牛头人圣母"
                    else:
                        if has_talent(204):
                            msgs.append(f"作为宴客用肉便器，{tn}在兽人的屋子里有着特殊的地位。")
                            msgs.append("拿勇者来当肉便器，充分满足了兽人富商的虚荣心。")
                            msgs.append(f"被放在书房角落的肉便器，经常在主人和客人的视线下毫无顾忌地疯狂自慰着。")
                            msgs.append("只是这样看着，就让兽人富商沉醉在像得到一切似的成就感……")
                            maturo = "宴客肉便器"
                        else:
                            msgs.append(f"作为爱人被买回来的{tn}在兽人的屋子里有着特殊的地位。")
                            msgs.append(f"兽人富商完全倾心于{tn}，每天都用珠宝华服打扮着她。")
                            msgs.append(f"{tn}穿着华丽的衣饰，似乎整个人连气质都变了。")
                            maturo = "兽人的爱人"

                # 魔族 10万+
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "六头海蛇的联防队"; local = 3
                    elif has_talent(205) or has_talent(201):
                        locals_name = "黑暗精灵的学校"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔像的大农场"; local = 1
                    else:
                        locals_name = "狼人的赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为六头海蛇联防队的外雇战士被雇佣了。")
                            msgs.append(f"被调教过的{tn}，顺从着命令，在联防队里表现活跃。")
                            msgs.append(f"然而，{tn}的性欲太强了，经常在训练时偷偷地和其它的六头海蛇做爱。")
                            msgs.append("最近，她把全队的风气都搞得一团糟，终于被装上了贞操带，并严令不得在工作时间进行任何形式的性行为。")
                        else:
                            msgs.append(f"{tn}作为六头海蛇联防队的外雇战士被雇佣了。")
                            msgs.append(f"被调教过的{tn}，顺从着命令，在联防队里表现活跃。")
                            msgs.append("在共同的磨砺和战斗中，逐渐与其它六头海蛇建立起了信赖。")
                            msgs.append("最近，还传来了即将要和队里其中一只年轻的六头海蛇结婚的消息。")
                        maturo = "六头海蛇的联防队外籍战士"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在黑暗精灵的中学做讲师。")
                            msgs.append(f"胸部呼之欲出，{tn}被少年们所憧憬着。")
                            msgs.append(f"最近，她和黑暗精灵少年的淫行被发现了。")
                            msgs.append(f"作为惩罚，{tn}被刺上了【淫行老师】的刺青。")
                            maturo = "黑暗精灵学校的淫行老师"
                        else:
                            msgs.append(f"{tn}在黑暗精灵的中学做讲师。")
                            msgs.append(f"经验丰富的{tn}被少年们所憧憬着。")
                            msgs.append(f"与全班的男生都维持着性关系，{tn}貌似对几名女生都出手了。")
                            msgs.append("据说在保健课上，与全班一起在搞性实习……")
                            maturo = "黑暗精灵学校的淫行老师"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}在魔像的大农场里，从事着生产肥料的工作。")
                            msgs.append("大量的剩菜残羹和饲料被灌入像孕妇一样发胀的肚子，在被改造过的内脏里发酵。")
                            msgs.append("然后，随着她的娇喘，优质的肥料就会被排泄出来。")
                            maturo = "肥料生产奴隶"
                        else:
                            msgs.append(f"{tn}成为了魔像的生物部件在大农场里工作着。")
                            msgs.append(f"{tn}全身都被封入了魔像体内，大脑一片空白地操纵着魔像的行动。")
                            msgs.append("已经失去了所有的思考能力，只是永恒体验着在胯间和乳头的慰安装置带来的快乐。")
                            maturo = "魔像的生物部件"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}在狼人的赌场里，当肉便器。")
                            msgs.append(f"被改造成能怀上犬类的{tn}，正出演着被狼人侵犯的表演。")
                            msgs.append("「在被射第几次会怀孕呢？」带着这样的赌局，观众们纷纷投注。")
                            maturo = "赌场的兽奸女优"
                        else:
                            msgs.append(f"{tn}在狼人的赌场里，当肉便器。")
                            msgs.append(f"被改造成扶她的{tn}，在把女狼人弄高潮之前都不被允许射出来。")
                            msgs.append("「到底能干多少个女狼人才射呢？」带着这样的赌局，观众们纷纷投注。")
                            maturo = "赌场的扶她玩具"

                # 魔族 10万-
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "兽人佣兵团"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "巨魔的奴隶主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "黑暗精灵的学者"; local = 1
                    else:
                        locals_name = "街角的杂耍小屋"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为佣兵团的一员被招募了。")
                            msgs.append(f"喜欢性爱的{tn}，经常在训练的时候偷偷给别的兽人口交。")
                        else:
                            msgs.append(f"{tn}作为佣兵团的一员被招募了。")
                            msgs.append(f"被团长看上了，坚持要和她生个孩子，{tn}每晚都被团长播种着……")
                        maturo = "兽人佣兵团员"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}成为了巨魔苦力们的飞机杯。")
                            msgs.append("巨魔们完全不知道什么叫怜香惜玉，直接把她套在自己的阴茎上，疯狂地机械运动着。")
                            msgs.append("奶水从她丰满的胸部中被粗暴地挤出，用来给巨魔解渴。")
                        else:
                            msgs.append(f"{tn}成为了巨魔苦力的飞机杯。")
                            msgs.append("巨魔们完全不知道什么叫怜香惜玉，直接把她套在自己的阴茎上，疯狂地机械运动着。")
                            msgs.append("被改造成只能靠巨魔的精液生存。她经常带着淫荡的表情，脸都歪了。")
                        maturo = "巨魔的慰安妇"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}成为了新的性拷问研究用实验体。")
                            msgs.append("肛门被特殊的假阳具，日以继夜地蹂躏着。")
                            msgs.append("这个新发明，据说是用来开发通过阴道无法感受的超强快感。")
                        else:
                            msgs.append(f"{tn}成为了新的性拷问研究用实验体。")
                            msgs.append("不断地被注射着新型的媚药，不断地重复令人发疯的绝顶高潮。")
                            msgs.append("最近，只是被风吹到，就能令她绝顶高潮了。于是为了研究忍耐快感的药物，学者们开始了反向的实验……")
                        maturo = "黑暗精灵学者的实验体"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}的肉体被淫秽地改造了，被全身赤裸地放在店里招揽客人。")
                            msgs.append("被改造出了怪诞的性器官，乳房淫乱至极地膨胀着，吸引着街上行人的好奇心。")
                            msgs.append("最近，还和有着丑陋阴茎的扶她奴隶公开做爱。")
                        else:
                            msgs.append(f"{tn}的肉体被淫秽地改造了，被全身赤裸地放在店里招揽客人。")
                            msgs.append("被改造出了奇形怪状的阴茎。被带到街边进行公开自慰表演。")
                            msgs.append("因为射精太多而阳痿了。最近，好像学会了如何把软趴趴的阴茎塞入阴道里自慰。")
                        maturo = "杂耍小屋的扶她便器"

            else:
                # 其他种族 100万+
                if sell_price >= 1000000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "堕天使的贵族"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "狮鹫快递"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "蛇妖的高级妓院"; local = 1
                    else:
                        locals_name = "哥布林的大剧场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}成为了堕天使的贵族少年的性教育者。")
                            msgs.append("对越堕落越强大的堕天使来说，教育最重要的一环，就是性实习。")
                            msgs.append(f"但是，连性欲旺盛的堕天使少年都忍不住发出了悲鸣，因为{tn}每晚都疯狂地榨取着精液。")
                        else:
                            msgs.append(f"{tn}成为了堕天使的贵族少年的性教育者。")
                            msgs.append("对越堕落越强大的堕天使来说，教育最重要的一环，就是性实习。")
                            msgs.append(f"{tn}总是温柔地拥抱着因性欲旺盛而在自己身上拼命耸动腰身的堕天使少年。")
                        maturo = "堕天使少年的私教"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}成为了狮鹫的骑手。")
                            msgs.append("表面上是送快递，实际上却是上门服务的应召女郎。")
                            msgs.append(f"有着迷人胸部的{tn}，在屡次被指名后，成为看板娘了。")
                        else:
                            msgs.append(f"{tn}成为了狮鹫的骑手。")
                            msgs.append("表面上是送快递，实际上却是上门服务的应召女郎。")
                            msgs.append(f"进步很快的{tn}，以超强的口交技术而闻名。")
                        maturo = "狮鹫骑士"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}成为了专卖菊花的妓女。")
                            msgs.append(f"在各色各样异种族名流聚集的蛇妖妓院里，{tn}拥有很高的人气。")
                            msgs.append(f"在平常妓院会被拒之门外的异形客人，今天也聚集在{tn}的门外企图一亲芳泽。")
                            maturo = "菊穴娼妇"
                        else:
                            msgs.append(f"{tn}在异种族热衷的蛇妖妓院里工作着。")
                            msgs.append(f"哪怕怀上了异形的孩子，{tn}依然要为一些喜欢孕妇的客人打开双腿。")
                            msgs.append(f"在平常妓院会被拒之门外的异形客人，今天也聚集在{tn}的门外企图一亲芳泽。")
                            maturo = "异种奸娼妇"
                    else:
                        if get_abl(15) >= 5:
                            msgs.append(f"{tn}成为了哥布林们的偶像，现在也在大剧场里载歌载舞着。")
                            msgs.append(f"{tn}穿着欲盖弥彰的下流布条作为衣服，在舞台上唱着黄色歌曲。")
                            msgs.append("为了欣赏那淫荡的姿态，哥布林们把场馆都快挤爆了。")
                        else:
                            msgs.append(f"{tn}成为了哥布林们的偶像，现在也在大剧场里载歌载舞着。")
                            msgs.append(f"{tn}穿着欲盖弥彰的下流布条作为衣服，在舞台上扭动着纤腰。")
                            msgs.append("那淫荡的姿态，让哥布林粉丝越来越多。")
                        maturo = "哥布林的偶像"

                # 其他种族 50万+
                elif sell_price >= 500000:
                    if has_talent(207) or has_talent(203):
                        locals_name = "黑暗精灵的暗杀公会"; local = 3
                    elif has_talent(205) or has_talent(200):
                        locals_name = "六头海蛇的海盗船"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "大富豪蛇妖"; local = 1
                    else:
                        locals_name = "暗黑兽人战士"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(203):
                            msgs.append(f"{tn}成为了暗杀公会的情报人员。")
                            msgs.append(f"过往成了谜，{tn}从不同的炮友身上不断地窃取着信息。")
                            msgs.append("在没有工作的日子里，每晚都焦急地等待着性拷问。")
                            maturo = "暗杀公会的情报员"
                        else:
                            msgs.append(f"{tn}成为了暗杀公会的刺客。")
                            msgs.append(f"过往成了谜，和{tn}睡过的男人，第二天总会发现已经惨死。")
                            msgs.append("在没有工作的日子里，每晚都焦急地等待着性拷问。")
                            maturo = "暗杀公会的刺客"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}成为了六头海蛇海贼团的船长。")
                            msgs.append("好像是因为那双引人入胜的漂亮乳房，被六头海蛇们推举上去的。")
                            msgs.append("现在，她正坐在船长室的高座上，享受着亲信的按摩。")
                            maturo = "女海贼团船长"
                        else:
                            msgs.append(f"{tn}成为了六头海蛇海贼团的水手。")
                            msgs.append("船上的水手们，都是被掠夺来的奴隶。")
                            msgs.append(f"{tn}，向这些肮脏的水手分开双腿，缓和着他们的不满情绪。")
                            maturo = "女海贼团船员"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}每晚都被喜欢百合的蛇妖欺负着。")
                            msgs.append(f"喜欢玩弄后庭的蛇妖富豪，用她的灵活的长舌头捣弄着{tn}的肛门。")
                            msgs.append(f"{tn}只感觉肛门都要融化了，每次都忍不住发出苦恼的喘息……")
                            maturo = "蛇妖的百合奴隶"
                        else:
                            msgs.append(f"{tn}每晚都被喜欢百合的蛇妖欺负着。")
                            msgs.append(f"蛇妖们喜欢用她修长的身体，缠绕着{tn}。")
                            msgs.append(f"每次，{tn}都忍不住发出苦闷的喘息，痛苦地扭动着。")
                            maturo = "蛇妖的百合奴隶"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}全身都被刻上了奇怪的咒术刺青，在未开化的蛮族部落里生活着。")
                            msgs.append("乳头、私处、鼻子、耳朵统统穿满了环，完全不像以前的样子了。")
                            msgs.append(f"{tn}的背上，还刻着蛮族主人的名字。这种被拥有的感觉，让她觉得愉悦不已。")
                            maturo = "蛮族兽人的一员"
                        else:
                            msgs.append(f"{tn}全身都被刻上了奇怪的咒术刺青，在未开化的蛮族部落里生活着。")
                            msgs.append("乳头、私处、鼻子、耳朵统统穿满了环，完全不像以前的样子了。")
                            msgs.append(f"从那时起，{tn}已经完全成为另一个人，总是满怀喜悦地拥抱着蛮族那宽广的胸膛。")
                            maturo = "蛮族兽人的一员"

                # 其他种族 10万+
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "魔界的植物园"; local = 3
                    elif has_talent(205) or has_talent(201):
                        locals_name = "兽人骑士团"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "鹰身女妖的奴隶中介"; local = 1
                    else:
                        locals_name = "花妖炼金术师"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为养分的供给，在培育着魔界的植物。")
                            msgs.append("魔界植物的根，深深地扎入了她的阴道，直接吸取体内的养分。")
                            msgs.append(f"喜欢做爱的{tn}，无法抗拒那插入的感觉，通过阴道把自己的一切都献给植物了。")
                            maturo = "魔界植物的苗床"
                        else:
                            msgs.append(f"{tn}作为养分的供给，在培育着魔界的植物。")
                            msgs.append("魔界植物的根，深深地扎入了她的直肠，直接吸取体内的养分。")
                            msgs.append(f"{tn}培育出来的植物，发育得非常良好，甚至在品评会上得奖了。")
                            maturo = "魔界植物的苗床"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}被兽人的骑士团拿来抚育和训练兽人的孩子。")
                            msgs.append("随着傲人双峰被改造，她负责了所有孩子的喂养。同时努力地给兽人的孩子进行战斗训练。")
                            msgs.append("村庄的深处，偶尔会传来作为母体的女人们的呻吟声……")
                            msgs.append("她一听就知道又有一个兽人的孩子出生了，自己又有工作了。")
                            maturo = "兽人的幼教"
                        else:
                            msgs.append(f"{tn}作为兽人骑士团的一员而战斗着。")
                            msgs.append("骑士团袭击了人类的村庄，掠夺着金钱和女人。")
                            msgs.append(f"{tn}发现了一个躲藏着的女人，将手里的人类战士首级丢出，把她吓了出来。")
                            msgs.append(f"带着拼命求饶的女人，{tn}凯旋而归，回到了深爱的兽人丈夫身边。")
                            maturo = "兽人骑士团员"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}被鹰身女妖富豪作为照顾生活的奴隶买下了。")
                            msgs.append("她全身赤裸着，只戴着项圈，照顾着富豪的女儿。")
                            msgs.append(f"富豪的女儿，是个有名的性虐狂。{tn}经常被塞上肛塞，享受着严格的排泄管理。")
                            maturo = "鹰身女妖富豪的奴隶"
                        else:
                            msgs.append(f"{tn}被鹰身女妖富豪作为照顾生活的奴隶买下了。")
                            msgs.append("她全身赤裸着，只戴着项圈，照顾着鹰身女妖一家的生活。")
                            msgs.append(f"{tn}为了生出新的奴隶，在工作的闲暇，还要与男奴隶交配。")
                            maturo = "鹰身女妖的奴隶"
                    else:
                        if has_talent(204):
                            msgs.append(f"作为肉便器的{tn}为了收集实验用的精液，成为了公众便器。")
                            msgs.append(f"被肉体改造过的{tn}，用她那奇形怪状的阴道，吸取着精液，将精液存储在气球一般膨胀的子宫内。")
                            msgs.append("这大量的精液，将来会参与人造人的实验与制作。")
                            maturo = "公众肉便器"
                        else:
                            msgs.append(f"{tn}为了进行魔法的素材收集，被肉体改造了。")
                            msgs.append(f"{tn}被弄出了巨大的阴囊，不停地生产着精液。")
                            msgs.append("永远勃起无法软下的巨大阴茎，被管子连通着，不断地被榨精。")
                            msgs.append("「今天的量已经过半了。还剩下五千次，加油哦！」")
                            msgs.append(f"肛门被侵犯着，{tn}虚弱的身体不断颤抖，在这种折磨中持续地高潮。")
                            maturo = "生产精液的扶她奴隶"

                # 其他种族 10万-
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "兽人的高级战士"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "蜥蜴人骑士"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "黑暗精灵的女神官"; local = 1
                    else:
                        locals_name = "街边的公厕"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}与兽人的高级战士结婚了。")
                            msgs.append("迷上了兽人健壮的肉体，两人深深地相爱着。")
                            msgs.append(f"最近，作为丈夫的兽人，开始在性欲方面输给{tn}了。")
                        else:
                            msgs.append(f"{tn}与兽人的高级战士结婚了。")
                            msgs.append("迷上了兽人健壮的肉体，两人深深地相爱着。")
                            msgs.append("据说马上就要生第五个孩子了。")
                        maturo = "兽人高等战士的妻子"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}与蜥蜴人骑士结婚了。")
                            msgs.append("陌生的鳞片式肌肤，也没能阻止两人的爱。")
                            msgs.append(f"丈夫因为{tn}的巨乳而非常自豪，整天赞美着她。")
                        else:
                            msgs.append(f"{tn}与蜥蜴人骑士结婚了。")
                            msgs.append("陌生的鳞片式肌肤，也没能阻止两人的爱。")
                            msgs.append(f"随着一同度过的日子一天天过去，{tn}越发被丈夫所溺爱着，总是被丈夫赞美。")
                        maturo = "蜥蜴人骑士的妻子"
                    elif local == 1:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在黑暗精灵女神官的指引下修行着。")
                            msgs.append("交换了姐妹契约，每天都过着奉献给暗黑之神的生活。")
                            msgs.append(f"{tn}的傲人双峰外露着，乳环上发出契约魔法的光芒。")
                            maturo = "邪教的姐妹信徒"
                        else:
                            msgs.append(f"{tn}在黑暗精灵女神官的指引下修行着。")
                            msgs.append("交换了姐妹契约，每天都过着奉献给暗黑之神的生活。")
                            msgs.append(f"{tn}的性器被契约之环封闭着，应该再也不能接受阴茎了吧。")
                            maturo = "邪教的姐妹信徒"
                    else:
                        if has_talent(204):
                            msgs.append(f"在异种族的街道上，{tn}作为公众便器被锁在公厕里。")
                            msgs.append(f"{tn}必须接受所有种族的阴茎，哪怕怀孕也不能休息。")
                            msgs.append("生下来的孩子，受孤儿院收养，进行着出色的教育，将来也会为街区作出贡献吧。")
                            maturo = "公众肉便器"
                        else:
                            msgs.append(f"在异种族的街道上，{tn}作为公众便器被锁在公厕里。")
                            msgs.append(f"{tn}必须接受所有种族的阴茎，什么精液都要喝下去。")
                            msgs.append(f"据说，{tn}成为了相当有名的便器女，后来被常客买走结婚了。")
                            maturo = "公众肉便器"

        # ==================================================================
        # 普通 (その他)
        # ==================================================================
        else:
            if is_mazoku:
                # 魔族 50万+
                if sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "食人魔佣兵团"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "半人马的骑士团"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "牛头人祭司"; local = 1
                    else:
                        locals_name = "兽人富商"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(203):
                            msgs.append(f"{tn}作为顾问，加入了食人魔佣兵团。")
                            msgs.append(f"食人魔们服从着{tn}，将佣兵团的运营完全交给了她。")
                            msgs.append("前任团长手下的战士，则在偷偷地密谋，")
                            msgs.append(f"通过自己的巨根令{tn}服从，从而获得佣兵团里更大的权力。")
                            maturo = "食人魔佣兵团顾问"
                        else:
                            msgs.append(f"{tn}作为保镖，加入了食人魔佣兵团。")
                            msgs.append(f"在佣兵团进行掠夺的时候，{tn}自豪地挥舞着自己的武器。")
                            msgs.append("有着魔族力量的她，单手就把女骑士之类的撂倒了。")
                            msgs.append("抓回来的女人，则作为佣兵团的公共财产，被当作任意使用的肉便器。")
                            maturo = "食人魔佣兵团保镖"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}作为教职人员，加入了半人马的骑士团。")
                            msgs.append("教导着半人马的孩子们如何做一个合格的魔族。")
                            msgs.append("丰满的乳房，分泌出魔族的母乳，常常令孩子们勃起。")
                            msgs.append(f"这种时候，{tn}总会温柔地用手帮他们处理。")
                            maturo = "半人马的幼教"
                        else:
                            msgs.append(f"{tn}作为教职人员，加入了半人马的骑士团。")
                            msgs.append("教导着半人马的孩子们如何做一个合格的魔族。")
                            msgs.append(f"半人马的孩子，沐浴在{tn}的魔族的力量里，常常情不自禁地勃起。")
                            msgs.append(f"这种时候，{tn}就会扭动着腰，帮他们处理。")
                            maturo = "半人马的幼教"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}每晚都在牛头人神官们的仪式上奉献着后庭。")
                            msgs.append("被牛头人的巨根侵犯着的肛门，已经被扩张到了极限。")
                            msgs.append("括约肌完全松弛，没有肛门制动器的话，相信会对她的日常生活带来困扰吧。")
                            maturo = "牛头人神殿的贡品"
                        else:
                            msgs.append(f"{tn}接受了牛头人的信仰，成为了牛头人神殿的圣母。")
                            msgs.append("今天，性欲高涨的牛头人信徒们，又来到神殿了。")
                            msgs.append(f"{tn}一边听着他们的烦恼与告解，一边用手和嘴巴帮他们解决。")
                            maturo = "牛头人神殿的圣母"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为宴客用的肉便器，在屋子里像家畜似的被养着。")
                            msgs.append("全身都被写满了淫贱的话语，每天都被扶她奴隶侵犯着。")
                            msgs.append("肉体被下流地改造过的扶她奴隶，因为思考能力已经完全被性欲所掩盖，而疯狂地侵犯着其他的奴隶。")
                            msgs.append(f"「等到客人们也厌倦{tn}的时候，就把她也改造成扶她奴隶吧……」")
                            maturo = "宴客肉便器"
                        else:
                            msgs.append(f"作为情人被买回来的{tn}，温顺地顺从着自己的主人。")
                            msgs.append(f"兽人富商，几乎每天都买漂亮的衣服和饰品给{tn}穿戴。")
                            msgs.append("没过多久，她就爱上了兽人富商，子宫里孕育着半兽人的婴儿。")
                            maturo = "兽人商人的情人"

                # 魔族 10万+
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "六头海蛇的联防队"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "黑暗精灵的学校"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔像的大农场"; local = 1
                    else:
                        locals_name = "魔界的大监狱"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为六头海蛇联防队的外雇战士被雇佣了。")
                            msgs.append(f"工作结束后，{tn}常常被六头海蛇的前辈命令做性处理服侍。")
                            msgs.append(f"喜欢做爱的{tn}，没有一丝犹豫，")
                            msgs.append("今天的她也搔首弄姿地，在休息室里等候着……")
                            maturo = "六头海蛇的联防队外籍战士"
                        else:
                            msgs.append(f"{tn}作为六头海蛇联防队的外雇战士被雇佣了。")
                            msgs.append(f"工作结束后，{tn}常常被六头海蛇的前辈命令做性处理服侍。")
                            msgs.append("现在，已经完全适应了六头海蛇那与众不同的阴茎了。")
                            maturo = "六头海蛇的联防队外籍战士"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在黑暗精灵的中学做保健老师。")
                            msgs.append(f"胸部呼之欲出，{tn}被少年们所憧憬着。")
                            msgs.append("有烦恼的青少年们，都会去找她倾诉，被学生们信赖着。")
                            msgs.append("秉承着如果发泄掉性欲，那么烦恼就会消失的信条，保健室被弄得像妓院似的……")
                            maturo = "黑暗精灵学校的保健老师"
                        else:
                            msgs.append(f"{tn}在黑暗精灵的中学做保健老师。")
                            msgs.append(f"经验丰富的{tn}被少年们所憧憬着。")
                            msgs.append("有恋爱烦恼的少年少女们，都会去找她做性启蒙。")
                            msgs.append("保健室拜此所赐，被弄得像情人旅馆似的……")
                            maturo = "黑暗精灵学校的保健老师"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}在魔像的大农场里，从事着魔像维护的工作。")
                            msgs.append(f"{tn}的肉体被改造了，吃了的东西会在肠内变成魔像的燃料。")
                            msgs.append("然后，肛门被插入了管子，去供应魔像的活动。")
                            maturo = "魔像的维护工"
                        else:
                            msgs.append(f"{tn}在魔像的大农场里，从事着看守作物的工作。")
                            msgs.append(f"{tn}用探照魔法，照亮入侵的野生动物和盗贼，然后引导安保部队去处理。")
                            msgs.append("休息的时间，则在保安室里小睡，几乎没有任何的娱乐。")
                            msgs.append("只能拜托作为同事的奴隶，靠激烈的性爱来消磨时间。")
                            maturo = "农场保安"
                    else:
                        if has_talent(204):
                            msgs.append("为了让牛头人和半人马之类性欲旺盛的种族不造反。")
                            msgs.append(f"{tn}作为犯人的娱乐用具而被监狱买回来了，继续从事着肉便器的工作。")
                            msgs.append(f"{tn}接受着各种各样异种族的阴茎，几乎没有哪个现存种族的阴茎她没有品尝过了。")
                            maturo = "囚犯便器"
                        else:
                            msgs.append(f"{tn}作为犯人的娱乐用具而被监狱买回来了，继续从事着肉便器的工作。")
                            msgs.append("忍耐多时的犯人们毫不客气，用尽她身上的每一个部位来让自己舒服。")
                            msgs.append("据说和因猥亵罪而被捕的变态兽人相爱，准备要在监狱里结婚。")
                            maturo = "兽人囚犯的妻子"

                # 魔族 10万-
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "兽人佣兵团"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "巨魔的奴隶主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "黑暗精灵的学者"; local = 1
                    else:
                        locals_name = "街角的杂耍小屋"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}成为了兽人佣兵团的备品。")
                            msgs.append("她被绑在马车里，无休止地被侵犯着。")
                            maturo = "兽人佣兵团的备品"
                        else:
                            msgs.append(f"{tn}成为了兽人佣兵团的性处理器。")
                            msgs.append("每天都要为全员进行口交，清洁着大家的阴茎。")
                            maturo = "兽人佣兵团的性处理器"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在巨魔奴隶的工厂里作为慰安婦而工作着。")
                            msgs.append(f"{tn}用那迷人的巨乳，安抚着巨魔们的巨根。")
                            msgs.append(f"今天也是，工作完之后，巨魔们又在{tn}面前排起了长队。")
                            maturo = "苦力巨魔的慰安妇"
                        else:
                            msgs.append(f"{tn}在巨魔奴隶的工厂里作为慰安婦而工作着。")
                            msgs.append("有着巨大阴囊的巨魔们，性欲是非常旺盛的，得不到发泄就会捣乱。")
                            msgs.append(f"{tn}被镶嵌在墙上，只露出屁股。今天，又会被多少巨根蹂躏呢？")
                            maturo = "苦力巨魔的慰安妇"
                    elif local == 1:
                        if get_abl(3) >= 3:
                            msgs.append(f"{tn}成为了新媚药的实验体。")
                            msgs.append("肛门被涂上了烈性的新药，令人发疯的快感将她的一切思考能力都吹散了。")
                            maturo = "媚药实验体"
                        else:
                            msgs.append(f"{tn}成为了新媚药的实验体。")
                            msgs.append("阴蒂被涂上了烈性的新药，一整天都不断地绝顶高潮着。")
                            maturo = "媚药实验体"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为魔族奴隶，在杂耍小屋里全裸地被戏弄着。")
                            msgs.append("和肮脏的兽人公开做爱，为店里集聚了一点人气。")
                            maturo = "杂耍小屋的肉便器"
                        else:
                            msgs.append(f"{tn}作为魔族奴隶，在杂耍小屋里全裸地被戏弄着。")
                            msgs.append("身体被改造，还穿上了环，刻了刺青，为店里集聚了一点人气。")
                            maturo = "杂耍小屋的肉便器"

            else:
                # 其他种族 50万+
                if sell_price >= 500000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "食人魔佣兵团"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "半人马的骑士团"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "牛头人祭司"; local = 1
                    else:
                        locals_name = "兽人富商"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if has_talent(75):
                            msgs.append(f"{tn}作为高级性奴隶，加入了食人魔佣兵团。")
                            msgs.append(f"食人魔们恋慕着{tn}，像对圣母一样对待她。")
                            msgs.append("前任团长手下的战士，则在偷偷地密谋，")
                            msgs.append(f"通过自己的巨根令{tn}服从，从而获得佣兵团里更大的权力。")
                            maturo = "食人魔佣兵团的高级性奴"
                        else:
                            msgs.append(f"{tn}作为保镖，加入了食人魔佣兵团。")
                            msgs.append(f"经验丰富的{tn}，成为了佣兵团的剑，在前线作战着。")
                            msgs.append("她也不是对食人魔没有性魅力，因此为了不做性奴隶，")
                            msgs.append(f"{tn}也常常抢夺女人，用她们来代替自己成为肉便器。")
                            maturo = "食人魔佣兵团保镖"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}作为教职人员，加入了半人马的骑士团。")
                            msgs.append("教导着半人马的孩子们如何做一个合格的战士。")
                            msgs.append(f"有着巨乳的{tn}，非常受孩子们的欢迎，经常被缠着要喝母乳。")
                            maturo = "半人马的幼教"
                        else:
                            msgs.append(f"{tn}作为教职人员，加入了半人马的骑士团。")
                            msgs.append("教导着半人马的孩子们如何做一个合格的战士。")
                            msgs.append(f"作为异种族的{tn}，早早地就被孩子们舔遍全身，成为了班级里的共用便器了。")
                            maturo = "半人马的幼教"
                    elif local == 1:
                        if has_talent(77):
                            msgs.append(f"{tn}被牛头人神官作为祭品买回来了。")
                            msgs.append("虽然不需要奉献生命，但是每天都要在祭坛上奉献肛门。")
                            msgs.append("作为奴隶与其它奴隶一起卑微地戴着项圈，通过锁链被连在一起，等待着被侵犯。")
                            maturo = "牛头人的性祭品"
                        else:
                            msgs.append(f"{tn}被牛头人神官作为祭品买回来了。")
                            msgs.append("虽然不需要奉献生命，但是每天都要在祭坛上做爱。")
                            msgs.append("和性欲旺盛的青年疯狂地做爱，如果怀孕了就把孩子当奴隶卖掉。")
                            maturo = "牛头人的性祭品"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为宴客用的肉便器，在屋子里像家畜似得养着。")
                            if has_talent(121):
                                msgs.append(f"身为扶她的{tn}被改造出巨根，不停地侵犯着其它的奴隶。")
                            else:
                                msgs.append(f"被改造成扶她的{tn}，不停地侵犯着其它的奴隶。")
                            msgs.append("思考能力经过洗脑后完全被性欲所掩盖了，不再考虑射精以外的事情。")
                            maturo = "扶她便器"
                        else:
                            msgs.append(f"作为情人被买回来的{tn}，温顺地服从着自己的主人。")
                            msgs.append(f"兽人富商溺爱着{tn}，两人过着幸福的生活。")
                            msgs.append("没过多久，她就爱上了兽人富商，子宫里孕育着半兽人的婴儿。")
                            maturo = "兽人的情人"

                # 其他种族 10万+
                elif sell_price >= 100000:
                    if has_talent(200) or has_talent(203):
                        locals_name = "六头海蛇的联防队"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "黑暗精灵的学校"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "魔像的大农场"; local = 1
                    else:
                        locals_name = "哥布林赌场"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}作为六头海蛇联防队的外雇战士被雇佣了。")
                            msgs.append(f"工作结束后，{tn}总会被战斗心激昂的六头海蛇抓去泄欲。")
                            maturo = "六头海蛇的联防队外籍战士"
                        else:
                            msgs.append(f"{tn}作为六头海蛇联防队的杂役被雇佣了。")
                            msgs.append(f"被命令打磨铠甲的{tn}，如果工作有怠慢，屁股就会挨鞭子。")
                            maturo = "六头海蛇的联防队的打杂"
                    elif local == 2:
                        if has_talent(110) or has_talent(114) or has_talent(119):
                            msgs.append(f"{tn}在黑暗精灵的中学做备品。")
                            msgs.append(f"拥有漂亮巨乳的{tn}，在肉体改造的实验课上，被作为实验品摆上实验台了。")
                            maturo = "黑暗精灵中学的备品"
                        else:
                            msgs.append(f"{tn}在黑暗精灵的中学做备品。")
                            msgs.append("在肉体改造的实验课上，被作为实验品摆上实验台了，接下来要进行的是异种交配的控制实验。")
                            maturo = "黑暗精灵中学的备品"
                    elif local == 1:
                        if has_talent(124):
                            msgs.append(f"{tn}因为外形接近动物，因此作为繁殖用家畜，被饲养在马厩里。")
                            msgs.append("子宫被改造了，现在每三天就能生下一只家畜。")
                            msgs.append(f"这样的子宫，在分娩的时候，有着产生常人难以理解的快感的副作用，让{tn}的思考能力接近崩溃了。")
                            maturo = "繁殖用家畜奴隶"
                        else:
                            msgs.append(f"{tn}在农场里照看牲口。")
                            msgs.append("所谓的牲口，其实也是被家畜化改造过的肉便器。肥大化的乳房，方便被榨乳。")
                            msgs.append("有时，为了检查牲口是否健康，要把手伸进她们的肛门里，这时候，肉便器们的娇喘总是此起彼伏着。")
                            maturo = "家畜便器的管理员"
                    else:
                        if has_talent(204):
                            msgs.append(f"作为肉便器的{tn}，主持着赌场里受欢迎的赌局。")
                            msgs.append(f"哥布林们投注后，各自把精液装在一排的酒杯里，让{tn}喝掉，然后猜哪杯是谁的。")
                            msgs.append("被猜中的那个哥布林，就能独得所有人的投注。")
                            maturo = "赌场的玩具"
                        else:
                            msgs.append(f"{tn}在赌场里穿着兔女郎装做荷官。")
                            msgs.append(f"如果客人赢了，就能获得{tn}的一次口交。")
                            msgs.append("因此，她的那桌总是很受欢迎，排着长队。")
                            maturo = "赌场的兔女郎"

                # 其他种族 10万-
                else:
                    if has_talent(200) or has_talent(203):
                        locals_name = "兽人的公共澡堂"; local = 3
                    elif has_talent(205) or has_talent(207):
                        locals_name = "巨魔的奴隶主"; local = 2
                    elif has_talent(202) or has_talent(206):
                        locals_name = "黑暗精灵的大学生"; local = 1
                    else:
                        locals_name = "哥布林的村庄"; local = 0
                    msgs.append(f"{locals_name}买下{tn}之后………")
                    msgs.append("………"); msgs.append("……"); msgs.append("…")
                    if local == 3:
                        if get_abl(2) >= 5:
                            msgs.append(f"{tn}在公共澡堂里为兽人们按摩。")
                            msgs.append(f"如果在{tn}的手法下勃起了的话，只要加一点钱就能狠操{tn}一顿。")
                            maturo = "公共浴场的按摩师"
                        else:
                            msgs.append(f"{tn}在公共澡堂里为兽人们按摩。")
                            msgs.append("虽然经常累得肩膀生痛，但很受客人们的好评。")
                            maturo = "公共浴场的按摩师"
                    elif local == 2:
                        if has_talent(61) or has_talent(62):
                            msgs.append(f"{tn}被当做巨魔奴隶的清洁工。")
                            msgs.append(f"{tn}每天都要用身体，漂亮地擦干净那些脏得不行的巨魔们的屁股。")
                            maturo = "苦力巨魔的慰安妇"
                        else:
                            msgs.append(f"{tn}被当做巨魔奴隶的清洁工。")
                            msgs.append(f"{tn}每天都要用湿毛巾把那些不愿洗澡的巨魔们擦干净。")
                            maturo = "苦力巨魔的慰安妇"
                    elif local == 1:
                        if has_talent(315):
                            msgs.append(f"黑暗精灵的大学生，居然是{tn}原来的同学。")
                            msgs.append("结果，两人结婚了，过着幸福的生活。")
                            maturo = "黑暗精灵学生的妻子"
                        else:
                            msgs.append(f"黑暗精灵的大学生，把{tn}当做宿舍里的共用便器。")
                            msgs.append("结果那间宿舍，每天都有很多人来串门。")
                            maturo = "黑暗精灵学生的宿舍便器"
                    else:
                        if has_talent(204):
                            msgs.append(f"{tn}作为生育便器被哥布林们宠爱着。")
                            msgs.append("据说学会了哥布林的语言，幸福地为它们生下了孩子。")
                            maturo = "哥布林的生育便器"
                        else:
                            msgs.append(f"{tn}作为打杂受到了哥布林们的喜爱。")
                            msgs.append("据说学会了哥布林的语言，过着平淡而又幸福的生活。")
                            maturo = "哥布林的打杂"

        # ------------------------------------------------------------------
        # Final output: set family CSTR, TSTR, closing text
        # ------------------------------------------------------------------
        family_idx = self._search_family(target)
        if family_idx >= 0:
            self.interpreter.vars.chars[family_idx].cstr[5] = f"{maturo}{tn}"

        if not hasattr(self.interpreter.vars, 'tstr'):
            self.interpreter.vars.tstr = {}
        self.interpreter.vars.tstr[30] = f"{maturo}{tn}"

        msgs.append("")
        msgs.append(f"就这样，{master_name}和{tn}再也没有见面……")
        msgs.append("")

        return (msgs, maturo)

    # ======================================================================
    # SELL_MATURO_K2 (牝犬末路口上)
    # ======================================================================




    def _sell_maturo_k2(self, target: Character, sell_price: int) -> Tuple[List[str], str]:
        """牝犬末路口上 - sold as bitch dog.
        Returns (messages, maturo_title).
        """
        msgs: List[str] = []
        tn = target.name
        player = self._get_player()
        master_name = player.name if player else ""

        def has_talent(tid: int) -> bool:
            return int(target.talent.get(tid, 0)) == 1

        def get_abl(aid: int) -> int:
            return int(target.abl.get(aid, 0))

        maturo = ""
        is_hound = has_talent(136)

        # If 牝犬, add 50000 to sell_price
        if is_hound:
            sell_price += 50000
            msgs.append(f"已经是牝犬的{tn}可以多卖50000点。")

        if is_hound:
            # 牝犬 100万+
            if sell_price >= 1000000:
                if has_talent(75):
                    locals_name = "魔界牝犬饲养员"; local = 3
                elif get_abl(15) >= 5:
                    locals_name = "魔界牝犬训练员"; local = 2
                else:
                    locals_name = "魔界土豪"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                if has_talent(75):
                    # K2_101
                    msgs.append(f"{tn}今天也作为最高级牝犬饲养员在为让牝犬奴隶怀上幼犬而努力。")
                    msgs.append("看来她把怀上幼犬当做了至高的喜悦了，甚至买来了女奴隶来孕育幼犬。")
                    msgs.append(f"在畜舍里看着泣不成声的兽奸奴隶们和兽类做爱的样子，{tn}自慰着时不时自己也参与着兽奸，就这么过着悠然自得的生活。")
                    maturo = "最高级牝犬饲养员"
                elif get_abl(15) >= 5:
                    # K2_102
                    msgs.append(f"觉醒了兽爱性癖的{tn}、成为了致力于让其他女人也觉醒兽爱性癖的牝犬训练员。")
                    msgs.append("买下来的女奴隶，只消一个来月就把她们变成了趴在地上腰抖不止的牝犬兽奸奴隶的样子。")
                    msgs.append("最终把世界变得谁在路边进行着牝犬交配都不是什么奇怪的事似乎是她的梦想……。")
                    maturo = "最高级牝犬训练员"
                else:
                    # K2_103
                    msgs.append(f"被土豪买下作为宠物的{tn}、优雅的作为牝犬生活着。")
                    msgs.append("当有变态的客人时、必定要看她的交尾秀、来为宴会助兴的样子。")
                    msgs.append("之后更是在牝犬品评会上、多次获奖成为了让其他牝犬奴隶羡慕的榜样。")
                    maturo = "最高级牝犬奴隷"

            # 牝犬 50万+
            elif sell_price >= 500000:
                if has_talent(75):
                    locals_name = "魔界牝犬饲养员"; local = 3
                elif get_abl(15) >= 5:
                    locals_name = "魔界圆形剧场"; local = 2
                else:
                    locals_name = "魔界女富豪"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                if has_talent(75):
                    # K2_51
                    msgs.append(f"{tn}今天也作为魔族最高级母种犬孕育着幼犬。")
                    msgs.append("异种族的遗传因子交合而成的幼犬有着比魔犬更优秀的智能。")
                    msgs.append("完全无法想象它的母亲是这么一副露着高潮脸不断受孕着的毫无知性品性可言的模样……。")
                    maturo = "高级母种犬"
                elif get_abl(15) >= 5:
                    # K2_52
                    msgs.append(f"{tn}、成为了在圆形剧场表演兽奸秀的牝犬女优。")
                    msgs.append("在无数观众的目光中、她伏在地上和犬或是山羊交尾着让他们兴奋不已。")
                    msgs.append("她的门票销量已经可以说是一票难求的样子……。")
                    maturo = "高级牝犬女优"
                else:
                    # K2_53
                    msgs.append(f"被女富豪买下作为宠物的{tn}、过着淫行牝犬的生活。")
                    msgs.append(f"有施虐兴趣的女富豪对于{tn}越来越堕落的模样感到很兴奋的样子。")
                    msgs.append(f"最近在路边时不时就让{tn}开始交尾并被臭骂着她，看着这幅光景就十分开心的样子。")
                    maturo = "高级牝犬奴隶"

            # 牝犬 10万+
            elif sell_price >= 100000:
                if has_talent(75):
                    locals_name = "魔界个体饲养员"; local = 3
                elif get_abl(15) >= 5:
                    locals_name = "魔界个体经营训练员"; local = 2
                else:
                    locals_name = "魔界女兽奸狂"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                if has_talent(75):
                    # K2_11
                    msgs.append(f"{tn}作为牝犬饲养员和同伴一起致力于让牝犬奴隶孕育幼犬。")
                    msgs.append(f"对于交尾既喜欢看也喜欢做的{tn}和同伴的女调教师一起买了奴隶。")
                    msgs.append("每个月都会愉快的和同伴或是奴隶一起进行着乱交兽奸的样子。")
                    maturo = "牝犬饲养员"
                elif get_abl(15) >= 5:
                    # K2_12
                    msgs.append(f"觉醒了兽爱性癖的{tn}、成为了致力于增加兽奸狂的牝犬训练员。")
                    msgs.append("买下女奴隶、深入地将兽爱传授给她们、并公开。")
                    msgs.append("最终创办起兽奸杂志似乎是她的梦想来着……。")
                    maturo = "牝犬训练员"
                else:
                    # K2_13
                    msgs.append(f"作为女兽奸狂的朋友被买下来的{tn}、过上了愉快的牝犬生活的样子。")
                    msgs.append(f"有着共同兴趣的主人和{tn}很快就情投意合、开始同居了。")
                    msgs.append("不时亲密的把屁股并排着和大型犬一起发情……。")
                    maturo = "牝犬奴隶"

            # 牝犬 10万-
            else:
                if has_talent(75):
                    locals_name = "魔犬"; local = 3
                elif get_abl(15) >= 5:
                    locals_name = "魔界小剧场"; local = 2
                else:
                    locals_name = "魔界变态"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                if has_talent(75):
                    # K2_1
                    msgs.append(f"{tn}被拥有知性的魔犬买了下来。")
                    msgs.append("他为了繁衍自己优秀的遗传因子、渴求着最棒的母体的样子。")
                    msgs.append("可惜的是预算似乎不太够、索性双方的身体相性十分的好的样子……。")
                    maturo = "魔犬新娘"
                elif get_abl(15) >= 5:
                    # K2_2
                    msgs.append(f"{tn}、成为了在小劇場表演兽奸秀的牝犬女优。")
                    msgs.append("在无数观众的目光中、她伏在地上和犬或是山羊交尾着让他们兴奋不已。")
                    msgs.append("为了让票的销量更好一些、开始和丑陋的奇珍异兽交尾了的样子……。")
                    maturo = "牝犬女优"
                else:
                    # K2_3
                    msgs.append(f"被変態作为宠物买下的{tn}、过上了奇妙的性生活的样子。")
                    msgs.append(f"变态的奴隶主人似乎要看着{tn}和大型犬交尾的姿态才会兴奋。")
                    msgs.append(f"看着自慰着的主人、心中五味杂陈的{tn}高潮了。")
                    maturo = "牝犬"

        elif has_talent(76):
            # 非牝犬 + 淫乱
            if sell_price >= 1000000:
                locals_name = "魔界土豪"; local = 3
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_104
                msgs.append(f"被土豪买下作为宠物的{tn}、过上了淫乱的牝犬生活。")
                msgs.append("当有变态的客人时、必定要她的自慰秀或是交尾秀来为宴会助兴。")
                msgs.append("之后在牝犬品评会上、多次名列前茅成为了远近闻名的名犬。")
                maturo = "高级牝犬"
            elif sell_price >= 500000:
                locals_name = "魔界牝犬饲养员"; local = 2
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_51
                msgs.append(f"{tn}今天也作为魔族最高级母种犬孕育着幼犬。")
                msgs.append("异种族的遗传因子交合而成的幼犬有着比魔犬更优秀的智能。")
                msgs.append("完全无法想象它的母亲是这么一副露着高潮脸不断受孕着的毫无知性品性可言的模样……。")
                maturo = "母种犬"
            else:
                locals_name = "魔犬"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_1
                msgs.append(f"{tn}被拥有知性的魔犬买了下来。")
                msgs.append("他为了繁衍自己优秀的遗传因子、渴求着最棒的母体的样子。")
                msgs.append("可惜的是预算似乎不太够、索性双方的身体相性十分的好的样子……。")
                maturo = "淫乱母犬"

        else:
            # 非牝犬 + 普通
            if sell_price >= 1000000:
                locals_name = "魔界土豪"; local = 3
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_104
                msgs.append(f"被土豪买下作为宠物的{tn}、过上了淫乱的牝犬生活。")
                msgs.append("当有变态的客人时、必定要她的自慰秀或是交尾秀来为宴会助兴。")
                msgs.append("之后在牝犬品评会上、多次名列前茅成为了远近闻名的名犬。")
                maturo = "高级牝犬"
            elif sell_price >= 500000:
                locals_name = "魔界牝犬训练员"; local = 2
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_55 (missing from ERB, create appropriate text for 滥交牝犬)
                msgs.append(f"{tn}被牝犬训练员买下，成为了滥交牝犬。")
                msgs.append(f"在训练员的调教下，{tn}与各种各样的雄性动物交配着。")
                msgs.append(f"无论是什么种类的雄性，{tn}都来者不拒，成为了一只彻头彻尾的滥交牝犬。")
                maturo = "滥交牝犬"
            else:
                locals_name = "魔界变态"; local = 0
                msgs.append(f"{locals_name}买下{tn}之后………")
                msgs.append("………"); msgs.append("……"); msgs.append("…")
                # K2_3
                msgs.append(f"被変態作为宠物买下的{tn}、过上了奇妙的性生活的样子。")
                msgs.append(f"变态的奴隶主人似乎要看着{tn}和大型犬交尾的姿态才会兴奋。")
                msgs.append(f"看着自慰着的主人、心中五味杂陈的{tn}高潮了。")
                maturo = "牝犬"

        # ------------------------------------------------------------------
        # Final output: set family CSTR, TSTR, closing text
        # ------------------------------------------------------------------
        family_idx = self._search_family(target)
        if family_idx >= 0:
            self.interpreter.vars.chars[family_idx].cstr[5] = f"{maturo}{tn}"

        if not hasattr(self.interpreter.vars, 'tstr'):
            self.interpreter.vars.tstr = {}
        self.interpreter.vars.tstr[30] = f"{maturo}{tn}"

        msgs.append("")
        msgs.append(f"就这样，{master_name}和{tn}再也没有见面……")
        msgs.append("")

        return (msgs, maturo)

    # ======================================================================
    # MOD_SWITCH (MOD开关系统)
    # ======================================================================




    def _sell_maturo_market_select(self) -> int:
        """Show market selection menu and return the user's choice.
        Returns: 0=魔界黑市, 1=异族交易市场, 2=宠物市场, 999=随手卖掉
        """
        print("要卖到哪个市场？")
        print("[0] 魔界的黑市")
        print("[1] 魔界的异族交易市场")
        print("[2] 魔界的宠物市场")
        print("[999] 找什么市场？随手卖掉吧！！")
        while True:
            try:
                choice = int(input())
            except (ValueError, EOFError):
                continue
            if choice in (0, 1, 2, 999):
                return choice




    def _sell_target(self, idx: int, target: Character, estimate: Dict[str, Any]) -> bool:
        if self._is_maou_shadow(target):
            return False
        price = estimate.get("price", 0)
        if price <= 0:
            return False

        self._emit_sell_reaction(target)
        self._add_global_money(price)
        prestige_delta, prestige_message = self._apply_sell_prestige_change(target)
        self._apply_long_goodbye_after_sale(idx, target)
        self._show_sell_followup(target, price)
        self._remove_character_at(idx)
        print(prestige_message)
        if prestige_delta != 0:
            current_prestige = self._get_prestige_value()
            print(f" 当前威望值: {current_prestige}")
        return True




    def _show_sell_candidate_menu(self):
        while True:
            if self._advance_sell_candidate_menu():
                return




    def _show_sell_candidate_selection_menu(self, candidates: List[tuple[int, Character]]) -> bool:
        self._render_sell_candidate_menu(candidates)
        if not candidates:
            self._pause()
            return False

        choice = self._prompt_sell_candidate_choice()
        if choice == "100":
            return True
        return self._handle_sell_candidate_menu_choice(candidates, choice)




    def _show_sell_confirmation_menu(self, idx: int, target: Character, estimate: Dict[str, Any]) -> bool:
        self._print_sell_estimate_detail(target, estimate)
        if estimate["price"] <= 0:
            print("\nThis captive cannot be sold at the current valuation.")
            self._pause()
            return False

        print("\n [1] Confirm Sale")
        print(" [100] Back")
        confirm = self._prompt_choice_raw()
        if confirm != "1":
            return False

        if self._sell_target(idx, target, estimate):
            print(f"\n{target.name} was sold for {self._format_sell_price(estimate['price'])} pts.")
        else:
            print(f"\n{target.name} could not be sold.")
        self._pause()
        return True




    def _show_sell_estimate(self, target: Character) -> List[str]:
        lines: List[str] = []
        detail = self._build_sell_price_detail(target)
        name = target.name or "无名"
        lines.append(f"{name} 的评价明细")
        lines.append("-" * 30)
        for label, level, value in detail.get("base_additions", []):
            lines.append(f" {label} LV{level}  +{value}")
        for label, level, value in detail.get("base_penalties", []):
            level_text = f" LV{level}" if level else ""
            lines.append(f" {label}{level_text}  -{value}")
        for label, value in detail.get("multipliers", []):
            if value != 100:
                whole = value // 100
                frac = value % 100
                lines.append(f" {label} × {whole}.{frac // 10}{frac % 10}")
        if detail.get("assistant_multiplier", 100) != 100:
            val = detail["assistant_multiplier"]
            lines.append(f" 原助手 × {val // 100}.{(val % 100) // 10}{val % 10}")
        if detail.get("merchant_multiplier", 100) != 100:
            val = detail["merchant_multiplier"]
            lines.append(f" 价钱谈判 × {val // 100}.{(val % 100) // 10}{val % 10}")
        lines.append("")
        price = detail.get("price", 0)
        lines.append(f"{name}能卖出{self._format_sell_price(price)}点的样子。")
        lines.append(f"把{name}卖掉吗？")
        lines.append("  [0] - 好的")
        lines.append("  [1] - 不要")
        return lines

    # =====================================================================
    # COMF 指令 SOURCE 计算
    # =====================================================================



    def _show_sell_followup(self, target: Character, price: int):
        print("\n【卖出后的去向】")
        for option in self._get_sell_followup_market_options():
            print(f" [{option['id']}] {option['name']}")
        choice = self._prompt_choice()
        option = next((item for item in self._get_sell_followup_market_options() if str(item["id"]) == choice), None)
        if option is None:
            option = next(item for item in self._get_sell_followup_market_options() if int(item["id"]) == 999)
        for line in self._build_sell_followup_lines(target, price, str(option["kind"])):
            print(line)




    def _update_sell_flags_for_target(self, target: Character):
        submission = target.abl.get(10, 0)
        desire = target.abl.get(11, 0)
        if submission + desire < 6:
            return
        if all(target.abl.get(idx, 0) < 3 for idx in range(4)):
            return
        if submission < 4 and (target.talent.get(11, 0) or target.talent.get(12, 0)):
            return
        if desire < 4 and (target.talent.get(20, 0) or target.talent.get(32, 0) or target.talent.get(34, 0)):
            return

        sale_ready = (
            (target.abl.get(12, 0) >= 3 and target.abl.get(16, 0) >= 3)
            or (target.abl.get(17, 0) >= 3 and target.abl.get(31, 0) >= 2)
            or target.abl.get(21, 0) >= 3
            or sum(target.abl.get(idx, 0) for idx in range(4)) >= 13
            or submission >= 5
            or desire >= 5
        )
        if not sale_ready:
            return

        target.cflag[0] = max(target.cflag.get(0, 0), 1)

        assistant_ready = (
            (submission >= 3 and desire >= 3 and target.abl.get(12, 0) >= 3 and target.abl.get(0, 0) >= 3 and target.abl.get(22, 0) >= 3)
            or (submission >= 5 and desire >= 4)
        )
        if assistant_ready:
            target.cflag[0] = max(target.cflag.get(0, 0), 2)




    def show_sell(self):
        """Show sell menu"""
        self._show_sell_candidate_menu()

    def _sell_video(self):
        return self.call_erb_function('SELL_VIDEO')

    def _sell_milk(self):
        return self.call_erb_function('SELL_MILK')

    def _sell_fightmoney(self):
        return self.call_erb_function('SELL_FIGHTMONEY')

    def _sell_ex_item(self):
        return self.call_erb_function('SELL_EX_ITEM')

    def _sell_bitch(self):
        return self.call_erb_function('SELL_BITCH')





