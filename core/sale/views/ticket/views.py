from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, View
from django.db import transaction
from django.template.loader import get_template
from django.conf import settings

from core.sale.models import Ticket, Ticket_Detail, Client
from core.sale.forms import TicketForm

from core.stock.models import Product

from core.setting.models import Company

import json
from xhtml2pdf import pisa
import os


class TicketListView(LoginRequiredMixin, ListView):
    """
    Clase para ver en pantalla los tickets de la empresa a manera de listado.
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
                product_weight = request.POST['term']
                # si ingreso busqueda de 13 caracteres y es pesable
                if len(product_weight) == 13 and product_weight[0:2] == str(20):
                    prod = product_weight[2:6]  # obtengo id del producto
                    prods = Product.objects.filter(id__icontains=prod)  # filtro por id del producto
                    for i in prods:
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
                             Product.objects.filter(id__icontains=request.POST['term']))[0:10]
                    for i in prods:
                        item = i.toJSON()
                        # item['value'] = i.name
                        item['text'] = i.name  # parametro que recibe select2
                        item['quantity'] = 1
                        data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    tickets = json.loads(request.POST['tickets'])
                    ticket = Ticket()
                    # client_ticket = Client(id=(tickets['client']))
                    # ticket.client = client_ticket.id
                    ticket.client = Client(id=(tickets['client']))
                    for comp in Company.objects.filter(id=1):
                        ticket.letter = comp.letter
                        ticket.center = comp.center
                        ticket.number = comp.number
                    ticket.date_joined = tickets['date_joined']
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
                    data = {'id': ticket.id}  # se usa imprimir el ticket
                    # Aumentamos el numerador de ticket en la empresa
                    company = Company.objects.get(pk=1)
                    company.number = ticket.number + 1
                    company.save()
                    # Disminuimos el stock de cada producto
                    for p in tickets['products']:
                        product = Product.objects.get(pk=p['id'])
                        product.stock = float(product.stock) - float(p['quantity'])
                        product.save()
                    """
                    elif action == 'search_client':
                        data = []
                        cli = Client.objects.filter(name__icontains=request.POST['term'])[0:10]
                        for i in cli:
                            item = i.toJSON()
                            item['value'] = i.name
                            data.append(item)
                    """
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
        # context['create_url'] = reverse_lazy('erp:client_create')
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
            template = get_template('ticket/createpdf0.html')
            context = {
                'ticket': Ticket.objects.get(pk=self.kwargs['pk']),
                'company': Company.objects.get(pk=1)
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
