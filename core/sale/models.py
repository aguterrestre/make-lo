from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from datetime import datetime

from core.sale.choices.client.choices import GENDER_CHOICES
from core.sale.choices.ticket.choices import LETTER_CHOICESS

from crum import get_current_user

from core.stock.models import Product


class Voucher_Type(models.Model):
    """
    Tabla para guardar los tipos de comprobantes existentes en Argentina.
    Esta tabla será utilizada tanto para Venta como para Compra.
    Ejemplo:
            001	FACTURAS A
            002	NOTAS DE DEBITO A
            003	NOTAS DE CREDITO A
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.PositiveIntegerField(verbose_name='Codigo fiscal')
    internal_code = models.CharField(max_length=30, verbose_name='Código interno', blank=True)
    description = models.TextField(verbose_name='Información', blank=True)

    def __str__(self):
        return self.name

    def get_fiscal_code(self):
        return ("{:03d}".format(self.fiscal_code))

    class Meta:
        verbose_name = 'Tipo de comprobante'
        verbose_name_plural = 'Tipos de comprobantes'
        ordering = ['id']


class Fiscal_Condition(models.Model):
    """
    Tabla para guardar los tipos de condicion fiscal en Argentina. Son los tipos de
    responsables al momento de generar comprobantes.
    Esta tabla será utilizada tanto para Venta como para Compra.
    Ejemplo:
            1	IVA Responsable Inscripto
            2	IVA Responsable no Inscripto
            3	IVA no Responsable
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.PositiveIntegerField(verbose_name='Codigo fiscal')
    internal_code = models.CharField(max_length=30, verbose_name='Código interno', blank=True)
    description = models.TextField(verbose_name='Información', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Condición fiscal'
        verbose_name_plural = 'Condiciones fiscales'
        ordering = ['id']


class Document_Type(models.Model):
    """
    Tabla para guardar los tipos de documentos identificatorios en Argentina.
    Esta tabla será utilizada tanto para Venta como para Compra.
    Ejemplo:
            80	CUIT
            86	CUIL
            87	CDI
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.PositiveIntegerField(verbose_name='Codigo fiscal')
    internal_code = models.CharField(max_length=30, verbose_name='Código interno', blank=True)
    description = models.TextField(verbose_name='Información', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'
        ordering = ['id']


class Country(models.Model):
    """
    Tabla para guardar los países.
    Esta tabla será utilizada tanto para Venta como para Compra.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.PositiveIntegerField(verbose_name='Código fiscal')
    fiscal_name = models.CharField(max_length=150, verbose_name='Nombre fiscal', blank=True)
    document = models.CharField(max_length=25, verbose_name='Documento fiscal', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['id']


class Province(models.Model):
    """
    Tabla para guardar las provincias.
    Esta tabla será utilizada tanto para Venta como para Compra.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.PositiveIntegerField(verbose_name='Código fiscal')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='País')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['id']


class City(models.Model):
    """
    Tabla para guardar las cuidades.
    Esta tabla será utilizada tanto para Venta como para Compra.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    postcode = models.CharField(max_length=50, verbose_name='Código postal')
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='Provincia')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['id']


class Sale_Condition(models.Model):
    """
    Tabla para guardar las condiciones de ventas al momento de generar un comprobante.
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

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Condición de venta'
        verbose_name_plural = 'Condiciones de ventas'
        ordering = ['id']


class Client_Photo(models.Model):
    """
    Tabla para guardar fotos de perfil de usuario. Vamos a usar la clave
    primaria (campo id) para relacionar con el cliente. El campo client_id será
    para filtrar las fotos de cada cliente.
    Será una clase para guardar un histórico de imágenes.
    """
    # id = models.AutoField(primary_key=True)
    client_id = models.IntegerField()
    photo = models.ImageField(upload_to='sale/client_profile/%Y/%m/%d',
                              max_length=150, verbose_name='Imágen')
    is_active = models.BooleanField(verbose_name='Foto actual')

    def __str__(self):
        return 'photo'

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['id']


class Client_Status(models.Model):
    """
    Tabla para guardar estados asociado al cliente.
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


class Client(models.Model):
    """
    Tabla para guardar los clientes.
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
    sales_email = models.EmailField(max_length=254, blank=True, verbose_name='Email de Venta')
    telephone = models.CharField(max_length=50, default='', blank=True, verbose_name='Teléfono')
    date_birthday = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    user_creation = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='user_creation',
                                      blank=True, null=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='user_update',
                                    blank=True, null=True, default=None)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male', verbose_name='Sexo')
    document_type = models.ForeignKey(Document_Type, default=1, on_delete=models.PROTECT,
                                      verbose_name='Tipo documento')
    fiscal_condition = models.ForeignKey(Fiscal_Condition, on_delete=models.PROTECT,
                                         default=1, verbose_name='Condición fiscal')
    # photo = models.ForeignKey(Client_Photo, on_delete=models.PROTECT,
    #                           default=1, verbose_name='Foto')
    photo = models.ImageField(upload_to='sale/client_profile/%Y/%m/%d',
                              null=True, blank=True, max_length=150, verbose_name='Foto')
    residence_city = models.ForeignKey(City, on_delete=models.PROTECT, default=1,
                                       verbose_name='Ciudad de residencia')
    sale_condition = models.ForeignKey(Sale_Condition, on_delete=models.PROTECT, default=1,
                                       verbose_name='Condición de Venta')
    status = models.ForeignKey(Client_Status, on_delete=models.PROTECT, default=1, verbose_name='Estado')

    def __str__(self):
        return (f"{self.name} {self.surname}")

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = (f"{self.name} {self.surname}")
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        # item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
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
        super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Ticket(models.Model):
    """
    Tabla para guardar los comprobantes de ventas.
    """
    # id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, default=1, verbose_name='Cliente')
    letter = models.CharField(max_length=1, choices=LETTER_CHOICESS, default='c', verbose_name='Letra')
    center = models.PositiveIntegerField(verbose_name='Centro')
    number = models.PositiveIntegerField(verbose_name='Número')
    voucher_type = models.ForeignKey(Voucher_Type, on_delete=models.PROTECT, default=1,
                                     verbose_name='Tipo de comprobante')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha')
    sale_condition = models.ForeignKey(Sale_Condition, on_delete=models.PROTECT, default=1,
                                       verbose_name='Condición de Venta')
    user_creation = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                      related_name='ticket_user_creation',
                                      blank=True, null=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                    related_name='ticket_user_update',
                                    blank=True, null=True, default=None)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=12,
                                   decimal_places=4, verbose_name='SubTotal')
    total_tax = models.DecimalField(default=0.00, max_digits=12,
                                    decimal_places=4, verbose_name='Impuesto')
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=4,
                                verbose_name='Total')

    def __str__(self):
        # return (f"{self.letter}-{self.center}-{self.number}")
        # return ("{}-{:04d}-{:08d}".format(self.letter, self.center, self.number))
        return ("{}-{:04d}-{:08d}".format(self.get_letter_display(), self.center, self.number))

    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = self.client.toJSON()
        item['ticket_number'] = "{}-{:04d}-{:08d}".format(self.get_letter_display(),
                                                          self.center,
                                                          self.number)
        item['subtotal'] = format(self.subtotal, '.4f')
        item['total_tax'] = format(self.total_tax, '.4f')
        item['total'] = format(self.total, '.4f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.ticket_detail_set.all()]
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
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Boleta'
        verbose_name_plural = 'Boletas'
        ordering = ['-id']


class Ticket_Detail(models.Model):
    """
    Tabla para guardar los renglones del comprobante de venta.
    """
    # id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
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
        item = model_to_dict(self, exclude=['ticket'])
        item['product'] = self.product.toJSON()
        item['quantity'] = format(self.quantity, '.4f')
        item['final_price'] = format(self.final_price, '.4f')
        item['subtotal'] = format(self.subtotal, '.4f')
        return item

    class Meta:
        verbose_name = 'Detalle de Boleta'
        verbose_name_plural = 'Detalle de Boletas'
        ordering = ['row_number']
