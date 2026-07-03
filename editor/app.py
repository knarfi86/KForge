import json
import math
from pathlib import Path

from direct.showbase.ShowBase import ShowBase
from panda3d.core import BitMask32, LineSegs, WindowProperties

from editor import config

from editor.camera import CameraController
from editor.terrain import Terrain
from editor.grid import Grid
from editor.brush import Brush
from editor.exporter import SpringExporter
from editor.history import History
from editor.picker import MousePicker
from editor.ui.ui import EditorUI
from editor.world import WorldObjects
from editor.tools.tool_manager import ToolManager
from editor.tools.raise_tool import RaiseTool
from editor.tools.lower_tool import LowerTool
from editor.tools.smooth_tool import SmoothTool
from editor.tools.flatten_tool import FlattenTool


class EditorApp(ShowBase):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        props = WindowProperties()
        props.setTitle(config.WINDOW_TITLE)
        props.setSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.win.requestProperties(props)

        self.disableMouse()

        print("KForge starting...")

        # =========================
        # CORE SYSTEMS
        # =========================

        self.render.setShaderAuto()

        self.brush = Brush()
        # tools
        self.tool_manager = ToolManager(self)
        self.tool_manager.register("raise", RaiseTool(self))
        self.tool_manager.register("lower", LowerTool(self))
        self.tool_manager.register("smooth", SmoothTool(self))
        self.tool_manager.register("flatten", FlattenTool(self))
        self.tool_manager.select("raise")
        self.history = History()
        self.save_path = Path(config.SAVE_FILE)

        self.terrain = Terrain(
            self.render,
            config.TERRAIN_SIZE,
            config.TERRAIN_STEP
        )

        self.grid = Grid(self.render)

        self.camera_controller = CameraController(self)

        self.picker = MousePicker(self)
        self.world = WorldObjects(self.render)

        self.ui = EditorUI(self)
        self.brush_cursor = None
        self.brush_cursor_size = None

        # =========================
        # INPUT
        # =========================

        self.paint_raise = False
        self.paint_lower = False
        self.last_pointer_position = None
        self.stroke_active = False

        self.accept("mouse1", self.start_raise)
        self.accept("mouse1-up", self.stop_raise)

        self.accept("mouse3", self.start_lower)
        self.accept("mouse3-up", self.stop_lower)

        self.accept("1", self.set_mode, ["raise"])
        self.accept("2", self.set_mode, ["lower"])
        self.accept("3", self.set_mode, ["smooth"])
        self.accept("4", self.set_mode, ["flatten"])
        self.accept("[", self.brush.decrease_size)
        self.accept("]", self.brush.increase_size)
        self.accept("-", self.brush.decrease_strength)
        self.accept("=", self.brush.increase_strength)
        self.accept("control-z", self.undo)
        self.accept("control-y", self.redo)
        self.accept("control-s", self.save)
        self.accept("control-o", self.load)
        self.accept("control-n", self.new)
        self.accept("control-e", self.export)

        # =========================
        # LOOP
        # =========================

        self.taskMgr.add(self.update, "update")

        print("KForge v0.1 READY")

    # -------------------------

    def start_raise(self):
        self.paint_raise = True
        self.begin_stroke()
        self.tool_manager.begin(self.last_pointer_position)

    def stop_raise(self):
        self.paint_raise = False
        self.tool_manager.end()
        self.stroke_active = False

    def start_lower(self):
        self.paint_lower = True
        self.begin_stroke()
        self.tool_manager.begin(self.last_pointer_position)

    def stop_lower(self):
        self.paint_lower = False
        self.tool_manager.end()
        self.stroke_active = False

    # -------------------------

    def begin_stroke(self):

        if not self.stroke_active:
            self.history.snapshot(self.terrain.heights)
            self.stroke_active = True

    # -------------------------

    def set_mode(self, mode):

        # select a registered tool by name
        self.tool_manager.select(mode)
        self.ui.set_status(f"mode: {mode}")

    # -------------------------

    def set_texture_layer(self, layer):

        self.brush.texture_layer = layer
        self.set_mode("paint_texture")
        self.ui.set_status(f"texture: {config.TEXTURE_LAYERS[layer][0]}")

    # -------------------------

    def set_type_id(self, type_id):

        self.brush.type_id = type_id
        self.set_mode("paint_type")
        self.ui.set_status(f"type: {config.TYPEMAP_NAMES[type_id]}")

    # -------------------------

    # painting/modify entry now delegated to ToolManager
    # -------------------------

    def undo(self):

        previous = self.history.undo(self.terrain.heights)

        if previous is None:
            self.ui.set_status("nothing to undo")
            return

        self.terrain.replace_heights(previous)
        self.ui.set_status("undo")

    # -------------------------

    def redo(self):

        next_state = self.history.redo(self.terrain.heights)

        if next_state is None:
            self.ui.set_status("nothing to redo")
            return

        self.terrain.replace_heights(next_state)
        self.ui.set_status("redo")

    # -------------------------

    def save(self):

        data = {
            "terrain": self.terrain.to_data(),
            "world": self.world.to_data(),
        }
        self.save_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
        self.ui.set_status(f"saved {self.save_path.name}")

    # -------------------------

    def load(self):

        if not self.save_path.exists():
            self.ui.set_status(f"{self.save_path.name} not found")
            return

        self.history.snapshot(self.terrain.heights)
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        self.terrain.load_data(data.get("terrain", data))
        self.world.load_data(data.get("world", {}))
        self.ui.set_status(f"loaded {self.save_path.name}")

    # -------------------------

    def new(self):

        self.history.snapshot(self.terrain.heights)
        self.terrain.clear()
        self.world.clear()
        self.ui.set_status("new terrain")

    # -------------------------

    def export(self):

        SpringExporter(self.terrain, self.world).export(config.EXPORT_DIR)
        self.ui.set_status(f"exported {config.EXPORT_DIR}")

    # -------------------------

    def update_brush_cursor(self, pos):

        if self.brush_cursor_size != self.brush.size:

            if self.brush_cursor:
                self.brush_cursor.removeNode()

            radius = self.brush.size * self.terrain.step
            segments = LineSegs()
            segments.setThickness(3)
            segments.setColor(0.95, 0.95, 0.95, 0.9)

            steps = 72

            for i in range(steps + 1):
                angle = (i / steps) * 6.283185307
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)

                if i == 0:
                    segments.moveTo(x, y, 0)
                else:
                    segments.drawTo(x, y, 0)

            self.brush_cursor = self.render.attachNewNode(segments.create())
            self.brush_cursor.setCollideMask(BitMask32.allOff())
            self.brush_cursor_size = self.brush.size

        if pos is None:
            if self.brush_cursor:
                self.brush_cursor.hide()
            return

        self.brush_cursor.show()
        self.brush_cursor.setPos(pos.x, pos.y, pos.z + 0.15)

    # -------------------------

    def update(self, task):

        pos = self.picker.get_position()
        self.last_pointer_position = pos
        self.update_brush_cursor(pos)

        if pos is not None:

            if self.paint_raise:
                self.tool_manager.apply(pos)

            if self.paint_lower:
                self.tool_manager.apply(pos, True)

        self.ui.render()

        return task.cont
