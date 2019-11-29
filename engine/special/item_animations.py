from engine.lex import *

class Item_Animations():
	def __init__():
		pass

	def wear_animation(self, user_input, input_kwargs):
	
		if input_kwargs['target'].worn == "back":
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'You sling {} on to your back.'.format(Lex.a_an(input_kwargs['target'].name)),
				target_person = "",
				third_person = '{} slings {} on to {} back.'.format(self.name, Lex.a_an(input_kwargs['target'].name), Lex.gender(self, "own")))
		else:
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'You put on {}.'.format(Lex.a_an(input_kwargs['target'].name)),
				target_person = "",
				third_person = '{} puts on {}.'.format(self.name, Lex.a_an(input_kwargs['target'].name)))

	def remove_animation(self, user_input, input_kwargs):
	
		if input_kwargs['target'].worn == "back":
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'You pull {} down off your back.'.format(Lex.a_an(input_kwargs['target'].name)),
				target_person = "",
				third_person = '{} pulls {} down off {} back.'.format(self.name, Lex.a_an(input_kwargs['target'].name), Lex.gender(self, "own")))
		else:
			Lex.pub_print(
				self=self,
				target=input_kwargs['target'],
				send_kwargs={'type': 'text', 'spacing': 1},
				first_person = 'You remove {}.'.format(Lex.a_an(input_kwargs['target'].name)),
				target_person = "",
				third_person = '{} removes {}.'.format(self.name, Lex.a_an(input_kwargs['target'].name)))