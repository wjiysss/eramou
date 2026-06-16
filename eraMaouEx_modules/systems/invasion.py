from __future__ import annotations
"""Module for InvasionMixin - Invasion and battle methods"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class InvasionMixin:
    """Mixin providing Invasion and battle methods"""
    def _invasion_main(self) -> List[str]:
        """Main invasion processing.

        Handles territory invasion with different areas (human world, elf
        domain, dragon mountain, heaven, divine palace) and invasion types
        (monster army, demon lord magic, hero dispatch, plunder).
        """
        lines: List[str] = []
        v = self.interpreter.vars

        # Area and depth tracking
        # FLAG:81 = human world, FLAG:86 = elf, FLAG:88 = dragon, FLAG:90 = heaven
        # EX_FLAG:101 = divine palace
        area_flags = {
            0: (81, 82, "地上的魔界领土"),
            1: (86, 87, "精灵族的领域"),
            2: (88, 89, "龙之山脉"),
            3: (90, 91, "天界"),
            5: (101, 102, "天神宫"),
        }

        # Count monsters
        mon_num = 0
        for i in range(100, 190):
            count = int(v.get_var(f"ITEM:{i}", 0))
            if count > 0:
                mon_num += count

        # Default area
        area = 81
        sindo = 82

        # Invasion type processing
        inv_type = 0  # Default: monster invasion
        sinkou = 0

        if inv_type == 0:
            # Monster invasion
            for i in range(100, 190):
                mon_id = i
                mon_count = int(v.get_var(f"ITEM:{mon_id}", 0))
                if mon_count < 1:
                    continue
                # Monster attack power calculation
                atk = int(v.get_array("E", 2, 0)) + int(v.get_array("E", 3, 0)) + int(v.get_array("E", 4, 0))
                mon_count //= 2
                sinkou += atk * ((mon_count // 9) + 1)
            sinkou //= 20

            # Prestige modifier
            prestige = int(v.get_var("EX_FLAG:99", 50))
            if prestige <= 20:
                lines.append("威望值是【岌岌可危】")
                sinkou = 0
                lines.append("侵攻失败")
                return lines
            elif prestige <= 40:
                lines.append("威望值是【动荡不安】")
                sinkou //= 4
            elif prestige <= 60:
                lines.append("威望值是【略受质疑】")
                sinkou = sinkou * (100 + (prestige - 60) * 2) // 100
            elif prestige <= 80:
                lines.append("威望值是【相安无事】")
            else:
                lines.append("威望值是【广受爱戴】")
                sinkou = sinkou * (100 + (prestige - 80)) // 100

            lines.append(f"怪物的战斗力　{sinkou}点")

        elif inv_type == 1:
            # Demon lord magic
            mp = int(v.get_array("BASE", 0, 1, 0))
            sinkou = mp // 25
            v.set_array("BASE", 0, 1, mp // 2)
            lines.append(f"战斗力　{sinkou}点")

        elif inv_type == 2:
            # Hero dispatch
            lines.append("派遣勇者去侵攻……")
            sinkou = random.randint(100, 500)

        elif inv_type == 3:
            # Plunder
            lines.append("派遣勇者前去掠夺资金……")
            sinkou = random.randint(50, 300)

        # Apply invasion progress
        if area in (81, 86, 88, 90):
            current = int(v.get_var(f"FLAG:{area}", 0))
            new_val = min(current + sinkou, 10000)
            v.set_var(f"FLAG:{area}", new_val)
            lines.append(f"侵攻度变为{new_val}")
        elif area == 101:
            current = int(v.get_var("EX_FLAG:101", 0))
            new_val = min(current + sinkou, 10000)
            v.set_var("EX_FLAG:101", new_val)
            lines.append(f"侵攻度变为{new_val}")

        # Income from invasion
        if sinkou > 0:
            income = sinkou // 10
            v.set_var("MONEY", int(v.get_var("MONEY", 0)) + income)
            lines.append(f"获得了资金{income}")

        # Check for invasion events
        lines.extend(self._invasion_event())

        return lines


    def _invasion_event(self) -> List[str]:
        """Invasion events triggered by invasion progress thresholds.

        Events fire at 2000, 4000, 6000, 8000, 10000 invasion progress.
        Can also trigger recapture events when progress drops.
        """
        lines: List[str] = []
        v = self.interpreter.vars

        # Area event data: (area_flag, event_flag, area_name, events)
        area_data = [
            (81, 93, "人间界", [
                (2000, 0, "占领了村庄", 1),
                (4000, 1, "占领了港口", 2),
                (6000, 2, "攻陷了堡垒", 3),
                (8000, 3, "占领了街道", 4),
                (10000, 4, "占领了城市", 5),
            ]),
            (86, 94, "精灵族的领域", [
                (2000, 0, "侵入了精灵森林", 1),
                (4000, 1, "攻陷了精灵村落", 2),
                (6000, 2, "占领了精灵王庭", 3),
                (8000, 3, "征服了精灵圣地", 4),
                (10000, 4, "完全征服了精灵族", 5),
            ]),
            (88, 95, "龙之山脉", [
                (2000, 0, "侵入了龙之山脉", 1),
                (4000, 1, "攻陷了龙巢", 2),
                (6000, 2, "占领了龙之圣域", 3),
                (8000, 3, "征服了龙之山巅", 4),
                (10000, 4, "完全征服了龙族", 5),
            ]),
            (90, 96, "天界", [
                (2000, 0, "侵入了天界", 1),
                (4000, 1, "攻陷了天使之城", 2),
                (6000, 2, "占领了天界神殿", 3),
                (8000, 3, "征服了天界圣域", 4),
                (10000, 4, "完全征服了天界", 5),
            ]),
        ]

        for area_flag, event_flag, area_name, events in area_data:
            progress = int(v.get_var(f"FLAG:{area_flag}", 0))
            event_state = int(v.get_var(f"FLAG:{event_flag}", 0))

            for threshold, req_state, desc, new_state in events:
                if progress >= threshold and event_state == req_state:
                    lines.append("=" * 60)
                    lines.append(f"  {desc}")
                    lines.append("=" * 60)
                    v.set_var(f"FLAG:{event_flag}", new_state)
                    break

            # Recapture events (human world only)
            if area_flag == 81:
                recapture_events = [
                    (500, 1, "人间界的军队夺回了据点", 0),
                    (2000, 2, "人间界的军队夺回了据点", 1),
                    (4000, 3, "人间界的军队夺回了据点", 2),
                    (6000, 4, "人间界的军队夺回了据点", 3),
                    (8000, 5, "人间界的军队夺回了据点", 4),
                ]
                for threshold, req_state, desc, new_state in recapture_events:
                    if progress <= threshold and event_state == req_state:
                        lines.append("=" * 60)
                        lines.append(f"  {desc}")
                        lines.append("=" * 60)
                        v.set_var(f"FLAG:{event_flag}", new_state)
                        break

        return lines


    def _invasion_ryouzyoku(self, target: Character) -> List[str]:
        """Invasion violation events.

        Processes violation during territory invasion with different
        enemy types and area-specific victim descriptions.
        """
        lines: List[str] = []
        v = self.interpreter.vars

        # Invasion point adjustment (0-10 range)
        inv_point = int(v.get_var("FLAG:81", 0)) // 5000

        # Area-specific victim names
        area_victims = {
            1: ("看板娘", "女骑士", "少女"),
            2: ("精灵少女", "精灵猎手", "精灵少女"),
            3: ("看板娘", "龙族女战士", "龙族少女"),
            4: ("天使", "破邪天使", "妙龄天使"),
            5: ("十字军", "十字军队长", "十字军军官"),
        }

        # Process 3 violation rounds
        for i in range(3):
            # Generate random monster
            mon_id = (random.randint(1, 9)) * 10 + 100 + random.randint(0, 4)
            ryou_type = random.randint(1, 12)

            lines.append(f"怪物ID{mon_id}的凌辱开始了。")

            # Area selection (default to human world)
            area = 1
            victims = area_victims.get(area, area_victims[1])

            # Branch by violation type
            if ryou_type == 1:
                # Orc invasion violation
                roll = random.randint(0, 4)
                if roll == 0 and inv_point > 1:
                    lines.append(f"被亚人群所包围的{victims[1]}的部队、被迫做出了决断")
                    lines.append("『已经无法再期待救援了……』")
                elif roll == 1:
                    lines.append(f"{victims[1]}的抵抗是如此地无力")
                    if inv_point > 6:
                        lines.append("亚人军队的攻势排山倒海")
                    elif inv_point > 2:
                        lines.append(f"{victims[1]}的部队寡不敌众")
                    lines.append("身体因为妊娠促进剂而受胎，肚子夸张地膨胀着。")
                elif roll == 2:
                    lines.append(f"兽人们冲入面包店，把里面的{victims[0]}抓住")
                    lines.append(f"{victims[0]}的私处内被灌满了兽人的浓厚精液。")
                elif roll == 3:
                    lines.append(f"{victims[1]}在广场上被公开处刑。")
                    lines.append("脖子和手腕被固定的枷锁死死扣住")
                else:
                    lines.append(f"作为新的奴隶的{victims[2]}，被带入奴隶的帐篷中")
                    lines.append("大量被锁着，两眼无神的全裸女人正在不停地侍奉着兽人")

            elif ryou_type == 2:
                # Slime invasion violation
                lines.append(f"粘液状的生物覆盖了{victims[0]}的身体……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[20] = int(target.exp.get(20, 0)) + 1

            elif ryou_type == 3:
                # Insect invasion violation
                lines.append(f"虫群爬满了{victims[0]}的身体……")
                target.juel[10] = int(target.juel.get(10, 0)) + 10

            elif ryou_type == 4:
                # Ivy invasion violation
                lines.append(f"藤蔓触手缠绕住了{victims[0]}……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[1] = int(target.exp.get(1, 0)) + 1

            elif ryou_type == 5:
                # Tentacle invasion violation
                lines.append(f"触手抓住了{victims[0]}……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[20] = int(target.exp.get(20, 0)) + 1

            elif ryou_type == 6:
                # Fairy invasion violation
                lines.append(f"妖精们对{victims[0]}施加了恶作剧……")

            elif ryou_type == 7:
                # Giant invasion violation
                lines.append(f"巨人将{victims[1]}握在手中……")
                target.juel[9] = int(target.juel.get(9, 0)) + 15

            elif ryou_type == 8:
                # Man invasion violation
                lines.append(f"男人们围住了{victims[0]}……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[20] = int(target.exp.get(20, 0)) + 1

            elif ryou_type == 9:
                # Girl invasion violation
                lines.append(f"女人们围住了{victims[0]}……")
                target.juel[8] = int(target.juel.get(8, 0)) + 10

            elif ryou_type == 10:
                # Beast invasion violation
                lines.append(f"野兽扑向了{victims[0]}……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[20] = int(target.exp.get(20, 0)) + 1

            elif ryou_type == 11:
                # Brain invasion violation
                lines.append(f"某种力量侵入了{victims[0]}的大脑……")
                target.juel[5] = int(target.juel.get(5, 0)) + 15

            elif ryou_type == 12:
                # Horse invasion violation
                lines.append(f"马型生物对{victims[0]}施加了暴行……")
                target.exp[0] = int(target.exp.get(0, 0)) + 1
                target.exp[1] = int(target.exp.get(1, 0)) + 1
                target.exp[20] = int(target.exp.get(20, 0)) + 1

            lines.append("")

        return lines


    def _arcana_battle(self, attacker: int, defender: int) -> Dict[str, int]:
        """Arcana battle - one-on-one duel between hero and holy knight.

        Runs up to 20 turns of combat with speed-based initiative,
        talent bonuses, and equipment effects.
        """
        v = self.interpreter.vars
        result: Dict[str, int] = {"winner": 0, "turns": 0}

        # Initialize ammo
        v.set_array("CFLAG", attacker, 571, 15)
        v.set_array("CFLAG", defender, 571, 15)

        # Preemptive strikes
        atk_preempt = int(v.get_array("TALENT", attacker, 252, 0))
        def_preempt = int(v.get_array("TALENT", defender, 252, 0))

        if atk_preempt:
            def_hp = int(v.get_array("BASE", defender, 0, 0))
            damage = random.randint(10, 30)
            v.set_array("BASE", defender, 0, max(0, def_hp - damage))

        if def_preempt:
            atk_hp = int(v.get_array("BASE", attacker, 0, 0))
            damage = random.randint(10, 30)
            v.set_array("BASE", attacker, 0, max(0, atk_hp - damage))

        # Main battle loop
        for turn in range(20):
            result["turns"] = turn + 1

            atk_hp = int(v.get_array("BASE", attacker, 0, 0))
            atk_mp = int(v.get_array("BASE", attacker, 1, 0))
            def_hp = int(v.get_array("BASE", defender, 0, 0))
            def_mp = int(v.get_array("BASE", defender, 1, 0))

            # Flee check after turn 15
            if turn > 15:
                v.set_array("BASE", attacker, 1, atk_mp - random.randint(0, 30))
                break

            # Speed calculation
            atk_speed = random.randint(0, 5)
            def_speed = random.randint(0, 5)

            # Speed bonuses from talents
            if int(v.get_array("TALENT", attacker, 243, 0)):  # Ambush
                atk_speed += 1
            if int(v.get_array("TALENT", attacker, 245, 0)):  # Demon wings
                atk_speed += 1
            if int(v.get_array("TALENT", attacker, 258, 0)):  # Swift
                atk_speed += 1
            if int(v.get_array("TALENT", defender, 243, 0)):
                def_speed += 1
            if int(v.get_array("TALENT", defender, 245, 0)):
                def_speed += 1
            if int(v.get_array("TALENT", defender, 258, 0)):
                def_speed += 1

            # Combat stats
            atk_atk = int(v.get_array("CFLAG", attacker, 11, 0))
            atk_def = int(v.get_array("CFLAG", attacker, 12, 0))
            def_atk = int(v.get_array("CFLAG", defender, 11, 0))
            def_def = int(v.get_array("CFLAG", defender, 12, 0))

            if atk_speed >= def_speed:
                # Attacker goes first
                damage = max(1, atk_atk - def_def // 2 + random.randint(-10, 10))
                v.set_array("BASE", defender, 0, max(0, def_hp - damage))
                def_hp = max(0, def_hp - damage)

                if def_hp > 0:
                    damage = max(1, def_atk - atk_def // 2 + random.randint(-10, 10))
                    v.set_array("BASE", attacker, 0, max(0, atk_hp - damage))
                    atk_hp = max(0, atk_hp - damage)
            else:
                # Defender goes first
                damage = max(1, def_atk - atk_def // 2 + random.randint(-10, 10))
                v.set_array("BASE", attacker, 0, max(0, atk_hp - damage))
                atk_hp = max(0, atk_hp - damage)

                if atk_hp > 0:
                    damage = max(1, atk_atk - def_def // 2 + random.randint(-10, 10))
                    v.set_array("BASE", defender, 0, max(0, def_hp - damage))
                    def_hp = max(0, def_hp - damage)

            # MP drain
            v.set_array("BASE", attacker, 1, max(0, atk_mp - random.randint(0, 20)))
            v.set_array("BASE", defender, 1, max(0, def_mp - random.randint(0, 20)))

            # Death check
            if atk_hp <= 0 or atk_mp <= 0:
                result["winner"] = 2  # Defender wins
                break
            if def_hp <= 0 or def_mp <= 0:
                result["winner"] = 1  # Attacker wins
                break

        # Equipment restoration
        atk_max_mp = max(1, int(v.get_array("MAXBASE", attacker, 1, 0)))
        atk_mp_ratio = int(v.get_array("BASE", attacker, 1, 0)) * 100 // atk_max_mp
        if atk_mp_ratio <= 40 and int(v.get_array("TALENT", attacker, 249, 0)):  # Iron wall
            v.set_array("CFLAG", attacker, 11,
                        int(v.get_array("CFLAG", attacker, 11, 0)) + int(v.get_array("CFLAG", attacker, 9, 0)))
            v.set_array("CFLAG", attacker, 12,
                        int(v.get_array("CFLAG", attacker, 12, 0)) + int(v.get_array("CFLAG", attacker, 9, 0)))

        def_max_mp = max(1, int(v.get_array("MAXBASE", defender, 1, 0)))
        def_mp_ratio = int(v.get_array("BASE", defender, 1, 0)) * 100 // def_max_mp
        if def_mp_ratio <= 40 and int(v.get_array("TALENT", defender, 249, 0)):
            v.set_array("CFLAG", defender, 11,
                        int(v.get_array("CFLAG", defender, 11, 0)) + int(v.get_array("CFLAG", defender, 9, 0)))
            v.set_array("CFLAG", defender, 12,
                        int(v.get_array("CFLAG", defender, 12, 0)) + int(v.get_array("CFLAG", defender, 9, 0)))

        return result


    def _arcana_fort(self, area: int) -> Dict[str, int]:
        """Fort battle against holy knights.

        FLAG:92 tracks fort conquest progress (bit flags for E/S/W/N).
        Each direction has a holy knight that must be defeated.
        """
        v = self.interpreter.vars
        result: Dict[str, int] = {"conquered": 0, "direction": area}

        fort_state = int(v.get_var("FLAG:92", 0))

        # Direction bit flags: E=1, S=2, W=4, N=8
        direction_bits = {0: 1, 1: 4, 2: 2, 3: 8}
        direction_names = {0: "东方", 1: "西方", 2: "南方", 3: "北方"}
        knight_names = {0: "黑方片", 1: "白梅花", 2: "银黑桃", 3: "金红桃"}

        if area not in direction_bits:
            return result

        bit = direction_bits[area]

        # Already conquered
        if fort_state & bit:
            result["conquered"] = 2  # Already conquered
            return result

        # Find eligible attacker (assistant with love/lust talent)
        attacker = -1
        chara_num = int(v.get_var("CHARANUM", 0))
        for i in range(1, max(chara_num, 1)):
            role = int(v.get_array("CFLAG", i, 1, 0))
            ownership = int(v.get_array("CFLAG", i, 0, 0))
            love = int(v.get_array("TALENT", i, 85, 0))
            lust = int(v.get_array("TALENT", i, 76, 0))
            if (role in (0, 7)) and (love or lust) and ownership == 2:
                attacker = i
                break

        if attacker < 0:
            result["conquered"] = -1  # No eligible attacker
            return result

        # Simulate battle (simplified)
        knight_level = 15 + area * 5
        knight_atk = 20 + area * 10
        knight_def = 25 + area * 8

        atk_power = int(v.get_array("CFLAG", attacker, 11, 0)) + int(v.get_array("CFLAG", attacker, 12, 0)) // 2

        # Battle outcome based on power comparison with randomness
        win_chance = min(90, max(10, atk_power * 100 // max(1, knight_atk + knight_def)))

        if random.randint(0, 100) < win_chance:
            # Victory
            result["conquered"] = 1
            v.set_var("FLAG:92", fort_state | bit)
        else:
            # Defeat
            result["conquered"] = 0
            mp = int(v.get_array("BASE", attacker, 1, 0))
            v.set_array("BASE", attacker, 1, max(0, mp - random.randint(30, 60)))

        return result


    def _group_battle(self, side_a: List[int], side_b: List[int]) -> Dict[str, int]:
        """Group battle between two parties.

        Each side has up to 3 members. Combat runs in rounds with
        random attack order. Battle ends when one side is wiped out.
        """
        v = self.interpreter.vars
        result: Dict[str, int] = {"winner": 0, "rounds": 0}

        # Preemptive strikes
        for member in side_a:
            if member <= 0:
                continue
            if int(v.get_array("TALENT", member, 252, 0)):  # Preemptive
                for enemy in side_b:
                    if enemy <= 0:
                        continue
                    hp = int(v.get_array("BASE", enemy, 0, 0))
                    if hp > 0:
                        damage = random.randint(5, 15)
                        v.set_array("BASE", enemy, 0, max(0, hp - damage))
                        break

        # Main combat loop
        for turn in range(99):
            result["rounds"] = turn + 1

            # Check side A alive
            a_alive = False
            for m in side_a:
                if m > 0 and int(v.get_array("BASE", m, 0, 0)) > 0:
                    a_alive = True
                    break

            # Check side B alive
            b_alive = False
            for m in side_b:
                if m > 0 and int(v.get_array("BASE", m, 0, 0)) > 0:
                    b_alive = True
                    break

            if not a_alive:
                result["winner"] = 2  # Side B wins
                break
            if not b_alive:
                result["winner"] = 1  # Side A wins
                break

            # Random attack order
            attacker_idx = random.randint(0, len(side_a) - 1)
            attacker = side_a[attacker_idx]
            if attacker <= 0 or int(v.get_array("BASE", attacker, 0, 0)) <= 0:
                continue

            # Pick random alive defender
            alive_defenders = [m for m in side_b if m > 0 and int(v.get_array("BASE", m, 0, 0)) > 0]
            if not alive_defenders:
                result["winner"] = 1
                break
            defender = random.choice(alive_defenders)

            # Calculate damage
            atk_stat = int(v.get_array("CFLAG", attacker, 11, 0))
            def_stat = int(v.get_array("CFLAG", defender, 12, 0))
            damage = max(1, atk_stat - def_stat // 2 + random.randint(-5, 10))

            def_hp = int(v.get_array("BASE", defender, 0, 0))
            v.set_array("BASE", defender, 0, max(0, def_hp - damage))

            # Counter attack
            if int(v.get_array("BASE", defender, 0, 0)) > 0:
                counter_damage = max(1, int(v.get_array("CFLAG", defender, 11, 0)) -
                                     int(v.get_array("CFLAG", attacker, 12, 0)) // 2 +
                                     random.randint(-5, 5))
                atk_hp = int(v.get_array("BASE", attacker, 0, 0))
                v.set_array("BASE", attacker, 0, max(0, atk_hp - counter_damage))

            # MP drain for all participants
            for m in side_a + side_b:
                if m > 0:
                    mp = int(v.get_array("BASE", m, 1, 0))
                    v.set_array("BASE", m, 1, max(0, mp - random.randint(0, 5)))

        return result

    # -------------------------------------------------
    # ABLUP functions: calculate cost to upgrade abilities
    # -------------------------------------------------


