# Query data from Yahoo Finance (late by 15 mins compared to live data - use for backtesting)

import pandas as pd
import yfinance as yf
from tradingpenguin.core import Constants, Keys
from tradingpenguin.core.dataproviders import Query, HistoricalQueryParams, LiveQueryParams
from tradingpenguin.core.utils import Logger
from tradingpenguin.core.exceptions import QueryUnexpectedError

class YFQuery(Query):
    def __init__(self) -> None:
        self._logger = Logger.for_context(YFQuery)
    
    def fetch_historical_data(
            self,
            *,
            params:HistoricalQueryParams
    ) -> pd.DataFrame|None:
        """
        Fetch historical data from Yahoo Finance using yfinance.
        """

        try:
            stock = yf.Ticker(params.ticker.upper())

            # Casting
            start_date = params.start_date.strftime(Constants.Query.YF_DATEFORMAT)
            end_date = params.end_date.strftime(Constants.Query.YF_DATEFORMAT)

            historical_data = stock.history(
                start=start_date,
                end=end_date,
                interval=params.interval,
                auto_adjust=True
            )

            if historical_data.empty:
                self._logger.warning(f"No historical data retrieved for ticker: '{params.ticker}'. Please verify the ticker symbol or date ranges.")
            
            historical_data.insert(0, params.ticker)

            self._logger.info(f"✓ Successfully fetched historical data for '{params.ticker}'")
            self._logger.info(f"  Date range: {historical_data.index[0]} to {historical_data.index[-1]}")
            self._logger.info(f"  Total records: {len(historical_data)}")

        except QueryUnexpectedError as e:
            self._logger.error(f"✗ Error fetching historical data: {e}")
            return None
    
    def fetch_live_data(
            self,
            *,
            params:LiveQueryParams
    ) -> dict|None:
        """
        Fetch live data from Yahoo Finance using yfinance.
        Only for testing due to delays from actual live data
        """

        try:
            stock = yf.Ticker(params.ticker.upper())
            current_data = stock.history(
                period=params.yf_period,
                interval=params.interval
            )

            if current_data.empty:
                self._logger.info(f"✗ No data fetched for '{params.ticker}'")
                return None

            live_data = {
                Keys.Query.LiveData.TICKER: params.ticker.upper(),
                Keys.Query.LiveData.CURRENT_PRICE: current_data[Keys.Data.Market.CLOSE].iloc[-1],
                Keys.Query.LiveData.LAST_TRADE_TIME: current_data.index[-1],
                Keys.Query.LiveData.HIGH: current_data[Keys.Data.Market.HIGH].iloc[-1],
                Keys.Query.LiveData.LOW: current_data[Keys.Data.Market.LOW].iloc[-1],
                Keys.Query.LiveData.VOLUME: current_data[Keys.Data.Market.VOLUME].iloc[-1]
            }

            self._logger.info(f"✓ Successfully fetched data for '{params.ticker}'")

            return live_data
        except QueryUnexpectedError as e:
            self._logger.error(f"✗ Error fetching live data: {e}")
            return None