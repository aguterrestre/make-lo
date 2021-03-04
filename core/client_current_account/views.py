from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy

from django_filters.views import FilterView
from .filters import ClientCurrentAccountFilter

from .models import ClientCurrentAccount
from core.sale.models import Client
from core.setting.models import Company


class ClientCurrentAccountListView(LoginRequiredMixin, FilterView):
    """
    Vista para listado de comprobantes de ventas en cuenta corriente de cliente.
    Se usan filtros a través de la librería django_filter.
    """
    model = ClientCurrentAccount
    template_name = 'client_current_account/list.html'
    filterset_class = ClientCurrentAccountFilter

    def get_queryset(self):
        filter = self.request.GET.get('ticket__client')
        if filter is None or filter == '':
            # Si no ingresa cliente no realiza el filtro
            return ClientCurrentAccount.objects.none()

        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = self.request.POST['action']
            if action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                            Q(name__icontains=term) | Q(surname__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Cuenta Corriente de Cliente'
        context['company'] = Company.objects.get(pk=1)
        context['list_url'] = reverse_lazy('client_current_account:client_current_account_list')
        context['entity'] = 'Cuenta Corriente Cliente'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['create_url'] = reverse_lazy('sale:client_create')
        context['btn_new_detail'] = 'Nuevo Recibo'
        return context
