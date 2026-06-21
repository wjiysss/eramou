"""ERB 游戏知识整理：供 RAG 静态索引使用。

两类：
- 天赋说明：从 CSV/Talent.csv 解析（id,名称,;说明）
- ERB 机制文档：手写中文说明（调教/JUEL/ABL/口上/地城等关键机制）
"""
from __future__ import annotations

import csv
import os
from typing import Any


def _talent_csv_path(erb_dir: str) -> str:
    return os.path.join(erb_dir, "CSV", "Talent.csv")


def parse_talent_csv(erb_dir: str) -> list[tuple[int, str, str]]:
    """返回 [(id, 名称, 说明), ...]。说明为空则跳过。"""
    path = _talent_csv_path(erb_dir)
    out: list[tuple[int, str, str]] = []
    if not os.path.exists(path):
        return out
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                first = (row[0] or "").strip()
                if first.startswith(";") or not first.isdigit():
                    continue
                try:
                    tid = int(first)
                except ValueError:
                    continue
                name = (row[1] or "").strip()
                note = ""
                for cell in row[2:]:
                    c = (cell or "").strip()
                    if c.startswith(";"):
                        note = c.lstrip(";").strip()
                        break
                if not note:
                    continue
                out.append((tid, name, note))
    except Exception as e:
        print(f"[erb_knowledge] 解析 Talent.csv 失败: {e}")
    return out


# 关键 ERB 机制中文说明（基于代码库调研整理）
ERB_MECHANIC_DOCS: list[str] = [
    "【口上系统】talent[160-175] 决定角色口上编号（KOJO_NUM = talent编号 - 60）。160慈爱/161自信家/162懦弱/163高贵/164冷静/166恶女/172智慧/173庇护者/174贵公子/175伶俐。每个性格对应 EVENT_Kxx.ERB 专属台词模板。性格天赋同时驱动善恶值初始化、自称决定、联动素质。",
    "【性格天赋·高贵(163)】参与 JUEL（屈服/耻情）收益加成，与处女/高姿态/保守的/看重贞操同组提升屈服JUEL获取率（EVENT_NEXTDAY.ERB）。善恶值偏善(+10~+29)，自称教育+10姿态+10，联动刚强/嚣张素质。卖身文案相关。",
    "【性格天赋·冷静(164)】地城垃圾战额外掉落+10（dungeon_ext.py）。善恶值中立(-20~+19)，自称教育+5，联动刚强/嚣张。地城探索决策：与自信家/高贵/恶女同列触发直奔最深层。",
    "【性格天赋·智慧(172)】ABL 升级成本×0.80（ABLUP100.ERB）。自称姿态+5开放+3。是提升调教对象能力的高性价比性格。",
    "【性格天赋·慈爱(160)】圣女语气，第一人称=私，宽容怜悯试图感化对方。善恶值偏善(+40~+69)，与庇护者同档。联动胆怯/文静/软弱素质。",
    "【性格天赋·懦弱(162)】第一人称卑怯，胆小爱哭。自称姿态-5教育-3。联动胆怯/文静/软弱，ABL顺从更易提升。",
    "【JUEL 屈服/耻情】调教核心资源。受处女/高姿态/保守的/看重贞操/高贵加成。屈服JUEL用于提升ABL顺从，耻情JUEL用于提升服从相关。",
    "【ABL 系统】能力等级：顺从/侍奉精神/技巧/欲望等。升级消耗JUEL与金钱。坦率(13)/低姿态(17)使顺从与侍奉精神更易提升；高姿态(15)/嚣张(16)使其更难。智慧(172)降低全部ABL升级成本20%。",
    "【PALAM 参数】调教中变动：恭顺/欲情/屈服/恐怖/反感/习得。胆怯(10)/文静(14)使反感上升慢；好奇心(23)使习得上升快；克制(20)/冷漠(21)使多种PALAM上升慢。",
    "【调教指令】TRAIN状态下对target执行。反抗心(11)/刚强(12)/高姿态(15)/保守的(24)使指令更难执行；坦率(13)/低姿态(17)/好奇心(23)使指令更易执行。傲娇(18)在顺从4以上时反抗心变为坦率。",
    "【魔王设定】chars[0]是玩家=魔王。得到不死之力，受'只会被女性打倒'的诅咒，曾被女勇者封印，今日苏醒。默认21岁，HP10000，talent[200]=魔王标签。玩家可自定义名字/性别(男/女/扶她)/年龄/肉棒尺寸。",
    "【狂王】葵希罗(Chara34)，地方领主，继承封印魔王的勇者血脉，意图再次封印魔王。HP60000，素質2=狂王替身。是魔王的主要对手。",
    "【调教对象】固定为人类女性（魔王诅咒）。原型archetype对应职业模板：村娘(17)/女战士(1)/魔法师(2)/女神官(3)/盗贼(4)/女骑士(5)/巫女(6)/忍者(7)/弓手(8)。talent[314]=种族(0人类)。",
    "【独特NPC】165玛奥(村娘A)/167金红桃/168银黑桃/169黑方片/170白梅花/171村娘B莉莉 为稀有角色，售价+400。170白梅花独特体质：爱液生成×0.10。",
    "【场景规则】SHOP=地下城商店街/经营区（调教对象不在眼前，在监牢）；TRAIN=监牢/调教室（target在场）；START=王座厅/封印之地。SHOP下提及target只能用心理活动（想起/盘算），不能跨场景感知监牢。",
]


def build_static_knowledge(erb_dir: str) -> list[tuple[str, str, dict]]:
    """返回 [(text, source, metadata), ...] 供 RAGSystem.build_static_if_needed 使用。"""
    items: list[tuple[str, str, dict]] = []
    # 天赋说明
    for tid, name, note in parse_talent_csv(erb_dir):
        text = f"天赋 {name}({tid})：{note}"
        items.append((text, "talent", {"id": tid, "name": name}))
    # ERB 机制文档
    for doc in ERB_MECHANIC_DOCS:
        items.append((doc, "erb", {}))
    return items
