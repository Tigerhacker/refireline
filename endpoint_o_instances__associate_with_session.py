import json
from common_errors import valueError, methodError
# from datetime import datetime

from dbops_mysql import DB
db = DB()


def handler(request, match):
    if request.method != 'POST':
        return methodError(['POST'])
    # timestamp = datetime.utcnow()
    instance_id = match.group(1)
    try:
        payload = json.loads(request.data)
        session_id = payload['session_id']
        db.updateInstanceSession(session_id, instance_id)
    except:
        return valueError('session_id')
    return (200, {}, {})