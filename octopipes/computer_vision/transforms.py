import numpy as np


def mask_to_xyxy(mask: np.ndarray) -> np.ndarray:
    bboxes = np.zeros((1, 4), dtype=int)

    rows, cols = np.where(mask)

    if len(rows) > 0 and len(cols) > 0:
        x_min, x_max = np.min(cols), np.max(cols)
        y_min, y_max = np.min(rows), np.max(rows)
        bboxes[0, :] = [x_min, y_min, x_max, y_max]

    return bboxes
