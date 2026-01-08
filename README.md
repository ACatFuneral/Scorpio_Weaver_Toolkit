# 🐱 OldCat Ren'Py Translator Tool (老猫神器)

[![Latest Release](https://img.shields.io/github/v/release/ACatFuneral/Scorpio_Weaver_Toolkit?label=release)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest) [![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/blob/main/LICENSE) [![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases)

> **专为 Ren'Py 汉化者打造的终极提取/翻译辅助工具。**
> *无需 Python 基础 · 图形化界面 · 一键提取 · 智能去重 · 战果统计*

## ✨ 为什么选择老猫神器？

以前汉化 Ren'Py 游戏，你需要：
1. 学 Python 跑脚本。
2. 手动改复杂的 `config.json` 配置文件。
3. 忍受黑框框命令行的折磨。
4. 面对一堆提取出来的乱七八糟文件，不知道哪些该翻。

**现在，你只需要：**
**双击 exe，点一下按钮。** 完事！🚀

## 🔥 核心功能 (v8.1)

### 🖥️ 1. 图形化界面 (GUI)
告别命令行！清晰的界面，简单的选项。
- **傻瓜式操作**：浏览选择游戏目录 -> 设置语言 -> 点击开始。
- **实时日志**：运行过程全程可视，不再“摸黑干活”。

### 📊 2. 战果统计系统 (NEW!)
提取完成后，自动弹出详细的统计报告：
- **扫描文件数**：扫了多少个文件？
- **人名/术语**：提取了多少个角色名？（自动生成 `names.xlsx`）
- **对话/UI**：提取了多少句对白？（自动生成 `others.xlsx`）
- **精准分类**：让你对汉化工作量心中有数。

### 🧹 3. 智能过滤 & 去重
- **垃圾过滤**：自动剔除代码、变量名、文件路径等无需翻译的“垃圾文本”。
- **智能去重**：相同的文本只提取一次，节省 50% 以上的翻译成本。
- **增量更新**：如果 `tl` 文件夹里已经翻译过一部分，工具会自动跳过，**只提取新增文本**！

### 🔒 4. 独家黑科技
- **Tag 保护 (Emoji 映射)**：防止机翻软件破坏 `{color=#f00}` 这种代码标签。
- **疯狗模式**：深度扫描 Python 代码块中的硬编码文本（慎用，威力巨大）。
- **AI 辅助**：一键生成 `AI_Prompt_Names.txt`，直接喂给 AI 统一角色译名。

---

## 🚀 极速上手

### 方式一：直接下载 (推荐小白)
1. 前往 [**Releases 页面**](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest) 下载最新的 **`老猫神器 v8.1.zip`**。
2. 解压文件夹。
3. 双击运行 **`OldCat_Translator.exe`**。
4. 选择游戏 `game` 目录，点击 **“开始提取”**。
5. 去 `translate_output` 文件夹收菜！

### 方式二：源码运行 (推荐开发者)
如果你想自己修改代码或在 Mac/Linux 上运行：

```bash
# 1. 克隆仓库
git clone https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit.git

# 2. 安装依赖
pip install pandas openpyxl pyyaml

# 3. 运行脚本
python OldCat_GUI.py

---

## 📂 输出文件说明

工具运行完毕后，会在同目录下生成 `translate_output` 文件夹：

| 文件夹/文件 | 说明 |
| :--- | :--- |
| **`1_Excels/names.xlsx`** | **人名表**。这里全是角色名字，建议先翻这个，统一称呼。 |
| **`1_Excels/others.xlsx`** | **对话表**。游戏的主要剧情都在这里，直接拿去喂 AI 或手翻。 |
| **`2_RPY_Files/*.rpy`** | **生成的翻译文件**。翻译完 Excel 后，可以用工具把译文回填到这里（如果你会写回填脚本的话），或者直接手动参考。 |
| **`AI_Prompt_Names.txt`** | **AI 提示词**。把这个文件内容发给 ChatGPT/Claude，让它帮你生成人名翻译表。 |
| **`Duplicate_Report.txt`** | **统计报告**。看看哪些词出现频率最高，方便优先汉化。 |

---

## 📝 更新日志

### v8.1 (Latest) - 战果统计版
- ✅ **新增**：任务完成后的详细统计弹窗（扫描数、提取数、分类统计）。
- ✅ **优化**：外部数据文件 (`.json`/`.yml`) 的扫描逻辑更加精准。
- ✅ **优化**：依赖库自动检测与静默安装体验。

### v8.0 - 图形化重构
- 🎨 **重构**：从命令行脚本全面升级为 GUI 图形界面。
- 📦 **打包**：支持打包为独立 `.exe`，无需 Python 环境。

---

## 🤝 贡献与反馈

本项目由 **OldCat** & **Scorpio Weaver** 联合打造。
如果你发现了 Bug，或者有好的建议，欢迎提 [Issues](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/issues) 或 Pull Request！

**如果不麻烦的话，给个 ⭐ Star 支持一下吧！**
