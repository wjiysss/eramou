"""LLM 技能层(Skills)

提供 function-calling 风格的工具，封装现有数值系统。
LLM 通过调用这些工具来查询/修改游戏状态，所有变更受数值约束。
"""
from __future__ import annotations
import io
import json
import contextlib
from typing import TYPE_CHECKING, Any, Callable, Optional

from .context import ContextBuilder
from .personality_profile import profile_personality, to_narrative_block

if TYPE_CHECKING:
    from eraMaouEx import GameEngine, Character


class SkillRegistry:
    def __init__(self, engine: "GameEngine", context_builder: ContextBuilder, rag: Optional["RAGSystem"] = None, runtime: Optional[Any] = None):
        self.engine = engine
        self.context = context_builder
        self.rag = rag
        self.runtime = runtime
        self._handlers: dict[str, Callable[[dict[str, Any]], str]] = {
            "get_status": self._get_status,
            "get_available_commands": self._get_available_commands,
            "get_shop_items": self._get_shop_items,
            "select_target": self._select_target,
            "execute_train_command": self._execute_train_command,
            "buy_item": self._buy_item,
            "use_item": self._use_item,
            "advance_time": self._advance_time,
            "change_state": self._change_state,
            "end_train": self._end_train,
            "create_character": self._create_character,
            "random_character": self._random_character,
            "configure_master": self._configure_master,
        }

    def tool_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_status",
                    "description": "查询当前游戏状态、目标角色与魔王的数值摘要。不修改状态。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_available_commands",
                    "description": "查询当前状态(SHOP/TRAIN)下可用的调教指令或商店指令列表。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_shop_items",
                    "description": "查询当前可购买的道具列表(编号/名称/价格)。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "select_target",
                    "description": "选择调教对象。选择后状态切换为 TRAIN。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target_index": {
                                "type": "integer",
                                "description": "角色在列表中的索引(从 get_available_commands 获取)",
                            }
                        },
                        "required": ["target_index"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_train_command",
                    "description": "执行一条调教指令(如爱抚/接吻等)。需先 select_target。受角色状态约束。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command_id": {
                                "type": "integer",
                                "description": "调教指令编号(如 0=爱抚, 6=接吻)",
                            }
                        },
                        "required": ["command_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "buy_item",
                    "description": "购买道具。受金钱约束，金钱不足会失败。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {"type": "integer", "description": "道具编号"},
                            "quantity": {"type": "integer", "description": "数量(默认1)"},
                        },
                        "required": ["item_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "advance_time",
                    "description": "推进时间/结束当前回合。上午→下午→次日。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "change_state",
                    "description": "切换游戏状态机。可选: START, SHOP, TRAIN。实际写入运行时状态。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "new_state": {
                                "type": "string",
                                "enum": ["START", "SHOP", "TRAIN"],
                                "description": "目标状态",
                            }
                        },
                        "required": ["new_state"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "use_item",
                    "description": "使用已购买的道具。item_id 见 get_status 的道具清单。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_id": {"type": "string", "description": "道具ID（get_status 道具清单中的编号）"}
                        },
                        "required": ["item_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "end_train",
                    "description": "结束本轮调教，触发调教后事件并回到 SHOP 状态。建议在完成若干 execute_train_command 后调用。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "configure_master",
                    "description": "设定魔王(玩家本人,chars[0])的初始属性（仅 START 第一步可用）。根据玩家选择设置名字/性别/年龄/肉棒尺寸，对应原作 FIRST_SETTING。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "魔王名字（默认'你'）"},
                            "sex": {
                                "type": "string",
                                "enum": ["male", "female", "futanari"],
                                "description": "魔王性别：male=男性/female=女性/futanari=扶她（默认male）",
                            },
                            "age": {"type": "integer", "description": "魔王年龄（默认21）"},
                            "penis_size": {
                                "type": "integer",
                                "enum": [0, 1, 2, 3, 4],
                                "description": "肉棒尺寸（仅男性/扶她生效）：0=普通/1=巨根/2=短小包茎/3=包茎/4=马阴茎（默认0）",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_character",
                    "description": "创建首个调教对象（仅 START 第二步可用）。基于 eraMaouEx 原作职业模板生成人类女性勇者/村娘。生成后游戏正式开始，状态切换到 SHOP。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "角色名字"},
                            "archetype": {
                                "type": "string",
                                "enum": ["村娘", "女战士", "魔法师", "女神官", "盗贼", "女骑士", "巫女", "忍者", "弓手"],
                                "description": "原型/职业，对应原作模板。默认村娘。均为女性。",
                            },
                            "age": {"type": "integer", "description": "年龄(默认18-25)"},
                            "personality": {
                                "type": "string",
                                "description": "性格/气质的自由描述（如 '傲慢的贵族大小姐'、'温柔爱哭的村姑'）。系统会自动映射到对应天赋（高贵/冷静/慈爱/自信家/懦弱/智慧/魅惑）。优先用此参数。",
                            },
                            "talents": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "（可选）天赋标签或额外性格关键词，如 ['魅惑']。personality 未提供时也可从这里取性格描述。",
                            },
                        },
                        "required": ["name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "random_character",
                    "description": "随机生成一个初始角色（仅 START 状态可用）。生成后游戏正式开始，状态切换到 SHOP。",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
        ]

    def dispatch(self, name: str, args: dict[str, Any]) -> str:
        handler = self._handlers.get(name)
        if handler is None:
            return f"未知技能: {name}"
        try:
            return handler(args)
        except Exception as e:
            return f"技能 {name} 执行失败: {e}"

    # ---------------- 查询类 ----------------

    def _get_status(self, args: dict[str, Any]) -> str:
        target = self.context._get_target_char()
        master = self.context._get_master_char()
        parts: list[str] = []
        state = self.engine.state
        time_str = "上午" if state.time == 0 else "下午"
        parts.append(f"日期:第{state.day[2]}天 {time_str} | 金钱:{state.money} | 调教次数:{state.train_count}")
        if master is not None:
            parts.append(self.context.build_character_summary(master, "魔王", compact=True))
        if target is not None:
            parts.append(self.context.build_character_summary(target, "调教对象"))
        else:
            parts.append("调教对象:未选择")
        items = self.engine.interpreter.vars.items
        catalog = getattr(self.engine, "item_catalog", {})
        owned: list[tuple[Any, int, str]] = []
        for k, v in items.items():
            try:
                qty = int(v)
            except (TypeError, ValueError):
                continue
            if qty <= 0:
                continue
            if isinstance(k, str) and not k.lstrip("-").isdigit():
                continue
            entry = catalog.get(k) if isinstance(catalog, dict) else None
            name = entry.get("name", str(k)) if isinstance(entry, dict) else str(k)
            owned.append((k, qty, name))
        if owned:
            owned.sort(key=lambda x: (str(x[0])))
            lines = ["--- 已购道具（use_item 传入编号）---"]
            for k, qty, name in owned[:20]:
                lines.append(f"  [{k}] {name} ×{qty}")
            if len(owned) > 20:
                lines.append(f"  ...还有 {len(owned) - 20} 种")
            parts.append("\n".join(lines))
        assi_idx = state.assi_no
        if assi_idx is not None and assi_idx >= 0:
            chars = self.engine.interpreter.vars.chars
            if 0 <= assi_idx < len(chars):
                assi = chars[assi_idx]
                parts.append(f"助手：{getattr(assi, 'name', '?')}")
        return "\n".join(parts)

    def _get_available_commands(self, args: dict[str, Any]) -> str:
        # 根据是否有目标决定返回调教指令还是角色列表
        target = self.context._get_target_char()
        if target is None:
            return self._list_targets()
        return self._list_train_commands(target)

    def _list_targets(self) -> str:
        chars = self.engine.interpreter.vars.chars
        lines: list[str] = ["可调教对象列表(使用 select_target 选择索引):"]
        count = 0
        for idx, char in enumerate(chars):
            if idx == 0:
                continue
            if char.cflag.get(1, 0) != 0:
                continue
            name = getattr(char, "name", "") or f"角色{idx}"
            lv = char.cflag.get(9, 0)
            lines.append(f"  [{idx}] {name} (Lv{lv})")
            count += 1
        if count == 0:
            lines.append("  (暂无可调教对象)")
        return "\n".join(lines)

    _TRAIN_COMMAND_GROUPS = [
        (0, 19, "爱抚·接吻类"),
        (20, 39, "道具类"),
        (40, 59, "性交类"),
        (60, 79, "侍奉类"),
        (80, 99, "SM·特殊类"),
        (100, 10 ** 9, "触手·派生类"),
    ]

    def _list_train_commands(self, target: "Character") -> str:
        catalog = getattr(self.engine, "train_commands", {})
        if not catalog:
            return "调教指令目录未加载。"
        available_ids: list[int] = []
        for cmd_id in sorted(catalog.keys()):
            try:
                ok = self.engine._is_train_command_available(cmd_id, target)
            except Exception:
                ok = True
            if ok:
                available_ids.append(cmd_id)
        lines: list[str] = ["可用调教指令(execute_train_command 传入编号):"]
        if not available_ids:
            lines.append("  (当前无可用指令)")
            return "\n".join(lines)
        PER_GROUP_CAP = 25
        for lo, hi, label in self._TRAIN_COMMAND_GROUPS:
            group = [cid for cid in available_ids if lo <= cid <= hi]
            if not group:
                continue
            lines.append(f"【{label}】")
            head = group[:PER_GROUP_CAP]
            for cmd_id in head:
                name = catalog.get(cmd_id, f"指令{cmd_id}")
                lines.append(f"  [{cmd_id}] {name}")
            if len(group) > PER_GROUP_CAP:
                lines.append(f"  ...还有 {len(group) - PER_GROUP_CAP} 条（本组）")
        return "\n".join(lines)

    def _get_shop_items(self, args: dict[str, Any]) -> str:
        catalog = getattr(self.engine, "item_catalog", {})
        if not catalog:
            return "商品目录未加载。"
        groups = {
            "调教道具": list(range(0, 24)),
            "消耗道具": [24, 25, 26, 27, 28, 29, 30, 31, 34, 35, 37],
            "知识与强化": [38, 39, 42, 52, 53, 54, 55, 56],
        }
        lines: list[str] = ["可购买道具(buy_item 传入编号):"]
        money = self.engine.state.money
        lines.append(f"当前金钱: {money}点")
        for cat, ids in groups.items():
            lines.append(f"【{cat}】")
            for item_id in ids:
                entry = catalog.get(item_id)
                if entry is None:
                    continue
                name = entry.get("name", str(item_id)) if isinstance(entry, dict) else str(entry)
                price = entry.get("price", 0) if isinstance(entry, dict) else 0
                affordable = "✓" if money >= int(price) else "✗"
                lines.append(f"  [{item_id}] {name} ({price}点) {affordable}")
        return "\n".join(lines)

    # ---------------- 动作类 ----------------

    def _select_target(self, args: dict[str, Any]) -> str:
        idx = int(args.get("target_index", -1))
        chars = self.engine.interpreter.vars.chars
        if idx < 1 or idx >= len(chars):
            return f"无效的角色索引: {idx}。请先用 get_available_commands 查询。"
        char = chars[idx]
        if char.cflag.get(1, 0) != 0:
            return f"{getattr(char, 'name', '')} 当前不可调教。"
        self.engine.interpreter.vars.target = idx
        name = getattr(char, "name", f"角色{idx}")
        self._record_event(
            f"[第{self.engine.state.day[2]}天/SHOP] 选择了调教对象 {name}",
            {"target_index": idx, "name": name},
        )
        return f"已选择调教对象: {name}。现在可以执行调教指令。"

    def _execute_train_command(self, args: dict[str, Any]) -> str:
        cmd_id = int(args.get("command_id", -1))
        target = self.context._get_target_char()
        if target is None:
            try:
                self.context._try_auto_lock_target()
            except Exception:
                pass
            target = self.context._get_target_char()
        if target is None:
            return "未选择调教对象，请先 select_target。"
        player = self.context._get_master_char()
        try:
            available = self.engine._is_train_command_available(cmd_id, target)
        except Exception:
            available = True
        if not available:
            return f"指令 [{cmd_id}] 当前不可用(受角色状态/道具约束)。"
        catalog = getattr(self.engine, "train_commands", {})
        name = catalog.get(cmd_id, f"指令{cmd_id}")
        captured = self._capture_print(lambda: self.engine._dispatch_train_command(str(cmd_id), target, player))
        summary = self._summarize_after_train(target)
        result = f"执行调教指令 [{cmd_id}] {name}。\n"
        if captured.strip():
            result += captured.strip()[:600] + "\n"
        result += summary
        return result

    def _summarize_after_train(self, target: "Character") -> str:
        parts: list[str] = []
        base0 = int(target.base.get(0, 0))
        maxb0 = int(target.maxbase.get(0, 0))
        base1 = int(target.base.get(1, 0))
        maxb1 = int(target.maxbase.get(1, 0))
        parts.append(f"对象状态: 体力 {base0}/{maxb0}, 气力 {base1}/{maxb1}")
        palam_keys = [0, 1, 2, 3, 5, 6]
        palam_parts = []
        from .context import PALAM_NAMES
        for k in palam_keys:
            val = int(target.palam.get(k, 0))
            if val > 0 and k in PALAM_NAMES:
                palam_parts.append(f"{PALAM_NAMES[k]}{val}")
        if palam_parts:
            parts.append("参数变化: " + ", ".join(palam_parts))
        return "\n".join(parts)

    def _buy_item(self, args: dict[str, Any]) -> str:
        item_id = int(args.get("item_id", -1))
        quantity = int(args.get("quantity", 1))
        catalog = getattr(self.engine, "item_catalog", {})
        entry = catalog.get(item_id) if isinstance(catalog, dict) else None
        if entry is None:
            return f"无效的道具编号: {item_id}"
        name = entry.get("name", str(item_id)) if isinstance(entry, dict) else str(item_id)
        price = int(entry.get("price", 0)) if isinstance(entry, dict) else 0
        total = price * quantity
        money = self.engine.state.money
        if money < total:
            return f"金钱不足: {name} 需要 {total}点(单价{price}×{quantity})，当前 {money}点。"
        self.engine.state.money = money - total
        items = self.engine.interpreter.vars.items
        items[item_id] = int(items.get(item_id, 0)) + quantity
        return f"购买成功: {name} ×{quantity}，花费 {total}点，剩余金钱 {self.engine.state.money}点。"

    def _resolve_inventory_key(self, items: dict, raw_id: str) -> Optional[Any]:
        try:
            int_key = int(raw_id)
        except (ValueError, TypeError):
            int_key = None
        if int_key is not None and int(items.get(int_key, 0)) > 0:
            return int_key
        if raw_id in items and int(items.get(raw_id, 0)) > 0:
            return raw_id
        return None

    def _use_item(self, args: dict[str, Any]) -> str:
        raw_id = str(args.get("item_id", "")).strip()
        if not raw_id:
            return "use_item 失败：缺少 item_id 参数（用 get_status 查看道具清单）"
        items = self.engine.interpreter.vars.items
        key = self._resolve_inventory_key(items, raw_id)
        if key is None:
            return f"use_item 失败：未持有道具 {raw_id}（用 get_status 查看道具清单）"
        qty = int(items.get(key, 0))
        items[key] = qty - 1
        remaining = int(items.get(key, 0))
        if remaining <= 0:
            items.pop(key, None)
            remaining = 0
        catalog = getattr(self.engine, "item_catalog", {})
        entry = catalog.get(key) if isinstance(catalog, dict) else None
        disp_name = entry.get("name", str(key)) if isinstance(entry, dict) else str(key)
        master = self.context._get_master_char()
        target = self.context._get_target_char()
        owner = target if target is not None else master
        used = False
        if owner is not None:
            try:
                item_name = disp_name
                try:
                    item_name = self.engine._get_item_name(int(key))
                except Exception:
                    pass
                used = bool(self.engine._use_item(owner, item_name, 1))
            except Exception as e:
                print(f"[skills] _use_item 引擎调用失败: {e}")
        owner_name = getattr(owner, "name", "?") if owner is not None else "?"
        self._record_event(
            f"[第{self.engine.state.day[2]}天] 使用了道具 {disp_name}",
            {"item_id": str(key), "name": disp_name, "target": owner_name},
        )
        effect_note = "，效果已生效" if used else "，引擎无对应效果逻辑（供叙事）"
        return f"使用了道具 {disp_name}（剩余 {remaining}）{effect_note}。"

    def _advance_time(self, args: dict[str, Any]) -> str:
        state = self.engine.state
        old_time = state.time
        new_time = old_time + 1
        crossed_day = False
        if new_time >= 2:
            new_time = 0
            state.raw.day[2] = int(state.raw.day[2]) + 1
            crossed_day = True
        state.raw.time = new_time
        time_str = "上午" if new_time == 0 else "下午"
        summary: list[str] = []
        if crossed_day:
            try:
                msgs = self.engine._event_nextday() or []
                summary.extend(str(m) for m in msgs[:5])
            except Exception as e:
                summary.append(f"(每日结算异常: {e})")
        result = f"时间推进到第{state.day[2]}天 {time_str}。"
        if summary:
            result += "\n每日结算：\n" + "\n".join(summary)
        return result

    def _change_state(self, args: dict[str, Any]) -> str:
        new_state = str(args.get("new_state", "")).strip().upper()
        if new_state not in ("START", "SHOP", "TRAIN"):
            return f"change_state 失败：无效状态 {new_state}（允许 START/SHOP/TRAIN）"
        old_state = getattr(self.runtime, "current_state", None) if self.runtime is not None else None
        if old_state is None:
            old_state = "UNKNOWN"
        if old_state == "TRAIN" and new_state == "SHOP":
            target = self.context._get_target_char()
            if target is not None:
                try:
                    self.engine._event_aftertrain(target)
                except Exception as e:
                    print(f"[skills] aftertrain 触发失败: {e}")
        if self.runtime is not None:
            self.runtime.current_state = new_state
        return f"状态切换：{old_state} → {new_state}"

    def _end_train(self, args: dict[str, Any]) -> str:
        target = self.context._get_target_char()
        after_msgs: list[str] = []
        if target is not None:
            try:
                after_msgs = list(self.engine._event_aftertrain(target) or [])
            except Exception as e:
                after_msgs = [f"(aftertrain异常: {e})"]
        old_state = getattr(self.runtime, "current_state", "TRAIN") if self.runtime is not None else "TRAIN"
        if self.runtime is not None:
            self.runtime.current_state = "SHOP"
        result = f"结束本轮调教，返回 SHOP（{old_state} → SHOP）。\n"
        if target is not None:
            try:
                summary = self._summarize_after_train(target)
                if summary:
                    result += summary + "\n"
            except Exception as e:
                print(f"[skills] _summarize_after_train 失败: {e}")
        if after_msgs:
            result += "调教后事件：\n" + "\n".join(str(m) for m in after_msgs[:5])
        return result

    # ---------------- 角色生成 ----------------

    # archetype（原型/职业）→ eraMaouEx 原作 template_id（CSV/Chara/CharaN.csv）
    # 调教对象为人类，故不使用 DnD 种族；用职业原型对齐原作
    ARCHETYPE_MAP = {
        "村娘": 17,
        "女战士": 1,
        "魔法师": 2,
        "女神官": 3,
        "盗贼": 4,
        "女骑士": 5,
        "巫女": 6,
        "忍者": 7,
        "弓手": 8,
    }
    _RANDOM_ARCHETYPES = ["村娘", "女战士", "魔法师", "女神官", "盗贼", "女骑士", "巫女", "忍者", "弓手"]

    # eraMaouEx 风格名字池（随机生成用）
    _RANDOM_NAME_PARTS_A = ["莉", "露", "艾", "梅", "塞", "芙", "薇", "瑟", "琳", "蕾", "希", "诺", "雅", "伊", "丝"]
    _RANDOM_NAME_PARTS_B = ["莉丝", "露娜", "艾拉", "梅尔", "塞拉", "芙蕾", "薇儿", "瑟琳", "琳娜", "蕾雅", "希尔", "诺亚", "雅琳", "伊丝", "丝卡"]
    _RANDOM_TALENT_POOL = [
        ("处女", 0), ("懦弱", 162), ("慈爱", 160), ("自信家", 161), ("冷静", 164),
        ("高贵", 163), ("伶俐", 175), ("智慧", 172), ("魅惑", 91),
    ]

    def _instantiate_from_archetype(self, archetype: str) -> tuple[Any, str, int]:
        """从 archetype 加载原作模板角色，返回 (char, archetype_display, template_id)。
        模板加载失败时抛出异常，由调用方 _create_character 捕获并返回明确错误。"""
        archetype = archetype or "村娘"
        template_id = self.ARCHETYPE_MAP.get(archetype)
        used_default = False
        if template_id is None:
            template_id = 17  # 村娘玛奥
            archetype = "村娘"
            used_default = True
        char = self.engine._create_character_from_template(template_id)
        display = archetype + ("（默认）" if used_default else "")
        return char, display, template_id

    PENIS_SIZE_NAMES = {0: "普通阴茎", 1: "巨根", 2: "短小包茎", 3: "包茎", 4: "马阴茎"}

    def _configure_master(self, args: dict[str, Any]) -> str:
        master = self.context._get_master_char()
        if master is None:
            chars = self.engine.interpreter.vars.chars
            if not chars:
                return "configure_master 失败：chars 列表为空。"
            master = chars[0]

        name = str(args.get("name", "") or "").strip() or "你"
        sex = str(args.get("sex", "male") or "male").strip().lower()
        if sex not in ("male", "female", "futanari"):
            sex = "male"
        age = int(args.get("age", 0) or 0) or 21
        penis_size = int(args.get("penis_size", 0) or 0)
        if penis_size not in (0, 1, 2, 3, 4):
            penis_size = 0

        master.name = name
        master.callname = name

        # 性别映射（遵循原作 SYSTEM.ERB FIRST_SETTING 770-798）
        # talent[1]=男人? talent[122]=童贞? talent[121]=扶她? talent[100]=少年?
        master.talent[1] = 0
        master.talent[121] = 0
        master.talent[122] = 0
        master.talent[100] = 0
        if sex == "male":
            master.talent[1] = 1
            master.talent[122] = 1  # 童贞
        elif sex == "futanari":
            master.talent[1] = 1
            master.talent[121] = 1  # 扶她
        # female: 全 0

        # 肉棒尺寸（仅男性/扶她生效，对应原作 801-808）
        if sex in ("male", "futanari"):
            master.talent[318] = penis_size
        else:
            master.talent.pop(318, None)

        # 年龄
        master.cflag[451] = age
        # 保留魔王标签
        master.talent[200] = 1

        sex_display = {"male": "男性", "female": "女性", "futanari": "扶她"}[sex]
        lines = [f"已设定魔王：{name}（{sex_display}，{age}岁）。"]
        if sex in ("male", "futanari"):
            lines.append(f"肉棒尺寸：{self.PENIS_SIZE_NAMES.get(penis_size, '普通阴茎')}。")
        lines.append("魔王标签已激活（talent[200]=1）。")
        return "\n".join(lines)

    # 性格自由文本 → talent[16X] 关键词映射（保留底层机制：JUEL/ABL/善恶值/地城掉落等）
    # 互斥：一个角色只匹配一个 talent[16X]（遵循原作 CHARA_CUSTOM2.ERB）
    PERSONALITY_KEYWORD_MAP = [
        (["傲慢", "高贵", "贵族", "大小姐", "女王", "高傲", "冷艳", "贵族大小姐"], 163, "高贵"),
        (["沉着", "冷酷", "冷漠", "冷静", "无情", "冷淡", "冰山", "理性"], 164, "冷静"),
        (["温柔", "慈爱", "善良", "圣女", "怜悯", "慈悲", "包容", "仁慈"], 160, "慈爱"),
        (["嚣张", "狂妄", "自信", "强势", "霸道", "骄傲", "自大"], 161, "自信家"),
        (["胆小", "爱哭", "懦弱", "软弱", "怯弱", "羞涩", "胆怯", "内向"], 162, "懦弱"),
        (["聪明", "智慧", "伶俐", "机智", "知性", "理智", "博学", "睿智"], 172, "智慧"),
        (["妖艳", "魅惑", "淫荡", "诱惑", "狐媚", "艳丽"], 91, "魅惑"),
        (["慵懒", "倦怠", "懒散", "怠惰"], 164, "冷静"),
        (["三无", "无口", "无表情", "面瘫"], 164, "冷静"),
        (["天然呆", "迷糊", "冒失", "呆萌"], 172, "智慧"),
        (["病娇", "病み", "病态", "偏执痴恋"], 91, "魅惑"),
        (["元气", "活泼", "开朗", "热情似火"], 161, "自信家"),
        (["腹黑", "狡诈", "心机", "笑里藏刀"], 172, "智慧"),
    ]
    _PERSONALITY_TALENT_IDS = {160, 161, 162, 163, 164, 172}  # 性格口上互斥组（91 魅惑不互斥）

    def _map_personality_to_talent(self, text: str) -> tuple[int, str] | None:
        """把自由文本性格映射到 talent_id。返回 (talent_id, 天赋名) 或 None。"""
        if not text:
            return None
        text_low = text.lower()
        for keywords, tid, label in self.PERSONALITY_KEYWORD_MAP:
            for kw in keywords:
                if kw in text or kw.lower() in text_low:
                    return tid, label
        return None

    def _create_character(self, args: dict[str, Any]) -> str:
        name = str(args.get("name", "")).strip()
        if not name:
            return "create_character 失败：缺少 name 参数。"
        archetype = str(args.get("archetype", "村娘")).strip()
        age = int(args.get("age", 0)) or 0
        personality = str(args.get("personality", "") or "").strip()
        talents_req = [str(t) for t in (args.get("talents", []) or [])]

        try:
            char, archetype_display, _ = self._instantiate_from_archetype(archetype)
        except Exception as e:
            return f"create_character 失败：角色实例化异常 - {e}"
        # 覆盖名字
        char.name = name
        char.callname = name
        # eraMaouEx 世界观：调教对象固定为人类女性（魔王受"只会被女性打倒"的诅咒）
        char.talent[312] = 0  # 女性
        char.talent[314] = 0  # 人类
        # 年龄（若未指定，保留模板/默认）
        if age > 0:
            char.cflag[9] = age
        elif not char.cflag.get(9):
            char.cflag[9] = 20
        char.cflag[1] = 0  # 可用

        # 性格映射：优先 personality，其次从 talents 里找性格关键词
        personality_text = personality or " ".join(talents_req)
        mapped = self._map_personality_to_talent(personality_text)
        # 若玩家用了旧标签（如直接说"高贵"），也能识别
        if mapped is None and talents_req:
            for req in talents_req:
                m = self._map_personality_to_talent(req)
                if m is not None:
                    mapped = m
                    break
        # 清除模板自带的性格口上天赋（互斥组），只保留映射结果
        for tid in self._PERSONALITY_TALENT_IDS:
            if int(char.talent.get(tid, 0)):
                char.talent[tid] = 0
        personality_label = "冷静"  # 默认中性
        if mapped is not None:
            tid, personality_label = mapped
            char.talent[tid] = 1
        else:
            char.talent[164] = 1  # 未匹配默认冷静
        # 记录原始性格描述，供 LLM 叙事弱引导使用
        char.cflag[799] = personality or personality_label
        try:
            profile = profile_personality(personality or personality_label)
            char.cflag[798] = to_narrative_block(profile)
        except Exception as e:
            print(f"[skills] 性格画像生成失败（不影响流程）: {e}")
            char.cflag[798] = ""

        # 魅惑作为非互斥天赋，可叠加
        applied_extra: list[str] = []
        for req in talents_req:
            for keywords, tid, label in self.PERSONALITY_KEYWORD_MAP:
                if tid == 91 and label == req:
                    char.talent[91] = 1
                    if "魅惑" not in applied_extra:
                        applied_extra.append("魅惑")
                    break

        # 女性默认标记处女
        if not int(char.talent.get(0, 0)):
            char.talent[0] = 1

        # char 已由 _create_character_from_template append 到 chars 末尾，无需再次插入
        summary = self.context.build_character_summary(char, f"新角色:{name}")
        self._record_event(
            f"[第{self.engine.state.day[2]}天/START] 创建角色 {name}（{archetype}，性格:{personality_label}）",
            {"name": name, "archetype": archetype, "talent": personality_label},
        )
        return (
            f"已创建角色：{name}（原型:{archetype_display}，人类女性，{char.cflag.get(9, 20)}岁）。\n"
            f"性格：{personality or '(未描述，默认冷静)'} → 映射天赋【{personality_label}】\n"
            f"其他：处女" + (f"，{', '.join(applied_extra)}" if applied_extra else "")
            + "\n" + summary
            + "\n游戏开始，状态切换到 SHOP。"
        )

    def _random_character(self, args: dict[str, Any]) -> str:
        import random
        archetype = random.choice(self._RANDOM_ARCHETYPES)
        name = random.choice(self._RANDOM_NAME_PARTS_A) + random.choice(self._RANDOM_NAME_PARTS_B)
        age = random.randint(18, 25)
        pool = random.sample(self._RANDOM_TALENT_POOL, k=random.randint(1, 3))
        talents = [label for label, _ in pool]
        return self._create_character({
            "name": name,
            "archetype": archetype,
            "age": age,
            "talents": talents,
        })

    # ---------------- 工具 ----------------

    def _record_event(self, text: str, metadata: Optional[dict] = None) -> None:
        if self.rag is None:
            return
        try:
            self.rag.record_event(text, metadata)
        except Exception as e:
            print(f"[skills] 事件记录失败（不影响主流程）: {e}")

    def _capture_print(self, fn: Callable[[], Any]) -> str:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                fn()
            except Exception as e:
                return f"(执行中断: {e})"
        return buf.getvalue()
