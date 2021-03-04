from django.contrib import admin
from django.urls import path, include

# Para servir los archivos media en modo desarrollo
from django.conf import settings
from django.conf.urls.static import static

from core.login.views import LoginEmptyFormView

urlpatterns = [
    path('', LoginEmptyFormView.as_view(), name='login_empty'),
    path('admin/', admin.site.urls),
    path('login/', include('core.login.urls')),
    path('sale/', include('core.sale.urls')),
    path('stock/', include('core.stock.urls')),
    path('report/', include('core.report.urls')),
    path('purchase/', include('core.purchase.urls')),
    path('money/', include('core.money.urls')),
    path('setting/', include('core.setting.urls')),
    path('client_current_account/', include('core.client_current_account.urls')),
]

# Para servir los archivos media en modo desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
