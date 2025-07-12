from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from functools import wraps


class GroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    group_required = 'Venditori'

    def test_func(self):
        return self.request.user.groups.filter(name=self.group_required).exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('accesso_negato')

class GroupRequiredCompratoreMixin(LoginRequiredMixin, UserPassesTestMixin):
    group_required = 'Compratori'

    def test_func(self):
        return self.request.user.groups.filter(name=self.group_required).exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('accesso_negato')

class AnonymousRequiredMixin:
    redirect_authenticated_user_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_user_url)
        return super().dispatch(request, *args, **kwargs)

def solo_compratori(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Devi essere loggato.")
        if request.user.groups.filter(name='Venditori').exists():
            raise PermissionDenied("Solo i compratori possono accedere.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view