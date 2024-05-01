from MainFramework.Initialization.configuration_init import ConfigurationInit
from MainFramework.Initialization.application_init import ApplicationInit

class Initializator:
    def __init__(self) -> None:
        pass

    @classmethod
    def program(cls, in_config_path: str) -> dict:
        """
            The class uses to initialize all settings which includes Configuration and Relevant Application
            Return : None
        """
        try:
            print(in_config_path)
            out_config : dict = cls.read_configuration(in_config_path = in_config_path)
            cls.init_application(config = out_config)
            return out_config
        except Exception as e:
            raise e

    @staticmethod
    def read_configuration(in_config_path: str) -> dict:
        """
        This class uses to read the configuration file in Data folder
        """
        try:
            ConfigurationInit.init(in_config_path=in_config_path)
        except Exception as e:
            raise e

    @staticmethod
    def init_application(config : dict) -> None:
        """
        The class uses to initialize the needed application
        """
        try:
            ApplicationInit.init(in_config= config)
        except Exception as e:
            raise e

