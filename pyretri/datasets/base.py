import os
import cv2
import json
import urllib.request

import pandas as pd


def persist_2_json(gt_json, save_path, write_type='w'):
    with open(save_path, write_type) as f:
        json.dump(gt_json, f)


def read_xlsx(xlsx_file_path, sheet_name, cols):
    df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name, usecols=cols)
    return df.values


def download_img(imgurl, save_dir, sub_dir=None):
    imgurl = imgurl.replace('\"', '')

    if sub_dir is not None:
        save_dir = os.path.join(save_dir, sub_dir)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    try:
        img_path = '{}/{}'.format(save_dir, imgurl.split('/')[-1])
        img = cv2.imread(img_path)
        if img is None:
            urllib.request.urlretrieve(imgurl, img_path)
        return True
    except:
        return False
