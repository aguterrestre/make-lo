from django.urls import path
from core.money.views import MoneyDashboardView

app_name = 'money'

urlpatterns = [
    path('dashboard/', MoneyDashboardView.as_view(), name='money_dashboard'),
]
