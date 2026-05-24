# 临时Logo生成脚本
# 用于生成ZRC工具箱的临时Logo占位符

from PIL import Image, ImageDraw, ImageFont
import os


def create_logo(size, bg_color=None):
    """创建Logo图片"""
    # 创建画布
    if bg_color:
        img = Image.new('RGB', (size, size), bg_color)
    else:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    
    # 定义颜色
    blue_main = (33, 150, 243)  # #2196F3
    blue_dark = (21, 101, 192)  # #1565C0
    white = (255, 255, 255)
    
    # 绘制背景圆形
    margin = size // 10
    draw.ellipse([margin, margin, size - margin, size - margin], fill=blue_dark)
    
    # 绘制内层圆形
    inner_margin = size // 6
    draw.ellipse([inner_margin, inner_margin, size - inner_margin, size - inner_margin], fill=blue_main)
    
    # 尝试加载字体，如果失败则使用简单图形
    try:
        # 尝试使用系统字体
        font_size = size // 3
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("msyh.ttc", font_size)  # 微软雅黑
            except:
                font = ImageFont.load_default()
        
        # 绘制文字
        text = "ZRC"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (size - text_width) // 2 - text_bbox[0]
        text_y = (size - text_height) // 2 - text_bbox[1]
        
        draw.text((text_x, text_y), text, fill=white, font=font)
    except:
        # 如果字体加载失败，绘制简单图形
        s = size // 4
        draw.rectangle([s, s, size - s, size - s], fill=white, outline=None)
    
    return img


def main():
    """主函数"""
    # 输出目录
    output_dir = os.path.join('assets', 'logo')
    os.makedirs(output_dir, exist_ok=True)
    
    # 尺寸列表
    sizes = [512, 256, 128, 64, 32, 16]
    
    # 生成不同尺寸的Logo
    for size in sizes:
        print(f"生成 {size}x{size} Logo...")
        
        # 透明背景版本
        img = create_logo(size)
        img.save(os.path.join(output_dir, f'zrc_logo_{size}x{size}.png'))
        
        # 白色背景版本
        if size == 512:
            img_white_bg = create_logo(size, bg_color=(255, 255, 255))
            img_white_bg.save(os.path.join(output_dir, 'zrc_logo_white_bg.png'))
            
            # 深色背景版本
            img_dark_bg = create_logo(size, bg_color=(44, 62, 80))  # #2C3E50
            img_dark_bg.save(os.path.join(output_dir, 'zrc_logo_dark_bg.png'))
            
            # 单色版本
            img_mono = Image.new('RGB', (size, size), (255, 255, 255))
            draw_mono = ImageDraw.Draw(img_mono)
            margin = size // 10
            draw_mono.ellipse([margin, margin, size - margin, size - margin], fill=(51, 51, 51))
            img_mono.save(os.path.join(output_dir, 'zrc_logo_monochrome.png'))
    
    print(f"\nLogo已生成到 {output_dir}/")
    print("\n注意：这些是临时占位符Logo，请使用设计软件制作正式Logo")


if __name__ == "__main__":
    main()
