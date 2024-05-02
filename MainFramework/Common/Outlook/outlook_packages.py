import win32com.client as client

class Outlook:
    def __init__(self, **kwargs) -> None:
        pass
    
    @staticmethod
    def SendMailMessage(mailTo: str, mailFrom: str = None, **kwargs):
        '''
            Send email using Outlook:
                mailFrom (str): account used to send email
                mailTo (str): reciepent(s)' email address
                mailCC (str): reciepent(s)' email address for CC
                subject (str): email's subject
                body (str): email's body
                attachments (list): list of attachments 
        '''
        try:
            ol = client.Dispatch("Outlook.Application")
            mail_item = ol.CreateItem(0)

            if mailFrom == None or mailFrom == "": mailFrom = ol.Session.Accounts[0]
            mail_item.To = mailTo
            mail_item.CC = kwargs["mailCC"] if ("mailCC" in kwargs and kwargs["mailCC"] != None) else ""
            mail_item.Subject = kwargs["subject"] if ("subject" in kwargs and kwargs["subject"] != None) else ""
            mail_item.Body = kwargs["body"] if ("body" in kwargs and kwargs["body"] != None) else ""
            
            for attachment in kwargs["attachments"]:
                mail_item.Attachments.Add(attachment)
            
            # Send mail
            mail_item.Send()
        except Exception as e:
            raise e       

    def GetMailMessages(
            account: str = None, 
            folder_name: str = "Inbox", 
            mail_count: int = 1,
            filter: str = None, 
            unread_only: bool = True,
            sortby_receive_time: bool = True
            ) -> list:
        try: 
            # Connect
            ol = client.Dispatch("Outlook.Application")
            namespace = ol.GetNamespace("MAPI")
            
            # Get folder
            if account == None or account == "": 
                account = ol.Session.Accounts[0]
            else:
                used_account = namespace.Accounts.Item(account)

            root_folder = namespace.Folders.Item(account.DeliveryStore.DisplayName)
            folder = root_folder.Folders(folder_name)

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

            return list(messages)[:mail_count] if len(messages) >= mail_count else list(messages)
        except Exception as e:
            raise e

    def DeleteMailMessage() -> bool:
        pass

    def MoveMailMessage() -> bool:
        pass
        
    def MarkAsReadUnread() -> bool:
        pass


if __name__ == "__main__":
    # test
    # Outlook.SendMailMessage("pqvinh2@cmcglobal.vn;pqvinh3@cmcglobal.vn", body="Test email", subject="Test subject", attachments=["C:\\Users\\ADMIN\\Pictures\\Screenshot 2020-10-05 030949.png"])
    messages = Outlook.GetMailMessages()
    for message in messages:
        print(message)