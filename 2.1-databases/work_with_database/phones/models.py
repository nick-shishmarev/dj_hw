from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=150)
    release_date = models.DateField()
    lte_exists = models.BooleanField(False)
    slug = models.SlugField(max_length=50)
