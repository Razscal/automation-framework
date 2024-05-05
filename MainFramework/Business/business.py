import os

class Business:
    def __init__(self) -> None:
        pass

    @staticmethod
    def program(in_config: dict) -> None:
        """
            Run main business process
            Return: None
        """
        try:
            print("Rum Main Business Process...")
            pass
        except Exception as e:
            raise Exception(f"{os.path.basename(__name__)}-{e}")