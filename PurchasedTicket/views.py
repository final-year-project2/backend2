from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from PurchasedTicket.models import PurchasedTicket
from .serializer import PurchasedTicketSerializer
class PurchaseTicket(generics.ListCreateAPIView):
    queryset = PurchasedTicket.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchasedTicketSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for ticket_data in serializer.validated_data:
            ticket_data['User_id'] = user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        qs =  super().get_queryset()
        user = self.request.user
        return qs.filter(User_id = user)

