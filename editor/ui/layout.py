from . import theme


class Layout:

    def __init__(self):

        self.window_width = 0
        self.window_height = 0

        self.sidebar_width = theme.SIDE_PANEL_WIDTH
        self.statusbar_height = theme.BOTTOM_BAR_HEIGHT

    def update(self, width, height):

        self.window_width = width
        self.window_height = height

    @property
    def sidebar(self):

        return {
            "x": 0,
            "y": self.statusbar_height,
            "width": self.sidebar_width,
            "height": self.window_height - self.statusbar_height,
        }

    @property
    def viewport(self):

        return {
            "x": self.sidebar_width,
            "y": self.statusbar_height,
            "width": self.window_width - self.sidebar_width,
            "height": self.window_height - self.statusbar_height,
        }

    @property
    def statusbar(self):

        return {
            "x": 0,
            "y": 0,
            "width": self.window_width,
            "height": self.statusbar_height,
        }