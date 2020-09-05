from django.urls import path
from core.purchase.views.provider.views import ProviderListView, ProviderCreateView
from core.purchase.views.provider.views import ProviderUpdateView, ProviderDeleteView
# from core.sale.views.ticket.views import TicketListView, TicketCreateView
# from core.sale.views.ticket.views import TicketCreatePDFView

app_name = 'purchase'

urlpatterns = [
    # client
    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/edit/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/del/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # ticket
    # path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    # path('ticket/add/', TicketCreateView.as_view(), name='ticket_create'),
    # path('ticket/pdf/add/<int:pk>/', TicketCreatePDFView.as_view(),
    #      name='ticket_create_pdf'),
]
