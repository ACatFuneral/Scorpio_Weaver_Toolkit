[![Latest Release](https://img.shields.io/github/v/release/ACatFuneral/Scorpio_Weaver_Toolkit)](https://github.com/ACatFuneral/Scorpio_Weaver_Toolkit/releases/latest)
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
-   🪄 **字体替换魔法 (`z_font_hack.rpy` 模板)**: 一段简单的配置代码，解决所有中文字体显示问题。

---

## 🚀 功能特性

| 特性 | 描述 |
| :--- | :--- |
| ⚙️ **配置分离 (v5.4新增)** | **核心配置与代码完全分离！** 用户只需填写一次 `config.json`，未来更新脚本再也无需重复配置！ |
| 🔄 **混合动力 (v5.4.1新增)** | `Glossary_Forge.py` 支持**混合动力模式**！优先读取共享配置，失败则自动切换为独立运行模式，灵活应对多项目需求。 |
| 📖 **术语究极提取(v5.5新增)** | **究极飞升！** `Glossary_Forge.py` 现已能兼容各种“骚操作”写法，如 `DynamicCharacter`、单/双引号，并能智能排除变量名！ |
| 🤖 **AI 自动化核心** | 利用大语言模型（支持所有 OpenAI 兼容接口）的上下文理解能力，精准识别并包裹待翻译文本。 |
| ախ **智能诊断 (v5.3新增)** | 能精准识别因AI模型输出超限导致的失败，并提供清晰的错误报告，不再被模糊的网络错误困扰。 |
| 📖 **术语高度统一** | **双核搜索**提取角色名，生成 Excel 术语表，从源头上杜绝“张三/李四”人名不统一的尴尬。 |
| 🛡️ **绝对安全**   | 默认采用非破坏性操作，生成 `.new.rpy` 新文件，为你保留了随时可以吃下的“后悔药”。 |
| 🪄 **字体完美显示** | 提供即插即用的字体替换方案，只需准备一个中文字体，即可彻底告别“口口口”。 |
| 👁️ **手动模式兼容** | 当AI“不听话”或遇到超大文件时，可无缝切换到 VS Code 正则模式，实现零成本、高精度的手动干预。 |
| 🔌 **轻量零依赖**  | 纯 Python 脚本，部分脚本会自动安装所需依赖库，无需复杂配置，下载即用。 |

---

## 📜 更新日志 (Changelog)

### v5.5 - 究极飞升版 (2024-07-04)
*   **【究极飞升】`Glossary_Forge.py` 迎来史诗级加强！**
    *   **兼容性MAX**：现在能完美兼容 `Character` 和 `DynamicCharacter` 的定义。
    *   **智能识别**：能同时处理单引号 `'` 和双引号 `"` 包裹的字符串。
    *   **精准排除**：能自动识别并排除方括号 `[]` 包裹的变量名和 `name=None` 的情况，提取结果更纯净。
*   **【文档同步】** 全面更新 `README.md`，以匹配究极飞升版的强大功能。

*(更早版本的详细更新日志可在历史版本中追溯。)*

---
## 🛠️ 使用流程

### 第零步：战前的配置与准备 (Initial Setup)
> 这是你第一次使用本工具集时，需要完成的准备工作。

#### 1. 软件与环境
- [ ] 安装 [Python](https://www.python.org/downloads/) (**务必勾选 `Add Python to PATH`**)
- [ ] **备份你的整个游戏文件夹！(血的教训)**
- [ ] 准备一个你喜欢的 `.ttf` 或 `.otf` 中文字体
- [ ] 安装一个代码对比工具 (推荐: [Beyond Compare](https://www.scootersoftware.com/), [WinMerge](https://winmerge.org/), 或 [VS Code](https://code.visualstudio.com/))

#### 2. 文件与文件夹结构
为了让工具正常工作，请按照以下结构组织你的文件：
1.  在你电脑里新建一个文件夹，作为你的“军火库”，任意你喜欢的、方便你找的、`非中文`的文件夹即可。例如 `D:\4396`。
2.  下载本项目的 `.zip` 包并解压，将里面的 `scripts` 文件夹完整地复制到你的“军火库”中。

最终你的文件夹结构应该如下：

    D:\4396\
    └── scripts\
        ├── Scorpio_Weaver.py
        ├── Glossary_Forge.py
        └── config.json (如果不存在，首次运行会自动生成)

---

### 第一步：配置你的“遥控器” (`config.json`)
> 这是整个流程的核心，**只需要做一次**！以后无论脚本怎么更新，你的配置都会被保留。    

*   **重要提示**: `config.json` 文件**必须**和 `Scorpio_Weaver.py`、`Glossary_Forge.py` 脚本放在同一个文件夹里！

 1.  **找到配置文件**: 在 `scripts` 文件夹里找到 `config.json` 文件。    

     *   如果找不到，直接运行一次 `scripts/Scorpio_Weaver.py`，它会自动为你创建一个（文件名，路径可改，后面也有提示）
 2.  **填写配置**: 用任何文本编辑器（如记事本、VS Code）打开 `config.json`。  
     *   **【警告！】**
     -   你**永远**只需要修改 `config.json` 这一个文件来调整配置。
     -   脚本文件（`.py`）内部的 `default_config` 仅用于首次生成 `config.json`，**修改它不会产生任何效果！**  
3.  **修改示例**:
    ```json
    {
      "API_KEY": "sk-xxxxxxxxxxxxxxxxxxx",
      "BASE_URL": "https://api.oneapi.run/v1",
      "MODEL_NAME": "gemini-1.5-pro-latest",
      "GAME_DIRECTORY": "G:\\你的游戏路径\\game",
      "EXCLUDE_FILES": [
        "gui.rpy",
        "options.rpy"
      ]
    }
    ```
   **【重要、必读】**:    
   -   `API_KEY`, `BASE_URL`, `MODEL_NAME`, `GAME_DIRECTORY` 是必填项！  
   -   `GAME_DIRECTORY` 中的路径分隔符，请使用**双反斜杠 `\\`**，例如 `C:\\Users\\YourName\\MyGame\\game`。
   -   `EXCLUDE_FILES` 是一个**排除列表**，用于跳过不需要处理的文件。你可以手动添加或删减里面的项，只需保证是 `"文件名"` 的格式，并用 `,` 分隔即可。
 4.  **保存 `config.json` 文件。** 你的“遥控器”就设置好了！     

---

### 第二步：自动打标，批量预处理 (`Scorpio_Weaver.py`) 

> 这是最核心的工具，用于批量给代码添加翻译标记。

**运行脚本**: 在项目根目录打开终端，执行：

    python scripts/Scorpio_Weaver.py

   <div align="center">
   <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/运行提取脚本.jpg" width="550" alt="运行脚本" />
   </div>  
  
   注：`Scorpio_Weaver.py` 文件名是可改的，路径是可改可删的，但要确保和 `config.json` 配置表在同一目录，你可以改成任意方便你操作的非中文文件名，比如：`777.py`。
    
   看到提示后输入 `yes` 回车。  
   
   <div align="center">
   <img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/完成提取脚本.jpg" width="550" alt="完成脚本" />
   </div>
  
   然后就可以泡杯茶，抽支烟，看会剧，等待脚本为你自动完成所有繁重的工作吧！    

 **注意：** 这一步不光要求速度，道德审核也很严重。有少量报错是正常的，毕竟API有波动。如果报错超多，或遇到道德审核问题，别着急，请直接跳到下面的 **【最终手段：手动正则决战】**。

---

### 第三步：铸造术语，灵魂熔炉启动！ (`Glossary_Forge.py`)
> 翻译的灵魂在于统一。
> 这个工具能帮你把所有角色名都抓出来，做成一个Excel术语表，确保“艾米丽”不会被翻译成“爱美丽”。

**运行脚本**: 在项目根目录打开终端，执行：

    python scripts/Glossary_Forge.py

注：同上，依然是可改可删的，依然要确保和 `config.json` 配置表在同一目录。      
    
<div align="center">
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/运行术语库.jpg" width="550" alt="运行术语表" />
</div>
    
**填写译名**: 它会智能地决定使用哪个游戏路径（优先 `config.json`），运行结束后，会在同目录下生成 `glossary.xlsx`。打开它，在 `dst` 列填上你定好的译名。

---

### 第四步：审查与合并 (过河拆桥！)
⚠️ **这是保证质量的关键环节，不可跳过！**  
1.  **对比**: 使用 Beyond Compare 等工具，仔细对比原始 `.rpy` 和新生成的 `.new.rpy` 文件。
2.  **确认**: 确认 AI 的修改无误后，删除原文件，并将 `.new.rpy` 重命名，去掉 `.new` 后缀。
3.  **清理**: **所有文件都确认完毕后，把没用的 `.new.rpy` 备份全部删除！**

---

### 第五步：替换字体 (施展终极魔法！`z_font_hack.rpy`)  
> 有时候会遇到骚作者，在文本里硬编码字体！这时候我们就需要魔法卷轴来帮忙了！    
> **注：如果作者很正常，且没有在文本中内嵌字体的习惯，那么这一步可直接跳过。** 

1.  **创建目录**: 在 `game/` 目录下，创建 `tl/Chinese/fonts` 文件夹。（`Chinese`可替换为你自己的翻译语言名）
2.  **放入字体**: 把你准备好的中文字体文件放进去。
3.  **部署脚本**: 在 `game/` 目录下，新建 `z_font_hack.rpy` 文件或者把 `z_font_hack.rpy` 文件复制粘贴过去也行，然后把项目中的模板代码复制进去并按需修改。

        # z_font_hack.rpy 示例
        init -999 python:
            font_replacement_map = {
                "DejaVuSans.ttf": "tl/Chinese/fonts/your_font.ttf",
                "Action_Man.ttf": "tl/Chinese/fonts/your_font.ttf"
            }
            config.font_replacement_map.update(font_replacement_map)

---

### 第六步：生成翻译 & 总攻！
一切就绪！现在你可以：

1.  打开 Ren'Py Launcher，点击 **"Generate Translations"** (生成翻译)。
2.  把生成的待翻译文件 (`game/tl/Chinese` 目录下) 扔进 **Lingua**, **AiNee** 或任何你喜欢的翻译工具。
3.  **导入你刚刚制作的 `glossary.xlsx` 术语表**，开始你的翻译之旅！

---

## 💥 最终手段：手动正则决战
> 当遇到AI因“道德审查”罢工，或文件过大导致处理失败时，切换到零成本、高精准的手动模式。  

#### 第一步：开启“神之眼” (VS Code 全局正则搜索)
1.  用 **VS Code** 打开你的游戏 `game` 文件夹。
2.  按下 `Ctrl + Shift + F`，开启全局搜索。
3.  **点击 `.*` 图标，启用正则表达式模式。**
4.  输入下面的“索敌咒语”，精准定位需要翻译的文本。

#### 第二步：吟唱【你的专属正则咒语库】
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
*   **咒语四：查找被赋值的长字符串 (通常是描述或UI文本)**
    ```regex
    \$\s*\w+\s*=\s*"([^"]{10,})"
    ```
*   **咒语五：查找通用函数调用中的字符串参数 (较宽泛，会匹配到某些不需要翻译的项，甚至会重复角色名，需甄别、自我筛选)**
    ```regex
    \w+\s*\(\s*[^)]*\b"([^"/]+?)"
    ```

#### 第三步：手动“点穴” (应用 `_()`)
VS Code的搜索结果会像清单一样列出，点击即可跳转。你的任务，就是用智慧判断是否需要翻译，然后手动“附魔”。

*   **方法一：首尾包抄**
    1.  光标定位到字符串的第一个引号 `"` 前。
    2.  输入 `_(`。
    3.  光标移动到字符串最后一个引号 `"` 后。
    4.  输入 `)`。

*   **方法二：“选中环绕” (高手推荐)**
    1.  用鼠标双击字符串（如 `Holy shit！`），VS Code会自动选中它（包括引号）。
    2.  直接按下 `(` 左括号键。
    3.  奇迹发生！VS Code会自动用一对 `()` 把你选中的内容包起来。
    4.  现在只需在第一个括号前补上 `_` 即可。**这是程序员的必备神技！**

> **手动模式优势**: 零API成本、无视AI审查、速度极快、精准可控、无惧文件大小！是应对疑难杂症的最终解决方案。

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

恭喜你！这趟奇妙的旅程已经到达终点，你已完全掌握这套神器的使用方法了！

### **去吧，英雄！**
