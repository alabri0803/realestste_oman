from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404, request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, get_language
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
    CompanyDocumentForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    LoginForm,
    UserProfileForm,
)
from .models import CompanyDocument, CustomUser, UserProfile


class BaseRTLView:
    """
    كلاس أساسي لإعدادات والترجمة
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rtl'] = True
        context['lang'] = 'ar'
        context['dir'] = 'rtl'
        context['page_title'] = getattr(self, 'page_title', _('نظام الإيجارات'))
        return context


def toggle_rtl(request):
    """
    دالة لتبديل وضع RTL/LTR وحفظه في الجلسة
    """
    if 'rtl_mode' not in request.session:
        request.session['rtl_mode'] = True if get_language() == 'ar' else False

    request.session['rtl_mode'] = not request.session['rtl_mode']
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


class CustomLoginView(BaseRTLView, View):
    """
    واجهة تسجيل الدخول مع دعم الترجمة
    """
    template_name = 'accounts/login.html'
    page_title = _('تسجيل الدخول')

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {
            'form': form,
            **self.get_context_data()
        })

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(self.get_redirect_url(user))
        return render(request, self.template_name, {
            'form': form,
            **self.get_context_data()
        })

    def get_redirect_url(self, user):
        if user.user_type == 'owner':
            return reverse_lazy('accounts:owner_dashboard')
        elif user.user_type == 'investor':
            return reverse_lazy('accounts:investor_dashboard')
        return reverse_lazy('accounts:company_dashboard')


class ProfileUpdateView(LoginRequiredMixin, BaseRTLView, UpdateView):
    """
    واجهة تحديث الملف الشخصي مع دعم ثنائي اللغة
    """
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    page_title = _('الملف الشخصي')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        return CustomUserChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'profile'):
            context['profile_form'] = UserProfileForm(instance=self.request.user.profile)
        context['documents'] = CompanyDocument.objects.filter(user=self.request.user)[:3]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = UserProfileForm(request.POST, request.FILES, 
                                    instance=self.request.user.profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)