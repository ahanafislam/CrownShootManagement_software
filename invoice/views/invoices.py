from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from invoice.models import Client, Invoice, Package, Venue
from invoice.invoive_no_generator import invoive_no_gen
from invoice.choices import program_type


#For Showing List Of Invoice
@login_required
def invoice_list(request):
        invoices = Invoice.objects.order_by('-invoice_date')

        if 'search' in request.GET:
            search = request.GET['search']
            if search:
                invoices = invoices.filter(Q(invoice_no=search) | Q(event_name=search) | Q(client_name__phone=search) | Q(due_date=search))

        if 'status' in request.GET:
            status = request.GET['status']
            if status:
                invoices = invoices.filter(payment_status__iexact=status)

        paginator = Paginator(invoices,30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'invoices': page_obj,
        }

        return render(request,"invoice/invoice_list.html", context)

#For Delete Invoice
@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.delete()
    messages.error(request,"The Invoice Has Been Deleted.")
    return HttpResponseRedirect(reverse('invoice_list'))

#For Showing Invoice Detail View
@login_required
def invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice,pk=invoice_id)
    package = Package.objects.order_by('package_code')
    venue = Venue.objects.order_by('venue_name')
    context = {
        'invoice' : invoice,
        'packages' : package,
        'venues' : venue,
        'program_type' : program_type,
    }
    return render(request,"invoice/invoice.html", context)


#For Update Invoice
@login_required
def update_invoice(request,invoice_id):
    invoice = get_object_or_404(Invoice,pk=invoice_id)
    package = Package.objects.order_by('package_code')
    venue = Venue.objects.order_by('venue_name')
    context = {
        'invoice' : invoice,
        'packages' : package,
        'venues' : venue,
        'program_type' : program_type,
    }

    try:
        event_name = str(f"{request.POST['groom']} & {request.POST['bride']}")
        invoice.payment_status = request.POST['payment_status']
        invoice.groom_name = request.POST['groom']
        invoice.bride_name = request.POST['bride']
        invoice.due_date = request.POST['due_date']
        invoice.event_name = event_name
        invoice.save()
        messages.warning(request,"Client's Invoice Information Has been updated !")

    except (KeyError, Invoice.DoesNotExist):
        messages.error(request,"Invoice Is Not Available !")
        return redirect('invoice_list')
            
    
    else:
        return render(request,"invoice/invoice.html", context)


#For Updat Invoice Price
@login_required
def update_invoice_price(request,invoice_id):
    invoice = get_object_or_404(Invoice,pk=invoice_id)
    package = Package.objects.order_by('package_code')
    venue = Venue.objects.order_by('venue_name')
    context = {
        'invoice' : invoice,
        'packages' : package,
        'venues' : venue,
        'program_type' : program_type,
    }

    try:
        invoice.advance = request.POST['advance']
        invoice.discount = request.POST['discount']
        invoice.save()
        messages.warning(request,"Client's Invoice Price Has been updated !")

    except (KeyError, Invoice.DoesNotExist):
        return render(request, 'invoice/invoice.html',context)
    
    else:
        return render(request,"invoice/invoice.html", context)


#For Creating New Invoice
@login_required
def new_invoice(request):
    queryset_list = Client.objects.order_by('-join_date')
    search_list = ""

    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            search_list = queryset_list.filter(phone__icontains=search)
    
    else:
        search_list = ""

    if request.method=='POST':
        try:
            invoice_no = invoive_no_gen()
            client_id = request.POST['btnradio']
            client = get_object_or_404(Client, pk=client_id)
            invoice = Invoice(client_name=client,payment_status='Unpaid',invoice_no=invoice_no)
            invoice.save()
            return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))
        
        except (KeyError, Client.DoesNotExist):
            messages.error(request,"Please Search And Select Client Before Creating Any Invoice. If You Not Found Your Client Please Click On ' Create New Client ' Button.")

    context = {
        'clients' : search_list,
    }
    
    return render(request,'invoice/new_invoice.html',context)

#For Printing Invoice
@login_required
def print_invoice(request,print_invoice_id):
    invoice = get_object_or_404(Invoice,pk=print_invoice_id)
    context = {
        'invoice' : invoice,
    }
    return render(request,'invoice/print_invoice.html',context)
