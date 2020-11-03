import os
import argparse
from pyretri.datasets.base import persist_2_json, read_xlsx, download_img


def parse_args():
    parser = argparse.ArgumentParser(
        description='Making json file from xlsx file')
    parser.add_argument(
        '--xlsx_file_path',
        '-xf',
        default=
        '/home/yanghui/yanghui/data/image_retrieval/daneng/7月防作弊对应数据样本v1.0.xlsx',
        help='Input dir of xlsx file')
    parser.add_argument('--sheet_name',
                        '-sn',
                        default='Sheet3',
                        help='sheet name which sheet need to be process')
    parser.add_argument('--usecols',
                        '-c',
                        default=[3, 6, 7],
                        type=list,
                        help='cols which is needed to be process')
    parser.add_argument(
        '--query_save_dir',
        '-qs',
        default='/home/yanghui/yanghui/data/image_retrieval/daneng/imgs/query',
        help='download img and save path as query')
    parser.add_argument(
        '--gallery_save_dir',
        '-gs',
        default=
        '/home/yanghui/yanghui/data/image_retrieval/daneng/imgs/gallery',
        help='download img and save path as gallery')
    parser.add_argument('--img_save_dir',
                        '-is',
                        default=None,
                        help='download img and save path')
    parser.add_argument(
        '--json_save_path',
        '-js',
        default='/home/yanghui/yanghui/data/image_retrieval/daneng/daneng.json',
        help='Save path for the json results')

    args = parser.parse_args()
    return args


def get_imgs(data):
    for img_path1, img_path2, is_similar in data:
        yield img_path1, img_path2, is_similar


def add_request_2_dict(result_dict, similar_img_list, request_img,
                       similar_img):
    if request_img in similar_img_list:
        return result_dict, similar_img_list

    if request_img in result_dict.keys():
        result_dict[request_img].append(similar_img)
    else:
        result_dict[request_img] = [similar_img]

    similar_img_list.append(similar_img)
    return result_dict, similar_img_list


def main():
    args = parse_args()
    data = read_xlsx(args.xlsx_file_path, args.sheet_name, args.usecols)

    result_dict, similar_img_list = dict(), list()
    for img_path1, img_path2, is_similar in get_imgs(data):
        print(img_path1, img_path2, is_similar)
        if args.img_save_dir is not None:
            download_img(img_path1, args.img_save_dir)
            download_img(img_path2, args.img_save_dir)

        request_img = os.path.basename(img_path1)
        similar_img = os.path.basename(img_path2)

        if is_similar == '是':
            result_dict, similar_img_list = add_request_2_dict(
                result_dict, similar_img_list, request_img, similar_img)
            if args.query_save_dir is not None:
                download_img(img_path1,
                             args.query_save_dir,
                             sub_dir=request_img.split('.jpg')[0])

            if args.gallery_save_dir is not None:
                download_img(img_path2,
                             args.gallery_save_dir,
                             sub_dir=request_img.split('.jpg')[0])
        else:
            if args.gallery_save_dir is not None:
                download_img(img_path1,
                             args.gallery_save_dir,
                             sub_dir=request_img.split('.jpg')[0])
                download_img(img_path2,
                             args.gallery_save_dir,
                             sub_dir=similar_img.split('.jpg')[0])

    if len(result_dict.keys()):
        persist_2_json(result_dict, args.json_save_path, write_type='a')


if __name__ == "__main__":
    main()