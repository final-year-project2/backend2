from django.urls import path
from .views import  SaveTicketView,BecomeSellerAPIView, CheckSellerView ,RetriveTicketList,RetriveSingleSellerTickets,AllTicketList
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views
app_name = 'Product'
urlpatterns = [
    path('save-ticket/', SaveTicketView.as_view(), name='save-ticket'),
    path('become_seller/',BecomeSellerAPIView.as_view(), name='become_seller'),
    path('check_seller/', CheckSellerView.as_view(), name='check_seller'),
    path('ticket-list/<str:prize_categories>', RetriveTicketList.as_view(), name='ticket-list'),
    path('ticket_list/', AllTicketList.as_view()),
    path('ticket_list/<str:seller>', RetriveSingleSellerTickets.as_view(), name='ticket-list'),
]

