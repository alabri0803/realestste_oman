import os

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import CompanyDocument, CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        send_welcome_email(instance)

def send_welcome_email(user):
    subject = _('مرحباً بك في نظام إدارة الإيجارات')
    if user.user_type == 'owner':
        message = _('مرحباً بك في نظام إدارة الإيجارات. يمكنك الآن إضافة عقاراتك وتتبع الإيجارات.')
    elif user.user_type == 'investor':
        message = _('مرحباً بك في نظام إدارة الإيجارات. يمكنك الآن إضافة استثماراتك وتتبع الأرباح.')
    else:
        message = _('مرحباً بك في نظام إدارة الإيجارات. يمكنك الآن إضافة شركاتك وتتبع الإيجارات.')
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

@receiver(post_save, sender=CompanyDocument)
def validate_company_documents(sender, instance, **kwargs):
    if instance.user.user_type == 'owner':
        validate_owner_document(instance)
    elif instance.user.user_type == 'investor':
        validate_investor_document(instance)
    elif instance.user.user_type == 'tenant':
        validate_tenant_document(instance)

def validate_owner_document(document):
    allowed_types = ['commercial_license', 'ownership_deed']
    if document.document_type not in allowed_types:
        raise ValidationError(_('نوع الوثيقة غير مسموح به للمالك.'))

def validate_investor_document(document):
    allowed_types = ['commercial_license', 'investment_agreement']
    if document.document_type not in allowed_types:
        raise ValidationError(_('نوع الوثيقة غير مسموح به للمستثمر.'))

def validate_tenant_document(document):
    allowed_types = ['commercial_license', 'rental_agreement']
    if document.document_type not in allowed_types:
        raise ValidationError(_('نوع الوثيقة غير مسموح به للشركة المستأجرة.'))

@receiver(post_delete, sender=CompanyDocument)
def delete_document_file(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

@receiver(post_save, sender=CompanyDocument)
def notify_document_update(sender, instance, created, **kwargs):
    if created:
        subject = _('تم إضافة وثيقة جديدة')
        message = _('تم رفع وثيقة جديدة من نوع {document_type} من قبل {user_name}. نوع المستخدم: {user_type} تاريخ الانتهاء: {expiry_date}').format(
            document_type=instance.get_document_type_display(),
            user_name=instance.user.arabic_name,
            user_type=instance.user.get_user_type_display(),
            expiry_date=instance.expiry_date or _('غير محدد')
        )
        admin_emails = [admin[1] for admin in settings.ADMINS]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails, fail_silently=True)