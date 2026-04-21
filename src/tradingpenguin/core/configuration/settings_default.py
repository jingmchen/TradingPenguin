# Defaults for settings.json for TradingPenguin

from typing import Final
from tradingpenguin.core.configuration import LogLevel, ThemeMode, ColorMode

class SettingsDefault:
    """Settings defaults for TradingPenguin"""
    class LoggingSection:
        log_level:Final[LogLevel] = LogLevel.INFO
        retained_days:Final[int] = 7

    class ThemeSection:
        theme_mode:Final[ThemeMode] = ThemeMode.LIGHT
        color_mode:Final[ColorMode] = ColorMode.BLUE
        font_family:Final[str] = "Segoe UI"
        font_size:Final[int] = 12
    
    class WindowSection:
        length:Final[int] = 1100
        width:Final[int] = 500
        min_length:Final[int] = 800
        min_width:Final[int] = 500
        max_length:Final[int] = 1920
        max_width:Final[int] = 1080