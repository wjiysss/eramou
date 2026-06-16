# 实时进度

更新时间：2026-06-15

## 本轮新增（第七轮系统补完）

### 新增实现

- **COMF 指令 SOURCE 计算**（eraMaouEx.py）：
  - `_confirm_lost_virgin(target)` - 处女夺取确认
  - `_com_ejac_player_sex(target)` - 调教者性交射精量计算（技巧/顺从/淫乱/爱慕倍率）
  - `_com_ejac_player_analsex(target)` - 调教者肛交射精量计算

- **EQUIP_COM 装备效果**（eraMaouEx.py）：
  - 13种调教中装备效果：振动棒(11)/肛门振动棒(13)/阴蒂夹(14)/乳头夹(15)/榨乳器(16)/眼罩(43)/绳(44)/口塞(45)/视频(53)/野外(54)/羞耻(57)/兽奸(89)/触手(100)
  - 每种装备返回SOURCE字典（快感/恐怖/露出/屈辱/不洁等）

- **SOURCE SUB 辅助计算**（eraMaouEx.py）：
  - `_source_sex_check(target)` - 同性检查修正（双性恋/百合气质/好奇心/保守的）
  - `_player_skill_check(target)` - 调教者技巧修正
  - `_master_skill_check(target)` - 主人技巧修正
  - `_lost_virgin_check(target)` - 处女丧失检查+消息
  - `_incest_sex_check(target)` - 近亲相奸修正
  - `_ex_check_up(target)` - 绝顶检查（C/V/A/B/强绝顶）
  - `_target_ejac_check(target)` - 调教对象射精检查（扶她/男主）
  - `_target_milk_check(target)` - 喷乳检查
  - `_love_moist_check(target)` - 爱液处理

### 项目统计

- 主文件：~55,500 行
- GameEngine 方法：3,449 个
- 编译状态：✅ 通过
- 已实现核心系统：调教/商店/地牢/事件/结局/装备/卖出/银行/打工/MOD/配置/处刑/外观/称呼/SOURCE计算/素质获取/指令注册

## 前轮新增（第六轮系统补完）

### 新增实现

- **EVENT_NEXTDAY**（eraMaouEx.py）：
  - `_event_nextday()` - 每日事件处理（HP/MP回复、妊娠推进、出産、育児、善恶值、信仰值等）
  - `_ninsin_main()` - 妊娠/出産/育児室处理
  - `_childbirth()` - 出産处理
  - `_karma()` / `_faith()` - 善恶值/信仰值增减
  - `_auto_buying()` - 自动购买（润滑液/录像带/安全套）
  - `_human_age_generate()` - 外表年龄计算

- **EVENT_NEXTMONTH**（eraMaouEx.py）：
  - `_event_nextmonth()` - 每月事件处理（年越し、外表年龄更新）

- **EVENT_TURNEND**（eraMaouEx.py）：
  - `_event_turnend()` - 回合结束处理（午前→午后切换、日付更新、NEXTDAY→NEXTMONTH调用链）

- **EVENT_BEFORETRAIN**（eraMaouEx.py）：
  - `_event_beforetrain(target)` - 调教前事件（着衣设定、初次/常规分支、妊娠检查）
  - `_beforetrain_noclothes(target)` - 全裸模式脱衣反应（素质别分岐）
  - `_beforetrain_clothed(target)` - 着衣模式入场反应
  - `_print_clothtype(target)` / `_wearing_cloth_all(target)` - 衣着状态描述

- **EVENT_AFTERTRAIN**（eraMaouEx.py）：
  - `_event_aftertrain(target)` - 调教后事件（死亡检查→SELF_CHECK）
  - `_death_check(target)` - 死亡检查（濒死保护/魔王转生/GAMEOVER）
  - `_self_check(target)` - 行为总检（性交→百合→自慰→兽奸）
  - `_self_check_sex(target)` - 阴道性交自检（V感觉/中毒/素质判定）
  - `_self_check_analsex(target)` - 肛交自检
  - `_self_check_lesbian(target, s)` - 百合自检
  - `_self_check_masturbation(target, s, n)` - 自慰自检（含妄想对象判定）
  - `_self_check_beast(target)` - 兽奸自检

- **EVENT_AUTOTRAIN**（eraMaouEx.py）：
  - `_event_autotrain()` - 自动调教循环（CFLAG:666≠0角色）
  - `_format_autotrain(target)` - 调教前重置（射精计数/TFLAG/PALAM）
  - `_before_autotrain(target)` / `_after_autotrain(target)` - 前后处理
  - `_juel_check_main(target)` / `_auto_ablup(target)` - 珠反映/自动升级

- **EVENT_CHARA_LEAVE**（eraMaouEx.py）：
  - `_chara_leave(char_idx)` - 角色离去（序列化→存档→清理引用→删除）
  - `_chara_return(slot, set_level)` - 角色回归（反序列化→恢复→HP/MP全回复）

- **SYSTEM_SOURCE**（eraMaouEx.py）：
  - `_source_check(target, com_id)` - 主SOURCE计算框架（避孕套/装备效果/连续惩罚/气力0/相性修正）
  - `_source_check_up_c/v/a/b/free(target)` - C/V/A/B/F五区SOURCE计算（素质倍率/欲情等级/欲望ABL/否定快感/抑郁等）

- **GET_SPECIALTALENT**（eraMaouEx.py）：
  - `_check_special_skill(target, seiin)` - 特殊素质获取判定（爱慕/淫乱/精飲/性技/崩壊体転等完整分支）
  - `_check_special_skill_bodyshift(target)` - 崩壊体転判定

- **SHOP_2**（eraMaouEx.py）：
  - `_ability_up()` - 能力值升级菜单（奴隶一览/勇者一览/能力升级）

- **COM_REGISTER**（eraMaouEx.py）：
  - `_comseq_register()` - 调教指令注册
  - `_comseq_show()` - 已注册指令显示
  - `_comseq_train()` - 注册指令执行
  - `_multi_comable(com_id)` - 指令可用性检查

## 前轮新增（第五轮系统补完）

### 新增实现

- **EXECUTION**（eraMaouEx.py）：
  - `_check_execution_available(target)` - 检查目标是否可处刑
  - `_show_execution_menu(target)` - 8种处刑方式菜单（流放/公开处刑/博物馆/猎奇/肉便器/士兵化/固定示众/消除记忆释放）
  - `_execute_character(target, method)` - 执行处刑，含完整肉便器分支

- **GROTESQUE**（eraMaouEx.py）：
  - `_show_grotesque_menu(target)` - 残酷处刑菜单
  - `_execute_grotesque(target, method)` - 残酷处刑执行

- **FULLMOON**（eraMaouEx.py）：
  - `_check_fullmoon()` - 满月事件检查与处理

- **SELF_CALL**（eraMaouEx.py）：
  - `_get_self_call(target)` / `_set_self_call(target, call)` - 角色自称获取/设置
  - `_get_self_call_first(target)` - 自称首字
  - `_get_call_name(target, other)` - 角色间称呼
  - `_random_self_call(target, mode)` - 随机自称决定（模板→因子→昵称三层逻辑）
  - `_calc_selfcall_factor(target)` - 教育/姿态/开放三因子计算
  - `_set_suit_selfcall(target, start)` - 基于因子选择自称（吾辈/老身/奴家/妾身/俺/老子等）
  - `_set_nick_selfcall(target, start)` - 基于角色名昵称自称

- **CONFIG**（eraMaouEx.py）：
  - `_show_config()` - 27项配置菜单
  - `_set_config(key, value)` / `_get_config(key)` - 配置项设置/获取
  - `_config_show_filter_status()` - 过滤状态显示
  - `_config_filter_setting(filter_bit)` - 过滤位切换
  - `_config_virgin_conceded_status()` / `_config_set_virgin_conceded(value)` - 处女献身设置
  - `_config_get_penis_status()` / `_config_set_penis(value)` - 魔王兵器状态
  - `_config_modlist_status()` - MOD开关状态

- **LABO**（eraMaouEx.py）：
  - `_show_labo()` - 实验室菜单
  - `_labo_execute(choice)` - 执行实验室命令
  - `_craft_item(recipe_id)` / `_decompose_item(item_id)` - 合成/分解
  - `_labo_geo_test()` / `_labo_geo_output()` - 地形生成与输出
  - `_labo_face_test()` - 头像测试

- **LOOK**（eraMaouEx.py）：
  - `_show_look(target)` - 完整角色外观显示（种族/发色/眼/体型/服装/过去/信仰等）
  - `_get_body_desc(target)` / `_get_face_desc(target)` / `_get_cloth_desc(target)` / `_get_state_desc(target)` - 各部分描述
  - `_get_love_preferences(target)` - 喜欢的东西计算系统（种族/职业/素质/能力补正+排序+金红桃显示）
  - 17个 `_XXX_NAMES` 字典和 `_get_xxx_name` 辅助方法

- **ENDING**（eraMaouEx.py）：
  - `_ENDING_DEFINITIONS` - 12个结局定义（Good/Bad/Normal End + 领域制霸 + 角色线结局）
  - `_ENDING_TEXTS` - 每个结局完整中文文本
  - `_check_ending()` - 结局触发检查（优先级：Normal→Good→领域制霸→角色线→魔王城陷落）
  - `_show_ending(ending_id)` - 结局文本显示
  - `_get_ending_list()` - 结局列表（含达成状态和进度）
  - `_apply_endcheck_characters()` - 角色专属结局检定

- **EQUIP**（eraMaouEx.py）：
  - `_EQUIP_WEAPON_DATABASE` - 13种武器完整数据
  - `_EQUIP_RING_DATABASE` - 21种戒指完整数据
  - `_show_equip(target)` - 三装备槽显示（武器/装饰A/装饰B）
  - `_equip_item(target, slot, item_id)` / `_unequip_item(target, slot)` - 装备/卸下（含诅咒处理）
  - `_get_equip_stats(target)` - 合计属性计算
  - `_compute_equip_stats(...)` - 单件装备属性计算（含前缀附魔和强化加成）
  - `_apply_prefix_effects(...)` - 武器前缀附魔效果
  - `_apply_equip_powerup(...)` - 角色天赋加成

## 前轮新增（第四轮系统补完）

### 新增实现

- **SELL_MATURO**（eraMaouEx.py）：
  - `_sell_maturo(target, sell_price)` - 卖出末路口上系统，完整实现160+种末路分支：
    - 市场选择菜单（魔界黑市/异族交易市场/宠物市场/随手卖掉）
    - 主分支：反抗刻印Lv3 / 爱慕 / 淫乱 / 普通
    - 子分支：魔族(TALENT:314==9) / 其他种族（含龙族特殊处理）
    - 价格段：100万+ / 50万+ / 10万+ / 10万-
    - 职业分支：战士&盗贼 / 骑士&忍者(或骑士&魔法师) / 巫女&神官 / 其他
    - 特殊素质子分支：性爱狂/肛门狂/巨乳/肉便器/话术LV5+/V感觉LV5+/等级检查
    - 家族成员CSTR:5设置、TSTR:30末路标题、最终告别文案
  - `_sell_maturo_market_select()` - 市场选择菜单
  - `_search_family(target)` - 通过CFLAG:605查找家族成员

- **EXCOM**（eraMaouEx.py）：
  - `_EX_TALENT_NAMES` - 15种EX素质名称定义（灵魂错位/近卫/后代/魔王替身/狂王替身/琼/普林希斯/嘉德/菲娅/魔王/无双/一人军团/魔女/魔界公主/天神）
  - `_add_chara_ex(char_idx)` - 角色添加时EX素质初始化：
    - CFLAG:6检查→口上素质(101-104)
    - 魔王素质(200)、特殊战斗素质(801/901)
    - 动态调用`_chara_ex_{NO}()`方法
  - `_get_ex_kojo_num(char_idx)` - EX口上编号获取（遍历101-200，返回index+900）
  - `_init_ex_talent_names()` - EX素质名称初始化

- **MAKAI_BANK**（eraMaouEx.py）：
  - `_calc_loan_limit()` - 四段贷款额度计算（基于CFLAG:0:9等级）
  - `_calc_interest()` - 存款利息计算（0.1%/天）+ 欠款滞纳金（超30天+50%）
  - `_makai_bank_deposit(amount)` - 存款（EX_FLAG:9001增加/MONEY减少/EX_FLAG:4444追踪）
  - `_makai_bank_withdraw(amount)` - 取款
  - `_makai_bank_loan(amount)` - 贷款（20%利息，额度限制）
  - `_makai_bank_repay(amount)` - 还款（超额自动转存款）
  - `_show_makai_bank()` - 银行界面显示

- **PTJ**（eraMaouEx.py）：
  - `_PTJ_NAMES` - 10种打工名称（风俗/斗姬/演艺/女仆/教师/驯兽师/狱卒/图书管理员/宗教/研究）
  - `_get_ptj_name(ptj_pos)` - 打工名称获取
  - `_get_ptj_info(target)` - 打工状态统计（活跃数/最高位置/等级/名称）
  - `_set_ptj_level(target, ptj_pos, level)` - 打工等级设定
  - `_show_ptj_status(target)` - 打工状态显示

- **SELL_MATURO_K1**（eraMaouEx.py）：
  - `_sell_maturo_k1(target, sell_price)` - 异种族卖出末路口上，完整实现160+种末路分支：
    - 反抗刻印Lv3：魔族/其他种族 × 价格段 × 食脑魔/恶魔/高阶魔法研究所/兽人/吸血鬼/巨魔等买家
    - 爱慕或淫乱：魔族/其他种族 × 4价格段 × 暗黑龙/上级恶魔/异形之神/食人魔/半人马/牛头人/堕天使/狮鹫/蛇妖/哥布林等买家
    - 普通：魔族/其他种族 × 3价格段 × 同类买家不同文本
    - 特殊素质检查：扶她(TALENT:121)/不怕污臭(TALENT:61)/动物耳朵(TALENT:124)/成为勇者前的生活(TALENT:315)/肛门感觉(ABL:3)等

- **SELL_MATURO_K2**（eraMaouEx.py）：
  - `_sell_maturo_k2(target, sell_price)` - 牝犬卖出末路口上：
    - 牝犬(TALENT:136)加价50000
    - 牝犬：4价格段 × 性爱狂/话术LV5+/其他 → 最高级牝犬饲养员/训练员/奴隶等12种末路
    - 非牝犬淫乱：3价格段 → 高级牝犬/母种犬/淫乱母犬
    - 非牝犬普通：3价格段 → 高级牝犬/滥交牝犬/牝犬

- **MOD_SWITCH**（eraMaouEx.py）：
  - `_get_bit(val, bit)` / `_toggle_bit(val, bit)` - 位操作辅助
  - `_show_mod_switch()` - MOD开关菜单（魔界银行/铁石心肠/打工系统）
  - `_toggle_mod_switch(mod_bit)` - 切换MOD位，含银行债务处理和打工同步
  - `_show_mod_status()` - 紧凑状态行
  - `_maounet_mod_print()` - MaouNet银行按钮
  - `_maounet_mod_script(result)` - MaouNet银行命令处理

## 前轮新增（第四轮系统补完）

### 新增实现

- **EVENT_ADDICT**（eraMaouEx.py）：
  - `_check_aphrodisiac_addict()` - 媚药中毒检查系统：
    - 每7天减少体内残留度（CFLAG:31）
    - 媚药中毒消失判定（残留度=0时消除TALENT:46）
    - 媚药中毒获取判定（残留度≥12/容易陷落≥9）
    - 疯狂获取判定（残留度≥40/容易陷落≥30）
    - 崩坏获取判定（残留度≥100/容易陷落≥75）
  - `_precipitate_withdrawal()` - 禁断症状系统：
    - 按残留度计算症状酷度（治疗/献身人数修正）
    - 严重恶化：崩坏→疯狂→被嫌弃→抵抗→悲观→感情淡薄
    - 体力/气力/最大体力/最大气力下降
    - 看护者体力下降

- **EVENT_SABBATH**（eraMaouEx.py）：
  - `_check_sabbath()` - 安息日（满月）仪式系统：
    - 满月+法术/咒术+淫乱条件检查
    - 男性/扶她/处女/私处封印/兽奸中毒/普通 分支
    - 经验加算（V/A/性交/精液/兽奸）
    - 珠加算（快V/快A/欲情/耻情）
    - 童贞丧失处理
  - `_check_sabbath_day()` - 安息日（每日版）仪式：
    - 每3天一次+信仰值≥40条件
    - 兽奸仪式/乱交仪式/亵渎仪式/默认仪式

- **NAMING**（eraMaouEx.py）：
  - `_edit_character_name()` - 角色命名（名称/呼称/绰号）
  - `_init_character_names()` - 初始化角色名称
  - `_get_default_callname()` - 默认自称（俺/僕/わたくし/わたし/あたし/私）

- **FUNC_CLOTH**（eraMaouEx.py）：
  - `_CLOTH_NAMES` - 50种服装名称定义
  - `_get_cloth_name()` - 服装ID→名称映射
  - `_get_wearing_cloths()` - 获取角色穿着列表（主服装+TEQUIP装备）
  - `_is_cloth_exposing()` - 服装暴露判定

## 前轮新增（系统全面补完第二轮）

### 新增实现

- **IKAI_BONUS**（eraMaouEx.py）：
  - `_apply_ikai_bonus()` - 异界奖励系统，按探索层数给予奖励：
    - 异界综合征检查（MARK:10 刻印）
    - 源倍率计算（MARK等级→Y值：5→60, 4→70, 3→80, 2→90, 1→95）
    - 金钱奖励（基础金额×层数系数×异界倍率）
    - 经验奖励（EXP:99 = 层数×100×倍率）
    - 勋章经验（每3层+1）
    - 特殊层数奖励（9层异界素质/6层综合征加深/3层战斗等级提升）

- **MAGIC**（eraMaouEx.py）：
  - `_MAGIC_DEFINITIONS` - 9种魔法定义表（名称/类型/MP消耗/描述）
  - `_check_magic_available()` - 魔法可用性检查（天赋+MP）
  - `_use_magic()` - 魔法使用主方法，按ID分派到具体实现
  - `_get_magic_list()` - 获取可用魔法列表
  - 9种魔法实现：传送术/睡眠咒语/魔法箭/魔法吸取/火球术/治疗术/诅咒术/精神吸收/经验吸取
  - 辅助方法：伤害上限/角色对怪物补正/怪物对角色补正/角色对角色补正

- **LOVERS**（eraMaouEx.py）：
  - `_name_lover()` - 20种恋人类型名称映射
  - `_enter_lover()` - 恋人派遣（设置CFLAG:606/607）
  - `_dungeon_town_lover()` - 城镇恋人事件，按LOVE_LV分支：
    - 0: 初遇 → 10: 再遇 → 20: 约会 → 30: 亲密 → 40: 同居 → 50+: 激烈性交
    - 经验/珠结算（接吻/口交/V/A性交/百合/兽奸/被拍/前戏等加成）
    - 贞操带/处女封印检查、处女丧失、初吻标记、膣内射精处理

- **MARRIAGE_DAY**（eraMaouEx.py）：
  - `_marriage_day()` - 结婚生活事件，按CFLAG:601婚姻类型分派：
    - 900: 野狗婚姻 → 901: 主人婚姻 → 902: 恋人婚姻
    - 其他: 怪物配偶（按怪物类型分派）

- **LIFE_LIST**（eraMaouEx.py）：
  - `_life_list()` - 角色列表显示（编号/名称/职业/等级/沦陷状态/妊娠/派遣标记）
  - `_life_list_enemy()` - 勇者列表显示
  - `_life_list_slave()` - 奴隶列表显示

- **MAOUNET**（eraMaouEx.py）：
  - `_maounet_export()` - 魔王网导出（最多5人/队，验证主人/敌方排除）
  - `_maounet_import()` - 魔王网导入（等级上限/等级1设定检查）
  - `_maounet_clear_imports()` - 清除通信勇者
  - `_maounet_set_level_cap()` - 等级上限设定
  - `_maounet_toggle_level1()` - 登场等级1切换
  - `_maounet_list_saves()` - 通信存档列表

- **INFRASTRUCTURE**（eraMaouEx.py）：
  - `_INFRASTRUCTURE_TYPES` - 12种设施类型定义（石像/标本/蜡像/人偶/金属像/冰雕/宝石像/家具/画像/喷水像等）
  - `_show_infrastructure()` - 设施展示主方法
  - `_show_all_exhibits()` - 全部展品一览
  - `_show_benki()` - 肉便器展示
  - `_show_video_crystal()` - 影像水晶球展示

## 前轮新增（COMF 共享函数 + 调教消息系统 + 功能审计）

### 全面功能审计结果
对整个项目进行了全面功能缺失审计，对比 ERB 源码与 Python 实现。主要发现：

1. **COMF 共享函数完全缺失**：COMF_VAGINASEX、COMF_ANALSEX、COMF_CONDOM、COMF_JUMP 四个被多个 COMF 指令共享的核心函数在 Python 中完全没有实现。
2. **COMORDER/COM_REGISTER 缺失**：指令实行值计算和调教菜单注册系统没有实现。
3. **EVENT_TRAIN_MESSAGE 缺失**：调教消息文本生成系统没有实现。
4. **usercom.py 占位方法**：set_clear_point/clear_to_point 为空壳。
5. **ABLUP/SHOP 系统**：已完全覆盖。
6. **DUNGEON 系统**：主流程已实现，子模块（AFTER/BATTLE/BITCH/DAILY/PARTY/QUEST/ROOM/RYOUZYOKU/SETUP/TOWN/TRAP）在 dungeon.py 中有对应逻辑。
7. **其他系统**：大部分有 Python 文件，但实现深度不一。

### 新增实现

- **COMF_VAGINASEX**（train.py）：
  - `confirm_lost_virgin()` - 处女夺取确认
  - `com_ejac_player_sex()` - 调教者射精检查（阴道性交），按指令类型/能力/润滑/经验/安全套等多维度计算射精量，处理大量/通常射精判定
  - `_com_ejac_player_milk()` - 调教者喷乳检查，处理母乳喷射判定和经验
  - `com_after_vagina_sex()` - 阴道性交后处理，包括私处经验/性交经验/异常经验/百合经验/爱情经验/好感度/童贞丧失/污れ转移

- **COMF_ANALSEX**（train.py）：
  - `com_ejac_player_analsex()` - 调教者射精检查（肛门性交），按指令类型/能力/润滑/肛门经验/扩张经验等计算射精量
  - `com_after_anal_sex()` - 肛门性交后处理，包括肛门经验/性交经验/CFLAG更新/百合经验/爱情经验/好感度/污れ转移

- **COMF_CONDOM**（train.py）：
  - `confirm_condom()` - 安全套使用确认，支持每次确认/自动使用/不使用三种设定
  - `confirm_condom2()` - 安全套确认2（逆侵犯助手用）
  - `condom_settings()` - 安全套设定

- **COMF_JUMP**（train.py）：
  - `get_adv_com()` - 高级指令派生/连招系统，完整实现原 ERB 的指令派生逻辑：
    - 接吻→正常位接吻/站立背后位
    - 舔阴→六九式
    - 自慰→口交时自慰
    - 胸爱抚→正常位胸爱抚/背后位胸爱抚
    - 插入手指→G点刺激
    - 正常位→正常位SP/3P/G点/子宫口
    - 背后位→背后位SP/3P/G点/子宫口
    - 对面座位/背面座位/骑乘位→G点/子宫口
    - 手淫→手搓口交
    - 口交→六九式/乳夹口交/深喉/真空口交/3P
    - 乳交→乳夹口交
    - 股间性交→双人股间性交
    - 打屁股→背后位打屁股
    - 强制舔阴→六九式
    - 强制口交→3P
    - 自助舔舐→口交时自慰

- **COMORDER**（train.py）：
  - `com_order()` - 指令实行值计算，综合顺从/抖M/百合/刻印/恭顺/恐怖/素质/相性等多维度计算

- **COM_REGISTER**（train.py）：
  - `comseq_register()` - 调教菜单注册
  - `comseq_show()` - 显示已注册菜单
  - `comseq_train()` - 执行调教菜单

- **EVENT_TRAIN_MESSAGE**（train_message.py 新文件）：
  - `TrainMessageSystem` 类，框架化调教消息文本生成系统
  - `generate_message_b()` - 调教动作描述（按 SELECTCOM 分支）
  - `generate_message_a()` - 调教结果描述（按 TFLAG 分支）
  - 辅助方法：肤色/胸部/体型/私处描述、PALAM等级计算

- **usercom.py**：
  - `set_clear_point()` - 从空壳改为实际保存游戏状态快照
  - `clear_to_point()` - 从空壳改为实际回滚状态

- **辅助方法**（train.py）：
  - `_get_palam_levels()` - PALAM 等级阈值
  - `_get_exp_levels()` - EXP 等级阈值
  - `_comable_check()` - 简化版 COM_ABLE 检查

- **EVENT_AUTOTRAIN**（train_main.py）：
  - `run_autotrain()` - 自动调教主循环，遍历所有 CFLAG:666 > 0 的角色
  - `_format_autotrain()` - 自动调教前格式化（射精归零/TFLAG重置/PALAM重置/常时发情奖励）
  - `_before_autotrain()` - 自动调教前置（SOURCE/UP/DOWN重置）
  - `_execute_autotrain_commands()` - 执行自动调教指令序列（按 CFLAG:666 类型选择指令组合）
  - `_after_autotrain()` - 自动调教后处理（业力增减/润滑欲情蓄积/回数累计）

- **EVENT_BEFORETRAIN**（train_main.py）：
  - `before_train_message()` - 调教开始时消息，完整实现原 ERB 的所有分支：
    - 初调教/非初调教分支
    - 崩坏/坦率/温顺/默认态度分支
    - 妊娠状态描述（临月/稳定期/显怀）
    - 助手态度描述（施虐/爱慕/默认）
  - `_before_train_noclothes()` - 初调教时·裸体消息（14种性格分支）
  - `_before_train_clothed()` - 初调教时·着衣消息（14种性格分支）

- **DATA_FIX**（eraMaouEx.py）：
  - `_apply_data_fix()` - 存档数据修复，在加载存档后自动执行：
    - 魔王高贵标识（EX_TALENT:200）
    - 来历/理由修复补丁（TALENT:315/316）
    - 菲娅修正补丁（NO:35）
    - 最大体力/气力下限（600/100）
    - EX口上素质转移（NO:31-35 → EX_TALENT:101-104）
    - EX技能转移（TALENT:265-269 → EX_TALENT:801/900-903）
    - 近卫和后代素质转移（TALENT:221-222 → EX_TALENT:1-2）
    - CFLAG转移（CFLAG:800 → EX_CFLAG:99）
    - FLAG转移（FLAG:1000-9999 → EX_FLAG）
    - 声望初始化（EX_FLAG:99 = 70）
    - 菲娅淫乱线剧情节点修复（FLAG:2807 1400→140）

- **GET_SPECIALTALENT**（eraMaouEx.py）：
  - `_check_special_talent()` - 特殊素质获取判定主方法，完整实现原 ERB 的 20 项判定：
    - 卖却/助手资格判定（CFLAG:2 >= 2000 + 淫乱/爱慕）
    - 爱慕获取（顺从3+侍奉精神3+屈服刻印3+好感1000+）
    - 淫乱获取（欲望3+CVAB合计10+快乐/屈服刻印3+异常经验3+）
    - 高顺从消除（从不自慰/绝不侍奉/不受洗脑）
    - 喜欢精液/擅用舌头/施虐狂/受虐狂/露出狂/牝犬
    - 特殊性感素质（自慰狂/性爱狂/尻穴狂/弄乳狂）
    - 强化素质（淫核/淫壶/淫肛/淫乳）+ 性豪
    - 时常发情/强制精饮→喜欢精液
    - 负面素质消失/主人谜之魅力/妓女/倾城/妄信
  - `_check_special_talent_sex_skill()` - 特殊性感素质子方法
  - `_check_special_talent_shojo_seal_release()` - 贞操封印解封子方法
  - `_check_special_talent_maou_ex_talent()` - 玛奥替身判定子方法
  - `_check_special_talent_corruption_race_fall()` - 恶堕种族变化子方法
  - `_check_special_talent_bodyshift()` - 肉体强制变化子方法

- **FULLMOON**（eraMaouEx.py）：
  - `_apply_fullmoon_effect()` - 满月效果，按种族调整基础数值：
    - 狼人：攻击/防御×10，HP/MP全恢复
    - 吸血鬼：攻击/防御取最大值，HP/MP×10
    - 天使：MP减半
    - 暗精灵：攻击×2，HP/MP全恢复
    - 堕天使/魔族：攻击×2
    - 种族2：植物/触手/妖精等各有加成

## 本轮新增（SELF_KOJO 桥接修复）

- 复核 `NINSIN_GIVE_BIRTH` / `NTR_CHILD_BIRTH` 后，已将普通分娩成功分支的收尾收紧回原作语义：正常顺产不再共享 `N_RESET_STATUS` 式的整套产后重置，只保留原文可证实的父性计数、处女膜破损提示与育儿开始；`NTR_CHILD_BIRTH` 仍保留原作式的完整产后清理。
- `NTR_CHILD_BIRTH` 现在已经从原始 `ERB/EVENT_K*.ERB` 直接读取 `@NTR_KOUJO_K*` 角色口上块，避免继续误借 `SELF_KOJO` 源文件；当前仍保留无匹配时的最小兜底文案，但优先路径已回到原作分发结构。
- `NTR_VIDEO` 的“解除 NTR 状态并重新作为侵攻者放出”分支已拆成 NTR 专用的轻量 helper，避免继续复用更重的通用侵攻恢复流程，把原文只提到的 `CFLAG:1/501/502/508/151/2` 收尾和其它侵攻初始化混在一起。
- 修复 `SELF_KOJO` 桥接层的文件名匹配 bug：原 `_load_self_kojo_source_text` 只查 `EVENT_K{N}.ERB`，但实际文件名带后缀（如 `EVENT_K4_冷徹.ERB`、`EVENT_K903_嘉德.ERB`），导致所有口上块都加载失败、`_run_self_kojo` 一直返回空。
- `_load_self_kojo_source_text` 现在按 `EVENT_K{N}.ERB` → `EVENT_K{N}.erb` → `EVENT_K{N}_*` 前缀通配三级查找，命中 K0~K15、K19 以及 K903/K904 等 20 个原始口上文件。
- 修复 kojo_num 与文件号错位：`_get_kojo_num` 对 talent 160-179 返回 100-119，但 EVENT_K 文件用的是 0-19 编号。`_get_self_kojo_source_variants` 现在把 100-119 区间映射回 0-19，`@SELF_KOJO_K{N}` 标签解析恢复正常。
- 至此 `SELF_KOJO` 链路从“空分发层”升级为可真正读取并渲染原版口上文本，aftertrain 的性交/百合/自慰三段 `_run_self_kojo(target, 4/2/1)` 现在能按角色性格输出对应 K 文件的内容。
- 已确认 K19 与 K904 都对应菲娅但 `@SELF_KOJO_K` 标签编号不同（K19 vs K904），现有映射 `1004 → 文件 K904 → 标签 SELF_KOJO_K904`、`119 → 文件 K19 → 标签 SELF_KOJO_K19` 两路独立、互不冲突。
- 补回 `SELF_CHECK` 开头的逆强奸清理：`_apply_aftertrain_followup_checks` 现在会在进入结算前把 `CFLAG:MASTER:61` 清零，对齐原作 `SIF CFLAG:MASTER:61: CFLAG:MASTER:61 = 0` 的边界。
- 修复 `_apply_self_kojo_assignment` 只处理 Q/S/N/A/B/C 的严重 bug：原版 SELF_KOJO 文件里大量 `CFLAG:261 = 4`、`CFLAG:262 = 5`、`ABL:33 = X` 等推进赋值被静默丢弃，导致口上解锁标记永远不写入、每轮重复触发同一段。新增 `_apply_self_kojo_target_assignment` 处理 CFLAG/TALENT/ABL/EXP/TFLAG/FLAG 系列的 TARGET/ASSI/MASTER/索引/简写五种写法。
- 同步补齐 `_expand_self_kojo_condition` 的单参数简写：原版 K 文件里 `IF TALENT:76 && CFLAG:261 < 4` 这种省略 `:TARGET:` 的简写现在能正确解析为 target 的对应字段。同时补上 `CFLAG:TARGET:N`、`CFLAG:ASSI:N`、`CFLAG:MASTER:N`、`EXP:TARGET:N`、`MARK:TARGET:N`、`JUEL:TARGET:N`、`NOWEX:N` 等扩展形式。
- 修复 `SIF` 单行 if 被错误地按多行 IF 处理的 bug：原版 K 文件里大量 `SIF CFLAG:271 >= 1 / RETURN 0` 这种两行结构，之前 `_collect_self_kojo_branch` 会去找不存在的 ENDIF，把后续所有代码吞进分支块，导致妊娠発覚/出産/育児室等整段 SELF_KOJO 永远只输出第一段。`_parse_self_kojo_block` 现在单独处理 SIF：读条件→读下一行→按条件成立与否决定执行，并支持 SIF + RETURN 直接跳出当前 block。
- 同步修复 `_collect_self_kojo_branch` 对 SIF 的处理：IF 块内嵌套的 SIF 现在会连同它的下一行一起被收集进块体，再由递归 `_parse_self_kojo_block` 解析，避免 SIF 被当成独立 IF 误读 ENDIF 边界。
- 补齐 `_render_self_kojo_command` 的命令支持：原版只处理 `PRINTFORMW/PRINTFORML/PRINTFORM/PRINT` 四种带空格的打印命令，遇到 `PRINTFORMW` 单独一行（K4 里多次出现的空 PRINTFORMW）会直接静默丢失。现在补上 `PRINTL/PRINTW` 带参/无参、`PRINTFORMW` 无参（输出空行）、`CALL XXX`（暂返回空，避免静默丢失）。
- 修复 `_extract_self_kojo_block_lines` 块边界判定 bug：原实现只查 `@SELF_KOJO_K{N}` 形式的下一个 marker，但 K 文件里 `@SELF_KOJO_K4` 之后跟着的是 `@DUNGEON_RYOUZYOKU_K4`、`@BENKI_KOUJO_K4` 等 27 个不同前缀的标签，原逻辑会把后续 1100+ 行 unrelated 内容全部吞进 SELF_KOJO 块（实测 K4 块从 1279 行错读到 EOF）。现在改为"找下一个 `\n@` 标签"作为块结束，K4 块正确收敛到 154 行（25 IF / 25 ENDIF 完全平衡）。
- 修复 `_expand_self_kojo_condition` 里 `!` 转 `not` 的 regex：原 `!(?!=)` 会让 `!=` 里的 `!` 错误转成 `not =`，破坏不等比较。改为 `!(?![=])`，确保 `!=` 保留原样。
- 全量验证 19 个 K 文件的 SELF_KOJO 块解析：K0-K15、K19、K903、K904 共 19 个文件的 IF/ENDIF 全部平衡（K0:35/35、K5_マオ:67/67 最大、K12:23/23、K4:25/25 等），无悬空 ENDIF 或未闭合 IF。K4 SELF_KOJO 块的全部 44 个独立条件表达式（含 `TALENT:85 && CFLAG:102 == 1`、`ABL:16 >= 5 && (CFLAG:263 < 2 || FLAG:7 == 2)` 等复合形式）都能被 `_expand_self_kojo_condition` 正确转换。
- 重构 K 文件加载逻辑消除重复：`_load_self_kojo_source_text` 和 `_load_ntr_kojo_source_text` 之前各有 20+ 行重复的文件查找/读取代码。抽出共享 helper `_resolve_kojo_file_path`（三级查找：精确匹配 → 小写后缀 → 前缀通配）和 `_read_kojo_file_content`（utf-8 优先、cp932 兜底）。两个加载器现在各缩减到 8 行。
- `py_compile` 全量通过：44 个 Python 文件、61012 行、0 错误。

- 狗婚姻日常分支已回收为更接近原 ERB 的三段结构，避免把状态判断继续叠成一层过深的复合条件。
- 狗婚姻日常的原作兜底分支已补回 JUEL:6 累加，普通狗屋阶段现在与原 ERB 的情绪/慵懒结算一致。
- 狗婚姻日常已补回原作的 CFLAG:106 累加逻辑，三段分支中的经验/亲密推进现在会同步维护狗婚姻状态。
- 婚姻日常开头已按原作同时清空 CFLAG:107 / CFLAG:112，避免上一轮受孕来源残留到下一次婚后流程。

- 商店调试输出已挪回商店会话入口，`【DEBUG】进入商店...` 现在只会在 `run_shop()` 开始时打印一次，避免和原版 `EVENTSHOP` 的一次性入口日志次数不一致。
- 回合结束与商店入口的调试输出已按原版重新补回，`turn_end_processing()` 和 `show_shop()` 相关路径现在会再次输出 `【DEBUG】` 行，与 `EVENTTURNEND` / `EVENTSHOP` 的原始日志行为保持一致。
- 回合结束正式路径中的调试打印已移除，`turn_end_processing()` 现在不再额外输出 `【DEBUG】回合结束...`，避免把原版 `EVENTTURNEND` 没有的调试信息带进正式流程。
- 角色离场/返场存档边界已收紧：`EVENT_CHARA_LEAVE` 的离场序列化不再携带 `item` / `share_id` 等通信队伍字段，返场时会回到模板默认姓名并清空离场时残留的自定义物品状态，避免把 MAOUNET 的共享序列化污染到普通离场流程。
- `OFFERVIRGIN_CHECK` 的触发评分已回调为原版的重复 `TALENT:27` 逻辑，移除了 Python 里误加的 `TALENT:28` 参与项，避免纯好奇/警戒权重被改成另一套判定。
- 公共床上服务筛选已补回原版的孕期/育儿排除，`_can_join_bedroom_daily_service()` 现在会在朝フェ拉、夜袭等共享入口前拦掉育儿中与临月角色，避免晨间和夜间服务被同一处公共 helper 的缺失条件一起污染。
- `EVENT_NEXTDAY` 的晨间入口已回调为原作式四段调用，移除了 Python 里额外插入的 shadow servant 寿命衰减步，避免在朝フェラ/梦遗/遛狗/ENDCHECK 之间多出一层原作没有的前置处理。
- 扶她化事件已收回为原作式交互分支，`EVENT_FUTA_F` 现在在 `TALENT:326 == 1 && EXP:20 >= 150` 时会弹出“要不要扶她化”的输入流程，不再被 Python 当成自动成长检查直接静默处理。
- 漏尿癖事件已补回原作式可见输出，`EVENT_MORASI` 现在会明确打印“当晚，XX尿床了…”以及获得【漏尿癖】的两行提示，而不只是静默给状态加值。
- 媚药禁断的给药分支已补回原作式离队行为，`PRECIPITATE_WITHDRAWAL` 里勇者如果在侵攻中喝下媚药，现在会先陷落并从队伍中移除，再继续后续的药瘾结算，避免只做状态回写而不改变角色流转。
- 已修正 EVENT_NEXTDAY 中 ENTER_ENEMY 的额外生成天数阈值顺序，恢复为与原作一致的 100 / 300 / 500 分段判断，避免 300/500 天条件被前置分支吞掉。
- `FLAG:61` 的日切重置已提前到 `EVENT_NEXTDAY` 对应的位置，避免它晚于次日流程初始化而偏离原作收尾顺序。
- `EVENTTURNEND` 中 `ENTER_ENEMY` 的额外生成阈值已恢复为原作式 `100 / 300 / 500` 分支顺序，不再使用覆盖式判断。
- `NINSIN` 相关的孕育清理边界已继续收紧：`N_FLAG_CLEAR` 不再误清怪物父源/孕育类型位，育儿开始也不再携带额外的状态恢复槽，避免把出生与育儿收尾串成一条。
- 怀孕压力分支中“主人以外父亲关系值”的计算已回调到原作式表达，避免关系值在怀孕崩坏判定里被多算。
- 这轮重新核对后，`NTR_VIDEO` 主分发暂未发现能直接证实的新漏接点；当前先保持原有 helper 拆分，不把尚未证实的差异硬塞回视频链里。
- 示众台日常已补回一层原作式前置可见输出，`_apply_character_daily_pillory_event()` 现在会先打印示众状态与孕期/处女提示，再进入计数与数值结算。
- 示众状态判断已回调到原作的日切日号语义，不再误拿怀孕到期轴去比对 `CFLAG:110`。
- 示众台的口号层已开始独立拆分，`_build_pillory_slogan_lines()` 现在负责原作那种简短示众牌风格的可见文案，避免把这类输出继续揉进计数 helper。
- 这轮复核后确认，`PILLORY` 的种族示众牌映射还不能仅靠现成种族年龄表做薄映射，因此先回退该层过拟合补丁，避免把未证实的族名树硬接进输出。
- 示众状态的日计数已改回总天数语义，`_build_pillory_intro_lines()` 现在按原作那种跨月稳定的全局日号判断临月/出产标签。
- 月祭 `SABBATH` 这轮复核暂未找到可直接证实的新功能缺口，当前实现已基本覆盖原文主分支，先保持现有 helper 分层，不把细微文案差异误判为功能缺失。
- 育儿开始链路已继续按原 ERB 拆分为“开始育儿 / 崩坏换照看者 / 育儿结束”三段，产后清理不再和育儿开始共用同一收尾 helper。
- `NINSIN_MAIN` 已从新日的前置清理流中拆出，改为和原 ERB 一样放在 `FLAG:61` 重置之后、夜袭/处女检查之前执行，避免孕育主链过早触发。
- 孕育主流程已进一步收敛为 `_apply_daily_pregnancy_main_flow`，按原 ERB 的角色串行顺序统一处理意识怀孕、临月转移、到期分娩、育儿结束与育儿中状态展示，避免再走多段全局批处理。
- 已补回临月前 3 天的迎击返回分支，允许临月调教时不再把迎击中的角色误当作统一进育儿室处理，尽量贴近原 ERB 的状态分歧。
- 临月转移的场上槽位清理已补回，当前调教对象/助手在角色被移出当前活动状态后会一并解除，贴近原版 `NINSIN_REACH_TERM` 的收尾效果。
- 育儿开始与换照看者分支已抽出统一的当前选择清理 helper，避免孕育收尾与调教槽位逻辑继续散落在多个分支里。
- 临产与流产的基础值缩放已继续对齐原 ERB 的除法系数，避免怀孕结算把角色体力改得过重。
- `turn_end_processing` 的 new-day 骨架已继续拆分：`process_new_day` 现在只保留日切主流程，`EVENT_NEXTDAY`/晨间事件的调用被重新放回回合结算外层，减少了把新日与回合收尾揉成一层的风险。
- 新日主链已重新合回单一路径，`NINSIN_MAIN` 和 `EVENT_NEXTDAY` 继续由 `process_new_day` 统一调度，避免回合结算里出现重复或分散的入口。
- `turn_end_processing` / `_process_turn_end_new_day` 的职责边界已回调：回合结算负责触发 new-day，日切主链仍由 `process_new_day` 统一输出，避免把 `EVENTTURNEND` 的收尾和日切主体重复展开。
- 重新核对后确认：`EVENT_NEXTDAY` 的原文主体仍需要和夜袭/税收/候补刷新保持一整条线性执行顺序，后续对齐应继续以这条调用骨架为准，避免把主体拆散成多个松散入口。

## 当前目标
继续完善整个游戏系统的 Python 重构，要求尽可能与原始 ERB 行为一致，同时保持解耦，不把功能堆砌在一起。

## 本轮确认
- 已确认 `NOITEM` 在原作里是全局条件开关，但 Python 现有表达式求值会把未识别符号回落为 `0`，因此暂时不需要额外映射。
- `ENDRESET` 的黑方片存在性清理已对齐：`EX_FLAG:2811` 在角色缺席时不再错误保留 `>=300` 的旧状态，和原 ERB 的无条件清零一致。
- `ENDRESET` 的嘉德清理条件已修正为检查 `EX_FLAG:2810` 自身是否达到 `500`，不再误拿 `EX_FLAG:2814` 作为保留依据。
- `ENDCHECKMAIN` 的主线角色轮询已包含 0 号位，不再把魔王自身从 `EX_FLAG:2803` 的候选中排除。
- `ENDCHECKMAIN` 的 500 天游走条件已回调为原作等值判断 `DAY:0 == 500`，不再提前用 `>= 500` 把 `EX_FLAG:2801` 锁成 99，避免结局触发时机比原 ERB 更早。
- 银黑桃离场后的额外等待计数 `92814` 已移除，`EX_FLAG:2814` 的后续推进回到原作那种只依赖既有阶段与随机抽样的方式。
- `ENDRESET` 里银黑桃的缺席保留阈值已回调为原作的 `EX_FLAG:2814 < 300`；嘉德的缺席保留条件也已改回依赖 `EX_FLAG:2814 >= 500`，不再错误地只看 `EX_FLAG:2810` 自身，避免把两条线的存在性清理拆错顺序。
- `ENDCHECKSPADE` / `ENDCHECKSQUARE` 这轮复核后暂未发现新的可证实分支偏差；当前已确认黑方片和银黑桃的阶段推进依旧按原作分段 helper 拆分，接下来应继续从更细的等待阈值与角色状态串联中找差异，而不是只看文案是否齐全。
- `ENDCHECKPRINCESS` 这轮复核后也暂未发现新的可证实偏差；菲娅的白/黑路线在 Python 里已经按原作阶段块做了逐段映射，当前更像是 helper 拆分方式与原文结构不同，而不是阶段推进逻辑本身偏离。
- 菲娅分支中原文注明“移动至 aftertrain”的 160-170 段已继续确认，目前 Python 侧更像是由后续菲娅场景块与结局块承接，尚未找到能证实的漏接入口；这部分先记为待继续核查，而不是立即改动。
- 白梅花与琼相关的 `ENDCHECK` 入口这轮复核后也暂未发现新的可证实偏差，当前实现更接近原作那种标准阶段推进分支，后续应继续从结局块或更细的状态串联里找差异。
- `_refresh_story_presence_flags()` 里嘉德的保留阈值仍保持原作式 `500`，不再提前清空 `EX_FLAG:2810`。
- 菲娅分支的 `160-170` aftertrain 承接已补出一个独立 helper，避免把 `EVENT_AFTERTRAIN` 的阶段推进继续缺失在主 `ENDCHECKPRINCESS` 之外；当前仅对 `EX_FLAG:2807` 的 `160-170` 做推进，不耦合其它训练逻辑。
- aftertrain 承接已进一步收紧为“当前训练目标仍是菲娅”时才推进 `2807:160-170 -> 170`，避免把后处理挂成全局训练收尾而误触其它角色。
- `SELF_CHECK` 后续的百合/自慰/兽奸分支已开始补成独立 aftertrain helper，并把助手对象接入到后处理链里，避免继续把原作的训练后检查漏成单角色占位逻辑；后续仍需继续对照原文补足具体计数规则。
- 百合 aftertrain 已继续补入原作式的 `N` 计数骨架，开始按性癖、品性、关系值与双人加成计算回数，而不是只做简单的毒性自增；自慰与兽奸分支仍需继续按原文细修。
- `SELF_KOJO` 已从空桥接收口到原作 `ERB/EVENT_K*.ERB` 的角色口上片段，并开始按 `IF / ELSEIF / SIF` 的原文结构进行薄执行，避免再把 aftertrain 相关文本留在“只会返回空列表”的壳里。
- 口上桥接层已开始补 `CALLNAME / SAVESTR / SELF_CALL / TFLAG` 等原文占位符，并把 `GameEngine` 的旧壳委托回解释器实现，避免同一入口存在两套互相打架的 `SELF_KOJO`。
- `SELF_KOJO` 这条链路已经补成可闭环的解释器入口，`GameEngine` 现在会先设置口上上下文，再由解释器读取并解析原始 `EVENT_K*.ERB` 片段；同时 `EX_TALENT:903/904` 也已纳入口上编号路由，避免特殊口上继续落到空分发。
- `SELF_KOJO` 的特殊文件路由已经按原作式编号归一：`1003 -> 903`、`1004 -> 904`，避免把 EX 角色的口上块直接当成普通 100 系口上去找。
- 嘉德离场后的“重新拉回场上”辅助恢复已删除，`ENDCHECKGODNESS_SKY_TEMPLE` 只保留原作式的状态推进，不再额外恢复角色实体。
- 已再次核对嘉德天界线的阶段链：`END10_54` 末尾的 `EX_FLAG:2810 += 1`、`END10_55` 末尾的 `EX_FLAG:2810 += 5`，以及后续 `END10_16` / `END10_17` / `END10_18` / `END10_19` 等段落，说明 Python 里对 `2810` 的分段推进是在复用原 ERB 的事件块顺序，而不是自己原创了一条新的推进逻辑。
- 进一步核对后确认，嘉德 540 之后的承接确实是由 `INVASION.ERB` 的 `CALL END10_55` 接入，再由 `END10_16` / `END10_17` / `END10_18` / `END10_19` 继续推进；Python 侧现有的 `stage=540` 事件、`541 <= current < 560` 的侵略完成推进，以及 `GODNESS_EVENT_LINES` 的 540 场景块，和原作事件链一致，没有发现需要额外塞入独立“原创”入口的证据。

## 已完成
- 训练结算已拆成 `_finalize_train_effects()` 等小 helper。
- 训练侧的来源修正、经验后续、掌握度、派生 PALAM 等流程已按原逻辑恢复。
- 孕育流程已拆出独立 helper，包含：
  - 日常怀孕意识判定
  - 临产前育儿室转移
  - 到期分娩
  - 流产
  - NTR 分娩
  - 育儿结束独立
  - 怀孕/育儿状态清理
- `talent[122]` 已按原始逻辑参与受孕判定，不再被错误当成“不能怀孕”。
- `talent[343]` 已纳入妊娠意识阻断。
- 怀孕确认已恢复乳房变化、泌乳、压力/崩坏和体力上限变化。
- 胎儿到期日已从月内日号比较统一为连续天数时间轴 helper。
- `cflag[108]` 的育儿室状态保留问题已修正。
- 怪物生育与子育儿状态重置已做安全处理。
- 当前孕育链路已经重新对照 `ERB/NINSIN.ERB`，主流程与原始脚本的产前转移、临盆、流产、NTR、育儿结束基本对齐。
- 孕育相关时间判断内部已不再直接依赖月内 `day[2]`，改为统一时间轴 helper。
- 本轮已再次清掉孕育系统内部残留的月内日号比较，避免跨月时序失真。
- `EVENT_NEXTDAY` 的新一天顺序已继续对齐：体质变化 / 中毒 / 错位先于孕育主流程，排卵诱发剂清除也回到原作的收尾位置。
- 怀孕意识判定已继续收敛：不再把乳内/精巢/肛内妊娠当成额外的“无法意识怀孕”条件，怪物父亲标记也按原作在意识时统一清理。
- 怪物父亲显示已贴近原作：意识怀孕时会按概率保留具体怪物名，否则才清空来源标记。
- 怀孕确认时的胸部变大提示已补回，和原作 `NINSIN_AWARE` / `N_CHANGE_STATUS` 的表现继续对齐。
- 崩坏角色的育儿开始已拆出独立流，避免继续把“正常开始育儿”与“遗弃/换照看者”堆在同一条路径里。
- 崩坏育儿分流已补成可选照看者的独立 helper，候选人筛选条件也继续贴近原作的“母性 + 非崩坏 + 非妊娠/育儿 + 调教/助手状态”。
- 崩坏育儿候选筛选已复用现有的待命/可调教基线，减少了新旧筛选逻辑的重复分叉。
- 崩坏育儿候选筛选已回调为原作式条件，不再依赖训练系统的通用可调教限制。
- 育儿结束已拆出独立流，孩子离开与母亲恢复不再和怀孕清理混在一起。
- 育儿结束里的母亲/孩子状态清理已再拆出小 helper，避免 departure 自己承担过多收尾责任。
- `CFLAG:274` 已从育儿结束核心路径中移除，避免把亲离开标记扩散成新的全局状态分支。
- 发现并修正了一处全局税收结算误接到孕育时间轴 helper 的回归，避免把月度系统也改偏。
- 育儿结束的孩子实体化时机已向原版靠拢，普通出生不再在到期日提前创建孩子对象，而是延后到离开育儿室时再执行。
- 育儿开始已补回 `CFLAG:1 = 10` 的状态切换，换照看者时也会复制必要的怀孕上下文，避免 departure 时丢失出生信息。
- 媚药中毒的周衰减时机已改回原版的月内日号节奏，避免跨月后断药/成瘾检查错位。
- 该处衰减逻辑已拆成独立 helper，避免把日切判断继续揉进主流程。
- `COM51` 的媚药训练效果已补回原版的残留度增长与断药回避标记，避免训练链和日切中毒逻辑脱节。
- `COM51` 的 `TEQUIP:21` 使用态标记也已补回，和原版“正在使用媚药”的状态保持一致。
- `EVENTTURNEND` 的侵攻生成次数已重新按原作拆回“固定一次 + 按天数追加”的调用结构，避免把 `ENTER_ENEMY` 压成单次上限。
- `ENTER_ENEMY` 的单次生成仍保持独立 helper，不再把日切调度和角色创建逻辑揉在一起。
- 侵攻追加的天数阈值顺序已回调为原作写法，避免把“可读性更好”的重排当成行为修正。
- `EVENTTURNEND` 的 `ENTER_ENEMY` 触发时机已调整到日期推进之后，和原作“先更新日历，再刷新侵攻”的顺序保持一致。
- 跨日进入结算时，`TIME` 已临时回落到原作式的 `1`，避免新日恢复与当天判定继续落在 Python 里的 `2`。
- `ENTER_ENEMY` 的额外生成阈值已改为跟随总天数而不是年份，避免 100/300/500 分段在 Python 中被读成错误的时间轴。
- `EVENT_NEXTDAY` 的主体顺序已重新接回 `process_new_day`：`NINSIN_MAIN` 对应的孕育主链回到新日主流程，次日检查不再只留在晨间入口。
- `EVENT_NEXTDAY` 里的夜袭/处女检查已重新和晨间事件分层，避免把次日主体和朝事件揉成同一个入口。
- 角色日常里原本误挂到 `EVENT_NEXTDAY` 的戒指效果链已移出，改回更接近 `SYSTEM.ERB` 的日常恢复入口，避免和 `PILLORY / SABBATH / NTR_VIDEO` 混在一起。
- 已再次核对 `EVENT_NEXTDAY` / `EVENT_TURNEND` 的线性调用骨架：`FLAG:61` 清理、`NINSIN_MAIN`、处女检查、夜袭、戒指、召唤、设施效果，以及回合结算里的妊娠判定 / `EVENT_NEXTDAY` / 日期推进顺序，目前都与原作保持一致，没有发现新的顺序漂移。
- 已补回回合结束的全员妊娠轮询：`EVENTTURNEND` 现在不再只围绕当前 `TARGET` 做单体受孕结算，而是按原作 `IN_VAGINA_ALL` / `CONCEPTION_CHECK_ALL` 的语义逐角色处理；同时特殊技能检查也只跳过当前训练对象，不再误跳过编号 0 的角色。
- 角色日常的地点状态重置已补回原作式的位置判断，新的戒指状态 helper 只负责恢复链上的装备效果，不再承载 HP/MP 恢复职责。
- `MORNING_FELLATIO` / `NIGHT_STALKING` / 恋人日常共用的床上服务筛选已移除额外的临产怀孕排除，回到原作那种更宽的公共基线。
- 已再次核对育儿结束的满员路径，当前仍保持“先报满员，再走怪物/转化分支”的独立 helper 结构，没有把失败处理继续堆回主流程。
- `CURSE_EQUIP_RING` 的戒指诅咒概率表和提示文案已回调到原作式分布，避免把日切里的戒指转换做成了另一套随机映射。
- `TAX_GET` 中的肉便器税已回调为原作式的 `ITEM:143 / 152 / 182` 直接计数，不再误接到怪物库存统计。
- `MAOU_KOUHO` 的候补筛选已回调为原作式 `EX_TALENT:3` 维度，不再依赖自定义的候补标记。
- 之前把 `MAOU_KOUHO` 挂到玩家爆炸型 gameover 的做法已回退，避免把候补刷新绑定到错误生命周期。
- 日切里额外自动执行的战役维持费已移出，回到原作 `EVENT_NEXTDAY` 注释掉 `RUNNING_COST` 的边界。
- `TAX_GET` 的魔界支援收入已改回按 `DAY:0` 年数计算，不再误用累计总天数。
- 已识别并移除一处把 `MAOU_KOUHO` 错挂到玩家爆炸型 gameover 的过度耦合，避免继续在错误生命周期里刷新候补。
- `MAOU_KOUHO` 的 after-train 悬空封装已清理，避免保留不存在的生命周期入口误导后续对齐。
- 已再次核对 `NINSIN_GIVE_BIRTH` 的边界分流：原版满员时会直接走 `SUMMON_MONSTER` / `SUMMON_MONSTER_MASTER`，当前 Python 也已把满员回退收紧到更接近原作的分流语义，而不是只做单一路径的怪物库存补发。
- 育儿离巢的满员回退已补回与原版接近的“怪物父源/狂王/助手”等分支文案与双胞胎兜底，避免把离巢失败继续压成纯库存写入。
- 魔王本人分娩的怪物数量上限已回调到原作的 1-3 只，避免满员回退在魔王分支里多出一档。
- 已核实 `CSV/Chara/Chara211.csv` 真实存在，而 `200` 并没有对应的角色模板文件；因此 `CHARA_MAKE` 里的 `200-211` 范围不能简单等同于“所有编号都能直接实例化”，后续对齐应继续按资源存在性分流。
- 已收回出生模板的父系兜底：`_choose_birth_child_template_id()` 现在不再偷看父亲模板作为普通出生模板的替代来源，改回更接近原 `GB_ADD_*` 的母系/随机人类模板选择。
- 已把回合结束的角色后处理从新日主链中拆回 `turn_end_processing()`，头发增长、好感衰减与自动处刑现在重新按原作的回合结算时机执行，不再混入 `EVENT_NEXTDAY` 的日切主流程。
- `compileall` 已通过，说明这轮把回合后处理拆回独立 helper 后没有引入语法回归。
- 已回退一处错误的生命周期外溢：`PILLORY / SABBATH / NTR_VIDEO / EVENT_VIDEO_DAY` 保持在 `EVENT_NEXTDAY` 的日切主体中，不再被误放进回合末角色后处理。
- 已把回合结束的特殊技能提示改为先输出再进入后续结算，消息时序重新贴近 `EVENTTURNEND` 原始位置，不影响状态处理。
- `compileall` 再次通过，说明这轮的消息时序修正没有引入新的语法问题。
- 已将侵略度衰减从新日全局流中挪回回合末收尾，和原作 `EVENTTURNEND` 的 `WAIT / LVUP` 后处理时机更接近。
- `compileall` 再次通过，说明这轮把侵略度衰减改回回合末后没有引入语法问题。
- 已复核 `CHECK_SPECIALSKIL` 的消息输出时机，当前 Python 仍保持在回合主结算前打印，未发现可证实的时序漂移。
- 已复核 `FLAG:61` 的日切清理位置，当前 Python 的 `_reset_daily_shop_flags()` 仍对齐 `EVENT_NEXTDAY` 中熏香计数清空的位置。
- 已补回日期推进时的总天数更新：`_advance_calendar_day()` 现在同时递增 `DAY[0]`，避免 `ENTER_ENEMY` 等依赖总天数的系统继续漂移。
- `compileall` 已通过，说明这轮补回总天数推进后没有引入语法问题。
- 已复核 `PILLORY / SABBATH / NTR_VIDEO / EVENT_VIDEO_DAY` 的日切角色流位置，当前 Python 的分层仍与原作 `EVENT_NEXTDAY` 中的 per-character 处理一致，未发现可证实时序漂移。
- 已复核月末/月初文案与跨年推进位置，当前 Python 的 `_advance_calendar_month()` 仍与原作 `EVENT_NEXTMONTH` 的提示顺序一致，未发现可证实时序漂移。
- 已将侵略度衰减从回合恢复之后拆回更早的 world decay cycle，当前顺序更接近原作 `EVENTTURNEND` 中 `WAIT / LVUP` 后的先衰减、后回血。
- `compileall` 已通过，说明这轮回合末世界衰减顺序调整后没有引入语法问题。
- 已把跨日后处理从通用回合结算中拆出去，`_apply_turn_end_new_day_cycle()` 现在只在 `TIME == 1` 的新日分支执行。
- `compileall` 已通过，说明这轮把跨日后处理独立出来后没有引入语法问题。
- 已将回合恢复收回到玩家专属逻辑，恢复值改回原作 `EVENTTURNEND` 中的 1400 / 1000 与战役惩罚 -10。
- `compileall` 已通过，说明这轮恢复逻辑回调后没有引入语法问题。
- 已补回 `ENTER_ENEMY` 的两层重复骨架：先按 `DAY >= 100 / 300 / 500` 追加单次调用，再按 `EX_FLAG:9012` 计算循环生成次数。
- 已补回 `ENTER_ENEMY` 的原作式多次调用骨架，额外生成次数现在按 `DAY >= 100 / 300 / 500` 的阈值顺序计算，不再漏掉原作里那层重复触发。
- 已补回 `NTR_CHILD_BIRTH` 后的 `NTR_KOUJO` 分发层，确保 NTR 分娩收尾不再只有固定文案而没有角色口上入口。
- `NTR_CHILD_BIRTH` 口上已从自造固定文案收回为更接近原作的角色分发实现，当前只保留已能从原文证实的 `P == 20` 方向。
- 已再次核对 `NTR_CHILD_BIRTH` / `NTR_KOUJO`：出生入口文本已收回为原作式“从狂王处收到了水晶球。”，`K0` 保留公开出产的 `P == 20` 文案，而 `K5` / `K19` 的 `P == 20` 仍保持空分支，与原 ERB 对齐。
- 已把“再生的处女膜因为生产而破损了……”挪回分娩成功后的收尾位置，避免育儿开始 helper 承担出生状态变化，顺序更贴近 `NINSIN.ERB` 原文。
- 已把育儿崩坏/非崩坏的换照看者提示拆开，避免 `CHILD_CARE_CHANGE_NURSE` 一律使用崩坏口吻，候选交互更接近原作分支。
- 已把育儿结束的 `N_RESET_STATUS` 收尾重新收回外层调用，`_resolve_child_care_depart()` 只负责孩子生成/离开动作，结构更贴近 `CHILD_CARE_DEPART` 原文。
- 已收紧出生孩子模板选择，去掉不必要的父系模板临时推断，让 `NINSIN_GIVE_BIRTH` 的子代生成更贴近原始 `GB_ADD_*` 分流。
- 已把 `EVENTTURNEND` 里的 `ENTER_ENEMY` 额外生成计数分支顺序收回原文写法，避免 Python 继续沿着“更合理”的顺序改变行为。
- 已复核分娩后状态清理与育儿开始 helper，当前未发现可直接证实的新偏差，先保持现有解耦结构不再扩大改动面。
- 已复核 `EVENT_NEXTDAY` 的主体时序与孕育主链，当前未发现新的硬偏差，先维持现有分层结构不再增加新封装。
- 已补回回合结束入口的调试输出，`turn_end_processing()` 现在会先打印和原 ERB 一致的回合状态行。
- 已把回合结束调试输出里的 `DAY` 展开成具体年月日格式，避免 Python 直接打印内部对象结构。
- 已修正角色移除后的 `TARGET` 回写：当被删角色正好是当前调教对象时，现在会按原版语义归空，而不会强行切到 1 号位。
- 已修正回合末超载异常的侧 victim 选择，删除主 victim 后改为按当前对象身份排除，避免继续沿用旧索引误伤不该排除的角色。
- 已修正怪物分娩后的状态回收：`_apply_monster_birth_status_reset()` 现在无条件清空 `CFLAG:1`，和原作 `NINSIN_GIVE_BIRTH` 的分娩后状态收尾保持一致。
- 已补回妊娠相关缓存清理里的父亲字符串字段，`_clear_pregnancy_tracking_flags()` 现在会同步清空 `CSTR:2`，避免怀孕来源残留到后续检查。
- 已顺手去掉 `_clear_pregnancy_tracking_flags()` 里重复的 `CSTR:2` 清理，行为不变，只是把冗余收敛回单次写入。
- 出生模板选择已回调得更贴近原作 `GB_ADD_GUARD`：魔王父系不再优先跳到 200 系模板，优先维持原母体模板与普通人类模板池的一致性。
- `ENTER_ENEMY` 的 100/300/500 天阈值分支已按原作写法收回为线性可达顺序，避免分支判断继续漂移到错误顺位。
- 育儿离巢链路已回收为更干净的原作式动作层，离巢只保留原本的提示、孩子生成与状态清理，不再额外堆叠独立口上支线。
- NTR 分娩口上已移除 Python 里额外落下的 `CFLAG:650` 写入，避免原作没有的专用状态旗标在收尾后残留。
- 普通分娩的怪物分支收尾顺序已重新贴近原文，先做怪物分娩状态回收，再进入结果/清理链，避免状态可见性继续漂移。
- 育儿离巢已回到更贴近原文的动作流，不再把“孩子要离开”的情绪句额外挂进独立 helper，避免同一入口重复叠加口上层。
- 育儿离巢的 `CFLAG:1` 回收已合并回成功分支，状态清理现在跟随孩子成功离开育儿室的时机，而不是再单独走一个清理 helper。
- 普通分娩的孕育清理已重新放回育儿开始前，避免 Python 把 `N_RESET_STATUS` 对应的状态回收继续拖到更后面的子流程里。
- 已复核回合末宝库/超载异常触发链，当前未发现新的硬偏差，继续保持现有模块化分层。
- 已补回月末跨年年龄回写：`_advance_character_age_year()` 现在会在 `cflag[452]` 自增后，按种族规则同步回写 `cflag[451]`，贴近 `EVENT_NEXTMONTH.ERB` 的原版流程。
- 已修正新日入口的晨间事件时机：`_process_new_day()` 不再提前触发 `@EVENT_NEWDAY` 对应事件，晨间事件继续只在商店入口的 pending 链路中执行，避免重复跑一遍。
- 已修正 `OFFERVIRGIN_CHECK` 评分末尾的素质判断：`TALENT:28` 现在回到原版对应位置，避免 Python 把 `TALENT:27` 重复算了两次。
- 已复核 `EVENT_NEXTDAY` 的角色日常主链，`PILLORY / SABBATH / NTR_VIDEO / EVENT_VIDEO_DAY / KARMA / FAITH` 对应函数都已在 Python 里存在；`SABBATH_DAY` 已确认是原始 `EVENT_SABBATH.ERB` 里的独立备用标签，原版 `EVENT_NEXTDAY` 不会直接调用它。
- 已继续核对 `EVENT_FUTA_F / EVENT_MORASI / EVENT_YOUJI / EVENT_MAZOKU` 等原版独立入口；当前 Python 中对应的日常检查函数都已存在，暂未找到可直接证实的新漏接点，继续向更深层状态分支推进。
- 已补正魔族化判定里的排除素质，`_apply_daily_mazoku_transformation_checks()` 现在回到原版的 `魂缚(274)` 过滤，不再误把 `魔王之影(292)` 当成魔族化阻断条件。
- 已补回幼儿退行的原作式消息流，`_apply_daily_dematurity_regression_state()` 现在会逐项输出消失素质、补回 `漏尿癖` 提示，并打印 `反抗刻印` 归零信息，和原版 `EVENT_YOUJI` 的可见行为更一致。
- 已把魔族化的输出演出补回原作式多行文本，`_apply_daily_mazoku_transformation_checks()` 现在会按原版分支打印魔族化过程、魅惑/铠破坏结果与空行分隔，不再只留一条简化摘要。
- 已核实魔族化的 `ITEMNAME:(TALENT:现种族)` 走的是 `CSV/Item.csv`，`132 / 140 / 152` 分别对应 `小恶魔 / 下等恶魔 / 魅魔`，因此魔族化输出已回调为真正的物品名表而不是素质名表。
- 已补回媚药禁断症状里的服药交互，`_apply_daily_aphrodisiac_withdrawal()` 现在会在背包存在 `媚药` 时先走一次独立 prompt，再继续后续症状结算，避免把原作 `EVENT_ADDICT` 的道具分支整段漏掉。
- 已回调媚药服用后的分支边界，`_apply_daily_aphrodisiac_withdrawal()` 现在在选择服药后会像原作一样直接结束本次禁断事件，避免把道具分支补成继续叠加后续症状的半对齐状态。
- 已修正媚药给药分支的残留度回写，服药后现在会按原作先把 `CFLAG:31` 加 1 再结束事件，同时去掉了 Python 自己补出来的“症状暂时缓和”提示。
- 已补回媚药给药时的可见演出，`_prompt_aphrodisiac_withdrawal_item_use()` 现在会按原作补出“抢过瓶子并喝下去”的两行文本，而不是只改状态不出画面。
- 已收紧 `ONESHO` 的导尿配件分支，`_apply_onesho_event_for_character()` 现在在满足导尿条件时会直接停在导尿结算，不再继续落到普通尿床分支，避免把原作里该静默跳过的状态改成双重事件。
- 已再次复核 `EVENT_FUTA_F` 与 `SOUL_DISLOCATION` 的原文入口，当前 Python 的触发门槛、输入分支、EX_TALENT 递减与归零提示都与原 ERB 对齐，暂未发现需要继续补的硬缺口。
- 已开始补 `PILLORY` 的身份口号层，先把原作里明显存在的扶她、男体、肌肉、巨乳、怀孕、大小姐等标签回填到独立 helper，避免示众台只剩少量身份牌可见文本。
- 已回退 `PILLORY` 里对扶她阴茎状态的误用字段，先保留可直接从现有数据结构读取的短句，避免把输出层补成不稳定的运行时访问。
- 已整理 `PILLORY` 身份口号 helper 里的重复短句，先把明显重复的胸部/怀孕/贫乳相关标签收敛，避免输出层越补越乱。
- 已继续收紧 `PILLORY` 的身份口号层，这次把原作里能证实的恋母/恋父/萝莉控/正太控、体型/胸部/怀孕和职业随机短句拆回独立分支，并把扶她阴茎状态改回读 `TALENT:318`，避免继续把示众台写成静态标签堆。
- 已继续拆 `PILLORY` 的计数来源，`_get_pillory_daily_counts()` 现在按处女、菊花专用、兽奸、贞操带和普通等原作主条件分流，再通过独立 helper 组装计数包，避免把原本的条件树压成一坨统一随机数。
- 已继续拆 `PILLORY` 的结算呈现，兽奸、A&V 和肛交的施加者称呼现在走独立 helper，不再把不同场景塞进同一段大分支里，后续再继续补台词细节会更稳。
- 已继续补 `PILLORY` 的怀孕展示，临月 / 怀孕中 / 未怀孕三段现在有单独 helper，避免示众台只剩总计数而丢掉原作里先看孕期状态再看涂鸦的顺序。
- 已继续补 `PILLORY` 的正字记号展示，`661-665` 的累计次数现在会走独立 helper 输出类别标签与“正字”进度，不再只剩一条总计数摘要。
- 已把 `PILLORY` 的施加者抽样回调到更接近原作的 `0-4` 分布，并把扶她固定为原文式的第二号施加者，避免继续把兽奸 / A&V 的默认态压扁成 1-4 的简化随机。
- 已把 `PILLORY` 的高计数记号收束成“特殊称号 + 正字”并存，`661` 超过 10/30/50/100 时不再提前吞掉正字结果。
- 已修正公开视频日的结算边界，`_apply_character_event_video_day()` 现在会像原作 `EVENT_VIDEO_DAY` 一样无条件回收视频收益，即使标题为空也不会漏掉金钱入账。
- 已把 `EVENT_AFTERTRAIN.ERB` 的后调教三段检查继续往 Python 里对齐，当前已经补到“条件门槛 -> 次数计算 -> EXP/JUEL 结算”的主干，后续主要剩余的是更细的输出句式和个别原文边角差异。
- 已确认这次 aftertrain 对齐是基于原始 `ERB/EVENT_AFTERTRAIN.ERB` 手工补出来的，不是现成项目逻辑直接搬运；当前 Python 只是把原版行为映射进了现有解释器框架。
- 目前仍在继续核对 `SELF_CHECK` 里前半段的普通性交/肛交后调教主链，避免只把百合/自慰/兽交三段补齐而遗漏掉更基础的训练后结算。
- 当前已开始收回 `SELF_CHECK` 前半段里我额外加重的条件，避免把原文里的后调教触发标准“优化”成另一个版本。
- 已确认仓库里没有现成的通用 `SELF_KOJO` 执行层可以直接复用，因此当前 aftertrain 仍保持为独立 hook，并继续借用现有输出/奖励管道逐步贴近原作表现。
- 已把 aftertrain 的百合段补回“调教结束之后”的可见提示，让 `SELF_CHECK` 的三段后续输出顺序更接近原文。
- 当前这轮 aftertrain 对齐已经过 `py_compile`，没有引入新的语法问题。
- 已回收 aftertrain 百合段的开头提示，现在会按原文在“主人出去之后 / 调教结束之后”之间切换。
- 已修正 aftertrain 兽交段的朝日报告奖励计数，避免误把兽交次数直接拿去替代原文的结算语义。
- 已把兽交分支末尾的朝日报告奖励回调到原文式的旧计数来源，避免 Python 继续用兽交次数替代前一段自慰计数。
- 已把兽交分支末尾的朝报输出收紧回原文式的单层提示，避免奖励结算继续额外插入解释性说明。
- 已把 aftertrain 四段的分隔线输出收回各自正文前，保持原文里“分段 -> 正文 -> 结算”的节奏。
- 已把 aftertrain 的百合/自慰/兽交可见句式重新压回原文的前后续写风格，避免换行把一句口上切成两段。
- 已把育儿离巢的 `SELF_KOJO` 入口补回到独立 helper，时机对齐为“离开孩子前先口上，再做出生/清理”。
- 已确认 Python 侧当前没有独立的 ERB 级 `SELF_KOJO` 函数执行器，只有函数注册表和各类 Python 口上辅助输出。
- 当前要继续沿现有结构补最小口上分发层，避免把 aftertrain 直接堆进训练主流程。
- 目前还没找到能直接复用的统一 `SELF_KOJO` 文本 helper 集群，所以后续只能先补极薄分发层，再逐个接回具体口上文本。
- 现阶段 aftertrain 主链已经稳定到可继续验证的程度，后续口上桥接会独立推进，避免和奖励结算再混在一起。
- 已确认此前试探性的 `_run_self_kojo` 没有真实调用点，属于无效壳，已经移除以保持代码边界干净。
- 已补回一个最小的 `SELF_KOJO` 空分发层，并把它挂到 aftertrain 的 sex / lesbian / masturbation 入口上，后续可逐个填入口上文本而不再污染结算逻辑。

## 正在对齐
- 继续核对 `ERB/NINSIN.ERB` 的边角措辞和少量状态细节，重点是：
  - 育儿结束链路里母亲/孩子状态清理是否还和原作存在细微时序差异
  - NTR 分娩和怪物分娩的收尾文案
  - 其他系统里是否还有类似的时间轴错位
  - `EVENTTURNEND` 里剩余的世界推进顺序是否还有和原作不一致之处
- 继续核对 `EVENT_TURNEND` / `EVENT_NEXTDAY` 的剩余分支与原作细节，寻找仍未证实对齐的系统入口。
- 继续细化 `EVENT_AFTERTRAIN.ERB` 的后调教文本与奖励换算，尤其是原文里 `SELF_CHECK` 触发顺序、`SELF_KOJO` 回调和三段结算文案的可见输出。

## 风险点
- 目前旧的 `todo.md` 仍是历史任务记录，不能当作当前实时进度。
- 需要继续用原始 `ERB/NINSIN.ERB` 逐段对照，避免只修到“看起来差不多”的状态。
- 目前实时进度只覆盖孕育子系统的最新状态，整套游戏系统的剩余模块还要继续按同样方式维护。
- `ENTER_ENEMY` 的可见输出仍需要结合运行时再确认，但调度次数已经回到原作结构。

## 下一步
1. 运行语法检查。
2. 做几组针对性行为验证。
3. 如果还发现对齐差异，继续按 helper 颗粒度补齐。

## 本轮新增
- 修正 `EVENT_AFTERTRAIN` 兽交段朝日报告的珠经验结算，原文这里按兽交回数 `B` 计数，Python 侧之前误用了自慰段的回数变量。
- 补回 `SELF_CHECK` 头部两个原作式早退：调教对象为空直接返回，以及失神结束时跳过后续 aftertrain 检查。
- 将正常分娩后的 341/342/343 出生形态标记清理拆成独立 helper，并只挂到正常出生分支上，避免流产/怪物分娩共用一段状态清理。
- 校正出生场所前缀文案里“通过”/“经由”的字面差异，让 `CHILD_BIRTH_PLACE` 的输出重新贴近原文短句。
- `NTR_VIDEO` 的各个播放分支重新挂回原作式 `CALL NTR_KOUJO` 口上输出，避免只保留数值结算而丢掉视频剧情文案。
