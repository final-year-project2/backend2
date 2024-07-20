from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from .models import userAccountModel,Wallet,Transaction
from .serializer import UserAcountSerializer,TransactionSerializer,WalletSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
import random
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import( ListAPIView,RetrieveAPIView)

import os
from dotenv import load_dotenv 
load_dotenv()

from rest_framework.renderers import TemplateHTMLRenderer
import logging



logger =logging.getLogger(__name__)










class ApiDocsView(APIView):
    
    def get(self,request,*args,**kwargs):
        api_endpoints =[
            {
                'path':"example/for/endpoint"
            }
        ]
        return Response(api_endpoints)
        
    
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['is_active_user'] = True
        token['is_staf_user'] = user.is_staff
        token['is_superUser'] = user.is_superuser 
        wallet=user.wallet
        if wallet:
            token['wallet_id'] = wallet.id
        else:
            token['wallet_id']=None
        token['can_add_user'] = user.has_perm('Can add user')
        return token  
    @classmethod 
    def get_token(cls,user):
        token = super().get_token(user)
        wallet = user.wallet
        print(f"walletid:{wallet.id}")
        if wallet:
            token['wallet_id'] = wallet.id
        else:
            token['wallet_id']=None
        return token
    def validate(self, attrs):
        data = super().validate(attrs)  # Corrected method call with parentheses
        data.update({
            'wallet_id': self.user.wallet.id if self.user.wallet else None,
            'user_id':self.user.id
        })
        return data

  
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    












"""this CreateUserAcount class is used to create user account"""
class CreateUserAcount(generics.CreateAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer


"""this ActivateUserAcount class used for activate user account"""
class ActivateUserAcount(generics.UpdateAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer

    def update(self, serializer, *args, **kwargs):
        instance = self.get_object()
        if(not instance.is_active and self.request.data['otp'] == instance.Otp and instance.Otp_expre_at):
            instance.is_active = True
            instance.Otp_expre_at = None
            instance.Maximum_otp_try = settings.MAX_OTP_TRY
            instance.Maximum_otp_out = None
            instance.save()
            return Response('Successfully activated',status=status.HTTP_200_OK)
        else:
            return Response('user alredy active or please inter correct otp ',status=status.HTTP_400_BAD_REQUEST)
        
"""this RegenerateOtp class is used for regenerate new otp """
class RegenerateOtp(generics.UpdateAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        phone_no = instance.Phone_no
        if int(instance.Maximum_otp_try) == 0 and timezone.now() < instance.Maximum_otp_out:
            return Response('Max otp try reacheded, try after an houre',status=status.HTTP_400_BAD_REQUEST)
        
        otp = random.randint(1000,9999)
        Maximum_otp_try = int(instance.Maximum_otp_try)-1
        Otp_expre_at = timezone.now() + timedelta(minutes=10)
        instance.Otp = otp
        instance.Maximum_otp_try = Maximum_otp_try
        instance.Otp_expre_at = Otp_expre_at
        if Maximum_otp_try==0:
            instance.Maximum_otp_out = timezone.now() + timedelta(hours=1)
        elif Maximum_otp_try== -1:
            instance.Maximum_otp_try = settings.MAX_OTP_TRY
        else:
            instance.Maximum_otp_out = None
            instance.Maximum_otp_try = Maximum_otp_try
        instance.save()
        try:
            account_sid = os.environ.get('ACCOUNT_SSID')
            auth_token = os.environ.get('AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f'Hello your Otp is {otp}',
            from_='+13082223702',
            to=f'+251{phone_no}'
            )
            print(message.sid)
        except:
            print('some thing went ')
        return Response('successfuly regenerated',status=status.HTTP_200_OK)
    


"""
this getVerificationNo class is used for to get verification no for password reset.
frome here may be you get 404 not found error so you have to consider it
"""
class getVerificationNo(generics.RetrieveAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer
    lookup_field = 'Phone_no'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Otp = instance.Otp
        phone_no = instance.Phone_no
        try:

            
            
            from_='+13109064102',
            account_sid = os.environ.get('ACCOUNT_SSID')
            auth_token = os.environ.get('AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f'Hello your verification number is {Otp}',
            from_='+13109064102',

            to=f'+251{phone_no}'
            )
            return Response('verification number send successfuly',status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'messaging service dose not work try again {e}',status=status.HTTP_400_BAD_REQUEST)
        

"""
this verufyVerificationNo class is used to authenticate wether the user inter the correct otp what we ssend befor request (getVerificationNo) request.
frome here may be you get 404 not found error so you have to consider it
"""
class verifyVerificationNo(generics.RetrieveAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer
    lookup_field = 'Phone_no'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if( self.request.data['otp'] == instance.Otp):
            return Response('correct verification no',status=status.HTTP_200_OK)
        else:
            return Response('incorrect verification no please use correct phone_no or correct verification_no',status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(generics.UpdateAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer
    lookup_field = 'Phone_no'
    def update(self, serializer, *args, **kwargs):
            instance = self.get_object()
            if(self.request.data['otp'] == instance.Otp):
                instance.set_password(self.request.data['password'])
                instance.save()
                return Response('password Successfully changed',status=status.HTTP_200_OK)
            else:

                return Response('incorrect verification Number or password dose not match ',status=status.HTTP_400_BAD_REQUEST)
        
            
            
class UpdateWallet(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    logger.debug('message')
    def post(self,request,*args, **kwargs) :
    
        wallet_id=kwargs['wallet_id']
        print(f"walletid:{wallet_id}")
        wallet = get_object_or_404(Wallet, id=wallet_id)
        if not wallet:
            return Response({"message":"user do not exists"},status=status.HTTP_400_BAD_REQUEST)
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            transaction = serializer.save(wallet=wallet)
            transaction.wallet=wallet
            logger.debug(f"Validated data: {serializer.validated_data}")
            
            
            if transaction.transaction_type == 'deposit':
                wallet.balance+=transaction.amount
            elif transaction.transaction_type == 'withdrawal':
                if wallet.balance < transaction.amount:
                    return Response({"message":"Insufficent amount"},status=status.HTTP_400_BAD_REQUEST)
                wallet.balance-=transaction.amount
            wallet.save()
            print(f'updated wallet balance :{wallet.balance}')
            
            transaction.save()
            print(f"serialized{serializer.data}")
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class RetriveWalletInformations(RetrieveAPIView):
    queryset=Wallet.objects.all()
    serializer_class=WalletSerializer
    lookup_field='id' 
        
class RetiveTransaction(ListAPIView):
    queryset=Transaction.objects.all().order_by('-transaction_date')
    serializer_class=TransactionSerializer
    lookup_field='wallet'
    
    

    
        

