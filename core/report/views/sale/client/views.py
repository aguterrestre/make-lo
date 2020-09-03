from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.sale.models import Client
from core.report.forms import ClientReportForm
from core.setting.models import Company


class ReportClientView(LoginRequiredMixin, TemplateView):
    """
    Clase para generar reportes de clientes.
    """
    template_name = 'sale/client/report.html'

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
                # Hago la busqueda de todos los client
                search = Client.objects.all()
                # Filtro la busqueda de client por fecha de nacimiento
                if len(start_date) and len(end_date):
                    search = search.filter(date_birthday__range=[start_date, end_date])
                # Filtro la busqueda de client por cliente elegido
                if client > 0:
                    search = search.filter(id=client)
                for s in search:
                    data.append(s.toJSON())
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
        context['title'] = 'Reporte de Clientes'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Reportes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('report:client_report')
        context['form'] = ClientReportForm()
        context['btn_cancel_url'] = reverse_lazy('sale:client_list')
        return context
