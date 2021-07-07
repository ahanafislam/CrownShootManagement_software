from django.contrib import admin
from invoice.models import Client, Invoice, Package, Venue, InvoiceItem

admin.site.register(Client)
# admin.site.register(InvoiceItem)
# admin.site.register(Invoice)
admin.site.register(Package)
admin.site.register(Venue)

