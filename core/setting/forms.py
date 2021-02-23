from django.forms import ModelForm, TextInput, DateInput, Select
from django.forms import EmailInput
from core.setting.models import Company


class CompanyForm(ModelForm):
    """
    Clase para crear el formulario de empresa
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = ['name', 'address', 'contact_email', 'fiscal_condition', 'document_type', 'document',
                  'document_IIBB', 'date_activity_start']
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
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
            'fiscal_condition': Select(),
            'document_type': Select(),
            'document': TextInput(
                attrs={
                    'placeholder': 'Ingrese su documento',
                }
            ),
            'document_IIBB': TextInput(
                attrs={
                    'placeholder': 'Ingrese su documento de ingresos brutos',
                }
            ),
            'date_activity_start': DateInput(format='%Y-%m-%d',
                                             attrs={
                                                    'class': 'datetimepicker-input',
                                                    'id': 'date_activity_start',
                                                    'data-target': '#date_activity_start',
                                                    'data-toggle': 'datetimepicker'
                                             })
        }
