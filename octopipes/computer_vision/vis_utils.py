from typing import Tuple
import numpy as np

from octopipes.computer_vision.annotations import Bbox, Circle, Point


def viz_opencv_bboxes(image: np.ndarray, bboxes: list[Bbox]) -> np.ndarray:
    """displays bounding boxes on the supplied image"""
    import cv2

    color = np.random.choice(range(256), size=3).tolist()

    for bbox in bboxes:
        cv2.rectangle(image, (bbox.x0, bbox.y0), (bbox.x1, bbox.y1), color, 3)

    return image


def viz_opencv_cm_bboxes(image: np.ndarray, bboxes: list[Tuple[Bbox, int]]) -> np.ndarray:
    """displays bounding boxes with a color map on the supplied image"""
    import cv2
    import cmap

    boxes, values = zip(*bboxes)
    values = np.array(values)
    norm_values = (values - values.min()) / (values.max() - values.min())
    cm = cmap.Colormap('viridis')(norm_values)

    for i, bbox in enumerate(boxes):
        color = np.array(255 * cm[i, :3], dtype=int)
        cv2.rectangle(image,
                      (bbox.x0, bbox.y0), (bbox.x1, bbox.y1),
                      (int(color[0]), int(color[1]), int(color[2])), 3)

    return image


def viz_opencv_points(image: np.ndarray, points: list[Point]) -> np.ndarray:
    import cv2

    color = tuple(map(int, np.random.choice(range(256), size=3)))

    for p in points:
        cv2.circle(image, (p.x, p.y), 8, color, 3)

    return image

def viz_opencv_circles(image: np.ndarray, circles: list[Circle]) -> np.ndarray:
    import cv2

    color = tuple(map(int, np.random.choice(range(256), size=3)))
    for c in circles:
        cv2.circle(image, (c.x, c.y), int(c.r), color, 3)

    return image

