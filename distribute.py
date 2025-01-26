import os
import shutil
from tqdm import tqdm

def split_files(src_root, dest_root, date_prefix, group_size=1000):
    """
    将源目录中的文件分成每组指定数量的文件，并复制到目标目录
    :param src_root: 源目录路径
    :param dest_root: 目标目录路径
    :param date_prefix: 目标文件夹前缀，如 "20250114"
    :param group_size: 每组文件的数量，默认为1000
    """
    # 获取所有文件
    all_files = [f for f in os.listdir(src_root) if os.path.isfile(os.path.join(src_root, f))]
    
    # 计算分组数量
    total_files = len(all_files)
    num_groups = (total_files // group_size) + (1 if total_files % group_size != 0 else 0)

    print(f"总共 {total_files} 个文件，分为 {num_groups} 组。")
    
    # 分组并复制文件
    for i in range(num_groups):
        group_start = i * group_size
        group_end = min((i + 1) * group_size, total_files)
        group_files = all_files[group_start:group_end]
        
        # 创建新组的目标文件夹，使用数字命名
        group_dest_folder = os.path.join(dest_root, f"{date_prefix}_{i + 1}")
        os.makedirs(group_dest_folder, exist_ok=True)
        
        # 复制文件，使用进度条
        for file in tqdm(group_files, desc=f"复制到 {group_dest_folder}"):
            src_file = os.path.join(src_root, file)
            dest_file = os.path.join(group_dest_folder, file)
            shutil.copy2(src_file, dest_file)  # 使用copy2保留文件的元数据

def main():
    date_prefix = "20250126"  # 可以根据需求更改

    # 使用日期前缀构建源路径和目标路径
    src_root = fr"D:\datasets\Distributed\{date_prefix}\images"
    dest_root = fr"D:\datasets\Distributed\{date_prefix}\packages"

    
    # 调用函数进行分组并复制文件
    split_files(src_root, dest_root, date_prefix)

if __name__ == "__main__":
    main()