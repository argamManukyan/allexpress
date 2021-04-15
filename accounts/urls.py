from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutVIew.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('activate/<uid64>/<token>/',ActivationEmail.as_view(),name='activate'),
    path('password-reset/',ForgotPassword.as_view(),name='password-reset'),
    path('password-reset-confirm/<uid64>/<token>/',ForgotPasswordConfirm.as_view(),name='password-reset-confirm'),
    path('password-change/',PasswordChangeView.as_view(),name='password-change'),
    path('profile/',UserProfileVIew.as_view(),name='profile')
]
