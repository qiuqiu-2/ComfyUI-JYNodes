import os
import json

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {
                "jianYing": {
                    "drafts_root": os.path.join(os.path.expanduser("~"), "JianyingPro Drafts"),
                    "image_duration": 3000000  # 3秒，单位微秒
                }
            }
        return cls._instance
    
    @property
    def jianYing(self):
        return self._config["jianYing"]