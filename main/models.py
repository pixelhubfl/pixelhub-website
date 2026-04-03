from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    base_price = models.FloatField()
    is_custom_size = models.BooleanField(default=True)

    def __str__(self):
        return self.name