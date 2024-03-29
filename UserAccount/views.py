from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from .models import userAccountModel
from .serializer import UserAcountSerializer
from rest_framework.response import Response
from twilio.rest import Client
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['is_active_user'] = user.is_active
        token['is_staf_user'] = user.is_staff
        token['is_superUser'] = user.is_superuser
        token['can_add_user'] = user.has_perm('Can add user')
        return token
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
            account_sid = 'AC3b149e8df13637611de9a595d354ca2c'
            auth_token = 'd0961b8aa6ad93f5411c2528cb990341'
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
            account_sid = 'AC3b149e8df13637611de9a595d354ca2c'
            auth_token = 'd0961b8aa6ad93f5411c2528cb990341'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f'Hello your verification number is {Otp}',
            from_='+13082223702',
            to=f'+251{phone_no}'
            )
            return Response('verification no send successfuly',status=status.HTTP_200_OK)
        except:
            return Response('messaging service dose not work try again',status=status.HTTP_400_BAD_REQUEST)
        

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
            