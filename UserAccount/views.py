from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .models import userAccountModel
from .serializer import UserAcountSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        token['is_active_user'] = user.is_active
        token['is_staf_user'] = user.is_staff
        token['is_superUser'] = user.is_superuser
        token['can_add_user'] = user.has_perm('Can add user')
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserAcount(generics.CreateAPIView):
    queryset = userAccountModel.objects.all()
    serializer_class = UserAcountSerializer