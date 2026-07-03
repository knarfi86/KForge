"""
KForge Configuration
Alle globalen Einstellungen des Editors.
"""

# ==========================================
# VERSION
# ==========================================

VERSION = "0.1.0"

# ==========================================
# WINDOW
# ==========================================

WINDOW_TITLE = "KForge"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# ==========================================
# CAMERA
# ==========================================

CAMERA_START_POS = (0, -80, 40)

CAMERA_FOV = 70

CAMERA_SPEED = 40
CAMERA_FAST_SPEED = 120
CAMERA_SLOW_SPEED = 15

CAMERA_ROTATE_SPEED = 0.25

CAMERA_MIN_FOV = 30
CAMERA_MAX_FOV = 120

CAMERA_ZOOM_STEP = 5

# ==========================================
# TERRAIN
# ==========================================

TERRAIN_SIZE = 256

TERRAIN_STEP = 2

TERRAIN_DEFAULT_HEIGHT = 0.0

SAVE_FILE = "kforge_terrain.json"
EXPORT_DIR = "spring_export"

# ==========================================
# BRUSH
# ==========================================

BRUSH_MIN_SIZE = 1
BRUSH_MAX_SIZE = 10

BRUSH_DEFAULT_SIZE = 5

BRUSH_MIN_STRENGTH = 1
BRUSH_MAX_STRENGTH = 20

BRUSH_DEFAULT_STRENGTH = 5

# interne Umrechnung
BRUSH_HEIGHT_SCALE = 0.1

SMOOTH_STRENGTH = 0.45

# ==========================================
# TEXTURES / SPRINGRTS
# ==========================================

TEXTURE_LAYERS = [
    ("Grass", (0.18, 0.58, 0.22, 1)),
    ("Rock", (0.42, 0.42, 0.40, 1)),
    ("Sand", (0.78, 0.68, 0.42, 1)),
    ("Snow", (0.92, 0.94, 0.92, 1)),
]

OBJECT_TYPES = {
    "tree": (0.08, 0.55, 0.18, 1),
    "rock": (0.45, 0.45, 0.48, 1),
    "building": (0.55, 0.34, 0.22, 1),
}

TYPEMAP_NAMES = {
    0: "Default",
    1: "Road",
    2: "NoBuild",
    3: "Water",
}

# ==========================================
# GRID
# ==========================================

GRID_SIZE = 256
GRID_STEP = 2

GRID_COLOR = (0.35, 0.35, 0.35, 1)

AXIS_X_COLOR = (1, 0, 0, 1)
AXIS_Y_COLOR = (0, 1, 0, 1)
