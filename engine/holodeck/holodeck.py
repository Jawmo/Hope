import uuid

from engine.global_lists import *

from websocket_server.wswrap import WsWrap

from engine.room import Room
from engine.lex import Lex
from engine.holodeck.holodeck_scenarios import scenarios

class Holodeck():

	def __init__(self, uuid_id, room_count, room_list):
		
		self.uuid_id = uuid.uuid4()
		self.room_count = room_count
		self.room_list = room_list

	def enter_holo(self, user_input, input_kwargs):	

		holo_template = "6942edc5-1f21-4164-86e7-b10f7a3d0b6a"

		new_holo = Room(**{"uuid_id": uuid.uuid4(),  	# uuid
                        "entity_type": rooms[holo_template].entity_type,   # base_type
                        "ship_id": rooms[holo_template].ship_id,    	# ship_id
                        "coordinates": rooms[holo_template].coordinates, # coordinates
                        "name": rooms[holo_template].name,    	# name
                        "description": rooms[holo_template].description, # description
                        "exits": {"out": self.location},    	# exits
                        "region": rooms[holo_template].region,    	# region
                        "zone": rooms[holo_template].zone,    	# zone
                        "elevation": rooms[holo_template].elevation,   # elevation
                        "effects": rooms[holo_template].effects,   	# effects
                        "player_inv": rooms[holo_template].player_inv,  # player_inv
                        "item_inv": rooms[holo_template].item_inv,   	# item_inv
                        "npc_inv": rooms[holo_template].npc_inv,   	# npc_inv
                        "mob_inv": rooms[holo_template].mob_inv,   	# mob_inv
                        "owner": rooms[holo_template].owner})   	# owner

		rooms[new_holo.uuid_id] = new_holo

		rooms[self.location].player_inv.remove(self)
		print("before holo:", self.location)
		self.location = new_holo.uuid_id
		print("after holo:", self.location)
		rooms[self.location].player_inv.append(self)
		Room.display_room(self)

		Lex.pub_print(
			self=self,
			target=None,
			send_kwargs = {'type': 'text', 'spacing': 1}, 
			first_person = "",
			target_person = "",
			third_person = "{} just arrived.".format(self.name))

	def create_simulation(self, user_input, input_kwargs):

		Room.create_room()

		new_holo = Holodeck(self,
							scenarios['test']['room_count'],
							scenarios['test']['room_list'])

		holodecks[new_holo.uuid_id] = new_holo

	def start_simulation(self, user_input, input_kwargs):

		holo = Holodeck.create_simulation(self, user_input, input_kwargs)

		self.location = None

		WsWrap.ws_send(self.client, speech, "Your surroundings shift and you see {}.".format())

