import importlib.util
import glob
import os
import sys
from .JYNodes import init, get_ext_dir
import time
from server import PromptServer

repo_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, repo_dir)
original_modules = sys.modules.copy()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if init():
    print("Loading ComfyUI-JYNodes (剪映节点)")
    py = get_ext_dir("py")
    files = os.listdir(py)
    for file in files:
        if not file.endswith(".py"):
            continue
        name = os.path.splitext(file)[0]
        try:
            imported_module = importlib.import_module(".py.{}".format(name), __name__)
            NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
            NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}
        except Exception as e:
            print("节点：'"+name+"'导入异常",e)

WEB_DIRECTORY = "./js" 

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS","WEB_DIRECTORY"]
