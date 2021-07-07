from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q #For Quaey Multaple Search
from django.contrib import messages
from django.core.paginator import Paginator
from invoice.choices import district_list, divisions_list
from invoice.models import Client, Invoice
from invoice.invoive_no_generator import invoive_no_gen


#For Creating New Client
@login_required
def create_client(request):
    context = {
        'district_list' : district_list,
        'divisions_list' : divisions_list,
    }
    if request.method == 'POST':
        if Client.objects.filter(phone=request.POST['phoneNumber']).exists():
            messages.error(request,'This Phone Number is already exist! Please Try With Different Phone Number! ')
            return redirect('create_client')
        
        # In this conditon we are filter all email that's not null or blank from Client Model
        if Client.objects.exclude(email__isnull=True).exclude(email__exact='').filter(email=request.POST['email']).exists():
            messages.error(request,'This Email ID is already exist! Please Try With Different Email ID! ')
            return redirect('create_client')
        
        else:
            client = Client(
                name=request.POST['fullName'],
                phone=request.POST['phoneNumber'],
                email=request.POST['email'],
                address=request.POST['address'],
                district=request.POST['district'],
                division=request.POST['division'],
                facebook_link=request.POST['facebook'],
                descriptions=request.POST['description'],
            )
            client.save()
            messages.success(request,f'{client.name} has been added to the client list!')

            if 'savecreate' in request.POST:
                invoice_no = invoive_no_gen()
                invoice = Invoice(client_name=client, payment_status='Unpaid', invoice_no=invoice_no)
                invoice.save()
                return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))
            
            else:
                return redirect('create_client')

    else:
        return render(request,'invoice/create_client.html',context)

#For Showing List Of Client
@login_required
def client_list(request):
        clients = Client.objects.order_by('-join_date')

        if 'search' in request.GET:
            search = request.GET['search']
            if search:
                clients = clients.filter(Q(name=search) | Q(phone=search) | Q(email=search))

        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'Old':
                clients = clients.order_by('join_date')

        #Search by Division
        if 'division' in request.GET:
            division = request.GET['division']
            if division:
                clients = clients.filter(division__iexact=division)

        #Search by district
        if 'district' in request.GET:
            district = request.GET['district']
            if district:
                clients = clients.filter(district__iexact=district)

        #Paginations
        paginator = Paginator(clients,30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'clients': page_obj,
            'district_list' : district_list,
            'divisions_list' : divisions_list,
        }

        return render(request,"invoice/client_list.html", context)


#In Client Deatils users can view details
@login_required
def client_deatils(request,client_id):
    client = get_object_or_404(Client,pk=client_id)
    invoices = Invoice.objects.filter(client_name = client)

    context = {
        'client' : client,
        'district_list' : district_list,
        'divisions_list' : divisions_list,
        'invoices' : invoices,
    }

    return render(request,'invoice/client_details.html',context)


#For Update Client Informations
@login_required
def update_client(request,client_id):
    client = get_object_or_404(Client,pk=client_id)

    # This will check 'is this phone number is match with other client's phone number without this client ?'
    if Client.objects.exclude(id__exact=client_id).filter(phone=request.POST['phoneNumber']).exists():
        messages.error(request,'This Phone Number is already exist! Please Try With Different Phone Number! ')
        return HttpResponseRedirect(reverse('client_details', args=(client.id,)))

    # In this conditon we are filter all email that's not null or blank from Client Model
    if Client.objects.exclude(email__isnull=True).exclude(email__exact='').exclude(id__exact=client_id).filter(email=request.POST['email']).exists():
        messages.error(request,'This Email ID is already exist! Please Try With Different Email ID! ')
        return HttpResponseRedirect(reverse('client_details', args=(client.id,)))

    client.name = request.POST['fullName']
    client.phone = request.POST['phoneNumber']
    client.email = request.POST['email']
    client.address = request.POST['address']
    client.district = request.POST['district']
    client.division = request.POST['division']
    client.facebook_link = request.POST['facebook']
    client.descriptions = request.POST['description']
    client.save()
    messages.warning(request,"Client's Information Has been updated !")

    if 'savecreate' in request.POST:
        invoice_no = invoive_no_gen()
        invoice = Invoice(client_name=client, payment_status='Unpaid', invoice_no=invoice_no)
        invoice.save()
        return HttpResponseRedirect(reverse('invoice', args=(invoice.id,)))

    return HttpResponseRedirect(reverse('client_details', args=(client.id,)))


#For Delete Client
@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    invoices = Invoice.objects.filter(client_name = client)
    
    if invoices:
        messages.error(request,"You Can't Delete Any Client If They Have Any Invoice.")
        return redirect('client_list')

    else:        
        client.delete()
        messages.error(request,"The Client Has Been Deleted.")
        return redirect('client_list')
