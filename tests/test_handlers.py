from octopipes.handlers import DefaultHandler


def test_DefaultHandler():
    handler = DefaultHandler()
    assert handler.output_on_image(None, None) is None
    assert handler.len_output([1, 2, 3]) is None
    assert handler.to_json([1, 2, 3]) == '{}'
