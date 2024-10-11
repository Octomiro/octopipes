"""General useful set of processes"""

def circles_to_bboxes(circles) -> list:
    return [(int(x) - int(r), int(y) - int(r), int(x) + int(r), int(y) + int(r)) 
            for x, y, r in circles]
