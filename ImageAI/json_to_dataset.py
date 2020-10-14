import json
import os
import re
import numpy
import time
from labelme import utils

import cv2

class CropImage():
    def __init__(self, file_dir, outpath):
        self.outpath = outpath
        self.imgpath = file_dir
        self.folder = []
        for folder in os.listdir(self.outpath):
            if os.path.isdir(os.path.join(self.outpath, folder)):
                self.folder.append(folder)
        self.json_reader()

    def cut(self, img, labels, regions):
        for num in range(len(labels)):
            roi = regions[num]
            label = labels[num]
            
            crop = img[roi[0]:roi[1], roi[2]:roi[3]]
            self.save(label, crop)

    def save(self, label, crop):
        if not label in self.folder:
            os.mkdir(os.path.join(self.outpath, label))
            self.folder.append(label)

        img_list = numpy.hstack(numpy.hstack(crop)).tolist()
        img_str = ''.join(str(s) for s in img_list if s not in ['NONE','NULL'])
        path = os.path.join(self.outpath, label, str(hash(img_str)) + ".jpg")
        cv2.imwrite(path, crop)

    def json_reader(self):
        # load shapes
        data = json.load(open(self.imgpath))

        imageData = data.get("imageData")

        img = utils.img_b64_to_arr(imageData)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        shapes = data['shapes']

        labels = []
        regions = []
        for shape in shapes:
            label = re.split('\d+$', shape['label'])[0]
            labels.append(label)

            original_region = numpy.array(shape['points'], 
                                                dtype='int' # 取整 Rounding
                                                )
            original_region_max = numpy.max(original_region, axis=0)
            original_region_min = numpy.min(original_region, axis=0)
            xmin, ymin = original_region_min
            xmax, ymax = original_region_max
            regions.append([ymin, ymax, xmin, xmax])
        self.cut(img, labels, regions)


if __name__ == "__main__":
    outpath = 'dataset'
    imgpath = 'images'
    
    filenames = []
    for file in os.walk(imgpath):
        for filename in file[2]:
            if os.path.splitext(filename)[1] == '.json':
                filenames.append(filename)

    for filename in filenames:
        file_dir = os.path.join(imgpath, filename)
        CropImage(file_dir, outpath)