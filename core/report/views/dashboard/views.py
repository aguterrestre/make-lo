from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from core.setting.models import Company


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista principal del dashboard de reportes.
    Muestra tarjetas con acceso a todos los reportes disponibles.
    """
    template_name = 'report/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Reportes'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Reportes'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['list_url'] = reverse_lazy('report:report_dashboard')
        
        context['reports'] = [
            {
                'title': 'Reporte de Ventas',
                'description': 'Consulta y analiza las ventas realizadas por período y cliente',
                'icon': 'fas fa-chart-line',
                'url': reverse_lazy('report:ticket_report'),
                'color': 'bg-success'
            },
            {
                'title': 'Reporte de Clientes',
                'description': 'Información detallada de clientes registrados',
                'icon': 'fas fa-users',
                'url': reverse_lazy('report:client_report'),
                'color': 'bg-info'
            },
            {
                'title': 'Reporte de Productos',
                'description': 'Estado de inventario y stock de productos',
                'icon': 'fas fa-boxes',
                'url': reverse_lazy('report:product_report', args=[0]),
                'color': 'bg-warning'
            },
            {
                'title': 'Reporte de Proveedores',
                'description': 'Listado y análisis de proveedores',
                'icon': 'fas fa-truck',
                'url': reverse_lazy('report:provider_report'),
                'color': 'bg-primary'
            },
            {
                'title': 'Reporte de Compras',
                'description': 'Historial de facturas y compras realizadas',
                'icon': 'fas fa-shopping-cart',
                'url': reverse_lazy('report:invoice_report'),
                'color': 'bg-danger'
            },
        ]
        
        return context
