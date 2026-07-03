from panda3d.core import (
    CollisionTraverser,
    CollisionNode,
    CollisionRay,
    CollisionHandlerQueue,
    BitMask32
)


class MousePicker:

    def __init__(self, app):

        self.app = app

        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        self.ray_node = CollisionNode("mouseRay")
        self.ray = CollisionRay()

        self.ray_node.addSolid(self.ray)
        self.ray_node.setFromCollideMask(BitMask32.bit(1))
        self.ray_node.setIntoCollideMask(BitMask32.allOff())

        self.ray_np = self.app.camera.attachNewNode(self.ray_node)

        self.traverser.addCollider(self.ray_np, self.queue)

    # -------------------------

    def update(self):

        if not self.app.mouseWatcherNode.hasMouse():
            return

        mouse = self.app.mouseWatcherNode.getMouse()

        self.ray.setFromLens(
            self.app.camNode,
            mouse.getX(),
            mouse.getY()
        )

    # -------------------------

    def get_position(self):

        self.update()

        self.traverser.traverse(self.app.render)

        if self.queue.getNumEntries() == 0:
            return None

        self.queue.sortEntries()

        entry = self.queue.getEntry(0)

        return entry.getSurfacePoint(self.app.render)