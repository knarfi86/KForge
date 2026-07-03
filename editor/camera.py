from direct.task import Task
from panda3d.core import Vec3

from editor import config


class CameraController:

    def __init__(self, app):

        self.app = app
        self.camera = app.camera

        # Startposition
        self.camera.setPos(*config.CAMERA_START_POS)
        self.camera.lookAt(0, 0, 0)

        app.camLens.setFov(config.CAMERA_FOV)

        # Tastatur
        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "q": False,
            "e": False,
            "shift": False,
            "mouse2": False
        }

        for key in self.keys:
            app.accept(key, self.set_key, [key, True])
            app.accept(f"{key}-up", self.set_key, [key, False])

        # Zoom
        app.accept("wheel_up", self.zoom_in)
        app.accept("wheel_down", self.zoom_out)

        self.last_mouse = None

        app.taskMgr.add(self.update, "camera_update")

    def set_key(self, key, value):
        self.keys[key] = value

    def zoom_in(self):
        fov = self.app.camLens.getFov().x
        fov = max(config.CAMERA_MIN_FOV, fov - config.CAMERA_ZOOM_STEP)
        self.app.camLens.setFov(fov)

    def zoom_out(self):
        fov = self.app.camLens.getFov().x
        fov = min(config.CAMERA_MAX_FOV, fov + config.CAMERA_ZOOM_STEP)
        self.app.camLens.setFov(fov)

    def update(self, task):

        dt = globalClock.getDt()

        speed = config.CAMERA_SPEED

        if self.keys["shift"]:
            speed = config.CAMERA_FAST_SPEED

        move = Vec3(0, 0, 0)

        if self.keys["w"]:
            move.y += 1

        if self.keys["s"]:
            move.y -= 1

        if self.keys["a"]:
            move.x -= 1

        if self.keys["d"]:
            move.x += 1

        if self.keys["q"]:
            move.z -= 1

        if self.keys["e"]:
            move.z += 1

        if move.length() > 0:
            move.normalize()
            self.camera.setPos(
                self.camera,
                move * speed * dt
            )

        # Kamera drehen nur mit mittlerer Maustaste
        if self.keys["mouse2"]:

            if self.app.mouseWatcherNode.hasMouse():

                x = self.app.mouseWatcherNode.getMouseX()
                y = self.app.mouseWatcherNode.getMouseY()

                if self.last_mouse is None:
                    self.last_mouse = (x, y)

                dx = x - self.last_mouse[0]
                dy = y - self.last_mouse[1]

                self.camera.setH(
                    self.camera.getH()
                    - dx * 150 * config.CAMERA_ROTATE_SPEED
                )

                pitch = (
                    self.camera.getP()
                    - dy * 150 * config.CAMERA_ROTATE_SPEED
                )

                pitch = max(-89, min(89, pitch))

                self.camera.setP(pitch)

                self.last_mouse = (x, y)

        else:
            self.last_mouse = None

        return Task.cont
