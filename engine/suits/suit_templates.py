
### SUIT TEMPLATES
alpha_suit_table = {
	
	"rabbit":	{
		"static_stats": {"visible": True},
		"vitals": {"shield_max_base": 100, "shield_max_current": 100, "shield_base": 100, "shield_current": 100, "shield_regen_base": 1, "shield_regen_current": 1},
		"entity_type": {"base": "item", "group": "armor", "model": "tac_suit", "sub_model": "rabbit"},
		"name": "Rabbit tactical suit",
		"keyword": "suit",
		"item_desc": "It's a Rabbit tactical suit.",
		"size": "light",
		"weight": 100,
		"capacity": 0,
		"combines_with": [],
		"worn": "suit",
		"armor"				: 100,
		"hard_points"		: {1: {}, 2: {}},
		"augments"			: {1: {}},
		"location_body"		: {"state": "not_worn", "location": None},
		"compartments" 		: {
			"ammo" 	: {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "ammo"
				},

			"medical" : {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "medical"
				},

			"thigh_holster" : {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "weapon"
				},
		}

	},
	"falcon":	{
		"static_stats": {"shield_max": 100, "shield_current": 100, "visible": True},
		"entity_type": {"base": "item", "group": "armor", "model": "tac_suit", "sub_model": "rabbit"},
		"name": "a Rabbit tactical suit",
		"keyword": "suit",
		"item_desc": "It's a Rabbit tactical suit.",
		"size": "light",
		"weight": 100,
		"capacity": 0,
		"combines_with": [],
		"worn": "suit",
		"armor"				: 100,
		"hard_points"		: {1: {}, 2: {}},
		"augments"			: {1: {}},
		"location_body"		: "suit",
		"compartments" 		: {
			"ammo" 	: {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "ammo"
				},

			"medical" : {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "medical"
				},

			"thigh_holster" : {
				"inv" 		: {},
				"capacity" 	: 2,
				"type" 		: "weapon"
				},
		}

	},
	
}