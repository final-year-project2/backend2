from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone

"""
AbstractBaseUser => that provides a foundation for creating custom user models with additional fields and functionalities.

PermissionsMixin => is a mixin class provided by Django that can be used in conjunction with the Django user model to add permission-related functionalities.

BaseUserManager => this class in Django is a base class provided by Django's authentication system for creating custom user.It provides a set of methods and attributes that help with managing user creation and manipulation

"""



class userAcountManager(BaseUserManager):
    def create_user(self,name,Email,Phone_no,password = None):
        if not Email :
            raise ValueError('user must have email addres')
        Email = self.normalize_email(Email)
        user = self.model(name = name,Email = Email,Phone_no = Phone_no)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,name,Email,Phone_no,password = None):
        user = self.model(name = name,Email = Email,Phone_no = Phone_no)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class userAccountModel(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length = 50, null = False, blank = False)
    Email = models.EmailField(max_length = 50,unique = True , null = True, blank = True)
    Phone_no = models.CharField(max_length = 13,unique = True, null = False, blank = False)
    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    objects = userAcountManager()
    USERNAME_FIELD = 'Phone_no'
    REQUIRED_FIELDS = ["name","Email"]

    def __str__(self):
        return self.Phone_no

    