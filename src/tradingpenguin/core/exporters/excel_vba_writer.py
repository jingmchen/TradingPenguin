# Adds VBA scripts to a targeted Excel workbook

import xlwings as xw
from pathlib import Path
from tradingpenguin.core import Keys
from tradingpenguin.core.utils import Logger
from tradingpenguin.core.exceptions import ExcelWriterUnexpectedError

class ExcelVBAWriter:
    def __init__(self) -> None:
        self._logger = Logger.for_context(ExcelVBAWriter)
        self.script_dir = Path(__file__).parent / "scripts"
    
    def insert_macro_into_workbook(
            self,
            *,
            excel_file_path:str|Path,
            macro_file:str,
            macro_name:str|None = None
    ) -> None:
        macro_file_path = self.script_dir / Path(macro_file).with_suffix(Keys.Exporter.ExcelVBAWriter.MACRO_FILE_EXT)

        if not macro_file_path.exists():
            self._logger.error(f"Macro file not found at: {macro_file_path}.")
        
        vba_code = Path(macro_file_path).read_text(encoding="utf-8")

        try:
            wb = xw.Book(excel_file_path)

            vba_module = wb.api.VBProject.VBComponents.Add(1)
            vba_module.Name = macro_name or macro_file.removesuffix(".txt")
            vba_module.CodeModule.AddFromString(vba_code)

            self._logger(f"✓ Successfully embedded VBA macros into Excel workbook: {excel_file_path}.")
        
        except ExcelWriterUnexpectedError as e:
            self._logger.error(f"✗ Error saving VBA macros to Excel workbook: {e}")
        
        finally:
            wb.close()