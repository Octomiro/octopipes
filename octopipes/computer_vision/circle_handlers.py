import json
from dataclasses import dataclass

import numpy as np

from octopipes.computer_vision.annotations import Circle
from octopipes.computer_vision.vis_utils import viz_opencv_circles


@dataclass
class CirclesHandler():
    """CirclesHandler handles output of the form [(x, y, radius), ...]"""
    image: np.ndarray
    circles: list[Circle]

    def viz(self, _: str = 'default') -> list[np.ndarray]:
        return [viz_opencv_circles(self.image.copy(), self.circles)]

    def to_json(self) -> str:
        return json.dumps({'circles': [c.to_list() for c in self.circles]})

    def size(self) -> int | None:
        return len(self.circles)
