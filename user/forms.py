from django import forms
from django.core.exceptions import ValidationError

from user.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email Cannot be None')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User Not Found')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise  forms.ValidationError('Password Cannot be None')
        return password


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=True)  # Qo‘shildi
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)  # Qo‘shildi

    class Meta:
        model = User
        fields = ['email', 'username', 'password']  # confirm_password olib tashlandi

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already registered')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data




#
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["email", "password1", "password2"]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = user.email
#         if commit:
#             user.save()
#         return user
#
#
# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)  # Parolni yashirin ko‘rsatish
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if not email:
#             raise forms.ValidationError('Email Cannot be None')
#         if not User.objects.filter(email=email).exists():
#             raise forms.ValidationError('User not Found')
#         return email
#
#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if not password:
#             raise forms.ValidationError('Password Cannot be None')
#         return password