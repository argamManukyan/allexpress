from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.views import View
from django.utils.translation import ugettext_lazy as _
from .email import SendMail
from .forms import *


class LoginView(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, 'accounts/login.html')

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            try:
                is_user = User.objects.get(email=email)
            except:
                messages.error(request, _('Այս էլ․հասցեով օգտատեր գոյություն չունի։ '))
                return redirect('login')

            user = authenticate(email=email, password=password)

            if user is None:
                messages.error(request, _('Սխալ մուտքանուն կամ գաղտնաբառ'))
                return redirect('login')

            if not remember_me:
                request.session.set_expiry(0)

            login(request, user)

            if not 'next' in request.get_full_path():
                return redirect('home')
            return HttpResponseRedirect(request.GET.get('next'))


class RegisterView(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, 'accounts/register.html')

    def post(self, request):

        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            
            if len(name.split(' ')) == 2:
                f_n = name.split(' ')[0]
                l_n = name.split(' ')[1]
            else:
                f_n = name.split(' ')[0]

            if User.objects.filter(phone=phone).exists():
                messages.error(request, _('Այս հեռախոսահամարով օգտատեր արդեն գոյություն ունի։ '))
                return redirect('register')

            instance = form.save()
            instance.is_active = False
            instance.first_name = f_n
            instance.username = f_n + str(instance.id)
            instance.save()
            data = {'user': instance, 'request': request}
            SendMail.send_activation_message(data)

            return redirect('faq')
        else:

            if form.errors.get('email'):
                messages.error(request, _('Այս էլ․ հասցեով օգտատեր արդեն գոյություն ունի։ '))
                return redirect('register')
            return redirect('register')


class ActivationEmail(View):

    def get(self, request, **kwargs):

        if request.user.is_authenticated:
            return redirect('profile')

        try:
            _kw_uid = kwargs.get('uid64')
            _kw_token = kwargs.get('token')
            user_id = force_text(urlsafe_base64_decode(_kw_uid))
            user = User.objects.get(id=user_id)

            if user.is_active:
                return HttpResponse(_('Հղումն արդեն օգտագործվել է: '))

            if PasswordResetTokenGenerator().check_token(user=user, token=_kw_token):
                user.is_active = True
                user.save(force_update=True)
            else:
                user.delete()
                return HttpResponse(_('Տվյալների մշակման սխալ։ Փորձեք նորից գրանցվել։ '))

            request.session
        except User.DoesNotExist:
            return HttpResponse(_("Տվյալների անհամապատասխանություն։ Օգտատերը չի գտնվել։ "))

        messages.success(request, _('Շնորհակալություն։ Տվյալները հաջողությամբ հաստատված են։ '))

        data = {}
        data['request'] = request
        data['type'] = 'activation'
        data['email'] = user.email

        SendMail.send_confirmation_message(data)
        return redirect('faq')


class ForgotPassword(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, 'accounts/password-reset.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            data = {}
            data['request'] = request
            data['user'] = user
            SendMail.send_password_reset_mail(data)
        except User.DoesNotExist:
            messages.error(request, _('Էլ-փոստը չի գտնվել: '))
            return redirect('password-reset')

        messages.success(request, _('<b>Գաղտաբառի վերականգնման նամակն ուղարկվել է:</b><br>Ձեր \
                                    էլ. փոստին ուղարկվել են գաղտնաբառի վերականգնման կարգավորումները: Դուք շուտով \
                                    կստանաք այն: Եթե Դուք չեք ստացել էլ. նամակ, խնդրում ենք համոզվել, որ \
                                    մուտքագրել եք հենց այն էլ. հասցեն, որն օգտագործել եք մեր կայքում գրանցվելու \
                                    համար:<br>Խնդրում ենք ստուգել նաև «սպամ» թղթապանակը։ '))

        return redirect('password-reset')


class ForgotPasswordConfirm(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')

        _token = kwargs.get('token')
        _uid = kwargs.get('uid64')

        session_token = request.session.get('password_reset_token')
        user_id = urlsafe_base64_decode(_uid).decode()

        try:
            self.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(_('Օգտատերը չի գտնվել։ Ստուգեք հղման ճշտությունը։ '))

        valid_link = False
        if not PasswordResetTokenGenerator().check_token(user=self.user, token=_token) \
                or not session_token:
            messages.error(request, _("Հղման սխալ։ Ստուգեք հղման ճշտությունը։ "))
            return redirect('password-reset')

        if PasswordResetTokenGenerator().check_token(user=self.user, token=_token) \
                and session_token == _token:
            valid_link = True
        return render(request, 'accounts/password-reset-confirm.html')

    def post(self, request, **kwargs):

        form = ResetPasswordForm(request.POST or None)
        _uid = kwargs.get('uid64')
        user_id = urlsafe_base64_decode(_uid).decode()

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(_('Օգտատերը չի գտնվել։ Ստուգեք հղման ճշտությունը։ '))

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            del request.session['password_reset_token']
            messages.success(request, _("Գաղտնաբառը հաջողությամբ թարմացվել է։ "))
            return redirect('login')


class UserProfileVIew(LoginRequiredMixin, View):
    redirect_field_name = 'next'
    login_url = settings.LOGIN_URL

    def get(self, request, **kwargs):

        return render(request, 'accounts/user-profile.html')

    def post(self, request):
        form = UserProfileUpdateForm(request.POST or None, instance=request.user)

        
        if form.is_valid():
            spl_name = request.POST.get('name').split(' ')
            profile = form.save(commit=False)
            profile.first_name = spl_name[0]
            profile.last_name = spl_name[1] if len(spl_name) > 1 else ''
            messages.success(request, _('Ձեր տվյալները հաջողությամբ թարմացվել են։ '))
            profile.save(force_update=True)

        return redirect('profile')


class PasswordChangeView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):

        return render(request, 'accounts/user-profile.html')

    def post(self, request):

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        try:
            request.user.check_password(old_password)
        except:
            messages.error(request, _('Հին գաղտնաբառը սխալ է մուտքագրված։ '))
            return redirect('profile')

        request.user.set_password(new_password)
        user = request.user.save()
        login(request, user)
        messages.success(request, _('Գաղտնաբառը հաջողությամբ թարմացվել է։ '))

        return redirect('profile')


class LogoutVIew(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('home')
