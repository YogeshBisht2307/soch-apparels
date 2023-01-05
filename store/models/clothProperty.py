from django.db import models

class clothProperty(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique= True)

    def __str__(self) -> str:
        return self.name

    class Meta :
        abstract = True # This class will not reflect into Table


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