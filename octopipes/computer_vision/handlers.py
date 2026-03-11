from dataclasses import dataclass
import json
from typing import Tuple

import numpy as np

from octopipes.computer_vision.vis_utils import viz_opencv_bboxes, viz_opencv_cm_bboxes, viz_opencv_points
from octopipes.handlers import DefaultHandler
from .annotations import Point, Bbox


@dataclass
class ImageHandler(DefaultHandler):
    input_image: np.ndarray
    masks: list[np.ndarray]
    heat_maps_2d: list[np.ndarray]
    bboxes: list[Bbox]
    cm_bboxes: list[Tuple[Bbox, int]]
    points: list[Point]
    images: list[np.ndarray]

    def viz(self, _: str = 'default') -> list[np.ndarray]:
        image = self.input_image.copy()

        if len(self.bboxes) > 0:
            image = viz_opencv_bboxes(image, self.bboxes)

        if len(self.cm_bboxes) > 0:
            image = viz_opencv_cm_bboxes(image, self.cm_bboxes)

        if len(self.points) > 0:
            image = viz_opencv_points(image, self.points)

        return [image]

    def size(self) -> int | None:
        return max(
            len(self.masks),
            len(self.heat_maps_2d),
            len(self.bboxes),
            len(self.cm_bboxes),
            len(self.points),
            len(self.images),
        )

    def to_json(self) -> str:
        return json.dumps({
            'masks': self.masks,
            'bboxes': self.bboxes,
            'points': self.points,
            '2d_heat_maps': self.heat_maps_2d,
        })

@dataclass
class ImagesHandler:
    images: list[ImageHandler]

    def viz(self, _: str = 'default') -> list[np.ndarray]:
        images: list[np.ndarray] = []

        for h in self.images:
            images.extend(h.viz())

        return images

    def size(self) -> int | None:
        return max(h.size() for h in self.images if h.size())

    def to_json(self) -> str:
        return json.dumps(self.images)
