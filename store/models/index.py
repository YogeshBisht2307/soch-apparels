from django.db import models

class WebsiteDetail(models.Model):
    website_name = models.CharField(max_length=50)
    website_logo = models.ImageField(upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    website_description = models.CharField(max_length=250)
    favicon_icon = models.ImageField(upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    hero_image = models.ImageField(upload_to="media/images/", height_field=None, width_field=None,
    max_length=None)
    hero_headline = models.CharField(max_length=200)
    offer_headine = models.CharField(max_length=50)
    offer_image = models.ImageField(upload_to="media/images/", height_field=None, width_field=None, max_length=None)
    offer_text = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    email_1 = models.EmailField(max_length=254)
    email_2 = models.EmailField(max_length=254)
    mobile_1 = models.CharField(max_length=10)
    mobile_2 = models.CharField(max_length=10)
    city = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.website_name

