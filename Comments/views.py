from rest_framework import generics,permissions
from .serializer import TicketCommentSerializer
from .models import TicketComment

class TicketComment(generics.ListCreateAPIView):
    queryset = TicketComment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketCommentSerializer

    def perform_create(self, serializer):
        users =  self.request.user
        serializer.save(User_id = users)

