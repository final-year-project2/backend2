from django.urls import path
from . import views
from .views import SellerCategoryPercentageAPIView,FrequentBuyer
urlpatterns = [
    path('<int:pk>/category-percentages/', SellerCategoryPercentageAPIView.as_view(), name='seller-category-percentages'),
    path('frequent_buyer/<int:seller_id>/', FrequentBuyer.as_view(), name='frequentBuyer'),
]
