from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.sale.models import Ticket, Client
from core.report.forms import TicketReportForm
from core.setting.models import Company

# from django.db.models.functions import Coalesce
# from django.db.models import Sum


class ReportTicketView(LoginRequiredMixin, TemplateView):
    """
    Clase para generar reportes de tickets.
    """
    template_name = 'sale/ticket/report.html'

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
                client = int(request.POST.get('client', ''))
                # Hago la busqueda de todos los ticket
                search = Ticket.objects.all()
                # Filtro la busqueda de ticket por fecha de registro
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                # Filtro la busqueda de ticket por cliente
                if client > 0:
                    search = search.filter(client=client)
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
            elif action == 'search_client':
                data = []
                cli = Client.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in cli:
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
        context['title'] = 'Reporte de Ventas'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Reportes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('report:ticket_report')
        context['form'] = TicketReportForm()
        context['btn_cancel_url'] = reverse_lazy('sale:ticket_list')
        return context
