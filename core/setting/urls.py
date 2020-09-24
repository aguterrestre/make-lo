from django.urls import path

from core.setting.views import CompanyUpdateView

app_name = 'setting'

urlpatterns = [
    path('company/edit/<int:pk>/', CompanyUpdateView.as_view(),
         name='company_update'),
]
