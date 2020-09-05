from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, View
from django.db import transaction
from django.template.loader import get_template
from django.conf import settings

from core.purchase.models import Invoice, Invoice_Detail, Provider
from core.purchase.forms import InvoiceForm

from core.stock.models import Product

from core.setting.models import Company

import json
from xhtml2pdf import pisa
import os


class InvoiceListView(LoginRequiredMixin, ListView):
    """
    Clase para ver en pantalla las invoices de la empresa a manera de listado.
    """
    model = Invoice
    template_name = 'invoice/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Invoice.objects.all():
                    item = i.toJSON()
                    item['options'] = ''
                    data.append(item)
                    # data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Invoice_Detail.objects.filter(invoice=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Listado de Compras'
        context['company'] = Company.objects.get(pk=1)
        context['create_url'] = reverse_lazy('purchase:invoice_create')
        context['list_url'] = reverse_lazy('purchase:invoice_list')
        context['entity'] = 'Compras'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['btn_new_detail'] = 'Nueva Compra'
        context['invoice_report_url'] = reverse_lazy('report:invoice_report')
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    """
    Clase para crear una nueva invoice.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice/create.html'
    success_url = reverse_lazy('purchase:invoice_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.name
                    item['text'] = i.name  # parametro que recibe select2
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    invoices = json.loads(request.POST['invoices'])
                    invoice = Invoice()
                    invoice.provider = Provider(id=(invoices['provider']))
                    for comp in Company.objects.filter(id=1):
                        invoice.letter = comp.letter
                        invoice.center = comp.center
                        invoice.number = comp.number
                    invoice.date_joined = invoices['date_joined']
                    invoice.subtotal = float(invoices['subtotal'])
                    invoice.total_tax = float(invoices['total_tax'])
                    invoice.total = float(invoices['total'])
                    invoice.save()
                    J = 0  # Para contabilizar el número de renglones al guardar el detalle del invoice
                    for i in invoices['products']:
                        J += 1
                        invoice_detail = Invoice_Detail()
                        invoice_detail.invoice = Invoice(id=invoice.id)
                        invoice_detail.row_numer = J
                        invoice_detail.product = Product(id=i['id'])
                        invoice_detail.quantity = float(i['quantity'])
                        invoice_detail.final_price = float(i['final_price'])
                        invoice_detail.subtotal = float(i['subtotal'])
                        invoice_detail.save()
                    data = {'id': invoice.id}  # se usa imprimir el ticket
                    # Aumentamos el numerador de ticket en la empresa
                    company = Company.objects.get(pk=1)
                    company.number = invoice.number + 1
                    company.save()
                    # Aumentamos el stock de cada producto
                    for p in invoices['products']:
                        product = Product.objects.get(pk=p['id'])
                        product.stock = float(product.stock) + float(p['quantity'])
                        product.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'Creación de Compra'
        context['company'] = Company.objects.get(pk=1)
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        context['action'] = 'add'
        return context


class InvoiceCreatePDFView(LoginRequiredMixin, View):
    """
    Vista para generar PDF del invoice
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
            template = get_template('invoice/createpdf0.html')
            context = {
                'invoice': Invoice.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('purchase:invoice_list'))
