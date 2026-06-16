---
task_id: 03
owner: ClaudeCode
status: done
source_scope: F:\code\eraMaouEx\ERB\COMABLE.ERB, F:\code\eraMaouEx\ERB\COM_REGISTER.ERB, F:\code\eraMaouEx\ERB\_DRAW_EXT_COMM.ERB, F:\code\eraMaouEx\ERB\COMF20_正常位.ERB
updated_at: 2026-02-28 16:00
---

# 03_调教指令系统_COMF

## 功能概述

调教指令系统是 eraMaouEx 的核心玩法系统，负责管理所有调教相关指令的**可用性判定**、**执行处理**和**菜单显示**。

系统包含：
- **可用性判定**：`@COM_ABLE` 系列函数
- **指令执行**：`@COMxxx` 系列函数（xxx=指令编号）
- **指令注册**：调教菜单自定义系统

---

## 关键文件清单

| 文件路径 | 功能说明 |
|---------|----------|
| `F:\code\eraMaouEx\ERB\COMABLE.ERB` | 指令可用性判定函数集合 |
| `F:\code\eraMaouEx\ERB\COM_REGISTER.ERB` | 调教菜单自定义系统 |
| `F:\code\eraMaouEx\ERB\_DRAW_EXT_COMM.ERB` | UI 辅助函数（菜单按钮、颜色条） |
| `F:\code\eraMaouEx\ERB\COMF*.ERB` | 各指令的具体执行逻辑（约200+文件） |

---

## 关键流程分析

### 1. 指令可用性判定流程

每个指令有一个对应的 `@COM_ABLE{n}` 函数，返回值为：
- `1`：指令可用
- `0`：指令不可用

**示例：舔阴指令 (@COM_ABLE1)**
```
位置：COMABLE.ERB:39-66

IF FLAG:25 & 1 (爱抚系过滤开启)
    RETURN 0
IF TALENT:122 (对象是男人)
    RETURN 0
IF TEQUIP:90 (触手调教中)
    RETURN 0
IF CFLAG:40 & 17 && FLAG:37 (穿着内裤/下装)
    RETURN 0
...其他条件检查...
RETURN 1
```

### 2. 指令执行流程（以正常位为例）

```
用户选择 [20] 正常位
    ↓
@COM20 (COMF20_正常位.ERB:7)
    │
    ├─ CALL CONFIRM_LOST_VIRGIN (处女确认)
    ├─ CALL CONFIRM_CONDOM (避孕套确认)
    ├─ CALL GET_ADV_COM (进阶指令跳转)
    │
    ├─ 打印指令名称
    ├─ CALL TRAIN_MESSAGE_B (调教消息)
    │
    ├─ 基础 source 计算
    │   ├─ LOSEBASE:0 (体力消耗) = 50
    │   ├─ LOSEBASE:1 (气力消耗) = 100
    │   └─ SOURCE:露出 = 400
    │
    ├─ 根据 ABL:2 (V感觉) 计算 source
    ├─ 根据 EXP:0 (V经验) 计算快感和疼痛
    ├─ 根据 PALAM:3 (润滑) 计算
    ├─ 根据 TALENT (性格/体质) 加成
    │
    ├─ CALL COM_EJAC_PLAYER_SEX (射精检查)
    ├─ [后续处理...]
    │
    └─ RETURN 1
```

### 3. 调教菜单系统

**菜单注册** (`@COMSEQ_REGISTER`)：
- 最多注册 10 个指令
- 支持指令重复执行
- 指令不可用时自动跳过

**菜单执行** (`@COMSEQ_TRAIN`)：
- 按顺序自动执行已注册指令
- 遇不可用指令时停止

---

## 关键变量/标志位

### 过滤器设置
| 标志 | 功能 |
|------|------|
| `FLAG:25` | 指令过滤器（位掩码） |
| `FLAG:6` | 调教文本显示设置 |

### 调教状态
| 变量 | 说明 |
|------|------|
| `TEQUIP:n` | 当前装备状态（n=设备ID） |
| `TARGET` | 当前调教对象 |
| `ASSI` | 当前助手 |
| `ASSIPLAY` | 0=主人调教，1=助手调教 |

### 身体状态
| 变量 | 说明 |
|------|------|
| `CFLAG:40` | 服装状态（位掩码） |
| `CFLAG:42` | 特殊装备（贞操带等） |
| `STAIN:n` | 污渍状态 |

### 经验与能力
| 变量 | 说明 |
|------|------|
| `ABL:n` | 能力等级 |
| `EXP:n` | 经验值 |
| `TALENT:n` | 性格/体质 |

---

## 指令分类

根据 COMF*.ERB 文件名，指令分为以下类别：

| 编号范围 | 类别 | 示例 |
|---------|------|------|
| 0-9 | 爱抚系 | 爱抚、舔阴、肛门爱抚、自慰 |
| 10-19 | 道具系 | 按摩棒、振动宝石、二プルキャップ |
| 20-29 | 性交系 | 正常位、后背位、骑乘位 |
| 30-39 | 奉仕系 | 手淫、口交、胸交 |
| 40-49 | SM系 | 斯帕nk、鞭打、绳子 |
| 50-59 | 道具系 | 润滑液、媚药 |
| 60-69 | 组合系 | 3P、双重口交、六九式 |
| 100+ | 特殊系 | 触手召唤、怪物调教 |

---

## 模块调用关系

```
调教开始
    │
    ├─ EVENT_BEFORETRAIN (@PRITRAIN_MESSAGE)
    │
    └─ 主循环
        │
        ├─ 用户选择指令编号
        │
        ├─ @COM_ABLE{编号} (可用性判定)
        │   └─ 检查 FLAG:25、TALENT、TEQUIP、CFLAG:40 等
        │
        ├─ @COM{编号} (指令执行)
        │   ├─ 确认检查 (处女、避孕套等)
        │   ├─ 消息打印
        │   ├─ SOURCE 计算
        │   ├─ 经验/珠计算
        │   ├─ 射精/绝顶判定
        │   └─ 各种标志设置
        │
        ├─ @SOURCE_CHECK (SYSTEM_SOURCE.ERB)
        │   ├─ 口上处理
        │   ├─ 装备状态检查
        │   └─ 射精后处理
        │
        ├─ @SELF_CHECK (调教后行为)
        │
        └─ @EVENT_AFTERTRAIN (调教结束)
```

---

## TODO / 未确认问题

1. **COMF*.ERB 文件数量**：实际有约 200+ 个文件，需要完整列表

2. **进阶指令跳转**：`CALL GET_ADV_COM` 函数未找到定义

3. **指令过滤器 FLAG:25**：需要分析具体位含义

4. **COMF150 之后指令**：需要进一步分析自由调教系统

5. **指令触发事件**：部分指令可能有特殊事件触发条件未分析

---

## Handoff

- **已完成**：
  - 指令可用性判定流程
  - 指令执行逻辑分析
  - 调教菜单系统分析
  - 关键变量/标志位梳理

- **未完成**：
  - 所有 COMF 文件的详细分析
  - 指令触发事件的完整分析

- **下一步建议**：
  - 继续分析 P0 任务：04_角色属性与成长

