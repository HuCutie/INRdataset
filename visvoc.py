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

category_item_id = -1


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
        def hex2rgb(h):  # rgb order (PIL)
            return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))

        hex = ('FF0000', '00FF00', '0000FF', 'FFA500', 'FF00FF', '00FFFF', 'FFD700', '800080', '008000', '800000',
               '008080', 'FF4500', '9400D3', '008B8B', 'FF1493', '32CD32', '1E90FF', 'FF69B4', 'FF6347', '20B2AA')


        palette = [hex2rgb('#' + c) for c in hex]
        n = len(palette)
        c = palette[int(category_id) % n]
        color = (c[2], c[1], c[0])

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color)
        cv2.putText(img, category_name, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
    return img


def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    category_set[name] = category_item_id
    return category_item_id


def parse_xml_to_dict(xml):
    if len(xml) == 0:  # 遍历到底层，直接返回tag对应的信息
        return {xml.tag: xml.text}

    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)  # 递归遍历标签信息
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:  # 因为object可能有多个，所以需要放入列表里
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def show_image(image_path, anno_path, save_path, plot_image=False):
    assert os.path.exists(image_path), "image path:{} dose not exists".format(image_path)
    assert os.path.exists(anno_path), "annotation path:{} does not exists".format(anno_path)
    anno_file_list = [os.path.join(anno_path, file) for file in os.listdir(anno_path) if file.endswith(".xml")]
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for xml_file in tqdm(anno_file_list):
        if not xml_file.endswith('.xml'):
            continue

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
            img = draw_box(img, xml_info_dict['annotation']['object'])
        res_path = os.path.join(save_path, filename)
        cv2.imwrite(res_path, img)
        
    if plot_image:
        plt.bar(range(len(every_class_num)), every_class_num.values(), align='center')
        plt.xticks(range(len(every_class_num)), every_class_num.keys(), rotation=0)
        for index, (i, v) in enumerate(every_class_num.items()):
            plt.text(x=index, y=v, s=str(v), ha='center')
        plt.xlabel('image class')
        plt.ylabel('number of images')
        plt.title('class distribution')

        res_path = os.path.join(save_path, '00000_class_distribution.png')
        plt.savefig(res_path)
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--image-path', type=str, default=r'D:\datasets\Distributed\20250122\packages\20250122_5', help='image path')
    parser.add_argument('-ap', '--anno-path', type=str, default=r'D:\datasets\Collected\20250122\anno\20250124_5', help='annotation path')
    parser.add_argument('-sp', '--save-path', type=str, default=r'D:\datasets\Collected\20250122\vis\20250124-vis', help='labeled img saving path')
    parser.add_argument('-p', '--plot-image', action='store_true', help='weather to save stastic result')
    opt = parser.parse_args()

    print(opt)
    show_image(opt.image_path, opt.anno_path, opt.save_path, opt.plot_image)
    print(every_class_num)
    print("category nums: {}".format(len(category_set)))
    print("image nums: {}".format(len(image_set)))
    print("bbox nums: {}".format(sum(every_class_num.values())))