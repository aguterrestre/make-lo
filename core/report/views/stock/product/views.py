from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.stock.models import Product
from core.report.forms import ProductReportForm
from core.setting.models import Company


class ReportProductView(LoginRequiredMixin, TemplateView):
    """
    Clase para generar reportes de productos.
    """
    template_name = 'stock/product/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                # Obtengo los filtros elegidos en el template
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                product = request.POST.get('product', '')
                stock = int(request.POST.get('stock', ''))
                # Hago la busqueda de todos los product
                search = Product.objects.all()
                # Filtro la busqueda de product por fecha de vencimiento
                if len(start_date) and len(end_date):
                    search = search.filter(date_expiration__range=[start_date, end_date])
                # Filtro la busqueda de product por product elegido
                if len(product):
                    search = search.filter(id=product)
                # Filtro la busqueda de product por el stock
                if stock == 1:  # Product sin stock
                    search = search.filter(stock__lte=0)
                elif stock == 2:  # Product con stock
                    search = search.filter(stock__gt=0)
                elif stock == 3:  # Product con bajo stock
                    search = search.filter(stock__lte=3, stock__gt=0)
                for s in search:
                    data.append(s.toJSON())
            elif action == 'search_product':
                data = []
                prod = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prod:
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Reporte de Productos'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Reportes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('report:product_report')
        context['form'] = ProductReportForm()
        context['btn_cancel_url'] = reverse_lazy('stock:product_list')
        return context
