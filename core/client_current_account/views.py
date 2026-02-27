import json
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, View

from django_filters.views import FilterView
from xhtml2pdf import pisa

from .filters import ClientCurrentAccountFilter, ClientReceiptFilter
from .forms import ClientReceiptForm
from .models import ClientCurrentAccount, ClientReceipt, ClientReceiptDetail
from core.sale.models import Client
from core.setting.models import Company


class ClientCurrentAccountListView(LoginRequiredMixin, FilterView):
    """
    Vista para listado de comprobantes de ventas en cuenta corriente de cliente.
    Se usan filtros a través de la librería django_filter.
    """
    model = ClientCurrentAccount
    template_name = 'client_current_account/list.html'
    filterset_class = ClientCurrentAccountFilter

    def get_queryset(self):
        filter = self.request.GET.get('ticket__client')
        if filter is None or filter == '':
            # Si no ingresa cliente no realiza el filtro
            return ClientCurrentAccount.objects.none()

        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = self.request.POST['action']
            if action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                            Q(name__icontains=term) | Q(surname__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Cuenta Corriente de Cliente'
        context['company'] = Company.objects.get(pk=1)
        context['list_url'] = reverse_lazy('client_current_account:client_current_account_list')
        context['entity'] = 'Cuenta Corriente Cliente'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['create_url'] = reverse_lazy('client_current_account:client_receipt_create')
        context['btn_new_detail'] = 'Nuevo Recibo'
        return context


class ClientReceiptListView(LoginRequiredMixin, FilterView):
    """
    Vista para listado de recibos de clientes.
    Se usan filtros a través de la librería django_filter.
    """
    model = ClientReceipt
    template_name = 'client_receipt/list.html'
    filterset_class = ClientReceiptFilter

    def get_queryset(self):
        filter = self.request.GET.get('client')
        if filter is None or filter == '':
            # Si no ingresa cliente no realiza el filtro
            return ClientCurrentAccount.objects.none()

        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = self.request.POST['action']
            if action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                            Q(name__icontains=term) | Q(surname__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Recibo de Cliente'
        context['company'] = Company.objects.get(pk=1)
        context['list_url'] = reverse_lazy('client_current_account:client_receipt_list')
        context['entity'] = 'Recibo Cliente'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['create_url'] = reverse_lazy('client_current_account:client_receipt_create')
        context['btn_new_detail'] = 'Nuevo Recibo'
        return context


class ClientReceiptCreateView(LoginRequiredMixin, CreateView):
    """ Vista para registrar un recibo de cliente """
    model = ClientReceipt
    form_class = ClientReceiptForm
    template_name = 'client_receipt/create.html'
    success_url = reverse_lazy('client_current_account:client_receipt_create')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_ticket_current_account':
                data = []
                print(request.POST['client_id'])
                cli = request.POST['client_id']
                # client_tickets = Ticket.objects.all(client=client)
                client_current_account = ClientCurrentAccount.objects.filter(ticket__client=cli,
                                                                             status='owed')
                print(client_current_account)
                for c in client_current_account:
                    item = c.toJSON()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    # Obtenemos los datos que vienen desde el frontend
                    client_receipt = json.loads(request.POST['receipt'])
                    # Creamos instancia de la clase Ticket
                    receipt = ClientReceipt()
                    # Guardamos cabecera de ticket
                    receipt.total = float(client_receipt['total'])
                    if client_receipt['tickets']:
                        pass
                    else:
                        receipt.balance = float(client_receipt['total'])
                    receipt.status = 'earring'
                    receipt.client = Client(id=(client_receipt['client']))
                    receipt.date_joined = client_receipt['date_joined']
                    receipt.letter = client_receipt['letter']
                    receipt.center = client_receipt['center']
                    receipt.number = client_receipt['number']
                    receipt.save()
                    # Guardamos los renglones del receipt y cambiamos el saldo de cada comprobante en cta cte
                    for t in client_receipt['tickets']:
                        receipt_detail = ClientReceiptDetail()
                        receipt_detail.client_receipt = ClientReceipt(id=receipt.id)
                        receipt_detail.ticket_receipt = ClientCurrentAccount(id=t['id'])
                        receipt_detail.total = float(t['total'])
                        receipt_detail.save()
                        current_account = ClientCurrentAccount.objects.get(pk=t['id'])
                        current_account.balance = float(current_account.balance) - float(t['total'])
                        if current_account.balance == current_account.ticket.total:
                            current_account.status = 'paid'
                        current_account.save()
                    # Devuelvo id del receipt
                    data = {'id': receipt.id}
            elif action == 'search_clients':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                            Q(name__icontains=term) | Q(surname__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Creación de Recibo'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        return context


class ClientReceiptCreatePDFView(LoginRequiredMixin, View):
    """
    Generates PDF for a client receipt.
    """

    def link_callback(self, uri, rel):
        """Serves static and media files for PDF generation."""
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('client_receipt/createpdf.html')
            receipt = ClientReceipt.objects.get(pk=self.kwargs['pk'])
            context = {
                'receipt': receipt,
                'company': Company.objects.get(pk=1)
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="recibo_{}.pdf"'.format(receipt)
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy('client_current_account:client_receipt_list'))
