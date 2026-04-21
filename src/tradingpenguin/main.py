# Main entry point for TradingPenguin

from tradingpenguin.app import Application
from tradingpenguin.core.configuration import SettingsProvider, Settings
from tradingpenguin.core.utils import LogManager, Logger, configure_logger

def main(sysargv:list[str]|None = None) -> None:
    # -- CLEAN UP OLD LOGS
    LogManager.archive_previous_logs()
    LogManager.clean_old_logs()

    # -- SET UP LOGGER
    configure_logger()
    logger = Logger.for_context(__name__)

    # -- SET UP CONFIG
    settings = SettingsProvider().load_settings()

    # -- Bootstrap application
    app = Application(settings=settings)
    app.run()

if __name__ == "__main__":
    main()