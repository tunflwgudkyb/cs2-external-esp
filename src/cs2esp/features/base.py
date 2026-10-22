from __future__ import annotations

from abc import ABC, abstractmethod

from cs2esp.core.process_handle import ProcessHandle


class BaseFeature(ABC):
    name: str = "base"

    def __init__(self, options: dict):
        self.options = options or {}

    @abstractmethod
    def tick(self, handle: ProcessHandle, overlay) -> None:
        """Called once per overlay frame."""
</br>