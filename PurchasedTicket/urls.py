from django.urls import path
from .views import PurchaseTicket
urlpatterns = [
    path('purchase/', PurchaseTicket.as_view()),
] 