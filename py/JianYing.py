import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from JianYingDraft.utils.dataStruct import TransitionData, AnimationData
from JianYingDraft.utils.innerBizTypes import *
from JianYingDraft.utils import tools
from JianYingDraft.core.draft import Draft
from JianYingDraft.core.otherSettings import Clip_settings

import os
import folder_paths
import zipfile
import shutil
import uuid
import json

class JyMediaAnimation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件路径": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "素材开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "从素材的哪个时间点开始截取（秒）"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "在轨道上的开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒），0表示使用素材原始时长"}),
            },
            "optional": {
                "媒体组": ("MEDIA_GROUP",),
                "入场动画": ("ANIMATION_IN",),
                "组合动画": ("ANIMATION_GROUP",),
                "出场动画": ("ANIMATION_OUT",),
            }
        }

    def animation_video(self, 文件路径, 素材开始时间, 轨道开始时间, 持续时间, 媒体组=[], 入场动画=None, 组合动画=None, 出场动画=None):
        if not os.path.exists(文件路径):
            raise ValueError(f"文件不存在: {文件路径}")
        
        animation_datas = []
        if 入场动画:
            animation_datas.append(入场动画)
        if 组合动画:
            animation_datas.append(组合动画)
        if 出场动画:
            animation_datas.append(出场动画)
        
        meida={"media_file_full_name": 文件路径, "start_in_media": int(素材开始时间*1000000), "start_at_track": int(轨道开始时间*1000000), "duration": int(持续时间*1000000), "animation_datas": animation_datas}
        
        if 媒体组:
            媒体组.append(meida)
            return (媒体组,)
        else:
            return ([meida],)

class JyMediaNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件路径": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "素材开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "从素材的哪个时间点开始截取（秒）"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "在轨道上的开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒），0表示使用素材原始时长"}),
            },
            "optional": {
                "媒体组": ("MEDIA_GROUP",),
            }
        }

    def jy_media(self, 文件路径, 素材开始时间, 轨道开始时间, 持续时间, 媒体组=[]):
        if not os.path.exists(文件路径):
            raise ValueError(f"文件不存在: {文件路径}")
        
        meida={"media_file_full_name": 文件路径, "start_in_media": int(素材开始时间*1000000), "start_at_track": int(轨道开始时间*1000000), "duration": int(持续时间*1000000)}
        
        if 媒体组:
            媒体组.append(meida)
            return (媒体组,)
        else:
            return ([meida],)

class JyAudioNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件路径": ("STRING",{"default": "","tooltip": "音频地址"}),
                "素材开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "从素材的哪个时间点开始截取（秒）"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "在轨道上的开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒），0表示使用音频原始时长"}),
            },
            "optional": {
                "音频组": ("AUDIO_GROUP",),
            }
        }

    def jy_audio(self, 文件路径, 素材开始时间, 轨道开始时间, 持续时间, 音频组=[]):
        if not os.path.exists(文件路径):
            raise ValueError(f"文件不存在: {文件路径}")
        
        audio={"media_file_full_name": 文件路径, "start_in_media": int(素材开始时间*1000000), "start_at_track": int(轨道开始时间*1000000), "duration": int(持续时间*1000000)}
        
        if 音频组:
            音频组.append(audio)
            return (音频组,)
        else:
            return ([audio],)

class JyCaptionsNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文字内容": ("STRING",{"default": "","multiline": True,"tooltip": "字幕显示的文字内容"}),
                "颜色": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色，支持十六进制颜色值"}),
                "字体大小": ("FLOAT", {"default": 60.0, "min": 1.0, "max": 200.0, "step": 1.0,"tooltip": "字幕字体大小"}),
                "X轴位移": ("FLOAT", {"default": 0.0, "min": -2000.0, "max": 2000.0, "step": 1.0,"tooltip": "字幕在X轴方向的位移像素"}),
                "Y轴位移": ("FLOAT", {"default": 0.0, "min": -2000.0, "max": 2000.0, "step": 1.0,"tooltip": "字幕在Y轴方向的位移像素"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "字幕在轨道上的开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "字幕持续时间（秒）"}),
            },
            "optional": {
                "字幕组": ("CAPTIONS_GROUP",),
            }
        }

    def jy_captions(self, 文字内容, 颜色, 字体大小, X轴位移, Y轴位移, 轨道开始时间, 持续时间, 字幕组=[]):
        captions={"subtitle": 文字内容,"color":颜色,"size":字体大小,"transform_x":X轴位移,"transform_y":Y轴位移, "start_at_track": int(轨道开始时间*1000000), "duration": int(持续时间*1000000)}
        
        if 字幕组:
            字幕组.append(captions)
            return (字幕组,)
        else:
            return ([captions],)

class JyEffectNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "特效名称": ("STRING",{"default": "","tooltip": "剪映内置的特效名称或资源ID"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "特效在轨道上的开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "特效持续时间（秒）"}),
            },
            "optional": {
                "特效组": ("EFFECT_GROUP",),
            }
        }

    def jy_effect(self, 特效名称, 轨道开始时间, 持续时间, 特效组=[]):
        effect={"effect_name_or_resource_id": 特效名称, "start": int(轨道开始时间*1000000), "duration": int(持续时间*1000000)}
        
        if 特效组:
            特效组.append(effect)
            return (特效组,)
        else:
            return ([effect],)

class JyTransition:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "转场名称": ("STRING",{"default": "","tooltip": "剪映内置的转场名称或资源ID"}),
                "持续时间": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "转场持续时间（秒）"}),
                "前媒体": ("MEDIA_GROUP",),
            },
            "optional": {
                "后媒体": ("MEDIA_GROUP",),
            }
        }

    def jy_transition(self, 转场名称, 持续时间, 前媒体, 后媒体=None, 媒体组=[]):
        if 后媒体:
            媒体组.extend(前媒体)
            媒体组.extend(后媒体)
        else:
            媒体组.extend(前媒体)
        
        transition = {"transition": 转场名称, "duration": int(持续时间*1000000)}
        return (媒体组, transition)

class JyAnimationIn:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "动画名称": ("STRING",{"default": "","tooltip": "剪映内置的入场动画名称或资源ID"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_IN",)
    RETURN_NAMES = ("入场动画",)
    FUNCTION = "jy_animation_in"
    CATEGORY = "剪映节点"

    def jy_animation_in(self, 动画名称, 开始时间, 持续时间):
        animation_data = {
            "animation_name_or_resource_id": 动画名称,
            "start": int(开始时间*1000000),
            "duration": int(持续时间*1000000),
            "animation_type": "in"
        }
        return (animation_data,)

class JyAnimationGroup:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "动画名称": ("STRING",{"default": "","tooltip": "剪映内置的组合动画名称或资源ID"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_GROUP",)
    RETURN_NAMES = ("组合动画",)
    FUNCTION = "jy_animation_group"
    CATEGORY = "剪映节点"

    def jy_animation_group(self, 动画名称, 开始时间, 持续时间):
        animation_data = {
            "animation_name_or_resource_id": 动画名称,
            "start": int(开始时间*1000000),
            "duration": int(持续时间*1000000),
            "animation_type": "组"
        }
        return (animation_data,)

class JyAnimationOut:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "动画名称": ("STRING",{"default": "","tooltip": "剪映内置的出场动画名称或资源ID"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画开始时间（秒）"}),
                "持续时间": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "动画持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("ANIMATION_OUT",)
    RETURN_NAMES = ("出场动画",)
    FUNCTION = "jy_animation_out"
    CATEGORY = "剪映节点"

    def jy_animation_out(self, 动画名称, 开始时间, 持续时间):
        animation_data = {
            "animation_name_or_resource_id": 动画名称,
            "start": int(开始时间*1000000),
            "duration": int(持续时间*1000000),
            "animation_type": "out"
        }
        return (animation_data,)

class JyMultiMediaGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "媒体0": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
            },
            "optional": {
                "媒体1": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体2": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体3": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体4": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体5": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体6": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体7": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体8": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
                "媒体9": ("MEIDA,ANIMATION_MEIDA,TRANSITION", ),
            }
        }

    RETURN_TYPES = ("MEIDA_GROUP",)
    RETURN_NAMES = ("媒体组",)
    FUNCTION = "media_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def media_group(self, **kwargs):
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('媒体'):
                if type(kwargs[arg]) == list:
                    mediaList.extend(kwargs[arg])
                else:
                    mediaList.append(kwargs[arg])
        return (mediaList, )

class JyMultiAudioGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "音频0": ("JY_AUDIO", ),
            },
            "optional": {
                "音频1": ("JY_AUDIO", ),
                "音频2": ("JY_AUDIO", ),
                "音频3": ("JY_AUDIO", ),
                "音频4": ("JY_AUDIO", ),
                "音频5": ("JY_AUDIO", ),
                "音频6": ("JY_AUDIO", ),
                "音频7": ("JY_AUDIO", ),
                "音频8": ("JY_AUDIO", ),
                "音频9": ("JY_AUDIO", ),
            }
        }

    RETURN_TYPES = ("AUDIO_GROUP",)
    RETURN_NAMES = ("音频组",)
    FUNCTION = "audio_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def audio_group(self, **kwargs):
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('音频'):
                mediaList.append(kwargs[arg])
        return (mediaList, )

class JyMultiCaptionsGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "字幕0": ("JY_CAPTIONS", ),
            },
            "optional": {
                "字幕1": ("JY_CAPTIONS", ),
                "字幕2": ("JY_CAPTIONS", ),
                "字幕3": ("JY_CAPTIONS", ),
                "字幕4": ("JY_CAPTIONS", ),
                "字幕5": ("JY_CAPTIONS", ),
                "字幕6": ("JY_CAPTIONS", ),
                "字幕7": ("JY_CAPTIONS", ),
                "字幕8": ("JY_CAPTIONS", ),
                "字幕9": ("JY_CAPTIONS", ),
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP",)
    RETURN_NAMES = ("字幕组",)
    FUNCTION = "captions_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def captions_group(self, **kwargs):
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('字幕'):
                mediaList.append(kwargs[arg])
        return (mediaList, )

class JyMultiEffectGroup:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "特效0": ("JY_EFFECT", ),
            },
            "optional": {
                "特效1": ("JY_EFFECT", ),
                "特效2": ("JY_EFFECT", ),
                "特效3": ("JY_EFFECT", ),
                "特效4": ("JY_EFFECT", ),
                "特效5": ("JY_EFFECT", ),
                "特效6": ("JY_EFFECT", ),
                "特效7": ("JY_EFFECT", ),
                "特效8": ("JY_EFFECT", ),
                "特效9": ("JY_EFFECT", ),
            }
        }

    RETURN_TYPES = ("EFFECT_GROUP",)
    RETURN_NAMES = ("特效组",)
    FUNCTION = "effect_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def effect_group(self, **kwargs):
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('特效'):
                mediaList.append(kwargs[arg])
        return (mediaList, )

class JyAudio2CaptionsGroup:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "模型": ("WHISPER_MODEL",),
                "文件路径": ("STRING",{"default": "","tooltip": "音频文件路径"}),
                "轨道开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "字幕在轨道上的开始时间（秒）"}),
                "颜色": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "字体大小": ("FLOAT", {"default": 60.0, "min": 1.0, "max": 200.0, "step": 1.0,"tooltip": "字幕字体大小"}),
                "X轴位移": ("FLOAT", {"default": 0.0, "min": -2000.0, "max": 2000.0, "step": 1.0,"tooltip": "X轴位移"}),
                "Y轴位移": ("FLOAT", {"default": 0.0, "min": -2000.0, "max": 2000.0, "step": 1.0,"tooltip": "Y轴位移"}),
            },
            "optional": {
                "字幕组": ("CAPTIONS_GROUP",),
            }
        }

    RETURN_TYPES = ("CAPTIONS_GROUP",)
    RETURN_NAMES = ("字幕组",)
    FUNCTION = "jy_audio2captions_group"
    CATEGORY = "剪映节点"

    def jy_audio2captions_group(self, 模型, 文件路径, 轨道开始时间, 颜色, 字体大小, X轴位移, Y轴位移, 字幕组=[]):
        if not os.path.exists(文件路径):
            raise ValueError(f"文件不存在: {文件路径}")
        
        result = 模型.transcribe(文件路径)
        segments = result["segments"]
        
        for segment in segments:
            text = segment["text"].strip()
            start = segment["start"] + 轨道开始时间
            end = segment["end"] + 轨道开始时间
            持续时间 = end-start
            captions = {"subtitle": text,"color":颜色,"size":字体大小,"transform_x":X轴位移,"transform_y":Y轴位移, "start_at_track": int(start*1000000), "duration": int(持续时间*1000000)}
            字幕组.append(captions)
        
        return (字幕组,)

class JySaveDraft:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件名前缀": ("STRING",{"default": "剪映草稿"}),
                "媒体组": ("MEDIA_GROUP",),
            },
            "optional": {
                "音频组": ("AUDIO_GROUP",),
                "字幕组": ("CAPTIONS_GROUP",),
                "特效组": ("EFFECT_GROUP",),
                "草稿名称": ("STRING",{"default": "我的剪映草稿"}),
                "画布宽度": ("INT", {"default": 1920, "min": 1, "max": 8192}),
                "画布高度": ("INT", {"default": 1080, "min": 1, "max": 8192}),
                "画布比例": (["16:9", "9:16", "1:1", "4:3", "3:4"], {"default": "16:9"}),
                "草稿时长": ("FLOAT", {"default": 60.0, "min": 0.1, "max": 9999999, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("草稿路径",)
    FUNCTION = "jy_save_draft"
    OUTPUT_NODE = True
    CATEGORY = "剪映节点"

    def jy_save_draft(self, 文件名前缀, 媒体组, 音频组=[], 字幕组=[], 特效组=[], 草稿名称="我的剪映草稿", 画布宽度=1920, 画布高度=1080, 画布比例="16:9", 草稿时长=60.0):
        draft = Draft()
        draft.draft_name = 草稿名称
        draft.canvas_width = 画布宽度
        draft.canvas_height = 画布高度
        draft.canvas_ratio = 画布比例
        draft.duration = int(草稿时长*1000000)
        
        for media in 媒体组:
            draft.add_media(media)
        
        for audio in 音频组:
            draft.add_audio(audio)
        
        for caption in 字幕组:
            draft.add_caption(caption)
        
        for effect in 特效组:
            draft.add_effect(effect)
        
        output_dir = folder_paths.get_output_directory()
        draft_path = draft.save_draft(output_dir, 文件名前缀)
        return (draft_path,)

class JySaveOutDraft:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "草稿路径": ("STRING",{"default": "","tooltip": "JySaveDraft节点生成的草稿文件路径"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("下载链接",)
    FUNCTION = "jy_save_out_draft"
    OUTPUT_NODE = True
    CATEGORY = "剪映节点"

    def jy_save_out_draft(self, 草稿路径):
        if not os.path.exists(草稿路径):
            raise ValueError(f"草稿文件不存在: {草稿路径}")
        
        output_dir = folder_paths.get_output_directory()
        filename = os.path.basename(草稿路径).replace('.draft', '')
        zip_path = os.path.join(output_dir, f"{filename}.zip")
        
        shutil.make_archive(os.path.join(output_dir, filename), 'zip', os.path.dirname(草稿_path))
        return (zip_path,)

NODE_CLASS_MAPPINGS = {
    "JyMediaAnimation": JyMediaAnimation,
    "JyMediaNative": JyMediaNative,
    "JyAudioNative": JyAudioNative,
    "JyCaptionsNative": JyCaptionsNative,
    "JyEffectNative": JyEffectNative,
    "JyTransition": JyTransition,
    "JyAnimationIn": JyAnimationIn,
    "JyAnimationGroup": JyAnimationGroup,
    "JyAnimationOut": JyAnimationOut,
    "JyMultiMediaGroup": JyMultiMediaGroup,
    "JyMultiAudioGroup": JyMultiAudioGroup,
    "JyMultiCaptionsGroup": JyMultiCaptionsGroup,
    "JyMultiEffectGroup": JyMultiEffectGroup,
    "JyAudio2CaptionsGroup": JyAudio2CaptionsGroup,
    "JySaveDraft": JySaveDraft,
    "JySaveOutDraft": JySaveOutDraft,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JyMediaAnimation": "带动画媒体",
    "JyMediaNative": "基础媒体",
    "JyAudioNative": "音频文件",
    "JyCaptionsNative": "字幕文本",
    "JyEffectNative": "视频特效",
    "JyTransition": "转场效果",
    "JyAnimationIn": "入场动画",
    "JyAnimationGroup": "组合动画",
    "JyAnimationOut": "出场动画",
    "JyMultiMediaGroup": "媒体组",
    "JyMultiAudioGroup": "音频组",
    "JyMultiCaptionsGroup": "字幕组",
    "JyMultiEffectGroup": "特效组",
    "JyAudio2CaptionsGroup": "音频转字幕",
    "JySaveDraft": "保存草稿",
    "JySaveOutDraft": "打包下载",
}
