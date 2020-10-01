from django.contrib.auth.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.db.models.functions import Coalesce

# from datetime import datetime
import datetime

from core.setting.models import Company
from core.sale.models import Ticket
from core.purchase.models import Invoice


class MoneyDashboardView(LoginRequiredMixin, TemplateView):
    """
    Pantalla inicial de app money.
    """

    template_name = 'dashboard_money.html'

    def get_card_money_percentage_increase(self, obj):
        increase = 0
        try:
            # obtengo la fecha actual
            current_date = datetime.date.today()
            # obtengo datos numericos del ultimo día del mes pasado
            last_month = current_date.replace(day=1)+datetime.timedelta(days=-1)
            # inicio variable del primer dia del mes anterior
            start_date = datetime.datetime(last_month.year, last_month.month, 1)
            # inicio variable del ultimo dia del mes anterior
            end_date = datetime.datetime(last_month.year, last_month.month, last_month.day)
            # obtengo todas las ventas del mes pasado
            total_last_month = obj.objects.filter(date_creation__range=(start_date, end_date))
            # sumo los totales del mes pasado
            total_last_month_tot = total_last_month.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            # saco promedio de venta del mes pasado
            total_last_month_tot = total_last_month_tot / last_month.day
            # obtengo datos numericos del ultimo dia del mes actual
            cur_month = current_date.replace(month=current_date.month+1, day=1) - datetime.timedelta(days=1)
            # inicio variable del primer dia del mes actual
            start_date = datetime.datetime(cur_month.year, cur_month.month, 1)
            # inicio variable del ultimo dia del mes actual
            end_date = datetime.datetime(cur_month.year, cur_month.month, cur_month.day)
            # obtengo todas las ventas del mes actual
            total_current_month = obj.objects.filter(date_creation__range=(start_date, end_date))
            # sumo los totales del mes actual
            total_current_month_tot = total_current_month.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
            # saco promedio de venta del mes actual
            total_current_month_tot = total_current_month_tot / cur_month.day
            # calculo de aumento de ventas del mes actual sin decimales
            increase = int((((total_current_month_tot / total_last_month_tot) - 1) * 100))
            # controlamos cuando el aumento es negativo ya el total del mes pasado es mayor al actual
            if increase < 0:
                increase = 0
            # esta faltando ajustar el calculo de ultimo dia del mes cuando hay cambio de año
        except ZeroDivisionError:
            increase = 100  # al no tener totales del mes pasado mostramos un 100%
        except Exception:
            increase = 0
        return increase

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
        ticket_num_total = ticket_total.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_ticket_num_total'] = ticket_num_total
        context['card_money_ticket_sale_increase'] = self.get_card_money_percentage_increase(Ticket)
        # Card de egresos totales
        invo_total = Invoice.objects.all()
        invoice_num_total = invo_total.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_invoice_num_total'] = invoice_num_total
        context['card_money_invoice_purchase_increase'] = self.get_card_money_percentage_increase(Invoice)
        # Card de resultados totales
        total_result = ticket_num_total - invoice_num_total
        context['card_money_total_result'] = total_result
        # Card de ingresos por forma de pago - experimental
        ticket_s_cond = Ticket.objects.filter(sale_condition__id=1)
        ticket_s_cond_quan = ticket_s_cond.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_ticket_sale_1condition_num'] = ticket_s_cond
        context['card_money_ticket_sale_1condition'] = ticket_s_cond_quan
        ticket_s_cond = Ticket.objects.filter(sale_condition__id=2)
        ticket_s_cond_quan = ticket_s_cond.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_ticket_sale_2condition_num'] = ticket_s_cond
        context['card_money_ticket_sale_2condition'] = ticket_s_cond_quan
        ticket_s_cond = Ticket.objects.filter(sale_condition__id=3)
        ticket_s_cond_quan = ticket_s_cond.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_ticket_sale_3condition_num'] = ticket_s_cond
        context['card_money_ticket_sale_3condition'] = ticket_s_cond_quan
        ticket_s_cond = Ticket.objects.filter(sale_condition__id=4)
        ticket_s_cond_quan = ticket_s_cond.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        context['card_money_ticket_sale_4condition_num'] = ticket_s_cond
        context['card_money_ticket_sale_4condition'] = ticket_s_cond_quan
        return context
