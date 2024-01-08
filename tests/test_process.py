from octopipes.process import circles_to_bboxes


def test_circles_to_bboxes():
    assert circles_to_bboxes([]) == []
    assert circles_to_bboxes([(0, 0, 0)]) == [(0, 0, 0, 0)]
    assert circles_to_bboxes([(0, 0, 0), (0, 0, 0)]) == [(0, 0, 0, 0), (0, 0, 0, 0)]
