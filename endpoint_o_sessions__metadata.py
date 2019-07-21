import json
from common_errors import valueError, methodError
# from datetime import datetime

from dbops_mysql import DB
db = DB()


VALUE_MAP = {
    'attributes': {
        "disableJoining": None,
        "freeCount": 'free_count',
        "gameMode": None,
        "joinChallengeKey": None, #this modifies attribute, not Join_params, which is not stored currently!
        "playerCount": 'filled_slots',
        "public": None,
        "serverAddress": 'address',
        "serverPort": 'port',
        "state": 'state',
    },
    'slot_count' : 'slot_count',
    'state': 'state_name',
    'name': 'name',
    'region': 'region'
}
# 'last_keepalive',
# 'reservation_count',
# 'filled_slots',
# 'server_address',
# 'server_port',
# 'server_match_challenge_key',

# Actual allowed, not sure the purpose of head and options, returns empty response
# VALID_METHODS = ["HEAD", "GET", "OPTIONS", "PATCH"] 
VALID_METHODS = ["GET", "PATCH"]

def _traverseDict(value_map, set_values):
    update_list = []
    ignored_list = []
    for key, value in set_values.iteritems():
        if key in value_map and value_map[key] is not None:
            if isinstance(value,dict):
                (to_update, to_ignore) = _traverseDict(value_map[key], value)
                update_list.extend(to_update)
                ignored_list.extend(to_ignore)
            else:
                update_list.append((value_map[key], value))
        else:
            ignored_list.append({key: value})
    return (update_list, ignored_list)

def handler(request, match):
    if request.method in VALID_METHODS:
        session_id = match.group(1)

        if request.method == 'PATCH':
            #update the db
            current_value = None
            try:
                update_list = []
                ignored_list = []
                payload = json.loads(request.data)
                if 'ops' in payload:
                    for key in payload['ops']:
                        current_value = key
                        if key in VALUE_MAP and VALUE_MAP[key] is not None:
                            if len(payload['ops'][key]) == 2:
                                (verb, value) = payload['ops'][key]
                                #then its an array? string 'set' followed by what to set
                                if verb == 'set':
                                    #can probably unwind this up one level
                                    if isinstance(value,dict):
                                        (to_update, to_ignore) = _traverseDict(VALUE_MAP[key], value)
                                        update_list.extend(to_update)
                                        ignored_list.extend(to_ignore)
                                    else:
                                        update_list.append((VALUE_MAP[key], value))
                                else:
                                    print("Unexpected PATCH comand in o_sessions__metadata")
                                    print("Command: {}".format(verb))
                                    ignored_list.append({key: payload['ops'][key]})
                            else:
                                print("Unexpected PATCH command lendth in o_sessions__metadata")
                                print("Length: {}".format(len(payload['ops'][key])))
                                print("Command: {}".format(verb))
                                ignored_list.append({key: payload['ops'][key]})
                        else:
                            ignored_list.append({key: payload['ops'][key]})
                    current_value = "DB_ERROR_ignore_description"
                    print(update_list)
                    print(ignored_list)
                    db.updateSession(session_id, update_list)
            except:
                return valueError(current_value)
            
        res = db.getSession(session_id)
        session_data = {
            "attributes": {
                "disableJoining": 0,
                "freeCount": res['free_count'],
                "gameMode": "conquest",
                "joinChallengeKey": res['server_join_challenge_key'],
                "playerCount": res['free_count'],
                "public": 1,
                "serverAddress": res['address'],
                "serverPort": res['server_port'],
                "state": res['state'],
            },
            "join_params": {
                "joinChallengeKey": res['server_join_challenge_key'],
                "matchChallengeKey": res['server_match_challenge_key'],
                "serverAddress": res['server_address'],
                "serverPort": res['server_port'],
            },
            "name": res['name'],
            "password_protected": False,
            "purpose": "public",
            "region": res['region'],
            "slot_count": res['slot_count'],
            "state": res['state_name'],
        }

            # return current session info
        return (200, session_data, {})
    else:
        return methodError(VALID_METHODS)