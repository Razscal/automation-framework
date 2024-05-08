import win32com.client as client
from typing import List, Optional, Tuple

class Outlook:
    '''
        Automate Outlook tasks
    '''
    def __init__(self) -> tuple:
        self.ol, self.namespace, self.default_account = self.__GetOutlookConfig()
    
    @staticmethod
    def __GetOutlookConfig() -> tuple:
        '''
            Initialize connection to Outlook, return a tuple for Application object, namespace object, default account
        '''
        try:
            ol = client.Dispatch("Outlook.Application")
            namespace = ol.GetNamespace("MAPI")
            default_account = ol.Session.Accounts[0]
            return  ol, namespace, default_account
        except Exception as e:
            raise e
    
    def __GetFolder(
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
            raise e
    
    @staticmethod
    def DeleteMailMessage(mail_item):
        """
            Delete Email message
                -mail_item: email that exists in Outlook folder
        """
        try:
            mail_item.Delete()
        except Exception as e:
            error_message = f'Error deleteing mail message: {e}'
            raise Exception(error_message)
        
    @staticmethod    
    def MarkAsReadUnread(mail_item, mark_unread: bool):
        '''
            Mark mail message as read/unread:
                - mail_item: MailItem object
                - mark_unread: False=Mark as read, True=Mark as unread
        '''
        try:
            mail_item.UnRead = mark_unread
        except Exception as e:
            error_message = f'Error marking message as read/unread: {e}'
            raise Exception(error_message)

    def SendMailMessage(
                        self,
                        mailTo: str, 
                        mailFrom: Optional[str] = None, 
                        mailCC: Optional[str] = None,
                        subject: Optional[str] = None,
                        body: Optional[str] = None,
                        attachments: Optional[List[str]] = [],
                        isBodyHtml: Optional[str] = False
                        ) -> Tuple[bool, str]:
        '''
            Send email using Outlook:
                - mailFrom (str): account used to send email
                - mailTo (str): reciepent(s)' email address
                - mailCC (str): reciepent(s)' email address for CC
                - subject (str): email's subject
                - body (str): email's body
                - attachments (list): list of attachments
        '''
        try:
            mail_item = self.ol.CreateItem(0)

            # Add mail item information
            used_account_address = self.default_account if (mailFrom == None or mailFrom == "") else self.namespace.Session.Accounts.Item(mailFrom)
            mail_item._oleobj_.Invoke(*(64209, 0, 8, 0, used_account_address))
            if mail_item.SendUsingAccount == None or mail_item.SendUsingAccount.DisplayName == "":
                return False, f'Can not find {mailFrom} or any default account'
            
            mail_item.To = mailTo
            mail_item.CC = mailCC if (mailCC != None and mailCC != "") else ""
            mail_item.Subject = subject if (subject != None and subject != "") else ""

            if body != None and body != "":
                if isBodyHtml:
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
            error_message = f"Error sending email: {e}"
            raise Exception(error_message)   

    def GetMailMessages(
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

            folder = self.__GetFolder(folder_name, account_address = used_account_address)

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
            error_message = f'Error retrieving mail messages from {folder_name}: {e}'
            raise Exception(error_message)

    def MoveMailMessage(
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
            folder = self.__GetFolder(dest_folder, account_address = folder_account)
            mail_item.Move(folder)
        except Exception as e:
            error_message = f'Error moving mail message to {dest_folder}: {e}'
            raise Exception(error_message)