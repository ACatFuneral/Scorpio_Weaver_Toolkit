# 【字体替换魔法卷轴 - v1.0】
#  作用：在游戏加载时，强行替换指定的英文字体为中文字体。

init -999 python:
    # 在这里定义一个“字体替换字典”
    # 格式是： "要被替换的英文字体文件名" : "用来替换它的中文字体路径"
    font_replacement_map = {
        "LailaL.ttf"    : "tl/Chinese/fonts/SYTW04.ttf", # <-- 这里写你准备好的中文字体
        "whitrabt.ttf"  : "tl/Chinese/fonts/prefix.ttf", # <-- 再加一个，把这个也换掉
        "lightsider.ttf": "tl/Chinese/fonts/SCJSSHT.otf", # <-- 再加一个
        "OriginTech.ttf": "tl/Chinese/fonts/SCJSSHT.otf", # <-- 再加一个
        "DejaVuSans.ttf": "tl/Chinese/fonts/prefix.ttf", # <-- 把游戏默认的也换掉
        "HappyDay.otf"  : "tl/Chinese/fonts/SYTW04.ttf", # <-- 把游戏默认的也换掉
        "Lemon.ttf"     : "tl/Chinese/fonts/zst-Heavy.ttf", # <-- 把游戏默认的也换掉
        "LailaM.ttf"    : "tl/Chinese/fonts/zst-Heavy.ttf", # <-- 把游戏默认的也换掉
        # 如果你还发现了其他英文字体，就继续往这里加！
        # 注意：最后一行可以不加逗号，但为了方便以后增删，建议都加上。
    }

    # 下面是魔法的核心，直接复制，不要动
    config.font_replacement_map.update(font_replacement_map)
