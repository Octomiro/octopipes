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

def viz_opencv_sam_segmentation(image: np.ndarray, segmentation) -> np.ndarray:
    import cv2

    sorted_anns = sorted(segmentation, key=(lambda x: x['area']), reverse=True)
    w, h = sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1]
    overlay_mask = np.zeros((w, h, 3), dtype=np.uint8)

    for ann in sorted_anns:
        mask = ann['segmentation']
        overlay_mask[mask] = np.random.randint(256, size=3, dtype=np.uint8)

    overlayed = cv2.addWeighted(image, 1, overlay_mask, 0.3, 20)

    return overlayed 

def viz_opencv_sam_predictor_segmentation(image: np.ndarray, segmentation) -> np.ndarray:
    import cv2

    # Get the masks from segmentation model
    masks, scores, _ = segmentation

    height = masks.shape[1]
    width = masks.shape[2]

    overlay_masks = []
    text_position = (0, 100)
    for idx in range(masks.shape[0]):
        overlay_mask = np.zeros((height, width, 3), dtype=np.uint8)
        m = masks[idx]
        overlay_mask[m] = np.random.randint(256, size=3, dtype=np.uint8)
        overlay_masks.append(overlay_mask)

    images = []
    for idx, overlay_mask in enumerate(overlay_masks):
        overlayed = cv2.addWeighted(image, 1, overlay_mask, 0.7, 20)
        cv2.putText(overlayed, f'Score: {scores[idx]:.3f}',
                    text_position, cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 2, cv2.LINE_AA)
        images.append(overlayed)

    return np.concatenate(images, axis=0)
