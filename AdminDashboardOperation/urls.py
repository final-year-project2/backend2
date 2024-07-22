from django.urls import path, include
from.views import UserCountView,TransactionHistory,UserStausCount,SellerList,SingleSellerInfo,TicketCatagoryStatics  # Adjust the import based on where your views.py is located

urlpatterns = [
    path('user_number/', UserCountView.as_view()),
    path('Total_trunsaction/', TransactionHistory.as_view()),
    path('UserStausCount/', UserStausCount.as_view()),
    path('sellerList/', SellerList.as_view()),
    path('sellerDetail/<int:pk>/',SingleSellerInfo.as_view()),
    path('TicketCatagorystatics/',TicketCatagoryStatics.as_view()),
]