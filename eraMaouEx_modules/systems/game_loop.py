from __future__ import annotations
"""Module for GameLoopMixin - Game loop and main flow methods"""
import os
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class GameLoopMixin:
    """Mixin providing Game loop and main flow methods"""
    def _system_init(self) -> None:
        v = self.interpreter.vars
        v.flags[26] = 232015325431115011
        v.flags[27] = 1001
        v.flags[500] = 2
        for i in range(14):
            v.flags[60 + i] = -1
        v.target = -1
        v.flags[5] = 17179934119
        v.day = [1, 1, 1, 0]
        v.itemsales[53] = 1
        for i in range(8):
            v.flags[200 + i] = 1
        v.flags[35] = 0
        v.flags[37] = 1
        current_flag8 = int(v.flags.get(8, 0))
        v.flags[8] = current_flag8 | 0b111
        v.money = 10000
        v.globals[4444] = 1234
        if len(v.chars) > 0:
            v.chars[0].cflag[451] = 21
        v.globals[99] = 70
        v.flags[400] = 0


    def _show_title(self) -> List[str]:
        lines: List[str] = []
        lines.append("═══════════════════════════════════════")
        lines.append("")
        lines.append("      eraMaouEx - 魔王帝国物语")
        lines.append("")
        lines.append("═══════════════════════════════════════")
        lines.append("")
        lines.append("  从前，魔王得到了不死之力，")
        lines.append("  他受到了只会被女性打倒的诅咒。")
        lines.append("  虽然渐渐得到了足以掌握世界的力量，")
        lines.append("  后来却败给了传说中的女勇者，被封印起来了。")
        lines.append("")
        lines.append("  经过漫长的岁月，封印被打破了！")
        lines.append("  今天，又有纯洁无垢的勇者敲响了地下城的大门……")
        lines.append("")
        lines.append("───────────────────────────────────────")
        lines.append("  [0] 开始新游戏")
        lines.append("  [1] 读取存档")
        lines.append("  [2] 设置")
        lines.append("  [3] 退出")
        lines.append("───────────────────────────────────────")
        return lines

    # =====================================================================
    # SELL_CHARA_ESTIMATE (角色估价系统)
    # Corresponds to ERB SELL_CHARA_ESTIMATE.ERB
    # =====================================================================


    def _get_train_message_a(self, target: Character, com_id: int) -> List[str]:
        """获取调教消息类型A（调教结果描写）

        ERB中 TRAIN_MESSAGE_A 在 SOURCE.ERB 之后调用，
        主要描写参数上升引起的反应和调教结果。
        查找优先级: TRAIN_MESSAGE_{com_id} → TRAIN_MESSAGE_A → Python回退
        """
        # 1. 尝试指令专用的ERB函数
        specific_func = f"TRAIN_MESSAGE_{com_id}"
        if specific_func in self.interpreter.functions:
            return self.interpreter.call_erb_function(specific_func)

        # 2. 尝试通用的 TRAIN_MESSAGE_A
        if "TRAIN_MESSAGE_A" in self.interpreter.functions:
            return self.interpreter.call_erb_function("TRAIN_MESSAGE_A")

        # 3. Python回退: 生成简单消息
        com_name = self.train_commands.get(com_id, f"指令{com_id}")
        name = target.name or "她"
        messages = [f"  ‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥"]
        palam5 = target.palam.get(5, 0)
        if palam5 >= 3000:
            messages.append(f"  {name}全身剧烈颤抖着、沉浸在绝顶的快感之中…")
        elif palam5 >= 1000:
            messages.append(f"  {name}发出了甜美的喘息声…")
        elif palam5 >= 300:
            messages.append(f"  {name}身体微微颤动着…")
        else:
            messages.append(f"  {name}似乎没有太大的反应…")
        return messages


    def _get_train_message_b(self, target: Character, com_id: int) -> List[str]:
        """获取调教消息类型B（调教情景描写）

        ERB中 TRAIN_MESSAGE_B 在各COMFxx.ERB中调用，
        主要描写"进行了怎样的调教"这一情景。
        显示顺序为 TRAIN_MESSAGE_B → TRAIN_MESSAGE_A。
        查找优先级: TRAIN_MESSAGE_{com_id} → TRAIN_MESSAGE_B → Python回退
        """
        # 1. 尝试指令专用的ERB函数
        specific_func = f"TRAIN_MESSAGE_{com_id}"
        if specific_func in self.interpreter.functions:
            return self.interpreter.call_erb_function(specific_func)

        # 2. 尝试通用的 TRAIN_MESSAGE_B
        if "TRAIN_MESSAGE_B" in self.interpreter.functions:
            return self.interpreter.call_erb_function("TRAIN_MESSAGE_B")

        # 3. Python回退: 生成简单消息
        com_name = self.train_commands.get(com_id, f"指令{com_id}")
        name = target.name or "她"
        player = self._get_player()
        player_name = player.name if player else "你"
        messages = [f"  ‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥"]
        messages.append(f"  {player_name}对{name}执行了{com_name}…")
        return messages

    # ------------------------------------------------------------------
    # 游戏主循环集成
    # ------------------------------------------------------------------


    def _game_loop(self) -> None:
        """游戏主循环 - 管理TITLE/SHOP/TRAIN/AFTERTRAIN/TURNEND状态流转

        状态说明:
        - TITLE: 标题画面 → 新游戏/读取/设置
        - SHOP: 商店阶段 → 购买物品、管理角色等
        - TRAIN: 调教阶段 → 选择并执行调教指令
        - AFTERTRAIN: 调教后处理 → 处理结果、检查结局
        - TURNEND: 回合结束 → 处理每日事件、推进时间
        """
        state = "TITLE"
        while self.running:
            if state == "TITLE":
                state = self._game_loop_title()
            elif state == "SHOP":
                state = self._game_loop_shop()
            elif state == "TRAIN":
                state = self._game_loop_train()
            elif state == "AFTERTRAIN":
                state = self._game_loop_aftertrain()
            elif state == "TURNEND":
                state = self._game_loop_turnend()
            elif state == "EXIT":
                break
            else:
                print(f"[游戏主循环] 未知状态: {state}")
                state = "TITLE"


    def _game_loop_title(self) -> str:
        """TITLE状态处理"""
        result = self.run_title()
        if result == "SHOP":
            return "SHOP"
        if result == "EXIT":
            return "EXIT"
        return "TITLE"


    def _game_loop_shop(self) -> str:
        """SHOP状态处理"""
        result = self.run_shop()
        if result == "TRAIN":
            return "TRAIN"
        if result == "LOAD":
            return "TITLE"
        if result == "EXIT":
            return "EXIT"
        return "SHOP"


    def _game_loop_train(self) -> str:
        """TRAIN状态处理"""
        target = self._get_train_menu_target()
        if target is not None:
            # 调教前事件
            for msg in self._event_beforetrain(target):
                print(msg)

        result = self.run_train()

        if result == "SHOP":
            # 调教后事件
            if target is not None:
                for msg in self._event_aftertrain(target):
                    print(msg)
            return "AFTERTRAIN"
        return result if result in ("SHOP", "EXIT") else "SHOP"


    def _game_loop_aftertrain(self) -> str:
        """AFTERTRAIN状态处理"""
        # 自动调教事件
        for msg in self._event_autotrain():
            print(msg)

        # 特殊技能检查
        target = self._get_train_menu_target()
        if target is not None:
            for msg in self._check_special_skill(target):
                print(msg)

        return "TURNEND"


    def _game_loop_turnend(self) -> str:
        """TURNEND状态处理"""
        # 回合结束事件
        for msg in self._event_turnend():
            print(msg)

        # 次日事件
        for msg in self._event_nextday():
            print(msg)

        # 次月事件
        day = self.interpreter.vars.day
        if isinstance(day, (list, tuple)) and len(day) >= 3 and day[2] == 1:
            for msg in self._event_nextmonth():
                print(msg)

        return "SHOP"

    # ------------------------------------------------------------------
    # COMABLE 指令可用性桥接
    # ------------------------------------------------------------------


    def _check_com_available(self, com_id: int, target: Character) -> bool:
        """检查指令是否可用

        查找优先级: ERB函数 COM_ABLE{com_id} → ComableSystem模块 → 默认允许
        """
        # 1. 尝试ERB函数 COM_ABLE{com_id}
        erb_func = f"COM_ABLE{com_id}"
        if erb_func in self.interpreter.functions:
            result = self.interpreter.call_erb_function(erb_func)
            # ERB中 COM_ABLE 返回1=可用, 0=不可用
            if result:
                for line in result:
                    stripped = line.strip()
                    if stripped.isdigit():
                        return int(stripped) != 0
            return True

        # 2. 使用ComableSystem模块
        player = self._get_player()
        if player is not None:
            from eraMaouEx_modules.systems.comable import ComableSystem
            if not hasattr(self, '_comable_system'):
                self._comable_system = ComableSystem(self)
            return self._comable_system.can_execute(com_id, target, player)

        # 3. 默认允许
        return True

    # ------------------------------------------------------------------
    # SHOP 主显示集成
    # ------------------------------------------------------------------

    def load_erb_files(self):
        """Load all ERB files"""
        self.interpreter.functions = {}
        self.interpreter.lines = []
        for root, dirs, files in os.walk(self.erb_dir):
            for file in files:
                if file.endswith('.ERB'):
                    filepath = os.path.join(root, file)
                    try:
                        self.interpreter.load_file(filepath)
                    except Exception as e:
                        print(f"Warning: Failed to load {filepath}: {e}")

    def analyze_erb(self):
        """Analyze and report on loaded ERB functions"""
        functions = self.interpreter.functions
        report = self._build_erb_analysis_header(functions)
        report.extend(self._build_erb_analysis_categories(functions))
        report.extend(self._build_erb_analysis_key_terms(functions))
        report.extend(self._build_erb_analysis_samples(functions))
        report.append("=" * 60)
        return "\n".join(report)

    def run_title(self):
        """Run title screen"""
        self._render_title_screen()
        choice = self._prompt_title_choice()
        return self._handle_title_choice(choice)

    def run(self):
        """Main game loop"""
        self._bootstrap_game_runtime()
        self._run_game_state_loop()
        print("\nThanks for playing eraMaouEx Python!")

    def _system_title(self):
        """标题画面 - 桥接ERB SYSTEM_TITLE"""
        return self.call_erb_function('SYSTEM_TITLE')


