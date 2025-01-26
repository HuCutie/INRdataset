import os
from functools import reduce
from tqdm import tqdm

def get_file_names(folder_path):
    """
    获取指定文件夹中的所有文件名（不包括路径）
    """
    return {f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))}

def find_common_files(folders):
    """
    比较多个文件夹中的文件名，找出相同的文件名
    """
    # 获取所有文件夹的文件名集合
    file_sets = []
    for folder in tqdm(folders, desc="Collecting file names"):
        file_sets.append(get_file_names(folder))
    
    # 计算交集，找出所有文件夹中都存在的文件名
    common_files = reduce(lambda x, y: x & y, tqdm(file_sets, desc="Finding common files", leave=False))
    
    return common_files, file_sets

def compare_pairs(file_sets, folders):
    """
    比较每对文件夹的文件名，输出相同的文件数量
    """
    comparisons = []
    for i in range(len(file_sets)):
        for j in range(i + 1, len(file_sets)):
            common_files = file_sets[i] & file_sets[j]
            comparisons.append((folders[i], folders[j], len(common_files)))
    return comparisons

def main():
    folders = [
        r"D:\datasets\Distributed\20241211\images",
        r"D:\datasets\Distributed\20241226\images",
        r"D:\datasets\Distributed\20250114\images"
    ]
    
    common_files, file_sets = find_common_files(folders)
    
    # 输出多个文件夹中相同的文件数量
    common_count = len(common_files)
    if common_count > 0:
        print(f"所有文件夹中相同的文件数量为：{common_count}")
        print("所有文件夹中相同的文件名如下：")
        for file in common_files:
            print(file)
    else:
        print("没有文件在所有文件夹中都存在。")
    
    # 输出每对文件夹中相同的文件数量
    comparisons = compare_pairs(file_sets, folders)
    for folder1, folder2, count in comparisons:
        if count > 0:
            print(f"{folder1} 和 {folder2} 中相同的文件数量为：{count}")

if __name__ == "__main__":
    main()