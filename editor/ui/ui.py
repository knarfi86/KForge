from direct.gui.DirectGui import DirectSlider

from editor import config

from .layout import Layout
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .statusbar import StatusBar


class EditorUI:

    def __init__(self, app):

        self.app = app
        self.status = "Ready"

        self.layout = Layout()

        # --------------------------------------------------
        # ROOT NODES
        # --------------------------------------------------

        self.left_root = app.pixel2d.attachNewNode("left_panel")
        self.right_root = app.pixel2d.attachNewNode("right_panel")
        self.bottom_root = app.pixel2d.attachNewNode("bottom_bar")

        # --------------------------------------------------
        # PANELS
        # --------------------------------------------------

        self.left_panel = LeftPanel(
            self.left_root,
            self.app,
        )

        self.left_panel.build()

        self.right_panel = RightPanel(
            self.right_root,
            self.app,
        )

        self.statusbar = StatusBar(
            self.bottom_root
        )

        self.statusbar.set_title(
            f"KForge {config.VERSION}"
        )

        self.statusbar.set_help(
            "LMB Paint | RMB Lower | MMB Rotate | WASD/QE Move"
        )

        # --------------------------------------------------
        # SLIDER
        # --------------------------------------------------

        self.size_slider = DirectSlider(
            parent=self.bottom_root,
            range=(
                config.BRUSH_MIN_SIZE,
                config.BRUSH_MAX_SIZE,
            ),
            value=self.app.brush.size,
            pageSize=1,
            command=self.on_size_slider,
        )

        self.strength_slider = DirectSlider(
            parent=self.bottom_root,
            range=(
                config.BRUSH_MIN_STRENGTH,
                config.BRUSH_MAX_STRENGTH,
            ),
            value=self.app.brush.strength,
            pageSize=1,
            command=self.on_strength_slider,
        )

        self.app.accept(
            "window-event",
            self.on_window_event,
        )

        self.on_window_event(None)

    # --------------------------------------------------
    # WINDOW
    # --------------------------------------------------

    def on_window_event(self, window):

        if self.app.win is None:
            return

        self.update_layout()

    def update_layout(self):

        width = self.app.win.getXSize()
        height = self.app.win.getYSize()

        self.layout.update(width, height)

        sidebar = self.layout.sidebar
        status = self.layout.statusbar

        # Left Panel
        self.left_root.setPos(
            sidebar["x"],
            0,
            sidebar["y"],
        )

        # Right Panel
        self.right_root.setPos(
            width - 260,
            0,
            sidebar["y"],
        )

        # Statusbar
        self.bottom_root.setPos(
            status["x"],
            0,
            status["y"],
        )

        self.statusbar.layout(
            status["width"],
            status["height"],
        )

        # Slider Positionen
        self.size_slider.setScale(180, 1, 18)
        self.size_slider.setPos(
            170,
            0,
            status["height"] * 0.5,
        )

        self.strength_slider.setScale(180, 1, 18)
        self.strength_slider.setPos(
            470,
            0,
            status["height"] * 0.5,
        )

    # --------------------------------------------------
    # CALLBACKS
    # --------------------------------------------------

    def on_size_slider(self):

        self.app.brush.set_size(
            int(round(self.size_slider["value"]))
        )

    def on_strength_slider(self):

        self.app.brush.set_strength(
            int(round(self.strength_slider["value"]))
        )

    # --------------------------------------------------
    # STATUS
    # --------------------------------------------------

    def set_status(self, text):

        self.status = text

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def render(self):

        brush = self.app.brush

        pos = self.app.last_pointer_position

        if pos is None:
            pointer = "No Terrain"
        else:
            pointer = (
                f"x {pos.x:.1f} "
                f"y {pos.y:.1f} "
                f"h {pos.z:.2f}"
            )

        self.statusbar.set_info(
            f"{brush.mode} | "
            f"Size {brush.size} | "
            f"Strength {brush.strength} | "
            f"{pointer} | "
            f"{self.status}"
        )

        if int(round(self.size_slider["value"])) != brush.size:
            self.size_slider["value"] = brush.size

        if int(round(self.strength_slider["value"])) != brush.strength:
            self.strength_slider["value"] = brush.strength

        self.left_panel.set_active(
            brush.mode
        )

        self.right_panel.update()

    # --------------------------------------------------

    def update(self):

        self.render()