"""General useful set of processes"""

def circles_to_bboxes(circles) -> list:
    return [(int(x - r), int(y + r), int(x + r), int(y - r))
                for x, y, r in circles]
