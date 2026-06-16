from __future__ import annotations

import json
import mimetypes
import re
from dataclasses import dataclass, field
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from random import Random, randrange
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = ROOT / "web-prototype"
HOST = "127.0.0.1"
PORT = 4307


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def load_train_names() -> dict[int, str]:
    names: dict[int, str] = {}
    for raw_line in read_text(ROOT / "CSV" / "Train.csv").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split(",", 2)
        if len(parts) < 2:
            continue
        try:
            command_id = int(parts[0])
        except ValueError:
            continue
        name = parts[1].strip()
        if name:
            names[command_id] = name
    return names


def load_item_catalog() -> dict[int, dict[str, int | str]]:
    catalog: dict[int, dict[str, int | str]] = {}
    path = ROOT / "CSV" / "Item.csv"
    if not path.exists():
        return catalog
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split(",", 3)
        if len(parts) < 3:
            continue
        try:
            item_id = int(parts[0])
        except ValueError:
            continue
        name = parts[1].strip()
        try:
            price = int(parts[2])
        except ValueError:
            price = 0
        if name:
            catalog[item_id] = {"name": name, "price": price}
    return catalog


def load_csv_names(filename: str) -> dict[int, str]:
    names: dict[int, str] = {}
    path = ROOT / "CSV" / filename
    if not path.exists():
        return names
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split(",", 2)
        if len(parts) < 2:
            continue
        try:
            item_id = int(parts[0])
        except ValueError:
            continue
        name = parts[1].strip()
        if name:
            names[item_id] = name
    return names


def parse_erb_case_targets(text: str) -> list[tuple[int, int]]:
    targets: list[tuple[int, int]] = []
    for item in text.split(","):
        part = item.strip()
        range_match = re.fullmatch(r"(-?\d+)\s+TO\s+(-?\d+)", part, flags=re.IGNORECASE)
        if range_match:
            targets.append((int(range_match.group(1)), int(range_match.group(2))))
            continue
        if re.fullmatch(r"-?\d+", part):
            value = int(part)
            targets.append((value, value))
    return targets


def parse_erb_plain_value(line: str, keyword: str) -> str:
    text = line.split(keyword, 1)[1].strip()
    if not text or any(marker in text for marker in ("(", ")", "%", "{", "}", '"')):
        return ""
    return text


def load_erb_function_lines(path: Path, function_name: str) -> list[str]:
    if not path.exists():
        return []
    lines = read_text(path).splitlines()
    marker = f"@{function_name}"
    in_function = False
    function_lines: list[str] = []
    for raw_line in lines:
        line = raw_line.rstrip("\n")
        if raw_line.strip().startswith(marker):
            in_function = True
            continue
        if in_function and raw_line.strip().startswith("@"):
            break
        if in_function:
            function_lines.append(line)
    return function_lines


def load_replace_array_initial_values(array_name: str, fallback: list[int]) -> dict[int, int]:
    path = ROOT / "CSV" / "_replace.csv"
    values = list(fallback)
    if path.exists():
        pattern = re.compile(rf"^\s*;?\s*{re.escape(array_name)}の初期値\s*,\s*(.+?)\s*$")
        for raw_line in read_text(path).splitlines():
            match = pattern.match(raw_line)
            if not match:
                continue
            parsed: list[int] = []
            for part in match.group(1).split("/"):
                text = part.split(";", 1)[0].strip()
                if text == "":
                    continue
                try:
                    parsed.append(int(text))
                except ValueError:
                    parsed = []
                    break
            if parsed:
                values = parsed
                break
    return {index: value for index, value in enumerate(values)}


def load_look_info_tables() -> dict[str, list[tuple[int, int, str]]]:
    """Extract simple SELECTCASE display tables from ERB/LOOK.ERB."""
    path = ROOT / "ERB" / "LOOK.ERB"
    tables: dict[str, list[tuple[int, int, str]]] = {}
    if not path.exists():
        return tables

    lines = read_text(path).splitlines()
    in_get_look = False
    current_key = ""
    current_cases: list[tuple[int, int]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("@GET_LOOK_INFO"):
            in_get_look = True
            current_key = ""
            current_cases = []
            continue
        if in_get_look and line.startswith("@"):
            break
        if not in_get_look:
            continue

        key_match = re.search(r'ARGS\s*==\s*"([^"]+)"', line)
        if key_match:
            current_key = key_match.group(1)
            tables.setdefault(current_key, [])
            current_cases = []
            continue
        if not current_key:
            continue
        case_match = re.match(r"CASE\s+(.+)$", line, flags=re.IGNORECASE)
        if case_match and not line.upper().startswith("CASEELSE"):
            current_cases = parse_erb_case_targets(case_match.group(1))
            continue
        if line.startswith("LOCALS = ") and current_cases:
            value = parse_erb_plain_value(line, "LOCALS = ")
            if value:
                tables.setdefault(current_key, []).extend((start, end, value) for start, end in current_cases)

    in_love_base = False
    current_cases = []
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("@LOVE_LIKE_BASE"):
            in_love_base = True
            current_cases = []
            tables.setdefault("喜欢的东西", [])
            continue
        if in_love_base and line.startswith("@"):
            break
        if not in_love_base:
            continue
        case_match = re.search(r"TALENT:317\s*==\s*(-?\d+)", line)
        if case_match:
            value = int(case_match.group(1))
            current_cases = [(value, value)]
            continue
        if line.startswith("PRINTFORM ") and current_cases:
            value = parse_erb_plain_value(line, "PRINTFORM ")
            if value:
                tables["喜欢的东西"].extend((start, end, value) for start, end in current_cases)

    return tables


def csv_value_int(value: str, default: int = 0) -> int:
    text = value.split(";", 1)[0].strip()
    if text == "":
        return default
    try:
        return int(text)
    except ValueError:
        return default


def load_character_csv(filename: str) -> "CharacterState":
    path = ROOT / "CSV" / "Chara" / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing character CSV: {path}")

    no = csv_value_int(Path(filename).stem.replace("Chara", ""), 0)
    name = Path(filename).stem
    callname = name
    base: dict[int, int] = {}
    maxbase: dict[int, int] = {}
    abl: dict[int, int] = {}
    talent: dict[int | str, int] = {}
    exp: dict[int, int] = {}
    juel: dict[int, int] = {}
    cflag: dict[int, int] = {}
    cstr: dict[int, str] = {}

    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = [part.strip() for part in line.split(",")]
        key = parts[0]
        if key == "番号" and len(parts) >= 2:
            no = csv_value_int(parts[1], no)
        elif key == "名前" and len(parts) >= 2:
            name = parts[1].split(";", 1)[0].strip() or name
        elif key == "呼び名" and len(parts) >= 2:
            callname = parts[1].split(";", 1)[0].strip() or callname
        elif key == "基礎" and len(parts) >= 3:
            index = csv_value_int(parts[1])
            value = csv_value_int(parts[2])
            base[index] = value
            maxbase[index] = value
        elif key == "素質" and len(parts) >= 2:
            index = csv_value_int(parts[1])
            value = csv_value_int(parts[2], 1) if len(parts) >= 3 else 1
            talent[index] = value
        elif key in {"フラグ", "CFLAG"} and len(parts) >= 3:
            cflag[csv_value_int(parts[1])] = csv_value_int(parts[2])
        elif key == "ABL" and len(parts) >= 3:
            abl[csv_value_int(parts[1])] = csv_value_int(parts[2])
        elif key in {"経験", "EXP"} and len(parts) >= 3:
            exp[csv_value_int(parts[1])] = csv_value_int(parts[2])
        elif key == "JUEL" and len(parts) >= 3:
            juel[csv_value_int(parts[1])] = csv_value_int(parts[2])
        elif key == "CSTR" and len(parts) >= 3:
            cstr[csv_value_int(parts[1])] = parts[2].split(";", 1)[0].strip()

    return CharacterState(
        name=name,
        hp=base.get(0, 1000),
        mp=base.get(1, 1000),
        max_hp=maxbase.get(0, base.get(0, 1000)),
        max_mp=maxbase.get(1, base.get(1, 1000)),
        no=no,
        callname=callname,
        source_file=str(path.relative_to(ROOT)).replace("\\", "/"),
        base=base,
        maxbase=maxbase,
        abl=abl,
        talent=talent,
        exp=exp,
        juel=juel,
        cflag=cflag,
        cstr=cstr,
    )


@dataclass
class CharacterState:
    name: str
    hp: int
    mp: int
    max_hp: int
    max_mp: int
    no: int = -1
    callname: str = ""
    source_file: str = ""
    posture: str = "通常"
    base: dict[int, int] = field(default_factory=dict)
    maxbase: dict[int, int] = field(default_factory=dict)
    abl: dict[int, int] = field(default_factory=dict)
    talent: dict[int | str, int] = field(default_factory=dict)
    palam: dict[int | str, int] = field(default_factory=dict)
    exp: dict[int, int] = field(default_factory=dict)
    juel: dict[int, int] = field(default_factory=dict)
    source: dict[int, int] = field(default_factory=dict)
    cflag: dict[int, int] = field(default_factory=dict)
    cstr: dict[int, str] = field(default_factory=dict)
    mark: dict[int, int] = field(default_factory=dict)
    stain: dict[int, int] = field(default_factory=dict)
    tequip: dict[int, int] = field(default_factory=dict)
    losebase: dict[int, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.callname:
            self.callname = self.name
        self.base.setdefault(0, self.hp)
        self.base.setdefault(1, self.mp)
        self.maxbase.setdefault(0, self.max_hp)
        self.maxbase.setdefault(1, self.max_mp)


class BodyMetricsGenerator:
    WOMAN_HEIGHT_P3 = [128200, 134200, 140200, 145000, 147900, 149500, 149800, 149900, 150000, 150100]
    WOMAN_HEIGHT_P50 = [140100, 146600, 152400, 156300, 158600, 159800, 160100, 160200, 160300, 160400]
    WOMAN_HEIGHT_P97 = [152700, 159200, 154500, 167600, 169300, 170100, 170300, 170400, 170500, 170600]
    WOMAN_WEIGHT_P3 = [21800, 24500, 28000, 32000, 35500, 37800, 39000, 39900, 40000, 40100, 40200, 40200, 40200]
    WOMAN_WEIGHT_P50 = [31100, 35400, 40000, 44000, 47100, 49000, 50100, 50700, 51100, 51400, 51700, 51900, 52000]
    WOMAN_WEIGHT_P97 = [46500, 54000, 60500, 64500, 66100, 67000, 67200, 67500, 68000, 68400, 68700, 68900, 69000]
    MAN_HEIGHT_P3 = [127900, 132200, 137200, 144000, 151900, 158500, 158800, 160300, 160500, 160900]
    MAN_HEIGHT_P50 = [140200, 145300, 151900, 159500, 165900, 169800, 171600, 172300, 172700, 173100]
    MAN_HEIGHT_P97 = [152000, 158900, 166900, 175100, 180200, 182800, 184000, 184500, 184800, 185000]
    MAN_WEIGHT_P3 = [23600, 24800, 28400, 32000, 36500, 40600, 43500, 45300, 46300, 46500, 46700, 46800, 47000]
    MAN_WEIGHT_P50 = [33700, 37700, 42500, 48100, 53400, 57100, 59400, 60700, 61400, 61600, 61800, 61900, 62000]
    MAN_WEIGHT_P97 = [51400, 57600, 64700, 72600, 79100, 82500, 83900, 84500, 84700, 84900, 85100, 85200, 85200]
    DEFAULT_RACE_AGE_FLAG26 = 232015325431115011
    DEFAULT_RACE_AGE_FLAG27 = 1001

    def __init__(self, target: CharacterState) -> None:
        self.target = target
        self.rng = Random(f"body:{target.source_file}:{target.no}:{target.name}")

    def apply(self) -> None:
        if all(key in self.target.cflag for key in (451, 452, 453, 454, 455, 456, 457)):
            return
        metrics = self._generate()
        for key, value in metrics.items():
            self.target.cflag[key] = value

    def _generate(self) -> dict[int, int]:
        age_hint = 0
        if self.target.no == 0:
            age_hint = 21
        elif self._talent(165):
            age_hint = self.rng.randrange(2) + 12
        elif self._talent(171):
            age_hint = self.rng.randrange(2) + 17
        human_age, race_age, height, weight, bust, waist, hip, bust_top, bust_under = self._char_size_generate(age_hint)
        if human_age <= 14:
            self.target.talent.setdefault(135, 1)
        return {
            451: human_age,
            452: race_age,
            453: height,
            454: weight,
            455: bust,
            456: waist,
            457: hip,
            458: bust_top,
            459: bust_under,
        }

    def _char_size_generate(self, age_hint: int = 0) -> tuple[int, int, int, int, int, int, int, int, int]:
        if age_hint <= 0:
            human_age, race_age = self._char_age_generate()
        else:
            human_age = age_hint
            race_age = 21 if self.target.no == 0 else self._race_age_generate(human_age, self._talent(314))
        char_height, char_weight = self._char_hweight_generate(human_age)

        char_waist = char_height * (3700 + self._talent(308)) // 10000
        if self._talent(122):
            char_waist += 8000
            char_waist -= self._rand(4000)
        if char_waist > 60000:
            char_waist = char_waist * 983 // 1000
        if self._talent(91):
            char_waist = char_waist * 96 // 100
        if self._talent(248):
            char_waist = char_waist * 102 // 100
        if self._talent(248) and self._talent(122):
            char_waist = char_waist * 105 // 100
        if self._talent(115):
            char_waist = char_waist * 115 // 100
        if self._talent(256):
            char_waist = char_waist * 98 // 100
        if self._talent(314) == 11:
            char_waist = char_waist * 104 // 100

        char_bust, char_bust_under, char_bust_top = self._char_bust_generate(human_age, char_height)
        if self._talent(100) and not self._talent(110):
            pass
        if self._talent(100) and self._talent(110):
            char_bust_top += 1500 + self._rand(1000)
        if self._talent(99):
            char_bust_top -= 2000 + self._rand(1000)
        if self._exp(60) > 0:
            char_bust_top += 200 + self._rand(800)
        if self._talent(130) and self._talent(119):
            char_bust_top += 8500 + self._rand(4000)
        char_bust = char_bust_under + char_bust_top

        char_hip = char_height * (5300 + self._talent(308)) // 10000
        if self._talent(91):
            char_hip += 1500
        if self._talent(248):
            char_hip = char_hip * 102 // 100
        if self._talent(256):
            char_hip = char_hip * 98 // 100
        if self._talent(100):
            char_hip = char_hip * 96 // 100
        if self._talent(122):
            char_hip = char_hip * 90 // 100
        if self._talent(115):
            char_hip = char_hip * 115 // 100
        if human_age < 16:
            char_hip = max(min(char_hip, char_bust + max(human_age - 12, 0) * 1000), char_waist)

        cal_var = char_bust_under * char_bust_under // 100000000
        cal_var = cal_var * char_bust_top // 100000
        cal_var = cal_var * char_bust_top // 100000
        char_weight += cal_var * 250
        if self._talent(314) == 0:
            race_age = human_age

        return (
            human_age,
            race_age,
            char_height // 100,
            char_weight // 100,
            char_bust // 100,
            char_waist // 100,
            char_hip // 100,
            char_bust_top // 100,
            char_bust_under // 100,
        )

    def _char_age_generate(self) -> tuple[int, int]:
        exp_age = 17 + self._char_age_expect()
        exp_age = self._limit(exp_age, 12, 35)
        human_age = self._normal_point_pickup(exp_age)
        if self._talent(314) == 0:
            race_age = human_age
        else:
            race_age = self._race_age_generate(human_age, self._talent(314))
        return human_age, race_age

    def _char_age_expect(self) -> int:
        exp_age = 0
        if self._talent(99):
            exp_age += 1
        if self._talent(100):
            exp_age -= 1
        if self._talent(100):
            exp_age -= 3
        if self._talent(109):
            exp_age -= 1
        if self._talent(110):
            exp_age += 1
        if self._talent(114):
            exp_age += 1
        if self._talent(119):
            exp_age += 1
        if self._talent(116):
            exp_age -= 1
        if self._talent(132):
            exp_age -= 2
        if self._talent(135):
            exp_age -= 2
        if self._talent(140) or self._talent(141):
            exp_age -= 2
        if self._talent(142) or self._talent(143):
            exp_age += 2
        if self._talent(157):
            exp_age += 6
        if self._talent(248):
            exp_age += 1
        life_before_hero = self._talent(315)
        if life_before_hero in {1, 6, 7, 20}:
            exp_age -= 4
        elif life_before_hero in {11, 12}:
            exp_age -= 1
        elif life_before_hero in {2, 19}:
            exp_age += 4
        elif life_before_hero == 21:
            exp_age += 6
        if self._talent(316) == 6:
            exp_age += 2
        if self._talent(317) in {4, 11}:
            exp_age += 2
        if self._exp(60):
            exp_age += 6
        elif self._exp(5):
            exp_age += 4
        elif self._exp(10):
            exp_age += 2
        elif not self._talent(0) and not self._talent(1):
            exp_age += 1
        return exp_age

    def _char_hweight_generate(self, human_age: int) -> tuple[int, int]:
        if self._talent(122):
            height_p3, height_p50, height_p97, weight_p3, weight_p50, weight_p97 = self._statistics_man(human_age)
        else:
            height_p3, height_p50, height_p97, weight_p3, weight_p50, weight_p97 = self._statistics_woman(human_age)

        if self._talent(100):
            height_low = height_p3 * 2 - (height_p3 + height_p50) // 2
            height_mid = height_p3
            height_high = (height_p3 + height_p50) // 2
            weight_low = weight_p3 * 2 - (weight_p3 + weight_p50) // 2
            weight_mid = weight_p3
            weight_high = (weight_p3 + weight_p50) // 2
        elif self._talent(99):
            height_low = (height_p50 + height_p97) // 2
            height_mid = height_p97
            height_high = height_p97 * 2 - (height_p50 + height_p97) // 2
            weight_low = (weight_p50 + weight_p97) // 2
            weight_mid = weight_p97
            weight_high = weight_p97 * 2 - (weight_p50 + weight_p97) // 2
        else:
            height_low = (height_p3 + height_p50) // 2
            height_mid = height_p50
            height_high = (height_p50 + height_p97) // 2
            weight_low = (weight_p3 + weight_p50) // 2
            weight_mid = weight_p50
            weight_high = (weight_p50 + weight_p97) // 2

        char_height, scale = self._normal_range_pickup(height_low, height_mid, height_high)
        char_weight, _ = self._normal_range_pickup(weight_low, weight_mid, weight_high, scale)

        base_height = 109000
        base_weight = 17000
        race = self._talent(314)
        if race in {1, 7}:
            char_height += (char_height - base_height) * 3 // 20
            char_weight += (char_weight - base_weight) * 3 // 20
        elif race == 5:
            char_height += (char_height - base_height) // 4
            char_weight += (char_weight - base_weight) * 4 // 5
        elif race == 10:
            char_height -= (char_height - base_height) * 15 // 20
            char_weight -= (char_weight - base_weight) * 12 // 20
        elif race == 11:
            char_height -= (char_height - base_height) * 9 // 20
            char_weight -= (char_weight - base_weight) * 7 // 20
        elif self._talent(220):
            if self._talent(319) == 6:
                char_height //= 3
                char_weight //= 3
            elif self._talent(319) == 7:
                char_height *= 2
                char_weight *= 2

        if self._talent(248):
            char_weight = char_weight * 108 // 100
        if self._talent(248) and self._talent(122):
            char_weight = char_weight * 108 // 100
        if self._talent(256):
            char_weight = char_weight * 92 // 100
        if self._talent(256) and self._talent(122):
            char_weight = char_weight * 103 // 100
        if self._talent(115):
            char_weight = char_weight * 115 // 100
        return char_height, char_weight

    def _char_bust_generate(self, human_age: int, char_height: int) -> tuple[int, int, int]:
        wall = 2500
        aaa = 5000
        aa = 7500
        a = 10000
        b = 12500
        c = 15000
        d = 17500
        e = 20000
        g = 25000
        h = 27500
        j = 32500
        k = 35000
        m = 40000

        if self._talent(116) and human_age >= 14:
            bust_top = aaa + self._rand(2500) if human_age >= 16 else wall + self._rand(5000)
        elif self._talent(109) and human_age >= 14:
            bust_top = a + self._rand(2500) if human_age >= 16 else aa + self._rand(5000)
        elif human_age <= 11 and self._talent(135):
            bust_top = self._rand(2500)
        elif human_age <= 14 and self._talent(135):
            bust_top = self._rand(5000)
        elif human_age >= 16 or self._talent(110) or self._talent(114) or self._talent(119) or (human_age < 16 and not self._talent(135) and not self._talent(109) and not self._talent(116)):
            age_count = 16 - human_age
            adjusted_age = self._limit(human_age, 16, 24)
            bust_low = b
            bust_high = e
            bust_center = (bust_low + bust_high) // 2
            bust_mid = ((adjusted_age - 16) * (d + e - b - c)) // (2 * (24 - 16)) + (b + c) // 2
            if bust_mid < bust_center:
                bust_high = bust_mid * 2 - bust_low
            else:
                bust_low = bust_mid * 2 - bust_high
            bust_top, _ = self._normal_range_pickup(bust_low, bust_mid, bust_high)
            if self._talent(119) and adjusted_age >= 16:
                bust_top += (k - b) + self._rand(max(m - k, 1))
            elif (self._talent(119) and adjusted_age >= 12) or (self._talent(114) and adjusted_age >= 16):
                bust_top += (g - b) + self._rand(max(j - g, 1))
            elif (self._talent(114) and adjusted_age >= 12) or (self._talent(110) and adjusted_age >= 12):
                bust_top += (e - b) + self._rand(max(h - e, 1))
            if self._talent(119) and (self._rand(2) == 0 or self._talent(130)):
                bust_top += 18000 + self._rand(2000) + self._rand(2000) + self._rand(3000)
            if age_count < 0:
                bust_top = bust_top * (20 + age_count) // 20
        elif self._talent(122):
            bust_top = wall + self._rand(3000)
            if self._talent(256):
                bust_top -= self._rand(1500)
            if self._talent(248):
                bust_top += self._rand(6500) * 2
            if self._talent(115):
                bust_top += self._rand(5000) * 2
        else:
            adjusted_age = self._limit(human_age, 12, 16)
            bust_low = wall
            bust_high = c
            bust_center = (bust_low + bust_high) // 2
            bust_mid = ((adjusted_age - 12) * (b + c - wall - aaa)) // (2 * (16 - 12)) + (aaa + wall) // 2
            if bust_mid < bust_center:
                bust_high = bust_mid * 2 - bust_low
            else:
                bust_low = bust_mid * 2 - bust_high
            bust_top, _ = self._normal_range_pickup(bust_low, bust_mid, bust_high)

        bust_under = self._under_bust(char_height // 100) * 100
        return bust_under + bust_top, bust_under, bust_top

    def _under_bust(self, height_tenths: int) -> int:
        bust_under = height_tenths * (43100 + self._talent(308)) // 100000
        if self._talent(248):
            bust_under = bust_under * 105 // 100
        if self._talent(256):
            bust_under = bust_under * 98 // 100
        return bust_under

    def _race_age_generate(self, human_age: int, race_talent: int) -> int:
        if 7 <= race_talent < 10:
            if race_talent == 7:
                race_id = 0
            elif race_talent == 8:
                race_id = 5
            else:
                return human_age
        else:
            race_id = race_talent - 1
            if race_id > 8:
                race_id -= 3
        if race_id < 0:
            config = 1
        elif race_id > 5:
            config = self._race_age_chunks()[race_id]
        else:
            config = self._race_age_chunks()[race_id]
        race_cla = config // 100
        race_deg = config // 10 % 10
        race_num = config % 10
        factor = race_num * (10 ** race_deg)
        if race_cla == 0:
            return human_age * factor + self._rand(max(factor, 1))
        if race_cla == 1:
            return human_age * (race_deg * 10 + race_num) // 10
        if race_cla == 2:
            upper = max(factor, 1)
            scale = min(upper, (10 ** self._rand(len(str(upper)) + 1)) * 10)
            return self._rand(max(scale, 1))
        if race_cla == 3:
            return self._rand(max(factor // 2, 1)) + factor // 2
        if race_cla == 4:
            return self._rand(max(factor - human_age, 1)) + human_age
        return human_age

    def _race_age_chunks(self) -> list[int]:
        chunks: list[int] = []
        value = self.DEFAULT_RACE_AGE_FLAG26
        for _ in range(6):
            chunks.append(value % 1000)
            value //= 1000
        value = self.DEFAULT_RACE_AGE_FLAG27
        for _ in range(2):
            chunks.append(value % 1000)
            value //= 1000
        return chunks

    def _statistics_woman(self, age: int) -> tuple[int, int, int, int, int, int]:
        age = self._limit(age, 10, 22)
        index = age - 10
        if index < 9:
            return (
                self.WOMAN_HEIGHT_P3[index],
                self.WOMAN_HEIGHT_P50[index],
                self.WOMAN_HEIGHT_P97[index],
                self.WOMAN_WEIGHT_P3[index],
                self.WOMAN_WEIGHT_P50[index],
                self.WOMAN_WEIGHT_P97[index],
            )
        return (
            self.WOMAN_HEIGHT_P3[9],
            self.WOMAN_HEIGHT_P50[9],
            self.WOMAN_HEIGHT_P97[9],
            self.WOMAN_WEIGHT_P3[index],
            self.WOMAN_WEIGHT_P50[index],
            self.WOMAN_WEIGHT_P97[index],
        )

    def _statistics_man(self, age: int) -> tuple[int, int, int, int, int, int]:
        age = self._limit(age, 10, 22)
        index = age - 10
        if index < 9:
            return (
                self.MAN_HEIGHT_P3[index],
                self.MAN_HEIGHT_P50[index],
                self.MAN_HEIGHT_P97[index],
                self.MAN_WEIGHT_P3[index],
                self.MAN_WEIGHT_P50[index],
                self.MAN_WEIGHT_P97[index],
            )
        return (
            self.MAN_HEIGHT_P3[9],
            self.MAN_HEIGHT_P50[9],
            self.MAN_HEIGHT_P97[9],
            self.MAN_WEIGHT_P3[index],
            self.MAN_WEIGHT_P50[index],
            self.MAN_WEIGHT_P97[index],
        )

    def _normal_point_pickup(self, center: int) -> int:
        roll = self.rng.randrange(17) + 1
        if roll == 1:
            return center - 2
        if roll <= 4:
            return center - 1
        if roll <= 13:
            return center
        if roll <= 16:
            return center + 1
        return center + 2

    def _normal_range_pickup(self, low: int, mid: int, high: int, scale: int = -1) -> tuple[int, int]:
        if scale < 0:
            roll = self.rng.randrange(34) + 1
            if roll <= 2:
                local = self._rand(20)
            elif roll <= 8:
                local = self._rand(20) + 20
            elif roll <= 17:
                local = self._rand(10) + 40
            elif roll <= 26:
                local = self._rand(10) + 50
            elif roll <= 32:
                local = self._rand(20) + 60
            else:
                local = self._rand(20) + 80
        else:
            local = min(scale, 100)
        if local <= 50:
            value = low + (mid - low) * local // 50
        else:
            value = mid + (high - mid) * (local - 50) // 50
        return value, local

    def _limit(self, value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))

    def _rand(self, upper: int) -> int:
        return self.rng.randrange(upper) if upper > 0 else 0

    def _talent(self, key: int) -> int:
        return int(self.target.talent.get(key, 0) or 0)

    def _exp(self, key: int) -> int:
        return int(self.target.exp.get(key, 0) or 0)


class TalentConditionRenderer:
    def __init__(
        self,
        target: CharacterState,
        name_tables: dict[str, dict[int, str]],
        condition_lines: list[str],
        seiin_check_lines: list[str],
        explv_values: dict[int, int],
    ) -> None:
        self.target = target
        self.name_tables = name_tables
        self.condition_lines = condition_lines
        self.seiin_check_lines = seiin_check_lines
        self.scalars: dict[str, int] = {"RESULT": 0, "SEXSKILL_COUNT": 0}
        self.arrays: dict[str, dict[int, int]] = {
            "EXPLV": dict(explv_values),
            "FLAG": {},
            "JUEL": dict(target.juel),
            "SEXSKILL_EXP": {},
        }
        self.rendered_lines: list[str] = []
        self.current_label = ""
        self.current_label_talent: int | None = None
        self.current_fragments: list[str] = []
        self.current_color: str | None = None
        self.unsupported: set[str] = set()

    def render(self) -> tuple[list[str], list[str]]:
        self._run_lines(self.condition_lines, render_output=True)
        self._flush_line()
        return self.rendered_lines, sorted(self.unsupported)

    def _run_lines(self, lines: list[str], render_output: bool) -> int:
        frames: list[dict[str, bool]] = []
        single_if: bool | None = None
        return_value = 0
        for raw_line in lines:
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(";"):
                continue
            if single_if is not None:
                should_run = single_if
                single_if = None
                if not should_run:
                    continue
            current_active = frames[-1]["current"] if frames else True
            if stripped.startswith("SIF "):
                single_if = current_active and self._truthy(self._eval_expr(stripped[4:]))
                continue
            if stripped.startswith("IF "):
                condition = current_active and self._truthy(self._eval_expr(stripped[3:]))
                frames.append({"parent": current_active, "taken": condition, "current": condition})
                continue
            if stripped.startswith("ELSEIF "):
                if not frames:
                    self.unsupported.add("ELSEIF without IF")
                    continue
                frame = frames[-1]
                condition = frame["parent"] and (not frame["taken"]) and self._truthy(self._eval_expr(stripped[7:]))
                frame["current"] = condition
                frame["taken"] = frame["taken"] or condition
                continue
            if stripped == "ELSE":
                if not frames:
                    self.unsupported.add("ELSE without IF")
                    continue
                frame = frames[-1]
                condition = frame["parent"] and (not frame["taken"])
                frame["current"] = condition
                frame["taken"] = True
                continue
            if stripped == "ENDIF":
                if frames:
                    frames.pop()
                else:
                    self.unsupported.add("ENDIF without IF")
                continue
            current_active = frames[-1]["current"] if frames else True
            if not current_active:
                continue
            if stripped.startswith("CALL "):
                self._handle_call(stripped[5:], render_output)
                continue
            if stripped.startswith("#DIM "):
                continue
            if stripped.startswith(("PRINTFORM ", "PRINTFORML ", "PRINTS ", "PRINT ")):
                if render_output:
                    self._handle_print(stripped)
                continue
            if stripped == "PRINTL":
                if render_output:
                    self._flush_line()
                continue
            if stripped in {"RESETCOLOR", 'PRINT_IMG "COVER_WHITE"'}:
                if stripped == "RESETCOLOR":
                    self.current_color = None
                continue
            if stripped.startswith("RETURN"):
                expr = stripped[6:].strip()
                return_value = self._to_int(self._eval_expr(expr)) if expr else 0
                break
            if self._handle_assignment(stripped):
                continue
            self.unsupported.add(stripped)
        return return_value

    def _handle_assignment(self, stripped: str) -> bool:
        match = re.match(r"^([A-Z_]+(?::-?\d+)?)\s*(\+=|-=|\*=|/=|=)\s*(.+)$", stripped)
        if not match:
            return False
        target, op, expr = match.groups()
        value = self._to_int(self._eval_expr(expr))
        current = self._get_storage_value(target)
        if op == "=":
            result = value
        elif op == "+=":
            result = current + value
        elif op == "-=":
            result = current - value
        elif op == "*=":
            result = current * value
        elif op == "/=":
            result = 0 if value == 0 else int(current / value)
        else:
            return False
        self._set_storage_value(target, result)
        return True

    def _handle_call(self, body: str, render_output: bool) -> None:
        name, args = self._parse_call(body)
        if name == "STC_LAB_TAL":
            if render_output and args:
                self._start_talent_block(self._to_int(self._eval_expr(args[0])))
            return
        if name == "STC_SEIIN_CHECK":
            self.scalars["RESULT"] = self._run_lines(self.seiin_check_lines, render_output=False)
            return
        if name.startswith("STC_COLOR_"):
            self.current_color = name.removeprefix("STC_COLOR_")
            return
        if not render_output:
            return
        if name == "STC_PRINTC" and args:
            self.current_fragments.append(self._annotate_print_fragment(self._render_print_text(args[0])))
            return
        if name == "STC_SAY_ABL" and len(args) >= 2:
            self.current_fragments.append(self._render_abl_fragment(args[0], args[1]))
            return
        if name == "STC_SAY_EXP" and len(args) >= 2:
            self.current_fragments.append(self._render_exp_fragment(args[0], args[1]))
            return
        if name == "STC_SAY_MARK" and len(args) >= 2:
            self.current_fragments.append(self._render_mark_fragment(args[0], args[1]))
            return
        if name == "STC_SAYNO_MARK" and args:
            threshold = args[1] if len(args) >= 2 else "0"
            self.current_fragments.append(self._render_no_mark_fragment(args[0], threshold))
            return
        if name == "STC_SAY_TAL" and args:
            self.current_fragments.append(self._render_talent_fragment(args[0]))
            return
        if name == "STC_SAYNO_TAL" and args:
            threshold = args[1] if len(args) >= 2 else "0"
            self.current_fragments.append(self._render_no_talent_fragment(args[0], threshold))
            return
        if name == "STC_SAYSUM_EXP" and len(args) >= 2:
            self.current_fragments.append(self._render_sum_exp_fragment(args))
            return
        if name == "STC_SAY_ABCV" and args:
            self.current_fragments.append(self._render_abcv_fragment(args[0]))
            return
        if name in {"STC_COLOR_TRUE", "STC_COLOR_FALSE", "STC_COLOR_RIGHT", "STC_COLOR_ALERT", "STC_COLOR_INVALID", "STC_COLOR_ACHIEVE", "STC_COLOR_DEFAULT"}:
            return
        self.unsupported.add(f"CALL {name}")

    def _handle_print(self, stripped: str) -> None:
        keyword = next(prefix for prefix in ("PRINTFORM ", "PRINTFORML ", "PRINTS ", "PRINT ") if stripped.startswith(prefix))
        text = self._render_print_text(stripped[len(keyword) :].strip())
        if text.endswith("条件：") and not self.current_label:
            self.current_label = text.removesuffix("：")
            self.current_label_talent = None
            return
        self.current_fragments.append(self._annotate_print_fragment(text))

    def _start_talent_block(self, talent_id: int) -> None:
        self._flush_line()
        self.current_label_talent = talent_id
        label = self._talent_name(talent_id)
        if talent_id == 230 and self._value_of("TALENT", 122):
            label = "绝伦"
        state = "无效" if self._value_of("TALENT", 9) else "已取得" if self._value_of("TALENT", talent_id) else "未取得"
        self.current_label = f"{label}条件[{state}]"
        self.current_fragments = []
        self.current_color = None

    def _flush_line(self) -> None:
        if not self.current_label and not self.current_fragments:
            return
        body = "".join(self.current_fragments).strip()
        line = f"{self.current_label}：{body}" if self.current_label else body
        self.rendered_lines.append(line.rstrip("：") if not body else line)
        self.current_label = ""
        self.current_label_talent = None
        self.current_fragments = []
        self.current_color = None

    def _render_abl_fragment(self, ability_expr: str, need_expr: str) -> str:
        ability_id = self._to_int(self._eval_expr(ability_expr))
        current = self._value_of("ABL", ability_id)
        resolved = self._resolve_int_expr(need_expr)
        label = "阴茎感觉" if ability_id == 0 and self._value_of("TALENT", 122) else self._abl_name(ability_id)
        if resolved is None:
            return f"[{label} >= {need_expr} / 现Lv{current} / 阈值待接入]"
        return f"[{label} Lv{resolved} / 现Lv{current}]"

    def _render_exp_fragment(self, exp_expr: str, need_expr: str) -> str:
        exp_id = self._to_int(self._eval_expr(exp_expr))
        current = self._value_of("EXP", exp_id)
        resolved = self._resolve_int_expr(need_expr)
        label = self._exp_name(exp_id)
        if resolved is None:
            return f"[{label} >= {need_expr} / 现{current} / 阈值待接入]"
        return f"[{label} {resolved} / 现{current}]"

    def _render_mark_fragment(self, mark_expr: str, need_expr: str) -> str:
        mark_id = self._to_int(self._eval_expr(mark_expr))
        current = self._value_of("MARK", mark_id)
        resolved = self._resolve_int_expr(need_expr)
        label = self._mark_name(mark_id)
        if resolved is None:
            return f"[{label} >= {need_expr} / 现Lv{current} / 阈值待接入]"
        return f"[{label} Lv{resolved} / 现Lv{current}]"

    def _render_no_mark_fragment(self, mark_expr: str, need_expr: str) -> str:
        mark_id = self._to_int(self._eval_expr(mark_expr))
        current = self._value_of("MARK", mark_id)
        resolved = self._resolve_int_expr(need_expr)
        label = self._mark_name(mark_id)
        if resolved is None:
            return f"[{label} <= {need_expr} / 现Lv{current} / 阈值待接入]"
        return f"[{label} <= Lv{resolved} / 现Lv{current}]"

    def _render_talent_fragment(self, talent_expr: str) -> str:
        talent_id = self._to_int(self._eval_expr(talent_expr))
        label = "绝伦" if talent_id == 230 and self._value_of("TALENT", 122) else self._talent_name(talent_id)
        return f"[{label} / {'已取得' if self._value_of('TALENT', talent_id) else '未取得'}]"

    def _render_no_talent_fragment(self, talent_expr: str, need_expr: str) -> str:
        talent_id = self._to_int(self._eval_expr(talent_expr))
        current = self._value_of("TALENT", talent_id)
        resolved = self._resolve_int_expr(need_expr)
        label = self._talent_name(talent_id)
        if resolved is None:
            return f"[{label} <= {need_expr} / 现{current} / 阈值待接入]"
        return f"[{label} <= {resolved} / 现{current}]"

    def _render_sum_exp_fragment(self, args: list[str]) -> str:
        target_value = self._resolve_int_expr(args[0])
        exp_ids = [self._to_int(self._eval_expr(arg)) for arg in args[1:] if arg.strip() and self._to_int(self._eval_expr(arg)) > 0]
        labels = [self._exp_name(exp_id) for exp_id in exp_ids]
        current = sum(self._value_of("EXP", exp_id) for exp_id in exp_ids)
        label = "|".join(labels) if labels else "经验合计"
        if target_value is None:
            return f"[{label} >= {args[0]} / 现{current} / 阈值待接入]"
        return f"[{label} {target_value} / 现{current}]"

    def _render_abcv_fragment(self, need_expr: str) -> str:
        resolved = self._resolve_int_expr(need_expr)
        current = sum(self._value_of("ABL", index) for index in range(4))
        if resolved is None:
            return f"[四点感觉 >= {need_expr} / 现Lv{current} / 阈值待接入]"
        return f"[四点感觉 Lv{resolved} / 现Lv{current}]"

    def _annotate_print_fragment(self, text: str) -> str:
        compact = text.strip()
        love_match = re.fullmatch(r"\[好感度\s*(\d+)%\]", compact)
        if love_match:
            return f"[好感度 {love_match.group(1)}% / 现{self._value_of('CFLAG', 2) / 10:.1f}%]"
        juel_match = re.fullmatch(r"\[胸部点数\s*(\d+)\]", compact)
        if juel_match:
            return f"[胸部点数 {juel_match.group(1)} / 现{self._value_of('JUEL', 14)}]"
        seiin_match = re.fullmatch(r"\[饮精绝顶\s*(\d+)\]", compact)
        if seiin_match:
            return f"[饮精绝顶 {seiin_match.group(1)} / 现{self._value_of('EXP', 8)}]"
        suffix = {
            "TRUE": " / 达成",
            "RIGHT": " / 达成",
            "ACHIEVE": " / 已取得",
            "FALSE": " / 未达成",
            "ALERT": " / 不满足",
            "INVALID": " / 无效",
        }.get(self.current_color or "")
        if suffix and compact.startswith("[") and compact.endswith("]"):
            return compact[:-1] + suffix + "]"
        return text

    def _render_print_text(self, token: str) -> str:
        text = token.strip()
        if text.startswith('@"') and text.endswith('"'):
            text = text[2:-1]
        elif text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        text = re.sub(
            r"%([A-Z]+NAME):(-?\d+)%",
            lambda match: self.name_tables.get(match.group(1), {}).get(int(match.group(2)), f"{match.group(1)}:{match.group(2)}"),
            text,
        )

        def replace_expr(match: re.Match[str]) -> str:
            expr = match.group(1)
            expr = expr.split(",", 1)[0].strip()
            resolved = self._resolve_int_expr(expr)
            return str(resolved) if resolved is not None else expr

        return re.sub(r"\{([^{}]+)\}", replace_expr, text)

    def _parse_call(self, body: str) -> tuple[str, list[str]]:
        if "(" not in body:
            return body.strip(), []
        name, remainder = body.split("(", 1)
        args_text = remainder.rsplit(")", 1)[0]
        return name.strip(), self._split_args(args_text)

    def _split_args(self, text: str) -> list[str]:
        args: list[str] = []
        current: list[str] = []
        depth = 0
        in_string = False
        escape = False
        for char in text:
            if char == "\\" and in_string:
                escape = not escape
                current.append(char)
                continue
            if char == '"' and not escape:
                in_string = not in_string
                current.append(char)
                continue
            escape = False
            if not in_string and char == "," and depth == 0:
                args.append("".join(current).strip())
                current = []
                continue
            if not in_string and char in "({[":
                depth += 1
            elif not in_string and char in ")}]":
                depth = max(0, depth - 1)
            current.append(char)
        if current:
            args.append("".join(current).strip())
        return args

    def _resolve_int_expr(self, expr: str) -> int | None:
        try:
            return self._to_int(self._eval_expr(expr))
        except Exception:
            self.unsupported.add(f"EXPR {expr}")
            return None

    def _eval_expr(self, expr: str) -> int | bool:
        text = expr.strip()
        if not text:
            return 0
        translated = text.replace("&&", " and ").replace("||", " or ")
        translated = re.sub(r"(?<![=!<>])!(?!=)", " not ", translated)
        array_refs: list[str] = []

        def replace_array(match: re.Match[str]) -> str:
            array_refs.append(f'__get("{match.group(1)}", {match.group(2)})')
            return f"__arrref_{len(array_refs) - 1}__"

        translated = re.sub(r"\b([A-Z_]+):(-?\d+)\b", replace_array, translated)
        translated = re.sub(
            r"\b([A-Z][A-Z0-9_]*)\b",
            lambda match: match.group(1)
            if match.group(1) in {"and", "or", "not", "True", "False"} or match.group(1).startswith("__arrref_")
            else f'__scalar("{match.group(1)}")',
            translated,
        )
        for index, replacement in enumerate(array_refs):
            translated = translated.replace(f"__arrref_{index}__", replacement)
        try:
            return eval(
                translated,
                {"__builtins__": {}},
                {"__get": self._value_of, "__scalar": self._scalar_value},
            )
        except Exception as exc:
            raise ValueError(f"Unsupported expression: {expr}") from exc

    def _value_of(self, name: str, index: int) -> int:
        if name == "TALENT":
            return self._to_int(self.target.talent.get(index, 0))
        if name == "ABL":
            return self._to_int(self.target.abl.get(index, 0))
        if name == "EXP":
            return self._to_int(self.target.exp.get(index, 0))
        if name == "MARK":
            return self._to_int(self.target.mark.get(index, 0))
        if name == "CFLAG":
            return self._to_int(self.target.cflag.get(index, 0))
        if name == "JUEL":
            return self._to_int(self.target.juel.get(index, 0))
        if name in self.arrays:
            return self._to_int(self.arrays[name].get(index, 0))
        return 0

    def _scalar_value(self, name: str) -> int:
        return self._to_int(self.scalars.get(name, 0))

    def _get_storage_value(self, target: str) -> int:
        if ":" not in target:
            return self._scalar_value(target)
        name, raw_index = target.split(":", 1)
        index = self._to_int(self._eval_expr(raw_index))
        return self._value_of(name, index)

    def _set_storage_value(self, target: str, value: int) -> None:
        if ":" not in target:
            self.scalars[target] = value
            return
        name, raw_index = target.split(":", 1)
        index = self._to_int(self._eval_expr(raw_index))
        self.arrays.setdefault(name, {})[index] = value

    def _talent_name(self, talent_id: int) -> str:
        return self.name_tables["TALENTNAME"].get(talent_id, f"TALENT:{talent_id}")

    def _abl_name(self, ability_id: int) -> str:
        return self.name_tables["ABLNAME"].get(ability_id, f"ABL:{ability_id}")

    def _exp_name(self, exp_id: int) -> str:
        return self.name_tables["EXPNAME"].get(exp_id, f"EXP:{exp_id}")

    def _mark_name(self, mark_id: int) -> str:
        return self.name_tables["MARKNAME"].get(mark_id, f"MARK:{mark_id}")

    def _truthy(self, value: Any) -> bool:
        return bool(value)

    def _to_int(self, value: Any) -> int:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0


@dataclass
class ErbFunction:
    name: str
    path: Path
    lines: list[str]


class ErbExecutionStopped(Exception):
    def __init__(self, message: str, function: str, line: str, path: Path):
        super().__init__(message)
        self.message = message
        self.function = function
        self.line = line
        self.path = path


class ErbReturn(Exception):
    def __init__(self, value: Any = 0):
        self.value = value


class ErbCommandBridge:
    """Small but real ERB runtime for the browser prototype.

    It executes a strict subset of ERB and stops loudly on unknown semantics.
    The browser never simulates command effects; all command output and changed
    variables below come from ERB lines that this runtime actually executed.
    """

    def __init__(self, root: Path):
        self.root = root
        self.command_files: dict[int, Path] = {}
        self.functions: dict[str, ErbFunction] = {}
        self.name_tables = {
            "ABLNAME": load_csv_names("Abl.csv"),
            "EXPNAME": load_csv_names("exp.csv"),
            "MARKNAME": load_csv_names("Mark.csv"),
            "PALAMNAME": load_csv_names("Palam.csv"),
            "SOURCENAME": load_csv_names("source.csv"),
            "TALENTNAME": load_csv_names("Talent.csv"),
        }
        self.scalars: dict[str, int | str] = {}
        self.arrays: dict[str, dict[Any, int | str]] = {}
        self.output: list[str] = []
        self.changed: list[str] = []
        self.characters: list[CharacterState] = []
        self.target_index = 1
        self.function_return: Any = 0
        self._load_functions()

    def reset(self, characters: list[CharacterState], target_index: int) -> None:
        self.characters = characters
        self.target_index = target_index
        self.output = []
        self.changed = []
        self.scalars = {
            "A": 0,
            "B": 0,
            "E": 0,
            "L": 0,
            "S": 0,
            "V": 0,
            "Y": 0,
            "Z": 0,
            "ASSI": -1,
            "ASSIPLAY": 0,
            "ARG": 0,
            "DAY": 1,
            "MASTER": 0,
            "PLAYER": 0,
            "PREVCOM": -1,
            "SELECTCOM": -1,
            "TARGET": target_index,
            "TIME": 0,
        }
        self.arrays = {
            "DOWN": {},
            "EX": {},
            "EX_FLAG": {},
            "FLAG": {},
            "GOTJUEL": {},
            "GLOBAL": {},
            "JUEL": {},
            "LOCAL": {},
            "LOCALS": {},
            "NO": {},
            "PALAMLV": {1: 1000, 2: 3000, 3: 10000, 4: 30000, 5: 60000},
            "RELATION": {},
            "SAVESTR": {
                "PLAYER": "你",
                "MASTER": "你",
                "TARGET": self._char(target_index).name,
                0: "你",
                1: self._char(1).name,
                target_index: self._char(target_index).name,
                "ASSI": "",
            },
            "TFLAG": {},
            "UP": {},
        }
        self.arrays["FLAG"][7] = 2
        for index, char in enumerate(self.characters):
            self.arrays["NO"][index] = char.no if char.no >= 0 else index
            self.arrays["SAVESTR"][index] = char.callname or char.name
        self.arrays["SAVESTR"]["TARGET"] = self._char(target_index).callname or self._char(target_index).name
        self._enable_available_kojo_flags()

    def _load_functions(self) -> None:
        for path in sorted((self.root / "ERB").rglob("*.ERB")):
            self._parse_file(path)
            match = re.match(r"COMF(\d+)_", path.name, re.IGNORECASE)
            if match:
                self.command_files[int(match.group(1))] = path

    def _enable_available_kojo_flags(self) -> None:
        for char in self.characters:
            for talent_id, value in char.talent.items():
                if not isinstance(talent_id, int) or not value:
                    continue
                if not 160 <= talent_id < 180:
                    continue
                local = talent_id - 60
                if f"KOJO_MESSAGE_COM_{local - 100}".upper() in self.functions:
                    self.arrays["FLAG"][local] = 1

    def _parse_file(self, path: Path) -> None:
        current_name = ""
        current_lines: list[str] = []

        def commit() -> None:
            if current_name:
                self.functions[current_name.upper()] = ErbFunction(
                    current_name.upper(),
                    path,
                    current_lines.copy(),
                )

        for raw in read_text(path).splitlines():
            line = raw.lstrip("\ufeff")
            stripped = self._strip_comment(line).strip()
            if stripped.startswith("@"):
                commit()
                header = stripped[1:].strip()
                current_name = re.split(r"[\s,(]", header, maxsplit=1)[0].strip()
                current_lines = []
                continue
            if current_name:
                current_lines.append(stripped)
        commit()

    def execute_command(self, command_id: int) -> dict[str, object]:
        path = self.command_files.get(command_id)
        if not path:
            return {
                "ok": False,
                "status": "missing_erb",
                "output": [],
                "unsupported": [f"ERB/COMF{command_id}_*.ERB not found"],
            }

        self.output = []
        self.changed = []
        self.scalars["SELECTCOM"] = command_id
        self.arrays["SAVESTR"][22] = f"COM{command_id}"
        try:
            value = self._call(f"COM{command_id}")
            if value != 0:
                kojo = self.run_kojo_message_com()
                if kojo.get("status") == "partial":
                    self.output.append("口上执行未完成。")
                    for item in kojo.get("unsupported", []):
                        self.output.append(f"未支持: {item}")
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "output": self.output,
                "unsupported": [err.message, err.line],
                "changed": self.changed[-18:],
                "returnValue": 0,
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/"),
            }
        except RecursionError:
            return {
                "ok": False,
                "status": "partial",
                "output": self.output,
                "unsupported": ["ERB CALL stack exceeded Python recursion limit"],
                "changed": self.changed[-18:],
                "returnValue": 0,
                "erbFile": str(path.relative_to(self.root)).replace("\\", "/"),
            }

        return {
            "ok": True,
            "status": "executed",
            "output": self.output,
            "unsupported": [],
            "changed": self.changed[-18:],
            "returnValue": value,
            "erbFile": str(path.relative_to(self.root)).replace("\\", "/"),
        }

    def run_kojo_message_com(self) -> dict[str, object]:
        start_len = len(self.output)
        try:
            self._call("KOJO_MESSAGE_COM")
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "output": self.output[start_len:],
                "unsupported": [err.message, err.line],
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/")
                if err.path.exists() and err.path.is_file()
                else "",
            }
        return {"ok": True, "status": "executed", "output": self.output[start_len:], "unsupported": []}

    def run_kojo_message_palamcng(self) -> dict[str, object]:
        start_len = len(self.output)
        try:
            self._call("KOJO_MESSAGE_PALAMCNG")
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "output": self.output[start_len:],
                "unsupported": [err.message, err.line],
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/")
                if err.path.exists() and err.path.is_file()
                else "",
            }
        return {"ok": True, "status": "executed", "output": self.output[start_len:], "unsupported": []}

    def run_mark_got_check(self) -> dict[str, object]:
        try:
            self._call("MARK_GOT_CHECK")
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "unsupported": [err.message, err.line],
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/")
                if err.path.exists() and err.path.is_file()
                else "",
            }
        return {"ok": True, "status": "executed", "unsupported": []}

    def run_kojo_message_markcng(self) -> dict[str, object]:
        start_len = len(self.output)
        try:
            self._call("KOJO_MESSAGE_MARKCNG")
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "output": self.output[start_len:],
                "unsupported": [err.message, err.line],
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/")
                if err.path.exists() and err.path.is_file()
                else "",
            }
        return {"ok": True, "status": "executed", "output": self.output[start_len:], "unsupported": []}

    def run_source_settlement(self) -> dict[str, object]:
        """Run the ERB source-to-UP/DOWN part of SOURCE_CHECK.

        This intentionally executes real ERB helper functions instead of
        reimplementing their formulas in Python. The surrounding SOURCE_CHECK
        function still contains many UI and kojo hooks, so the prototype runs
        the numeric subchain first and reports exact gaps when one appears.
        """

        functions = [
            "SOURCE_CHECK_UP_C",
            "SOURCE_CHECK_UP_V",
            "SOURCE_CHECK_UP_A",
            "SOURCE_CHECK_UP_B",
            "SOURCE_CHECK_UP_FREE",
            "UP_TALENT_CVA_CHECK",
            "LOVE_MOIST_CHECK_UP",
            "EX_CHECK_UP",
            "SOURCE_CHECK_UP_LOVE",
            "SOURCE_CHECK_UP_IMPULSIVE",
            "SOURCE_CHECK_UP_ACHIEVE",
            "SOURCE_CHECK_UP_PAIN",
            "SOURCE_CHECK_UP_POISON",
            "SOURCE_CHECK_UP_DIRTY",
            "SOURCE_CHECK_UP_MOIST",
            "SOURCE_CHECK_UP_DESIRE",
            "SOURCE_CHECK_UP_FLASHER",
            "SOURCE_CHECK_UP_SUBMIT",
            "SOURCE_CHECK_UP_DEVIATE",
            "SOURCE_CHECK_UP_ANTI",
            "SOURCE_CHECK_UP_LIKE",
            "UP_TALENT_CHECK",
        ]
        try:
            for function_name in functions:
                self._call(function_name)
        except ErbExecutionStopped as err:
            return {
                "ok": False,
                "status": "partial",
                "unsupported": [err.message, err.line],
                "erbFile": str(err.path.relative_to(self.root)).replace("\\", "/")
                if err.path.exists() and err.path.is_file()
                else "",
            }
        return {"ok": True, "status": "executed", "unsupported": []}

    def _strip_comment(self, line: str) -> str:
        return line.split(";", 1)[0]

    def _call(self, function_name: str) -> Any:
        function_name = self._format_call_name(function_name)
        if function_name.upper() == "GET_EX_KOJO_NUM":
            return 0
        function = self.functions.get(function_name.upper())
        if not function:
            raise ErbExecutionStopped(
                f"未支持: CALL {function_name} 找不到对应 ERB 函数",
                function_name,
                f"CALL {function_name}",
                self.root / "ERB",
            )

        block_stack: list[dict[str, bool]] = []
        loop_stack: list[dict[str, Any]] = []
        skip_next = False
        pc = 0
        steps = 0

        try:
            while pc < len(function.lines):
                steps += 1
                if steps > 20000:
                    raise ErbExecutionStopped("未支持: 单个 ERB 函数超过执行步数上限", function.name, "", function.path)

                line = function.lines[pc].strip()
                pc += 1
                if not line or line.startswith("$"):
                    continue

                keyword = self._keyword(line)
                if keyword == "FOR":
                    if not self._active(block_stack):
                        continue
                    args = self._split_args(line[4:].strip(), 3)
                    var_name = args[0].upper()
                    start = self._to_int(self._eval(args[1]))
                    end = self._to_int(self._eval(args[2]))
                    self._set(var_name, start)
                    if start < end:
                        loop_stack.append({"var": var_name, "end": end, "start_pc": pc})
                    else:
                        pc = self._find_matching_next(function.lines, pc)
                    continue
                if keyword == "NEXT":
                    if not loop_stack:
                        raise ErbExecutionStopped("未支持: NEXT 没有对应 FOR", function.name, line, function.path)
                    ctx = loop_stack[-1]
                    var_name = str(ctx["var"])
                    current = self._to_int(self._get(var_name)) + 1
                    self._set(var_name, current)
                    if current < self._to_int(ctx["end"]):
                        pc = self._to_int(ctx["start_pc"])
                    else:
                        loop_stack.pop()
                    continue

                if keyword == "IF":
                    parent_active = self._active(block_stack)
                    active = parent_active and self._truthy(self._eval(line[3:].strip()))
                    block_stack.append({"parent": parent_active, "active": active, "taken": active})
                    continue
                if keyword == "ELSEIF":
                    if not block_stack:
                        raise ErbExecutionStopped("未支持: ELSEIF 没有对应 IF", function.name, line, function.path)
                    ctx = block_stack[-1]
                    active = ctx["parent"] and not ctx["taken"] and self._truthy(self._eval(line[7:].strip()))
                    ctx["active"] = active
                    ctx["taken"] = ctx["taken"] or active
                    continue
                if keyword == "ELSE":
                    if not block_stack:
                        raise ErbExecutionStopped("未支持: ELSE 没有对应 IF", function.name, line, function.path)
                    ctx = block_stack[-1]
                    active = ctx["parent"] and not ctx["taken"]
                    ctx["active"] = active
                    ctx["taken"] = True
                    continue
                if keyword == "ENDIF":
                    if not block_stack:
                        raise ErbExecutionStopped("未支持: ENDIF 没有对应 IF", function.name, line, function.path)
                    block_stack.pop()
                    continue

                if not self._active(block_stack):
                    continue
                if skip_next:
                    skip_next = False
                    continue

                if keyword == "SIF":
                    skip_next = not self._truthy(self._eval(line[4:].strip()))
                    continue

                self._execute_line(function, line)
        except ErbReturn as ret:
            return ret.value

        return 0

    def _find_matching_next(self, lines: list[str], pc: int) -> int:
        depth = 1
        while pc < len(lines):
            keyword = self._keyword(lines[pc].strip())
            pc += 1
            if keyword == "FOR":
                depth += 1
            elif keyword == "NEXT":
                depth -= 1
                if depth == 0:
                    return pc
        return pc

    def _format_call_name(self, function_name: str) -> str:
        return re.sub(r"\{([^{}]+)\}", lambda match: str(self._eval(match.group(1))), function_name.strip())

    def _active(self, block_stack: list[dict[str, bool]]) -> bool:
        return all(ctx["active"] for ctx in block_stack)

    def _execute_line(self, function: ErbFunction, line: str) -> None:
        keyword = self._keyword(line)
        rest = line[len(keyword):].strip() if keyword else ""

        if keyword in {"PRINT", "PRINTS", "PRINTL", "PRINTFORM", "PRINTFORML", "PRINTFORMW"}:
            text = self._print_text(keyword, rest)
            if keyword in {"PRINTL", "PRINTFORML", "PRINTFORMW"} or not self.output:
                self.output.append(text)
            else:
                self.output[-1] += text
            return

        if keyword == "PRINTV":
            text = self._printv(rest)
            if self.output:
                self.output[-1] += text
            else:
                self.output.append(text)
            return

        if keyword == "CALL":
            self._call(rest.split(",", 1)[0].strip())
            return

        if keyword in {"CALLFORM", "TRYCALLFORM"}:
            function_name = rest.split(",", 1)[0].strip()
            function_name = self._format_call_name(self._format_text(function_name))
            if function_name.upper() in self.functions:
                self._call(function_name)
            elif keyword == "CALLFORM":
                raise ErbExecutionStopped(f"未支持: CALLFORM {function_name} 找不到对应 ERB 函数", function.name, line, function.path)
            return

        if keyword == "RETURN":
            raise ErbReturn(self._eval(rest) if rest else 0)

        if keyword == "RETURNF":
            raise ErbReturn(self._eval(rest) if rest else 0)

        if keyword in {"WAIT", "RESETCOLOR"}:
            return

        if keyword.startswith("#"):
            return

        if keyword in {"CUSTOMDRAWLINE", "DRAWLINE"}:
            fill = rest[:1] or "-"
            self.output.append(fill * 58)
            return

        if keyword == "TIMES":
            left, right = self._split_args(rest, 2)
            self._assign(left, "*=", right)
            return

        match = re.match(r"^(.+?)\s*(\+=|-=|\*=|/=|\|=|&=|=)\s*(.*)$", line)
        if match:
            left, op, expr = match.groups()
            self._assign(left.strip(), op, expr.strip())
            return

        raise ErbExecutionStopped(f"未支持: {keyword or line}", function.name, line, function.path)

    def _keyword(self, line: str) -> str:
        return line.split(None, 1)[0].upper() if line else ""

    def _split_args(self, text: str, expected: int) -> list[str]:
        parts = [part.strip() for part in text.split(",", expected - 1)]
        while len(parts) < expected:
            parts.append("")
        return parts

    def _assign(self, left: str, op: str, expr: str) -> None:
        old = self._get(left)
        if op == "=":
            value: int | str = self._eval_or_text(expr)
        else:
            right = self._eval(expr)
            old_num = self._to_int(old)
            right_num = self._to_int(right)
            if op == "+=":
                value = old_num + right_num
            elif op == "-=":
                value = old_num - right_num
            elif op == "*=":
                value = int(old_num * self._to_float(right))
            elif op == "/=":
                right_float = self._to_float(right)
                value = 0 if right_float == 0 else int(old_num / right_float)
            elif op == "|=":
                value = old_num | right_num
            elif op == "&=":
                value = old_num & right_num
            else:
                value = right_num
        self._set(left, value)

    def _eval_or_text(self, expr: str) -> int | str:
        if expr == "":
            return ""
        if (
            re.fullmatch(r"[\w\u0080-\uffff]+", expr)
            and ":" not in expr
            and expr.upper() not in self.scalars
            and expr.upper() not in {"MONEY", "DAY", "TIME", "TARGET", "PLAYER", "MASTER", "ASSI", "ASSIPLAY"}
            and not re.fullmatch(r"-?\d+(?:\.\d+)?", expr)
        ):
            return expr
        if any(ch in expr for ch in "%{}") or re.search(r"[^\w:()+\-*/%&|<>=!.\s]", expr):
            return self._format_text(expr)
        return self._eval(expr)

    def _eval(self, expr: str) -> Any:
        expr = expr.strip()
        if expr == "":
            return 0
        if re.fullmatch(r"-?\d+", expr):
            return int(expr)
        if re.fullmatch(r"-?\d+\.\d+", expr):
            return float(expr)

        translated = expr.replace("&&", " and ").replace("||", " or ")
        translated = re.sub(r"(?<![<>=!])!(?!=)", " not ", translated)
        translated = translated.replace("^", "**")
        translated = re.sub(
            r"\b(GET_KOJO_NUM|GET_EX_KOJO_NUM)\(([^()]*)\)",
            lambda match: str(self._call_function_expression(match.group(1), match.group(2))),
            translated,
        )

        refs: list[str] = []

        def hold_ref(match: re.Match[str]) -> str:
            refs.append(match.group(0))
            return f"__REF_{len(refs) - 1}__"

        translated = re.sub(
            r"\b(?:DOWN|EX|EX_FLAG|FLAG|GLOBAL|GOTJUEL|JUEL|LOCAL|LOCALS|NO|PALAMLV|RELATION|SAVESTR|TFLAG|UP|ABL|TALENT|CFLAG|MARK|BASE|MAXBASE|EXP|SOURCE|PALAM|TEQUIP|STAIN|LOSEBASE|RAND)(?::[\w\u0080-\uffff]+)+\b",
            hold_ref,
            translated,
        )
        translated = re.sub(
            r"\b[A-Z][A-Z0-9_]*\b",
            lambda match: f'get_var("{match.group(0)}")',
            translated,
        )
        for idx, ref in enumerate(refs):
            translated = translated.replace(f"__REF_{idx}__", f'get_var("{ref}")')

        try:
            return eval(translated, {"__builtins__": {}}, {"get_var": self._get})
        except Exception:
            return self._get(expr)

    def _call_function_expression(self, function_name: str, args_text: str = "") -> Any:
        previous_arg = self.scalars.get("ARG", 0)
        args = [arg.strip() for arg in args_text.split(",") if arg.strip()]
        if args:
            self.scalars["ARG"] = self._eval(args[0])
        elif function_name.upper() == "GET_KOJO_NUM":
            self.scalars["ARG"] = -1
        try:
            return self._call(function_name)
        finally:
            self.scalars["ARG"] = previous_arg

    def _format_text(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        text = re.sub(r"%([^%]+)%", lambda match: str(self._get(match.group(1))), text)
        text = re.sub(r"\{([^{}]+)\}", lambda match: str(self._eval(match.group(1))), text)
        return text

    def _print_text(self, keyword: str, text: str) -> str:
        text = text.strip()
        if keyword == "PRINTS" and re.fullmatch(r"[A-Z][A-Z0-9_]*(?::[\w\u0080-\uffff]+)+", text):
            return str(self._get(text))
        return self._format_text(text)

    def _printv(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        parts = []
        for item in re.split(r"\s*,\s*", text):
            if not item:
                continue
            if item.startswith("'") and item.endswith("'"):
                parts.append(item[1:-1])
            else:
                parts.append(str(self._eval(item)))
        return "".join(parts)

    def _get(self, name: str) -> Any:
        name = name.strip()
        if not name:
            return 0
        if name in self.scalars:
            return self.scalars[name]
        if name == "MONEY":
            return 10000
        if ":" not in name:
            return self.scalars.get(name, 0)

        head, *parts = name.split(":")
        head = head.upper()
        if head == "RAND":
            limit = max(1, self._to_int(self._resolve_index(parts[0] if parts else 1)))
            return randrange(limit)
        if head in self.name_tables:
            return self.name_tables[head].get(self._resolve_index(parts[0]), name)
        if head in {"DOWN", "EX", "EX_FLAG", "FLAG", "GLOBAL", "GOTJUEL", "JUEL", "LOCAL", "LOCALS", "NO", "PALAMLV", "RELATION", "SAVESTR", "TFLAG", "UP"}:
            return self.arrays.setdefault(head, {}).get(self._resolve_index(parts[0]), 0)
        if head in {"ABL", "TALENT", "CFLAG", "MARK", "BASE", "MAXBASE", "EXP", "SOURCE", "PALAM", "TEQUIP", "STAIN"}:
            char_index, key = self._char_key(parts)
            char = self._char(char_index)
            store = self._char_store(char, head)
            return store.get(key, 0)
        if head == "LOSEBASE":
            return self._char(self.target_index).losebase.get(self._resolve_index(parts[0]), 0)
        return 0

    def _set(self, name: str, value: int | str) -> None:
        name = name.strip()
        if ":" not in name:
            self.scalars[name.upper()] = value
            self._remember_change(f"{name.upper()} = {value}")
            return

        head, *parts = name.split(":")
        head = head.upper()
        if head in {"DOWN", "EX", "EX_FLAG", "FLAG", "GLOBAL", "GOTJUEL", "JUEL", "LOCAL", "LOCALS", "NO", "PALAMLV", "RELATION", "SAVESTR", "TFLAG", "UP"}:
            key = self._resolve_index(parts[0])
            self.arrays.setdefault(head, {})[key] = value
            self._remember_change(f"{head}:{key} = {value}")
            return
        if head in {"ABL", "TALENT", "CFLAG", "MARK", "BASE", "MAXBASE", "EXP", "SOURCE", "PALAM", "TEQUIP", "STAIN"}:
            char_index, key = self._char_key(parts)
            char = self._char(char_index)
            store = self._char_store(char, head)
            store[key] = self._to_int(value)
            if head == "BASE" and key == 0:
                char.hp = self._to_int(value)
            elif head == "BASE" and key == 1:
                char.mp = self._to_int(value)
            self._remember_change(f"{head}:{char_index}:{key} = {value}")
            return
        if head == "LOSEBASE":
            key = self._resolve_index(parts[0])
            self._char(self.target_index).losebase[key] = self._to_int(value)
            self._remember_change(f"LOSEBASE:{key} = {value}")
            return
        self.scalars[name] = value
        self._remember_change(f"{name} = {value}")

    def _remember_change(self, text: str) -> None:
        self.changed.append(text)

    def _resolve_index(self, raw: Any) -> Any:
        if isinstance(raw, int):
            return raw
        text = str(raw).strip()
        if text == "":
            return 0
        if text.upper() in self.scalars:
            return self.scalars[text.upper()]
        if text.upper() == "TARGET":
            return self.target_index
        if text.upper() in {"PLAYER", "MASTER"}:
            return 0
        if text.upper() == "ASSI":
            return self._to_int(self.scalars.get("ASSI", -1))
        if text.upper() in self.scalars:
            return self.scalars[text.upper()]
        if re.fullmatch(r"-?\d+", text):
            return int(text)
        return text

    def _char_key(self, parts: list[str]) -> tuple[int, Any]:
        if len(parts) >= 2:
            return self._char_index(parts[0]), self._resolve_index(parts[1])
        return self.target_index, self._resolve_index(parts[0] if parts else 0)

    def _char_index(self, raw: str) -> int:
        resolved = self._resolve_index(raw)
        if isinstance(resolved, int):
            return resolved
        return self.target_index

    def _char(self, index: int) -> CharacterState:
        if index < 0:
            index = self.target_index
        while index >= len(self.characters):
            self.characters.append(CharacterState(f"角色{index}", 1000, 1000, 1000, 1000))
        return self.characters[index]

    def _char_store(self, char: CharacterState, head: str) -> dict[Any, int]:
        if head == "ABL":
            return char.abl
        if head == "TALENT":
            return char.talent
        if head == "CFLAG":
            return char.cflag
        if head == "MARK":
            return char.mark
        if head == "BASE":
            return char.base
        if head == "MAXBASE":
            return char.maxbase
        if head == "EXP":
            return char.exp
        if head == "SOURCE":
            return char.source
        if head == "PALAM":
            return char.palam
        if head == "TEQUIP":
            return char.tequip
        if head == "STAIN":
            return char.stain
        return {}

    def _truthy(self, value: Any) -> bool:
        return self._to_int(value) != 0 if not isinstance(value, str) else value != ""

    def _to_int(self, value: Any) -> int:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0

    def _to_float(self, value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0


class GameSession:
    def __init__(self, root: Path):
        self.root = root
        self.train_names = load_train_names()
        self.look_info_tables = load_look_info_tables()
        self.explv_values = load_replace_array_initial_values("EXPLV", [0, 1, 4, 20, 50, 200, 400, 700, 1000, 1500, 2000])
        self.talent_condition_lines = load_erb_function_lines(ROOT / "ERB" / "CHARA_INFO_SHOW_TALENT.ERB", "SHOW_TALENT_CONDITION")
        self.seiin_check_lines = load_erb_function_lines(ROOT / "ERB" / "CHARA_INFO_SHOW_TALENT.ERB", "STC_SEIIN_CHECK")
        self.erb = ErbCommandBridge(root)
        self.screen = "TITLE"
        self.target_index = 1
        self.return_screen = "SHOP"
        self.log = ["Prototype ready."]
        self.recent_lines: list[str] = []
        self.filters = {
            "caress": False,
            "tools": False,
            "vagina": False,
            "anus": False,
            "sm": False,
        }
        self.characters = self._new_characters()
        self.item_catalog = load_item_catalog()
        self.items: dict[int, int] = {}
        self.money = 10000
        self.day = [0, 1, 1]
        self.time = 0
        self.ability_page = 0

    def _new_characters(self) -> list[CharacterState]:
        self.items = {}
        characters = [
            load_character_csv("Chara0.csv"),
            load_character_csv("Chara1.csv"),
            load_character_csv("Chara31.csv"),
        ]
        for character in characters:
            BodyMetricsGenerator(character).apply()
        characters[2].posture = "通常"
        return characters

    @property
    def target(self) -> CharacterState:
        return self.characters[self.target_index]

    def dispatch(self, payload: dict[str, object]) -> dict[str, object]:
        action = str(payload.get("action", ""))
        if action == "new-game":
            self.characters = self._new_characters()
            self.screen = "SHOP"
            self.target_index = 1
            self.recent_lines = ["新的猎物出现了！", "你作为魔王苏醒了..."]
        elif action == "go-target-select":
            self.screen = "TARGET_SELECT"
            self.recent_lines = ["现在选择角色是:你", "你要选择哪个对象？ <page.1>"]
        elif action == "select-target":
            self.target_index = int(payload.get("target", 1))
            self.screen = "TRAIN"
            self.recent_lines = []
        elif action == "train-command":
            self.screen = "TRAIN"
            self._run_train_command(int(payload.get("command", -1)))
        elif action == "toggle-filter":
            key = str(payload.get("filter", ""))
            if key in self.filters:
                self.filters[key] = not self.filters[key]
                self.recent_lines = [f"{self._filter_label(key)}：{'ON' if self.filters[key] else 'OFF'}"]
        elif action == "show-characters":
            self.return_screen = self.screen
            self.screen = "ABILITY"
            self.ability_page = int(payload.get("page", 0)) % 4
        elif action == "ability-page":
            self.screen = "ABILITY"
            self.ability_page = int(payload.get("page", self.ability_page)) % 4
        elif action == "return-from-ability":
            self.screen = self.return_screen
        elif action == "back-to-shop":
            self.screen = "SHOP"
            self._advance_time()
            self.recent_lines = ["返回商店。"]
        elif action == "back-to-shop-no-time":
            self.screen = "SHOP"
            self.recent_lines = ["返回商店。"]
        elif action == "go-shop-buy":
            self.screen = "SHOP_BUY"
            self.recent_lines = []
        elif action == "buy-item":
            self._handle_buy_item(int(payload.get("item", -1)))
        elif action == "frontend-save-disabled":
            self.recent_lines = ["保存需要后端游戏状态接口。前端不保存游戏信息。"]
        elif action == "frontend-load-disabled":
            self.recent_lines = ["读取需要后端游戏状态接口。前端不读取或持久化游戏信息。"]
        else:
            self.recent_lines = [f"{action or '未知操作'} 暂未实现。"]
        return self.view()

    def _run_train_command(self, command_id: int) -> None:
        self.erb.reset(self.characters, self.target_index)
        result = self.erb.execute_command(command_id)
        settlement = {"status": "skipped", "unsupported": []}
        palam_kojo = {"status": "skipped", "unsupported": []}
        mark_check = {"status": "skipped", "unsupported": []}
        mark_kojo = {"status": "skipped", "unsupported": []}
        if result.get("status") == "executed" and result.get("returnValue", 0) != 0:
            settlement = self.erb.run_source_settlement()
            if settlement.get("status") == "executed":
                palam_kojo = self.erb.run_kojo_message_palamcng()
                if palam_kojo.get("status") == "executed":
                    mark_check = self.erb.run_mark_got_check()
                if mark_check.get("status") == "executed" and self._mark_changed():
                    mark_kojo = self.erb.run_kojo_message_markcng()
        name = self.train_names.get(command_id, f"COM{command_id}")
        lines = [f"[{command_id}] {name}"]
        lines.extend(str(line) for line in result.get("output", []))
        lines.extend(self._apply_train_result(settlement))
        if result.get("status") != "executed":
            lines.append("ERB执行未完成。当前桥接器已停止在第一个不支持语句。")
            for item in result.get("unsupported", []):
                lines.append(f"未支持: {item}")
        elif settlement.get("status") == "partial":
            lines.append("ERB结算未完全执行。已显示目前可由真实 ERB 结算出的数值。")
            for item in settlement.get("unsupported", []):
                lines.append(f"未支持: {item}")
        elif palam_kojo.get("status") == "partial":
            lines.append("参数变化口上未完全执行。")
            for item in palam_kojo.get("unsupported", []):
                lines.append(f"未支持: {item}")
        elif mark_check.get("status") == "partial":
            lines.append("刻印检查未完全执行。")
            for item in mark_check.get("unsupported", []):
                lines.append(f"未支持: {item}")
        elif mark_kojo.get("status") == "partial":
            lines.append("刻印变化口上未完全执行。")
            for item in mark_kojo.get("unsupported", []):
                lines.append(f"未支持: {item}")
        self.recent_lines = lines

    def _mark_changed(self) -> bool:
        tflag = self.erb.arrays.get("TFLAG", {})
        return any(int(tflag.get(index, 0) or 0) for index in (21, 22, 23, 24))

    def _apply_train_result(self, settlement: dict[str, object]) -> list[str]:
        target = self.target
        lines = ["." * 118]

        base_changes = []
        for index, label in ((0, "体力"), (1, "气力")):
            loss = target.losebase.get(index, 0)
            if not loss:
                continue
            old = target.base.get(index, target.hp if index == 0 else target.mp)
            new = max(0, old - loss)
            target.base[index] = new
            if index == 0:
                target.hp = new
            else:
                target.mp = new
            base_changes.append(f"{label}{self._bar(new, target.maxbase.get(index, 1), 34)} -{loss}")
        lines.extend(base_changes)

        source_lines = self._source_result_lines(target)
        exp_lines = self._exp_result_lines(target)
        if source_lines or exp_lines:
            if base_changes:
                lines.append("-" * 58)
            lines.extend(source_lines)
            if source_lines and exp_lines:
                lines.append("-" * 58)
            lines.extend(exp_lines)
        palam_lines = self._palam_result_lines(target)
        if palam_lines:
            lines.append("-" * 58)
            lines.extend(palam_lines)
        elif settlement.get("status") == "skipped":
            lines.append("本次命令没有进入调教结算。")
        return lines

    def _source_result_lines(self, target: CharacterState) -> list[str]:
        rows = []
        for source_id, value in sorted(target.source.items(), key=lambda item: self._source_sort_key(item[0])):
            if not value:
                continue
            label = self._source_name(source_id)
            rows.append(f"{label:<8}+{value}")
        return rows

    def _exp_result_lines(self, target: CharacterState) -> list[str]:
        lines = []
        for exp_id, value in sorted(target.exp.items(), key=lambda item: str(item[0])):
            if value:
                label = self.erb.name_tables["EXPNAME"].get(exp_id, f"EXP:{exp_id}")
                lines.append(f"{label:<8}+{value}")
        return lines

    def _palam_result_lines(self, target: CharacterState) -> list[str]:
        lines = []
        for palam_id in self._palam_display_order():
            up = self._array_int("UP", palam_id)
            down = self._array_int("DOWN", palam_id)
            if up <= 0 and down <= 0:
                continue
            old = target.palam.get(palam_id, 0)
            new = max(0, old + up - down)
            target.palam[palam_id] = new
            label = self._palam_name(palam_id)
            plus = f"+{up}" if up > 0 else "    "
            minus = f"-{down}" if down > 0 else "    "
            message = self._palam_message(palam_id, new)
            lines.append(f"{label:<4} {old:>5}{plus:>7}{minus:>7} = {new:>5}{message}")
        return lines

    def _palam_display_order(self) -> list[int]:
        return [0, 1, 2, 14, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]

    def _array_int(self, name: str, key: int) -> int:
        return int(self.erb.arrays.get(name, {}).get(key, 0) or 0)

    def _palam_message(self, palam_id: int, value: int) -> str:
        lv = self.erb.arrays["PALAMLV"]
        if palam_id == 3:
            if value < lv[2]:
                return "（干如沙漠）"
            if value < lv[4]:
                return "（晨露般稍湿）"
            return "（洪水泛滥）"
        if palam_id == 4:
            if value < lv[1]:
                return "（没有好感）"
            if value < lv[4]:
                return "（抱有好感）"
            return "（寄予信赖）"
        if palam_id == 5:
            if value < lv[1]:
                return "（没欲望）"
            if value < lv[4]:
                return "（正在发情）"
            return "（成为快乐的俘虏）"
        if palam_id == 6:
            if value < lv[2]:
                return "（还未屈服）"
            if value < lv[4]:
                return "（稍显弱势）"
            return "（顶礼膜拜）"
        if palam_id == 7:
            if value < lv[1]:
                return "（不是很懂）"
            if value < lv[4]:
                return "（开心地学）"
            return "（充分掌握）"
        if palam_id == 8:
            if value < lv[1]:
                return "（没有感到羞耻）"
            if value < lv[3]:
                return "（感到害羞）"
            if value < lv[4]:
                return "（强烈的羞耻）"
            return "（羞愧欲死）"
        if palam_id == 9:
            if value < lv[1]:
                return "（没有感到疼痛）"
            if value < lv[3]:
                return "（有点痛楚）"
            if value < lv[4]:
                return "（疼得不得了）"
            return "（几乎痛得晕过去）"
        if palam_id == 10:
            if value < lv[1]:
                return "（相当坦然）"
            if value < lv[3]:
                return "（稍稍害怕）"
            if value < lv[4]:
                return "（怕得不行）"
            return "（抓狂的恐怖）"
        if palam_id == 11:
            if value < lv[1]:
                return "（并不讨厌）"
            if value < lv[2]:
                return "（有点反感）"
            if value < lv[3]:
                return "（讨厌）"
            if value < lv[4]:
                return "（强烈的憎恨）"
            return "（抱有杀意）"
        if palam_id == 12:
            if value < lv[1]:
                return "（没有感到不快）"
            if value < lv[2]:
                return "（心情不好）"
            if value < lv[4]:
                return "（相当不快）"
            return "（抓狂的不快）"
        if palam_id == 13:
            if value < lv[1]:
                return "（没有郁闷）"
            if value < lv[2]:
                return "（稍欠精神）"
            if value < lv[4]:
                return "（消沉）"
            return "（完全绝望）"
        return ""

    def _source_sort_key(self, source_id: int | str) -> tuple[int, str]:
        order = {0: 0, 1: 1, 2: 2, 17: 3, 3: 4, 4: 5, 5: 6, 6: 7, 8: 8, 12: 9, 13: 10, 14: 11}
        return (order.get(source_id, 999), str(source_id))

    def _source_name(self, source_id: int | str) -> str:
        if isinstance(source_id, int):
            return self.erb.name_tables["SOURCENAME"].get(source_id, f"SOURCE:{source_id}")
        return str(source_id)

    def _abl_name(self, abl_id: int | str) -> str:
        if isinstance(abl_id, int):
            return self.erb.name_tables["ABLNAME"].get(abl_id, f"ABL:{abl_id}")
        return str(abl_id)

    def _exp_name(self, exp_id: int | str) -> str:
        if isinstance(exp_id, int):
            return self.erb.name_tables["EXPNAME"].get(exp_id, f"EXP:{exp_id}")
        return str(exp_id)

    def _mark_name(self, mark_id: int | str) -> str:
        if isinstance(mark_id, int):
            return self.erb.name_tables["MARKNAME"].get(mark_id, f"MARK:{mark_id}")
        return str(mark_id)

    def _palam_name(self, palam_id: int | str) -> str:
        if isinstance(palam_id, int):
            return self.erb.name_tables["PALAMNAME"].get(palam_id, f"PALAM:{palam_id}")
        return str(palam_id)

    def _talent_name(self, talent_id: int | str) -> str:
        if isinstance(talent_id, int):
            return self.erb.name_tables["TALENTNAME"].get(talent_id, f"TALENT:{talent_id}")
        return str(talent_id)

    def _advance_time(self) -> None:
        self.time += 1
        if self.time >= 2:
            self.time = 0
            self.day[2] += 1

    def _handle_buy_item(self, item_id: int) -> None:
        self.screen = "SHOP_BUY"
        entry = self.item_catalog.get(item_id)
        if entry is None:
            self.recent_lines = [f"无效的道具编号：{item_id}"]
            return
        name = str(entry["name"])
        price = int(entry["price"])
        if self.money < price:
            self.recent_lines = [f"金钱不足！{name}需要{price}点，当前只有{self.money}点。"]
            return
        # Knowledge items: grant talent, don't keep item
        knowledge_talent_map = {38: 91, 39: 325, 42: 55, 54: 327, 56: 328}
        if item_id in knowledge_talent_map:
            talent_id = knowledge_talent_map[item_id]
            master = self.characters[0] if self.characters else None
            if master and master.talent.get(talent_id, 0):
                self.recent_lines = [f"已经掌握了{name}。"]
                return
            self.money -= price
            if master:
                master.talent[talent_id] = 1
            self.recent_lines = [f"《购买了{name}》", f"{self.characters[0].name if self.characters else '主人'}掌握了【{name}】！"]
            return
        # Technique level item
        if item_id == 52:
            master = self.characters[0] if self.characters else None
            if master and master.abl.get(12, 0) >= 10:
                self.recent_lines = ["技巧等级已达上限。"]
                return
            self.money -= price
            if master:
                master.abl[12] = master.abl.get(12, 0) + 1
                lv = master.abl[12]
                self.recent_lines = [f"《购买了{name}》", f"{self.characters[0].name if self.characters else '主人'}的技巧LV{lv}了！"]
            return
        # Experience item (53): grant exp, don't keep
        if item_id == 53:
            self.money -= price
            self.recent_lines = [f"《购买了{name}》", "请选择使用对象（当前版本自动给予主人）。"]
            master = self.characters[0] if self.characters else None
            if master:
                master.exp[80] = master.exp.get(80, 0) + 10
                self.recent_lines.append(f"得到了10点经验值。")
            return
        # Trap level item (55)
        if item_id == 55:
            self.money -= price
            self.items[item_id] = self.items.get(item_id, 0) + 1
            self.recent_lines = [f"《购买了{name}》"]
            return
        # Normal items (consumables and equipment)
        self.money -= price
        self.items[item_id] = self.items.get(item_id, 0) + 1
        count = self.items[item_id]
        self.recent_lines = [f"《购买了{name}》", f"当前持有：{count}个"]

    def view(self) -> dict[str, object]:
        if self.screen == "TITLE":
            return self._title_view()
        if self.screen == "SHOP":
            return self._shop_view()
        if self.screen == "SHOP_BUY":
            return self._shop_buy_view()
        if self.screen == "TARGET_SELECT":
            return self._target_select_view()
        if self.screen == "TRAIN":
            return self._training_view()
        if self.screen == "ABILITY":
            return self._ability_view()
        return self._title_view()

    def _title_view(self) -> dict[str, object]:
        return {
            "mode": "normal",
            "debugLine": "[DEBUG] 标题界面 - Day:0, Time:0, MONEY:10000",
            "screenLabel": "ERA_MAOU_EX 0.92",
            "dateStatus": self._status_text(),
            "targetInfo": "",
            "assistantInfo": "",
            "itemInfo": "技巧Lv： Lv0",
            "trapInfo": "所持知识：",
            "regionInfo": "",
            "dailyInfo": "",
            "commands": [
                [self._cmd("1", "新的游戏", "new-game"), self._cmd("0", "读取游戏", "frontend-load-disabled")],
                [self._cmd("777", "设置", "stub-feature", feature="设置")],
                [],
            ],
            "messages": ["eraMaouEx Browser Prototype", "请选择开始方式。"],
        }

    def _shop_view(self) -> dict[str, object]:
        target = self.target
        return {
            "mode": "normal",
            "debugLine": f"[DEBUG] 进入商店 - Day:{self.day[2] - 1}, Time:{self.time}, MONEY:{self.money}",
            "screenLabel": "",
            "dateStatus": self._status_text(),
            "targetInfo": f"{target.name}\nHP:{target.hp}/{target.max_hp}　MP:{target.mp}/{target.max_mp}",
            "assistantInfo": "",
            "itemInfo": "技巧Lv： Lv0",
            "trapInfo": "所持知识：",
            "regionInfo": "",
            "dailyInfo": "",
            "commands": [
                [
                    self._cmd("100", "调教", "go-target-select"),
                    self._cmd("103", "处刑", "stub-feature", feature="处刑"),
                    self._empty("---"),
                    self._cmd("109", "侵略", "stub-feature", feature="侵略"),
                    self._cmd("120", "召唤", "stub-feature", feature="召唤"),
                    self._cmd("300", "读取", "frontend-load-disabled"),
                ],
                [
                    self._cmd("101", "能力显示", "show-characters"),
                    self._cmd("104", "迎击", "stub-feature", feature="迎击"),
                    self._cmd("107", "购物", "go-shop-buy"),
                    self._empty("---"),
                    self._cmd("199", "休息", "back-to-shop"),
                    self._cmd("777", "设置", "stub-feature", feature="设置"),
                ],
                [
                    self._cmd("102", "地下城", "stub-feature", feature="地下城"),
                    self._cmd("105", "能力值提升", "stub-feature", feature="能力值提升"),
                    self._cmd("108", "换装", "stub-feature", feature="换装"),
                    self._empty("---"),
                    self._cmd("200", "保存", "frontend-save-disabled"),
                    self._cmd("888", "通信", "stub-feature", feature="通信"),
                ],
            ],
            "messages": self.recent_lines or self.log,
        }

    # --- Shop buy categories ---
    _SHOP_CATEGORIES = [
        ("调教道具", list(range(0, 24))),
        ("消耗道具", [24, 25, 26, 27, 28, 29, 30, 31, 34, 35, 37]),
        ("知识与强化", [38, 39, 42, 52, 53, 54, 55, 56]),
        ("陷阱", list(range(60, 87))),
    ]
    _SHOP_NON_CONSUMABLE_IDS = set(range(0, 24)) | {37, 39, 42, 90}

    def _shop_buy_view(self) -> dict[str, object]:
        commands: list[list[dict[str, object]]] = []
        for cat_title, item_ids in self._SHOP_CATEGORIES:
            row: list[dict[str, object]] = []
            for item_id in item_ids:
                entry = self.item_catalog.get(item_id)
                if entry is None:
                    continue
                # Skip already-owned non-consumables
                if item_id in self._SHOP_NON_CONSUMABLE_IDS and self.items.get(item_id, 0) > 0:
                    continue
                # Skip knowledge items already acquired (tracked via talent)
                knowledge_talent_map = {38: 91, 39: 325, 42: 55, 54: 327, 56: 328}
                if item_id in knowledge_talent_map:
                    master = self.characters[0] if self.characters else None
                    if master and master.talent.get(knowledge_talent_map[item_id], 0):
                        continue
                name = str(entry["name"])
                price = int(entry["price"])
                label = f"{name}({price})"
                row.append(self._cmd(str(item_id), label, "buy-item", item=item_id))
                if len(row) >= 3:
                    commands.append(row)
                    row = []
            if row:
                commands.append(row)
        commands.append([self._cmd("999", "返回", "back-to-shop-no-time")])
        return {
            "mode": "normal",
            "debugLine": f"[DEBUG] 购物 - MONEY:{self.money}",
            "screenLabel": "黑市商人",
            "dateStatus": self._status_text(),
            "targetInfo": f"所持金：{self.money}点",
            "assistantInfo": "",
            "itemInfo": "",
            "trapInfo": "",
            "regionInfo": "",
            "dailyInfo": "",
            "commands": commands,
            "messages": self.recent_lines or ["《可以购买用于调教的物品》", "请选择要购买的道具。"],
        }

    def _target_select_view(self) -> dict[str, object]:
        target_rows = [
            self._cmd(str(display_index), char.name, "select-target", target=index)
            for display_index, (index, char) in enumerate((item for item in enumerate(self.characters) if item[0] != 0))
        ]
        return {
            "mode": "target-select",
            "debugLine": "100",
            "screenLabel": "",
            "dateStatus": "",
            "targetInfo": "",
            "assistantInfo": "",
            "itemInfo": "",
            "trapInfo": "",
            "regionInfo": "",
            "dailyInfo": "",
            "commands": [
                target_rows,
                [self._cmd("1000", "返回", "back-to-shop-no-time")],
            ],
            "messages": ["现在选择角色是:你", "你要选择哪个对象？ <page.1>"],
        }

    def _training_view(self) -> dict[str, object]:
        return {
            "mode": "training",
            "trainingText": self._training_text(),
            "trainingCommands": self._training_commands(),
        }

    def _ability_view(self) -> dict[str, object]:
        return {
            "mode": "ability",
            "abilityText": self._ability_text(),
            "characterDetail": self._character_detail(self.target_index),
            "abilityPage": self.ability_page,
            "abilityCommands": self._ability_commands(),
        }

    def _training_text(self) -> str:
        target = self.target
        hp = target.base.get(0, target.hp)
        mp = target.base.get(1, target.mp)
        max_hp = target.maxbase.get(0, target.max_hp)
        max_mp = target.maxbase.get(1, target.max_mp)
        lines = ["-" * 118]
        if self.recent_lines:
            lines.extend(self.recent_lines)
        else:
            lines.extend([
                f"{target.name}的第一次调教开始了，把她变成棒棒哒性奴隶吧！",
                f"{target.posture}的{target.name}被带到调教室了。",
                "-" * 118,
                "　「你觉得我会变成你想要的那样吗？」",
                f"身为无头骑士的{target.name}还很涉世不深的样子。……",
            ])
        lines.extend([
            "-" * 118,
            "1日（上午）",
            f"{target.name}　调教中　　调教者：你",
            f"体力{self._bar(hp, max_hp, 34)}({hp}/{max_hp})",
            f"气力{self._bar(mp, max_mp, 34)}({mp}/{max_mp})",
            f"【{target.posture}】",
            *self._param_lines(target),
            f"射精（你）　　[{'-' * 0}{'.' * 36}](0/10000)",
            "",
            "",
            "-" * 118,
            "",
            "",
            "",
            "",
            "",
        ])
        return "\n".join(lines)

    def _ability_text(self) -> str:
        target = self.target
        lines = self._ability_header_lines(target)
        page = self.ability_page % 4
        if page == 0:
            lines.extend(self._ability_page_basic(target))
        elif page == 1:
            lines.extend(self._ability_page_experience(target))
        elif page == 2:
            lines.extend(self._ability_page_appearance(target))
        else:
            lines.extend(self._ability_page_conditions(target))
        lines.extend(["", "", "", "", "", "", "", "", "-" * 118])
        return "\n".join(lines)

    def _ability_header_lines(self, target: CharacterState) -> list[str]:
        hp = target.base.get(0, target.hp)
        mp = target.base.get(1, target.mp)
        max_hp = target.maxbase.get(0, target.max_hp)
        max_mp = target.maxbase.get(1, target.max_mp)
        age = self._age_text(target)
        bust = self._bust_text(target)
        waist = self._body_metric_text(target, "W", 456, "cm")
        hip = self._body_metric_text(target, "H", 457, "cm")
        lines = [
            "=" * 118,
            f"NO.{target.no:<4}{target.name:<24}{age:^44}",
            "." * 118,
            f"一人称：{self._self_call(target):<18}　[8] 一人称重设　　来源 {target.source_file}",
            f"体力{self._bar(hp, max_hp, 34)}({hp}/{max_hp})　{self._body_metric_text(target, '身高', 453, 'cm')}",
            f"气力{self._bar(mp, max_mp, 34)}({mp}/{max_mp})　{self._body_metric_text(target, '体重', 454, 'kg')}",
            f"三围：{bust}　{waist}　{hip}",
            "." * 118,
        ]
        return lines

    def _ability_page_basic(self, target: CharacterState) -> list[str]:
        lines: list[str] = []
        lines.extend(self._talent_group_lines(target))
        lines.append("." * 118)
        abl_lines = self._ability_abl_lines(target)
        if abl_lines:
            lines.extend(abl_lines)
            lines.append("." * 118)
        lines.append(self._mark_line(target))
        lines.append("." * 118)
        return lines

    def _ability_page_experience(self, target: CharacterState) -> list[str]:
        lines = [self._mark_line(target), "." * 118]
        exp_lines = self._experience_lines(target)
        lines.extend(exp_lines if exp_lines else ["　经验：无"])
        lines.append(self._level_experience_line(target))
        lines.append("." * 118)
        return lines

    def _ability_page_appearance(self, target: CharacterState) -> list[str]:
        lines = [
            self._equipment_line(target),
            "." * 118,
            f"[结婚对象:{self._marriage_text(target)}]",
            "[外观]",
        ]
        lines.extend(self._look_lines(target))
        lines.append(f"[共{len([key for key in range(300, 318) if target.talent.get(key)])}个外观/背景CSV字段]")
        lines.append("." * 118)
        return lines

    def _ability_page_conditions(self, target: CharacterState) -> list[str]:
        lines = ["素质取得条件："]
        lines.extend(self._condition_lines(target))
        lines.append("." * 118)
        lines.append("※ 当前页结构对应 CHARA_INFO_SHOW.ERB CASE 3。")
        lines.append("※ 真实条件入口：ERB/CHARA_INFO_SHOW_TALENT.ERB @SHOW_TALENT_CONDITION。")
        lines.append("※ 当前页由后端解析 STC_* 条件行生成；前端不保存任何素质条件或游戏数据。")
        return lines

    def _talent_group_lines(self, target: CharacterState) -> list[str]:
        return [
            f"　性别：{self._sex_chips(target)}",
            f"　性格：{self._talent_chips(target, [(160, 180), (10, 40), (60, 70), (150, 157)], skip={153, 154})}",
            f"　体质：{self._talent_chips(target, [(40, 50), (99, 140), (244, 250)], extra=[56, 57, 153, 154, 158, 253, 255, 256, 258])}",
            f"　技术：{self._talent_chips(target, [(50, 60), (90, 99), (180, 190)], skip={56, 57}, extra=[113, 117, 118, 126, 325, 327, 328, 329])}",
            f"　性癖：{self._talent_chips(target, [(70, 90), (101, 109), (140, 144), (230, 240), (270, 273)])}",
            f"　战斗：{self._talent_chips(target, [(200, 221), (240, 265)])}",
        ]

    def _sex_chips(self, target: CharacterState) -> str:
        chips = ["[男]" if target.talent.get(122) else "[扶她]" if target.talent.get(121) else "[女]"]
        if target.talent.get(0):
            chips.append(f"[{self._talent_name(0)}]")
        if target.talent.get(273):
            chips.append(f"[{self._talent_name(273)}]")
        return "".join(chips)

    def _talent_chips(
        self,
        target: CharacterState,
        ranges: list[tuple[int, int]],
        skip: set[int] | None = None,
        extra: list[int] | None = None,
    ) -> str:
        skip = skip or set()
        keys: list[int] = []
        for start, end in ranges:
            keys.extend(range(start, end))
        keys.extend(extra or [])
        seen: set[int] = set()
        chips: list[str] = []
        for key in keys:
            if key in seen or key in skip:
                continue
            seen.add(key)
            if target.talent.get(key):
                chips.append(f"[{self._talent_name(key)}]")
        return "".join(chips) or "[...]"

    def _ability_abl_lines(self, target: CharacterState) -> list[str]:
        rows = []
        for key in self._abl_display_order():
            value = int(target.abl.get(key, 0) or 0)
            if value:
                rows.append(f"{self._abl_name(key)} - LV{value}")
        return self._columns(rows, 4, 22)

    def _mark_line(self, target: CharacterState) -> str:
        return (
            f"苦痛:LV{target.mark.get(0, 0)} [{self._level_bar(target.mark.get(0, 0), 3)}]　"
            f"快乐:LV{target.mark.get(1, 0)} [{self._level_bar(target.mark.get(1, 0), 3)}]　"
            f"屈服:LV{target.mark.get(2, 0)} [{self._level_bar(target.mark.get(2, 0), 3)}]　"
            f"反抗:LV{target.mark.get(3, 0)} [{self._level_bar(target.mark.get(3, 0), 3)}]"
        )

    def _experience_lines(self, target: CharacterState) -> list[str]:
        rows = [f"{self._exp_name(key)}:{value:>6}" for key, value in sorted(target.exp.items()) if value]
        return self._columns(rows, 4, 24)

    def _level_experience_line(self, target: CharacterState) -> str:
        level = int(target.cflag.get(9, 1) or 1)
        battle_exp = int(target.exp.get(80, 0) or 0)
        if self.target_index == 0:
            need = level * 100 + 10
            total = level * level * 50 - level * 40 + battle_exp
        elif target.talent.get(220):
            need = level * 20 + 10
            total = level * level * 10 - 10 + battle_exp
        else:
            need = level * 10 + 10
            total = level * level * 5 + level * 5 - 10 + battle_exp
        return f"　{target.name}当前是Lv{level}，战斗经验值总计{total}点，本级经验：{battle_exp}/{need}"

    def _equipment_line(self, target: CharacterState) -> str:
        weapon = self._equip_name(target.cflag.get(550))
        armor_a = self._equip_name(target.cflag.get(551))
        armor_b = self._equip_name(target.cflag.get(552))
        return f"[武器]：{weapon}　 [装饰A]：{armor_a}　 [装饰B]：{armor_b}"

    def _equip_name(self, value: Any) -> str:
        if value is None:
            return "未载入"
        if int(value or 0) < 0:
            return "未装备"
        return f"ID {value}"

    def _marriage_text(self, target: CharacterState) -> str:
        love = int(target.cflag.get(2, 0) or 0)
        return f"未婚][亲爱值:{love}"

    def _look_lines(self, target: CharacterState) -> list[str]:
        look = lambda key: self._look_info(target, key)
        lines = [
            f"头发是{look('头发颜色')}的{look('头发状态')}。　留着{look('头发长度')}发，{look('头发修剪方式')}的{look('发型')}。",
            f"她的深邃眼是{look('瞳色')}的呢。嘴唇是{look('唇')}的。",
            f"标准的体型……乳头嘛……{look('乳头')}呢。下面的毛毛……{look('阴毛状态')}……。",
            f"美貌是她的魅力点呢。 总之{look('魅力点')}是她的习惯呢。",
            f"身上的钱……身无分文……呜呜。",
            f"喜欢的东西是……{look('喜欢的东西')}。",
            f"{target.name}现在的样子是{look('种族')}，{look('成为勇者前的生活')}出身，因为{look('成为勇者的契机')}成为勇者。",
        ]
        missing_metrics = [label for label, key in (("年龄", 451), ("身高", 453), ("体重", 454), ("B", 455), ("W", 456), ("H", 457)) if key not in target.cflag]
        if missing_metrics:
            lines.append(f"未载入字段：{'、'.join(missing_metrics)}（需接入 CHARA_MAKE.ERB 或完整角色状态）")
        return lines

    def _condition_lines(self, target: CharacterState) -> list[str]:
        values = [
            f"好感度 {int(target.cflag.get(2, 0) or 0) / 10:.1f}%",
            f"顺从LV{target.abl.get(10, 0)}",
            f"欲望LV{target.abl.get(11, 0)}",
            f"技巧LV{target.abl.get(12, 0)}",
            f"侍奉精神LV{target.abl.get(16, 0)}",
            f"露出癖LV{target.abl.get(17, 0)}",
            f"抖MLV{target.abl.get(21, 0)}",
            f"快乐刻印LV{target.mark.get(1, 0)}",
            f"屈服刻印LV{target.mark.get(2, 0)}",
            f"反抗刻印LV{target.mark.get(3, 0)}",
        ]
        exp_values = [
            f"{self._exp_name(key)} {target.exp.get(key, 0)}"
            for key in (8, 21, 22, 30, 33, 50, 56, 74, 80)
            if target.exp.get(key, 0)
        ]
        renderer = TalentConditionRenderer(
            target=target,
            name_tables=self.erb.name_tables,
            condition_lines=self.talent_condition_lines,
            seiin_check_lines=self.seiin_check_lines,
            explv_values=self.explv_values,
        )
        condition_lines, unsupported = renderer.render()
        lines = [
            "当前能力/刻印摘要：",
            "　" + "　".join(values),
            "当前相关经验摘要：",
            "　" + ("　".join(exp_values) if exp_values else "无"),
            "." * 118,
        ]
        lines.extend(condition_lines if condition_lines else ["未解析出条件行。"])
        if unsupported:
            lines.append("." * 118)
            lines.append("未完全接入的条件表达式：")
            lines.extend(f"　- {item}" for item in unsupported[:8])
        return lines

    def _look_info(self, target: CharacterState, key: str) -> str:
        value_by_key = {
            "头发颜色": 300,
            "头发状态": 301,
            "头发长度": 302,
            "头发修剪方式": 303,
            "发型": 304,
            "目": 305,
            "瞳色": 306,
            "唇": 307,
            "体型": 308,
            "乳头": 309,
            "阴毛状态": 310,
            "魅力点": 312,
            "癖": 313,
            "种族": 314,
            "成为勇者前的生活": 315,
            "成为勇者的契机": 316,
            "喜欢的东西": 317,
        }
        talent_key = value_by_key[key]
        value = int(target.talent.get(talent_key, 0) or 0)
        if talent_key not in target.talent:
            return "未载入"
        return self._look_value(key, value)

    def _look_value(self, key: str, value: int) -> str:
        for start, end, label in self.look_info_tables.get(key, []):
            if start <= value <= end:
                return label
        return f"{key}:{value}"

    def _ability_commands(self) -> list[list[dict[str, object]]]:
        prev_page = (self.ability_page - 1) % 4
        next_page = (self.ability_page + 1) % 4
        if self.ability_page == 0:
            primary = [
                self._ability_cmd("0", "改名", "stub-feature", feature="改名"),
                self._ability_cmd("1", "还原名字", "stub-feature", feature="还原名字"),
                self._ability_cmd("2", "转职", "stub-feature", feature="转职"),
                self._ability_cmd("4", "结婚", "stub-feature", feature="结婚"),
                self._ability_cmd("10", "提升能力", "stub-feature", feature="提升能力"),
                self._ability_cmd("9", "收藏", "stub-feature", feature="收藏"),
            ]
        else:
            primary = [
                self._ability_cmd("6", "设为目标", "select-target", target=self.target_index),
                self._ability_cmd("18", "卖春积极性 - 普通", "stub-feature", feature="卖春积极性"),
                self._ability_cmd("11", "更换服装", "stub-feature", feature="更换服装"),
                self._ability_cmd("15", "提升等级", "stub-feature", feature="提升等级"),
                self._ability_cmd("17", "灵魂转移", "stub-feature", feature="灵魂转移"),
            ]
        return [
            primary,
            [
                self._ability_cmd("101", "前页", "ability-page", page=prev_page),
                self._ability_cmd("100", "返回", "return-from-ability"),
                self._ability_cmd("102", "后页", "ability-page", page=next_page),
            ],
            [self._ability_cmd("500", "前一人", "stub-feature", feature="前一人")],
        ]

    def _ability_cmd(self, code: str, name: str, action: str, **extra: object) -> dict[str, object]:
        extra["layout"] = "code-first"
        return self._cmd(code, name, action, **extra)

    def _age_text(self, target: CharacterState) -> str:
        if 451 not in target.cflag:
            return "年龄 未载入"
        if 452 in target.cflag and target.cflag[451] != target.cflag[452]:
            return f"{target.cflag[452]} 岁（换算人类 {target.cflag[451]} 岁）"
        return f"{target.cflag[451]} 岁"

    def _body_metric_text(self, target: CharacterState, label: str, key: int, unit: str) -> str:
        if key not in target.cflag:
            return f"{label} 未载入"
        value = int(target.cflag[key] or 0)
        return f"{label} {value // 10}.{value % 10} {unit}"

    def _bust_text(self, target: CharacterState) -> str:
        bust = self._body_metric_text(target, "B", 455, "cm")
        cup = self._cup_size_text(target)
        return f"{bust} {cup}" if cup else bust

    def _cup_size_text(self, target: CharacterState) -> str:
        if 455 not in target.cflag or 453 not in target.cflag:
            return ""
        under_bust = self._under_bust(target)
        diff = int(target.cflag[455] - under_bust)
        cup_index = diff // 25
        cup_map = {
            0: "-",
            2: "AAA",
            3: "AA",
            4: "A",
            5: "B",
            6: "C",
            7: "D",
            8: "E",
            9: "F",
            10: "G",
            11: "H",
            12: "I",
            13: "J",
            14: "K",
            15: "L",
            16: "M",
            17: "N",
            18: "O",
            19: "P",
            20: "Q",
            21: "R",
            22: "S",
            23: "T",
            24: "U",
            25: "V",
            26: "W",
            27: "X",
            28: "Y",
            29: "Z",
        }
        if cup_index <= 1:
            return "[-]"
        return f"[{cup_map.get(cup_index, 'Z+')}]"

    def _under_bust(self, target: CharacterState) -> int:
        if 459 in target.cflag:
            return int(target.cflag[459] or 0)
        if 453 not in target.cflag:
            return 0
        height = int(target.cflag[453] or 0)
        body_type = int(target.talent.get(308, 0) or 0)
        under_bust = height * (43100 + body_type) // 100000
        if target.talent.get(248):
            under_bust = under_bust * 105 // 100
        if target.talent.get(256):
            under_bust = under_bust * 98 // 100
        return under_bust

    def _self_call(self, target: CharacterState) -> str:
        return target.cstr.get(0) or "我"

    def _level_bar(self, value: int, width: int) -> str:
        filled = max(0, min(width, int(value or 0)))
        return "*" * filled + "." * (width - filled)

    def _columns(self, rows: list[str], columns: int, width: int) -> list[str]:
        lines: list[str] = []
        for index in range(0, len(rows), columns):
            lines.append("　".join(item.ljust(width) for item in rows[index : index + columns]))
        return lines

    def _param_lines(self, target: CharacterState) -> list[str]:
        p = target.palam
        rows = [
            [("阴核", 0), ("私处", 1), ("肛门", 2)],
            [("润滑", 3), ("慕顺", 4), ("欲情", 5)],
            [("屈服", 6), ("习得", 7), ("耻情", 8)],
            [("苦痛", 9), ("恐怖", 10), ("反感", 11)],
            [("不快", 12), ("抑郁", 13), ("乳房", 14)],
            [("局部", "local"), ("", ""), ("", "")],
        ]
        return ["　".join(self._param_cell(name, p.get(key, 0)) for name, key in row) for row in rows]

    def _runtime_summary_lines(self, target: CharacterState) -> list[str]:
        groups = [
            ("SOURCE", target.source),
            ("LOSEBASE", target.losebase),
            ("EXP", target.exp),
            ("TFLAG", self.erb.arrays.get("TFLAG", {})),
        ]
        lines: list[str] = []
        for label, values in groups:
            if values:
                pairs = "　".join(f"{key}:{value}" for key, value in sorted(values.items(), key=lambda item: str(item[0]))[:8])
                lines.append(f"{label}　{pairs}")
        return lines

    def _character_detail(self, index: int) -> dict[str, object]:
        char = self.characters[index]
        sections = [
            {"title": "PALAM", "variant": "palam", "rows": self._value_rows(self._palam_display_order(), char.palam, self._palam_name, include_zero=True)},
            {"title": "素质", "variant": "chips", "rows": self._value_rows(sorted(char.talent, key=lambda key: str(key)), char.talent, self._talent_name)},
            {"title": "能力", "variant": "pairs", "rows": self._value_rows(self._abl_display_order(), char.abl, self._abl_name)},
            {"title": "刻印", "variant": "marks", "rows": self._value_rows(self._mark_display_order(), char.mark, self._mark_name, include_zero=True)},
            {"title": "经验", "variant": "pairs", "rows": self._value_rows(sorted(char.exp, key=lambda key: str(key)), char.exp, self._exp_name)},
            {"title": "SOURCE", "variant": "pairs", "rows": self._value_rows(sorted(char.source, key=lambda key: str(key)), char.source, self._source_name)},
            {"title": "运行变量", "variant": "pairs", "rows": self._runtime_detail_rows(char)},
        ]
        return {
            "name": char.name,
            "metadata": [
                {"label": "编号", "value": char.no},
                {"label": "呼名", "value": char.callname},
                {"label": "来源", "value": char.source_file},
            ],
            "posture": char.posture,
            "base": [
                self._stat_row(0, "体力", char.base.get(0, char.hp), char.maxbase.get(0, char.max_hp)),
                self._stat_row(1, "气力", char.base.get(1, char.mp), char.maxbase.get(1, char.max_mp)),
            ],
            "sections": sections,
        }

    def _stat_row(self, index: int, name: str, value: int, maximum: int) -> dict[str, object]:
        return {"id": index, "name": name, "value": value, "max": maximum, "bar": self._bar(value, max(1, maximum), 18)}

    def _value_rows(
        self,
        keys: list[int | str],
        values: dict[int | str, int],
        name_getter: Any,
        include_zero: bool = False,
    ) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for key in keys:
            value = int(values.get(key, 0) or 0)
            if not include_zero and value == 0:
                continue
            rows.append({"id": key, "name": name_getter(key), "value": value})
        return rows

    def _abl_display_order(self) -> list[int]:
        return [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 30, 31, 32, 33, 37, 39, 40, 100, 101, 102, 103]

    def _mark_display_order(self) -> list[int]:
        return [0, 1, 2, 3, 10]

    def _runtime_detail_rows(self, char: CharacterState) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for label, values in (
            ("CFLAG", char.cflag),
            ("TEQUIP", char.tequip),
            ("STAIN", char.stain),
            ("LOSEBASE", char.losebase),
            ("TFLAG", self.erb.arrays.get("TFLAG", {})),
            ("UP", self.erb.arrays.get("UP", {})),
            ("DOWN", self.erb.arrays.get("DOWN", {})),
        ):
            for key, value in sorted(values.items(), key=lambda item: str(item[0])):
                if value:
                    rows.append({"scope": label, "id": key, "name": f"{label}:{key}", "value": value})
        return rows[:48]

    def _training_commands(self) -> list[list[dict[str, object]]]:
        return [
            [self._train_cmd(0), self._train_cmd(6), self._train_cmd(30)],
            [self._train_cmd(31, "pink"), self._train_cmd(37), self._train_cmd(38)],
            [self._empty(""), self._train_cmd(54), self._train_cmd(56)],
            [self._train_cmd(110), self._empty(""), self._empty("")],
            [self._cmd("100", "能力表示", "show-characters"), self._cmd("101", "污核表示", "stub-feature", feature="污核表示"), self._cmd("103", "避孕套设定", "stub-feature", feature="避孕套设定")],
            [self._filter_cmd("104", "爱抚过滤", "caress", "blue"), self._filter_cmd("105", "器具系过滤", "tools", "blue"), self._filter_cmd("106", "私处性交过滤", "vagina", "yellow")],
            [self._filter_cmd("107", "肛门性交过滤", "anus", "pink"), self._filter_cmd("108", "SM系过滤", "sm", "red"), self._cmd("990", "调教菜单登录", "stub-feature", feature="调教菜单登录")],
            [self._cmd("999", "调教结束", "back-to-shop"), self._empty(""), self._empty("")],
        ]

    def _status_text(self) -> str:
        return f"第{self.day[0]}年　{self.day[1]}月{self.day[2]}日（第{self.day[2]}日）　{'上午' if self.time == 0 else '下午'}　（所持金：{self.money} pts.）"

    def _bar(self, value: int, max_value: int, width: int) -> str:
        filled = max(0, min(width, round(value / max_value * width)))
        return "*" * filled + "." * (width - filled)

    def _param_cell(self, name: str, value: int) -> str:
        if not name:
            return " " * 18
        return f"{name}[..........]{value:>4}".ljust(18)

    def _cmd(self, code: str, name: str, action: str, **extra: object) -> dict[str, object]:
        return {"code": code, "name": name, "action": action, "extra": extra}

    def _empty(self, code: str) -> dict[str, object]:
        return {"code": code, "name": "", "action": "", "extra": {}}

    def _train_cmd(self, command_id: int, tone: str = "") -> dict[str, object]:
        name = self.train_names.get(command_id)
        if not name:
            return self._empty("")
        return self._cmd(str(command_id), name, "train-command", command=command_id, tone=tone)

    def _filter_cmd(self, code: str, label: str, key: str, tone: str) -> dict[str, object]:
        return self._cmd(code, f"{label}{'ON' if self.filters[key] else 'OFF'}", "toggle-filter", filter=key, tone=tone)

    def _filter_label(self, key: str) -> str:
        return {
            "caress": "爱抚过滤",
            "tools": "器具系过滤",
            "vagina": "私处性交过滤",
            "anus": "肛门性交过滤",
            "sm": "SM系过滤",
        }.get(key, key)


SESSION = GameSession(ROOT)


class PrototypeHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.split("?", 1)[0] == "/api/state":
            self._send_json(SESSION.view())
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path.split("?", 1)[0] != "/api/action":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        self._send_json(SESSION.dispatch(payload))

    def translate_path(self, path: str) -> str:
        clean_path = unquote(path.split("?", 1)[0].split("#", 1)[0])

        if clean_path == "/" or clean_path == "":
            return str(PROTO_DIR / "index.html")

        if clean_path.startswith("/resources/") or clean_path.startswith("/CSV/"):
            return str(ROOT / clean_path.lstrip("/"))

        return str(PROTO_DIR / clean_path.lstrip("/"))

    def guess_type(self, path: str) -> str:
        content_type, _ = mimetypes.guess_type(path)
        return content_type or "application/octet-stream"

    def _send_json(self, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), PrototypeHandler)
    print(f"Serving eraMaouEx browser prototype at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping prototype server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
