# 文件名: Glossary_Forge.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import sys

def install_and_import_pandas():
    """检查并安装pandas和openpyxl库"""
    try:
        import pandas as pd
        # 检查openpyxl，因为pandas写xlsx需要它
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
    """从config.json加载GAME_DIRECTORY"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if not os.path.exists(config_path):
        print(f"✘ 错误：找不到配置文件 '{config_path}'！")
        print("  请先运行主脚本 Scorpio_Weaver.py 生成配置文件，或确保它们在同一目录下。")
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        game_dir = config.get("GAME_DIRECTORY")
        if not game_dir or '你的游戏路径' in game_dir or not os.path.isdir(game_dir):
            print(f"✘ 错误：config.json 中的 GAME_DIRECTORY 无效！")
            return None
        return game_dir
    except Exception as e:
        print(f"✘ 读取配置文件时出错: {e}")
        return None

def main():
    """主程序入口"""
    pd = install_and_import_pandas()
    if not pd:
        input("\n按回车键退出...")
        return

    GAME_DIRECTORY = load_game_directory_from_config()
    if not GAME_DIRECTORY:
        input("\n按回车键退出...")
        return

    print("\n" + "="*60)
    print("  术语表铸造机 - 灵魂熔炉已启动  ")
    print("="*60)
    print(f"扫描路径: {GAME_DIRECTORY}")

    character_pattern = re.compile(r'define\s+\w+\s*=\s*Character\s*\(\s*_\(\s*"([^"]+)"\s*\)\s*\)')
    characters = set()

    for root, _, files in os.walk(GAME_DIRECTORY):
        for file in files:
            if file.endswith('.rpy'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        found = character_pattern.findall(content)
                        for char_name in found:
                            characters.add(char_name)
                except Exception as e:
                    print(f"  - 处理文件 {file} 时出错: {e}")

    if not characters:
        print("\n未找到任何已标记的角色定义 (e.g., define e = Character(_(\"Eileen\"))).")
        print("请确保主脚本已成功运行，或文件中存在此类定义。")
        input("\n按回车键退出...")
        return

    sorted_characters = sorted(list(characters))
    df = pd.DataFrame({
        'src': sorted_characters,
        'dst': [''] * len(sorted_characters),
        'desc': ['character'] * len(sorted_characters)
    })

    output_filename = 'glossary.xlsx'
    df.to_excel(output_filename, index=False)

    print("\n" + "-"*60)
    print(f"✔ 提取完成！共找到 {len(sorted_characters)} 个角色名。")
    print(f"✔ 术语表已保存为 '{output_filename}'。")
    print("="*60)
    input("\n按回车键退出...")

if __name__ == '__main__':
    main()
