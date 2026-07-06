from .registry import UI_REGISTRY
from .widgets import KButton, SectionLabel
from . import theme


class LeftPanel:

    def __init__(self, parent, app):

        self.parent = parent
        self.app = app

        self.sections = []
        self.buttons = {}

        self.margin = theme.CONTENT_PADDING
        self.width = theme.SIDE_PANEL_WIDTH

    # ---------------------------------------------------------

    def build(self):

        y = -self.margin

        for category in UI_REGISTRY:

            label = SectionLabel(
                parent=self.parent,
                text=category.title,
            )

            label.setPos(
                self.margin,
                0,
                y,
            )

            self.sections.append(label)

            y -= theme.SECTION_SPACING

            for tool in category.tools:

                if not hasattr(self.app, tool.command):
                    print(
                        f"[LeftPanel] Missing command: {tool.command}"
                    )
                    continue

                command = getattr(
                    self.app,
                    tool.command
                )

                button = KButton(
                    parent=self.parent,
                    text=tool.title,
                    command=command,
                    extra_args=list(tool.args),
                )

                button.kforge_mode = tool.mode

                button.setPos(
                    self.width * 0.5,
                    0,
                    y,
                )

                self.buttons[tool.mode] = button

                y -= (
                    theme.BUTTON_HEIGHT
                    + theme.BUTTON_SPACING
                )

            y -= theme.SECTION_SPACING

    # ---------------------------------------------------------

    def set_active(self, mode):

        for button in self.buttons.values():
            button.set_active(False)

        if mode in self.buttons:
            self.buttons[mode].set_active(True)

    # ---------------------------------------------------------

    def show(self):

        self.parent.show()

    def hide(self):

        self.parent.hide()

    # ---------------------------------------------------------

    def destroy(self):

        for button in self.buttons.values():
            button.destroy()

        for section in self.sections:
            section.destroy()

        self.buttons.clear()
        self.sections.clear()