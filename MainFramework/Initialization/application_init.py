from MainFramework.Initialization.Abstract.abstract_initializor import AbsInitializor
import os

class ApplicationInit(AbsInitializor):
    """
        ApplicationInit class use to initialize all application needed for automation
    """
    def __init__(self) -> None:
        return super().__init__()

    @classmethod
    def init(self, in_config : dict) -> None:
        """
            Initialize application
            -in_config: config object retrieves from config file
            Return: None
        """
        print("Init Application...")
        try:
            pass
        except Exception as e:
            raise Exception(f"{os.path.basename(__name__)}-{e}")    