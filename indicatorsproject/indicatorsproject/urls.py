from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url = '/indicators/upload/')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('indicators/', include('indicators.urls', namespace='indicators')),

]
