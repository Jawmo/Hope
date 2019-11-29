import uuid

from engine.global_lists import *

from engine.item import Item
from engine.update_client import Update_Client

from engine.suits.suit_templates import alpha_suit_table
# from engine.suits.tac_rabbit import Rabbit

class TacSuit(Item):

	def __init__(self, **kwargs):

		if kwargs['join_table']['table']:
			if kwargs['join_table']['table'] == 'alpha_suit_table':
				table = alpha_suit_table
				entry = kwargs['join_table']['keyword']
			else:
				pass

		super().__init__(**kwargs)

		self.static_stats = 	table[entry]['static_stats']
		self.entity_type = 		table[entry]['entity_type']
		self.name = 			table[entry]['name']
		self.keyword = 			table[entry]['keyword']
		self.item_desc = 		table[entry]['item_desc']
		self.size = 			table[entry]['size']
		self.weight = 			table[entry]['weight']
		self.capacity = 		table[entry]['capacity']
		self.combines_with = 	table[entry]['combines_with']
		self.worn = 			table[entry]['worn']
		self.armor = 			table[entry]['armor']
		self.hard_points = 		table[entry]['hard_points']
		self.augments = 		table[entry]['augments']
		self.compartments = 	table[entry]['compartments']
		self.location_body = 	table[entry]['location_body']
		self.vitals = 			table[entry]['vitals']

	def action_pull(self, user_input, input_kwargs):

		WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You pull the suit.")

	def convert_entry_to_obj(self):

		print("CONVERTING item:", items[self], "|", items[self][0]['keyword'])

		new_suit = TacSuit(
			self,                                          					# uuid
	        alpha_suit_table[items[self][0]['keyword']]['entity_type'],     # entity_type
            items[self][1],                                					# name
            items[self][2],                                					# keyword
            items[self][3],                                					# item_desc
            alpha_suit_table[items[self][0]['keyword']]['size'],            # size
            alpha_suit_table[items[self][0]['keyword']]['weight'],          # weight
            alpha_suit_table[items[self][0]['keyword']]['capacity'],        # capacity
            alpha_suit_table[items[self][0]['keyword']]['worn'],            # worn
            items[self][4],                                					# attributes
            items[self][5],                                					# dynamic_stats
            alpha_suit_table[items[self][0]['keyword']]['static_stats'],    # static_stats
            items[self][6],                                					# room_target
            alpha_suit_table[items[self][0]['keyword']]['combines_with'],   # combines_with
            items[self][7],                                					# is_open
            [],                                         					# item_inv
            items[self][8],                                					# location
            items[self][9],                                					# location_body
            alpha_suit_table[items[self][0]['keyword']]['vitals'],                                				# vitals
            items[self][11])                               					# owner

		items[self] = new_suit

		print("CONVERT SUIT TO OBJ | FINISHED:", new_suit.name, new_suit, new_suit.location)

	def suit_shield_regen(self):
	
		if self.inventory['suit']['contents'].vitals['shield_current'] == 0:
			pass
		else:
			
			if self.inventory['suit']['contents'].vitals['shield_current'] + self.inventory['suit']['contents'].vitals['shield_regen_current'] > self.inventory['suit']['contents'].vitals['shield_max_current']:
				self.vitals['hp_current'] = self.vitals['hp_max']
			else:
				self.inventory['suit']['contents'].vitals['shield_current'] += self.inventory['suit']['contents'].vitals['shield_regen_current'] 
		
		Update_Client.update_suit_shield(self)