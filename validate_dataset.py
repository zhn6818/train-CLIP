#!/usr/bin/env python3
"""
数据集验证脚本

使用方法:
python validate_dataset.py --dataset_dir /path/to/dataset
"""

import argparse
from pathlib import Path
import random

def validate_dataset(dataset_dir):
    """验证数据集格式和完整性"""
    
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        print(f"❌ 错误: 数据集目录不存在: {dataset_path}")
        return False
    
    print(f"🔍 验证数据集: {dataset_path}")
    print("=" * 50)
    
    # 检查是否有子目录（训练/验证集）
    subdirs = [d for d in dataset_path.iterdir() if d.is_dir()]
    
    if subdirs:
        print("📁 发现子目录，验证每个子目录...")
        for subdir in subdirs:
            print(f"\n验证子目录: {subdir.name}")
            validate_single_directory(subdir)
    else:
        print("📁 验证单一目录...")
        validate_single_directory(dataset_path)
    
    return True

def validate_single_directory(dir_path):
    """验证单个目录的数据集格式"""
    
    # 获取所有文件
    image_files = list(dir_path.glob('*.jpg'))
    text_files = list(dir_path.glob('*.txt'))
    
    print(f"图像文件: {len(image_files)} 个")
    print(f"文本文件: {len(text_files)} 个")
    
    # 检查配对
    image_stems = {f.stem for f in image_files}
    text_stems = {f.stem for f in text_files}
    paired = image_stems & text_stems
    
    print(f"成功配对: {len(paired)} 对")
    print(f"配对率: {len(paired) / len(image_files) * 100:.1f}%")
    
    # 检查未配对的文件
    unpaired_images = image_stems - text_stems
    unpaired_texts = text_stems - image_stems
    
    if unpaired_images:
        print(f"⚠️  未配对的图像: {len(unpaired_images)} 个")
        if len(unpaired_images) <= 5:
            print(f"   示例: {list(unpaired_images)[:5]}")
    
    if unpaired_texts:
        print(f"⚠️  未配对的文本: {len(unpaired_texts)} 个")
        if len(unpaired_texts) <= 5:
            print(f"   示例: {list(unpaired_texts)[:5]}")
    
    # 检查文本文件内容
    if text_files:
        print(f"\n📝 检查文本文件内容...")
        sample_files = random.sample(text_files, min(5, len(text_files)))
        
        for txt_file in sample_files:
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    descriptions = [line.strip() for line in lines if line.strip()]
                    print(f"   {txt_file.name}: {len(descriptions)} 个描述")
                    if descriptions:
                        print(f"     示例: {descriptions[0][:50]}...")
            except Exception as e:
                print(f"   ❌ 读取 {txt_file.name} 失败: {e}")
    
    # 检查图像文件
    if image_files:
        print(f"\n🖼️  检查图像文件...")
        sample_files = random.sample(image_files, min(3, len(image_files)))
        
        for img_file in sample_files:
            file_size = img_file.stat().st_size
            print(f"   {img_file.name}: {file_size / 1024:.1f} KB")
    
    if len(paired) == len(image_files) and len(paired) == len(text_files):
        print("✅ 数据集格式正确!")
        return True
    else:
        print("❌ 数据集格式有问题")
        return False

def main():
    parser = argparse.ArgumentParser(description='验证CLIP训练数据集格式')
    parser.add_argument('--dataset_dir', required=True, help='数据集目录路径')
    
    args = parser.parse_args()
    
    success = validate_dataset(args.dataset_dir)
    
    if success:
        print("\n🎉 数据集验证完成!")
    else:
        print("\n💥 数据集验证失败!")
        exit(1)

if __name__ == "__main__":
    main()
