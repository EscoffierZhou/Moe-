# Moe-Digit

一个可爱的数字计数器生成器，支持多种主题风格。

## 使用方法

启动 `main.py`，根据提示：
1. 选择主题
2. 输入数字
3. 输入输出地址（默认同目录下的output文件夹）

## 主题类型

### GIF动画主题
如果选择的主题里面都是gif文件，则按照原来的动画样式显示。

>**注意：`def _generate_gif_counter(self, number: str, theme_name: str, output_path: str, speed_multiplier: float = 0.5)` 中的0.5是生成的gif的动画速度，按倍率设置**

### PNG静态主题
如果选择的主题里面都是png文件，默认使用SVG动画样式（上下跳动效果）。

## 注意事项

- **数字长度**：没有尝试过过大的数字生成，100位数字测试没有问题
- **主题使用**：theme文件夹中的主题仅作为参考，非商业化，仅供个人使用
