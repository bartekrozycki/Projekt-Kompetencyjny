from UI.draw_single_road import DrawSingleRoad
from UI.drawingPanel.button_draw import DrawRoadButton
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.infoBar.fps_counter import FPSCounter
from UI.infoBar.zoom import Zoom


class Components:
    def _init_(self):
        self.grid = Grid(self.screen)
        self.fps_display = FPSCounter(self.screen, self.clock)
        self.zoom_display = Zoom(self.screen)
        self.xy_display = Coordinates(self.screen)

        DrawSingleRoad(self, self.screen)  # FIXME bruh

        DrawRoadButton(self.screen)
