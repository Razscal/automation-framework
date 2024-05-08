from MainFramework.Initialization.Abstract.abstract_initializor import AbsInitializor
import pandas as pd
import os

class ConfigurationInit(AbsInitializor):
    """
        ConfigurationInit class use to read all configuration in config.xlsx file
    """
    config : dict = {}

    def __init__(self) -> None:
        pass

    @classmethod
    def init(cls, in_config_path: str) -> dict:
        """
            Read config file using pandas sheet "CONFIG_VALUE"
            -in_config_path: config_path to get the config object
            Return: config : dict
        """
        try:
            print("Initializing Configuration...")
            df = pd.read_excel(in_config_path, sheet_name= 'CONFIG_VALUE')
            for index, row in df.iterrows():
                key = row['Key']
                value = row['Value']
                cls.config[key] = value
            return cls.config
        except Exception as e:
            raise Exception(f"{os.path.basename(__name__)}-{e}")
        
