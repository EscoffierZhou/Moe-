# main.py
import os
from pathlib import Path
from Generator import CounterGenerator

def get_default_output_path():
    """获取默认输出路径：main.py所在目录下的output文件夹"""
    # 获取main.py的绝对路径
    current_file = Path(__file__).resolve()
    # 获取main.py所在目录
    current_dir = current_file.parent
    # 在当前目录下创建output文件夹
    output_dir = current_dir / 'output'
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir)

def generate_output_filename(number: str, theme_name: str) -> str:
    # 获取数字的前10位（如果不足10位则使用全部）
    number_prefix = number[:10] if len(number) > 10 else number
    # 组合文件名
    return f"{number_prefix}_{theme_name}"

def validate_number(number: str) -> bool:
    """验证输入的数字"""
    # 检查是否只包含数字
    if not number.isdigit():
        return False
    # 检查长度是否合理（这里设置最大长度为1000，可以根据需要调整）
    if len(number) > 1000:
        return False
    return True

def main():
    generator = CounterGenerator()
    # 显示可用主题
    generator.list_themes()

    # 获取用户输入
    theme_choice = input("\n请选择主题编号: ")
    try:
        theme_index = int(theme_choice) - 1
        if theme_index < 0:
            raise ValueError("主题编号必须大于0")
        theme_name = list(generator.themes.keys())[theme_index]
    except (ValueError, IndexError):
        print("无效的主题选择！请输入有效的数字编号。")
        return

    number = input("请输入要转换的数字: ")
    if not validate_number(number):
        print("无效的数字！请输入有效的数字（长度不超过1000位）。")
        return

    # 获取输出路径
    custom_path = input("请输入输出路径（直接回车使用默认路径）: ").strip()
    try:
        output_path = custom_path if custom_path else get_default_output_path()
        # 确保输出目录存在
        os.makedirs(output_path, exist_ok=True)
    except Exception as e:
        print(f"创建输出目录失败：{str(e)}")
        return
    
    try:
        # 生成文件名
        filename = generate_output_filename(number, theme_name)
        # 生成计数器
        result_path = generator.generate_counter(number, theme_name, output_path, filename)
        print(f"生成成功：{result_path}")
    except Exception as e:
        print(f"生成失败：{str(e)}")
        print("请检查主题文件是否存在，或者尝试其他主题。")

if __name__ == "__main__":
    main()
