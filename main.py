import os
from dotenv import load_dotenv
from MainFramework.Initialization.initializator import Initializator
from MainFramework.Exception.exception import SystemException, BusinessException
from MainFramework.Transaction.transaction import Transaction
from MainFramework.Business.business import Business
from MainFramework.Termination.terminate import Terminate

class Main:

    __config = {}

    def __init__(self) -> None:
        pass

    @staticmethod
    def initialization() -> None:
        try:
            load_dotenv()
            if os.getenv("CONFIG_PATH"):
                Initializator.program(in_config_path=os.getenv("CONFIG_PATH"))
            else:
                raise FileNotFoundError("Can't retrieve config path")
        except Exception as e:
            raise SystemException.raise_exception(e)

    @staticmethod
    def get_transaction_item(in_config: dict) -> None:
        try:
            Transaction.program()
        except Exception as e:
            raise SystemException.raise_exception(e)

    @staticmethod
    def process(in_config : dict) -> None:
        try:
            Business.program()
        except Exception as e:
            raise BusinessException.raise_exception(e)

    @staticmethod
    def end_process(in_confg : dict) -> None:
        try:
            Terminate.program()
        except Exception as e:
            print("Kill all process ...")

    @classmethod
    def program(self):
        self.initialization()
        self.get_transaction_item(self.__config)
        self.process(self.__config)
        self.end_process(self.__config)

Main.program()
