from __future__ import annotations
"""Module for DataLoadMixin - 数据加载"""
import os
import csv
import re
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


def _get_character_class():
    """延迟导入Character类，避免循环导入"""
    from eraMaouEx import Character as _Character
    return _Character


class DataLoadMixin:
    """Mixin providing 数据加载 methods for GameEngine"""

    def _build_erb_analysis_categories(self, functions: Dict[str, Any]) -> List[str]:
        categories: Dict[str, List[str]] = {}
        for func_name in functions.keys():
            prefix = func_name.split('_')[0] if '_' in func_name else func_name
            categories.setdefault(prefix, []).append(func_name)
        report = ["Functions by category:", "-" * 40]
        for prefix, funcs in sorted(categories.items()):
            report.append(f"  {prefix}: {len(funcs)} functions")
        report.append("")
        return report




    def _build_erb_analysis_header(self, functions: Dict[str, Any]) -> List[str]:
        return [
            "=" * 60,
            "ERB Analysis Report",
            "=" * 60,
            f"Total functions loaded: {len(functions)}",
            "",
        ]




    def _build_erb_analysis_key_terms(self, functions: Dict[str, Any]) -> List[str]:
        report = ["Key game functions detected:", "-" * 40]
        for term, desc in ERB_ANALYSIS_KEY_TERMS.items():
            matches = [f for f in functions.keys() if term in f]
            if matches:
                report.append(f"  {desc}: {len(matches)} functions found")
        report.append("")
        return report




    def _build_erb_analysis_samples(self, functions: Dict[str, Any]) -> List[str]:
        report = ["Sample function names:", "-" * 40]
        for func in list(functions.keys())[:20]:
            report.append(f"  - {func}")
        return report




    def _find_csv_path(self, *parts: str) -> str:
        candidates = [
            os.path.join(self.erb_dir, *parts),
            os.path.join(os.path.dirname(self.erb_dir), *parts),
        ]
        return next((path for path in candidates if os.path.exists(path)), "")




    def _load_chara_template(self, template_id: int) -> Dict[str, Any]:
        """从ERB文件加载角色模板数据 - 对应 キャラ創立素質関数/CHARA{N}.ERB

        CHARA0-35.ERB 定义了角色创建时的额外素质(EX_TALENT)。
        格式: @CHARA_EX_{id} / EX_TALENT:{key} = {value}

        Args:
            template_id: 模板ID (0-35)

        Returns:
            包含 talent 等属性的字典
        """
        result: Dict[str, Any] = {"template_id": template_id, "ex_talent": {}}

        # 1. 尝试从ERB函数加载
        erb_func = f"CHARA_EX_{template_id}"
        if erb_func in self.interpreter.functions:
            try:
                self.interpreter.call_erb_function(erb_func)
                # 从解释器变量中提取 EX_TALENT
                v = self.interpreter.vars
                if hasattr(v, 'ex_talent'):
                    for key, val in v.ex_talent.items():
                        result["ex_talent"][int(key)] = int(val)
            except Exception:
                pass

        # 2. 尝试从ERB文件直接解析
        if not result["ex_talent"]:
            erb_path = os.path.join(
                self.erb_dir, "ERB", "キャラ創立素質関数", f"CHARA{template_id}.ERB"
            )
            if os.path.exists(erb_path):
                try:
                    with open(erb_path, encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            # 解析 EX_TALENT:KEY = VALUE
                            m = re.match(r'EX_TALENT\s*:\s*(\d+)\s*=\s*(\d+)', line)
                            if m:
                                result["ex_talent"][int(m.group(1))] = int(m.group(2))
                except Exception:
                    pass

        # 3. 内置回退数据 (基于已知的CHARA ERB文件)
        if not result["ex_talent"]:
            builtin = {
                0: {200: 1},
                31: {101: 1},
                32: {102: 1},
                33: {103: 1},
                34: {4: 1, 801: 1, 901: 1},
                35: {104: 1},
            }
            if template_id in builtin:
                result["ex_talent"] = builtin[template_id]

        return result

    # ==================================================================
    # Bridge Methods - ERB优先→模块回退
    # ==================================================================



    def _load_character_template(self, template_id: int) -> Optional[Character]:
        template = self.character_template_catalog.get("templates", {}).get(template_id)
        if template is not None:
            char = _get_character_class()()
            char.template_id = template_id
            char.name = template.name
            char.callname = template.callname
            char.nick_name = template.nick_name
            char.base = dict(template.base)
            char.maxbase = dict(template.maxbase)
            char.abl = dict(template.abl)
            char.exp = dict(template.exp)
            char.juel = dict(template.juel)
            char.talent = dict(template.talent)
            char.mark = dict(template.mark)
            char.palam = dict(template.palam)
            char.source = dict(template.source)
            char.losebase = dict(template.losebase)
            char.equipt = dict(template.equipt)
            char.stain = dict(template.stain)
            char.cflag = dict(template.cflag)
            char.cstr = dict(template.cstr)
            char.item = dict(template.item)
            return char

        csv_path = self._find_csv_path("CSV", "Chara", f"Chara{template_id}.csv")
        if not csv_path:
            return None
        return self._load_character_template_from_path(csv_path, template_id)




    def _load_character_template_from_path(self, csv_path: str, template_id: int) -> Optional[Character]:
        char = _get_character_class()()
        char.template_id = template_id
        char.cflag[190] = template_id
        with open(csv_path, "r", encoding="utf-8-sig") as csv_file:
            for row in csv.reader(csv_file):
                self._apply_character_template_csv_row(char, row)

        if not char.callname:
            char.callname = char.name
        if char.base:
            for base_id, value in list(char.base.items()):
                char.maxbase[base_id] = max(char.maxbase.get(base_id, 0), value)
        return char if char.name else None




    def _load_level_thresholds(self) -> tuple[List[int], List[int]]:
        palam_thresholds = [0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000, 500000, 1000000, 5000000, 10000000]
        exp_thresholds = [0, 1, 4, 20, 50, 200, 400, 700, 1000, 1500, 2000]
        csv_path = os.path.join(self.erb_dir, "CSV", "_replace.csv")
        if not os.path.exists(csv_path):
            return palam_thresholds, exp_thresholds

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            for row in csv.reader(csv_file):
                if not row or len(row) < 2:
                    continue
                key = row[0].strip()
                values = row[1].strip()
                if "PALAMLV" in key and values:
                    parsed = [int(value) for value in values.split("/") if value.strip()]
                    if parsed:
                        palam_thresholds = parsed
                elif "EXPLV" in key and values:
                    parsed = [int(value) for value in values.split("/") if value.strip()]
                    if parsed:
                        exp_thresholds = parsed

        return palam_thresholds, exp_thresholds




    def _load_talent_catalog(self) -> Dict[int, str]:
        catalog: Dict[int, str] = {}
        csv_path = self._find_csv_path("CSV", "Talent.csv")
        if not csv_path:
            return catalog
        with open(csv_path, "r", encoding="utf-8-sig") as csv_file:
            for row in csv.reader(csv_file):
                if not row or not row[0] or row[0].startswith(";"):
                    continue
                try:
                    talent_id = int(row[0])
                except ValueError:
                    continue
                name = row[1].strip() if len(row) > 1 else ""
                if name:
                    catalog[talent_id] = name
        return catalog




    def _load_train_commands(self) -> Dict[int, str]:
        commands: Dict[int, str] = {}
        csv_path = os.path.join(self.erb_dir, "CSV", "Train.csv")
        if not os.path.exists(csv_path):
            return commands

        with open(csv_path, "r", encoding="utf-8") as csv_file:
            for row in csv.reader(csv_file):
                if not row or not row[0] or row[0].startswith(";"):
                    continue
                try:
                    command_id = int(row[0])
                except ValueError:
                    continue
                if len(row) > 1 and row[1]:
                    commands[command_id] = row[1]
        return commands




    def analyze_erb(self):
        """Analyze and report on loaded ERB functions"""
        functions = self.interpreter.functions
        report = self._build_erb_analysis_header(functions)
        report.extend(self._build_erb_analysis_categories(functions))
        report.extend(self._build_erb_analysis_key_terms(functions))
        report.extend(self._build_erb_analysis_samples(functions))
        report.append("=" * 60)
        return "\n".join(report)




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



