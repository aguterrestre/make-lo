from django.db import models
from django.conf import settings
from django.forms import model_to_dict

from crum import get_current_user

from datetime import datetime


class Tax_IVA(models.Model):
    """
    Tabla de impuesto al valor agregado. Se asocia a un producto o servicio.
    Ejemplo:
            0   No Corresponde
            1   No Gravado
            2   Exento
            etc.
    """
    # id = models.AutoField(primary_key=True)
    fiscal_code = models.PositiveIntegerField(verbose_name='Código fiscal')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    alicuot = models.DecimalField(default=0.00, max_digits=5, decimal_places=4, verbose_name='Alícuota')
    description = models.TextField(blank=True, verbose_name='Información')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Condición de IVA'
        verbose_name_plural = 'Condiciones de IVA'
        ordering = ['id']


class Unit_Measure(models.Model):
    """
    Tabla para guardar la unidad de medida de un producto.
    Ejemplo:
            00  SIN DESCRIPCION
            01  KILOGRAMO
            02  METROS
            etc.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Nombre')
    fiscal_code = models.CharField(max_length=5, default='00', verbose_name='Código fiscal')
    description = models.TextField(blank=True, verbose_name='Información')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'
        ordering = ['id']


class Product_Image(models.Model):
    """
    Tabla para guardar fotos de productos. Vamos a usar la clave
    primaria (campo id) para relacionar con el producto. El campo product será
    para filtrar las fotos de cada producto.
    Será una clase para guardar un histórico de imágenes.
    """
    # id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=25)
    image = models.ImageField(upload_to='stock/product/%Y/%m/%d', max_length=150, verbose_name='Imágen')
    is_active = models.BooleanField(verbose_name='Imágen actual')

    def __str__(self):
        return 'image'

    class Meta:
        verbose_name = 'Imágen de producto'
        verbose_name_plural = 'Imágenes de producto'
        ordering = ['id']


class Category(models.Model):
    """
    Tabla para guardar categorias asociadas a los productos.
    """
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Información')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de producto'
        ordering = ['id']


class Product(models.Model):
    """
    Tabla para guardar los productos.
    """
    id = models.CharField(primary_key=True, max_length=25, verbose_name='Código')
    name = models.CharField(max_length=150, default='', verbose_name='Nombre')
    barcode = models.CharField(max_length=150, default='', verbose_name='Código de barra')
    purchase_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=4,
                                         verbose_name='Precio de compra')
    sale_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=4,
                                     verbose_name='Precio de venta')
    exception = models.BooleanField(default=False, verbose_name='Exento')
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=4, verbose_name='Descuento')
    final_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=4,
                                      verbose_name='Precio final')
    user_creation = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                      related_name='product_user_creation',
                                      blank=True, null=True, default=None)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                                    related_name='product_user_update',
                                    blank=True, null=True, default=None)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    category = models.ForeignKey(Category, default=1, on_delete=models.PROTECT, verbose_name='Categoría')
    # image = models.ForeignKey(Product_Image, on_delete=models.PROTECT,
    #                           default=1, verbose_name='Imágen')
    image = models.ImageField(upload_to='stock/product/%Y/%m/%d', null=True,
                              blank=True, max_length=150, verbose_name='Imágen')
    unit = models.ForeignKey(Unit_Measure, on_delete=models.PROTECT, default=1,
                             verbose_name='Unidad de medida')
    tax = models.ForeignKey(Tax_IVA, on_delete=models.PROTECT, default=1, verbose_name='Condición de IVA')
    stock = models.DecimalField(default=0.00, max_digits=10, decimal_places=3, verbose_name='Stock')
    date_expiration = models.DateField(null=True, blank=True, default=datetime.now,
                                       verbose_name='Fecha de vencimiento')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['categ'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['unit'] = self.unit.toJSON()
        item['text'] = self.name
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    def save(self,  *args, **kwargs):
        """
        Sobreescribimos el metodo save para hacer auditoria de la tabla con
        librería django-crum.
        """
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.user_creation:
            self.user_creation = user
        self.user_update = user
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
