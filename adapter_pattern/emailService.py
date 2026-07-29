from NotificationInterface import NotificationInterface

class EmailService(NotificationInterface):
    def send(self,sender:str,to:str,msg:str):
        print('Sending mail with EmailService')
        print(f'Sender is {sender}')
        print(f'Receiver is {to}')
        print(f'Message is {msg}')

        