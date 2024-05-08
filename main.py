import os
from dotenv import load_dotenv
from MainFramework.Common.logger import Logger
from MainFramework.Initialization.initializator import Initializator
from MainFramework.Exception.exception import SystemException, BusinessException
from MainFramework.Transaction.transaction import Transaction
from MainFramework.Business.business import Business
from MainFramework.Termination.terminate import Terminate

max_sysex_retry = 3
sysex_retry_count = 0
max_businessex_retry = 3
businessex_retry_count = 0

class Main:
    __config = {}
    load_dotenv()
    # Logger()

    def __init__(self) -> None:
        pass

    @staticmethod
    def initialization() -> None:
        """
            Read Config. Initialize all applications.
            If facing any errors, re-try based on what users've config
        """
        global max_sysex_retry
        global sysex_retry_count
        try:
            if os.getenv("CONFIG_PATH"):
                Main.__config = Initializator.program(in_config_path=os.getcwd() + os.getenv('CONFIG_PATH'))
                max_sysex_retry = int(Main.__config["max_sysex_retry"])
                sysex_retry_count = 0
            else:
                raise FileNotFoundError(f"Can't retrieve config path {os.getcwd() + os.getenv('CONFIG_PATH')}")
        except Exception as e:
            if (sysex_retry_count < max_sysex_retry):
                sysex_retry_count += 1
                Logger.info(f"Retry initialization, count: {str(sysex_retry_count)}")
                Main.initialization()
            else:
                print(e)
                SystemException.raise_exception(f"Initialization step: {str(e)}")

    @staticmethod
    def get_transaction_item(in_config: dict) -> None:
        """
            Retrieve, set and maintain transactional business data. Decide when process ends.
            -in_config: configuration object retrieves from config file
            Return: None
        """
        global max_sysex_retry
        global sysex_retry_count
        try:
            Transaction.program(in_config = in_config)
            max_sysex_retry = int(in_config["max_sysex_retry"])
            sysex_retry_count = 0
        except Exception as e:
            if (sysex_retry_count < max_sysex_retry):
                sysex_retry_count += 1
                Logger.info(f"Retry get transaction item, count: {str(sysex_retry_count)}")
                Main.get_transaction_item(in_config)
            else:
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
        global max_businessex_retry
        global businessex_retry_count
        try:
            Business.program(in_config = in_config)
            max_businessex_retry = int(in_config["max_businessex_retry"])
            businessex_retry_count = 0
        except Exception as e:
            if (businessex_retry_count < max_businessex_retry):
                businessex_retry_count += 1
                Logger.info(f"Retry process, count: {str(businessex_retry_count)}")
                Main.process(in_config)
            else:
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
            if (sysex_retry_count < max_sysex_retry):
                sysex_retry_count += 1
                Logger.info(f"Retry end process, count: {str(sysex_retry_count)}")
                Main.end_process()
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
