import numpy as np

from octopipes.handlers import BboxesHandler, CirclesHandler, DefaultHandler


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

    assert handler.to_json([[0, 0, 10, 10]]) == '[[0, 0, 10, 10]]'
    assert handler.to_json(np.array([[0, 0, 10, 10]])) == '[[0, 0, 10, 10]]'
    assert handler.to_json([[]]) == '[[]]'
    assert handler.to_json(np.array([[]])) == '[[]]'
    assert handler.to_json(np.array([])) == '[]'
    assert handler.to_json(None) == 'null'


def test_CirclesHandler():
    handler = CirclesHandler()
    test_list = [[0, 0, 10], [10, 7, 5]]
    test_array = np.array(test_list)

    assert handler.len_output(test_list) == 2
    assert handler.len_output(test_array) == 2

    assert handler.to_json(test_list) == '[[0, 0, 10], [10, 7, 5]]'
    assert handler.to_json(test_array) == '[[0, 0, 10], [10, 7, 5]]'
    assert handler.to_json([]) == '[]'
    assert handler.to_json(None) == 'null'

