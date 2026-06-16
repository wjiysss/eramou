"""
CSV数据加载系统 - 加载ERB目录下的CSV文件
对应eraMaouEx中的各种*.csv数据文件
"""
from typing import Dict, List, Tuple, Optional
import os
import csv


class CsvDataSystem:
    """CSV数据加载管理系统"""

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self._cache: Dict[str, Dict[int, str]] = {}

    def _get_csv_dir(self) -> str:
        """获取CSV目录"""
        if hasattr(self.game_engine, 'paths') and self.game_engine.paths:
            return self.game_engine.paths.csv_dir
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'CSV')

    def load_csv(self, filename: str) -> Dict[int, str]:
        """加载CSV文件，返回ID→名称映射"""
        if filename in self._cache:
            return self._cache[filename]

        result: Dict[int, str] = {}
        filepath = os.path.join(self._get_csv_dir(), filename)

        if not os.path.exists(filepath):
            self._cache[filename] = result
            return result

        try:
            with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or len(row) < 2:
                        continue
                    line = row[0].strip()
                    if line.startswith(';') or line.startswith('#'):
                        continue
                    try:
                        item_id = int(line)
                        item_name = row[1].strip()
                        if item_name and not item_name.startswith(';'):
                            result[item_id] = item_name
                    except (ValueError, IndexError):
                        continue
        except Exception:
            pass

        self._cache[filename] = result
        return result

    def get_talent_name(self, talent_id: int) -> str:
        """获取素质名称"""
        data = self.load_csv('Talent.csv')
        return data.get(talent_id, f"素质{talent_id}")

    def get_abl_name(self, abl_id: int) -> str:
        """获取能力名称"""
        data = self.load_csv('Abl.csv')
        return data.get(abl_id, f"能力{abl_id}")

    def get_exp_name(self, exp_id: int) -> str:
        """获取经验名称"""
        data = self.load_csv('Exp.csv')
        return data.get(exp_id, f"经验{exp_id}")

    def get_mark_name(self, mark_id: int) -> str:
        """获取刻印名称"""
        data = self.load_csv('Mark.csv')
        return data.get(mark_id, f"刻印{mark_id}")

    def get_palam_name(self, palam_id: int) -> str:
        """获取参数名称"""
        data = self.load_csv('Palam.csv')
        return data.get(palam_id, f"参数{palam_id}")

    def get_source_name(self, source_id: int) -> str:
        """获取SOURCE名称"""
        data = self.load_csv('Source.csv')
        return data.get(source_id, f"来源{source_id}")

    def get_item_name(self, item_id: int) -> str:
        """获取道具名称"""
        data = self.load_csv('Item.csv')
        return data.get(item_id, f"物品{item_id}")

    def get_monster_name(self, monster_id: int) -> str:
        """获取魔物名称"""
        data = self.load_csv('Monster.csv')
        if data:
            return data.get(monster_id, f"魔物{monster_id}")
        data = self.load_csv('EQUIP_MONSTER.csv')
        return data.get(monster_id, f"魔物{monster_id}")

    def get_train_name(self, train_id: int) -> str:
        """获取调教指令名称"""
        data = self.load_csv('Train.csv')
        return data.get(train_id, f"指令{train_id}")

    def get_equip_name(self, equip_id: int) -> str:
        """获取装备名称"""
        data = self.load_csv('Equip.csv')
        return data.get(equip_id, f"装备{equip_id}")

    def get_juel_name(self, juel_id: int) -> str:
        """获取宝珠名称"""
        data = self.load_csv('Juel.csv')
        return data.get(juel_id, f"宝珠{juel_id}")

    def get_chara_template(self, template_id: int) -> Optional[Dict]:
        """获取角色模板"""
        filepath = os.path.join(self._get_csv_dir(), 'CHARA', f'{template_id}.csv')
        if not os.path.exists(filepath):
            return None

        template: Dict[str, any] = {'id': template_id}
        try:
            with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(';') or line.startswith('#'):
                        continue
                    parts = line.split(',')
                    if len(parts) >= 3:
                        category = parts[0].strip()
                        try:
                            item_id = int(parts[1])
                            value = parts[2].strip()
                            if category not in template:
                                template[category] = {}
                            try:
                                template[category][item_id] = int(value)
                            except ValueError:
                                template[category][item_id] = value
                        except (ValueError, IndexError):
                            continue
        except Exception:
            pass

        return template if len(template) > 1 else None

    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()

    def get_all_names(self, category: str) -> Dict[int, str]:
        """获取指定类别的所有名称"""
        csv_map = {
            'talent': 'Talent.csv',
            'abl': 'Abl.csv',
            'exp': 'Exp.csv',
            'mark': 'Mark.csv',
            'palam': 'Palam.csv',
            'source': 'Source.csv',
            'item': 'Item.csv',
            'monster': 'Monster.csv',
            'train': 'Train.csv',
            'equip': 'Equip.csv',
            'juel': 'Juel.csv',
        }
        filename = csv_map.get(category.lower())
        if filename:
            return self.load_csv(filename)
        return {}
