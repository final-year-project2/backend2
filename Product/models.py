from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from UserAccount.models import userAccountModel
#Create models here.
class Seller(models.Model):
    user = models.ForeignKey(userAccountModel, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_images/')
    successful_campaigns = models.IntegerField(default=0)  # Number of successful campaigns
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp of when the seller was created
    rating = models.IntegerField(default=0)  # Rating of the seller

    def __str__(self):
        return self.user.name

class Ticket(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()  # Change to TextField for unlimited length
    number_of_tickets = models.CharField()
    prize_categories = models.TextField()
    my_datetime_field = models.DateTimeField(default=timezone.now) #which is updated every time when ticket is updated
    date_createds = models.DateTimeField(auto_now_add=True)#this hold the intial date created of ticket which is not updated
    price_of_ticket=models.CharField(default=0)
    image_1 = models.ImageField(upload_to='ticket_images/',default='default_image.jpg')
    image_2 = models.ImageField(upload_to='ticket_images/',null=True,blank=True)
    image_3 = models.ImageField(upload_to='ticket_images/',null=True,blank=True)
    winner_drawn = models.BooleanField(default=False)  # Track if winner is drawn
    fully_purchased_at = models.DateTimeField(null=True, blank=True)# Store multiple images without specifying upload_to
    def __str__(self):
          return self.title
class Winner(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    winner = models.ForeignKey(userAccountModel, on_delete=models.CASCADE)
    Ticket_number=models.ForeignKey('PurchasedTicket.PurchasedTicket', on_delete=models.CASCADE)
    winner_name = models.CharField(max_length=50)
    drawn_at = models.DateTimeField(auto_now_add=True)