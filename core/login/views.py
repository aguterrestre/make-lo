from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from django.db.models import Sum

from core.sale.models import Client, Ticket
from core.stock.models import Product
from core.setting.models import Company
from core.purchase.models import Provider, Invoice

from datetime import datetime

import config.settings as settings


class LoginFormView(LoginView):
    """
    Clase para autenticar un usuario al sistema.
    """

    template_name = 'login.html'

    # Validamos si el user está logueado para no abrir la vista de login
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Iniciar sesión'
        context['company'] = Company.objects.get(pk=1)
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        return context


class LoginEmptyFormView(LoginView):
    """
    Clase para redireccionar al login cuando un usuario ingresa a la url raiz.
    """

    # Validamos si el user está logueado para no abrir la vista de login
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return redirect(settings.LOGIN_URL)


class LogoutFormView(LogoutView):
    """
    Vista para hacer logout del sistema.
    """

    # Definimos atributo de LogoutView para saber donde tiene que redireccionar
    # cuando se hace logout. Podemos usar settings.LOGOUT_REDIRECT_URL pero no
    # va bien con logout del backends django
    next_page = '/login/'


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Pantalla inicial al hacer login exitoso.
    """

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Dashboard'
        context['company'] = Company.objects.get(pk=1)
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        # Card de nuevos clientes
        context['card_news_client_num'] = Client.objects.filter(date_creation__date=datetime.now())
        context['card_news_client_url'] = reverse_lazy('report:client_report')
        # Card de productos bajo stock
        context['card_low_product_stock_num'] = Product.objects.filter(stock__lte=3, stock__gt=0)
        context['card_low_product_stock_url'] = reverse_lazy('report:product_report', args=[1])
        # Card de nuevas ventas en el día de hoy
        context['card_news_ticket_num'] = Ticket.objects.filter(date_creation__date=datetime.now())
        context['card_news_ticket_url'] = reverse_lazy('report:ticket_report')
        # Card de ingresos en el día de hoy
        ticket_today = Ticket.objects.filter(date_creation__date=datetime.now())
        context['card_money_ticket_num'] = ticket_today.aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        # Card de nuevos proveedores
        context['card_news_provider_num'] = Provider.objects.filter(date_creation__date=datetime.now())
        context['card_news_provider_url'] = reverse_lazy('report:provider_report')
        # Card de nuevas compras en el día de hoy
        context['card_news_invoice_num'] = Invoice.objects.filter(date_creation__date=datetime.now())
        context['card_news_invoice_url'] = reverse_lazy('report:invoice_report')
        return context
