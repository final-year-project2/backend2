from django.db import models
from django.conf import settings
from Product.models import Ticket
user = settings.AUTH_USER_MODEL

class TicketComment(models.Model):
    User_id = models.ForeignKey(user,on_delete=models.CASCADE)
    Ticket_id = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    Comment = models.CharField(null=False,max_length=100)