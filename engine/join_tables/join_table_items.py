
item_table = {

	# size = 1-7
	# xxs, xs, s, m, l , xl, xxl

	## SUIT DEFAULT
	"rabbit": {
		"vitals": {"shield_max_base": 100, "shield_max_current": 100, "shield_base": 100, "shield_current": 100, "shield_regen_base": 5, "shield_regen_current": 5},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "armor", "model": "tac_suit", "sub_model": "rabbit"},
		"size": "light",
		"weight": 100,
		"capacity": 0,
		"combines_with": [],
		"worn": "suit",
		},

	## DOORS

	"door_ship_invisible": {
		"vitals": {},
		"static_stats": {"visible": False},
		"entity_type": {"base": "item", "group": "environment", "model": "door", "sub_model": None},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": [],
		"worn": None
		},

	"door_ship_visible": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "environment", "model": "door", "sub_model": None},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": [],
		"worn": None
		},

	## BALLISTIC WEAPONS

	"pistol_9mm": {
		"vitals": {},
		"static_stats": {"str_base": 3, "str_mod": 0,
						 "dex_base": 5, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "gun", "model": "pistol", "sub_model": "pistol_9mm"},
		"size": 3,
		"weight": 5,
		"capacity": 10,
		"combines_with": ["ammo_ballistic_9mm"],
		"worn": None
		},

	"pistol_9mm_generator": {
		"vitals": {},
		"static_stats": {"str_base": 3, "str_mod": 0,
						 "dex_base": 5, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": False},
		"entity_type": {"base": "item", "group": "gun", "model": "pistol", "sub_model": "pistol_9mm"},
		"size": 3,
		"weight": 5,
		"capacity": 10,
		"combines_with": ["ammo_ballistic_9mm"],
		"worn": None
		},

	"ammo_9mm":	{
		"vitals": {},
		"static_stats": {"str_base": 1, "str_mod": 0,
						 "dex_base": 2, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "ammo", "model": "ammo_ballistic", "sub_model": "ammo_ballistic_9mm"},
		"size": 1,
		"weight": 1,
		"capacity": 10,
		"combines_with": ["pistol_9mm"],
		"worn": None
		},

	"ammo_9mm_generator":	{
		"vitals": {},
		"static_stats": {"str_base": 1, "str_mod": 0,
						 "dex_base": 2, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "ammo", "model": "ammo_ballistic", "sub_model": "ammo_ballistic_9mm"},
		"size": 1,
		"weight": 1,
		"capacity": 10,
		"combines_with": ["pistol_9mm"],
		"worn": None
		},

	## ENERGY WEAPONS

	"assault_rifle_energy": {
		"vitals": {},
		"static_stats": {"str_base": 5, "str_mod": 0,
						 "dex_base": 5, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "gun", "model": "assault_rifle", "sub_model": "assault_rifle_energy"},
		"size": 3,
		"weight": 5,
		"capacity": 10,
		"combines_with": ["ammo_energy_disc"],
		"worn": None
		},

	"assault_rifle_energy_generator": {
		"vitals": {},
		"static_stats": {"str_base": 5, "str_mod": 0,
						 "dex_base": 5, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "gun", "model": "assault_rifle", "sub_model": "assault_rifle_energy"},
		"size": 3,
		"weight": 5,
		"capacity": 10,
		"combines_with": ["ammo_energy_disc"],
		"worn": None
		},

	"ammo_energy":	{
		"vitals": {},
		"static_stats": {"str_base": 2, "str_mod": 0,
						 "dex_base": 2, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": True},
		"entity_type": {"base": "item", "group": "ammo", "model": "ammo_energy", "sub_model": "ammo_energy_disc"},
		"size": 1,
		"weight": 1,
		"capacity": 10,
		"combines_with": ["assault_rifle_energy"],
		"worn": None
		},

	"ammo_energy_generator":	{
		"vitals": {},
		"static_stats": {"str_base": 2, "str_mod": 0,
						 "dex_base": 2, "dex_mod": 0, 
						 "con_base": 0, "con_mod": 0, 
						 "ins_base": 0, "ins_mod": 0, 
						 "edu_base": 0, "edu_mod": 0, 
						 "soc_base": 0, "soc_mod": 0,
						 "visible": False},
		"entity_type": {"base": "item", "group": "ammo", "model": "ammo_energy", "sub_model": "ammo_energy_disc"},
		"size": 1,
		"weight": 1,
		"capacity": 10,
		"combines_with": ["assault_rifle_energy"],
		"worn": None
		},

	## NATURAL
	
	"sinkhole": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "environment", "model": "hole", "sub_model": "vertical"},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	"hole_vertical": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "environment", "model": "hole", "sub_model": "vertical"},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	"wall": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "environment", "model": "wall", "sub_model": None},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	## COMMUNICATORS

	"communicator": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "communicator", "model": None, "sub_model": None},
		"size": 1,
		"weight": 1,
		"capacity": 1,
		"combines_with": "",
		"worn": "wrist"
		},

	"battery": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "battery", "model": "comm_battery", "sub_model": None},
		"size": 1,
		"weight": 1,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	## CONTAINERS

	"backpack": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "container", "model": "backpack", "sub_model": None},
		"size": 1,
		"weight": 1,
		"capacity": 10,
		"combines_with": "",
		"worn": "back"
		},

	## INDOOR

	"case": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "container", "model": "case", "sub_model": None},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": ""
		},


	## SHIPS

	"ship_capital_hope": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "ship", "model": "capital", "sub_model": "hope"},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	"ship_capital": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "ship", "model": "capital", "sub_model": "other"},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	"ship_personal": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "ship", "model": "personal", "sub_model": None},
		"size": 0,
		"weight": 0,
		"capacity": 0,
		"combines_with": "",
		"worn": None
		},

	## SUITS

	"suit_combat": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "suit", "model": "combat", "sub_model": "rabbit"},
		"size": 2,
		"weight": 2,
		"capacity": 10,
		"combines_with": "",
		"worn": "suit"
		},

	## MISC

	"toy": {
		"vitals": {},
		"static_stats": {"visible": True},
		"entity_type": {"base": "item", "group": "misc", "model": "toy", "sub_model": None},
		"size": 2,
		"weight": 2,
		"capacity": 10,
		"combines_with": "",
		"worn": None
		},

}