from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files import File

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

    def post(self, request, *args, **kwargs):
        data = {}

        # Create a TaxPayer object:
        taxpayer = models.TaxPayer(
            pk=1,
            name='Agustín Terrestre',
            cuit=20342778950,
            is_sandboxed=True,
            active_since='2014-10-01',
        )
        print('creo instancia del contribuyente, en este caso yo je')

        # Add the key and certificate files to the TaxPayer:
        with open('c:/Django_Proyectos/Make-lo/Make-lo/Make-lo/static/afip/makelotestKEY.key') as key:
            taxpayer.key.save('test.key', File(key))
            print('asocio la key al contribuyente instanciado')
        with open('c:/Django_Proyectos/Make-lo/Make-lo/Make-lo/static/afip/makelotestCRT.crt') as crt:
            taxpayer.certificate.save('test.crt', File(crt))
            print('asocio el crt al contribuyente instanciado')

        # Save a TaxPayer object:
        taxpayer.save()
        print('guardo el contribuyente instanciado')

        # Load all metadata:
        models.populate_all()
        print('cargo todos los datos de afip en los modelos de la aplicacion')

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
            # receipt_number=
            issued_date='2020-10-24',
            total_amount=100.00,
            net_untaxed=0,
            net_taxed=100.00,
            exempt_amount=0,
            service_start='2020-10-24',
            service_end='2020-10-24',
            expiration_date='2020-10-24',
            # currency=models.CurrencyType(code='PES'),
            currency=models.CurrencyType(id=1),
            currency_quote=1,
            # related_receipts
        )
        print('creo instancia del contribuyente')

        # Guardo el comprobante
        comprobante.save()
        print('guardo el comprobante')

        # Genero comprobante
        comprobante.validate(None, True)
        print('generamos el comprobante')

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
