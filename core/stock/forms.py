from django.forms import ModelForm, Form, TextInput, NumberInput, DateInput, Select, ChoiceField, DecimalField
from core.stock.models import Product, Category, Unit_Measure


class ProductForm(ModelForm):
    """
    Clase para crear el formulario de producto
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'id': TextInput(
                attrs={
                    'placeholder': 'Ingrese el código',
                }
            ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                }
            ),
            'barcode': TextInput(
                attrs={
                    'placeholder': 'Ingrese el código de barra',
                }
            ),
            'purchase_price': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el precio de compra',
                }
            ),
            'final_price': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el precio final',
                }
            ),
            'stock': NumberInput(),
            'unit': Select(),
        }
        exclude = ['sale_price', 'exception', 'discount',
                   'user_creation', 'date_creation', 'user_update',
                   'date_update', 'category', 'tax', 'date_expiration']


class BulkPriceUpdateForm(Form):
    """
    Formulario para filtros y parámetros de actualización masiva de precios.
    """
    CHOICES_STOCK = [
        ('0', 'Todo el stock'),
        ('1', 'Productos sin stock'),
        ('2', 'Productos con stock'),
        ('3', 'Productos con bajo stock'),
    ]
    CHOICES_UPDATE_TYPE = [
        ('percentage', 'Porcentaje (%)'),
        ('fixed', 'Valor fijo'),
    ]

    category = ChoiceField(
        required=False,
        widget=Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%',
            'autocomplete': 'off',
        })
    )
    unit = ChoiceField(
        required=False,
        widget=Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%',
            'autocomplete': 'off',
        })
    )
    stock = ChoiceField(
        choices=CHOICES_STOCK,
        widget=Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%',
            'autocomplete': 'off',
        })
    )
    product = ChoiceField(
        required=False,
        widget=Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%',
            'autocomplete': 'off',
        })
    )
    update_type = ChoiceField(
        choices=CHOICES_UPDATE_TYPE,
        widget=Select(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
        })
    )
    update_value = DecimalField(
        required=False,
        max_digits=10,
        decimal_places=4,
        widget=NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 15 (aumento) o -10 (disminución)',
            'step': '0.01',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [('', 'Todas las categorías')] + [
            (c.pk, c.name) for c in Category.objects.all().order_by('name')
        ]
        self.fields['unit'].choices = [('', 'Todas las unidades')] + [
            (u.pk, u.name) for u in Unit_Measure.objects.all().order_by('name')
        ]
        self.fields['product'].choices = [('', 'Todos los productos')]
