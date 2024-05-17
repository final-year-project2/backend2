from django.db import models
from django.conf import settings
from Product.models import Ticket
user = settings.AUTH_USER_MODEL
class PurchasedTicket(models.Model):
    User_id = models.ForeignKey(user,on_delete=models.CASCADE)
    Ticket_id = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    Ticket_number = models.CharField(null=False)
    