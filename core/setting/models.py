from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from django_afip import models as django_afip

from core.sale.models import City


class Company(models.Model):
    """ Modelo para administrar los datos de empresa """

    name = models.CharField(max_length=150, verbose_name='Nombre')
    address = models.CharField(max_length=200, default='', blank=True, verbose_name='Dirección')
    contact_email = models.EmailField(max_length=254, blank=True, verbose_name='Email de Contacto')
    fiscal_condition = models.CharField(max_length=60, default='Responsable Monotributo',
                                        choices=((cond, cond,) for cond in django_afip.VAT_CONDITIONS),
                                        verbose_name='Condición fiscal')
    document_type = models.ForeignKey(django_afip.DocumentType, null=True, on_delete=models.PROTECT,
                                      default=1, verbose_name='Tipo documento')
    document = models.CharField(max_length=25, default='', verbose_name='Número documento')
    image_login = models.ImageField(upload_to='setting/company_image_login/%Y/%m/%d',
                                    null=True, blank=True, max_length=150,
                                    verbose_name='Foto para Inicio de sesión')
    image_sidebar = models.ImageField(upload_to='setting/company_image_sidebar/%Y/%m/%d',
                                      null=True, blank=True, max_length=150,
                                      verbose_name='Foto para Menú izquierdo')
    image_favicon = models.ImageField(upload_to='setting/company_image_favicon/%Y/%m/%d',
                                      null=True, blank=True, max_length=150,
                                      verbose_name='Foto para pestaña de navegador')
    description = models.TextField(verbose_name='Información', blank=True)
    image_ticket = models.ImageField(upload_to='setting/company_image_ticket/%Y/%m/%d',
                                     null=True, blank=True, max_length=150,
                                     verbose_name='Foto para Comprobante de venta')
    document_IIBB = models.CharField(max_length=25, default='', blank=True,
                                     verbose_name='Número ingresos brutos')
    date_activity_start = models.DateField(null=True, blank=True, verbose_name='Inicio de actidad')
    residence_city = models.ForeignKey(City, on_delete=models.PROTECT, default=1, verbose_name='Ciudad')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['image_login'] = self.get_photo_image_login()
        item['image_sidebar'] = self.get_photo_image_sidebar()
        item['image_favicon'] = self.get_photo_image_favicon()
        return item

    def get_photo_image_login(self):
        if self.image_login:
            return '{}{}'.format(settings.MEDIA_URL, self.image_login)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def get_photo_image_sidebar(self):
        if self.image_sidebar:
            return '{}{}'.format(settings.MEDIA_URL, self.image_sidebar)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def get_photo_image_sidebar_url(self):
        """ Metodo para retornar la url de la imagen """
        if self.image_sidebar:
            return self.image_sidebar.url
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def get_photo_image_favicon(self):
        if self.image_favicon:
            return '{}{}'.format(settings.MEDIA_URL, self.image_favicon)
        return '{}{}'.format(settings.STATIC_URL, 'img/favicon.ico')

    def get_photo_image_ticket(self):
        if self.image_ticket:
            return '{}{}'.format(settings.MEDIA_URL, self.image_ticket)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def get_photo_image_ticket_url(self):
        """ Metodo para retornar la url de la imagen """
        if self.image_ticket:
            return self.image_ticket.url
        return self.image_ticket

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['id']
