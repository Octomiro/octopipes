import numpy as np

from octopipes.handlers import BboxesHandler, CirclesHandler, CmapBboxesHandler, DefaultHandler


def test_DefaultHandler():
    handler = DefaultHandler()
    assert handler.output_on_image(None, None) is None
    assert handler.len_output([1, 2, 3]) == 3
    assert handler.to_json([1, 2, 3]) == '[1, 2, 3]'


def test_BboxHandler():
    handler = BboxesHandler()
    test_list = [[0, 0, 10, 10], [0, 0, 10, 10]]
    test_array = np.array(test_list)

    assert handler.len_output([[0, 0, 10, 10]]) == 1
    assert handler.len_output(test_list) == 2
    assert handler.len_output(test_array) == 2

    assert handler.to_json([[0, 0, 10, 10]]) == '{"bboxes": [{"bbox": [0, 0, 10, 10]}], "len_output": 1}'
    assert handler.to_json(np.array([[0, 0, 10, 10]])) == '{"bboxes": [{"bbox": [0, 0, 10, 10]}], "len_output": 1}'
    assert handler.to_json([[]]) == '{"bboxes": [{"bbox": []}], "len_output": 1}'
    assert handler.to_json(np.array([[]])) == '{"bboxes": [{"bbox": []}], "len_output": 1}'
    assert handler.to_json(np.array([])) == '{"bboxes": [], "len_output": 0}'
    assert handler.to_json(None) == '{"bboxes": null, "len_output": 0}'


def test_CirclesHandler():
    handler = CirclesHandler()
    test_list = [[0, 0, 10], [10, 7, 5]]
    test_array = np.array(test_list)

    assert handler.len_output(test_list) == 2
    assert handler.len_output(test_array) == 2

    assert handler.to_json(test_list) == '{"circles": [[0, 0, 10], [10, 7, 5]], "len_output": 2}'
    assert handler.to_json(test_array) == '{"circles": [[0, 0, 10], [10, 7, 5]], "len_output": 2}'
    assert handler.to_json([]) == '{"circles": [], "len_output": 0}'
    assert handler.to_json(None) == '{"circles": null, "len_output": 0}'


def test_CmapBboxesHandler():
    handler = CmapBboxesHandler()
    test_list = [([0, 0, 10, 10], 1), ([0, 0, 10, 10], 2)]

    assert handler.len_output(test_list) == 2

    assert handler.to_json(test_list) == '{"bboxes": [{"bbox": [0, 0, 10, 10], "val": 1}, {"bbox": [0, 0, 10, 10], "val": 2}], "len_output": 2}'
    assert handler.to_json([]) == '{"bboxes": [], "len_output": 0}'
    assert handler.to_json(None) == '{"bboxes": null, "len_output": 0}'

