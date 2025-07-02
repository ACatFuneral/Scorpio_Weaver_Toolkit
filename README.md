<div align="center">

# ⚔️ Scorpio Weaver Toolkit (Localization Trinity)

</div>

<div align="center">

<!-- 在这里放一个你酷炫的 Logo -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/Scorpio.png" width="350" alt="Project Logo" />


### ✨ 一键完成Ren'Py游戏汉化前的所有准备工作 ✨
**你好，未来的汉化大佬！**
**还在为手动给成千上万行代码添加翻译符号 _() 而头疼吗？**
**还在为游戏里人名翻译不统一而抓狂吗？**
**还在为汉化后字体变成“口口口”而束手无策吗？**
**忘掉那些痛苦吧！**

**这套工作流，就是你的终极答案。**
**现在为你带来了这套“本地化”组合包，它将为你扫清汉化路上的三大障碍，让你能把宝贵的精力真正投入到“翻译”这件核心工作上。**
**本工具集的作用是：自动化地为游戏做好翻译前的所有准备工作。它不能帮你翻译，但能让你接下来的翻译过程顺畅百倍！**
**准备好了吗？让我们开始解放生产力！！**

---

## 📍 项目简介

**Scorpio Weaver Toolkit** 不是一个单一的软件，而是一套为Ren'Py 游戏开发者和汉化者量身打造的 **自动化预处理工作流**。它包含三个核心 Python 脚本和一套标准作业程序（SOP），旨在将汉化人员从繁琐、重复的准备工作中解放出来，全身心投入到翻译创作本身。

这套工具集的核心组件包括：

-   🤖 **AI自动打标器 (`Scorpio_Weaver.py`)**: 智能识别需要翻译的文本，并自动添加 `_()` 标记。
-   📖 **术语表铸造机 (`Glossary_Forge.py`)**: 自动提取所有角色名称，一键生成术语表 (`.xlsx`)。
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

### 第零步：战前环境准备 (Checklist)
- [ ] 安装 [Python](https://www.python.org/downloads/) (**务必勾选 `Add Python to PATH`**)
- [ ] 准备好你的 [AI API Key 和 Base URL](https://#)
- [ ] **备份你的整个游戏文件夹！(血的教训)**
- [ ] 准备一个你喜欢的 `.ttf` 或 `.otf` 中文字体
- [ ] 安装一个代码对比工具 (推荐: [Beyond Compare](https://www.scootersoftware.com/), [WinMerge](https://winmerge.org/), 或 [VS Code](https://code.visualstudio.com/))

---

### 第一步：自动打标 (主力战舰出港！)
1.  **配置脚本**: 打开 `Scorpio_Weaver.py`，填写顶部的 **【配置区】**。
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
    python Scorpio_Weaver.py
    ```
    看到提示后输入 `yes` 回车。
<div align="center">

<!-- 插图 -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/运行提取脚本.jpg" width="200" alt="Project Logo" />

**然后就泡杯茶，看着脚本为你自动完成所有繁重的工作吧！**

<div align="center">

<!-- 插图 -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/完成提取脚本.jpg" width="200" alt="Project Logo" />
---
##注意
**这一步不光要求速度，道德审核也很严重，阿西吧！**
**有报错是正常的哈，毕竟API有波动就有抽风的情况，报错少可以选择手动提取，报错超多建议检查网络或配置后重新来过。**
**别着急，如果遇到道德审核或者你的API不咋滴，后面还有手动的办法！**


### 第二步：铸造术语 (灵魂熔炉启动！)
**翻译的灵魂在于统一。这个工具能帮你把所有角色名都抓出来，做成一个Excel术语表，确保“艾米丽”不会被翻译成“爱美丽”。**
1.  **配置脚本**: 打开 `Glossary_Forge.py`，同样修改 `GAME_DIRECTORY` 指向你的 `game` 目录。
2.  **运行脚本**:
    ```bash
    python Glossary_Forge.py.py
    ```
<div align="center">

<!-- 插图 -->
<img src="https://raw.githubusercontent.com/ACatFuneral/Scorpio_Weaver_Toolkit/main/images/运行术语库.jpg" width="200" alt="Project Logo" />

3.  **填写译名**: 运行结束后，会在同目录下生成 `glossary.xlsx`。打开它，在 `dst` 列填上你定好的译名。

---

### 第三步：审查与合并 (过河拆桥！)
⚠️ **这是保证质量的关键环节，不可跳过！**
1.  **对比**: 使用 Beyond Compare 等工具，仔细对比原始 `.rpy` 和新生成的 `.new.rpy` 文件。
2.  **确认**: 确认 AI 的修改无误后，删除原文件，并将 `.new.rpy` 重命名，去掉 `.new` 后缀。
3.  **清理**: **所有文件都确认完毕后，把没用的 `.new.rpy` 备份全部删除！**

---

### 第四步：替换字体 (施展终极魔法！)
**有时候会遇到骚作者，在文本里嵌入字体的！这时候我们就需要魔法卷轴来帮忙了！**
1.  **创建目录**: 在 `game/` 目录下，创建 `tl/你的中文目录：可以是Chinese，可以是chinese，随你喜欢/fonts` 文件夹。
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
1.  打开 Ren'Py Launcher，点击 **"Generate Translations（生成翻译文件）"**。
2.  把生成的待翻译文件 (`game/tl/Chinese` 目录下) 扔进 **Lingua**, **AiNee** 或任何你喜欢的翻译工具。
3.  **导入你刚刚制作的 `glossary.xlsx` 术语表**，开始你的翻译之旅！

---

## 🖼️ 最后的战役

**如果说你遇到的严重的道德审核，以及要提取的文件超大（超过了我们设置的500k的阈值）**

这时候你可以采取两种办法：
一、分割！
把文件挪走，然后拆分成若干个小的文件，让脚本去读取小文件，等你完成替换之后再把新的小文件挨个移回大文件中。

二、手动解决：
你需要的神兵利器：
一个强大的代码编辑器，比如 VS Code (Visual Studio Code)。它免费、强大，并且拥有顶级的全局搜索和正则匹配功能。（Sublime Text, Notepad++ 也可以，但VS Code是首选）
作战步骤：
战场分割 (File Triage)：
按照你的想法，在运行“最终圣剑”脚本前，先把那些高风险文件（如script.rpy, gallery.rpy等）从game文件夹里暂时移走，放到一个单独的“待处理”文件夹里。然后对剩下的低风险文件运行自动化脚本。

开启“神之眼” (Global Search with Regex)：
用VS Code打开你那个“待处理”文件夹。
按下 Ctrl + Shift + F，打开全局搜索面板。
在搜索框旁边，点亮一个看起来像 .* 的小图标，这就是**“启用正则表达式”**的开关。
输入“索敌咒语” (The Regex Patterns)：

现在，你可以在搜索框里输入我们专门设计的“正则咒语”，来一次性找到所有需要处理的“天坑”代码。


【你的专属正则咒语库】

咒语一：查找所有renpy.input()里的文本
renpy\.input\s*\(\s*"([^"]+)"
效果：它会立刻列出所有文件中，所有renpy.input("...")里面的那段文本。

咒语二：查找所有Character()里的角色名
Character\s*\(\s*"([^"]+)"
效果：找到所有define x = Character("角色名")里的“角色名”。

咒语三：查找所有show text后面的文本
show\s+text\s+"([^"]+)"

咒语四：查找所有赋值给变量的、可能是对话的字符串 (这个比较复杂，但很强大)
\$\s*\w+\s*=\s*"([^"]{10,})"
效果：查找所有$ 变量 = "..."的行，但只显示那些字符串长度超过10个字符的（为了过滤掉$ flag = "win"这种短的代码变量）。

咒语五：查找所有函数调用里的字符串参数 (这是一个比较通用的“大招”)
\w+\s*\(\s*[^)]*\b"([^"/]+?)"
效果：查找大多数函数调用里的字符串，并且会尝试排除掉像"images/a.png"这样的文件路径。

手动“点穴” (Manual Application of _())：
VS Code的搜索结果会像一个清单一样列出来，你可以点击每一条结果，编辑器就会自动跳转到对应的代码行。
现在，轮到你——人类指挥官——出场了。你看着跳转到的代码行，用你的智慧判断：“这句是不是给玩家看的？”
如果是，你就手动在字符串外面加上_()。
如果不是（比如它是个文件名），你就直接跳过，看下一条搜索结果。

你的“附魔”工作台
1.	左边是“索敌结果”列表：VS Code的全局搜索结果。
2.	右边是“代码操作台”：点击左边的结果，右边就会自动跳转到对应的代码行。
“附魔”手法详解
假设你点击了一条搜索结果，右边的代码操作台显示了这一行：
$ fn = renpy.input("Fuck!", default=persistent.galleryfn)
你的任务，就是把 _() 加在那个字符串的外面。
手法一：经典“首尾包抄”
1.	把光标移动到字符串的第一个引号 " 前面。
2.	输入 _(。
3.	代码会变成：$ fn = renpy.input(_("Fuck!", default=persistent.galleryfn)
4.	把光标移动到字符串的最后一个引号 " 后面。
5.	输入 )。
6.	附魔完成！ 最终代码：
$ fn = renpy.input(_("Fuck!"), default=persistent.galleryfn)

手法二：高手“选中环绕” (VS Code快捷键)
这是更快、更不容易出错的方法，强烈推荐你练习一下！
1.	用鼠标双击那个字符串 " Fuck!"，VS Code会自动帮你选中整个字符串（包括引号）。
2.	现在，直接按下 ( （左括号）键。
3.	奇迹发生！ VS Code会自动用一对括号 () 把你选中的内容包起来！
代码会变成：$ fn = renpy.input(("Fuck!"), default=persistent.galleryfn)
4.	现在，你只需要把光标移动到第一个括号 ( 前面，补上一个下划线 _ 就行了。
5.	附魔完成！
（这个“选中环绕”功能对 "、'、[、{ 等所有成对的符号都有效，是程序员的必备神技！）

你的工作流程就是：
1.	在左边的搜索结果列表里，从上到下，挨个点击。
2.	每点击一个，就在右边的代码操作台里，用你喜欢的手法给它“附魔”。
3.	按 Ctrl + S 保存你对这个文件的修改。
4.	继续点击下一条搜索结果。
这个过程虽然是手动的，但因为有“索敌咒语”帮你定位，你的效率会非常高。而且最重要的是，每一步都在你的掌控之中，100%安全可靠！

这个方案的巨大优势
•	零API成本：整个过程完全在你本地电脑上进行，不花一分钱。
•	无视道德审核：没有任何AI会来审查你的文本，你想怎么处理就怎么处理。
•	速度极快：全局正则搜索的速度是毫秒级的，比任何API请求都快。
•	精准可控：最终的决定权在你手上，你可以100%确保不会改错任何一行代码。
•	无视文件大小：别说500KB，就算是5MB的超大文件，VS Code处理起来也毫无压力。

## 特别声明
这套工具不是万能的，记住，会报错，会漏，也许还会有各种各样我没测试到的问题。
它只是最大幅度的把Ren'PySDK提取不了的文本帮你提取出来，减轻一些你的工作量，让你翻译的时候更省心一些。
自动版用不了的情况下（原因很多，最重要是不稳定和道德审核），手动操作也很不错，至少这套正则还是很好用的！
AI也不是神，虽然迄今为止发展很快，迭代也很迅速，但还是有很多超出AI极限，根本处理不了的代码！你把AI脑瓜子干冒烟它也搞不定！
所以，人和AI搭配才能真正的所向披靡！
恭喜你！你已经掌握了这套神器的使用方法！
去吧，英雄！！！



