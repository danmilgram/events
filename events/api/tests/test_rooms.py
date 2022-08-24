import json

from datetime import datetime, timedelta
from multiprocessing import Event

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import(
    Room,
    User
)

class RoomTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.created_room = Room(
            name="test_room",
            capacity=2
        )
        self.created_room.save()               

    def test_create_room_bussines_user_ok(self):

        self.client.login(
            username="test_user", 
            password="test_password"
        )    

        response = self.client.post(
                "/rooms/", 
                {"name": "test_room_2","capacity": 2},
                format='multipart'
        )  

        json_response = json.loads(response.content)

        created_room = Room.objects.filter(
            name="test_room_2"
        ).get()              

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["id"], created_room.id)
        self.assertEqual(json_response["name"], created_room.name)
        self.assertEqual(json_response["capacity"], created_room.capacity)

    def test_create_room_customer_user_forbidden(self):
        self.client.login(
            username="test_user2", 
            password="test_password_2"
        )    

        response = self.client.post(
                "/rooms/", 
                {"name": "test_room","capacity": 2},
                format='multipart'
        )  

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_room_with_events_forbidden(self):
        
        self.client.login(
            username="test_user", 
            password="test_password"
        )              

        # create event 
        json_body={
            "name": "test_event",
            "type": "PU",
            "date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d"),
            "room": self.created_room.id
        }

        self.client.post(
                "/events/", 
                json_body,
                format='multipart'
        )     
         
        # try to delete creatd room 
        response = self.client.delete(
                "/rooms/{}/".format(self.created_room.id),
                format='multipart'
        )            

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)        

        created_room = Room.objects.filter(
            name="test_room"
        ).get()            

        # created room already exists
        self.assertTrue(created_room is not None)


    def test_delete_room_bussines_user_ok(self):

        self.client.login(
            username="test_user", 
            password="test_password"
        )         

        # try to delete created room 
        response = self.client.delete(
                "/rooms/{}/".format(self.created_room.id),
                format='multipart'
        )            

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)        

        rooms = Room.objects.filter(
            name="test_room"
        )

        # created room doesn't exists
        self.assertTrue(len(rooms) == 0)        

    def test_delete_room_customer_user_forbidden(self):
        self.client.login(
            username="test_user2", 
            password="test_password_2"
        )    

        # try to delete created room 
        response = self.client.delete(
                "/rooms/{}/".format(self.created_room.id),
                format='multipart'
        )            

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)        

        created_room = Room.objects.filter(
            name="test_room"
        ).get()            

        # created room already exists
        self.assertTrue(created_room is not None)



