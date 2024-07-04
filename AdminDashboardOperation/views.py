
from UserAccount.models import userAccountModel,Transaction
from Product.models import Seller,Ticket
from PurchasedTicket.models import PurchasedTicket
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import DecimalField, Sum

class UserCountView(APIView):
      def get(self, request, format=None):
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
            "start_of_22_28":end_of_15_21day,
            "start_of_15_21":start_of_22_28day,
            "start_of_8_14":start_of_8_14day,
            "start_of_1_7":start_of_1_7day,
            # "secondWeekWeackTransaction":total_second_week,
            })
