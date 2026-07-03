import json
from pathlib import Path

from editor import config


class SpringExporter:

    def __init__(self, terrain, world):

        self.terrain = terrain
        self.world = world

    def export(self, target):

        target = Path(target)
        maps_dir = target / "maps"
        mapconfig_dir = target / "mapconfig"
        maps_dir.mkdir(parents=True, exist_ok=True)
        mapconfig_dir.mkdir(parents=True, exist_ok=True)

        self.write_images(maps_dir)
        self.write_mapinfo(target / "mapinfo.lua")
        self.write_metal_layout(mapconfig_dir / "map_metal_layout.lua")
        self.write_startboxes(mapconfig_dir / "map_startboxes.lua")
        self.write_features(target / "features.lua")

        (target / "kforge_project.json").write_text(
            json.dumps(
                {
                    "terrain": self.terrain.to_data(),
                    "world": self.world.to_data(),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def write_images(self, maps_dir):

        grid = int(self.terrain.size / self.terrain.step)
        width = grid * 2 + 1
        height = width

        def points():
            for y in range(-grid, grid + 1):
                for x in range(-grid, grid + 1):
                    yield x, y

        heights = [self.terrain.get_height(x, y) for x, y in points()]
        min_height = min(heights) if heights else 0.0
        max_height = max(heights) if heights else 1.0
        span = max(1.0, max_height - min_height)

        height_pixels = [
            int(((self.terrain.get_height(x, y) - min_height) / span) * 255)
            for x, y in points()
        ]
        self.write_tga_gray(maps_dir / "kforge_heightmap.tga", width, height, height_pixels)

        metal_pixels = [
            int(self.terrain.metalmap.get((x, y), 0.0) * 255)
            for x, y in points()
        ]
        self.write_tga_gray(maps_dir / "kforge_metalmap.tga", width, height, metal_pixels)

        type_pixels = [
            int(self.terrain.typemap.get((x, y), 0) * 64)
            for x, y in points()
        ]
        self.write_tga_gray(maps_dir / "kforge_typemap.tga", width, height, type_pixels)

        splat_pixels = []

        for x, y in points():
            weights = self.terrain.textures.get((x, y), [1.0, 0.0, 0.0, 0.0])
            splat_pixels.append(tuple(int(max(0.0, min(1.0, value)) * 255) for value in weights))

        self.write_tga_rgba(maps_dir / "kforge_splatmap.tga", width, height, splat_pixels)

    def write_mapinfo(self, path):

        starts = self.world.starts or [
            {"x": -self.terrain.size * 0.6, "y": 0, "z": -self.terrain.size * 0.6},
            {"x": self.terrain.size * 0.6, "y": 0, "z": self.terrain.size * 0.6},
        ]

        teams = []
        for index, start in enumerate(starts):
            teams.append(
                f"\t\t[{index}] = {{startPos = {{x = {self.to_spring_x(start['x'])}, z = {self.to_spring_z(start['y'])}}}}},"
            )

        terrain_types = []
        for type_id, name in config.TYPEMAP_NAMES.items():
            terrain_types.append(
                "\t\t[%d] = { name = \"%s\", hardness = 1.0, receiveTracks = true, "
                "moveSpeeds = { tank = 1.0, kbot = 1.0, hover = 1.0, ship = 1.0 } },"
                % (type_id, name)
            )

        content = f"""local mapinfo = {{
\tname        = "KForge Map",
\tshortname   = "kforge",
\tdescription = "KForge Zero-K draft export",
\tauthor      = "KForge",
\tversion     = "v0.1",
\tmodtype     = 3,

\tmaphardness     = 140,
\tnotDeformable   = false,
\tgravity         = 130,
\ttidalStrength   = 18,
\tmaxMetal        = 1.20,
\textractorRadius = 110,
\tvoidWater       = false,
\tautoShowMetal   = true,

\tsmf = {{
\t\tminheight = -128,
\t\tmaxheight = 384,
\t\tmapfile = "maps/kforge.smf",
\t\tmetalmapTex = "kforge_metalmap.tga",
\t\ttypemapTex = "kforge_typemap.tga",
\t}},

\tresources = {{
\t\tsplatDistrTex = "kforge_splatmap.tga",
\t\tsplatDetailNormalTex = {{
\t\t\t"grass.tga",
\t\t\t"rock.tga",
\t\t\t"sand.tga",
\t\t\t"snow.tga",
\t\t\talpha = true,
\t\t}},
\t}},

\tsplats = {{
\t\ttexScales = {{0.00471, 0.00097, 0.0013, 0.0027}},
\t\ttexMults  = {{0.5, 0.31, 0.5, 0.65}},
\t}},

\tteams = {{
{chr(10).join(teams)}
\t}},

\tterrainTypes = {{
{chr(10).join(terrain_types)}
\t}},
}}

return mapinfo
"""
        path.write_text(content, encoding="utf-8")

    def write_metal_layout(self, path):

        spots = []

        for (x, y), value in sorted(self.terrain.metalmap.items()):
            if value >= 0.65:
                spots.append(
                    "\t\t{x = %.1f, z = %.1f, metal = %.2f},"
                    % (self.to_spring_x(x * self.terrain.step), self.to_spring_z(y * self.terrain.step), value)
                )

        content = "return {\n\tspots = {\n%s\n\t},\n\tneedMexDrawing = true,\n}\n" % "\n".join(spots)
        path.write_text(content, encoding="utf-8")

    def write_startboxes(self, path):

        boxes = []

        for index, start in enumerate(self.world.starts):
            x = self.to_spring_x(start["x"])
            z = self.to_spring_z(start["y"])
            size = 350
            boxes.append(
                f"""\t[{index}] = {{
\t\tstartpoints = {{{{ {x:.1f}, {z:.1f} }}}},
\t\tboxes = {{{{
\t\t\t{{ {x - size:.1f}, {z - size:.1f} }},
\t\t\t{{ {x + size:.1f}, {z - size:.1f} }},
\t\t\t{{ {x + size:.1f}, {z + size:.1f} }},
\t\t\t{{ {x - size:.1f}, {z + size:.1f} }},
\t\t}}}},
\t\tnameLong = "Start {index + 1}",
\t\tnameShort = "S{index + 1}",
\t}},"""
            )

        path.write_text("return {\n%s\n}\n" % "\n".join(boxes), encoding="utf-8")

    def write_features(self, path):

        rows = []

        for item in self.world.objects:
            rows.append(
                "\t{ name = \"%s\", x = %.1f, z = %.1f, rot = 0 },"
                % (self.feature_name(item["kind"]), self.to_spring_x(item["x"]), self.to_spring_z(item["y"]))
            )

        path.write_text("return {\n%s\n}\n" % "\n".join(rows), encoding="utf-8")

    def to_spring_x(self, value):

        return value + self.terrain.size

    def to_spring_z(self, value):

        return value + self.terrain.size

    def feature_name(self, kind):

        return {
            "tree": "lowpoly_tree_1",
            "rock": "rock1",
            "building": "building_placeholder",
        }.get(kind, kind)

    def write_tga_gray(self, path, width, height, pixels):

        data = bytes(max(0, min(255, value)) for value in pixels)
        self.write_tga(path, width, height, 8, data)

    def write_tga_rgba(self, path, width, height, pixels):

        data = bytearray()

        for r, g, b, a in pixels:
            data.extend([b, g, r, a])

        self.write_tga(path, width, height, 32, bytes(data))

    def write_tga(self, path, width, height, bits, data):

        image_type = 3 if bits == 8 else 2
        header = bytearray(18)
        header[2] = image_type
        header[12] = width & 255
        header[13] = (width >> 8) & 255
        header[14] = height & 255
        header[15] = (height >> 8) & 255
        header[16] = bits
        header[17] = 32 if bits == 32 else 0

        path.write_bytes(bytes(header) + data)
