from django.forms import Select

from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter

from .models import ClientCurrentAccount
from core.sale.models import Client


class ClientCurrentAccountFilter(FilterSet):
    """
    Filtro de comprobantes de ventas en cuenta corriente de cliente.
    """

    status = ChoiceFilter(choices=ClientCurrentAccount.STATUS_TICKET_CURRENT_ACCOUNT, widget=Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%',
            'autocomplete': 'off',
    }))

    ticket__client = ModelChoiceFilter(queryset=Client.objects.all(), widget=Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%',
            'autocomplete': 'off'
    }))

    class Meta:
        model = ClientCurrentAccount
        fields = []
