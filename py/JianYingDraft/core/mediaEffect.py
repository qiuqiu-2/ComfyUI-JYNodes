"""
 * @file   : materialVideo.py
 * @date   : 2025/8/8
"""

from . import template
from .media import Media
from ..utils import tools
from ..utils.innerBizTypes import effectDict


class MediaEffect(Media):

    def __init__(self, **kwargs):
        kwargs.setdefault("media_type", "effect")
        super().__init__(**kwargs)

    def _set_material_data_for_content(self):
        """
        设置草稿文件的content部分
        """
        effect_name_or_resource_id = self.kwargs.get("effect_name_or_resource_id")

        effect_data = tools.generate_effect_data(effect_name_or_resource_id)
        effect_data.guid = self.id

        effect_entity = template.get_video_effect(effect_data.guid, effect_data.resource_id, effect_data.name)

        self.material_data_for_content["video_effects"] = effect_entity

        # 特效的各种业务信息为空。后续供track下的segment使用
        self.material_data_for_content["X.extra_material_refs"] = []

    pass
