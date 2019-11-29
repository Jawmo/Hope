
npc_table = {

	## PLANET OXINE

	"giant oxineworm": {
		"entity_type": {"base": "npc", "group": "giant_worm", "model": None, "sub_model": None},
		"vitals": {"hp_max": 100, "hp_current": 100, "hp_mod": 0, "hp_regen": 10, "hp_regen_mod": 0, "alive": True},
		"core_attributes": {"str": {"base": 8, "mod": 0}, "dex": {"base": 10, "mod": 0}, "con": {"base": 8, "mod": 0}, "ins": {"base": 12, "mod": 0}, "edu": {"base": 10, "mod": 0}, "soc": {"base": 10, "mod": 0}, "xp": {"current": 0, "buffer": 0, "absorp_rate_percent": 1}},
		"conditions": {"stance": "standing", "action": "None", "state": "sleep", "round_time": 0},
		"credit": {"credit": 100},
		"description": {"name": "giant oxineworm", "gender": "neutral", "desc": "He looks busy. Maybe you shouldn't bother him.", "race": "insectoid"},
		"npc_state": {},
		"supply": {},
		"demand": {},
		"home_loc": "oxine",
		"demeanor": "aggressive"
		},

	"guard": {
		"entity_type": {"base": "npc", "group": "human", "model": "guard", "sub_model": "hope_guard"},
		"vitals": {"hp_max": 100, "hp_current": 100, "hp_mod": 0, "hp_regen": 10, "hp_regen_mod": 0, "alive": True},
		"core_attributes": {"str": {"base": 8, "mod": 0}, "dex": {"base": 10, "mod": 0}, "con": {"base": 8, "mod": 0}, "ins": {"base": 12, "mod": 0}, "edu": {"base": 10, "mod": 0}, "soc": {"base": 10, "mod": 0}, "xp": {"current": 0, "buffer": 0, "absorp_rate_percent": 1}},
		"conditions": {"stance": "standing", "action": "None", "state": "sleep", "round_time": 0},
		"credit": {"credit": 100},
		"description": {"name": "Lt. Dan", "gender": "male", "desc": "He looks busy. Maybe you shouldn't bother him.", "race": "human"},
		"npc_state": {},
		"supply": {},
		"demand": {},
		"home_loc": "ship_hope",
		"demeanor": "friendly"
		},

	"predator": {
		"entity_type": {"base": "npc", "group": "predator", "model": None, "sub_model": None},		
		"vitals": {"hp_max": 100, "hp_current": 100, "hp_mod": 0, "hp_regen": 10, "hp_regen_mod": 0, "alive": True},
		"core_attributes": {"str": {"base": 8, "mod": 0}, "dex": {"base": 10, "mod": 0}, "con": {"base": 8, "mod": 0}, "ins": {"base": 12, "mod": 0}, "edu": {"base": 10, "mod": 0}, "soc": {"base": 10, "mod": 0}, "xp": {"current": 0, "buffer": 0, "absorp_rate_percent": 1}},
		"conditions": {"stance": "standing", "action": "None", "state": "sleep", "round_time": 0},
		"credit": {"credit": 100},
		"description": {"name": "predator", "gender": "neutral", "desc": "Gross.", "race": "oxinate"},
		"npc_state": {},
		"supply": {},
		"demand": {},
		"home_loc": "oxine",
		"demeanor": "aggressive"
		}
}