# gif.py
from PIL import Image
import base64
from pathlib import Path

class GifGenerator:
    def __init__(self, themes_path):
        self.themes_path = themes_path

    def _image_to_data_uri(self, image_path):
        """将图片转换为data URI"""
        with open(image_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            ext = Path(image_path).suffix.lower()
            mime_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif'
            }.get(ext, 'image/png')
            return f"data:{mime_type};base64,{data}"

    def _generate_gif_counter(self, number: str, theme_name: str, output_path: str, filename: str = None, speed_multiplier: float = 0.5):
        """
        生成GIF动画计数器并同时输出GIF和SVG文件

        Args:
            number: 要显示的数字
            theme_name: 主题名称
            output_path: 输出路径
            filename: 输出文件名（不包含扩展名）
            speed_multiplier: 速度倍率，大于1加速，小于1减速。例如0.7表示减速到原来的70%

        Returns:
            tuple: (gif_path, svg_path) 返回生成的GIF和SVG文件路径
        """
        if not isinstance(speed_multiplier, (int, float)):
            speed_multiplier = float(speed_multiplier)
            
        if speed_multiplier <= 0:
            raise ValueError("速度倍率必须大于0")

        theme_path = self.themes_path / theme_name
        max_width = 0
        max_height = 0

        # 收集所有数字的GIF
        digit_gifs = []
        for digit in str(number):
            gif_path = theme_path / f"{digit}.gif"
            if not gif_path.exists():
                raise ValueError(f"找不到数字 {digit} 的GIF文件")

            gif = Image.open(gif_path)
            digit_gifs.append(gif)

            # 更新最大尺寸
            max_width += gif.width
            max_height = max(max_height, gif.height)

        # 创建合并后的GIF
        durations = []
        frames = []

        # 获取所有GIF的最大帧数
        n_frames = max(gif.n_frames for gif in digit_gifs)

        # 合并每一帧
        for frame_idx in range(n_frames):
            # 创建一张新的透明背景图像
            new_frame = Image.new('RGBA', (max_width, max_height), (0, 0, 0, 0))
            x_offset = 0

            for gif in digit_gifs:
                current_frame = frame_idx % gif.n_frames
                gif.seek(current_frame)

                frame = Image.new('RGBA', gif.size, (0, 0, 0, 0))

                if gif.mode == 'P':
                    frame.paste(gif.convert('RGBA'), (0, 0))
                else:
                    frame.paste(gif, (0, 0))

                new_frame.paste(frame, (x_offset, 0), frame)
                x_offset += frame.width

                if frame_idx == 0:
                    original_duration = gif.info.get('duration', 100)
                    adjusted_duration = int(original_duration / speed_multiplier)
                    durations.append(adjusted_duration)

            frames.append(new_frame)

        # 确保输出路径正确
        output_path = Path(output_path)
        if filename:
            base_path = output_path / filename
        else:
            base_path = output_path / f"counter_{number}"

        # 生成GIF文件路径和SVG文件路径
        gif_path = base_path.with_suffix('.gif')
        svg_path = base_path.with_suffix('.svg')

        # 保存GIF
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=min(durations),
            loop=0,
            optimize=False,
            transparency=0,
            disposal=2
        )

        # 创建SVG文件
        # 将GIF转换为base64编码
        with open(gif_path, 'rb') as gif_file:
            gif_data = gif_file.read()
            gif_base64 = base64.b64encode(gif_data).decode('utf-8')

        # 创建SVG内容
        svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="{max_width}" height="{max_height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <image width="{max_width}" height="{max_height}" xlink:href="data:image/gif;base64,{gif_base64}"/>
    </svg>'''

        # 保存SVG文件
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            return str(gif_path), str(svg_path)
"""
        # 生成markdown引用，包含两种格式
        md_path = base_path.with_suffix('.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f'''# GIF 格式
    ![counter]({gif_path.name})
    # SVG 格式
    ![counter]({svg_path.name})
    ''')*/
"""

