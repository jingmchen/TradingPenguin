import customtkinter as ctk
from tradingpenguin.core.configuration import Settings

class MainWindow:
    def __init__(self, root:ctk.CTk, settings:Settings) -> None:
        self.root = root
        self.settings = settings
        self._views:dict[str, ctk.CTkFrame] = {}
        self._current_view:str|None = None

    def _build_layout(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        