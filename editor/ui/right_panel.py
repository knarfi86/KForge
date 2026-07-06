"""
KForge Right Panel

Eigenschaften des aktuell ausgewählten Werkzeugs.
"""

from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode

from . import theme


class RightPanel:

    def __init__(self, parent, app):

        self.parent = parent
        self.app = app

        self.labels = {}

        self._create()

    # -----------------------------------------------------

    def _create(self):

        y = -20

        self._add_title("Brush", y)
        y -= 40

        self.labels["tool"] = self._add_value("Tool:", y)
        y -= 25

        self.labels["size"] = self._add_value("Size:", y)
        y -= 25

        self.labels["strength"] = self._add_value("Strength:", y)
        y -= 40

        self._add_title("Scene", y)
        y -= 40

        self.labels["pointer"] = self._add_value("Pointer:", y)

    # -----------------------------------------------------

    def _add_title(self, text, y):

        DirectLabel(
            parent=self.parent,
            text=text,
            text_fg=theme.SECTION,
            text_align=TextNode.ALeft,
            text_scale=theme.SECTION_TEXT_SCALE,
            frameColor=(0, 0, 0, 0),
            pos=(15, 0, y),
        )

    # -----------------------------------------------------

    def _add_value(self, prefix, y):

        label = DirectLabel(
            parent=self.parent,
            text=prefix,
            text_fg=theme.TEXT,
            text_align=TextNode.ALeft,
            text_scale=theme.STATUS_TEXT_SCALE,
            frameColor=(0, 0, 0, 0),
            pos=(25, 0, y),
        )

        return label

    # -----------------------------------------------------

    def update(self):

        brush = self.app.brush

        self.labels["tool"]["text"] = f"Tool: {brush.mode}"
        self.labels["size"]["text"] = f"Size: {brush.size}"
        self.labels["strength"]["text"] = f"Strength: {brush.strength}"

        pos = self.app.last_pointer_position

        if pos is None:
            self.labels["pointer"]["text"] = "Pointer: ---"
        else:
            self.labels["pointer"]["text"] = (
                f"Pointer: "
                f"{pos.x:.1f}, "
                f"{pos.y:.1f}, "
                f"{pos.z:.2f}"
            )