from engine.global_config import *

from engine.lex import Lex

from engine.items.gun import Gun

from engine.join_tables.join_table_items import *
from engine.suits.suit_templates import alpha_suit_table

class Assault_Rifle(Gun):

	def __init__(self, **kwargs):
		
		super().__init__(**kwargs)

	def animation_load(self, user, user_input, input_kwargs):

		pass