from django.urls import path
from .views import PurchaseTicket,PurchasedTicketNo
urlpatterns = [
    path('purchase/', PurchaseTicket.as_view()),
    path('purchased_ticket/<str:Ticket_id>/', PurchasedTicketNo.as_view()),
#    path('ticket-info/', stream_updates,name='ticket_count_sse'),
] 