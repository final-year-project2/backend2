from django.db import models
from django.conf import settings
  # Import MultiFileField from django-multiupload

#Create your models here.
class Seller(models.Model):
    user = models.ForeignKey('UserAccount.userAccountModel', on_delete=models.CASCADE)  # Foreign key to User model
    successful_campaigns = models.IntegerField(default=0)  # Number of successful campaigns
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp of when the seller was created
    rating = models.IntegerField(default=0)  # Rating of the seller

    def __str__(self):
        return self.user.name
 # Import MultiFileField from django-multiupload
class Ticket(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()  # Change to TextField for unlimited length
    number_of_tickets = models.IntegerField()
    prize_category = models.CharField(max_length=50)
    image_1 = models.ImageField(upload_to='ticket_images/')
    image_2 = models.ImageField(upload_to='ticket_images/')
    image_3 = models.ImageField(upload_to='ticket_images/')# Store multiple images without specifying upload_to

    def __str__(self):
        return self.title


