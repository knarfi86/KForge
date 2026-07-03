from panda3d.core import LineSegs
from editor import config


class Grid:

    def __init__(self, render):

        self.node = render.attachNewNode("grid_root")

        size = config.GRID_SIZE
        step = config.GRID_STEP

        grid = LineSegs()
        grid.setThickness(1)
        grid.setColor(*config.GRID_COLOR)

        for i in range(-size, size + 1, step):

            grid.moveTo(-size, i, 0)
            grid.drawTo(size, i, 0)

            grid.moveTo(i, -size, 0)
            grid.drawTo(i, size, 0)

        self.node.attachNewNode(grid.create())

        # X axis
        x = LineSegs()
        x.setThickness(3)
        x.setColor(*config.AXIS_X_COLOR)
        x.moveTo(-size, 0, 0.1)
        x.drawTo(size, 0, 0.1)

        self.node.attachNewNode(x.create())

        # Y axis
        y = LineSegs()
        y.setThickness(3)
        y.setColor(*config.AXIS_Y_COLOR)
        y.moveTo(0, -size, 0.1)
        y.drawTo(0, size, 0.1)

        self.node.attachNewNode(y.create())