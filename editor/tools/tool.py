from abc import ABC, abstractmethod


class Tool(ABC):

    def __init__(self, app):
        self.app = app

    def begin(self, pos):
        """Called when a stroke begins. pos may be None."""
        return None

    def apply(self, pos):
        """Called repeatedly while mouse is held and pointer is over terrain."""
        return None

    def end(self):
        """Called when a stroke ends."""
        return None
