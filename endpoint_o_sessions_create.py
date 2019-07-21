from timestamp import gmt_string
import json
from datetime import datetime
import uuid

from dbops_mysql import DB
db = DB()

from common_errors import valueError, methodError


def handler(request, match): #get db as param
    if request.method != 'POST':
        return methodError(['POST'])

    if request.data:
        payload = json.loads(request.data)

        timestamp = datetime.utcnow()
        timestring = gmt_string(timestamp)

        try:
            session_id = str(uuid.uuid4())
            server_address = payload['join_params']['serverAddress']
            server_port = payload['join_params']['serverPort']
            server_join_challenge_key = payload['join_params']['joinChallengeKey']
            server_match_challenge_key = payload['join_params']['matchChallengeKey']
            session_state = payload['attributes']['state']
            session_name = payload['name']
            session_region = payload['region']
            session_slot_count = payload['slot_count']
        except:
            return valueError()

        db.createSession(session_id, server_address, server_port, server_join_challenge_key, server_match_challenge_key, session_state, session_name, session_region, session_slot_count, timestamp)

        response = {
            "_created_at": timestring,
            "_id": session_id, #fireline generated
            "_modified_at": timestring, 
            "_type": "_sessions", #static
            "attributes": {
                "disableJoining": payload['attributes']['disableJoining'],
                "gameMode": payload['attributes']['gameMode'],
                "ip": server_address,
                "public": payload['attributes']['public'],
                "serverProfile": payload['attributes']['serverProfile'],
                "state": session_state
            },
            "filled_slots": 0, #TODO: static?
            "host": "25721053-ebe8-59f1-95b3-de39bc253c7f", #static
            "last_keepalive": timestring, #TODO:current time string
            "name": session_name, #TODO: from req
            "password_protected": False, #static?
            "purpose": "public", #TODO: from req
            "region": session_region, #TODO: from req
            "reservation_count": 0, #static?
            "slot_count": session_slot_count, #TODO: from req
            "state": "created", #static? are tehre failed states?
            "reflection": payload
        }
        status = 201
        headers = {'Content-Location': "/o/_sessions/{}".format(session_id)}
    else:
        return valueError()
    return (status, response, headers)