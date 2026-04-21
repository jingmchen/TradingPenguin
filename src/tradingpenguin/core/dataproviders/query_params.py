# Query params for TradingPenguin

from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from tradingpenguin.core import Constants

class QueryInterval(StrEnum):
    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    SIXTY_MINUTES = "60m"
    NINETY_MINUTES = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"

@dataclass
class HistoricalQueryParams:
    """
    Holds a group of input params for `fetch_historical_data` method.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (datetime|None): Start date in 'YYYY-MM-DD' format
        end_date (datetime|None): End date in 'YYYY-MM-DD' format
        interval (QueryInterval(StrEnum)): valid intervals; 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    
    ticker:str
    start_date:datetime = field(
        default_factory=lambda:
        (datetime.now() - timedelta(days=Constants.Query.LOOKBACK_DAYS))
    )
    end_date:datetime = field(
        default_factory=lambda:
        datetime.now()
    )
    interval:QueryInterval

@dataclass
class LiveQueryParams:
    """
    Holds a group of input params for `fetch_live_data` method.

    Args:
        ticker (str): Stock ticker symbol
        interval (QueryInterval(StrEnum)): valid intervals; 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """

    ticker:str
    interval:QueryInterval

    # Fixed parameters, non-ctor params
    yf_period:str = field(default="1d", init=False)