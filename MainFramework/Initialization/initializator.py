from MainFramework.Initialization.configuration_init import ConfigurationInit
from MainFramework.Initialization.application_init import ApplicationInit
from MainFramework.Common.logger import Logger

class Initializator:
    """
        The class uses static method program() for initialize configuration and application needed for automation
    """
    def __init__(self) -> None:
        pass
    
    @classmethod
    def program(cls, in_config_path: str) -> dict:
        """
            The class uses to initialize all settings which includes Configuration and Relevant Application
            -in_config_path: config_path to get the config object
            Return : None
        """
        out_config : dict = cls.read_configuration(in_config_path = in_config_path)
        cls.init_application(config = out_config)
        return out_config

    @staticmethod
    def read_configuration(in_config_path: str) -> dict:
        """
            This class uses to read the configuration file in Data folder
            -in_config_path: config_path to get the config object
            Return: dict
        """
        ConfigurationInit.init(in_config_path=in_config_path)

    @staticmethod
    def init_application(config : dict) -> None:
        """
            The class uses to initialize the needed application
            -config : config object retrieves from config file
            Return: None
        """
        ApplicationInit.init(in_config= config)

