from django.db import models
from store.models.cloth import Cloth
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=355, null=False)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, auto_now_add=True)
