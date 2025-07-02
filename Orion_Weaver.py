# ==============================================================================
#  自动化本地化预处理工具 v5.0 - 最终圣剑版
#  作者：猫之送葬者 & 你的AI助手Gemini & DeepSeek
#  更新日志：
#    v5.0: 融合所有版本精华，形成终极“圣剑”提示词，并强化熔断保险丝。
#    v4.8: 优化"代码优先逻辑"，添加明确边界条件。
#    v4.7: 引入"代码优先逻辑"，颠覆规则体系。
#    v4.6: 新增“白金圣旨”规则，终极定义“对话行”，解决 menu 和自定义角色(msg)的误判问题。
#    v4.5: 强化"反创作"指令，明确禁止任何形式的文本修改。
#    v4.4: 新增"熔断保险丝"，防止AI返回残缺内容。
# ==============================================================================
import os
import sys
import time
import requests
import subprocess
import uuid
import re

# ==============================================================================
# ===== 配置区 (小白友好，只需修改这部分) =====
# ==============================================================================
# 1. 粘贴你的API密钥 (从你的AI服务商网站获取)
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # <--- 在这里粘贴你的API Key

# 2. 粘贴API基础URL (中转站地址，通常以 /v1 结尾)
BASE_URL = 'https://xxxxxxxxxxxxx/v1' # <--- 在这里粘贴你的API Base URL

# 3. 粘贴模型名称 (例如：gemini-1.5-pro-latest, deepseek-v2, gpt-4o)
MODEL_NAME = 'gemini-2.5-flash-preview-05-20' # <--- 在这里填写你使用的模型名称

# 4. 粘贴你的游戏 'game' 文件夹的完整路径 (在文件夹上右键 -> 复制地址)
GAME_DIRECTORY = r'G:\你的游戏路径\game' # <--- 在这里填写你的游戏game文件夹路径

# 5. 安全模式开关 (True = 直接覆盖原文件, False = 创建.new.rpy新文件)
# 警告：AI并非100%可靠，强烈建议保持为 False，通过对比工具人工审核后再合并修改！
OVERWRITE_FILES = False

# 6. 最大文件大小限制 (单位KB，超过这个大小的文件会被自动跳过)
MAX_FILE_SIZE_KB = 500  # 推荐值: 200-1000

# 7. 文件排除列表 (这些文件将被脚本自动忽略)
EXCLUDE_FILES = ['gui.rpy', 'options.rpy', 'screens.rpy']

# ==============================================================================
# ===== 脚本核心 (高手勿动，小白更不要动！) =====
# ==============================================================================

# "最终圣剑版"系统提示词 (v5.0)
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
    """检查并安装tqdm库，返回tqdm模块或None。"""
    print("正在检查所需组件...")
    try:
        import tqdm
        print("✓ tqdm 库已安装")
        return tqdm
    except ImportError:
        print("检测到缺少 'tqdm' 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
            import tqdm
            print("✓ tqdm 库安装成功！")
            return tqdm
        except Exception as e:
            print(f"✘ 自动安装失败: {e}")
            print("  请手动在命令行运行: py -m pip install tqdm")
            return None

def validate_config():
    """启动时验证配置是否正确。"""
    print("\n正在验证配置...")
    errors = []
    if 'xxxx' in API_KEY or len(API_KEY) < 20:
        errors.append("API密钥无效 (请粘贴正确的API密钥)")
    if '你的游戏路径' in GAME_DIRECTORY or not os.path.isdir(GAME_DIRECTORY):
        errors.append("游戏路径无效 (请粘贴正确的game文件夹路径)")
    if not MODEL_NAME.strip():
        errors.append("模型名称未设置 (请填写模型名称)")
    if not BASE_URL.strip() or not BASE_URL.startswith('http'):
        errors.append("API地址格式错误 (必须以http/https开头)")
    
    if errors:
        print("\n" + "!"*60)
        print("配置错误，请打开脚本修正以下问题:")
        for error in errors:
            print(f"  ✘ {error}")
        print("!"*60)
        input("\n按Enter键退出...")
        sys.exit(1)
    print("✓ 配置验证通过")

def post_process_code(code):
    """对AI返回的代码进行强制净化处理"""
    # 移除代码块标记
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    if code.startswith("```"):
        code = code[3:].strip()
    if code.endswith("```"):
        code = code[:-3].strip()
    
    # 确保代码以换行符结束
    if not code.endswith('\n'):
        code += '\n'
    
    return code.strip(' \t\n\r~')

def call_llm_api_with_retry(api_key, base_url, model_name, system_prompt, user_prompt, log_func):
    """带5次重试功能的API调用函数。"""
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    data = {
        'model': model_name,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        'temperature': 0.0,
        'top_p': 1.0
    }
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    
    # 5次重试
    for attempt in range(5):
        try:
            response = requests.post(endpoint, headers=headers, json=data, timeout=180)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content']
                return content
            else:
                error_msg = f"API返回格式错误: {result.get('error', {}).get('message', '未知错误')}"
                log_func(f"  ✘ API错误: {error_msg}")
                return error_msg
                
        except requests.exceptions.Timeout:
            wait_time = (attempt + 1) * 10
            log_func(f"  ⚠️ API请求超时，{wait_time}秒后重试... (尝试 {attempt+1}/5)")
            time.sleep(wait_time)
            
        except Exception as e:
            if attempt < 4:  # 前4次失败后重试
                wait_time = (attempt + 1) * 5
                log_func(f"  ⚠️ API请求失败: {type(e).__name__}, {wait_time}秒后重试... (尝试 {attempt+1}/5)")
                time.sleep(wait_time)
            else:
                return f"API请求失败: {type(e).__name__} - {str(e)}"
    
    return "API请求失败: 超过最大重试次数(5次)"

def process_file(file_path, stats, log_func):
    """处理单个.rpy文件，包含净化和熔断保险丝。"""
    file_name = os.path.basename(file_path)
    
    # 检查文件大小
    try:
        file_size = os.path.getsize(file_path)
        if file_size / 1024 > MAX_FILE_SIZE_KB:
            log_func(f"  → 跳过大文件: {file_name} ({file_size/1024:.1f}KB > {MAX_FILE_SIZE_KB}KB)")
            stats['skipped'].append(file_name)
            return
    except Exception as e:
        log_func(f"  ✘ 无法获取文件大小: {file_name} ({e})")
        stats['error'].append(file_name)
        return
    
    # 创建唯一临时文件名
    temp_path = f"{file_path}.{uuid.uuid4().hex}.tmp"
    
    try:
        # 读取原始文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        # 空文件检查
        if not original_code.strip():
            log_func(f"  → 跳过空文件: {file_name}")
            stats['skipped'].append(file_name)
            return
        
        # 调用API处理
        log_func(f"  ⌛ 开始处理: {file_name}")
        raw_modified_code = call_llm_api_with_retry(
            API_KEY, BASE_URL, MODEL_NAME, SYSTEM_PROMPT, original_code, log_func
        )
        
        # 检查API是否返回错误
        if "API请求失败" in raw_modified_code or "错误" in raw_modified_code:
            log_func(f"  ✘ 处理失败: {file_name} (原因: {raw_modified_code})")
            stats['error'].append(file_name)
            return
        
        # 对代码进行后处理
        final_code = post_process_code(raw_modified_code)
        
        # v4.8 强化的熔断保险丝
        # 检查1：是否过短（小于原长度的70%）
        if len(final_code) < len(original_code) * 0.7:
            log_func(f"  ✘ 处理失败: {file_name} (AI返回内容被严重截断，已自动跳过)")
            stats['error'].append(f"{file_name} [AI内容截断]")
            return
        # 检查2：是否过长（超过原长度的150%，以容纳少量_()增加）
        if len(final_code) > len(original_code) * 1.5:
            log_func(f"  ✘ 处理失败: {file_name} (AI返回内容异常膨胀，已自动跳过)")
            stats['error'].append(f"{file_name} [AI内容膨胀]")
            return
        
        # 安全写入临时文件
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        
        # 重命名文件
        if OVERWRITE_FILES:
            os.replace(temp_path, file_path)
            log_func(f"  ✓ 已覆盖更新: {file_name} (警告：请确保已备份！)")
        else:
            new_file = file_path.replace('.rpy', '.new.rpy')
            os.rename(temp_path, new_file)
            log_func(f"  ✓ 已创建建议文件: {os.path.basename(new_file)}")
        
        stats['success'] += 1
            
    except Exception as e:
        log_func(f"  ✘ 处理时发生未知错误: {file_name} ({type(e).__name__}: {e})")
        stats['error'].append(file_name)
    finally:
        # 确保清理临时文件
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def main():
    """主程序入口，包含最终的战报汇总。"""
    tqdm_module = install_and_import_tqdm()
    validate_config()
    
    print("\n" + "="*60)
    print("  自动化本地化预处理工具 v5.0 - 最终圣剑版")
    print("="*60)
    print(f"  游戏路径: {GAME_DIRECTORY}")
    print(f"  处理模式: {'[覆盖模式]' if OVERWRITE_FILES else '[安全模式-生成.new.rpy]'}")
    print(f"  文件大小限制: {MAX_FILE_SIZE_KB}KB")
    print(f"  排除文件列表: {EXCLUDE_FILES}")
    print(f"  API重试次数: 5次")
    print("="*60)
    
    if OVERWRITE_FILES:
        print("\n⚠️ 警告：您已启用[覆盖模式]，将直接修改源文件！")
        print("⚠️ 请再次确认已备份所有重要文件！")
    else:
        print("\n💡 提示：当前为[安全模式]，将生成.new.rpy文件。")
        print("   请使用Beyond Compare等工具对比，将AI正确的修改【选择性合并】到原文件中。")

    try:
        confirm = input("\n我已阅读提示并备份了文件，确认开始处理？(输入 yes 继续): ")
        if confirm.lower() != 'yes':
            print("操作已取消。")
            return
    except KeyboardInterrupt:
        print("\n操作已由用户取消。")
        return
    
    print("\n正在扫描游戏文件 (将自动排除 'tl' 文件夹及指定文件)...")
    rpy_files = []
    normalized_game_dir = os.path.normpath(GAME_DIRECTORY)
    
    exclude_paths = [
        os.path.join(normalized_game_dir, 'tl'),
        os.path.join(normalized_game_dir, 'archive')
    ]
    exclude_files = set(EXCLUDE_FILES)

    for root, _, files in os.walk(normalized_game_dir):
        if any(os.path.commonprefix([root, path]) == path for path in exclude_paths):
            continue
        for file in files:
            if file in exclude_files:
                continue
            if file.endswith('.rpy') and not file.endswith('.new.rpy'):
                rpy_files.append(os.path.join(root, file))
    
    if not rpy_files:
        print("在非翻译文件夹中未找到任何 .rpy 文件！请检查路径和排除列表。")
        input("\n按Enter键退出...")
        return
    
    print(f"找到 {len(rpy_files)} 个需要处理的 .rpy 文件。")
    
    stats = {'success': 0, 'skipped': [], 'error': []}
    start_time = time.time()
    
    print("\n" + "="*60)
    print("处理日志:")
    print("="*60)
    
    if tqdm_module:
        pbar = tqdm_module.tqdm(total=len(rpy_files), unit="file", 
                                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
        log_func = pbar.write
    else:
        pbar = None
        log_func = print
        print(f"[0/{len(rpy_files)}] 开始处理文件...")
    
    for i, file_path in enumerate(rpy_files):
        if pbar:
            pbar.set_description(f"当前文件: {os.path.basename(file_path)[:25]:<25}")
        else:
            print(f"[{i+1}/{len(rpy_files)}] ", end='', flush=True)
        
        process_file(file_path, stats, log_func)
        
        if pbar:
            pbar.update(1)
        
        time.sleep(1)
    
    if pbar:
        pbar.close()

    time_taken = time.time() - start_time
    processed_count = stats['success'] + len(stats['skipped']) + len(stats['error'])
    
    print("\n" + "="*60)
    print("处理完成！最终战报:")
    print("="*60)
    print(f"  ✓ 成功: {stats['success']} 个文件")
    print(f"  → 跳过: {len(stats['skipped'])} 个文件 (空/过大/排除)")
    if stats['skipped']:
        print("    跳过的文件列表:")
        for filename in stats['skipped']:
            print(f"      - {filename}")
    print(f"  ✘ 错误: {len(stats['error'])} 个文件")
    if stats['error']:
        print("    错误的文件列表:")
        for filename in stats['error']:
            print(f"      - {filename}")
    print(f"  ⏱️ 总耗时: {time_taken:.1f} 秒 ({time_taken/60:.1f} 分钟)")
    print(f"  📊 处理速度: {processed_count/max(time_taken, 1):.1f} 文件/秒")
    print("="*60)
    
    if stats['error']:
        print("\n提示：对于处理出错的文件，可能是AI返回内容被截断或API请求失败。")
        print("建议检查网络或尝试手动处理这些文件。")
    
    if not OVERWRITE_FILES and stats['success'] > 0:
        print("\n所有新文件已创建为 .new.rpy 后缀。")
        print("【重要】请务必使用Beyond Compare等工具，人工审核并【选择性合并】正确的修改！")
    
    input("\n所有任务已结束，按Enter键退出...")

if __name__ == '__main__':
    main()