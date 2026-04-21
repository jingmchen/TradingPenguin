# Values initialized from settings.json

from dataclasses import dataclass
from tradingpenguin.core.base import KeyEnum

class LogLevel(KeyEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ThemeMode(KeyEnum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

class ColorMode(KeyEnum):
    BLUE = "blue"
    GREEN = "green"
    DARK_BLUE = "dark-blue"

@dataclass
class LoggingSection:
    log_level:LogLevel
    retained_days:int

@dataclass
class ThemeSection:
    theme_mode:ThemeMode
    color_mode:ColorMode
    font_family:str
    font_size:int

@dataclass
class WindowSection:
    length:int
    width:int
    min_length:int
    min_width:int

@dataclass
class Settings:
    logging:LoggingSection
    theme:ThemeSection
    window:WindowSection