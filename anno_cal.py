import os
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm
from lxml import etree
from collections import defaultdict
import argparse

category_set = dict()
image_set = set()
every_class_num = defaultdict(int)
image_box_count = defaultdict(int)

category_item_id = -1

def hex2rgb(h):
    return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))

def draw_box(img, objects):
    for object in objects:
        category_name = object['name']
        every_class_num[category_name] += 1
        if category_name not in category_set:
            category_id = addCatItem(category_name)
        else:
            category_id = category_set[category_name]
        xmin = int(object['bndbox']['xmin'])
        ymin = int(object['bndbox']['ymin'])
        xmax = int(object['bndbox']['xmax'])
        ymax = int(object['bndbox']['ymax'])

        palette = [hex2rgb('#' + c) for c in (
            'FF0000', '00FF00', '0000FF', 'FFA500', 'FF00FF',
            '00FFFF', 'FFD700', '800080', '008000', '800000',
            '008080', 'FF4500', '9400D3', '008B8B', 'FF1493',
            '32CD32', '1E90FF', 'FF69B4', 'FF6347', '20B2AA'
        )]
        c = palette[int(category_id) % len(palette)]
        color = (c[2], c[1], c[0])

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color)
        cv2.putText(img, category_name, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
    return img

def addCatItem(name):
    global category_item_id
    category_item_id += 1
    category_set[name] = category_item_id
    return category_item_id

def parse_xml_to_dict(xml):
    if len(xml) == 0:
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}

def show_image(image_path, anno_path, save_path, plot_image=False, do_stats=False):
    assert os.path.exists(image_path), f"image path:{image_path} does not exist"
    assert os.path.exists(anno_path), f"annotation path:{anno_path} does not exist"

    anno_file_list = [os.path.join(anno_path, file) for file in os.listdir(anno_path) if file.endswith(".xml")]

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    total_boxes = 0

    for xml_file in tqdm(anno_file_list):
        with open(xml_file) as fid:
            xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        xml_info_dict = parse_xml_to_dict(xml)

        filename = xml_info_dict['annotation']['filename']
        image_set.add(filename)
        file_path = os.path.join(image_path, filename)
        if not os.path.exists(file_path):
            continue

        img = cv2.imread(file_path)
        if img is None:
            continue

        if 'object' in xml_info_dict['annotation']:
            objects = xml_info_dict['annotation']['object']
            img = draw_box(img, objects)
            num_boxes = len(objects)
            image_box_count[num_boxes] += 1
            total_boxes += num_boxes
        else:
            image_box_count[0] += 1

        cv2.imwrite(os.path.join(save_path, filename), img)

    if do_stats:
        print("\n📊 统计结果:")
        print(f"总图片数量: {len(image_set)} 张")
        print(f"总 bounding box 数量: {total_boxes} 个")
        avg_boxes_per_image = total_boxes / len(image_set) if image_set else 0
        print(f"平均每张图片的 bounding box 数量: {avg_boxes_per_image:.2f} 个")

        print("\n每个类别对应的 bounding box 数量:")
        for label, count in every_class_num.items():
            print(f"{label}: {count} 个 bounding box")

        print("\n每张图片包含 bounding box 数量统计:")
        for box_num, img_count in sorted(image_box_count.items()):
            print(f"包含 {box_num} 个 bounding box 的图片数量: {img_count} 张")

    if plot_image:
        plt.bar(range(len(every_class_num)), every_class_num.values(), align='center')
        plt.xticks(range(len(every_class_num)), every_class_num.keys(), rotation=45)
        for index, (i, v) in enumerate(every_class_num.items()):
            plt.text(x=index, y=v, s=str(v), ha='center')
        plt.xlabel('Category')
        plt.ylabel('Bounding Boxes')
        plt.title('Class Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, '00000_class_distribution.png'))
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--image-path', type=str, required=True, help='Path to image files')
    parser.add_argument('-ap', '--anno-path', type=str, required=True, help='Path to annotation files (.xml)')
    parser.add_argument('-sp', '--save-path', type=str, required=True, help='Path to save labeled images')
    parser.add_argument('-p', '--plot-image', action='store_true', help='Whether to save class distribution plot')
    parser.add_argument('--do-stats', action='store_true', help='Whether to perform statistical analysis')
    args = parser.parse_args()

    show_image(args.image_path, args.anno_path, args.save_path, args.plot_image, args.do_stats)