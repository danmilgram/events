from asyncio import events
from datetime import datetime, timedelta
import json
from venv import create

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import(
    Room,
    User,
    Event,
    Participant
)

class ParticipantTestCase(TestCase):
    def setUp(self):
        
        self.client = APIClient()

        self.user = User(
            username="customer",
            type="CU"
        )
        self.user.set_password('customer')
        self.user.save()    

        self.user2 = User(
            username="customer2",
            type="CU"
        )
        self.user2.set_password('customer2')
        self.user2.save()    

        self.user3 = User(
            username="customer3",
            type="CU"
        )
        self.user3.set_password('customer3')
        self.user3.save()                            

        self.room = Room(
            name="test_room",
            capacity=2
        )
        self.room.save()        

        self.room2 = Room(
            name="test_room2",
            capacity=2
        )
        self.room2.save()             

        self.public_event = Event(
            name="test_event",
            type="PU",
            date=datetime.utcnow() + timedelta(days=1),
            room=self.room
        )
        self.public_event.save()     

        self.private_event = Event(
            name="test_event",
            type="PR",
            date=datetime.utcnow(),
            room=self.room2
        )
        self.private_event.save()              

        self.participant = Participant(
            user=self.user2,
            event=self.public_event
        )
        self.participant.save()
        


    def test_join_event_ok(self):
        self.client.login(
            username="customer",
            password="customer"
        )

        json_body={
            "event": self.public_event.id,
            "user": self.user.id
        }

        response = self.client.post(
                "/participants/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_participant = Participant.objects.filter(
            event=self.public_event.id,
            user=self.user.id
        ).get()

        json_response = json.loads(response.content)

        self.assertEqual(json_response["id"], created_participant.id)


    def test_abandon_event_ok(self):

        self.client.login(
            username="customer2",
            password="customer2"
        )        

        response = self.client.delete(
                "/participants/{}/".format(self.participant.id), 
                format='multipart'
        )        

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_cannot_join_private_event(self):
        self.client.login(
            username="customer",
            password="customer"
        )

        json_body={
            "event": self.private_event.id,
            "user": self.user.id
        }

        response = self.client.post(
                "/participants/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        p = Participant.objects.filter(
            event=self.private_event.id,
            user=self.user.id
        )

        self.assertTrue(len(p) == 0)
        self.assertTrue(json.loads(response.content) == {'non_field_errors': ["Can't join private event"]})


    def test_cannot_join_event_twice(self):
        self.client.login(
            username="customer2",
            password="customer2"
        )        

        json_body={
            "user": self.user2.id,
            "event": self.public_event.id,
        }

        response = self.client.post(
                "/participants/".format(self.participant.id), 
                json_body,
                format='multipart'
        )        

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(json.loads(response.content) == {'non_field_errors': ["User already joined that event"]})


    def test_cannot_join_full_event(self):

        # 2nd user --> join ok
        self.client.login(
            username="customer",
            password="customer"
        )

        json_body={
            "event": self.public_event.id,
            "user": self.user3.id
        }

        response = self.client.post(
                "/participants/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3rd user --> unable to join because room is full
        self.client.login(
            username="customer3",
            password="customer3"
        )

        json_body={
            "event": self.public_event.id,
            "user": self.user.id
        }

        response = self.client.post(
                "/participants/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(json.loads(response.content) == {'non_field_errors': ["Event room is full"]})        