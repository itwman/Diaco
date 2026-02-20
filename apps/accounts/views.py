"""
Diaco MES - Accounts Web Views
================================
ورود و خروج کاربران.
"""
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    """صفحه ورود با قالب Bootstrap RTL."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    """خروج و بازگشت به صفحه ورود."""
    next_page = '/accounts/login/'
