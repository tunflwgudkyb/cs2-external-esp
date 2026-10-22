from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def distance_to(self, other: "Vec3") -> float:
        return (self - other).length()

    def to_screen(self, view_matrix: list[float], width: int, height: int
                  ) -> tuple[int, int] | None:
        clip_x = view_matrix[0] * self.x + view_matrix[1] * self.y + view_matrix[2] * self.z + view_matrix[3]
        clip_y = view_matrix[4] * self.x + view_matrix[5] * self.y + view_matrix[6] * self.z + view_matrix[7]
        clip_w = view_matrix[12] * self.x + view_matrix[13] * self.y + view_matrix[14] * self.z + view_matrix[15]
        if clip_w < 0.01:
            return None
        ndc_x = clip_x / clip_w
        ndc_y = clip_y / clip_w
        return (int((width / 2) * (ndc_x + 1)),
                int((height / 2) * (1 - ndc_y)))