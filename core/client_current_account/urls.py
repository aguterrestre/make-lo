from django.urls import path
from core.client_current_account import views

app_name = 'client_current_account'

urlpatterns = [
    # client_current_account
    path('list/', views.ClientCurrentAccountListView.as_view(), name='client_current_account_list'),
    path('receipt/list/', views.ClientReceiptListView.as_view(), name='client_receipt_list'),
    path('receipt/add/', views.ClientReceiptCreateView.as_view(), name='client_receipt_create'),
    path('receipt/pdf/<int:pk>/', views.ClientReceiptCreatePDFView.as_view(), name='client_receipt_pdf'),
]
