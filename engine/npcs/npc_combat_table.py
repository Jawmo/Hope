
from engine.combat.combat_main import Combat
	
	## 2d6 rolling table used to determine the action of NPCs. Peak of the curve occurs at a roll of 7
	## while the tails of the curve occur towards 2 and 12. These occur less frequently.

	# Example:

	## name of the NPC
	# "predator": {

	## 
	# 	"12": 	{"fire_super", func},
	
	# 	"11": 	{"fire_special", func},
	
	# 	"10": 	{"maneuver", func},
	
	# 	"9": 	{"block_exit", func},
	
	## NPC will assess he situation. Based on number of players in the room, number of allies, 
	## current health, and player strength
	# 	"8": 	{"assess": func},
	
	## NPC will fire at a target, 95% of the time will be a player but can also attack another NPC
	# 	"7": 	{"fire": func},
	
	# 	"6": 	{"fire", func},
	
	# 	"5": 	{"fire", func},
	
	# 	"4": 	{"fire", func},
	
	# 	"3": 	{"fire", func},
	
	# 	"2": 	{"fire", func},
	
	# 	# 1 cannot occur with two dice rolls
	
	# 	},

hit_table = {
		1: 	{"base": 100, "mod": 0},
		2: 	{"base": 100, "mod": 0},
		3: 	{"base": 100, "mod": 0},
		4: 	{"base": 100, "mod": 0},
		5: 	{"base": 100, "mod": 0},
		6: 	{"base": 100, "mod": 0},
		7: 	{"base": 100, "mod": 0},
		8: 	{"base": 100, "mod": 0},
		9: 	{"base": 100, "mod": 0},
		10: {"base": 100, "mod": .1},
		11: {"base": 100, "mod": .3},
		12: {"base": 100, "mod": .5},
		13: {"base": 100, "mod": .7},
		14: {"base": 100, "mod": .15}
}

npc_combat_table = {

	########
	## Oxine

	"predator": {
		1: 	{"name": "fire", "func": Combat.attack},
		2: 	{"name": "fire", "func": Combat.attack},
		3: 	{"name": "fire", "func": Combat.attack},
		4: 	{"name": "fire", "func": Combat.attack},
		5: 	{"name": "fire", "func": Combat.attack},
		6: 	{"name": "fire", "func": Combat.attack}
		# 1 cannot occur with two dice rolls
		},

}