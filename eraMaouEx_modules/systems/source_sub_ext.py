from __future__ import annotations
"""Module for SourceSubExtMixin - SOURCE辅助计算

对应 ERB 文件: SYSTEM_SOURCE_SUB1.ERB, SYSTEM_SOURCE_SUB2.ERB
包含 SOURCE_CHECK 流程中调用的所有辅助函数的 Python 实现。
"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class SourceSubExtMixin:
    """Mixin providing SOURCE辅助计算 methods for GameEngine"""

    # =================================================================
    # SOURCE_SEX_CHECK 相关 (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _source_lesbian_sex_check(self, target: Character) -> None:
        """女性同士の場合のチェック - SOURCE_LESBIAN_SEX_CHECK"""
        v = self.interpreter.vars
        source = target.source
        abl22 = int(target.abl.get(22, 0))  # 百合气质
        abl33 = int(target.abl.get(33, 0))  # 百合中毒

        # ABL:百合气质
        if abl22 == 0:
            source[8] = int(source.get(8, 0) * 0.80)
            source[14] = int(source.get(14, 0) * 0.80)
            source[13] = int(source.get(13, 0) * 0.90)
        elif abl22 == 1:
            source[7] = source.get(7, 0) + 100
            source[8] = int(source.get(8, 0) * 0.60)
            source[14] = int(source.get(14, 0) * 0.60)
            source[13] = int(source.get(13, 0) * 0.75)
            source[0] = int(source.get(0, 0) * 1.10)
            source[1] = int(source.get(1, 0) * 1.10)
            source[2] = int(source.get(2, 0) * 1.10)
            source[5] = int(source.get(5, 0) * 1.10)
            source[17] = int(source.get(17, 0) * 1.10)
        elif abl22 == 2:
            source[7] = source.get(7, 0) + 200
            source[8] = int(source.get(8, 0) * 0.40)
            source[14] = int(source.get(14, 0) * 0.40)
            source[13] = int(source.get(13, 0) * 0.60)
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
        elif abl22 == 3:
            source[7] = source.get(7, 0) + 350
            source[8] = int(source.get(8, 0) * 0.25)
            source[14] = int(source.get(14, 0) * 0.25)
            source[13] = int(source.get(13, 0) * 0.45)
            source[0] = int(source.get(0, 0) * 1.30)
            source[1] = int(source.get(1, 0) * 1.30)
            source[2] = int(source.get(2, 0) * 1.30)
            source[5] = int(source.get(5, 0) * 1.30)
            source[17] = int(source.get(17, 0) * 1.30)
        elif abl22 == 4:
            source[7] = source.get(7, 0) + 500
            source[8] = int(source.get(8, 0) * 0.15)
            source[14] = int(source.get(14, 0) * 0.15)
            source[13] = int(source.get(13, 0) * 0.30)
            source[0] = int(source.get(0, 0) * 1.40)
            source[1] = int(source.get(1, 0) * 1.40)
            source[2] = int(source.get(2, 0) * 1.40)
            source[5] = int(source.get(5, 0) * 1.40)
            source[17] = int(source.get(17, 0) * 1.40)
        else:
            source[7] = source.get(7, 0) + 750
            source[8] = int(source.get(8, 0) * 0.10)
            source[14] = int(source.get(14, 0) * 0.10)
            source[13] = int(source.get(13, 0) * 0.15)
            source[0] = int(source.get(0, 0) * 1.60)
            source[1] = int(source.get(1, 0) * 1.60)
            source[2] = int(source.get(2, 0) * 1.60)
            source[5] = int(source.get(5, 0) * 1.60)
            source[17] = int(source.get(17, 0) * 1.60)

        # ABL:百合中毒
        if abl33 == 0:
            source[8] = int(source.get(8, 0) * 0.80)
            source[14] = int(source.get(14, 0) * 0.80)
        elif abl33 == 1:
            source[8] = int(source.get(8, 0) * 0.60)
            source[14] = int(source.get(14, 0) * 0.60)
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
        elif abl33 == 2:
            source[8] = int(source.get(8, 0) * 0.40)
            source[14] = int(source.get(14, 0) * 0.40)
            source[0] = int(source.get(0, 0) * 1.40)
            source[1] = int(source.get(1, 0) * 1.40)
            source[2] = int(source.get(2, 0) * 1.40)
            source[5] = int(source.get(5, 0) * 1.40)
            source[17] = int(source.get(17, 0) * 1.40)
        elif abl33 == 3:
            source[8] = int(source.get(8, 0) * 0.30)
            source[14] = int(source.get(14, 0) * 0.30)
            source[0] = int(source.get(0, 0) * 1.60)
            source[1] = int(source.get(1, 0) * 1.60)
            source[2] = int(source.get(2, 0) * 1.60)
            source[5] = int(source.get(5, 0) * 1.60)
            source[17] = int(source.get(17, 0) * 1.60)
        elif abl33 == 4:
            source[8] = int(source.get(8, 0) * 0.20)
            source[14] = int(source.get(14, 0) * 0.20)
            source[0] = int(source.get(0, 0) * 1.80)
            source[1] = int(source.get(1, 0) * 1.80)
            source[2] = int(source.get(2, 0) * 1.80)
            source[5] = int(source.get(5, 0) * 1.80)
            source[17] = int(source.get(17, 0) * 1.80)
        else:
            source[8] = int(source.get(8, 0) * 0.10)
            source[14] = int(source.get(14, 0) * 0.10)
            source[0] = int(source.get(0, 0) * 2.00)
            source[1] = int(source.get(1, 0) * 2.00)
            source[2] = int(source.get(2, 0) * 2.00)
            source[5] = int(source.get(5, 0) * 2.00)
            source[17] = int(source.get(17, 0) * 2.00)

        # 调教者的ABL:百合气质
        player = self._get_player()
        if player is not None:
            p_abl22 = int(player.abl.get(22, 0))
            if p_abl22 == 0:
                source[0] = int(source.get(0, 0) * 0.40)
                source[1] = int(source.get(1, 0) * 0.40)
                source[2] = int(source.get(2, 0) * 0.40)
                source[3] = int(source.get(3, 0) * 0.20)
                source[4] = int(source.get(4, 0) * 0.30)
                source[5] = int(source.get(5, 0) * 0.30)
                source[17] = int(source.get(17, 0) * 0.40)
            elif p_abl22 == 1:
                source[0] = int(source.get(0, 0) * 0.70)
                source[1] = int(source.get(1, 0) * 0.70)
                source[2] = int(source.get(2, 0) * 0.70)
                source[3] = int(source.get(3, 0) * 0.60)
                source[4] = int(source.get(4, 0) * 0.70)
                source[5] = int(source.get(5, 0) * 0.70)
                source[17] = int(source.get(17, 0) * 0.70)
            elif p_abl22 == 2:
                pass  # 1.00
            elif p_abl22 == 3:
                source[0] = int(source.get(0, 0) * 1.10)
                source[1] = int(source.get(1, 0) * 1.10)
                source[2] = int(source.get(2, 0) * 1.10)
                source[3] = int(source.get(3, 0) * 1.40)
                source[4] = int(source.get(4, 0) * 1.30)
                source[5] = int(source.get(5, 0) * 1.30)
                source[17] = int(source.get(17, 0) * 1.10)
            elif p_abl22 == 4:
                source[0] = int(source.get(0, 0) * 1.20)
                source[1] = int(source.get(1, 0) * 1.20)
                source[2] = int(source.get(2, 0) * 1.20)
                source[3] = int(source.get(3, 0) * 1.80)
                source[4] = int(source.get(4, 0) * 1.60)
                source[5] = int(source.get(5, 0) * 1.60)
                source[17] = int(source.get(17, 0) * 1.20)
            else:
                source[0] = int(source.get(0, 0) * 1.30)
                source[1] = int(source.get(1, 0) * 1.30)
                source[2] = int(source.get(2, 0) * 1.30)
                source[3] = int(source.get(3, 0) * 2.50)
                source[4] = int(source.get(4, 0) * 2.00)
                source[5] = int(source.get(5, 0) * 2.00)
                source[17] = int(source.get(17, 0) * 1.30)

            # 调教者的ABL:百合中毒
            p_abl33 = int(player.abl.get(33, 0))
            if p_abl33 == 1:
                source[0] = int(source.get(0, 0) * 1.10)
                source[1] = int(source.get(1, 0) * 1.10)
                source[2] = int(source.get(2, 0) * 1.10)
                source[3] = int(source.get(3, 0) * 1.50)
                source[4] = int(source.get(4, 0) * 1.50)
                source[5] = int(source.get(5, 0) * 1.50)
                source[17] = int(source.get(17, 0) * 1.10)
            elif p_abl33 == 2:
                source[0] = int(source.get(0, 0) * 1.20)
                source[1] = int(source.get(1, 0) * 1.20)
                source[2] = int(source.get(2, 0) * 1.20)
                source[3] = int(source.get(3, 0) * 2.00)
                source[4] = int(source.get(4, 0) * 2.00)
                source[5] = int(source.get(5, 0) * 2.00)
                source[17] = int(source.get(17, 0) * 1.20)
            elif p_abl33 == 3:
                source[0] = int(source.get(0, 0) * 1.40)
                source[1] = int(source.get(1, 0) * 1.40)
                source[2] = int(source.get(2, 0) * 1.40)
                source[3] = int(source.get(3, 0) * 2.50)
                source[4] = int(source.get(4, 0) * 2.50)
                source[5] = int(source.get(5, 0) * 2.50)
                source[17] = int(source.get(17, 0) * 1.40)
            elif p_abl33 == 4:
                source[0] = int(source.get(0, 0) * 1.60)
                source[1] = int(source.get(1, 0) * 1.60)
                source[2] = int(source.get(2, 0) * 1.60)
                source[3] = int(source.get(3, 0) * 3.50)
                source[4] = int(source.get(4, 0) * 3.00)
                source[5] = int(source.get(5, 0) * 3.00)
                source[17] = int(source.get(17, 0) * 1.60)
            elif p_abl33 >= 5:
                source[0] = int(source.get(0, 0) * 1.80)
                source[1] = int(source.get(1, 0) * 1.80)
                source[2] = int(source.get(2, 0) * 1.80)
                source[3] = int(source.get(3, 0) * 5.00)
                source[4] = int(source.get(4, 0) * 4.00)
                source[5] = int(source.get(5, 0) * 4.00)
                source[17] = int(source.get(17, 0) * 1.80)

            # 调教者的克制
            if int(player.talent.get(20, 0)):
                source[4] = int(source.get(4, 0) * 0.50)
                source[5] = int(source.get(5, 0) * 0.50)

    def _source_gay_sex_check(self, target: Character) -> None:
        """男性同士の場合のチェック - SOURCE_GAY_SEX_CHECK"""
        source = target.source
        abl23 = int(target.abl.get(23, 0))  # ホモっ気

        if abl23 == 0:
            source[8] = int(source.get(8, 0) * 4.00)
            source[14] = int(source.get(14, 0) * 4.00)
            source[5] = int(source.get(5, 0) * 0.50)
        elif abl23 == 1:
            source[7] = source.get(7, 0) + 10
            source[8] = int(source.get(8, 0) * 2.00)
            source[14] = int(source.get(14, 0) * 2.00)
            source[5] = int(source.get(5, 0) * 0.70)
            source[0] = int(source.get(0, 0) * 1.10)
            source[1] = int(source.get(1, 0) * 1.10)
            source[2] = int(source.get(2, 0) * 1.10)
            source[17] = int(source.get(17, 0) * 1.10)
        elif abl23 == 2:
            source[7] = source.get(7, 0) + 40
            source[8] = int(source.get(8, 0) * 1.40)
            source[14] = int(source.get(14, 0) * 1.40)
            source[5] = int(source.get(5, 0) * 0.90)
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
        elif abl23 == 3:
            source[7] = source.get(7, 0) + 100
            source[8] = int(source.get(8, 0) * 1.00)
            source[14] = int(source.get(14, 0) * 1.00)
            source[5] = int(source.get(5, 0) * 1.10)
            source[0] = int(source.get(0, 0) * 1.30)
            source[1] = int(source.get(1, 0) * 1.30)
            source[2] = int(source.get(2, 0) * 1.30)
            source[17] = int(source.get(17, 0) * 1.30)
        elif abl23 == 4:
            source[7] = source.get(7, 0) + 200
            source[8] = int(source.get(8, 0) * 0.70)
            source[14] = int(source.get(14, 0) * 0.70)
            source[5] = int(source.get(5, 0) * 1.20)
            source[0] = int(source.get(0, 0) * 1.40)
            source[1] = int(source.get(1, 0) * 1.40)
            source[2] = int(source.get(2, 0) * 1.40)
            source[17] = int(source.get(17, 0) * 1.40)
        elif abl23 == 5:
            source[7] = source.get(7, 0) + 350
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[5] = int(source.get(5, 0) * 1.30)
            source[0] = int(source.get(0, 0) * 1.50)
            source[1] = int(source.get(1, 0) * 1.50)
            source[2] = int(source.get(2, 0) * 1.50)
            source[17] = int(source.get(17, 0) * 1.50)

        # 调教者的克制
        player = self._get_player()
        if player is not None and int(player.talent.get(20, 0)):
            source[4] = int(source.get(4, 0) * 0.50)
            source[5] = int(source.get(5, 0) * 0.50)

    # =================================================================
    # PLAYER_SKILL_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _player_skill_check_full(self, target: Character) -> None:
        """调教者的スキルによるチェック - PLAYER_SKILL_CHECK (完整版)"""
        source = target.source
        player = self._get_player()
        if player is None:
            return

        # 调教者的TALENT:开放
        if int(player.talent.get(33, 0)):
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[3] = int(source.get(3, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)

        # 调教者的TALENT:小恶魔
        if int(player.talent.get(87, 0)):
            source[12] = int(source.get(12, 0) * 1.60)

        # 调教者的TALENT:魅惑
        if int(player.talent.get(91, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)

        # 调教者的TALENT:谜之魅力
        if int(player.talent.get(92, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)

        # 调教者が【母性】か【人妻】で調教対象が【恋母情结】
        if (int(player.talent.get(155, 0)) or int(player.talent.get(157, 0))) and int(target.talent.get(140, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[3] = int(source.get(3, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)

        # 调教者が【父性】で調教対象が【恋父情结】
        if int(player.talent.get(156, 0)) and int(target.talent.get(141, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[3] = int(source.get(3, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)

        # 调教者が【男人】ではなく【未熟】か【娇小】で調教対象が【萝莉控】
        if int(player.talent.get(122, 0)) == 0 and (int(player.talent.get(100, 0)) or int(player.talent.get(135, 0))) and int(target.talent.get(142, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[3] = int(source.get(3, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)

        # 调教者が【男人】であり【未熟】か【娇小】で調教対象が【正太控】
        if int(player.talent.get(122, 0)) and (int(player.talent.get(100, 0)) or int(player.talent.get(135, 0))) and int(target.talent.get(143, 0)):
            source[8] = int(source.get(8, 0) * 0.50)
            source[14] = int(source.get(14, 0) * 0.50)
            source[3] = int(source.get(3, 0) * 1.20)
            source[5] = int(source.get(5, 0) * 1.20)

        # 调教者が【萝莉控】で調教対象が【未熟】か【娇小】かつ【男人】ではない
        if int(player.talent.get(142, 0)) and (int(target.talent.get(100, 0)) or int(target.talent.get(135, 0))) and int(target.talent.get(122, 0)) == 0:
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
            source[14] = int(source.get(14, 0) * 0.80)

        # 调教者が【正太控】で調教対象が【未熟】か【娇小】かつ【男人】である
        if int(player.talent.get(143, 0)) and (int(target.talent.get(100, 0)) or int(target.talent.get(135, 0))) and int(target.talent.get(122, 0)):
            source[0] = int(source.get(0, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
            source[14] = int(source.get(14, 0) * 0.80)

        # 调教者的ABL:技巧
        abl12 = int(player.abl.get(12, 0))
        if abl12 == 0:
            source[0] = int(source.get(0, 0) * 0.50)
            source[1] = int(source.get(1, 0) * 0.50)
            source[2] = int(source.get(2, 0) * 0.50)
            source[17] = int(source.get(17, 0) * 0.50)
        elif abl12 == 1:
            source[0] = int(source.get(0, 0) * 0.80)
            source[1] = int(source.get(1, 0) * 0.80)
            source[2] = int(source.get(2, 0) * 0.80)
            source[17] = int(source.get(17, 0) * 0.80)
        elif abl12 == 2:
            pass  # 1.00
        elif abl12 == 3:
            source[0] = int(source.get(0, 0) * 1.20)
            source[1] = int(source.get(1, 0) * 1.20)
            source[2] = int(source.get(2, 0) * 1.20)
            source[17] = int(source.get(17, 0) * 1.20)
        elif abl12 == 4:
            source[0] = int(source.get(0, 0) * 1.50)
            source[1] = int(source.get(1, 0) * 1.50)
            source[2] = int(source.get(2, 0) * 1.50)
            source[17] = int(source.get(17, 0) * 1.50)
        elif abl12 >= 5:
            source[0] = int(source.get(0, 0) * 2.00)
            source[1] = int(source.get(1, 0) * 2.00)
            source[2] = int(source.get(2, 0) * 2.00)
            source[17] = int(source.get(17, 0) * 2.00)

    # =================================================================
    # MASTER_SKILL_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _master_skill_check_full(self, target: Character) -> None:
        """主人による調教のボーナス - MASTER_SKILL_CHECK (完整版)"""
        v = self.interpreter.vars
        source = target.source
        assiplay = self.state.assiplay

        if assiplay == 0:
            cflag2 = int(target.cflag.get(2, 0))
            if cflag2 >= 500:
                source[8] = int(source.get(8, 0) * 0.70)
                source[14] = int(source.get(14, 0) * 0.70)
                source[0] = int(source.get(0, 0) * 1.20)
                source[1] = int(source.get(1, 0) * 1.20)
                source[2] = int(source.get(2, 0) * 1.20)
                source[3] = int(source.get(3, 0) * 1.30)
                source[17] = int(source.get(17, 0) * 1.20)
            elif cflag2 >= 300:
                source[8] = int(source.get(8, 0) * 0.80)
                source[14] = int(source.get(14, 0) * 0.80)
                source[0] = int(source.get(0, 0) * 1.10)
                source[1] = int(source.get(1, 0) * 1.10)
                source[2] = int(source.get(2, 0) * 1.10)
                source[3] = int(source.get(3, 0) * 1.20)
                source[17] = int(source.get(17, 0) * 1.10)
            elif cflag2 >= 100:
                source[8] = int(source.get(8, 0) * 0.90)
                source[14] = int(source.get(14, 0) * 0.90)
                source[3] = int(source.get(3, 0) * 1.10)

        # 淫乱
        if int(target.talent.get(76, 0)) and assiplay == 0:
            source[0] = int(source.get(0, 0) * 1.80)
            source[1] = int(source.get(1, 0) * 1.80)
            source[2] = int(source.get(2, 0) * 1.80)
            source[17] = int(source.get(17, 0) * 1.80)

        # 爱慕
        if int(target.talent.get(85, 0)) and assiplay == 0:
            source[0] = int(source.get(0, 0) * 1.30)
            source[1] = int(source.get(1, 0) * 1.30)
            source[2] = int(source.get(2, 0) * 1.30)
            source[3] = int(source.get(3, 0) * 1.80)
            source[17] = int(source.get(17, 0) * 1.30)

    # =================================================================
    # INCEST_SEX_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _incest_sex_check_full(self, target: Character) -> None:
        """近親相姦のチェック - INCEST_SEX_CHECK (完整版)"""
        v = self.interpreter.vars
        source = target.source
        player = self._get_player()

        v.tflag[14] = 0
        self._incest(target)

        if v.tflag.get(14, 0) and v.tflag.get(19, 0):
            incest_type = v.tflag.get(14, 0)
            if incest_type == 1 or incest_type == 2:
                source[3] = int(source.get(3, 0) * 2.00)
                source[14] = int(source.get(14, 0) * 2.00)
                source[16] = int(source.get(16, 0) * 2.00)
            elif incest_type == 3 or incest_type == 4:
                source[3] = int(source.get(3, 0) * 1.50)
                source[14] = int(source.get(14, 0) * 1.50)
                source[16] = int(source.get(16, 0) * 1.50)

    def _incest(self, target: Character) -> None:
        """親族関係の判定 - INCEST"""
        v = self.interpreter.vars
        player = self._get_player()
        if player is None:
            return

        v.tflag[14] = 0
        player_no = int(player.cflag.get(0, 0))  # NO:PLAYER

        # CFLAG:21-25 から親族判定
        for cflag_idx in [21, 22, 23, 24, 25]:
            cflag_val = int(target.cflag.get(cflag_idx, 0))
            if cflag_val and cflag_val % 100 == player_no:
                v.tflag[14] = (cflag_val // 100) + 1

        # 主人が父親か母親である場合の処理
        master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
        if master is not None and player is master:
            for cflag_idx in [21, 22, 23, 24, 25]:
                if int(target.cflag.get(cflag_idx, 0)) == -1:
                    v.tflag[14] = 1
                    break

    # =================================================================
    # UP_TALENT_CVA_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _up_talent_cva_check(self, target: Character, up: Dict[int, int]) -> Dict[int, int]:
        """素質などによる上下の処理（快楽系）- UP_TALENT_CVA_CHECK"""
        v = self.interpreter.vars

        # 媚药
        if int(target.equipt.get(21, 0)):
            up[0] = int(up.get(0, 0) * 2.00)
            up[1] = int(up.get(1, 0) * 2.00)
            up[2] = int(up.get(2, 0) * 2.00)
            up[14] = int(up.get(14, 0) * 2.00)

        # 利尿剂
        if int(target.equipt.get(22, 0)):
            up[0] = int(up.get(0, 0) * 0.70)
            up[1] = int(up.get(1, 0) * 0.70)
            up[2] = int(up.get(2, 0) * 0.70)
            up[14] = int(up.get(14, 0) * 0.70)

        # 失神中
        if int(v.tflag.get(899, 0)) > 0:
            up[0] = int(up.get(0, 0) * 0.20)
            up[1] = int(up.get(1, 0) * 0.20)
            up[2] = int(up.get(2, 0) * 0.20)
            up[14] = int(up.get(14, 0) * 0.20)

        # 克制
        if int(target.talent.get(20, 0)):
            up[0] = int(up.get(0, 0) * 0.30)
            up[1] = int(up.get(1, 0) * 0.50)
            up[2] = int(up.get(2, 0) * 0.70)
            up[14] = int(up.get(14, 0) * 0.30)

        # 男人
        if int(target.talent.get(122, 0)):
            up[2] = int(up.get(2, 0) * 1.30)

        # 性豪
        if int(target.talent.get(272, 0)):
            up[0] = int(up.get(0, 0) * 1.20)
            up[1] = int(up.get(1, 0) * 1.20)
            up[2] = int(up.get(2, 0) * 1.20)
            up[14] = int(up.get(14, 0) * 1.20)

        return up

    # =================================================================
    # UP_TALENT_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _up_talent_check(self, target: Character, up: Dict[int, int]) -> Dict[int, int]:
        """素質などによる上下の処理 - UP_TALENT_CHECK"""
        v = self.interpreter.vars
        player = self._get_player()

        # 媚药
        if int(target.equipt.get(21, 0)):
            up[4] = int(up.get(4, 0) * 1.20)
            up[5] = int(up.get(5, 0) * 2.00)
            up[6] = int(up.get(6, 0) * 1.20)
            up[11] = int(up.get(11, 0) * 0.75)
            up[12] = int(up.get(12, 0) * 0.50)

        # 利尿剂
        if int(target.equipt.get(22, 0)):
            up[4] = int(up.get(4, 0) * 0.80)
            up[5] = int(up.get(5, 0) * 1.50)
            up[6] = int(up.get(6, 0) * 0.80)
            up[11] = int(up.get(11, 0) * 0.50)
            up[12] = int(up.get(12, 0) * 1.20)
            up[13] = int(up.get(13, 0) * 1.50)
            up[15] = int(up.get(15, 0) * 1.20)

        # 失神中
        if int(v.tflag.get(899, 0)) > 0:
            up[4] = int(up.get(4, 0) * 0.50)
            up[5] = int(up.get(5, 0) * 0.75)
            up[6] = int(up.get(6, 0) * 0.10)
            up[8] = int(up.get(8, 0) * 0.10)
            up[10] = int(up.get(10, 0) * 0.00)
            up[11] = int(up.get(11, 0) * 0.00)
            up[12] = int(up.get(12, 0) * 0.10)
            up[13] = int(up.get(13, 0) * 0.00)

        # 胆怯
        if int(target.talent.get(10, 0)):
            up[10] = int(up.get(10, 0) * 2.00)
            up[11] = int(up.get(11, 0) * 0.50)
            up[13] = int(up.get(13, 0) * 0.25)

        # 反抗心
        if int(target.talent.get(11, 0)):
            up[4] = int(up.get(4, 0) * 0.25)
            up[5] = int(up.get(5, 0) * 0.50)
            up[11] = int(up.get(11, 0) * 1.50)

        # 刚强
        if int(target.talent.get(12, 0)):
            up[4] = int(up.get(4, 0) * 0.30)
            up[5] = int(up.get(5, 0) * 0.75)
            up[10] = int(up.get(10, 0) * 0.80)
            up[11] = int(up.get(11, 0) * 2.00)
            up[13] = int(up.get(13, 0) * 2.00)

        # 坦率
        if int(target.talent.get(13, 0)):
            up[4] = int(up.get(4, 0) * 2.00)
            up[11] = int(up.get(11, 0) * 0.60)

        # 文静
        if int(target.talent.get(14, 0)):
            up[11] = int(up.get(11, 0) * 0.30)

        # 高姿态
        if int(target.talent.get(15, 0)):
            up[6] = int(up.get(6, 0) * 0.50)
            up[10] = int(up.get(10, 0) * 0.60)
            up[11] = int(up.get(11, 0) * 1.20)

        # 低姿态
        if int(target.talent.get(17, 0)):
            up[6] = int(up.get(6, 0) * 2.00)
            up[10] = int(up.get(10, 0) * 1.50)
            up[11] = int(up.get(11, 0) * 0.80)

        # 冷漠
        if int(target.talent.get(21, 0)):
            up[4] = int(up.get(4, 0) * 0.50)
            up[5] = int(up.get(5, 0) * 0.50)
            up[6] = int(up.get(6, 0) * 0.50)
            up[10] = int(up.get(10, 0) * 0.80)
            up[11] = int(up.get(11, 0) * 0.80)

        # 感情淡薄
        if int(target.talent.get(22, 0)):
            up[4] = int(up.get(4, 0) * 0.60)
            up[5] = int(up.get(5, 0) * 0.60)
            up[6] = int(up.get(6, 0) * 0.60)
            up[8] = int(up.get(8, 0) * 0.60)
            up[10] = int(up.get(10, 0) * 0.60)
            up[11] = int(up.get(11, 0) * 0.60)
            up[12] = int(up.get(12, 0) * 0.60)
            up[13] = int(up.get(13, 0) * 0.60)

        # 好奇心
        if int(target.talent.get(23, 0)):
            up[7] = int(up.get(7, 0) * 1.20)

        # 保守的
        if int(target.talent.get(24, 0)):
            up[7] = int(up.get(7, 0) * 0.80)

        # 乐观的
        if int(target.talent.get(25, 0)):
            up[13] = int(up.get(13, 0) * 0.30)

        # 悲观的
        if int(target.talent.get(26, 0)):
            up[13] = int(up.get(13, 0) * 2.50)

        # 压抑
        if int(target.talent.get(32, 0)):
            up[5] = int(up.get(5, 0) * 0.50)
            up[11] = int(up.get(11, 0) * 2.00)
            up[13] = int(up.get(13, 0) * 1.50)

        # 开放
        if int(target.talent.get(33, 0)):
            up[5] = int(up.get(5, 0) * 2.00)
            up[6] = int(up.get(6, 0) * 2.00)

        # 抵抗
        if int(target.talent.get(34, 0)):
            up[5] = int(up.get(5, 0) * 0.50)
            up[11] = int(up.get(11, 0) * 2.00)

        # 害怕疼痛
        if int(target.talent.get(40, 0)):
            up[10] = int(up.get(10, 0) * 2.00)
            up[11] = int(up.get(11, 0) * 1.50)

        # 不惧疼痛
        if int(target.talent.get(41, 0)):
            up[10] = int(up.get(10, 0) * 0.50)
            up[11] = int(up.get(11, 0) * 0.75)

        # 快速学习
        if int(target.talent.get(50, 0)):
            up[7] = int(up.get(7, 0) * 2.00)

        # 学习缓慢
        if int(target.talent.get(51, 0)):
            up[7] = int(up.get(7, 0) * 0.50)

        # 献身的
        if int(target.talent.get(63, 0)):
            up[6] = int(up.get(6, 0) * 2.00)

        # 接受快感
        if int(target.talent.get(70, 0)):
            up[5] = int(up.get(5, 0) * 2.00)

        # 否定快感
        if int(target.talent.get(71, 0)):
            up[5] = int(up.get(5, 0) * 0.50)

        # 爱慕
        if int(target.talent.get(85, 0)) and self.state.assiplay == 0:
            up[4] = int(up.get(4, 0) * 1.20)
            up[6] = int(up.get(6, 0) * 2.00)
            up[11] = int(up.get(11, 0) * 0.50)
            up[12] = int(up.get(12, 0) * 0.50)

        # 盲从
        if int(target.talent.get(86, 0)):
            up[6] = int(up.get(6, 0) * 4.00)
            up[11] = int(up.get(11, 0) * 0.50)

        # 调教者がTALENT:威圧感
        if player is not None and int(player.talent.get(93, 0)):
            up[10] = int(up.get(10, 0) * 2.00)
            up[11] = int(up.get(11, 0) * 0.50)

        # 性豪
        if int(target.talent.get(272, 0)):
            up[5] = int(up.get(5, 0) * 1.20)

        # 时常发情
        if int(target.talent.get(271, 0)):
            up[5] = int(up.get(5, 0) * 1.20)
            up[3] = int(up.get(3, 0) * 1.20)

        # 膣内射精による妊娠への恐怖
        if v.tflag.get(2, 0):
            com_id = self.state.prevcom
            if com_id in [20, 21, 22, 23, 34]:
                if self.state.assiplay == 0 and int(target.equipt.get(35, 0)) == 0 and v.tflag.get(2, 0) and int(target.talent.get(85, 0)) == 0:
                    up[10] = int(up.get(10, 0) * 2.00)
                elif int(v.assi) > 0 and self.state.assiplay and int(target.equipt.get(36, 0)) == 0:
                    assi_char = self.interpreter.vars.chars[int(v.assi)] if int(v.assi) < len(self.interpreter.vars.chars) else None
                    if assi_char is not None:
                        r = int(assi_char.cflag.get(0, 0))
                        rel = int(target.relation.get(r, 0)) if hasattr(target, 'relation') else 0
                        if rel < 200:
                            up[10] = int(up.get(10, 0) * 2.00)

        # 反抗刻印
        mark3 = int(target.mark.get(3, 0))
        if mark3 == 3:
            up[4] = int(up.get(4, 0) * 0.10)
        elif mark3 == 2:
            up[4] = int(up.get(4, 0) * 0.40)
        elif mark3 == 1:
            up[4] = int(up.get(4, 0) * 0.70)

        return up

    # =================================================================
    # MARK_GOT_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _mark_got_check(self, target: Character, up: Dict[int, int]) -> None:
        """刻印取得のチェック - MARK_GOT_CHECK"""
        v = self.interpreter.vars

        # 反抗刻印
        local = up.get(11, 0) + up.get(12, 0)
        if local >= 500 and local < 1200 and int(target.mark.get(4, 0)) <= 0 and v.tflag.get(150, 0) == 0:
            target.mark[3] = 1
            target.mark[4] = 1
            v.tflag[21] = 1
        elif local >= 1200 and local < 3000 and int(target.mark.get(4, 0)) <= 1 and v.tflag.get(150, 0) == 0:
            target.mark[3] = 2
            target.mark[4] = 2
            v.tflag[21] = 2
            if int(target.abl.get(10, 0)) == 1 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 0
            elif int(target.abl.get(10, 0)) == 2 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 1
        elif local >= 3000 and int(target.mark.get(4, 0)) <= 2 and v.tflag.get(150, 0) == 0:
            target.mark[3] = 3
            target.mark[4] = 3
            v.tflag[21] = 3
            if 0 < int(target.abl.get(10, 0)) <= 2 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 0
            elif int(target.abl.get(10, 0)) == 3 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 2
        v.tflag[150] = 0

        # 苦痛刻印
        up9 = up.get(9, 0)
        if up9 >= 500 and up9 < 1500 and int(target.mark.get(0, 0)) <= 0:
            target.mark[0] = 1
            v.tflag[22] = 1
        elif up9 >= 1500 and up9 < 3000 and int(target.mark.get(0, 0)) <= 1:
            target.mark[0] = 2
            v.tflag[22] = 2
            if int(target.abl.get(10, 0)) == 0 and int(target.talent.get(12, 0)) == 0 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 1
                self._jujun_up_check(target)
        elif up9 >= 3000 and int(target.mark.get(0, 0)) <= 2:
            target.mark[0] = 3
            v.tflag[22] = 3
            if int(target.abl.get(10, 0)) == 0 and int(target.talent.get(12, 0)) == 0 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 1
                self._jujun_up_check(target)
            player = self._get_player()
            if player is not None and int(player.talent.get(83, 0)):
                target.exp[50] = int(target.exp.get(50, 0)) + 1

        # 快乐刻印
        local2 = up.get(0, 0) + up.get(1, 0) + up.get(2, 0) + up.get(14, 0)
        if local2 >= 500 and local2 < 1500 and int(target.mark.get(1, 0)) <= 0:
            target.mark[1] = 1
            v.tflag[23] = 1
        elif local2 >= 1500 and local2 < 3000 and int(target.mark.get(1, 0)) <= 1:
            target.mark[1] = 2
            v.tflag[23] = 2
        elif local2 >= 3000 and int(target.mark.get(1, 0)) <= 2:
            target.mark[1] = 3
            v.tflag[23] = 3
            if int(target.abl.get(10, 0)) == 0 and int(target.talent.get(20, 0)) == 0 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 1
                self._jujun_up_check(target)

        # 屈服刻印
        tflag200 = v.tflag.get(200, 0)
        if tflag200 == 1 and int(target.mark.get(2, 0)) <= 0:
            target.mark[2] = 1
            v.tflag[24] = 1
        elif tflag200 == 2 and int(target.mark.get(2, 0)) <= 1:
            target.mark[2] = 2
            v.tflag[24] = 2
            if int(target.abl.get(10, 0)) == 0 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 1
                self._jujun_up_check(target)
        elif tflag200 == 3 and int(target.mark.get(2, 0)) <= 2:
            target.mark[2] = 3
            v.tflag[24] = 3
            if int(target.abl.get(10, 0)) <= 1 and int(target.talent.get(22, 0)) == 0:
                target.abl[10] = 2
                self._jujun_up_check(target)

    # =================================================================
    # YOKUBO_UP_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _yokubo_up_check(self, target: Character) -> None:
        """欲望の上昇による[压抑][抵抗]の消滅をチェック - YOKUBO_UP_CHECK"""
        v = self.interpreter.vars
        if int(target.abl.get(11, 0)) >= 3 and (int(target.talent.get(32, 0)) or int(target.talent.get(34, 0))):
            if int(target.talent.get(32, 0)):
                target.talent[32] = 0
            if int(target.talent.get(34, 0)):
                target.talent[34] = 0
            target.juel[100] = int(target.juel.get(100, 0)) // 2
            v.tflag[25] = 1

    # =================================================================
    # JUJUN_UP_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _jujun_up_check(self, target: Character) -> None:
        """顺从の上昇による[反抗心]の反転をチェック - JUJUN_UP_CHECK"""
        if int(target.abl.get(10, 0)) >= 4 and int(target.talent.get(11, 0)) and int(target.talent.get(18, 0)):
            target.talent[11] = 0
            target.talent[13] = 1

    # =================================================================
    # EXP_GOT_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _exp_got_check(self, target: Character, up: Dict[int, int]) -> Dict[int, int]:
        """侍奉快乐经验、被虐快乐经验、肛门快乐经验のチェック - EXP_GOT_CHECK"""
        v = self.interpreter.vars

        # 侍奉快乐经验のチェック
        local = up.get(0, 0) + up.get(1, 0) + up.get(2, 0) + up.get(14, 0)
        local1 = 0

        if up.get(7, 0) < 100:
            local = 0
        elif up.get(7, 0) < 300:
            pass  # local *= 1
        elif up.get(7, 0) < 700:
            local *= 2
        elif up.get(7, 0) < 1500:
            local *= 3
        else:
            local *= 4

        if v.tflag.get(100, 0):
            if local >= 12000:
                local1 = 16
                up[11] = int(up.get(11, 0) * 0.65)
                up[12] = int(up.get(12, 0) * 0.30)
            elif local >= 8000:
                local1 = 12
                up[11] = int(up.get(11, 0) * 0.70)
                up[12] = int(up.get(12, 0) * 0.40)
            elif local >= 5000:
                local1 = 8
                up[11] = int(up.get(11, 0) * 0.75)
                up[12] = int(up.get(12, 0) * 0.50)
            elif local >= 3000:
                local1 = 4
                up[11] = int(up.get(11, 0) * 0.80)
                up[12] = int(up.get(12, 0) * 0.60)
            elif local >= 2000:
                local1 = 2
                up[11] = int(up.get(11, 0) * 0.85)
                up[12] = int(up.get(12, 0) * 0.70)
            elif local >= 1000:
                local1 = 1
                up[11] = int(up.get(11, 0) * 0.90)
                up[12] = int(up.get(12, 0) * 0.80)
            if local1:
                target.exp[21] = int(target.exp.get(21, 0)) + local1
                v.tflag[26] = local1

        # Ａ快楽経験のチェック
        local = up.get(2, 0)
        local1 = 0

        if up.get(2, 0) < 300:
            local = 0
        elif up.get(2, 0) < 1000:
            pass  # local *= 1
        elif up.get(2, 0) < 5000:
            local *= 2
        elif up.get(2, 0) < 10000:
            local *= 3
        else:
            local *= 4

        if local >= 12000:
            local1 = 16
            up[11] = int(up.get(11, 0) * 0.80)
            up[12] = int(up.get(12, 0) * 0.90)
            up[6] = int(up.get(6, 0) * 1.20)
        elif local >= 8000:
            local1 = 12
            up[11] = int(up.get(11, 0) * 0.85)
            up[12] = int(up.get(12, 0) * 0.90)
            up[6] = int(up.get(6, 0) * 1.15)
        elif local >= 5000:
            local1 = 8
            up[11] = int(up.get(11, 0) * 0.85)
            up[12] = int(up.get(12, 0) * 0.95)
            up[6] = int(up.get(6, 0) * 1.10)
        elif local >= 3000:
            local1 = 4
            up[11] = int(up.get(11, 0) * 0.90)
            up[12] = int(up.get(12, 0) * 0.95)
            up[6] = int(up.get(6, 0) * 1.05)
        elif local >= 2000:
            local1 = 2
            up[11] = int(up.get(11, 0) * 0.90)
            up[12] = int(up.get(12, 0) * 1.00)
            up[6] = int(up.get(6, 0) * 1.00)
        elif local >= 1000:
            local1 = 1
            up[11] = int(up.get(11, 0) * 0.95)
            up[12] = int(up.get(12, 0) * 1.00)
            up[6] = int(up.get(6, 0) * 1.00)

        if local1:
            target.exp[32] = int(target.exp.get(32, 0)) + local1
            v.tflag[28] = local1

        # 被虐・嗜虐快楽経験のチェック
        local = up.get(0, 0) + up.get(1, 0) + up.get(2, 0) + up.get(14, 0)
        if local == 0:
            local = up.get(5, 0)

        local1 = 0
        if local >= 3000 and up.get(9, 0) >= 2000:
            local1 = 16
            up[11] = int(up.get(11, 0) * 0.65)
        elif local >= 2500 and up.get(9, 0) >= 1500:
            local1 = 12
            up[11] = int(up.get(11, 0) * 0.70)
        elif local >= 1500 and up.get(9, 0) >= 1000:
            local1 = 8
            up[11] = int(up.get(11, 0) * 0.75)
        elif local >= 1000 and up.get(9, 0) >= 500:
            local1 = 4
            up[11] = int(up.get(11, 0) * 0.80)
        elif local >= 600 and up.get(9, 0) >= 300:
            local1 = 2
            up[11] = int(up.get(11, 0) * 0.85)
        elif local >= 300 and up.get(9, 0) >= 100:
            local1 = 1
            up[11] = int(up.get(11, 0) * 0.90)

        if local1:
            target.exp[30] = int(target.exp.get(30, 0)) + local1
            v.tflag[27] = local1

            # 助手の嗜虐快楽経験上昇
            if self.state.assiplay and int(v.assi) > 0:
                assi_idx = int(v.assi)
                if assi_idx < len(self.interpreter.vars.chars):
                    assi_char = self.interpreter.vars.chars[assi_idx]
                    abl_sum = int(assi_char.abl.get(20, 0)) + int(target.equipt.get(47, 0))
                    local2 = 0
                    if abl_sum == 0:
                        local1 = 0
                        local2 = 0
                    elif abl_sum == 1:
                        local1 = int(local1 * 0.50)
                        local2 = 0
                    elif abl_sum == 2:
                        local2 = local1 // 2
                    elif abl_sum == 3:
                        local2 = local1 * 2
                    elif abl_sum == 4:
                        local2 = local1 * 10
                    elif abl_sum >= 5:
                        local2 = local1 * 50
                    if local1:
                        assi_char.exp[33] = int(assi_char.exp.get(33, 0)) + local1
                    if local2:
                        assi_char.juel[5] = int(assi_char.juel.get(5, 0)) + local2

        return up

    # =================================================================
    # SOKUOCHI_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _sokuochi_check(self, target: Character, up: Dict[int, int]) -> None:
        """[容易陷落]のチェック - SOKUOCHI_CHECK"""
        if int(target.talent.get(73, 0)) == 0:
            return

        # C感
        if not (int(target.talent.get(101, 0)) & 2):
            if up.get(0, 0) > 1 and int(target.abl.get(0, 0)) < 1:
                target.abl[0] = 1
            elif up.get(0, 0) > 30 and int(target.abl.get(0, 0)) < 2:
                target.abl[0] = 2
            elif up.get(0, 0) > 60 and int(target.abl.get(0, 0)) < 3:
                target.abl[0] = 3
            elif up.get(0, 0) > 200 and int(target.abl.get(0, 0)) < 4:
                target.abl[0] = 4
            elif up.get(0, 0) > 1000 and int(target.abl.get(0, 0)) < 5:
                target.abl[0] = 5

        # V感
        if not (int(target.talent.get(103, 0)) & 2):
            if up.get(1, 0) > 1 and int(target.abl.get(2, 0)) < 1:
                target.abl[2] = 1
            elif up.get(1, 0) > 30 and int(target.abl.get(2, 0)) < 2:
                target.abl[2] = 2
            elif up.get(1, 0) > 60 and int(target.abl.get(2, 0)) < 3:
                target.abl[2] = 3
            elif up.get(1, 0) > 200 and int(target.abl.get(2, 0)) < 4:
                target.abl[2] = 4
            elif up.get(1, 0) > 1000 and int(target.abl.get(2, 0)) < 5:
                target.abl[2] = 5

        # A感
        if not (int(target.talent.get(105, 0)) & 2):
            if up.get(2, 0) > 1 and int(target.abl.get(3, 0)) < 1:
                target.abl[3] = 1
            elif up.get(2, 0) > 30 and int(target.abl.get(3, 0)) < 2:
                target.abl[3] = 2
            elif up.get(2, 0) > 60 and int(target.abl.get(3, 0)) < 3:
                target.abl[3] = 3
            elif up.get(2, 0) > 200 and int(target.abl.get(3, 0)) < 4:
                target.abl[3] = 4
            elif up.get(2, 0) > 1000 and int(target.abl.get(3, 0)) < 5:
                target.abl[3] = 5

        # B感
        if not (int(target.talent.get(107, 0)) & 2):
            if up.get(14, 0) > 1 and int(target.abl.get(1, 0)) < 1:
                target.abl[1] = 1
            elif up.get(14, 0) > 30 and int(target.abl.get(1, 0)) < 2:
                target.abl[1] = 2
            elif up.get(14, 0) > 60 and int(target.abl.get(1, 0)) < 3:
                target.abl[1] = 3
            elif up.get(14, 0) > 200 and int(target.abl.get(1, 0)) < 4:
                target.abl[1] = 4
            elif up.get(14, 0) > 1000 and int(target.abl.get(1, 0)) < 5:
                target.abl[1] = 5

        # 顺从
        if up.get(4, 0) > 1 and int(target.abl.get(10, 0)) < 1:
            target.abl[10] = 1
        elif up.get(4, 0) > 30 and int(target.abl.get(10, 0)) < 2:
            target.abl[10] = 2
        elif up.get(4, 0) > 60 and int(target.abl.get(10, 0)) < 3:
            target.abl[10] = 3
        elif up.get(4, 0) > 200 and int(target.abl.get(10, 0)) < 4:
            target.abl[10] = 4
        elif up.get(4, 0) > 1000 and int(target.abl.get(10, 0)) < 5:
            target.abl[10] = 5

        # 欲望
        if up.get(5, 0) > 1 and int(target.abl.get(11, 0)) < 1:
            target.abl[11] = 1
        elif up.get(5, 0) > 30 and int(target.abl.get(11, 0)) < 2:
            target.abl[11] = 2
        elif up.get(5, 0) > 60 and int(target.abl.get(11, 0)) < 3:
            target.abl[11] = 3
        elif up.get(5, 0) > 200 and int(target.abl.get(11, 0)) < 4:
            target.abl[11] = 4
        elif up.get(5, 0) > 1000 and int(target.abl.get(11, 0)) < 5:
            target.abl[11] = 5

        # 技巧
        if up.get(7, 0) > 1 and int(target.abl.get(12, 0)) < 1:
            target.abl[12] = 1
        elif up.get(7, 0) > 30 and int(target.abl.get(12, 0)) < 2:
            target.abl[12] = 2
        elif up.get(7, 0) > 60 and int(target.abl.get(12, 0)) < 3:
            target.abl[12] = 3
        elif up.get(7, 0) > 200 and int(target.abl.get(12, 0)) < 4:
            target.abl[12] = 4
        elif up.get(7, 0) > 1000 and int(target.abl.get(12, 0)) < 5:
            target.abl[12] = 5

        # 奉仕精神
        if up.get(6, 0) > 1 and int(target.abl.get(16, 0)) < 1 and int(target.abl.get(0, 0)) >= 1:
            target.abl[16] = 1
        elif up.get(6, 0) > 30 and int(target.abl.get(16, 0)) < 2 and int(target.abl.get(0, 0)) >= 2:
            target.abl[16] = 2
        elif up.get(6, 0) > 60 and int(target.abl.get(16, 0)) < 3 and int(target.abl.get(0, 0)) >= 3:
            target.abl[16] = 3
        elif up.get(6, 0) > 200 and int(target.abl.get(16, 0)) < 4 and int(target.abl.get(0, 0)) >= 4:
            target.abl[16] = 4
        elif up.get(6, 0) > 1000 and int(target.abl.get(16, 0)) < 5 and int(target.abl.get(0, 0)) >= 5:
            target.abl[16] = 5

        # 露出癖
        if up.get(8, 0) > 1 and int(target.abl.get(17, 0)) < 1 and int(target.abl.get(1, 0)) >= 1:
            target.abl[17] = 1
        elif up.get(8, 0) > 30 and int(target.abl.get(17, 0)) < 2 and int(target.abl.get(1, 0)) >= 2:
            target.abl[17] = 2
        elif up.get(8, 0) > 60 and int(target.abl.get(17, 0)) < 3 and int(target.abl.get(1, 0)) >= 3:
            target.abl[17] = 3
        elif up.get(8, 0) > 200 and int(target.abl.get(17, 0)) < 4 and int(target.abl.get(1, 0)) >= 4:
            target.abl[17] = 4
        elif up.get(8, 0) > 1000 and int(target.abl.get(17, 0)) < 5 and int(target.abl.get(1, 0)) >= 5:
            target.abl[17] = 5

        # 苦痛楽しみ
        if up.get(9, 0) > 1 and int(target.abl.get(21, 0)) < 1 and int(target.abl.get(11, 0)) >= 1:
            target.abl[21] = 1
        elif up.get(9, 0) > 30 and int(target.abl.get(21, 0)) < 2 and int(target.abl.get(11, 0)) >= 2:
            target.abl[21] = 2
        elif up.get(9, 0) > 60 and int(target.abl.get(21, 0)) < 3 and int(target.abl.get(11, 0)) >= 3:
            target.abl[21] = 3
        elif up.get(9, 0) > 200 and int(target.abl.get(21, 0)) < 4 and int(target.abl.get(11, 0)) >= 4:
            target.abl[21] = 4
        elif up.get(9, 0) > 1000 and int(target.abl.get(21, 0)) < 5 and int(target.abl.get(11, 0)) >= 5:
            target.abl[21] = 5

        # 百合气质
        if int(target.exp.get(40, 0)) > 1 and int(target.abl.get(22, 0)) < 1 and int(target.abl.get(11, 0)) >= 1:
            target.abl[22] = 1
        elif int(target.exp.get(40, 0)) > 5 and int(target.abl.get(22, 0)) < 2 and int(target.abl.get(11, 0)) >= 2:
            target.abl[22] = 2
        elif int(target.exp.get(40, 0)) > 20 and int(target.abl.get(22, 0)) < 3 and int(target.abl.get(11, 0)) >= 3:
            target.abl[22] = 3
        elif int(target.exp.get(40, 0)) > 40 and int(target.abl.get(22, 0)) < 4 and int(target.abl.get(11, 0)) >= 4:
            target.abl[22] = 4
        elif int(target.exp.get(40, 0)) > 100 and int(target.abl.get(22, 0)) < 5 and int(target.abl.get(11, 0)) >= 5:
            target.abl[22] = 5

        # ホモっ気
        if int(target.exp.get(41, 0)) > 1 and int(target.abl.get(23, 0)) < 1 and int(target.abl.get(11, 0)) >= 1:
            target.abl[23] = 1
        elif int(target.exp.get(41, 0)) > 5 and int(target.abl.get(23, 0)) < 2 and int(target.abl.get(11, 0)) >= 2:
            target.abl[23] = 2
        elif int(target.exp.get(41, 0)) > 20 and int(target.abl.get(23, 0)) < 3 and int(target.abl.get(11, 0)) >= 3:
            target.abl[23] = 3
        elif int(target.exp.get(41, 0)) > 40 and int(target.abl.get(23, 0)) < 4 and int(target.abl.get(11, 0)) >= 4:
            target.abl[23] = 4
        elif int(target.exp.get(41, 0)) > 100 and int(target.abl.get(23, 0)) < 5 and int(target.abl.get(11, 0)) >= 5:
            target.abl[23] = 5

    # =================================================================
    # ECST_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _ecst_check(self, arg: int) -> None:
        """絶頂時の追加処理 - ECST_CHECK"""
        self.interpreter.vars.tflag[29] = arg

    # =================================================================
    # PISSING_ECST_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _pissing_ecst_check(self, target: Character) -> None:
        """絶頂時のおもらし処理 - PISSING_ECST_CHECK"""
        v = self.interpreter.vars
        tflag29 = int(v.tflag.get(29, 0))
        tequip22 = int(target.equipt.get(22, 0))
        talent57 = int(target.talent.get(57, 0))

        # 超大量放尿
        if tflag29 >= 7 and tequip22 and talent57:
            target.exp[31] = int(target.exp.get(31, 0)) + 5
            target.equipt[22] = 0
            target.stain[2] = int(target.stain.get(2, 0)) | 32
            target.stain[3] = int(target.stain.get(3, 0)) | 32
        # 大量放尿
        elif (tflag29 >= 7 and tequip22) or (tflag29 >= 5 and tequip22 and talent57):
            target.exp[31] = int(target.exp.get(31, 0)) + 4
            target.equipt[22] = 0
            target.stain[2] = int(target.stain.get(2, 0)) | 32
            target.stain[3] = int(target.stain.get(3, 0)) | 32
        # 放尿
        elif (tflag29 >= 7 and talent57) or (tflag29 >= 5 and tequip22) or (tflag29 >= 3 and tequip22 and talent57):
            target.exp[31] = int(target.exp.get(31, 0)) + 3
            target.equipt[22] = 0
            target.stain[2] = int(target.stain.get(2, 0)) | 32
            target.stain[3] = int(target.stain.get(3, 0)) | 32
        # 失禁
        elif (tflag29 >= 5 and talent57) or (tflag29 >= 3 and tequip22) or (tflag29 >= 1 and tequip22 and talent57):
            target.exp[31] = int(target.exp.get(31, 0)) + 2
            if talent57 == 0:
                target.equipt[22] = 0
            target.stain[2] = int(target.stain.get(2, 0)) | 32
            target.stain[3] = int(target.stain.get(3, 0)) | 32
        # 微量失禁
        elif (tflag29 >= 3 and talent57) or (tflag29 >= 1 and tequip22):
            target.exp[31] = int(target.exp.get(31, 0)) + 1
            target.stain[2] = int(target.stain.get(2, 0)) | 32
            target.stain[3] = int(target.stain.get(3, 0)) | 32

    # =================================================================
    # MASTER_FLAG_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _master_flag_check(self, target: Character) -> None:
        """主人による調教の经验值 - MASTER_FLAG_CHECK"""
        v = self.interpreter.vars

        # 絶頂
        v.tflag[29] = int(v.tflag.get(29, 0)) + int(v.tflag.get(10, 0)) + int(v.tflag.get(11, 0))
        q = 0
        if int(target.nowex.get(0, 0)) > 0:
            q += 1
        if int(target.nowex.get(1, 0)) > 0:
            q += 1
        if int(target.nowex.get(2, 0)) > 0:
            q += 1
        if int(target.nowex.get(3, 0)) > 0:
            q += 1
        if int(v.tflag.get(10, 0)) > 0:
            q += 1
        if int(v.tflag.get(11, 0)) > 0:
            q += 1
        v.tflag[30] = int(v.tflag.get(30, 0)) + int(v.tflag.get(29, 0)) * q

        # 射精
        for count in range(5):
            if int(v.tflag.get(count, 0)) > 0 and int(target.exp.get(20, 0)) >= self.exp_level_thresholds[3]:
                v.tflag[30] = int(v.tflag.get(30, 0)) + int(v.tflag.get(count, 0))
        if int(v.tflag.get(9, 0)) > 0 and int(target.exp.get(20, 0)) >= self.exp_level_thresholds[3]:
            v.tflag[30] = int(v.tflag.get(30, 0)) + int(v.tflag.get(9, 0))

        # 主人と対象の能力を計算
        if self.state.assiplay == 0 and int(target.equipt.get(90, 0)) == 0:
            r = int(target.abl.get(10, 0))

            # 素質による増減
            if int(target.talent.get(11, 0)):
                r -= 1
            if int(target.talent.get(13, 0)):
                r += 1
            if int(target.talent.get(20, 0)):
                r -= 1
            if int(target.talent.get(21, 0)):
                r -= 1
            if int(target.talent.get(22, 0)):
                r -= 1
            if int(target.talent.get(34, 0)):
                r -= 1
            if int(target.talent.get(63, 0)):
                r += 1
            if int(target.talent.get(70, 0)):
                r += 1
            if int(target.talent.get(71, 0)):
                r -= 1

            # 男人婆
            if int(target.talent.get(79, 0)):
                master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
                if master is not None and int(master.talent.get(122, 0)) == 0:
                    r -= 1

            # 讨厌男人
            if int(target.talent.get(82, 0)):
                master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
                if master is not None and int(master.talent.get(122, 0)):
                    r -= 1

            if int(target.talent.get(85, 0)):
                r += 2
            if int(target.talent.get(86, 0)):
                r += 2

            # 主人の魅惑/谜之魅力/魅力/人気
            master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
            if master is not None:
                if int(master.talent.get(91, 0)):
                    r += 1
                if int(master.talent.get(92, 0)):
                    r += 1
                if int(master.talent.get(113, 0)):
                    r += 1
                if int(master.talent.get(126, 0)):
                    r += 1

            if r <= 0:
                r = 1

            r += int(v.tflag.get(30, 0))

            # 相性による修正
            master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
            if master is not None:
                relation_val = self._get_relation_value(master)
                if relation_val != 0:
                    r = r * relation_val // 100

            target.cflag[2] = int(target.cflag.get(2, 0)) + r

        v.tflag[30] = 0

    # =================================================================
    # TARGET_WORMBABY_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _target_wormbaby_check(self, target: Character, up: Dict[int, int]) -> None:
        """ワーム出産チェック - TARGET_WORMBABY_CHECK"""
        v = self.interpreter.vars

        if int(target.talent.get(190, 0)) == 0 and int(target.talent.get(191, 0)) == 0:
            return

        local = up.get(0, 0) + up.get(1, 0) + up.get(2, 0) + up.get(14, 0)

        # 克制
        if int(target.talent.get(20, 0)):
            local //= 2

        # 接受快感
        if int(target.talent.get(70, 0)):
            local = int(local * 1.20)

        # 淫乱化
        if int(target.talent.get(76, 0)):
            local = int(local * 1.10)

        # 否定快感
        if int(target.talent.get(71, 0)):
            local = int(local * 0.80)

        # 媚药
        if int(target.equipt.get(21, 0)):
            local *= 2

        if local > 25000:
            local1 = 2
        elif local > 10000:
            local1 = 1
        else:
            local1 = 0

        source = target.source
        if local1 == 2:
            target.base[0] = int(target.base.get(0, 0)) - 20
            target.base[1] = int(target.base.get(1, 0)) - 100
            exp3 = int(target.exp.get(3, 0))
            exp_lv = self.exp_level_thresholds
            if exp3 < exp_lv[1]:
                source[12] = source.get(12, 0) + 20000
                source[13] = source.get(13, 0) + 10000
            elif exp3 < exp_lv[2]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 8000
            elif exp3 < exp_lv[3]:
                source[12] = source.get(12, 0) + 7000
                source[13] = source.get(13, 0) + 6000
            elif exp3 < exp_lv[4]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp3 < exp_lv[5]:
                source[12] = source.get(12, 0) + 3000
                source[13] = source.get(13, 0) + 2000
            else:
                source[12] = source.get(12, 0) + 1800
                source[13] = source.get(13, 0) + 1200
            target.exp[60] = int(target.exp.get(60, 0)) + 2
        elif local1 == 1:
            target.base[1] = int(target.base.get(1, 0)) - 40
            exp3 = int(target.exp.get(3, 0))
            exp_lv = self.exp_level_thresholds
            if exp3 < exp_lv[1]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 5000
            elif exp3 < exp_lv[2]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp3 < exp_lv[3]:
                source[12] = source.get(12, 0) + 2500
                source[13] = source.get(13, 0) + 2000
            elif exp3 < exp_lv[4]:
                source[12] = source.get(12, 0) + 1600
                source[13] = source.get(13, 0) + 1400
            elif exp3 < exp_lv[5]:
                source[12] = source.get(12, 0) + 800
                source[13] = source.get(13, 0) + 500
            else:
                source[12] = source.get(12, 0) + 200
                source[13] = source.get(13, 0) + 250
            target.exp[60] = int(target.exp.get(60, 0)) + 1

        if int(target.talent.get(190, 0)) == 1 and int(target.talent.get(191, 0)) == 1:
            v.tflag[120] = local1
            v.tflag[121] = local1
        elif int(target.talent.get(190, 0)) == 1:
            v.tflag[120] = local1
        else:
            v.tflag[121] = local1

    # =================================================================
    # AUTO_NUM_CHECK (SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _auto_num_check(self, target: Character, up: Dict[int, int]) -> Dict[int, int]:
        """自動調教回数による調教のボーナス - AUTO_NUM_CHECK"""
        cflag667 = int(target.cflag.get(667, 0))

        if cflag667 < 5:
            mult = 1.25
        elif cflag667 < 10:
            mult = 1.50
        elif cflag667 < 15:
            mult = 2.10
        elif cflag667 < 20:
            mult = 2.85
        elif cflag667 < 25:
            mult = 3.90
        elif cflag667 < 30:
            mult = 5.30
        elif cflag667 < 40:
            mult = 7.25
        else:
            mult = 9.90

        for local in range(17):
            if local >= 11 and local != 14:
                continue
            up[local] = int(up.get(local, 0) * mult)

        return up

    # =================================================================
    # SOUL_DISLOCATION_DEBUFF (SYSTEM_SOURCE_SUB2.ERB)
    # =================================================================

    def _soul_dislocation_debuff(self, target: Character) -> None:
        """灵魂错位处理 - SOUL_DISLOCATION_DEBUFF"""
        ex_talent0 = int(target.ex_talent.get(0, 0)) if hasattr(target, 'ex_talent') else 0
        if ex_talent0 == 0:
            return
        temp = 100 - 15 * ex_talent0
        source = target.source
        for local in range(19):
            source[local] = int(source.get(local, 0) * temp) // 100

    # =================================================================
    # TARGET_EJAC_CHECK (完整版, SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _target_ejac_check_full(self, target: Character, up: Dict[int, int]) -> None:
        """調教対象の射精チェック - TARGET_EJAC_CHECK (完整版)"""
        v = self.interpreter.vars

        if int(target.talent.get(121, 0)) == 0 and int(target.talent.get(122, 0)) == 0:
            return

        import random
        mijyuku = 0
        if int(target.talent.get(135, 0)):
            mijyuku = random.randint(0, 699) - random.randint(0, 799) + 400

        local = up.get(0, 0) + up.get(1, 0) + up.get(2, 0) + up.get(14, 0)

        # 克制
        if int(target.talent.get(20, 0)):
            local //= 2

        # 接受快感
        if int(target.talent.get(70, 0)):
            local = int(local * 1.20)

        # 淫乱化
        if int(target.talent.get(76, 0)):
            local = int(local * 1.10)

        # 否定快感
        if int(target.talent.get(71, 0)):
            local = int(local * 0.80)

        # 媚药
        if int(target.equipt.get(21, 0)):
            local *= 2

        # 利尿剂
        if int(target.equipt.get(22, 0)):
            local //= 2

        # 安全套
        if int(target.equipt.get(37, 0)):
            local //= 2

        # 未熟
        if int(target.talent.get(135, 0)):
            local -= mijyuku

        local = 1000 + (local - 1000) // 2
        target.base[2] = int(target.base.get(2, 0)) + local

        # 未熟処理
        if int(target.talent.get(135, 0)):
            base2 = int(target.base.get(2, 0))
            maxbase2 = int(target.maxbase.get(2, 0))
            if base2 >= 2000 and int(target.base.get(2, 0)) - local < 2000:
                pass  # 尚未成熟的阴茎似乎渐渐有了感觉
            if base2 <= 2000 and int(target.base.get(2, 0)) - local >= 2000:
                target.base[2] = 2000

        local = int(target.base.get(2, 0))
        ejac = int(target.maxbase.get(2, 0))

        if local > ejac * 2:
            local1 = 2
        elif local > ejac:
            local1 = 1
        else:
            local1 = 0

        source = target.source
        exp3 = int(target.exp.get(3, 0))
        exp_lv = self.exp_level_thresholds

        if local1 == 2:
            target.base[0] = int(target.base.get(0, 0)) - 20
            target.base[1] = int(target.base.get(1, 0)) - 100

            if exp3 < exp_lv[1]:
                source[12] = source.get(12, 0) + 20000
                source[13] = source.get(13, 0) + 10000
            elif exp3 < exp_lv[2]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 8000
            elif exp3 < exp_lv[3]:
                source[12] = source.get(12, 0) + 7000
                source[13] = source.get(13, 0) + 6000
            elif exp3 < exp_lv[4]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp3 < exp_lv[5]:
                source[12] = source.get(12, 0) + 3000
                source[13] = source.get(13, 0) + 2000
            else:
                source[12] = source.get(12, 0) + 1800
                source[13] = source.get(13, 0) + 1200

            if exp3 == 0 and int(target.talent.get(122, 0)) == 0:
                target.exp[50] = int(target.exp.get(50, 0)) + 1
            target.exp[20] = int(target.exp.get(20, 0)) + 1
            target.exp[3] = int(target.exp.get(3, 0)) + 2

            # 未熟
            if int(target.talent.get(135, 0)):
                target.maxbase[0] = max(600, int(target.maxbase.get(0, 0)) - 10)
                target.maxbase[1] = max(100, int(target.maxbase.get(1, 0)) - 30)
                target.base[0] = int(target.base.get(0, 0)) - 50
                target.base[1] = int(target.base.get(1, 0)) - 100

            # Pに精液汚れ
            target.stain[2] = int(target.stain.get(2, 0)) | 4

            target.base[2] = int(target.base.get(2, 0)) - ejac * 2
            if int(target.base.get(2, 0)) >= ejac:
                target.base[2] = ejac - 1

            v.tflag[10] = 2
            target.nowex[5] = int(target.nowex.get(5, 0)) + 1
            target.ex[5] = int(target.ex.get(5, 0)) + 1

        elif local1 == 1:
            target.base[1] = int(target.base.get(1, 0)) - 40

            if exp3 < exp_lv[1]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 5000
            elif exp3 < exp_lv[2]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp3 < exp_lv[3]:
                source[12] = source.get(12, 0) + 2500
                source[13] = source.get(13, 0) + 2000
            elif exp3 < exp_lv[4]:
                source[12] = source.get(12, 0) + 1600
                source[13] = source.get(13, 0) + 1400
            elif exp3 < exp_lv[5]:
                source[12] = source.get(12, 0) + 800
                source[13] = source.get(13, 0) + 500
            else:
                source[12] = source.get(12, 0) + 200
                source[13] = source.get(13, 0) + 250

            if exp3 == 0 and int(target.talent.get(122, 0)) == 0:
                target.exp[50] = int(target.exp.get(50, 0)) + 1
            target.exp[3] = int(target.exp.get(3, 0)) + 1

            # 未熟
            if int(target.talent.get(135, 0)):
                target.maxbase[0] = max(600, int(target.maxbase.get(0, 0)) - 10)
                target.maxbase[1] = max(100, int(target.maxbase.get(1, 0)) - 10)
                target.base[0] = int(target.base.get(0, 0)) - 10
                target.base[1] = int(target.base.get(1, 0)) - 40

            # Pに精液汚れ
            target.stain[2] = int(target.stain.get(2, 0)) | 4

            target.base[2] = int(target.base.get(2, 0)) - ejac
            if int(target.base.get(2, 0)) >= ejac:
                target.base[2] = ejac - 1

            v.tflag[10] = 1
            target.nowex[6] = int(target.nowex.get(6, 0)) + 1
            target.ex[6] = int(target.ex.get(6, 0)) + 1

    # =================================================================
    # TARGET_MILK_CHECK (完整版, SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _target_milk_check_full(self, target: Character, up: Dict[int, int]) -> None:
        """調教対象の噴乳チェック - TARGET_MILK_CHECK (完整版)"""
        v = self.interpreter.vars

        if int(target.talent.get(130, 0)) == 0:
            return

        local = up.get(0, 0) // 5 + up.get(1, 0) // 5 + up.get(2, 0) // 5 + up.get(14, 0) * 3

        # 克制
        if int(target.talent.get(20, 0)):
            local //= 2

        # 接受快感
        if int(target.talent.get(70, 0)):
            local = int(local * 1.20)

        # 淫乱化
        if int(target.talent.get(76, 0)):
            local = int(local * 1.10)

        # 否定快感
        if int(target.talent.get(71, 0)):
            local = int(local * 0.80)

        # B敏感
        if int(target.talent.get(108, 0)):
            local = int(local * 1.50)

        # 媚药
        if int(target.equipt.get(21, 0)):
            local *= 2

        # 利尿剂
        if int(target.equipt.get(22, 0)):
            local //= 2

        # 调教者が幼儿退行
        player = self._get_player()
        if player is not None and int(player.talent.get(131, 0)):
            local *= 2

        # 调教者が幼稚
        if player is not None and int(player.talent.get(132, 0)):
            local *= 2

        # 贫乳
        if int(target.talent.get(109, 0)):
            local = int(local * 0.50)

        # 绝壁
        if int(target.talent.get(116, 0)):
            local = int(local * 0.20)

        local = 1000 + (local - 1000) // 2
        target.base[3] = int(target.base.get(3, 0)) + local

        local = int(target.base.get(3, 0))
        ejac = int(target.maxbase.get(3, 0))

        if local > ejac * 2:
            local1 = 2
        elif local > ejac:
            local1 = 1
        else:
            local1 = 0

        source = target.source
        exp54 = int(target.exp.get(54, 0))
        exp_lv = self.exp_level_thresholds

        if local1 == 2:
            target.base[0] = int(target.base.get(0, 0)) - 20
            target.base[1] = int(target.base.get(1, 0)) - 100

            if exp54 < exp_lv[1]:
                source[12] = source.get(12, 0) + 20000
                source[13] = source.get(13, 0) + 10000
            elif exp54 < exp_lv[2]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 8000
            elif exp54 < exp_lv[3]:
                source[12] = source.get(12, 0) + 7000
                source[13] = source.get(13, 0) + 6000
            elif exp54 < exp_lv[4]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp54 < exp_lv[5]:
                source[12] = source.get(12, 0) + 3000
                source[13] = source.get(13, 0) + 2000
            else:
                source[12] = source.get(12, 0) + 1800
                source[13] = source.get(13, 0) + 1200

            if exp54 == 0:
                target.exp[50] = int(target.exp.get(50, 0)) + 1
            target.exp[54] = int(target.exp.get(54, 0)) + 2

            # Bに母乳汚れ
            target.stain[5] = int(target.stain.get(5, 0)) | 16

            target.base[3] = int(target.base.get(3, 0)) - ejac * 2
            if int(target.base.get(3, 0)) >= ejac:
                target.base[3] = ejac - 1

            v.tflag[11] = int(v.tflag.get(11, 0)) + 2
            if int(target.equipt.get(16, 0)) and int(target.equipt.get(90, 0)) == 0:
                v.tflag[35] = int(v.tflag.get(35, 0)) + 2

            target.nowex[5] = int(target.nowex.get(5, 0)) + 1
            target.ex[5] = int(target.ex.get(5, 0)) + 1

        elif local1 == 1:
            target.base[1] = int(target.base.get(1, 0)) - 40

            if exp54 < exp_lv[1]:
                source[12] = source.get(12, 0) + 10000
                source[13] = source.get(13, 0) + 5000
            elif exp54 < exp_lv[2]:
                source[12] = source.get(12, 0) + 5000
                source[13] = source.get(13, 0) + 4000
            elif exp54 < exp_lv[3]:
                source[12] = source.get(12, 0) + 2500
                source[13] = source.get(13, 0) + 2000
            elif exp54 < exp_lv[4]:
                source[12] = source.get(12, 0) + 1600
                source[13] = source.get(13, 0) + 1400
            elif exp54 < exp_lv[5]:
                source[12] = source.get(12, 0) + 800
                source[13] = source.get(13, 0) + 500
            else:
                source[12] = source.get(12, 0) + 200
                source[13] = source.get(13, 0) + 250

            if exp54 == 0:
                target.exp[50] = int(target.exp.get(50, 0)) + 1
            target.exp[54] = int(target.exp.get(54, 0)) + 1

            # Bに母乳汚れ
            target.stain[5] = int(target.stain.get(5, 0)) | 16

            target.base[3] = int(target.base.get(3, 0)) - ejac
            if int(target.base.get(3, 0)) >= ejac:
                target.base[3] = ejac - 1

            v.tflag[11] = int(v.tflag.get(11, 0)) + 1
            if int(target.equipt.get(16, 0)) and int(target.equipt.get(90, 0)) == 0:
                v.tflag[35] = int(v.tflag.get(35, 0)) + 1

            target.nowex[5] = int(target.nowex.get(5, 0)) + 1
            target.ex[5] = int(target.ex.get(5, 0)) + 1

    # =================================================================
    # LOST_VIRGIN_CHECK (完整版, SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _lost_virgin_check_full(self, target: Character) -> List[str]:
        """处女丧失のチェック - LOST_VIRGIN_CHECK (完整版)"""
        v = self.interpreter.vars
        msgs = []

        if int(target.talent.get(0, 0)) == 0 or v.tflag.get(19, 0) == 0:
            return msgs

        msgs.append("【处女丧失】")
        target.talent[0] = 0

        # 处女丧失フラグ
        v.tflag[3] = 1
        v.tflag[31] = 1

        # ビデオ撮影
        if int(target.equipt.get(53, 0)):
            v.tflag[32] = int(v.tflag.get(32, 0)) | 1

        # 親族関係の判定
        v.tflag[14] = 0
        self._incest(target)

        player = self._get_player()
        if int(target.cflag.get(15, 0)) == 0 and player is not None:
            player_no = int(player.cflag.get(0, 0))
            target.cflag[15] = player_no + 1

            # 初体験が近親相姦
            incest_type = int(v.tflag.get(14, 0))
            if incest_type == 1 and int(player.talent.get(122, 0)):
                target.cflag[15] = 300
            elif incest_type == 1 and int(player.talent.get(122, 0)) == 0:
                target.cflag[15] = 301
            elif incest_type == 3 and int(player.talent.get(122, 0)):
                target.cflag[15] = 304
            elif incest_type == 3 and int(player.talent.get(122, 0)) == 0:
                target.cflag[15] = 305
            elif incest_type == 4 and int(player.talent.get(122, 0)):
                target.cflag[15] = 306
            elif incest_type == 4 and int(player.talent.get(122, 0)) == 0:
                target.cflag[15] = 307
            elif incest_type == 5 and int(player.talent.get(122, 0)) == 0:
                target.cflag[15] = 308
            elif incest_type == 6 and int(player.talent.get(122, 0)):
                target.cflag[15] = 309

            # 初体験がバイブ
            selectcom = self.state.prevcom
            if selectcom == 11:
                target.cflag[15] = 101
            # 初体験が触手生物
            if int(target.equipt.get(90, 0)) and selectcom == 101:
                target.cflag[15] = 102
            # 初体験が犬
            if int(target.equipt.get(89, 0)):
                target.cflag[15] = 103
            # 初体験が死斗场怪物
            if int(target.equipt.get(55, 0)) and self.state.assiplay == 0:
                target.cflag[15] = 104

        source = target.source
        # 初体験の相手が主人で【爱慕】
        master = self.interpreter.vars.chars[0] if self.interpreter.vars.chars else None
        if player is master and int(target.talent.get(85, 0)):
            v.tflag[150] = 1
            source[3] = int(source.get(3, 0) * 2.00)
            source[15] = int(source.get(15, 0) * 0.30)
        # 初体験の時点で既に【淫乱】
        elif int(target.talent.get(76, 0)):
            v.tflag[150] = 1
            source[3] = int(source.get(3, 0) * 2.00)
            source[6] = int(source.get(6, 0) * 0.50)
            source[15] = int(source.get(15, 0) * 0.30)
        # 初体験の相手が助手で相性最高で親族でない
        elif self.state.assiplay and player is not None:
            r = int(player.cflag.get(0, 0))
            rel = int(target.relation.get(r, 0)) if hasattr(target, 'relation') else 0
            if rel >= 200 and v.tflag.get(14, 0) == 0:
                v.tflag[150] = 1

        return msgs

    # =================================================================
    # SOURCE_SEX_CHECK (完整版, SYSTEM_SOURCE_SUB1.ERB)
    # =================================================================

    def _source_sex_check_full(self, target: Character) -> None:
        """同性の場合のチェック - SOURCE_SEX_CHECK (完整版)"""
        player = self._get_player()
        if player is None:
            return

        target_female = int(target.talent.get(122, 0)) == 0
        player_female = int(player.talent.get(122, 0)) == 0

        if target_female and player_female:
            self._source_lesbian_sex_check(target)
        elif not target_female and not player_female:
            self._source_gay_sex_check(target)
