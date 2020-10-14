import json
import os
import re
import numpy
import time

import cv2

class CropImage():
    def __init__(self, filename, ROI):
        self.ROI = ROI
        self.filename = filename
        self.outpath = 'dataset'

    def cut(self):
        img = cv2.imread(self.filename)
        for roi in self.ROI:
            crop = img[roi[1]:roi[2], roi[3]:roi[4]]
            save(roi[0], crop)

        imwrite.release()
        cv2.destroyAllWindows()

    def save(folder, crop):
        path = os.path.join(self.outpath, floder, str(time()) + ".jpg")
        cv2.imwrite(path, crop)

    def path_check(path):
        for folder in paths:
            if os.path.exists(folder):


def json_reader(path, filename):
    # load shapes
    _file = json.load(open(os.path.join(path, filename)))
    shapes = _file['shapes']

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
        regions.append([label, ymin, ymax, xmin, xmax])



    return labels, regions

# def path_check(path):
#     for folder in paths:
#         if os.path.exists(folder):

#     检测path， 如果没有则添加

# cutROI（图片路径，ROI）

if __name__ == "__main__":
    # workpath = "dataset"
    # if not os.path.exists(workpath):
    #     os.mkdir(workpath)
    # os.chdir(workpath)


    labels, regions = json_reader('C:\\Users\\wyf55\\Documents\\GitHub\\json2dataset', 'train90m00003.json')
    print(labels, regions)
    CropImage('C:\\Users\\wyf55\\Documents\\GitHub\\json2dataset\\train90m00003.jpg', labels, regions)



    
