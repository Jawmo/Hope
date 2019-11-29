from engine.global_config import *
# from engine.global_config2 import *
# from websocket_server import WebsocketServer
from engine.lex import Lex
from engine.room import Room
from engine.gen import Gen
from engine.item import Item

from websocket_server.wswrap import WsWrap

from world.universe import *

class Ship(Item):

	def __init__(self, **kwargs):
		pass

		super().__init__(**kwargs)

	def voice_command(self, user, user_input, input_kwargs):

		for cmd_entry in ship_ai_cmds:
	
			if user_input[2] == cmd_entry:

				cmd = ship_ai_cmds[cmd_entry]
	
				ship_ai_cmds[cmd_entry]['cmd_run'](self, user_input, input_kwargs)
	
				break

		else:
			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = "That didn't work.",
				target_person = "",
				third_person = "")

	def open_door(self, user_input, input_kwargs):

		room_obj_outside_of_ship = rooms[items[input_kwargs['ship_id']].location]

		if items[input_kwargs['ship_id']].is_open == True:
			
			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'comp| "The door is already open." |/comp|',
				target_person = "",
				third_person = '|comp| "The door is already open." |/comp|')

		if items[input_kwargs['ship_id']].is_open == False:
			
			items[input_kwargs['ship_id']].is_open = True
			
			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'The ship door opens with a *whoosh*.',
				target_person = "",
				third_person = 'The ship door opens with a *whoosh*.')


		for i in room_obj_outside_of_ship.player_inv:
			WsWrap.ws_send(i.client, {'type': 'text', 'spacing': 1}, "A ship door closes with a *whoosh*.")

		items[input_kwargs['ship_id']].is_open = True
		rooms[self.location].exits = {"out": input_kwargs['room_of_ship'].uuid_id}


	def close_door(self, user_input, input_kwargs):

		room_obj_outside_of_ship = rooms[items[input_kwargs['ship_id']].location]

		if items[input_kwargs['ship_id']].is_open == False:
			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'comp| "The door is already closed." |/comp|',
				target_person = "",
				third_person = '|comp| "The door is already closed." |/comp|')

			# all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
			# 	   'target': None,
			# 	   'send_kwargs': {'type': 'text', 'spacing': 1},
			# 	   'first_person': '|comp|"The door is already closed."|/comp|',
			# 	   'target_person': '',
			# 	   'third_person': '|comp|"The door is already closed."|/comp|'})

		if items[input_kwargs['ship_id']].is_open == True:

			items[input_kwargs['ship_id']].is_open = False
			
			Lex.pub_print(
				self=self,
				target=None,
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'The ship door closes with a *whoosh*.',
				target_person = "",
				third_person = 'The ship door closes with a *whoosh*.')

			for i in room_obj_outside_of_ship.player_inv:
				WsWrap.ws_send(i.client, {'type': 'text', 'spacing': 1}, "A ship door closes with a *whoosh*.")

			items[input_kwargs['ship_id']].is_open = False
			rooms[self.location].exits = {}

		# Lex.pub_print_outside(
		# 	kwargs={
		# 		'target_room': input_kwargs['room_of_ship'], 
		# 		'msg': 'A shuttle door closes with a *whoosh*.'})

	def takeoff(self, user_input, input_kwargs):

		# print(room_of_ship.name)	

		if room_of_ship.entity_type['group'] != "planet_landing" and "_dock" not in room_of_ship.entity_type['group']:
			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				   'target': None,
				   'first_person': '|comp|"This it not suitable place to do that."|/comp|'.format(self.name),
				   'target_person': '',
				   'third_person': '|comp|"This it not suitable place to do that."|/comp|'.format(self.name)})
		else:

			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
					   'target': None,
					   'first_person': '|comp|"Confirmed, standby for takeoff."|/comp|',
					   'target_person': '',
					   'third_person': '|comp|"Confirmed, standby for takeoff."|/comp|'})

				# close the ship if it is open
			if items[ship_id].is_open == True:
				items[ship_id].is_open = False

				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 2, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
					   'target': None,
					   'first_person': 'The ship door closes with a *whoosh*.',
					   'target_person': '',
					   'third_person': 'The ship door closes with a *whoosh*.'})

			# remove the ship from the item_inventory of the room it was in
			room_of_ship.item_inv.remove(items[ship_id])
			# remove exits from the ship room
			rooms[self.location].exits = {}
			# make the ship's location None
			items[ship_id].location = "pp2aa543-ab72-93n1-c93c-1f4803ceefd0"

			if "_dock" in room_of_ship.entity_type['group']:
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': None,
						   'first_person': '|comp|"Exiting docking bay."|/comp|',
						   'target_person': '',
						   'third_person': '|comp|"Exiting docking bay."|/comp|'})

			elif "_landing" in room_of_ship.entity_type['group']:
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': None,
						   'first_person': 'The ships core ignites and you feel a gentle change in pressure as it lifts from the ground. You pass through layers of the atmosphere before the ship enters into orbit.',
						   'target_person': '',
						   'third_person': 'The ships core ignites and you feel a gentle change in pressure as it lifts from the ground. You pass through layers of the atmosphere before the ship enters into orbit.'})

			# ship_list = Gen.ships_in_room(self)
			# for i in ship_list:
			# 	room_ship_list.append(i.name)

			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 5, 2, Ship.takeoff, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target']})

	def travel(self, user_input, input_kwargs):
			
		# check the planet dict for travel targets
		destination = None

		for planet in planets:
			if planet not in user_input:
				pass
			else:
				destination = planets[planet]["location"]
				d_type = "planet"
				break

		# check the ship dict for travel targets
		if destination == None:
			for ship in ships:
				if ship not in user_input:
					pass
				else:
					destination = ships[ship]["location"]
					d_type = "ship"
					break

		if destination == None:
			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, server.send_message, argument=(self.client, speech, 
					   'The computer replies, "That is not a valid destination."'))

		else: 
			print("Ship list:", room_ship_list)
			if destination == room_of_ship.uuid_id:
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, server.send_message, argument=(self.client, speech, 
					   	   f'|comp|"You are already here, {self.name}."|/comp|'))

			elif "planet_landing" == room_of_ship.entity_type['group']:
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, server.send_message, argument=(self.client, speech, 
					   	   '|comp|"You must first TAKEOFF."|/comp|'))
			
			elif ship.lower() in room_ship_list:
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': '|comp|"Confirmed, entering docking bay."|/comp|',
						   'target_person': '',
						   'third_person': '|comp|"Confirmed, entering docking bay."|/comp|'})
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': 'The ship navigate securely inside the docking bay.',
						   'target_person': '',
						   'third_person': 'The ship navigate securely inside the docking bay.'})
				
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, Ship.space_travel, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target'], 'destination': destination})

			else:
				
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 2, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': f'|comp|"Confirmed, setting course for {rooms[destination].region}."|/comp|',
						   'target_person': '',
						   'third_person': f'|comp|"Confirmed, setting course for {rooms[destination].region}."|/comp|'})
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 6, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': "Your hear the ship's core engage and the lights of the universe appear to bend as the ship enters warp.",
						   'target_person': '',
						   'third_person': "Your hear the ship's core engage and the lights of the universe appear to bend as the ship enters warp."})
				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 7, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': "The ship's core slows as you approach your destination.",
						   'target_person': '',
						   'third_person': "The ship's core slows as you approach your destination."})

				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 9, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
						   'target': input_kwargs['target'],
						   'send_kwargs': {'type': 'text', 'spacing': 1},
						   'first_person': f'|comp|"Welcome to {rooms[destination].region}, {rooms[destination].name}."|/comp|',
						   'target_person': '',
						   'third_person': f'|comp|"Welcome to {rooms[destination].region}, {rooms[destination].name}."|/comp|'})

				all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 9, 1, Ship.space_travel, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target'], 'destination': destination})




				# elif user_input[2] == "dock":
					
				# 	destination = None

				# 	# check the ship dict for travel targets
				# 	if destination == None:
				# 		for ship in ships:
				# 			if ship not in user_input:
				# 				pass
				# 			else:
				# 				destination = ships[ship]["location"]
				# 				d_type = "ship"
				# 				break

				# 	if destination == None:

				# 		all_schedules[self.uuid_id]['sched'].eventabs(
				# 			time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'first_person': '|comp|"That is not a valid location."|/comp|'.format(self.name),
				# 				   'target_person': '',
				# 				   'third_person': '|comp|"That is not a valid location."|/comp|'.format(self.name)})
				# 	else:

				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'first_person': '|comp|"Confirmed. Prepare for docking."|/comp|',
				# 				   'target_person': '',
				# 				   'third_person': '|comp|"Confirmed. Prepare for docking."|/comp|'})

				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'first_person': 'The ship begins to navigate towards its docking target.',
				# 				   'target_person': '',
				# 				   'third_person': 'The ship begins to navigate towards its docking target.'})

				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 6, 2, Ship.docking, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target'], 'destination': destination})


				# elif user_input[2] == "land":

				# 	if room_of_ship.entity_type['group'] != "space_orbit":
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': None,
				# 					   'first_person': '|comp|"You must be in a planets orbit."|/comp|'.format(self.name),
				# 					   'target_person': '',
				# 					   'third_person': '|comp|"You must be in a planets orbit."|/comp|'.format(self.name)})
				# 	else:
				# 		if not room_of_ship.exits:
				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': None,
				# 					   'first_person': '|comp|"There is no suitable place to land."|/comp|'.format(self.name),
				# 					   'target_person': '',
				# 					   'third_person': '|comp|"There is no suitable place to land."|/comp|'.format(self.name)})
				# 		else:

				# 			destination = room_of_ship.exits["entry"]

				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': None,
				# 					   'first_person': '|comp|"Confirmed. Ive found {} below suitable for landing. Prepare for entry."|/comp|'.format(Lex.a_an(rooms[destination].name.lower())),
				# 					   'target_person': '',
				# 					   'third_person': '|comp|"Confirmed. Ive found {} below suitable for landing. Prepare for entry."|/comp|'.format(Lex.a_an(rooms[destination].name.lower()))})
							
				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 5, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': Noneg,
				# 					   'first_person': 'The ship turns to descend down and begins to pass through {}s atmosphere. You can begin to make out {} below.'.format(
				# 				   	   	room_of_ship.region, Lex.a_an(rooms[destination].name.lower())),
				# 					   'target_person': '',
				# 					   'third_person': 'Your ship turns to descend down and begins to pass through {}s atmosphere. You can begin make out {} below.'.format(
				# 				   	   	room_of_ship.region, Lex.a_an(rooms[destination].name.lower()))})
							
				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 7, 2, Ship.atmos_entry, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target'], 'destination': destination})

				# elif user_input[2] == "takeoff":

				# 	print(room_of_ship.name)
				# 	if room_of_ship.entity_type['group'] != "planet_landing" and "_dock" not in room_of_ship.entity_type['group']:
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 			   'target': None,
				# 			   'first_person': '|comp|"This it not suitable place to do that."|/comp|'.format(self.name),
				# 			   'target_person': '',
				# 			   'third_person': '|comp|"This it not suitable place to do that."|/comp|'.format(self.name)})
				# 	else:

				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'first_person': '|comp|"Confirmed, standby for takeoff."|/comp|',
				# 				   'target_person': '',
				# 				   'third_person': '|comp|"Confirmed, standby for takeoff."|/comp|'})

				# 			# close the ship if it is open
				# 		if items[ship_id].is_open == True:
				# 			items[ship_id].is_open = False

				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 2, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'first_person': 'The ship door closes with a *whoosh*.',
				# 				   'target_person': '',
				# 				   'third_person': 'The ship door closes with a *whoosh*.'})

				# 		# remove the ship from the item_inventory of the room it was in
				# 		room_of_ship.item_inv.remove(items[ship_id])
				# 		# remove exits from the ship room
				# 		rooms[self.location].exits = {}
				# 		# make the ship's location None
				# 		items[ship_id].location = "pp2aa543-ab72-93n1-c93c-1f4803ceefd0"

				# 		if "_dock" in room_of_ship.entity_type['group']:
				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': None,
				# 					   'first_person': '|comp|"Exiting docking bay."|/comp|',
				# 					   'target_person': '',
				# 					   'third_person': '|comp|"Exiting docking bay."|/comp|'})

				# 		elif "_landing" in room_of_ship.entity_type['group']:
				# 			all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 3, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 					   'target': None,
				# 					   'first_person': 'The ships core ignites and you feel a gentle change in pressure as it lifts from the ground. You pass through layers of the atmosphere before the ship enters into orbit.',
				# 					   'target_person': '',
				# 					   'third_person': 'The ships core ignites and you feel a gentle change in pressure as it lifts from the ground. You pass through layers of the atmosphere before the ship enters into orbit.'})

				# 		# ship_list = Gen.ships_in_room(self)
				# 		# for i in ship_list:
				# 		# 	room_ship_list.append(i.name)

				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 5, 2, Ship.takeoff, kwargs={'self': self, 'user_input': user_input, "input_kwargs['target']": input_kwargs['target']})

				# elif user_input[2] == "open":

				# 	if items[ship_id].is_open == True:
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 				   'target': None,
				# 				   'send_kwargs': {'type': 'text', 'spacing': 1},
				# 				   'first_person': '|comp|"The door is already open."|/comp|',
				# 				   'target_person': '',
				# 				   'third_person': '|comp|"The door is already open."|/comp|'})

				# 	if items[ship_id].is_open == False:
				# 		items[ship_id].is_open = True
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 			   'target': None,
				# 			   'send_kwargs': {'type': 'text', 'spacing': 1},
				# 			   'first_person': 'The ship door opens with a *whoosh*.',
				# 			   'target_person': '',
				# 			   'third_person': 'The ship door opens with a *whoosh*.'})

				# 	all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print_outside, kwargs={'target_room': room_of_ship, 'msg': 'A shuttle door opens with a *whoosh*.'})

				# 	rooms[self.location].exits = {"out": room_of_ship.uuid_id}

				# elif user_input[2] == "close":

				# 	if items[ship_id].is_open == False:
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 			   'target': None,
				# 			   'send_kwargs': {'type': 'text', 'spacing': 1},
				# 			   'first_person': '|comp|"The door is already closed."|/comp|',
				# 			   'target_person': '',
				# 			   'third_person': '|comp|"The door is already closed."|/comp|'})

				# 	if items[ship_id].is_open == True:
				# 		items[ship_id].is_open = False
				# 		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				# 			   'target': None,
				# 			   'send_kwargs': {'type': 'text', 'spacing': 1},
				# 			   'first_person': 'The ship door closes with a *whoosh*.',
				# 			   'target_person': '',
				# 			   'third_person': 'The ship door closes with a *whoosh*.'})

				# 		rooms[self.location].exits = {}

				# 	all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print_outside, kwargs={'target_room': room_of_ship, 'msg': 'A shuttle door closes with a *whoosh*.'})

				# else:
				# 	server.send_message(self.client, speech, '|comp|"Command not recognized."|/comp|')

	def space_travel(self, user_input, input_kwargs, destination):
		
		ship_id = rooms[self.location].ship_id

		print("Ship_ID:", ship_id)
		print("Ship was in room:", items[ship_id].location)

		items[ship_id].location = destination
		rooms[destination].item_inv.append(items[ship_id])

		print("Ship now in room:", destination)
		print("Inv of this room:", rooms[destination].item_inv)

	def atmos_entry(self, user_input, input_kwargs, destination):
			
		ship_id = rooms[self.location].ship_id

		print("Ship_ID:", ship_id)
		print("Ship was in room:", items[ship_id].location)

		items[ship_id].location = destination
		rooms[destination].item_inv.append(items[ship_id])

		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				   'target': input_kwargs['target'],
				   'first_person': 'Your ship rocks gently as it touches down. Outside, you see {}. {}'.format(
	   	   							Lex.a_an(rooms[items[ship_id].location].name).lower(), rooms[items[ship_id].location].description),
				   'target_person': '',
				   'third_person': 'Your ship rocks gently as it touches down. Outside, you see {}. {}'.format(
	   	   							Lex.a_an(rooms[items[ship_id].location].name).lower(), rooms[items[ship_id].location].description)})

		print("Ship now in room:", destination)
		print("Inv of this room:", rooms[destination].item_inv)

	def docking(self, user_input, input_kwargs, destination):
			
		ship_id = rooms[self.location].ship_id

		print("Ship_ID:", ship_id)
		print("Ship was in room:", items[ship_id].location)

		items[ship_id].location = destination
		rooms[destination].item_inv.append(items[ship_id])

		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				   'target': input_kwargs['target'],
				   'first_person': 'The ship safely completes its docking. Outside, you see {}. {}'.format(
	   	   							Lex.a_an(rooms[items[ship_id].location].name).lower(), rooms[items[ship_id].location].description),
				   'target_person': '',
				   'third_person': 'The ship safely completes its docking. Outside, you see {}. {}'.format(
	   	   							Lex.a_an(rooms[items[ship_id].location].name).lower(), rooms[items[ship_id].location].description)})

		print("Ship now in room:", destination)
		print("Inv of this room:", rooms[destination].item_inv)

	def takeoff(self, user_input, input_kwargs):
			
		ship_id = rooms[self.location].ship_id
		room_of_ship = rooms[items[ship_id].location]

		print("Ship_ID:", ship_id)
		print("Ship was in room:", items[ship_id].location)

		items[ship_id].location = items["r23b4335-5o7k-4f52-92b8-56ad69f63bea"].location
		rooms[items["r23b4335-5o7k-4f52-92b8-56ad69f63bea"].location].item_inv.append(items[ship_id])

		room_ship_list = []
		ship_list = Gen.ships_in_room(self)
		for i in ship_list:
			room_ship_list.append(i.name)

		all_schedules[self.uuid_id]['sched'].eventabs(time.time() + 1, 1, "ship_ai", "print", Lex.pub_print, kwargs={'self': self,
				   'target': input_kwargs['target'],
				   'first_person': 'You reach open space. Outside, {} You also see {}.'.format(
	   	   							rooms[items[ship_id].location].description, ", ".join(room_ship_list)),
				   'target_person': '',
				   'third_person': 'You reach open space. Outside, {} You also see {}.'.format(
	   	   							rooms[items[ship_id].location].description, ", ".join(room_ship_list))})

		print("Ship now in room:", items[ship_id].location)
		print("Inv of this room:", rooms[items[ship_id].location].item_inv)


ship_ai_cmds = {
	
	"open": {
		
		"cmd_name"	:	"open",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.open_door},

	"close": {
		
		"cmd_name"	:	"close",
		"cmd_group"	:	"Ship AI",
		"cmd_run"	:	Ship.close_door}

}