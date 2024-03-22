import logging
import json
from typing import Any, Protocol

import cmap


logger = logging.getLogger(__name__)

class HandlerInterface(Protocol):
    def output_on_image(self, image, output):
        pass

    def len_output(self, output: Any) -> int | None:
        pass

    def to_json(self, output: Any) -> str: # type: ignore
        pass


class DefaultHandler:
    def output_on_image(self, image, output):
        return image

    def len_output(self, output: Any) -> int | None:
        return len(output)

    def to_json(self, output: Any) -> str:
        return json.dumps(output)


class SegmentationMasksHandler:
    def output_on_image(self, image, output):
        import numpy as np
        import cv2

        sorted_anns = sorted(output, key=(lambda x: x['area']), reverse=True)
        w, h = sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1]
        overlay_mask = np.zeros((w, h, 3), dtype=np.uint8)
        for ann in sorted_anns:
            mask = ann['segmentation']
            overlay_mask[mask] = np.random.randint(256, size=3, dtype=np.uint8)
        overlayed = cv2.addWeighted(image, 1, overlay_mask, 0.3, 20)
        return overlayed

    def to_json(self, output) -> str:
        return json.dumps(output.tolist())

    def len_output(self, output: Any) -> int | None:
        return len(output)


class BboxesHandler:
    def output_on_image(self, image, output):
        import cv2
        import numpy as np

        if output is None:
            return image
        color = np.random.choice(range(256), size=3).tolist()
        for bbox in output:
            cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 3)

        return image

    def to_json(self, output) -> str:
        try:
            # convert to list if object is np array
            output = output.tolist()
        except AttributeError:
            pass
        return json.dumps({'bboxes': [{'bbox': bbox} for bbox in output] if output is not None else None})

    def len_output(self, output: Any) -> int | None:
        return len(output)


class CmapBboxesHandler:
    """CmapBboxesHandler colors bboxes with a colormap.
    Output is expected to be [(value, bbox), ...]"""

    def output_on_image(self, image, output):
        import cv2
        import numpy as np

        values, bboxes = zip(*output)
        values = np.array(values)
        norm_values = (values - values.min()) / (values.max() - values.min())
        cm = cmap.Colormap('viridis')(norm_values)

        for i, bbox in enumerate(bboxes):
            color = np.array(255 * cm[i, :3], dtype=int)
            cv2.rectangle(image,
                          (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                          (color[0], color[1], color[2]), 3)
        
        return image

    def to_json(self, output) -> str:
        try:
            # convert to list if object is np array
            output = output.tolist()
        except AttributeError:
            pass
        return json.dumps({'bboxes': [{'bbox': bbox, 'val': val} for bbox, val in output] if output is not None else None})

    def len_output(self, output: Any) -> int | None:
        return len(output)


class CirclesHandler:
    """CirclesHandler handles output of the form [(x, y, radius), ...]"""

    def output_on_image(self, image, output):
        import cv2
        import numpy as np

        if output is None:
            return image

        for x, y, r in output:
            color = list(np.random.choice(range(256), size=3))
            cv2.circle(image, (int(x), int(y)), int(r), color, 3)
        return image

    def to_json(self, output) -> str:
        try:
            # convert to list if object is np array
            output = output.tolist()
        except AttributeError:
            pass
        return json.dumps({'circles': output})

    def len_output(self, output: Any) -> int | None:
        return len(output)

