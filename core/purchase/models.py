from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from datetime import datetime

from crum import get_current_user

from core.sale.models import Document_Type
from core.sale.models import Fiscal_Condition
from core.sale.models import City
from core.sale.models import Voucher_Type

from core.purchase.choices.invoice.choices import LETTER_CHOICESS

from core.stock.models import Product


class Purchase_Condition(models.Model):
    """
    Tabla para guardar las condiciones de compras al momento de generar un comprobante.
    Ejemplo:
            1	Contado
            2	Cuenta Corriente
            3	A 30 dias
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    internal_code = models.CharField(max_length=30, verbose_name='Código interno', blank=True)
    description = models.TextField(verbose_name='Información', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Condición de compra'
        verbose_name_plural = 'Condiciones de compras'
        ordering = ['id']


class Provider_Photo(models.Model):
    """
    Tabla para guardar fotos de perfil de proveedor. Vamos a usar la clave
    primaria (campo id) para relacionar con el proveedor. El campo provider_id será
    para filtrar las fotos de cada proveedor.
    Será una clase para guardar un histórico de imágenes.
    """
    # id = models.AutoField(primary_key=True)
    provider_id = models.IntegerField()
    photo = models.ImageField(upload_to='purchase/provider_profile/%Y/%m/%d',
                              max_length=150, verbose_name='Imágen')
    is_active = models.BooleanField(verbose_name='Foto actual')

    def __str__(self):
        return 'photo'

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['id']


class Provider_Status(models.Model):
    """
    Tabla para guardar estados asociado al proveedor.
    Ejemplo:
            1 Activo
            2 Inactivo
            3 Cerrado
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.TextField(verbose_name='Información', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['id']


class Provider(models.Model):
    """
    Tabla para guardar los proveedores.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, default='', verbose_name='Nombre')
    surname = models.CharField(max_length=150, default='', blank=True, verbose_name='Apellido')
    business_name = models.CharField(max_length=150, default='', verbose_name='Nombre comercial')
    trade_name = models.CharField(max_length=150, default='', verbose_name='Razón social')
    comercial_address = models.CharField(max_length=200, default='', verbose_name='Dirección comercial')
    document = models.CharField(max_length=25, default='', verbose_name='Número documento')
    address = models.CharField(max_length=200, default='', blank=True, verbose_name='Dirección')
    contact_email = models.EmailField(max_length=254, blank=True, verbose_name='Email de Contacto')
    purchase_email = models.EmailField(max_length=254, blank=True, verbose_name='Email de Compra')
    telephone = models.CharField(max_length=50, default='', blank=True, verbose_name='Teléfono')
    date_birthday = models.DateField(default=datetime.now, blank=True, verbose_name='Fecha de nacimiento')
    user_creation = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                      related_name='provider_user_creation',
                                      blank=True, null=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                    related_name='provider_user_update',
                                    blank=True, null=True, default=None)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    document_type = models.ForeignKey(Document_Type, default=1, on_delete=models.PROTECT,
                                      verbose_name='Tipo documento')
    fiscal_condition = models.ForeignKey(Fiscal_Condition, on_delete=models.PROTECT,
                                         default=1, verbose_name='Condición fiscal')
    # photo = models.ForeignKey(Client_Photo, on_delete=models.PROTECT,
    #                           default=1, verbose_name='Foto')
    photo = models.ImageField(upload_to='purchase/provider_profile/%Y/%m/%d',
                              null=True, blank=True, max_length=150, verbose_name='Foto')
    residence_city = models.ForeignKey(City, on_delete=models.PROTECT, default=1,
                                       verbose_name='Ciudad de residencia')
    purchase_condition = models.ForeignKey(Purchase_Condition, on_delete=models.PROTECT, default=1,
                                           verbose_name='Condición de compra')
    status = models.ForeignKey(Provider_Status, on_delete=models.PROTECT, default=1, verbose_name='Estado')

    def __str__(self):
        return (f"{self.name} {self.surname}")

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = (f"{self.name} {self.surname}")
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['photo'] = self.get_photo()
        item['text'] = (f"{self.name} {self.surname}")
        item['document_type'] = self.document_type.name
        return item

    def get_photo(self):
        if self.photo:
            return '{}{}'.format(settings.MEDIA_URL, self.photo)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def save(self,  *args, **kwargs):
        """
        Sobreescribimos el metodo save para hacer auditoria de la tabla con
        librería django-crum.
        """
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user_creation = user
        self.user_update = user
        super(Provider, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


class Invoice(models.Model):
    """
    Tabla para guardar los comprobantes de compras.
    """
    # id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, default=1, verbose_name='Proveedor')
    letter = models.CharField(max_length=1, choices=LETTER_CHOICESS, default='c', verbose_name='Letra')
    center = models.PositiveIntegerField(verbose_name='Centro')
    number = models.PositiveIntegerField(verbose_name='Número')
    voucher_type = models.ForeignKey(Voucher_Type, on_delete=models.PROTECT, default=1,
                                     verbose_name='Tipo de comprobante')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha')
    purchase_condition = models.ForeignKey(Purchase_Condition, on_delete=models.PROTECT, default=1,
                                           verbose_name='Condición de compra')
    user_creation = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                      related_name='invoice_user_creation',
                                      blank=True, null=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                    related_name='invoice_user_update',
                                    blank=True, null=True, default=None)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=12,
                                   decimal_places=4, verbose_name='SubTotal')
    total_tax = models.DecimalField(default=0.00, max_digits=12,
                                    decimal_places=4, verbose_name='Impuesto')
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=4,
                                verbose_name='Total')

    def __str__(self):
        return ("{}-{:04d}-{:08d}".format(self.get_letter_display(), self.center, self.number))

    def toJSON(self):
        item = model_to_dict(self)
        item['provider'] = self.provider.toJSON()
        item['invoice_number'] = "{}-{:04d}-{:08d}".format(self.get_letter_display(),
                                                           self.center,
                                                           self.number)
        item['subtotal'] = format(self.subtotal, '.4f')
        item['total_tax'] = format(self.total_tax, '.4f')
        item['total'] = format(self.total, '.4f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.invoice_detail_set.all()]
        return item

    def save(self,  *args, **kwargs):
        """
        Sobreescribimos el metodo save para hacer auditoria de la tabla con
        librería django-crum.
        """
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user_creation = user
        self.user_update = user
        super(Invoice, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Boleta'
        verbose_name_plural = 'Boletas'
        ordering = ['-id']


class Invoice_Detail(models.Model):
    """
    Tabla para guardar los renglones del comprobante de compra.
    """
    # id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    row_number = models.PositiveIntegerField(default=1, verbose_name='Número de renglón')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(default=0.00, max_digits=10,
                                   decimal_places=3, verbose_name='Cantidad')
    final_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=4,
                                      verbose_name='Precio final')
    subtotal = models.DecimalField(default=0.00, max_digits=12,
                                   decimal_places=4, verbose_name='SubTotal')

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['invoice'])
        item['product'] = self.product.toJSON()
        item['quantity'] = format(self.quantity, '.4f')
        item['final_price'] = format(self.final_price, '.4f')
        item['subtotal'] = format(self.subtotal, '.4f')
        return item

    class Meta:
        verbose_name = 'Detalle de Boleta'
        verbose_name_plural = 'Detalle de Boletas'
        ordering = ['row_number']
