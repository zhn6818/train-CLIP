#!/usr/bin/env python3
"""
Flickr30k数据集转换为CLIP训练格式的脚本

使用方法:
python convert_flickr30k.py --input_dir /path/to/flickr30k_images --output_dir /path/to/output

数据集格式要求:
- 输入: flickr30k_images目录包含图像文件和results.csv标注文件
- 输出: 每张图像对应一个txt文件，包含所有描述文本，可直接用于CLIP训练
"""

import os
import csv
import shutil
from pathlib import Path
import argparse
from collections import defaultdict
import random

def convert_flickr30k_to_clip_format(input_dir, output_dir, shuffle_descriptions=True):
    """
    将Flickr30k数据集转换为CLIP训练格式
    
    Args:
        input_dir (str): 输入目录路径，包含flickr30k_images子目录和results.csv
        output_dir (str): 输出目录路径
        shuffle_descriptions (bool): 是否随机打乱每张图像的描述顺序
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 检查输入文件
    csv_file = input_path / "results.csv"
    images_dir = input_path / "flickr30k_images"
    
    if not csv_file.exists():
        raise FileNotFoundError(f"未找到标注文件: {csv_file}")
    
    if not images_dir.exists():
        raise FileNotFoundError(f"未找到图像目录: {images_dir}")
    
    print(f"开始处理Flickr30k数据集...")
    print(f"输入目录: {input_path}")
    print(f"输出目录: {output_path}")
    
    # 读取CSV文件并组织数据
    image_descriptions = defaultdict(list)
    
    print("正在读取标注文件...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row_num, row in enumerate(reader, 1):
            try:
                image_name = row.get('image_name', '').strip() if row.get('image_name') else ''
                comment = row.get(' comment', '').strip() if row.get(' comment') else ''  # 注意列名前面有空格
                
                if image_name and comment:
                    image_descriptions[image_name].append(comment)
            except Exception as e:
                print(f"警告: 处理第 {row_num} 行时出错: {e}")
                continue
    
    print(f"找到 {len(image_descriptions)} 张图像的描述")
    
    # 获取所有图像文件
    image_files = list(images_dir.glob('*.jpg'))
    print(f"找到 {len(image_files)} 个图像文件")
    
    # 过滤出有描述的图像
    valid_images = []
    for img_file in image_files:
        if img_file.name in image_descriptions:
            valid_images.append(img_file)
    
    print(f"有效图像数量: {len(valid_images)}")
    
    # 转换每个图像
    success_count = 0
    error_count = 0
    
    for i, img_file in enumerate(valid_images):
        try:
            # 获取图像的所有描述
            descriptions = image_descriptions[img_file.name]
            
            # 随机打乱描述顺序（可选）
            if shuffle_descriptions:
                random.shuffle(descriptions)
            
            # 创建输出图像文件
            output_img_path = output_path / img_file.name
            shutil.copy2(img_file, output_img_path)
            
            # 创建对应的文本文件
            txt_file = output_path / f"{img_file.stem}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                for desc in descriptions:
                    f.write(desc + '\n')
            
            success_count += 1
            
            if (i + 1) % 1000 == 0:
                print(f"已处理: {i + 1}/{len(valid_images)} 张图像")
                
        except Exception as e:
            print(f"处理图像 {img_file.name} 时出错: {e}")
            error_count += 1
    
    print(f"\n转换完成!")
    print(f"成功处理: {success_count} 张图像")
    print(f"处理失败: {error_count} 张图像")
    print(f"输出目录: {output_path}")
    
    # 验证输出
    output_images = list(output_path.glob('*.jpg'))
    output_texts = list(output_path.glob('*.txt'))
    
    print(f"\n验证结果:")
    print(f"输出图像文件: {len(output_images)} 个")
    print(f"输出文本文件: {len(output_texts)} 个")
    
    # 检查配对情况
    image_stems = {f.stem for f in output_images}
    text_stems = {f.stem for f in output_texts}
    paired = image_stems & text_stems
    
    print(f"成功配对: {len(paired)} 对")
    
    if len(paired) != len(output_images):
        print("警告: 部分图像未成功配对")
        unpaired_images = image_stems - text_stems
        unpaired_texts = text_stems - image_stems
        if unpaired_images:
            print(f"未配对的图像: {len(unpaired_images)} 个")
        if unpaired_texts:
            print(f"未配对的文本: {len(unpaired_texts)} 个")
    
    return success_count, error_count

def validate_dataset(dataset_dir):
    """
    验证转换后的数据集格式
    
    Args:
        dataset_dir (str): 数据集目录路径
    """
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        print(f"错误: 数据集目录不存在: {dataset_path}")
        return False
    
    # 获取所有文件
    image_files = list(dataset_path.glob('*.jpg'))
    text_files = list(dataset_path.glob('*.txt'))
    
    print(f"数据集验证结果:")
    print(f"图像文件: {len(image_files)} 个")
    print(f"文本文件: {len(text_files)} 个")
    
    # 检查配对
    image_stems = {f.stem for f in image_files}
    text_stems = {f.stem for f in text_files}
    paired = image_stems & text_stems
    
    print(f"成功配对: {len(paired)} 对")
    
    if len(paired) == len(image_files) and len(paired) == len(text_files):
        print("✅ 数据集格式正确!")
        return True
    else:
        print("❌ 数据集格式有问题")
        return False

def main():
    parser = argparse.ArgumentParser(description='将Flickr30k数据集转换为CLIP训练格式')
    parser.add_argument('--input_dir', required=True, help='Flickr30k数据集目录路径')
    parser.add_argument('--output_dir', required=True, help='输出目录路径')
    parser.add_argument('--no_shuffle', action='store_true', help='不打乱描述顺序')
    
    args = parser.parse_args()
    
    convert_flickr30k_to_clip_format(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        shuffle_descriptions=not args.no_shuffle
    )

if __name__ == "__main__":
    main()
