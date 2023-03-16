import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

client= Client()
class collect_event_test(TestCase):
    def setUp(self):
        self.url = reverse('collect_event')
      
        self.server_event = {
            'eventId':'event1',
            'eventTimestamp':'10:00',
            'parentEventId' : '',
            'userId' : 'user1',
            'advertiserId' : 'adv1',
            'deviceId' : '',
            'price' : '10'}

        self.user_event = {
            'eventId':'event5',
            'eventTimestamp':'10:01',
            'eventType' : 'click',
            'parentEventId' : 'event1',
            'userId' : 'user1',
            'advertiserId' : 'adv2',
            'deviceId' : 'dev1',
            'price' : ''}
            
    def test_collect_server_event_success(self):
        data=self.server_event
        response = client.get(self.url, data=json.dumps(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_collect_user_event_success(self):
        data=self.user_event
        response = client.get(self.url, data=json.dumps(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
class validate_event_test(TestCase):
    def setUp(self):
        self.url = reverse('validate_event')
        
    def test_validate_event_success(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
