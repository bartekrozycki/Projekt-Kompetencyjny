BASIC_CURSOR = 1
DRAW_ROAD = 2

class ActiveTool():

    activeTool = BASIC_CURSOR

    def isActive(self, tool):
        return self.activeTool == tool

    def setBasicCursor(self):
        self.activeTool = BASIC_CURSOR

    def setDrawRoad(self):
        self.activeTool = DRAW_ROAD
