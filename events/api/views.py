from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from api.serializers import (
    UserSerializer, 
    RoomSerializer,
    EventSerializer,
    ParticipantSerializer
)
from api.models import Room, Event, Participant, User
from api.permisions import OnlyBussiness


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all().order_by('-created')
    serializer_class = RoomSerializer
    permission_classes = [OnlyBussiness]   

    def destroy(self, request, pk=None):
        room  = self.get_object()
        
        q_events = Event.objects.filter(room=room).count()

        if q_events > 0:
            return Response(data='Cannot delete room with assigned events', status=406)        

        self.perform_destroy(room)
        return Response(status=204)        

    
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.filter(type="PU").order_by('-created')
    serializer_class = EventSerializer
    permission_classes = [OnlyBussiness]

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be viewed or edited.
    """
    queryset = Participant.objects.all().order_by('-created')
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]  