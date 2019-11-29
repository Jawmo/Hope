import sched, time

from engine.global_lists import *
from engine.global_config import *


class Sched_Child(sched.scheduler):
	
	def __init__(self, timefunc, delayfunc):
		
		super().__init__(timefunc, delayfunc)

		self.event_names = {}
		self.event_types = {}

	def create_new_sched(self):

		sched_name = self.uuid_id

		all_schedules[sched_name] = {'sched': Sched_Child(time.time, time.sleep), 'obj': self}

	def eventabs(self, time, priority, event_name, event_type, action, *argument, **kwargs):

		# print("EVENT | Creating event of name:", event_name, "and type:", event_type)

		event = self.enterabs(time, priority, action, *argument, **kwargs)
		
		if self.event_names and self.event_types:
			
			if event_name in self.event_names:
				pass
			else:	
				self.event_names[event_name].append(event)
				# self.event_types[event_type].append(event)
		else:
			self.event_names[event_name] = list(event)
			self.event_types[event_type] = list(event)

	def remove_event_name(self, event_name, event_type):

		if event_name in self.event_names:
			self.event_names.pop(event_name)
				