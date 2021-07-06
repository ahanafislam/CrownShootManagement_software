from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from invoice.models import Invoice, InvoiceItem, Package

# Add invoiceitem to invoice
@login_required
def add_item(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    package = Package.objects.get(package_code=request.POST['packages'])
    try:
        invoiceItem = invoice.invoiceitem_set.create(
            event_date_time = request.POST['date_time'],
            event_period = request.POST['event_period'],
            venue = request.POST['venue'],
            program_name = request.POST['program_type'],
            packages = request.POST['packages'],
            price = package.price,
        )
        invoiceItem.save()

    except (KeyError, Invoice.DoesNotExist):
            return redirect('invoice_list')
    
    else:
        return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))


# Delete invoiceitem to invoice
@login_required
def delete_item(request, invoiceitem_id, invoice_id):
	item = get_object_or_404(InvoiceItem, pk=invoiceitem_id)
	invoice = get_object_or_404(Invoice, pk=invoice_id)
	try:
		item.delete()

	except (KeyError, InvoiceItem.DoesNotExist):
		return redirect('invoice_list')

	else:
		return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))
