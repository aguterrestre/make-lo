from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from core.purchase.forms import ProviderForm
from core.purchase.models import Provider
from core.setting.models import Company


class ProviderListView(LoginRequiredMixin, ListView):
    """
    Clase para ver en pantalla los proveedores de la empresa a manera de listado.
    """
    model = Provider
    template_name = 'provider/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Listado de Proveedores'
        context['company'] = Company.objects.get(pk=1)
        context['create_url'] = reverse_lazy('purchase:provider_create')
        context['list_url'] = reverse_lazy('purchase:provider_list')
        context['entity'] = 'Proveedores'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['btn_new_detail'] = 'Nuevo Proveedor'
        context['provider_report_url'] = reverse_lazy('report:provider_report')
        return context


class ProviderCreateView(LoginRequiredMixin, CreateView):
    """
    Clase para crear un nuevo proveedor.
    """
    model = Provider
    form_class = ProviderForm
    template_name = 'provider/create.html'
    success_url = reverse_lazy('purchase:provider_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Creación de Proveedor'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        return context


class ProviderUpdateView(LoginRequiredMixin, UpdateView):
    """
    Clase para modificar un proveedor.
    """
    model = Provider
    form_class = ProviderForm
    template_name = 'provider/create.html'
    success_url = reverse_lazy('purchase:provider_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Edición de Proveedor'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'edit'
        return context


class ProviderDeleteView(LoginRequiredMixin, DeleteView):
    """
    Clase para eliminar un proveedor.
    """
    model = Provider
    template_name = 'provider/delete.html'
    success_url = reverse_lazy('purchase:provider_list')

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
            data['error'] = 'No puede borrar el proveedor ya que tiene compras realizadas.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Eliminación de Proveedor'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'del'
        context['detail'] = 'el proveedor'
        return context
