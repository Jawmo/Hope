from engine.global_config import *
from engine.functions import *
from engine.lex import *
from engine.room import *
from engine.ship.ship_main import Ship
from engine.handler.input_handler import Input_Handler

class Skill():
	def __init__(self, base_type, skill_type, name, description):
		self.base_type = base_type
		self.skill_type = skill_type
		self.name = name
		self.description = description

	def climb(self, user_input, input_kwargs):

		input_kwargs['target'] = Input_Handler.target_items_in_room(self, user_input[1], input_kwargs)
		print(input_kwargs['target'])

		if self.conditions['action'] == "on_wall":

			print("coord before:", self.conditions)
			print(self.conditions['wall_coord']['y'])

			if "climb" in user_input and "down" in user_input:
				self.conditions['wall_coord']['y'] = self.conditions['wall_coord']['y'] - 1

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You climb down.",
					target_person = "",
					third_person = "{} climbs down.".format(self.name))

			elif "climb" in user_input and "up" in user_input:
				self.conditions['wall_coord']['y'] = self.conditions['wall_coord']['y'] + 1

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You climb up.",
					target_person = "",
					third_person = "{} climbs up.".format(self.name))

			elif "climb" in user_input and "left" in user_input:
				self.conditions['wall_coord']['x'] = self.conditions['wall_coord']['x'] - 1

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You climb to the left.",
					target_person = "",
					third_person = "{} climbs to the left.".format(self.name))

			elif "climb" in user_input and "right" in user_input:
				self.conditions['wall_coord']['x'] = self.conditions['wall_coord']['x'] + 1

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You climb to the right.",
					target_person = "",
					third_person = "{} climbs to the right.".format(self.name))

			else:
				server.send_message(self.client, speech, "Climb which way?")


			if self.conditions['wall_coord']['y'] == 0:

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You reach the bottom and step down.",
					target_person = "",
					third_person = "{} reaches the bottom and steps down.".format(self.name))

				self.conditions['action'] == "standing"
			
			elif self.conditions['wall_coord']['y'] == 5:
				
				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You reach the top and climb up on to the surface.",
					target_person = "",
					third_person = "{} reaches the top and climbs up on to the surface.".format(self.name))

				self.conditions['action'] = "standing"

				rooms[self.current_room].player_inv.remove(self)
				self.current_room = rooms[items[self.conditions['wall_coord']['wall_id']].room_target['top']].uuid_id
				rooms[self.current_room].player_inv.append(self)
				Room.display_room(self)
				del self.conditions['wall_coord']

			print("coord after:", self.conditions)

		elif input_kwargs['target'] == None or "must_climb" not in input_kwargs['target'].attributes:
			server.send_message(self.client, speech, "Climb what?")

		else:

			if "hole_vertical" == input_kwargs['target'].item_type:
				
				# wall = target.room_target[list(target.room_target.keys())[0]]
				wall = input_kwargs['target'].room_target['wall_id_in_target']
				print("wall", wall)
				wall_room = rooms[input_kwargs['target'].room_target['target']].uuid_id
				print("w_room", wall_room)
				self.conditions['action'] = "on_wall"

				# wall coordinate and difficulty {x, y, wall_item_id}
				self.conditions['wall_coord'] = {"x": 0, "y": 4, "wall_id": wall}

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You climb {}.".format(Lex.a_an(input_kwargs['target'].name)),
					target_person = "",
					third_person = "{} climbs {}.".format(self.name, Lex.a_an(input_kwargs['target'].name)))

				rooms[self.current_room].player_inv.remove(self)
				self.current_room = wall_room
				rooms[self.current_room].player_inv.append(self)
				Room.display_room(self)

				server.send_message(self.client, speech, "")

				Lex.pub_print(
					self=self,
					target=None,
					first_person = "You cling to the rock wall just below the edge of the hole.",
					target_person = "",
					third_person = "{} just climbed {}.".format(self.name, Lex.a_an(input_kwargs['target'].name)))