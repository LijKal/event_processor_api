# event_processor_api
## create python virtual environment and install all dependencies
```
virtualenv event_env 
source event_env/bin/activate
pip install -r requirements.txt
```

# run the app
```
python manage.py runserver
```
## to test collect event api
 ```
 curl "http://localhost:8000/event/collect/?eventId=event1&eventTimestamp=10:00&parentEventId=&userId=user1&advertiserId=
adv1&deviceId=&price=10"

curl "http://localhost:8000/event/collect/?eventId=event2&eventTimestamp=10:01&parentEventId=&userId=user2&advertiserId=
adv2&deviceId=&price=10"

curl "http://localhost:8000/event/collect/?eventId=event3&eventTimestamp=10:11&eventType=impression&parentEventId=event
1&userId=user1&advertiserId=adv1&deviceId=dev1&price="

curl "http://localhost:8000/event/collect/?eventId=event4&eventTimestamp=10:00&eventType=&parentEventId=event1&userId=
user1&advertiserId=adv1&deviceId=&price="

curl "http://localhost:8000/event/collect/?eventId=event5&eventTimestamp=10:11&eventType=click&parentEventId=event2&use
rId=user2&advertiserId=adv2&deviceId=&price="
 ```
 ## to test validate event api
 ```
 curl "http://localhost:8000/event/validate"
 ```
