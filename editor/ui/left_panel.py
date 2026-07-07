from direct.gui.DirectGui import DirectScrolledFrame

from .registry import TOOLS
from .widgets import KButton, SectionLabel
from . import theme


class LeftPanel:

    def __init__(self, parent, app):

        self.parent = parent
        self.app = app

        self.buttons = {}

        self.frame = DirectScrolledFrame(
            parent=parent,
            canvasSize=(0, theme.SIDE_PANEL_WIDTH, -2000, 0),
            frameSize=(0, theme.SIDE_PANEL_WIDTH, -800, 0),
            manageScrollBars=False,
            frameColor=(0.12, 0.12, 0.12, 1),
        )

        self.build()

    def build(self):

        current_category = None
        y = -20

        for tool in TOOLS:

            if tool.category != current_category:

                current_category = tool.category

                label = SectionLabel(
                    parent=self.frame.getCanvas(),
                    text=current_category,
                )

                label.setPos(10, 0, y)

                y -= 35

            command = getattr(self.app, tool.command)

            button = KButton(
                parent=self.frame.getCanvas(),
                text=tool.title,
                command=command,
                extra_args=list(tool.args),
            )

            button.kforge_mode = tool.mode

            button.setPos(120, 0, y)

            self.buttons[tool.id] = button

            y -= theme.BUTTON_HEIGHT + theme.BUTTON_SPACING

        self.frame["canvasSize"] = (
            0,
            theme.SIDE_PANEL_WIDTH,
            y - 20,
            0,
        )

    def set_active(self, mode):

        for button in self.buttons.values():

            active = getattr(button, "kforge_mode", None) == mode

            button.set_active(active)