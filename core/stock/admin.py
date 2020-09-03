from django.contrib import admin
from core.stock.models import Tax_IVA, Unit_Measure, Product_Image, Category
from core.stock.models import Product

admin.site.register(Tax_IVA)
admin.site.register(Unit_Measure)
admin.site.register(Product_Image)
admin.site.register(Category)
admin.site.register(Product)
