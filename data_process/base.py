import json
import urllib.request

import pandas as pd


def persist_2_json(gt_json, save_path, write_type='w'):
    with open(save_path, write_type) as f:
        json.dump(gt_json, f)


def read_xlsx(xlsx_file_path, sheet_name, cols):
    df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name, usecols=cols)
    return df.values


def download_img(imgurl, save_dir):
    imgurl = imgurl.replace('\"', '')
    try:
        urllib.request.urlretrieve(
            imgurl, '{}/{}'.format(save_dir,
                                   imgurl.split('/')[-1]))
        return True
    except expression as identifier:
        print(identifier)
        return False