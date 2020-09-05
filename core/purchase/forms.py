from django.forms import ModelForm, TextInput, DateInput, Select
from django.forms import EmailInput

from datetime import datetime

from core.purchase.models import Provider, Invoice


class ProviderForm(ModelForm):
    """
    Clase para crear el formulario de proveedor
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'surname': TextInput(
                attrs={
                    'placeholder': 'Ingrese su apellido',
                }
            ),
            'document': TextInput(
                attrs={
                    'placeholder': 'Ingrese su documento',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'contact_email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese su email de contacto',
                }
            ),
            'purchase_email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese su email de facturación',
                }
            ),
            'telephone': TextInput(
                attrs={
                    'placeholder': 'Ingrese su teléfono',
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                                       attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       )
        }
        exclude = ['business_name', 'trade_name', 'comercial_address',
                   'user_creation', 'date_creation', 'user_update',
                   'date_update', 'document_type', 'fiscal_condition',
                   'photo', 'residence_city', 'purchase_condition',
                   'status']


class InvoiceForm(ModelForm):
    """
    Clase para crear el formulario de compra. Lo usaremos para la cabecera de la compra.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].widget.attrs['autofocus'] = True

    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'provider': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
            }),
            'voucher_type': Select(),
            'date_joined': DateInput(format='%Y-%m-%d',
                                     attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                            'autocomplete': 'off',
                                            'class': 'form-control datetimepicker-input',
                                            'id': 'date_joined',
                                            'data-target': '#date_joined',
                                            'data-toggle': 'datetimepicker'
                                     }),
            'subtotal': DateInput(attrs={
                                        'readonly': True,
                                }),
            'total_tax': DateInput(attrs={
                                        'readonly': True,
                                }),
            'total': DateInput(attrs={
                                        'readonly': True,
                                })
        }
        exclude = ['letter', 'center', 'number', 'purchase_condition',
                   'date_creation', 'user_creation', 'user_update',
                   'date_update']
