import time, random

from pprint import pprint

from engine.global_lists import *
from engine.global_config import *
from engine.sched_mgr.sched_mgr import Sched_Child

from engine.npc import Npc
from engine.character import Character
from engine.suits.suit import TacSuit

class MainLoop():

	def __init__(self):
		pass

	def main_loop_all():
		
		s.eventabs(time.time() + 1, 1, "main_loop", "loop", MainLoop.main_loop_all, kwargs={})
		# s.enterabs(time.time() + .5, 1, MainLoop.main_loop_all, kwargs={})

		MainLoop.npc_player_same_room()
		
		for i in all_schedules:

			# print("MAIN LOOP | Events:", all_schedules[i]['obj'].name, all_schedules[i]['sched'].event_names)
			# print(all_schedules)

			MainLoop.check_vitals(all_schedules[i]['obj'])

			if all_schedules[i]['sched'].empty():
				pass
			
			elif all_schedules[i]['obj'].conditions['state'] == "sleep":
				pass
			
			else:
				all_schedules[i]['sched'].run(blocking=False)
			
		# print("")

	def initial_sched_check(self):
		pass

	def check_vitals(self):
		
		sched_name = self.uuid_id

		if self.vitals['hp_current'] <= 0:

			self.vitals['alive'] = False
			self.conditions['state'] = "sleep"
			self.conditions['stance'] = "lying"
			self.conditions['action'] = None
			self.conditions['round_time'] = 0
			self.conditions['round_time_init'] = 0
			all_schedules[self.uuid_id]['sched'].event_names = {}

		else:

			if self.entity_type['base'] == 'player':
				if self.player_state == "online":
				
					if self.vitals['hp_current'] < self.vitals['hp_max']:
						self.hp_regen()

		# check suit shield status
		if self.inventory['suit']['contents'] != None:
			TacSuit.suit_shield_regen(self)


	def npc_player_same_room():

		rand_die = random.randint(4, 10)

		for room in rooms:

			if rooms[room].player_inv == []:
				pass
			else:

				for npc in rooms[room].npc_inv:
					if npc.vitals['alive'] == False:
						pass
					else:
						npc.conditions['state'] = "engaged"

						if all_schedules[npc.uuid_id]['sched'].empty():	
							all_schedules[npc.uuid_id]['sched'].eventabs(time.time() + rand_die, 1, "npc_assess", "npc", Npc.npc_assess, kwargs={"self": npc})
						else:
							pass

						# all_schedules[npc.uuid_id]['sched'].enterabs(time.time() + 1, 1, Npc.npc_assess, kwargs={"self": npc})
						# Npc.npc_assess(npc)