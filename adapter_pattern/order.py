from NotificationInterface import NotificationInterface
class Order:
    def __init__(self,email_service:'NotificationInterface'):
        self.__email_service=email_service
    def accept_order_receipt(self,customer:str,oderderId:int):
        message:str = f'Order request of orderId:{oderderId} received'
        self.__email_service.send('amazon.com',customer,message)

    