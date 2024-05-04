import os
from dotenv import load_dotenv
from MainFramework.Common.logger import Logger
import logging

class SystemException(Exception):
    """
        The exception happens during initialization and get transaction data
    """
    logger = Logger()
    def __init__(self ,*args):
        super().__init__(*args)
    
    @classmethod
    def raise_exception(cls, exception: Exception) -> None:
        """
            Raise system exception
            -exception: exception retrieves from sub-function
        """
        # Send email or perform other advanced exception handling
        
        Logger.error(str(exception))
        os._exit(1)

class BusinessException(Exception):
    """
        The exception happens when facing any errors during automation
    """

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def raise_exception(cls, exception: Exception) -> None:
        """
            Raise business exception
            -exception: exception retrieves from sub-function
        """
        # Send email or perform other advanced exception handling
        Logger.error((str(exception)))
        os._exit(1)
        
        