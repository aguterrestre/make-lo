from django.urls import path
from core.sale.views.client.views import ClientListView, ClientCreateView
from core.sale.views.client.views import ClientUpdateView, ClientDeleteView
from core.sale.views.ticket.views import TicketListView, TicketCreateView
from core.sale.views.ticket.views import TicketCreatePDFView
from core.sale.views.tests.views import TestsAfipView

app_name = 'sale'

urlpatterns = [
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(),
         name='client_update'),
    path('client/del/<int:pk>/', ClientDeleteView.as_view(),
         name='client_delete'),
    # ticket
    path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/add/', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/pdf/add/<int:pk>/', TicketCreatePDFView.as_view(),
         name='ticket_create_pdf'),
    path('client/testafip/', TestsAfipView.as_view(), name='test_afip'),
]
