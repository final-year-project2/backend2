from rest_framework import serializers
from PurchasedTicket.models import PurchasedTicket
class PurchasedTicketSerializer(serializers.ModelSerializer):
    User_id = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model= PurchasedTicket
        fields = ['id','User_id','Ticket_id','Ticket_number']
    def get_User_id(self,obj):
        return  obj.User_id.id
    def validate(self, data):
        Ticket_id = data.get('Ticket_id')
        Ticket_number = data.get('Ticket_number')
        IsTicketAlredyPurchased=PurchasedTicket.objects.filter(Ticket_id =Ticket_id , Ticket_number = Ticket_number )
        if IsTicketAlredyPurchased:
            raise serializers.ValidationError({'Tcket_number': f'Ticket number {Ticket_number} already purchased.'})
        return data