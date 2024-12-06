# Generator.py
import os
import base64
from pathlib import Path
from PIL import Image
from gif import GifGenerator
from png import PngGenerator

class CounterGenerator:
    def __init__(self):
        self.themes_path = Path("theme")
        self.themes = self._get_available_themes()
        self.gif_generator = GifGenerator(self.themes_path)
        self.png_generator = PngGenerator(self.themes_path)

    def _get_available_themes(self):
        """获取所有可用的主题及其文件类型"""
        themes = {}
        for d in self.themes_path.iterdir():
            if d.is_dir():
                theme_type = self._get_theme_file_type(d)
                if theme_type:
                    themes[d.name] = theme_type
        return themes

    def _get_theme_file_type(self, theme_path):
        """检查主题文件夹中的文件类型"""
        files = list(theme_path.glob('*.*'))
        if not files:
            return None
        ext = files[0].suffix.lower()
        if all(f.suffix.lower() == ext for f in files):
            return ext
        return None

    def list_themes(self):
        """列出所有可用的主题"""
        print("可用的主题：")
        for i, (theme, ext) in enumerate(self.themes.items(), 1):
            print(f"{i}. {theme}({ext})")

    def generate_counter(self, number: str, theme_name: str, output_path: str, filename: str = None):
        """根据文件类型选择不同的生成策略"""
        if theme_name not in self.themes:
            raise ValueError(f"主题 '{theme_name}' 不存在")

        file_type = self.themes[theme_name]
        if file_type == '.gif':
            return self.gif_generator._generate_gif_counter(number, theme_name, output_path, filename)
        else:
            return self.png_generator._generate_svg_counter(number, theme_name, output_path, filename)
