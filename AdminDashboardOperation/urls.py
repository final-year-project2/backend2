from django.urls import path, include
from.views import UserCountView,TransactionHistory  # Adjust the import based on where your views.py is located

urlpatterns = [
    path('user_number/', UserCountView.as_view()),
    path('Total_trunsaction/', TransactionHistory.as_view()),
]