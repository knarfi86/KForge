class ToolManager:

    def __init__(self, app):
        self.app = app
        self.tools = {}
        self._current_name = None

    def register(self, name, tool):
        self.tools[name] = tool

    def select(self, name):
        if name not in self.tools:
            return
        self._current_name = name
        # inform UI
        try:
            self.app.ui.set_status(f"tool: {name}")
        except Exception:
            pass

    @property
    def current_tool(self):
        if self._current_name is None:
            return None
        return self.tools.get(self._current_name)

    @property
    def current_name(self):
        return self._current_name

    def begin(self, pos):
        tool = self.current_tool
        if tool:
            return tool.begin(pos)

    def apply(self, pos, force_lower=False):
        if force_lower and "lower" in self.tools:
            return self.tools["lower"].apply(pos)

        tool = self.current_tool
        if tool:
            return tool.apply(pos)

    def end(self):
        tool = self.current_tool
        if tool:
            return tool.end()
