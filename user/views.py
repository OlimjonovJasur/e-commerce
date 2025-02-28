from http.client import HTTPResponse

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from user.forms import LoginForm, RegisterForm
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from user.custom_token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

from user.models import User


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('ecommerce:index')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid login')

    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('ecommerce:index')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()

            email = user.email

            if email:
                current_site = get_current_site(request)
                subject = 'Verify Email'
                message = render_to_string('user/email-verification/verify_email_message.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                try:
                    email_message = EmailMessage(subject, message, to=[email])
                    email_message.content_subtype = 'html'
                    email_message.send()
                    print("✅ Email muvaffaqiyatli yuborildi")
                except Exception as e:
                    print(f"❌ Email yuborishda xatolik: {e}")

            data = "Ro'yxatdan o'tish muvaffaqiyatli🎯🎯🎯"
            return HttpResponse(f'<h2>{data}</h2>')

        else:
            print(form.errors)

    return render(request, 'user/register.html', {"form": form})


# def register_page(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password'))
#             get_name_by_email = user.username if user.username else user.email.split('@')[0]
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             user = request.user
#             email = request.user.email
#
#
#             subject = 'Verify Email'
#             message = render_to_string('user/email-verification/verify_email_message.html',{
#                 'request': request,
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#
#             email = EmailMessage(
#                 subject, message, to=[email]
#             )
#             email.content_subtype = 'html'
#             email.send()
#
#
#             # send_mail(
#             #     f'{get_name_by_email}, Muvaffaqiyatli ro‘yxatdan o‘tdingiz!',
#             #     'Tabriklaymiz! Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz.',
#             #     settings.DEFAULT_FROM_EMAIL,  # settings import qilingan
#             #     [user.email],
#             #     fail_silently=False
#             # )
#
#             # return redirect('ecommerce:index')
#             data = "Ro'yxatdan o'tish muvaffaqiyatli🎯🎯🎯"
#             return HttpResponse(f'<h2>{data}</h2>')
#         else:
#             print(form.errors)  # Xatolarni konsolga chiqarish
#
#     return render(request, 'user/register.html', {"form": form})

# class BaseRegisterView(FormView):
#     template_name = 'user/register.html'
#     form_class = RegisterForm
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         get_name_by_email = user.email.split('@')[0]
#         user.is_staff = True
#         user.is_superuser = True
#         user.set_password(form.cleaned_data['password'])
#         user.save()
#
#         send_mail(
#             subject=f'{get_name_by_email}',
#             message='You successfully registered',
#             from_email=DEFAULT_FROM_EMAIL,
#             recipient_list=[user.email],
#             fail_silently=False
#         )
#
#         return redirect('ecommerce:index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('user:verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'user/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user/email-verification/verify_email_complete.html')