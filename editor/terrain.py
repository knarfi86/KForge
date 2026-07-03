from panda3d.core import (
    BitMask32,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
)

from editor import config


class Terrain:

    def __init__(self, render, size, step):

        self.render = render

        self.size = size
        self.step = step

        self.root = render.attachNewNode("terrain")

        # Heightmap
        self.heights = {}
        self.textures = {}
        self.metalmap = {}
        self.typemap = {}

        self.mesh = None

        self.build()

    # -------------------------------------------------

    def get_height(self, x, y):

        return self.heights.get((x, y), 0.0)

    # -------------------------------------------------

    def set_height(self, x, y, value):

        self.heights[(x, y)] = value

    # -------------------------------------------------

    def replace_heights(self, heights):

        self.heights = dict(heights)
        self.build()

    # -------------------------------------------------

    def clear(self):

        self.heights.clear()
        self.textures.clear()
        self.metalmap.clear()
        self.typemap.clear()
        self.build()

    # -------------------------------------------------

    def modify_height(self, position, strength, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):

                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                falloff = 1.0 - dist / radius

                x = cx + dx
                y = cy + dy

                h = self.get_height(x, y)
                h += strength * falloff

                self.set_height(x, y, h)

        self.build()

    # -------------------------------------------------

    def paint_texture(self, position, layer, strength, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                falloff = 1.0 - dist / radius
                key = (cx + dx, cy + dy)
                weights = self.textures.get(key, [1.0, 0.0, 0.0, 0.0])
                amount = min(1.0, strength * falloff)

                for index in range(len(weights)):
                    weights[index] *= 1.0 - amount

                weights[layer] += amount
                total = sum(weights) or 1.0
                self.textures[key] = [value / total for value in weights]

        self.build()

    # -------------------------------------------------

    def blend_texture(self, position, strength, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)
        updated = {}

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                key = (cx + dx, cy + dy)
                samples = []

                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        samples.append(
                            self.textures.get(
                                (key[0] + ox, key[1] + oy),
                                [1.0, 0.0, 0.0, 0.0],
                            )
                        )

                average = [
                    sum(sample[index] for sample in samples) / len(samples)
                    for index in range(4)
                ]
                current = self.textures.get(key, [1.0, 0.0, 0.0, 0.0])
                falloff = 1.0 - dist / radius
                amount = strength * falloff
                updated[key] = [
                    current[index] + (average[index] - current[index]) * amount
                    for index in range(4)
                ]

        self.textures.update(updated)
        self.build()

    # -------------------------------------------------

    def paint_metal(self, position, strength, radius):

        self.paint_value_map(self.metalmap, position, strength, radius, 0.0, 1.0)
        self.build()

    # -------------------------------------------------

    def paint_type(self, position, type_id, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dist = (dx * dx + dy * dy) ** 0.5

                if dist <= radius:
                    self.typemap[(cx + dx, cy + dy)] = type_id

        self.build()

    # -------------------------------------------------

    def paint_value_map(self, target, position, strength, radius, min_value, max_value):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                falloff = 1.0 - dist / radius
                key = (cx + dx, cy + dy)
                value = target.get(key, min_value)
                value += strength * falloff
                target[key] = max(min_value, min(max_value, value))

    # -------------------------------------------------

    def flatten(self, position, target_height, strength, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):

                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                falloff = 1.0 - dist / radius

                x = cx + dx
                y = cy + dy

                h = self.get_height(x, y)
                h += (target_height - h) * strength * falloff

                self.set_height(x, y, h)

        self.build()

    # -------------------------------------------------

    def smooth(self, position, strength, radius):

        cx = round(position.x / self.step)
        cy = round(position.y / self.step)

        updated = {}

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):

                dist = (dx * dx + dy * dy) ** 0.5

                if dist > radius:
                    continue

                x = cx + dx
                y = cy + dy
                samples = []

                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        samples.append(self.get_height(x + ox, y + oy))

                average = sum(samples) / len(samples)
                falloff = 1.0 - dist / radius
                h = self.get_height(x, y)

                updated[(x, y)] = h + (average - h) * strength * falloff

        for key, value in updated.items():
            self.heights[key] = value

        self.build()

    # -------------------------------------------------

    def to_data(self):

        return {
            "version": config.VERSION,
            "size": self.size,
            "step": self.step,
            "heights": [
                {"x": x, "y": y, "height": height}
                for (x, y), height in sorted(self.heights.items())
                if abs(height) > 0.0001
            ],
            "splatmap": [
                {"x": x, "y": y, "weights": weights}
                for (x, y), weights in sorted(self.textures.items())
            ],
            "metalmap": [
                {"x": x, "y": y, "metal": value}
                for (x, y), value in sorted(self.metalmap.items())
                if value > 0.0001
            ],
            "typemap": [
                {"x": x, "y": y, "type": value}
                for (x, y), value in sorted(self.typemap.items())
                if value != 0
            ],
        }

    # -------------------------------------------------

    def load_data(self, data):

        self.size = data.get("size", self.size)
        self.step = data.get("step", self.step)
        self.heights = {
            (int(item["x"]), int(item["y"])): float(item["height"])
            for item in data.get("heights", [])
        }
        self.textures = {
            (int(item["x"]), int(item["y"])): list(item["weights"])
            for item in data.get("splatmap", [])
        }
        self.metalmap = {
            (int(item["x"]), int(item["y"])): float(item["metal"])
            for item in data.get("metalmap", [])
        }
        self.typemap = {
            (int(item["x"]), int(item["y"])): int(item["type"])
            for item in data.get("typemap", [])
        }
        self.build()

    # -------------------------------------------------

    def get_color(self, x, y, h):

        weights = self.textures.get((x, y))

        if weights is None:
            if h < -5:
                base = (0.0, 0.2, 0.9, 1)
            elif h < 1:
                base = config.TEXTURE_LAYERS[0][1]
            elif h < 6:
                base = config.TEXTURE_LAYERS[2][1]
            else:
                base = config.TEXTURE_LAYERS[3][1]
        else:
            base = [0.0, 0.0, 0.0, 1.0]

            for index, weight in enumerate(weights[:4]):
                color = config.TEXTURE_LAYERS[index][1]
                base[0] += color[0] * weight
                base[1] += color[1] * weight
                base[2] += color[2] * weight

            base = tuple(base)

        metal = self.metalmap.get((x, y), 0.0)
        type_id = self.typemap.get((x, y), 0)

        if metal > 0.0:
            base = (
                min(1.0, base[0] + metal * 0.45),
                min(1.0, base[1] + metal * 0.35),
                min(1.0, base[2] + metal * 0.08),
                1,
            )

        if type_id == 1:
            base = (0.20, 0.20, 0.20, 1)
        elif type_id == 2:
            base = (0.55, 0.12, 0.12, 1)
        elif type_id == 3:
            base = (0.05, 0.24, 0.55, 1)

        return base

    # -------------------------------------------------

    def build(self):

        if self.mesh:
            self.mesh.removeNode()

        fmt = GeomVertexFormat.getV3c4()

        vdata = GeomVertexData(
            "terrain",
            fmt,
            Geom.UHStatic
        )

        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        tris = GeomTriangles(Geom.UHStatic)

        grid = int(self.size / self.step)

        # -----------------------------
        # Vertices
        # -----------------------------

        for y in range(-grid, grid + 1):
            for x in range(-grid, grid + 1):

                h = self.get_height(x, y)

                vertex.addData3(
                    x * self.step,
                    y * self.step,
                    h
                )

                c = self.get_color(x, y, h)

                color.addData4(*c)

        # -----------------------------
        # Index
        # -----------------------------

        def idx(ix, iy):

            return (
                (iy + grid)
                * (grid * 2 + 1)
                + (ix + grid)
            )

        # -----------------------------
        # Triangles
        # -----------------------------

        for y in range(-grid, grid):
            for x in range(-grid, grid):

                i1 = idx(x, y)
                i2 = idx(x + 1, y)
                i3 = idx(x, y + 1)
                i4 = idx(x + 1, y + 1)

                tris.addVertices(i1, i2, i3)
                tris.addVertices(i2, i4, i3)

        geom = Geom(vdata)

        geom.addPrimitive(tris)

        node = GeomNode("terrain")

        node.addGeom(geom)

        self.mesh = self.root.attachNewNode(node)

        self.mesh.setCollideMask(
            BitMask32.bit(1)
        )
