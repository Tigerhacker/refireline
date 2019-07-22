import json
from common_errors import valueError, methodError
# from datetime import datetime

from timestamp import gmt_string
from dbops_mysql import DB
db = DB()

def handler(request, match):
    if request.method == 'GET':
        res = db.getInstances()

        items = []
        for r in res:
            item = {
                "_type": "_instances",
                "display_name": r['instance']['name'],
                "_created_at": gmt_string(r['instance']['time_created']),
                "_modified_at": gmt_string(r['instance']['time_modified']),
                "session": {
                    "_type": "_sessions",
                    "last_keepalive": gmt_string(r['session']['last_keepalive']),
                    "password_protected": False,
                    "_modified_at": gmt_string(r['session']['modified_at']),
                    "filled_slots": r['session']['filled_slots'],
                    "reservation_count": r['session']['reservation_count'],
                    "_created_at": gmt_string(r['session']['created_at']),
                    "state": r['session']['state_name'],
                    "purpose": "public",
                    "host": "25721053-ebe8-59f1-95b3-de39bc253c7f",
                    "attributes": {
                        "joinChallengeKey": r['session']['server_join_challenge_key'],
                        "freeCount": r['session']['free_count'],
                        "playerCount": r['session']['filled_slots'], #is this the right value mapping?
                        "disableJoining": 0,
                        "gameMode": "conquest",
                        "state": r['session']['state'],
                        "serverPort": r['session']['port'],
                        "public": 1,
                        "serverAddress": r['session']['address'],
                    },
                    "slot_count": r['session']['slot_count'],
                    "_id": r['session']['id'],
                    "region": r['session']['region'],
                    "name": r['session']['name'],
                },
                "is_favorite": False,
                "owner": "25721053-ebe8-59f1-95b3-de39bc253c7f",
                "attributes": {},
                "_id": r['instance']['id'],
            }
            items.append(item)
        session_data = {
            "page": 1,
            "items": items,
            "prev_cursor": "",
            "next_cursors": []
        }
            # return current session info
        return (200, session_data, {})
    else:
        return methodError(VALID_METHODS)