import json
import os
import re
import numpy
import time
from labelme import utils

import cv2

class Json2dataset():
    def __init__(self, jsonpath, filename, outpath, saveas, 
                    saveimg=False, # save image form .json file
                    ):
        self.filename = filename
        self.outpath = outpath
        shapes = self.json_reader(jsonpath)
        self.get_regions(shapes)
        if saveas == 'VOC2012':
            self.voc2012format(saveimg)
            
    def json_reader(self, jsonpath):
        # load .json file
        data = json.load(open(os.path.join(jsonpath, filename + ".json")))
        
        # json to jpg
        imageData = data.get("imageData")
        img = utils.img_b64_to_arr(imageData)
        self.size = img.shape
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # get shapes
        shapes = data['shapes']
        return shapes

    def get_regions(self, shapes):
        regions = []
        for shape in shapes:
            _object = {}

            label = re.split('\d+$', shape['label'])[0]
            _object["label"] = label

            original_region = numpy.array(shape['points'], 
                                                dtype='int' # 取整 Rounding
                                                )
            original_region_max = numpy.max(original_region, axis=0)
            original_region_min = numpy.min(original_region, axis=0)
            _object["xmin"], _object["ymin"] = original_region_min
            _object["xmax"], _object["ymax"] = original_region_max
            regions.append(_object)
        self.regions = regions

    def voc2012format(self, saveimg):
        from Format.VOC2012format import XML_writer

        xml_output_path = os.path.join(self.outpath, 'Annotations')
        if not os.path.exists(xml_output_path):
            os.makedirs(xml_output_path)
        xml_output_path_filename = os.path.join(xml_output_path, self.filename+".xml")

        with open(xml_output_path_filename, 'w') as f:
            xml = XML_writer(filename=self.filename+".jpg", size=self.size, regions=self.regions)
            f.write(xml)

        if saveimg:
            jpg_outpath = os.path.join(self.outpath, 'JPEGImages')
            if not os.path.exists(jpg_outpath):
                os.makedirs(jpg_outpath)
            self.img_save(path=jpg_outpath, filename=self.filename, img=self.img)

    def img_save(self, img, filename, path):
        cv2.imwrite(os.path.join(path, filename+".jpg"), img)

if __name__ == "__main__":
    outpath = 'dataset'
    imgpath = 'images'
    saveas = 'VOC2012'

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    
    filenames = []
    for file in os.walk(imgpath):
        for filename in file[2]:
            if os.path.splitext(filename)[1] == '.json':
                filenames.append(filename[:-5])

    for filename in filenames:
        Json2dataset(jsonpath=imgpath, filename=filename, outpath=outpath, saveas=saveas, saveimg=True)
