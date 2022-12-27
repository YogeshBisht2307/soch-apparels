from django.db import models
from django.contrib.auth.models import User
from store.models import Category,Sub_Category,Color,Brand,Occasion


class Cloth(models.Model):
    cloth_slug = models.CharField(null=True, default="", unique= True, max_length=200)
    cloth_name = models.CharField(max_length=150)
    cloth_description = models.CharField(max_length=500)
    cloth_image = models.ImageField(upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    cloth_discount = models.IntegerField(default = 0)
    ocassion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cloth_name
