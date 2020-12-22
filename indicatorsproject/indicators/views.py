import requests as rq

from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import UploadFileForm

class UploadView(LoginRequiredMixin, FormView):

    form_class = UploadFileForm
    template_name = "indicators/upload.html"

    def get_success_url(self):
        file = self.request.FILES['file'].read()
        client = rq.session()
        client.get('https://e-sprawozdania.biz.pl/show/?lang=pl')
        csrftoken = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken':csrftoken}

        response = client.post('https://e-sprawozdania.biz.pl/show/',
            files={'document':file}, data=payload)

        source = response.content.decode()

        return reverse_lazy('indicators:upload')

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        return context
