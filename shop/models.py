from django.db import models
from django.urls import reverse
from django.utils.timezone import timedelta
from mptt.models import MPTTModel, TreeForeignKey
from flatepages.models import slug_generator
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import post_save


class Sliders(models.Model):
    image = models.ImageField(upload_to='slider_images/', verbose_name='Նկար')
    context = RichTextUploadingField(verbose_name='Նկարագրություն')
    url = models.URLField(verbose_name='Հղում')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Սլայդեր'
        verbose_name_plural = 'Սլայդեր'


class SpecialOffer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Անուն')
    url = models.URLField(verbose_name='Հղում')
    image = models.FileField(upload_to='offer_images/', verbose_name='Նկար')
    description = RichTextUploadingField(blank=True, verbose_name='Նկարագրություն')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Հատուկ առաջարկ'
        verbose_name_plural = 'Հատուկ առաջարկ'


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Անուն')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Հղում')
    icon = models.FileField(upload_to='category_images/')
    image = models.FileField(upload_to='category_images/')
    meta_title = models.CharField(max_length=200,blank=True, verbose_name='Մետա անուն')
    meta_description = models.TextField(max_length=300,blank=True, verbose_name='Մետա նկարագրություն')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):

        latest_cat = 0
        if Category.objects.all().count() > 0:
            latest_cat = Category.objects.all().order_by('-id').first().id + 1
        else:
            latest_cat += 1

        if not self.slug:
            self.slug = slug_generator(self.name , str(latest_cat))

        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse('category-details', kwargs={'slug': self.slug})

    def __str__(self):
        if Category.objects.all().count() > 0:
            title = [self.name]
            k = self.parent
            while k is not None:
                title.append(k.name)
                k = k.parent
            return f" --> ".join(title[::-1])
        else:
            return 'Category does not exist'

    class Meta:
        verbose_name = 'Բաժիններ'
        verbose_name_plural = 'Բաժիններ'




class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name='Անուն')
    icon = models.FileField(upload_to='brand_icons/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Բրենդ'
        verbose_name_plural = 'Բրենդ'


class Color(models.Model):
    name = models.CharField(max_length=150, verbose_name='Անուն')
    code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Գույն'
        verbose_name_plural = 'Գույն'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Անուն')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Հղում')
    manufactured = models.CharField(max_length=150, verbose_name='Արտադրող', blank=True)
    country = models.CharField(max_length=150, verbose_name='Արտադրող երկիր', blank=True)
    volume = models.CharField(max_length=150, blank=True, verbose_name='Ծավալ')
    weight = models.CharField(max_length=150, blank=True, verbose_name='Քաշ')
    power = models.CharField(max_length=150, blank=True, verbose_name='Հզորություն')
    sort = models.CharField(max_length=150, blank=True, verbose_name='Տեսակ')
    qty_in_coll = models.CharField(max_length=50, blank=True, verbose_name='Քանակը հավաքածուում')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0, blank=True, verbose_name='Դիտումների քանակ')
    meta_title = models.CharField(max_length=200, blank=True,verbose_name='Մետա անուն')
    meta_description = models.TextField(blank=True,verbose_name='Մետա նկարագրություն')
    # is_popular = models.BooleanField(default=False,verbose_name='Հայտնի ապրանք')

    def get_absolute_url(self):
        return reverse("product-details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def published_timedelta(self):
        return self.created > self.created - timedelta(days=15)

    def variants_sale(self):
        if self.productvariants_set.count():
            return bool(self.productvariants_set.filter(models.Q(sale__isnull=False) | ~models.Q(sale=0)).count() > 0)
        return False

    class Meta:
        verbose_name = 'Ապրանք'
        verbose_name_plural = 'Ապրանք'





class ProductVariants(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Գույն')
    size = models.CharField(max_length=150, verbose_name='Չափս')
    product_code = models.CharField(max_length=15, verbose_name='Ապրանքի կոդ')
    price = models.IntegerField(default=0, verbose_name='Գին')
    sale = models.IntegerField(default=0, verbose_name='Զեղչված գին')
    description = RichTextUploadingField(blank=True, null=True)
    filter_price = models.IntegerField(blank=True,null=True)

    def __str__(self):
        col = self.color.name if self.color is not None else ''
        size = self.size if self.size is not None else ''
        name = self.product.name

        return name + ' / ' + col + ' / ' + size

    def save(self,*args,**kwargs):
        if self.sale > 0 :
            self.filter_price = self.sale
        else:
            self.filter_price = self.price

        return super().save(*args,**kwargs)

    def get_prices(self):
        if self.sale:
            return self.sale
        else:
            return self.price


def slug_post_save(sender, instance, *args, **kwargs):
    product = instance

    if not product.slug:
        product.slug = slug_generator(product.name, product.id)
        product.save()

    try:
        variants = ProductVariants.objects.filter(product=product)
        for variant in variants:
            variant.save()
    except:
        pass


post_save.connect(slug_post_save, sender=Product)


class ProductVariantImages(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    variant = models.ForeignKey(ProductVariants,
                                on_delete=models.CASCADE,

                                null=True)
    image = models.FileField(upload_to='product_images/')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Ապրանքների նկարներ'
        verbose_name_plural = 'Ապրանքների նկարներ'
