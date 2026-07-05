"""
KForge UI Widgets

Zentrale Widget-Klassen.
Alle Buttons, Labels und Panels werden später über diese Klassen erzeugt.
"""

from direct.gui.DirectGui import DirectButton, DirectLabel
from panda3d.core import TextNode

from . import theme


class KButton(DirectButton):
    """
    Standardbutton für KForge.
    """

    def __init__(self, parent, text, command=None, extra_args=None):

        super().__init__(
            parent=parent,
            text=text,
            command=command,
            extraArgs=extra_args or [],
            frameColor=theme.BUTTON_BG,
            text_fg=theme.TEXT,
            text_scale=theme.BUTTON_TEXT_SCALE,
            text_pos=(0, -0.02),
            frameSize=(-110, 110, -16, 16),
            relief=1,
        )

        self.default_color = theme.BUTTON_BG
        self.active_color = theme.BUTTON_ACTIVE

    def set_active(self, active=True):

        if active:
            self["frameColor"] = self.active_color
        else:
            self["frameColor"] = self.default_color


class SectionLabel(DirectLabel):
    """
    Überschrift einer Sidebar-Gruppe.
    """

    def __init__(self, parent, text):

        super().__init__(
            parent=parent,
            text=text,
            text_fg=theme.SECTION,
            text_align=TextNode.ALeft,
            text_scale=theme.SECTION_TEXT_SCALE,
            frameColor=(0, 0, 0, 0),
        )


class StatusLabel(DirectLabel):
    """
    Statusanzeige unten.
    """

    def __init__(self, parent, text=""):

        super().__init__(
            parent=parent,
            text=text,
            text_fg=theme.TEXT,
            text_align=TextNode.ALeft,
            text_scale=theme.STATUS_TEXT_SCALE,
            frameColor=(0, 0, 0, 0),
        )

    def set_text(self, text):
        self["text"] = text