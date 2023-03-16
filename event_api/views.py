from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
@api_view(['GET'])
def collect_event(request):
        data = request.data 
        try:
            event_type=data.get('eventType')
        except:
            event_type=None
        data = {
                'eventId': data.get('eventId'),
                'eventTimestamp':data.get('eventTimestamp'),
                'eventType' : event_type,
                'parentEventId' : dat.get('parentEventId'),
                'userId' : data.get('userId'),
                'advertiserId' : data.get('advertiserId'),
                'deviceId' : data.get('deviceId'),
                'price' : data.get('price')
            }
        df=pd.DataFrame(data)
        if data['eventId'] and data['eventTimestamp']:
            if data['eventType'] and data['parentEventId']:
                if data['eventType'] in ['impression','click']:
                    try:
                        df.to_csv('user-events.csv', mode='a', index=False, header=False)
                    except:
                        df.to_csv('user-events.csv', index=False, header=False)
                    return Response(df.to_json(orient="records"), status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                try:
                    df.to_csv('server-events.csv', mode='a', index=False, header=False)
                except:
                    df.to_csv('server-events.csv', index=False, header=False)
                return Response(df.to_json(orient="records"), status=status.status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

def validate_event(request):
    df_usr=None
    df_srv=None
    try :
        df_usr = pd.read_csv('user-events.csv')
        df_usr = df_usr.sort_values(by ='eventTimestamp', ascending=True)
        df_usr = df_usr.drop_duplicates(subset=['eventType','parentEventId'], keep='first')
        df_usr = df_usr.drop_duplicates(subset=['eventId'], keep='first')
        df_srv = pd.read_csv('server-events.csv')
        df_srv = df_srv.sort_values(by ='eventTimestamp', ascending=True)
        df_srv = df_srv.drop_duplicates(subset=['eventId'], keep='first')
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if df_usr and df_srv:
        df_srv=df_srv[['eventId','eventTimestamp','userId','advertiserId','price']]
        df_srv.rename(columns= {'eventId':'eventId_srv', 'eventTimestamp':'eventTimestamp_srv'}, inplace=True)
        df_usr=df_usr[['eventId','eventTimestamp','eventType','parentEventId','userId','deviceId']]
        validated_events=pd.merge(df_usr,df_srv, on='userId', left_on='parentEventId', right_on='eventId_srv')
        validate_events.loc[(pd.to_datetime(validated_events.eventTimestamp) > pd.to_datetime(validated_events.eventTimestamp_srv))]
        validate_events=validate_events[['eventId','eventTimestamp','parentEventId','userId','eventType','advertiserId','deviceId','price']]
        try:
            validate_events.to_csv('validate_events.csv', mode='a', index=False, header=False)
        except:
            validate_events.to_csv('validate_events.csv', index=False, header=False)
        return Response(validate_events.to_json(orient="records"), status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
