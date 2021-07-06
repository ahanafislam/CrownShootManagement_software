from invoice.models import Invoice
from datetime import date

# Automatic invoice_no generator #
def invoive_no_gen():
    today = date.today()
    today_string = today.strftime('%y%m%d')
    next_invoice_number = '01'
    last_invoice = Invoice.objects.filter(invoice_no__startswith=today_string).order_by('invoice_no').last()
    if last_invoice:
        last_invoice_number = int(last_invoice.invoice_no[6:])
        next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
    invoice_no = today_string + next_invoice_number
    
    return invoice_no