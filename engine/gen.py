from engine.global_config import *
from engine.global_lists import *
import random

class Gen():

	def random_number(total_dice, die_min, die_max):

		d_min = die_min
		d_max = die_max

		current_total_dice = 0
		result = 0

		while current_total_dice < total_dice:
			roll = random.randint(d_min, d_max)
			result += roll
			current_total_dice += 1

		return result

	def random_movement(self):
		
		if rooms[self.location].exits:
			choice = random.choice(list(rooms[self.location].exits.keys()))
			return choice
		else:
			return None


	def players_in_room(self):
		
		player_list = []

		if rooms[self.location].player_inv:
			for i in rooms[self.location].player_inv:
				if self == i:
					pass
				else:
					player_list.append(i)

		# print("Players in room:", player_list)
		return player_list

	def players_in_exit_room(self, name, exit_room):
		
		players_in_exit_room = {}

		if rooms[exit_room].player_inv:
			for i in rooms[exit_room].player_inv:
				players_in_exit_room[i] = rooms[exit_room].player_inv[i]

		# print("PIER:", players_in_exit_room)
		return players_in_exit_room

	def items_in_container(self):

		item_list = []

		if self.item_inv:
			for i in self.item_inv:
				item_list.append(i)

		print("GEN | I in Container:", item_list)
		return item_list

	def items_in_room(self):

		item_list = []

		if rooms[self.location].item_inv:
			# print(rooms[self.location].item_inv)
			for i in rooms[self.location].item_inv:
				item_list.append(i)

		# print("Items in room:", item_list)
		return item_list

	def ships_in_room(self):

		item_ship_list = []
		ship_num = rooms[self.location].ship_id
		room_of_ship = rooms[items[ship_num].location]

		if room_of_ship.item_inv:
			for i in room_of_ship.item_inv:
				if i.room_target["target"] == self.location:
					pass
				elif i.entity_type['group'] != "ship":
					pass
				else:
					item_ship_list.append(i)

		# print("Items in room:", item_list)
		return item_ship_list

	def npcs_in_room(self):

		npc_list = []

		if rooms[self.location].npc_inv:
			for i in rooms[self.location].npc_inv:
				npc_list.append(i)

		# print("Items in room:", item_list)
		return npc_list