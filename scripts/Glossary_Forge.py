# 文件名: Glossary_Forge.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#  术语表铸造熔炉 v2.4 - 究极飞升版
#  功能：
#    1. 混合动力模式：可独立运行，也可与主工具集联动。
#    2. 究极兼容搜索：兼容 Character/DynamicCharacter、单/双引号、
#       带附加参数的定义，并能智能排除变量名。
#    3. 全文件扫描：同时扫描 .rpy 和 .new.rpy 文件。
# ==============================================================================
import os
import re
import json
import sys
import subprocess

# ===== 配置区 (手动挡模式) =====
# 当无法从 config.json 获取有效路径时，将使用此处的配置
GAME_DIRECTORY_FALLBACK = r'G:\你的游戏路径\game' # <--- 在这里填写备用游戏路径
OUTPUT_EXCEL_FILE = 'glossary.xlsx'

def install_and_import_pandas():
    """检查并安装pandas和openpyxl库"""
    try:
        import pandas as pd
        try:
            import openpyxl
        except ImportError:
            print("检测到缺少 'openpyxl' 库，正在自动安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        return pd
    except ImportError:
        print("检测到缺少 'pandas' 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
            import pandas as pd
            return pd
        except Exception as e:
            print(f"✘ 自动安装失败: {e}")
            return None

def load_game_directory_from_config():
    """尝试从config.json加载GAME_DIRECTORY，失败则返回None"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        game_dir = config.get("GAME_DIRECTORY")
        if game_dir and '你的游戏路径' not in game_dir and os.path.isdir(game_dir):
            return game_dir
        return None
    except Exception:
        return None

def main():
    """主程序入口"""
    pd = install_and_import_pandas()
    if not pd:
        input("\n缺少核心组件，无法继续。按Enter键退出...")
        return

    print("\n" + "="*60)
    print("  术语表铸造机 v2.4 - 究极飞升版  ")
    print("="*60)

    game_directory = load_game_directory_from_config()
    if game_directory:
        print(f"ℹ️ 已从 config.json 加载路径 (自动挡模式)")
    else:
        print(f"⚠️ 未从 config.json 加载到有效路径，切换至脚本内配置 (手动挡模式)")
        game_directory = GAME_DIRECTORY_FALLBACK
        if '你的游戏路径' in game_directory or not os.path.isdir(game_directory):
            print(f"✘ 错误：脚本内配置的备用路径无效！")
            print(f"  请打开 {__file__} 并修改 GAME_DIRECTORY_FALLBACK 的值。")
            input("\n按Enter键退出...")
            return

    print(f"扫描路径: {game_directory}")

    # 【核心升级】究极飞升版正则表达式
    # 匹配 (Dynamic)Character, 兼容单/双引号, 排除变量[...], 排除name=None
    # 解释:
    # (?:DynamicCharacter|Character) - 匹配 "DynamicCharacter" 或 "Character"
    # \s*\(\s* - 匹配左括号和任意空格
    # (?:_\(\s*)? - 可选地匹配 _( 和空格 (用于已处理的)
    # (["']) - 捕获开始的引号 (单引号或双引号)
    # ((?:(?!\1).)*?) - 捕获引号内的所有内容，直到遇到与之匹配的结束引号
    # \1 - 匹配之前捕获的同类型引号
    # (?!\s*\[) - 负向前瞻，确保捕获的内容不是以 [ 开头的变量
    # (?!\s*None) - 负向前瞻，确保捕获的内容不是 None
    pattern = re.compile(r'(?:DynamicCharacter|Character)\s*\(\s*(?:_\(\s*)?(["\'])((?:(?!\1).)*?)\1(?!\s*\[)(?!\s*None)')
    
    found_names = set()

    print("正在扫描 .rpy 和 .new.rpy 文件并提取角色名...")
    for root, _, files in os.walk(game_directory):
        for file in files:
            if file.endswith(('.rpy', '.new.rpy')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = pattern.findall(content)
                        for match in matches:
                            # match 是一个元组，例如 ('"', 'Eileen')，我们需要第二个元素
                            name = match[1]
                            # 再次确认不是变量
                            if not (name.startswith('[') and name.endswith(']')):
                                found_names.add(name)
                except Exception as e:
                    print(f"  ! 读取文件 {file} 时出错: {e}")

    if not found_names:
        print("\n未找到任何符合条件的角色名。")
        input("\n按Enter键退出...")
        return
        
    sorted_characters = sorted(list(found_names))
    
    df = pd.DataFrame({
        'src': sorted_characters,
        'dst': [''] * len(sorted_characters),
        'desc': ['character'] * len(sorted_characters)
    })

    try:
        df.to_excel(OUTPUT_EXCEL_FILE, index=False)
        print("\n" + "-"*60)
        print(f"✔ 提取完成！共找到 {len(sorted_characters)} 个独特的角色名。")
        print(f"✔ 术语表已保存为 '{OUTPUT_EXCEL_FILE}'。")
        print("="*60)
    except Exception as e:
        print(f"\n✘ 生成Excel文件时出错: {e}")

    input("\n所有任务已结束，按Enter键退出...")

if __name__ == '__main__':
    main()
