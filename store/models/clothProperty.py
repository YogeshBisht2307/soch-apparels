from django.db import models
from django.contrib.auth.models import User

class clothProperty(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique= True)

    def __str__(self):
        return self.name

    class Meta :
        abstract = True # so that there will be no class for clothProperty class
class Occasion(clothProperty):
    pass

class Brand(clothProperty):
    pass

class Sub_Category(clothProperty):
    pass

class Category(clothProperty):
    pass

class Color(clothProperty):
    pass