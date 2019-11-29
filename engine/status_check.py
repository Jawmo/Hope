from engine.handler.input_handler import Input_Handler
from websocket_server.wswrap import WsWrap
from engine.lex import *

class Status_Check():

	def __init__(self):
		pass

	def container_is_open(self, user_input, input_kwargs):
		
		if input_kwargs.get('target_parent') is not None:

			if input_kwargs['target_parent'].is_open == input_kwargs['cmd_req']:
				status = True
				response = self.name

			else:
				status = False
				response = "That is closed."

		else:
				status = False
				response = "Error in container_is_open."

		return status, response

	def container_required(self, user_input, input_kwargs):
		
		print("HANDLER | Cont Required:", user_input[3])

		input_kwargs['target_parent'] = Input_Handler.full_handler(self, user_input, user_input[3])

		if input_kwargs['target'] != input_kwargs['cmd_req']:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			response = "Can't seem to find that."

		return status, response

	def hands_free(self, user_input, input_kwargs):
		
		if self.inventory['l_hand']['contents'] == input_kwargs['cmd_req'] and self.inventory['r_hand']['contents'] == input_kwargs['cmd_req']:
			status = True
			response = input_kwargs['cmd_req']

		else:
			status = False
			response = "Your hands must be empty."

		return status, response

	def has_ammo(self, user_input, input_kwargs):
		# if self.inventory['r_hand']['contents']
		req = input_kwargs['cmd_req']

		# set final
		if self.inventory['r_hand']['contents'].dynamic_stats['loaded'] == True:
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = input_kwargs['target']
		else:
			status = False

			if req == True:
				response = "It is not loaded."
			else:
				response = "It is already loaded."

		return status, response

	def holding_target(self, user_input, input_kwargs):
		
		holding = False
		
		if input_kwargs['target'] == self.inventory['r_hand']['contents'] or input_kwargs['target'] == self.inventory['l_hand']['contents']:
			holding = True
			
		if holding == input_kwargs['cmd_req']:
			status = True
			response = "Holding True"
		else:
			status = False
			response = "You must be holding that."

		return status, response

	def is_admin(self, user_input, input_kwargs):
		
		req = input_kwargs['cmd_req']

		# set final
		if self.entity_type['base'] == "player":
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = user_input
		else:
			status = False
			response = "Do what?"

		return status, response

	def is_alive_self(self, user_input, input_kwargs):
		
		req = input_kwargs['cmd_req']

		# set final
		if self.vitals['alive'] == True:
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = user_input
		else:
			status = False
			response = "|alert|You're dead!|alertx| You can't do that right now."

		return status, response
	
	def is_alive_target(self, user_input, input_kwargs):
		
		req = input_kwargs['cmd_req']

		# set final

		if input_kwargs['target'].vitals['alive'] == req:
			final = True

		else:
			final = False

			if req == True:
				
				special_response = "{} is already dead.".format(Lex.gender(input_kwargs['target'], "pro").capitalize())
			
			elif req == False:

				special_response = "{} is not dead!".format(Lex.gender(input_kwargs['target'], "pro").capitalize())


		# final check against the requirement
		if final == True:
			status = True
			response = user_input
		else:
			status = False
			response = special_response

		return status, response

	def is_gun(self, user_input, input_kwargs):
		
		req = input_kwargs['cmd_req']

		if self.inventory['r_hand']['contents'] == None:
			final = False

		elif "is_gun" in self.inventory['r_hand']['contents'].attributes:
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			response = "You need a suitable weapon in your right hand to do that."

		return status, response
	
	def is_npc(self, user_input, input_kwargs):

		req = input_kwargs['cmd_req']

		# set final
		if input_kwargs['target'].entity_type['base'] == "npc":
			final = True

		elif input_kwargs['target'].entity_type['base'] != "npc":
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			response = "It must be an NPC target."

		return status, response

	def is_owner(self, user_input, input_kwargs):
		
		if self.name == input_kwargs['cmd_req']:
			status = True
			response = self.name

		else:
			status = False
			response = "That does not belong to you."

		return status, response

	def is_wearable(self, user_input, input_kwargs):

		req = input_kwargs['cmd_req']

		if "is_wearable" in input_kwargs['target'].attributes:
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			repsonse = "You cannot wear that."

		return status, response

	def is_worn(self, user_input, input_kwargs):

		req = input_kwargs['cmd_req']

		if input_kwargs['target'].location_body['state'] == "worn":
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			response = "You are wearing that."

		return status, response

	def item_open_closed(self, user_input, input_kwargs):

		# if user_input[0] != "open" and user_input[0] != "close":

		# 	status = False
		# 	response = "That didn't work."

		# else:

		if "is_container" not in input_kwargs['target'].attributes:
			status = False
			response = "It doesn't seem to do that."

		else:

			if input_kwargs['cmd_req'] == "open":
				if input_kwargs['target'].is_open == False:
					status = True
					response = input_kwargs['cmd_req']

				else:
					status = False
					response = "That is already open."			

			elif input_kwargs['cmd_req'] == "close":
				if input_kwargs['target'].is_open == True:
					status = True
					response = input_kwargs['cmd_req']
				
				else:
					status = False
					response = "That is closed."
			else:

				if input_kwargs['target'].is_open == True:
					status = True
					response = input_kwargs['target']
				else:
					status = False
					response = "That must be open."

		return status, response

	def one_hand_free(self, user_input, input_kwargs):

		if self.inventory['r_hand']['contents'] == input_kwargs['cmd_req']:
			status = True
			response = "r_hand"

		elif self.inventory['l_hand']['contents'] == input_kwargs['cmd_req']:
			status = True
			response = input_kwargs['cmd_req']

		else:
			status = False
			response = "You need a free hand."

		return status, response

	def movable(self, user_input, input_kwargs):

		if input_kwargs['target'].entity_type['base'] == "item":
			if input_kwargs['target'].weight != input_kwargs['cmd_req']:
				status = True
				response = None
			else:
				status = False
				response = "You can't move that."
		else:
				status = False
				response = "You can't move that."

		return status, response

	def round_time(self, user_input, input_kwargs):

		req = input_kwargs['cmd_req']

		# set final
		if self.conditions['round_time'] == 0:
			final = True

		else:
			final = False

		# final check against the requirement
		if final == req:
			status = True
			response = self.conditions['round_time']
		else:
			status = False
			response = "Please wait {} seconds...".format(self.conditions['round_time'])

		return status, response

	def stance(self, user_input, input_kwargs):

		if self.conditions['stance'] == input_kwargs['cmd_req']:
			status = True
			response = input_kwargs['cmd_req']

		# elif self.conditions['stance'] in input_kwargs['cmd_req']:
		# 	status = True
		# 	response = input_kwargs['cmd_req']

		else:
			status = False
			response = "You must {} to do that.".format(input_kwargs['cmd_req'])

		return status, response

	def target_required(self, user_input, input_kwargs):

		input_kwargs['target'] = None
		input_kwargs['target_parent'] = None		
		
		if len(user_input) < 2:
			pass
		
		elif user_input[1] == "in":
			input_kwargs['target'] = Input_Handler.full_handler(self, user_input[2], input_kwargs)

		elif len(user_input) > 2:
			
			if user_input[2] == "from":
				input_kwargs['target_parent'] = Input_Handler.full_handler(self, user_input[3], input_kwargs)
				
				if input_kwargs['target_parent'] is not None:
					input_kwargs['target'] = Input_Handler.target_items_in_container(self, user_input[1], input_kwargs)
				else:
					input_kwargs['target'] = Input_Handler.full_handler(self, user_input[1], input_kwargs)

			elif user_input[2] == "in":
				input_kwargs['target_parent'] = Input_Handler.full_handler(self, user_input[3], input_kwargs)
				input_kwargs['target'] = Input_Handler.full_handler(self, user_input[1], input_kwargs)
		
		else:
			input_kwargs['target'] = Input_Handler.full_handler(self, user_input[1], input_kwargs)


		if input_kwargs['target'] != input_kwargs['cmd_req']:
			status = True
			response = input_kwargs['target']
		else:
			status = False
			response = "Can't seem to find that."

		return status, response

	def target_valid(self, user_input, input_kwargs):

		req = input_kwargs['cmd_req']

		# set final

		if input_kwargs['target'].entity_type['base'] == "npc":
			final = True
			response = user_input
		else:
			final = False
			response = user_input

		# final check against the requirement
		if final == req:
			status = True
			response = user_input
		else:
			status = False
			response = "That is not a valid target."

		return status, response