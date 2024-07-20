from django.urls import path
from .views import TicketComment,SingleTicketComment
urlpatterns = [
    path('', TicketComment.as_view()),
    path('<str:Ticket_id>/', SingleTicketComment.as_view()),
] 