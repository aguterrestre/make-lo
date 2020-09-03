from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from core.sale.forms import ClientForm
from core.sale.models import Client
from core.setting.models import Company


class ClientListView(LoginRequiredMixin, ListView):
    """
    Clase para ver en pantalla los clientes de la empresa a manera de listado.
    """
    model = Client
    template_name = 'client/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Listado de Clientes'
        context['company'] = Company.objects.get(pk=1)
        context['create_url'] = reverse_lazy('sale:client_create')
        context['list_url'] = reverse_lazy('sale:client_list')
        context['entity'] = 'Clientes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['btn_new_detail'] = 'Nuevo Cliente'
        context['client_report_url'] = reverse_lazy('report:client_report')
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Clase para crear un nuevo cliente.
    """
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('sale:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Creación de Cliente'
        context['company'] = Company.objects.get(pk=1)
        # context['create_url'] = reverse_lazy('erp:client_create')
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Clase para modificar un cliente.
    """
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('sale:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Edición de Cliente'
        context['company'] = Company.objects.get(pk=1)
        # context['create_url'] = reverse_lazy('erp:client_create')
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'edit'
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Clase para eliminar un cliente.
    """
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('sale:client_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except ProtectedError:
            # data['error'] = str(e)
            data['error'] = 'No puede borrar el cliente ya que tiene ventas realizadas.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Eliminación de Cliente'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'del'
        context['detail'] = 'el cliente'
        return context
