import json

from datetime import datetime, timedelta
from multiprocessing import Event

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import(
    Room,
    User,
    Event
)

class EventTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()

        self.room = Room(
            name="test_room",
            capacity=2
        )
        self.room.save()

        self.bussiness_user = User(
            username="test_user",
            type="BU"
        )
        self.bussiness_user.set_password('test_password')
        self.bussiness_user.save()

        self.customer_user = User(
            username="test_user2",
            type="CU"
        )
        self.customer_user.set_password('test_password_2')
        self.customer_user.save()        

    def test_create_event_not_authorized(self):
    
        json_body={
            "name": "test_event",
            "type": "PU",
            "date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d"),
            "room": self.room.id
        }

        response = self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event_with_customer_user_forbidden(self):
        self.client.login(
            username="test_user_2", 
            password="test_password_2"
        )        

        json_body={
            "name": "test_event",
            "type": "PU",
            "date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d"),
            "room": self.room.id
        }

        response = self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)        

    def test_create_event_with_bussiness_user_ok(self):
        self.client.login(
            username="test_user", 
            password="test_password"
        )

        now_date = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")

        json_body={
            "name": "test_event",
            "type": "PU",
            "date": now_date,
            "room": self.room.id
        }

        response = self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_event = Event.objects.filter(
            date=now_date
        ).get()

        json_response = json.loads(response.content)

        self.assertEqual(json_response["id"], created_event.id)
        self.assertEqual(json_response["name"], created_event.name)
        self.assertEqual(json_response["type"], created_event.type)
        self.assertEqual(json_response["date"], now_date)
        self.assertEqual(json_response["room"], created_event.room.id)

    def test_create_two_events_same_day_validation(self):
        self.client.login(
            username="test_user", 
            password="test_password"
        )

        now_date = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")

        json_body={
            "name": "test_event",
            "type": "PU",
            "date": now_date,
            "room": self.room.id
        }

        # create first event
        response = self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create second event
        response = self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )

        expected_response = {
            "date": [
                "event with this date already exists."
            ]
        }               
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected_response)
                

    def test_get_public_events(self):
        self.client.login(
            username="test_user", 
            password="test_password"
        )

        # create public event
        public_event_date = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")    

        json_body={
            "name": "test_event",
            "type": "PU",
            "date": public_event_date,
            "room": self.room.id
        }

        self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )

        # create private event
        private_event_date = datetime.strftime(
            datetime.utcnow() + timedelta(days=1), "%Y-%m-%d")    

        json_body={
            "name": "test_event_2",
            "type": "PR",
            "date": private_event_date,
            "room": self.room.id
        }

        self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )        


        # get events --> returns only 1 event(public one)
        response = self.client.get("/events/")
        json_response = json.loads(response.content)

        self.assertTrue(len(json_response["results"]) == 1 )
        self.assertTrue(json_response["results"][0]["type"] == "PU")
        self.assertTrue(json_response["results"][0]["date"] == public_event_date)
        self.assertTrue(json_response["results"][0]["name"] == "test_event")

