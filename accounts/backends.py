from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None or password is None:
            return None

        try:
            # حاول المصادقة باستخدام البريد الإلكتروني أولاً
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            try:
                # إذا فشل، حاول المصادقة باستخدام رقم الهاتف
                user = UserModel.objects.get(phone__iexact=username)
            except UserModel.DoesNotExist:
                # إذا لم يتم العثور على المستخدم
                return None
            except UserModel.MultipleObjectsReturned:
                # في حالة وجود أرقام هواتف مكررة (غير مرجح إذا كان الحقل unique)
                return None
        except UserModel.MultipleObjectsReturned:
            # في حالة وجود بريد إلكتروني مكرر (غير مرجح إذا كان الحقل unique)
            return None

        # تحقق من كلمة المرور وحالة الحساب
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def user_can_authenticate(self, user):
        """
        تأكد من أن المستخدم مسموح له بتسجيل الدخول
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None