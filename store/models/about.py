from django.db import models


class About(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    link = models.CharField(max_length=50)
    link_text = models.CharField(max_length=50)

    def __str__(self):
        return self.title

