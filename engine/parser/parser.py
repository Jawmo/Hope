from engine.command_list import *

class Input_Parser():
	def __init__():
		pass

	def speech(self, user_input, input_kwargs):

		if user_input[0][0] == "'" or user_input[0] == "say":

			sentence = []
			speaking = True

			print("PARSE-SAY | Pre Speak UI:", user_input)

			if user_input[0] == "'" or user_input[0] == "say":
				pass
			else:
				say_cmd = user_input[0][0]
				user_input[0] = user_input[0][1:]
				user_input.insert(0, say_cmd)

			all_commands["'"]["func"](self, user_input, input_kwargs)

		else:
			speaking = False

		return speaking

	def parse_input(user_input):

		cmd_input = user_input[0]
		params = user_input[1:]

		return cmd_input, params