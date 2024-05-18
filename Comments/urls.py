from django.urls import path
from .views import TicketComment
urlpatterns = [
    path('', TicketComment.as_view()),
] 