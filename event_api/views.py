from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
@api_view(['GET'])
def collect_event(request): 
        try:
            event_type=request.GET.get('eventType')
        except:
            event_type=None
        data = {
                'eventId': request.GET.get('eventId'),
                'eventTimestamp':request.GET.get('eventTimestamp'),
                'eventType' : event_type,
                'parentEventId' : request.GET.get('parentEventId'),
                'userId' : request.GET.get('userId'),
                'advertiserId' : request.GET.get('advertiserId'),
                'deviceId' : request.GET.get('deviceId'),
                'price' : request.GET.get('price')
            }
        df=pd.DataFrame([data])
        # print(data)
        if data['eventId'] and data['eventTimestamp']:
            if data['eventType'] or data['parentEventId']:
                if data['eventType'] in ['impression','click'] and data['parentEventId']:
                    try:
                        df.to_csv('user-events.csv', mode='a', index=False, header=False)
                    except:
                        df.to_csv('user-events.csv', index=False, header=False)
                    return Response(df.to_json(orient="records"), status=status.HTTP_201_CREATED)
                else:
                    return Response('Invalid eventType or ParentEventID',status=status.HTTP_400_BAD_REQUEST)

            else:
                try:
                    
                    df.to_csv('server-events.csv', mode='a', index=False, header=False)
                except:
                    df.to_csv('server-events.csv', index=False, header=False)
                return Response(df.to_json(orient="records"), status=status.HTTP_201_CREATED)
        else:
            return Response('Invalid Event data',status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def validate_event(request):
    df_usr=None
    df_srv=None
    cols=['eventId','eventTimestamp','eventType', 'parentEventId', 'userId', 'advertiserId', 'deviceId', 'price']
    try :
        df_usr = pd.read_csv('user-events_validation.csv',header=None)
        df_usr.columns=cols
        # print(df_usr)
        df_usr['eventTimestamp']=pd.to_datetime(df_usr['eventTimestamp'])
        # print(df_usr)
        df_usr = df_usr.sort_values(by ='eventTimestamp', ascending=True)
        df_usr = df_usr.drop_duplicates(subset=['eventId'], keep='first')
        # print(df_usr)
        df_srv = pd.read_csv('server-events_validation.csv',header=None)
        df_srv.columns=cols
        df_srv['eventTimestamp']=pd.to_datetime(df_srv['eventTimestamp'])
        df_srv = df_srv.sort_values(by ='eventTimestamp', ascending=True)
        df_srv = df_srv.drop_duplicates(subset=['eventId'], keep='first')
    except:
        return Response('unable to read csv files',status=status.HTTP_400_BAD_REQUEST)
    if df_usr.empty == False and df_srv.empty == False:
        df_srv=df_srv[['eventId','eventTimestamp','userId','advertiserId','price']]
        df_srv.rename(columns= {'eventId':'eventId_srv', 'eventTimestamp':'eventTimestamp_srv'}, inplace=True)
        df_usr=df_usr[['eventId','eventTimestamp','eventType','parentEventId','userId','deviceId']]
        validated_events=pd.merge(df_usr,df_srv, on='userId')
        print(validated_events)
        validated_events=validated_events.loc[(validated_events.parentEventId == validated_events.eventId_srv)]
        validated_events=validated_events.loc[(validated_events.eventTimestamp > validated_events.eventTimestamp_srv)]
        validated_events=validated_events[['eventId','eventTimestamp','parentEventId','userId','eventType','advertiserId','deviceId','price']]
        validated_events = validated_events.drop_duplicates(subset=['eventType','parentEventId'], keep='first')
        # validated_events['eventTimestamp']=validated_events['eventTimestamp'].dt.hour
        try:
            validated_events.to_csv('validate_events.csv', mode='a', index=False, header=False)
        except:
            validated_events.to_csv('validate_events.csv', index=False, header=False)
        return Response(validated_events.to_json(orient="records"), status=status.HTTP_200_OK)
    else:
        return Response('one of the event csv file is empty',status=status.HTTP_400_BAD_REQUEST)
