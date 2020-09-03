from django.contrib import admin

from core.sale.models import Fiscal_Condition, Document_Type, Country, Province, City
from core.sale.models import Sale_Condition, Client_Photo, Client_Status, Client, Ticket
from core.sale.models import Ticket_Detail, Voucher_Type

admin.site.register(Fiscal_Condition)
admin.site.register(Document_Type)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Sale_Condition)
admin.site.register(Client_Photo)
admin.site.register(Client_Status)
admin.site.register(Client)
admin.site.register(Ticket)
admin.site.register(Ticket_Detail)
admin.site.register(Voucher_Type)
