from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm

class AccountRegisterForm(UserCreationForm):

  email = forms.EmailField()

  class Meta:
      model = Account
      fields = [
      'email',
      'username',
      'password1',
      'password2',
      ]
