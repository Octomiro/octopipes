"""General debuging processes for workflow troubleshooting"""

def echo_output(input):
    print(input)
    return input

def echo_bbox_outofbound(width: int, height: int):
    """Echo out of bound bboxes"""
    def check_bbox_outofbound(bboxes):
        for x, y, maxx, maxy in bboxes:
            if (x > width or maxx > width or 
                    y > height or maxy > height):
                print(f'Out of bound bbox {(x, y, maxx, maxy)}')
        return bboxes
    return check_bbox_outofbound
