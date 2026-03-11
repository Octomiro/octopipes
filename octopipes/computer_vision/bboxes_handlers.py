from dataclasses import dataclass
import json
from typing import Tuple

import numpy as np

from octopipes.computer_vision.viz_utils import viz_opencv_bboxes, viz_opencv_cm_bboxes
from .annotations import Bbox


@dataclass
class BboxesHandler():
    image: np.ndarray
    bboxes: list[Bbox]

    def viz(self, _ : str = 'default') -> list[np.ndarray]:
        image = self.image.copy()

        return [viz_opencv_bboxes(image, self.bboxes)]

    def to_json(self) -> str:
        return json.dumps({
            'bboxes': [b.to_list() for b in self.bboxes],
        })

    def size(self) -> int | None:
        return len(self.bboxes)

@dataclass
class CmapBboxesHandler():
    """CmapBboxesHandler colors bboxes with a colormap.
    Output is expected to be [(bbox, value), ...]"""
    image: np.ndarray
    bboxes: list[Tuple[Bbox, int]]

    def viz(self, _: str = 'default'):
        image = self.image.copy()

        return [viz_opencv_cm_bboxes(image, self.bboxes)]

    def to_json(self) -> str:
        return json.dumps({
            'cm_bboxes': [{'bbox': b.to_list(), 'val': v} for b, v in self.bboxes],
        })

    def size(self) -> int | None:
        return len(self.bboxes)
