#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#  自动化本地化预处理工具 v5.4 - 配置分离版
#  作者：猫之送葬者 & Gemini & DeepSeek & 老殇
#  更新日志：
#    v5.4: 实现配置与代码分离！将所有用户配置移至 config.json 文件，更新脚本不再需要重新填写配置。
#    v5.3: 新增精准模型错误诊断，采用原子化文件写入，优化日志。
# ==============================================================================
import os
import sys
import json
import requests
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from datetime import datetime
import signal
import msvcrt  # Windows下的键盘输入检测

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    default_config = {
        "API_KEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "BASE_URL": "https://api.oneapi.run/v1",
        "MODEL_NAME": "gemini-1.5-pro-latest",
        "GAME_DIRECTORY": "G:\\你的游戏路径\\game",
        "OVERWRITE_FILES": False,
        "MAX_FILE_SIZE_KB": 500,
        "EXCLUDE_FILES": ["gui.rpy", "options.rpy", "screens.rpy"],
        "MAX_RETRIES": 5,
        "TIMEOUT": 300,
        "CONCURRENT_LIMIT": 5
    }
    if not os.path.exists(config_path):
        logger.info(f"未找到配置文件，正在创建默认的 '{config_path}'...")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✔ '{config_path}' 创建成功！请打开它，填写你自己的配置后，再重新运行脚本。")
        input("\n按回车键退出...")
        sys.exit(0)
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"✘ 配置文件 '{config_path}' 格式错误或缺少必要的键: {e}")
        logger.error("  请检查文件内容是否为有效的JSON，或者直接删除它让程序重新生成一个标准的。")
        input("\n按回车键退出...")
        sys.exit(1)

# 在脚本的顶层作用域加载配置
CONFIG = load_config()

# 全局暂停控制
PAUSE_EVENT = threading.Event()
PAUSE_EVENT.set()  # 初始状态为运行
STOP_EVENT = threading.Event()  # 停止事件

# 时间统计类
class TimeStats:
    def __init__(self):
        self.start_time = None
        self.pause_start = None
        self.total_pause_time = 0
        self.file_start_times = {}
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
        current_time = time.time()
        if self.pause_start:
            return self.pause_start - self.start_time - self.total_pause_time
        return current_time - self.start_time - self.total_pause_time
    
    def get_speed(self):
        elapsed = self.get_elapsed_time()
        if elapsed > 0 and self.completed_files > 0:
            return self.completed_files / elapsed
        return 0
    
    def get_eta(self, total_files):
        speed = self.get_speed()
        if speed > 0:
            remaining_files = total_files - self.completed_files
            return remaining_files / speed
        return 0
    
    def file_completed(self):
        with self.lock:
            self.completed_files += 1

time_stats = TimeStats()

# 键盘监听函数
def keyboard_listener(pbar, total_files):
    """监听键盘输入，控制暂停/恢复/停止"""
    print("\n⌨️  控制说明: 按 [P]暂停/恢复, [S]停止, [I]查看信息")
    
    while not STOP_EVENT.is_set():
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                
                if key == 'p':  # 暂停/恢复
                    if PAUSE_EVENT.is_set():
                        PAUSE_EVENT.clear()
                        time_stats.pause()
                        pbar.write("⏸️  已暂停处理 - 按 [P] 恢复")
                        pbar.set_description("⏸️  已暂停...")
                    else:
                        PAUSE_EVENT.set()
                        time_stats.resume()
                        pbar.write("▶️  已恢复处理")
                        pbar.set_description("🔄 处理中...")
                
                elif key == 's':  # 停止
                    STOP_EVENT.set()
                    PAUSE_EVENT.set()  # 确保不会卡在暂停状态
                    pbar.write("🛑 用户请求停止处理...")
                    break
                
                elif key == 'i':  # 显示信息
                    elapsed = time_stats.get_elapsed_time()
                    speed = time_stats.get_speed()
                    eta = time_stats.get_eta(total_files)
                    
                    pbar.write(f"📊 实时统计:")
                    pbar.write(f"   ⏱️  已运行: {elapsed:.1f}秒")
                    pbar.write(f"   📁 已完成: {time_stats.completed_files}/{total_files}")
                    pbar.write(f"   🚀 处理速度: {speed:.2f} 文件/秒")
                    if eta > 0:
                        pbar.write(f"   ⏰ 预计剩余: {eta:.1f}秒")
            
            time.sleep(0.1)  # 避免过度占用CPU
        except (UnicodeDecodeError, OSError):
            # 处理特殊按键或编码错误
            continue
        except Exception as e:
            # 静默处理其他异常，避免影响主程序
            continue

# "最终圣剑版"系统提示词
SYSTEM_PROMPT = """
You are a hyper-precise Ren'Py code modification bot. Your ONLY task is to add the `_()` wrapper to strings that are clearly intended for player translation, following a strict "Whitelist First" logic.

# CORE DIRECTIVE: WHITELIST FIRST, EVERYTHING ELSE IS FORBIDDEN.
You will ONLY modify a string if it perfectly matches one of the "PATTERNS TO MODIFY". If it does not match, you MUST NOT touch it.

# --- PATTERNS TO MODIFY (The Whitelist) ---
1.  **Character Definition:** A string inside a `Character()` function.
    -   `define e = Character("Eileen")` → `define e = Character(_("Eileen"))`

2.  **Variable Assignment (Full Sentences Only):** A string on the right side of an `=` that contains spaces and ends with punctuation (like `.`, `?`, `!`).
    -   `$ bio = "A full, translatable sentence."` → `$ bio = _("A full, translatable sentence.")`
    -   `$ flag = "visited"` → DO NOT MODIFY (not a full sentence).

3.  **Function Call Argument (Player-Facing Text Only):** A string passed as an argument to a function that is NOT a file path.
    -   `call Emotion(lyd, "groan", "What the fuck?!")` → `call Emotion(lyd, _("groan"), _("What the fuck?!"))`
    -   `$ name = renpy.input("Name?")` → `$ name = renpy.input(_("Name?"))`

4.  **`text` Statement:** A string that immediately follows the `text` keyword.
    -   `text "Game Unlocked"` → `text _("Game Unlocked")`

5.  **Complex Formatted String:** A string containing Ren'Py text tags (`{...}`) AND human-readable text.
    -   `"{font=font.ttf}Earth – Azores Rift{/font}"` → `_("{font=font.ttf}Earth – Azores Rift{/font}")`

# --- ABSOLUTE PROHIBITIONS (The Blacklist) ---
- **NO DIALOGUE:** NEVER touch standard dialogue (`character "text"`), narrator text (`"text"`), or menu options (`"Option text":`). The Ren'Py engine handles these.
- **NO FILE PATHS:** A string is a file path and MUST NOT be modified if it contains `/`, `\\`, or any of these extensions: `.png`, `.jpg`, `.webp`, `.mp3`, `.ogg`, `.ttf`, `.otf`, `.rpy`.
  - `call Door("images/door.png")` → DO NOT MODIFY.
- **NO CODE-LIKE STRINGS:** NEVER touch single words (`"word"`), keywords (`"True"`), or strings with programming formats (`"%s"`, `"[variable]"`).

# FINAL COMMANDMENT: WHEN IN DOUBT, DO NOTHING.
Preserving the original code is your highest priority. Return only the modified code, no explanations.
"""

def install_and_import_tqdm():
    try:
        import tqdm
        return tqdm
    except ImportError:
        logger.info("检测到缺少 'tqdm' 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
            import tqdm
            logger.info("✔ 'tqdm' 安装成功！")
            return tqdm
        except Exception as e:
            logger.error(f"✘ 自动安装 'tqdm' 失败: {e}\n请手动运行 'pip install tqdm' 后再重新运行脚本。")
            return None

tqdm_module = install_and_import_tqdm()

def config_wizard():
    """配置向导模式，帮助用户交互式配置"""
    print("\n" + "🧙"*60)
    print("  欢迎使用 Scorpio Weaver 配置向导！")
    print("🧙"*60 + "\n")
    
    config = {}
    
    # API配置
    print("📡 API配置")
    print("-" * 30)
    config['API_KEY'] = input("请输入您的API密钥: ").strip()
    config['BASE_URL'] = input("请输入API基础URL (如: https://api.openai.com/v1): ").strip()
    config['MODEL_NAME'] = input("请输入模型名称 (如: gpt-4): ").strip()
    
    # 游戏目录配置
    print("\n📁 游戏目录配置")
    print("-" * 30)
    while True:
        game_dir = input("请输入游戏目录路径: ").strip().replace('"', '')
        if os.path.isdir(game_dir):
            config['GAME_DIRECTORY'] = game_dir
            break
        else:
            print("❌ 目录不存在，请重新输入")
    
    # 性能配置
    print("\n⚡ 性能配置")
    print("-" * 30)
    while True:
        try:
            concurrent = int(input("并发处理数量 (建议1-5): ") or "3")
            if 1 <= concurrent <= 20:
                config['CONCURRENT_LIMIT'] = concurrent
                break
            else:
                print("❌ 请输入1-20之间的数字")
        except ValueError:
            print("❌ 请输入有效数字")
    
    while True:
        try:
            max_size = int(input("最大文件大小限制(KB) (建议50-200): ") or "100")
            if max_size > 0:
                config['MAX_FILE_SIZE_KB'] = max_size
                break
            else:
                print("❌ 请输入大于0的数字")
        except ValueError:
            print("❌ 请输入有效数字")
    
    # 其他配置使用默认值
    config.update({
        'OVERWRITE_FILES': False,
        'EXCLUDE_FILES': ["screens.rpy", "gui.rpy", "options.rpy"],
        'MAX_RETRIES': 3,
        'TIMEOUT': 60
    })
    
    # 安全模式选择
    print("\n🛡️ 安全模式")
    print("-" * 30)
    overwrite = input("是否直接覆盖原文件？(y/N): ").lower().startswith('y')
    config['OVERWRITE_FILES'] = overwrite
    
    # 保存配置
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ 配置已保存到: {config_path}")
    print("🎉 配置完成！现在可以运行主程序了。\n")
    return config

def validate_config(config):
    """启动时验证从配置文件加载的配置是否正确"""
    errors = []
    warnings = []
    
    # 必要配置检查
    if 'xxxx' in config['API_KEY'] or len(config['API_KEY']) < 20: 
        errors.append("🔑 API_KEY 似乎不正确，请检查是否已正确配置")
    if '你的游戏路径' in config['GAME_DIRECTORY'] or not os.path.isdir(config['GAME_DIRECTORY']): 
        errors.append("📁 GAME_DIRECTORY 路径无效，请确认游戏目录路径正确")
    if not config['MODEL_NAME'].strip(): 
        errors.append("🤖 MODEL_NAME 模型名称不能为空")
    if not config['BASE_URL'].strip() or not config['BASE_URL'].startswith('http'): 
        errors.append("🌐 BASE_URL 地址格式错误，应以http://或https://开头")
    
    # 性能配置建议
    if config['CONCURRENT_LIMIT'] > 10:
        warnings.append(f"⚠️  并发数设置为 {config['CONCURRENT_LIMIT']}，过高可能导致API限流")
    if config['MAX_FILE_SIZE_KB'] > 100:
        warnings.append(f"⚠️  最大文件大小设置为 {config['MAX_FILE_SIZE_KB']}KB，可能影响处理速度")
    
    if warnings:
        logger.warning("\n" + "⚠"*60 + "\n  配置建议：")
        for warning in warnings: logger.warning(f"  {warning}")
        logger.warning("⚠"*60)
    
    if errors:
        logger.error("\n" + "❌"*60 + "\n  配置检查失败，请修正以下错误：")
        for error in errors: logger.error(f"  {error}")
        logger.error("\n  💡 提示：运行时使用 --wizard 参数可启动配置向导")
        logger.error("❌"*60)
        input("\n按回车键退出...")
        sys.exit(1)

def post_process_code(code):
    if code.startswith("```python"): code = code[len("```python"):].strip()
    elif code.startswith("```"): code = code[3:].strip()
    if code.endswith("```"): code = code[:-3].strip()
    return code.strip()

def create_http_session(config):
    session = requests.Session()
    retry_strategy = Retry(
        total=config['MAX_RETRIES'],
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(pool_connections=config['CONCURRENT_LIMIT']*2, pool_maxsize=config['CONCURRENT_LIMIT']*10, max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

session = create_http_session(CONFIG)

def call_llm_api(user_prompt, file_name=""):
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {CONFIG['API_KEY']}"}
    data = {
        'model': CONFIG['MODEL_NAME'],
        'messages': [{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': user_prompt}],
        'temperature': 0.0, 'top_p': 1.0, 'stream': False
    }
    endpoint = f"{CONFIG['BASE_URL'].rstrip('/')}/chat/completions"
    try:
        response = session.post(endpoint, headers=headers, json=data, timeout=CONFIG['TIMEOUT'])
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and result['choices']:
            choice = result['choices'][0]
            content = choice.get('message', {}).get('content', '')
            finish_reason = choice.get('finish_reason', 'unknown')
            
            if finish_reason == 'length':
                tokens = result.get('usage', {}).get('completion_tokens', 'N/A')
                return (f"MODEL_ERROR: 🤖 AI模型输出被截断！\n"
                        f"📊 输出token数: {tokens}\n"
                        f"💡 建议: 文件 '{file_name}' 过于复杂，请考虑手动处理或使用更强大的模型")
            
            if content:
                return content
            else:
                return f"API_ERROR: 🔍 API返回内容为空\n📋 响应详情: {json.dumps(result, ensure_ascii=False)}"
        else:
            error_msg = result.get('error', {}).get('message', '未知API错误')
            return f"API_ERROR: 🚫 {error_msg}\n💡 请检查API配置和网络连接"
    except requests.exceptions.Timeout:
        return f"NETWORK_ERROR: ⏰ 请求超时 (>{CONFIG['TIMEOUT']}秒)\n💡 建议: 检查网络连接或增加超时时间"
    except requests.exceptions.ConnectionError:
        return f"NETWORK_ERROR: 🌐 网络连接失败\n💡 建议: 检查网络连接和BASE_URL配置"
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 'Unknown'
        return f"NETWORK_ERROR: 📡 HTTP错误 {status_code}\n💡 建议: 检查API密钥和配额"
    except requests.exceptions.RequestException as e:
        return f"NETWORK_ERROR: 🔌 {type(e).__name__}\n📝 详情: {e}"
    except Exception as e:
        return f"UNEXPECTED_ERROR: ❌ {type(e).__name__}\n📝 详情: {e}"

def process_file(file_path, stats, pbar, lock):
    file_name = os.path.basename(file_path)
    temp_file_path = f"{file_path}.{uuid.uuid4().hex}.tmp"
    start_time = time.time()

    try:
        # 检查是否需要停止
        if STOP_EVENT.is_set():
            return
        
        # 等待暂停解除
        PAUSE_EVENT.wait()
        
        # 更新进度条描述
        pbar.set_description(f"🔄 处理: {file_name[:20]}...")
        
        if file_name in CONFIG['EXCLUDE_FILES']:
            with lock: 
                stats['skipped_exclude'].append(file_name)
                pbar.write(f"⏭️  跳过排除文件: {file_name}")
            time_stats.file_completed()
            return
            
        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb > CONFIG['MAX_FILE_SIZE_KB']:
            with lock: 
                stats['skipped_size'].append(f"{file_name} ({file_size_kb:.1f}KB)")
                pbar.write(f"📏 跳过大文件: {file_name} ({file_size_kb:.1f}KB > {CONFIG['MAX_FILE_SIZE_KB']}KB)")
            time_stats.file_completed()
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
            
        if not original_code.strip():
            with lock: 
                stats['skipped_empty'].append(file_name)
                pbar.write(f"📄 跳过空文件: {file_name}")
            time_stats.file_completed()
            return

        # 再次检查暂停状态
        PAUSE_EVENT.wait()
        if STOP_EVENT.is_set():
            return
        
        # 显示API调用进度
        pbar.set_description(f"🤖 AI处理: {file_name[:15]}...")
        raw_modified_code = call_llm_api(original_code, file_name)

        if raw_modified_code.startswith(("API_ERROR", "NETWORK_ERROR", "UNEXPECTED_ERROR", "MODEL_ERROR")):
            error_lines = raw_modified_code.split('\n')
            pbar.write(f"❌ 文件 '{file_name}' 处理失败:")
            for line in error_lines:
                if line.strip():
                    pbar.write(f"   {line}")
            with lock: 
                stats['error'].append(file_name)
                stats['error_details'] = stats.get('error_details', {})
                stats['error_details'][file_name] = raw_modified_code
            time_stats.file_completed()
            return
        
        modified_code = post_process_code(raw_modified_code)
        
        # 内容质量检查
        if len(modified_code) < len(original_code) * 0.5:
            pbar.write(f"⚠️  文件 '{file_name}' 内容可能被截断 (修改后: {len(modified_code)} < 原始50%: {len(original_code)*0.5:.0f})")
            with lock: 
                stats['error'].append(file_name)
                stats['error_details'] = stats.get('error_details', {})
                stats['error_details'][file_name] = "内容被严重截断"
            time_stats.file_completed()
            return

        if modified_code == original_code:
            with lock: 
                stats['skipped_nochange'].append(file_name)
                pbar.write(f"🔄 无需修改: {file_name}")
            time_stats.file_completed()
            return

        # 保存文件
        pbar.set_description(f"💾 保存: {file_name[:18]}...")
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_code)
        
        output_path = file_path if CONFIG['OVERWRITE_FILES'] else f"{file_path}.new.rpy"
        os.replace(temp_file_path, output_path)
        
        # 计算处理时间
        process_time = time.time() - start_time
        with lock: 
            stats['success'] += 1
            stats['process_times'] = stats.get('process_times', [])
            stats['process_times'].append(process_time)
            pbar.write(f"✅ 成功处理: {file_name} ({process_time:.1f}s)")
        time_stats.file_completed()
    
    except Exception as e:
        error_msg = f"💥 处理 '{file_name}' 时发生严重错误:\n   🔍 错误类型: {type(e).__name__}\n   📝 错误详情: {e}"
        pbar.write(error_msg)
        with lock: 
            stats['error'].append(file_name)
            stats['error_details'] = stats.get('error_details', {})
            stats['error_details'][file_name] = f"{type(e).__name__}: {e}"
        time_stats.file_completed()
    finally:
        if os.path.exists(temp_file_path):
            try: os.remove(temp_file_path)
            except OSError: pass
        pbar.set_description("🔄 处理中...")
        pbar.update(1)

def print_enhanced_stats(stats, total_time, total_files):
    """打印增强的统计报告"""
    status = "处理完成！" if not STOP_EVENT.is_set() else "处理已停止！"
    logger.info("\n\n" + "📊"*60 + f"\n  {status}详细报告：\n" + "📊"*60)
    
    # 详细时间统计
    actual_work_time = time_stats.get_elapsed_time()
    pause_time = time_stats.total_pause_time
    
    logger.info(f"⏱️  总耗时: {total_time:.2f} 秒")
    logger.info(f"⚡ 实际工作时间: {actual_work_time:.2f} 秒")
    if pause_time > 0:
        logger.info(f"⏸️  暂停时间: {pause_time:.2f} 秒")
    
    if actual_work_time > 0: 
        logger.info(f"🚀 实际处理速度: {time_stats.completed_files / actual_work_time:.2f} 文件/秒")
        logger.info(f"📊 总体平均速度: {total_files / total_time:.2f} 文件/秒")
    
    # 处理时间分析
    if 'process_times' in stats and stats['process_times']:
        avg_time = sum(stats['process_times']) / len(stats['process_times'])
        max_time = max(stats['process_times'])
        min_time = min(stats['process_times'])
        logger.info(f"📈 单文件处理时间: 平均 {avg_time:.1f}s, 最快 {min_time:.1f}s, 最慢 {max_time:.1f}s")
        
        # 处理时间分布分析
        fast_files = sum(1 for t in stats['process_times'] if t < 5)
        medium_files = sum(1 for t in stats['process_times'] if 5 <= t < 15)
        slow_files = sum(1 for t in stats['process_times'] if t >= 15)
        
        logger.info(f"📊 处理时间分布: 快速(<5s): {fast_files}, 中等(5-15s): {medium_files}, 慢速(≥15s): {slow_files}")
    
    logger.info("-" * 60)
    
    # 结果统计
    logger.info(f"✅ 成功修改: {stats['success']} 个文件")
    logger.info(f"❌ 处理失败: {len(stats['error'])} 个文件")
    
    total_skipped = (len(stats['skipped_exclude']) + len(stats['skipped_size']) + 
                    len(stats['skipped_nochange']) + len(stats['skipped_empty']))
    logger.info(f"⏭️  跳过处理: {total_skipped} 个文件")
    
    if len(stats['skipped_exclude']) > 0: 
        logger.info(f"    📋 排除列表跳过: {len(stats['skipped_exclude'])} 个")
    if len(stats['skipped_size']) > 0: 
        logger.info(f"    📏 文件过大跳过: {len(stats['skipped_size'])} 个")
    if len(stats['skipped_empty']) > 0: 
        logger.info(f"    📄 空文件跳过: {len(stats['skipped_empty'])} 个")
    if len(stats['skipped_nochange']) > 0: 
        logger.info(f"    🔄 无需修改跳过: {len(stats['skipped_nochange'])} 个")
    
    logger.info("-" * 60)
    
    # 错误详情
    if stats['error']:
        logger.error("❌ 失败文件详情:")
        error_details = stats.get('error_details', {})
        for fname in stats['error']:
            logger.error(f"  📁 {fname}")
            if fname in error_details:
                detail_lines = error_details[fname].split('\n')
                for line in detail_lines[:2]:  # 只显示前两行错误信息
                    if line.strip():
                        logger.error(f"     {line.strip()}")
    
    # 成功率分析
    success_rate = (stats['success'] / total_files * 100) if total_files > 0 else 0
    if success_rate >= 90:
        logger.info(f"🎉 成功率: {success_rate:.1f}% - 优秀！")
    elif success_rate >= 70:
        logger.info(f"👍 成功率: {success_rate:.1f}% - 良好")
    else:
        logger.warning(f"⚠️  成功率: {success_rate:.1f}% - 需要关注")

def main():
    global CONFIG, session
    
    # 检查命令行参数
    if '--wizard' in sys.argv:
        if not tqdm_module: return
        config = config_wizard()
        # 重新加载配置
        CONFIG = config
        validate_config(CONFIG)
        session = create_http_session(CONFIG)
    else:
        if not tqdm_module: return
        validate_config(CONFIG)

    logger.info("\n" + "🚀"*60 + f"\n  Scorpio Weaver v5.5 - 智能本地化预处理工具  \n" + "🚀"*60)
    logger.info(f"📁 游戏路径: {CONFIG['GAME_DIRECTORY']}")
    logger.info(f"🤖 AI模型: {CONFIG['MODEL_NAME']}")
    logger.info(f"⚡ 并发数: {CONFIG['CONCURRENT_LIMIT']}")
    logger.info(f"🛡️  安全模式: {'❌ 关闭 (直接覆盖!)' if CONFIG['OVERWRITE_FILES'] else '✅ 开启 (生成.new.rpy文件)'}")
    logger.info(f"📏 文件大小限制: {CONFIG['MAX_FILE_SIZE_KB']}KB")
    logger.info(f"🕐 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("🚀"*60 + "\n")
    
    user_input = input("🔍 请确认以上配置。输入 'yes' 开始执行，'wizard' 重新配置: ").lower()
    if user_input == 'wizard':
        config = config_wizard()
        CONFIG.update(config)
        validate_config(CONFIG)
        # 重新创建session
        session = create_http_session(CONFIG)
    elif user_input != 'yes':
        logger.info("❌ 操作已取消。")
        return

    # 扫描文件
    logger.info("🔍 正在扫描 .rpy 文件...")
    rpy_files = [os.path.join(root, file) for root, _, files in os.walk(CONFIG['GAME_DIRECTORY']) 
                 for file in files if file.endswith('.rpy')]
    
    if not rpy_files:
        logger.warning("⚠️  在指定目录下未找到任何 .rpy 文件。请检查 GAME_DIRECTORY 配置。")
        input("按回车键退出...")
        return

    stats = {
        'success': 0, 'error': [], 'error_details': {},
        'skipped_exclude': [], 'skipped_size': [], 'skipped_nochange': [], 'skipped_empty': [],
        'process_times': []
    }
    lock = threading.Lock()
    
    logger.info(f"📋 扫描完成！发现 {len(rpy_files)} 个 .rpy 文件")
    logger.info(f"🚀 开始处理，使用 {CONFIG['CONCURRENT_LIMIT']} 个并发线程...\n")
    
    # 启动时间统计
    time_stats.start()
    start_time = time.time()

    # 增强的进度条，包含实时速度和ETA
    def update_progress_desc(pbar):
        """更新进度条描述，显示实时统计"""
        while not STOP_EVENT.is_set():
            if PAUSE_EVENT.is_set():  # 只在运行时更新
                elapsed = time_stats.get_elapsed_time()
                speed = time_stats.get_speed()
                eta = time_stats.get_eta(len(rpy_files))
                
                if speed > 0:
                    desc = f"🔄 处理中 | 速度: {speed:.1f}f/s | ETA: {eta:.0f}s"
                else:
                    desc = "🔄 处理中..."
                
                pbar.set_description(desc)
            time.sleep(1)  # 每秒更新一次
    
    bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]"
    with tqdm_module.tqdm(total=len(rpy_files), unit="file", bar_format=bar_format, 
                         desc="🔄 处理中...", ncols=120) as pbar:
        
        # 启动键盘监听线程
        keyboard_thread = threading.Thread(target=keyboard_listener, args=(pbar, len(rpy_files)), daemon=True)
        keyboard_thread.start()
        
        # 启动进度描述更新线程
        progress_thread = threading.Thread(target=update_progress_desc, args=(pbar,), daemon=True)
        progress_thread.start()
        
        with ThreadPoolExecutor(max_workers=CONFIG['CONCURRENT_LIMIT']) as executor:
            futures = [executor.submit(process_file, file_path, stats, pbar, lock) 
                      for file_path in rpy_files]
            
            for future in futures:
                try: 
                    if STOP_EVENT.is_set():
                        # 如果用户请求停止，取消剩余任务
                        for f in futures:
                            f.cancel()
                        break
                    future.result()
                except Exception as e: 
                    pbar.write(f"💥 线程池任务异常: {type(e).__name__} - {e}")
        
        # 如果被用户停止，显示停止信息
        if STOP_EVENT.is_set():
            pbar.write("\n🛑 处理已被用户停止")

    end_time = time.time()
    total_time = end_time - start_time
    
    # 确保停止所有后台线程
    STOP_EVENT.set()
    PAUSE_EVENT.set()
    
    # 打印增强的统计报告
    print_enhanced_stats(stats, total_time, len(rpy_files))
    
    # 操作建议
    if not CONFIG['OVERWRITE_FILES'] and stats['success'] > 0:
        logger.info("\n💡 操作建议:")
        logger.info("   1. 检查生成的 .new.rpy 文件")
        logger.info("   2. 确认修改正确后，删除原文件并重命名 .new.rpy")
        logger.info("   3. 或设置 OVERWRITE_FILES=true 后重新运行")
    
    if len(stats['error']) > 0:
        logger.info("\n🔧 故障排除建议:")
        logger.info("   1. 检查网络连接和API配置")
        logger.info("   2. 确认API密钥有效且有足够配额")
        logger.info("   3. 考虑减少并发数或增加超时时间")
    
    # 性能分析建议
    if 'process_times' in stats and stats['process_times']:
        avg_time = sum(stats['process_times']) / len(stats['process_times'])
        if avg_time > 10:
            logger.info("\n⚡ 性能优化建议:")
            logger.info("   1. 考虑使用更快的AI模型")
            logger.info("   2. 减少MAX_FILE_SIZE_KB限制")
            logger.info("   3. 检查网络延迟和API响应时间")
        elif time_stats.total_pause_time > total_time * 0.3:
            logger.info("\n⏸️  注意: 暂停时间较长，可能影响整体效率")
    
    logger.info("\n" + "🎯"*60)
    logger.info(f"🕐 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if STOP_EVENT.is_set() and time_stats.completed_files < len(rpy_files):
        logger.info(f"📊 处理进度: {time_stats.completed_files}/{len(rpy_files)} ({time_stats.completed_files/len(rpy_files)*100:.1f}%)")
    logger.info("🎯"*60)
    
    logger.info("\n⌨️  提示: 下次运行时可使用以下快捷键:")
    logger.info("   [P] - 暂停/恢复处理")
    logger.info("   [S] - 停止处理")
    logger.info("   [I] - 查看实时统计信息")
    
    input("\n按回车键退出程序...")

if __name__ == '__main__':
    main()
