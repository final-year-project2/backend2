
from UserAccount.models import userAccountModel,Transaction
from Product.models import Seller,Ticket
from PurchasedTicket.models import PurchasedTicket
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import DecimalField, Sum
from django.utils import timezone
from Product.models import Seller
from Product.serializers import SellerSerializer
class UserCountView(APIView):
      def get(self, request, format=None):
        print('this is yihenew')
        print(timezone.now().day)
        user_count = userAccountModel.objects.count()
        Seller_count = Seller.objects.count()
        Ticket_count = Ticket.objects.count()
        solledTicket_count = PurchasedTicket.objects.count()
        content = {
            'user_count': user_count,
            "seller_count":Seller_count,
            "ticket_count":Ticket_count,
            "solled_count":solledTicket_count,
            }
        return Response(content)
      

class UserStausCount(APIView):
    def get(self, request, format=None):
        user = user_count = userAccountModel.objects.count()
        Active_user = userAccountModel.objects.filter(is_active = True)
        Not_Active_user = userAccountModel.objects.filter(is_active = False)
        staff_user = userAccountModel.objects.filter(is_staff = True)
        UserStausCount = {
            "Total_user":user,
            "Active_user":Active_user.count(),
            "Not_Active_user":Not_Active_user.count(),
            "staff_user":staff_user.count()
        }
        return Response(UserStausCount)


class TransactionHistory(APIView):
      def get(self, request, format=None):
        
        withdrawals = Transaction.objects.filter(transaction_type='withdrawal')
        total_withdrawals = withdrawals.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        start_of_29_30 = Transaction.objects.filter( transaction_date__range = [29,30])
        start_of_29_28day = start_of_29_30.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        start_of_22_28 = Transaction.objects.filter( transaction_date__range = [22,28])
        start_of_22_28day = start_of_22_28.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        start_of_15_21 = Transaction.objects.filter( transaction_date__range = [15,21])
        end_of_15_21day = start_of_15_21.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        start_of_8_14 = Transaction.objects.filter( transaction_date__range = [8,14])
        start_of_8_14day = start_of_8_14.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        start_of_1_7 = Transaction.objects.filter( transaction_date__range = [1,7])
        start_of_1_7day = start_of_1_7.aggregate(total_amount=Sum('amount', output_field=DecimalField()))['total_amount']

        return Response({
            "total_Transaction":total_withdrawals,
            "start_of_29_30":start_of_29_28day,
            "start_of_22_28":start_of_22_28day,
            "start_of_15_21":end_of_15_21day ,
            "start_of_8_14":start_of_8_14day,
            "start_of_1_7":start_of_1_7day,
            # "secondWeekWeackTransaction":total_second_week,
            })

class SellerList(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class SingleSellerInfo(generics.RetrieveAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
class TicketCatagoryStatics(APIView):
    def get(self, request, format=None):
        electronics = Ticket.objects.filter(prize_categories = "electronics").count()
        car = Ticket.objects.filter(prize_categories = "car").count()
        home = Ticket.objects.filter(prize_categories = "home").count()
        other = Ticket.objects.filter(prize_categories = "other").count()
        total = Ticket.objects.count()
        return Response({
            "total":total,
            "electronics":electronics,
            "car":car,
            "home":home,
            "other":other,
        })