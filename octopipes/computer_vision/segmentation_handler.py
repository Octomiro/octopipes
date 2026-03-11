import json

import numpy as np

from octopipes.handlers import DefaultHandler


class SamSegmentationHandler(DefaultHandler):
    """SamSegmentation handles segmentation output from a SAM predictor."""
    image: np.ndarray

    def viz(self, _: str) -> list[np.ndarray]:
        import numpy as np
        import cv2

        sorted_anns = sorted(self.output, key=(lambda x: x['area']), reverse=True)
        w, h = sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1]
        overlay_mask = np.zeros((w, h, 3), dtype=np.uint8)
        for ann in sorted_anns:
            mask = ann['segmentation']
            overlay_mask[mask] = np.random.randint(256, size=3, dtype=np.uint8)
        overlayed = cv2.addWeighted(self.image, 1, overlay_mask, 0.3, 20)
        return [overlayed]

    def to_json(self) -> str:
        return json.dumps({'segmentation': self.output.tolist(),
                           'len_output': self.size()})

    def size(self) -> int | None:
        return len(self.output) if self.output is not None else 0
