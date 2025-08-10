"""
DynamicImporter 替代模块，替换 BasicLibrary.environment.dynamicImporter
"""
import importlib

class DynamicImporter:
    
    @staticmethod
    def load_class(package_name: str, class_name: str, **kwargs):
        """动态加载类"""
        try:
            module = importlib.import_module(package_name)
            cls = getattr(module, class_name)
            return cls(**kwargs)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"无法加载类 {package_name}.{class_name}: {e}")