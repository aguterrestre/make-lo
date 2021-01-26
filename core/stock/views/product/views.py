from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError
from django.http import JsonResponse

from core.stock.forms import ProductForm
from core.stock.models import Product
from core.setting.models import Company


class ProductListView(LoginRequiredMixin, ListView):
    """
    Clase para ver en pantalla los productos de la empresa a manera de listado.
    """
    model = Product
    template_name = 'product/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Listado de Productos'
        context['company'] = Company.objects.get(pk=1)
        context['create_url'] = reverse_lazy('stock:product_create')
        context['list_url'] = reverse_lazy('stock:product_list')
        context['entity'] = 'Productos'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['btn_new_detail'] = 'Nuevo Producto'
        context['product_report_url'] = reverse_lazy('report:product_report', args=[0])
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Clase para crear un nuevo producto.
    """
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('stock:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Creación de Producto'
        context['company'] = Company.objects.get(pk=1)
        # context['create_url'] = reverse_lazy('erp:client_create')
        context['entity'] = 'Producto'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Clase para modificar un producto.
    """
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('stock:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Edición de Producto'
        context['company'] = Company.objects.get(pk=1)
        # context['create_url'] = reverse_lazy('erp:client_create')
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'edit'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Clase para eliminar un producto.
    """
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('stock:product_list')

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
            data['error'] = 'No puede borrar el producto ya que tiene ventas realizadas.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Eliminación de Producto'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'del'
        context['detail'] = 'el producto'
        return context
