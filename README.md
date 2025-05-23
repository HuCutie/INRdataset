# 📁 图像提取脚本（extract.py）使用教程

本脚本用于从图像数据集中随机提取指定数量的图像，自动重命名后移动到目标目录中，并记录每轮提取的时间与轮次。适用于图像数据标注、任务分发等场景。

---

## ✅ 功能说明

该脚本实现以下功能：

1. **自动递归遍历最底层文件夹**，收集所有 `.jpg` / `.jpeg` / `.png` 图像路径；
2. **随机采样指定数量的图像文件**（默认提取 1000 张）；
3. **将原图像路径编码进新文件名**，避免重名并保留原始信息；
4. **将图像移动至以当前日期命名的目标目录**（如 `Distributed/20250523/images`）；
5. **将提取记录追加写入历史文件 `history.txt`**，包含轮次编号与时间戳。

---

## 📦 文件结构示意

```
D:
├── datasets
│   ├── images\               # 原始图像数据集目录
│   ├── Distributed\
│   │   └── 20250523\
│   │       └── images\       # 自动生成的提取结果
│   └── history.txt           # 提取记录文件
```

## 🛠 使用方式

### 1. 修改参数（可选）

打开 `extract_images.py`，根据实际情况修改以下参数：

```python
src_root = r"D:\datasets\images"           # 源图像目录
output_txt = r"D:\datasets\history.txt"    # 输出记录文件
num_samples = 1000                         # 提取图像数量
```

### 2. 运行脚本
在终端或 IDE 中运行脚本：

```python extract_images.py```

每次运行将自动执行一轮提取，输出目录形如：

```D:\datasets\Distributed\20250523\images\```


# 📦 图像文件打包脚本（distribute.py）教程

该脚本用于将指定目录中的图像文件进行分组（如每 1000 张为一组），自动复制到带日期与分组编号命名的文件夹中。适用于图像数据打包、任务分发等场景。

---

## ✅ 功能说明

该脚本实现以下功能：

1. 自动获取源目录中所有文件；
2. 每组默认提取 1000 个文件（可自定义）；
3. 自动生成分组目录，目录名格式为：`YYYYMMDD_1`, `YYYYMMDD_2`, ...；
4. 文件复制使用 `shutil.copy2`，保留元数据；
5. 使用 `tqdm` 展示进度条。

---

## 📦 示例结构
```
D:
├── datasets
│   ├── Distributed
│   │   └── 20250523
│   │       ├── images\        # 待分组图像目录
│   │       └── packages\      # 自动生成的打包结果目录
```

## 🛠 使用方式

### 1. 修改参数（可选）

打开 `split_images.py`，根据实际情况修改以下参数：

```
python split_files(src_root, dest_root, date_prefix, group_size=500)  # 改为每组 500 张
```

### 2. 运行脚本
在终端或 IDE 中运行脚本：

```
python split_images.py
```

# 标签可视化与统计脚本（anno_cal.py）使用说明

本工具支持将 VOC XML 格式的标注文件进行可视化，并输出以下统计信息：

- 每类物体的标注框数量
- 每张图像中包含的标注框数量分布
- 图像总数、bbox 总数、平均每张图像的标注框数量

## 🧩 运行环境

- Python 3.6+
- 安装依赖项：
  ```bash
  pip install opencv-python matplotlib lxml tqdm
  ```

## 🚀 使用方法
```bash
python visualize_and_stats.py \
  -ip D:\datasets\images \
  -ap D:\datasets\annotations \
  -sp D:\datasets\output \
  --plot-image \
  --do-stats
```

| 参数             | 说明               |
| -------------- | ---------------- |
| `-ip`          | 图像文件夹路径          |
| `-ap`          | 标注文件夹路径（VOC XML） |
| `-sp`          | 可视化图像保存路径        |
| `--plot-image` | 是否绘制并保存类别分布柱状图   |
| `--do-stats`   | 是否输出统计分析信息       |
