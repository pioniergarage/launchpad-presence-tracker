import datetime
import json
import config

api_url = config.api['url']

def post_activities(activities_dict):
    print('POST '+ str(api_url))
    now = datetime.datetime.now()
    body_dict = {
        'activities': [{ 'hash': activity['hash'] } for key, activity in activities_dict.items()],
        'date': now.isoformat()
    }
    print(json.dumps(body_dict, indent=2))
