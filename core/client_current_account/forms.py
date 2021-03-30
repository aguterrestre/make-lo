from django import forms
from datetime import datetime

from .models import ClientReceipt


class ClientReceiptForm(forms.ModelForm):
    """ Formulario para registar la cabecera de un recibo de cliente """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puesto
        self.fields['center'].initial = 1
        # Último número de recibo
        self.fields['number'].initial = ClientReceipt.get_next_receipt_number(self)

    class Meta:
        model = ClientReceipt
        fields = ['client', 'total', 'letter', 'center', 'number', 'date_joined']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'id': 'client',
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
            }),
            'letter': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'disabled': True,
            }),
            'center': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'disabled': True,
            }),
            'number': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'autocomplete': 'off',
                'disabled': True,
            }),
            'date_joined': forms.DateInput(format='%Y-%m-%d',
                                           attrs={
                                                'value': datetime.now().strftime('%Y-%m-%d'),
                                                'autocomplete': 'off',
                                                'class': 'form-control datetimepicker-input',
                                                'id': 'date_joined',
                                                'data-target': '#date_joined',
                                                'data-toggle': 'datetimepicker'
                                           })
        }
