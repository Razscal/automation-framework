import os
from dotenv import load_dotenv
from MainFramework.Common.logger import Logger
from MainFramework.Initialization.initializator import Initializator
from MainFramework.Exception.exception import SystemException, BusinessException
from MainFramework.Transaction.transaction import Transaction
from MainFramework.Business.business import Business
from MainFramework.Termination.terminate import Terminate

class Main:

    __config = {}
    load_dotenv()
    Logger()

    def __init__(self) -> None:
        pass

    @staticmethod
    def initialization() -> None:
        """
            Read Config. Initialize all applications.
            If facing any errors, re-try based on what users've config
        """
        try:
            if os.getenv("CONFIG_PATH"):
                Initializator.program(in_config_path=os.getcwd() + os.getenv('CONFIG_PATH'))
            else:
                raise FileNotFoundError(f"Can't retrieve config path {os.getcwd() + os.getenv('CONFIG_PATH')}")
        except Exception as e:
            print(e)
            SystemException.raise_exception(f"Initialization step: {str(e)}")

    @staticmethod
    def get_transaction_item(in_config: dict) -> None:
        """
            Retrieve, set and maintain transactional business data. Decide when process ends.
            -in_config: configuration object retrieves from config file
            Return: None
        """
        try:
            Transaction.program(in_config = in_config)
        except Exception as e:
            print(e)
            SystemException.raise_exception(f"Transaction step: {str(e)}")

    @staticmethod
    def process(in_config : dict) -> None:
        """
                Interact with applications opened in init state using data obtained in the data layer
                A transaction that fails with BusinessException will not retried. All others exception will be retried
                -in_config: configuration object retrieves from config file
                Return: None
        """
        try:
            Business.program(in_config = in_config)
        except Exception as e:
            print(e)
            BusinessException.raise_exception(f"Process Business step: {str(e)}")
            

    @staticmethod
    def end_process() -> None:
        """
                Terminate all process are running
                Return: None
        """
        try:
            Terminate.program()
        except Exception as e:
            SystemException.raise_exception(e)

    @classmethod
    def program(self) -> None:
        """
            Run main program through 4 steps:
                -Initialization
                -Get Transaction Data
                -Run Main Business Process
                -Terminate all process
            Return: None
        """
        self.initialization()
        self.get_transaction_item(self.__config)
        self.process(self.__config)
        #self.end_process()

Main.program()
