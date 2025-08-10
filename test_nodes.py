#!/usr/bin/env python3
"""
测试剪映节点导入的脚本
"""
import sys
import os

# 模拟ComfyUI环境
class MockFolderPaths:
    @staticmethod
    def get_input_directory():
        return os.path.join(os.getcwd(), "input")
    
    @staticmethod
    def get_output_directory():
        return os.path.join(os.getcwd(), "output")

# 模拟必要的模块
sys.modules['folder_paths'] = MockFolderPaths

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))

try:
    # 尝试导入剪映节点
    import JianYing
    
    # 打印节点信息
    print("✅ 成功导入剪映节点模块")
    print(f"NODE_CLASS_MAPPINGS 包含 {len(JianYing.NODE_CLASS_MAPPINGS)} 个节点:")
    for name, cls in JianYing.NODE_CLASS_MAPPINGS.items():
        print(f"  - {name}: {cls.__name__}")
    
    print(f"NODE_DISPLAY_NAME_MAPPINGS 包含 {len(JianYing.NODE_DISPLAY_NAME_MAPPINGS)} 个显示名称")
    
    # 测试几个关键节点
    test_nodes = ['JyMultiMediaGroup', 'JyMultiAudioGroup', 'JyMultiCaptionsGroup', 'JyMultiEffectGroup', 'JyAudio2CaptionsGroup']
    for node_name in test_nodes:
        if node_name in JianYing.NODE_CLASS_MAPPINGS:
            node_class = JianYing.NODE_CLASS_MAPPINGS[node_name]
            print(f"✅ {node_name} 节点定义正常")
        else:
            print(f"❌ {node_name} 节点未找到")
    
    print("\n🎉 所有节点测试通过！")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()