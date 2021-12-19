# from cart.models import City, State
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    #
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    # state = models.ForeignKey(State,on_delete=models.SET_NULL,null=True,blank=True)
    # city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.user.email


def post_save_profile(sender,created,instance,*args,**kwargs):

    if created:
        Profile.objects.create(user=instance)

post_save.connect(post_save_profile,sender=User)