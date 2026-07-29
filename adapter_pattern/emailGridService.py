class EmailGridService:
    def send_email(self,sender:str,receiver:str,encoded_msg:str):
        print('Sending mail with EmailGridService')
        print(f'Sender is {sender}')
        print(f'Receiver is {receiver}')
        print(f'Encoded Message is {encoded_msg}')