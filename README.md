<div align="center">

# ⚔️ Scorpio Weaver Toolkit (Localization Trinity)

</div>

<div align="center">

<!-- 在这里放一个你酷炫的 Logo -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/Scorpio.png" width="200" alt="Project Logo" />


### ✨ 一键完成Ren'Py游戏汉化前的所有准备工作 ✨

**还在手动打`_()`？还在为名词不统一抓狂？还在被“口口口”字体劝退？**  
**这套工作流，就是你的终极答案。**

| [**📜 中文文档**](#-项目简介) | [**🇬🇧 English Docs**](README_en.md) |
|---|---|

</div>

![Release](https://img.shields.io/badge/release-v1.0-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/YOUR_REPO?style=social)

---

## 📍 项目简介

**本地化三神器** 不是一个单一的软件，而是一套为 Ren'Py 游戏开发者和汉化组量身打造的 **自动化预处理工作流**。它包含三个核心 Python 脚本和一套标准作业程序（SOP），旨在将汉化人员从繁琐、重复的准备工作中解放出来，全身心投入到翻译创作本身。

这套工具集的核心组件包括：

-   🤖 **AI自动打标器 (`auto_tagger.py`)**: 智能识别需要翻译的文本，并自动添加 `_()` 标记。
-   📖 **术语表铸造机 (`glossary_builder.py`)**: 自动提取所有角色名称，一键生成术语表 (`.xlsx`)。
-   🪄 **字体替换魔法 (`z_font_hack.rpy`)**: 一段简单的配置代码，解决所有中文字体显示问题。

---

## 🚀 功能特性

| 特性 | 描述 |
| :--- | :--- |
| **🤖 AI 自动化核心** | 利用大语言模型（支持所有 OpenAI 兼容接口）的上下文理解能力，精准识别并包裹待翻译文本，告别人工打标。 |
| **📖 术语高度统一** | 自动提取角色名，生成 Excel 术语表，从源头上杜绝“张三/李四”人名不统一的尴尬。 |
| **🛡️ 绝对安全** | 默认采用非破坏性操作，生成 `.new.rpy` 新文件，为你保留了随时可以吃下的“后悔药”。 |
| **🪄 字体完美显示** | 提供即插即用的字体替换方案，只需准备一个中文字体，即可彻底告别“口口口”。 |
| **👁️ 手动模式兼容** | 当AI“不听话”或遇到超大文件时，可无缝切换到 VS Code 正则模式，实现零成本、高精度的手动干预。 |
| **🔌 轻量零依赖** | 纯 Python 脚本，无需安装复杂的依赖库，下载即用，绿色环保。 |

---

## 🛠️ 使用流程

### 第零步：环境准备 (Checklist)
- [ ] 安装 [Python](https://www.python.org/downloads/) (**务必勾选 `Add Python to PATH`**)
- [ ] 准备好你的 [AI API Key 和 Base URL](https://#)
- [ ] **备份你的整个游戏文件夹！(血的教训)**
- [ ] 准备一个你喜欢的 `.ttf` 或 `.otf` 中文字体
- [ ] 安装一个代码对比工具 (推荐: [Beyond Compare](https://www.scootersoftware.com/), [WinMerge](https://winmerge.org/), 或 [VS Code](https://code.visualstudio.com/))

---

### 第一步：自动打标 (主力战舰出港！)
1.  **配置脚本**: 打开 `auto_tagger.py`，填写顶部的 **【配置区】**。
    ```python
    # 【配置区】==========
    API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 你的API密钥
    BASE_URL = "https://api.xxxx.com/v1"         # 你的API地址
    MODEL_NAME = "gemini-1.5-pro-latest"         # 你使用的模型

    GAME_DIRECTORY = r'G:\Path\To\YourGame\game' # 【重中之重】游戏game文件夹路径
    OVERWRITE_FILES = False                      # 【安全开关】保持False！
    ```
2.  **运行脚本**: 在脚本所在目录打开终端，执行：
    ```bash
    python auto_tagger.py
    ```
    看到提示后输入 `yes` 回车，然后泡杯茶，静待奇迹发生。

---

### 第二步：铸造术语 (灵魂熔炉启动！)
1.  **配置脚本**: 打开 `glossary_builder.py`，同样修改 `GAME_DIRECTORY` 指向你的 `game` 目录。
2.  **运行脚本**:
    ```bash
    python glossary_builder.py
    ```
3.  **填写译名**: 运行结束后，会在同目录下生成 `glossary.xlsx`。打开它，在 `dst` 列填上你定好的译名。

---

### 第三步：审查与合并 (过河拆桥！)
⚠️ **这是保证质量的关键环节，不可跳过！**
1.  **对比**: 使用 Beyond Compare 等工具，仔细对比原始 `.rpy` 和新生成的 `.new.rpy` 文件。
2.  **确认**: 确认 AI 的修改无误后，删除原文件，并将 `.new.rpy` 重命名，去掉 `.new` 后缀。
3.  **清理**: **所有文件都确认完毕后，把没用的 `.new.rpy` 备份全部删除！**

---

### 第四步：替换字体 (施展终极魔法！)
1.  **创建目录**: 在 `game/` 目录下，创建 `tl/Chinese/fonts` 文件夹。
2.  **放入字体**: 把你准备好的中文字体文件放进去。
3.  **部署脚本**: 在 `game/` 目录下，新建 `z_font_hack.rpy` 文件，把我们提供的代码复制进去并按需修改。
    ```python
    # z_font_hack.rpy 示例
    init python:
        font_replacement_map = {
            "DejaVuSans.ttf": "tl/Chinese/fonts/your_font.ttf", # 左边是原字体名，右边是你的中文字体路径
            "Action_Man.ttf": "tl/Chinese/fonts/your_font.ttf"
        }
    ```

---

### 第五步：生成翻译 & 总攻！
一切就绪！现在你可以：
1.  打开 Ren'Py Launcher，点击 **"Generate Translations"**。
2.  把生成的待翻译文件 (`game/tl/Chinese` 目录下) 扔进 **Lingua**, **AiNee** 或你喜欢的任何翻译工具。
3.  **导入你刚刚制作的 `glossary.xlsx` 术语表**，开始你的翻译之旅！

---

## 🖼️ 效果演示

（兄弟，这里强烈建议你录个GIF，展示一下运行脚本前后的代码对比，或者游戏里字体从口口口变成正常中文的效果，会非常直观！）

**处理前 (Before):**
```rpy
"You can't do that!"
$ player_name = "Hero"
$ renpy.input("What is your name?")
