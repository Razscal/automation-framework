from office365.sharepoint.client_context import ClientContext
from dotenv import load_dotenv
from pathlib import PurePath
import os

load_dotenv()
SITE_URL = os.getenv("SITE_URL")
SITE_NAME = os.getenv("SITE_NAME")
DOC_NAME = os.getenv("DOC_NAME")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

class Sharepoint:
    def __auth(self):
        '''
            Authenticate Sharepoint App-only with client id and client secret
        '''
        try:
            ctx = ClientContext(SITE_URL).with_client_credentials(CLIENT_ID, CLIENT_SECRET)
            print(f"Access to {SITE_URL} has been authenticated!")
            return ctx
        except Exception as e:
            error_message = f"Access to {SITE_URL} was decliend due to:\n {e}"
            raise Exception(error_message)
    
    def __get_file_list(self, folder_relative_url: str):
        '''
            Retrieve all file objects inside a folder on Sharepoint
                - folder_relative_url: url of target folder to retrieve the list of all files inside of it (with out DOC_NAME). 
                - E.g.: Data/2024
        '''
        try:
            ctx = self.__auth()
            target_folder_url = f"{DOC_NAME}/{folder_relative_url}"
            folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
            folder.expand(["Folders, Files"]).get().execute_query()
            return folder.files
        except Exception as e:
            error_message = f"Couldn't get file list from folder {folder_relative_url} due to:\n {e}"
            raise Exception(error_message)
        
    def __save_file(self, local_folder_dest: str, local_file_name: str, file_object):
        '''
            Save file from Sharepoint by writing file oject to local file in binary mode
        '''
        try:
            file_dir_path = PurePath(local_folder_dest, local_file_name)
            with open(file_dir_path, "wb") as f:
                f.write(file_object)
        except Exception as e:
            error_message = f"Couldn't write file_object to {file_dir_path}, due to:\n {e}"
            raise Exception(error_message)

    def download_file(self, file_relative_url: str, local_folder_dest: str):
        '''
            Download file from Sharepoint
                - file_relative_url: relative url to target file. 
                - E.g.: file_relative_url = "Data/2024/2024.xlsx", SITE_NAME = "Contoso", DOC_NAME = "Shared Documents"
                => Full url: /sites/Contoso/Shared Documents/Data/2024.xlsx
        '''
        try:
            ctx = self.__auth()
            file_url = f"/sites/{SITE_NAME}/{DOC_NAME}/{file_relative_url}"
            file_object = ctx.web.get_file_by_server_relative_path(file_relative_url).execute_query()
            print(f"Retrieved file from {SITE_URL}/{file_url}, ready for download")
        except Exception as e:
            error_message = f"Couldn't retrieve file object from {SITE_URL}/{file_url}, due to:\n {e}"
            raise Exception(error_message)
        
        self.__save_file(local_folder_dest, file_object.name, file_object)
    
    def download_files(self, local_folder_dest: str, file_relative_urls: list):
        try:
            for file_relative_url in file_relative_urls:
                self.download_file(file_relative_url, local_folder_dest)
        except:
            print("Couldn't download multiple files")
    
    def download_all_files_in_subfolder(self, local_folder_dest: str, folder_relative_url: str):
        try:
            file_list = self.__get_file_list(folder_relative_url)
            for file in file_list:
                self.__save_file(local_folder_dest, file.name, file)
        except Exception as e:
            error_message = f"Couldn't download all files from {folder_relative_url} due to:\n {e}"
            raise Exception(error_message)

    def upload_file(self, relative_url, local_file_path):
        try:
            ctx = self.__auth()
            target_url = f"sites/{SITE_NAME}/{DOC_NAME}/{relative_url}"
            folder = ctx.web.get_folder_by_server_relative_url(target_url)

            with open(local_file_path, "rb") as f:
                file = folder.files.upload(f).execute_query()
            print(f"Upload {local_file_path} to {target_url} successfully")
        except Exception as e:
            error_message = f"Upload {local_file_path} to {relative_url} unsuccessfully, due to:\n {e}"
            raise Exception(error_message)
    