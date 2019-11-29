import uuid

from engine.global_config import *
from engine.db_commands import *
from engine.update_client import Update_Client

from engine.lex import *
from engine.item import Item

from engine.join_tables.join_table_items import *
from engine.suits.suit_templates import alpha_suit_table

class Gun(Item):

	def __init__(self, **kwargs):
		
		super().__init__(**kwargs)

	def ammo_load(self, user_input, input_kwargs):

		if self.inventory['r_hand']['contents'] != input_kwargs['target']:
			WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That must be in your right hand.")
		else:

			if "is_gun" not in input_kwargs['target'].attributes:
				WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That can't be loaded.")
			else:

				if self.inventory['l_hand']['contents'] == None:
					WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You need ammo in your left hand.")
				else:

					s_type = self.inventory['r_hand']['contents'].entity_type['model']
					s_mod = self.inventory['r_hand']['contents'].entity_type['sub_model']
					c_with = self.inventory['l_hand']['contents'].combines_with
					logging.debug('%s %s %s', ":", s_mod, c_with)
					logging.debug('%s %s', ":", "-----------")

					if s_mod not in c_with:
						WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "This is the wrong ammo type.")
					else:

						# gun loading animation

						animate_first, animate_target, animate_third = self.inventory["r_hand"]["contents"].animation_load(self, user_input, input_kwargs)

						Lex.pub_print(
							self=self,
							target=None,
							send_kwargs={'type': 'text', 'spacing': 1},
							first_person = animate_first,
							target_person = animate_target,
							third_person = animate_third)

						# end animation
						
						self.inventory["r_hand"]["contents"].dynamic_stats['loaded'] = True
						self.inventory["r_hand"]["contents"].dynamic_stats['ammo_id'] = self.inventory['l_hand']['contents'].uuid_id
						self.inventory['r_hand']['contents'].item_inv.append(self.inventory['l_hand']['contents'])
						self.inventory['l_hand']['contents'].location = self.inventory['r_hand']['contents'].uuid_id
						self.inventory['l_hand']['contents'] = None

						

		Update_Client.update_player_inventory(self)

	def ammo_unload(self, user_input, input_kwargs):

		if self.inventory['r_hand']['contents'] != input_kwargs['target']:
			WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "That must be in your right hand.")
		else:

			if "is_gun" not in self.inventory['r_hand']['contents'].attributes:
				WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't unload that.")
			else:

				if self.inventory['r_hand']['contents'].item_inv == []:
					WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "It's empty.")
				else:

					if self.inventory['l_hand']['contents'] != None:
						WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You need an empty left hand.")
					else:

							clip = items[self.inventory['r_hand']['contents'].dynamic_stats['ammo_id']]
							
							self.inventory['r_hand']['contents'].dynamic_stats['loaded'] = False
							self.inventory['r_hand']['contents'].dynamic_stats['ammo_id'] = None
							self.inventory['l_hand']['contents'] = clip
							self.inventory['r_hand']['contents'].item_inv.remove(clip)

							Lex.pub_print(
								self=self,
								target=input_kwargs['target'],
								send_kwargs={'type': 'text', 'spacing': 1},
								first_person = "The magazine slides out into your left hand.",
								target_person = "{} unloads {} {}.".format(self.name, Lex.gender(self, "own"), self.inventory['r_hand']['contents'].name),
								third_person = "{} unloads {} {}.".format(self.name, Lex.gender(self, "own"), self.inventory['r_hand']['contents'].name))

		Update_Client.update_player_inventory(self)


	def ammo_check(self, user_input, input_kwargs):
		if self.inventory['r_hand']['contents'] != input_kwargs['target'] and self.inventory['l_hand']['contents'] != input_kwargs['target']:
			WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "Check what?")
		else:

			if self.inventory['r_hand']['contents'] != input_kwargs['target']:
				WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "It needs to be in your right hand.")
			else:

				if self.inventory['l_hand']['contents'] != None:
					WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You need a free left hand.")
				else:

					if self.inventory['r_hand']['contents'].item_inv == []:
						WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "It's empty.")
					else:

						if "is_gun" not in input_kwargs['target'].attributes:
							WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "You can't check the ammo of this item.")
						else:

							if self.inventory['r_hand']['contents'].item_inv == []:
								WsWrap.ws_send(self.client, {'type': 'text', 'spacing': 1}, "It's empty.")
							else:

								clip = items[self.inventory['r_hand']['contents'].dynamic_stats['ammo_id']]

								Lex.pub_print(
									self=self,
									target=None,
									send_kwargs={'type': 'text', 'spacing': 1},
									first_person = "The magazine slides out and you see |y|{} rounds |yx| before snapping it back in.".format(clip.dynamic_stats['current_capacity']),
									target_person = "",
									third_person = "{} slides a magazine from {} {} and examines it before snapping it back in.".format(self.name, Lex.gender(self, "own"), self.inventory['r_hand']['contents'].name))