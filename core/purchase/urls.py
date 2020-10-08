from django.urls import path
from core.purchase.views.provider.views import ProviderListView, ProviderCreateView
from core.purchase.views.provider.views import ProviderUpdateView, ProviderDeleteView
from core.purchase.views.invoice.views import InvoiceListView, InvoiceCreateView, InvoiceCreatePDFView
from core.purchase.views.invoice.views import InvoiceDeleteView

app_name = 'purchase'

urlpatterns = [
    # provider
    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/edit/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/del/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # invoice
    path('invoice/list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/pdf/add/<int:pk>/', InvoiceCreatePDFView.as_view(), name='invoice_create_pdf'),
    path('invoice/del/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
]
