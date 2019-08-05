from timestamp import gmt_string
import json
from datetime import datetime
import uuid

from common_errors import valueError, methodError

def handler(request, match): #get db as param
    from dbops_mysql import DB
    db = DB()

    netid = match.group(1)

    db.touchIdentity(netid)

    return (200, {}, {})