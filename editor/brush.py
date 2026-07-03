from editor import config


class Brush:

    def __init__(self):

        self.size = config.BRUSH_DEFAULT_SIZE
        self.strength = config.BRUSH_DEFAULT_STRENGTH
        self.mode = "raise"
        self.flatten_height = 0.0
        self.texture_layer = 0
        self.type_id = 0

    @property
    def height_strength(self):

        return self.strength * config.BRUSH_HEIGHT_SCALE

    def increase_size(self):

        self.size = min(
            config.BRUSH_MAX_SIZE,
            self.size + 1
        )

    def decrease_size(self):

        self.size = max(
            config.BRUSH_MIN_SIZE,
            self.size - 1
        )

    def increase_strength(self):

        self.strength = min(
            config.BRUSH_MAX_STRENGTH,
            self.strength + 1
        )

    def decrease_strength(self):

        self.strength = max(
            config.BRUSH_MIN_STRENGTH,
            self.strength - 1
        )

    def set_mode(self, mode):

        self.mode = mode

    def set_size(self, value):

        self.size = max(
            config.BRUSH_MIN_SIZE,
            min(config.BRUSH_MAX_SIZE, int(round(value)))
        )

    def set_strength(self, value):

        self.strength = max(
            config.BRUSH_MIN_STRENGTH,
            min(config.BRUSH_MAX_STRENGTH, int(round(value)))
        )
