from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserCreationForm, UserUpdateForm
from .decorators import unauthenticated_user

User = get_user_model()

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                first_name = request.user.first_name
                last_name = request.user.last_name
                messages.success(request, f'Welcome {first_name} {last_name}!')
                return redirect('invoice_list')
        
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('loginPage')
    
    else:
        return render(request, 'accounts/login.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_updateForm = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_updateForm.is_valid():
            u_updateForm.save()
            messages.success(request, f'Your account has been update!')
            return redirect('profile')
    
    else:
        u_updateForm =UserUpdateForm(instance=request.user)

    context = {
        'form' : u_updateForm
    }
    return render(request,'accounts/profile.html', context)


@login_required
def logout_view(request):
    auth.logout(request)
    messages.info(request, 'You are Logout.')
    return redirect('loginPage')
