import os
import random
import shutil
import time
from tqdm import tqdm  # 用于显示进度条

def load_round_number(file_path):
    """
    读取上次提取的轮次编号，若文件不存在则返回1
    """
    if not os.path.exists(file_path):
        return 1
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        rounds = [int(line.split('第')[1].split('次')[0]) for line in lines if line.startswith("# 第")]
        return max(rounds) + 1 if rounds else 1

def write_to_txt(file_path, image_list, round_number):
    """
    将提取的图片路径和目标文件名写入txt文件，标明提取轮次和时间
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"# 第{round_number}次提取 - 时间: {timestamp}\n")
        for image in image_list:
            f.write(image + '\n')
        f.write("\n")

def rename_image_path(src_path):
    """
    将图片路径重命名为包含路径信息的文件名
    """
    base_path, file_name = os.path.split(src_path)
    relative_path = os.path.relpath(base_path)  # 获取相对路径
    new_name = f"{relative_path.replace(os.sep, '_')}_{file_name}"  # 使用相对路径和文件名生成新文件名
    return new_name

def collect_images(src_root):
    """
    遍历所有最底层目录并收集图片路径
    """
    image_paths = []
    for root, dirs, files in os.walk(src_root):
        if not dirs:  # 如果没有子目录，说明是最底层目录
            for file in files:
                if file.endswith(".jpg"):
                    image_paths.append(os.path.join(root, file))
    return image_paths

def move_and_rename_images(image_list, dest_root):
    """
    将图片移动到目标目录，并使用新命名规则
    """
    for src_path in tqdm(image_list, desc="Moving and renaming images"):
        new_name = rename_image_path(src_path)
        dest_path = os.path.join(dest_root, new_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.move(src_path, dest_path)  # 使用 move 替换 copy2

def check_and_create_folder(folder_path):
    """
    检查文件夹是否存在，如果不存在则创建
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 {folder_path} 不存在，已创建该文件夹。")
    else:
        print(f"文件夹 {folder_path} 已存在。")

def main():
    src_root = r"D:\datasets\images"  # 图片源目录
    date_str = "20250126"  # 手动指定日期字符串
    dest_root = fr"D:\datasets\Distributed\{date_str}\images"
    output_txt = r"D:\datasets\history.txt"  # 输出txt文件
    num_samples = 1000  # 需要提取的图片数量

    # 检查并确保目标目录存在
    check_and_create_folder(dest_root)

    # 收集图片路径
    print("Collecting image paths...")
    image_paths = collect_images(src_root)

    # 检查是否有可用图片
    if not image_paths:
        print("源目录中没有找到图片")
        return

    # 按照需求，提取指定数量的图片
    print("Selecting images...")
    sampled_images = random.sample(image_paths, min(num_samples, len(image_paths)))

    # 重命名并移动图片
    print("Moving and renaming images...")
    renamed_images = [rename_image_path(img) for img in tqdm(sampled_images, desc="Renaming images")]
    move_and_rename_images(sampled_images, dest_root)

    # 记录提取历史
    round_number = load_round_number(output_txt)
    write_to_txt(output_txt, renamed_images, round_number)

    print(f"成功提取了 {len(sampled_images)} 张图片，并写入 {output_txt}")

if __name__ == "__main__":
    main()