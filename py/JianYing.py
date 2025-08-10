from .JianYingDraft.utils.dataStruct import TransitionData, AnimationData
from .JianYingDraft.utils.innerBizTypes import *
from .JianYingDraft.utils import tools
from .JianYingDraft.core.draft import Draft
from .JianYingDraft.core.otherSettings import Clip_settings

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

class media_group:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            },
            "optional": {
                "媒体组": ("MEDIA_GROUP",),
                "音频组": ("AUDIO_GROUP",),
                "字幕组": ("CAPTIONS_GROUP",),
                "特效组": ("EFFECT_GROUP",),
            }
        }

    RETURN_TYPES = ("MEDIA_GROUP","AUDIO_GROUP","CAPTIONS_GROUP","EFFECT_GROUP")
    RETURN_NAMES = ("媒体组","音频组","字幕组","特效组")
    FUNCTION = "media_group"
    CATEGORY = "剪映节点"

    def media_group(self, **kwargs):
        媒体组 = kwargs.get("媒体组", [])
        音频组 = kwargs.get("音频组", [])
        字幕组 = kwargs.get("字幕组", [])
        特效组 = kwargs.get("特效组", [])
        return (媒体组, 音频组, 字幕组, 特效组)

class JyAudio2captionsGroup:
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
            },
            "optional": {
                "媒体组": ("MEDIA_GROUP",),
                "音频组": ("AUDIO_GROUP",),
                "字幕组": ("CAPTIONS_GROUP",),
                "特效组": ("EFFECT_GROUP",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("草稿路径",)
    FUNCTION = "save_draft"
    CATEGORY = "剪映节点"
    OUTPUT_NODE = True

    def save_draft(self, 文件名前缀, 媒体组=[], 音频组=[], 字幕组=[], 特效组=[]):
        draft = Draft()
        
        for media in 媒体组:
            draft.add_media(**media)
        for audio in 音频组:
            draft.add_media(**audio)
        for caption in 字幕组:
            draft.add_subtitle(**caption)
        for effect in 特效组:
            draft.add_effect(**effect)
        
        foldername = os.path.join(folder_paths.get_output_directory(), "剪映草稿")
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        
        filename = f"{文件名前缀}_{int(time.time())}.draft"
        file_path = os.path.join(foldername, filename)
        
        draft.save(file_path)
        return (file_path,)

class JySaveOutDraft:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件名前缀": ("STRING",{"default": "剪映草稿"}),
                "输出文件夹": ("STRING",{"default": "","tooltip": "输出文件夹路径，留空使用默认输出目录"}),
            },
            "optional": {
                "媒体组": ("MEDIA_GROUP",),
                "音频组": ("AUDIO_GROUP",),
                "字幕组": ("CAPTIONS_GROUP",),
                "特效组": ("EFFECT_GROUP",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("草稿路径",)
    FUNCTION = "save_out_draft"
    CATEGORY = "剪映节点"
    OUTPUT_NODE = True

    def save_out_draft(self, 文件名前缀, 输出文件夹, 媒体组=[], 音频组=[], 字幕组=[], 特效组=[]):
        draft = Draft()
        
        for media in 媒体组:
            draft.add_media(**media)
        for audio in 音频组:
            draft.add_media(**audio)
        for caption in 字幕组:
            draft.add_subtitle(**caption)
        for effect in 特效组:
            draft.add_effect(**effect)
        
        if 输出文件夹:
            foldername = 输出文件夹
        else:
            foldername = folder_paths.get_output_directory()
        
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        
        filename = f"{文件名前缀}_{int(time.time())}.draft"
        file_path = os.path.join(foldername, filename)
        
        draft.save(file_path)
        return (file_path,)

importStr=r"""import json
import os
import shutil

def replace_text(contentText, data):
    for i in data:
        primary=i["primary"]
        newfile=i["newfile"]
        #获取newfile的绝对路径
        newfile=os.path.abspath(newfile)
        #替换
        contentText.replace(primary,newfile)
    return contentText

inputPath=input("请输入剪映草稿目录:")
if not inputPath:
    inputPath=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft/"
#当前目录文件夹名称
folderName=os.path.basename(os.getcwd())
print(f"正在处理“{folderName}”目录下的剪映草稿...")

data=json.load(open("file_counter.json"))
contentText=""
with open("draft_content.json","r") as f:
    contentText=f.read()

with open("draft_content.json","w") as f:
    f.write(replace_text(contentText,data))

with open("draft_meta_info.json","r") as f:
    contentText=f.read()

with open("draft_meta_info.json","w") as f:
    f.write(replace_text(contentText,data))

newDraftsPath=os.path.join(inputPath,folderName)
os.makedirs(newDraftsPath,exist_ok=True)

shutil.copyfile("draft_content.json",os.path.join(newDraftsPath,"draft_content.json"))
shutil.copyfile("draft_meta_info.json",os.path.join(newDraftsPath,"draft_meta_info.json"))"""

importBat='''python importDraft.py
pause
'''
class JySaveOutDraft:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medias": ("MEIDA_GROUP", ),
                "draft_name": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "width": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "height": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "audios": ("AUDIO_GROUP", ),
                "effects": ("EFFECT_GROUP", ),
                "captions": ("CAPTIONS_GROUP", ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "剪映节点"

    def save_draft(self,medias,draft_name,width,height,audios=None,effects=None,captions=None):
        draft = Draft(draft_name,width,height)
        mediaList = [m for m in medias]
        if audios:
            mediaList.extend([a for a in audios])
        for m in mediaList:
            draft.add_media(**m)
        
        if effects:
            for e in effects:
                draft.add_effect(**e)
        
        if captions:
            for c in captions:
                draft.add_subtitle(**c)

        draft.save()
        
        timeSize=draft.calc_draft_duration()
        return (timeSize/1000000,)

importStr=r"""import json
import os
import shutil

def replace_text(contentText, data):
    for i in data:
        primary=i["primary"]
        newfile=i["newfile"]
        #获取newfile的绝对路径
        newfile=os.path.abspath(newfile)
        #替换
        contentText.replace(primary,newfile)
    return contentText

inputPath=input("请输入剪映草稿目录:")
if not inputPath:
    inputPath=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft/"
#当前目录文件夹名称
folderName=os.path.basename(os.getcwd())
print(f"正在处理“{folderName}”目录下的剪映草稿...")

data=json.load(open("file_counter.json"))
contentText=""
with open("draft_content.json","r") as f:
    contentText=f.read()

with open("draft_content.json","w") as f:
    f.write(replace_text(contentText,data))

with open("draft_meta_info.json","r") as f:
    contentText=f.read()

with open("draft_meta_info.json","w") as f:
    f.write(replace_text(contentText,data))

newDraftsPath=os.path.join(inputPath,folderName)
os.makedirs(newDraftsPath,exist_ok=True)

shutil.copyfile("draft_content.json",os.path.join(newDraftsPath,"draft_content.json"))
shutil.copyfile("draft_meta_info.json",os.path.join(newDraftsPath,"draft_meta_info.json"))"""

importBat='''python importDraft.py
pause
'''
class JySaveOutDraft:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medias": ("MEIDA_GROUP", ),
                "draft_name": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "width": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "height": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "audios": ("AUDIO_GROUP", ),
                "effects": ("EFFECT_GROUP", ),
                "captions": ("CAPTIONS_GROUP", ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("草稿时长",)
    FUNCTION = "save_draft"
    
    OUTPUT_NODE = True
    CATEGORY = "剪映节点"

    def save_draft(self,medias,draft_name,width,height,audios=None,effects=None,captions=None):
        draft = Draft(draft_name,width,height,draft_root=self.output_dir)
        mediaList = [m for m in medias]
        if audios:
            mediaList.extend([a for a in audios])

        fileList=[]
        fileCounter=[]
        for m in mediaList:
            draft.add_media(**m)
            fileList.append(m['media_file_full_name'])
        
        if effects:
            for e in effects:
                draft.add_effect(**e)
        
        if captions:
            for c in captions:
                draft.add_subtitle(**c)
        draft.save()
        folder_to_zip=os.path.join(self.output_dir, draft_name)
        filePath=os.path.join(folder_to_zip, "files")
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        
        for file in fileList:
            #复制文件到当前目录
            newFile=os.path.join(filePath, os.path.basename(file))
            if os.path.exists(newFile):
                newFile=os.path.join(filePath, os.path.splitext(os.path.basename(file))[0]+"_"+str(uuid.uuid4())+os.path.splitext(file)[1])
            shutil.copy(file, newFile)

            fileCounter.append({"primary":file, "newfile":"files/"+os.path.basename(newFile)})
        
        with open(os.path.join(folder_to_zip, "file_counter.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(fileCounter))

        with open(os.path.join(folder_to_zip, "importDraft.py"), "w", encoding="utf-8") as f:
            f.write(importStr)

        with open(os.path.join(folder_to_zip, "导入草稿.bat"), "w", encoding="utf-8") as f:
            f.write(importBat)

        zip_filename=os.path.join(self.output_dir, draft_name+".zip")
        # 创建一个ZipFile对象
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # os.walk遍历文件夹中的所有文件和子文件夹
            for foldername, subfolders, filenames in os.walk(folder_to_zip):
                for filename in filenames:
                    # 构建完整的文件路径并添加到压缩包中，注意路径的处理以正确反映目录结构
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, folder_to_zip)  # 使用相对路径以保持目录结构
                    zipf.write(file_path, arcname=arcname)
        #删除临时文件夹
        shutil.rmtree(folder_to_zip)
        timeSize=draft.calc_draft_duration()
        results=[]
        results.append({
            "filename": draft_name+".zip",
            "subfolder": '',
            "type": self.type
        })
        return {"ui": {"down": results}, "result": (timeSize/1000000,)} 

NODE_CLASS_MAPPINGS = {
    "JyMediaAnimation": JyMediaAnimation,
    "JyMediaNative":JyMediaNative,
    "JyAudioNative":JyAudioNative,
    "JyCaptionsNative":JyCaptionsNative,
    "JyEffectNative":JyEffectNative,
    "JyTransition":JyTransition,
    "JyAnimationIn":JyAnimationIn,
    "JyAnimationGroup":JyAnimationGroup,
    "JyAnimationOut":JyAnimationOut,
    "JyMultiMediaGroup":JyMultiMediaGroup,
    "JyMultiAudioGroup":JyMultiAudioGroup,
    "JyMultiCaptionsGroup":JyMultiCaptionsGroup,
    "JyMultiEffectGroup":JyMultiEffectGroup,
    "JyAudio2CaptionsGroup":JyAudio2CaptionsGroup,
    "JySaveDraft":JySaveDraft,
    "JySaveOutDraft":JySaveOutDraft,
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
