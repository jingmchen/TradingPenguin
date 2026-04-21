# Loads and validates settings.json into settings.py class

import json
from enum import Enum
from typing import TypeVar
from functools import lru_cache
from tradingpenguin.core import Constants, Keys
from tradingpenguin.core.configuration import LoggingSection, ThemeSection, WindowSection, Settings, SettingsDefault, LogLevel, ThemeMode, ColorMode
from tradingpenguin.core.exceptions import MissingKeyError, InvalidValueError, MissingSectionError
from tradingpenguin.core.utils import Logger

E = TypeVar("E", bound=Enum)

class SettingsProvider:
    """Provides `settings` class from settings.json"""

    def __init__(self) -> None:
        self._logger = Logger.for_context(SettingsProvider)

    @lru_cache
    def load_settings(self) -> Settings:
        settings_path = Constants.File.Path.SETTINGS

        if not settings_path.exists():
            raise FileNotFoundError(f"Settings file not found at: {Constants.File.Path.SETTINGS}.")
        
        with settings_path.open(encoding="utf-8") as f:
            raw = json.load(f)
        
        for section in (Keys.Settings.LoggingSection.TITLE, Keys.Settings.ThemeSection.TITLE):
            if section not in raw:
                raise MissingSectionError(section)
        
        return Settings(
            logging=self._load_logging_section(raw[Keys.Settings.LoggingSection.TITLE]),
            theme=self._load_theme_section(raw[Keys.Settings.ThemeSection.TITLE]),
            window=self._load_window_section(raw[Keys.Settings.WindowSection.TITLE])
        )

    def _load_logging_section(self, data:dict) -> LoggingSection:
        for key in (Keys.Settings.LoggingSection.LOG_LEVEL, Keys.Settings.LoggingSection.RETAINED_DAYS):
            if key not in data:
                raise MissingKeyError(f"{Keys.Settings.LoggingSection.TITLE}.{key}")
        
        return LoggingSection(
            log_level=self._parse_enum(
                enum=LogLevel,
                key=Keys.Settings.LoggingSection.LOG_LEVEL,
                value=data[Keys.Settings.LoggingSection.LOG_LEVEL],
                defaultvalue=SettingsDefault.LoggingSection.log_level
            ),
            retained_days=self._validate_values(
                key=Keys.Settings.LoggingSection.RETAINED_DAYS,
                value=data[Keys.Settings.LoggingSection.RETAINED_DAYS],
                min_limit=0,
                defaultvalue=SettingsDefault.LoggingSection.retained_days
            )
        )
    
    def _load_theme_section(self, data:dict) -> ThemeSection:
        for key in (
            Keys.Settings.ThemeSection.THEME_MODE,
            Keys.Settings.ThemeSection.COLOR_MODE,
            Keys.Settings.ThemeSection.FONT_FAMILY,
            Keys.Settings.ThemeSection.FONT_SIZE
        ):
            if key not in data:
                raise MissingKeyError(f"{Keys.Settings.ThemeSection.TITLE}.{key}")
        
        return ThemeSection(
            theme_mode=self._parse_enum(
                enum=ThemeMode,
                key=Keys.Settings.ThemeSection.THEME_MODE,
                value=data[Keys.Settings.ThemeSection.THEME_MODE],
                defaultvalue=SettingsDefault.ThemeSection.theme_mode
            ),
            color_mode=self._parse_enum(
                enum=ColorMode,
                key=Keys.Settings.ThemeSection.COLOR_MODE,
                value=data[Keys.Settings.ThemeSection.COLOR_MODE],
                defaultvalue=SettingsDefault.ThemeSection.color_mode
            ),
            font_family=data[Keys.Settings.ThemeSection.FONT_FAMILY],
            font_size=self._validate_values(
                key=Keys.Settings.ThemeSection.FONT_SIZE,
                value=data[Keys.Settings.ThemeSection.FONT_SIZE],
                min_limit=1,
                defaultvalue=SettingsDefault.ThemeSection.font_size
            )
        )
    
    def _load_window_section(self, data:dict) -> WindowSection:
        for key in (
            Keys.Settings.WindowSection.LENGTH,
            Keys.Settings.WindowSection.WIDTH,
            Keys.Settings.WindowSection.MIN_LENGTH,
            Keys.Settings.WindowSection.MIN_WIDTH
        ):
            if key not in data:
                raise MissingKeyError(f"{Keys.Settings.WindowSection.TITLE}.{key}")
        
        return WindowSection(
            length=self._validate_values(
                key=Keys.Settings.WindowSection.LENGTH,
                value=data[Keys.Settings.WindowSection.LENGTH],
                min_limit=SettingsDefault.WindowSection.min_length,
                max_limit=SettingsDefault.WindowSection.max_length,
                defaultvalue=SettingsDefault.WindowSection.length
            ),
            width=self._validate_values(
                key=Keys.Settings.WindowSection.WIDTH,
                value=data[Keys.Settings.WindowSection.WIDTH],
                min_limit=SettingsDefault.WindowSection.min_width,
                max_limit=SettingsDefault.WindowSection.max_width,
                defaultvalue=SettingsDefault.WindowSection.width
            ),
            min_length=self._validate_values(
                key=Keys.Settings.WindowSection.MIN_LENGTH,
                value=data[Keys.Settings.WindowSection.MIN_LENGTH],
                min_limit=SettingsDefault.WindowSection.min_length,
                max_limit=SettingsDefault.WindowSection.max_length,
                defaultvalue=SettingsDefault.WindowSection.min_length
            ),
            min_width=self._validate_values(
                key=Keys.Settings.WindowSection.MIN_WIDTH,
                value=data[Keys.Settings.WindowSection.MIN_WIDTH],
                min_limit=SettingsDefault.WindowSection.min_width,
                max_limit=SettingsDefault.WindowSection.max_width,
                defaultvalue=SettingsDefault.WindowSection.min_width
            )
        )
    
    def _validate_values(self, *, key:str, value:str|int, min_limit:str|int = None, max_limit:str|int = None, defaultvalue:str|int) -> str:
        try:
            num_value = float(value)

            if (min_limit is not None and num_value < float(min_limit)) or (max_limit is not None and num_value > float(max_limit)):
                self._logger.warning(
                    f"Key value for key: '{key}' is invalid. Reverting to default: '{defaultvalue}'"
                )
                return defaultvalue
        except ValueError:
            self._logger.warning(
                    f"Key value for key: '{key}' is not a number. Reverting to default: '{defaultvalue}'"
                )
            return defaultvalue
        
        return value
    
    def _parse_enum(self, *, enum:type[E], key:str, value:str|int, defaultvalue:E) -> E:
        match = next(
            (member for member in enum if member.name.casefold() == value.casefold()),
            None
        )
        
        if match is None:
            self._logger.warning(
                f"Unable to parse key '{key}' value: '{value}'. Reverting to default: {defaultvalue}"
            )
            return defaultvalue
        
        return match
