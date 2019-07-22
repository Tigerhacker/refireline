import json
from common_errors import valueError, methodError
# from datetime import datetime

from timestamp import gmt_string
from dbops_mysql import DB
db = DB()

def handler(request, match):
    if request.method == 'POST':
        sid = match.group(1)
        res = db.getJoinData(sid)

        status = 404
        if res is None:
            join_data = {
                "error": "resource_not_found",
                "http_status_code": 404,
                "error_description": "Session not found"
            }
        else:
            status = 201
            join_data = {
                "created_at": "Thu, 11 Jul 2019 14:55:05 GMT",
                "expires_at": "Thu, 11 Jul 2020 14:55:35 GMT",
                "has_slot": False,
                "identity": "197a97fc-4179-43f4-b009-9432ac0c8e53",
                "join_params": {
                    "joinChallengeKey": res['server_join_challenge_key'],
                    "matchChallengeKey": res['server_match_challenge_key'],
                    "serverAddress": res['server_address'],
                    "serverPort":res['server_port'],
                },
                "session": sid
            }
                # return current session info
        return (status, join_data, {})
    else:
        return methodError(['POST'])