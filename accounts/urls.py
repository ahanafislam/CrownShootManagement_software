from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserPasswordReset
from . import views

urlpatterns = [
    path('login/',views.loginPage,name='loginPage'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    #Url For Reset Password
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",form_class=UserPasswordReset),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_send.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"),
]

'''
##### RESET PASSWORD #####
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''