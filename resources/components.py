from UI.draw_single_road import DrawSingleRoad
from UI.drawingPanel.button_draw import DrawRoadButton
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.infoBar.fps_counter import FPSCounter
from UI.infoBar.zoom import Zoom


class Components:
    def __init__(self):
        self.grid = Grid()
        self.fps_display = FPSCounter()
        self.zoom_display = Zoom()
        self.xy_display = Coordinates()

        DrawSingleRoad(self)  # FIXME bruh

        DrawRoadButton()
