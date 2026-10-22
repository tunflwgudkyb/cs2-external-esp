from __future__ import annotations

import ctypes
from ctypes import wintypes


class Win32Overlay:
    def __init__(self, options: dict):
        self.options = options
        self.width = 1920
        self.height = 1080
        self._user32 = ctypes.windll.user32
        self._gdi32 = ctypes.windll.gdi32
        self._hwnd = None

    def begin_frame(self):
        dc = self._user32.GetDC(0)
        return dc

    def end_frame(self, dc) -> None:
        self._user32.ReleaseDC(0, dc)

    def draw_box(self, x: int, y: int, w: int, h: int, color: str = "#ff3b30") -> None:
        # Actual GDI drawing stub — real impl uses CreatePen + Rectangle
        rgb = self._hex_to_rgb(color)
        _ = (x, y, w, h, rgb)

    def begin_radar(self, scale: float) -> None:
        self._radar_scale = scale

    def plot_radar_point(self, x: float, y: float) -> None:
        _ = (x * getattr(self, "_radar_scale", 1.0),
             y * getattr(self, "_radar_scale", 1.0))

    def end_radar(self) -> None:
        pass

    def move_mouse_smooth(self, dx: float, dy: float) -> None:
        self._user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)

    def click(self) -> None:
        self._user32.mouse_event(0x0002, 0, 0, 0, 0)
        self._user32.mouse_event(0x0004, 0, 0, 0, 0)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        h = hex_color.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
</br>