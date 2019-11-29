import psycopg2
from config import config
import json


# def create_tables():
#     """ create tables in the PostgreSQL database"""
#     commands = (
#         """
#         CREATE TABLE players (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             password VARCHAR(255) NOT NULL,
#             gender VARCHAR(255) NOT NULL,
#             hp smallint NOT NULL,
#             core_attributes VARCHAR(255) NOT NULL,
#             player_state VARCHAR(255) NOT NULL,
#             conditions VARCHAR(255),
#             credit smallint NOT NULL,
#             stow_loc VARCHAR(255),
#             location VARCHAR(255) NOT NULL
#         )
#         """,
#         """ 
#         CREATE TABLE rooms (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             ship_id VARCHAR(255),
#             room_type VARCHAR(255) NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(255) NOT NULL,
#             exits VARCHAR(255),
#             region VARCHAR(255),
#             zone VARCHAR(255),
#             elevation VARCHAR(255),
#             effects VARCHAR(255),
#             owner VARCHAR(255)
#         )
#         """,
#         """ 
#         CREATE TABLE npcs (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             entity_type VARCHAR(255) NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             race VARCHAR(255) NOT NULL,
#             gender VARCHAR(255) NOT NULL,
#             npc_desc VARCHAR(255) NOT NULL,
#             core_attributes VARCHAR(255) NOT NULL,
#             npc_state VARCHAR(255) NOT NULL, 
#             conditions VARCHAR(255),
#             credit smallint NOT NULL, 
#             supply VARCHAR(255) NOT NULL,
#             demand VARCHAR(255) NOT NULL,
#             home_loc VARCHAR(255) NOT NULL,
#             demeanor VARCHAR(255) NOT NULL,
#             location VARCHAR(255) NOT NULL
#         )
#         """,
#         """ 
#         CREATE TABLE orgs (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             org_desc VARCHAR(255) NOT NULL,
#             supply VARCHAR(255) NOT NULL,
#             demand VARCHAR(255) NOT NULL,
#             home VARCHAR(255) NOT NULL
#         )
#         """,
#         """ 
#         CREATE TABLE universe (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             univ_type NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             supply VARCHAR(255) NOT NULL,
#             demand VARCHAR(255) NOT NULL
#         )
#         """,
#         """ 
#         CREATE TABLE items (
#             unique_id SERIAL PRIMARY KEY,
#             uuid_id VARCHAR(255) NOT NULL,
#             name VARCHAR(255) NOT NULL,
#             item_desc VARCHAR(255) NOT NULL,
#             entity_type VARCHAR(255) NOT NULL,
#             size smallint NOT NULL,
#             weight smallint NOT NULL,
#             capacity smallint NOT NULL,
#             can_attributes VARCHAR(255),
#             room_target VARCHAR(255), 
#             combines_with VARCHAR(255),
#             is_open BOOLEAN NOT NULL,
#             location VARCHAR(255) NOT NULL,
#             location_body VARCHAR(255),
#             owner VARCHAR(255) NOT NULL
#         )
#         """)
#     conn = None
#     try:
#         # read the connection parameters
#         params = config()
#         # connect to the PostgreSQL server
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
#         # create table one by one
#         for command in commands:
#             cur.execute(command)
#         # close communication with the PostgreSQL database server
#         cur.close()
#         # commit the changes
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

# def add_player(uuid_id, name, gender, hp, core_attributes, player_state, conditions, stow_loc, location):
#     # statement for inserting a new row into the parts table
#     insert_player = "INSERT INTO accounts_players(uuid_id, name, gender, hp, core_attributes, player_state, conditions, stow_loc, location) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING uuid_id, name, gender, hp, core_attributes, player_state, conditions, stow_loc, location;"

 
#     conn = None
#     try:
#         dbparams = config()
#         conn = psycopg2.connect(**dbparams)
#         cur = conn.cursor()
#         # insert a new part
#         jatt = core_attributes
#         cur.execute(insert_player, (uuid_id, name, gender, hp, json.dumps(jatt), player_state, stow_loc, conditions, location,))
#         # commit changes
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

def guest_to_reg(message):
    # statement for inserting a new row into the parts table
    insert_item = """INSERT INTO items(uuid_id, entity_type, name, gender, vitals, core_attributes, player_state, conditions, stow_loc, location)
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                     RETURNING uuid_id, entity_type, name, gender, vitals, core_attributes, player_state, conditions, stow_loc, location;"""

 
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()
        # insert a new part
        cur.execute(insert_item, (uuid_id, entity_type, name, gender, vitals, core_attributes, player_state, conditions, stow_loc, location,))
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_db(message):
    
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()
        
        cur.execute("SELECT unique_id, uuid_id, name, gender, vitals, core_attributes, player_state, conditions, stow_loc, location FROM players ORDER BY unique_id")

        rows = cur.fetchall()
        for row in rows:
            # print(row)
            if row[2] == message:
                print("Found result for", row[2], "with player ID:", row[1])
                return row
                break
        else:
            print("Did not find anything with", message)
            return None

        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_login(login):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("SELECT uuid_id FROM accounts_players ORDER BY uuid_id")
        rows = cur.fetchall()
    
        print("DB | Checking Login:", login)
        # print("DB | From options:", rows)
        for row in rows:
            if row[0] == login:
                print("DB | Logging in UUID:", row[0])
                print("")
                return row[0]
        
        else:
            print("DB | Character not found.")
            print("")
            return False
        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def check_pw(pw, login):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("SELECT password FROM accounts_players WHERE name = %s;", (login,))
        rows = cur.fetchone()
        rows = "".join(rows[0] for x in rows)

        print("DB | Password provided:", pw, type(pw))
        print("DB | Password needed:", rows, type(rows))
        if pw == rows:
            print("DB | Password correct, completing login.")
            return True
        else:
            print("DB | Password incorrect.")
            return False
        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### Players ###

def load_all_players(players):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("""SELECT uuid_id, entity_type, description, vitals, core_attributes, conditions, credit, location, player_state, stow_loc, unique_id
                       FROM accounts_players 
                       ORDER BY uuid_id""")
        rows = cur.fetchall()

        for i in rows:
            # print(i)
            players[i[0]] = {
                "uuid_id": i[0],
                "entity_type": json.loads(i[1]),  
                "description": json.loads(i[2]),
                "vitals": json.loads(i[3]), 
                "core_attributes": json.loads(i[4]), 
                "conditions": json.loads(i[5]), 
                "credit": json.loads(i[6]), 
                "location": i[7], 
                "player_state": i[8], 
                "stow_loc": i[9], 
                "unique_id": i[10],
                "client": None
                }

        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### Items ###

# def add_item_to_db(uuid_id, name, item_desc, entity_type, size, weight, capacity, can_attributes, room_target, combines_with, is_open, location, location_body, owner):
#     # statement for inserting a new row into the parts table
#     insert_item = """INSERT INTO items(uuid_id, name, item_desc, entity_type, size, weight, capacity, can_attributes, room_target, combines_with, is_open, location, location_body, owner)
#                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
#                      RETURNING uuid_id, name, item_desc, entity_type, size, weight, capacity, can_attributes, room_target, combines_with, is_open, location, location_body, owner;"""

 
#     conn = None
#     try:
#         dbparams = config()
#         conn = psycopg2.connect(**dbparams)
#         cur = conn.cursor()
#         # insert a new part
#         cur.execute(insert_item, (uuid_id, name, item_desc, entity_type, size, weight, capacity, can_attributes, room_target, combines_with, is_open, location, location_body, owner,))
#         # commit changes
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

def load_all_items(items):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("""SELECT uuid_id, join_table, keyword, description, attributes, dynamic_stats, room_target, is_open, location, location_body, vitals, owner
                       FROM accounts_items 
                       ORDER BY uuid_id""")
        rows = cur.fetchall()

        for i in rows:

            # print("db:", i)

            items[i[0]] = {
                "uuid_id": i[0],
                "join_table": json.loads(i[1]), 
                "keyword": i[2], 
                "description": json.loads(i[3]), 
                "attributes": json.loads(i[4]), 
                "dynamic_stats": json.loads(i[5]), 
                "room_target": json.loads(i[6]), 
                "is_open": i[7], 
                "location": i[8], 
                "location_body": json.loads(i[9]), 
                "vitals": json.loads(i[10]), 
                "owner": i[11]
            }

        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

### ROOMS ###

# def add_room_to_db(uuid_id, name, description, exits, region, zone, effects, owner):
#     # statement for inserting a new row into the parts table
#     insert_room = """INSERT INTO rooms(uuid_id, name, description, exits, region, zone, effects, owner) 
#                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s) 
#                      RETURNING uuid_id, name, description, exits, region, zone, effects, owner;"""

 
#     conn = None
#     try:
#         dbparams = config()
#         conn = psycopg2.connect(**dbparams)
#         cur = conn.cursor()
#         # insert a new part
#         jexits = exits
#         cur.execute(insert_room, (uuid_id, name, description, json.dumps(jexits), region, zone, effects, owner,))
#         # commit changes
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

def load_all_rooms(rooms):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("""SELECT uuid_id, entity_type, ship_id, coordinates, name, description, exits, region, zone, elevation, effects, owner 
                       FROM accounts_rooms 
                       ORDER BY uuid_id""")
        rows = cur.fetchall()

        for i in rows:
            # print(i)
            jcoords = json.loads(i[3])
            jexits = json.loads(i[6])
            rooms[i[0]] = {
                "uuid_id": i[0],
                "entity_type": json.loads(i[1]), 
                "ship_id": i[2], 
                "coordinates": jcoords, 
                "name": i[4], 
                "description": i[5], 
                "exits": jexits,
                "region": i[7], 
                "zone": i[8], 
                "elevation": i[9],
                "effects": [],
                "owner": i[11]
                }

        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def load_all_npcs(npcs):
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        ###
        cur.execute("""SELECT uuid_id, name, gender, vitals, conditions, credit, location, join_table, description, npc_state, supply, demand, demeanor 
                       FROM accounts_npcs 
                       ORDER BY uuid_id""")
        rows = cur.fetchall()

        for i in rows:

            npcs[i[0]] = {
                "uuid_id": i[0], 
                "name": i[1], 
                "gender": i[2], 
                "vitals": json.loads(i[3]), 
                "conditions": json.loads(i[4]), 
                "credit": json.loads(i[5]), 
                "location": i[6], 
                "join_table": i[7], 
                "description": json.loads(i[8]), 
                "npc_state": json.loads(i[9]), 
                "supply": json.loads(i[10]), 
                "demand": json.loads(i[11]), 
                "demeanor": i[12]
                }

        ###
        
        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# ADDING

def add_new_player_to_db(self):

    print("Adding new player to DB:", self, self.name, self.uuid_id)

    # statement for inserting a new row into the players table
    insert_item = """INSERT INTO accounts_players(uuid_id, name, gender, core_attributes, player_state, conditions, stow_loc, location, entity_type, race, vitals, credit)
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                     RETURNING uuid_id, name, gender, core_attributes, player_state, conditions, stow_loc, location, entity_type, race, vitals, credit;"""

 
    conn = None
    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()
        # insert a new part
        cur.execute(insert_item, (self.uuid_id, self.name, self.gender, json.dumps(self.core_attributes), self.player_state, json.dumps(self.conditions), self.stow_loc, self.location, json.dumps(self.entity_type), self.race, json.dumps(self.vitals), json.dumps(self.credit),))
        # commit changes
        conn.commit()

        print("DB | Finished adding player to accounts_players.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# UPDATES

def update_user_player(self):

    print("Updating update user player:", self, self.name, self.uuid_id)

    update = """UPDATE accounts_customuser
                SET char_name = %s
                WHERE uuid_id = %s"""
    
    conn = None
    updated_rows = 0

    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        # execute the UPDATE  statement
        cur.execute(update, (self.name,
                             self.uuid_id)
                    )
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()

        print("DB | Finished updating player's character name.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def update_db_item(self):

    """ update vendor name based on the vendor id """

    update = """UPDATE accounts_items
                SET dynamic_stats = %s,
                    room_target = %s, 
                    is_open = %s, 
                    location = %s, 
                    location_body = %s, 
                    owner = %s
                WHERE uuid_id = %s"""
    
    conn = None
    updated_rows = 0

    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        # execute the UPDATE  statement
        cur.execute(update, (json.dumps(self.dynamic_stats), 
                             json.dumps(self.room_target), 
                             self.is_open, 
                             self.location, 
                             json.dumps(self.location_body), 
                             self.owner, 
                             self.uuid_id)
                            )
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()

        print("DB | Finished updating item to DB.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
 
    # return updated_rows

def update_db_player(self):

    """ update vendor name based on the vendor id """

    update = """UPDATE accounts_players
                SET core_attributes = %s,
                    player_state = %s, 
                    conditions = %s,
                    stow_loc = %s,
                    location = %s, 
                    vitals = %s,
                    credit = %s
                WHERE uuid_id = %s"""
    
    conn = None
    updated_rows = 0

    try:
        dbparams = config()
        conn = psycopg2.connect(**dbparams)
        cur = conn.cursor()

        # execute the UPDATE  statement
        cur.execute(update, (json.dumps(self.core_attributes), 
                             self.player_state, 
                             json.dumps(self.conditions), 
                             self.stow_loc, 
                             self.location, 
                             json.dumps(self.vitals), 
                             json.dumps(self.credit), 
                             self.uuid_id)
                            )
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()

        print("DB | Finished updating player to DB.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
 
    # return updated_rows