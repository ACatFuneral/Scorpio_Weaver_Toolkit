[![Latest Release](https://img.shields.io/github/v/release/ACatFuneral/Scorpio_Weaver_Toolkit?label=release)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest) [![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/blob/main/LICENSE) [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/) [![Stars](https://img.shields.io/github/stars/ACatFuneral/Scorpio_Weaver_Toolkit?style=social)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/stargazers)

<div align="center">

# ⚔️ Scorpio Weaver Toolkit (Localization Trinity)

</div>

<div align="center">

<!-- 在这里放一个你酷炫的 Logo -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/Scorpio.png" width="400" alt="Project Logo" />

### ✨ 一键完成Ren'Py游戏汉化前的所有准备工作 ✨

**你好，未来的汉化大佬！**

还在为手动给成千上万行代码添加 `_()` 而头疼吗？  
还在为游戏里人名翻译不统一而抓狂吗？  
还在为汉化后字体变成“口口口”而束手无策吗？  

**忘掉那些痛苦吧！**

这套 **Scorpio Weaver Toolkit** 工作流，就是你的终极答案。  
它将为你扫清汉化路上的三大障碍，让你能把宝贵的精力真正投入到“翻译”这件核心工作上。  
本工具集的作用是：**自动化地为游戏做好翻译前的所有准备工作**。  
它不能帮你翻译，但能让你接下来的翻译过程顺畅百倍！

准备好了吗？让我们开始解放生产力！

</div>

---

## 📍 项目简介

**Scorpio Weaver Toolkit** 不是一个单一的软件，而是一套为 Ren'Py 游戏开发者和汉化者量身打造的 **自动化预处理工作流**。它包含核心 Python 脚本和一套标准作业程序（SOP），旨在将汉化人员从繁琐、重复的准备工作中解放出来，全身心投入到翻译创作本身。

这套工具集的核心组件包括：

-   🤖 **自动化预处理 (`scripts/Scorpio_Weaver.py`)**: 智能识别需要翻译的文本，并自动添加 `_()` 标记。
-   📖 **术语表铸造机 (`scripts/Glossary_Forge.py`)**: 自动提取所有角色名称，一键生成术语表 (`.xlsx`)。
-   🪄 **字体替换魔法 (`scripts/z_font_hack.rpy` 模板)**: 一段简单的配置代码，解决所有中文字体显示问题。

---

## 🚀 功能特性

| 特性 | 描述 |
| :--- | :--- |
| 🧙 **配置向导 (v6.0+)** | **告别手动改代码！** 首次运行或使用 `--wizard` 参数，即可进入交互式向导，轻松生成 `config.json` 配置文件。 |
| ⌨️ **交互控制 (v6.0+)** | **掌控一切！** 在脚本运行时，可随时按 `[P]` 暂停/恢复，`[S]` 安全停止，`[I]` 查看实时统计，体验专业工具的驾驶舱。|
| 📊 **动态仪表盘 (v6.0+)** | **告别枯燥日志！** 华丽的动态进度条实时显示进度、速度(f/s)、预计剩余时间(ETA)，处理完成后更有专业级的详细报告。|
| 📖 **究极提取 (v5.5+)** | **究极创世引擎！** `Glossary_Forge.py` 现已能兼容各种“骚操作”写法，并能智能排除变量名！ |
| ⚙️ **配置分离 (v5.4+)** | **核心配置与代码完全分离！** 用户只需填写一次 `config.json`，未来更新脚本再也无需重复配置！ |
| 🔄 **混合动力 (v5.4+)** | `Glossary_Forge.py` 支持**混合动力模式**！优先读取共享配置，失败则自动切换为独立运行模式，灵活应对多项目需求。 |
| 🩺 **智能诊断 (v5.3+)** | 能精准识别因AI模型输出超限导致的失败，并提供清晰的错误报告，不再被模糊的网络错误困扰。 |
| 🤖 **AI 自动化核心** | 利用大语言模型（支持所有 OpenAI 兼容接口）的上下文理解能力，精准识别并包裹待翻译文本。 |
| 🛡️ **绝对安全**   | 默认采用非破坏性操作，生成 `.new.rpy` 新文件，为你保留了随时可以吃下的“后悔药”。 |
| 🪄 **字体完美显示** | 提供即插即用的字体替换方案，只需准备一个中文字体，即可彻底告别“口口口”。 |
| 👁️ **手动模式兼容** | 当AI“不听话”或遇到超大文件时，可无缝切换到 VS Code 正则模式，实现零成本、高精度的手动干预。 |
| 🔌 **轻量零依赖**  | 纯 Python 脚本，部分脚本会自动安装所需依赖库，无需复杂配置，下载即用。 |

---

## 📜 更新日志 (Changelog)

### 🤝v6.0.1 - 老猫高能紧急修复版 (2025-07-05)
**紧急Bug修复 (Hotfix):**
*   修复了一个因 `重试` 关键字被错误“汉化”成中文而导致的致命 `SyntaxError` (语法错误)，该错误会导致脚本无法运行。
*   现在所有用户都可以正常使用 v6.0 的全部功能了！

### 🤝v6.0 - 老猫高能版 (2025-07-04)
*   **【核弹级升级】引入全新交互体验！**
    *   **配置向导**：新增 `--wizard` 模式，首次使用或需要修改配置时，提供手把手的交互式问答，自动生成 `config.json`。
    *   **运行时控制**：现在可以在脚本运行时，通过键盘实时控制程序的**暂停(P)**、**停止(S)**和**信息查询(I)**。
    *   **动态仪表盘**：重构了输出界面，引入 `tqdm` 动态进度条，实时显示处理速度和预计剩余时间。
    *   **专业统计报告**：处理完成后，生成包含总耗时、实际工作时间、平均速度、处理时间分布等详细数据的专业报告。
*   **【健壮性MAX】** 大幅优化了错误处理和网络请求逻辑，引入自动重试和更清晰的错误提示。

### v5.5.1 - 究极创世引擎版 (2024-07-03)
*   **【究极创世引擎】`Glossary_Forge.py` 迎来史诗级加强！** 兼容性、智能识别、精准排除能力大幅提升。

*(更早版本的详细更新日志可在历史版本中追溯。)*

---

## 🛠️ 使用流程

### 阶段一：首次配置 (Initial Setup)
> 这是你第一次使用本工具集时需要完成的准备工作，**大部分操作只需要做一次**！

#### 1. 软件与环境
- [ ] 安装 [Python](https://www.python.org/downloads/) (**务必勾选 `Add Python to PATH`**)
- [ ] **备份你的整个游戏文件夹！(血的教训)**
- [ ] 准备一个你喜欢的 `.ttf` 或 `.otf` 中文字体
- [ ] 安装一个代码对比工具 (推荐: [Beyond Compare](https://www.scootersoftware.com/), [WinMerge](https://winmerge.org/), 或 [VS Code](https://code.visualstudio.com/))

#### 2. 下载并配置工具包
1.  **下载工具包**：前往本项目的 [**Releases 页面**](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest)，下载最新版本的 `.zip` 压缩包。
2.  **创建“军火库”**：在你电脑里新建一个**非中文路径**的文件夹，作为你的工具基地，例如 `D:\MyToolkit`。
3.  **解压入库**：将下载的 `.zip` 包解压，把里面的 `scripts` 文件夹完整地复制到你的“军火库”中。最终结构应如下：
    ```
    D:\MyToolkit\
    └── scripts\
        ├── Scorpio_Weaver.py
        ├── Glossary_Forge.py
        └── ... (其他文件)
    ```  
4.  **启动配置向导**：
    *   打开命令行/终端，进入你的“军火库”目录 (例如 `cd D:\MyToolkit`)。
    *   执行以下命令，启动配置向导：
      ```bash
      python scripts/Scorpio_Weaver.py --wizard
      ```
    *   根据提示，一步步输入你的 API 信息和游戏路径。完成后，会自动在 `scripts` 文件夹内生成一个 `config.json` 文件。        

    > **【重要提示！】**    
    > - `config.json` 是你的“遥控器”，**以后所有配置修改，只改这一个文件！**
    > - `config.json` 里的路径分隔符，请使用**双反斜杠 `\\`**，例如 `C:\\Games\\MyGame\\game`。
    > - 修改脚本 `.py` 文件内部的 `default_config` **不会有任何效果！**
    > - `config.json` 文件**必须**和 `Scorpio_Weaver.py`、`Glossary_Forge.py` 脚本放在同一个文件夹里！  

---

### 阶段二：日常运行 (Regular Use)
> 完成首次配置后，每次汉化都从这里开始。

#### 1. 自动打标，批量预处理(`Scorpio_Weaver.py`)
*   在你的“军火库”终端里，执行：
    ```bash
    python scripts/Scorpio_Weaver.py
    ```
*   确认配置无误后，输入 `yes` 开始。
*   **在运行途中，你可以随时按 `[P]` 暂停，`[S]` 停止，`[I]` 查看信息！**

    <div align="center">
        <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/新运行脚本提取.jpg" width="550" alt="新运行脚本" />
    </div>

    然后你就可以泡杯茶，抽支烟，看会剧，等待脚本为你自动完成所有繁重的工作吧！

<div align="center">
    <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/完成提取脚本1.jpg" width="550" alt="完成提取脚本1" />
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/新完成提取脚本2.jpg" width="550" alt="新完成提取脚本2" />
</div>

**注意：** 这一步不光要求速度，道德审核也很严重。有报错是正常的，毕竟API有波动。  
如果报错超多，或遇到道德审核问题，别着急，请直接跳到下面的 **【最终手段：手动正则决战】**。

#### 2. 铸造术语，灵魂熔炉启动！(`Glossary_Forge.py`)  
> 翻译的灵魂在于统一。
> 这一步能够帮你把所有角色名都抓出来，做成一个Excel术语表，确保“艾米丽”不会被翻译成“爱美丽”。  
*   在同一个终端里，执行：
    ```bash
    python scripts/Glossary_Forge.py
    ```
*   脚本会自动读取 `config.json`，运行后在 `scripts` 目录下生成 `glossary.xlsx`。
    <div align="center">
        <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/运行术语库.jpg" width="550" alt="运行术语表" />
    </div>  

*   **填写译名：** 打开生成的 `glossary.xlsx`，在 `dst` 列填上你定好的译名。

#### 3. 完成收尾工作
> 脚本处理完成后，剩下的就是收尾工作了。详细的操作指南，如**审查合并、替换字体、生成翻译**等，都已为你整理在下方的 **【附录】** 中，可按需展开查看。  

---

## 📚 附录：详细操作指南

<details>  
<summary><strong>💀 附录 A：审查与合并 - 过河拆桥(点击展开)</strong></summary>

> 这是保证质量的关键环节，不可跳过！

1.  **对比**: 使用 Beyond Compare 等工具，仔细对比原始 `.rpy` 和新生成的 `.new.rpy` 文件。
2.  **确认**: 确认 AI 的修改无误后，删除原文件，并将 `.new.rpy` 重命名，去掉 `.new` 后缀。
3.  **清理**: **所有文件都确认完毕后，把没用的 `.new.rpy` 备份全部删除！**

</details>

<details>  
<summary><strong>🪄 附录 B：替换字体 - 施展终极魔法(点击展开)</strong></summary>

> 有时候会遇到骚作者，在文本里硬编码字体！这时候我们就需要魔法卷轴来帮忙了！    
> **注：如果作者很正常，没有在文本中内嵌字体的习惯，那么这一步可直接跳过。** 

1.  **创建目录**: 在 `game/` 目录下，创建 `tl/Chinese/fonts` 文件夹。（`Chinese`可替换为你自己的翻译语言名）
2.  **放入字体**: 把你准备好的中文字体文件放进去。
3.  **部署脚本**: 在 `game/` 目录下，新建 `z_font_hack.rpy` 文件，把我们提供的模板代码复制进去并按需修改。
    ```python
    # z_font_hack.rpy 示例
    init -999 python:
        font_replacement_map = {
            "DejaVuSans.ttf": "tl/Chinese/fonts/your_font.ttf",
            "Action_Man.ttf": "tl/Chinese/fonts/your_font.ttf"
        }
        config.font_replacement_map.update(font_replacement_map)
    ```

</details>

<details>  
<summary><strong>⚔️ 附录 C：生成翻译 & 总攻开启(点击展开)</strong></summary>

一切就绪！现在你可以：

1.  打开 Ren'Py Launcher，点击 **"Generate Translations"** (生成翻译)。
2.  把生成的待翻译文件 (`game/tl/Chinese` 目录下) 扔进 **Lingua**, **AiNee** 或任何你喜欢的翻译工具。
3.  **导入你刚刚制作的 `glossary.xlsx` 术语表**，开始你的翻译之旅！

</details>

<details>  
<summary><strong>💥 附录 D：最终手段 - 手动正则决战(点击展开)</strong></summary>

> 当遇到AI因“道德审查”罢工，或文件过大导致处理失败时，切换到零成本、高精准的手动模式。

#### 第一步：开启“神之眼” (VS Code 全局正则搜索)
1.  用 **VS Code** 打开你的游戏 `game` 文件夹。
2.  按下 `Ctrl + Shift + F`，开启全局搜索。
3.  **点击 `.*` 图标，启用正则表达式模式。**
4.  输入下面的“索敌咒语”，精准定位需要翻译的文本。

#### 第二步：吟唱【你的究极完全体咒语库】
*   **咒语一：查找 `renpy.input()` 中的提示文本**
    ```regex
    renpy\.input\s*\(\s*"([^"]+)"
    ```
*   **咒语二：查找 `Character()` 定义中的角色名**
    ```regex
    Character\s*\(\s*"([^"]+)"
    ```
*   **咒语三：查找 `show text` 显示的文本**
    ```regex
    show\s+text\s+"([^"]+)"
    ```
*   **咒语四：【狙击枪】查找被赋值的`长字符串` (主抓对话/描述)**
    ```regex
    \$\s*\w+\s*=\s*"([^"]{10,})"
    ```
*   **咒语五：【冲锋枪】查找被赋值的`短字符串` (主抓UI/关键词)**
    ```regex
    \$\s*\w+\s*=\s*"([^"]{2,9})"
    ```
*   **咒语六：【霰弹枪】查找通用函数调用参数 (威力巨大，误伤率高)**
    ```regex
    \w+\s*\(\s*[^)]*\b"([^"/]+?)"
    ```
    > **建议使用顺序**：从上到下依次使用咒语。先用“狙击枪”解决大部分，再用“冲锋枪”补漏，最后才考虑动用“霰弹枪”。  
    > **注**：咒语六威力巨大，可能会匹配到某些不需要翻译的项，会误伤友军，请谨慎使用并仔细甄别结果。

#### 第三步：手动“点穴” (应用 `_()`)
VS Code的搜索结果会像清单一样列出，点击即可跳转。你的任务，就是用智慧判断是否需要翻译，然后手动“附魔”。

*   **方法一：首尾包抄**
    1.  光标定位到字符串的第一个引号 `"` 前，输入 `_(`。
    2.  光标移动到字符串最后一个引号 `"` 后，输入 `)`。

*   **方法二：“选中环绕” (高手推荐)**
    1.  用鼠标双击字符串，VS Code会自动选中它（包括引号）。
    2.  直接按下 `(` 左括号键，VS Code会自动用一对 `()` 包起来。
    3.  在第一个括号前补上 `_` 即可。**这是程序员的必备神技！**

> **手动模式优势**: 零API成本、无视AI审查、速度极快、精准可控、无惧文件大小！    

</details>  

---

## 📢 特别声明

这套工具不是万能的，记住，它**会报错、会遗漏**，也许还有各种我没测试到的问题。  
它的核心价值，是最大幅度地减轻你的重复劳动，让你更省心地投入翻译。

**请牢记，AI也不是神：**

把AI脑瓜子干冒烟它也搞不定？ **是的，没错！**

很多代码它就是处理不了？ **的确如此，千真万确！**

自动版用不了时，手动正则永远是你最可靠的后盾！

---

**只有人和AI搭配，才能真正地所向披靡！**

恭喜你！这趟奇妙的旅程已经到达终点，你已完全掌握这套神器的使用方法！

### **去吧，英雄！**
