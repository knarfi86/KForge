from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectSlider
from panda3d.core import TextNode, TransparencyAttrib

from editor import config


class EditorUI:

    def __init__(self, app):

        self.app = app
        self.buttons = {}
        self.status = "ready"

        self.panel = DirectFrame(
            frameColor=(0.06, 0.07, 0.08, 0.9),
            frameSize=(-1.34, 1.34, -1.0, -0.52),
            pos=(0, 0, 0),
        )
        self.panel.setTransparency(TransparencyAttrib.MAlpha)

        self.left_tool_panel = DirectFrame(
            frameColor=(0.06, 0.07, 0.08, 0.86),
            frameSize=(-1.34, -0.92, -0.66, 0.94),
            pos=(0, 0, 0),
        )
        self.left_tool_panel.setTransparency(TransparencyAttrib.MAlpha)

        self.right_tool_panel = DirectFrame(
            frameColor=(0.06, 0.07, 0.08, 0.86),
            frameSize=(0.92, 1.34, -0.66, 0.94),
            pos=(0, 0, 0),
        )
        self.right_tool_panel.setTransparency(TransparencyAttrib.MAlpha)

        self.title = DirectLabel(
            parent=self.panel,
            text=f"KForge {config.VERSION}",
            text_fg=(0.92, 0.95, 0.95, 1),
            text_align=TextNode.ALeft,
            text_scale=0.05,
            frameColor=(0, 0, 0, 0),
            pos=(-1.28, 0, -0.76),
        )

        self.info = DirectLabel(
            parent=self.panel,
            text="",
            text_fg=(0.82, 0.86, 0.86, 1),
            text_align=TextNode.ALeft,
            text_scale=0.035,
            frameColor=(0, 0, 0, 0),
            pos=(-1.28, 0, -0.96),
        )

        self.help = DirectLabel(
            text="LMB paint | RMB lower | MMB rotate | WASD/QE move | Wheel zoom",
            text_fg=(0.78, 0.82, 0.82, 1),
            text_align=TextNode.ARight,
            text_scale=0.034,
            frameColor=(0, 0, 0, 0),
            pos=(1.29, 0, -0.99),
        )

        self.make_button("Raise", -0.46, -0.76, self.app.set_mode, ["raise"])
        self.make_button("Lower", -0.25, -0.76, self.app.set_mode, ["lower"])
        self.make_button("Smooth", -0.04, -0.76, self.app.set_mode, ["smooth"])
        self.make_button("Flat", 0.17, -0.76, self.app.set_mode, ["flatten"])
        self.make_button("Undo", 0.43, -0.76, self.app.undo)
        self.make_button("Redo", 0.64, -0.76, self.app.redo)
        self.make_button("Save", 0.85, -0.76, self.app.save)
        self.make_button("Load", 1.04, -0.76, self.app.load)
        self.make_button("Export", 1.24, -0.76, self.app.export)

        self.make_section("Textures", 0.86, parent=self.left_tool_panel)
        self.make_side_button("Grass", 0.76, self.app.set_texture_layer, [0], "paint_texture", parent=self.left_tool_panel)
        self.make_side_button("Rock", 0.66, self.app.set_texture_layer, [1], "paint_texture", parent=self.left_tool_panel)
        self.make_side_button("Sand", 0.56, self.app.set_texture_layer, [2], "paint_texture", parent=self.left_tool_panel)
        self.make_side_button("Snow", 0.46, self.app.set_texture_layer, [3], "paint_texture", parent=self.left_tool_panel)
        self.make_side_button("Blend", 0.36, self.app.set_mode, ["blend_texture"], "blend_texture", parent=self.left_tool_panel)

        self.make_section("Objects", 0.22, parent=self.left_tool_panel)
        self.make_side_button("Trees", 0.12, self.app.set_mode, ["tree"], "tree", parent=self.left_tool_panel)
        self.make_side_button("Rocks", 0.02, self.app.set_mode, ["rock"], "rock", parent=self.left_tool_panel)
        self.make_side_button("Buildings", -0.08, self.app.set_mode, ["building"], "building", parent=self.left_tool_panel)

        self.make_section("SpringRTS", -0.22, parent=self.right_tool_panel)
        self.make_side_button("Metalmap", -0.32, self.app.set_mode, ["paint_metal"], "paint_metal", parent=self.right_tool_panel)
        self.make_side_button("Default", -0.42, self.app.set_type_id, [0], "paint_type", parent=self.right_tool_panel)
        self.make_side_button("Road", -0.52, self.app.set_type_id, [1], "paint_type", parent=self.right_tool_panel)
        self.make_side_button("NoBuild", -0.62, self.app.set_type_id, [2], "paint_type", parent=self.right_tool_panel)
        self.make_side_button("Start", -0.72, self.app.set_mode, ["start_position"], "start_position", parent=self.right_tool_panel)

        self.size_label = self.make_slider_label("Size", -1.28, -0.86)
        self.size_slider = self.make_slider(
            -1.0,
            -0.86,
            config.BRUSH_MIN_SIZE,
            config.BRUSH_MAX_SIZE,
            self.app.brush.size,
            self.on_size_slider,
        )

        self.strength_label = self.make_slider_label("Strength", -0.26, -0.86)
        self.strength_slider = self.make_slider(
            0.08,
            -0.86,
            config.BRUSH_MIN_STRENGTH,
            config.BRUSH_MAX_STRENGTH,
            self.app.brush.strength,
            self.on_strength_slider,
        )

    def make_button(self, text, x, z, command, extra_args=None):

        button = DirectButton(
            parent=self.panel,
            text=text,
            text_scale=0.034,
            text_fg=(0.95, 0.97, 0.97, 1),
            text_pos=(0, -0.012),
            frameSize=(-0.09, 0.09, -0.035, 0.035),
            frameColor=(0.16, 0.18, 0.2, 1),
            relief=1,
            pos=(x, 0, z),
            command=command,
            extraArgs=extra_args or [],
        )
        self.buttons[text.lower()] = button

    def make_section(self, text, z, parent=None):

        panel = parent or self.left_tool_panel
        x = -0.16 if panel == self.left_tool_panel else 0.16

        DirectLabel(
            parent=panel,
            text=text,
            text_fg=(0.92, 0.95, 0.95, 1),
            text_align=TextNode.ALeft if panel == self.left_tool_panel else TextNode.ARight,
            text_scale=0.04,
            frameColor=(0, 0, 0, 0),
            pos=(x, 0, z),
        )

    def make_side_button(self, text, z, command, extra_args=None, mode=None, parent=None):

        panel = parent or self.left_tool_panel
        x = -0.26 if panel == self.left_tool_panel else 0.26

        button = DirectButton(
            parent=panel,
            text=text,
            text_scale=0.031,
            text_fg=(0.95, 0.97, 0.97, 1),
            text_pos=(0, -0.011),
            frameSize=(-0.13, 0.13, -0.035, 0.035),
            frameColor=(0.16, 0.18, 0.2, 1),
            relief=1,
            pos=(x, 0, z),
            command=command,
            extraArgs=extra_args or [],
        )
        self.buttons[text.lower()] = button
        button.kforge_mode = mode

    def make_slider_label(self, text, x, z):

        return DirectLabel(
            parent=self.panel,
            text=text,
            text_fg=(0.9, 0.93, 0.93, 1),
            text_align=TextNode.ALeft,
            text_scale=0.035,
            frameColor=(0, 0, 0, 0),
            pos=(x, 0, z),
        )

    def make_slider(self, x, z, min_value, max_value, value, command):

        return DirectSlider(
            parent=self.panel,
            range=(min_value, max_value),
            value=value,
            pageSize=1,
            scale=0.34,
            frameSize=(-1, 1, -0.045, 0.045),
            frameColor=(0.13, 0.15, 0.17, 1),
            thumb_frameSize=(-0.055, 0.055, -0.085, 0.085),
            thumb_frameColor=(0.12, 0.43, 0.38, 1),
            pos=(x, 0, z),
            command=command,
        )

    def on_size_slider(self):

        self.app.brush.set_size(self.size_slider["value"])

    def on_strength_slider(self):

        self.app.brush.set_strength(self.strength_slider["value"])

    def render(self):

        brush = self.app.brush
        pos = self.app.last_pointer_position
        pointer = "no terrain"

        if pos is not None:
            pointer = f"x {pos.x:6.1f}  y {pos.y:6.1f}  h {pos.z:5.2f}"

        self.size_label["text"] = f"Size {brush.size}"
        self.strength_label["text"] = f"Strength {brush.strength}"

        if int(round(self.size_slider["value"])) != brush.size:
            self.size_slider["value"] = brush.size

        if int(round(self.strength_slider["value"])) != brush.strength:
            self.strength_slider["value"] = brush.strength

        tool_name = getattr(self.app.tool_manager, "current_name", brush.mode)
        self.info["text"] = (
            f"Tool {tool_name} | Size {brush.size} | Strength {brush.strength} | "
            f"{pointer} | {self.status}"
        )

        for key, button in self.buttons.items():
            button_mode = getattr(button, "kforge_mode", key)
            active = button_mode == tool_name or (
                key == "flat" and tool_name == "flatten"
            ) or (
                button_mode == "paint_texture" and tool_name == "paint_texture"
            ) or (
                key.lower() == config.TYPEMAP_NAMES.get(brush.type_id, "").lower()
                and tool_name == "paint_type"
            )
            button["frameColor"] = (
                (0.12, 0.43, 0.38, 1) if active else (0.16, 0.18, 0.2, 1)
            )

    def set_status(self, message):

        self.status = message
