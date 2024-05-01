from MainFramework.Initialization.Abstract.abstract_initializor import AbsInitializor

class ApplicationInit(AbsInitializor):
    """
        ApplicationInit class use to initialize all application needed for automation
    """
    def __init__(self) -> None:
        return super().__init__()

    @classmethod
    def init(self, in_config : dict):
        """
        Initialize application
        """
        print("Init Application ...")
        return super().init()    