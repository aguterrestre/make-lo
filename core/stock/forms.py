from django.forms import ModelForm, TextInput, NumberInput, DateInput, Select
from core.stock.models import Product


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
            'date_expiration': DateInput(format='%Y-%m-%d',
                                         # attrs={
                                         #         'class': 'datetimepicker-input',
                                         #        'id': 'date_expiration',
                                         #        'data-target': '#date_expiration',
                                         #        'data-toggle': 'datetimepicker'
                                         # }
                                         ),
            'unit': Select(),
        }
        exclude = ['sale_price', 'exception', 'discount',
                   'user_creation', 'date_creation', 'user_update',
                   'date_update', 'category', 'tax']
