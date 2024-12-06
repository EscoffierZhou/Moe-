# png.py
from PIL import Image
from pathlib import Path

class PngGenerator:
    def __init__(self, themes_path):
        self.themes_path = themes_path

    def _image_to_data_uri(self, image_path):
        """将图片转换为data URI"""
        with open(image_path, 'rb') as f:
            import base64
            data = base64.b64encode(f.read()).decode('utf-8')
            ext = Path(image_path).suffix.lower()
            mime_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif'
            }.get(ext, 'image/png')
            return f"data:{mime_type};base64,{data}"

    def _generate_svg_counter(self, number: str, theme_name: str, output_path: str, filename: str = None):
        """生成计数器SVG动画

        Args:
            number: 要显示的数字
            theme_name: 主题名称
            output_path: 输出路径
            filename: 输出文件名（不包含扩展名）
        """
        theme_path = self.themes_path / theme_name
        if not theme_path.exists():
            raise ValueError(f"主题 '{theme_name}' 不存在")

        # 获取数字图片信息
        digit_info = {}
        total_width = 0
        max_height = 0

        # 收集所有数字的信息
        for digit in str(number):
            # 尝试不同的图片格式
            for ext in ['.png', '.gif', '.jpg', '.jpeg']:
                digit_path = theme_path / f"{digit}{ext}"
                if digit_path.exists():
                    img = Image.open(digit_path)
                    width, height = img.size
                    digit_info[digit] = {
                        'width': width,
                        'height': height,
                        'data': self._image_to_data_uri(digit_path)
                    }
                    total_width += width
                    max_height = max(max_height, height)
                    break
            else:
                raise ValueError(f"在主题 '{theme_name}' 中找不到数字 '{digit}' 的图片")

        # 生成SVG
        svg_parts = []
        svg_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        svg_parts.append(
            f'<svg viewBox="0 0 {total_width} {max_height}" width="{total_width}" height="{max_height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')

        # 添加样式
        svg_parts.append('<style>')
        svg_parts.append('@keyframes shake {')
        svg_parts.append('  0%, 100% { transform: translateY(0); }')
        svg_parts.append('  10%, 30%, 50%, 70%, 90% { transform: translateY(-2px); }')
        svg_parts.append('  20%, 40%, 60%, 80% { transform: translateY(2px); }')
        svg_parts.append('}')
        svg_parts.append('.digit { animation: shake 2s infinite; }')
        svg_parts.append('.digit:hover { animation: shake 0.5s infinite; }')
        svg_parts.append('</style>')

        # 添加定义
        svg_parts.append('<defs>')
        for digit, info in digit_info.items():
            svg_parts.append(
                f'<image id="d{digit}" width="{info["width"]}" height="{info["height"]}" xlink:href="{info["data"]}" />')
        svg_parts.append('</defs>')

        # 添加数字
        x = 0
        for i, digit in enumerate(str(number)):
            info = digit_info[digit]
            y = (max_height - info['height']) // 2
            # 添加动画延迟，使每个数字的动画错开
            delay = i * 0.1
            svg_parts.append(
                f'<use class="digit" x="{x}" y="{y}" xlink:href="#d{digit}" style="animation-delay: {delay}s" />')
            x += info['width']

        svg_parts.append('</svg>')

        # 确保输出路径是有效的
        output_path = Path(output_path)
        if filename:
            output_path = output_path / f"{filename}.svg"
        else:
            output_path = output_path / f"counter_{number}.svg"

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存SVG
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_parts))

        return str(output_path)
