from editor.tools.tool import Tool


class LowerTool(Tool):

    def begin(self, pos):
        return None

    def apply(self, pos):
        # apply negative height modification using the brush
        self.app.terrain.modify_height(
            pos,
            -self.app.brush.height_strength,
            self.app.brush.size
        )

    def end(self):
        return None
