
from engine.suits.suit_templates import rabbit

class Rabbit(TacSuit):

	def __init__(self, uuid_id, entity_type, name, keyword, item_desc, size, weight, capacity,
                 worn, attributes, dynamic_stats, static_stats, room_target, combines_with, is_open,
                 item_inv, location, location_body, owner,
                 armor, hard_points, augments, compartments, vitals):

		super().__init__(uuid_id, attributes, dynamic_stats, room_target, is_open,
		                 item_inv, location, owner)

		self.static_stats = 	alpha_suit_table['stat_stats']
		self.entity_type = 		alpha_suit_table['entity_type']
		self.name = 			alpha_suit_table['name']
		self.keyword = 			alpha_suit_table['keyword']
		self.item_desc = 		alpha_suit_table['item_desc']
		self.size = 			alpha_suit_table['size']
		self.weight = 			alpha_suit_table['weight']
		self.capacity = 		alpha_suit_table['capacity']
		self.combines_with = 	alpha_suit_table['combines_with']
		self.worn = 			alpha_suit_table['worn']
		self.armor = 			alpha_suit_table['armor']
		self.hard_points = 		alpha_suit_table['hard_points']
		self.augments = 		alpha_suit_table['augments']
		self.compartments = 	alpha_suit_table['compartments']
		self.location_body = 	alpha_suit_table['location_body']
		self.vitals = 			alpha_suit_table['vitals']