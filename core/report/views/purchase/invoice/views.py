from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.purchase.models import Invoice, Provider
from core.report.forms import InvoiceReportForm
from core.setting.models import Company

# from django.db.models.functions import Coalesce
# from django.db.models import Sum


class ReportInvoiceView(LoginRequiredMixin, TemplateView):
    """
    Clase para generar reportes de invoices.
    """
    template_name = 'purchase/invoice/report.html'

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
                provider = int(request.POST.get('provider', ''))
                # Hago la busqueda de todos los invoices
                search = Invoice.objects.all()
                # Filtro la busqueda de invoice por fecha de registro
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                # Filtro la busqueda de invoice por proveedor
                if provider > 0:
                    search = search.filter(provider=provider)
                for s in search:
                    data.append(s.toJSON())
                    """
                    data.append([
                        s.id,
                        s.client.name,
                        s.letter,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.4f'),
                        format(s.total_tax, '.4f'),
                        format(s.total, '.4f'),
                    ])
                    """
                """
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])
                """
            elif action == 'search_provider':
                data = []
                pro = Provider.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in pro:
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
        context['title'] = 'Reporte de Compras'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Reportes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('report:invoice_report')
        context['form'] = InvoiceReportForm()
        context['btn_cancel_url'] = reverse_lazy('purchase:invoice_list')
        return context
