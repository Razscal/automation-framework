from MainFramework.Initialization.Abstract.abstract_initializor import AbsInitializor
import pandas as pd

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
        Read config file
        """
        try:
            print("Initializing Configuration...")
            print("inconfigpath" + in_config_path)
            df = pd.read_excel(in_config_path, sheet_name= 'CONFIG_VALUE')
            print(df)
            for index, row in df.iterrows():
                key = row['Key']
                value = row['Value']
                cls.config[key] = value
            print(cls.config)
            return cls.config
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e
        
