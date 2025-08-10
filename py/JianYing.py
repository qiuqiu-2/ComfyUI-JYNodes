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
    """
    剪映带动画的媒体
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "媒体路径": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "视频开始时间（秒）"}),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "在草稿的第几秒开始（为0时默认拼接在上一个素材的末尾）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "媒体组":("媒体组",),
                "入场动画":("入场动画",),
                "动画组":("动画组",),
                "出场动画":("出场动画",),
            }
        }

    RETURN_TYPES = ("媒体","媒体组",)
    RETURN_NAMES = ("带动画的媒体","媒体组",)

    OUTPUT_NODE = False     #是否为输出节点

    FUNCTION = "animation_video"

    CATEGORY = "剪映节点"

    def animation_video(self, file_path, start_in_media, start_at_track, duration,meida_group=[], animation_in:AnimationData=None, animation_group:AnimationData=None, animation_out:AnimationData=None):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        animation_datas: list[AnimationData] = []
        if animation_in:
            animation_datas.append(animation_in)
        if animation_group:
            animation_datas.append(animation_group)
        if animation_out:
            animation_datas.append(animation_out)
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000), "animation_datas": animation_datas}
        meida_group.append(meida)
        return (meida,meida_group,)

class JyMediaNative:
    """
    剪映添加媒体
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "媒体路径": ("STRING",{"default": "","tooltip": "图片/视频地址"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "视频开始时间（秒）"}),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "在草稿的第几秒开始（为0时默认拼接在上一个素材的末尾）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "媒体组":("媒体组",)
            }
        }

    RETURN_TYPES = ("媒体","媒体组",)
    RETURN_NAMES = ("媒体","媒体组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_media"

    CATEGORY = "剪映节点"

    def jy_media(self, file_path, start_in_media, start_at_track, duration,meida_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        meida_group=[*meida_group]
        meida={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        meida_group.append(meida)
        return (meida,meida_group,)

class JyAudioNative:
    """
    剪映添加音频
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "音频路径": ("STRING",{"default": "","tooltip": "音频地址"}),
                "开始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "音频开始时间（秒）"}),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "在草稿的第几秒开始（为0时默认拼接在上一个素材的末尾）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "音频组":("音频组",)
            }
        }

    RETURN_TYPES = ("音频","音频组",)
    RETURN_NAMES = ("音频","音频组",)

    OUTPUT_NODE = False
    FUNCTION = "jy_audio"

    CATEGORY = "剪映节点"

    def jy_audio(self, file_path, start_in_media, start_at_track, duration,audio_group=[]):
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        audio_group=[*audio_group]
        audio={"media_file_full_name": file_path, "start_in_media": int(start_in_media*1000000), "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        audio_group.append(audio)
        return (audio,audio_group,)

class JyCaptionsNative:
    """
    剪映添加字幕
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "字幕内容": ("STRING",{"default": "","multiline": True,"tooltip": "字幕内容"}),
                "字体颜色": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "字体大小": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "水平位置x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "垂直位置y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
                "起始时间": ("FLOAT", {"default": 1.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "在草稿的第几秒开始（为0时默认拼接在上一个素材的末尾）"}),
                "持续时间": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "字幕组":("字幕组",)
            }
        }

    RETURN_TYPES = ("字幕","字幕组",)
    RETURN_NAMES = ("字幕","字幕组",)

    OUTPUT_NODE = False
    FUNCTION = "jy_captions"

    CATEGORY = "剪映节点"

    def jy_captions(self, text, color,size,transform_x,transform_y, start_at_track, duration,captions_group=[]):
        captions_group=[*captions_group]
        captions={"subtitle": text,"color":color,"size":size, "start_at_track": int(start_at_track*1000000), "duration": int(duration*1000000)}
        captions['clip_settings']=Clip_settings(transform_y=transform_y,transform_x=transform_x)
        captions_group.append(captions)
        return (captions,captions_group,)

class JyEffectNative:
    """
    剪映添加特效
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "特效": (list(effectDict.keys()),),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "在草稿的第几秒开始（为0时默认拼接在上一个素材的末尾）"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            },
            "optional": {
                "特效组":("特效组",)
            }
        }

    RETURN_TYPES = ("特效","特效组",)
    RETURN_NAMES = ("特效","特效组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_effect"

    CATEGORY = "剪映节点"

    def jy_effect(self, effect, start_at_track, duration,effect_group=[]):
        #拷贝一份
        effect_group=[*effect_group]
        effect={"effect_name_or_resource_id": effect, "start": int(start_at_track*1000000), "duration": int(duration*1000000)}
        effect_group.append(effect)
        return (effect,effect_group,)


class JyTransition:
    """
    剪映添加转场
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "转场": (list(transitionDict.keys()),),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
                "媒体输出":("媒体",),
            },
            "optional": {
                "媒体输入":("媒体",),
                "媒体组":("媒体组",)
            }
        }

    RETURN_TYPES = ("转场","媒体组",)
    RETURN_NAMES = ("转场","媒体组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_transition"

    CATEGORY = "剪映节点"

    def jy_transition(self, transition, duration,meida_out,meida_in=None,meida_group=[]):
        meida_group=[*meida_group]
        #添加转场
        transition_data: TransitionData = tools.generate_transition_data(
            name_or_resource_id=transition,  # 转场名称（可以是内置的转场名称，也可以是剪映本身的转场资源id）
            duration=int(duration*1000000),  # 转场持续时间 
        )
        meida_out['transition_data']=transition_data
        meida_group.append(meida_out)
        transition=[meida_out]
        if meida_in:
            meida_group.append(meida_in)
            transition.append(meida_in)
        return (transition,meida_group,)
    
class JyAnimationIn:
    """
    剪映入场动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "入场动画": (list(animationInDict.keys()),),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "入场动画的起始时间永远为0（即便设置了其他起始时间，也会被忽略）(秒)"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("入场动画",)
    RETURN_NAMES = ("入场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_in"

    CATEGORY = "剪映节点"

    def jy_animation_in(self, animation, start, duration):
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 入场动画的起始时间永远为0（即便设置了其他起始时间，也会被忽略）。（这是一个相对素材片段的时间，不是时间轴上的绝对时间）
            duration=int(duration*1000000),  # 动画持续时间
            animation_type="in",  # 动画类型
        ),)

class JyAnimationGroup:
    """
    剪映动画组
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "动画": (list(animationGroupDict.keys()),),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "动画开始时间(秒)"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("动画组",)
    RETURN_NAMES = ("动画组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_group"

    CATEGORY = "剪映节点"

    def jy_animation_group(self, animation, start, duration):
        animation_type="组",  # 动画类型
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 动画开始时间
            duration=int(duration*1000000), # 动画持续时间
            animation_type="group",  # 动画类型
        ),)
    
class JyAnimationOut:
    """
    剪映出场动画
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "出场动画": (list(animationOutDict.keys()),),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "出场动画的起始时间永远为0（具体的时间会根据素材片段的长度自动计算)(秒)"}),
                "持续时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 9999999, "step": 0.01,"tooltip": "持续时间（秒）"}),
            }
        }

    RETURN_TYPES = ("出场动画",)
    RETURN_NAMES = ("出场动画",)
    OUTPUT_NODE = False
    FUNCTION = "jy_animation_out"

    CATEGORY = "剪映节点"

    def jy_animation_out(self, animation, start, duration):
        return (tools.generate_animation_data(
            name_or_resource_id=animation,  # 动画名称（可以是内置的动画名称，也可以是剪映本身的动画资源id）
            start=int(start*1000000),  # 出场动画的起始时间永远为0（具体的时间会根据素材片段的长度自动计算）。（这是一个相对素材片段的时间，不是时间轴上的绝对时间）
            duration=int(duration*1000000),  # 动画持续时间
            animation_type="out",  # 动画类型
        ),)
    

class JyMultiMediaGroup:
    """
    剪映媒体组
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "媒体1": ("媒体,ANIMATION_MEIDA,转场", ),
            },
            "optional": {
                "媒体2": ("媒体,ANIMATION_MEIDA,转场", ),
            }
        }

    RETURN_TYPES = ("媒体组",)
    FUNCTION = "media_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def media_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('meida'):
                if type(kwargs[arg]) == list:
                    mediaList.extend(kwargs[arg])
                else:
                    mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiAudioGroup:
    """
    剪映音频组
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "音频1": ("音频", ),
            },
            "optional": {
                "音频2": ("音频", ),
            }
        }

    RETURN_TYPES = ("音频组",)
    FUNCTION = "audio_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def audio_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('audio'):
                mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiCaptionsGroup:
    """
    剪映字幕组
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "字幕1": ("字幕", ),
            },
            "optional": {
                "字幕2": ("字幕", ),
            }
        }

    RETURN_TYPES = ("字幕组",)
    FUNCTION = "captions_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def captions_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('captions'):
                mediaList.append(kwargs[arg])

        return (mediaList, )
    
class JyMultiEffectGroup:
    """
    剪映特效组
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "特效1": ("特效", ),
            },
            "optional": {
                "特效2": ("特效", ),
            }
        }

    RETURN_TYPES = ("特效组",)
    FUNCTION = "effect_group"
    OUTPUT_NODE = False
    CATEGORY = "剪映节点"

    def effect_group(self, **kwargs):
       
        mediaList=[]
        for arg in kwargs:
            if arg.startswith('effect'):
                mediaList.append(kwargs[arg])

        return (mediaList, )

class JyAudio2CaptionsGroup:
    """
    剪映音频转字幕
    """
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "模型":(["tiny","base","small","medium","large-v1","large-v2","large-v3"],{"default": "medium"}),
                "音频文件路径": ("STRING",{"default": "","tooltip": "音频地址"}),
                "起始时间": ("FLOAT", {"default": 0.0, "min": 0.0, "max":9999999, "step": 0.01,"tooltip": "字幕起始时间（秒）"}),
                "颜色": ("STRING",{"default": "#FFFFFF","tooltip": "字幕颜色"}),
                "大小": ("FLOAT", {"default": 8.0, "min": 0.0, "max":300, "step": 1.0,"tooltip": "字幕大小"}),
                "水平位置x": ("FLOAT", {"default": 0.0, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "水平位移, 单位为半个画布宽"}),
                "垂直位置y": ("FLOAT", {"default": -0.8, "min": -1.0, "max":1.0, "step": 0.1,"tooltip": "垂直位移, 单位为半个画布高"}),
            },
            "optional": {
                "字幕组":("字幕组",)
            }
        }

    RETURN_TYPES = ("字幕组",)
    RETURN_NAMES = ("字幕组",)
    OUTPUT_NODE = False
    FUNCTION = "jy_audio2captions_group"

    CATEGORY = "剪映节点"

    def jy_audio2captions_group(self,model, file_path,start_at_track,color,size,transform_x,transform_y,captions_group=[]):
        import whisper
        if not os.path.exists(file_path):
            raise Exception('对应文件不存在')
        model = whisper.load_model(model)
        result = model.transcribe(file_path)
        segments = result["segments"]
        captions_group=[*captions_group]
        for i in range(len(segments)):
            text = segments[i]["text"]
            start=start_at_track+segments[i]["start"]
            end=segments[i]["end"]
            duration=end-start
            captions={"subtitle": text,"color":color,"size":size, "start_at_track": int(start*1000000), "duration": int(duration*1000000)}
            captions['clip_settings']=Clip_settings(transform_y=transform_y,transform_x=transform_x)
            captions_group.append(captions)
        return (captions_group,)

class JySaveDraft:
    """
    剪映保存草稿
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "媒体组": ("媒体组", ),
                "草稿名": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "宽": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "高": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "音频组": ("音频组", ),
                "特效组": ("特效组", ),
                "字幕组": ("字幕组", ),
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
    """
    剪映草稿下载
    """
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "媒体组": ("媒体组", ),
                "草稿名": ("STRING", {"default": "Draft", "tooltip": "保存的草稿名称"}),
                "宽": ("INT", {"default": 1920, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿宽"}),
                "高": ("INT", {"default": 1080, "min": 1, "max": 9999999, "step": 1, "tooltip": "草稿高"}),
            },
            "optional": {
                "音频组": ("音频组", ),
                "特效组": ("特效组", ),
                "字幕组": ("字幕组", ),
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
    "JyMediaAnimation":JyMediaAnimation,
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
    "JyMediaAnimation": "剪映带动画的媒体",
    "JyMediaNative": "剪映添加媒体",
    "JyAudioNative": "剪映添加音频",
    "JyCaptionsNative": "剪映添加字幕",
    "JyEffectNative": "剪映添加特效",
    "JyTransition": "剪映添加转场",
    "JyAnimationIn": "剪映入场动画",
    "JyAnimationGroup": "剪映动画组",
    "JyAnimationOut": "剪映出场动画",
    "JyMultiMediaGroup": "剪映媒体组",
    "JyMultiAudioGroup": "剪映音频组",
    "JyMultiCaptionsGroup": "剪映字幕组",
    "JyMultiEffectGroup": "剪映特效组",
    "JyAudio2CaptionsGroup": "剪映音频转字幕",
    "JySaveDraft": "剪映保存草稿",
    "JySaveOutDraft": "剪映草稿下载",
}
