from django.db import models
from django.db.models.signals import post_save
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.safestring import mark_safe
from unidecode import unidecode
from django.utils.text import slugify


def slug_generator(name, id):
    if '-' in str(name):
        name = name.split('-')[0]
    new_slug = slugify(unidecode(name) +'-'+ str(id))
    return new_slug


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Հաճախակի տրվող հարցեր'
        verbose_name_plural = 'Հաճախակի տրվող հարցեր'


class AboutUs(models.Model):
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'About us'

    class Meta:
        verbose_name = 'Մեր մասին'
        verbose_name_plural = 'Մեր մասին'


class DeliveryAndPayment(models.Model):
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Առաքում և վճարում'

    class Meta:
        verbose_name = 'Առաքում և վճարում'
        verbose_name_plural = 'Առաքում և վճարում'


class ReturnProduct(models.Model):
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Ապրանքի վերադարձ'

    class Meta:
        verbose_name = 'Ապրանքի վերադարձ'
        verbose_name_plural = 'Ապրանքի վերադարձ'


class TermsAndConditions(models.Model):

    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Պայմաններ և Դրույթներ'

    class Meta:
        verbose_name = 'Պայմաններ և Դրույթներ'
        verbose_name_plural = 'Պայմաններ և Դրույթներ'

class PrivacyAndPolicy(models.Model):
    
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Գաղտնիության քաղաքականություն'

    class Meta:
        verbose_name = 'Գաղտնիության քաղաքականություն'
        verbose_name_plural = 'Գաղտնիության քաղաքականություն'


class HowOrder(models.Model):
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Ինչպես պատվիրել'

    class Meta:
        verbose_name = 'Ինչպես պատվիրել'
        verbose_name_plural = 'Ինչպես պատվիրել'


class Blog(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextUploadingField()
    short_description = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_images/')
    views_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200,blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-details',kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Բլոգ'
        verbose_name_plural = 'Բլոգ'


def slug_generator_blog(sender, instance, *args, **kwargs):
    post = instance
    if not post.slug:
        post.slug = slug_generator(post.title, post.id)
        post.save()


post_save.connect(slug_generator_blog, sender=Blog)
