from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")


class AzureKeyVault:
    '''
        Azure Key vault actions
        - Provide vault name for authentication
        - Set up your tenant id, client id/secret either on local machine or .env
    '''
    def __init__(self, vault_name: str):
        self.vault_url = f"https://{vault_name}.vault.azure.net/"

    def __auth(self):
        try:
            credential = ClientSecretCredential(
                tenant_id = TENANT_ID,
                client_id = CLIENT_ID,
                client_secret = CLIENT_SECRET,
                connection_verify=False # Only in dev, investigating for furthere stable solution
            )
            client = SecretClient(vault_url=self.vault_url, credential=credential)
            return client
        except Exception as e:
            error_message = f"Couldn't authenticate key vault {self.vault_url}, due to:\n {e}"
            raise Exception(error_message)

    def get_secret(
                    self, 
                    secret_name: str, 
                    secret_version: Optional[str] = None, 
                    **kwargs
                    ) -> str:
        '''
            Get secret value from Azure key vault
            - secret_name: name of target secret to retrieve value
            - secret_version: version of target secret
        '''
        try:
            client = self.__auth()
            secret = client.get_secret(secret_name, secret_version, **kwargs).value
            return secret
        except Exception as e:
            error_message = f"Couldn't retrieve secret {secret_name} from {self.vault_url}, due to:\n {e}"
            raise Exception(error_message)

    def set_secret(
                    self, 
                    secret_name: str, 
                    secret_value: str, 
                    **kwargs
                    ):
        '''
            Set secret value on Azure key vault
            - secret_name: name of target secret to set new value
            - secret_value: value to update secret
        '''
        try:
            client = self.__auth()
            secret = client.set_secret(secret_name, secret_value, **kwargs)
            if secret != None:
                return secret
        except Exception as e:
            error_message = f"Couldn't retrieve secret {secret_name} from {self.vault_url}, due to:\n {e}"
            raise Exception(error_message)
        
    def delete_secret(
                        self, 
                        secret_name: str, 
                        **kwargs
                        ):
        '''
            Delete secret from Azure key vault
            - secret_name: name of target secret to delete
        '''
        try:
            client = self.__auth()
            poller = client.begin_delete_secret(secret_name, **kwargs)
            poller.result()
        except Exception as e:
            error_message = f"Couldn't delete secret {secret_name} from {self.vault_url}, due to:\n {e}"
            raise Exception(error_message)