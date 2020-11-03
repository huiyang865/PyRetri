import os
import json
import argparse
from main.daneng.base import persist_2_json


def get_gt_json(request_dir, gt_base_dir, data_base_dir):
    gt_json = {}
    for item_img in os.listdir(request_dir):
        img_name = item_img[:-4]
        gt_json[img_name] = []
        item_base_dir = os.path.join(gt_base_dir, img_name)

        if not os.path.exists(item_base_dir):
            continue

        for item_base_img in os.listdir(item_base_dir):
            base_img_path = os.path.join(data_base_dir, item_base_img)
            if not os.path.exists(base_img_path):
                print(base_img_path, 'not exists in database.')
                continue

            gt_json[img_name].append(item_base_img)
    return gt_json


def parse_args():
    parser = argparse.ArgumentParser(
        description='Making json file for image retrieval task')
    # 查询图片目录
    # request_dir
    # ├── class_A_requst.jpg
    # ├── class_B_requst.jpg
    # ├── class_C_requst.jpg
    # └── ···
    parser.add_argument('--request_dir',
                        required=True,
                        help='Input dir of request imgs')

    # 底库中有重复图片的结果
    # general_recognition
    # ├── class_A_requst
    # │   ├── img1.jpg
    # │   └── ···
    # ├── class_B_requst
    # │   ├── img2.jpg
    # │   └── ···
    # └── ···
    parser.add_argument('--data_base_dir',
                        required=True,
                        help='Input dir of database imgs')

    # 底库中有重复图片的结果
    # general_recognition
    # ├── class_A_requst
    # │   ├── img1.jpg
    # │   └── ···
    # ├── class_B_requst
    # │   ├── img2.jpg
    # │   └── ···
    # └── ···
    parser.add_argument('--gt_base_dir',
                        required=True,
                        help='Input dir of gt results')

    parser.add_argument('--save_path',
                        required=True,
                        help='Save path for the json results')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    gt_json = get_gt_json(args.request_dir, args.gt_base_dir,
                          args.data_base_dir)
    persist_2_json(gt_json, args.save_path)


if __name__ == '__main__':
    main()
