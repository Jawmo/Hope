import uuid, copy
from engine.global_config import *
from engine.global_lists import *

from websocket_server.wswrap import WsWrap

from engine.rooms.room_procgen import Room_Procgen
from engine.npc import Npc
from engine.inventory import inv
from engine.sched_mgr.sched_mgr import Sched_Child
from engine.join_tables.join_table_npcs import npc_table
from engine.suits.suit import alpha_suit_table

class Admin_Cmd():

	def __init__(self):
		pass

	def spawn(self, user_input, input_kwargs):

		if self.entity_type["group"] != "admin":

			WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You must be an admin to do that.")

		else:

			creature = user_input[1]
			
			# try:
			npc_obj = Npc(**{
				"uuid_id": 			uuid.uuid4(),                     			# uuid
				"entity_type": 		npc_table[creature]['entity_type'],			# entity_type
				"join_table": 		creature,									# join_table reference name
				"vitals": 			npc_table[creature]['vitals'],				# vitals
				"core_attributes": 	npc_table[creature]['core_attributes'],   	# core_attributes
				"conditions": 		npc_table[creature]['conditions'], 			# conditions
				"credit": 			npc_table[creature]['credit'],            	# credit
				"inventory": 		copy.deepcopy(inv),        					# inventory
				"location": 		self.location,                          	# location
				"description": 		npc_table[creature]['description'],			# npc_desc
				"npc_state": 		npc_table[creature]['npc_state'],			# npc_state
				"supply": 			npc_table[creature]['supply'],				# supply
				"demand": 			npc_table[creature]['demand'],				# demand
				"home_loc": 		npc_table[creature]['home_loc'],          	# hom_loc
				"demeanor": 		npc_table[creature]['demeanor']				# demeanor
				})

			print(vars(npc_obj))

			npcs[npc_obj.uuid_id] = npc_obj
			Sched_Child.create_new_sched(npc_obj)

			WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, f"|alert|A {creature} runs in!|alertx|")

			rooms[self.location].npc_inv.append(npc_obj)
			npc_obj.conditions['awake'] = True

			# except AttributeError as e:
			# 	print("Admin Spawn:", e)

			# except:
			# 	WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, f"Syntax: spawn (npc_type)")

	def create_item():

		admin_item_list = {
			"rabbit suit" : {"func": Rabbit}
		}

	def create_instance(self, user_input, input_kwargs):

		print("ADMIN | Creating Instance:", user_input)
		Room_Procgen(**{'user': self, 'region': user_input[1].capitalize()})