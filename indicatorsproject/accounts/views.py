from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import AccountRegisterForm

class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'accounts/signup.html'

  form_class = AccountRegisterForm
  success_message = "Your profile was created successfully"

  def get_success_url(self):
        return reverse_lazy('accounts:login')
