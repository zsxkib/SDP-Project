# run this script under TACO/data folder

from matplotlib import pyplot as plt
from tqdm import tqdm
import lycon
import json
import sys
import os

OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'cropped'

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

annotations = json.load(open('annotations.json'))

category_id_to_name = {}
for c in annotations['categories']:
    category_id_to_name[c['id']] = c['name']

image_id_to_array = {}
for i in tqdm(annotations['images'], desc='loading images'):
    image_id_to_array[i['id']] = lycon.load(i['file_name'])

for i, a in enumerate(
    tqdm(annotations['annotations'], desc='loading annotations')
):
    image = image_id_to_array[ a['image_id'] ]
    label = category_id_to_name[ a['category_id'] ]
    x, y, w, h = map(int, a['bbox'])
    crop = image[y : y+h, x : x+w] # image is height first width second
    filename = str(i) + '.png'
    filepath = os.path.join(OUTPUT_DIR, label)
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    try:
        plt.imsave(os.path.join(filepath, filename), crop)
    except:
        print('error on saving annotation', a['id'], 'from image', a['image_id'])
