from engine.global_config import *

from engine.lex import Lex

from engine.items.guns.pistol import Pistol

from engine.join_tables.join_table_items import *
from engine.suits.suit_templates import alpha_suit_table

class Pistol_9mm(Pistol):

	def __init__(self, **kwargs):
		
		super().__init__(**kwargs)

	def animation_load(self, user, user_input, input_kwargs):

		first_person = "You easily slide the magazine into your {}.".format(self.name)
		target_person = "{} slides a magazine into {} {}.".format(user.name, Lex.gender(user, "own"), self.name)
		third_person = "{} slides a magazine into {} {}.".format(user.name, Lex.gender(user, "own"), self.name)

		return first_person, target_person, third_person