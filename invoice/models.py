from __future__ import division, unicode_literals
from django.db import models
from datetime import datetime

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    facebook_link = models.URLField(blank=True,null=True)
    descriptions = models.TextField(blank=True,null=True)
    join_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    #Calculate How Many Invoice Is Create By This Client
    def number_of_invoice(self):
        return Invoice.objects.filter(client_name=self).count()


class Invoice(models.Model):
    client_name = models.ForeignKey(Client,on_delete=models.SET_NULL,blank=True,null=True)
    groom_name = models.CharField(max_length=255,blank=True,null=True,default="")
    bride_name = models.CharField(max_length=255,blank=True,null=True,default="")
    invoice_no = models.CharField(max_length=255,blank=True,null=True)
    invoice_date = models.DateTimeField(default=datetime.now,blank=True,null=True)
    due_date = models.CharField(max_length=255,blank=True,null=True,default="")
    advance = models.IntegerField(blank=True,null=True,default=0)
    due_amount = models.IntegerField(blank=True,null=True,default=0)
    payment_status = models.CharField(max_length=25,blank=True,null=True)
    discount = models.IntegerField(blank=True,null=True,default=0)
    total_income = models.IntegerField(blank=True,null=True,default=0)
    event_name = models.CharField(max_length=255,blank=True,null=True)

    def paid(self):
        return self.payment_status == 'Paid'
		
    def unpaid(self):
        return self.payment_status == 'Unpaid'
		
    def due(self):
        return self.payment_status == 'Due'

    #Count Total Amount User Have to pay
    @property
    def get_item_total(self):
        invoiceitem = self.invoiceitem_set.all()
        total = sum([item.get_total for item in invoiceitem])
        return total - int(self.discount)

    #Calculate Total Due
    @property
    def get_due_amount(self):
        due_amount = int(self.get_item_total) - int(self.advance)
           
        if self.payment_status == 'Paid':
            due_amount = 0
        return due_amount

    def save(self, *args, **kwargs):
        if self.discount == "":
            self.discount = 0
        if self.payment_status == 'Paid':
            self.total_income = int(self.get_item_total)
        else:
            self.total_income = int(self.advance)
        super(Invoice, self).save(*args, **kwargs)


class Package(models.Model):
    package_name = models.CharField(max_length=255)
    package_code = models.CharField(max_length=255)
    duration = models.DurationField()
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.package_code


class Venue(models.Model):
    venue_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.venue_name


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    event_date_time = models.DateTimeField(blank=True,null=True)
    event_period = models.CharField(max_length=255,blank=True,null=True)
    venue = models.CharField(max_length=255,blank=True,null=True)
    program_name = models.CharField(max_length=255,blank=True,null=True)
    packages = models.CharField(max_length=255,blank=True,null=True)
    price = models.IntegerField(blank=True,null=True)

    #Calculate Total Item Price
    @property
    def get_total(self):
        total = self.price
        return total
