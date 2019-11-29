from engine.global_config import *
# from websocket_server.websocket_server import WebsocketServer
import datetime

class WsWrap():
	
	def init(self):
		pass

	def ws_send(self, send_kwargs, msg):
		
		timestamp = datetime.datetime.now()
		# print("LOG | WS |", timestamp, ":", "ID:", self['id'], "|", "IP:", self['address'], "|", send_kwargs)
		# if self['obj'].entity_type['base'] == "player":
		# 	print("LOG | WS |", "Name:", self['obj'].name, "| UUID_ID:", self['obj'].uuid_id)
		# print("LOG | WS |", "ws_send msg:", msg)
		# print("")

		server.send_message(self, send_kwargs, msg)

		if send_kwargs['type'] == "text":
			if send_kwargs['spacing'] == 1:
				server.send_message(self, send_kwargs, "")
					

	def ws_send_group(self, send_kwargs, msg):

		timestamp = datetime.datetime.now()
		# print("LOG | WSGRP |", timestamp, ":", "ID:", self['id'], "|", "IP:", self['address'])
		# if self['obj'].entity_type['base'] == "player":
		# 	print("LOG | WSGRP |", "| Name:", self['obj'].name, "| UUID_ID:", self['obj'].uuid_id)
		# print("LOG | WSGRP", "ws_send_dict msg:", msg)
		# print("")

		for line in msg:
			server.send_message(self, send_kwargs, line)

		self['output_buffer'] = []

		server.send_message(self, send_kwargs, "")

	def ws_send_to_all(self, msg):

		server.send_message_to_all(self, msg)

		server.send_message_to_all(self, "")