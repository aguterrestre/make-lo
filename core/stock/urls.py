from django.urls import path
from core.stock.views.product.views import ProductListView, ProductCreateView
from core.stock.views.product.views import ProductUpdateView, ProductDeleteView

app_name = 'stock'

urlpatterns = [
    # client
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<pk>/', ProductUpdateView.as_view(),
         name='product_update'),
    path('product/del/<pk>/', ProductDeleteView.as_view(),
         name='product_delete'),
]
