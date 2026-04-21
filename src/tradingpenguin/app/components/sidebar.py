import customtkinter as ctk
from typing import Callable
from tradingpenguin.app.components import SideBarOptions
from tradingpenguin.core import Constants

class SideBar:
    def __init__(
            self,
            parent,
            nav_items:list[str],
            on_navigate:Callable[[str], None],
            options:SideBarOptions|None = None
    ) -> None:
        self.options = options or SideBarOptions()
        self.on_navigate = on_navigate
        self._buttons:dict[str, ctk.CTkButton] = {}

        self.frame = ctk.CTkFrame(
            parent,
            width=self.options.width,
            corner_radius=self.options.corner_radius
        )

        self.frame.grid_propagate(False)
        self.frame.grid_rowconfigure(len(nav_items) + 2, weight=1)

        self._build(nav_items)
    
    def _build(self, nav_items:list[str]) -> None:
        title = ctk.CTkLabel(
            self.frame,
            text=self.options.title.name,
            font=ctk.CTkFont(
                size=self.options.title.font_size,
                weight="bold" if self.options.title.font_bold else "normal"
            )
        )