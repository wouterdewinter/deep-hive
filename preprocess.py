"""Preprocessing image datasets, compatible with the Kaggle Dogs & Cats dataset
"""

import os, sys
from os.path import join
from server.Config import Config
from PIL import Image
from random import shuffle

# limits the amount of images to preprocess
limit = 1000

path = ''
output_path = ''

if len(sys.argv) == 3:
    path = sys.argv[1]
    output_path = sys.argv[2]
else:
    print("Preprocesses images for use in the application\nUsage: python preprocess.py <input path> <output path>")
    exit()

if not os.path.exists(output_path):
    os.makedirs(output_path)

files = next(os.walk(path))[2]
image_id = 0

# shuffle so we evenly balance the amount of images per class
shuffle(files)

for file in files[:limit]:
    filename = join(path, file)

    # only process of format is classname.id.extension
    parts = file.split('.')
    if len(parts) == 3:
        class_name = parts[0]
        output_class_path = join(output_path, class_name)
        output_filename = join(output_class_path, str(image_id) + '.png')

        if not os.path.exists(output_class_path):
            os.makedirs(output_class_path)

        try:
            img = Image.open(filename)
            img = img.resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE))
            img.save(output_filename, 'PNG')
            print("Processed: %s" % filename)
        except:
            print("Error processing image: %s" % filename)
            pass

        image_id += 1

print("Preprocessed %d images" % image_id)