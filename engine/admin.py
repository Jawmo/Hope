from engine.global_config import *
import psycopg2
from config import config
import json

class Admin_Commands():
    def __init__(self, name):
        self.name = name

    def fill_db():

        insert_item = """INSERT INTO items(uuid_id, name, item_desc, base_type, size, weight, capacity, can_attributes, room_target, combines_with, is_open, location, location_body, owner)
                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                         RETURNING uuid_id, name, item_desc, base_type, size, weight, capacity, can_attributes, combines_with, room_target, is_open, location, location_body, owner;"""

        insert_room = """INSERT INTO rooms(uuid_id, room_type, name, description, exits, region, zone, effects, owner) 
                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                         RETURNING uuid_id, room_type, name, description, exits, region, zone, effects, owner;"""

        insert_player = """INSERT INTO players(uuid_id, name, gender, hp, core_attributes, player_state, conditions, credit, stow_loc, current_room) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                           RETURNING uuid_id, name, gender, hp, core_attributes, player_state, conditions, credit, stow_loc, current_room;"""

        insert_npc = """INSERT INTO npcs(uuid_id, base_type, name, race, gender, npc_desc, core_attributes, npc_state, conditions, credit, supply, demand, home_loc, demeanor, current_room) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                           RETURNING uuid_id, base_type, name, race, gender npc_desc, core_attributes, npc_state, conditions, credit, supply, demand, home_loc, demeanor, current_room;"""

        insert_org = """INSERT INTO orgs(uuid_id, name, org_desc, supply, demand, home)
                           VALUES(%s, %s, %s, %s, %s, %s) 
                           RETURNING uuid_id, name, org_desc, supply, demand, home;"""

        conn = None
        try:
            dbparams = config()
            conn = psycopg2.connect(**dbparams)
            cur = conn.cursor()

            # insert a new part

            # uuid, name, item_desc, base_type, size, weight, capacity, can_attributes, combines_with, is_open, location, location_body, owner
            cur.execute(insert_item, ("70306652-fbda-479a-a06d-48b411911ed7", "9mm magazine", "It's a 9mm magazine.", "ammo_9mm", 1, 1, 10, None, "", "pistol_9mm", False, "65d56cbe-f276-4055-899c-3244c0c92003", None, "da",))
            cur.execute(insert_item, ("035d0c23-fbda-479a-a06d-48b411911ed7", "9mm pistol", "Mmm, shiny.", "pistol_9mm", 2, 2, 10, "is_gun", "", "ammo_9mm", False, "65d56cbe-f276-4055-899c-3244c0c92003", None, "da",))
            cur.execute(insert_item, ("6123e586-93c7-4fff-8787-3ca5706ad2a8", "rabbit toy", "Huh, looks real.", "toy", 1, 1, 0, None, "", None, False, "70306652-08cf-4c99-ac7d-c8bd1082220c", None, "da",))
            cur.execute(insert_item, ("70306652-08cf-4c99-ac7d-c8bd1082220c", "backpack", "It's a backpack.", "storage_backpack", 2, 2, 0, "is_container", "", None, False, "c93e5db1-fabe-496f-a6a6-6769a1bf1404", "r_hand", "da",))
            cur.execute(insert_item, ("e87c6768-0e3d-4f52-92b8-56ad69f63bea", "shuttle", "This shuttle belongs to the S.S. Hope.", "ship", 0, 5000, 0, "is_door", "ba0d6g25-ae3r-43n8-b25c-1f4342chyfd0", None, True, "65d56cbe-f276-4055-899c-3244c0c92003", "", "da",))
            
            cur.execute(insert_room, ("65d56cbe-f276-4055-899c-3244c0c92003", None, "ship_capital_dock", "Shuttle Bay", "The room is simple.", json.dumps({"north": "aa0dd325-ae9e-43b0-b25c-1f4803ceefd0"}), "S.S. Hope", "space", None, "da",))
            cur.execute(insert_room, ("aa0dd325-ae9e-43b0-b25c-1f4803ceefd0", None, "ship_capital_dock", "Shuttle Bay", "The room is simple.", json.dumps({"south": "65d56cbe-f276-4055-899c-3244c0c92003"}), "S.S. Hope", "space", None, "aa",))
            cur.execute(insert_room, ("ba0d6g25-ae3r-43n8-b25c-1f4342chyfd0", "e87c6768-0e3d-4f52-92b8-56ad69f63bea", "ship_private_main", "Shuttle", "You see the inside of the shuttle.", json.dumps({"out": "65d56cbe-f276-4055-899c-3244c0c92003"}), "shuttle", "shuttle", None, "da",))
            cur.execute(insert_room, ("ny0d6j56-ae3r-43n8-m28s-1f4342chyfd0", None, "planet_forest", "Forest", "There are lots of trees.", json.dumps({"south": "aa0dd234-ab72-32b6-c93c-1f4803ceefd0"}), "shuttle", "shuttle", None, "da",))
            cur.execute(insert_room, ("34d66jru-f276-2144-384v-3244c0c92003", None, "space", "Space", "Like a back-lit canopy, the stars and galaxies shine across the black.", json.dumps({}), "shuttle", "shuttle", None, "da",))
            cur.execute(insert_room, ("aa0dd234-ab72-32b6-c93c-1f4803ceefd0", None, "e87c6768-0e3d-4f52-92b8-56ad69f63bea", "planet_landing", "Open Field", "Tall, golden wheat grows wild here. You can see the edge of a dense forest to the north.", json.dumps({"north": "ny0d6j56-ae3r-43n8-m28s-1f4342chyfd0"}), "shuttle", "shuttle", None, "da",))
            cur.execute(insert_room, ("pp2aa543-ab72-93n1-c93c-1f4803ceefd0", None, "e87c6768-0e3d-4f52-92b8-56ad69f63bea", "space_orbit", "Orbit around Oxine", "Green and blue hues decorate the planet of Oxine.", json.dumps({"entry": "aa0dd234-ab72-32b6-c93c-1f4803ceefd0"}), "shuttle", "shuttle", None, "da",))
            
            cur.execute(insert_player, ("c93e5db1-fabe-496f-a6a6-6769a1bf1404", "da", "male", 100, json.dumps({"str": 12, "dex": 8, "con": 15, "ins": 6, "edu": 5, "soc": 6}), "standing", None, 100, None, "65d56cbe-f276-4055-899c-3244c0c92003",))
            cur.execute(insert_player, ("3563874d-8646-487f-8beb-3c0278d2f292", "ry", "female", 100, json.dumps({"str": 8, "dex": 12, "con": 8, "ins": 12, "edu": 10, "soc": 10}), "standing", None, 100, None, "65d56cbe-f276-4055-899c-3244c0c92003",))
            cur.execute(insert_player, ("06ce6e88-f666-4cac-9901-698f7464e1c5", "fa", "female", 100, json.dumps({"str": 8, "dex": 12, "con": 8, "ins": 12, "edu": 10, "soc": 10}), "standing", None, 100, None, "65d56cbe-f276-4055-899c-3244c0c92003",))

            cur.execute(insert_npc, ("c93e5db1-08cf-4cac-a06d-c8bd1082220c", "npc_human", "Lt. Dan", "human", "male", "He looks like he's busy.", json.dumps({"str": 5, "dex": 5, "con": 5, "ins": 5, "edu": 5, "soc": 5}), "standing", None, 100, json.dumps({}), json.dumps({}), "S.S. Hope", "friendly", "65d56cbe-f276-4055-899c-3244c0c92003"))
            cur.execute(insert_npc, ("c93e5db1-08cf-4cac-a06d-c8bd1082220c", "npc_predator", "Predator", "onxine", "male", "He looks mean.", json.dumps({"str": 5, "dex": 5, "con": 5, "ins": 5, "edu": 5, "soc": 5}), "standing", None, 100, json.dumps({}), json.dumps({}), "Oxine", "Hostile", "ny0d6j56-ae3r-43n8-m28s-1f4342chyfd0"))
            
            cur.execute(insert_org, ("6123e586-f276-4c99-a06d-48b411911ed7", "Heiss", "A humanoid race focused heavily on cybernetics and augments.", json.dumps({}), json.dumps({}), "Eroli"))
            
            # commit changes
            conn.commit()
            print("Done adding objects to DB.")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def create_instance(self, user, user_input, input_kwargs):

        print("ADMIN | Creating Instance:", user_input)
        Room_Procgen(user_input[1])