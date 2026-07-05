from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode

from . import theme


class StatusBar:

    def __init__(self, parent):

        self.parent = parent

        self.title = DirectLabel(
            parent=parent,
            text="KForge",
            text_fg=theme.TEXT,
            text_scale=theme.TITLE_TEXT_SCALE,
            text_align=TextNode.ALeft,
            frameColor=(0, 0, 0, 0),
        )

        self.info = DirectLabel(
            parent=parent,
            text="Ready",
            text_fg=theme.TEXT,
            text_scale=theme.STATUS_TEXT_SCALE,
            text_align=TextNode.ACenter,
            frameColor=(0, 0, 0, 0),
        )

        self.help = DirectLabel(
            parent=parent,
            text="",
            text_fg=theme.TEXT_DIM,
            text_scale=theme.STATUS_TEXT_SCALE,
            text_align=TextNode.ARight,
            frameColor=(0, 0, 0, 0),
        )

    def layout(self, width, height):

        pad = theme.CONTENT_PADDING
        center = height * 0.5

        self.title.setPos(pad, 0, center)

        self.info.setPos(width * 0.5, 0, center)

        self.help.setPos(width - pad, 0, center)

    def set_title(self, text):
        self.title["text"] = text

    def set_info(self, text):
        self.info["text"] = text

    def set_help(self, text):
        self.help["text"] = text