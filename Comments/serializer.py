from rest_framework import serializers
from .models import TicketCommentModel
class TicketCommentSerializer(serializers.ModelSerializer):
    User_id = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model= TicketCommentModel
        fields = ['id','User_id','Ticket_id','Comment']
    def get_User_id(self,obj):
        return  obj.User_id.id