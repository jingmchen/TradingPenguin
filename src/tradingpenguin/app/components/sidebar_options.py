from dataclasses import dataclass, field
from tradingpenguin.core import Constants

@dataclass
class SideBarTitleOptions:
    name:str = Constants.AppInfo.APPNAME
    font_size:int = 20
    font_bold:bool = True
    padding_x:int = 20
    padding_top:int = 24
    padding_bottom:int = 16

@dataclass
class SideBarNavOptions:
    active_color: tuple = ("gray75", "gray25")
    hover_color: tuple = ("gray80", "gray30")
    text_color: tuple = ("gray10", "gray90")

@dataclass
class SideBarNavButtonOptions:
    padding_x:int = 12
    padding_y:int = 4
    anchor:str = "w"

@dataclass
class SideBarOptions:
    width:int = 200
    corner_radius:int = 0
    title:SideBarTitleOptions = field(default_factory=SideBarTitleOptions)
    nav:SideBarNavOptions = field(default_factory=SideBarNavOptions)
    nav_button:SideBarNavButtonOptions = field(default_factory=SideBarNavButtonOptions)