from __future__ import annotations
"""Module for FaceExtMixin - 面部系统"""
from typing import Dict, List, Any, Optional, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from eraMaouEx import Character


class FaceExtMixin:
    """Mixin providing 面部系统 methods for GameEngine"""

    def _apply_face_sex_base_source_experience_scaling(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        exp_level = self._get_exp_level(target.exp.get(0, 0))
        source[1] = self._scale_value(source[1], self._level_value(exp_level, [20, 60, 100, 120, 130, 180]) / 100.0)
        if exp_level == 0:
            source[6] = 5500
        elif exp_level == 1:
            source[6] = 300
        elif exp_level == 2:
            source[6] = 50
        elif exp_level == 3:
            source[6] = 10
        return source






    def _apply_face_sex_base_source_lube_scaling(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        lube_level = self._get_palam_level(target.palam.get(3, 0))
        source[1] = self._scale_value(source[1], self._level_value(lube_level, [10, 40, 100, 140, 180, 180]) / 100.0)
        source[6] = self._scale_value(source[6], self._level_value(lube_level, [300, 100, 50, 20, 10, 10]) / 100.0)
        return source






    def _apply_face_sex_base_source_lust_scaling(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        lust_level = self._get_palam_level(target.palam.get(5, 0))
        source[1] = self._scale_value(source[1], self._level_value(lust_level, [60, 80, 100, 120, 150, 180]) / 100.0)
        source[3] = self._scale_value(source[3], self._level_value(lust_level, [30, 60, 100, 150, 180, 180]) / 100.0)
        return source






    def _apply_face_sex_base_source_submission_scaling(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        submission_level = target.abl.get(10, 0)
        source[1] = self._scale_value(source[1], self._level_value(submission_level, [50, 80, 100, 130, 160, 200]) / 100.0)
        source[3] = self._scale_value(source[3], self._level_value(submission_level, [60, 80, 100, 120, 140, 160]) / 100.0)
        if target.talent.get(85, 0):
            source[1] = self._scale_value(source[1], 1.5)
            source[3] = self._scale_value(source[3], 2.0)
        return source






    def _apply_face_sex_base_source_technique_scaling(self, target: Character, source: Dict[int, int]) -> Dict[int, int]:
        technique_scale = self._level_value(target.abl.get(12, 0), [50, 80, 100, 150, 250, 400]) / 100.0
        source[4] = self._scale_value(source[4], technique_scale)
        source[5] = self._scale_value(source[5], technique_scale)
        return source






    def _build_face_sex_base_source(self, target: Character) -> Dict[int, int]:
        source = self._build_face_sex_base_source_baseline(target)
        source = self._apply_face_sex_base_source_technique_scaling(target, source)
        source = self._apply_face_sex_base_source_experience_scaling(target, source)
        source = self._apply_face_sex_base_source_lube_scaling(target, source)
        source = self._apply_face_sex_base_source_lust_scaling(target, source)
        source = self._apply_face_sex_base_source_submission_scaling(target, source)
        return source






    def _build_face_sex_base_source_baseline(self, target: Character) -> Dict[int, int]:
        return {
            12: 400,
            4: self._level_value(target.abl.get(16, 0), [50, 150, 200, 250, 300, 350]),
            5: self._level_value(target.abl.get(16, 0), [10, 50, 100, 180, 300, 500]),
            1: self._level_value(target.abl.get(2, 0), [40, 150, 400, 1000, 1700, 2200]),
            3: self._level_value(target.abl.get(2, 0), [150, 250, 350, 500, 700, 1000]),
            6: 0,
        }






    def _get_face_desc(self, target) -> str:
        """Get face description.
        Corresponds to ERB LOOK_INFO eye/pupil/lip section.
        """
        parts: List[str] = []
        eye_shape = int(target.talent.get(305, 0))
        eye_color = int(target.talent.get(306, 0))
        lip = int(target.talent.get(307, 0))
        if eye_shape and eye_color and lip:
            parts.append(f"[眼形：{self._get_eye_shape_name(target)}]"
                         f"[瞳色：{self._get_eye_color_name(target)}]"
                         f"[唇：{self._get_lip_name(target)}]")
        return "".join(parts)





