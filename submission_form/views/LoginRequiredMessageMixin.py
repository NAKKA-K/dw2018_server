# django module
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# app module

# lib


class LoginRequiredMessageMixin(LoginRequiredMixin):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'このページにアクセスするにはログインが必要です')

    return super().dispatch(request, *args, **kwargs)
