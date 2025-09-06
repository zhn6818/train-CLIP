# Flickr30k数据集转换指南

本指南将帮助您将Flickr30k数据集转换为CLIP训练所需的格式。

## 📁 数据集结构

### 原始Flickr30k数据集格式
```
flickr30k_images/
├── flickr30k_images/          # 图像文件目录
│   ├── 1000092795.jpg
│   ├── 10002456.jpg
│   └── ...
└── results.csv                # 标注文件
```

### 转换后的CLIP训练格式
```
flickr30k_clip_dataset/
├── train/                     # 训练集 (80%)
│   ├── 1000092795.jpg
│   ├── 1000092795.txt
│   └── ...
└── val/                       # 验证集 (20%)
    ├── 10002456.jpg
    ├── 10002456.txt
    └── ...
```

## 🚀 快速开始

### 1. 转换Flickr30k数据集
```bash
# 转换Flickr30k数据集为CLIP训练格式
python convert_flickr30k.py --input_dir /path/to/flickr30k_images --output_dir /path/to/output
```

### 2. 验证转换结果
```bash
# 验证数据集格式
python validate_dataset.py --dataset_dir /path/to/output
```

## 📋 详细使用说明

### 转换脚本选项

#### `convert_flickr30k.py` - 数据集转换脚本
```bash
python convert_flickr30k.py \
    --input_dir /path/to/flickr30k_images \
    --output_dir /path/to/output \
    --no_shuffle
```

**参数说明：**
- `--input_dir`: Flickr30k数据集目录路径
- `--output_dir`: 输出目录路径
- `--no_shuffle`: 不打乱描述顺序

#### `validate_dataset.py` - 数据集验证
```bash
python validate_dataset.py --dataset_dir /path/to/dataset
```

**功能：**
- 验证数据集格式正确性
- 检查图像-文本配对情况
- 显示数据集统计信息

## 📊 数据集统计

### Flickr30k数据集概览
- **总图像数**: 31,783张
- **总描述数**: 158,915个（每张图像5个描述）
- **平均每张图像描述数**: 5.0个
- **图像格式**: JPG
- **描述语言**: 英文

### 转换后格式
- **训练集**: 25,426张图像（80%）
- **验证集**: 6,357张图像（20%）
- **文件配对率**: 100%
- **文本文件格式**: 每行一个描述

## 🎯 使用转换后的数据集训练CLIP

### 从头训练
```bash
# 使用ResNet-50训练
python train.py --model_name RN50 --folder flickr30k_clip_dataset/train --batchsize 32

# 使用Vision Transformer训练
python train.py --model_name ViT-B/32 --folder flickr30k_clip_dataset/train --batchsize 64
```

### 微调预训练模型
```bash
# 微调预训练模型
python train_finetune.py --folder flickr30k_clip_dataset/train --batchsize 32
```

## 🔧 故障排除

### 常见问题

#### 1. CSV文件读取错误
**错误**: `KeyError: 'image_name'`
**解决**: 确保CSV文件使用管道符（|）作为分隔符

#### 2. 图像文件未找到
**错误**: `FileNotFoundError: 未找到图像目录`
**解决**: 检查输入目录路径是否正确

#### 3. 内存不足
**错误**: 处理大量数据时内存不足
**解决**: 使用`--max_samples`参数分批处理

#### 4. 文件权限错误
**错误**: 无法创建输出目录
**解决**: 检查输出目录的写入权限

### 验证数据集质量

运行验证脚本检查数据集：
```bash
python validate_dataset.py --dataset_dir your_dataset_path
```

期望输出：
- 配对率: 100%
- 数据集格式正确
- 无未配对文件

## 📈 性能优化建议

### 1. 批量处理
对于大型数据集，建议分批处理：
```bash
# 分批处理，每批1000个样本
python convert_flickr30k.py --max_samples 1000
```

### 2. 并行处理
可以使用多进程加速转换：
```python
# 在脚本中添加多进程支持
from multiprocessing import Pool
```

### 3. 存储优化
- 使用SSD存储提高I/O性能
- 确保有足够的磁盘空间（约2-3GB）

## 📝 输出文件说明

### 图像文件
- 格式: JPG
- 命名: 保持原始文件名
- 质量: 保持原始质量

### 文本文件
- 格式: TXT
- 编码: UTF-8
- 内容: 每行一个描述文本
- 命名: 与对应图像文件同名

### 统计报告
转换完成后会生成`dataset_stats.md`文件，包含：
- 数据集概览
- 训练/验证集统计
- 文件结构说明
- 使用方法示例

## 🎉 完成！

转换完成后，您就可以使用Flickr30k数据集训练CLIP模型了。这个数据集包含高质量的图像-文本对，非常适合多模态学习任务。

如果您在使用过程中遇到任何问题，请检查：
1. 输入目录路径是否正确
2. 文件权限是否足够
3. 磁盘空间是否充足
4. Python环境是否正确配置
