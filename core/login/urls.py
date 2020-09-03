from django.urls import path

from core.login.views import LoginFormView, LogoutFormView, DashboardView

app_name = 'login'

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
