from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_status_mail(order_id,order_status,email):
    if order_status == 1:
        subject="Your order is confirmed"
        message = "order is confirmed"
    elif order_status ==2:
        subject = "order is proccessing"
        message=f"your order is being proccessed"
    else:
        subject = "order status changed"
        message = f"your order status changed"
    send_mail(subject,message,"from@gmail.com",[email])    