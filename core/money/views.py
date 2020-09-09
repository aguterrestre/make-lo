from django.contrib.auth.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.setting.models import Company
from core.sale.models import Ticket


class MoneyDashboardView(LoginRequiredMixin, TemplateView):
    """
    Pantalla inicial de app money.
    """

    template_name = 'dashboard_money.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Dashboard'
        context['company'] = Company.objects.get(pk=1)
        context['list_url'] = reverse_lazy('money:money_dashboard')
        context['entity'] = 'Dinero'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        # Card de ingresos totales
        ticket_total = Ticket.objects.all()
        context['card_money_ticket_num_total'] = ticket_total.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        return context
