#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML实体编码修复工具
该工具用于修复文件中的HTML实体编码（如 &lt; 转换为 <）
"""

import html
import os

def fix_html_entities(file_path):
    """
    修复文件中的HTML实体编码
    将HTML实体（如 &lt;, &gt;, &amp; 等）转换回原始字符
    
    Args:
        file_path: 需要修复的文件路径
        
    Returns:
        bool: 修复成功返回True，失败返回False
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用html模块的unescape函数修复HTML实体编码
        fixed_content = html.unescape(content)
        
        # 将修复后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"已修复: {file_path}")
        return True
    except Exception as e:
        print(f"修复失败 {file_path}: {e}")
        return False

if __name__ == '__main__':
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 目标文件：主窗口模块
    target_file = os.path.join(script_dir, 'src', 'gui', 'main_window.py')
    
    # 检查文件是否存在
    if os.path.exists(target_file):
        print(f"正在修复: {target_file}")
        fix_html_entities(target_file)
    else:
        print(f"文件不存在: {target_file}")
