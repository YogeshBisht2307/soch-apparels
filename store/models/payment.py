from django.db import models
from django.contrib.auth.models import User
from store.models.order import Order

class Payment(models.Model):
    date = models.DateTimeField(null = False, auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=25 ,default = 'FAILED')
    payment_id = models.CharField(max_length=100)
    payment_request_id = models.CharField(unique= True,null = False, max_length=50)

    def __str__(self):
        return self.order.user.username