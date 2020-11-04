import os
from PIL import Image

img_dir = '/home/yanghui/yanghui/data/image_retrieval/daneng/imgs/query'

for item_dir in os.listdir(img_dir):
    dir_path = '{}/{}'.format(img_dir, item_dir)
    for item_img in os.listdir(dir_path):
        img_path = os.path.join(dir_path, item_img)
        try:
            img = Image.open(img_path).convert("RGB")
        except:
            print(f'remove img_path: {img_path}')
            os.remove(img_path)
            if len(os.listdir(dir_path)) == 0:
                print(f'remove img_dir: {dir_path}')
                os.removedirs(dir_path)
