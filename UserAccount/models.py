from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,User
from django.utils import timezone
from django.conf import settings

"""
AbstractBaseUser => that provides a foundation for creating custom user models with additional fields and functionalities.

PermissionsMixin => is a mixin class provided by Django that can be used in conjunction with the Django user model to add permission-related functionalities.

BaseUserManager => this class in Django is a base class provided by Django's authentication system for creating custom user.It provides a set of methods and attributes that help with managing user creation and manipulation

"""



class userAcountManager(BaseUserManager):
    def create_user(self,name,Phone_no,Otp,Otp_expre_at,Maximum_otp_try,Maximum_otp_out,password = None):
 
        if not name :
            raise ValueError('user must have name ')
        # Email = self.normalize_email(Email)
        user = self.model(name = name,Phone_no = Phone_no,Otp = Otp,Otp_expre_at = Otp_expre_at,Maximum_otp_try = Maximum_otp_try,Maximum_otp_out = Maximum_otp_out)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,name,Phone_no,password = None):
        user = self.model(name = name,Phone_no = Phone_no)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class userAccountModel(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length = 50, null = False, blank = False)
    # Email = models.EmailField(max_length = 50,unique = True , null = True, blank = True)
    Phone_no = models.CharField(max_length = 13,unique = True, null = False, blank = False)
    Otp = models.CharField(max_length = 4)
    Otp_expre_at = models.DateTimeField(null = True,blank = True)
    Maximum_otp_try = models.CharField(max_length = 2, default = settings.MAX_OTP_TRY)
    """Maximum_otp_out is used for when the user get otp for three times after that please try again after delay"""
    Maximum_otp_out =  models.DateTimeField(null = True,blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = userAcountManager()
    USERNAME_FIELD = 'Phone_no'
    REQUIRED_FIELDS = ["name"]
    def save(self, *args, **kwargs):
        # Call the "real" save method.
        super().save(*args, **kwargs)
        # Now, create a wallet for the user.
        if not Wallet.objects.filter(user=self):
         Wallet.objects.create(user=self, balance=0.0)


    def __str__(self):
        return self.Phone_no
    
class Wallet(models.Model):
    user=models.OneToOneField(userAccountModel,on_delete=models.CASCADE) 
    balance=models.DecimalField(max_digits=8,default=0.0 ,decimal_places=2)
    def __str__(self):
        return f"{self.id}'s wallet"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES= [
        ('deposit','DEPOSIT'),
        ('withdrawal','WITHDRAWAL')
    ]
    
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='transactions')
    amount=models.DecimalField(max_digits=8,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE_CHOICES)
    transaction_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.wallet
    

    