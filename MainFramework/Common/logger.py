import logging
import os
from datetime import datetime
from dotenv import load_dotenv

class Logger:
    """
    Custom Logger using logging library:
        - format_type: format of logging file
        - file_mode: logging.BasicConfig mode "a" for append, mode "w" for replace, ...
    """
    load_dotenv()
    __logger : logging.Logger = None
    if not __logger:
        __logger = logging.getLogger(__name__)
        print(__logger.hasHandlers())
    else:
        pass
    
    def __init__(self, file_mode: str = "a", format_type="%(asctime)s - %(created)s - %(msecs)s - %(levelname)s - %(message)s") -> None:
        try:
            self.format_type = format_type
            self.file_mode = file_mode
            if os.getenv('AUTOMATION_LOGS') and os.getenv('PROCESS_NAME'):
                self.file_path = f"{os.getcwd()}/{os.getenv('AUTOMATION_LOGS')}/{datetime.now().strftime('%d%m%Y')}-{os.getenv('PROCESS_NAME')}.log"
            else:
                raise Exception("os.getenv('AUTOMATION_LOGS') or os.getenv('PROCESS_NAME') are not set")
            self.__base_config_logger()
            self.__config_log_handler()
        except FileNotFoundError as e:
            raise Exception(f"File path: {self.file_path} does not exist")
        except Exception as e:
            raise e

    def __config_log_handler(self) -> None:
        """
            Set up handler for logging
            Return: None
        """
        formatter = logging.Formatter(self.format_type)
        handler = logging.FileHandler(filename=self.file_path)
        handler.setFormatter(formatter)
        self.__logger.addHandler(hdlr= handler)

    def __base_config_logger(self) -> None:
        """
            Set up baseConfig for logging
            Return: None
        """
        logging.basicConfig(level=logging.INFO, format=self.format_type)

    @staticmethod
    def trace_exception(msg: str) -> None:
        """
            -msg: log messages
            Return: None
        """
        Logger.__logger.exception(msg=msg)

    @staticmethod
    def info(msg) -> None:
        """
            -msg: log messages
            Return: None
        """
        Logger.__logger.info(msg)

    @staticmethod
    def error(msg) -> None:
        """
            -msg: log messages
            Return: None
        """
        Logger.__logger.error(msg)

    @staticmethod
    def debug(msg) -> None:
        """
            -msg: log messages
            Return: None
        """
        Logger.__logger.debug(msg)
    
    @staticmethod
    def critical(msg) -> None:
        """
            -msg: log messages
            Return: None
        """
        Logger.__logger.critical(msg)