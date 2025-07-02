# 【全新神器：术语表铸造熔炉 v1.1 - 双核搜索版】
#  功能：同时扫描带_()和不带_()的Character定义。
import os
import re
import sys
import subprocess

# ==============================================================================
# ===== 配置区 (小白友好，只需修改这部分) =====
# ==============================================================================
# 1. 粘贴你的游戏 'game' 文件夹的完整路径
GAME_DIRECTORY = r'G:\你的游戏路径\game' # <--- 在这里填写你的游戏game文件夹路径

# 2. 你希望生成的Excel术语表的文件名
OUTPUT_EXCEL_FILE = 'glossary.xlsx'

# ==============================================================================
# ===== 脚本核心 (高手勿动，小白更不要动！) =====
# ==============================================================================

def install_and_import_pandas():
    """检查并安装pandas和openpyxl库。"""
    print("正在检查术语表生成所需组件...")
    try:
        import pandas as pd
        print("✓ pandas 库已安装")
        return pd
    except ImportError:
        print("检测到缺少 'pandas' 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
            import pandas as pd
            print("✓ pandas 和 openpyxl 库安装成功！")
            return pd
        except Exception as e:
            print(f"✘ 自动安装失败: {e}")
            print("  请手动在命令行运行: py -m pip install pandas openpyxl")
            return None

def main():
    """主程序入口。"""
    pd = install_and_import_pandas()
    if not pd:
        input("\n缺少核心组件，无法继续。按Enter键退出...")
        return

    print("\n" + "="*60)
    print("  术语表铸造熔炉 v1.1 - 双核搜索版")
    print("="*60)
    
    if '你的游戏路径' in GAME_DIRECTORY or not os.path.isdir(GAME_DIRECTORY):
        print("✘ 配置错误：请先打开脚本，填写正确的 GAME_DIRECTORY 路径。")
        input("\n按Enter键退出...")
        return

    print(f"扫描目标路径: {GAME_DIRECTORY}")
    
    # 【核心升级】准备两个正则表达式
    char_pattern_marked = re.compile(r'Character\s*\(\s*_\(\s*"([^"]+)"\s*\)\s*\)') # 匹配 Character(_("..."))
    char_pattern_unmarked = re.compile(r'define\s+\w+\s*=\s*Character\s*\(\s*"([^"]+)"') # 匹配 define ... = Character("...")
    
    found_names = set()

    print("正在扫描 .rpy 和 .new.rpy 文件并提取角色名...")
    for root, _, files in os.walk(GAME_DIRECTORY):
        for file in files:
            # 同时扫描两种文件
            if file.endswith('.rpy'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # 先用精确的带_()的规则匹配
                            match1 = char_pattern_marked.search(line)
                            if match1:
                                found_names.add(match1.group(1))
                                continue
                            
                            # 再用不带_()的规则匹配
                            match2 = char_pattern_unmarked.search(line)
                            if match2:
                                found_names.add(match2.group(1))

                except Exception as e:
                    print(f"  ! 读取文件时出错: {file_path} ({e})")

    if not found_names:
        print("\n未找到任何 Character 定义的角色名。")
        input("\n按Enter键退出...")
        return
        
    print(f"\n✓ 提取完成！共找到 {len(found_names)} 个独特的角色名。")
    
    df = pd.DataFrame({
        'src': sorted(list(found_names)),
        'dst': '',
        'info': '角色名',
        'regex': ''
    })

    try:
        print(f"正在生成Excel术语表: {OUTPUT_EXCEL_FILE} ...")
        df.to_excel(OUTPUT_EXCEL_FILE, index=False)
        print("\n" + "="*60)
        print(f"🎉 神功大成！术语表 '{OUTPUT_EXCEL_FILE}' 已成功生成在脚本所在目录！")
        print("="*60)
    except Exception as e:
        print(f"\n✘ 生成Excel文件时出错: {e}")

    input("\n所有任务已结束，按Enter键退出...")


if __name__ == '__main__':
    main()