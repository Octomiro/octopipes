import os
import pathlib

import numpy as np
import cv2

from octopipes.computer_vision.annotations import Bbox, Circle
from octopipes.handlers import DefaultHandler
from octopipes.computer_vision.bboxes_handlers import BboxesHandler, CmapBboxesHandler
from octopipes.computer_vision.circle_handlers import CirclesHandler


CURRENT_DIR = pathlib.Path(os.path.dirname(__file__))
DATA_DIR = CURRENT_DIR / '..' / 'data'
OUTPUT_DIR = CURRENT_DIR / '..' / 'outputs'

def test_DefaultHandler():
    handler = DefaultHandler(None)
    assert handler.viz() == []

    handler = DefaultHandler([1, 2, 3])
    assert handler.size() == 3
    assert handler.to_json() == '[1, 2, 3]'


def test_BboxHandler():
    img = cv2.imread((DATA_DIR / 'cornell-box.png').as_posix())

    handler0 = BboxesHandler(image=img, bboxes=[])
    handler1 = BboxesHandler(image=img, bboxes=[Bbox(0, 0, 10, 10)])
    handler2 = BboxesHandler(image=img, bboxes=[Bbox(0, 0, 10, 10), Bbox(0, 0, 10, 35)])
    test_list = [[0, 0, 10, 10], [0, 0, 10, 10]]
    test_array = np.array(test_list)

    assert handler1.size() == 1
    assert handler2.size() == 2
    assert handler0.size() == 0

    assert handler1.to_json() == '{"bboxes": [[0, 0, 10, 10]]}'
    assert handler2.to_json() == '{"bboxes": [[0, 0, 10, 10], [0, 0, 10, 35]]}'
    assert handler0.to_json() == '{"bboxes": []}'

    image_outputs = handler2.viz()
    assert len(image_outputs) == 1

    out = (OUTPUT_DIR / 'test_bboxhandler.png').as_posix()
    cv2.imwrite(out, image_outputs[0])


def test_CirclesHandler():
    img = cv2.imread((DATA_DIR / 'cornell-box.png').as_posix())
    handler0 = CirclesHandler(img, circles=[])
    handler1 = CirclesHandler(img, circles=[Circle(0, 0, 50)])
    handler2 = CirclesHandler(img, circles=[Circle(0, 0, 50), Circle(150, 130, 50)])

    assert handler0.size() == 0
    assert handler1.size() == 1
    assert handler2.size() == 2

    assert handler0.to_json() == '{"circles": []}'
    assert handler1.to_json() == '{"circles": [[0, 0, 50]]}'
    assert handler2.to_json() == '{"circles": [[0, 0, 50], [150, 130, 50]]}'

    img = np.random.rand(100,100,3) * 255

    image_outputs = handler2.viz()
    assert len(image_outputs) == 1

    out = (OUTPUT_DIR / 'test_CirclesHandler.png').as_posix()
    cv2.imwrite(out, image_outputs[0])


def test_CmapBboxesHandler():
    img = cv2.imread((DATA_DIR / 'cornell-box.png').as_posix())
    handler0 = CmapBboxesHandler(img, bboxes=[])
    handler3 = CmapBboxesHandler(img, bboxes=[(Bbox(50, 50, 100, 150), 1),
                                              (Bbox(20, 45, 140, 250), 2),
                                              (Bbox(55, 60, 130, 230), 1)])

    assert handler0.size() == 0
    assert handler3.size() == 3

    assert handler0.to_json() == '{"cm_bboxes": []}'
    assert handler3.to_json() == '{"cm_bboxes": [{"bbox": [50, 50, 100, 150], "val": 1}, {"bbox": [20, 45, 140, 250], "val": 2}, {"bbox": [55, 60, 130, 230], "val": 1}]}'

    image_outputs = handler3.viz()
    assert len(image_outputs) == 1

    out = (OUTPUT_DIR / 'test_CmapBboxesHandler.png').as_posix()
    cv2.imwrite(out, image_outputs[0])
