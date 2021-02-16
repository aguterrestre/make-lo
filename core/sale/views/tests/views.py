from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.core.files import File
# from django.template.loader import get_template
from django.conf import settings

# from xhtml2pdf import pisa
import os

from core.setting.models import Company

from django_afip import models


class TestsAfipView(LoginRequiredMixin, TemplateView):
    """
    Clase para ver en pantalla los clientes de la empresa a manera de listado.
    """
    template_name = 'tests/tests.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        data = {}

        # Create a TaxPayer object:
        # taxpayer = models.TaxPayer(
        #     pk=1,
        #     name='Agustín Terrestre',
        #     cuit=20342778950,
        #     is_sandboxed=True,
        #     active_since='2014-10-01',
        # )
        # print('creo instancia del contribuyente, en este caso yo je')

        # Add the key and certificate files to the TaxPayer:
        # with open('c:/Django_Proyectos/Make-lo/Make-lo/Make-lo/static/afip/makelotestKEY.key') as key:
        #     taxpayer.key.save('test.key', File(key))
        #     print('asocio la key al contribuyente instanciado')
        # with open('c:/Django_Proyectos/Make-lo/Make-lo/Make-lo/static/afip/makelotestCRT.crt') as crt:
        #     taxpayer.certificate.save('test.crt', File(crt))
        #     print('asocio el crt al contribuyente instanciado')

        # Save a TaxPayer object:
        # taxpayer.save()
        # print('guardo el contribuyente instanciado')

        # Load all metadata:
        # models.populate_all()
        # print('cargo todos los datos de afip en los modelos de la aplicacion')

        # Get the TaxPayer's Point of Sales:
        # Este metodo no es necesario con ws homologacion
        # taxpayer.fetch_points_of_sales()
        # print('obtengo el punto de venta del contribuyente')

        # generar un comprobante en afip usamos una instancia de Receipt
        comprobante = models.Receipt(
            point_of_sales=models.PointOfSales(id=1),
            receipt_type=models.ReceiptType(id=19),
            concept=models.ConceptType(id=2),
            document_type=models.DocumentType(id=1),
            document_number=23343123469,
            # receipt_number=5,
            issued_date='2021-02-15',
            total_amount=100.00,
            net_untaxed=0,
            net_taxed=100.00,
            exempt_amount=0,
            service_start='2021-02-15',
            service_end='2021-02-15',
            expiration_date='2021-02-15',
            # currency=models.CurrencyType(code='PES'),
            currency=models.CurrencyType(id=1),
            currency_quote=1,
            # related_receipts
        )
        print('creo instancia del comprobante')

        # Guardo el comprobante
        comprobante.save()
        print('guardo instancia del comprobante')

        # Genero comprobante
        comprobante.validate(None, True)
        print('generamos el comprobante')

        # Genero instancia de pdf para comprobante
        # receipt_pdf = models.ReceiptPDF(
        #     receipt=comprobante,
        #     issuing_name='Dada',
        #     issuing_address='Tucucu',
        #     issuing_email='aa@g.com',
        #     vat_condition='contado con liqui',
        #     gross_income_condition='qui si o',
        #     client_name='El dudu',
        #     client_address='sumao tara 22',
        #     client_vat_condition='clin caja',
        #     sales_terms='arrebato',
        # )
        # print('creo instancia de pdf del comprobante')

        # template = get_template('afip/receipts/code_11.html')
        # context = {
        #     'pdf': receipt_pdf,
        #     'taxpayer': taxpayer
        # }
        # html = template.render(context)
        # f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
        # pisa.CreatePDF(html, dest=f, link_callback=self.link_callback)
        # print('generamos el archivo pdf')

        # Guardo pdf en instancia
        # receipt_pdf.pdf_file = File(f)
        # print('guardo pdf en instancia')

        # Guardo comprobante pdf
        # receipt_pdf.save()
        # print('guardo pdf del comprobante')

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favicon'] = Company.objects.get(pk=1)
        context['title'] = 'test afip'
        context['company'] = Company.objects.get(pk=1)
        context['list_url'] = reverse_lazy('sale:client_list')
        context['entity'] = 'testafip'
        context['dashboard_url'] = reverse_lazy('login:dashboard')
        return context
