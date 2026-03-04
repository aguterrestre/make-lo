from decimal import Decimal

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError, F
from django.db import transaction
from django.http import JsonResponse

from core.stock.forms import ProductForm, BulkPriceUpdateForm
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


class BulkPriceUpdateView(LoginRequiredMixin, TemplateView):
    """
    Vista para actualización masiva de precios de productos.
    Filtros por categoría, unidad, stock y producto.
    Permite aplicar porcentaje o valor fijo sobre final_price.
    """
    template_name = 'product/bulk_price_update.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def _get_filtered_queryset(self, request):
        """Aplica filtros y retorna el queryset de productos."""
        search = Product.objects.all()
        product_id = request.POST.get('product', '')
        category_id = request.POST.get('category', '')
        unit_id = request.POST.get('unit', '')
        stock = request.POST.get('stock', '0')

        if product_id:
            search = search.filter(id=product_id)
        if category_id:
            search = search.filter(category_id=category_id)
        if unit_id:
            search = search.filter(unit_id=unit_id)
        if stock == '1':
            search = search.filter(stock__lte=0)
        elif stock == '2':
            search = search.filter(stock__gt=0)
        elif stock == '3':
            search = search.filter(stock__lte=3, stock__gt=0)

        return search

    def _calculate_new_price(self, current_price, update_type, update_value):
        """Calcula el nuevo precio según tipo y valor."""
        if not update_value:
            return current_price
        value = Decimal(str(update_value))
        if update_type == 'percentage':
            factor = Decimal('1') + (value / Decimal('100'))
            return (current_price * factor).quantize(Decimal('0.0001'))
        else:
            return (current_price + value).quantize(Decimal('0.0001'))

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'search_products':
                search = self._get_filtered_queryset(request)
                update_type = request.POST.get('update_type', 'percentage')
                update_value = request.POST.get('update_value', '')

                results = []
                for p in search:
                    item = p.toJSON()
                    item['final_price'] = str(p.final_price)
                    new_price = self._calculate_new_price(
                        p.final_price, update_type, update_value
                    )
                    item['new_price'] = str(max(Decimal('0'), new_price))
                    results.append(item)
                data = results

            elif action == 'search_product':
                data = []
                prod = Product.objects.filter(
                    name__icontains=request.POST.get('term', '')
                )[:10]
                for i in prod:
                    item = i.toJSON()
                    data.append(item)

            elif action == 'apply_update':
                product_ids = request.POST.getlist('product_ids[]', [])
                if not product_ids:
                    data['error'] = 'No se seleccionaron productos.'
                else:
                    update_type = request.POST.get('update_type', 'percentage')
                    update_value = request.POST.get('update_value', '')
                    if not update_value:
                        data['error'] = 'Debe ingresar un valor de actualización.'
                    else:
                        value = Decimal(str(update_value))
                        search = Product.objects.filter(id__in=product_ids)

                        with transaction.atomic():
                            if update_type == 'percentage':
                                factor = Decimal('1') + (value / Decimal('100'))
                                updated = search.update(
                                    final_price=F('final_price') * factor
                                )
                            else:
                                updated = search.update(
                                    final_price=F('final_price') + value
                                )

                        data['success'] = True
                        data['updated_count'] = updated
                        data['message'] = f'Se actualizaron {updated} productos correctamente.'
            else:
                data['error'] = 'Acción no válida.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Actualización masiva de precios'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Productos'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('stock:product_list')
        context['form'] = BulkPriceUpdateForm()
        context['btn_cancel_url'] = reverse_lazy('stock:product_list')
        return context
