import random, uuid, pprint, copy

from engine.global_lists import *
from engine.lex import Lex

from engine.room import Room
from engine.item import Item
from engine.update_client import Update_Client

from engine.join_tables.join_table_items import *

from engine.rooms.room_regions import room_regions


class Room_Procgen():

	def __init__(self, **kwargs):

		self.uuid_id = uuid.uuid4()

		self.user = kwargs['user']

		# when creating an instance, set the region type, e.g. jungle, ships, etc.
		self.region = kwargs['region']
		self.zone = str(uuid.uuid4())
		
		# set grid for coordinates and room location tracking, x * y (z disabled)
		self.min_x = 0
		self.min_y = 0
		self.max_x = random.randint(3, 15)
		self.max_y = random.randint(3, 15)
		self.max_size = self.max_x * self.max_y
		print("PROCGEN | Instance Size:", self.max_x, self.max_y)

		# set size to 0 to match max_size later
		self.current_size = 0

		# exit list (up/down disabled currently)
		self.exit_types = ["north", "south", "east", "west"]

		# how many total rooms to create
		self.total_rooms_on_path = random.randint(2, self.max_size)

		print("PROCGEN | Creating Instance. Max Size:", self.max_size, "| Total Rooms on Path:", self.total_rooms_on_path)

		# list of the room uuids:
		# 	uuid_id : room object
		self.instance = []

		# add instance to global instance list to be able to modify entire instance
		instances[self.uuid_id] = self

		# run procgen
		self.procgen_flow()

	def procgen_flow(self):
		
		first_room = self.create_first_room()
		self.create_path(first_room, random.choice(self.exit_types))

		print("PROCGEN | Finished creating path.")

		print("PROCGEN | Rooms:")
		for i in self.instance:
			print(i, i.coordinates)

	def create_first_room(self):
		
		# create the first room
		room_obj = self.create_room()
		self.current_size += 1

		# pick a random spot in the max_size grid
		room_obj.coordinates['x'] = 0
		room_obj.coordinates['y'] = 0

		# add to global room list
		rooms[room_obj.uuid_id] = room_obj

		# add to local instance room list
		self.instance.append(room_obj)

		# create portal to first room from current room
		portal_in = Item(
			uuid_id =          uuid.uuid4(),
	        join_table =       {"module": "Item", "class": "Item", "table": "item_table", "keyword": "door_ship_visible"},
	        description =      {"name": "portal", "desc": "Looks like a black void with purple clouds encircling it."},
	        keyword =          "portal",
	        attributes =       {"is_door"},
	        dynamic_stats =    {},
	        room_target =      {'target': room_obj.uuid_id},
	        location =         self.user.location,
	        location_body =    None,
	        owner =            None,
	        is_open =          True,
	        vitals =           {})

		portal_out = Item(
			uuid_id =          uuid.uuid4(),
	        join_table =       {"module": "Item", "class": "Item", "table": "item_table", "keyword": "door_ship_visible"},
	        description =      {"name": "portal", "desc": "Looks like a black void with purple clouds encircling it."},
	        keyword =          "portal",
	        attributes =       {"is_door"},
	        dynamic_stats =    {},
	        room_target =      {'target': rooms[self.user.location].uuid_id},
	        location =         room_obj.uuid_id,
	        location_body =    None,
	        owner =            None,
	        is_open =          True,
	        vitals =           {})

		# pprint.pprint(vars(portal_in))
		# pprint.pprint(vars(portal_out))

		# add portal into instance in current room
		items[portal_in.uuid_id] = portal_in
		rooms[portal_in.location].item_inv.append(portal_in)

		# add exit portal from instance back to original room
		items[portal_out.uuid_id] = portal_out
		rooms[portal_out.location].item_inv.append(portal_out)

		Lex.pub_print(
            self=self.user,
            target=None,
            send_kwargs={'type': 'text', 'spacing': 1},
            first_person = 'A portal suddenly appears.',
            target_person = "",
            third_person = 'A portal suddenly appears.')

		print("PROCGEN | Created First Room:", room_obj.name, "|", room_obj.coordinates, "|", room_obj.exits)
		return room_obj

	def get_left_right(self, current_dir):

		if current_dir == "north":
			left = "west"
			right = "east"
		elif current_dir == "south":
			left = "east"
			right = "west"
		elif current_dir == "east":
			left = "north"
			right = "south"
		elif current_dir == "west":
			left = "south"
			right = "north"

		return left, right

	def create_path(self, first_room, last_exit_dir):

		current_room = first_room
		current_dir_num = 0
		straight_path_attempts = 0

		# if the instance max_size for rooms is met, stop creating the path
		while self.current_size < self.total_rooms_on_path:

			print(f"PROCGEN | CREATE_EXIT | From room: [{current_room.coordinates['x']}, {current_room.coordinates['y']}]")

			# establish variables
			self.current_size += 1
			straight_path_attempts += 1
			available_exits = copy.deepcopy(self.exit_types)
			attempts = 0
			path_finished = False
			straight_path_amt = random.randint(1,4)

			if attempts > 3:
				print("Attempted 3, stopping.")
				break

			# create a new room object for the next room in the path
			new_room = self.create_room()				

			# start loop to alter exit to new location
			coords_valid = False

			while coords_valid == False:

				if attempts < 3:

					# to reduce blocky paths
					if straight_path_attempts > straight_path_amt:

						straight_path_attempts = 0

						die_roll = random.randint(1,10)

						if die_roll == 1 or die_roll == 10:
							exit_dir = last_exit_dir
							print(f"PROCGEN | Continuing straight, roll: {die_roll}.")
						else:
							# since we are now not going to go straight, randomly choose
							# left or right based on the last direction
							left, right = self.get_left_right(last_exit_dir)
							exit_dir = random.choice([left, right])
							print(f"PROCGEN | Turning {exit_dir}.")

					else:

						print(f"PROCGEN | Continuing straight, s_path < 3.")
						exit_dir = last_exit_dir
			

					new_room.coordinates = copy.deepcopy(current_room.coordinates)

					print(f"PROCGEN | Current_room coords: [{current_room.coordinates['x']}, {current_room.coordinates['x']}] given to new_room [{new_room.coordinates['x']}, {new_room.coordinates['x']}].")
						
					if exit_dir == "north":
						opp_exit = "south"
						new_room.coordinates['y'] = new_room.coordinates['y'] - 1
					elif exit_dir == "south":
						opp_exit = "north"
						new_room.coordinates['y'] = new_room.coordinates['y'] + 1
					elif exit_dir == "east":
						opp_exit = "west"
						new_room.coordinates['x'] = new_room.coordinates['x'] + 1
					elif exit_dir == "west":
						opp_exit = "east"
						new_room.coordinates['x'] = new_room.coordinates['x'] - 1
					elif exit_dir == "up":
						opp_exit = "down"
						new_room.coordinates['z'] = new_room.coordinates['z'] + 1
					elif exit_dir == "down":
						opp_exit = "up"
						new_room.coordinates['z'] = new_room.coordinates['z'] - 1

					print(f"PROCGEN | Attempting exit going {exit_dir} to [{new_room.coordinates['x']}, {new_room.coordinates['y']}]")

					attempts += 1
					coords_valid = True

					for i in self.instance:

						if new_room.coordinates == i.coordinates:
							print("PROCGEN | Rooms exists, random change.")
							coords_valid = False
							current_room = random.choice(self.instance)
							break
				else:
					print("Attempted 3, stopping. 2")
					# random_room = random.choice(self.instance)
					# self.create_path(random_room, last_exit_dir)
					break

			if coords_valid == True:
				current_room.exits[exit_dir] = new_room.uuid_id
				new_room.exits[opp_exit] = current_room.uuid_id

				self.instance.append(new_room)
				rooms[new_room.uuid_id] = new_room

				current_room = new_room
			
			last_exit_dir = exit_dir


			print("PROCGEN | FINISHED EXIT")
			print("")
		
		else:

			print(f"PROCGEN | Current_size: {self.current_size} is equal to total_rooms_on_path: {self.total_rooms_on_path}")
		

	def create_exit(self, new_room, current_room):

		pass

	def random_exit_gen(self):
		
		exits = ['north', 'south', 'east', 'west']

	def create_room(self):

		# choose random room from appropriate region template,
		# create a room, and add it to the instance list

		template = self.region

		for i in room_regions:
			if template == room_regions[i]['name']:
				template = room_regions[i]['template']
			else:
				template = None
				print("PROCGEN | Create Room | Error: Can't find the template.")

		if template != None:

			choice = random.choice(template)

			# room_uuid_id = uuid.uuid4()
			# print("create_room test:", room_uuid_id)

			created_room = Room(
				uuid_id =      str(uuid.uuid4()),
			    entity_type =  choice['entity_type'],
			    ship_id =      choice['ship_id'],
			    coordinates =  {'x': None, 'y': None},
			    name =         choice['name'],
			    description =  choice['description'],
			    exits =        {},
			    region =       self.region,
			    zone =         self.zone,
			    elevation =    choice['elevation'],
			    effects =      choice['effects'],
			    player_inv =   [],
			    item_inv =     [],
			    npc_inv =      [],
			    mob_inv =      [],
			    owner =        choice['owner']
	        )

			# add the room to the global room list
			rooms[created_room.uuid_id] = created_room
			
			return created_room