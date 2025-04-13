from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True, label='البريد الإلكتروني')
  phone = forms.CharField(max_length=20, label='رقم الهاتف')

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'phone']

class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ['phone', 'role']

class LoginForm(forms.Form):
  username = forms.CharField(label='اسم المستخدم')
  password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)