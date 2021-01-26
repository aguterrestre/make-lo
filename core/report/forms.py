from django.forms import Form, CharField, TextInput, Select, ChoiceField


class TicketReportForm(Form):
    date_joined_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    client = ChoiceField(widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))


class ClientReportForm(Form):
    date_creation_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    date_birthday_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    client = ChoiceField(widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))


class ProductReportForm(Form):
    date_expiration_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    product = ChoiceField(widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))
    choices_stock = [('0', 'Todo el stock'), ('1', 'Productos sin stock'), ('2', 'Productos con stock'),
                     ('3', 'Productos con bajo stock')]
    stock = ChoiceField(choices=choices_stock, widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))


class ProviderReportForm(Form):
    date_creation_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    date_birthday_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    provider = ChoiceField(widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))


class InvoiceReportForm(Form):
    date_joined_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    provider = ChoiceField(widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%',
        'autocomplete': 'off'
    }))
