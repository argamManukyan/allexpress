from django.db import models
from shop.models import ProductVariants


class WishItem(models.Model):
    product = models.ForeignKey(ProductVariants,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.product.product.name)

class Wish(models.Model):

    items = models.ManyToManyField(WishItem)

    def __str__(self):
        return str(self.pk)