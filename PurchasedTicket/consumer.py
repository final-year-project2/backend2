from channels.generic.websocket import AsyncWebsocketConsumer
# from models import PurchasedTicket
import json
import logging
logger = logging.getLogger(__name__)
class PurchasedTicketConsumer(AsyncWebsocketConsumer):
     async def connect(self):
        self.room_group_name = f'ticket_updates_{self.scope["url_route"]["kwargs"]["seller_id"]}'
        
        print(self.scope["url_route"]["kwargs"]["seller_id"])
      #   self.room_group_name = f'ticket_updates_1'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        
        )
      #   print(event['content'])
        
        await self.accept()
        logger.info("websocket info")
        await self.send(" websocket")
        
        
       

     async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
     async def ticket_update(self, event):
        # This method will handle messages received from the group
          try:
           await self.send(text_data='hello')
         #   logger.info("Event object: %s", event)
           await self.send(text_data=json.dumps( event["content"]))
         
          except Exception as e: 
           logger.error(f"Error sending message: {e}")
        
        

  
    

 


