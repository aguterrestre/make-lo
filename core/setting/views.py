from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from core.setting.forms import CompanyForm
from core.setting.models import Company


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """
    Clase para modificar datos de la empresa.
    """
    model = Company
    form_class = CompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('login:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Edición de Empresa'
        context['company'] = Company.objects.get(pk=1)
        # context['create_url'] = reverse_lazy('erp:client_create')
        context['entity'] = 'Empresa'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'edit'
        return context
