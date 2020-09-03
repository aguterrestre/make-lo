from django.urls import path

from core.report.views.sale.ticket.views import ReportTicketView
from core.report.views.sale.client.views import ReportClientView
from core.report.views.stock.product.views import ReportProductView

app_name = 'report'

urlpatterns = [
    # reports
    path('ticket/', ReportTicketView.as_view(), name='ticket_report'),
    path('client/', ReportClientView.as_view(), name='client_report'),
    path('product/', ReportProductView.as_view(), name='product_report'),
]
