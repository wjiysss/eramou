"""
eraMaouEx 核心模块
"""

from .constants import *
from .csv_data import CsvDataSystem

__all__ = [
    'ABL_C_SENS', 'ABL_B_SENS', 'ABL_V_SENS', 'ABL_A_SENS',
    'TALENT_VIRGIN', 'TALENT_MALE', 'TALENT_FUTA',
    'TALENT_KIND', 'TALENT_CONFIDENT', 'TALENT_WEAK', 'TALENT_NOBLE',
    'TALENT_SHY', 'TALENT_REBEL', 'TALENT_STRONG', 'TALENT_FRANK',
    'TALENT_LOVE', 'TALENT_CHARM', 'TALENT_ELITE',
    'PALAMLV', 'EXPLV',
    'RACE_HUMAN', 'RACE_ELF', 'RACE_FAIRY', 'RACE_GIANT',
    'CsvDataSystem',
]