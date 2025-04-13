from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


def user_login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('home')
  else:
    form = AuthenticationForm()
  return render(request, 'accounts/login.html', {'form': form})

def user_register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    form = UserRegistrationForm()
  return render(request, 'accounts/register.html', {'form': form})

def user_logout(request):
  logout(request)
  return redirect('login')

def user_profile(request):
  return render(request, 'accounts/profile.html')

def change_password(request):
  return render(request, 'accounts/change_password.html')