from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('CS@dmin/', admin.site.urls),
    path('dash',include('pages.urls')),
    path('',include('invoice.urls')),
    path('account/',include('accounts.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
