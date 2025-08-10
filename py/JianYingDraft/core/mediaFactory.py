"""
 * @file   : materialFactory.py
 * @time   : 16:10
 * @date   : 2024/3/24
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os

from ..utils.string_helper import StringHelper
from ..utils.dynamic_importer import DynamicImporter
from pymediainfo import MediaInfo


class MediaFactory:
    """
    媒体工厂
    """

    @staticmethod
    def create(media_full_name: str, **kwargs):
        """
        根据素材来信创建素材实体
        :param media_full_name:
        :return:
        """
        if  os.path.isfile(media_full_name) and not os.path.exists(media_full_name):
            return None
        pass
        

                

        media_info = MediaInfo.parse(media_full_name).to_data()["tracks"][1]
        
        
        material_type = media_info['track_type'].lower()
        material_type = StringHelper.upper_first_char(material_type)
        
        if media_full_name.endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")):

            material_type ="Photo"
        
        package_name = __package__+f".media{material_type}"
        class_name = f"Media{material_type}"


        kwargs["mediaInfo"] = media_info
        kwargs["mediaFileFullName"] = media_full_name

        material = DynamicImporter.load_class(package_name, class_name, **kwargs)

        return material
    

        
        
