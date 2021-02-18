from django.forms import ModelForm, TextInput, DateInput, Select
from django.forms import EmailInput, NumberInput
from django_afip import models as django_afip
from datetime import datetime
from core.sale.models import Client, Ticket


class ClientForm(ModelForm):
    """
    Clase para crear el formulario de cliente
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
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
            'sales_email': EmailInput(
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
                                            # 'value': datetime.now().strftime('%Y-%m-%d'),
                                            'placeholder': 'Ejemplo: 1989-02-18 (formato año-mes-día)',
                                       }
                                       ),
            'gender': Select(),
            'document_type': Select(),
            'fiscal_condition': Select()
        }
        exclude = ['business_name', 'trade_name', 'comercial_address',
                   'user_creation', 'date_creation', 'user_update',
                   'date_update', 'photo', 'residence_city', 'status', 'sale_condition']


class TicketForm(ModelForm):
    """
    Clase para crear el formulario de venta. Lo usaremos para la cabecera de la venta.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puesto común por id
        self.fields['center'].initial = 2
        # Factura C por id
        self.fields['voucher_type'].initial = 19
        # Filtro tipos de comprobantes. Solo Factura C
        self.fields['voucher_type'].queryset = django_afip.ReceiptType.objects.filter(pk=19)
        # Último núm de comprob
        self.fields['number'].initial = Ticket.get_next_ticket_number(self, 2, 19)

    class Meta:
        model = Ticket
        fields = ['client', 'voucher_type', 'letter', 'center', 'number', 'date_joined', 'sale_condition',
                  'subtotal', 'total_tax', 'total']
        widgets = {
            'client': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autocomplete': 'off',
            }),
            'voucher_type': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autocomplete': 'off',
            }),
            'letter': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'disabled': True,
            }),
            'center': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
            }),
            'number': NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'readonly': True,
            }),
            'date_joined': DateInput(format='%Y-%m-%d',
                                     attrs={
                                            'value': datetime.now().strftime('%Y-%m-%d'),
                                            'autocomplete': 'off',
                                            'class': 'form-control datetimepicker-input',
                                            'id': 'date_joined',
                                            'data-target': '#date_joined',
                                            'data-toggle': 'datetimepicker'
                                     }),
            'sale_condition': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autocomplete': 'off',
            }),
            'subtotal': DateInput(attrs={
                                        'readonly': True,
                                        'class': 'form-control',
                                        'style': 'width: 100%',
                                        'autocomplete': 'off',
                                }),
            'total_tax': DateInput(attrs={
                                        'readonly': True,
                                        'class': 'form-control',
                                        'style': 'width: 100%',
                                        'autocomplete': 'off',
                                }),
            'total': DateInput(attrs={
                                        'readonly': True,
                                        'class': 'form-control',
                                        'style': 'width: 100%',
                                        'autocomplete': 'off',
                                })
        }
