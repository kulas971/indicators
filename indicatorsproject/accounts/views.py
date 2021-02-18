from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from .forms import AccountRegisterForm

class HomeView(TemplateView):
    template_name = 'home.html'

class HomeLoggedView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/logged_in.html'

class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'accounts/signup.html'

  form_class = AccountRegisterForm
  success_message = "Your profile was created successfully"

  def get_success_url(self):
        return reverse_lazy('accounts:login')

class LoginView(FormView):

    success_url = '/auth/home/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:home_logged')
        # redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        # if not is_safe_url(url=redirect_to, host=self.request.get_host()):
        #     redirect_to = self.success_url
        # return redirect_to


class LogoutView(RedirectView):

    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super().get(request, *args, **kwargs)
        # return super(LogoutView, self).get(request, *args, **kwargs)
