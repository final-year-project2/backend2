from django.db import models
from django.conf import settings
from Product.models import Ticket
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

user = settings.AUTH_USER_MODEL

class PurchasedTicket(models.Model):
    User_id = models.ForeignKey(user,on_delete=models.CASCADE)
    Ticket_id = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    Ticket_number = models.CharField(null=False)
    


@receiver(post_save , sender=PurchasedTicket)
def ticket_purchased_broadcaster(sender,instance,created,**kwargs):
    if created:
        seller_id=instance.Ticket_id.seller.id
        
        print(f'seller_id{seller_id}')
        left_ticket= int(instance.Ticket_id.number_of_tickets)-PurchasedTicket.objects.filter(Ticket_id=instance.Ticket_id).count()
        number_of_buyer=PurchasedTicket.objects.filter(Ticket_id=instance.Ticket_id).values('User_id').distinct().count()
        
        print(f"ticket left:{left_ticket}")
        print(f"number of people :{number_of_buyer}")
        
        
        message={
            "type":"ticket.update",
            "content":{
                "action":"purchase",
                "seller_id": seller_id,
                "ticket_left":left_ticket,
                "number_of_buyer":number_of_buyer
                
                
            }
        }
        print(f'client updated{message}')
        channel_layer =get_channel_layer()
        
        async_to_sync(channel_layer.group_send)( f'ticket_updates_{seller_id}', message  )
        