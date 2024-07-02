from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Product.models import Seller
from .serializers import PichartSerializer

class SellerCategoryPercentageAPIView(APIView):
    """
    Retrieve category percentages for a given seller.
    """
    def get_object(self, pk):
        try:
            return Seller.objects.get(pk=pk)
        except Seller.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seller = self.get_object(pk)
        serializer = PichartSerializer(seller)
        return Response(serializer.data)

# Assuming your Django app is named 'myapp', add the following to myapp/urls.py
# from django.urls import path
# from .views import SellerCategoryPercentageAPIView
# urlpatterns = [
#     path('sellers/<int:pk>/category-percentages/', SellerCategoryPercentageAPIView.as_view(), name='seller-category-percentages'),
# ]
# Create your views here.
