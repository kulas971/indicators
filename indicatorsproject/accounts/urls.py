from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(
    template_name='accounts/login.html'), name='login' ),
    path('', views.HomeView.as_view(), name='home'),
    path('logged/', views.HomeLoggedView.as_view(), name='home_logged'),

]
