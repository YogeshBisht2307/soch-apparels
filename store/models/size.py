from django.db import models
from django.contrib.auth.models import User
from store.models.cloth import Cloth


class Size_Variant(models.Model):
    SIZES = (
        ('S',"Small"),
        ('M',"Medium"),
        ('L',"Large"),
        ('XL', "Extra Large"),
        ('XXL', "Extra Extra Large"),
    )
    price = models.IntegerField(null = False)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE, default="")
    size = models.CharField(choices=SIZES, max_length=5)
