from django.urls import path
from . import views
from .views import SellerCategoryPercentageAPIView
urlpatterns = [
    path('<int:pk>/category-percentages/', SellerCategoryPercentageAPIView.as_view(), name='seller-category-percentages'),
]
