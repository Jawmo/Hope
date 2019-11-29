from engine.global_config import *

from engine.lex import Lex

from engine.items.guns.assault_rifle import Assault_Rifle

from engine.join_tables.join_table_items import *
from engine.suits.suit_templates import alpha_suit_table

class Assault_Rifle_Energy(Assault_Rifle):

	def __init__(self, **kwargs):
		
		super().__init__(**kwargs)

	def animation_load(self, user, user_input, input_kwargs):
		print(user.inventory)

		first_person = "You side-load {} into your {} and it immediately spins up, humming with energy.".format(Lex.a_an(user.inventory['l_hand']['contents'].name), user.inventory['r_hand']['contents'].name)
		target_person = ""
		third_person = "{} side-loads {} into {} {}.".format(user.name, Lex.a_an(user.inventory['l_hand']['contents'].name), Lex.gender(user, "own"), Lex.a_an(user.inventory['r_hand']['contents'].name))

		return first_person, target_person, third_person