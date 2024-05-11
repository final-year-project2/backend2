from django.contrib import admin
from .models import userAccountModel,Wallet,Transaction
admin.site.register(userAccountModel)
admin.site.register(Wallet)
admin.site.register(Transaction)
# Register your models here.
