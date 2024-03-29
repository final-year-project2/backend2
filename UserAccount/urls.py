from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
<<<<<<< HEAD
from .views import MyTokenObtainPairView,CreateUserAcount,ActivateUserAcount, ApiDocsView,PasswordReset,RegenerateOtp,getMyOtp
=======
from .views import MyTokenObtainPairView,CreateUserAcount,ActivateUserAcount, PasswordReset,RegenerateOtp,getVerificationNo,verifyVerificationNo
>>>>>>> f18e5ae2e91e40d38c26699494c53fc2613e3d3c
from django.urls import path

urlpatterns = [
    path('', ApiDocsView.as_view(),name='api-docs'),
    path('create/',CreateUserAcount.as_view()),
    path('activate/<int:pk>/',ActivateUserAcount.as_view()),
    path('otp/regenerate/<int:pk>/',RegenerateOtp.as_view()),
<<<<<<< HEAD
    path('getVerification/<int:pk>/',getMyOtp.as_view()),
    path('resetpassword/<int:pk>/',PasswordReset.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
=======
    path('getVerification/<str:Phone_no>/',getVerificationNo.as_view()),
    path('verifyVerification/<str:Phone_no>/',verifyVerificationNo.as_view()),
    path('resetpassword/<str:Phone_no>/',PasswordReset.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
>>>>>>> f18e5ae2e91e40d38c26699494c53fc2613e3d3c
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]