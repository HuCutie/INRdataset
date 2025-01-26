import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# 指定标签文件所在的根目录
root_dir = r'D:\datasets\Collected\20241211\anno'  # 替换为你的路径

# 用来统计每个标签对应的 bounding box 数量
label_bbox_count = defaultdict(int)
# 用来统计每张图片包含多少 bounding box
image_box_count = defaultdict(int)
# 统计图片数量
image_count = 0
# 统计总 bounding box 数量
total_boxes = 0

# 遍历所有的文件夹和文件
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.xml'):
            # 获取XML文件路径
            xml_file = os.path.join(dirpath, filename)
            
            # 解析XML文件
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # 统计每张图片中的 bounding box 数量
            num_boxes_in_image = 0

            for obj in root.findall('object'):
                # 每个 <object> 标签下可能有一个 <bndbox> 标签
                bndbox = obj.find('bndbox')
                if bndbox is not None:
                    num_boxes_in_image += 1  # 每找到一个 bounding box，就说明多了一个 box
                    
                    # 获取物体的标签名称，并更新该标签的 bounding box 数量
                    label = obj.find('name').text
                    label_bbox_count[label] += 1

            # 更新每张图片包含的 bounding box 数量
            image_box_count[num_boxes_in_image] += 1
            total_boxes += num_boxes_in_image
            image_count += 1

# 计算平均每张图片的 bounding box 数量
avg_boxes_per_image = total_boxes / image_count if image_count > 0 else 0

# 打印统计结果
print(f"总图片数量: {image_count} 张")
print(f"总 bounding box 数量: {total_boxes} 个")
print(f"平均每张图片的 bounding box 数量: {avg_boxes_per_image:.2f} 个")

print("\n每个类别对应的 bounding box 数量:")
for label, count in label_bbox_count.items():
    print(f"{label}: {count} 个 bounding box")

print("\n每张图片包含 bounding box 数量统计:")
for box_num, img_count in image_box_count.items():
    print(f"包含 {box_num} 个 bounding box 的图片数量: {img_count} 张")