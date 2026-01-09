</div>
<div align="center">
<!-- 在这里放一个你酷炫的 Logo -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/Scorpio.png" width="400" alt="Project Logo" />

# 🐱 OldCat Ren'Py Translator Tool
### —— 哈基猫 Ren'Py 盒子 v8.2 ——

[![Latest Release](https://img.shields.io/github/v/release/ACatFuneral/Scorpio_Weaver_Toolkit?label=Version&style=for-the-badge&color=orange)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/blob/main/LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases)

**专为 Ren'Py 汉化者打造的提取/翻译/保护全能工具**  
*无需 Python 基础 · 图形化界面 · 一键提取 · 智能去重 · 集成Tag保护 · 战果统计*

<br>

<img width="686" alt="哈基猫神器界面" src="https://github.com/user-attachments/assets/f3171811-c5dc-4c96-a347-92016d8e56f5" />

<br>

</div>

---

## ✨ 为什么选择哈基猫？

**核心痛点：官方工具提取不全！**

你是否遇到过这种情况：明明用 Ren'Py 官方 SDK 提取了翻译文件，进游戏一看，依然有大量**未汉化的英文**？
这是因为许多游戏作者代码写得比较“骚”，喜欢把文本**硬编码 (Hardcode)** 在 Python 逻辑、动态变量或复杂的屏幕 (Screen) 代码里，官方工具根本识别不了！

**哈基猫的真正意义在于：**
它不仅仅是一个提取工具，它是**官方 SDK 的强力补充**，专为解决“漏网之鱼”而生。

1.  🎯 **专治“漏网之鱼”**：
    官方工具提不到的**硬编码文本、Python 里的字符串**，老猫用“疯狗模式”帮你全挖出来！
2.  📝 **术语统一**：
    自动把所有角色名提取到 `names.xlsx`，确保你不会把“Alice”一会翻成“爱丽丝”，一会翻成“阿李嫂”。
3.  🛡️ **代码保护**：
    集成了 Tag 保护功能，翻译前把代码变 Emoji，翻译后再变回来，防止机翻搞炸游戏。
4.  ⚡ **解放生产力**：
    你只管翻译，繁琐的**提取、去重、保护、还原**工作，全部交给哈基猫！

**现在，你只需要：**  
**🔥 双击 exe -> 点一下按钮 -> 完事！** 

---

## 🚀 核心功能 (v8.1)

| 功能模块 | 详细说明 |
| :--- | :--- |
| **🖥️ 图形界面 (GUI)** | **全面升级！** 采用 Tab 分页设计，提取与保护功能一站式管理，操作更顺滑。 |
| **📊 战果统计 (NEW)** | **心中有数！** 提取完成后自动弹窗，显示扫描文件数、人名数、对话数，工作量一目了然。 |
| **🧹 智能过滤** | **去伪存真！** 自动剔除代码、变量名、路径等垃圾文本，只提取人话。 |
| **🛡️ 集成 Tag 保护** | **无需切换！** 直接在工具内一键加密/解密翻译文件，防止翻译软件损坏 `{w=0.5}` 等标签。 |
| **🔄 增量更新** | **拒绝重复！** 如果 `tl` 文件夹已有翻译，工具会自动跳过，**只提取新增文本**。 |
| **🤖 AI 辅助** | **一键生成！** 自动输出 `AI_Prompt_Names.txt`，直接喂给 AI 统一角色译名。 

---

## 🚀 极速上手

### 方式一：直接下载 (推荐小白)
1. 前往 [**Releases 页面**](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest) 下载最新的 **`哈基猫盒子 v8.2.zip`**。
2. 解压，双击运行 **`OldCat_Translator.exe`**。
3. 选好游戏 `game` 目录，点击 **“开始提取”**。
4. **提取文本**：切换到“功能1”，点击开始提取。
5. **保护代码**：切换到“功能2”，一键加密/还原。
6. 去 `translate_output` 文件夹收菜！

### 方式二：源码运行 (推荐开发者)
如果你想自己修改代码或在 Mac/Linux 上运行：

```bash
# 1. 克隆仓库
git clone https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit.git

# 2. 安装依赖
pip install pandas openpyxl pyyaml

# 3. 运行脚本
python OldCat_GUI.py

```
---

## 📂 输出文件说明

工具运行完毕后，会在同目录下生成 `translate_output` 文件夹：

| 文件夹/文件 | 说明 |
| :--- | :--- |
| **`1_Excels/names.xlsx`** | **人名表**。这里全是角色名字，建议先翻这个，统一称呼。 |
| **`1_Excels/others.xlsx`** | **对话表**。游戏的主要剧情都在这里，直接拿去喂 AI 或手翻。 |
| **`2_RPY_Files/*.rpy`** | **生成的翻译文件**。可直接翻译替换回游戏。 |
| **`3_Emoji_Tools/*.xlsx`** | **Tag 保护映射表**。工具会自动调用，无需手动操作。 |
| **`AI_Prompt_Names.txt`** | **AI 提示词**。把这个文件内容发给 AI，让它帮你生成人名翻译表。 |
| **`Duplicate_Report.txt`** | **统计报告**。查看高频词汇。 |

---

## 📝 更新日志

### v8.2 (Latest) - 全能整合版
- 🎨 **重构**：采用全新的 Tab 分页界面，整合了“文本提取”与“Tag 保护”两大核心功能。
- ✅ **智能**：保护功能现在能自动识别路径和映射表，彻底告别手动拖文件。
- ✅ **优化**：统一了全局配置（游戏路径/语言），一次设置，全局通用。
- 
### v8.1 (Latest) - 战果统计版
- ✅ **新增**：任务完成后的详细统计弹窗（扫描数、提取数、分类统计）。
- ✅ **优化**：外部数据文件 (`.json`/`.yml`) 的扫描逻辑更加精准。
- ✅ **优化**：依赖库自动检测与静默安装体验。

---

<div align="center">

## 🤝 贡献与反馈

本项目由 **OldCat** & **Scorpio Weaver** 联合打造。  
如果你发现了 Bug，或者有好的建议，欢迎提 [议题](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/issues) 或 Pull Request！

**如果不麻烦的话，给个 ⭐ Star 支持一下吧！** 

</div>
