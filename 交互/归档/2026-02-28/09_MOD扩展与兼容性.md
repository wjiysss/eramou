---
task_id: 09
owner: ClaudeCode
status: done
source_scope: F:\code\eraMaouEx\ERB\MOD\MOD_SWITCH.ERB, F:\code\eraMaouEx\ERB\MOD\PartTimeJob\PTJ.ERB, F:\code\eraMaouEx\ERB\MOD\SYSTEM_DEBUG_Universal_era.ERB
updated_at: 2026-02-28 19:00
---

# 09_MOD扩展与兼容性

## 功能概述

本模块分析 eraMaouEx 的 **MOD 扩展与兼容性系统**，包括：
- MOD 开关机制
- 内置 MOD 扩展
- 调试系统

---

## 关键文件清单

| 文件路径 | 功能说明 |
|---------|----------|
| `F:\code\eraMaouEx\ERB\MOD\MOD_SWITCH.ERB` | MOD 开关系统 |
| `F:\code\eraMaouEx\ERB\MOD\PartTimeJob\PTJ.ERB` | 打工系统 |
| `F:\code\eraMaouEx\ERB\MOD\MAKAIGINKOU v2.03v1\*` | 魔界银行扩展 |
| `F:\code\eraMaouEx\ERB\MOD\SYSTEM_DEBUG_Universal_era.ERB` | 调试系统 |

---

## MOD 开关系统

位置：`F:\code\eraMaouEx\ERB\MOD\MOD_SWITCH.ERB`

### 开关定义

| 位 | 标志位 | 功能 |
|----|--------|------|
| 0 | EX_FLAG:9000 & 1 | 魔界银行 |
| 1 | EX_FLAG:9000 & 2 | 铁石心肠（后代可处刑、可迎击） |
| 2 | EX_FLAG:9000 & 4 | 打工系统 |
| 3-15 | EX_FLAG:9000 & 8-32768 | 预留 |

### 开关调用

```
@MODLIST
    ├─ 显示 MOD 列表
    ├─ INVERTBIT EX_FLAG:9000, RESULT
    └─ 开关状态保存
```

---

## 打工系统 (PartTimeJob)

位置：`F:\code\eraMaouEx\ERB\MOD\PartTimeJob\PTJ.ERB`

### 打工类型

| ID | 名称 |
|----|------|
| 400 | 风俗 |
| 401 | 斗姬 |
| 402 | 演艺 |
| 403 | 女仆 |
| 404 | 教师 |
| 405 | 驯兽师 |
| 406 | 狱卒 |
| 407 | 图书管理员 |
| 408 | 宗教 |
| 409 | 研究 |

### 打工等级

- 0: 无
- 1: 普通
- 2+: 等级

---

## 魔界银行

位置：`F:\code\eraMaouEx\ERB\MOD\MAKAIGINKOU v2.03v1\MAKAI_BANK.ERB`

```
功能：
├─ 存款功能
├─ 利息计算
└─ 资金提取
```

---

## 调试系统

位置：`F:\code\eraMaouEx\ERB\MOD\SYSTEM_DEBUG_Universal_era.ERB`

```
功能：
├─ 角色数据调试
├─ 物品调试
├─ 资金调试
└─ 状态调试
```

---

## TODO / 未确认问题

1. **MAKAIGINKOU 详细分析**：魔界银行 v2.03v1 完整功能未分析

2. **SYSTEM_DEBUG**：调试函数详细列表未列出

3. **兼容性风险**：各 MOD 与主版本的兼容性未测试

---

## Handoff

- **已完成**：
  - MOD 开关机制分析
  - 打工系统分析
  - 调试系统概述

- **未完成**：
  - MOD 详细功能分析

- **下一步建议**：
  - P2 任务 10：补丁历史与版本演化

