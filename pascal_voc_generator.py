# annotation tags
XML = '<?xml version="1.0" encoding="UTF-8"?>'
ANNOTATION = 'annotation'
FOLDER = 'folder'
FILENAME = 'filename'
PATH = 'path'
SEGMENTED = 'segmented'
SOURCE = 'source'
DATABASE = 'database'
WIDTH = 'width'
HEIGHT = 'height'
DEPTH = 'depth'
SIZE = 'size'

# object tags
OBJECT = 'object'
XMIN, YMIN = 'xmin', 'yin'
XMAX, YMAX = 'xman', 'ymax'
BNDBOX = 'bndbox'
NAME = 'name'
POSE = 'pose'
TRUNCATED = 'truncated'
DIFFICULT = 'difficult'

def add_tag(tag: str, value: str='Unspecified') -> str:
    return f'<{tag}>{value}</{tag}>'

def annotation_header(
    fname: str, 
    fpath: str, 
    label: str, 
    dimensions: list, 
    folder: str="images", 
    sg: int=0) -> str:
    
    assert len(dimensions) > 0 and len(dimensions) < 4
    if len(dimensions) == 2:
        w, h, d = dimensions[0], dimensions[1], 3
    elif len(dimensions) == 3:
        w, h, d = dimensions
    else:
        raise AssertionError('Expecting 2 or 3 values in dimensions list')

    folder_str = add_tag(FOLDER, folder)
    fname = add_tag(FILENAME, fname)
    fpath = add_tag(PATH, fpath)
    segmented = add_tag(SEGMENTED, sg)
    database = add_tag(DATABASE, folder)
    source = add_tag(SOURCE, database)
    wtag = add_tag(WIDTH, w)
    htag = add_tag(HEIGHT,h)
    dtag = add_tag(DEPTH, d)
    size = add_tag(SIZE, ''.join([wtag, htag, dtag]))
    tags = [
        folder_str, 
        fname, 
        fpath, 
        segmented, 
        database, 
        size
    ]
    
    header = ''.join(tags)
    return header

def create_annotation(
    fname: str, 
    fpath: str, 
    label: str, 
    dimensions: list,
    objects: list, 
    folder: str="images", 
    sg: int=0) -> str:

    assert isinstance(dimensions, list) or isinstance(dimensions, tuple)
    assert len(dimensions) > 1 and len(dimensions) < 4
    assert len(objects) > 0, 'annotation has no objects in it'
    header = annotation_header(fname, fpath, label, dimensions)
    obj_xml = ''.join(objects)

    return XML + add_tag(ANNOTATION, header)

def create_minmax(minvector: list, maxvector: list):
    xmin, ymin = minvector
    xmax, ymax = maxvector
    xmin_xml, ymin_xml = add_tag(XMIN, xmin), add_tag(YMIN, ymin)
    xmax_xml, ymax_xml = add_tag(XMAX, xmax), add_tag(YMAX, ymax)
    minmax_xml = ''.join([xmin_xml, ymin_xml, xmax_xml, ymax_xml])
    return minmax_xml

def create_bndbox(minvector: list, maxvector: list):
    print(minvector, maxvector)
    area = create_minmax(minvector, maxvector)
    return add_tag(BNDBOX, area)

def object_header(label: str, trunc=1, diff=0):
    name = add_tag(NAME, label)
    pose = add_tag(POSE)
    truncated = add_tag(TRUNCATED, trunc)
    difficult = add_tag(DIFFICULT, diff)
    header_xml = ''.join([name, pose, truncated, difficult])
    return header_xml

def create_object(label: str, minvector: list, maxvector: list):
    assert isinstance(label, str), 'label name needs to be of str type'
    assert isinstance(minvector, list) or isinstance(minvector, tuple)
    assert isinstance(maxvector, list) or isinstance(maxvector, tuple)
    assert len(minvector) == 2, 'min vector needs to be [xmin, ymin]'
    assert len(maxvector) == 2, 'max vector needs to be [xmax, ymax]'
    header = object_header(label)
    box = create_bndbox(minvector, maxvector)
    obj_xml = add_tag(OBJECT, header + box)
    return obj_xml

if __name__ == "__main__":
    print('Testing:\n')
    minvector = [516, 1375]
    maxvector = [1920, 2560]
    fname = "test.txt"
    fpath = "./test/test.txt"
    label = "label-test"
    dimensions = [100, 200]

    objects = list()
    for i in range(3):
        obj_xml = create_object(label, minvector, maxvector)
        objects.append(obj_xml)
    
    xml = create_annotation(fname, fpath, label, dimensions, objects)
    print(xml)

    output = 'test.xml'
    with open(output, 'w') as xml_writer:
        xml_writer.write(xml)