from engine.lex import Lex
from engine.gen import Gen
from pprint import pprint

class Input_Handler():
	def __init__():
		pass

	def full_handler(self, user_input, input_kwargs):
			
		target = None
		print("HANDLER | Searching for target:", user_input)

		if target == None:
			print("Checking  1")
			target = Input_Handler.target_items_in_room(self, user_input, input_kwargs)
				
			if target == None:
				print("Checking  2")
				target = Input_Handler.target_npcs_in_room(self, user_input, input_kwargs)
			
				if target == None:
					print("Checking  3")
					target =  Input_Handler.target_players_in_room(self, user_input, input_kwargs)

					if target == None:
						print("Checking  4")
						target =  Input_Handler.target_self(self, user_input, input_kwargs)
		
						if target == None:
							print("Checking  5")
							target =  Input_Handler.target_self_inventory(self, user_input, input_kwargs)
		
							if target == None:
								print("Checking  6")
								target =  Input_Handler.target_items_in_self_r_hand(self, user_input, input_kwargs)
		
								if target == None:	
									print("Checking  7")
									target =  Input_Handler.target_items_in_self_l_hand(self, user_input, input_kwargs)
		
		if target is not None:
			print("HANDLER | Target in Full Handler:", pprint(target), target.name)
			# pprint(vars(target))
		else:
			print("HANDLER | Target in Full Handler:", target)

		return target

	def target_items_in_room(self, user_input, input_kwargs):

		# check if the target is an item in the room
		target = None

		for y in Gen.items_in_room(self):

			if Lex.first_three(y.keyword) in user_input:
				target = y
				print("HANDLER | Target Found: item in room, ", target)

		return target

	def target_items_in_container(self, user_input, input_kwargs):

		target = None

		for y in Gen.items_in_container(input_kwargs['target_parent']):
			if Lex.first_three(y.keyword) in user_input:
				target = y
				print("HANDLER | Target Found: item in container, ", target)

		# print("Items in room:", item_list)
		return target

	def target_npcs_in_room(self, user_input, input_kwargs):

		# check if the target is an NPC in the room

		for npc in Gen.npcs_in_room(self):
			if user_input in npc.name.lower():
				target = npc
				print("HANDLER | Target Found: NPC, ", target)
				break
				
		else:
			target = None

		return target

	def target_players_in_room(self, user_input, input_kwargs):
		# check if the target is a player in the room
	
		for player in Gen.players_in_room(self):
			if user_input in player.name:
				target = player
				print("HANDLER | Target Found: player, ", target)
				break

		else:
			target = None

		return target

	def target_self(self, user_input, input_kwargs):
	
		# check if you are the target

		if self.name == user_input:
			target = self
			print("HANDLER | Target Found: self, ", target)

		else:
			target = None

		return target

	def target_self_inventory(self, user_input, input_kwargs):

		# check if the target is in your inventory
		target = None

		for inv in self.inventory:
			if self.inventory[inv]['contents']:
				item = self.inventory[inv]['contents']
			
				if Lex.first_three(item.keyword) in user_input:
					target = item

		return target

	def target_items_in_self_r_hand(self, user_input, input_kwargs):

		# check right hand
		target = None
		print("hand user_input:", user_input)
        
		if self.inventory['r_hand']['contents']:		
			if Lex.first_three(self.inventory['r_hand']['contents'].keyword) in user_input:
				target = item
				print("HANDLER | Target Found: self r_hand, ", target)
	
		return target

	def target_items_in_self_l_hand(self, user_input, input_kwargs):

		# check left hand next
		target = None
		print("hand user_input:", user_input)

		if self.inventory['l_hand']['contents']:		
			if Lex.first_three(self.inventory['l_hand']['contents'].keyword) in user_input:
				target = item
				print("HANDLER | Target Found: self l_hand, ", target)

		return target