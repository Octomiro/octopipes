import logging
import json
from typing import Any, Protocol
from dataclasses import dataclass

import numpy as np


logger = logging.getLogger(__name__)

class HandlerInterface(Protocol):
    def viz(self, param: str = 'default') -> list[np.ndarray]:
        ...

    def size(self) -> int | None:
        ...

    def to_json(self) -> str:
        ...

@dataclass
class DefaultHandler():
    output: Any

    def viz(self, param : str = 'default') -> list[np.ndarray]:
        return []

    def size(self) -> int | None:
        if self.output is not None and hasattr(self.output, '__len__'):
            return len(self.output)
        return 0

    def to_json(self) -> str:
        return json.dumps(self.output)
