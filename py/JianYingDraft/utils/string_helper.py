"""
StringHelper 替代模块，替换 BasicLibrary.data.stringHelper
"""

class StringHelper:
    
    @staticmethod
    def upper_first_char(text: str) -> str:
        """将字符串首字母大写"""
        if not text:
            return text
        return text[0].upper() + text[1:] if text else text