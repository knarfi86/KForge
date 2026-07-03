from panda3d.core import BitMask32, LineSegs

from editor import config


class WorldObjects:

    def __init__(self, render):

        self.render = render
        self.objects = []
        self.starts = []
        self.nodes = []

    def clear(self):

        for node in self.nodes:
            node.removeNode()

        self.objects.clear()
        self.starts.clear()
        self.nodes.clear()

    def add_object(self, kind, position):

        item = {
            "kind": kind,
            "x": round(position.x, 2),
            "y": round(position.y, 2),
            "z": round(position.z, 2),
        }
        self.objects.append(item)
        self.nodes.append(self.make_marker(position, config.OBJECT_TYPES[kind], kind))

    def add_start(self, position):

        index = len(self.starts) + 1
        item = {
            "player": index,
            "x": round(position.x, 2),
            "y": round(position.y, 2),
            "z": round(position.z, 2),
        }
        self.starts.append(item)
        self.nodes.append(self.make_start_marker(position, index))

    def make_marker(self, position, color, kind):

        marker = LineSegs()
        marker.setThickness(4)
        marker.setColor(*color)
        size = 2.0 if kind != "building" else 3.5
        height = 5.0 if kind == "tree" else 2.5

        marker.moveTo(-size, 0, 0)
        marker.drawTo(size, 0, 0)
        marker.moveTo(0, -size, 0)
        marker.drawTo(0, size, 0)
        marker.moveTo(0, 0, 0)
        marker.drawTo(0, 0, height)

        node = self.render.attachNewNode(marker.create())
        node.setPos(position.x, position.y, position.z + 0.25)
        node.setCollideMask(BitMask32.allOff())
        return node

    def make_start_marker(self, position, index):

        marker = LineSegs()
        marker.setThickness(5)
        marker.setColor(0.1, 0.65, 1.0, 1)
        size = 4.0

        marker.moveTo(-size, -size, 0)
        marker.drawTo(size, size, 0)
        marker.moveTo(-size, size, 0)
        marker.drawTo(size, -size, 0)
        marker.moveTo(-size, 0, 0)
        marker.drawTo(size, 0, 0)
        marker.moveTo(0, -size, 0)
        marker.drawTo(0, size, 0)
        marker.moveTo(0, 0, 0)
        marker.drawTo(0, 0, 6 + index)

        node = self.render.attachNewNode(marker.create())
        node.setPos(position.x, position.y, position.z + 0.35)
        node.setCollideMask(BitMask32.allOff())
        return node

    def to_data(self):

        return {
            "objects": list(self.objects),
            "start_positions": list(self.starts),
        }

    def load_data(self, data):

        self.clear()

        for item in data.get("objects", []):
            self.objects.append(dict(item))
            self.nodes.append(
                self.make_marker(
                    SimplePosition(item["x"], item["y"], item["z"]),
                    config.OBJECT_TYPES.get(item["kind"], (1, 1, 1, 1)),
                    item["kind"],
                )
            )

        for item in data.get("start_positions", []):
            self.starts.append(dict(item))
            self.nodes.append(
                self.make_start_marker(
                    SimplePosition(item["x"], item["y"], item["z"]),
                    int(item.get("player", len(self.starts))),
                )
            )


class SimplePosition:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
