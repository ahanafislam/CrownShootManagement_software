from django.urls import path
from .views import client, invoices, items

urlpatterns = [
    ## Client ##
    path('client_list/',client.client_list,name='client_list'),
    path('client/<int:client_id>/',client.client_deatils,name='client_details'),
    path('client/<int:client_id>/update',client.update_client,name='update_client'),
    path('client/<int:client_id>/delete/',client.delete_client,name='delete_client'),
    path('create_client/',client.create_client,name='create_client'),

    ## Invoice ##
    path('',invoices.invoice_list,name='invoice_list'),
    path('<int:invoice_id>/delete_invoice/',invoices.delete_invoice,name='delete_invoice'),
    path('new_invoice/',invoices.new_invoice,name='new_invoice'),
    path('<int:invoice_id>/',invoices.invoice,name='invoice'),
    path('<int:invoice_id>/update/',invoices.update_invoice,name='update_invoice'),
    path('<int:invoice_id>/update_price/',invoices.update_invoice_price,name='update_invoice_price'),
    path('<int:print_invoice_id>/print_invoice/',invoices.print_invoice, name='print_invoice'),

    ## Invoice Item ##
    path('<int:invoice_id>/item/add/',items.add_item, name='add_item'),
    path('<int:invoice_id>/item/<int:invoiceitem_id>/delete/',items.delete_item, name='delete_item'),
]
