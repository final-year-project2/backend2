from django.urls import path
from .views import PurchaseTicket,TicketCountSseView
from sse_wrapper.views import EventStreamView
urlpatterns = [
    path('purchase/', PurchaseTicket.as_view()),
    
   path('ticket-info/<int:ticket_id>/', TicketCountSseView.as_view(), name='ticket_count_sse')

] 