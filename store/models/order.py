from django.db import models
from django.contrib.auth.models import User
from store.models.cloth import Cloth
from store.models.size import Size_Variant


class Order(models.Model):
    orderStatus = (
        ('PENDING', "Pending"),
        ('PLACED', "Placed"),
        ('CANCELED', "Canceled"),
        ('COMPLETE', "Completed"),
    )
    method = (
        ('COD', "COD"),
        ('ONLINE', "Online")
    )

    order_status = models.CharField(max_length=25, choices=orderStatus)
    payment_method = models.CharField(max_length=50, choices=method)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(null=False, max_length=255)
    phone = models.CharField(null=False, max_length=10)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    size = models.ForeignKey(Size_Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return self.order.user.username
