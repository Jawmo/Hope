import random
from pprint import pprint

from engine.global_config import *

from websocket_server.wswrap import WsWrap

from engine.lex import Lex
from engine.character import Character
from engine.update_client import Update_Client
from engine.sched_mgr.sched_mgr import Sched_Child


from engine.join_tables.join_table_items import *

class Combat():

	def __init__():
		pass

	def combat_flow(self, user_input, input_kwargs, combat_kwargs):
		
		# Debug ---
		print(f"COMBAT | FLOW | Entity: {self.name}, input_kwargs: {input_kwargs}, combat_kwargs: {combat_kwargs}")

		# Determine dmg output ---
		Combat.calc_dmg(self, user_input, input_kwargs, combat_kwargs)

		# Establish RT ---
		if self.entity_type['base'] == "player":

			self.round_time_set(combat_kwargs['round_time'])
			Update_Client.update_round_time(self)

			Lex.pub_print(
                self=self,
                target=None,
                send_kwargs={'type': 'text', 'spacing': 1},
                first_person = f"Round time, {combat_kwargs['round_time']} seconds...",
                target_person = "",
                third_person = "",)
		
		# Check death ---
		self.check_death(user_input, input_kwargs)


	def calc_dmg(self, user_input, input_kwargs, combat_kwargs):

		# Establish attack die and attack modifier from ammo, these are defaults
		# or overridden if items are present 

		weapon_base_dmg = 1
		weapon_base_dmg_mod = 0

		if self.inventory["r_hand"]["contents"]:

			weapon_base = combat_kwargs['attribute'] + "_base"
			weapon_mod_base = combat_kwargs['attribute'] + "_mod"

			# Override R hand weapon_base_dmg
			
			if weapon_base in self.inventory["r_hand"]["contents"].static_stats:
				if self.inventory["r_hand"]["contents"].static_stats[weapon_base]:
					weapon_base_dmg = self.inventory["r_hand"]["contents"].static_stats[weapon_base]			
		
			# Override R hand weapon_base_mod

			if weapon_mod_base in self.inventory["r_hand"]["contents"].static_stats:
				if self.inventory["r_hand"]["contents"].item_inv != []:
					if self.inventory["r_hand"]["contents"].entity_type['group'] == "gun":
						weapon_base_dmg_mod = items[self.inventory["r_hand"]["contents"].dynamic_stats['ammo_id']].static_stats[weapon_base]
	

		# Pull in attacker's appropriate attibute and create a base roll

		attrib_base = self.core_attributes[combat_kwargs['attribute']]['base']
		base_roll = random.randint(1, 12)

		# Base Attack is simply the attack die multiplied by the base roll
		base_att = attrib_base + weapon_base_dmg + weapon_base_dmg_mod + base_roll
		final_dmg = base_att


		# apply damage
		if input_kwargs['target'].inventory['suit']['contents'] == None:

			# client printing options
			if self.entity_type['base'] == "player":
				send_kwargs = {'type': 'text', 'spacing': 0}

			# if AI is performing
			elif self.entity_type['base'] == "npc":
				send_kwargs = {'type': 'text', 'spacing': 1}


			input_kwargs['target'].vitals['hp_current'] = input_kwargs['target'].vitals['hp_current'] - final_dmg

			if input_kwargs['target'].entity_type['base'] == 'player':
			
				Update_Client.update_player_health(input_kwargs['target'])

			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs = {'type': 'text', 'spacing': 0},
				first_person = "AB: {} + WBD: {} + WBDM: {} + BR: {} = {}".format(attrib_base, weapon_base_dmg, weapon_base_dmg_mod, base_roll, base_att),
				target_person = "AB: {} + WBD: {} + WBDM: {} + BR: {} = {}".format(attrib_base, weapon_base_dmg, weapon_base_dmg_mod, base_roll, base_att),
				third_person = "",
				)

			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs=send_kwargs,
				first_person = "You hit for {} damage!".format(final_dmg),
				
				target_person = "|alert| You take {} damage! |alertx|".format(
								final_dmg),

				third_person = "{} takes the force of the blow.".format(
								input_kwargs['target'].name),
				)

		else:

			if input_kwargs['target'].entity_type['base'] == 'player':

				if input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current'] > 0:

					if input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current'] < final_dmg:
						input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current'] = 0
					else:
						input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current'] = input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current'] - final_dmg

					Lex.pub_print(
					self=self,
					target=input_kwargs['target'],
					send_kwargs={'type': 'text', 'spacing': 1},
					first_person = "You see its shield glimmer as you hit for {} damage!".format(final_dmg),
					
					target_person = '|self_suit| "Shields absorb {} damage, {}% integrity." |self_suitx|'.format(
									final_dmg, input_kwargs['target'].inventory['suit']['contents'].vitals['shield_current']),

					third_person = "{}'s suit glimmers as it absorbs the damage.".format(
									input_kwargs['target'].name),
					)

				else:

					input_kwargs['target'].vitals['hp_current'] = input_kwargs['target'].vitals['hp_current'] - final_dmg
					Update_Client.update_player_health(input_kwargs['target'])

					Lex.pub_print(
					self=self,
					target=input_kwargs['target'],
					send_kwargs={'type': 'text', 'spacing': 1},
					first_person = "Shields are down! You hit for {} damage!".format(final_dmg),
					
					target_person = '|alert| "Your suit\'s shield is broken and your body takes {} damage!" |alertx|'.format(
									final_dmg),

					third_person = "",
					)


		return attrib_base, base_roll, final_dmg


	def fire_gun(self, user_input, input_kwargs):

		# Combat flow parameters ---

		combat_kwargs = {
			"round_time"		: 5,
			"combat_action"		: "fire_gun",
			"attribute"			: "dex"
		}

		# ---


		mag = items[self.inventory["r_hand"]["contents"].dynamic_stats['ammo_id']]
		mag.dynamic_stats['current_capacity'] -= 1

		Lex.pub_print(
			self=self,
			target=None,
			send_kwargs={'type': 'text', 'spacing': 0},
			first_person = "|self_speech| You fire your {} at {}! |self_speechx|".format(
							self.inventory["r_hand"]["contents"].name,
							Lex.a_an(input_kwargs['target'].name)),

			target_person = "",

			third_person = "{} fires {} {} at {}!".format(
							self.name, Lex.gender(self, "own"),
							self.inventory["r_hand"]["contents"].name,
							Lex.a_an(input_kwargs['target'].name)))

		# Run post-attack combat flow
		Combat.combat_flow(self, user_input, input_kwargs, combat_kwargs)

		if mag.dynamic_stats['current_capacity'] < 1:
			
			self.inventory["r_hand"]["contents"].dynamic_stats['loaded'] = False
			self.inventory["r_hand"]["contents"].dynamic_stats['ammo_id'] = None
			self.inventory["r_hand"]["contents"].item_inv.remove(items[mag.uuid_id])
			del items[mag.uuid_id]

			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = "|alert|You're dry!|alertx| You release the empty {} and it casually falls to the ground out of sight.".format(mag.name),
				target_person = "",
				third_person = "{} releases a spent magazine from {} {} and it falls aside.".format(self.name, Lex.gender(self, "own"), self.inventory["r_hand"]["contents"].name))
		else:
			pass

	def attack(self, user_input, input_kwargs):

		# Combat flow parameters ---
		
		combat_kwargs = {
			"round_time"		: 5,
			"combat_action"		: "attack",
			"attribute"			: "str"
		}

		# input_kwargs['round_time'] = round_time

		# input_kwargs["combat_action"] = "attack"

		# if player is performing
		if self.entity_type['base'] == "player":
			ent_label = "player"
			ent_name = self.name.capitalize()
			send_kwargs = {'type': 'text', 'spacing': 0}

		# if AI is performing
		elif self.entity_type['base'] == "npc":
			send_kwargs = {'type': 'text', 'spacing': 0}
			ent_label = "npc"
			ent_name = Lex.a_an(self.name).capitalize()
		
		# catch other errors
		else:
			ent_label = ""
			ent_name = "|error: no ent name|"

		# ---

		# LOG for reviewing attacks
		if self.entity_type['base'] == "npc":
			print("COMBAT | AI | CMD: ATTACK |", self.name, "attacking", input_kwargs['target'].name)
		else:
			print("COMBAT | PLAYER | CMD: ATTACK |", self.name, "attacking", input_kwargs['target'].name)


		# Determine if unarmed or armed attack and set nouns for rest of function
		if self.inventory["r_hand"]["contents"]:
			weapon = self.inventory["r_hand"]["contents"].name
		else:
			weapon = "fist"


		if self.inventory["r_hand"]['contents'] == None:
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs=send_kwargs,
				first_person = "|self_text| You swing a fist at {}! |self_textx|".format(
									Lex.a_an(input_kwargs['target'].name)),
				
				target_person = "{} swings a fist at you!".format(
									Lex.a_an(self.name).capitalize()),
	
				third_person = "{} swings a fist at {}!".format(
									ent_name,
									Lex.a_an(input_kwargs['target'].name))
				)

		else:
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs=send_kwargs,
				first_person = "|self_text| You swing {} at {}! |self_textx|".format(
								Lex.a_an(weapon),
								Lex.a_an(input_kwargs['target'].name)),
				
				target_person = "{} swings {} at you!".format(
								ent_name,
								Lex.a_an(weapon)),

				third_person = "{} swings {} at {}!".format(
								ent_name,
								Lex.a_an(weapon),
								Lex.a_an(input_kwargs['target'].name))
				)


		# Run post-attack combat flow
		Combat.combat_flow(self, user_input, input_kwargs, combat_kwargs)