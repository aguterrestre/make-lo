from django.contrib import admin

from core.purchase.models import Purchase_Condition, Provider_Photo, Provider_Status
from core.purchase.models import Provider, Invoice, Invoice_Detail

admin.site.register(Purchase_Condition)
admin.site.register(Provider_Photo)
admin.site.register(Provider_Status)
admin.site.register(Provider)
admin.site.register(Invoice)
admin.site.register(Invoice_Detail)
