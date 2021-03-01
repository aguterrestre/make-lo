import base64

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, View
from django.db import transaction
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings

from django_afip import models as django_afip
from django_afip import pdf

from core.sale.models import Ticket, Ticket_Detail, Client, Sale_Condition
from core.sale.forms import TicketForm

from core.stock.models import Product

from core.setting.models import Company

import json
from xhtml2pdf import pisa
import os


class TicketListView(LoginRequiredMixin, ListView):
    """
    Vista para consultar los tickets en forma de listado.
    """
    model = Ticket
    template_name = 'ticket/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ticket.objects.all():
                    item = i.toJSON()
                    item['options'] = ''
                    data.append(item)
                    # data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Ticket_Detail.objects.filter(ticket=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'ticket_validated_afip':
                pass  # sin desarrollar en caso de volver a validar un comprobante en AFIP
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Listado de Ventas'
        context['company'] = Company.objects.get(pk=1)
        context['create_url'] = reverse_lazy('sale:ticket_create')
        context['list_url'] = reverse_lazy('sale:ticket_list')
        context['entity'] = 'Ventas'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['btn_new_detail'] = 'Nueva Venta'
        context['ticket_report_url'] = reverse_lazy('report:ticket_report')
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    Clase para crear un nuevo ticket.
    """
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/create.html'
    success_url = reverse_lazy('sale:ticket_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                # Productos a excluir porque ya fueron seleccionados en el ticket
                products_exclude = json.loads(request.POST['prod_exclude'])
                # Producto ingresado en buscador
                product_weight = request.POST['term']
                # si ingreso busqueda de 13 caracteres y es pesable
                if len(product_weight) == 13 and product_weight[0:2] == str(20):
                    prod = product_weight[2:6]  # obtengo id del producto
                    prods = Product.objects.filter(id__icontains=prod)  # filtro por id del producto
                    for i in prods.exclude(id__in=products_exclude):
                        price_i = product_weight[6:10]  # obtengo la parte entera del precio del prod
                        price_d = product_weight[10:12]  # obtengo la parte decimal del prod
                        price = float(price_i + "." + price_d)  # armo el precio del producto
                        quantity_prod = price / float(i.final_price)  # calculo la cantidad del prod
                        item = i.toJSON()
                        item['text'] = i.name  # parametro que recibe select2
                        item['quantity'] = quantity_prod
                        data.append(item)
                else:
                    prods = (Product.objects.filter(name__icontains=request.POST['term']) |
                             Product.objects.filter(barcode__icontains=request.POST['term']) |
                             Product.objects.filter(id__icontains=request.POST['term']))
                    # [0:10] esto no lo uso por el momento. al dividir el queryset lo debo hacer en ultima
                    # instancia de la consulta
                    for i in prods.exclude(id__in=products_exclude):
                        item = i.toJSON()
                        item['text'] = i.name  # parametro que recibe select2
                        item['quantity'] = 1
                        data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    tickets = json.loads(request.POST['tickets'])
                    ticket = Ticket()
                    ticket.client = Client(id=(tickets['client']))
                    ticket.letter = tickets['letter']
                    ticket.center = django_afip.PointOfSales(id=tickets['center'])
                    ticket.number = tickets['number']
                    ticket.voucher_type = django_afip.ReceiptType(id=tickets['voucher_type'])
                    ticket.date_joined = tickets['date_joined']
                    ticket.sale_condition = Sale_Condition(id=(tickets['sale_condition']))
                    ticket.subtotal = float(tickets['subtotal'])
                    ticket.total_tax = float(tickets['total_tax'])
                    ticket.total = float(tickets['total'])
                    ticket.save()
                    J = 0  # Para contabilizar el número de renglones al guardar el detalle del ticket
                    for i in tickets['products']:
                        J += 1
                        ticket_detail = Ticket_Detail()
                        ticket_detail.ticket = Ticket(id=ticket.id)
                        ticket_detail.row_numer = J
                        ticket_detail.product = Product(id=i['id'])
                        ticket_detail.quantity = float(i['quantity'])
                        ticket_detail.final_price = float(i['final_price'])
                        ticket_detail.subtotal = float(i['subtotal'])
                        ticket_detail.save()
                    data = {'id': ticket.id}  # se usa para imprimir el ticket
                    # Disminuimos el stock de cada producto
                    for p in tickets['products']:
                        product = Product.objects.get(pk=p['id'])
                        product.stock = float(product.stock) - float(p['quantity'])
                        product.save()
                    # Generamos comprobante en AFIP
                    center = django_afip.PointOfSales.objects.get(pk=tickets['center'])
                    if center.issuance_type != 'COMUN':
                        # Generamos datos iniciales
                        receipt_type = tickets['voucher_type']
                        concept = 3  # productos y servicios
                        ticket_client = Client.objects.get(id=(tickets['client']))
                        document_type = ticket_client.document_type.id
                        document_number = ticket_client.document
                        currency = 1  # 'PES'
                        # Generamos instancia de un comprobante
                        receipt = django_afip.Receipt(
                            point_of_sales=django_afip.PointOfSales(id=center.id),
                            receipt_type=django_afip.ReceiptType(id=receipt_type),
                            concept=django_afip.ConceptType(id=concept),
                            document_type=django_afip.DocumentType(id=document_type),
                            document_number=document_number,
                            # receipt_number=5,
                            issued_date=tickets['date_joined'],
                            total_amount=float(tickets['total']),
                            net_untaxed=0,
                            net_taxed=float(tickets['total']),
                            exempt_amount=0,
                            service_start=tickets['date_joined'],
                            service_end=tickets['date_joined'],
                            expiration_date=tickets['date_joined'],
                            currency=django_afip.CurrencyType(id=currency),
                            currency_quote=1,
                            # related_receipts
                        )
                        # Guardo el comprobante
                        receipt.save()
                        # Genero comprobante
                        receipt.validate(None, True)
                        # Relacionamos comprobante afip con comprobante propio
                        ticket.receipt_afip = django_afip.Receipt(id=receipt)
                        ticket.save()
            elif action == 'search_next_ticket_number':
                tickets = json.loads(request.POST['tickets'])
                next_number = Ticket.get_next_ticket_number(self, tickets['center'], tickets['voucher_type'])
                data = {'next_ticket_number': next_number}
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
        context['title'] = 'Creación de Venta'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        context['sidebar'] = 'sidebar-collapse'
        return context


class TicketCreatePDFView(LoginRequiredMixin, View):
    """
    Vista para generar PDF del ticket
    """

    def link_callback(self, uri, rel):
        """
        Metodo para servir archivos estáticos
        """
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
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ticket/createpdf.html')
            barcode = ''
            ticket = Ticket.objects.get(pk=self.kwargs['pk'])
            if ticket.receipt_afip:
                receipt = django_afip.Receipt.objects.get(pk=ticket.receipt_afip.id)
                generator = pdf.ReceiptBarcodeGenerator(receipt)
                barcode = (base64.b64encode(generator.generate_barcode())).decode()
            context = {
                'ticket': ticket,
                'company': Company.objects.get(pk=1),
                'barcode': barcode
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # Para guardar directamente el archivo sin vista previa
            # response['Content-Disposition'] = 'attachment; filename="r.pdf"'
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy('sale:ticket_list'))
