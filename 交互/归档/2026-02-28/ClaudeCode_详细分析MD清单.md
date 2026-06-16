# eraMaouEx 详细分析 MD 清单（供 Claude Code 执行）

更新时间：2026-02-28

## 任务执行状态

| 优先级 | 任务 | 状态 | 完成日期 |
|--------|------|------|----------|
| P0 | 01_项目入口与主循环 | ✅ 已完成 | 2026-02-28 |
| P0 | 02_回合与事件驱动 | ✅ 已完成 | 2026-02-28 |
| P0 | 03_调教指令系统 | ✅ 已完成 | 2026-02-28 |
| P0 | 04_角色属性与成长 | ✅ 已完成 | 2026-02-28 |
| P1 | 05_侵略与战斗系统 | ✅ 已完成 | 2026-02-28 |
| P1 | 06_地城探索系统 | ✅ 已完成 | 2026-02-28 |
| P1 | 07_商店经济与处刑售卖 | ✅ 已完成 | 2026-02-28 |
| P1 | 08_数据表与资源映射 | ✅ 已完成 | 2026-02-28 |
| P2 | 09_MOD扩展与兼容性 | ✅ 已完成 | 2026-02-28 |
| P2 | 10_补丁历史与版本演化 | ✅ 已完成 | 2026-02-28 |

**执行者：Claude Code**
**总任务数：10**
**已完成：10**
**完成率：100%**

---

## 一、快速结构分析（简版）
- 项目核心不是 Markdown，而是脚本与数据：
- `ERB/`：329 个文件（核心逻辑，含 `COMF*`、`EVENT*`、`DUNGEON*`、`SHOP*`、`侵略/`、`MOD/`）
- `CSV/`：60 个文件（数值、文本、角色数据）
- `資料/`：225 个文件（补丁历史、说明、许可证等文本资料）
- `resources/`：8 个文件（图片与 `img.csv`）
- 根目录现有 `md` 仅 `README.md`，内容很少，且有编码异常

## 二、执行约束（给 Claude Code）
1. 按下表顺序执行，先 `P0` 后 `P1` 再 `P2`。
2. 每个任务输出一个独立 `md` 到 `F:\code\eraMaouEx\交互\`。
3. 每个输出 `md` 最少包含：
- 功能概述
- 关键文件清单
- 关键流程（按“输入 -> 条件 -> 结果”）
- 关键变量/标志位（若可识别）
- 与其他模块的调用关系
- 未确认问题（TODO）
4. 若遇到编码异常，先保留原文并给出“推测含义”。

## 三、需要详细分析的 MD 清单
| 优先级 | 输出文件（写入路径） | 详细阅读范围 | 本任务重点 |
|---|---|---|---|
| P0 | `F:\code\eraMaouEx\交互\01_项目入口与主循环.md` | `README.md`、`修改內容.txt`、`整合内容菜单.txt`、`ERB/TITLE.ERB`、`ERB/_DRAW_MAINMENU.ERB`、`ERB/SYSTEM*.ERB`、`ERB/SYSTEM_MODEINT.ERB` | 启动入口、主菜单、系统主循环和模式切换 |
| P0 | `F:\code\eraMaouEx\交互\02_回合与事件驱动.md` | `ERB/EVENT_TURNEND.ERB`、`ERB/EVENT_NEXTDAY.ERB`、`ERB/EVENT_NEXTMONTH.ERB`、`ERB/EVENT_SABBATH.ERB`、`ERB/EVENT_BEFORETRAIN.ERB`、`ERB/EVENT_AFTERTRAIN.ERB`、`ERB/EVENT_AUTOTRAIN.ERB` | 时间推进、回合结束钩子、日/月事件触发关系 |
| P0 | `F:\code\eraMaouEx\交互\03_调教指令系统_COMF.md` | `ERB/COMABLE.ERB`、`ERB/COM_REGISTER.ERB`、`ERB/_DRAW_EXT_COMM.ERB`、`ERB/COMF*.ERB` | 指令注册、可用性判定、执行后状态变化 |
| P0 | `F:\code\eraMaouEx\交互\04_角色属性与成长.md` | `ERB/ABL.ERB`、`ERB/ABLUP*.ERB`、`ERB/CHARA*.ERB`、`ERB/CHAR_MAKE.ERB`、`ERB/CHAR_ST.ERB`、`ERB/LVUP.ERB`、`ERB/RELATION*.ERB`、`CSV/Abl.csv`、`CSV/Talent.csv`、`CSV/Palam.csv`、`CSV/exp.csv` | 角色创建、属性成长、关系与状态系统 |
| P1 | `F:\code\eraMaouEx\交互\05_侵略与战斗系统.md` | `ERB/侵略/**`（含 `AGENT/`、`CAMPAIGN/`）、`ERB/GROUP_BATTLE.ERB`、`ERB/ENTER_ENEMY.ERB` | 侵略流程、战斗调用链、阵营与事件联动 |
| P1 | `F:\code\eraMaouEx\交互\06_地城探索系统.md` | `ERB/DUNGEON*.ERB`、`ERB/LABO*.ERB`、`ERB/SUMMON_MONSTER.ERB`、`ERB/MONSTER_*.ERB` | 地城地图、遭遇、战斗、结算与特殊事件 |
| P1 | `F:\code\eraMaouEx\交互\07_商店经济与处刑售卖.md` | `ERB/SHOP*.ERB`、`ERB/SELL*.ERB`、`ERB/TAX.ERB`、`ERB/EXECUTION.ERB`、`ERB/PUBLIC_EXECUTION.ERB`、`ERB/MOD/MAKAIGINKOU v2.03v1/*` | 经济循环、物品/角色售卖、处刑收益与银行扩展 |
| P1 | `F:\code\eraMaouEx\交互\08_数据表与资源映射.md` | `CSV/*.csv`、`CSV/Chara/*.csv`、`CSV/_replace.csv`、`CSV/Str.csv`、`resources/img.csv` | 数据字典、ID/文本映射、资源引用关系 |
| P2 | `F:\code\eraMaouEx\交互\09_MOD扩展与兼容性.md` | `ERB/MOD/**`（`MOD_SWITCH.ERB`、`SYSTEM_DEBUG_Universal_era.ERB`、`PartTimeJob/PTJ.ERB` 等） | MOD 开关点、兼容风险、调试入口 |
| P2 | `F:\code\eraMaouEx\交互\10_补丁历史与版本演化.md` | `資料/パッチREADME/**`、`資料/readme*.txt`、`資料/Emuera_readme*.txt`、`資料/ライセンス/**`、根目录 `.txt` | 补丁时间线、功能来源、可能影响到的脚本模块 |

## 四、建议执行顺序（直接可用）
1. 先完成 `01` 到 `04`，建立主框架。
2. 再完成 `05` 到 `08`，补足主要玩法与数据层。
3. 最后完成 `09` 到 `10`，做扩展与历史追溯。

