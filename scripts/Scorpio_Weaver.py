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
import time
import requests
import subprocess
import json
import logging
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import重试

# --- v5.4 核心：不再有配置区，所有配置来自 config.json ---

# 配置日志系统
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """加载或创建配置文件"""
    # 配置文件与脚本在同一目录
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

# "最终圣剑版"系统提示词
SYSTEM_PROMPT = """
You are a hyper-precise Ren'Py code modification bot. Your ONLY task is to add the `_()` wrapper to strings that are clearly intended for player translation, following a strict "Whitelist First" logic.
# CORE DIRECTIVE: WHITELIST FIRST, EVERYTHING ELSE IS FORBIDDEN.
You will ONLY modify a string if it perfectly matches one of the "PATTERNS TO MODIFY". If it does not match, you MUST NOT touch it.
# --- PATTERNS TO MODIFY (The Whitelist) ---
1.  **Character Definition:** `define e = Character("Eileen")` → `define e = Character(_("Eileen"))`
2.  **Variable Assignment (Full Sentences Only):** `$ bio = "A full, translatable sentence."` → `$ bio = _("A full, translatable sentence.")`
3.  **Function Call Argument (Player-Facing Text Only):** `call Emotion(lyd, "groan", "What the fuck?!")` → `call Emotion(lyd, _("groan"), _("What the fuck?!"))`
4.  **`text` Statement:** `text "Game Unlocked"` → `text _("Game Unlocked")`
5.  **Complex Formatted String:** `"{font=font.ttf}Earth – Azores Rift{/font}"` → `_("{font=font.ttf}Earth – Azores Rift{/font}")`
# --- ABSOLUTE PROHIBITIONS (The Blacklist) ---
- **NO DIALOGUE:** NEVER touch standard dialogue (`character "text"`), narrator text (`"text"`), or menu options (`"Option text":`). The Ren'Py engine handles these.
- **NO FILE PATHS:** A string is a file path and MUST NOT be modified if it contains `/`, `\\`, or any of these extensions: `.png`, `.jpg`, `.webp`, `.mp3`, `.ogg`, `.ttf`, `.otf`, `.rpy`.
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

def validate_config(config):
    """启动时验证从配置文件加载的配置是否正确"""
    errors = []
    if 'xxxx' in config['API_KEY'] or len(config['API_KEY']) < 20: errors.append("API_KEY 似乎不正确，请在 config.json 中检查。")
    if '你的游戏路径' in config['GAME_DIRECTORY'] or not os.path.isdir(config['GAME_DIRECTORY']): errors.append("GAME_DIRECTORY 路径无效，请在 config.json 中检查。")
    if not config['MODEL_NAME'].strip(): errors.append("MODEL_NAME 模型名称不能为空。")
    if not config['BASE_URL'].strip() or not config['BASE_URL'].startswith('http'): errors.append("BASE_URL 地址格式错误。")
    if errors:
        logger.error("\n" + "!"*60 + "\n  配置检查失败，请修正以下错误：")
        for error in errors: logger.error(f"  ✘ {error}")
        logger.error("!"*60)
        input("\n按回车键退出...")
        sys.exit(1)

def post_process_code(code):
    if code.startswith("```python"): code = code[len("```python"):].strip()
    elif code.startswith("```"): code = code[3:].strip()
    if code.endswith("```"): code = code[:-3].strip()
    return code.strip()

def create_http_session(config):
    session = requests.Session()
    retry_strategy = 重试(
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

def call_llm_api(user_prompt):
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
                return (f"MODEL_ERROR: AI模型输出被截断! (finish_reason: 'length', 输出token数: {tokens}). "
                        f"这通常意味着文件过于复杂或模型陷入逻辑循环。建议手动处理此文件或更换更强大的模型。")
            
            if content:
                return content
            else:
                return f"API_ERROR: 返回内容为空，但未报告超限。响应: {json.dumps(result)}"
        else:
            return f"API_ERROR: {result.get('error', {}).get('message', '未知API错误')}"
    except requests.exceptions.RequestException as e:
        return f"NETWORK_ERROR: {type(e).__name__} - {e}"
    except Exception as e:
        return f"UNEXPECTED_ERROR: {type(e).__name__} - {e}"

def process_file(file_path, stats, pbar, lock):
    file_name = os.path.basename(file_path)
    temp_file_path = f"{file_path}.{uuid.uuid4().hex}.tmp"

    try:
        if file_name in CONFIG['EXCLUDE_FILES']:
            with lock: stats['skipped_exclude'].append(file_name)
            return
        if os.path.getsize(file_path) / 1024 > CONFIG['MAX_FILE_SIZE_KB']:
            with lock: stats['skipped_size'].append(f"{file_name} ({os.path.getsize(file_path)/1024:.1f}KB)")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        if not original_code.strip():
            with lock: stats['skipped_empty'].append(file_name)
            return

        raw_modified_code = call_llm_api(original_code)

        if raw_modified_code.startswith(("API_ERROR", "NETWORK_ERROR", "UNEXPECTED_ERROR", "MODEL_ERROR")):
            pbar.write(f"✘ 文件 '{file_name}' 处理失败: {raw_modified_code}")
            with lock: stats['error'].append(file_name)
            return
        
        modified_code = post_process_code(raw_modified_code)
        
        if len(modified_code) < len(original_code) * 0.5:
             pbar.write(f"✘ 文件 '{file_name}' 内容可能被严重截断 (修改后长度不足原始50%)，跳过保存。")
             with lock: stats['error'].append(file_name)
             return

        if modified_code == original_code:
            with lock: stats['skipped_nochange'].append(file_name)
            return

        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_code)
        
        output_path = file_path if CONFIG['OVERWRITE_FILES'] else f"{file_path}.new.rpy"
        os.replace(temp_file_path, output_path)
        with lock: stats['success'] += 1
    
    except Exception as e:
        pbar.write(f"✘ 处理 '{file_name}' 时发生严重错误: {type(e).__name__} - {e}")
        with lock: stats['error'].append(file_name)
    finally:
        if os.path.exists(temp_file_path):
            try: os.remove(temp_file_path)
            except OSError: pass
        pbar.update(1)

def main():
    if not tqdm_module: return
    validate_config(CONFIG)

    logger.info("\n" + "="*60 + f"\n  自动化本地化预处理工具 v5.4 - 配置分离版  \n" + "="*60)
    logger.info(f"游戏路径: {CONFIG['GAME_DIRECTORY']}")
    logger.info(f"模型: {CONFIG['MODEL_NAME']}")
    logger.info(f"并发数: {CONFIG['CONCURRENT_LIMIT']}")
    logger.info(f"安全模式: {'关闭 (直接覆盖!)' if CONFIG['OVERWRITE_FILES'] else '开启 (生成.new.rpy文件)'}")
    logger.info("="*60 + "\n")
    
    if input("请再次确认以上配置。输入 'yes' 开始执行: ").lower() != 'yes':
        logger.info("操作已取消。")
        return

    rpy_files = [os.path.join(root, file) for root, _, files in os.walk(CONFIG['GAME_DIRECTORY']) for file in files if file.endswith('.rpy')]
    if not rpy_files:
        logger.warning("在指定目录下未找到任何 .rpy 文件。请检查 GAME_DIRECTORY 配置。")
        return

    stats = {'success': 0, 'error': [], 'skipped_exclude': [], 'skipped_size': [], 'skipped_nochange': [], 'skipped_empty': []}
    lock = threading.Lock()
    start_time = time.time()
    
    logger.info(f"\n扫描到 {len(rpy_files)} 个 .rpy 文件，开始处理...")

    with tqdm_module.tqdm(total=len(rpy_files), unit="file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
        with ThreadPoolExecutor(max_workers=CONFIG['CONCURRENT_LIMIT']) as executor:
            futures = [executor.submit(process_file, file_path, stats, pbar, lock) for file_path in rpy_files]
            for future in futures:
                try: future.result()
                except Exception as e: pbar.write(f"一个线程池任务发生未捕获异常: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    total_processed = sum(len(v) if isinstance(v, list) else v for v in stats.values())
    
    logger.info("\n\n" + "="*60 + "\n  处理完成！最终报告：\n" + "="*60)
    logger.info(f"总耗时: {total_time:.2f} 秒")
    if total_time > 0: logger.info(f"平均速度: {total_processed / total_time:.2f} 文件/秒")
    logger.info("-" * 60)
    logger.info(f"✔ 成功修改: {stats['success']} 个文件")
    logger.info(f"✘ 处理失败: {len(stats['error'])} 个文件")
    total_skipped = len(stats['skipped_exclude']) + len(stats['skipped_size']) + len(stats['skipped_nochange']) + len(stats['skipped_empty'])
    logger.info(f"➔ 跳过处理: {total_skipped} 个文件")
    if len(stats['skipped_exclude']) > 0: logger.info(f"    - 因排除列表跳过: {len(stats['skipped_exclude'])}")
    if len(stats['skipped_size']) > 0: logger.info(f"    - 因文件过大跳过: {len(stats['skipped_size'])}")
    if len(stats['skipped_empty']) > 0: logger.info(f"    - 因内容为空跳过: {len(stats['skipped_empty'])}")
    if len(stats['skipped_nochange']) > 0: logger.info(f"    - 因AI判定无需修改跳过: {len(stats['skipped_nochange'])}")
    logger.info("-" * 60)

    if stats['error']:
        logger.error("失败文件列表:")
        for fname in stats['error']: logger.error(f"  - {fname}")
    if not CONFIG['OVERWRITE_FILES'] and stats['success'] > 0:
        logger.info("\n提示：已成功生成 .new.rpy 文件。请检查修改是否正确，\n确认无误后，可手动删除原文件并将 .new.rpy 文件重命名，\n或将配置项 OVERWRITE_FILES 设置为 True 后重新运行。")
    logger.info("\n" + "="*60)
    input("按回车键退出程序...")

if __name__ == '__main__':
    main()
