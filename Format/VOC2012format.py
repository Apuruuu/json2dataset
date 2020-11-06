from xml.dom.minidom import Document

def XML_writer(filename, # 'xxx.jpg'
            size, # (width, height, depth)
            regions, # [{'label':car, 'xmin':200, 'ymin':300, 'xmax':500, 'ymax':400}, ...]
            folder='VOC2012',
            database='KLAB2020', 
            segmented=0, 
            truncated=0,
            ):

    Doc = Document()
    annotation = Doc.createElement('annotation')
    Doc.appendChild(annotation)

    Folder = Doc.createElement('Folder')
    Folder.appendChild(Doc.createTextNode(str(folder)))
    annotation.appendChild(Folder)

    Filename = Doc.createElement('filename')
    Filename.appendChild(Doc.createTextNode(str(filename)))
    annotation.appendChild(Filename)

    source = Doc.createElement('source')
    Database = Doc.createElement('database')
    Database.appendChild(Doc.createTextNode(str(database)))
    source.appendChild(Database)
    annotation.appendChild(source)

    Size = Doc.createElement('size') # fix add size
    Width = Doc.createElement('width')
    Width.appendChild(Doc.createTextNode(str(size[0])))
    height = Doc.createElement('height')
    height.appendChild(Doc.createTextNode(str(size[1])))
    Depth = Doc.createElement('depth')
    Depth.appendChild(Doc.createTextNode(str(size[2])))
    Size.appendChild(Width)
    Size.appendChild(height)
    Size.appendChild(Depth)
    annotation.appendChild(Size)

    Segmented = Doc.createElement('segmented')
    Segmented.appendChild(Doc.createTextNode(str(segmented)))
    annotation.appendChild(Segmented)

    for region in regions:
        _object = Doc.createElement('object')
        annotation.appendChild(_object)
        name = Doc.createElement('name')
        name.appendChild(Doc.createTextNode(str(region['label'])))
        _object.appendChild(name)

        pose = Doc.createElement('pose')
        pose.appendChild(Doc.createTextNode('Unspecified'))
        _object.appendChild(pose)

        Truncated = Doc.createElement('truncated')
        Truncated.appendChild(Doc.createTextNode(str(truncated)))
        _object.appendChild(Truncated)

        Difficult = Doc.createElement('difficult')
        Difficult.appendChild(Doc.createTextNode('0'))
        _object.appendChild(Difficult)

        Bndbox = Doc.createElement('bndbox')
        _object.appendChild(Bndbox)

        Xmin = Doc.createElement('xmin')
        Xmin.appendChild(Doc.createTextNode(str(region['xmin'])))
        Bndbox.appendChild(Xmin)
        Ymin = Doc.createElement('ymin')
        Ymin.appendChild(Doc.createTextNode(str(region['ymin'])))
        Bndbox.appendChild(Ymin)
        Xmax = Doc.createElement('xmax')
        Xmax.appendChild(Doc.createTextNode(str(region['xmax'])))
        Bndbox.appendChild(Xmax)
        Ymax = Doc.createElement('ymax')
        Ymax.appendChild(Doc.createTextNode(str(region['ymax'])))
        Bndbox.appendChild(Ymax)

    return Doc.toprettyxml()

# debug
if __name__ == "__main__":
    size = (1920,1080,3)
    regions = [{'label': 'truck', 'xmin': 172, 'ymin': 128, 'xmax': 286, 'ymax': 287}, {'label': 'car', 'xmin': 640, 'ymin': 680, 'xmax': 727, 'ymax': 790}, {'label': 'car', 'xmin': 638, 'ymin': 849, 'xmax': 733, 'ymax': 972}, {'label': 'car', 'xmin': 744, 'ymin': 870, 'xmax': 823, 'ymax': 979}, {'label': 'car', 'xmin': 835, 'ymin': 216, 'xmax': 885, 'ymax': 282}]

    with open("test.xml", 'w') as f:
        xml = XML_writer(filename='xxx.jpg', size=size, regions=regions)
        f.write(xml)