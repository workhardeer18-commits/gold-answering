from django.db import models
from django.db.models import CharField


class ProductCategory(models.Model):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title
