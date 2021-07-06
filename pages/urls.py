from django.urls import path
from .views import HomeView

urlpatterns = [
    path('dash', HomeView.as_view(), name='home'),
]
