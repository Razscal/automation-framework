import win32com.client as client
from typing import List, Optional, Tuple

class Outlook:
    '''
        Automate Outlook tasks
    '''
    def __init__(self) -> tuple:
        self.ol, self.namespace, self.default_account = self.__get_outlook_config()
    
    @staticmethod
    def __get_outlook_config() -> tuple:
        '''
            Initialize connection to Outlook, return a tuple for Application object, namespace object, default account
        '''
        try:
            ol = client.Dispatch("Outlook.Application")
            namespace = ol.GetNamespace("MAPI")
            default_account = ol.Session.Accounts[0]
            return  ol, namespace, default_account
        except Exception as e:
            error_message = f"Couldn't get outlook config, due to {e}"
            raise Exception(error_message)
    
    def __get_folder(
                    self,
                    folder_name: str, 
                    account_address: Optional[str] = None
                    ):
        '''
            Retrieve Outlook folder object
                - account_address: account address where target folder is stored
                - folder_name: target folder. E.g: Inbox
        '''
        try:
            if account_address == None: 
                used_account = self.default_account
            else:
                used_account = self.namespace.Session.Accounts.Item(account_address)

            root_folder = self.namespace.Folders.Item(used_account.DeliveryStore.DisplayName)
            folder = root_folder.Folders(folder_name)
            return folder
        except Exception as e:
            error_message = f"Couldn't retreive folder object {folder_name}, due to:\n {e}"
            raise Exception(error_message)
    
    @staticmethod
    def delete_mail_message(mail_item):
        """
            Delete Email message
                -mail_item: email that exists in Outlook folder
        """
        try:
            mail_item.Delete()
        except Exception as e:
            error_message = f'Error deleteing mail message, due to:\n {e}'
            raise Exception(error_message)
        
    @staticmethod    
    def mark_as_read_unread(mail_item, mark_unread: bool):
        '''
            Mark mail message as read/unread:
                - mail_item: MailItem object
                - mark_unread: False=Mark as read, True=Mark as unread
        '''
        try:
            mail_item.UnRead = mark_unread
        except Exception as e:
            error_message = f'Error marking message as read/unread, due to:\n {e}'
            raise Exception(error_message)

    def send_mail_message(
                        self,
                        mail_to: str, 
                        mail_from: Optional[str] = None, 
                        mail_cc: Optional[str] = None,
                        subject: Optional[str] = None,
                        body: Optional[str] = None,
                        attachments: Optional[List[str]] = [],
                        is_body_html: Optional[str] = False
                        ) -> Tuple[bool, str]:
        '''
            Send email using Outlook:
                - mail_from (str): account used to send email
                - mail_to (str): reciepent(s)' email address
                - mail_cc (str): reciepent(s)' email address for CC
                - subject (str): email's subject
                - body (str): email's body
                - attachments (list): list of attachments
                - is_body_html: to convert plain text body to html format
        '''
        try:
            mail_item = self.ol.CreateItem(0)

            # Add mail item information
            used_account_address = self.default_account if (mail_from == None or mail_from == "") else self.namespace.Session.Accounts.Item(mail_from)
            mail_item._oleobj_.Invoke(*(64209, 0, 8, 0, used_account_address))
            if mail_item.SendUsingAccount == None or mail_item.SendUsingAccount.DisplayName == "":
                return False, f'Can not find {mail_from} or any default account'
            
            mail_item.To = mail_to
            mail_item.CC = mail_cc if (mail_cc != None and mail_cc != "") else ""
            mail_item.Subject = subject if (subject != None and subject != "") else ""

            if body != None and body != "":
                if is_body_html:
                    mail_item.HTMLBody = body
                else:
                    mail_item.Body =body
            else:
                body = ""
                            
            for attachment in attachments:
                mail_item.Attachments.Add(attachment)
            
            # Send mail
            mail_item.Send()
            
            return True, ""
        except Exception as e:
            error_message = f"Error sending email, due to:\n {e}"
            raise Exception(error_message)   

    def get_mail_messages(
                        self,
                        account_address: Optional[str] = None, 
                        folder_name: Optional[str] = "Inbox", 
                        max_mail_count: Optional[int] = 10,
                        filter: Optional[str] = None, 
                        unread_only: Optional[bool] = True,
                        sortby_receive_time: Optional[bool] = True
                        ) -> list:
        '''
            Retrieve list of mail messages
                - account_address: target email address that is used to retrieve mail messages
                - folder_name: name of target folder to retrieve mail messages
                - max_mail_count: maximum number of mail message to retrieve
                - filter: criteria to filder mail messages (Reference: https://learn.microsoft.com/en-us/office/vba/api/outlook.items.restrict?source=recommendations)
        '''
        try: 
            # Get folder
            if account_address == None or account_address == "": 
                used_account_address = self.default_account.DisplayName
            else:
                used_account_address = account_address

            folder = self.__get_folder(folder_name, account_address = used_account_address)

            # Retrieve messages
            combined_filter = ""
            if unread_only: 
                combined_filter += "[UnRead] = True"
            
            if filter != None and filter != "" and combined_filter != "":
                combined_filter += " AND " + filter
            elif filter != None and filter != "" and combined_filter == "":
                combined_filter = filter
            
            if combined_filter == "":
                messages = folder.Items 
            else:
                messages = folder.Items.Restrict(combined_filter)

            messages.Sort("[ReceivedTime]", sortby_receive_time)

            return list(messages)[:max_mail_count-1] if len(messages) >= max_mail_count else list(messages)
        except Exception as e:
            error_message = f'Error retrieving mail messages from {folder_name}, due to:\n {e}'
            raise Exception(error_message)

    def move_mail_message(
                        self, 
                        mail_item, 
                        dest_folder: str, 
                        folder_account: Optional[str] = None
                        ):
        '''
            Move mail message to target folder
                - mail_item: mail message item
                - dest_folder: target folder to move mail message to
                - folder_account: target account that stores target folder
        '''
        try:
            folder = self.__get_folder(dest_folder, account_address = folder_account)
            mail_item.Move(folder)
        except Exception as e:
            error_message = f'Error moving mail message to {dest_folder}, due to:\n {e}'
            raise Exception(error_message)