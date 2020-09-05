from django.contrib import admin
from django.urls import path, include

# Para servir los archivos media en modo desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('core.login.urls')),
    path('sale/', include('core.sale.urls')),
    path('stock/', include('core.stock.urls')),
    path('report/', include('core.report.urls')),
    path('purchase/', include('core.purchase.urls')),
]

# Para servir los archivos media en modo desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
