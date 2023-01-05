from django.db import models
from django.contrib.auth.models import User
from store.models.size import Size_Variant

class Cart(models.Model):
    sizeVariant = models.ForeignKey(Size_Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
