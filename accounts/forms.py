from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from  django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    remember_me = forms.BooleanField(required=False)

class RegisterForm(UserCreationForm):
    name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name','last_name','name',
                  'phone','email','password1','password2']


class ResetPasswordForm(forms.Form):

    new_password1 = forms.CharField()
    new_password2 = forms.CharField()
    
class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','phone','address',]

  





        
       

    