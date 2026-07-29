from order import Order
from emailGridService import EmailGridService
from emailService import EmailService
from emailGridServiceAdapter import emailGridServiceAdapter
email = EmailService()
new_email_service = EmailGridService()
emailAdapter = emailGridServiceAdapter(new_email_service)
amazon_order = Order(email_service=emailAdapter)

amazon_order.accept_order_receipt('ekagra',111)
