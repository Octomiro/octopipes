import json

import numpy as np

from octopipes.computer_vision import transforms
from octopipes.computer_vision.viz_utils import viz_opencv_sam_predictor_segmentation, viz_opencv_sam_segmentation
from octopipes.handlers import DefaultHandler


class SamSegmentationHandler(DefaultHandler):
    """SamSegmentation handles segmentation output from a SAM predictor."""
    image: np.ndarray

    def viz(self, param: str = 'default') -> list[np.ndarray]:
        return [viz_opencv_sam_segmentation(self.image.copy(), self.output)]

    def to_json(self) -> str:
        return json.dumps({'segmentation': self.output.tolist(),
                           'len_output': self.size()})

    def size(self) -> int | None:
        return len(self.output) if self.output is not None else 0

class PredictorSamSegmentationHandler(DefaultHandler):
    """PredictorSamSegmentationHandler handles sam's predictor output"""
    image: np.ndarray

    def viz(self, param: str = 'default') -> list[np.ndarray]:
        return [viz_opencv_sam_predictor_segmentation(self.image.copy(), self.output)]

    def to_json(self) -> str:
        masks, scores, _ = self.output

        output_dict = []
        for idx in range(masks.shape[0]):
            score = scores[idx]
            bbox = transforms.mask_to_xyxy(masks[idx])
            output_dict.append({'score': score, 'bbox': bbox})

        return json.dumps(output_dict)

    def size(self) -> int | None:
        return len(self.output[0].shape[0])
