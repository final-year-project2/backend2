from rest_framework import generics,permissions
from .serializer import TicketCommentSerializer
from .models import TicketCommentModel

class TicketComment(generics.ListCreateAPIView):
    queryset = TicketCommentModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketCommentSerializer

    def perform_create(self, serializer):
        users =  self.request.user
        serializer.save(User_id = users)



class SingleTicketComment(generics.ListCreateAPIView):
    queryset =  TicketCommentModel.objects.all()
    serializer_class = TicketCommentSerializer
    lookup_field = 'Ticket_id' 
    def get_queryset(self):
        TicketId = self.kwargs['Ticket_id']
        print(TicketId)
        qs =  super().get_queryset()
        return qs.filter(Ticket_id = TicketId)
    

