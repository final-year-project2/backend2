from django.urls import path
from .views import SaveTicketView
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

app_name = 'Product'
urlpatterns = [
    path('save-ticket/', SaveTicketView.as_view(), name='save-ticket'),
    # Add more URL patterns as needed
]

