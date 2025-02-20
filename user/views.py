from django.contrib.auth import authenticate, login, logout
from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import FormView

from config.settings import DEFAULT_FROM_EMAIL
from user.forms import LoginForm, RegisterForm


# Create your views here.


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
            get_name_by_email = user.email.split('@')[0]
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)

            user.save()
            send_mail(
                f'{get_name_by_email}',
                'You successfully register',
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            # login(request, form)
            return redirect('ecommerce:index')
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context=context)


class BaseRegisterView(FormView):
    template_name = 'user/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        get_name_by_email = user.email.split('@')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user.password)
        user.save()

        send_mail(
            subject=f'{get_name_by_email}',
            message='You successfully registered',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return redirect('ecommerce:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
