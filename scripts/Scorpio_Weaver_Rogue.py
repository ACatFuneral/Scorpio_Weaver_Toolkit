#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#  Scorpio Weaver Toolkit - Rogue Edition v2.6 (Readable Soul Edition)
#  作者：猫之送葬者 & Gemini
#  设计哲学：基于猫之送葬者的“人机结合，天下无敌”理念。
#  此版本为极速、零成本的正则自动化版，仅处理绝对安全的文本模式。
#  高风险文本请使用README中描述的手动正则模式，以实现完美的人机协同。
# ==============================================================================
import os
import sys
import json
import re
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
import msvcrt  # Windows下的键盘输入检测

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# --- 精密正则引擎核心 v2.5 ---
SAFE_REGEX_PATTERNS = [
    ("Character定义", re.compile(r'(Character\s*\(\s*)(?!_\()("[^"]*")((?:,.*?)?\s*\))')),
    ("renpy.input提示", re.compile(r'(renpy\.input\s*\(\s*)(?!_\()(".*?")((?:,.*?)?\s*\))')),
    ("show/text语句", re.compile(r'((?:show\s+)?text\s+)(?!_)(".*?")(\s*$)'))
]

def process_file_with_regex(original_code):
    """使用预定义的安全正则表达式列表来处理代码。"""
    modified_code = original_code
    total_changes = 0
    for desc, pattern in SAFE_REGEX_PATTERNS:
        modified_code, changes = pattern.subn(r'\1_(\2)\3', modified_code)
        total_changes += changes
    return modified_code, total_changes
# --- 正则引擎结束 ---

# --- 游侠版专属配置系统 ---
def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_rogue.json')
    default_config = {
        "GAME_DIRECTORY": "G:\\你的游戏路径\\game",
        "OVERWRITE_FILES": False,
        "EXCLUDE_FILES": ["gui.rpy", "options.rpy", "screens.rpy"],
        "CONCURRENT_LIMIT": max(1, os.cpu_count() or 1)
    }
    if not os.path.exists(config_path):
        logger.info(f"🔎 未找到游侠版配置文件，正在创建默认的 '{config_path}'...")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✔ '{config_path}' 创建成功！请打开它，填写你的游戏目录后，再重新运行脚本。")
        input("\n按回车键退出...")
        sys.exit(0)
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            config = default_config.copy()
            config.update(user_config)
            return config
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"✘ 配置文件 '{config_path}' 格式错误或缺少必要的键: {e}")
        logger.error("  请检查文件内容是否为有效的JSON，或者直接删除它让程序重新生成一个标准的。")
        input("\n按回车键退出...")
        sys.exit(1)

def config_wizard():
    print("\n" + "🧙"*30 + " 欢迎使用 Scorpio Weaver [游侠版] 配置向导 " + "🧙"*30)
    config = {}
    print("\n📁 游戏目录配置")
    while True:
        game_dir = input("请输入游戏目录的完整路径 (例如 G:\\MyGame\\game): ").strip().replace('"', '')
        if os.path.isdir(game_dir):
            config['GAME_DIRECTORY'] = game_dir
            break
        else:
            print("❌ 目录不存在，请重新输入")
    
    print("\n⚡ 性能配置")
    default_cpu = max(1, os.cpu_count() or 1)
    while True:
        try:
            concurrent_str = input(f"请输入并发处理数量 (建议1-{default_cpu*2}，默认为{default_cpu}): ")
            concurrent = int(concurrent_str) if concurrent_str else default_cpu
            if concurrent > 0:
                config['CONCURRENT_LIMIT'] = concurrent
                break
            else:
                print("❌ 请输入大于0的数字")
        except ValueError:
            print("❌ 请输入有效数字")

    print("\n🛡️ 安全模式")
    config['OVERWRITE_FILES'] = input("是否直接覆盖原文件？(y/N，默认为否): ").lower().startswith('y')
    config['EXCLUDE_FILES'] = ["gui.rpy", "options.rpy", "screens.rpy"]
    config_path = os.path.join(os.path.dirname(__file__), 'config_rogue.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 配置已保存到: {config_path}\n🎉 配置完成！现在可以运行主程序了。\n")
    return config

# --- 全局控制事件 ---
PAUSE_EVENT = threading.Event()
PAUSE_EVENT.set()
STOP_EVENT = threading.Event()

# --- 核心模块 ---
def install_and_import_tqdm():
    try:
        import tqdm
        return tqdm
    except ImportError:
        logger.info("...检测到缺少 'tqdm' 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
            import tqdm
            logger.info("✔ 'tqdm' 安装成功！")
            return tqdm
        except Exception as e:
            logger.error(f"✘ 'tqdm' 自动安装失败: {e}\n请手动运行 'pip install tqdm'。")
            return None

tqdm_module = install_and_import_tqdm()

def validate_config(config):
    errors = []
    if '你的游戏路径' in config.get('GAME_DIRECTORY', ''):
        errors.append("📁 GAME_DIRECTORY 路径无效，请在 config_rogue.json 中设置正确的游戏目录路径。")
    elif not os.path.isdir(config.get('GAME_DIRECTORY', '')):
        errors.append(f"📁 GAME_DIRECTORY 路径 '{config.get('GAME_DIRECTORY')}' 不存在或不是一个有效目录。")
    if errors:
        logger.error("\n" + "❌"*30 + " 配置检查失败 " + "❌"*30)
        for error in errors:
            logger.error(f"  - {error}")
        logger.error("\n  💡 提示：你可以直接删除 config_rogue.json 文件，")
        logger.error("     或者使用 --wizard 参数来启动配置向导，重新生成一份正确的配置。")
        logger.error("❌"*70)
        input("\n按回车键退出...")
        sys.exit(1)

# 【可读性终极修复】恢复了 TimeStats 类的标准写法
class TimeStats:
    def __init__(self):
        self.start_time = None
        self.pause_start = None
        self.total_pause_time = 0
        self.completed_files = 0
        self.lock = threading.Lock()

    def start(self):
        self.start_time = time.time()

    def pause(self):
        if not self.pause_start:
            self.pause_start = time.time()

    def resume(self):
        if self.pause_start:
            self.total_pause_time += time.time() - self.pause_start
            self.pause_start = None

    def get_elapsed_time(self):
        if not self.start_time:
            return 0
        current = time.time()
        if self.pause_start:
            return self.pause_start - self.start_time - self.total_pause_time
        return current - self.start_time - self.total_pause_time

    def get_speed(self):
        elapsed = self.get_elapsed_time()
        if elapsed > 0 and self.completed_files > 0:
            return self.completed_files / elapsed
        return 0

    def file_completed(self):
        with self.lock:
            self.completed_files += 1
time_stats = TimeStats()

# 【可读性终极修复】恢复了 keyboard_listener 的标准 if/else 写法
def keyboard_listener(pbar):
    print("\n⌨️  控制说明: 按 [P]暂停/恢复, [S]停止, [I]查看信息")
    while not STOP_EVENT.is_set():
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'p':
                    if PAUSE_EVENT.is_set():
                        PAUSE_EVENT.clear()
                        time_stats.pause()
                        pbar.write("⏸️  已暂停 - 按 [P] 恢复")
                        pbar.set_description("⏸️  已暂停...")
                    else:
                        PAUSE_EVENT.set()
                        time_stats.resume()
                        pbar.write("▶️  已恢复")
                elif key == 's':
                    STOP_EVENT.set()
                    PAUSE_EVENT.set()
                    pbar.write("🛑 用户请求停止...")
                    break
                elif key == 'i':
                    pbar.write(f"📊 实时统计: ⏱️ {time_stats.get_elapsed_time():.1f}s | 📁 {time_stats.completed_files}/{pbar.total} | 🚀 {time_stats.get_speed():.1f} f/s")
            time.sleep(0.1)
        except:
            continue

def process_file(file_path, stats, pbar, lock):
    file_name = os.path.basename(file_path)
    try:
        if STOP_EVENT.is_set(): return
        PAUSE_EVENT.wait()
        if file_name in CONFIG['EXCLUDE_FILES']:
            with lock: stats['skipped_exclude'].append(file_name); return
        with open(file_path, 'r', encoding='utf-8') as f: original_code = f.read()
        if not original_code.strip():
            with lock: stats['skipped_empty'].append(file_name); return
        modified_code, changes_made = process_file_with_regex(original_code)
        if STOP_EVENT.is_set(): return
        PAUSE_EVENT.wait()
        if changes_made == 0:
            with lock: stats['skipped_nochange'].append(file_name); return
        temp_file_path = f"{file_path}.{uuid.uuid4().hex}.tmp"
        with open(temp_file_path, 'w', encoding='utf-8') as f: f.write(modified_code)
        output_path = file_path if CONFIG['OVERWRITE_FILES'] else f"{file_path}.new.rpy"
        os.replace(temp_file_path, output_path)
        with lock:
            stats['success_files'].add(file_name)
            stats['total_tags_added'] += changes_made
            pbar.write(f"✅ {file_name} (添加了 {changes_made} 个标记)")
    except Exception as e:
        pbar.write(f"💥 处理 '{file_name}' 时发生严重错误: {type(e).__name__} - {e}")
        with lock: stats['error_files'].add(file_name)
    finally:
        time_stats.file_completed()
        pbar.update(1)

def print_rogue_stats(stats, total_time):
    status = "处理完成！" if not STOP_EVENT.is_set() else "处理已停止！"
    logger.info("\n\n" + "📊"*20 + " 游侠版任务报告 " + "📊"*20)
    actual_work_time = time_stats.get_elapsed_time()
    logger.info(f"⏱️  总耗时: {total_time:.2f} 秒 (实际工作: {actual_work_time:.2f}s, 暂停: {time_stats.total_pause_time:.2f}s)")
    if actual_work_time > 0: logger.info(f"🚀 实际处理速度: {time_stats.completed_files / actual_work_time:.2f} 文件/秒")
    logger.info("-" * 60)
    logger.info(f"✅ 成功修改: {len(stats['success_files'])} 个文件")
    logger.info(f"🔖 添加标记总数: {stats['total_tags_added']} 个")
    logger.info(f"❌ 处理失败: {len(stats['error_files'])} 个文件")
    total_skipped = len(stats['skipped_exclude']) + len(stats['skipped_nochange']) + len(stats['skipped_empty'])
    logger.info(f"⏭️  跳过处理: {total_skipped} 个文件 (无需修改: {len(stats['skipped_nochange'])}, 排除: {len(stats['skipped_exclude'])}, 空文件: {len(stats['skipped_empty'])})")
    if stats['error_files']: logger.error(f"\n❌ 失败文件列表: {', '.join(sorted(list(stats['error_files'])))}")

def main():
    if '--wizard' in sys.argv: config_wizard(); return
    if not tqdm_module: return
    
    global CONFIG
    CONFIG = load_config()
    validate_config(CONFIG)

    logger.info("\n" + "⚔️ "*30 + f"\n  Scorpio Weaver - Rogue Edition v2.6  \n" + "⚔️ "*30)
    logger.info(f"🛡️  模式: 精密正则打击 (零成本，极速)")
    logger.info(f"📁 游戏路径: {CONFIG['GAME_DIRECTORY']}")
    logger.info(f"⚡ 并发数: {CONFIG['CONCURRENT_LIMIT']}")
    logger.info(f"🛡️  安全模式: {'❌ 关闭 (直接覆盖!)' if CONFIG['OVERWRITE_FILES'] else '✅ 开启 (生成.new.rpy文件)'}")
    logger.info("⚔️ "*60 + "\n")
    
    user_input = input("🔍 请确认以上配置。输入 'yes' 开始执行，或 'wizard' 重新配置: ").lower()
    if user_input == 'wizard': config_wizard(); print("\n配置已更新，请重新运行脚本以应用新配置。"); return
    if user_input != 'yes': logger.info("❌ 操作已取消。"); return

    rpy_files = [os.path.join(root, file) for root, _, files in os.walk(CONFIG['GAME_DIRECTORY']) for file in files if file.endswith('.rpy')]
    if not rpy_files: logger.warning("⚠️  在指定目录下未找到任何 .rpy 文件。"); input("按回车键退出..."); return

    stats = {'success_files': set(), 'error_files': set(), 'skipped_exclude': [], 'skipped_nochange': [], 'skipped_empty': [], 'total_tags_added': 0}
    lock = threading.Lock()
    
    logger.info(f"\n📋 扫描完成！发现 {len(rpy_files)} 个 .rpy 文件，开始处理...")
    time_stats.start(); start_time = time.time()

    with tqdm_module.tqdm(total=len(rpy_files), unit="file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]", ncols=120) as pbar:
        keyboard_thread = threading.Thread(target=keyboard_listener, args=(pbar,), daemon=True)
        keyboard_thread.start()
        
        with ThreadPoolExecutor(max_workers=CONFIG['CONCURRENT_LIMIT']) as executor:
            futures = [executor.submit(process_file, file_path, stats, pbar, lock) for file_path in rpy_files]
            for future in futures:
                try: 
                    if STOP_EVENT.is_set():
                        for f in futures: f.cancel(); break
                    future.result()
                except Exception: pass
        
        if STOP_EVENT.is_set(): pbar.write("\n🛑 处理已被用户停止")

    total_time = time.time() - start_time
    STOP_EVENT.set(); PAUSE_EVENT.set()
    print_rogue_stats(stats, total_time)
    
    logger.info("\n" + "🎯"*30)
    logger.info("✅ 游侠版任务完成！对于剩余复杂文本，请使用“手动正则决战”方法进行精准打击。")
    logger.info("   人机协同，方能所向披靡！")
    logger.info("🎯"*30)
    
    input("\n按回车键退出程序...")

if __name__ == '__main__':
    main()
