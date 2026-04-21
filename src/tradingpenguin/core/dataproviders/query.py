# Abstract class for query classes

from abc import ABC, abstractmethod
from tradingpenguin.core.dataproviders import HistoricalQueryParams, LiveQueryParams

class Query(ABC):
    @abstractmethod
    def fetch_historical_data(self, params:HistoricalQueryParams, *args, **kwargs):
        pass
    
    @abstractmethod
    def fetch_live_data(self, params:LiveQueryParams, *args, **kwargs):
        pass