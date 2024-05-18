from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from UserAccount.models import userAccountModel
#Create models here.
class Seller(models.Model):
    user = models.ForeignKey(userAccountModel, on_delete=models.CASCADE)
    successful_campaigns = models.IntegerField(default=0)  # Number of successful campaigns
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp of when the seller was created
    rating = models.IntegerField(default=0)  # Rating of the seller

    def __str__(self):
        return self.user.name

class Ticket(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,null=True)
    title = models.TextField()
    description = models.TextField()  # Change to TextField for unlimited length
    number_of_tickets = models.CharField()
    prize_categories = models.TextField()
    image_1 = models.ImageField(upload_to='ticket_images/',default='default_image.jpg')
    image_2 = models.ImageField(upload_to='ticket_images/',null=True,blank=True)
    image_3 = models.ImageField(upload_to='ticket_images/',null=True,blank=True)# Store multiple images without specifying upload_to



