from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_status_mail

@receiver(pre_save,sender=Order)
def order_status_change(sender,instance, **kwargs):
    print("Signal triggered")  # Debugging line
    print("instance",instance.id)
    if instance.id:
        old_order = Order.objects.get(id=instance.id)
        print(instance)
        if old_order.order_status != instance.order_status:
            send_order_status_mail.delay(instance.id,instance.order_status,instance.owner.user.email)
