from enum import Enum
from typing import List, Optional, Tuple
from azure.servicebus import (
    ServiceBusClient, 
    ServiceBusMessage, 
    ServiceBusReceivedMessage, 
    ServiceBusReceiveMode, 
    ServiceBusReceiver,
    ServiceBusSender)

class SettleType(Enum):
    COMPLETE = "complete"
    ABANDON = "abandon"
    DEAD_LETTER = "dead letter"
    DEFER = "defer"

class AzureServiceBus:
    '''
        Azure Service Bus's actions:
        - Provide connection string in order to authenticate
        - Send, receive and settle queue messages
    '''
    def __init__(self, connection_string: str) -> ServiceBusClient:
        self.connection_string = connection_string

    def __auth(self) -> ServiceBusClient:
        '''
            Create a service bus client, authenticated via a connection string to create ServiceBusSender and ServiceBusReceiver
        '''
        try:
            return ServiceBusClient.from_connection_string(conn_str=self.connection_string)
        except Exception as e:
            error_message = f"Couldn't connect to service bus"
            raise Exception(error_message)
    
    def send_messages_to_queue(
                            self, 
                            queue_name: str, 
                            queue_messages: list,
                            client: Optional[ServiceBusClient] = None,
                            sender: Optional[ServiceBusSender] = None
                            ) -> ServiceBusSender:
        '''
            Send (a) message(s) to a specific queue

            queue_name: name of target queue to send message to
            queue_messages: list of messages to send to queue
            client: Authenticated client
            sender: ServiceBusSender client to send message to queue

            Return: ServiceBusSender client
        '''
        try:
            if not client:
                client = self.__auth()
            with client:
                if not sender:
                    sender = client.get_queue_sender(queue_name)
                with sender:
                    list_message = []
                    for queue_message in queue_messages:
                        list_message.append(ServiceBusMessage(queue_message))
                    sender.send_messages(list_message)

                    print(f"Sent message to queue {queue_name} successfully!")
                    return sender
        except ValueError as val_err:
            raise ValueError(val_err)
        except Exception as e:
            error_message = f"Couldn't send message to queue {queue_name}. due to:\n {e}"
            raise Exception(error_message)
    
    def receive_queue_messages(
                            self, 
                            queue_name: str, 
                            number_of_messages: int = 1, 
                            timeout: float = 60,
                            receive_mode: str = ServiceBusReceiveMode.PEEK_LOCK.value,
                            client: Optional[ServiceBusClient] = None,
                            receiver: Optional[ServiceBusReceiver] = None
                            ) -> Tuple[List[ServiceBusReceivedMessage], ServiceBusReceiver]:
        '''
            Receive batch of messages from a specific queue

            queue_name: name of target queue to send message to
            number_of_messages: max number of messages to be retrieved in a batch
            timeout: maximum amount of time to wait for success retrieval of batch
            receive_mode: PEEK_LOCK or RECEIVE_AND_DELETE

            Return: List of messages and ServiceBusReceiver client to later settle queue message
        '''
        try:
            if not client:
                client = self.__auth()
            if not receiver:
                receiver = client.get_queue_receiver(queue_name, receive_mode=receive_mode)
            receive_messages = receiver.receive_messages(max_message_count=number_of_messages, max_wait_time=timeout)
            if receive_messages != None and len(receive_messages) > 0:
                print(f"Recevied {len(receive_messages)} message(s)!")
                return receive_messages, receiver
            else:
                print("Recevied no message!")
                return [], receiver
        except Exception as e:
            error_message = f"Couldn't receive message from queue {queue_name}. due to:\n {e}"
            raise Exception(error_message)

    def settle_queue_message(
                            self,
                            receiver: ServiceBusReceiver, 
                            queue_message: ServiceBusReceivedMessage,
                            settle_mode: str,
                            dead_letter_reason: Optional[str] = None,
                            dead_letter_desc: Optional[str] = None
                            ):
        '''
            Settle a queue message from a specific ServiceBusReceiver client
            
            receiver: ServiceBusReceiver client to settle a queue message
            queue_message: queue message to settle 
            settle_mode: settle mode in SettleType
        '''
        try:
            with receiver:
                match settle_mode.lower():
                    case SettleType.COMPLETE.value:
                        receiver.complete_message(queue_message)
                    case SettleType.ABANDON.value:
                        receiver.abandon_message(queue_message)
                    case SettleType.DEAD_LETTER.value:
                        receiver.dead_letter_message(
                            message = queue_message,
                            reason = dead_letter_reason,
                            error_description = dead_letter_desc)
                    case SettleType.DEFER.value:
                        receiver.defer_message(queue_message)
                
                print(f"Settled message successfully. Mode: {settle_mode}")
        except Exception as e:
            error_message = f"Couldn't settele queue message\nMode: {settle_mode}\nDue to:\n {e}"
            raise Exception(error_message)