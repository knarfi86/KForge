class History:

    def __init__(self, limit=50):

        self.limit = limit
        self.undo_stack = []
        self.redo_stack = []

    def snapshot(self, heights):

        self.undo_stack.append(dict(heights))

        if len(self.undo_stack) > self.limit:
            self.undo_stack.pop(0)

        self.redo_stack.clear()

    def undo(self, current):

        if not self.undo_stack:
            return None

        self.redo_stack.append(dict(current))
        return self.undo_stack.pop()

    def redo(self, current):

        if not self.redo_stack:
            return None

        self.undo_stack.append(dict(current))
        return self.redo_stack.pop()
