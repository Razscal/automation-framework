import logging
import os

class Logger:
    def __init__(self, format_type: str = "%(asctime)s - %(module)s - %(name)s - %(levelname)s - %(message)s", file_path: str = None) -> None:
        self.log = logging
        self.logger = self.log.getLogger(__file__)
        self.format_type = format_type
        self.file_path = file_path
        self.base_config_logger()
        self.config_log_handler()

    def config_log_handler(self) -> None:
        formatter = self.log.Formatter(self.format_type)
        handler = self.log.FileHandler(filename=self.file_path)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def base_config_logger(self) -> None:
        self.log.basicConfig(level=self.log.INFO,format=self.format_type ,filename=self.file_path, filemode="w")

    def trace_exception(self, msg: str) -> None:
        self.log.exception(msg=msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)
        
