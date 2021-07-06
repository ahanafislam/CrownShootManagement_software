from django.shortcuts import redirect


#Don't Allow authenticated user to view login page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('invoice_list')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func