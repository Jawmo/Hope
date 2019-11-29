import json, logging

from engine.global_config import *
from engine.parser.parser import Input_Parser

from engine.start import start
from engine.audio import initialize_sounds, Recurring_BG
from engine.initial.check_user import check_user

from engine.update_client import Update_Client
from engine.command_list import all_commands
from websocket_server.wswrap import WsWrap
from engine.lex import Lex
from engine.db_commands import update_db_item, update_db_player


# Called for every client connecting (after handshake)
def new_client(client, server):

	client['reg'] = 'logged_out'
	client['type'] = 'guest'
	client['uuid_id'] = None
	client['guest_progress'] = "name_input"

# Called for every client disconnecting
def client_left(client, server):

	# client['obj'].conditions['schedule'] = {
	# 	'event_names': all_schedules[client['obj'].uuid_id]['sched'].event_names,
	# 	'event_types': all_schedules[client['obj'].uuid_id]['sched'].event_types
	# }
	
	# update_db_player(players[client['obj'].uuid_id])

	send_kwargs = {'type': 'text', 'spacing': 1}

	Lex.pub_print(
        self=client['obj'],
        target=None,
        send_kwargs={'type': 'text', 'spacing': 1},
        first_person = "",
        target_person = "",
        third_person = "{} just left.".format(client['obj'].name.capitalize()))

	logging.debug('%s %s', "LOG | Removing client:", client['obj'])
	logging.info("----------")
	print("LOG | Removing client:", client['obj'], "from room:", rooms[client['obj'].location].player_inv)
	
	players[client['obj'].uuid_id].player_state = "logged_out"
	rooms[client['obj'].location].player_inv.remove(client['obj'])

	# Update_Client.update_player_object(client['obj'])
	Update_Client.update_player_list(client['obj'])

# Called when a client sends a message / game loop parser
def message_received(client, server, message):

	send_kwargs = {'type': 'text', 'spacing': True}
	
	# WsWrap.ws_send(client, send_kwargs, "")

	# if client['token'] == None:
	# 	client['guest_progress'] = 'name_input'
	# 	user_id = message.replace('"', "")
	# 	print(username)
	# 	client['token'] = username

	if client['type'] == 'guest':

		# server.send_message(client, send_kwargs, "> {}".format(message))

		check_user(client, server, message)


	elif client['type'] == 'member_authenticated' or client['type'] == 'tourist':

		if client['obj'].conditions['echo'] == True:
			WsWrap.ws_send(client, {'type': 'text', 'spacing': 0}, "|repeat|> {}|repeatx|".format(message))

		logging.debug('%s %s %s', ":", client['obj'].name, client['obj'].uuid_id)
		logging.debug('%s %s', ":", message)

		input_kwargs = {}

		all_ok = True
		cmd_found = False
		cmd_help = None

		user_input = message.split()
		print("SERVER PY | Splitting Input:", user_input)

		if not user_input:
			WsWrap.ws_send(client, send_kwargs, "|alert|No input.|alertx|")

		else:

			speaking = Input_Parser.speech(client['obj'], user_input, input_kwargs)

			if speaking == False:

				cmd_input, params = Input_Parser.parse_input(user_input)

				print("SERVER PY | cmd_input:", cmd_input)
				print("SERVER PY | params:", params)
				print("SERVER PY | user_input:", user_input)

				print("PARSE | inp matching command:", user_input)

				# input_kwargs['target'] = Input_Handler.full_handler(client['obj'], user_input, params)
				
				# try:

				T3_CMD = Lex.first_three(cmd_input)

				for i in all_commands:

					for hotkey in all_commands[i]['hotkey']:

						if user_input[0] == hotkey:
							cmd_found = True

							if all_commands[i]['requirements']:
								for func in all_commands[i]['requirements']:
									input_kwargs['cmd_name'] = i
									input_kwargs['cmd_req'] = all_commands[i]['requirements'][func]['req']
									
									if 'help' in all_commands[i]:
										cmd_help = all_commands[i]['help']


									status, response = all_commands[i]['requirements'][func]['func'](client['obj'], user_input, input_kwargs)
									input_kwargs['status'] = status
									input_kwargs['response'] = response


									if input_kwargs['status'] == False:
										if response != None:											
											WsWrap.ws_send(client, {'type': 'text', 'spacing': 1}, "{}".format(response))
											all_ok = False
											break

								# cmd_help
								if client['obj'].conditions['help'] == "enabled":
									if cmd_help != None:
										WsWrap.ws_send(client, {'type': 'text', 'spacing': 1}, "{}".format(cmd_help))

							if all_ok == True:

								if all_commands[i]["need_com_name"] == "yes":
									all_commands[i]["func"](client['obj'], user_input, all_commands[i]["name"])
									break

								elif all_commands[i]["need_com_input"] == "yes":
									all_commands[i]["func"](client['obj'], user_input, input_kwargs)
									break

								else:
									all_commands[i]["func"](client['obj'])
									break

				if cmd_found == False:
					WsWrap.ws_send(client, {'type': 'text', 'spacing': 1}, "Hmm?")

				logging.info("----------")

				# except:
				# 	print("LOG | SERVERTWO | Error:", cmd_input)
				# 	send_kwargs = {'type': 'text', 'spacing': False}
				# 	WsWrap.ws_send(client, send_kwargs, "|alert|Error (MAIN). Please contact your Admin.|alertx|")

		# WsWrap.ws_send(client, send_kwargs, "")
		
		