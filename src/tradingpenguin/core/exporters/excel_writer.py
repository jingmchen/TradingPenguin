# Excel Writer to save DataFrames to Excel files

import pandas as pd
from pathlib import Path
from tradingpenguin.core import Keys
from tradingpenguin.core.utils import Logger
from tradingpenguin.core.exceptions import ExcelWriterUnexpectedError

class ExcelWriter:
    """Writes DataFrame to an Excel file."""

    def __init__(self) -> None:
        self._logger = Logger.for_context(ExcelWriter)
    
    def save_data_to_excel(
            self,
            *,
            data:pd.DataFrame,
            excel_file_path:str|Path,
            excel_sheet_name:str,
            overwrite:bool = True
    ) -> None:
        """
        Saves DataFrame to an Excel file path
        
        Args:
            data (pd.DataFrame): Data to be saved
            excel_file_path (str|Path): file path to the Excel file
            excel_sheet_name (str): Excel worksheet name
            overwrite (bool): 
        """

        try:
            data_copy = data.copy()

            # Reset index to make a date column
            data_copy.reset_index(inplace=True)

            # Remove timezone data from any columns (i.e., datetime columns) to make it Excel-compatible
            for col in data_copy.columns:
                if pd.api.types.is_datetime64_any_dtype(data_copy[col]):
                    data_copy[col] = data_copy[col].dt.tz_localize(None)
            
            # Create new file if not exists, and write
            if not excel_file_path.exists():
                data_copy.to_excel(
                    excel_writer=excel_file_path,
                    index=False,
                    sheet_name=excel_sheet_name
                )
                self._logger.info(f"✓ Created new Excel file: {excel_file_path} | Sheet: {excel_sheet_name}")
                return None
            
            # If file path exists, check existing worksheets
            with pd.ExcelFile(excel_file_path) as xls:
                existing_sheets = xls.sheet_names
            
            sheet_exists = excel_sheet_name in existing_sheets

            if sheet_exists and not overwrite:
                # Worksheets exists, to append
                existing_data = pd.read_excel(
                    io=excel_file_path,
                    sheet_name=excel_sheet_name
                )
                data_copy = (
                    pd.concat([existing_data, data_copy], ignore_index=True)
                    .drop_duplicates(keep='last')
                    .sort_values(by=Keys.Data.Market.DATE)
                )
                logger_message = "Appended worksheet with new data"
            elif sheet_exists and overwrite:
                # Worksheet exists, to overwrite
                logger_message = "Overwritten existing data in worksheet"
            else:
                # Worksheet do not exist, create new
                logger_message = "Created new worksheet"
            
            # Write to existing file
            with pd.ExcelWriter(
                path=excel_file_path,
                mode="a",
                if_sheet_exists="replace",
                engine="openpyxl"
            ) as writer:
                data_copy.to_excel(
                    excel_writer=writer,
                    index=False,
                    sheet_name=excel_sheet_name
                )
            
            self._logger.info(f"✓ Successfully saved DataFrame to path: {excel_file_path} | {logger_message} : {excel_sheet_name}")
            return None
        
        except ExcelWriterUnexpectedError as e:
            self._logger.error(f"✗ Error saving DataFrame to Excel: {e}")
            return False
