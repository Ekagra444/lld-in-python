from NotificationInterface import NotificationInterface
from emailGridService import EmailGridService
class emailGridServiceAdapter(NotificationInterface):
    def __init__(self,email_service:EmailGridService):
        self.__email_service = email_service
    def send(self,sender:str,to:str,msg:str):
        self.__email_service.send_email(sender,to,msg)
        