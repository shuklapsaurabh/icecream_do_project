from celery import shared_task
from .models import Order
import time, random

@shared_task
def process_payment(order_id):
    order = Order.objects.get(id=order_id)
    time.sleep(random.randint(10, 60))
    order.status = random.choice(['paid', 'failed'])
    order.save()