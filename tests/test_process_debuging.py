from octopipes.process_debuging import echo_bbox_outofbound


def test_echo_bbox_outofbound(capfd):
    echo_bbox_outofbound(100, 100)([(0, 0, 0, 0)])
    out, _ = capfd.readouterr()
    assert out == ''

    echo_bbox_outofbound(50, 50)([(50, 50, 100, 100)])
    out, _ = capfd.readouterr()
    assert out.startswith('Out of bound bbox')
