# Application for TradingPenguin

import customtkinter as ctk
from tradingpenguin.app.views import MainWindow
from tradingpenguin.core import Constants
from tradingpenguin.core.configuration import Settings

class Application:
    def __init__(self, settings:Settings) -> None:
        """Bootstraps TradingPenguin application"""
        self.settings = settings

        # -- Appearance
        ctk.set_appearance_mode(self.settings.theme.theme_mode)
        ctk.set_default_color_theme(self.settings.theme.color_mode)
        
        # -- Root window
        self.root = ctk.CTk()
        self.root.title(Constants.AppInfo.APPNAME)
        self.root.geometry(f"{self.settings.window.width}x{self.settings.window.length}")
        self.root.minsize(self.settings.window.min_length, self.settings.window.min_width)

        # -- Main Window
        self.main_window = MainWindow(self.root, self.settings)
        
    def run(self):
        self.root.mainloop()