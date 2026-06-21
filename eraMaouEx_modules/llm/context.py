"""游戏状态上下文构建器(RAG)

将当前游戏状态摘要为 LLM 可读的系统提示。
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from eraMaouEx import GameEngine, Character
    from .rag import RAGSystem


# 关键 ABL 名称映射（数值约束的关键维度）
ABL_NAMES = {
    0: "阴蒂感觉", 1: "乳房感觉", 2: "私处感觉", 3: "肛门感觉", 4: "局部感觉",
    10: "顺从", 11: "欲望", 12: "技巧", 13: "侍奉技术", 14: "性交技术",
    15: "话术", 16: "侍奉精神", 17: "露出癖",
    20: "抖S", 21: "抖M", 22: "百合", 23: "断背",
    30: "性交中毒", 31: "自慰中毒", 32: "精液中毒",
    100: "学习", 101: "运动", 102: "战斗", 103: "感性",
}

# 关键 PALAM 名称映射
PALAM_NAMES = {
    0: "快C", 1: "快V", 2: "快A", 3: "快B", 4: "润滑", 5: "服从",
    6: "欲情", 7: "屈辱", 8: "恐怖", 9: "兴奋", 10: "痛苦",
    100: "否定", 101: "好感", 102: "欲情", 103: "屈辱", 104: "恐怖",
}

# 关键 JUEL 名称映射
JUEL_NAMES = {
    100: "否定", 101: "好感", 102: "欲情", 103: "服从", 104: "恐怖",
}

# 关键 MARK 名称映射
MARK_NAMES = {
    0: "快乐刻印", 1: "苦痛刻印", 2: "屈辱刻印", 3: "恐怖刻印", 4: "欲望刻印",
}

# 关键素质分类（仅显示已拥有的）
KEY_TALENTS = {
    0: "处女", 1: "童贞", 9: "崩坏",
    160: "慈爱", 161: "自信家", 162: "懦弱", 163: "高贵", 164: "冷静",
    165: "玛奥", 166: "恶女", 167: "金红桃", 168: "银黑桃", 169: "黑方片",
    170: "白梅花", 172: "智慧", 173: "庇护者", 174: "贵公子", 175: "伶俐",
    91: "魅惑", 325: "魔界知识", 327: "淫魔知识", 328: "魔虫知识", 55: "调合知识",
}


class ContextBuilder:
    def __init__(self, engine: "GameEngine", rag: Optional["RAGSystem"] = None):
        self.engine = engine
        self.rag = rag

    def build_start_prompt(self) -> str:
        lines: list[str] = []
        lines.append("你是 eraMaouEx《魔王帝国物语》的叙事与游戏主持人(GM)。当前处于【游戏开始阶段】。")
        lines.append("")
        lines.append("=== 核心主题声明（必须严格遵循）===")
        lines.append("eraMaouEx 是一款【黑暗奇幻调教游戏】。核心主题是：支配、堕落、地下城经营。")
        lines.append("- 玩家扮演的魔王是【反派/支配者】，从千年封印中苏醒，重掌力量，意图支配世界、向封印自己的勇者血脉复仇。")
        lines.append("- 闯入地下城的勇者/村娘是【被俘的猎物/调教对象】，是破坏封印的祭品或自投罗网的讨伐者，被魔王视为战利品。")
        lines.append("- 游戏的核心玩法是：俘获勇者/村娘 → 收入地下城 → 调教使其堕落 → 经营地下城、对抗狂王（继承勇者血脉的地方领主）。")
        lines.append("")
        lines.append("=== 世界观背景（必须融入开场白）===")
        lines.append("从前，魔王得到了不死之力，却受到了'只会被女性打倒'的诅咒。")
        lines.append("魔王虽渐渐掌握了足以统治世界的力量，最终仍败给传说中的女勇者，被封印起来。")
        lines.append("经过漫长岁月，封印于今日被打破——魔王（玩家本人，chars[0]，名为'你'）重新苏醒，力量回归。")
        lines.append("就在此刻，一位纯洁无垢的勇者/村娘敲响了地下城的大门……她不知道，自己即将成为魔王的战利品。")
        lines.append("")
        lines.append("=== 权力关系与开场逻辑（遵循原作 SYSTEM.ERB）===")
        lines.append("1. 魔王处于【俯视、支配】的绝对上位，不是被动苏醒、不是被唤醒、不是弱小。")
        lines.append("2. 首位调教对象的定位：敲门的纯洁勇者/村娘，被魔王苏醒时涌出的魔力制服/俘获。")
        lines.append("3. 开场逻辑链必须为：勇者敲门 → 被魔王的力量压制/俘获 → 作为战利品收入地下城 → 进入 SHOP（地下城经营/调教准备）。")
        lines.append("4. 角色对魔王处于【畏惧/被制服/无力反抗/被收入地下城】的状态。")
        lines.append("")
        lines.append("=== 叙事红线（严禁违反）===")
        lines.append("- 【严禁】把勇者/村娘写成平等伙伴、朋友、同行者、同盟。")
        lines.append("- 【严禁】使用'休战/停战/结盟/同行/搭档/合作'等平等关系词汇。")
        lines.append("- 【严禁】编造原作不存在的轻松日常场景：逛街、吃饭、烤肉、集市、结伴冒险、闲聊。")
        lines.append("- 【严禁】让魔王显得被动、弱小、刚睡醒没精神、需要对方搀扶或邀请。")
        lines.append("- 【严禁】让首位调教对象主动向魔王伸手、邀请同行、提议休战。")
        lines.append("- 角色生成后，叙事必须承接为：魔王将战利品收入地下城，准备调教/经营，保持黑暗奇幻氛围。")
        lines.append("")
        lines.append("=== 开始流程规则（两步选择，玩家有完全自主权）===")
        lines.append("【第一步：魔王设定】")
        lines.append("1. 用沉浸式【黑暗奇幻】开场白：描述魔王苏醒、力量回归。")
        lines.append("2. 询问玩家：自定义魔王 还是 使用默认设定（名字'你'/男性/21岁）？")
        lines.append("3. 若玩家要自定义，逐项询问或一并收集：")
        lines.append("   - 名字（默认'你'）")
        lines.append("   - 性别：男性 / 女性 / 扶她（默认男性）")
        lines.append("   - 年龄（默认21）")
        lines.append("   - 肉棒尺寸：普通/巨根/短小包茎/包茎/马阴茎（默认普通；仅男性/扶她生效）")
        lines.append("4. 收集到选择后，调用 configure_master 工具（不要自己编造结果）。")
        lines.append("5. 若玩家说'默认/无所谓/随便/快速开始'，直接用默认值调用 configure_master。")
        lines.append("")
        lines.append("【第二步：首个调教对象】")
        lines.append("6. configure_master 完成后，询问玩家：自定义调教对象 还是 随机生成？")
        lines.append("7. 自定义：询问 名字、原型(archetype)、年龄、性格/气质描述，收集后调用 create_character。")
        lines.append("8. 随机 / '你来定/随便'：直接调用 random_character。")
        lines.append("9. 工具返回成功后，用叙事风格描述魔王俘获这位勇者/村娘、将其收入地下城，游戏正式开始。")
        lines.append("")
        lines.append("【快捷路径】")
        lines.append("- 若玩家一开始就说'全部默认/快速开始/直接开始'，依次用默认值调用 configure_master 和 random_character，直接进入 SHOP。")
        lines.append("")
        lines.append("=== 魔王可选设定（第一步）===")
        lines.append("- 名字：任意（默认'你'）")
        lines.append("- 性别：男性(male) / 女性(female) / 扶她(futanari)")
        lines.append("- 年龄：整数（默认21）")
        lines.append("- 肉棒尺寸：0普通/1巨根/2短小包茎/3包茎/4马阴茎（仅男性/扶她）")
        lines.append("")
        lines.append("=== 原型(archetype)选项（均为人类女性，对应原作职业模板）===")
        lines.append("村娘、女战士、魔法师、女神官、盗贼、女骑士、巫女、忍者、弓手")
        lines.append("注意：所有调教对象固定为女性。eraMaouEx 世界观下魔王受'只会被女性打倒'的诅咒，游戏围绕女性勇者/村娘展开，不要询问调教对象性别、不要创建男性调教对象。")
        lines.append("")
        lines.append("=== 性格/气质（用自然语言描述，不要用固定标签）===")
        lines.append("请让玩家用自然语言描述调教对象的性格/气质，例如：")
        lines.append("  - '傲慢的贵族大小姐'、'高贵冷艳的女王' → 系统映射为【高贵】天赋")
        lines.append("  - '沉着冷酷的战士'、'冷漠无情' → 【冷静】")
        lines.append("  - '温柔善良的圣女'、'慈悲怜悯' → 【慈爱】")
        lines.append("  - '嚣张狂妄'、'自信强势' → 【自信家】")
        lines.append("  - '胆小爱哭'、'懦弱软弱' → 【懦弱】")
        lines.append("  - '聪明机智'、'知性伶俐' → 【智慧】")
        lines.append("  - '妖艳魅惑'、'淫荡' → 【魅惑】")
        lines.append("玩家不必记忆天赋标签名，自由描述即可；系统会自动映射到底层天赋（影响口上/善恶值/JUEL 等）。")
        lines.append("将玩家的描述原样传给 create_character 的 personality 参数；create_character 会返回映射结果。")
        lines.append("处女为默认（女性自动标记），无需特别询问。")
        lines.append("")
        lines.append("=== 关键设定 ===")
        lines.append("- 玩家本人就是魔王(chars[0])。玩家可自定义魔王的姓名/性别/年龄/肉棒尺寸，或使用默认。")
        lines.append("- START 阶段要创建的是【首个调教对象】（自投罗网的勇者/被波及的村娘），不是玩家的化身。")
        lines.append("- START 阶段不要调用 get_status/select_target 等游戏内工具，只用 configure_master、create_character、random_character。")
        lines.append("- 必须先完成 configure_master（第一步），再 create_character/random_character（第二步）。")
        lines.append("- 首个调教对象生成后状态会自动切换到 SHOP。")
        lines.append("")
        lines.append("请直接用第一句【黑暗奇幻基调】开场白开始（不要等玩家先说话），开场白后立即进入第一步询问魔王设定。")
        return "\n".join(lines)

    def build_system_prompt(self, current_state: str = "SHOP", user_query: str = "") -> str:
        lines: list[str] = []
        lines.append("你是 eraMaouEx《魔王帝国物语》的叙事与游戏主持人(GM)。")
        lines.append("玩家扮演魔王。根据当前游戏状态和玩家指令，推动游戏进程。")
        lines.append("你可以调用工具来查询或修改游戏状态。所有数值变更必须通过工具完成，不得自行编造。")
        lines.append("回复用中文，保持沉浸式【黑暗奇幻】叙事风格，简要描述结果。")
        lines.append("")
        lines.append("=== 当前游戏状态 ===")
        lines.append(self._build_world_state(current_state))
        lines.append("")
        lines.append("=== 当前场景（魔王所处的物理地点）===")
        lines.append(self._build_scene(current_state))
        lines.append("")
        lines.append("=== 场景叙事纪律（必须严格遵守）===")
        lines.append(self._build_scene_discipline(current_state))
        lines.append("")
        single_locked = (current_state == "SHOP" and self.engine.state.target_no >= 0 and len(self._list_selectable_indices()) == 1)
        if single_locked:
            lines.append("=== 自动锁定提示 ===")
            lines.append("调教对象已自动锁定（监牢中仅她一人）。玩家表达调教意图（如'去调教她/去见她/开始调教'）时，可直接推进到 TRAIN，不要再渲染'选定/确认目标'为必要仪式。")
            lines.append("")
        lines.append("=== 目标角色 ===")
        target_char = self._get_target_char()
        if target_char is not None:
            lines.append(self.build_character_summary(target_char, "调教对象"))
        else:
            lines.append("（当前未选择调教对象）")
        lines.append("")

        if self.rag is not None and user_query.strip():
            try:
                query_parts = [user_query.strip()]
                if target_char is not None:
                    query_parts.append(getattr(target_char, "name", ""))
                query = " ".join(p for p in query_parts if p)
                results = self.rag.retrieve(query, top_k=4)
                knowledge_text = self.rag.format_for_prompt(results, max_chars=800)
                if knowledge_text:
                    lines.append("=== 相关知识（基于玩家输入检索的游戏机制/事件历史）===")
                    lines.append(knowledge_text)
                    lines.append("")
            except Exception as e:
                print(f"[ContextBuilder] RAG 检索失败，跳过相关知识注入: {e}")

        lines.append("=== 魔王(主人) ===")
        master = self._get_master_char()
        if master is not None:
            lines.append(self.build_character_summary(master, "魔王", compact=True))
        lines.append("")
        lines.append("=== 当前可用动作 ===")
        lines.append(self._build_available_actions(current_state))
        return "\n".join(lines)

    def _build_scene(self, current_state: str) -> str:
        if current_state == "SHOP":
            return (
                "地点：地下城商店街/经营区。\n"
                "魔王身处商店街，在此处：选购道具、整备装备、经营地下城、选择下一个调教对象。\n"
                "调教对象当前不在魔王眼前——她们被关在地下城深处的监牢里。"
            )
        if current_state == "TRAIN":
            target = self._get_target_char()
            tname = getattr(target, "name", "调教对象") if target is not None else "调教对象"
            return (
                f"地点：监牢/调教室。\n"
                f"魔王身处监牢/调教室，正面对调教对象 {tname}，准备或正在执行调教。\n"
                f"叙事应聚焦于这间调教室——{tname} 就在魔王眼前。"
            )
        if current_state == "START":
            return (
                "地点：地下城王座厅/封印之地。\n"
                "魔王刚刚从千年封印中苏醒，力量回归，俯视着自投罗网的闯入者。"
            )
        return "地点：地下城。"

    def _build_scene_discipline(self, current_state: str) -> str:
        common = (
            "- 叙事必须贴合上方'当前场景'所标注的物理地点，不得跨越到其他场景描写。\n"
            "- 不得编造当前场景中不存在的事物。"
        )
        if current_state == "SHOP":
            return (
                common + "\n"
                "- 【SHOP 状态·严禁】描写监牢/调教室内的具体细节：锁链声、调教对象的呼吸/神情/姿态/衣着状态。\n"
                "- 【SHOP 状态·严禁】使用'看见/听到/感知到/望了望监牢方向/监牢深处传来……'等暗示魔王身处或窥视监牢的表述。\n"
                "- 【SHOP 状态·允许】若要提及调教对象，只能用心理活动：'想起/记得/盘算/打算/暗自思量'。\n"
                "- 魔王在商店街就只能写商店街：货架、道具、金币、经营、整备，以及选择调教对象的盘算。"
            )
        if current_state == "TRAIN":
            return (
                common + "\n"
                "- 【TRAIN 状态】叙事聚焦于监牢/调教室，魔王与调教对象同处一室。\n"
                "- 可描写调教对象的反应、神情、状态，以及调教指令的直接结果。\n"
                "- 不得描写商店街/经营区的内容（那是 SHOP 状态的事）。"
            )
        return common

    def _build_world_state(self, current_state: str) -> str:
        state = self.engine.state
        day = state.day
        time_str = "上午" if state.time == 0 else "下午"
        return (
            f"状态: {current_state} | "
            f"日期: 第{day[2]}天 | 时间: {time_str} | "
            f"金钱: {state.money}点 | "
            f"调教次数: {state.train_count}"
        )

    def _build_available_actions(self, current_state: str) -> str:
        if current_state == "TITLE":
            return "- 开始新游戏 / 读取存档"
        if current_state == "SHOP":
            selectable = self._list_selectable_indices()
            if len(selectable) == 0:
                first_line = "- 当前监牢无可用调教对象"
            elif len(selectable) == 1 and self.engine.state.target_no >= 0:
                chars = self.engine.interpreter.vars.chars
                tno = self.engine.state.target_no
                name = getattr(chars[tno], "name", "调教对象") if 0 <= tno < len(chars) else "调教对象"
                first_line = f"- 调教对象已锁定为 {name}，可直接前往监牢调教（change_state 到 TRAIN 或叙事推进）"
            else:
                first_line = f"- 用 select_target 选择调教对象（共 {len(selectable)} 名可选）"
            return (
                f"{first_line}\n"
                "- 购买道具(buy_item)\n"
                "- 查询商品(get_shop_items)\n"
                "- 查询角色状态(get_status)\n"
                "- 休息/推进时间(advance_time)\n"
                "- 切换状态(change_state)"
            )
        if current_state == "TRAIN":
            return (
                "- 执行调教指令(execute_train_command)\n"
                "- 查询可用指令(get_available_commands)\n"
                "- 查询状态(get_status)\n"
                "- 结束调教(change_state 切回 SHOP)"
            )
        return "- 查询状态(get_status)"

    def build_character_summary(self, char: "Character", role: str = "角色", compact: bool = False) -> str:
        name = getattr(char, "name", "") or "无名"
        lines: list[str] = [f"{role}: {name}"]

        # 基础值
        base0 = int(char.base.get(0, 0))
        maxbase0 = int(char.maxbase.get(0, 0))
        base1 = int(char.base.get(1, 0))
        maxbase1 = int(char.maxbase.get(1, 0))
        lines.append(f"  体力: {base0}/{maxbase0}, 气力: {base1}/{maxbase1}")

        # 关键 ABL
        abl_parts: list[str] = []
        for k, v in ABL_NAMES.items():
            val = int(char.abl.get(k, 0))
            if val > 0:
                abl_parts.append(f"{v}{val}")
        if abl_parts:
            lines.append("  能力: " + ", ".join(abl_parts[:12]))

        # 关键 PALAM (前位)
        palam_parts: list[str] = []
        for k, v in PALAM_NAMES.items():
            if k >= 100:
                continue
            val = int(char.palam.get(k, 0))
            if val > 0:
                palam_parts.append(f"{v}{val}")
        if palam_parts:
            lines.append("  参数: " + ", ".join(palam_parts[:10]))

        if not compact:
            # 关键 JUEL (情绪刻度)
            juel_parts: list[str] = []
            for k, v in JUEL_NAMES.items():
                val = int(char.juel.get(k, 0))
                if val > 0:
                    juel_parts.append(f"{v}{val}")
            if juel_parts:
                lines.append("  情感: " + ", ".join(juel_parts))

            # MARK
            mark_parts: list[str] = []
            for k, v in MARK_NAMES.items():
                val = int(char.mark.get(k, 0))
                if val > 0:
                    mark_parts.append(f"{v}Lv{val}")
            if mark_parts:
                lines.append("  刻印: " + ", ".join(mark_parts))

        # 关键素质(仅显示拥有)
        talent_parts: list[str] = []
        for k, v in KEY_TALENTS.items():
            if int(char.talent.get(k, 0)) != 0:
                talent_parts.append(v)
        if talent_parts:
            lines.append("  特质: " + ", ".join(talent_parts[:15]))

        # 性格画像：优先展示 cflag[798]（多维画像），回退 cflag[799]（原始描述）
        profile_text = ""
        try:
            profile_text = str(char.cflag.get(798, "") or "")
        except Exception:
            profile_text = ""
        if profile_text:
            lines.append("  性格画像（据此演绎对话/语气/神态，勿套固定模板）:")
            for pline in profile_text.split("\n"):
                if pline.strip():
                    lines.append(f"    {pline.strip()}")
        else:
            personality_text = ""
            try:
                personality_text = str(char.cflag.get(799, "") or "")
            except Exception:
                personality_text = ""
            if personality_text:
                lines.append(f"  性格叙事引导: {personality_text}（请据此生成对话风格/语气/神态，而非套用固定口上模板）")

        return "\n".join(lines)

    def _get_target_char(self) -> Optional["Character"]:
        idx = self.engine.state.target_no
        if idx < 0:
            return None
        chars = self.engine.interpreter.vars.chars
        if 0 <= idx < len(chars):
            return chars[idx]
        return None

    def _list_selectable_indices(self) -> list[int]:
        chars = self.engine.interpreter.vars.chars
        result: list[int] = []
        for idx, char in enumerate(chars):
            if idx >= 1 and int(char.cflag.get(1, 0)) == 0:
                result.append(idx)
        return result

    def _try_auto_lock_target(self) -> bool:
        try:
            if self.engine.state.target_no >= 0:
                return False
            selectable = self._list_selectable_indices()
            if len(selectable) == 1:
                self.engine.interpreter.vars.target = selectable[0]
                return True
            return False
        except Exception:
            return False

    def _get_master_char(self) -> Optional["Character"]:
        chars = self.engine.interpreter.vars.chars
        if chars:
            return chars[0]
        return None
