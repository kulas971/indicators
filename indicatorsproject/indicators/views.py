import requests

from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import UploadFileForm
from .htmlparse import create_brsf

class UploadView(LoginRequiredMixin, FormView):

    form_class = UploadFileForm
    template_name = "indicators/upload.html"

    def get_success_url(self):
        file = self.request.FILES['file'].read()
        client = requests.session()
        client.get('https://e-sprawozdania.biz.pl/show/?lang=pl')
        csrftoken = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken':csrftoken}

        response = client.post('https://e-sprawozdania.biz.pl/show/',
            files={'document':file}, data=payload)

        source = response.content.decode('utf-8', 'ignore')
        self.request.session['brsf'] = create_brsf(source)
        return reverse_lazy('indicators:upload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['brsf'] = self.request.session['brsf']
        except:
            pass
        return context
