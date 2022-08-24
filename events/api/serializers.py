from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import (
    Item, Room, Event, Participant, User
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'type', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        
        user.type = validated_data['type']
        user.save()
        return user    


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"        

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"       

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"      

        validators = [
            UniqueTogetherValidator(
                queryset=Participant.objects.all(),
                fields=['user', 'event'],
                message="User already joined that event"
            )
        ]      

    def validate(self, data):
        q_participants = Participant.objects.filter(event=data["event"]).count()

        if q_participants >= data["event"].room.capacity:
            raise serializers.ValidationError("Event room is full")

        return data