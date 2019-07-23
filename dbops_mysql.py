from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

import dbpw

class DB:
    def __init__(
        self,
        user = dbpw.user,
        password = dbpw.password,
        host = dbpw.host,
        database = dbpw.database ):

        self.user = user
        self.password = password
        self.host = host
        self.database = database

        assert self.connect()

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      database=self.database,
                                      use_unicode=True)
            self.cnx.autocommit = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False
            
        return True

    def getCursor(self):
        try:
            cur = self.cnx.cursor()
        except mysql.connector.Error as err:
            #MySQL Connection not available.
            if err.errno == -1:
                self.connect()
                cur = self.cnx.cursor()
        return cur

    def testCnx(self):
        try:
            cursor = self.cnx.cursor()    
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            # Check if anything at all is returned
            if results:
                return True
            else:
                return False               
        except Exception,e:
            print("ERROR IN CONNECTION")
        return False

    def createInstance(self, iid, name):

        q = "INSERT INTO instances (`id`, `name`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id=id;"
        cur = self.getCursor()
        cur.execute(q, (iid, name))
        print(cur.statement)
        cur.close()
        return
    
    def createSession(self, session_id, server_address, server_port, server_join_challenge_key, server_match_challenge_key, 
                    session_state, session_name, session_region, slot_count, timestamp):

        q = ("""INSERT INTO sessions 
            (id, server_address, server_port, server_join_challenge_key, server_match_challenge_key, 
            state, state_name, name, region, slot_count, free_count, created_at, modified_at) VALUES 
            (%s, %s, %s, %s, %s, %s, "created", %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id;""")
            
        cur = self.getCursor()
        cur.execute(q, (session_id, server_address, server_port, server_join_challenge_key, server_match_challenge_key, session_state, session_name, session_region, slot_count, slot_count, timestamp, timestamp))
        print(cur.statement)
        cur.close()
        return

    def updateInstanceSession(self, session_id, instance_id):
        q = "UPDATE instances SET attached_session = %s WHERE id = %s;"
        cur = self.getCursor()
        cur.execute(q, (session_id, instance_id))
        print(cur.statement)
        cur.close()
        return

    def updateSession(self, session_id, update_list):
        """Update Session table as per list of values
        
        This is list of tuples (column_name, value_to_set), the column name
        MUST come from a pre-defined list or carfully sanatized of sql injections
        """

        if len(update_list) > 0:
            cols = [i[0] for i in update_list]
            params = [i[1] for i in update_list]

            q = "UPDATE sessions SET"
            for col in cols:
                q = q + ' {} = %s,'.format(col)
            q = q[:-1] + ' WHERE id = %s;'
            print(q)

            params.append(session_id)

            cur = self.getCursor()
            cur.execute(q, params)
            print(cur.statement)
            cur.close()
        return

    def getSession(self, session_id):
        cur = self.getCursor()
        cur.execute("SELECT name, region, slot_count, filled_slots, free_count, state, state_name, address, port, server_address, server_port, server_join_challenge_key, server_match_challenge_key FROM sessions WHERE id = %s;", (session_id,))
        rows = cur.fetchall()
        cur.close()

        result = {}
        for row in rows:
            result = {
                'name': row[0],
                'region': row[1],
                'slot_count': row[2],
                'filled_slots': row[3],
                'free_count': row[4],
                'state': row[5],
                'state_name': row[6],
                'address': row[7],
                'port': row[8],
                'server_address': row[9],
                'server_port': row[10],
                'server_join_challenge_key': row[11],
                'server_match_challenge_key': row[12],
            }
        return result

    def keepaliveSession(self, sid):
        q = 'UPDATE sessions SET last_keepalive = CURRENT_TIME() WHERE id = %s;'
        cur = self.getCursor()
        cur.execute(q, (sid,))
        print(cur.statement)
        cur.close()

        return

    def getJoinData(self, session_id):
        cur = self.getCursor()
        cur.execute("SELECT server_join_challenge_key, server_match_challenge_key, server_address, server_port FROM sessions WHERE id = %s;", (session_id,))
        rows = cur.fetchall()
        cur.close()

        result = None
        for row in rows:
            result = {
                'server_join_challenge_key': row[0],
                'server_match_challenge_key': row[1],
                'server_address': row[2],
                'server_port': row[3],
            }
        return result

    def getInstances(self):
        q = """SELECT i.id, i.name, i.time_created, i.time_modified, i.attached_session, 
        s.id, s.name, s.created_at, s.modified_at, s.last_keepalive, s.region, s.slot_count, 
        s.reservation_count, s.filled_slots, s.free_count, s.state, s.state_name, s.address, 
        s.port, s.server_address, s.server_port, s.server_join_challenge_key, 
        s.server_match_challenge_key 
        FROM instances i INNER JOIN sessions s ON i.attached_session = s.id;"""
        cur = self.getCursor()
        cur.execute(q)
        print(cur.statement)
        rows = cur.fetchall()
        cur.close()

        servers = []
        for row in rows:
            res = {
                'instance':
                {
                    'id': row[0],
                    'name': row[1],
                    'time_created': row[2],
                    'time_modified': row[3],
                    'attached_session': row[4],
                },
                'session': {
                    'id': row[5],
                    'name': row[6],
                    'created_at': row[7],
                    'modified_at': row[8],
                    'last_keepalive': row[9],
                    'region': row[10],
                    'slot_count': row[11],
                    'reservation_count': row[12],
                    'filled_slots': row[13],
                    'free_count': row[14],
                    'state': row[15],
                    'state_name': row[16],
                    'address': row[17],
                    'port': row[18],
                    'server_address': row[19],
                    'server_port': row[20],
                    'server_join_challenge_key': row[21],
                    'server_match_challenge_key': row[22],
                }
            }
            servers.append(res)

        return servers

    
    @classmethod
    def uuid2hex(cls, uuid):
        return uuid.replace('-', '')

    @classmethod
    def hex2uuid(cls, hex):
        return "{}-{}-{}-{}-{}".format(hex[0:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])


def main():
    db = DB()
    db.testCnx()
    print()
  
if __name__== "__main__":
    main()
