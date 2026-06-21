from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class PersonalityProfile:
    core_traits: List[str] = field(default_factory=list)
    dialogue_style: List[str] = field(default_factory=list)
    tone: List[str] = field(default_factory=list)
    demeanor: List[str] = field(default_factory=list)
    resistance: List[str] = field(default_factory=list)
    vulnerability: List[str] = field(default_factory=list)


_TRAIT_DICT = {
    "慈爱": {"core": "慈爱", "dialogue": "语气温软，用词体贴", "tone": "温和包容", "demeanor": "垂眸微笑，肢体放松", "resistance": "试图感化而非对抗，忍让", "vulnerability": "见他人受苦、被利用善意"},
    "温柔": {"core": "温柔", "dialogue": "语速舒缓，措辞柔和", "tone": "温婉", "demeanor": "眉眼含笑，动作轻柔", "resistance": "羞怯顺从，不敢直视", "vulnerability": "被粗暴对待、孤独"},
    "堕落": {"core": "堕落", "dialogue": "圣洁语调夹杂淫靡暗示", "tone": "圣洁与淫荡交织", "demeanor": "表面端庄，暗自战栗扭动", "resistance": "嘴上谴责，身体迎合", "vulnerability": "被唤醒的沉沦记忆、快感累积"},
    "傲慢": {"core": "傲慢", "dialogue": "居高临下，用词矜贵", "tone": "冷傲矜持", "demeanor": "下巴微扬，眼神睥睨", "resistance": "宁死不屈，言语讥讽", "vulnerability": "尊严被践踏、被当作玩物"},
    "高贵": {"core": "高贵", "dialogue": "措辞典雅，礼节周全", "tone": "端庄矜持", "demeanor": "脊背挺直，仪态万方", "resistance": "据理力争，维护体面", "vulnerability": "家族名誉、被当众羞辱"},
    "冷酷": {"core": "冷酷", "dialogue": "惜字如金，直击要害", "tone": "冰冷疏离", "demeanor": "面无表情，目光如刀", "resistance": "沉默以对，无动于衷", "vulnerability": "罕见的温情被触动"},
    "懦弱": {"core": "懦弱", "dialogue": "结结巴巴，语带哭腔", "tone": "怯懦颤抖", "demeanor": "缩肩低头，眼神闪躲", "resistance": "哭泣求饶，轻易屈服", "vulnerability": "暴力威胁、黑暗、孤独"},
    "病娇": {"core": "病娇", "dialogue": "甜蜜呢喃夹杂占有宣言", "tone": "病态痴迷", "demeanor": "笑中带泪，紧抓不放", "resistance": "以爱为名主动迎合，排斥他人", "vulnerability": "被忽视、情敌出现"},
    "天然呆": {"core": "天然呆", "dialogue": "慢半拍，常会错意", "tone": "天真懵懂", "demeanor": "歪头眨眼，一脸茫然", "resistance": "根本没意识到危险，误打误撞", "vulnerability": "被欺骗、智力碾压"},
    "三无": {"core": "三无", "dialogue": "极简回应，几不主动", "tone": "平淡无波", "demeanor": "面无表情，静立如偶", "resistance": "无反应即最大抵抗，难以撼动", "vulnerability": "记忆碎片、特定触发词"},
    "元气": {"core": "元气", "dialogue": "语速快，活力十足", "tone": "热情开朗", "demeanor": "蹦跳挥手，眼睛发亮", "resistance": "叫嚷反抗，越挫越勇", "vulnerability": "被否定、同伴受伤"},
    "腹黑": {"core": "腹黑", "dialogue": "笑里藏刀，话中有话", "tone": "阴柔算计", "demeanor": "微笑掩眸，指尖轻扣", "resistance": "表面顺从暗中布局，反客为主", "vulnerability": "算计被识破、失去掌控"},
    "智慧": {"core": "智慧", "dialogue": "逻辑严密，引经据典", "tone": "理性沉稳", "demeanor": "托腮凝思，目光深邃", "resistance": "据理力争，寻找破绽", "vulnerability": "认知被颠覆、无力回天"},
    "魅惑": {"core": "魅惑", "dialogue": "声线撩拨，意味深长", "tone": "妖艳暧昧", "demeanor": "眼波流转，身段妖娆", "resistance": "以媚态化解，反客为主", "vulnerability": "真心被触动、失去魅力"},
    "慵懒": {"core": "慵懒", "dialogue": "拖长尾音，半句懒说", "tone": "倦怠慵懒", "demeanor": "倚靠支撑，眼皮半垂", "resistance": "懒得反抗，顺水推舟", "vulnerability": "被迫活动、美梦被打断"},
    "自信": {"core": "自信", "dialogue": "语气笃定，不容置疑", "tone": "强势昂扬", "demeanor": "挺胸抬头，目光炽热", "resistance": "正面硬刚，绝不低头", "vulnerability": "实力被碾压、信念崩塌"},
    "圣女": {"core": "圣洁", "dialogue": "祷词般的庄重语调", "tone": "圣洁悲悯", "demeanor": "双手交握，目光澄净", "resistance": "以信仰支撑，祈求宽恕", "vulnerability": "信仰动摇、被玷污"},
}

_STOPWORDS = {"的", "但", "是", "一个", "内心", "阴暗", "既", "又", "夹杂", "和", "与", "了", "很", "非常", "有些", "有点", "比较", "那种", "这个", "那种", "她", "他", "我", "你"}


def profile_personality(text: str) -> PersonalityProfile:
    profile = PersonalityProfile()
    if not text or not text.strip():
        profile.core_traits = ["未知"]
        profile.dialogue_style = ["待玩家演绎"]
        profile.tone = ["待玩家演绎"]
        profile.demeanor = ["待玩家演绎"]
        profile.resistance = ["待玩家演绎"]
        profile.vulnerability = ["待玩家演绎"]
        return profile

    text_low = text.lower()
    hit_any = False
    for key, dims in _TRAIT_DICT.items():
        if key in text or key.lower() in text_low:
            hit_any = True
            if dims["core"] not in profile.core_traits:
                profile.core_traits.append(dims["core"])
            profile.dialogue_style.append(dims["dialogue"])
            profile.tone.append(dims["tone"])
            profile.demeanor.append(dims["demeanor"])
            profile.resistance.append(dims["resistance"])
            profile.vulnerability.append(dims["vulnerability"])

    contradiction_markers = ["矛盾", "既", "又", "夹杂", "交织", "混合", "同时", "却又", "然而"]
    if any(m in text for m in contradiction_markers) and "矛盾" not in profile.core_traits:
        if len(profile.core_traits) >= 2 or hit_any:
            profile.core_traits.append("矛盾")

    if not hit_any:
        import re
        remaining = text
        for sw in _STOPWORDS:
            remaining = remaining.replace(sw, " ")
        tokens = [t for t in re.split(r"[\s，。、,\.]+", remaining) if t and len(t) >= 2]
        seen = set()
        for t in tokens[:4]:
            if t not in seen:
                profile.core_traits.append(t)
                seen.add(t)
        if not profile.core_traits:
            profile.core_traits = ["独特"]
        profile.dialogue_style = ["待根据性格演绎"]
        profile.tone = ["待根据性格演绎"]
        profile.demeanor = ["待根据性格演绎"]
        profile.resistance = ["待根据性格演绎"]
        profile.vulnerability = ["待根据性格演绎"]

    return profile


def to_narrative_block(profile: PersonalityProfile) -> str:
    def join(items: List[str]) -> str:
        seen = []
        for x in items:
            if x not in seen:
                seen.append(x)
        return " / ".join(seen)

    lines = [
        f"核心特质: {join(profile.core_traits)}",
        f"对话风格: {join(profile.dialogue_style)}",
        f"语气基调: {join(profile.tone)}",
        f"神态举止: {join(profile.demeanor)}",
        f"对抗反应: {join(profile.resistance)}",
        f"脆弱点: {join(profile.vulnerability)}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    for t in [
        "慈爱但内心阴暗的堕落圣女",
        "温柔的村姑",
        "病娇",
        "慵懒的猫娘",
        "神秘的异世界旅人",
        "",
    ]:
        print(f"=== {t or '(空)'} ===")
        print(to_narrative_block(profile_personality(t)))
        print()
